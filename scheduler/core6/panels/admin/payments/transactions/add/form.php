<?php
$taxRate = $this->getValue('tax_rate');
$typeOptions = array(
	array( 'cash', M('Cash') ),
	array( 'check', M('Check') ),
	array( 'credit card', M('Credit Card') ),
	);
?>
<?php
$help = '';
if( $taxRate )
{
	$ntsConf =& ntsConf::getInstance();
	$taxTitle = $ntsConf->get('taxTitle');
	$help = M('Including') . ': ' . $taxTitle . ' ' . $taxRate . '%';
}

echo ntsForm::wrapInput(
	M('Amount'),
	$this->buildInput (
	/* type */
		'text',
	/* attributes */
		array(
			'id'		=> 'amount',
			'attr'		=> array(
				'size'	=> 6,
				),
			'help'	=> $help
			),
	/* validators */
		array(
			array(
				'code'		=> 'notEmpty.php', 
				'error'		=> M('Required'),
				),
			array(
				'code'		=> 'number.php', 
				'error'		=> M('Numbers only'),
				),
			)
		)
	);
?>

<?php
echo ntsForm::wrapInput(
	M('Type'),
	$this->buildInput (
	/* type */
		'select',
	/* attributes */
		array(
			'id'		=> 'type',
			'options'	=> $typeOptions,
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

<?php
echo ntsForm::wrapInput(
	M('Notes'),
	$this->buildInput (
	/* type */
		'textarea',
	/* attributes */
		array(
			'id'		=> 'notes',
			'attr'		=> array(
				'cols'	=> 24,
				'rows'	=> 2,
				),
			),
	/* validators */
		array(
			)
		)
	);
?>

<?php 
echo $this->makePostParams(
	'-current-',
	'add', 
	array(
		'invoice' => $this->getValue('invoice')
		)
	);
?>
<?php if( ! (isset($skip_button) && ($skip_button)) ) : ?>
<?php
echo ntsForm::wrapInput(
	'',
	'<INPUT class="btn btn-default" TYPE="submit" VALUE="' . M('Add') . '">'
	);
?>
<?php endif; ?>