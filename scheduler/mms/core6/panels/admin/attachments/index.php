<?php
$entries = ntsLib::getVar( 'admin/attachments::entries' );
$iCanEdit = ntsLib::getVar( 'admin/attachments::iCanEdit' );
$totalCols = 2;
$isAjax = ntsLib::isAjax();

if( $isAjax )
{
	$col = 'col-sm-6';
	$max_width = '100px';
}
else
{
	$col = 'col-sm-4';
	$max_width = '250px';
}

$am = new ntsAttachManager;
?>
<?php if( $iCanEdit ) : ?>
	<?php if( $isAjax ) : ?>
		<div class="nts-ajax-parent">
		<?php
		echo ntsLink::printLink(
			array(
				'panel'		=> '-current-',
				'title'		=> '<i class="fa fa-file-o"></i> ' . M('Attachments'),
				'params'	=> array(
					NTS_PARAM_VIEW_RICH	=> '-reset-',
					),
				'attr'		=> array(
					'class'	=> 'nts-no-ajax btn btn-info btn-xs',
					),
				)
			);
		?>
		<div class="nts-ajax-container"></div>
		</div>
	<?php else : ?>
		<?php
		echo ntsLink::printLink(
			array(
				'panel'		=> '-current-/create',
				'title'		=> '<i class="fa fa-plus"></i> ' . M('Attachment'),
				'attr'		=> array(
					'class'	=> 'nts-no-ajax btn btn-info btn-xs',
					),
				)
			);
		?>
	<?php endif; ?>
<?php endif; ?>

<?php if( count($entries) ) : ?>
	<p>
	<div class="row">
	<?php for( $ii = 0; $ii < count($entries); $ii++ ) : ?>
		<?php
		$e = $entries[$ii];
		$deleteLink = ntsLink::makeLink( '-current-/edit/delete', '', array('attachid' => $e['id']) );

		$NTS_VIEW['t']->setTimestamp( $e['created_at'] );
		$timeView =  $NTS_VIEW['t']->formatFull();

		$admin = new ntsUser;
		$admin->setId( $e['created_by'] );
		$adminView = '<i class="fa fa-user"></i> ' . ntsView::objectTitle( $admin );
		?>
		<div class="<?php echo $col; ?>">
			<div class="alert alert-archive2 nts-ajax-parent" style="overflow: hidden;">

				<?php if( $iCanEdit ) : ?>
					<a class="nts-ajax-loader close text-danger" href="<?php echo $deleteLink; ?>" title="<?php echo M('Delete'); ?>">
						&times;
					</a>
					<div class="nts-ajax-container"></div>
				<?php endif; ?>

				<?php
				$link = ntsLink::makeLink('system/attach', '', array('file' => $e['hash']) );
				$original_name = $am->original_name($e['file']);
				?>

				<a class="nts-no-ajax" href="<?php echo $link; ?>" title="<?php echo $original_name; ?>" target="_blank">
					<?php if( (! $e['is_image']) OR (! $isAjax) ) : ?>
						<?php echo $original_name; ?>
						<?php if( $e['is_image'] ) : ?>
							<br>
						<?php endif; ?>
					<?php endif; ?>

					<?php if( $e['is_image'] ) : ?>
						<img src="<?php echo $link; ?>" style="max-width: <?php echo $max_width; ?>; max-height: <?php echo $max_width; ?>;">
					<?php endif; ?>
				</a>

				<?php if( ! $isAjax ) : ?>
					<hr>
					<ul class="list-unstyled text-muted">
						<li>
							<small>
								<?php echo $timeView; ?>
							</small>
						</li>
						<li>
							<small>
								<?php echo $adminView; ?>
							</small>
						</li>
					</ul>
				<?php endif;  ?>
			</div>
		</div>
	<?php endfor; ?>
	</div>
<?php endif; ?>