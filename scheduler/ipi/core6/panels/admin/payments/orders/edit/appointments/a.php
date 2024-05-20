<?php
$order = ntsLib::getVar( 'admin/payments/orders/edit::OBJECT' );
$orderId = $order->getId();
$deps = $order->getItems();

$ids = array();
reset( $deps );
foreach( $deps as $dep )
{
	$className = $dep->getClassName();
	if( $className == 'appointment' )
	{
		$ids[] = $dep->getId();
	}
}

if( $ids ){
	$alias = 'admin/manage/agenda';
	ntsView::setBack( ntsLink::makeLink('admin/payments/orders/edit/appointments', '', array('_id' => $orderId)) );

	$period = 'all';
	ntsLib::setVar( 'admin/manage/agenda:period', $period );

	$cal = null;
	ntsLib::setVar( 'admin/manage/agenda:cal', $cal );

	$orderBy = 'ORDER BY starts_at DESC';
	ntsLib::setVar( 'admin/manage/agenda:orderBy', $orderBy );

	$where = array(
		'id ' => array( 'IN', $ids ),
		);

	$showFilter = FALSE;
	ntsLib::setVar( 'admin/manage/agenda:showFilter', $showFilter );
	}

$parent = NTS_APP_DIR . '/panels/admin/manage/agenda/a.php';
require( $parent );
?>