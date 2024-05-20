<table class="ntsForm">
<tr>
	<td class="ntsFormLabel"><?php echo M('Web Page Title'); ?></td>
	<td class="ntsFormValue">
	<?php
	echo $this->makeInput (
	/* type */
		'text',
	/* attributes */
		array(
			'id'	=> 'htmlTitle',
			'attr'	=> array(
				'size'	=> 48
				),
			)
		);
	?>
	</td>
</tr>

<tr>
	<td class="ntsFormLabel"><?php echo M('Max Appointments In Cart'); ?></td>
	<td class="ntsFormValue">
<?php
$appsInCartOptions = array();
for( $ii = 1; $ii <= 20; $ii++ ){
	$appsInCartOptions[] = array( $ii, $ii );
}

echo $this->makeInput (
/* type */
	'select',
/* attributes */
	array(
		'id'		=> 'appsInCart',
		'options'	=> $appsInCartOptions,
		)
	);
?>
	</td>
</tr>

<tr>
	<td class="ntsFormLabel"><?php echo M('Require Clients Give Appointment Cancellation Reason'); ?></td>
	<td class="ntsFormValue">
	<?php
	echo $this->makeInput (
	/* type */
		'checkbox',
	/* attributes */
		array(
			'id'		=> 'requireCancelReason',
			)
		);
	?>
	</td>
</tr>

<tr>
	<td class="ntsFormLabel"><?php echo M('CSV Field Delimiter'); ?></td>
	<td class="ntsFormValue">
	<?php
	$csvOptions = array(
		array( ',', ',' ),
		array( ';', ';' ),
		);

	echo $this->makeInput (
	/* type */
		'select',
	/* attributes */
		array(
			'id'		=> 'csvDelimiter',
			'options'	=> $csvOptions,
			)
		);
	?>
	</td>
</tr>
<tr>
	<td class="ntsFormValue" colspan="2">
	<i><?php echo M('This may depend on your Excel regional settings'); ?></i>
	</td>
</tr>

<tr>
	<td class="ntsFormLabel"><?php echo M('Attach Ical File To Notification Email'); ?></td>
	<td class="ntsFormValue">
	<?php
	echo $this->makeInput (
	/* type */
		'checkbox',
	/* attributes */
		array(
			'id'		=> 'attachIcal',
			)
		);
	?>
	</td>
</tr>

<tr>
	<td class="ntsFormLabel"><?php echo M('Use Captcha For Non-Registered Users'); ?></td>
	<td class="ntsFormValue">
	<?php
	echo $this->makeInput (
	/* type */
		'checkbox',
	/* attributes */
		array(
			'id'	=> 'useCaptcha',
			)
		);
	?>
	</td>
</tr>

<tr>
	<td class="ntsFormLabel"><?php echo M('Require Strong Passwords'); ?></td>
	<td class="ntsFormValue">
	<?php
	echo $this->makeInput (
	/* type */
		'checkbox',
	/* attributes */
		array(
			'id'	=> 'strongPassword',
			)
		);
	?>
	</td>
</tr>

<tr>
	<td class="ntsFormLabel"><?php echo M('Send CC For Appointment'); ?></td>
	<td class="ntsFormValue">
	<?php
	echo $this->makeInput (
	/* type */
		'checkbox',
	/* attributes */
		array(
			'id'	=> 'sendCcForAppointment',
			)
		);
	?>
	</td>
</tr>

<tr>
	<td class="ntsFormLabel"><?php echo M('Staff Can Edit Customers Login Details'); ?></td>
	<td class="ntsFormValue">
	<?php
	echo $this->makeInput (
	/* type */
		'checkbox',
	/* attributes */
		array(
			'id'	=> 'staffCanEditCustomerLogin',
			)
		);
	?>
	</td>
</tr>

<tr>
	<td class="ntsFormLabel"><?php echo M('Hide End Time In Customer Notification Emails'); ?></td>
	<td class="ntsFormValue">
	<?php
	echo $this->makeInput (
	/* type */
		'checkbox',
	/* attributes */
		array(
			'id'	=> 'customerNoEndTimeNotification',
			)
		);
	?>
	</td>
</tr>


<tr>
<td>&nbsp;</td>
<td>
<?php echo $this->makePostParams('-current-', 'update'); ?>
<input class="btn btn-default" type="submit" value="<?php echo M('Save'); ?>">
</td>
</tr>

</table>