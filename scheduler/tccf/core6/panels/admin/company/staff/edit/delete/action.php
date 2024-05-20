<?php
$object = ntsLib::getVar( 'admin/company/staff/edit::OBJECT' );

$ff =& ntsFormFactory::getInstance();
$NTS_VIEW['form'] =& $ff->makeForm( dirname(__FILE__) . '/form' );

switch( $action ){
	case 'delete':
		$cm =& ntsCommandManager::getInstance();
		$cm->runCommand( $object, 'delete' );

		if( $cm->isOk() ){
			$announce = join( ': ', array(M('Administrative User'), M('Delete'), M('OK')) );
			ntsView::setAnnounce( $announce, 'ok' );
			}
		else {
			$errorText = $cm->printActionErrors();
			ntsView::addAnnounce( $errorText, 'error' );
			}

		/* continue to list */
		$forwardTo = ntsLink::makeLink( '-current-/../../browse' );
		ntsView::redirect( $forwardTo );
		exit;
		break;
	}
?>