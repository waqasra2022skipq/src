<?php
$transactionId = $_NTS['REQ']->getParam( 'x_trans_id', FALSE );
$paymentAmountGross = $_NTS['REQ']->getParam( 'x_amount', FALSE );
$paymentAmountGross = sprintf( "%.2f", $paymentAmountGross );

/* authenticate */
$suppliedHash = $_NTS['REQ']->getParam( 'x_MD5_Hash', FALSE );
$suppliedHash = strtolower( $suppliedHash );

$myHash = md5( 
	$paymentGatewaySettings['md5hash'] . 
	$paymentGatewaySettings['login_id'] . 
	$transactionId . 
	$paymentAmountGross
	);

if( $myHash == $suppliedHash ){
	if( $_NTS['REQ']->getParam( 'x_response_code', FALSE ) == 1 ){
		$paymentOk = true;
		$paymentRef = $transactionId;
		$paymentAmountGross = $_NTS['REQ']->getParam( 'x_amount', FALSE );
		$paymentAmountNet = $paymentAmountGross;
		}
	else {
		$paymentOk = false;
		}
	}
else {
	$paymentOk = false;
	}
$paymentResponse = $_NTS['REQ']->getParam( 'x_response_reason_text', FALSE );
?>