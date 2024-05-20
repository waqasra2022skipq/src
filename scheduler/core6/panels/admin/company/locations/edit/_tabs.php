<?php
$tabs = array();

$tabs['edit'] = array(
	'title'	=> '<i class="fa fa-edit"></i> ' . M('Edit'),
	);

$locations = ntsObjectFactory::getAllIds( 'location' );
if( count($locations) > 1 )
{
	$tabs['delete'] = array(
		'title'	=> '<i class="fa fa-times text-danger"></i> ' . M('Delete'),
		'alert'	=> 1,
		);
}
?>