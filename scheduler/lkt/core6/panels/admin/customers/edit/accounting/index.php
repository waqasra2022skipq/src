<?php
$object = ntsLib::getVar( 'admin/customers/edit::OBJECT' );
$packs = ntsObjectFactory::getAllIds( 'pack' );

$t = $NTS_VIEW['t'];
$aam =& ntsAccountingAssetManager::getInstance();
$now = time();
?>

<?php if( $packs ) : ?>
	<p>
	<div class="nts-ajax-parent">
		<div>
		<?php
		echo ntsLink::printLink(
			array(
				'panel'		=> 'admin/payments/orders/create',
				'title'		=> '<i class="fa fa-plus"></i> ' . M('Package'),
				'params'	=> array(
					'customer'	=> $object->getId(),
					NTS_PARAM_VIEW_RICH	=> 'basic',
					),
				'attr'		=> array(
					'class'	=> 'nts-ajax-loader btn btn-success',
					),
				)
			);
		?>
		</div>
		<div class="nts-ajax-container nts-child nts-ajax-return">
		</div>
	</div>
	</p>
<?php endif; ?>

<?php if( $balance ) : ?>
	<h3>
		<?php echo M('Available Balance'); ?>
	</h3>

	<?php
	$balance_shown = FALSE;
	$balance_id = 0;
	?>
	<?php foreach( $balance as $asset_key => $asset_value ) : ?>
		<?php
		$balance_id++;
		if( $asset_value == 0 ){
			continue;
		}
		$balance_shown = TRUE;

		list( $asset_id, $asset_expires ) = explode( '-', $asset_key );
		$valid_for_view = $aam->asset_view(
			$asset_id,
			TRUE, // html
			array('location', 'resource', 'service'), //just
			array(), // skip
			$asset_value // force
			);
		$when_view = $aam->asset_view(
			$asset_id, 
			TRUE,
			array(),
			array('location', 'resource', 'service', 'expires_in')
			);
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
					<?php if( 1 OR $valid_for_view OR $when_view ) : ?>
						<a href="#" data-toggle="collapse-next">
							<?php echo $aam->format_asset( $asset_id, $asset_value, TRUE, $show_sign ); ?>
						</a>
					<?php else : ?>
						<?php echo $aam->format_asset( $asset_id, $asset_value, TRUE, $show_sign ); ?>
					<?php endif; ?>
				</h4>
			</div>

			<?php if( 1 OR $valid_for_view OR $when_view ) : ?>
				<div class="panel-collapse collapse<?php if(in_array($balance_id, $expand)){echo ' in';} ?>">
					<div class="panel-body">
						<ul class="list-unstyled">
						<?php if( $valid_for_view ) : ?>
							<?php foreach( $valid_for_view as $av ) : ?>
								<li>
									<ul class="list-inline">
										<li>
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

						<a href="<?php echo ntsLink::makeLink('admin/manage/appointments/create', '', array('customer_id' => $object->getId(), 'asset' => $asset_id) ); ?>" class="btn btn-default">
							<i class="fa fa-plus"></i> <?php echo M('Appointment'); ?>
						</a>
					</div>

					<div class="panel-footer">
						<div class="collapse-panel">
							<a href="#" data-toggle="collapse-next" class="display-block">
								<?php echo M('Remove Balance'); ?> <span class="caret"></span>
							</a>

							<div class="collapse<?php if(in_array($balance_id, $expand)){echo ' in';} ?>">
							<?php
							$ff =& ntsFormFactory::getInstance();
							$formFile = dirname( __FILE__ ) . '/remove_form';
							$formParams = array(
								'asset_id'		=> $asset_id,
								'asset_value'	=> $asset_value,
								'total_asset_value'	=> $asset_value,
								'balance_id'		=> $balance_id,
								);
							$this_form = $ff->makeForm( $formFile, $formParams, 'balance_' . $balance_id );
							$this_form->display();
							?>
							</div>
						</div>
					</div>
				</div>
			<?php endif; ?>
		</div>
	<?php endforeach; ?>

	<?php if( ! $balance_shown ) : ?>
		<p>
			<?php echo M('None'); ?>
		</p>
	<?php endif; ?>
<?php endif; ?>

<?php if( $entries ) : ?>
	<h3>
		<?php echo M('History'); ?>
	</h3>

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
					<?php 
					switch( $e['obj_class'] )
					{
						case 'transaction' :
						?>
							<?php
							$tra = $e['object'];
							$invoice_id = $tra->getProp('invoice_id');
							$invoice = ntsObjectFactory::get('invoice');
							$invoice->setId( $invoice_id );
							?>
							<a target="_blank" class="nts-no-ajax" href="<?php echo ntsLink::makeLink('admin/payments/invoices/edit/edit', '', array('_id' => $invoice_id )); ?>">
								<?php echo ntsView::objectTitle($invoice); ?>
							</a>
						<?php break; ?>

					<?php case 'appointment' : ?>
							<a target="_blank" class="nts-no-ajax" href="<?php echo ntsLink::makeLink('admin/manage/appointments/edit/overview', '', array('_id' => $e['obj_id'] )); ?>">
								<?php echo ntsView::objectTitle($e['object']); ?>
							</a>
					<?php break; ?>

					<?php default : ?>
							<?php echo ntsView::objectTitle($e['object']); ?>
					<?php break; ?>
				<?php } ?>
				</li>

				<li class="col-md-2 text-small text-muted">
					<?php echo $t->formatFull($e['created_at']); ?>
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