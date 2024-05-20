<?php
$object = ntsLib::getVar( 'admin/payments/invoices/edit::OBJECT' );
$ntsconf =& ntsConf::getInstance();
$taxTitle = $ntsconf->get('taxTitle');
$t = $NTS_VIEW['t'];
$ff =& ntsFormFactory::getInstance();
$printView = ($NTS_VIEW[NTS_PARAM_VIEW_MODE] == 'print') ? TRUE : FALSE;

$customer = $object->getCustomer();
$customer_email = $customer->getProp('email');
?>

<?php if( $customer ) : ?>
	<?php if( $customer ) : ?>
		<p>
		<a target="_blank" class="nts-no-ajax" href="<?php echo ntsLink::makeLink('admin/customers/edit/edit', '', array('_id' => $customer->getId())); ?>">
			<i class="fa fa-fw fa-user"></i><?php echo ntsView::objectTitle($customer); ?>
		</a>
		</p>
	<?php endif; ?>
<?php	endif; ?>

<?php
$customerLink = $NTS_VIEW['customerLink'];
?>
<p>
<?php echo M('URL For Customer'); ?>
</p>
<p>
<input style="width: 100%;" type="text" class="nts-url-to-send form-control" value="<?php echo $customerLink; ?>" onclick="this.focus();this.select();">
</p>
<p>
<a target="_blank" class="nts-no-ajax" href="<?php echo $customerLink; ?>"><?php echo M('Preview'); ?></a> 
</p>

<?php if( ! $customer_email ) : ?>
	<p class="text-danger">
		<?php echo M('No Email'); ?>
	</p>
<?php else : ?>
	<?php
	echo $NTS_VIEW['formSend']->display();
	?>
<?php endif; ?>