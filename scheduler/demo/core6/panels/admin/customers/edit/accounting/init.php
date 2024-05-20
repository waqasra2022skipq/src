<?php
$object = ntsLib::getVar( 'admin/customers/edit::OBJECT' );
ntsView::setBack( ntsLink::makeLink('admin/customers/edit/accounting', '', array('_id' => $object->getId())) );
?>