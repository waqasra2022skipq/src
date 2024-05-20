<?php
require( dirname(__FILE__) . '/_version_disable.php' );
$modify_version = 0;
$app_short = 'h6';
$order_link = 'http://www.hitappoint.com/order/';

/* features configuration */
$my_disable = array(
	'common',

	'wordpress',
	);

$skip = array(
//	'admin/conf/plugins',
	);

foreach( $my_disable as $d )
{
	$skip = array_merge( $skip, $disable[$d]['panels'] );
}

$disabled_features = array();
?>