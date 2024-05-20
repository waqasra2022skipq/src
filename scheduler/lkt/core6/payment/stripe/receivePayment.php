<?php
require_once( dirname(__FILE__) . '/conf.php' );

$customer = $invoice->getCustomer();
$customerEmail = $customer->getProp('email');

$subTotal = $invoice->getSubTotal();
$taxAmount = $invoice->getTaxAmount();
$total = $subTotal + $taxAmount;
$paidAmount = $invoice->getPaidAmount();
$totalDue = $total - $paidAmount;

$token = isset($_POST['stripeToken']) ? $_POST['stripeToken'] : '';

$paymentOk = 0;
$paymentAmountNet = 0;

try {
	$customer = Stripe_Customer::create(
		array(
			'email' => $customerEmail,
			'card'  => $token
		)
	);

	$invoice_objects = $invoice->getItemsObjects();
	$invoiceDetails_Id = $invoice->getProp('refno');

	$invoiceDetails_Title = array();
	$invoiceDetails_Resource = array();
	foreach( $invoice_objects as $invoice_object ){
		$invoiceDetails_Title[] = ntsView::objectTitle( $invoice_object );

		$resource_id = $invoice_object->getProp('resource_id');
		if( $resource_id ){
			$resource = ntsObjectFactory::get('resource');
			$resource->setId( $resource_id );
			$invoiceDetails_Resource[] = ntsView::objectTitle( $resource );
		}
	}
	$invoiceDetails_Title = join(' ', $invoiceDetails_Title);
	$invoiceDetails_Resource = join(' ', $invoiceDetails_Resource);

	$supply = array(
		'customer' => $customer->id,
		'amount'   => (100 * $totalDue),
		'currency' => $paymentCurrency,
		'description'	=> $invoiceDetails_Id . ', ' . $invoiceDetails_Resource . ', ' . $invoiceDetails_Title,
		'metadata'		=> array(
			'item_id'		=> $invoiceDetails_Id,
			'item_title'	=> $invoiceDetails_Title,
			'item_resource'	=> $invoiceDetails_Resource,
			)
		);

	$charge = Stripe_Charge::create( $supply );

	if(
		$charge->paid 
		// && 
		// ($charge->object == 'charge')
		){
		$paymentOk = true;
		$paymentAmountGross = ($charge->amount / 100);
		$fee = 0;
		$paymentAmountNet = $paymentAmountGross - $fee;
		$paymentRef = $charge->id;
	}
	else {
		$paymentOk = 0;
		$paymentAmountNet = 0;
	}
}
catch ( Exception $e ){
	$paymentResponse = $e->getMessage();
}

/*
catch( Stripe_InvalidRequestError $e ){
	$paymentResponse = $e->getMessage();
}
catch( Stripe_AuthenticationError $e ){
	$paymentResponse = $e->getMessage();
}
catch( Stripe_ApiConnectionError $e ){
	$paymentResponse = $e->getMessage();
}
catch( Stripe_Error $e ){
	$paymentResponse = $e->getMessage();
}
catch( Exception $e ){
	$paymentResponse = $e->getMessage();
}
*/
?>