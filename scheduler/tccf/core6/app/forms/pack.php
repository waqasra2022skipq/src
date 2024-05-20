<?php
$serviceType = $this->getValue('service_type');
$dateType = $this->getValue('date_type');
$packType = $this->getValue('pack_type');
$orderId = $this->getValue('order_id');

$minStart = NTS_TIME_STARTS;
$maxEnd = NTS_TIME_ENDS;
$t = new ntsTime;
$t->setNow();
$today = $t->formatDate_Db();

$serviceOptions = array();
$ntsdb =& dbWrapper::getInstance();
$allServices = ntsObjectFactory::getAll( 'service', 'price > 0' );
reset( $allServices );
foreach( $allServices as $s ){
	$servicePrice = $s->getProp('price');
	if( strlen($servicePrice) && ($servicePrice > 0) ){
//		$serviceView = $s->getProp('title');
//		$serviceView .= ' [' . ntsTime::formatPeriod($s->getProp('duration')) . ']';
//		$serviceView .= ' - ' . ntsCurrency::formatPrice($s->getProp('price')) . '';
		$serviceView = ntsView::objectTitle( $s );
		$serviceOptions[] = array( $s->getId(), $serviceView );
		}
	}
array_unshift( $serviceOptions, array(0, ' - ' . M('Any') . ' - ') );
array_unshift( $serviceOptions, array(-1, ' - ' . M('Select') . ' - ') );

$resourceOptions = array();
$ntsdb =& dbWrapper::getInstance();
$allResources = ntsObjectFactory::getAll( 'resource' );
reset( $allResources );
foreach( $allResources as $r ){
	$resourceView = ntsView::objectTitle( $r );
	$resourceOptions[] = array( $r->getId(), $resourceView );
	}
array_unshift( $resourceOptions, array(0, ' - ' . M('Any') . ' - ') );
?>

<?php if( ! $orderId ) : ?>
	<?php 
	echo ntsForm::wrapInput(
		M('Title'),
		$this->buildInput (
		/* type */
			'text',
		/* attributes */
			array(
				'id'		=> 'title',
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
				array(
					'code'		=> 'checkUniqueProperty.php', 
					'error'		=> M('Already in use'),
					'params'	=> array(
						'prop'	=> 'title',
						'class'	=> 'pack',
						'skipMe'	=> 1
						),
					),
				)
			)
		);
	?>
<?php endif; ?>

<?php
echo ntsForm::wrapInput(
	M('Services'),
	$this->buildInput (
	/* type */
		'radioSet',
	/* attributes */
		array(
			'id'		=> 'service_type',
			'options'	=> array(
				array( 'one',	M('Any From List') ),
				array( 'fixed',	M('Fixed') ),
				),
			)
		)
	);
?>

<div id="<?php echo $this->formId; ?>_fixed_services">
	<?php
	echo ntsForm::wrapInput(
		'&nbsp;',
		$this->buildInput (
		/* type */
			'fixedServices',
		/* attributes */
			array(
				'id'		=> 'fixed_service_id',
				'options'	=> $serviceOptions
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
</div>

<div id="<?php echo $this->formId; ?>_service">
	<?php
	$oneServiceOptions = $serviceOptions;
	// remove Select
	array_shift( $oneServiceOptions );
	array_shift( $oneServiceOptions );
	echo ntsForm::wrapInput(
		'&nbsp;',
		array(
			$this->buildInput (
			/* type */
				'checkbox',
			/* attributes */
				array(
					'id'		=> 'service_id_all',
					'box_value'	=> 1,
					'htmlId'	=> 'nts-toggle-all-services',
					'label'		=> ' - ' . M('Any') . ' - '
					)
				),
			$this->buildInput (
			/* type */
				'checkboxSet',
			/* attributes */
				array(
					'id'		=> 'service_id',
					'options'	=> $oneServiceOptions,
					),
				/* validators */
				array(
					array(
						'code'		=> 'notEmpty.php', 
						'error'		=> M('Please Select'),
						),
					)
				)
			)
		);
	?>

	<?php 
	echo ntsForm::wrapInput(
		M('Value Type'),
		$this->buildInput (
		/* type */
			'radioSet',
		/* attributes */
			array(
				'id'		=> 'pack_type',
				'options'	=> array(
					array( 'qty',		M('Number of appointments') ),
					array( 'duration',	M('Duration') ),
					array( 'amount',	M('Amount') ),
					array( 'unlimited',	M('Unlimited') ),
					),
				)
			)
		);
	?>
</div>

<div id="<?php echo $this->formId; ?>_details_qty">
	<?php 
	echo ntsForm::wrapInput(
		M('Number of appointments'),
		$this->buildInput (
		/* type */
			'text',
		/* attributes */
			array(
				'id'		=> 'qty',
				'attr'		=> array(
					'size'	=> 4,
					),
				),
		/* validators */
			array(
				array(
					'code'		=> 'notEmpty.php', 
					'error'		=> M('Required'),
					),
				array(
					'code'		=> 'integer.php', 
					'error'		=> M('Numbers only'),
					),
				)
			)
		);
	?>
</div>

<div id="<?php echo $this->formId; ?>_details_duration">
	<?php
	echo ntsForm::wrapInput(
		M('Duration'),
		$this->buildInput (
		/* type */
			'period/MinHour',
		/* attributes */
			array(
				'id'		=> 'duration',
				'default'	=> 2 * 60 * 60,
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
</div>

<div id="<?php echo $this->formId; ?>_details_amount">
	<?php 
	echo ntsForm::wrapInput(
		M('Total Amount'),
		$this->buildInput (
		/* type */
			'text',
		/* attributes */
			array(
				'id'		=> 'amount',
				'attr'		=> array(
					'size'	=> 8,
					),
				'required'	=> 1,
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
				array(
					'code'		=> 'greaterThan.php', 
					'error'		=> M('Required'),
					'params'	=> array(
						'compareWith'	=> 0,
						)
					),
				)
			)
		);
	?>
</div>

<?php if( ! $orderId ) : ?>
	<?php 
	$default = $this->getValue('price') ? 0 : 1;

	echo ntsForm::wrapInput(
		M('Selling Price'),
		array(
			'<div id="' . $this->getName() . 'price-wrapper">',
			$this->buildInput (
			/* type */
				'text',
			/* attributes */
				array(
					'id'		=> 'price',
					'attr'		=> array(
						'size'	=> 8,
						),
					'required'	=> 1,
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
					array(
						'code'		=> 'greaterThan.php', 
						'error'		=> M('Required'),
						'params'	=> array(
							'compareWith'	=> 0,
							)
						),
					)
				),
			'</div>',
			$this->buildInput (
			/* type */
				'checkbox',
			/* attributes */
				array(
					'id'		=> 'notForSale',
					'default'	=> $default,
					'label'		=> M('Not For Sale')
					)
				)
			)
		);
	?>
<?php endif; ?>

<?php
echo ntsForm::wrapInput(
	M('Bookable Resource'),
	$this->buildInput (
	/* type */
		'select',
	/* attributes */
		array(
			'id'		=> 'resource_id',
			'options'	=> $resourceOptions
			)
		)
	);
?>

<?php 
$default = $this->getValue('expires_in') ? 0 : 1;

echo ntsForm::wrapInput(
	M('Expires In'),
	array(
		'<div id="' . $this->getName() . 'expires-wrapper">',
		$this->buildInput (
		/* type */
			'period/DayWeekMonthYear',
		/* attributes */
			array(
				'id'		=> 'expires_in',
				),
		/* validators */
			array(
				array(
					'code'	=> 'notEmpty.php', 
					'error'	=> M('Required'),
					),
				)
			),
		'</div>',
		$this->buildInput (
		/* type */
			'checkbox',
		/* attributes */
			array(
				'id'		=> 'neverExpires',
				'default'	=> $default,
				'label'		=> M('Never Expires')
				)
			)
		)
	);
?>

<?php
echo ntsForm::wrapInput(
	M('Weekdays'),
	$this->buildInput (
	/* type */
		'date/Weekday',
	/* attributes */
		array(
			'id'			=> 'weekday',
			'includeAll'	=> TRUE,
			'allValue'		=> -1,
			'default'		=> array(-1),
			)
		)
	);
?>

<?php
echo ntsForm::wrapInput(
	M('Time'),
	array(
		$this->buildInput (
		/* type */
			'checkbox',
		/* attributes */
			array(
				'id'		=> 'time_all',
				'default'	=> 1,
				'label'		=> ' - ' . M('All') . ' - ',
				)
			),
		'<div id="' . $this->formId . 'time_container">',
		$this->buildInput (
		/* type */
			'date/Time',
		/* attributes */
			array(
				'id'		=> 'from_time',
				'conf'	=> array(
					'min'	=> $minStart,
					'max'	=> $maxEnd,
					),
				'default'	=> $minStart
				),
		/* validators */
			array(
				array(
					'code'		=> 'notEmpty.php', 
					'error'		=> M('Required'),
					),
				)
			),
		' - ',
		$this->buildInput (
		/* type */
			'date/Time',
		/* attributes */
			array(
				'id'		=> 'to_time',
				'conf'	=> array(
					'min'	=> $minStart,
					'max'	=> $maxEnd,
					),
				'default'	=> $maxEnd
				),
		/* validators */
			array(
				array(
					'code'		=> 'notEmpty.php', 
					'error'		=> M('Required'),
					),
				array(
					'code'		=> 'greaterThan.php', 
					'error'		=> "Slot can't start before end",
					'params'	=> array(
						'compareWithField' => 'from_time',
						),
					)
				)
			),
		'</div>',
		)
	);
?>

<?php
echo ntsForm::wrapInput(
	M('Dates'),
	array(
		$this->buildInput (
		/* type */
			'checkbox',
		/* attributes */
			array(
				'id'		=> 'date_all',
				'default'	=> 1,
				'label'		=> ' - ' . M('All') . ' - '
				)
			),
		'<div id="' . $this->formId . 'date_container">',
			'<div>',
				$this->buildInput (
				/* type */
					'radioSet',
				/* attributes */
					array(
						'id'		=> 'date_type',
						'default'	=> $dateType,
						'options'	=> array(
							array('range', 	M('Date Range') ),
							array('fixed', 	M('Fixed Dates') ),
							),
						)
					),
			'</div>',

			'<div id="' . $this->formId . 'date_range" style="margin: 0.5em 0;">',
				$this->buildInput (
				/* type */
					'date/Calendar',
				/* attributes */
					array(
						'id'		=> 'from_date',
						'default'	=> $today
						),
				/* validators */
					array(
						array(
							'code'		=> 'notEmpty.php', 
							'error'		=> M('Required'),
							),
						)
					),
				' - ',
				$this->buildInput (
				/* type */
					'date/Calendar',
				/* attributes */
					array(
						'id'		=> 'to_date',
						'default'	=> $today
						),
				/* validators */
					array(
						array(
							'code'		=> 'notEmpty.php', 
							'error'		=> M('Required'),
							),
						array(
							'code'		=> 'greaterThan.php', 
							'error'		=> "The end date should be after the start date",
							'params'	=> array(
								'compareWithField' => 'from_date',
								),
							)
						)
					),
			'</div>',

			'<div id="' . $this->formId . 'date_fixed" style="margin: 0.5em 0;">',
				$this->buildInput (
				/* type */
					'fixedDates',
				/* attributes */
					array(
						'id'		=> 'fixed_date',
						),
				/* validators */
					array(
						array(
							'code'		=> 'notEmpty.php', 
							'error'		=> M('Required'),
							),
						)
					),
			'</div>',

		'</div>'
		)
	);
?>

<?php echo $this->makePostParams('-current-', 'save', array('order_id' => $orderId) ); ?>
<?php
echo ntsForm::wrapInput(
	'&nbsp;',
	'<input class="btn btn-default" type="submit" value="' . M('Save') . '">'
	);
?>

<script language="JavaScript">
jQuery(document).ready( function(){
/* time */
	jQuery("#<?php echo $this->formId; ?>time_all").is(":checked") ? jQuery('#<?php echo $this->formId; ?>time_container').hide() : jQuery('#<?php echo $this->formId; ?>time_container').show(); 
	jQuery("#<?php echo $this->formId; ?>date_all").is(":checked") ? jQuery('#<?php echo $this->formId; ?>date_container').hide() : jQuery('#<?php echo $this->formId; ?>date_container').show(); 

	if( jQuery("#<?php echo $this->getName(); ?>neverExpires").is(":checked") ){
		jQuery("#<?php echo $this->getName(); ?>expires-wrapper").hide();
		}
	else {
		jQuery("#<?php echo $this->getName(); ?>expires-wrapper").show();
		}

	if( jQuery("#<?php echo $this->getName(); ?>notForSale").is(":checked") ){
		jQuery("#<?php echo $this->getName(); ?>price-wrapper").hide();
		}
	else {
		jQuery("#<?php echo $this->getName(); ?>price-wrapper").show();
		}

	var date_type = jQuery('#<?php echo $this->formId; ?>date_type:checked').val();
	switch( date_type )
	{
		case 'range':
			jQuery('#<?php echo $this->formId; ?>date_range').show();
			jQuery('#<?php echo $this->formId; ?>date_fixed').hide();
			break;
		case 'fixed':
			jQuery('#<?php echo $this->formId; ?>date_range').hide();
			jQuery('#<?php echo $this->formId; ?>date_fixed').show();
			break;
	}

	jQuery('#<?php echo $this->formId; ?>_service').hide();
	var serviceType = jQuery('#<?php echo $this->formId; ?>service_type:checked').val();
	switch( serviceType ){
		case 'one':
			jQuery('#<?php echo $this->formId; ?>_fixed_services').hide();

			jQuery('#<?php echo $this->formId; ?>_service').show();
			jQuery('#<?php echo $this->formId; ?>_details_qty').hide();
			jQuery('#<?php echo $this->formId; ?>_details_duration').hide();
			jQuery('#<?php echo $this->formId; ?>_details_amount').hide();

			var what2show = jQuery('#<?php echo $this->formId; ?>pack_type:checked').val();
			what2show = '#<?php echo $this->formId; ?>_details_' + what2show;
			jQuery(what2show).show();
			break;
		case 'fixed':
			jQuery('#<?php echo $this->formId; ?>_service').hide();
			jQuery('#<?php echo $this->formId; ?>_details_qty').hide();
			jQuery('#<?php echo $this->formId; ?>_details_duration').hide();
			jQuery('#<?php echo $this->formId; ?>_details_amount').hide();

			jQuery('#<?php echo $this->formId; ?>_fixed_services').show();
			break;
		}

	if( jQuery("#nts-toggle-all-services").is(":checked") ){
		jQuery('#<?php echo $this->formId; ?>service_id_container').hide();
		}
	else {
		jQuery('#<?php echo $this->formId; ?>service_id_container').show();
		}
	});

jQuery('#<?php echo $this->formId; ?>time_all').live("change", function()
{
	this.checked ? jQuery('#<?php echo $this->formId; ?>time_container').hide() : jQuery('#<?php echo $this->formId; ?>time_container').show(); 
});
jQuery('#<?php echo $this->formId; ?>date_all').live("change", function()
{
	this.checked ? jQuery('#<?php echo $this->formId; ?>date_container').hide() : jQuery('#<?php echo $this->formId; ?>date_container').show(); 
});

jQuery("#<?php echo $this->getName(); ?>neverExpires").live( 'click', function(){
	jQuery("#<?php echo $this->getName(); ?>expires-wrapper").toggle();
	});

jQuery("#<?php echo $this->getName(); ?>notForSale").live( 'click', function(){
	jQuery("#<?php echo $this->getName(); ?>price-wrapper").toggle();
	});

jQuery('#<?php echo $this->formId; ?>date_type').live("change", function(){
	var date_type = jQuery('#<?php echo $this->formId; ?>date_type:checked').val();
	switch( date_type )
	{
		case 'range':
			jQuery('#<?php echo $this->formId; ?>date_range').show();
			jQuery('#<?php echo $this->formId; ?>date_fixed').hide();
			break;
		case 'fixed':
			jQuery('#<?php echo $this->formId; ?>date_range').hide();
			jQuery('#<?php echo $this->formId; ?>date_fixed').show();
			break;
	}
});

jQuery('#<?php echo $this->formId; ?>service_type').live("change", function() {
	jQuery('#<?php echo $this->formId; ?>_service').hide();
	var serviceType = jQuery('#<?php echo $this->formId; ?>service_type:checked').val();
	switch( serviceType ){
		case 'one':
			jQuery('#<?php echo $this->formId; ?>_fixed_services').hide();

			jQuery('#<?php echo $this->formId; ?>_service').show();
			jQuery('#<?php echo $this->formId; ?>_details_qty').hide();
			jQuery('#<?php echo $this->formId; ?>_details_duration').hide();
			jQuery('#<?php echo $this->formId; ?>_details_amount').hide();

			var what2show = jQuery('#<?php echo $this->formId; ?>pack_type:checked').val();
			what2show = '#<?php echo $this->formId; ?>_details_' + what2show;
			jQuery(what2show).show();
			break;
		case 'fixed':
			jQuery('#<?php echo $this->formId; ?>_service').hide();
			jQuery('#<?php echo $this->formId; ?>_details_qty').hide();
			jQuery('#<?php echo $this->formId; ?>_details_duration').hide();
			jQuery('#<?php echo $this->formId; ?>_details_amount').hide();

			jQuery('#<?php echo $this->formId; ?>_fixed_services').show();
			break;
		}
	});

jQuery('#<?php echo $this->formId; ?>pack_type').live("change", function() {
	jQuery('#<?php echo $this->formId; ?>_details_qty').hide();
	jQuery('#<?php echo $this->formId; ?>_details_duration').hide();
	jQuery('#<?php echo $this->formId; ?>_details_amount').hide();

	var what2show = jQuery('#<?php echo $this->formId; ?>pack_type:checked').val();
	what2show = '#<?php echo $this->formId; ?>_details_' + what2show;
	jQuery(what2show).show();
	});

jQuery('#nts-toggle-all-services').live("change", function(){
	if( this.checked ){
		jQuery('#<?php echo $this->formId; ?>service_id_container').hide();
		}
	else {
		jQuery('#<?php echo $this->formId; ?>service_id_container').show();
		}
	});
</script>