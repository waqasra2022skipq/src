<?php
$service_id = $_NTS['REQ']->getParam('service');

$session = new ntsSession;
$apps = $session->userdata( 'apps' );

$service_ids = array();
foreach( $apps as $app ){
	$service_id = $app['service_id'];
	if( ! in_array($service_id, $service_ids) ){
		$service_ids[] = $service_id;
	}
}

$ff =& ntsFormFactory::getInstance();
$formFile = dirname(__FILE__) . '/form';
$formParams = array(
	'service_ids'	=> $service_ids
	);
$NTS_VIEW['form'] =& $ff->makeForm( $formFile, $formParams );

if( $NTS_VIEW['form']->validate() )
{
	$formValues = $NTS_VIEW['form']->getValues();

	/* save it in session */
	$session = new ntsSession;
	$apps = $session->userdata('apps');

	for( $ii = 0; $ii < count($apps); $ii++ )
	{
		reset( $formValues );
		foreach( $formValues as $k => $v )
		{
			$apps[$ii][$k] = $v;
		}
	}
	$session->set_userdata( 'apps', $apps );

	/* if not logged in then go to login form */
	if( ! ntsLib::getCurrentUserId() )
	{
		$forwardTo = ntsLink::makeLink('-current-/../login');
		ntsView::redirect( $forwardTo );
		exit;
	}

	/* otherwise finalize the confirm */
	require( dirname(__FILE__) . '/a-finalize.php' );
	return;
}
else
{
/* form not valid, back to form */
	require( dirname(__FILE__) . '/a-form.php' );
	return;
}
?>