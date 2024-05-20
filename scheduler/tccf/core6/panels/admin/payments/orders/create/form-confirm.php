<?php
echo $this->makePostParams('-current-', 'create' );
?>

<?php
echo ntsForm::wrapInput(
	'',
	'<INPUT class="btn btn-default" TYPE="submit" VALUE="' . M('OK') . '">'
	)
?>

<script language="JavaScript">
jQuery(document).ready( function()
{
	if( jQuery("#<?php echo $this->getName(); ?>addPayment").is(":checked") )
	{
		jQuery("#<?php echo $this->getName(); ?>_details_amount").show();
	}
	else
	{
		jQuery("#<?php echo $this->getName(); ?>_details_amount").hide();
	}
});

jQuery("#<?php echo $this->getName(); ?>addPayment").live( 'click', function()
{
	jQuery("#<?php echo $this->getName(); ?>_details_amount").toggle();
});
</script>
