<?php
$paymentOkUrl = ntsLink::makeLink( 'customer/invoices/view', '', array('refno' => $invoiceRefNo, 'display' => 'ok') );
$paymentFailedUrl = ntsLink::makeLink( 'customer/invoices/view', '', array('refno' => $invoiceRefNo, 'display' => 'fail') );
$paymentRetryUrl = ntsLink::makeLink( 'system/invoice', '', array('refno' => $invoiceRefNo) );
?>
<?php if( $paymentOk ) : ?>
	<META http-equiv="refresh" content="0;URL=<?php echo $paymentOkUrl; ?>">
<?php else : ?>
	<H2>There's a problem with your payment:</h2>
	<p>
	<?php echo $paymentResponse; ?>
	</p>
	<a href="<?php echo $paymentRetryUrl; ?>"><?php echo M('Please try again'); ?></a>
<?php endif; ?>