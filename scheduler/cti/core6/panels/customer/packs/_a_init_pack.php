<?php
$pack_id = $_NTS['REQ']->getParam('pack');
if( ! $pack_id )
{
	$error_msg = join( ': ', array(M('Package'), M('Required')) );
	ntsView::addAnnounce( $error_msg, 'error' );
	$forwardTo = ntsLink::makeLink('-current-/..');
	ntsView::redirect( $forwardTo );
	exit;
}

$pack = ntsObjectFactory::get('pack');
$pack->setId( $pack_id );
?>