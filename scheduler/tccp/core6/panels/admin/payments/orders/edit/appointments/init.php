<?php
$order = ntsLib::getVar( 'admin/payments/orders/edit::OBJECT' );
$orderId = $order->getId();
ntsView::setBack( ntsLink::makeLink('admin/payments/orders/edit/appointments', '', array('_id' => $orderId)) );

$persist = array( 
	'status' => 'all',
	'period' => 'all',
	);
reset( $persist );
foreach( $persist as $p => $default )
{
	$v = $_NTS['REQ']->getParam( $p );
	if( ! $v )
		$v = $default;
	$saveOn[$p] = $v;
}

ntsView::setPersistentParams( $saveOn, 'admin/payments/orders/edit/appointments' );
?>