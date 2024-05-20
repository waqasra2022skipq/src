<?php
$advanced_fields = TRUE;
$count = ntsLib::getVar( 'admin/payments/transactions::totalCount' );
$limit = ntsLib::getVar( 'admin/payments/transactions::limit' );
$invoice = ntsLib::getVar( 'admin/payments/transactions::invoice' );
$entries = ntsLib::getVar( 'admin/payments/transactions::entries' );
$transactionsAmount = ntsLib::getVar( 'admin/payments/transactions::transactionsAmount' );

$totalAmount = $invoice ? $invoice->getTotalAmount() : 0;
$dueAmount = ($totalAmount > $transactionsAmount) ? ($totalAmount - $transactionsAmount) : 0;

$t = $NTS_VIEW['t'];

$totalCols = 7;
if( $invoice ){
	$totalCols -= 1;
}
?>

<?php if( isset($NTS_VIEW['dateForm']) ) : ?>
	<p>
	<?php $NTS_VIEW['dateForm']->display(); ?>
	</p>
<?php endif; ?>

<?php if( ! count($entries) ) : ?>
	<p><?php echo M('None'); ?>
<?php endif; ?>

<?php if( ($transactionsAmount < $totalAmount) && ($NTS_VIEW[NTS_PARAM_VIEW_MODE] != 'print') ) : ?>
	<div class="nts-ajax-parent">
	<?php
	echo ntsLink::printLink(
		array(
			'panel'		=> 'admin/payments/transactions/add',
			'params'	=> array(
				'invoice'	=> $invoice->getId(),
				'default'	=> $dueAmount
				),
			'title'		=> '<i class="fa fa-plus"></i> ' . M('Payment'),
			'attr'		=> array(
				'class'	=> 'nts-ajax-loader btn btn-info btn-sm',
				),
			)
		);
	?>
	<div class="nts-ajax-container nts-child"></div>
	</div>
<?php endif; ?>

<?php if( count($entries) ) : ?>

<?php if( $limit && ($limit < $count) ) : ?>
	<p>
	Total <?php echo $count; ?> transactions, showing <?php echo $limit; ?> latest
<?php endif; ?>

<?php if( count($entries) ) : ?>
<?php
		$mcalc = new ntsMoneyCalc;
		for( $ii = 0; $ii < count($entries); $ii++ ){
			$tra = $entries[$ii];
			$mcalc->add( $tra->getProp('amount') );
		}
		$grand_total = $mcalc->result();
?>
	<?php echo M('Total'); ?>: <?php echo ntsCurrency::formatPrice($grand_total); ?>
<?php endif; ?>

<p>
<table class="table table-striped2 table-condensed">

<tr>
<?php if ($NTS_VIEW[NTS_PARAM_VIEW_MODE] != 'print') : ?>
<th style="width: 1em;">&nbsp;</th>
<?php endif; ?>

<th>&nbsp;</th>
<th><?php echo M('Date'); ?></th>
<th><?php echo M('Amount'); ?></th>

<?php if( ! $invoice ) : ?>
<th><?php echo M('Invoice'); ?></th>
<?php endif; ?>
<th><?php echo M('Paid Through'); ?></th>
<th><?php echo M('Notes'); ?></th>

<?php if( $advanced_fields ) : ?>
	<?php if( ! defined('NTS_SINGLE_RESOURCE') ) : ?>
		<th><?php echo M('Bookable Resource'); ?></th>
	<?php endif; ?>
	<?php if( ! defined('NTS_SINGLE_LOCATION') ) : ?>
		<th><?php echo M('Location'); ?></th>
	<?php endif; ?>
	<th><?php echo M('Customer'); ?></th>
	<th><?php echo M('Service'); ?></th>
	<th><?php echo M('Date'); ?></th>
	<th><?php echo M('Time'); ?></th>
<?php endif; ?>

</tr>

<?php for( $ii = 0; $ii < count($entries); $ii++ ) : ?>
<?php
$view = array();
$tra = $entries[$ii];

$deleteLink = ntsLink::makeLink( 'admin/payments/edit/delete', '', array('transid' => $tra->getId()) );

$thisInvoiceId = $tra->getProp('invoice_id');
if( $thisInvoiceId ){
	$thisInvoice = ntsObjectFactory::get('invoice');
	$thisInvoice->setId( $thisInvoiceId );
	$view['invoice'] = $thisInvoice->getProp('refno');
	$view['paid_through'] = $tra->getProp('pgateway');
	$view['paid_through'] = M( ntsLib::upperCaseMe($view['paid_through']) );

	if( $tra->getProp('pgateway_ref') ){
//		$view['notes'] = $tra->getProp('pgateway_ref') . '<br>' . $tra->getProp('pgateway_response');
		$view['notes'] = $tra->getProp('pgateway_ref');
		}
	else {
		$view['notes'] = $tra->getProp('pgateway_response');
		}

		if( $advanced_fields ){
		/* check if invoice contains only one item */
			$items = $thisInvoice->getItems();
			if( count($items) == 1 )
			{
				switch( $items[0]['object']->getClassName() )
				{
					case 'appointment':
						$rid = $items[0]['object']->getProp('resource_id');
						$resource = ntsObjectFactory::get('resource');
						$resource->setId( $rid );
						$view['resource'] = ntsView::objectTitle( $resource );

						$lid = $items[0]['object']->getProp('location_id');
						$location = ntsObjectFactory::get('location');
						$location->setId( $lid );
						$view['location'] = ntsView::objectTitle( $location );

						$cid = $items[0]['object']->getProp('customer_id');
						$customer = new ntsUser;
						$customer->setId( $cid );
						$view['customer'] = ntsView::objectTitle( $customer );

						$sid = $items[0]['object']->getProp('service_id');
						$service = ntsObjectFactory::get('service');;
						$service->setId( $sid );
						$view['service'] = ntsView::objectTitle( $service );

						$t->setTimestamp( $items[0]['object']->getProp('starts_at') );
						$view['date'] = $t->formatDate();
						$view['time'] = $t->formatTime();

						$view['app_id'] = $items[0]['object']->getId();
						break;
				}
			}
		}
	}
else {
	$view['invoice'] = M('N/A');
	$view['paid_through'] = '&nbsp;';
	$view['notes'] = '';
	}
?>

<tbody class="nts-ajax-parent">
<tr>

<?php if ($NTS_VIEW[NTS_PARAM_VIEW_MODE] != 'print') : ?>
<td>
	<a class="nts-ajax-loader btn btn-default btn-xs" href="<?php echo $deleteLink; ?>" title="<?php echo M('Delete'); ?>">
		<span class="close2 text-danger">&times;</span>
	</a>
</td>
<?php endif; ?>

<td>
#<?php echo $tra->getId(); ?>
</td>

<td>
<?php
$t->setTimestamp( $tra->getProp('created_at') );
$dateView = $t->formatFull();
?>
<?php echo $dateView; ?>
</td>

<td>
<?php echo ntsCurrency::formatPrice($tra->getProp('amount')); ?>
</td>

<?php if( ! $invoice ) : ?>
<td>
<?php if( $thisInvoiceId ) : ?>
	<a class="nts-no-ajax" target="_blank" href="<?php echo ntsLink::makeLink('admin/payments/invoices/edit/edit', '', array('_id' => $thisInvoiceId )); ?>">
	<?php echo $view['invoice']; ?>
	</a>
<?php else : ?>
	<?php echo $view['invoice']; ?>
<?php endif; ?>
</td>
<?php endif; ?>

<td><?php echo $view['paid_through']; ?></td>
<td><?php echo $view['notes']; ?></td>

<?php if( $advanced_fields ) : ?>
	<?php if( ! defined('NTS_SINGLE_RESOURCE') ) : ?>
		<td><?php if( isset($view['resource']) ){ echo $view['resource']; }; ?></td>
	<?php endif; ?>
	<?php if( ! defined('NTS_SINGLE_LOCATION') ) : ?>
		<td><?php if( isset($view['location']) ){ echo $view['location']; }; ?></td>
	<?php endif; ?>
	<td><?php if( isset($view['customer']) ){ echo $view['customer']; }; ?></td>
	<td><?php if( isset($view['service']) ){ echo $view['service']; }; ?></td>
	<td><?php if( isset($view['date']) ){ echo $view['date']; }; ?></td>
	<td><?php if( isset($view['time']) ){ echo $view['time']; }; ?></td>
<?php endif; ?>

</tr>

<tr>
<?php
$totalCols = count($view);
?>
<td colspan="<?php echo $totalCols; ?>" class="nts-ajax-container nts-child"></td>
</tr>

</tbody>

<?php endfor; ?>

</table>
<?php endif; ?>

