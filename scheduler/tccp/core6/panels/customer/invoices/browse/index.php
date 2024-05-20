<?php
$entries = ntsLib::getVar( 'customer/invoices/browse::entries' );
$t = $NTS_VIEW['t'];
$t->setNow();
$today = $t->formatDate_Db();

$pgm =& ntsPaymentGatewaysManager::getInstance();
$paymentGateways = $pgm->getActiveGateways();
$can_pay_online = TRUE;
if( (count($paymentGateways) == 1) && ($paymentGateways[0] == 'offline') )
	$can_pay_online = false;
?>
<div class="page-header">
	<h2><i class="fa fa-file-text-o"></i> <?php echo M('Invoices'); ?></h2>
</div>

<?php if( ! $entries ) : ?>
	<p>
	<?php echo M('None'); ?>
	</p>
	<?php return; ?>
<?php endif; ?>

<?php foreach( $entries as $e ) : ?>
	<?php
	$total_amount = $e->getTotalAmount();
	$paid_amount = $e->getPaidAmount();
	$total_due = $total_amount - $paid_amount;
	$due_date = $t->formatDate_Db( $e->getProp('due_at') );

	if( $total_due > 0 )
	{
		$status_class = ($today > $due_date) ? 'danger' : 'warning';
	}
	else
	{
		$status_class = 'success';
	}
	?>

	<div class="collapse-panel panel panel-<?php echo $status_class; ?>">
		<div class="panel-heading">
			<div class="pull-right">
				<?php echo ntsCurrency::formatPrice($total_amount); ?>
			</div>
			<h4 class="panel-title">
				<a href="#" data-toggle="collapse-next">
					<?php echo $e->getProp('refno'); ?>
				</a>
			</h4>
		</div>

		<div class="panel-collapse collapse">
			<div class="panel-body">
				<dl class="dl-horizontal">
					<dt>
						<?php echo M('Status'); ?>
					</dt>
					<dd>
						<?php
						$status_label = ( $total_due > 0 ) ? ntsCurrency::formatPrice(-$total_due) : M('Paid');
						?>
						<span class="btn btn-sm btn-<?php echo $status_class; ?>-o">
							<?php echo $status_label; ?>
						</span>
					</dd>

					<dt>
						<?php echo M('Due Date'); ?>
					</dt>
					<dd>
						<?php if( $status_class == 'danger' ) : ?>
							<span class="text-danger">
						<?php endif; ?>
							<?php echo $t->formatDateFull($e->getProp('due_at')); ?>
						<?php if( $status_class == 'danger' ) : ?>
							</span>
						<?php endif; ?>
					</dd>

					<dt>
						<?php echo M('Created'); ?>
					</dt>
					<dd>
						<?php echo $t->formatDateFull($e->getProp('created_at')); ?>
					</dd>

					<dt>
						<?php echo M('Details'); ?>
					</dt>
					<dd>
						<?php echo $e->getFullTitle(); ?>
					</dd>
				</dl>
			</div>

			<div class="panel-footer">
				<?php
				$link_label = ( $can_pay_online && ($total_due > 0) ) ? M('Pay Now') : M('View');
				?>
				<a target="_blank" class="btn btn-<?php echo $status_class; ?>" href="<?php echo ntsLink::makeLink('system/invoice', '', array('refno' => $e->getProp('refno'))); ?>">
					<?php echo $link_label; ?>
				</a>
			</div>
		</div>
	</div>
<?php endforeach; ?>