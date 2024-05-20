<?php
$entries = ntsLib::getVar( 'system/invoice::entries' );
if( ! count($entries) )
{
	return;
}

$transactionsAmount = ntsLib::getVar( 'system/invoice::transactionsAmount' );

$totalAmount = $invoice ? $invoice->getTotalAmount() : 0;
$dueAmount = ($totalAmount > $transactionsAmount) ? ($totalAmount - $transactionsAmount) : 0;

$t = $NTS_VIEW['t'];
?>

<h3><?php echo M('Payments'); ?></h3>

<ul class="list-unstyled list-padded list-striped">
<?php foreach( $entries as $e ) : ?>
	<li>
		<ul class="list-unstyled row">
			<li class="col-sm-1 text-strong">
				<?php echo ntsCurrency::formatPrice($e->getProp('amount')); ?>
			</li>

			<li class="col-sm-3 text-small text-muted">
				<?php echo $t->formatFull($e->getProp('created_at')); ?>
			</li>

			<li class="col-sm-8">
				<?php echo M( ntsLib::upperCaseMe($e->getProp('pgateway')) ); ?>
			</li>
		</ul>
	</li>
<?php endforeach; ?>
</ul>