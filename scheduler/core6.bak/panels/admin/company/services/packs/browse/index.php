<?php
$aam =& ntsAccountingAssetManager::getInstance();

$entries = ntsLib::getVar( 'admin/company/services/packs::entries' );
$totalCols = 5;
$totalCols += 1;
?>

<p>
<div class="nts-ajax-parent">
<?php
echo ntsLink::printLink(
	array(
		'panel'		=> '-current-/../create',
		'title'		=> '<i class="fa fa-plus"></i> ' . M('Package'),
		'attr'		=> array(
			'class'	=> 'btn btn-success',
			'title'	=> M('Add'),
			),
		)
	);
?>

<?php
/*
echo ntsLink::printLink(
	array(
		'panel'		=> '-current-/../settings',
		'title'		=> '<i class="fa fa-cogs"></i> ' . M('Settings'),
		'attr'		=> array(
			'class'	=> 'nts-ajax-loader btn btn-default',
			'title'	=> M('Package') . ': ' . M('Settings'),
			),
		)
	);
*/
?>
<div class="panel-body nts-ajax-container"></div>
</div>

<p>
<table class="table table-condensed table-striped2">
<?php if( count($entries) > 0 ) : ?>
<tbody>
<tr>
	<th style="width: 1em;">&nbsp;</th>
	<th>&nbsp;</th>
	<th><?php echo M('Value'); ?></th>
	<th><?php echo M('Valid For'); ?></th>
	<th><?php echo M('When'); ?></th>
	<th><?php echo M('Expires In'); ?></th>
</tr>
</tbody>
<?php endif; ?>

<?php $count = 0; ?>
<?php foreach( $entries as $e ) : ?>
	<?php
	$deleteLink = ntsLink::makeLink( '-current-/../edit/delete', 'delete', array('_id' => $e->getId()) );
	$editLink = ntsLink::makeLink( '-current-/../edit', '', array('_id' => $e->getId()) );
	$price = $e->getProp('price');
	?>
	<tbody>
	<tr>
		<td style="width: 1em;">
			<a class="hc-confirm btn btn-default btn-xs" href="<?php echo $deleteLink; ?>" title="<?php echo M('Delete'); ?>">
				<i class="fa fa-times text-danger"></i>
			</a>
		</td>

		<td>
			<a href="<?php echo $editLink; ?>">
				<?php echo ntsView::objectTitle($e); ?>
			</a>
			<?php if( $price ) : ?>
				<p class="text-success">
					<?php echo ntsCurrency::formatPrice($price); ?>
				</p>
			<?php else : ?>
				<p class="text-muted">
					<?php echo M('Not For Sale'); ?>
				</p>
			<?php endif; ?>
		</td>

		<td>
			<?php
			echo $aam->format_asset(
				$e->getProp('asset_id'),
				$e->getAssetValue(),
				TRUE,
				FALSE
				);
			?>
		</td>

		<td>
			<?php
			$asset_view = $aam->asset_view( 
				$e->getProp('asset_id'),
				TRUE, 
				array('location', 'resource', 'service')
				);
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
		</td>

		<td>
			<?php
			$asset_view = $aam->asset_view( $e->getProp('asset_id'), TRUE, array(), array('location', 'resource', 'service') );
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
		</td>

		<td>
			<?php
			$expires_in = $e->getProp('expires_in');
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
		</td>
	</tr>
	</tbody>
<?php endforeach; ?>
</table>