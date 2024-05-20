<?php
include_once( dirname(__FILE__) . '/code/PaymentFormHelper.php' );
require( dirname(__FILE__) . '/_config.php' );
require( dirname(__FILE__) . '/code/Config.php' );

$nOutputStatusCode = 30;
$szOutputMessage = "";
$szUpdateOrderMessage = "";
$boErrorOccurred = false;  

try
{
	// read in the transaction result variables
	if (!PaymentFormHelper::getTransactionResultFromPostVariables($_POST, $trTransactionResult, $szHashDigest, $szOutputMessage))
	{
		$nOutputStatusCode = 30;
	}
	else
	{
		if (!PaymentFormHelper::reportTransactionResults($trTransactionResult,
														 $szUpdateOrderMessage))
		{
			$nOutputStatusCode = 30;
			$szOutputMessage = $szOutputMessage.$szUpdateOrderMessage;
		}
		else
		{
			$nOutputStatusCode = 0;
		}
	}
}
catch (Exception $e)
{
	$nOutputStatusCode = 30;
	$szOutputMessage = $szOutputMessage.$e->getMessage();
}
if ($nOutputStatusCode != 0 &&
	$szOutputMessage == "")
{
	$szOutputMessage = "Unknown error";
}
// output the status code and message letting the payment form
// know whether the transaction result was processed successfully
$out = "StatusCode=".$nOutputStatusCode."&Message=".$szOutputMessage;
//echo("StatusCode=".$nOutputStatusCode."&Message=".$szOutputMessage);

if( $nOutputStatusCode == 0 ){
	switch ($trTransactionResult->getStatusCode()){
		case 0:
			$paymentRef = $_POST['CrossReference'];
			$paymentAmountGross = $_POST['Amount'];
			$paymentAmountGross = $paymentAmountGross / 100;
			$paymentOk = true;
			break;
		default:
			$paymentOk = false;
			break;
		}
	}
else {
	$paymentOk = false;
	}
$paymentResponse = $szOutputMessage;

// now we need to notify them back
$statusCode = isset($_POST['StatusCode']) ? $_POST['StatusCode'] : '';
$message = isset($_POST['Message']) ? $_POST['Message'] : '';

//$out .= "paymentRef=".$paymentRef."&paymentAmountGross=".$paymentAmountGross;
echo $out;
?>