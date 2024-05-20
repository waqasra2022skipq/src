<?php
$ff =& ntsFormFactory::getInstance();
$object = ntsLib::getVar( 'admin/company/staff/edit::OBJECT' );

$formFile = dirname( __FILE__ ) . '/form';
$NTS_VIEW['form'] =& $ff->makeForm( $formFile );
$NTS_VIEW['form']->skipRequiredAlert = true;

switch( $action ){
	case 'update_password':
		if( $NTS_VIEW['form']->validate() ){
			$cm =& ntsCommandManager::getInstance();
			$formValues = $NTS_VIEW['form']->getValues();

		/* update password */
			$object->setProp( 'new_password', $formValues['password'] );

			$cm->runCommand( $object, 'update' );
			if( $cm->isOk() ){
				ntsView::addAnnounce( M('Password Changed'), 'ok' );

			/* continue to customer edit */
				$forwardTo = ntsLink::makeLink( '-current-/../edit' );
				ntsView::redirect( $forwardTo );
				exit;
				}
			else {
				$actionError = true;
				$errorString = $cm->printActionErrors();
				}
			}
		else {
		/* form not valid, continue to edit form */
			}
		break;
	}
?>