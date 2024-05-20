<?php
$id = $_NTS['REQ']->getParam( '_id' );
ntsView::setPersistentParams( array('_id' => $id), 'admin/company/staff/edit' );

$object = new ntsUser;
$object->setId( $id );
ntsLib::setVar( 'admin/company/staff/edit::OBJECT', $object );
?>