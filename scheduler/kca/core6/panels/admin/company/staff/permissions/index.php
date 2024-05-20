<?php
$users = ntsLib::getVar( 'admin/company/staff/permissions::users' );
?>
<ul class="list-unstyled list-separated list-bordered">
<?php foreach( $users as $user ) : ?>
	<li>
		<h4>
		<?php echo ntsView::objectTitle( $user, TRUE ); ?> (<?php echo $user->getProp('email'); ?>) <span class="text-small text-muted">[id: <?php echo $user->getId(); ?>]</span>
		</h4>
		<?php
		$perm_apps = $user->getAppointmentPermissions();
		$perm_sche = $user->getSchedulePermissions();
		$res_ids = array_unique( array_merge( array_keys($perm_apps), array_keys($perm_sche) ) );
		?>
		<ul class="list-unstyled list-separated" style="margin-left: 2em;">
			<?php if( ! $res_ids ) : ?>
				<li>
					<?php echo M('None'); ?></span>
				</li>

			<?php else : ?>

				<li>
					<table style="table-layout: fixed;" class="table">
						<tr>
							<th style="width: 30%;"></th>
							<th style="width: 35%;" class="text-muted" style="font-weight: normal; font-size: 0.9em;"><?php echo M('Appointments'); ?></th>
							<th style="width: 35%;" class="text-muted"><?php echo M('Schedules'); ?></th>
						</tr>

						<?php foreach( $res_ids as $res_id ) : ?>
							<?php
							$res = ntsObjectFactory::get('resource');
							$res->setId( $res_id );

							$apps_view = array();
							if( isset($perm_apps[$res_id]) ){
								if( $perm_apps[$res_id]['view'] ){
									$apps_view[] = M('View');
								}
								if( $perm_apps[$res_id]['edit'] ){
									$apps_view[] = M('Edit');
								}
								if( $perm_apps[$res_id]['notified'] ){
									$apps_view[] = M('Get Notified');
								}
							}

							$sch_view = array();
							if( isset($perm_sche[$res_id]) ){
								if( $perm_sche[$res_id]['view'] ){
									$sch_view[] = M('View');
								}
								if( $perm_sche[$res_id]['edit'] ){
									$sch_view[] = M('Edit');
								}
							}
							?>
							<tr>
								<td>
									<?php echo ntsView::objectTitle($res, TRUE); ?> <br><span class="text-small text-muted">[id: <?php echo $res->getId(); ?>]</span>
								</td>
								<td>
									<?php echo join(', ', $apps_view); ?>
								</td>
								<td>
									<?php if( $sch_view ) : ?>
										<?php echo join(', ', $sch_view); ?>
									<?php endif; ?>
								</td>
							</tr>
						<?php endforeach; ?>
					</table>
				</li>
			<?php endif; ?>
		</ul>
	</li>
<?php endforeach; ?>
</ul>