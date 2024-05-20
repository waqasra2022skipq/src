<?php
$alias = 'admin/payments/invoices';

$object = ntsLib::getVar( 'admin/customers/edit::OBJECT' );
$customerId = $object->getId();
ntsView::setBack( ntsLink::makeLink('admin/customers/edit/payments/browse', '', array('_id' => $customerId) ) );

$where = array();
ntsLib::setVar( 'admin/payments/invoices::where', $where );
ntsLib::setVar( 'admin/payments/invoices::customer', $customerId );
?>