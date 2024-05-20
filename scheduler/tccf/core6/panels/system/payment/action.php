<?php
$ntsdb =& dbWrapper::getInstance();
$conf =& ntsConf::getInstance();

$outFile = NTS_APP_DIR . '/../paylog.txt';

$gateway = $_NTS['REQ']->getParam( 'gateway' );
if( ! $gateway ){
	$msg = "gateway required!";
	echo $msg;

	if( file_exists($outFile) ){
		$fp = fopen( $outFile, 'a' );
		fwrite( $fp, $msg . "\n\n" );
		fclose($fp);
	}

	exit;
}

/* payment manager */
$pgm =& ntsPaymentGatewaysManager::getInstance();
$paymentGateways = $pgm->getActiveGateways();

if(! in_array($gateway, $paymentGateways)){
	$msg = "gateway '$gateway' not found!";

	echo $msg;
	if( file_exists($outFile) ){
		$fp = fopen( $outFile, 'a' );
		fwrite( $fp, $msg . "\n\n" );
		fclose($fp);
	}

	exit;
}

$paymentGatewaySettings = $pgm->getGatewaySettings( $gateway );

$invoiceRefNo = '';

/* include gateway file to get invoice no */
$gatewayFile = $pgm->getGatewayFolder( $gateway ) . '/receivePayment_before.php';
if( file_exists( $gatewayFile ) )
	require( $gatewayFile );
else
	$invoiceRefNo = $_NTS['REQ']->getParam( 'refno' );

if( ! $invoiceRefNo ){
	$msg = "invoiceRefNo required!";

	echo $msg;
	if( file_exists($outFile) ){
		$fp = fopen( $outFile, 'a' );
		fwrite( $fp, $msg . "\n\n" );
		fclose($fp);
	}

	exit;
}

$invoiceId = 0;
$result = $ntsdb->select( 'id', 'invoices', array('refno' => array('=', $invoiceRefNo)) );
if( $i = $result->fetch() ){
	$invoiceId = $i['id'];
	}

if( ! $invoiceId ){
	$msg = "invoice '$invoiceRefNo' not found!";

	echo $msg;
	if( file_exists($outFile) ){
		$fp = fopen( $outFile, 'a' );
		fwrite( $fp, $msg . "\n\n" );
		fclose($fp);
	}

	exit;
}

$invoice = ntsObjectFactory::get( 'invoice' );
$invoice->setId( $invoiceId );

$paymentOk = true;
$paymentAmountGross = 100;
$paymentAmountNet = 95;
$paymentCurrency = $conf->get( 'currency' );
$paymentRef = 'abc';
$paymentResponse = 'resp from payment gateway';

/* process payment */
$gatewayFile = $pgm->getGatewayFolder( $gateway ) . '/receivePayment.php';
require( $gatewayFile );

$cm =& ntsCommandManager::getInstance();

/* if payment is ok */
if( $paymentOk ){
	header("Status: 200");
	$now = time();

	if( $paymentAmountGross ){
		$pm =& ntsPaymentManager::getInstance();
		$paymentParams = array(
			'amount_net'		=> $paymentAmountNet,
			'pgateway'			=> $gateway,
			'pgateway_ref'		=> $paymentRef,
			'pgateway_response'	=> $paymentResponse,
			);
		$transId = $pm->makeTransaction( $paymentAmountGross, $invoiceId, $paymentParams );
		}
	}
else {
	$pm =& ntsPaymentManager::getInstance();
	$paymentAmountGross = $paymentAmountNet = 0;
	$paymentParams = array(
		'amount_net'		=> $paymentAmountNet,
		'pgateway'			=> $gateway,
		'pgateway_ref'		=> $paymentRef,
		'pgateway_response'	=> $paymentResponse,
		);
	$transId = $pm->makeTransaction( $paymentAmountGross, $invoiceId, $paymentParams );
	}

/* add log */

if( file_exists($outFile) ){
	$paramsArray = array();
	$date = date( "F j, Y, g:i a", time() );
	$paramsArray['created_at'] = $date;
	$paramsArray['invoice'] = $invoiceId . ':' . $invoiceRefNo;
	$paramsArray['gateway'] = $gateway;
	$paramsArray['response'] = $paymentResponse;
	$paramsArray['ref'] = $paymentRef;
	$paramsArray['amount'] = $paymentAmountNet;

	$text = array();
	foreach( $paramsArray as $k => $v ){
//		$v = str_replace( "\n", "", $v );
		$text[] = $k . ':' . $v;
		}
	$text = join( "\n", $text );

	$fp = fopen( $outFile, 'a' );
	fwrite( $fp, $text . "\n\n" );
	fclose($fp);
	}

/* after payment */
$gatewayFile = $pgm->getGatewayFolder( $gateway ) . '/receivePayment_after.php';
if( file_exists( $gatewayFile ) )
	require( $gatewayFile );

exit;
?>