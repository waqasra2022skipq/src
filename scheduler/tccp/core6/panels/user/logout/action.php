<?php
$object = new ntsUser();
$object->setId( ntsLib::getCurrentUserId() );

/* complete actions */
$cm =& ntsCommandManager::getInstance();
$cm->runCommand( $object, 'logout' );

ntsView::setAnnounce( M('Logged out'), 'ok' );

/* continue to home page */
$forwardTo = ntsLink::makeLink();

if( $ri == 'wordpress' ){
	$forwardTo = home_url();
}

ntsView::redirect( $forwardTo );
exit;
?>