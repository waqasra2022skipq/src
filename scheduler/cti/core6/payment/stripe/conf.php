<?php
require_once( dirname(__FILE__) . '/stripe/lib/Stripe.php' );

$skey = $paymentGatewaySettings['skey'];
$pkey = $paymentGatewaySettings['pkey'];
$stripe = array(
	"secret_key"		=> $skey,
	"publishable_key"	=> $pkey,
	);
Stripe::setApiKey($stripe['secret_key']);
?>