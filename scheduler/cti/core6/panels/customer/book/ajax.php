<?php
/* prepare for promotions */
$current_user = ntsLib::getCurrentUser();
$ntspm =& ntsPaymentManager::getInstance();

$full_r = array();
if( isset($requested['location']) )
	$full_r['location_id'] = $requested['location'];
if( isset($requested['resource']) )
	$full_r['resource_id'] = $requested['resource'];
if( isset($requested['service']) )
	$full_r['service_id'] = $requested['service'];
if( $current_user->getId() )
	$full_r['customer_id'] = $current_user->getId();

require( dirname(__FILE__) . '/_index_time_view.php' );
?>