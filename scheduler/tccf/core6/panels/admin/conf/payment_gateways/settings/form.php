<?php
$pgm =& ntsPaymentGatewaysManager::getInstance();
$gateway = $this->getValue('gateway');
$new = $this->getValue('new');

$formFile = $pgm->getGatewayFolder( $gateway ) . '/settingsForm.php';
require( $formFile );
?>

<?php if( $new ) : ?>
	<?php echo $this->makePostParams('-current-', 'activate', array('gateway' => $gateway, 'new' => $new) ); ?>
	<?php
	echo ntsForm::wrapInput(
		'',
		'<INPUT class="btn btn-default" TYPE="submit" VALUE="' . M('Activate') . '">'
		);
	?>
<?php else : ?>
	<?php echo $this->makePostParams('-current-', 'update', array('gateway' => $gateway, 'new' => $new) ); ?>
	<?php
	echo ntsForm::wrapInput(
		'',
		'<INPUT class="btn btn-default" TYPE="submit" VALUE="' . M('Update') . '">'
		);
	?>
<?php endif; ?>
