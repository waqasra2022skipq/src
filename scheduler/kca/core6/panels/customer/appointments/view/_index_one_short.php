<?php
$conf =& ntsConf::getInstance();
$auto_resource = $conf->get('autoResource');
$auto_location = $conf->get('autoLocation');

$completedStatus = $a->getProp('completed');
$approvedStatus = $a->getProp('approved');

$service = ntsObjectFactory::get( 'service' );
$service->setId( $a->getProp('service_id') );

$displayColumns = array();
if( ! (NTS_SINGLE_LOCATION OR $auto_location) )
	$displayColumns[] = 'location';
if( ! (NTS_SINGLE_RESOURCE OR $auto_resource) )
	$displayColumns[] = 'resource';

/* due payment */
$cost = $a->getCost();
$payment_options = array();
$default_payment_option = '';

/* get any promotions applied for this appointment */
$promotions = array();
$am =& ntsAccountingManager::getInstance();
$acc_postings = $am->get_postings( $a->getClassName(), $a->getId() );
foreach( $acc_postings as $ap ){
	$promotion = NULL;
	switch( $ap['obj_class'] ){
		case 'promotion':
			$promotion = ntsObjectFactory::get('promotion');
			$promotion->setId( $ap['obj_id'] );
			break;
		case 'coupon':
			$coupon = ntsObjectFactory::get('coupon');
			$coupon->setId( $ap['obj_id'] );
			$promotion = ntsObjectFactory::get('promotion');
			$promotion->setId( $coupon->getProp('promotion_id') );
			break;
	}
	if( $promotion ){
		$promotions[] = $promotion;
	}
}

if( $cost )
{
	$due = $a->getDue();
	$paid = $a->getPaidAmount();

	$balance_cover = array();
	if( $customer_balance )
	{
		$balance_cover = $am->balance_cover( $customer_balance, $a );
	}
	$displayColumns[] = 'payment';

	if( $group_ref )
	{
		require( dirname(__FILE__) . '/_payment_group.php' );
	}
	else
	{
		require( dirname(__FILE__) . '/_payment_browse.php' );
	}
}
?>

<?php
$t->setTimestamp( $a->getProp('starts_at') );

$dateView = $t->formatDateFull();
$fullDateView = '<i class="fa fa-fw fa-calendar"></i>' . $dateView;

$timeView = $t->formatTime();
$fullTimeView = '<i class="fa fa-fw fa-clock-o"></i>' . $timeView;

$status_class = $a->statusClass();
$status_text = $a->statusText();

$collapse_in = $group_ref ? ' in' : '';
$collapse_in = ' in';

$app_seats = $a->getProp('seats');
?>
<li class="collapse-panel panel panel-default panel-<?php echo $status_class; ?>">
	<div class="panel-heading" title="<?php echo $status_text; ?>">
		<span class="xs-block"><?php echo $fullDateView; ?></span>
		<span class="xs-block"><?php echo $fullTimeView; ?></span>
		<span class="xs-block"><?php echo ntsView::objectTitle( $service, TRUE ); ?></span>
	</div>
</li>
