<?php
$aam =& ntsAccountingAssetManager::getInstance();
$t = $NTS_VIEW['t'];

$ntspm =& ntsPaymentManager::getInstance();

$coupon = '';
$show_coupon = $coupon_promotions ? TRUE : FALSE;

$base_price = $ntspm->getBasePrice( $object );
$service_price = $service->getProp('price');
$seats = $object->getProp('seats');

$uncovered_balance = $payment_balance;
if( $unpaid_invoices ){
	reset( $unpaid_invoices );
	foreach( $unpaid_invoices as $ui ){
		$amount = $ui->getTotalAmount();
		$uncovered_balance += $amount;
	}
}
?>

<?php if( strlen($base_price) ) : ?>
	<ul class="list-inline list-separated">
		<?php if( ($seats * $service_price) != $base_price ) : ?>
			<li>
				<?php echo M('Service'); ?>
			</li>
			<li>
				<span class="btn btn-default">
					<?php echo ntsCurrency::formatPrice($service_price); ?>
				</span>
			</li>
		<?php endif; ?>
		<li>
			<?php echo M('Full Price'); ?>
		</li>
		<li>
			<span class="btn btn-default">
				<?php echo ntsCurrency::formatPrice($base_price); ?>
				<?php if( $seats > 1 ) : ?>
					<span class="text-muted">(<?php echo $seats; ?> x <?php echo ntsCurrency::formatPrice($base_price/$seats); ?>)</span>
				<?php endif; ?>

			</span>
		</li>

		<?php if( $show_coupon ) : ?>
			<li>
				<?php require( dirname(__FILE__) . '/_form_coupon_options.php' ); ?>
			</li>
		<?php endif; ?>

		<?php if( $uncovered_balance < 0 ) : ?>
			<li>
				<a href="<?php echo ntsLink::makeLink('-current-', 'create-invoice'); ?>" class="btn btn-success-o">
					<i class="fa fa-plus"></i> <?php echo join( ': ', array( M('Invoice'), M('Create') ) ); ?> [<?php echo ntsCurrency::formatPrice(-$uncovered_balance); ?>]
				</a>
			</li>
		<?php endif; ?>
	</ul>
<?php endif; ?>

<?php if( $entries ) : ?>
	<p>
	<h3><?php echo M('History'); ?></h3>

	<p>
	<table class="table table-striped">
	<?php foreach( $entries as $e ) : ?>
		<?php
		$e['object'] = ntsObjectFactory::get( $e['obj_class'] );
		$e['object']->setId( $e['obj_id'] );
		?>
		<tr>
			<td>
				<?php
				$t->setTimestamp( $e['created_at'] );
				echo $t->formatFull();
				?>
			</td>
			<td>
				<?php echo $am->journal_label($e); ?>

				<?php if( $e['obj_class'] == 'coupon' ) : ?>
					<a class="nts-no-ajax btn btn-sm btn-danger-o hc-confirm" href="<?php echo ntsLink::makeLink('-current-', 'release-coupon', array('coupon_id' => $e['obj_id'] )); ?>">
						<i class="fa-fw fa fa-times text-danger"></i><span class="hidden-xs"><?php echo M('Delete'); ?></span>
					</a>
				<?php endif; ?>

				<?php if( $e['obj_class'] == 'transaction' ) : ?>
					<?php
					$tra = $e['object'];
					$invoice_id = $tra->getProp('invoice_id');
					$invoice = ntsObjectFactory::get('invoice');
					$invoice->setId( $invoice_id );
					$invoice_view = $invoice->getProp('refno');
					?>
					[<a target="_blank" class="nts-no-ajax" href="<?php echo ntsLink::makeLink('admin/payments/invoices/edit/edit', '', array('_id' => $invoice_id )); ?>">
						<?php echo ntsView::objectTitle($invoice); ?>
					</a>]
				<?php endif; ?>

			</td>
			<td>
				<?php
				$this_view = array( array($e['asset_id'], $e['asset_value']) );

				if( in_array($e['action'], array('fund', 'cancel', 'reject')) )
				{
					$asset_postings = $am->get_postings_where( 
						array(
							'journal_id'	=> array( '=', $e['journal_id'] ),
							'account_type'	=> array( '=', 'customer' )
							)
						);

					if( $asset_postings )
					{
						$this_view = array();
						foreach( $asset_postings as $ap )
						{
							$format_asset_id = $asset_postings[0]['asset_id'];
							$format_asset_value = - $asset_postings[0]['asset_value'];
							$this_view[] = array( $ap['asset_id'], - $ap['asset_value'] );
						}
					}
				}

				$final_view = array();
				foreach( $this_view as $tv )
				{
					$final_view[] = $aam->format_asset( 
						$tv[0],
						$tv[1],
						TRUE,
						TRUE,
						TRUE
						);
				}

				if( count($final_view) > 1 )
				{
					$final_view = join('<br/>', $final_view);
				}
				else
				{
					$final_view = $final_view[0];
				}
				?>
				<?php echo $final_view ; ?>
			</td>
		</tr>
	<?php endforeach; ?>

	<?php if( 1 OR ((count($entries) > 1)) ) : ?>
		<?php
		if( $payment_balance < 0 )
		{
			$class = 'danger';
			$text = '<span class="text-danger"><strong>' . ntsCurrency::formatPrice($payment_balance) . '</strong></span>';
		}
		elseif( $payment_balance > 0 )
		{
			$class = 'success';
			$text = '<span class="text-success"><strong>' . ntsCurrency::formatPrice($payment_balance) . '</strong></span>';
			$text .= '<br><span class="text-muted">' . M('Overpaid') . '</span>';
		}
		else
		{
			$class = 'success';
			$text = M('OK'); 
		}
		?>
		<tr class="<?php echo $class; ?>">
			<td>&nbsp;</td>
			<td>&nbsp;</td>
			<td><?php echo $text; ?></td>
		</tr>
	<?php endif; ?>

	</table>
<?php endif; ?>

<?php if( $unpaid_invoices ) : ?>
	<p>
	<h4><?php echo M('Unpaid Invoices'); ?></h4>
	<p>
	<ul class="list-unstyled">
		<?php foreach( $unpaid_invoices as $i ) : ?>
			<li>
				<ul class="list-inline">
					<li>
						<a target="_blank" class="nts-no-ajax" href="<?php echo ntsLink::makeLink('admin/payments/invoices/edit/edit', '', array('_id' => $i->getId() )); ?>">
							<?php echo ntsView::objectTitle($i); ?>
						</a>
					</li>
					<li>
						<?php echo ntsCurrency::formatPrice( $i->getItemAmount($object) ); ?>
					</li>
				</ul>
			</li>
		<?php endforeach; ?>
	</ul>
<?php endif; ?>

<?php if( $payment_balance > 0 ) : ?>
	<p>
	<a class="btn btn-default" href="<?php echo ntsLink::makeLink('-current-', 'refund'); ?>"><?php echo M('Refund'); ?> <?php echo ntsCurrency::formatPrice($payment_balance); ?></a>
<?php endif; ?>

<?php if( $balance_cover ) : ?>
	<h4><?php echo M('Pay By Balance'); ?></h4>

	<div class="btn-group">
		<button type="button" class="btn btn-default dropdown-toggle" data-toggle="dropdown">
			<?php echo M('Pay By Balance'); ?> <span class="caret"></span>
		</button>
		<ul class="dropdown-menu">
		<?php foreach( $balance_cover as $asset_id => $asset_value ) : ?>
			<li>
				<?php
				$balance_link = ntsLink::makeLink(
					'-current-',
					'balance',
					array(
						'asset_id' => $asset_id,
						'asset_value' => $asset_value
						)
					);
				?>
				<a href="<?php echo $balance_link; ?>">
					<?php echo $aam->format_asset( $asset_id, $asset_value, FALSE, FALSE ); ?>
					<?php
					$asset_expires = 0;
					if( strpos($asset_id, '-') !== FALSE )
					{
						list( $asset_short_id, $asset_expires ) = explode( '-', $asset_id );
					}
					?>
					[
						<?php echo M('Available'); ?>: 
						<?php echo $aam->format_asset( $asset_id, $customer_balance[$asset_id], TRUE, FALSE ); ?>
						<?php if( $asset_expires ) : ?>
							<?php
							$t->setTimestamp( $asset_expires );
							?>
							, <?php echo M('Expires'); ?>: <?php echo $t->formatDateFull(); ?>
						<?php endif; ?>
					]
				</a>
			</li>
		<?php endforeach; ?>
		</ul>
	</div>
<?php endif; ?>

<?php if( $form ) : ?>
	<div class="row">
		<div class="col-sm-6">
			<h4><i class="fa fa-plus"></i> <?php echo M('Payment'); ?></h4>
			<p>
			<?php $form->display(); ?>
		</div>
		<div class="col-sm-6">
			<p>
			<?php $discount_form->display(); ?>
		</div>
	</div>
<?php endif; ?>
