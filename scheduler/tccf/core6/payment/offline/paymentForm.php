<form method="post" action="<?php echo $paymentNotifyUrl; ?>">
<input class="btn btn-default" type="submit" value="<?php echo ( isset($paymentGatewaySettings['label']) ) ? $paymentGatewaySettings['label'] : 'Pay at our office'; ?>">
</form>