<?php
/* receives $msg, $to */
/* returns $success, $response */

//$text = urlencode( $msg );
$text = rawurlencode( $msg );

$user = $plm->getPluginSetting( $plugin, 'username' );
$password = $plm->getPluginSetting( $plugin, 'password' );
$from = $plm->getPluginSetting( $plugin, 'from' );

$baseUrl = 'https://www.textmagic.com/app/api?';
$url = $baseUrl . "?cmd=send&username=$user&password=$password&phone=$to&text=$text&unicode=0";

$http = new ntsHttpClient;
$response = $http->get( $url );

if( $http->isError() ){
	$success = 0;
	$error = $http->getError();
	$this->setError( $error );
	$response = $error;
	}
else {
	// parse response
	$parsed_response = trim( $response );
	$parsed_response = json_decode( $parsed_response, TRUE );
	if( isset($parsed_response['error_message']) ){
		$success = 0;
		$this->setError( $response );
	}
	else {
		$success = 1;
		}
	}
?>