	<input type="hidden" name="HashDigest" value="<?php echo $szHashDigest ?>" />
	<input type="hidden" name="MerchantID" value="<?php echo $MerchantID ?>" />
	<input type="hidden" name="Amount" value="<?php echo $szAmount ?>" />
	<input type="hidden" name="CurrencyCode" value="<?php echo $szCurrencyCode ?>" />
	<input type="hidden" name="OrderID" value="<?php echo $szOrderID ?>" />
	<input type="hidden" name="TransactionType" value="<?php echo $szTransactionType ?>" />
	<input type="hidden" name="TransactionDateTime" value="<?php echo $szTransactionDateTime ?>" />
	<input type="hidden" name="CallbackURL" value="<?php echo $szCallbackURL ?>" />
	<input type="hidden" name="OrderDescription" value="<?php echo $szOrderDescription ?>" />
	<input type="hidden" name="CustomerName" value="<?php echo $szCustomerName ?>" />
	<input type="hidden" name="Address1" value="<?php echo $szAddress1 ?>" />
	<input type="hidden" name="Address2" value="<?php echo $szAddress2 ?>" />
	<input type="hidden" name="Address3" value="<?php echo $szAddress3 ?>" />
	<input type="hidden" name="Address4" value="<?php echo $szAddress4 ?>" />
	<input type="hidden" name="City" value="<?php echo $szCity ?>" />
	<input type="hidden" name="State" value="<?php echo $szState ?>" />
	<input type="hidden" name="PostCode" value="<?php echo $szPostCode ?>" />
	<input type="hidden" name="CountryCode" value="<?php echo $szCountryCode ?>" />
	<input type="hidden" name="CV2Mandatory" value="<?php echo $szCV2Mandatory ?>" />
	<input type="hidden" name="Address1Mandatory" value="<?php echo $szAddress1Mandatory ?>" />
	<input type="hidden" name="CityMandatory" value="<?php echo $szCityMandatory ?>" />
	<input type="hidden" name="PostCodeMandatory" value="<?php echo $szPostCodeMandatory ?>" />
	<input type="hidden" name="StateMandatory" value="<?php echo $szStateMandatory ?>" />
	<input type="hidden" name="CountryMandatory" value="<?php echo $szCountryMandatory ?>" />
	<input type="hidden" name="ResultDeliveryMethod" value="<?php echo $ResultDeliveryMethod ?>" />
	<input type="hidden" name="ServerResultURL" value="<?php echo $szServerResultURL ?>" />
	<input type="hidden" name="PaymentFormDisplaysResult" value="<?php echo $szPaymentFormDisplaysResult ?>" />
	<input type="hidden" name="ServerResultURLCookieVariables" value="" />
	<input type="hidden" name="ServerResultURLFormVariables" value="" />
	<input type="hidden" name="ServerResultURLQueryStringVariables" value="" />
	

<input type="submit" value="<?php echo $paymentGatewaySettings['label']; ?>">

