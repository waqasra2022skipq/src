<?php
global $_NTS;
$limit_qty = isset($_NTS['limit']['staff']) ? $_NTS['limit']['staff'] : 0;
if( $limit_qty ){
	$uif =& ntsUserIntegratorFactory::getInstance();
	$integrator =& $uif->getIntegrator();
	$already_have = $integrator->getAdmins();

	if( count($already_have) >= $limit_qty ){
		$errorText = M('You are not allowed to create more administrative users');

		ntsView::addAnnounce( $errorText, 'error' );
		$forwardTo = ntsLink::makeLink( '-current-/../browse' );
		ntsView::redirect( $forwardTo );
		exit;
	}
}

$class = 'user';
$ff =& ntsFormFactory::getInstance();
$formFile = dirname( __FILE__ ) . '/form';
$NTS_VIEW['form'] =& $ff->makeForm( $formFile );

switch( $action ){
	case 'create':
		$removeValidation = array();
		if( NTS_ALLOW_NO_EMAIL && $_NTS['REQ']->getParam('noEmail') ){
			$removeValidation[] = 'email';
			}

		if( $NTS_VIEW['form']->validate($removeValidation) ){
			$formValues = $NTS_VIEW['form']->getValues();
			if( isset($formValues['noEmail']) && $formValues['noEmail'] )
				$formValues['email'] = '';

			$cm =& ntsCommandManager::getInstance();

		/* object */
			$object = new ntsUser();
			unset( $formValues['password2'] );
			$object->setByArray( $formValues );
			$object->setProp('_role', array('admin') );

		/* default permissions as by creating user */
			global $NTS_CURRENT_USER;
			$object->setProp( '_disabled_panels', $NTS_CURRENT_USER->getProp('_disabled_panels') ); 

			$cm->runCommand( $object, 'create' );

			if( $cm->isOk() ){
				$cm->runCommand( $object, 'activate' );

				$id = $object->getId();
				$announce = join(': ', array(M('Administrative User'), ntsView::objectTitle($object), M('Create'), M('OK')) );
				ntsView::addAnnounce( $announce, 'ok' );

			/* continue to edit with anouncement */
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
			if (isset($_POST['nts-source'])) {
				echo json_encode([
					'status' => false,
					'user' => 'admin',
					'data' => 'username already exist... Please try again with different username/email.'
				]);die;
			}
		/* form not valid, continue to create form */
			}
		break;
	default:
		break;
	}
?>