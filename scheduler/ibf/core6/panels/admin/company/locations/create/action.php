<?php
global $_NTS;
$limit_qty = isset($_NTS['limit']['location']) ? $_NTS['limit']['location'] : 0;
if( $limit_qty ){
	$already_have = ntsObjectFactory::getAllIds( 'location' );
	if( count($already_have) >= $limit_qty ){
		$errorText = M('You are not allowed to create more locations');

		ntsView::addAnnounce( $errorText, 'error' );
		$forwardTo = ntsLink::makeLink( '-current-/../browse' );
		ntsView::redirect( $forwardTo );
		exit;
	}
}

$ff =& ntsFormFactory::getInstance();
$formFile = NTS_APP_DIR . '/app/forms/location';
$NTS_VIEW['form'] =& $ff->makeForm( $formFile );

switch( $action ){
	case 'save':
		if( $NTS_VIEW['form']->validate() ){
			$formValues = $NTS_VIEW['form']->getValues();

			$cm =& ntsCommandManager::getInstance();

		/* location */
			$object = ntsObjectFactory::get( 'location' );
			$object->setByArray( $formValues );
			$cm->runCommand( $object, 'create' );

			if( $cm->isOk() ){
				$id = $object->getId();

				$msg = array( M('Location'), ntsView::objectTitle($object), M('Create'), M('OK') );
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