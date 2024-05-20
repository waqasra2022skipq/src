<?php
$conf =& ntsConf::getInstance();

$ff =& ntsFormFactory::getInstance();
$form =& $ff->makeForm( dirname(__FILE__) . '/form' );

if( $form->validate() ){
	$formValues = $form->getValues();
	$currentFlowSetting = $formValues['current-flow-setting'];
	$flow = explode( "|", $currentFlowSetting );
	$currentFlow = array();
	reset( $flow );
	foreach( $flow as $f ){
		$f = trim( $f );
		if( ! $f )
			continue;
		switch( $f ){
			case 'location':
			case 'resource':
				$mode = isset($formValues['assign-' . $f]) ? $formValues['assign-' . $f] : 'manual';
				break;
			default:
				$mode = 'manual';
				break;
			}
		$currentFlow[] = array( $f, $mode );
		}

	$serviceIndex = 0;
	$timeIndex = 0;
	$i = 0;
	reset( $currentFlow );
	foreach( $currentFlow as $f ){
		if( $f[0] == 'service' )
			$serviceIndex = $i;
		if( $f[0] == 'time' )
			$timeIndex = $i;
		$i++;
		}

	$conf->set( 'appointmentFlow', $currentFlow );
	$conf->set( 'appointmentFlowJustOne', $formValues['appointmentFlowJustOne'] );

	if( ! ($error = $conf->getError()) ){
		ntsView::setAnnounce( M('Settings') . ': ' . M('Update') . ': ' . M('OK'), 'ok' );

	/* continue to form */
		$forwardTo = ntsLink::makeLink( '-current-' );
		ntsView::redirect( $forwardTo );
		exit;
		}
	else {
		$errorText = 'Database error:<BR>' . $error;
		ntsView::addAnnounce( $errorText, 'error' );
		}
	}
?>