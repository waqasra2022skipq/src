<h3><?php echo M('Change Role'); ?></h3>
<?php
$admin_levels = array(
	array( 'admin',	M('Administrator') ),
	array( 'staff',	M('Staff') ),
	);

$this_readonly = ( $id == ntsLib::getCurrentUserId() ) ? TRUE : FALSE;
echo ntsForm::wrapInput(
	M('Access Level'),
	$this->buildInput (
	/* type */
		'select',
	/* attributes */
		array(
			'id'		=> '_admin_level',
			'options'	=> $admin_levels,
			'default'	=> 'admin',
			'help'		=> M('Staff do not have access to company configuration, payments, and system settings'),
			'readonly'	=> $this_readonly,
			)
		)
	);
?>
<?php echo $this->makePostParams('-current-', 'update'); ?>
<?php
echo ntsForm::wrapInput(
	'',
	'<INPUT class="btn btn-default" TYPE="submit" VALUE="' . M('Update') . '">'
	);
?>