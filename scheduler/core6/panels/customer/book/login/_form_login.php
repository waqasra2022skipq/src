<?php
$conf =& ntsConf::getInstance();

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

<?php if( $more_fields ) : ?>
	<div class="page-header">
		<h3><?php echo M('Login'); ?></h3>
	</div>
<?php endif; ?>

<?php if( ! NTS_EMAIL_AS_USERNAME ) : ?>
	<?php
	echo ntsForm::wrapInput(
		M('Username'),
		$this->buildInput (
		/* type */
			'text',
		/* attributes */
			array(
				'id'		=> 'login_username',
				'attr'		=> array(
					'size'	=> 20,
					),
				)
			)
		);
	?>

<?php else : ?>

	<?php
	echo ntsForm::wrapInput(
		M('Email'),
		$this->buildInput (
		/* type */
			'text',
		/* attributes */
			array(
				'id'		=> 'login_email',
				'attr'		=> array(
					'size'	=> 20,
					),
				)
			)
		);
	?>

<?php endif; ?>

<?php
echo ntsForm::wrapInput(
	M('Password'),
	$this->buildInput (
	/* type */
		'password',
	/* attributes */
		array(
			'id'		=> 'login_password',
			'attr'		=> array(
				'size'	=> 20,
				),
			)
		)
	);
?>

<?php
echo ntsForm::wrapInput(
	M('Remember Me'),
	$this->buildInput (
	/* type */
		'checkbox',
	/* attributes */
		array(
			'id'	=> 'remember',
			)
		)
	);
?>

<?php echo $this->makePostParams('-current-', 'login' ); ?>
<?php
echo ntsForm::wrapInput(
	'',
	'<INPUT NAME="nts-login" class="btn btn-default" TYPE="submit" VALUE="' . M('Login') . '">'
	);
?>

<input type="hidden" name="nts-skip-cookie" value="1">
