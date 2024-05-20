<?php
$ff =& ntsFormFactory::getInstance();
$attachId = $_NTS['REQ']->getParam('attachid');

$formParams = array();
$formParams['attachid'] = $attachId;

$formFile = dirname( __FILE__ ) . '/form';
$NTS_VIEW['form'] =& $ff->makeForm( $formFile, $formParams );

switch( $action ){
	case 'delete':
		$am = new ntsAttachManager;
		$result = $am->delete( $attachId );

		if( $result )
		{
			ntsView::setAnnounce( M('Attachment') . ': '. M('Delete') . ': ' . M('OK'), 'ok' );
		}
		else
		{
			$errorText = 'Error';
			ntsView::addAnnounce( $errorText, 'error' );
		}
	/* continue to the list with anouncement */
		ntsView::getBack();
		exit;
		break;
	}
?>