<?php
echo ntsForm::wrapInput(
	'Clickatell Username',
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
	'Clickatell API ID',
	$this->buildInput (
	/* type */
		'text',
	/* attributes */
		array(
			'id'		=> 'apiid',
			'default'	=> 'ABC123',
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
	'Clickatell Password',
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

<?php
echo ntsForm::wrapInput(
	'Sent From',
	$this->buildInput (
	/* type */
		'text',
	/* attributes */
		array(
			'id'		=> 'from',
			'default'	=> '',
			'attr'		=> array(
				'size'	=> 32,
				),
			'help'		=> 'Fill this if you configured two-way number in Clickatell'
			)
		)
	);
?>