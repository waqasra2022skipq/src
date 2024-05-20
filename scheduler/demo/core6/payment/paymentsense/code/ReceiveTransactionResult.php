<?php
	require_once ("PaymentFormHelper.php");
	include ("Config.php");

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
	echo("StatusCode=".$nOutputStatusCode."&Message=".$szOutputMessage);
?>