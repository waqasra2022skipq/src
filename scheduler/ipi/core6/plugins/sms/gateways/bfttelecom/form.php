<?php
if( ! $new ){
	require( dirname(__FILE__) . '/balance.php');
}
?>
<?php
echo ntsForm::wrapInput(
	'Token',
	$this->buildInput (
	/* type */
		'text',
	/* attributes */
		array(
			'id'		=> 'token',
			'default'	=> 'abc12345678',
			'attr'		=> array(
				'size'	=> 64,
				),
			'required'	=> 1,
			'help'		=> 'Get it in bfttelecom control panel, Configuration, API'
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
