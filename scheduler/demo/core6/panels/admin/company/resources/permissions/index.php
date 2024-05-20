<?php
$resources = ntsLib::getVar( 'admin/company/resources/permissions::entries' );
?>
<ul class="list-unstyled list-separated list-bordered">
<?php foreach( $resources as $resource ) : ?>
	<li>
		<h4>
		<?php echo ntsView::objectTitle( $resource, TRUE ); ?> <span class="text-small text-muted">[id: <?php echo $resource->getId(); ?>]</span>
		</h4>
		<?php
		list($perm_apps, $perm_sche) = $resource->getAdmins();
		$users_ids = array_unique( array_merge( array_keys($perm_apps), array_keys($perm_sche) ) );
		?>
		<ul class="list-unstyled list-separated" style="margin-left: 2em;">
			<?php if( ! $users_ids ) : ?>
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

						<?php foreach( $users_ids as $user_id ) : ?>
							<?php
							$user = new ntsUser;
							$user->setId( $user_id );

							$apps_view = array();
							if( isset($perm_apps[$user_id]) ){
								if( $perm_apps[$user_id]['view'] ){
									$apps_view[] = M('View');
								}
								if( $perm_apps[$user_id]['edit'] ){
									$apps_view[] = M('Edit');
								}
								if( $perm_apps[$user_id]['notified'] ){
									$apps_view[] = M('Get Notified');
								}
							}

							$sch_view = array();
							if( isset($perm_sche[$user_id]) ){
								if( $perm_sche[$user_id]['view'] ){
									$sch_view[] = M('View');
								}
								if( $perm_sche[$user_id]['edit'] ){
									$sch_view[] = M('Edit');
								}
							}
							?>
							<tr>
								<td>
									<?php echo ntsView::objectTitle($user, TRUE); ?> (<?php echo $user->getProp('email'); ?>) <br><span class="text-small text-muted">[id: <?php echo $user->getId(); ?>]</span>
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