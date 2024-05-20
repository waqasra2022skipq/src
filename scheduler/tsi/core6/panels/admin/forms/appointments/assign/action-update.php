<?php
$cm =& ntsCommandManager::getInstance();

$serviceId = $_NTS['REQ']->getParam( 'service_id' );
$object = new ntsObject( 'service' );
$object->setId( $serviceId );

$formId = $_NTS['REQ']->getParam( '_form' );
$object->setProp( '_form', $formId );

$cm->runCommand( $object, 'update' );

if( $cm->isOk() ){
	$id = $object->getId();
	ntsView::addAnnounce( M('Form') . ': ' . M('Assign') . ': ' . M('OK'), 'ok' );

/* continue to the list with anouncement */
	$forwardTo = ntsLink::makeLink( '-current-' );
	ntsView::redirect( $forwardTo );
	exit;
	}
else {
	$errorText = $cm->printActionErrors();
	ntsView::addAnnounce( $errorText, 'error' );
	}
?>