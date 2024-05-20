<?php
$object = ntsLib::getVar( 'admin/manage/appointments/edit::OBJECT' );

/* add payment */
$ff =& ntsFormFactory::getInstance();
$form_file = NTS_APP_DIR . '/panels/admin/payments/transactions/add/form';
$form_params = array(
	);
$form =& $ff->makeForm( $form_file, $form_params );

if( $form->validate() )
{
	$form_values = $form->getValues();

	$amount = $form_values['amount'];
	$notes = $form_values['notes'];
	$pgateway = $form_values['type'];

	$paymentInfo = array(
		'pgateway'			=> $pgateway,
		'pgateway_response'	=> $notes
		);

	$invoice_amount = $amount;
	$pm =& ntsPaymentManager::getInstance();
	$tax_rate = $pm->getTaxRate( $object ); 
	if( $tax_rate )
	{
		$invoice_amount = ntsLib::removeTax( $amount, $tax_rate );
	}

	$now = time();
	$pm =& ntsPaymentManager::getInstance();
	$invoices = $pm->makeInvoices(
		array( $object ),
		array( $invoice_amount ),
		$now
		);

	if( $invoices && is_array($invoices) && isset($invoices[0]))
	{
		$invoice_id = $invoices[0]->getId();
		$trans_id = $pm->makeTransaction( 
			$amount,
			$invoice_id,
			$paymentInfo
			);

		$amountFormatted = ntsCurrency::formatPrice( $amount );
		$msg = array( M('Payment'), $amountFormatted, M('Add'), M('OK') );
		$msg = join( ': ', $msg );
		ntsView::addAnnounce( $msg, 'ok' );
	}

	$forwardTo = ntsLink::makeLink( '-current-' );
	ntsView::redirect( $forwardTo );
	exit;
}
else
{
	require( dirname(__FILE__) . '/a.php' );
}

?>