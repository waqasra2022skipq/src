<H2><?php echo M('Checking your payment'); ?></H2>

<?php if( isset($NTS_VIEW['payments']) && $NTS_VIEW['payments'] ) : ?>
	<?php
	$payments = $NTS_VIEW['payments'];
	reset( $payments );
	global $NTS_CURRENT_USER;
	$t = $NTS_VIEW['t'];
	?>
	<?php foreach( $payments as $p ) : ?>
		<?php $t->setTimestamp( $p['created_at'] ); ?>
		<p><?php echo $t->formatFull(); ?></p>
		<p><?php echo M('Gateway Response'); ?>:</p>
		<p><?php echo nl2br($p['pgateway_response']); ?></p>
	<?php endforeach; ?>

	<p>
	<a href="<?php echo ntsLink::makeLink('-current-/../pay', '', array('refno' => $NTS_VIEW['invoiceInfo']['refno']) ); ?>"><?php echo M('Please try again'); ?></a>

<?php else : ?>
	<p>
	Trying to check it again in a few moments
	<META http-equiv="refresh" content="2">
<?php endif; ?>