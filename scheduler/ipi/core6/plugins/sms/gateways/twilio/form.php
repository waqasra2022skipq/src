<?php
echo ntsForm::wrapInput(
	'Account SID',
	$this->buildInput (
	/* type */
		'text',
	/* attributes */
		array(
			'id'		=> 'sid',
			'default'	=> '',
			'attr'		=> array(
				'size'	=> 32,
				),
			'help'		=> 'Your Account SID from www.twilio.com/user/account'
			)
		)
	);
?>
<?php
echo ntsForm::wrapInput(
	'Auth Token',
	$this->buildInput (
	/* type */
		'text',
	/* attributes */
		array(
			'id'		=> 'token',
			'default'	=> '',
			'attr'		=> array(
				'size'	=> 32,
				),
			'help'		=> 'Your Auth Token from www.twilio.com/user/account'
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
			'help'		=> 'Twilio number in your account'
			)
		)
	);
?>