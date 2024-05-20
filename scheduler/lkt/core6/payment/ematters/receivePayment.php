<?php
/* should return $paymentOk, $paymentAmountGross, $paymentAmountNet $paymentRef, $paymentResponse vars */

/* init */
$paymentOk = true;
$paymentAmountGross = 0;
$paymentAmountNet = 0;

$paymentRef = '';
$paymentResponse = '';
/* end of init */

$RCODE = $_NTS['REQ']->getParam( 'rcode', FALSE ); 
$UID = $_NTS['REQ']->getParam( 'uid', FALSE );
$amount = $_NTS['REQ']->getParam( 'sum', FALSE );

$myMerchantId = $paymentGatewaySettings['merchant_id'];
$checkMerchantId = preg_replace("/[^0-9]/", '', $myMerchantId); // digits only

$bankResponseCode = $RCODE - ( $checkMerchantId * $UID ) - ( $amount * 100 );

if( $bankResponseCode <> 8 ){
	$paymentOk = false;
	}
else {
	$paymentOk = true;
	}
$paymentAmountGross = $amount;
$paymentAmountNet   = $paymentAmountGross; 
$paymentRef         = $UID;
$paymentResponse = $bankResponseCode;

$emattersCodes = array(
	8	=> 'Transaction approved',
	51	=> 'Insufficient funds'
	);
if( isset($emattersCodes[$paymentResponse]) ){
	$paymentResponse = $paymentResponse . ':' . $emattersCodes[$paymentResponse];
	}
?>