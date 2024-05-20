<?php
$object = ntsLib::getVar( 'admin/payments/invoices/edit::OBJECT' );
$printView = ($NTS_VIEW[NTS_PARAM_VIEW_MODE] == 'print') ? TRUE : FALSE;
$display = $_NTS['REQ']->getParam( 'display' );
?>
<?php if ( ! $printView ) : ?>
	<a target="_blank" class="nts-no-ajax pull-right" href="<?php echo ntsLink::makeLink('-current-/../edit', '', array(NTS_PARAM_VIEW_MODE => 'print')); ?>">
		<i class="fa fa-print"></i> <?php echo M('Print View'); ?>
	</a> 
<?php endif; ?>

<h2>
	<i class="fa fa-file-text-o"></i> <?php echo M('Invoice'); ?> #<?php echo $object->getProp('refno'); ?>
</h2>
