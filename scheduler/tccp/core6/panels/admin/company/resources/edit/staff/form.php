<?php
echo $this->makeInput (
/* type */
	'resourceAdmins',
/* attributes */
	array(
		'id'	=> 'staff',
		)
	);
?>
<p>
<?php echo $this->makePostParams('-current-', 'update'); ?>
<INPUT class="btn btn-default" TYPE="submit" VALUE="<?php echo M('Update'); ?>">
