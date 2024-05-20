<?php
$tabs = array();

$tabs['browse'] = array(
	'title'	=> '<i class="fa fa-list"></i> ' . M('View'),
	);

$tabs['create'] = array(
	'title'	=> '<i class="fa fa-plus"></i> ' . M('Add'),
	);

$ress = ntsLib::getVar( 'admin::ress' );
if( count($ress) > 1 )
{
	$tabs['settings'] = array(
		'title'	=> '<i class="fa fa-cog"></i> ' . M('Settings'),
		);
	$tabs['permissions'] = array(
		'title'	=> '<i class="fa fa-list"></i> ' . M('Permissions Summary'),
		);
}
?>