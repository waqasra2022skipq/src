<?php
$entries = ntsLib::getVar( 'admin/company/resources::entries' );

$per_row = 4;
$span = 'col-md-3 col-sm-6';
$row_open = FALSE;
$total_count = 0;
if( isset($entries[0]) )
	$total_count += count($entries[0]);
if( isset($entries[1]) )
	$total_count += count($entries[1]);

$tm2 = ntsLib::getVar( 'admin::tm2' );
$tm2->resetLrs();
?>

<?php foreach( $entries as $is_archive => $subentries ) : ?>
	<?php for( $ii = 1; $ii <= count($subentries); $ii++ ) : ?>
		<?php
		$e = $subentries[$ii - 1];
		$is_archive = $e->getProp('archive');
		$is_internal = $e->getProp('_internal');

		/* get schedules */
		if( ! $is_archive )
		{
			$this_sers = array();
			$tm2->setResource( $e->getId() );
			$lrss = $tm2->getLrs( TRUE );
			reset( $lrss );
			foreach( $lrss as $lrs )
			{
				if( ! in_array($lrs[2], $this_sers) )
					$this_sers[] = $lrs[2];
			}
		}
		?>

		<?php if( 1 == ($ii % $per_row) ) : ?>
			<div class="row">
			<?php $row_open = TRUE; ?>
		<?php endif; ?>

		<div class="<?php echo $span; ?>">
			<?php
				$class = array( 'alert', 'alert-regular' );
				if( $is_archive )
				{
					$class[] = 'alert-archive';
					$title = M('Archived');
				}
				elseif( ! $this_sers )
				{
					$class[] = 'alert-danger';
					$title = M('No availability configured');
				}
				else
				{
					$class[] = 'alert-success';
					$title = M('OK');
				}
				$class = join( ' ', $class );
				$description = $e->getProp('description');
			?>
			<div class="<?php echo $class; ?>" title="<?php echo $title; ?>">
				<ul class="list-unstyled">
					<li class="squeeze-in">
						<?php if( $is_internal ) : ?>
							<div class="pull-right">
								<span class="label label-warning"><?php echo M('Internal'); ?></span>
							</div>
						<?php endif; ?>
						<?php
						echo ntsLink::printLink(
							array(
								'panel'		=> '-current-/../edit/edit',
								'params'	=> array('_id' => $e->getId()),
								'title'		=> ntsView::objectTitle($e),
								),
							true
							);
						?>
					</li>

					<li class="text-muted text-smaller">
						id: <?php echo $e->getId(); ?>
					</li>

					<?php if( strlen($description) ) : ?>
						<li class="muted">
							<?php echo $description; ?>
						</li>
					<?php endif; ?>

					<?php if( (! $is_archive) && ($total_count > 1) ) : ?>
						<li class="hc-toggled">
							<ul class="list-unstyled">
								<li class="divider"></li>
								<li>
									<ul class="list-inline list-separated">
										<li>
											<?php echo M('Show Order'); ?>
										</li>
										<li>
											<?php
											echo $this->makeInput (
											/* type */
												'text',
											/* attributes */
												array(
													'id'		=> 'order_' . $e->getId(),
													'attr'		=> array(
														'size'	=> 2,
														),
													),
											/* validators */
												array(
													array(
														'code'		=> 'notEmpty.php', 
														'error'		=> M('Required'),
														),
													array(
														'code'		=> 'integer.php', 
														'error'		=> M('Numbers only'),
														),
													)
												);
											?>
										</li>
									</ul>
								</li>
							</ul>
						</li>
					<?php endif; ?>
				</ul>
				<?php if( ! $this_sers ) : ?>
					<a href="<?php echo ntsLink::makeLink('admin/manage/schedules', '', array('filter' => 'r' . $e->getId())); ?>">
						<?php echo M('No availability configured'); ?>
					</a>
				<?php endif; ?>
			</div>
		</div>

		<?php if( ! ($ii % $per_row) ) : ?>
			</div>
			<?php $row_open = FALSE; ?>
		<?php endif; ?>
	<?php endfor; ?>

	<?php if( $row_open ) : ?>
		</div>
		<?php $row_open = FALSE; ?>
	<?php endif; ?>

<?php endforeach; ?>

<?php if( $row_open ) : ?>
</div>
<?php endif; ?>

<?php if( $total_count > 1 ) : ?>
	<div class="hc-toggled" style="display: block;">
		<p>
		<a class="btn btn-default hc-toggler" href="#"><?php echo M('Show Order'); ?></a>
		</p>
	</div>

	<div class="hc-toggled">
		<p>
		<?php echo $this->makePostParams('-current-', 'update'); ?>
		<INPUT class="btn btn-default" TYPE="submit" VALUE="<?php echo M('Show Order'); ?>: <?php echo M('Update'); ?>">
		</p>
	</div>
<?php endif; ?>