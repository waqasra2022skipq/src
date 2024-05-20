<?php
$class = 'user';
$om =& objectMapper::getInstance();
$fields = $om->getFields( $class, 'internal' );
reset( $fields );
?>

<?php foreach( $fields as $f ) : ?>
	<?php $c = $om->getControl( $class, $f[0], false ); ?>
	<?php
	echo ntsForm::wrapInput(
		$c[0],
		$this->buildInput (
			$c[1],
			$c[2],
			$c[3]
			)
		);
	?>
<?php endforeach; ?>

<?php
$timezoneOptions = ntsTime::getTimezones();
echo ntsForm::wrapInput(
	M('Timezone'),
	$this->buildInput (
	/* type */
		'select',
	/* attributes */
		array(
			'id'		=> '_timezone',
			'options'	=> $timezoneOptions,
			'default'	=> NTS_COMPANY_TIMEZONE,
			)
		)
	);
?>

<p>
<?php echo M('Leave these blank to autogenerate a random password'); ?>
</p>

<?php
echo ntsForm::wrapInput(
	M('Password'),
	$this->buildInput (
	/* type */
		'password',
	/* attributes */
		array(
			'id'		=> 'password',
			'attr'		=> array(
				'size'	=> 16,
				),
			'default'	=> '',
			'required'	=> 1,
			),
	/* validators */
		array(
			)
		)
	);
?>

<?php
echo ntsForm::wrapInput(
	M('Confirm Password'),
	$this->buildInput (
	/* type */
		'password',
	/* attributes */
		array(
			'id'		=> 'password2',
			'attr'		=> array(
				'size'	=> 16,
				),
			'default'	=> '',
			'required'	=> 1,
			),
	/* validators */
		array(
			array(
				'code'		=> 'confirmPassword.php', 
				'error'		=> "Passwords don't match!",
				'params'	=> array(
					'mainPasswordField' => 'password',
					),
				),
			)
		)
	);
?>

<?php echo $this->makePostParams('-current-', 'create' ); ?>

<?php
echo ntsForm::wrapInput(
	'',
	'<INPUT TYPE="submit" class="btn btn-default" VALUE="' . M('Create') . '">'
	);
?>
