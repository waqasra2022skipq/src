<?php
$t = $NTS_VIEW['t'];
$aam =& ntsAccountingAssetManager::getInstance();
$pm =& ntsPaymentManager::getInstance();
$current_user_id = ntsLib::getCurrentUserId();
?>

<p>
<?php
$grand_total_amount = 0;
$grand_base_total_amount = 0;

$r = array(
	'pack_id' 		=> $pack->getId(),
	'customer_id'	=> $current_user_id,
	);

$base_amount = $pm->getBasePrice( $r );
$total_amount = $pm->getPrice( $r, $coupon );

$grand_base_total_amount += $base_amount;
$grand_total_amount += $total_amount;
?>

<dl class="dl-horizontal">
	<dt></dt>
	<dd>
		<h3><?php echo ntsView::objectTitle($pack); ?></h3>
	</dd>

	<dt>
		<?php echo M('Value'); ?>
	</dt>
	<dd>
		<?php echo $aam->format_asset( $pack->getProp('asset_id'), $pack->getProp('asset_value'), TRUE, FALSE ); ?>
	</dd>

	<dt>
	<?php echo M('Valid For'); ?>
	</dt>
	<dd>
		<?php
		$asset_view = $aam->asset_view( $pack->getProp('asset_id'), TRUE, array('location', 'resource', 'service') );
		?>

		<?php if( $asset_view ) : ?>
			<ul class="list-unstyled">
			<?php foreach( $asset_view as $av ) : ?>
				<li>
					<ul class="list-inline">
						<li style="vertical-align: top;">
							<?php echo $av[0]; ?>
						</li>
						<li>
							<ul class="list-unstyled">
								<?php foreach( $av[1] as $av2 ) : ?>
									<li>
										<?php echo $av2; ?>
									</li>
								<?php endforeach; ?>
							</ul>
						</li>
					</ul>
				</li>
			<?php endforeach; ?>
			</ul>
		<?php else : ?>
			<?php echo M('Anything'); ?>
		<?php endif; ?>
	</dd>

	<dt>
	<?php echo M('When'); ?>
	</dt>
	<dd>
		<?php
		$asset_view = $aam->asset_view( $pack->getProp('asset_id'), TRUE, array(), array('location', 'resource', 'service') );
		?>

		<?php if( $asset_view ) : ?>
			<ul class="list-unstyled">
			<?php foreach( $asset_view as $av ) : ?>
				<li>
					<ul class="list-inline">
						<li style="vertical-align: top;">
							<?php echo $av[0]; ?>
						</li>
						<li>
							<ul class="list-unstyled">
								<?php foreach( $av[1] as $av2 ) : ?>
									<li>
										<?php echo $av2; ?>
									</li>
								<?php endforeach; ?>
							</ul>
						</li>
					</ul>
				</li>
			<?php endforeach; ?>
			</ul>
		<?php else : ?>
			<?php echo M('Anytime'); ?>
		<?php endif; ?>
	</dd>

	<dt>
	<?php echo M('Expires In'); ?>
	</dt>
	<dd>
		<?php
		$expires_in = $pack->getProp('expires_in');
		if( $expires_in )
		{
			$this_view = '';
			list( $qty, $measure ) = explode( ' ', $expires_in );
			$this_view .= $qty;
			$tag = ( $qty > 1 ) ? $measure : substr($measure, 0, -1);
			$tag = ucfirst( $tag );
			$this_view .= ' ' . M($tag);
		}
		else
			$this_view = M('Never Expires');
		?>
		<?php echo $this_view; ?>
	</dd>

	<?php if( $show_coupon ) : ?>
		<?php if( $coupon_valid ) : ?>
			<dt>
			</dt>
			<dd>
				<ul class="list-inline">
					<li>
						<?php echo M('Coupon Code'); ?>
					</li>
					<li>
						<div class="btn-group">
							<span class="btn btn-default">
								<?php echo $coupon; ?>
							</span>
							<a class="btn btn-default" href="<?php echo ntsLink::makeLink('-current-', 'coupon', array('coupon' => '')); ?>">
								<span class="text-danger close2"><strong>&times;</strong></span>
							</a>
						</div>
					</li>
				</ul>

				<ul class="list-unstyled text-italic">
				<?php foreach( $coupon_promotions as $cp ) : ?>
					<li>
						<?php echo ntsView::objectTitle( $cp ); ?>
					</li>
				<?php endforeach; ?>
				</ul>
			</dd>

		<?php else : ?>
			<dt>
			</dt>
			<dd>
				<div class="collapse-panel">
					<p>
						<a href="#" data-toggle="collapse-next"><?php echo M('Coupon Code'); ?>?</a>
					</p>

					<?php if( $coupon ) : ?>
					<div class="collapse in">
					<?php else : ?>
					<div class="collapse">
					<?php endif; ?>
						<?php echo $NTS_VIEW['form_coupon']->display(); ?>
					</div>
				</div>
			</dd>
		<?php endif; ?>
	<?php endif; ?>

	<dt>
		<?php echo M('Total Price'); ?>
	</dt>
	<dd>
		<span class="btn btn-default">
			<?php if( $grand_base_total_amount != $grand_total_amount ) : ?>
				<span class="text-muted" style="text-decoration: line-through;">
					<?php echo ntsCurrency::formatPrice($grand_base_total_amount); ?>
				</span>
				<strong>
					<?php echo ntsCurrency::formatPrice($grand_total_amount); ?>
				</strong>
			<?php else : ?>
				<strong>
				<?php echo ntsCurrency::formatPrice($grand_total_amount); ?>
				</strong>
			<?php endif; ?>
		</span>
	</dd>
</dl>
