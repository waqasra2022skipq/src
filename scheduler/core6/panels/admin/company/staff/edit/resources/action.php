<?php
$ff =& ntsFormFactory::getInstance();
$object = ntsLib::getVar( 'admin/company/staff/edit::OBJECT' );
$cm =& ntsCommandManager::getInstance();

$formFile = dirname( __FILE__ ) . '/form';

/* prepare 'resources' input */
$objectInfo['resources'] = array();
$resApps = $object->getAppointmentPermissions();
foreach( $resApps as $resId => $perm ){
	if( ! isset($objectInfo['resources'][ $resId ]) )
		$objectInfo['resources'][ $resId ] = array();
	$objectInfo['resources'][ $resId ][ 'appointments_view' ] = $perm['view'] ? '-checked-' : '';
	$objectInfo['resources'][ $resId ][ 'appointments_edit' ] = $perm['edit'] ? '-checked-' : '';
	$objectInfo['resources'][ $resId ][ 'appointments_notified' ] = $perm['notified'] ? '-checked-' : '';
	}

$resSch = $object->getSchedulePermissions();
foreach( $resSch as $resId => $perm ){
	if( ! isset($objectInfo['resources'][ $resId ]) )
		$objectInfo['resources'][ $resId ] = array();
	$objectInfo['resources'][ $resId ][ 'schedules_view' ] = $perm['view'] ? '-checked-' : '';
	$objectInfo['resources'][ $resId ][ 'schedules_edit' ] = $perm['edit'] ? '-checked-' : '';
	}
$NTS_VIEW['form'] =& $ff->makeForm( $formFile, $objectInfo );

switch( $action ){
	case 'update':
		if( $NTS_VIEW['form']->validate() ){
			$formValues = $NTS_VIEW['form']->getValues();

			$resourceSchedules = array();
			$resourceApps = array();
			reset( $formValues['resources'] );
			foreach( $formValues['resources'] as $resId => $resPerms ){
				$resourceSchedules[ $resId ]['view'] = $resPerms['schedules_view'] ? 1 : 0;
				$resourceSchedules[ $resId ]['edit'] = $resPerms['schedules_edit'] ? 1 : 0;

				$resourceApps[ $resId ]['view'] = $resPerms['appointments_view'] ? 1 : 0;
				$resourceApps[ $resId ]['edit'] = $resPerms['appointments_edit'] ? 1 : 0;
				$resourceApps[ $resId ]['notified'] = $resPerms['appointments_notified'] ? 1 : 0;
				}

		/* update user */
			$object->setAppointmentPermissions( $resourceApps );
			$object->setSchedulePermissions( $resourceSchedules );

			$cm->runCommand( $object, 'update' );
			if( $cm->isOk() ){
				ntsView::setAnnounce( M('User') . ': ' . M('Update') . ': ' . M('OK'), 'ok' );

			/* continue to the list with anouncement */
				$forwardTo = ntsLink::makeLink( '-current-', '', array('id' => $id ) );
				ntsView::redirect( $forwardTo );
				exit;
				}
			else {
				$errorText = $cm->printActionErrors();
				ntsView::addAnnounce( $errorText, 'error' );
				}
			}
		else {
		/* form not valid, continue to edit form */
			}
		break;

	default:
		break;
	}
?>