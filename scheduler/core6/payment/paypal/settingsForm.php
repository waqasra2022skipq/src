<?php
echo ntsForm::wrapInput(
	M('Paypal Email'),
	$this->buildInput (
	/* type */
		'text',
	/* attributes */
		array(
			'id'		=> 'email',
			'default'	=> 'my@email.com',
			'attr'		=> array(
				'size'	=> 24,
				),
			),
	/* validators */
		array(
			array(
				'code'		=> 'notEmpty.php', 
				'error'		=> M('Required'),
				),
			)
		)
	);
?>
<?php
echo ntsForm::wrapInput(
	M('Label'),
	$this->buildInput (
	/* type */
		'text',
	/* attributes */
		array(
			'id'		=> 'label',
			'default'	=> 'Pay online with Paypal',
			'attr'		=> array(
				'size'	=> 24,
				),
			),
	/* validators */
		array(
			array(
				'code'		=> 'notEmpty.php', 
				'error'		=> M('Required'),
				),
			)
		)
	);
?>