<?php
$customer_id = ntsLib::getCurrentUserId();
$aam =& ntsAccountingAssetManager::getInstance();
$am =& ntsAccountingManager::getInstance();

$customer_balance = array();
if( $customer_id )
{
	$customer_balance = $am->get_balance( 'customer', $customer_id );
}

require( dirname(__FILE__) . '/_a_init_objects.php' );

$cm =& ntsCommandManager::getInstance();

/* make invoice */
$pm =& ntsPaymentManager::getInstance();
$items = array();
$amounts = array();
$balance_funded = 0;

reset( $objects );
foreach( $objects as $object )
{
	$app = $object->getByArray();
	$obj_id = $object->getId();

	$default_prepay = $pm->getPrepayAmount( $app );
	$prepay_amount = isset($prepay[$obj_id]) ? $prepay[$obj_id] : $default_prepay;

	if( is_array($prepay_amount) )
	{
		// apply balance
		list( $asset_id, $asset_value ) = $prepay[$obj_id];
		$params = array(
			'asset_id'		=> $asset_id,
			'asset_value'	=> $asset_value,
			);
		$cm->runCommand( $object, 'fund', $params );

		if( $cm->isOk() )
		{
			$balance_funded++;
		}
		else
		{
			$errorText = $cm->printActionErrors();
			ntsView::addAnnounce( $errorText, 'error' );
		}
	}
	else
	{
		if( ! $prepay_amount )
		{
			$prepay_amount = $object->getCost();
		}
		$paid_amount = $object->getPaidAmount();

		if( $prepay_amount > $paid_amount )
		{
			$items[] = $object;
			$amounts[] = ($prepay_amount - $paid_amount);
		}
	}
}

$forwardTo = ntsLink::makeLink( '-current-' );
$invoices = array();

if( $amounts )
{
	$now = time();

// _print_r( $amounts );
// exit;

	// check if we already have unpaid invoices for this amounts
	$item_count = count($items);
	for( $ii = 0; $ii < $item_count; $ii++ ){
		$due_amount = $amounts[$ii];
		$this_invoices = $items[$ii]->getInvoices();

		foreach( $this_invoices as $ia ){
			list( $invoiceId, $myNeededAmount, $due ) = $ia;

			$invoice = ntsObjectFactory::get( 'invoice' );
			$invoice->setId( $invoiceId );
			$paid_amount = $invoice->getPaidAmount();
			$my_amount = $invoice->getItemAmount( $items[$ii] );

			if( $paid_amount > 0 )
			{
			}
			else
			{
				if( $myNeededAmount == $amounts[$ii] ){
					echo 'ALREADY!';
					$invoices = array(
						$invoice
						);
					// ALREADY!
					break;
				}
			}
		}
		if( $invoices ){
			break;
		}
	}

	if( ! $invoices ){
		$invoices = $pm->makeInvoices( $items, $amounts, $now );
	}

	if( isset($invoices[0]) )
	{
		$invoice = $invoices[0];
		$refno = $invoice->getProp('refno');
		$forwardTo = ntsLink::makeLink( 'system/invoice', '', array('refno' => $refno) );
		/* reset session */
		$session = new ntsSession;
		$session->sess_destroy();
	}
	else
	{
		$msg = join( ': ',
			array(
				M('Invoice'),
				M('Create'),
				M('Error'),
				)
			);
		$forwardTo = ntsLink::makeLink( '-current-' );
		ntsView::addAnnounce( $msg, 'error' );
	}
}

if( $balance_funded )
{
	$msg = array();
	if( $balance_funded > 1 )
		$msg[] = $balance_funded . ' ' . M('Appointments');
	else
		$msg[] = M('Appointment');
	$msg[] = M('Pay By Balance');
	$msg[] = M('OK');
	$msg = join( ': ', $msg);
	ntsView::addAnnounce( $msg, 'ok' );
}

/* redirect */
ntsView::redirect( $forwardTo );
exit;
?>