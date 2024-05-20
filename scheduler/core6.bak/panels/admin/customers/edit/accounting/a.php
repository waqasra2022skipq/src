<?php
$object = ntsLib::getVar( 'admin/customers/edit::OBJECT' );

$pm =& ntsPaymentManager::getInstance();
$am =& ntsAccountingManager::getInstance();

$entries = $am->get_postings( 'customer', $object->getId() );
$balance = $am->get_balance( 'customer', $object->getId() );

$unpaid_invoices = array();

/* add payment form */
if( isset($balance[0]) && ($balance[0] < 0) )
{
	$due_amount = - $balance[0];

	/* check if we already have unpaid invoices */
	$invoices = $object->getInvoices();
	foreach( $invoices as $ia )
	{
		list( $invoiceId, $myNeededAmount, $due ) = $ia;
		$invoice = ntsObjectFactory::get( 'invoice' );
		$invoice->setId( $invoiceId );
		$paid_amount = $invoice->getPaidAmount();
		$my_amount = $invoice->getItemAmount( $object );
		if( $paid_amount > 0 )
		{
		}
		else
		{
			$due_amount = $due_amount - $my_amount;
			$unpaid_invoices[] = $invoice;
		}
	}
}

if( ! isset($expand) ){
	$expand = array();
}

$view = array(
	'object'			=> $object,
	'entries'			=> $entries,
	'unpaid_invoices'	=> $unpaid_invoices,
	'balance'			=> $balance,
	'am'				=> $am,
	'expand'			=> $expand,
	);

$this->render(
	dirname(__FILE__) . '/index.php',
	$view
	);
?>