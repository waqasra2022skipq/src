<?php
$MerchantID = $paymentGatewaySettings['merchant_id']; //Enter your Gateway MerchantID
$Password = $paymentGatewaySettings['merchant_password']; //Enter your Gateway Password
// This is the PreSharedKey known to both this system and the payment system
// This MUST match the PreSharedKey set for the merchant in the MMS         
$PreSharedKey = $paymentGatewaySettings['preshared_key'];//Enter your Gateway PreSharedKey
?>