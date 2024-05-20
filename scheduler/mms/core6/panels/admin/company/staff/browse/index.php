<?php
$entries = ntsLib::getVar( 'admin/company/staff::entries' );
$totalCols = NTS_EMAIL_AS_USERNAME ? 2 : 3;
?>
<table class="table table-striped" style="table-layout: fixed;">

<?php if( count($entries) > 0 ) : ?>
<tr>
<th style="width: 4em;">ID</th>
<?php if( NTS_EMAIL_AS_USERNAME ) : ?>
	<th><?php echo M('Email'); ?></th>
<?php else: ?>
	<th><?php echo M('Username'); ?></th>
	<th><?php echo M('Email'); ?></th>
<?php endif; ?>
<th><?php echo M('Full Name'); ?></th>
<th><?php echo M('Access Level'); ?></th>
</tr>
<?php endif; ?>

<?php for( $ii = 0; $ii < count($entries); $ii++ ) : ?>
	<?php
	$e = $entries[$ii];
	?>
	<tr>
	<td>
	<?php echo $e->getId(); ?>
	</td>
	<td>
	<?php
	$title = NTS_EMAIL_AS_USERNAME ? $e->getProp('email') : $e->getProp('username');
	echo ntsLink::printLink(
		array(
			'panel'		=> '-current-/../edit/edit',
			'params'	=> array('_id' => $e->getId()),
			'title'		=> $title,
			),
		true
		);
	?>
	</td>

	<?php if( ! NTS_EMAIL_AS_USERNAME ) : ?>
	<td>
		<?php echo $e->getProp('email'); ?>
	</td>
	<?php endif; ?>

	<td>
		<?php echo ntsView::objectTitle($e); ?>
	</td>

	<td>
		<?php
		$level = $e->getProp('_admin_level');
		$admin_levels = array(
			'admin'	=> M('Administrator'),
			'staff'	=> M('Staff'),
			);
		echo isset($admin_levels[$level]) ? $admin_levels[$level] : $level;
		?>
	</td>
</tr>

<?php endfor; ?>

</table>