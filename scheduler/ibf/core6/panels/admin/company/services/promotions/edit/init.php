<?php
$id = $_NTS['REQ']->getParam( 'promotion_id' );
ntsView::setPersistentParams( array('promotion_id' => $id), 'admin/company/services/promotions/edit' );

$object = ntsObjectFactory::get( 'promotion' );
$object->setId( $id );
ntsLib::setVar( 'admin/company/services/promotions/edit::OBJECT', $object );
?>