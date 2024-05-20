<?php
$ntsdb =& dbWrapper::getInstance();
$object = ntsLib::getVar( 'admin/company/staff/edit::OBJECT' );
$objId = $object->getId();

$tabs = array();

$tabs['edit'] = array(
	'title'	=> '<i class="fa fa-edit"></i> ' . M('Edit'),
	);

$all_ress_count = ntsObjectFactory::count(
	'resource', 
	array(
		'archive'	=> array('<>', 1)
		)
	);

$my_ress = array();
$schPermissions = $object->getSchedulePermissions();
$my_ress = array_merge( $my_ress, array_keys($schPermissions) );
$appPermissions = $object->getAppointmentPermissions();
$my_ress = array_merge( $my_ress, array_keys($appPermissions) );
$my_ress = array_unique($my_ress);

$ress_archive = ntsObjectFactory::getIds( 
	'resource', 
	array(
		'archive'	=> array( '=', 1 ),
		)
	);
if( $ress_archive )
{
	$my_ress = array_diff( $my_ress, $ress_archive );
	$my_ress = array_values( $my_ress );
}

$tabs['resources'] = array(
	'title'	=> '<i class="fa fa-hand-o-up"></i> ' . M('Bookable Resources') . ' [' . count($my_ress) . '/' . $all_ress_count . ']',
	);

/*
$tabs['permissions'] = array(
	'title'	=> '<i class="fa fa-lock"></i> ' . M('System Access Level'),
	);
*/

$tabs['password'] = array(
	'title'	=> '<i class="fa fa-key"></i> ' . M('Password'),
	);

if( $objId != ntsLib::getCurrentUserId() )
{
	$tabs['delete'] = array(
		'title'	=> '<i class="fa fa-times text-danger"></i> ' . M('Delete'),
		'alert'	=> 1,
		);
}
?>