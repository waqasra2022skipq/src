<?php
$entries = ntsLib::getVar( 'admin/company/locations::entries' );
$totalCols = 2;
$editPanel = '-current-/../edit/edit';
$createPanel = '-current-/../create';

$showForm = ( count($entries) > 1 ) ? TRUE : FALSE;
?>
<table class="table table-striped table-condensed">

<?php if( count($entries) > 0 ) : ?>
<thead>
<tr>
<th><?php echo M('Title'); ?></th>

<?php if( $showForm ) : ?>
<th><?php echo M('Show Order'); ?></th>
<?php else : ?>
<th>&nbsp;</th>
<?php endif; ?>

</tr>
</thead>
<?php endif; ?>

<?php for( $ii = 0; $ii < count($entries); $ii++ ) : ?>
<?php 	
$e = $entries[$ii];
$editLink = ntsLink::makeLink( $editPanel, '', array('_id' => $e->getId()) );
?>
<tr>
<td>
<?php
echo ntsLink::printLink(
	array(
		'panel'		=> $editPanel,
		'params'	=> array('_id' => $e->getId()),
		'title'		=> ntsView::objectTitle($e),
		),
	true
	);
?>

<p class="text-muted text-smaller">
	id: <?php echo $e->getId(); ?>
</p>

<?php if( $e->getProp('capacity') ) : ?>
	<p>
		<?php echo M('Capacity'); ?>: <?php echo $e->getProp('capacity'); ?> <?php echo M('Seats'); ?>
	</p>
<?php endif; ?>

<?php if( $e->getProp('archive') ) : ?>
	<p>
		<span class="label label-archive"><?php echo M('Archived'); ?></span>
	</p>
<?php endif; ?>


</td>

<td>

<?php if( $showForm ) : ?>

<?php
	echo $this->makeInput (
	/* type */
		'text',
	/* attributes */
		array(
			'id'		=> 'order_' . $e->getId(),
			'attr'		=> array(
				'size'	=> 2,
				),
			),
	/* validators */
		array(
			array(
				'code'		=> 'notEmpty.php', 
				'error'		=> M('Required'),
				),
			array(
				'code'		=> 'integer.php', 
				'error'		=> M('Numbers only'),
				),
			)
		);
?>

<?php elseif( count($entries) > 1 ) : ?>

<?php
echo ntsLink::printLink(
	array(
		'panel'		=> $editPanel,
		'action'	=> 'up',
		'params'	=> array('_id' => $e->getId()),
		'title'		=> M('Up'),
		'attr'		=> array(
			'class'	=> 'ok',
			),
		)
	);
?>

<?php
echo ntsLink::printLink(
	array(
		'panel'		=> $editPanel,
		'action'	=> 'down',
		'params'	=> array('_id' => $e->getId()),
		'title'		=> M('Down'),
		'attr'		=> array(
			'class'	=> 'ok',
			),
		)
	);
?>
<?php endif; ?>
</td>
</tr>

<?php endfor; ?>

<?php if( $showForm ) : ?>
<tr>
<td colspan="<?php echo ($totalCols - 1); ?>"></td>
<td>
<?php echo $this->makePostParams('-current-', 'update'); ?>
<INPUT TYPE="submit" class="btn btn-default" VALUE="<?php echo M('Update'); ?>">
</td>
</tr>
<?php endif; ?>

</table>