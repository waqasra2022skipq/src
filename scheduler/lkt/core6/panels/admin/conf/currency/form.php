<?php
$pgm =& ntsPaymentGatewaysManager::getInstance();
$onlinePaymentAllowed = $pgm->hasOnline();

$allCurrOptions = $pgm->getAllCurrencies();
$allowedCurrencies = $pgm->getActiveCurrencies();
if( $allowedCurrencies )
{
	$currOptions = array();
	reset( $allCurrOptions );
	foreach( $allCurrOptions as $co )
	{
		if( in_array($co[0], $allowedCurrencies) )
			$currOptions[] = $co;
	}
}
else
{
	$currOptions = $allCurrOptions;
}

$formats = array(
	'.||,',
	'.|| ',
	',|| ',
	'.||',
	',||',
	',||.',
	);

$demoPrice = 54321;
reset( $formats );
$formatOptions = array();
foreach( $formats as $f )
{
	list( $decPoint, $thousandSep ) = explode( '||', $f );
	$formatOptions[] = array( $f, number_format($demoPrice, 2, $decPoint, $thousandSep) );
}
?>
<?php
echo ntsForm::wrapInput(
	M('Currency'),
	$this->buildInput(
	/* type */
		'select',
	/* attributes */
		array(
			'id'		=> 'currency',
			'options'	=> $currOptions,
			)
		)
	);
?>

<?php
echo ntsForm::wrapInput(
	M('Price Format'),
	array(
		'<ul class="list-inline list-separated">',
			'<li>',
				$this->buildInput(
				/* type */
					'text',
				/* attributes */
					array(
						'id'		=> 'sign-before',
						'attr'		=> array(
							'size'	=> 3,
							'style'	=> 'text-align: right;'
							),
						)
					),
			'</li>',
			'<li>',
				$this->buildInput(
				/* type */
					'select',
				/* attributes */
					array(
						'id'		=> 'format',
						'options'	=> $formatOptions,
						)
					),
			'</li>',
			'<li>',
				$this->buildInput(
				/* type */
					'text',
				/* attributes */
					array(
						'id'		=> 'sign-after',
						'attr'		=> array(
							'size'	=> 3,
							),
						)
					),
			'</li>',
			'<li>',
				'<a href="' . ntsLink::makeLink('-current-', 'reset') . '">' . M('Reset To Defaults') . '</a>',
			'</li>',
		'</ul>',
		)
	);
?>

<?php
echo ntsForm::wrapInput(
	M('Tax Title'),
	$this->buildInput(
	/* type */
		'text',
	/* attributes */
		array(
			'id'		=> 'taxTitle',
			'attr'		=> array(
				'size'	=> 20,
				),
			)
		)
	);
?>

<?php
echo ntsForm::wrapInput(
	M('Tax Rate'),
	$this->buildInput(
	/* type */
		'text',
	/* attributes */
		array(
			'id'		=> 'taxRate',
			'attr'		=> array(
				'size'	=> 3,
				),
			'after'		=> '%'
			),
	/* validators */
		array(
			array(
				'code'		=> 'number', 
				'error'		=> M('Numbers only'),
				),
			)
		)
	);
?>


<?php
echo ntsForm::wrapInput(
	M('Invoice Header'),
	$this->buildInput(
	/* type */
		'textarea',
	/* attributes */
		array(
			'id'	=> 'invoiceHeader',
			'attr'	=> array(
				'cols'	=> 48,
				'rows'	=> 5,
				),
			)
		)
	);
?>

<?php
echo ntsForm::wrapInput(
	M('Invoice Footer'),
	$this->buildInput(
	/* type */
		'textarea',
	/* attributes */
		array(
			'id'	=> 'invoiceFooter',
			'attr'	=> array(
				'cols'	=> 48,
				'rows'	=> 5,
				),
			)
		)
	);
?>

<?php
echo ntsForm::wrapInput(
	M('Invoice Ref Numbers'),
	array(
		$this->buildInput(
		/* type */
			'select',
		/* attributes */
			array(
				'id'		=> 'invoiceRef',
				'default'	=> 'random',
				'options'	=> array(
					array('random', M('Random') ),
					array('seq', M('Sequential') ),
					)
				)
			)
		)
	);
?>

<?php
echo ntsForm::wrapInput(
	M('If invoice ref numbers are sequential, then start with'),
	array(
		$this->buildInput(
		/* type */
			'text',
		/* attributes */
			array(
				'id'		=> 'invoiceRefStartWith',
				'default'	=> 1,
				)
			)
		)
	);
?>


<?php echo $this->makePostParams('-current-', 'update'); ?>
<?php
echo ntsForm::wrapInput(
	'',
	'<input class="btn btn-default" type="submit" value="' . M('Save') . '">'
	);
?>