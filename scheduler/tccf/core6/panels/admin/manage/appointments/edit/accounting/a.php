<?php
$object = ntsLib::getVar( 'admin/manage/appointments/edit::OBJECT' );

$pm =& ntsPaymentManager::getInstance();
$am =& ntsAccountingManager::getInstance();
$entries = $am->get_postings( $object->getClassName(), $object->getId() );

$due_amount = $object->getDue();
$payment_balance = - $due_amount;

$unpaid_invoices = array();

/* add payment form */
if( ! isset($form) )
{
	$form = NULL;
}
if( ! isset($discount_form) )
{
	$discount_form = NULL;
}

/* due amount */
$customer_balance = array();
$balance_cover = array();

if( $due_amount > 0 )
{
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

	$ff =& ntsFormFactory::getInstance();
	if( $due_amount > 0 )
	{
		$form_file = NTS_APP_DIR . '/panels/admin/payments/transactions/add/form';

		$tax_rate = $pm->getTaxRate( $object );
		$tax = ntsLib::calcTax( $due_amount, $tax_rate );
		$total_amount = $due_amount + $tax;

		$form_params = array(
			'amount'	=> $total_amount,
			'tax_rate'	=> $tax_rate,
			);
		if( ! isset($form) )
		{
			$form =& $ff->makeForm( $form_file, $form_params );
		}

		/* customer balance */
		$customer_id = $object->getProp('customer_id');
		$customer_balance = $am->get_balance( 'customer', $customer_id );
		$balance_cover = $am->balance_cover( $customer_balance, $object );
	}

	if( ! isset($discount_form) )
	{
		$discount_form_file = dirname(__FILE__) . '/form-discount';
		$discount_form =& $ff->makeForm( $discount_form_file );
	}
}

$coupon_applied = FALSE;
/* check if a coupon has already been implemented */
reset( $entries );
foreach( $entries as $e )
{
	if( 
		($e['obj_class'] == 'coupon') &&
		($e['action'] == 'apply')
		)
	{
		$coupon_applied = TRUE;
		break;
	}
}

$coupon_promotions = array();
if( ! $coupon_applied )
{
	$r = $object->getByArray();

	$coupon_promotions = array();
	$all_promotions = $pm->getPromotions( $r, '', TRUE );

	foreach( $all_promotions as $pr ){
		$this_codes = $pr->getCouponCodes();
		reset( $this_codes );
		foreach( $this_codes as $this_code ){
			$this_promotions = $pm->getPromotions( $r, $this_code, FALSE );
			if( $this_promotions ){
				$coupon_promotions = array_merge( $coupon_promotions, $this_promotions );
			}
		}
	}
}

$service = ntsObjectFactory::get('service');
$service->setId( $object->getProp('service_id') );

reset( $entries );
$view = array(
	'coupon_promotions'	=> $coupon_promotions,
	'object'			=> $object,
	'service'			=> $service,
	'entries'			=> $entries,
	'unpaid_invoices'	=> $unpaid_invoices,
	'payment_balance'	=> $payment_balance,
	'am'				=> $am,
	'form'				=> $form,
	'discount_form'		=> $discount_form,
	'balance_cover'		=> $balance_cover,
	'customer_balance'	=> $customer_balance,
	);

$this->render(
	dirname(__FILE__) . '/index.php',
	$view
	);
?>