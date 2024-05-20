<?php
$ntsdb =& dbWrapper::getInstance();
$ntsConf =& ntsConf::getInstance();
$currency = $ntsConf->get( 'currency' );
$currency = strtoupper( $currency );

$dateType = $this->getValue('date_type');
$t = new ntsTime;
$t->setNow();
$today = $t->formatDate_Db();

$minStart = NTS_TIME_STARTS;
$maxEnd = NTS_TIME_ENDS;

$ress = ntsLib::getVar( 'admin::ress' );
$locs = ntsLib::getVar( 'admin::locs' );
$sers = ntsLib::getVar( 'admin::sers' );
$packs = ntsObjectFactory::getAllIds( 'pack' );

$serviceOptions = array();
reset( $sers );
foreach( $sers as $sid ){
	$s = ntsObjectFactory::get( 'service', $sid );
	$servicePrice = $s->getProp('price');
	if( strlen($servicePrice) && ($servicePrice > 0) ){
		$serviceView = $s->getProp('title');
		$serviceView .= ' [' . ntsTime::formatPeriod($s->getProp('duration')) . ']';
		$serviceView .= ' - ' . ntsCurrency::formatPrice($s->getProp('price')) . '';
		$serviceOptions[] = array( $s->getId(), $serviceView );
		}
	}

$resourceOptions = array();
reset( $ress );
foreach( $ress as $rid ){
	$r = ntsObjectFactory::get( 'resource', $rid );
	$resourceView = ntsView::objectTitle( $r );
	$resourceOptions[] = array( $r->getId(), $resourceView );
	}

$locationOptions = array();
reset( $locs );
foreach( $locs as $lid ){
	$l = ntsObjectFactory::get( 'location', $lid );
	$locationView = ntsView::objectTitle( $l );
	$locationOptions[] = array( $l->getId(), $locationView );
	}

$packOptions = array();
reset( $packs );
foreach( $packs as $pid ){
	$p = ntsObjectFactory::get( 'pack', $pid );
	$packPrice = $p->getProp('price');
	if( strlen($packPrice) && ($packPrice > 0) ){
		$packView = $p->getProp('title');
		$packView .= ' - ' . ntsCurrency::formatPrice($p->getProp('price')) . '';
		$packOptions[] = array( $p->getId(), $packView );
		}
	}
?>

<?php
echo ntsForm::wrapInput(
	M('Title'),
	$this->buildInput(
	/* type */
		'text',
	/* attributes */
		array(
			'id'		=> 'title',
			'attr'		=> array(
				'size'	=> 42,
				),
			'default'	=> '',
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
					'class'	=> 'promotion',
					'skipMe'	=> 1
					),
				),
			)
		)
	);
?>

<?php
echo ntsForm::wrapInput(
	M('Price'),
	array(
		$this->buildInput(
		/* type */
			'select',
		/* attributes */
			array(
				'id'			=> 'sign',
				'options'		=> array(
					array('-', '&nbsp;&nbsp;-&nbsp;&nbsp;'),
					array('', '&nbsp;&nbsp;+&nbsp;&nbsp;'),
					),
				'default'	=> '-',
				),
		/* validators */
			array(
				)
			),
		' ',
		$this->buildInput(
		/* type */
			'text',
		/* attributes */
			array(
				'id'		=> 'amount',
				'attr'	=> array(
					'size'	=> 4,
					),
				'default'	=> 10,
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
/*
				array(
					'code'		=> 'greaterThan.php', 
					'error'		=> M('Required'),
					'params'	=> array(
						'compareWith'	=> 0,
						)
					),
*/
				)
			),
		' ',
		$this->buildInput(
		/* type */
			'select',
		/* attributes */
			array(
				'id'			=> 'measure',
				'options'		=> array(
					array('%', '%'),
					array('', $currency),
					),
				'default'	=> '%',
				),
		/* validators */
			array(
				)
			)
		)
	);
?>

<?php
echo ntsForm::wrapInput(
	M('Coupon Code Required') . '?',
	$this->buildInput(
	/* type */
		'checkbox',
	/* attributes */
		array(
			'id'		=> 'coupon_required',
			'default'	=> 0,
			)
		)
	);
?>

<div id="<?php echo $this->formId; ?>coupon_container">

<?php
echo ntsForm::wrapInput(
	M('Coupon Codes'),
	$this->buildInput(
	/* type */
		'textarea',
	/* attributes */
		array(
			'id'		=> 'coupon',
			'attr'	=> array(
				'rows'	=> 4,
				'cols'	=> 20,
				),
			'help' => M('One option per line')
			),
	/* validators */
		array(
			array(
				'code'		=> 'notEmpty.php', 
				'error'		=> M('Required'),
				)
			)
		)
	);
?>

<?php
echo ntsForm::wrapInput(
	M('Usage Limit'),
	$this->buildInput(
	/* type */
		'text',
	/* attributes */
		array(
			'id'		=> 'coupon_limit',
			'attr'	=> array(
				'size'	=> 4,
				),
			'help' => M('Enter 0 for no limit'),
			'default'	=> 0,
			),
	/* validators */
		array(
			array(
				'code'		=> 'notEmpty', 
				'error'		=> M('Required'),
				),
			array(
				'code'		=> 'number', 
				'error'		=> M('Numbers only'),
				),
			)
		)
	);
?>
</div>

<?php
$tabs_appointments_view = '';
ob_start();
?>

<?php if( count($locs) > 1 ) : ?>
	<?php
	echo ntsForm::wrapInput(
		M('Location'),
		$this->buildInput(
		/* type */
			'checkboxSet',
		/* attributes */
			array(
				'id'			=> 'location',
				'options'		=> $locationOptions,
				'includeAll'	=> TRUE,
				'allValue'		=> -1,
				'default'		=> array(-1),
				),
		/* validators */
			array(
				)
			)
		);
	?>
<?php endif; ?>

<?php if( count($ress) > 1 ) : ?>
	<?php
	echo ntsForm::wrapInput(
		M('Bookable Resource'),
		$this->buildInput(
		/* type */
			'checkboxSet',
		/* attributes */
			array(
				'id'			=> 'resource',
				'options'		=> $resourceOptions,
				'includeAll'	=> TRUE,
				'allValue'		=> -1,
				'default'		=> array(-1),
				),
		/* validators */
			array(
				)
			)
		);
	?>
<?php endif; ?>

<?php if( count($sers) > 1 ) : ?>
	<?php
	echo ntsForm::wrapInput(
		M('Service'),
		$this->buildInput(
		/* type */
			'checkboxSet',
		/* attributes */
			array(
				'id'			=> 'service',
				'options'		=> $serviceOptions,
				'includeAll'	=> 1,
				'allValue'		=> -1,
				'default'		=> array(-1),
				),
		/* validators */
			array(
				)
			)
		);
	?>
<?php endif; ?>

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
							'code'		=> 'greaterEqualThan.php', 
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

<?php
$tabs_appointments_view = ob_get_contents();
ob_end_clean();
?>

<?php
$tabs_packs_view = '';
ob_start();
?>

<?php if( 1 OR count($packs) > 1 ) : ?>
	<?php
	echo ntsForm::wrapInput(
		M('Package'),
		$this->buildInput(
		/* type */
			'checkboxSet',
		/* attributes */
			array(
				'id'			=> 'pack',
				'options'		=> $packOptions,
				'includeAll'	=> 1,
				'allValue'		=> -1,
				'default'		=> array(-1),
				),
		/* validators */
			array(
				)
			)
		);
	?>
<?php else : ?>
	<?php
	echo ntsForm::wrapInput(
		M('Package'),
		M('Any')
		);
	?>
<?php endif; ?>

<?php
$tabs_packs_view = ob_get_contents();
ob_end_clean();
?>

<?php
echo $this->makeInput(
/* type */
	'hidden',
/* attributes */
	array(
		'id'	=> 'tab',
		)
);

$tabs = HC_Html_Factory::widget('tabs');
$tabs_id = 'nts' . hc_random();
$tabs->set_id( $tabs_id );

$value_tab = $this->getValue('tab');
if( ! $value_tab ){
	$value_tab = 'appointments';
}
$tabs->set_active( $value_tab );

$tabs->add_tab( 'appointments', M('Appointments'), $tabs_appointments_view );
$tabs->add_tab( 'packs', M('Packages'), $tabs_packs_view );

/* hidden field */
$name_tab = 'nts-tab';
$tabs_js = <<<EOT

<script language="JavaScript">
jQuery('#{$tabs_id}').closest('form').find('[name={$name_tab}]').val( "{$value_tab}" )
jQuery('#{$tabs_id} a.hc-tab-toggler').on('shown.hc.tab', function(e)
{
	var active_tab = jQuery(this).data('toggle-tab');
	jQuery(this).closest('form').find('[name={$name_tab}]').val( active_tab );
});
</script>

EOT;

echo $tabs->render();
echo $tabs_js;
?>

<?php echo $this->makePostParams('-current-', 'save' ); ?>
<?php
echo ntsForm::wrapInput(
	'',
	'<input class="btn btn-default" type="submit" value="' . M('Save') . '">'
	);
?>

<script language="JavaScript">
jQuery(document).ready( function()
{
/* time */
	jQuery("#<?php echo $this->formId; ?>time_all").is(":checked") ? jQuery('#<?php echo $this->formId; ?>time_container').hide() : jQuery('#<?php echo $this->formId; ?>time_container').show(); 
/* coupon */
	jQuery("#<?php echo $this->formId; ?>coupon_required").is(":checked") ? jQuery('#<?php echo $this->formId; ?>coupon_container').show() : jQuery('#<?php echo $this->formId; ?>coupon_container').hide(); 

	jQuery("#<?php echo $this->formId; ?>date_all").is(":checked") ? jQuery('#<?php echo $this->formId; ?>date_container').hide() : jQuery('#<?php echo $this->formId; ?>date_container').show(); 
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

jQuery('#<?php echo $this->formId; ?>time_all').live("change", function()
{
	this.checked ? jQuery('#<?php echo $this->formId; ?>time_container').hide() : jQuery('#<?php echo $this->formId; ?>time_container').show(); 
});

jQuery('#<?php echo $this->formId; ?>coupon_required').live("change", function()
{
	this.checked ? jQuery('#<?php echo $this->formId; ?>coupon_container').show() : jQuery('#<?php echo $this->formId; ?>coupon_container').hide(); 
});

jQuery('#<?php echo $this->formId; ?>date_all').live("change", function()
{
	this.checked ? jQuery('#<?php echo $this->formId; ?>date_container').hide() : jQuery('#<?php echo $this->formId; ?>date_container').show(); 
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
</script>

