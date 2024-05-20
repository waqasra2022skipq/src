<?php
$entries = ntsLib::getVar( 'admin/company/locations::entries' );
?>

<table class="table table-striped table-condensed">

<thead>
<tr>
<th></th>
<th></th>
<th></th>
<th><?php echo M('Travel Time'); ?></th>
</tr>
</thead>

<?php //for( $ii = 0; $ii < count($entries); $ii++ ) : ?>
<?php for( $ii = 0; $ii < 0; $ii++ ) : ?>
<tr>
<td><?php echo M('Office'); ?></td>
<td>&lt;-&gt;</td>
<td><?php echo ntsView::objectTitle($entries[$ii]); ?></td>
<td>
<?php
	$key = 'travel-' . 0 . '-' . $entries[$ii]->getId();
	echo $this->makeInput (
	/* type */
		'period/HourMinute',
	/* attributes */
		array(
			'id'	=> $key,
			),
	/* validators */
		array(
			)
		);
?>
</td>

<?php endfor; ?>


<?php for( $ii = 0; $ii < count($entries); $ii++ ) : ?>
<?php 	for( $jj = ($ii + 1); $jj < count($entries); $jj++ ) : ?>
<tr>
<td><?php echo ntsView::objectTitle($entries[$ii]); ?></td>
<td>&lt;-&gt;</td>
<td><?php echo ntsView::objectTitle($entries[$jj]); ?></td>

<td>
<?php
	$key = 'travel-' . $entries[$ii]->getId() . '-' . $entries[$jj]->getId();
	echo $this->makeInput (
	/* type */
		'period/HourMinute',
	/* attributes */
		array(
			'id'	=> $key,
			),
	/* validators */
		array(
			)
		);
?>
</td>

</tr>
<?php 	endfor; ?>
<?php endfor; ?>


<tr>
<td colspan="3">&nbsp;</td>
<td>
<?php echo $this->makePostParams('-current-', 'update'); ?>
<INPUT class="btn btn-default" TYPE="submit" VALUE="<?php echo M('Update'); ?>">
</td>
</tr>

</table>
