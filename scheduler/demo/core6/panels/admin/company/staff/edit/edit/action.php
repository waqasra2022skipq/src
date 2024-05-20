<?php
$ff =& ntsFormFactory::getInstance();
$object = ntsLib::getVar( 'admin/company/staff/edit::OBJECT' );

$formParams = $object->getByArray();
$formFile = dirname( __FILE__ ) . '/form';
$NTS_VIEW['form'] =& $ff->makeForm( $formFile, $formParams );

switch( $action ){
	case 'update':
		if( $NTS_VIEW['form']->validate() ){
			$formValues = $NTS_VIEW['form']->getValues();

			$object->setByArray( $formValues );

			$cm =& ntsCommandManager::getInstance();
			$cm->runCommand( $object, 'update' );

			if( $cm->isOk() ){
				$announce = join(': ', array(M('Administrative User'), ntsView::objectTitle($object), M('Update'), M('OK')) );
				ntsView::addAnnounce( $announce, 'ok' );

			/* continue to the list with anouncement */
				$forwardTo = ntsLink::makeLink( '-current-/../../browse' );
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