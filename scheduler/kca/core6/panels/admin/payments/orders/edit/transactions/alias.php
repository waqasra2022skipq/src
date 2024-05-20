<?php
$alias = 'admin/payments/orders/transactions';

$object = ntsLib::getVar( 'admin/payments/orders/edit::OBJECT' );
$objId = $object->getId();

ntsLib::setVar( 'admin/payments/orders/transactions::order', $object );

ntsView::setBack( ntsLink::makeLink('admin/payments/orders/edit/transactions', '', array('_id' => $objId)), true );
?>