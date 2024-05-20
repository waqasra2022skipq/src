<?php
require_once( dirname(__FILE__) . '/conf.php' );
$customerEmail = $invoiceInfo['customer']->getProp( 'email' );
?>
<FORM ACTION="<?php echo $paymentNotifyUrl; ?>" METHOD=POST>
<script src="https://checkout.stripe.com/checkout.js" class="stripe-button" 
data-key="<?php echo $pkey; ?>" 
data-amount="<?php echo (100 * $paymentAmount); ?>" 
data-currency="<?php echo $paymentCurrency; ?>" 
data-email="<?php echo $customerEmail; ?>" 
data-label="<?php echo $paymentGatewaySettings['label']; ?>" 
data-description="<?php echo $paymentItemName; ?>">
</script>
</FORM>