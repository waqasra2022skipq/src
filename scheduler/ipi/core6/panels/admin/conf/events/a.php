<?php
$om =& ntsObserverManager::getInstance();

$observers = $om->get_all_observers();
$active_observers = $om->get_active_observers();

$observer_params = array();
foreach( $active_observers as $ao )
{
	$observer_params[$ao]  = $om->get_params( $ao );
}

$view = array(
	'observers'			=> $observers,
	'active_observers'	=> $active_observers,
	'observer_params'	=> $observer_params,
	);

$this->render( 
	dirname(__FILE__) . '/index.php',
	$view
	);
?>