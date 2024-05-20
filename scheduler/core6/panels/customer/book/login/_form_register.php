<?php
$conf =& ntsConf::getInstance();
$useCaptcha = $conf->get( 'useCaptcha' );
$strongPassword = $conf->get( 'strongPassword' );
$enableRegistration = $conf->get('enableRegistration');

$session = new ntsSession;
$apps = $session->userdata( 'apps' );

$service_ids = $this->getValue('service_ids');

$om =& objectMapper::getInstance();
$fields = $om->getFields( 'customer', 'external' );
reset( $fields );

$forms = array();
foreach( $service_ids as $service_id ){
	$form_id = $om->isFormForService( $service_id );
	if( ! isset($forms[$form_id]) ){
		$forms[$form_id] = array();
	}
	$forms[$form_id][] = $service_id;
}

$more_fields = array();
if( $forms ){
	$class = 'appointment';
	foreach( $forms as $form_id => $form_services ){
		$otherDetails = array(
			'service_id' => $form_services[0],
			);
		$this_form_fields = $om->getFields( $class, 'external', $otherDetails );

		foreach( $this_form_fields as $f ){
			if( isset($f[4]) && ($f[4] == 'read') ){
				// check if there's a default value
				if( strlen($f[3]) == 0 ){
					continue;
				}
			}
			if( ! isset($more_fields[$form_id]) ){
				$more_fields[$form_id] = array();
			}
			$more_fields[$form_id][] = $f;
		}
	}
}
?>

<div class="page-header">
	<h3><?php echo M('Customer'); ?></h3>
</div>

<?php foreach( $fields as $f ) : ?>
	<?php
	if( $f[0] == 'username' )
		continue;
	?>
	<?php $c = $om->getControl( 'customer', $f[0], false ); ?>
	<?php
	if( isset($f[4]) )
	{
		if( $f[4] == 'read' )
		{
			$c[2]['readonly'] = 1;
		}
	}

	if( ! $enableRegistration )
	{
		if( $f[0] == 'email' )
		{
			/* traverse validators */
			reset( $c[3] );
			$copyVali = $c[3];
			$c[3] = array();
			foreach( $copyVali as $vali )
			{
				if( preg_match('/checkUserEmail\.php$/', $vali['code']) )
				{
					continue;
				}
				$c[3][] = $vali;
			}
		}
	}

	if( $c[2]['description'] )
		$c[2]['help'] = $c[2]['description'];

	if( NTS_ALLOW_NO_EMAIL && ($c[2]['id'] == 'email') )
	{
		$c[2]['after']	= '';
		$c[2]['after']	.= '<div class="checkbox">';
		$c[2]['after']		.= '<label>';
		$c[2]['after']		.= $this->makeInput (
								/* type */
									'checkbox',
								/* attributes */
									array(
										'id'	=> 'noEmail',
										)
									);
		$c[2]['after']		.= ' ' . M('No Email');
		$c[2]['after']		.= '</label>';
		$c[2]['after']	.= '</div>';
	}

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

<?php foreach( $more_fields as $form_id => $form_fields ) : ?>
	<?php
	$form = ntsObjectFactory::get('form');
	$form->setId( $form_id );
	$form_title = $form->getProp('title');
	?>
	<div class="page-header">
		<h3><?php echo $form_title; ?></h3>
	</div>

	<?php foreach( $form_fields as $f ) : ?>
		<?php
		$c = $om->getControl( $class, $f[0], false );
		if( isset($f[4]) ){
			if( $f[4] == 'read' ){
				$c[1] = 'label';
			}
		}
		?>
		<?php
		if( $c[2]['description'] )
			$c[2]['help'] = $c[2]['description'];
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
<?php endforeach; ?>

<?php if( $enableRegistration ) : ?>
	<div class="page-header">
		<h3><?php echo M('Login Details'); ?></h3>
	</div>

	<?php if( ! NTS_EMAIL_AS_USERNAME ) : ?>
		<?php
		$control = $om->getControl( 'customer', 'username', false );
		if( isset($control[3]) && is_array($control[3]) )
		{
			$validators = $control[3];
		}
		else
		{
			$validators = array(
				array(
					'code'		=> 'notEmpty.php', 
					'error'		=> M('Required'),
					),
				array(
					'code'		=> 'checkUsername.php', 
					'error'		=> M('Already in use'),
					'params'	=> array(
						'skipMe'	=> 1,
						)
					),
				);
		}

		echo ntsForm::wrapInput(
			M('Desired Username'),
			$this->buildInput (
			/* type */
				'text',
			/* attributes */
				array(
					'id'		=> 'username',
					'attr'		=> array(
						'size'	=> 16,
						),
					'default'	=> '',
					'required'	=> 1,
					),
			/* validators */
				$validators
				)
			);
		?>
	<?php endif; ?>

	<?php
	$passwordValidate = array();
	$passwordValidate[] = array(
		'code'		=> 'notEmpty.php', 
		'error'		=> M('Required'),
		);
	if( $strongPassword ){
		$passwordValidate[] = array(
			'code'		=> 'strongPassword.php', 
			);
		}
	echo ntsForm::wrapInput(
		M('Password'),
		$this->buildInput(
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
			$passwordValidate
			)
		);
	?>

	<?php
	echo ntsForm::wrapInput(
		M('Confirm Password'),
		$this->buildInput(
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
					'error'		=> M("Passwords don't match!"),
					'params'	=> array(
						'mainPasswordField' => 'password',
						),
					),
				)
			)
		);
	?>
<?php endif; ?>

<?php if( $useCaptcha ) : ?>
	<?php
	echo ntsForm::wrapInput(
		M('Enter Code Shown'),
		$this->buildInput (
		/* type */
			'captcha',
		/* attributes */
			array(
				'id'	=> 'captcha',
				'attr'	=> array(
					'size'	=> 6
					)
				)
			)
		);
	?>
<?php endif; ?>

<?php echo $this->makePostParams('-current-', 'register' ); ?>

<?php
$btnTitle = M('Confirm');
$btnTitle = (count($apps) > 1) ? M('Confirm Appointments') : M('Confirm Appointment');
echo ntsForm::wrapInput(
	'',
	'<INPUT NAME="nts-register" class="btn btn-default" TYPE="submit" VALUE="' . $btnTitle . '">'
	);
?>

<?php if( NTS_ALLOW_NO_EMAIL ) : ?>
<script language="JavaScript">
jQuery(document).ready( function()
{
	if( jQuery("#<?php echo $this->getName(); ?>noEmail").is(":checked") )
	{
		jQuery("#<?php echo $this->getName(); ?>email").hide();
	}
	else
	{
		jQuery("#<?php echo $this->getName(); ?>email").show();
	}
});
jQuery("#<?php echo $this->getName(); ?>noEmail").live( 'click', function()
{
	jQuery("#<?php echo $this->getName(); ?>email").toggle();
});
</script>
<?php endif; ?>