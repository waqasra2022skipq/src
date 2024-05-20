<?php
echo ntsForm::wrapInput(
	'Username',
	$this->buildInput (
	/* type */
		'text',
	/* attributes */
		array(
			'id'		=> 'username',
			'default'	=> 'username',
			'attr'		=> array(
				'size'	=> 32,
				),
			'required'	=> 1,
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
	'Password',
	$this->buildInput (
	/* type */
		'text',
	/* attributes */
		array(
			'id'		=> 'password',
			'default'	=> 'password',
			'attr'		=> array(
				'size'	=> 32,
				),
			'required'	=> 1,
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