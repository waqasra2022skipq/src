<?php
	require_once ("PaymentFormHelper.php");
	require( dirname(__FILE__) . "/Config.php" );

	$Width = 800;
	$FormAction = "https://mms.".$PaymentProcessorDomain."/Pages/PublicPages/PaymentForm.aspx";
	include ("Templates/FormHeader.tpl");

	// the transaction type - can be SALE or PREAUTH
	$szTransactionType = "SALE";
	// the GMT/UTC relative date/time for the transaction (MUST either be in GMT/UTC 
	// or MUST include the correct timezone offset)
	
	$ts = time();
//	$ts = $ts - 1 * 60 * 60;
	$szTransactionDateTime = gmdate('Y-m-d H:i:s', $ts);
//	$szTransactionDateTime = '2013-01-15 16:19:11';
	
	$szAddress1 = "";
	$szAddress2 = "";
	$szAddress3 = "";
	$szAddress4 = "";
	$szCity = "";
	$szState = "";
	$szPostCode = "";
	// use these to control which fields on the hosted payment form are
	// mandatory
	$szCV2Mandatory = PaymentFormHelper::boolToString(true);
	$szAddress1Mandatory = PaymentFormHelper::boolToString(false);
	$szCityMandatory = PaymentFormHelper::boolToString(false);
	$szPostCodeMandatory = PaymentFormHelper::boolToString(false);
	$szStateMandatory = PaymentFormHelper::boolToString(false);
	$szCountryMandatory = PaymentFormHelper::boolToString(false);
	// the URL on this system that the payment form will push the results to (only applicable for 
	// ResultDeliveryMethod = "SERVER")
	if ($ResultDeliveryMethod != "SERVER")
	{
		$szServerResultURL = "";
	}
	else
	{
//		$szServerResultURL = PaymentFormHelper::getSiteSecureBaseURL()."ReceiveTransactionResult.php";
	}
	// set this to true if you want the hosted payment form to display the transaction result
	// to the customer (only applicable for ResultDeliveryMethod = "SERVER")
	if ($ResultDeliveryMethod != "SERVER")
	{
		$szPaymentFormDisplaysResult = "";
	}
	else
	{
		$szPaymentFormDisplaysResult = PaymentFormHelper::boolToString(false);
	}
	// the callback URL on this site that will display the transaction result to the customer
	// (always required unless ResultDeliveryMethod = "SERVER" and PaymentFormDisplaysResult = "true")
	if ($ResultDeliveryMethod == "SERVER" && PaymentFormHelper::stringToBool($szPaymentFormDisplaysResult) == false)
	{
//		$szCallbackURL = "http://paymentgatewayuk.com/PHP/HostedSample/DisplayTransactionResult.php";
	}
	else
	{
//		$szCallbackURL = "http://paymentgatewayuk.com/PHP/HostedSample/DisplayTransactionResult.php"; 
	}

	// get the string to be hashed
	$szStringToHash = PaymentFormHelper::generateStringToHash($MerchantID,
			        										  $Password,
			        										  $szAmount,
															  $szCurrencyCode,
															  $szOrderID,
															  $szTransactionType,
															  $szTransactionDateTime,
															  $szCallbackURL,
															  $szOrderDescription,
															  $szCustomerName,
															  $szAddress1,
															  $szAddress2,
															  $szAddress3,
															  $szAddress4,
															  $szCity,
															  $szState,
															  $szPostCode,
															  $szCountryCode,
															  $szCV2Mandatory,
															  $szAddress1Mandatory,
															  $szCityMandatory,
															  $szPostCodeMandatory,
															  $szStateMandatory,
															  $szCountryMandatory,
															  $ResultDeliveryMethod,
															  $szServerResultURL,
															  $szPaymentFormDisplaysResult,
			         		                                  $PreSharedKey,
			         		                                  $HashMethod);

	// pass this string into the hash function to create the hash digest
	$szHashDigest = PaymentFormHelper::calculateHashDigest($szStringToHash,
                        								   $PreSharedKey, 
                        								   $HashMethod);

	include ("Templates/StartHereForm.tpl");
	include ("Templates/FormFooter.tpl");
?>