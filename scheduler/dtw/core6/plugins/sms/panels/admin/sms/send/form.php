<?php
$plm =& ntsPluginManager::getInstance();
$plugin = 'sms';
$sms_settings = $plm->getPluginSettings( $plugin );

$carrier_options = array();
if( isset($sms_settings['carriers']) && ($sms_settings['gateway'] == 'email2sms') )
{
	reset( $sms_settings['carriers'] );
	foreach( $sms_settings['carriers'] as $carrier )
	{
		$carrier_options[] = array( $carrier, $carrier );
	}
}

if( $carrier_options ) 
{
	array_unshift( $carrier_options, array('', ' - ' . M('Select') . ' - ') );
}
?>

<?php
echo ntsForm::wrapInput(
	'Mobile Phone',
	$this->buildInput (
	/* type */
		'text',
	/* attributes */
		array(
			'id'		=> 'to',
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

<?php if( $carrier_options ) : ?>
	<?php
	echo ntsForm::wrapInput(
		'Mobile Carrier',
		$this->buildInput (
		/* type */
			'select',
		/* attributes */
			array(
				'id'		=> 'carrier',
				'required'	=> 1,
				'options'	=> $carrier_options
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
<?php endif ?>

<?php
echo ntsForm::wrapInput(
	'Message',
	$this->buildInput (
	/* type */
		'textarea',
	/* attributes */
		array(
			'id'		=> 'message',
			'default'	=> '',
			'attr'		=> array(
				'cols'	=> 32,
				'rows'	=> 4,
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

<?php echo $this->makePostParams('-current-', 'send' ); ?>
<?php
echo ntsForm::wrapInput(
	'',
	'<INPUT TYPE="submit" class="btn btn-default" VALUE="' . M('Send') . '">'
	);
?>