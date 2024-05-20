<?php
echo $this->makeInput (
/* type */
	'adminResources',
/* attributes */
	array(
		'id'	=> 'resources',
		)
	);
?>
<p>
<DIV CLASS="buttonBar">
<?php echo $this->makePostParams('-current-', 'update'); ?>
<INPUT class="btn btn-default" TYPE="submit" VALUE="<?php echo M('Update'); ?>">
</DIV>