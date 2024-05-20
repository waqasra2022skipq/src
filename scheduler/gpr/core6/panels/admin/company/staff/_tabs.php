<?php
$tabs = array();

$tabs['browse'] = array(
	'title'	=> '<i class="fa fa-list"></i> ' . M('View'),
	);

$tabs['create'] = array(
	'title'	=> '<i class="fa fa-plus"></i> ' . M('Add'),
	);

$uif =& ntsUserIntegratorFactory::getInstance();
$integrator =& $uif->getIntegrator();
$admins = $integrator->getAdmins();
if( count($admins) > 1 ){
	$tabs['permissions'] = array(
		'title'	=> '<i class="fa fa-list"></i> ' . M('Permissions Summary'),
		);
}
?>