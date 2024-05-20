<?php
$id = $this->getValue('id');
/* form params - used later for validation */
$this->setParams(
	array(
		'myId'	=> $id,
		)
	);
?>
<?php
$class = 'provider';
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

<?php
$admin_levels = array(
	array( 'admin',	M('Administrator') ),
	array( 'staff',	M('Staff') ),
	);

$this_readonly = ( $id == ntsLib::getCurrentUserId() ) ? TRUE : FALSE;
echo ntsForm::wrapInput(
	M('Access Level'),
	$this->buildInput (
	/* type */
		'select',
	/* attributes */
		array(
			'id'		=> '_admin_level',
			'options'	=> $admin_levels,
			'default'	=> 'admin',
			'help'		=> M('Staff do not have access to company configuration, payments, and system settings'),
			'readonly'	=> $this_readonly,
			)
		)
	);
?>

<?php echo $this->makePostParams('-current-', 'update'); ?>
<?php
echo ntsForm::wrapInput(
	'',
	'<INPUT class="btn btn-default" TYPE="submit" VALUE="' . M('Update') . '">'
	);
?>