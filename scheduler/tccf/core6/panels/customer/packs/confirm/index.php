<div class="page-header">
	<h2>
		<?php echo M('Confirm Package'); ?>
	</h2>
</div>

<?php require( dirname(__FILE__) . '/../_index_confirm.php' ); ?>

<dl class="dl-horizontal">
	<dt>
		&nbsp;
	</dt>
	<dd>
		<a class="btn btn-default btn-lg" href="<?php echo ntsLink::makeLink('-current-', 'confirm'); ?>">
			<?php echo M('Confirm Package'); ?>
		</a>
	</dd>
</dl>

<?php if( $show_coupon ) : ?>
<script language="JavaScript">
jQuery(document).on( 'click', 'a#nts-apply-coupon', function(e)
{
	var targetUrl = jQuery(this).attr('href');
	var couponCode = jQuery(this).closest('form').find('[name=nts-coupon]').val();
	targetUrl += '&nts-action=coupon&nts-coupon=' + couponCode;
	document.location.href = targetUrl;
	return false;
});
</script>
<?php endif; ?>