<?php
/* receives $msg, $to */
/* returns $success, $response */

//$text = urlencode( $msg );
// $text = rawurlencode( $msg );
$text = $msg;

$sid = $plm->getPluginSetting( $plugin, 'sid' );
$token = $plm->getPluginSetting( $plugin, 'token' );
$from = $plm->getPluginSetting( $plugin, 'from' );

include_once( dirname(__FILE__) . '/lib/Services/Twilio.php');

try {
	$client = new Services_Twilio($sid, $token);
}
catch( Exception $e ){
	$success = 0;
	$error = $e->getMessage();
	$this->setError( $error );
	$response = $error;
	return;
}

try {
	$message = $client->account->messages->sendMessage(
		$from, // From a valid Twilio number
		$to, // Text this number
		$text
	);
}
catch( Exception $e ){
	$success = 0;
	$error = $e->getMessage();
	$this->setError( $error );
	$response = $error;
	return;
}

$success = 1;
$response = $message->sid;