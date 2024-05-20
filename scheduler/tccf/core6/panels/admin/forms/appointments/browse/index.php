<table class="table table-striped">
<tr>
	<th><?php echo M('Title'); ?></th>
	<th><?php echo M('Form Fields'); ?></th>
	<th><?php echo M('Services'); ?></th>
	<th>&nbsp;</th>
</tr>

<?php foreach( $NTS_VIEW['entries'] as $e ) : ?>
<tr>
	<td>
		<a href="<?php echo ntsLink::makeLink('-current-/../edit/controls', '', array('_id' => $e['id']) ); ?>"><?php echo $e['title']; ?></a>
	</td>
	<td>
		<?php echo $e['count_fields']; ?>
	</td>
	<td>
		<?php echo $e['count_services']; ?>
	</td>
	<td>
		<a href="<?php echo ntsLink::makeLink('-current-/../edit/delete', '', array('_id' => $e['id']) ); ?>"><?php echo M('Delete'); ?></a>
	</td>
</tr>
<?php endforeach; ?>
</table>