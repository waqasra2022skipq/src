<?php
$session = new ntsSession;
$coupon = $session->userdata('coupon');

$conf =& ntsConf::getInstance();
$show_end_time = $conf->get('customerNoEndTimeNotification') ? FALSE : TRUE;

$pm =& ntsPaymentManager::getInstance();

$description = $obj->getProp('description');
$duration = $obj->getProp('duration');
$duration2 = $obj->getProp('duration2');
$duration_break = $obj->getProp('duration_break');

$duration = $duration + $duration2 + $duration_break;

$lead_out = $obj->getProp('lead_out');

$duration_view = ntsTime::formatPeriodShort($duration);
$duration_view_long = ntsTime::formatPeriod($duration);
$price_view = '';
if( ! isset($this_a) )
	$this_a = array();
$this_a['service_id'] = $obj->getId();
$base_amount = $pm->getBasePrice( $this_a );
$total_amount = $pm->getPrice( $this_a, $coupon );

if( $base_amount ){
	if( $base_amount != $total_amount ){
		$price_view = '<span class="text-muted" style="text-decoration: line-through;">' . ntsCurrency::formatPrice($base_amount) . '</span>' . ' ' . ntsCurrency::formatPrice($total_amount);
	}
	else {
		$price_view = ntsCurrency::formatPrice($total_amount);
	}
}
?>
<ul class="list-unstyled list-separated">
	<li>
		<ul class="list-inline list-separated">
			<?php if( $show_end_time ) : ?>
				<li>
					<span class="btn btn-default btn-condensed" title="<?php echo M('Duration'); ?>: <?php echo $duration_view_long; ?>">
						<i class="fa fa-clock-o"></i> <?php echo $duration_view_long; ?>
					</span>
				</li>
			<?php endif; ?>
		<?php if( $price_view ) : ?>
			<li>
				<span class="btn btn-default btn-condensed" title="<?php echo M('Price'); ?>: <?php echo ntsCurrency::formatPrice($total_amount); ?>">
					<?php echo $price_view; ?>
				</span>
			</li>
		<?php endif; ?>
		</ul>
	</li>

	<?php if( strlen($description) ) : ?>
		<li>
			<?php if( $can_book_this && isset($link) ) : ?>
				<a title="<?php echo ntsView::objectTitle($obj); ?>" href="<?php echo $link; ?>">
			<?php endif; ?>
			<?php echo $description; ?>
			<?php if( $can_book_this && isset($link) ) : ?>
				</a>
			<?php endif; ?>
		</li>
	<?php endif; ?>
</ul>