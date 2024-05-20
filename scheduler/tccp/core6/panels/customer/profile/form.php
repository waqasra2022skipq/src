<?php
$id = $this->getValue('id');
/* form params - used later for validation */
$this->setParams(
	array(
		'myId'	=> $id,
		)
	);

$object = $this->getValue('object');

if( $object->hasRole('customer') )
	$className = 'customer';
elseif( $object->hasRole('provider') )
	$className = 'provider';
else
	$className = 'user';

$om =& objectMapper::getInstance();
if( $className == 'customer' || $className == 'user' ){
	if( $object->hasRole('admin') )
		$side = 'internal';
	else
		$side = 'external';
	}
else {
	$side = 'internal';
	}

$fields = $om->getFields( $className, $side );
reset( $fields );
$restrictions = $object->getProp( '_restriction' );

if( $restrictions )
{
	if( in_array('email_not_confirmed', $restrictions) )
		$status_view = M('Email') . ': ' . M('Not Confirmed');
	elseif( in_array('not_approved', $restrictions) )
		$status_view = M('Not Approved');
	elseif( in_array('suspended', $restrictions) )
		$status_view = M('Suspended');
}
else
{
	$status_view = M('Active');
}

if( $restrictions )
{
	$status_view = '<span class="btn btn-sm btn-danger">' . $status_view . '</span>';
}
else
{
	$status_view = '<span class="btn btn-sm btn-success">' . $status_view . '</span>';
}
?>
<?php
echo ntsForm::wrapInput(
	M('Status'),
	$status_view
	);
?>

<?php foreach( $fields as $f ) : ?>
	<?php
	$c = $om->getControl( $className, $f[0], false );
	$fieldType = $c[1];
	if( isset($f[4]) ){
		if( $f[4] == 'read' ){
			if( $c[1] == 'date/Calendar' ){
				$value = $object->getProp($f[0]);
				if( $value ){
					global $NTS_VIEW;
					$t = $NTS_VIEW['t'];
					$t->setDateDb( $value );
					$c[2]['value'] = $t->formatDate();
				}
				else {
					$c[2]['value'] = M('N/A');
				}
			}

			$c[1] = 'label';
			$c[2]['readonly'] = 1;
			}
		}
	$ri = ntsLib::remoteIntegration();
	if( ($ri == 'wordpress') && ($c[2]['id'] == 'username') )
	{
		$c[1] = 'labelData';
	}
	if( $c[2]['description'] )
		$c[2]['help'] = $c[2]['description'];


	if( NTS_ALLOW_NO_EMAIL && ($c[2]['id'] == 'email') )
	{
		$c[2]['after']	= '';
		$c[2]['after']	.= '<div class="checkbox">';
		$c[2]['after']		.= '<label>';
		$c[2]['after']		.= $this->makeInput (
								/* type */
									'checkbox',
								/* attributes */
									array(
										'id'	=> 'noEmail',
										)
									);
		$c[2]['after']		.= ' ' . M('No Email');
		$c[2]['after']		.= '</label>';
		$c[2]['after']	.= '</div>';
	}

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

<?php if( NTS_ENABLE_TIMEZONES > 0 ) : ?>
	<?php if( $className == 'customer' ) : ?>
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
					)
				)
			);
		?>
	<?php endif; ?>
<?php endif; ?>

<?php echo $this->makePostParams('-current-', 'update'); ?>
<?php
echo ntsForm::wrapInput(
	'',
	'<INPUT class="btn btn-default" TYPE="submit" VALUE="' . M('Update') . '">'
	);
?>

<?php if( NTS_ALLOW_NO_EMAIL ) : ?>
<script language="JavaScript">
jQuery(document).ready( function()
{
	if( jQuery("#<?php echo $this->getName(); ?>noEmail").is(":checked") )
	{
		jQuery("#<?php echo $this->getName(); ?>email").hide();
	}
	else
	{
		jQuery("#<?php echo $this->getName(); ?>email").show();
	}
});
jQuery("#<?php echo $this->getName(); ?>noEmail").live( 'click', function()
{
	jQuery("#<?php echo $this->getName(); ?>email").toggle();
});
</script>
<?php endif; ?>