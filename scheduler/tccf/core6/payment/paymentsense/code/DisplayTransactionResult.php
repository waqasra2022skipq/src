<?php
	require_once ("PaymentFormHelper.php");
	include ("Config.php");

	$Width = 800;
    $FormAction = "";
	include ("Templates/FormHeader.tpl");

	// what we do here depends on the ResultDeliveryMethod
	$DuplicateTransaction = false;
	$PreviousTransactionMessage = "";

	switch ($ResultDeliveryMethod)
	{
		case "POST":
			// the results will be delivered via POST variables to this
			// page	
			$boResultValidationSuccessful = PaymentFormHelper::validateTransactionResult_POST($MerchantID, 
																   							  $Password, 
																							  $PreSharedKey, 
																							  $HashMethod,
																							  $_POST,
																							  $trTransactionResult,
																							  $szValidateErrorMessage);
			// the results need to be stored here as this is the first time
			// they will have touched this system
			if ($boResultValidationSuccessful)
			{
				if (!PaymentFormHelper::reportTransactionResults($trTransactionResult, $szOutputMessage))
				{
					// handle the case where the results aren't stored correctly
				}
			}
			break;
		case "SERVER":
			// the results have already been delivered via a server-to-server
			// call from the payment form to the ServerResultURL
			// need to query these transaction results to display
			$boResultValidationSuccessful = PaymentFormHelper::validateTransactionResult_SERVER($MerchantID, 
																								$Password, 
																								$PreSharedKey, 
																								$HashMethod,
																								$_GET,
																							    $trTransactionResult,
																								$szValidateErrorMessage);
			break;
		case "SERVER_PULL":
			// need to query the results from the payment form using the passed
			// cross reference
			$szPaymentFormResultHandler = "https://mms.".$PaymentProcessorDomain."/Pages/PublicPages/PaymentFormResultHandler.ashx";

			$boResultValidationSuccessful = PaymentFormHelper::validateTransactionResult_SERVER_PULL($MerchantID, 
																									 $Password, 
																									 $PreSharedKey, 
																									 $HashMethod,
																									 $_GET,
																									 $szPaymentFormResultHandler,
																							   		 $trTransactionResult,
																									 $szValidateErrorMessage);
			// the results need to be stored here as this is the first time
			// they will have touched this system
			if ($boResultValidationSuccessful)
			{
				if (!PaymentFormHelper::reportTransactionResults($trTransactionResult, $szOutputMessage))
				{
					// handle the case where the results aren't stored correctly
				}
			}
			break;
	}

	// display an error message if the transaction result couldn't be validated
	if (!$boResultValidationSuccessful)
	{
		$MessageClass = "ErrorMessage";
		$Message = $szValidateErrorMessage;
	}
	else
	{
		switch ($trTransactionResult->getStatusCode())
		{
			case 0:
				$MessageClass = "SuccessMessage";
				break;
			case 4:
				$MessageClass = "ErrorMessage";
				break;
			case 5:
				$MessageClass = "ErrorMessage";
				break;
			case 20:
				$DuplicateTransaction = true;
				if ($trTransactionResult->getPreviousStatusCode() == 0)
				{
					$MessageClass = "SuccessMessage";
				}
				else
				{
					$MessageClass = "ErrorMessage";
				}
				$PreviousTransactionMessage = $trTransactionResult->getPreviousMessage();
				break;
			case 30:
				$MessageClass = "ErrorMessage";
				break;
			default:
				$MessageClass = "ErrorMessage";
				break;

		}

		$Message = $trTransactionResult->getMessage();
	}

	include ("Templates/FinalResultsPanel.tpl");
	include ("Templates/FormFooter.tpl");
?>