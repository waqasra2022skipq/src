<?php
echo $this->makeInput (
/* type */
	'date/Calendar',
/* attributes */
	array(
		'id'	=> 'due_at',
		),
	/* validators */
	array(
		array(
			'code'		=> 'notEmpty.php', 
			'error'		=> M('Required'),
			)
		)
	);
?>
<?php echo $this->makePostParams('-current-', 'updatedate' ); ?>
<INPUT class="btn btn-default" TYPE="submit" VALUE="<?php echo M('Save'); ?>">
