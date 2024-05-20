<?php
/* should return $paymentOk, $paymentAmountGross, $paymentAmountNet, $paymentRef, $paymentResponse vars */
if( ! class_exists('WebToPay') ){
	include_once( dirname(__FILE__) . '/lib/WebToPay.php' );
}

try {
	$response = WebToPay::checkResponse($_GET, array(
		'projectid'			=> $paymentGatewaySettings['projectid'],
		'sign_password'		=> $paymentGatewaySettings['sign_password'],
	 ));

	$paymentOk = 0;
	if( $response['status'] == 1 ){
		$paymentOk = 1;
	}

	$paymentAmountGross = $response['amount'] / 100;
	$paymentAmountNet = $paymentAmountGross;
	$paymentRef = 'Order Id: ' . $response['orderid'];

	$paymentResponse = '';
	foreach( $response as $key => $value ){
		$paymentResponse .= "$key: $value\n";
	}
	// $orderId = $response['orderid'];
	// $currency = $response['currency'];
}

catch (Exception $e){
	// echo get_class($e) . ': ' . $e->getMessage();
	$paymentRef = '';
	$paymentResponse = get_class($e) . ': ' . $e->getMessage();
	$paymentOk = 0;
}
