<?php
$ntsdb =& dbWrapper::getInstance();
$ff =& ntsFormFactory::getInstance();
$object = ntsLib::getVar( 'admin/company/services/packs/edit::OBJECT' );

$formFile = dirname( __FILE__ ) . '/form';
$NTS_VIEW['form'] =& $ff->makeForm( $formFile );

switch( $action ){
	case 'delete':
		$title = ntsView::objectTitle($object);
		$cm =& ntsCommandManager::getInstance();
		$cm->runCommand( $object, 'delete' );
		
		if( $cm->isOk() ){
			ntsView::setAnnounce( $title . ': '. M('Delete') . ': ' . M('OK'), 'ok' );
			}
		else {
			$errorText = $cm->printActionErrors();
			ntsView::addAnnounce( $errorText, 'error' );
			}
	/* continue to the list with anouncement */
		$forwardTo = ntsLink::makeLink( '-current-/../../browse' );
		ntsView::redirect( $forwardTo );
		exit;
		break;
	}
?>