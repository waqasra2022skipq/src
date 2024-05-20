<?php
echo ntsForm::wrapInput(
	M('Pick one randomly from available ones in the front end'),
	$this->buildInput (
	/* type */
		'checkbox',
	/* attributes */
		array(
			'id'	=> 'autoResource',
			)
		),
	FALSE
	);
?>

<?php echo $this->makePostParams('-current-', 'update'); ?>
<INPUT class="btn btn-default" TYPE="submit" VALUE="<?php echo M('Save'); ?>">
