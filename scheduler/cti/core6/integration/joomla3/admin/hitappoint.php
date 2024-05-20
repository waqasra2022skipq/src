<?php
error_reporting( E_ALL );
ini_set( 'display_errors', 'On' );

/********************************************************************
Author  :  	hitAppoint
Date    :	February 2010
Version :	4.0.0
Contact :	support@hitappoint.com
Description:  Displays hitAppoint
*********************************************************************
This file is part of hitApppoint Module
*********************************************************************/
defined('_JEXEC') or die('Restricted access');
include_once( dirname(__FILE__) . '/../../../components/com_hitappoint/_conf.php' );
define( 'NTS_REMOTE_INTEGRATION',	'joomla3' );
$jsession	= JFactory::getSession();
$jSessionName = $jsession->getName();
define( 'NTS_SESSION_NAME', $jSessionName );

JToolBarHelper::title('hitAppoint');

$currentUser = JFactory::getUser();
define( 'NTS_CURRENT_USERID', $currentUser->id );

$rootWebpage = JURI::base() . 'index.php?option=com_hitappoint'; 
define( 'NTS_ROOT_WEBPAGE',	$rootWebpage );

$frontEnd = JURI::root() . 'index.php?option=com_hitappoint';
define( 'NTS_FRONTEND_WEBPAGE',	$frontEnd );

$file = HITAPPOINT_PATH . '/core5/controller.php';
require( $file );

$jApp = JFactory::getApplication();
global $_NTS;
/* redirect to customer if needed */
if( ($jApp->isAdmin()) && ( (substr($_NTS['CURRENT_PANEL'], 0, strlen('customer')) == 'customer') ) ){
	reset( $_GET );
	foreach( $_GET as $p => $v ){
		if( $p == 'option' )
			continue;
		$linkParts[] = $p . '=' . urlencode($v);
		}
	$link = join( '&', $linkParts );
	$forwardTo = JURI::root() . 'index.php?option=com_hitappoint';
	if( $link )
		$forwardTo .= '&' . $link;

	ntsView::redirect( $forwardTo );
	exit;
	}

/* add stylesheet */
$file = HITAPPOINT_PATH . '/core5/views/css.php';
require( $file );
$document = JFactory::getDocument();
$document->addStyleSheet($NTS_CSS_URL);

/* hitAppoint view */	
$file = HITAPPOINT_PATH . '/core5/view.php';
require( $file );
?>
