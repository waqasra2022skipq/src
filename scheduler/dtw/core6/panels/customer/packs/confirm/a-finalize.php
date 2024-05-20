<?php
require( dirname(__FILE__) . '/../_a_init_pack.php' );

$cm =& ntsCommandManager::getInstance();

$pack_id = $pack->getId();

$order = ntsObjectFactory::get( 'order' );
$order->setProp( 'customer_id', $customer_id );
$order->setProp( 'pack_id', $pack_id );

$session = new ntsSession;
$apps = $session->userdata('apps');
$coupon = $session->userdata('coupon');

$params = array(
	'coupon'	=> $coupon
	);

$cm->runCommand( $order, 'create', $params );

/* find invoice */
$invoices = $order->getInvoices();
if( $invoices && isset($invoices[0]) )
{
	$invoice = ntsObjectFactory::get( 'invoice' );
	$invoice->setId( $invoices[0][0] );
	$refno = $invoice->getProp('refno');
	$forwardTo = ntsLink::makeLink('system/invoice', '', array('refno' => $refno));
	ntsView::redirect( $forwardTo );
}
else
{
	echo 'error creating invoices';
}

//$forwardTo = ntsLink::makeLink('customer/appointments/view', '', array('ref' => $ref));
//ntsView::redirect( $forwardTo );
exit;
?>