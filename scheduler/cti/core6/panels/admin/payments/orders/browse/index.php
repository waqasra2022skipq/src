<?php
$fixCustomer = ntsLib::getVar( 'admin/payments/orders::customer' );
$entries = ntsLib::getVar( 'admin/payments/orders::entries' );
$currentPage = ntsLib::getVar( 'admin/payments/orders::currentPage' );
$showFrom = ntsLib::getVar( 'admin/payments/orders::showFrom' );
$showTo = ntsLib::getVar( 'admin/payments/orders::showTo' );
$totalCount = ntsLib::getVar( 'admin/payments/orders::totalCount' );
$showPerPage = ntsLib::getVar( 'admin/payments/orders::showPerPage' );
$search = ntsLib::getVar( 'admin/payments/orders::search' );

$t = $NTS_VIEW['t'];
$totalCols = 10;
if( $fixCustomer )
	$totalCols--;

$now = time();
$t->setNow();
$today = $t->formatDate_Db();

include_once( NTS_LIB_DIR . '/lib/view/ntsPager.php' );
$pager = new ntsPager( $totalCount, $showPerPage, 10 );
$pager->setPage( $currentPage );

$pages = $pager->getPages();
reset( $pages );
reset( $pages );
$pagerParams = array();
if( $NTS_VIEW['search'] )
	$pagerParams['search'] = $NTS_VIEW['search'];

$packs = ntsObjectFactory::getAllIds( 'pack' );
?>

<?php if( ! count($entries) ) : ?>
	<p>
	<?php echo M('None'); ?>
<?php endif; ?>

<p>
<?php if( $packs ) : ?>
	<div class="nts-ajax-parent">

	<?php if( $fixCustomer ) : ?>
		<div>
		<?php
		echo ntsLink::printLink(
			array(
				'panel'		=> '-current-/../create',
				'title'		=> '<i class="fa fa-plus"></i> ' . M('Add'),
				'params'	=> array(
					'customer'	=> $fixCustomer,
					NTS_PARAM_VIEW_RICH	=> 'basic',
					),
				'attr'		=> array(
					'class'	=> 'nts-ajax-loader btn btn-success',
					),
				)
			);
		?>
		</div>
	<?php elseif( 0 ) : ?>
		<div>
		<?php
		echo ntsLink::printLink(
			array(
				'panel'		=> '-current-/../create',
				'title'		=> '<i class="fa fa-plus"></i> ' . M('Add To Customer'),
				'attr'		=> array(
					'class'	=> 'nts-ajax-loader btn btn-success',
					),
				)
			);
		?>
		</div>
	<?php endif; ?>

	<div class="nts-ajax-container nts-child nts-ajax-return">
	</div>
	</div>
<?php endif; ?>

<?php if( count($entries) ) : ?>

<div class="text-right">
	<p>
	<ul class="list-inline">
		<li>
			[<?php echo $showFrom; ?> - <?php echo $showTo; ?> of <?php echo $totalCount; ?>]
		</li>

		<?php if( count($pages) > 1 ) : ?>
			<li>
			&nbsp;&nbsp;<?php echo M('Pages'); ?>: 
			<?php foreach( $pages as $pi ): ?>
				<?php if( $currentPage != $pi['number'] ) : ?>
					<?php $pagerParams['p'] = $pi['number']; ?>
					<a href="<?php echo ntsLink::makeLink('-current-', '', $pagerParams ); ?>"><?php echo $pi['title']; ?></a>
				<?php else : ?>
					<b><?php echo $pi['title']; ?></b>
				<?php endif; ?>
			<?php endforeach; ?>
			</li>
		<?php endif; ?>
	</ul>
</div>

<table class="table table-striped2 table-condensed">
<tbody>
<tr>
<?php if ($NTS_VIEW[NTS_PARAM_VIEW_MODE] != 'print') : ?>
<th>&nbsp;</th>
<?php endif; ?>
<th style="width: 4em;"><?php echo M('Status'); ?></th>
<th><?php echo M('Created'); ?></th>
<th><?php echo M('Package'); ?></th>
<?php if( ! $fixCustomer ) : ?>
<th><?php echo M('Customer'); ?></th>
<?php endif; ?>

</tr>
</tbody>

<?php for( $ii = 0; $ii < count($entries); $ii++ ) : ?>
<?php
$e = $entries[$ii];
$deps = $e->getItems();
$deleteLink = ntsLink::makeLink( '-current-/../edit/delete', '', array('order_id' => $e->getId()) );
?>
<tbody class="nts-ajax-parent">
<tr>

<?php if ($NTS_VIEW[NTS_PARAM_VIEW_MODE] != 'print') : ?>
	<td style="width: 1em;">
		<a class="nts-ajax-loader btn btn-default btn-xs" href="<?php echo $deleteLink; ?>" title="<?php echo M('Delete'); ?>">
		<span class="close text-danger">&times;</span>
		</a>
	</td>
<?php endif; ?>

<td>
	<?php
	$isActive = $e->getProp( 'is_active' );
	$thisView = $isActive ? M('Active') : M('Not Active');
	$linkTitle = $isActive ? M('Disable') : M('Activate');
	?>
	<?php if( (! $isActive) ) : ?>
		<a class="btn btn-xs btn-danger" href="<?php echo ntsLink::makeLink('-current-/../edit/toggle', '', array('order_id' => $e->getId())); ?>" title="<?php echo $linkTitle; ?>">
			<?php echo $thisView; ?>
		</a>
	<?php else : ?>
		<a class="btn btn-xs btn-success" href="<?php echo ntsLink::makeLink('-current-/../edit/toggle', '', array('order_id' => $e->getId())); ?>" title="<?php echo $linkTitle; ?>">
			<?php echo $thisView; ?>
		</a>
	<?php endif; ?>
</td>

<td>
	<?php
	$t->setTimestamp( $e->getProp('created_at') );
	$dateView = $t->formatDate();
	?>
	<?php echo $dateView; ?>

</td>

<td>
	<?php
	$pack_id = $e->getProp('pack_id');
	$pack = ntsObjectFactory::get( 'pack', $pack_id );
	$thisView = ntsView::objectTitle( $pack );
	?>
	<a target="_blank" href="<?php echo ntsLink::makeLink('admin/company/services/packs/edit', '', array('_id' => $pack_id)); ?>">
		<?php echo $thisView; ?>
	</a>
</td>

<?php if( ! $fixCustomer ) : ?>
<td>
<?php
$customer = $e->getCustomer();
$customerView = $customer->getProp('first_name') . ' ' . $customer->getProp('last_name');
?>
<?php echo $customerView; ?>
</td>
<?php endif; ?>

</tr>
<tr>
<td colspan="<?php echo $totalCols; ?>" class="nts-ajax-container nts-child" style="padding-left: 2em;"></td>
</tr>

</tbody>
<?php endfor; ?>

</table>

<?php endif; ?>
