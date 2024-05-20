<?php
$id = $_NTS['REQ']->getParam( '_id' );
ntsView::setPersistentParams( array('_id' => $id), 'admin/payments/orders/edit' );

$object = ntsObjectFactory::get( 'order' );
$object->setId( $id );
ntsLib::setVar( 'admin/payments/orders/edit::OBJECT', $object );
?>