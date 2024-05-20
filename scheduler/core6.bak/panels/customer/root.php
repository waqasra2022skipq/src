<?php
/* this file is here to indicate that the menu hierarchy starts here */
$conf =& ntsConf::getInstance();
$userLoginRequired = $conf->get('userLoginRequired');

$firstTimeSplash = $conf->get('firstTimeSplash');
if( $firstTimeSplash && (! isset($_COOKIE['ntsFirstTimeSplash'])) && ($_NTS['CURRENT_PANEL'] != 'customer/splash') ){
	$forwardTo = ntsLink::makeLink( 'customer/splash' );
	ntsView::redirect( $forwardTo );
	exit;
	}

/* also check permissions and set default panel */
$allow_nologin = array(
	'customer/splash',
//	'customer/book',
	'customer/invoices/view',
	);

if( (! ntsLib::getCurrentUserId()) && $userLoginRequired && (! in_array($_NTS['CURRENT_PANEL'], $allow_nologin)) )
{
	if( $_NTS['CURRENT_PANEL'] != 'customer' )
	{
		$requestParams = $_NTS['REQ']->getGetParams();
		$returnPage = array(
			NTS_PARAM_PANEL		=> $_NTS['CURRENT_PANEL'],
			NTS_PARAM_ACTION	=> $requestParams,
			'params'	=> $requestParams,
			);
		$_SESSION['return_after_login'] = $returnPage;
	}
	/* redirect to login page */
	$forwardTo = ntsLink::makeLink( 'anon/login' );
	ntsView::redirect( $forwardTo );
	exit;
//	$requested_panel = 'anon/login';
//	$_NTS['REQUESTED_PANEL'] = $requested_panel;
}


if( ! isset($_NTS['CURRENT_PANEL']) )
	$_NTS['CURRENT_PANEL'] = 'customer';

global $NTS_VIEW;
$t = new ntsTime();
global $NTS_CURRENT_USER;
$t->setTimezone( $NTS_CURRENT_USER->getTimezone() );
$NTS_VIEW['t'] = $t;

/* check user restrictions if any */
$restrictions = $NTS_CURRENT_USER->getProp('_restriction');
// _print_r( $restrictions );
// exit;

if( $restrictions ){
	$display = '';
	$logout = FALSE;
	if( in_array('email_not_confirmed', $restrictions) ){
		$display = 'emailNotConfirmed';
		$logout = TRUE;
	}
	elseif( in_array('not_approved', $restrictions) ){
		$display = 'notApproved';
	}
	elseif( in_array('suspended', $restrictions) ){
		$display = 'suspended';
	}

	if( $display ){
		if( $logout ){
			$cm =& ntsCommandManager::getInstance();
			$cm->runCommand( $NTS_CURRENT_USER, 'logout' );
		}

		$forwardTo = ntsLink::makeLink( 'anon/login', '', array('display' => $display) );
		ntsView::redirect( $forwardTo );
		exit;
	}
}

global $_NTS;
// $_NTS['REQ']->addSanitizer( 'service', '/^[\d-]*$/' );
// $_NTS['REQ']->addSanitizer( 'resource', '/^[\d-a]*$/' );
// $_NTS['REQ']->addSanitizer( 'location', '/^[\d-a]*$/' );
// $_NTS['REQ']->addSanitizer( 'time', '/^[\d-]*$/' );
// $_NTS['REQ']->addSanitizer( 'key', '/^[a-zA-Z\d_-]*$/' );
// $_NTS['REQ']->addSanitizer( 'cal', '/^[\d-]*$/' );
