<?php
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

$formFile = dirname( __FILE__ ) . '/_form_login';
$form =& $ff->makeForm( $formFile, $formParams );

if( $form->validate() )
{
	$formValues = $form->getValues();
	$remember = isset($formValues['remember']) ? $formValues['remember'] : FALSE;

/* local handler */
	$object = new ntsUser();
	if( NTS_EMAIL_AS_USERNAME )
		$object->setProp( 'email', $formValues['login_email'] );
	else
		$object->setProp( 'username', $formValues['login_username'] );
	$object->setProp( 'password', $formValues['login_password'] );

	$cm =& ntsCommandManager::getInstance();
	$cm->runCommand( $object, 'check_password' );

	if( ! $cm->isOk() )
	{
	/* wrong password */
		$msg = $cm->printActionErrors();

		ntsView::addAnnounce( $msg, 'error' );
		$forwardTo = ntsLink::makeLink('-current-');
		ntsView::redirect( $forwardTo );
		exit;
	}

/* check user restrictions if any */
	$restrictions = $object->getProp('_restriction');

/* restrictions apply */
	if( $restrictions )
	{
		$display = '';
		if( in_array('email_not_confirmed', $restrictions) )
		{
			$msg = M('Email') . ': ' . M('Not Confirmed');
		}
		elseif( in_array('not_approved', $restrictions) )
		{
			$msg = M('Account') . ': ' . M('Not Approved');
		}
		elseif( in_array('suspended', $restrictions) )
		{
			$msg = M('Account') . ': ' . M('Suspended');
		}
		else 
		{
			$msg = M('Error');
		}

		ntsView::addAnnounce( $msg, 'error' );
		$forwardTo = ntsLink::makeLink('-current-');
		ntsView::redirect( $forwardTo );
		exit;
	}
	else
	{
	/* complete actions */
		$params = array(
			'remember'	=> $remember 
			);
		$cm->runCommand( $object, 'login', $params );
	}
}
else 
{
/* form not valid, continue to login form */
	$forwardTo = ntsLink::makeLink('-current-');
	ntsView::redirect( $forwardTo );
	exit;
}

$tm2 = $NTS_VIEW['tm2'];
$tm2->customerId = $object->getId();
$NTS_VIEW['tm2'] = $tm2;

require( dirname(__FILE__) . '/a-finalize.php' );
?>