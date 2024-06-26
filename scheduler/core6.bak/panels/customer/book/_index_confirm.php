<?php
$pm =& ntsPaymentManager::getInstance();
$session = new ntsSession;
$apps = $session->userdata( 'apps' );

/* prepare for promotions */
$current_user = ntsLib::getCurrentUser();
$ntspm =& ntsPaymentManager::getInstance();

$ff =& ntsFormFactory::getInstance();
$current_user = ntsLib::getCurrentUser();

$t = $NTS_VIEW['t'];
$grand_total_amount = 0;
$grand_base_total_amount = 0;

$ntsConf =& ntsConf::getInstance();
$appsInCart = $ntsConf->get('appsInCart');

$tm2 = $NTS_VIEW['tm2'];
$available_seats = array();
for( $ai = 1; $ai <= count($apps); $ai++ ){
	if( ! isset($apps[ $ai-1 ]) )
		continue;
	$app = $apps[ $ai-1 ];
	$times = $tm2->getAllTime( $app['starts_at'], $app['starts_at'] + 1 );

	$this_available_seats = 0;
	if( isset($times[$app['starts_at']]) ){
		$this_available_seats = $tm2->getAvailableSeats(
			$times[$app['starts_at']],
			($app['starts_at'] + $app['duration'])
			);
	}
	$available_seats[$ai] = $this_available_seats;
}

?>

<?php if( NTS_ENABLE_TIMEZONES >= 0 ) : ?>
	<p>
	<?php if( NTS_ENABLE_TIMEZONES > 0 ) : ?>
		<div class="dropdown">
			<a class="dropdown-toggle btn btn-default" data-toggle="dropdown" href="#">
				<i class="fa fa-fw fa-globe"></i> 
				<?php echo ntsTime::timezoneTitle($current_user->getTimezone()); ?> <b class="caret"></b>
			</a>
			<ul class="dropdown-menu">
				<li>
					<span>
					<?php
					$formTimezoneParams = array(
						'tz'	=> $current_user->getTimezone(),
						);
					$timezoneForm = NTS_APP_DIR . '/panels/customer/appointments/view/formTimezone';
					$formTimezone =& $ff->makeForm( $timezoneForm, $formTimezoneParams );
					$formTimezone->display();
					?>
					</span>
				</li>
			</ul>
		</div>
	<?php elseif( NTS_ENABLE_TIMEZONES == 0 ) : ?>
		<span class="btn btn-default">
			<i class="fa fa-fw fa-globe"></i> 
			<?php echo ntsTime::timezoneTitle($current_user->getTimezone()); ?>
		</span>
	<?php endif; ?>
	</p>
<?php endif; ?>

<ul class="list-unstyled">
<?php for( $ai = 1; $ai <= count($apps); $ai++ ) : ?>
	<?php
	if( ! isset($apps[ $ai-1 ]) )
		continue;
	$app = $apps[ $ai-1 ];
	if( ! isset($app['seats']) ){
		$app['seats'] = 1;
	}
	$t->setTimestamp( $app['starts_at'] );

	$base_amount = $pm->getBasePrice( $app );
	$total_amount = $pm->getPrice( $app, $coupon );

	$grand_total_amount += $total_amount;
	$grand_base_total_amount += $base_amount;

	$price_view = '';
	if( $total_amount )
	{
		if( $base_amount != $total_amount )
		{
			$price_view = '<span class="text-muted" style="text-decoration: line-through;">' . ntsCurrency::formatPrice($base_amount) . '</span>' . ' ' . ntsCurrency::formatPrice($total_amount);
		}
		else
		{
			$price_view = ntsCurrency::formatPrice($total_amount);
		}
		$price_view = '<span class="btn btn-success-o btn-xs">' . $price_view . '</span>';
	}

	$promotions = $ntspm->getPromotions($app);
	?>
	<li class="collapse-panel panel panel-success">
		<div class="panel-heading panel-condensed">
			<a class="close text-danger pull-right" href="<?php echo ntsLink::makeLink('customer/book/remove', '', array('ai' => $ai)); ?>" title="<?php echo M('Remove'); ?>">
				<i class="fa fa-times text-danger"></i>
			</a>

			<ul class="list-inline">
				<li>
					<h4 class="panel-title">
						<a href="#" data-toggle="collapse-next">
							<i class="fa fa-fw fa-calendar"></i>&nbsp;<?php echo $t->formatDateFull(); ?> 
							<i class="fa fa-fw fa-clock-o"></i>&nbsp;<?php echo $t->formatTime(); ?>
						</a>
					</h4>
				</li>
				<?php if( $price_view ) : ?>
					<li>
						<?php echo $price_view; ?>
					</li>
				<?php endif; ?>
			</ul>
		</div>
		<div class="panel-collapse collapse in">
			<div class="panel-body">
				<ul class="list-unstyled">
					<?php if( (! NTS_SINGLE_LOCATION) && (! $auto_location) ) : ?>
						<?php
						$location = new ntsObject('location');
						$location->setId( $app['location_id'] );
						?>
						<li>
							<?php echo ntsView::objectTitle($location, TRUE); ?>
						</li>
					<?php endif; ?>

					<?php if( (! NTS_SINGLE_RESOURCE) && (! $auto_resource) ) : ?>
						<?php
						$resource = ntsObjectFactory::get( 'resource' );
						$resource->setId( $app['resource_id'] );
						?>
						<li>
							<?php echo ntsView::objectTitle($resource, TRUE); ?>
						</li>
					<?php endif; ?>

					<?php
					$service = ntsObjectFactory::get( 'service' );
					$service->setId( $app['service_id'] );
					?>
					<li>
						<?php echo ntsView::objectTitle( $service, TRUE ); ?>
					</li>

					<?php
					$this_available_seats = $available_seats[$ai];
					?>
					<?php if( $this_available_seats > 1 ) : ?>
						<li>
							<?php echo M('Seats'); ?>
							<ul class="list-inline list-separated">
							<?php for( $sss = 1; $sss <= $this_available_seats; $sss++ ) : ?>
								<?php
								if( $sss <= $app['seats'] ){
									$btn_class = 'btn-success';
								}
								else {
									$btn_class = 'btn-success-o';
									$btn_class = 'btn-archive-o';
								}
								$seats_link = ntsLink::makeLink('-current-', 'seats', array('ai' => $ai, 'seats' => $sss));
								?>
								<li>
									<a href="<?php echo $seats_link; ?>" class="btn btn-default btn-sm <?php echo $btn_class; ?>" title="<?php echo $sss; ?>">
										<?php echo $sss; ?>
									</a>
								</li>
							<?php endfor; ?>
							</ul>
						</li>
					<?php endif; ?>

					<?php if( $promotions ) : ?>
						<?php foreach( $promotions as $promo ) : ?>
							<li>
								<?php echo ntsView::objectTitle($promo, TRUE); ?>
							</li>
						<?php endforeach; ?>
					<?php endif; ?>

				</ul>
			</div>
		</div>
	</li>
<?php endfor; ?>
</ul>

<?php
$add_more_link = ntsLink::makeLink(
	'-current-/..',
	'',
	array(
		'time'	=> '-reset-',
		)
	);
?>
<?php if( $appsInCart > count($apps) ) : ?>
	<p>
	<a class="btn btn-default btn-xs btn-archive" href="<?php echo $add_more_link; ?>">
		<i class="fa fa-fw fa-plus"></i> <?php echo M('Add Another Appointment'); ?>
	</a>
	</p>
<?php endif; ?>

<?php if( $grand_total_amount OR $show_coupon ) : ?>
<hr>
<?php endif; ?>

<?php if( $show_coupon ) : ?>
	<?php if( $coupon_valid ) : ?>
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

	<?php else : ?>
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
	<?php endif; ?>
<?php endif; ?>

<?php if( $grand_total_amount OR $show_coupon ) : ?>
	<ul class="list-inline">
	<?php if( $grand_total_amount ) : ?>
		<li>
			<?php echo M('Total Price'); ?>
		</li>
		<li>
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
		</li>
	<?php endif; ?>
	</ul>
<?php endif; ?>

<?php if( $show_coupon ) : ?>
<script language="JavaScript">
jQuery(document).on( 'click', 'a#nts-apply-coupon', function(e)
{
	var targetUrl = jQuery(this).attr('href');
	var couponCode = jQuery(this).closest('form').find('[name=nts-coupon]').val();
	targetUrl += '&nts-action=coupon&nts-coupon=' + couponCode;
	document.location.href = targetUrl;
	return false;
});
</script>
<?php endif; ?>