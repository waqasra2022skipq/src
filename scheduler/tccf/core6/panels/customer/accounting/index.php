<?php
global $NTS_CURRENT_USER;
$object = $NTS_CURRENT_USER;

$t = $NTS_VIEW['t'];
$aam =& ntsAccountingAssetManager::getInstance();
$now = time();
?>
<div class="page-header">
	<h2><i class="fa fa-suitcase"></i> <?php echo M('Balance'); ?></h2>
</div>

<?php if( $balance ) : ?>
	<h3>
		<?php echo M('Available Balance'); ?>
	</h3>

	<?php foreach( $balance as $asset_key => $asset_value ) : ?>
		<?php
		if( $asset_value == 0 )
		{
			continue;
		}
		list( $asset_id, $asset_expires ) = explode( '-', $asset_key );
		$valid_for_view = $aam->asset_view( $asset_id, TRUE, array('location', 'resource', 'service') );
		$when_view = $aam->asset_view( $asset_id, TRUE, array(), array('location', 'resource', 'service', 'expires_in') );
		$status_class = ( $asset_expires && ($asset_expires < $now) ) ? 'danger' : 'default';
		?>

		<div class="collapse-panel panel panel-<?php echo $status_class; ?>">
			<div class="panel-heading">
				<?php if( $asset_expires ) : ?>
					<?php
					$t->setTimestamp( $asset_expires );
					?>
					<div class="pull-right">
						<?php echo M('Expires'); ?>: <strong><?php echo $t->formatDateFull(); ?></strong>
					</div>
				<?php else : ?>
					<?php // echo M('Never Expires'); ?>
				<?php endif; ?>

				<h4 class="panel-title">
					<?php
					$show_sign = ($asset_value >= 0) ? FALSE : TRUE;
					?>
					<?php if( $valid_for_view OR $when_view ) : ?>
						<a href="#" data-toggle="collapse-next">
							<?php echo $aam->format_asset( $asset_id, $asset_value, TRUE, $show_sign ); ?>
						</a>
					<?php else : ?>
						<?php echo $aam->format_asset( $asset_id, $asset_value, TRUE, $show_sign ); ?>
					<?php endif; ?>
				</h4>
			</div>

			<?php if( $valid_for_view OR $when_view ) : ?>
				<div class="panel-collapse collapse">
					<div class="panel-body">
						<ul class="list-unstyled">
						<?php if( $valid_for_view ) : ?>
							<?php foreach( $valid_for_view as $av ) : ?>
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
						<?php endif; ?>

						<?php if( $when_view ) : ?>
							<?php foreach( $when_view as $av ) : ?>
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
						<?php endif; ?>
						</ul>
					</div>

					<div class="panel-footer">
						<a href="<?php echo ntsLink::makeLink('customer/book', '', array('asset' => $asset_id) ); ?>" class="btn btn-default">
							<?php echo M('Schedule Now'); ?>
						</a>
					</div>
				</div>
			<?php endif; ?>
		</div>
	<?php endforeach; ?>
<?php endif; ?>

<?php if( $entries ) : ?>
	<p>
	<h3><?php echo M('History'); ?></h3>

	<ul class="list-unstyled list-padded list-striped">
	<?php foreach( $entries as $e ) : ?>
		<?php
		$e['object'] = ntsObjectFactory::get( $e['obj_class'] );
		$e['object']->setId( $e['obj_id'] );
		?>
		<li>
			<ul class="list-unstyled row">
				<li class="col-md-2">
					<strong>
						<?php echo $aam->format_asset( $e['asset_id'], $e['asset_value'], TRUE); ?>
					</strong>
					<?php if( isset($e['expires_at']) && $e['expires_at'] && ($e['asset_value'] > 0) ) : ?>
						<?php $t->setTimestamp( $e['expires_at'] ); ?>
						<br>
						<span class="text-muted text-small">
							<?php echo M('Expires'); ?>: <?php echo $t->formatDateFull(); ?>
						</span>
					<?php endif; ?>
				</li>

				<li class="col-md-3 text-italic">
					<?php echo $am->journal_label($e); ?>
				</li>

				<li class="col-md-5">
					<?php echo ntsView::objectTitle($e['object']); ?>
				</li>

				<li class="col-md-2 text-small text-muted">
					<?php $t->setTimestamp( $e['created_at'] ); ?>
					<?php echo $t->formatFull(); ?>
				</li>
			</ul>
		</li>
	<?php endforeach; ?>
	</ul>
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