<?php
/* check if our customer has any limit */
$customer_id = $this->customerId;
if( ! $customer_id ){
	return;
}

$customer = new ntsUser();
$customer->setId( $customer_id );
$last_date = $customer->getProp('last_date');

if( ! $last_date ){
	return;
}

$customerT = clone $this->customerT;
$customerT->setDateDb( $last_date );
$last_date_view = $customerT->formatDate();

$customerT->modify('+1 day');
$restrict_from = $customerT->getTimestamp();
if( $restrict_from <= $ts ){
	$restrict_to = $customerT->modify('+1 year');
	$restrict_to = $customerT->getTimestamp();

	/* OK REMOVE */
	$return_seats = array();

	$text = M('Last Date For Appointment') . ': ' . $last_date_view . ' ';
	$error = array(
		'customer' => $text
		);
	$this->throwSlotError( $error );

	$this->addGlobalLimit(
		'time',
		array($restrict_from, $restrict_to),
		$error
		);
}
