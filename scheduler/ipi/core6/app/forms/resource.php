<?php
$id = $this->getValue('id');
$object = $this->getValue('object');
?>
<?php if( $id ) : ?>
	<?php
	$is_archive = $object->getProp('archive');
	$is_internal = $object->getProp('_internal');

	$status_view = '<span class="label label-success">' . M('Active') . '</span>';
	if( $is_archive )
	{
		$status_view = '<span class="label label-archive">' . M('Archived') . '</span>';
	}
	elseif( 0 && $is_internal )
	{
		$status_view = '<span class="label label-warning">' . M('Internal') . '</span>';
	}

	echo ntsForm::wrapInput(
		M('Status'),
		$status_view
		);
	?>
<?php endif; ?>
<?php
echo ntsForm::wrapInput(
	M('Title') . ' *',
	$this->buildInput (
	/* type */
		'text',
	/* attributes */
		array(
			'id'		=> 'title',
			'attr'		=> array(
				'size'	=> 20,
				),
			'default'	=> '',
			'required'	=> 1,
			),
	/* validators */
		array(
			array(
				'code'		=> 'notEmpty.php', 
				'error'		=> M('Required'),
				),
			array(
				'code'		=> 'checkUniqueProperty.php', 
				'error'		=> M('Already in use'),
				'params'	=> array(
					'prop'	=> 'title',
					'class'	=> 'resource',
					'skipMe'	=> 1
					),
				),
			)
		)
	);
?>
<?php
echo ntsForm::wrapInput(
	M('Description'),
	$this->buildInput (
	/* type */
		'textarea',
	/* attributes */
		array(
			'id'		=> 'description',
			'attr'		=> array(
				'cols'	=> 20,
				'rows'	=> 6,
				),
			'default'	=> '',
			),
	/* validators */
		array(
			)
		)
	);
?>
<?php
echo ntsForm::wrapInput(
	M('Internal'),
	$this->buildInput (
	/* type */
		'checkbox',
	/* attributes */
		array(
			'id'		=> '_internal',
			'default'	=> 0,
			'help'		=> M('Set this if not available for booking by customers'),
			),
	/* validators */
		array(
			)
		)
	);
?>
<?php
$pgm =& ntsPaymentGatewaysManager::getInstance();
$paymentGateways = $pgm->getActiveGateways();
$paypalEnabled = in_array('paypal', $paymentGateways) ? true : false;
?>
<?php if( $paypalEnabled ) : ?>
<?php
echo ntsForm::wrapInput(
	M('Paypal Email'),
	$this->buildInput (
	/* type */
		'text',
	/* attributes */
		array(
			'id'		=> '_paypal',
			'attr'		=> array(
				'size'	=> 20,
				),
			'default'	=> '',
			'required'	=> 0,
			'help'		=> "Set this if you wish to provide a separate Paypal account for this resource. Otherwise the global account will be used.",
			),
	/* validators */
		array(
			)
		)
	);
?>
<?php endif; ?>

<?php echo $this->makePostParams('-current-', 'save'); ?>
<?php
$btn_label = $id ? M('Save') : M('Add');

$buttons = array();
$buttons[] = '<ul class="list-inline">';
$buttons[] = '<li>';
$buttons[] = '<INPUT class="btn btn-success" TYPE="submit" value="' . $btn_label . '">';
$buttons[] = '</li>';
if( $id )
{
	$buttons[] = '<li class="divider"></li>';
	$buttons[] = '<li>';
	$archive_link = ntsLink::makeLink('-current-', 'archive');
	$buttons[] = '<a href="' . $archive_link . '" class="btn btn-sm btn-archive" TYPE="submit" title="' . M('Archive') . '">';

	if( $is_archive )
	{
		$buttons[] = M('Activate');
	}
	else
	{
		$buttons[] = M('Archive');
	}

	$buttons[] = '</a>';
	$buttons[] = '</li>';
}

$buttons[] = '</ul>';
?>
<?php 
echo ntsForm::wrapInput(
	'',
	$buttons
	);
?>
