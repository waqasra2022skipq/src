<?php
$ff =& ntsFormFactory::getInstance();
$cm =& ntsCommandManager::getInstance();

$item_id = $_NTS['REQ']->getParam('item_id');
ntsView::setPersistentParams( array('item_id' => $item_id), 'admin/payments/invoices/edit/edit/delete_item' );

$invoice = ntsLib::getVar( 'admin/payments/transactions::invoice' );

$formFile = dirname( __FILE__ ) . '/form';
$NTS_VIEW['form'] =& $ff->makeForm( $formFile );

switch( $action )
{
	case 'delete':
		$cm->runCommand( 
			$invoice, 
			'delete_item',
			array(
				'item_id' => $item_id
				) 
			);

		if( $cm->isOk() )
		{
			$msg = array( ntsView::objectTitle($invoice), M('Update'), M('OK') );
			$msg = join( ': ', $msg );
			ntsView::addAnnounce( $msg, 'ok' );
		}
		else
		{
			$errorText = $cm->printActionErrors();
			ntsView::addAnnounce( $errorText, 'error' );
		}

		$forwardTo = ntsLink::makeLink( 
			'-current-/..',
			'',
			array(
				NTS_PARAM_VIEW_RICH	=> '-reset-',
				)
			);
		ntsView::redirect( $forwardTo );
		exit;
		break;
}
?>