<?php
$ff =& ntsFormFactory::getInstance();
$object = ntsLib::getVar( 'admin/company/services/edit::OBJECT' );
$formParams = $object->getByArray();

$formFile = dirname( __FILE__ ) . '/form';
$NTS_VIEW['form'] =& $ff->makeForm( $formFile, $formParams );

$pgm =& ntsPaymentGatewaysManager::getInstance();
$payOnline = $pgm->hasOnline();
if( ! $payOnline ){
	// $NTS_VIEW['form']->readonly = true;
}

switch( $action ){
	case 'update':
		if( $NTS_VIEW['form']->validate() ){
			$formValues = $NTS_VIEW['form']->getValues();
			if( $payOnline ){
				$object->setProp( 'prepay', $formValues['prepay'] );
				}
			$object->setProp( 'package_only', $formValues['package_only'] );

			$cm =& ntsCommandManager::getInstance();
			$cm->runCommand( $object, 'update' );

			if( $cm->isOk() ){
				$msg = array( ntsView::objectTitle($object), M('Update'), M('OK') );
				$msg = join( ': ', $msg );
				ntsView::addAnnounce( $msg, 'ok' );

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