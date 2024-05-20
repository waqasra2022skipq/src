<?php
$entries = ntsLib::getVar( 'admin/company/services/promotions::entries' );
$totalCols = 6;
?>

<p>
<?php
echo ntsLink::printLink(
	array(
		'panel'		=> '-current-/../create',
		'title'		=> '<i class="fa fa-plus"></i> ' . M('Promotion'),
		'attr'		=> array(
			'class'	=> 'btn btn-success',
			'title'	=> M('Add'),
			),
		)
	);
?>
</p>

<p>
<table class="table table-condensed table-striped2">
<?php if( count($entries) > 0 ) : ?>
<tbody>
<tr class="listing-header">
	<th style="width: 1em;">&nbsp;</th>
	<th><?php echo M('Price'); ?></th>
	<th><?php echo M('Title'); ?></th>
	<th><?php echo M('When'); ?></th>
	<th><?php echo M('Coupon Codes'); ?></th>
	<th><?php echo M('Usage Count'); ?></th>
</tr>
</tbody>
<?php endif; ?>

<?php $count = 0; ?>
<?php foreach( $entries as $e ) : ?>
<?php
$deleteLink = ntsLink::makeLink(
	'-current-/../edit/delete',
	'delete',
	array(
		'promotion_id' => $e->getId(),
		)
	);
$editLink = ntsLink::makeLink( 
	'-current-/../edit',
	'',
	array(
		'promotion_id' => $e->getId(),
		)
	);
?>
<tbody>
<tr>

<td style="width: 1em;">
	<a class="hc-confirm btn btn-default btn-xs" href="<?php echo $deleteLink; ?>" title="<?php echo M('Delete'); ?>">
		<i class="fa fa-times text-danger"></i>
	</a>
</td>

<td>
<?php
$thisView = $e->getModificationView();
?>
<a href="<?php echo $editLink; ?>"><?php echo $thisView; ?></a>
</td>

<td>
<?php echo $e->getTitle(); ?>
</td>

<?php
$thisView = array();
$rule = $e->getRuleView();
foreach( $rule as $r ){
	if( is_array($r) )
		$thisView[] = join( ': ', array( '<strong>' . $r[0] . '</strong>', join(', ', $r[1])) );
	else
		$thisView[] = '<strong>' . $r . '</strong>';
	}
$thisView = join( '<br>', $thisView );
?>
<td>
	<?php echo $thisView; ?>
</td>

<?php
$coupons = $e->getCoupons();
?>
<td>
<?php if( ! $coupons ) : ?>
<?php 	echo M('No'); ?>
<?php elseif( count($coupons) == 1 ) : ?>
<span style="font-style: italic;"><?php	echo $coupons[0]->getProp('code'); ?></span>
<?php else : ?>
<?php 	echo count($coupons); ?>
<?php endif; ?>
</td>

<td>
<?php
$useCount = $e->getUseCount();
?>
<?php echo $useCount; ?>
</td>

</tr>
</tbody>

<?php $count++; ?>
<?php endforeach; ?>
</table>