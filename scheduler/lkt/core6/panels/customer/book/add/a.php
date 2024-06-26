<?php
/* save this appointment in session */
$object = ntsObjectFactory::get( 'appointment' );
$location_id = NTS_SINGLE_LOCATION ? NTS_SINGLE_LOCATION : $_NTS['REQ']->getParam('location');
$resource_id = NTS_SINGLE_RESOURCE ? NTS_SINGLE_RESOURCE : $_NTS['REQ']->getParam('resource');
$service_id = $_NTS['REQ']->getParam('service');
$starts_at = $_NTS['REQ']->getParam('time');
$seats = $_NTS['REQ']->getParam('seats');
if( ! $seats ){
	$seats = 1;
}

$duration = 0;
$duration_break = 0;
$duration2 = 0;
if( $service_id )
{
	$service = ntsObjectFactory::get( 'service' );
	$service->setId( $service_id );
	$duration = $service->getProp('duration');
	$duration_break = $service->getProp('duration_break');
	$duration2 = $service->getProp('duration2');
}

$app = array(
	'location_id'	=> $location_id,
	'resource_id'	=> $resource_id,
	'service_id'	=> $service_id,
	'seats'			=> $seats,
	'starts_at'		=> $starts_at,
	'duration'		=> $duration,
	'duration_break'	=> $duration_break,
	'duration2'		=> $duration2,
	);

if( ntsLib::getCurrentUserId() )
{
	$app['customer_id'] = ntsLib::getCurrentUserId();
}

$session = new ntsSession;
$apps = $session->userdata('apps');
if( ! $apps )
	$apps = array();
$apps[] = $app;
require( dirname(__FILE__) . '/../confirm/_check.php' );

/* sort by starts_at */
usort( $apps, create_function(
	'$a, $b',
	'
	$return = ($a["starts_at"] - $b["starts_at"]);
	return $return;
	'
	)
);

/* save */
$session->set_userdata( 'apps', $apps );

$forwardTo = ntsLink::makeLink('-current-/../confirm', '', array(), FALSE, TRUE);
ntsView::redirect( $forwardTo );
exit;
?>