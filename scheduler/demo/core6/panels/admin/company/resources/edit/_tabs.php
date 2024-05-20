<?php
$ntsdb =& dbWrapper::getInstance();
$object = ntsLib::getVar( 'admin/company/resources/edit::OBJECT' );
$objId = $object->getId();

$tabs = array();

$tabs['edit'] = array(
	'title'	=> '<i class="fa fa-edit"></i> ' . M('Edit'),
	);

$tabs['staff'] = array(
	'title'	=> '<i class="fa fa-user"></i> ' . M('Administrative Users'),
	);

$resources_ids = ntsObjectFactory::getAllIds('resource');
if( count($resources_ids) > 1 )
{
	$tabs['delete'] = array(
		'title'	=> '<i class="fa fa-times text-danger"></i> ' . M('Delete'),
		'alert'	=> 1,
		);
}
?>