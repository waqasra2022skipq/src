<?php
$id = $_NTS['REQ']->getParam( '_id' );
ntsView::setPersistentParams( array('_id' => $id), 'admin/forms/appointments/edit' );

$object = ntsObjectFactory::get( 'form' );
$object->setId( $id );
ntsLib::setVar( 'admin/forms/appointments/edit::OBJECT', $object );
?>