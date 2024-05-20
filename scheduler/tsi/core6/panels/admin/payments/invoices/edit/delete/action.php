<?php
$ntsdb =& dbWrapper::getInstance();
$object = ntsLib::getVar( 'admin/payments/invoices/edit::OBJECT' );

$ff =& ntsFormFactory::getInstance();
$NTS_VIEW['form'] =& $ff->makeForm( dirname(__FILE__) . '/form' );

switch( $action )
{
	case 'delete':
		$cm =& ntsCommandManager::getInstance();
		$cm->runCommand( $object, 'delete' );

		if( $cm->isOk() )
		{
			ntsView::setAnnounce( ntsView::objectTitle($object) . ': '. M('Delete') . ': ' . M('OK'), 'ok' );
		}
		else
		{
			$errorText = $cm->printActionErrors();
			ntsView::addAnnounce( $errorText, 'error' );
		}

		/* continue to list */
		$forwardTo = ntsLink::makeLink( '-current-/../../browse' );
		ntsView::redirect( $forwardTo );
		exit;
		break;
}
?>