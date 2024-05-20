<?php
$where = array();
ntsLib::setVar( 'admin/payments/orders::where', $where );

$customer = null;
ntsLib::setVar( 'admin/payments/orders::customer', $customer );

$customer_id = $_NTS['REQ']->getParam( 'customer' );
if( ! $customer_id )
{
	ntsView::setBack( ntsLink::makeLink('admin/payments/orders/browse') );
}
?>