<?php
require( dirname(__FILE__) . '/_config.php' );

// the amount in *minor* currency (i.e. £10.00 passed as "1000")
$szAmount = $paymentAmount * 100;

// the currency	- ISO 4217 3-digit numeric (e.g. GBP = 826)
$szCurrencyCode = strval(826);
// the country code - ISO 3166-1  3-digit numeric (e.g. UK = 826)
$szCountryCode = strval(826);

// order ID
$szOrderID = $paymentOrderRefNo;

// order description
$szOrderDescription = $paymentItemName;

// these variables allow the payment form to be "seeded" with initial values
$szCustomerName = $invoiceInfo['customer']->getProp( 'first_name' ) . ' ' . $invoiceInfo['customer']->getProp( 'last_name' );

$szServerResultURL = $paymentNotifyUrl;
$szCallbackURL = $paymentOkUrl;

require( dirname(__FILE__) . '/code/StartHere.php' );