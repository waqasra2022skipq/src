<?php
$reason = $_NTS['REQ']->getParam( 'reason' );
$overpaid = $_NTS['REQ']->getParam( 'overpaid' );
$commandParams = array(
	'reason' => $reason,
	);

$resultCount = 0;
for( $ii = 0; $ii < count($object); $ii++ ){
	switch( $overpaid ){
		case 'delete':
			$invoices = $object[$ii]->getInvoices();
			foreach( $invoices as $ia ){
				list( $invoiceId, $myNeededAmount, $due ) = $ia;
				$inv = ntsObjectFactory::get('invoice');
				$inv->setId( $invoiceId );
				$cm->runCommand( $inv, 'delete');
			}
			break;
		case 'keep':
			/* do nothing */
			break;
	}

	$cm->runCommand( $object[$ii], 'reject', $commandParams );
	if( $cm->isOk() ){
		$resultCount++;
	}
	else {
		$errorText = $cm->printActionErrors();
		ntsView::addAnnounce( $errorText, 'error' );
		$failedCount++;
		$actionOk = false;
	}
}

if( $resultCount ){
	if( count($object) == 1 )
		$msg = array( M('Appointment'), ntsView::objectTitle($object[0]) );
	else
		$msg = array( $resultCount . ' ' . M('Appointments') );
	$msg[] = M('Reject');
	$msg[] = M('OK');
	$msg = join( ': ' , $msg );
	ntsView::addAnnounce( $msg, 'ok' );
}
?>