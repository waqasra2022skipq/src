<?php
$current_panel = $_NTS['CURRENT_PANEL'];
if( substr($current_panel, 0, strlen('customer/appointments')) == 'customer/appointments' ){
	return;
}

// get upcoming appointments
$current_user = ntsLib::getCurrentUser();
if( ! $current_user->getId() ){
	return;
}

$ntsdb =& dbWrapper::getInstance();
$customer_id = $current_user->getId();

global $NTS_VIEW;

if( ! isset($NTS_VIEW['t']) ){
	$t = new ntsTime();
	global $NTS_CURRENT_USER;
	$t->setTimezone( $NTS_CURRENT_USER->getTimezone() );
	$NTS_VIEW['t'] = $t;
}

$t = $NTS_VIEW['t'];
$t->setNow();
$t->setStartDay();
$startToday = $t->getTimestamp();

$where = array(
	'customer_id'	=> array( '=', $customer_id )
	);
$where['starts_at'] = array( '>=', $startToday );

$where['completed'] = array( '<>', HA_STATUS_CANCELLED );
$where['completed '] = array( '<>', HA_STATUS_NOSHOW );

$addon = 'ORDER BY starts_at ASC';

$count_upcoming_appointments = ntsObjectFactory::count( 'appointment', $where, $addon );

$where['starts_at'] = array( '<', $startToday );
$count_past_appointments = ntsObjectFactory::count( 'appointment', $where, $addon );
// $count_past_appointments = 0;
$total_appointments = $count_upcoming_appointments + $count_past_appointments;
?>

<?php if( $count_upcoming_appointments ) : ?>
	<div class="collapse-panel panel panel-group panel-default nts-ajax-parent" style="margin: 0.5em 0;">
		<div class="panel-heading">
			<h4 class="panel-title">
				<div class="pull-right">
					<span class="badge badge-default"><?php echo $count_upcoming_appointments; ?></span>
				</div>
				<a href="<?php echo ntsLink::makeLink('customer/appointments/view', '', array('show' => 'upcoming', 'display' => 'short')); ?>" data-toggle="collapse-next" class="display-block nts-ajax-loader">
					<?php echo M('My Upcoming Appointments'); ?> <span class="caret"></span>
				</a>
			</h4>
		</div>

		<div class="panel-collapse collapse">
			<div class="panel-body nts-ajax-container">
			</div>
		</div>
	</div>
<?php endif; ?>

<?php if( $count_past_appointments ) : ?>
	<div class="collapse-panel panel panel-group panel-default nts-ajax-parent" style="margin: 0.5em 0;">
		<div class="panel-heading">
			<h4 class="panel-title">
				<div class="pull-right">
					<span class="badge badge-default"><?php echo $count_past_appointments; ?></span>
				</div>
				<a href="<?php echo ntsLink::makeLink('customer/appointments/view', '', array('show' => 'old', 'display' => 'short')); ?>" data-toggle="collapse-next" class="display-block nts-ajax-loader">
					<?php echo M('My Past Appointments'); ?> <span class="caret"></span>
				</a>
			</h4>
		</div>

		<div class="panel-collapse collapse">
			<div class="panel-body nts-ajax-container">
			</div>
		</div>
	</div>
<?php endif; ?>
