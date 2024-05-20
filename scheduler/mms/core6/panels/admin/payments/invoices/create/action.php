<?php
$customer_id = ntsLib::getVar( 'admin/payments/invoices::customer' );
if( ! $customer_id )
{
	echo 'customer is required!';
	exit;
}

$invoice = ntsObjectFactory::get( 'invoice' );
//$invoice->setProp( 'due_at', $due );
$invoice->setProp( 'customer_id', $customer_id );

$cm =& ntsCommandManager::getInstance();
$cm->runCommand( $invoice, 'create' );
$invoice_id = $invoice->getId();

$msg = array( M('Invoice'), M('Add'), M('OK') );
$msg = join( ': ', $msg );
ntsView::addAnnounce( $msg, 'ok' );

$forwardTo = ntsLink::makeLink( 'admin/payments/invoices/edit/edit', '', array('_id' => $invoice_id) );
ntsView::redirect( $forwardTo );
?>