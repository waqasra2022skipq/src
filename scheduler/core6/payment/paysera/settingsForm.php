<?php
echo ntsForm::wrapInput(
	M('Project Id'),
	$this->buildInput (
	/* type */
		'text',
	/* attributes */
		array(
			'id'		=> 'projectid',
			'default'	=> '1',
			'attr'		=> array(
				'size'	=> 12,
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

<p>
<i>
Unique project number. Only activated projects can accept payments. 
</i>
</p>

<?php
echo ntsForm::wrapInput(
	M('Sign Password'),
	$this->buildInput (
	/* type */
		'text',
	/* attributes */
		array(
			'id'		=> 'sign_password',
			'default'	=> 'd41d8cd98f00b204e9800998ecf8427e',
			'attr'		=> array(
				'size'	=> 48,
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

<p>
<i>
Project password, which can be found by logging in to Paysera system using your user data, selecting “Service management” and “General settings” by a specific project.
</i>
</p>

<?php
echo ntsForm::wrapInput(
	M('Label'),
	$this->buildInput (
	/* type */
		'text',
	/* attributes */
		array(
			'id'		=> 'label',
			'default'	=> 'Pay online with Paysera',
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
	M('Test Mode'),
	$this->buildInput (
	/* type */
		'checkbox',
	/* attributes */
		array(
			'id'		=> 'test',
			)
		)
	);
?>