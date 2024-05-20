<?php
echo ntsForm::wrapInput(
	M('Automatically Activate Packages Even Without Payment'),
	$this->buildInput (
	/* type */
		'checkbox',
	/* attributes */
		array(
			'id'	=> 'autoActivatePackage',
			)
		),
	FALSE
	);
?>

<?php echo $this->makePostParams('-current-', 'update'); ?>
<INPUT class="btn btn-default" TYPE="submit" VALUE="<?php echo M('Save'); ?>">
