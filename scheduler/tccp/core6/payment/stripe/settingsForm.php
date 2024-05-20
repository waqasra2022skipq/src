<?php
echo ntsForm::wrapInput(
	'Secret Key',
	$this->buildInput (
	/* type */
		'text',
	/* attributes */
		array(
			'id'		=> 'skey',
			'default'	=> 'sk_test_BQokikJOvBiI2HlWgH4olfQ2',
			'attr'		=> array(
				'size'	=> 42,
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
	'Publishable Key',
	$this->buildInput (
	/* type */
		'text',
	/* attributes */
		array(
			'id'		=> 'pkey',
			'default'	=> 'pk_test_6pRNASCoBOKtIshFeQd4XMUh',
			'attr'		=> array(
				'size'	=> 42,
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
			'default'	=> 'Pay online with card',
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