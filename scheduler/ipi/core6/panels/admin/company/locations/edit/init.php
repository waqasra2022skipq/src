<?php
$id = $_NTS['REQ']->getParam( '_id' );
ntsView::setPersistentParams( array('_id' => $id), 'admin/company/locations/edit' );

$object = ntsObjectFactory::get( 'location' );
$object->setId( $id );
ntsLib::setVar( 'admin/company/locations/edit::OBJECT', $object );
?>