<?php
/* receives $msg, $to */
/* returns $success, $response */

$text = $msg;
$text = addslashes( $text );
$token = $plm->getPluginSetting( $plugin, 'token' );

$curl = curl_init();

$post = array(
	"numero"	=> $to,
	"mensagem"	=> $text
	);
$post = array( $post );
$post = json_encode( $post );

curl_setopt_array($curl, array(
  CURLOPT_URL => "https://apisms.bfttelecom.com.br/mt",
  CURLOPT_RETURNTRANSFER => true,
  CURLOPT_ENCODING => "",
  CURLOPT_MAXREDIRS => 10,
  CURLOPT_TIMEOUT => 30,
  CURLOPT_HTTP_VERSION => CURL_HTTP_VERSION_1_1,
  CURLOPT_CUSTOMREQUEST => "POST",
  CURLOPT_POSTFIELDS => $post,
  CURLOPT_HTTPHEADER => array(
    "authorization: Bearer $token",
    "content-type: application/json"
  ),
));

$response = curl_exec($curl);
$err = curl_error($curl);

curl_close($curl);

if ($err) {
	$success = 0;
	$error = $err;
	$this->setError( $error );
	$response = $error;
  
} else {
	$response = trim( $response );
	$parsed_response = json_decode( $response, TRUE );
	// echo $response . '<br>';
	// _print_r( $parsed_response );
	// exit;

	if( isset($parsed_response['status']) && (substr($parsed_response['status'], 0, 1) == 2) ){
		$success = 1;
		$details = array_shift( $parsed_response['detail'] );
		$response = 'id:' . $details['id'] . ', numero:' . $details['numero'] . ', status:' . $details['status'];
	}
	else {
		$success = 0;
		$error = $parsed_response['status'] . ' ' . $parsed_response['title'] . ' ' . $parsed_response['detail'];
		$response = $error;
		$this->setError( $error );
	}
  // echo $response;
}