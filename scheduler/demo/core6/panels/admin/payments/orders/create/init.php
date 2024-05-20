<?php
ntsLib::setVar( 'admin/payments/orders/create::fixCustomer', 0 );

$id = $_NTS['REQ']->getParam( '_id' );
ntsView::setPersistentParams( array('_id' => $id), 'admin/payments/orders/create' );

$object = ntsObjectFactory::get( 'pack' );
$object->setId( $id );
ntsLib::setVar( 'admin/payments/orders/create::fixPack', $object->getId() );

$customerId = $_NTS['REQ']->getParam( 'customer' );
if( $customerId )
{
	ntsLib::setVar( 'admin/payments/orders/create::fixCustomer', $customerId );
	ntsView::setPersistentParams( array('customer' => $customerId), 'admin/payments/orders/create' );
}
?>