<?php
$ff =& ntsFormFactory::getInstance();
$object = ntsLib::getVar( 'admin/company/resources/edit::OBJECT' );
$cm =& ntsCommandManager::getInstance();

$formFile = dirname( __FILE__ ) . '/form';

/* prepare 'staff' input */
$objectInfo['staff'] = array();
$currentAdminsIds = array();
list( $appsAdmins, $scheduleAdmins ) = $object->getAdmins();
reset( $appsAdmins );
foreach( $appsAdmins as $admId => $perm ){
	$currentAdminsIds[] = $admId;
	if( ! isset($objectInfo['staff'][ $admId ]) )
		$objectInfo['staff'][ $admId ] = array();
	$objectInfo['staff'][ $admId ][ 'appointments_view' ] = $perm['view'] ? '-checked-' : '';
	$objectInfo['staff'][ $admId ][ 'appointments_edit' ] = $perm['edit'] ? '-checked-' : '';
	$objectInfo['staff'][ $admId ][ 'appointments_notified' ] = $perm['notified'] ? '-checked-' : '';
	}
reset( $scheduleAdmins );
foreach( $scheduleAdmins as $admId => $perm ){
	$currentAdminsIds[] = $admId;
	if( ! isset($objectInfo['staff'][ $admId ]) )
		$objectInfo['staff'][ $admId ] = array();
	$objectInfo['staff'][ $admId ][ 'schedules_view' ] = $perm['view'] ? '-checked-' : '';
	$objectInfo['staff'][ $admId ][ 'schedules_edit' ] = $perm['edit'] ? '-checked-' : '';
	}
$currentAdminsIds = array_unique( $currentAdminsIds );
$NTS_VIEW['form'] =& $ff->makeForm( $formFile, $objectInfo );

switch( $action ){
	case 'update':
		if( $NTS_VIEW['form']->validate() ){
			$formValues = $NTS_VIEW['form']->getValues();

			$newAdminsIds = array_keys( $formValues['staff'] );
			$allAdminsIds = array_merge( $currentAdminsIds, $newAdminsIds );
			$allAdminsIds = array_unique( $allAdminsIds );

			reset( $allAdminsIds );
			foreach( $allAdminsIds as $admId ){
				$admin = new ntsUser;
				$admin->setId( $admId );

				$resourceApps = $admin->getAppointmentPermissions();
				if( isset($formValues['staff'][$admId]) ){
					$resourceApps[ $id ]['view'] = $formValues['staff'][$admId]['appointments_view'] ? 1 : 0;
					$resourceApps[ $id ]['edit'] = $formValues['staff'][$admId]['appointments_edit'] ? 1 : 0;
					$resourceApps[ $id ]['notified'] = $formValues['staff'][$admId]['appointments_notified'] ? 1 : 0;
					}
				else {
					$resourceApps[ $id ] = array();
					}
				$admin->setAppointmentPermissions( $resourceApps );

				$resourceSchedules = $admin->getSchedulePermissions();
				if( isset($formValues['staff'][$admId]) ){
					$resourceSchedules[ $id ]['view'] = $formValues['staff'][$admId]['schedules_view'] ? 1 : 0;
					$resourceSchedules[ $id ]['edit'] = $formValues['staff'][$admId]['schedules_edit'] ? 1 : 0;
					}
				else {
					$resourceSchedules[ $id ] = array();
					}
				$admin->setSchedulePermissions( $resourceSchedules );

				$cm->runCommand( $admin, 'update' );
				}

			if( $cm->isOk() ){
				ntsView::addAnnounce( M('Bookable Resource') . ': ' . M('Update') . ': ' . M('OK'), 'ok' );

			/* continue to the list with anouncement */
				$forwardTo = ntsLink::makeLink( '-current-' );
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