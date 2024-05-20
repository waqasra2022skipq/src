<?php
	// Will need to set these variables to valid a MerchantID and Password
	// These were obtained during sign up
//	$MerchantID = ""; //Enter your Gateway MerchantID
//	$Password = ""; //Enter your Gateway Password
	// This is the PreSharedKey known to both this system and the payment system
	// This MUST match the PreSharedKey set for the merchant in the MMS         
//	$PreSharedKey = "";//Enter your Gateway PreSharedKey
	
	// The domain ONLY for the hosted payment form - e.g. if the hosted payment form URL is
	// https://mms.paymentprocessor.net/Pages/PublicPages/PaymentForm.aspx, then the domain
	// will be "paymentprocessor.net"

	$PaymentProcessorDomain = "paymentsensegateway.com";

	// The chosen hash method - can be either "MD5", "SHA1", "HMACMD5" or "HMACSHA1"
	// This method MUST match the hash method set for the merchant in the MMS
	$HashMethod = "SHA1";

	// determines how the transaction result will be delivered back to this site:
	// "POST" - only use if this site has an SSL certificate. Best method to use if you do have an SSL
	// "SERVER" - best method with no SSL - don't use if this site requires to maintain 
	//			  cookie-based session to access its order object)
	// "SERVER_PULL" - only use if no SSL and site also requires cookie-based session to access 
	//			  	   its order object
//	$ResultDeliveryMethod = "POST";
	$ResultDeliveryMethod = "SERVER";
?>
