<?php
$runActions = array();
if( ($mainActionName == 'change') && ($changes = $object->getChanges()) && ( isset($changes['resource_id']) ) ){
	/* old resource */
	$oldRid = $changes['resource_id'];
	$resource = ntsObjectFactory::get( 'resource' );
	$resource->setId( $oldRid );

	list( $appsAdmins, $scheduleAdmins ) = $resource->getAdmins();
	$providers = array();
	reset( $appsAdmins );
	foreach( $appsAdmins as $admId => $access ){
		if( $access['notified'] ){
			$provider = new ntsUser;
			$provider->setId( $admId );
			$providers[] = $provider;
			}
		}
	$runActions[] = array( 'reassign_from', $providers );

	/* new resource */
	$newRid = $object->getProp('resource_id');
	$resource = ntsObjectFactory::get( 'resource' );
	$resource->setId( $newRid );

	list( $appsAdmins, $scheduleAdmins ) = $resource->getAdmins();
	$providers = array();
	reset( $appsAdmins );
	foreach( $appsAdmins as $admId => $access ){
		if( $access['notified'] ){
			$provider = new ntsUser;
			$provider->setId( $admId );
			$providers[] = $provider;
			}
		}
	$runActions[] = array( 'reassign_to', $providers );
	}
else {
/* --- GET TEMPLATE --- */
	$key = 'appointment-' . $mainActionName . '-provider';

	/* --- SKIP IF THIS NOTIFICATION DISABLED --- */
	$currentlyDisabled = $plm->getPluginSetting($plugin, 'disabledNotifications');
	if( ! $currentlyDisabled )
		$currentlyDisabled = array();
	if( ! is_array($currentlyDisabled) )
		$currentlyDisabled = array( $currentlyDisabled );

	if( in_array($key, $currentlyDisabled) ){
		return;
		}
		
	/* --- SKIP IF NO TEMPLATE --- */
	$userLang = $defaultLanguage;
	$templateInfo = $stm->getTemplate( $userLang, $key );
	if( ! $templateInfo ){
		return;
		}
		
	$resourceId = $object->getProp( 'resource_id' );
	$resource = ntsObjectFactory::get( 'resource' );
	$resource->setId( $resourceId );

	list( $appsAdmins, $scheduleAdmins ) = $resource->getAdmins();
	$providers = array();
	reset( $appsAdmins );
	foreach( $appsAdmins as $admId => $access ){
		if( $access['notified'] ){
			$provider = new ntsUser;
			$provider->setId( $admId );
			$providers[] = $provider;
			}
		}
	$runActions[] = array( $mainActionName, $providers );
	}

reset( $runActions );
foreach( $runActions as $ra ){
	list( $mainActionName, $providers ) = $ra;
/* --- GET TEMPLATE --- */
	$key = 'appointment-' . $mainActionName . '-provider';

	/* --- SKIP IF THIS NOTIFICATION DISABLED --- */
	$currentlyDisabled = $plm->getPluginSetting($plugin, 'disabledNotifications');
	if( ! $currentlyDisabled )
		$currentlyDisabled = array();
	if( ! is_array($currentlyDisabled) )
		$currentlyDisabled = array( $currentlyDisabled );

	if( in_array($key, $currentlyDisabled) ){
		return;
		}

	/* --- SKIP IF NO TEMPLATE --- */
	$userLang = $defaultLanguage;
	$templateInfo = $stm->getTemplate( $userLang, $key );
	if( ! $templateInfo ){
		continue;
		}

	/* parse templates */
	$tags = $om->makeTags_Appointment( $object, 'internal' );
	if( isset($params['reason']) ){
		$tags[0][] = '{REJECT_REASON}';
		$tags[1][] = $params['reason'];
		$tags[0][] = '{CANCEL_REASON}';
		$tags[1][] = $params['reason'];

		$tags[0][] = '{APPOINTMENT.REJECT_REASON}';
		$tags[1][] = $params['reason'];
		$tags[0][] = '{APPOINTMENT.CANCEL_REASON}';
		$tags[1][] = $params['reason'];
		}

	/* quick links */
	$authCode = $object->getProp( 'auth_code' );
	$approveLink = ntsLink::makeLink( 'system/appointments/edit', 'approve', array('auth' => $authCode, 'id' => $object->getId()) );
	$approveLink = '<a href="' . $approveLink . '">' . M('Approve') . '</a>';
	$rejectLink = ntsLink::makeLink( 'system/appointments/edit', 'reject', array('auth' => $authCode, 'id' => $object->getId()) );
	$rejectLink = '<a href="' . $rejectLink . '">' . M('Reject') . '</a>';

	$tags[0][] = '{APPOINTMENT.QUICK_LINK_APPROVE}';
	$tags[1][] = $approveLink;
	$tags[0][] = '{APPOINTMENT.QUICK_LINK_REJECT}';
	$tags[1][] = $rejectLink;

	/* add .ics attachement */
	$attachements = array();
	if( in_array($key, $attachTo) ){
		include_once( NTS_APP_DIR . '/helpers/ical.php' );
		$ntsCal = new ntsIcal();
		$ntsCal->setTimezone( NTS_COMPANY_TIMEZONE );
		$ntsCal->addAppointment( $object );
		$str = $ntsCal->printOut();

		$attachName = 'appointment-' . $object->getId() . '.ics';
		$attachements[] = array( $attachName, $str );

		$tags[0][] = '{APPOINTMENT.LINK_TO_ICAL}';
		$tags[1][] = 'cid:' . $attachName;
		}
	else {
		$tags[0][] = '{APPOINTMENT.LINK_TO_ICAL}';
		$tags[1][] = '';
		}

	/* replace tags */
	$subject = isset($templateInfo['subject']) ? str_replace( $tags[0], $tags[1], $templateInfo['subject'] ) : '';
	$body = isset($templateInfo['body']) ? str_replace( $tags[0], $tags[1], $templateInfo['body'] ) : '';

	/* --- SEND SMS --- */
	reset( $providers );
	foreach( $providers as $provider ){
		$userMobile = trim( $provider->getProp('mobile_phone') );
		if( $userMobile )
			$this->runCommand( $provider, 'sms', array('body' => $body) );
		}
	}
?>