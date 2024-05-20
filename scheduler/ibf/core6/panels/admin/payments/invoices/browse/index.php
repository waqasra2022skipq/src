<?php
$entries = ntsLib::getVar( 'admin/payments/invoices::entries' );
$currentPage = ntsLib::getVar( 'admin/payments/invoices::currentPage' );
$showFrom = ntsLib::getVar( 'admin/payments/invoices::showFrom' );
$showTo = ntsLib::getVar( 'admin/payments/invoices::showTo' );
$totalCount = ntsLib::getVar( 'admin/payments/invoices::totalCount' );
$showPerPage = ntsLib::getVar( 'admin/payments/invoices::showPerPage' );
$search = ntsLib::getVar( 'admin/payments/invoices::search' );

$t = $NTS_VIEW['t'];
$totalCols = 6;

$now = time();

include_once( NTS_LIB_DIR . '/lib/view/ntsPager.php' );
$pager = new ntsPager( $totalCount, $showPerPage, 5 );
$pager->setPage( $currentPage );

$pages = $pager->getPages();
reset( $pages );
reset( $pages );
$pagerParams = array();
if( $NTS_VIEW['search'] )
	$pagerParams['search'] = $NTS_VIEW['search'];

$amounts = array();	
for( $ii = 0; $ii < count($entries); $ii++ ){
	$inv = $entries[$ii];
	$totalAmount = $inv->getTotalAmount();
	$paidAmount = $inv->getPaidAmount();
	$amounts[ $ii ] = array( $totalAmount, $paidAmount );
	}

$customerId = ntsLib::getVar( 'admin/payments/invoices::customer' );
if( $customerId )
{
	// compile totals
	$grandTotalAmount = 0;
	$grandPaidAmount = 0;
	for( $ii = 0; $ii < count($entries); $ii++ )
	{
		$grandTotalAmount += $amounts[ $ii ][0];
		$grandPaidAmount += $amounts[ $ii ][1];
	}
}
?>

<?php if( $showPerPage != 'all' ) : ?>
<p>
<div class="row">
	<div class="col-sm-6">
		<ul class="pagination pagination-sm">
			<li class="disabled">
			<a>[<?php echo $showFrom; ?> - <?php echo $showTo; ?> of <?php echo $totalCount; ?>]</a>
			</li>

		<?php if( count($pages) > 1 ) : ?>
			<?php foreach( $pages as $pi ): ?>
				<?php if( $currentPage != $pi['number'] ) : ?>
					<?php $pagerParams['p'] = $pi['number']; ?>
					<li>
						<a href="<?php echo ntsLink::makeLink('-current-', '', $pagerParams ); ?>"><?php echo $pi['title']; ?></a>
					</li>
				<?php else : ?>
					<li class="active">
						<a href="<?php echo ntsLink::makeLink('-current-', '', $pagerParams ); ?>"><?php echo $pi['title']; ?></a>
					</li>
				<?php endif; ?>
			<?php endforeach; ?>
		<?php endif; ?>
		</ul>
	</div>

	<div class="col-sm-6">
		<?php $NTS_VIEW['searchForm']->display(); ?>
	</div>
</div>
<?php endif; ?>

<div class="clearfix"></div>

<?php if( $customerId ) : ?>
	<ul class="list-inline list-separated">
		<li>
			<?php echo M('Total Amount'); ?>
		</li>
		<li>
			<span class="btn btn-default"><?php echo ntsCurrency::formatPrice($grandTotalAmount); ?></span>
		</li>
		<li>
			<?php echo M('Total Paid'); ?>
		</li>
		<li>
			<span class="btn btn-default"><?php echo ntsCurrency::formatPrice($grandPaidAmount); ?></span>
		</li>

		<li class="divider hidden-xs">&nbsp;</li>
		<li>
			<a href="<?php echo ntsLink::makeLink('-current-/../create'); ?>" class="btn btn-success">
				<i class="fa fa-plus"></i> <?php echo M('Invoice'); ?>
			</a>
		</li>

	</ul>
<?php endif; ?>

<p>
<table class="table table-striped2 table-condensed">

<?php if( ! count($entries) ) : ?>
<?php echo M('None'); ?>
<?php else : ?>

<tr>
<th><?php echo M('Due Date'); ?></th>
<th><?php echo M('Refno'); ?></th>
<th><?php echo M('Amount'); ?></th>
<th><?php echo M('Status'); ?></th>
<?php if( ! $customerId ) : ?>
	<th><?php echo M('Customer'); ?></th>
<?php endif; ?>

</tr>

<?php for( $ii = 0; $ii < count($entries); $ii++ ) : ?>
<?php
$inv = $entries[$ii];
list( $totalAmount, $paidAmount ) = $amounts[ $ii ];
?>
<tbody class="nts-ajax-parent">
<tr>

<td>
<?php
$dueAt = $inv->getProp('due_at');
if( $dueAt > 0 ){
	$t->setTimestamp( $inv->getProp('due_at') );
	$dueDateView = $t->formatDate();
	}
else {
	$dueDateView = M('N/A');
	}

$t->setTimestamp( $inv->getProp('created_at') );
$createdView = $t->formatDate();
?>
<?php echo $dueDateView; ?>
</td>

<td>
	<a class="nts-no-ajax" target="_blank" href="<?php echo ntsLink::makeLink('admin/payments/invoices/edit/edit', '', array('_id' => $inv->getId())); ?>">
	<?php echo ntsLib::viewHighlighted( $inv->getProp('refno'), $search ); ?>
	</a>
</td>

<td>
<?php echo ntsCurrency::formatPrice($totalAmount); ?>
</td>

<td>
	<?php
	$balance = $paidAmount - $totalAmount;
	$items = $inv->getItems();
	?>
	<?php if( ! $items ) : ?>
		<span class="text-muted"><?php echo M('New'); ?></span>
	<?php else : ?>
		<?php if( $balance > 0 ) : ?>
			<span class="text-success"><?php echo ntsCurrency::formatPrice($balance); ?></span>
		<?php elseif( ($balance == 0) && ($paidAmount > 0)) : ?>
			<span class="text-success"><?php echo M('Paid'); ?></span>
		<?php elseif( $balance < 0 ) : ?>
			<?php if( $now > $inv->getProp('due_at') ) : ?>
				<span class="text-danger"><?php echo ntsCurrency::formatPrice($balance); ?></span>
			<?php else : ?>
				<?php echo ntsCurrency::formatPrice($balance); ?>
			<?php endif; ?>
		<?php else : ?>
			&nbsp;
		<?php endif; ?>
	<?php endif; ?>
</td>

<?php if( ! $customerId ) : ?>
	<td>
		<?php
		$customer = $inv->getCustomer();
		?>
		<a target="_blank" href="<?php echo ntsLink::makeLink('admin/customers/edit/edit', '', array('_id' => $customer->getId())); ?>">
			<?php echo ntsView::objectTitle( $customer ); ?>
		</a>
	</td>
<?php endif; ?>
</tr>

<tr>
<td colspan="<?php echo $totalCols; ?>" class="nts-ajax-container nts-child nts-ajax-return" style="padding-left: 2em;"></td>
</tr>
</tbody>
<?php endfor; ?>

<?php endif; ?>

</table>