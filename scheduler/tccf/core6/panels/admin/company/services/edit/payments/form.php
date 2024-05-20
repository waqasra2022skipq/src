<?php
$percentOptions = range( 0, 100, 10 );
$prepayOptions = array();
foreach( $percentOptions as $p ){
	$prepayOptions[] = array( $p . '%', $p . '%' );
}
?>
<?php
$attr = array();
$help = '';

$pgm =& ntsPaymentGatewaysManager::getInstance();
$payOnline = $pgm->hasOnline();
if( ! $payOnline ){
	$attr['disabled'] = 'disabled';
	$attr['readonly'] = 'readonly';
	$help = '<a href="' .  ntsLink::makeLink('admin/conf/payment_gateways') . '">' . M('Add online payment options to enable this') . '</a>';
}
echo ntsForm::wrapInput(
	M('Require Deposit'),
	$this->buildInput(
	/* type */
		'select',
	/* attributes */
		array(
			'id'		=> 'prepay',
			'options'	=> $prepayOptions,
			'attr'		=> $attr,
			'help'		=> $help,
			)
		)
	);
?>

<?php
echo ntsForm::wrapInput(
	M('Available In Package Only'),
	$this->buildInput(
	/* type */
		'checkbox',
	/* attributes */
		array(
			'id'	=> 'package_only',
			)
		)
	);
?>

<?php if( ! $this->readonly ) : ?>
	<?php echo $this->makePostParams('-current-', 'update'); ?>
	<?php
	echo ntsForm::wrapInput(
		'',
		'<INPUT class="btn btn-default" TYPE="submit" VALUE="' . M('Update') . '">'
		);
	?>
<?php endif; ?>