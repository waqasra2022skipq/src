<?php
echo ntsForm::wrapInput(
	M('Discount'),
	$this->buildInput (
	/* type */
		'text',
	/* attributes */
		array(
			'id'		=> 'discount',
			'attr'		=> array(
				'size'	=> 6,
				),
			),
	/* validators */
		array(
			array(
				'code'		=> 'notEmpty.php', 
				'error'		=> M('Required'),
				),
			array(
				'code'		=> 'number.php', 
				'error'		=> M('Numbers only'),
				),
			)
		)
	);
?>

<?php 
echo $this->makePostParams(
	'-current-',
	'discount'
	);
?>

<?php
echo ntsForm::wrapInput(
	'',
	'<INPUT class="btn btn-default" TYPE="submit" VALUE="' . M('Add') . '">'
	);
?>