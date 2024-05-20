<?php
$object = ntsLib::getVar( 'admin/payments/invoices/edit::OBJECT' );
$objId = $object->getId();

$tabs = array();

$tabs['edit'] = array(
	'title'	=> '<i class="fa fa-edit"></i> ' . M('Edit'),
	);

$tabs['send'] = array(
	'title'	=> '<i class="fa fa-envelope"></i> ' . M('Send'),
	);

$tabs['delete'] = array(
	'title'	=> '<i class="fa fa-times text-danger"></i> ' . M('Delete'),
	'alert'	=> 1,
	);
?>