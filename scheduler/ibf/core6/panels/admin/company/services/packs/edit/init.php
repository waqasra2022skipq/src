<?php
$id = $_NTS['REQ']->getParam( '_id' );
ntsView::setPersistentParams( array('_id' => $id), 'admin/company/services/packs/edit' );

$object = ntsObjectFactory::get( 'pack' );
$object->setId( $id );
ntsLib::setVar( 'admin/company/services/packs/edit::OBJECT', $object );
?>