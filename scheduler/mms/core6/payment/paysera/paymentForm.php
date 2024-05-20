<?php
if( ! class_exists('WebToPay') ){
	include_once( dirname(__FILE__) . '/lib/WebToPay.php' );
}

$test = isset($paymentGatewaySettings['test']) && $paymentGatewaySettings['test'] ? 1 : 0;

$data = array(
	'projectid'			=> $paymentGatewaySettings['projectid'],
	'sign_password'		=> $paymentGatewaySettings['sign_password'],
	// 'sign_password' => 'd41d8cd98f00b204e9800998ecf8427e',
	'orderid'		=> $paymentOrderRefNo,
	'amount'		=> $paymentAmount * 100,
	'currency'		=> strtoupper($paymentCurrency),
	// 'country'       => 'LT',
	'accepturl'		=> $paymentOkUrl,
	'cancelurl'		=> $paymentFailedUrl,
	'callbackurl'	=> $paymentNotifyUrl,
	'test'			=> $test,
	'paytext'		=> $paymentItemName,
	);

// $data['orderid'] = rand(100000, 999999);
	
$factory = new WebToPay_Factory( array('projectId' => $data['projectid'], 'password' => $data['sign_password']));
$url = $factory->getRequestBuilder()
	->buildRequestUrlFromData($data)
	;
?>
<a class="btn btn-default" href="<?php echo $url; ?>"><?php echo $paymentGatewaySettings['label']; ?></a>

<?php
// echo '<br>';
// echo 'SENDING DATA:<br>';
// _print_r( $data );