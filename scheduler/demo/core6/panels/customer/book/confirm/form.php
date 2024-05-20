<?php
$session = new ntsSession;
$apps = $session->userdata( 'apps' );

$om =& objectMapper::getInstance();
$service_ids = $this->getValue('service_ids');

$forms = array();
foreach( $service_ids as $service_id ){
	$form_id = $om->isFormForService( $service_id );
	if( ! isset($forms[$form_id]) ){
		$forms[$form_id] = array();
	}
	$forms[$form_id][] = $service_id;
}

$fields = array();

if( $forms ){
	$class = 'appointment';
	foreach( $forms as $form_id => $form_services ){
		$otherDetails = array(
			'service_id' => $form_services[0],
			);
		$this_form_fields = $om->getFields( $class, 'external', $otherDetails );

		$fields[$form_id] = array();
		foreach( $this_form_fields as $f ){
			if( isset($f[4]) && ($f[4] == 'read') ){
				// check if there's a default value
				if( strlen($f[3]) == 0 ){
					continue;
				}
			}
			$fields[$form_id][] = $f;
		}
	}
}
?>

<?php foreach( $fields as $form_id => $form_fields ) : ?>
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

<?php echo $this->makePostParams('-current-', 'submit' ); ?>
<?php
// $btn_label = (count($apps) > 1) ? M('Confirm Appointments') : M('Confirm Appointment');
$btn_label = (count($apps) > 1) ? M('Proceed') : M('Proceed');
$btn = '<INPUT class="btn btn-default btn-lg" TYPE="submit" VALUE="' . $btn_label . '">'
?>

<hr>
<p>
<?php if( $fields ) : ?>
	<?php
	echo ntsForm::wrapInput(
		'',
		$btn
		);
	?>
<?php else : ?>
	<?php echo $btn; ?>
<?php endif; ?>