<?php
require( dirname(__FILE__) . '/_prepare_apps.php' );

$view = array(
	'display'		=> $display,
	'show_control'	=> FALSE,
	'labels'		=> $labels,
	'apps'			=> $apps,
	'customer_id'	=> $customer_id,
	'stats'			=> $stats,
	);

$this->render(
	$calendar_dir . '/views/' . $view_file . '.php',
	$view
	);
?>