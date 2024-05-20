<?php
$aam =& ntsAccountingAssetManager::getInstance();
?>
<div class="page-header">
	<h2><?php echo M('Packages'); ?></h2>
</div>

<?php if( ! $packs ) : ?>
	<p>
	<?php echo M('Not Available'); ?>
	</p>
	<?php return; ?>
<?php endif; ?>

<?php foreach( $packs as $e ) : ?>
	<div class="collapse-panel panel panel-default">
		<div class="panel-heading">
			<div class="pull-right text-strong text-success">
				<?php echo ntsCurrency::formatPrice($e->getProp('price')); ?> 
			</div>
			<h4 class="panel-title">
				<a href="#" data-toggle="collapse-next">
					<?php echo ntsView::objectTitle($e); ?>
				</a>
			</h4>
		</div>

		<div class="panel-collapse collapse in">
			<div class="panel-body">
				<dl class="dl-horizontal">
					<dt>
						<?php echo M('Value'); ?>
					</dt>
					<dd>
						<?php
						echo $aam->format_asset(
							$e->getProp('asset_id'),
							$e->getAssetValue(),
							TRUE,
							FALSE
							);
						?>
					</dd>

					<?php
					$asset_view = $aam->asset_view( $e->getProp('asset_id'), TRUE, array('location', 'resource', 'service') );
					?>
					<?php if( $asset_view ) : ?>
						<dt>
							<?php echo M('Valid For'); ?>
						</dt>
						<dd>
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
						</dd>
					<?php endif; ?>
				
					<?php
					$expires_in = $e->getProp('expires_in');
					?>
					<?php if( $expires_in ) : ?>
						<?php
						$this_view = '';
						list( $qty, $measure ) = explode( ' ', $expires_in );
						$this_view .= $qty;
						$tag = ( $qty > 1 ) ? $measure : substr($measure, 0, -1);
						$tag = ucfirst( $tag );
						$this_view .= ' ' . M($tag);
						?>
						<dt>
							<?php echo M('Expires In'); ?>
						</dt>
						<dd>
							<?php echo $this_view; ?>
						</dd>
					<?php endif; ?>
				</dl>

			</div>

			<div class="panel-footer">
				<ul class="list-inline">
					<li class="text-strong text-success">
						<?php echo ntsCurrency::formatPrice($e->getProp('price')); ?> 
					</li>
					<li>
						<a class="btn btn-default" href="<?php echo ntsLink::makeLink('-current-/confirm', '', array('pack' => $e->getId())); ?>">
							<?php echo M('Purchase'); ?>
						</a>
					</li>
				</ul>
			</div>
		</div>
	</div>
<?php endforeach; ?>