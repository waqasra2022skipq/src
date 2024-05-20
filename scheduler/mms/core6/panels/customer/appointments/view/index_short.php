<?php
$now = time();
$t = $NTS_VIEW['t'];

$pgm =& ntsPaymentGatewaysManager::getInstance();
$pm =& ntsPaymentManager::getInstance();

$has_online = $pgm->hasOnline();
$has_offline = $pgm->hasOffline();

$conf =& ntsConf::getInstance();
$canCancel = $conf->get('customerCanCancel');
$canReschedule = $conf->get('customerCanReschedule');
$canReschedule = 0;

$aam =& ntsAccountingAssetManager::getInstance();
$am =& ntsAccountingManager::getInstance();

$grand_total_amount = 0;
$grand_prepay_amount = 0;
$grand_paid_amount = 0;
$grand_balance_count = 0;
$grand_due_amount = 0;
?>

<?php if( ! $objects ) : ?>
	<p>
	<?php echo M('None'); return; ?>
	</p>
<?php endif; ?>

<ul class="nav nav-pills" style="margin: 0 0 0.5em 0;">
	<li>
		<a href="<?php echo ntsLink::makeLink('-current-', '', array('show' => $show)); ?>" class="nts-no-ajax">
			<?php echo M('Go To Detailed View'); ?>
		</a>
	</li>
</ul>
<hr>

<ul class="list-unstyled">
<?php foreach( $objects as $a ) : ?>
	<?php
	$t->setTimestamp( $a->getProp('starts_at') );
	$dateView = $t->formatDateFull();
	$dateView = $t->getMonthName() . ' ' . $t->getYear();
	?>
	<?php if( ! isset($datesShown[$dateView]) ) : ?>
		<li>
			<h3><?php echo $dateView; ?></h3>
		</li>
		<?php $datesShown[$dateView] = 1; ?>
	<?php endif; ?>

	<?php 
	require( dirname(__FILE__) . '/_index_one_short.php' );
	?>
<?php endforeach; ?>
</ul>