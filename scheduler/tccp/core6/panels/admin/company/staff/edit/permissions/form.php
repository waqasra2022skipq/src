<?php
echo $this->makeInput (
/* type */
	'adminPanels',
/* attributes */
	array(
		'id'		=> '_disabled_panels',
		)
	);
?>
<p>
<DIV CLASS="buttonBar">
<?php echo $this->makePostParams('-current-', 'update'); ?>
<INPUT class="btn btn-default" TYPE="submit" VALUE="<?php echo M('Update'); ?>">
</DIV>