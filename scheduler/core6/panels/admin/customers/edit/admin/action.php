<?php
$ff =& ntsFormFactory::getInstance();
$cm =& ntsCommandManager::getInstance();
$object = ntsLib::getVar( 'admin/customers/edit::OBJECT' );

$formFile = dirname( __FILE__ ) . '/form';
$formParams['id'] = $object->getId();

$NTS_VIEW['form'] =& $ff->makeForm( $formFile, $formParams );

switch( $action ){

	case 'update':
		if( $NTS_VIEW['form']->validate() ){
			$cm =& ntsCommandManager::getInstance();
			$formValues = $NTS_VIEW['form']->getValues();

			$object->setProp('_role', array('admin') );
			$object->setProp('_admin_level', $formValues['_admin_level'] );

			$cm->runCommand( $object, 'update' );
			if( $cm->isOk() ){
				ntsView::addAnnounce( M('User') . ': ' . M('Update'), 'ok' );

			/* continue to customer edit */
				$forwardTo = ntsLink::makeLink( 'admin/company/staff/edit/edit', '', array('_id' => $object->getId()) );
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