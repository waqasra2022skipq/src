<?php
$object = ntsLib::getVar( 'admin/manage/appointments/edit::OBJECT' );

$now = time();
$due_amount = $object->getDue();

/* create invoice */
$pm =& ntsPaymentManager::getInstance();
$invoices = $pm->makeInvoices(
	array( $object ),
	array( $due_amount ),
	$now
	);

if( $invoices && is_array($invoices) && isset($invoices[0]))
{
	$invoice_id = $invoices[0]->getId();
	$msg = array( M('Invoice'), M('Add'), M('OK') );
	$msg = join( ': ', $msg );
	ntsView::addAnnounce( $msg, 'ok' );
	$forwardTo = ntsLink::makeLink( 'admin/payments/invoices/edit/edit', '', array('_id' => $invoice_id) );
}
else
{
	$msg = array( M('Invoice'), M('Add'), M('Error') );
	$msg = join( ': ', $msg );
	ntsView::addAnnounce( $msg, 'error' );
	$forwardTo = ntsLink::makeLink( '-current-' );
}

ntsView::redirect( $forwardTo );
?>