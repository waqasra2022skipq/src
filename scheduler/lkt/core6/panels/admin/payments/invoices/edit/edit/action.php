<?php
$ff =& ntsFormFactory::getInstance();
$cm =& ntsCommandManager::getInstance();

$invoice = ntsLib::getVar( 'admin/payments/transactions::invoice' );
$transactions = $invoice->getTransactions();
ntsLib::setVar( 'admin/payments/transactions::entries', $transactions );

$count = count( $transactions );
ntsLib::setVar( 'admin/payments/transactions::totalCount', $count );

$limit = 0;
ntsLib::setVar( 'admin/payments/transactions::limit', $limit );

$calc = new ntsMoneyCalc;
$transactionsAmount = 0;
reset( $transactions );
foreach( $transactions as $tr )
{
	$calc->add( $tr->getProp('amount') );
}
$transactionsAmount = $calc->result();
ntsLib::setVar( 'admin/payments/transactions::transactionsAmount', $transactionsAmount );

$formParams = array();
$formNewFile = dirname( __FILE__ ) . '/formNew';
$NTS_VIEW['formNew'] =& $ff->makeForm( $formNewFile, $formParams );

$t = $NTS_VIEW['t'];
$t->setTimestamp( $invoice->getProp('due_at') );
$due_at = $t->formatDate_Db();
$formParams = array(
	'due_at'	=> $due_at
	);
$formDueDate = dirname( __FILE__ ) . '/formDueDate';
$NTS_VIEW['formDueDate'] =& $ff->makeForm( $formDueDate, $formParams );

switch( $action )
{
	case 'updatedate':
		if( $NTS_VIEW['formDueDate']->validate() )
		{
			$formValues = $NTS_VIEW['formDueDate']->getValues();
			$t->setDateDb( $formValues['due_at'] );
			$due_at = $t->getTimestamp();
			$invoice->setProp( 'due_at', $due_at );
			$cm->runCommand( 
				$invoice, 
				'update'
				);

			if( $cm->isOk() ){
				$msg = array( ntsView::objectTitle($invoice), M('Update'), M('OK') );
				$msg = join( ': ', $msg );
				ntsView::addAnnounce( $msg, 'ok' );
			}
			else {
				$errorText = $cm->printActionErrors();
				ntsView::addAnnounce( $errorText, 'error' );
			}

			$forwardTo = ntsLink::makeLink( '-current-' );
			ntsView::redirect( $forwardTo );
			exit;
		}
		break;

	case 'add':
		if( $NTS_VIEW['formNew']->validate() )
		{
			$formValues = $NTS_VIEW['formNew']->getValues();
			$cm->runCommand( 
				$invoice, 
				'add_item', 
				array(
					'item' => $formValues
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

			$forwardTo = ntsLink::makeLink( '-current-' );
			ntsView::redirect( $forwardTo );
			exit;
		}
		break;
}


//ntsLib::setViewParams( $view, __FILE__ );
?>