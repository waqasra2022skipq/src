<?php
global $_NTS;
$limit_qty = isset($_NTS['limit']['resource']) ? $_NTS['limit']['resource'] : 0;
if( $limit_qty ){
	$already_have = ntsObjectFactory::getAllIds( 'resource' );
	if( count($already_have) >= $limit_qty ){
		$errorText = M('You are not allowed to create more resources');

		ntsView::addAnnounce( $errorText, 'error' );
		$forwardTo = ntsLink::makeLink( '-current-/../browse' );
		ntsView::redirect( $forwardTo );
		exit;
	}
}

$ff =& ntsFormFactory::getInstance();
$formFile = NTS_APP_DIR . '/app/forms/resource';
$NTS_VIEW['form'] =& $ff->makeForm( $formFile );

switch( $action ){
	case 'save':
		if( $NTS_VIEW['form']->validate() ){
			$formValues = $NTS_VIEW['form']->getValues();

			$cm =& ntsCommandManager::getInstance();

		/* resource */
			$object = ntsObjectFactory::get( 'resource' );
			$object->setByArray( $formValues );
			$cm->runCommand( $object, 'create' );
			$newObjId = $object->getId();

		/* assign all rights for the creating user */
			global $NTS_CURRENT_USER;
			$resourceSchedules = $NTS_CURRENT_USER->getSchedulePermissions();
			$resourceApps = $NTS_CURRENT_USER->getAppointmentPermissions();

			$resourceSchedules[ $newObjId ] = array( 'view' => 1, 'edit' => 1 );
			$resourceApps[ $newObjId ] = array( 'view' => 1, 'edit' => 1, 'notified' => 1 );

			$NTS_CURRENT_USER->setSchedulePermissions( $resourceSchedules );
			$NTS_CURRENT_USER->setAppointmentPermissions( $resourceApps );
			$cm->runCommand( $NTS_CURRENT_USER, 'update' );

			if( $cm->isOk() ){
				$msg = array( M('Bookable Resource'), ntsView::objectTitle($object), M('Create'), M('OK') );
				$msg = join( ': ', $msg );
				ntsView::addAnnounce( $msg, 'ok' );

			/* continue to the list with anouncement */
				$forwardTo = ntsLink::makeLink( '-current-/../browse' );
				ntsView::redirect( $forwardTo );
				exit;
				}
			else {
				$errorText = $cm->printActionErrors();
				ntsView::addAnnounce( $errorText, 'error' );
				}
			}
		else {
		/* form not valid, continue to create form */
			}

		break;
	default:
		break;
	}
?>