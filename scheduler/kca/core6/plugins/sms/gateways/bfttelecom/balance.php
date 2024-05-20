<?php
if( ! function_exists('curl_init') ){
	return;
}

$token = $plm->getPluginSetting( $plugin, 'token' );

$curl = curl_init();
curl_setopt_array($curl, array(
	CURLOPT_URL => "https://apisms.bfttelecom.com.br/balance",
	CURLOPT_RETURNTRANSFER => true,
	CURLOPT_ENCODING => "",
	CURLOPT_MAXREDIRS => 10,
	CURLOPT_TIMEOUT => 30,
	CURLOPT_HTTP_VERSION => CURL_HTTP_VERSION_1_1,
	CURLOPT_CUSTOMREQUEST => "GET",
	CURLOPT_POSTFIELDS => "",
	CURLOPT_HTTPHEADER => array(
		"authorization: Bearer $token"
		),
	)
);

$response = curl_exec($curl);
$err = curl_error($curl);

curl_close($curl);

if( $err ){
	$view = "cURL Error:" . $err;
}
else {
	$parsed_response = json_decode( $response, TRUE );
	if( substr($parsed_response['status'], 0, 1) != 2 ){
		$view = 'Error: ' . 'Status: ' . $parsed_response['status'] . ', Detail: ' . $parsed_response['detail'];
	}
	else {
		$parsed_detail = $parsed_response['detail'];
		$view = 'Saldo: ' . $parsed_detail['saldo'];
	}
}

echo ntsForm::wrapInput(
	'Balance Query',
	$view
	);
