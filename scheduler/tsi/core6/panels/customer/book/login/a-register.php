<?php
global $NTS_CURRENT_USER;
$conf =& ntsConf::getInstance();
$enableRegistration = $conf->get('enableRegistration');
$om =& objectMapper::getInstance();

$ff =& ntsFormFactory::getInstance();

$session = new ntsSession;
$apps = $session->userdata( 'apps' );

$service_ids = array();
foreach( $apps as $app ){
	$service_id = $app['service_id'];
	if( ! in_array($service_id, $service_ids) ){
		$service_ids[] = $service_id;
	}
}
$formParams = array(
	'service_ids'	=> $service_ids
	);

$formFile = dirname( __FILE__ ) . '/_form_register';
$NTS_VIEW['form_register'] =& $ff->makeForm( $formFile, $formParams );

$removeValidation = array();
if( NTS_ALLOW_NO_EMAIL && $_NTS['REQ']->getParam('noEmail') )
{
	$removeValidation[] = 'email';
}

if( $NTS_VIEW['form_register']->validate($removeValidation) )
{
	$registerNew = true;
	$formValues = $NTS_VIEW['form_register']->getValues();

	$cm =& ntsCommandManager::getInstance();

/* customer */
	$object = new ntsUser();
	unset( $formValues['password2'] );

	$conf =& ntsConf::getInstance();
	$allowDuplicateEmails = $conf->get( 'allowDuplicateEmails' );

/* if no reg enabled and this email exists, find it first */
	if( (! $enableRegistration) && $formValues['email'] && (! $allowDuplicateEmails) )
	{
		$uif =& ntsUserIntegratorFactory::getInstance();
		$integrator =& $uif->getIntegrator();

		$myWhere = array(
			'email'	=> array('=', $formValues['email']),
			);
		$thisUsers = $integrator->getUsers( $myWhere );

		if( $thisUsers && count($thisUsers) > 0 )
		{
			$existingUserId = $thisUsers[0]['id'];
			$object->setId( $existingUserId );
			$registerNew = false;
		}
	}

	if( (! $enableRegistration) && $registerNew )
	{
		if( $formValues['email'] )
			$formValues['username'] = $formValues['email'];
	}

	$object->setByArray( $formValues );
	$current_user_tz = $NTS_CURRENT_USER->getTimezone();
	$object->setProp( '_timezone', $current_user_tz );

	if( $registerNew )
	{
		$cm->runCommand( $object, 'create' );

		if( $cm->isOk() )
		{
			if( $object->getTimezone() != $current_user_tz ){
				$object->setProp( '_timezone', $current_user_tz );
				$cm->runCommand( $object, 'update' );
			}

			$lm =& ntsLanguageManager::getInstance(); 
			$activeLanguages = $lm->getActiveLanguages();
			if( $activeLanguages && count($activeLanguages) > 1 )
			{
				global $NTS_CURRENT_USER;
				$lng = $NTS_CURRENT_USER->getLanguage();
				$object->setLanguage( $lng );
			}

			if( $enableRegistration )
			{
			/* check if we need to require email validation */
				$userEmailConfirmation = $conf->get('userEmailConfirmation');

				$noEmail = $_NTS['REQ']->getParam('noEmail') ? TRUE : FALSE;
				if( $noEmail && $userEmailConfirmation ){
					$userEmailConfirmation = FALSE;
				}

			/* or admin approval */
				$userAdminApproval = $conf->get('userAdminApproval');
			}
			else
			{
			/* registration not enabled - not email confirmation required */	
				$userEmailConfirmation = 0;
				$userAdminApproval = 1;
			}

			if( $userEmailConfirmation || $userAdminApproval )
			{
				if( $userEmailConfirmation )
				{
					$cm->runCommand( $object, 'require_email_confirmation' );
				}
				elseif( $userAdminApproval ) 
				{
					$cm->runCommand( $object, 'require_approval' );
				}
			}
			else 
			{
			/* autoapprove */
				$cm->runCommand( $object, 'activate' );
			/* then login */
				$cm->runCommand( $object, 'login' );
			}
		}
		else 
		{
			$errorText = $cm->printActionErrors();
			ntsView::addAnnounce( $errorText, 'error' );
		}
	}
	else 
	{
	// update existing customer record
	/* if it is a provider then don't update */
		if( ! $object->hasRole('admin') ){
			$cm->runCommand( $object, 'update' );
			if( $cm->isOk() ){
	//			$_SESSION['temp_customer_id'] = $object->getId();
			}
			else {
				$errorText = $cm->printActionErrors();
				ntsView::addAnnounce( $errorText, 'error' );
			}
		}
	}
}
else
{
/* form not valid, continue to create form */
	require( dirname(__FILE__) . '/a.php' );
	return;
}

$tm2 = $NTS_VIEW['tm2'];
$tm2->customerId = $object->getId();
$NTS_VIEW['tm2'] = $tm2;

require( dirname(__FILE__) . '/a-finalize.php' );
?>