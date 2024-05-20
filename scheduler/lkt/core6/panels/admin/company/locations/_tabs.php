<?php
$tabs = array();

$tabs['browse'] = array(
	'title'	=> '<i class="fa fa-list"></i> ' . M('View'),
	);

$tabs['create'] = array(
	'title'	=> '<i class="fa fa-plus"></i> ' . M('Add'),
	);

$locs = ntsLib::getVar( 'admin::locs' );
if( count($locs) > 1 )
{
	$tabs['settings'] = array(
		'title'	=> '<i class="fa fa-cog"></i> ' . M('Settings'),
		);
	$tabs['travel'] = array(
		'title'	=> '<i class="fa fa-truck"></i> ' . M('Travel Time'),
		);
}
?>