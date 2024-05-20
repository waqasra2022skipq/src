<?php echo M('Please give a reason'); ?>
<p>
<?php
echo $this->makeInput (
	'textarea',
	array(
		'id'		=> 'reason',
		'attr'		=> array(
			'cols'	=> 32,
			'rows'	=> 3,
			),
		'default'	=> '',
		),
	array(
		)
	);
?>
<p>
<?php
$action = $_NTS['REQ']->getRequestedAction();
echo $this->makePostParams('-current-', $action . '-confirm' );

$object = $this->getValue('object');
if( is_array($object) ){
	$paid_amount = 0;
	foreach( $object as $obj ){
		$paid_amount += $obj->getPaidAmount();
	}
}
else {
	$paid_amount = $object->getPaidAmount();
}
?>
<?php if( $paid_amount ) : ?>
	<?php
	$invoices = $object->getInvoices();
	?>
	<div class="alert alert-default-o">
		<ul class="list-unstyled list-separated ">
			<li class="text-warning">
			<?php echo M('Already Paid'); ?>: <strong><?php echo ntsCurrency::formatPrice($paid_amount); ?></strong>
			</li>
			<li>
				<ul class="list-unstyled list-separated">
				<?php foreach( $invoices as $ia ) : ?>
					<?php
					list( $invoiceId, $myNeededAmount, $due ) = $ia;
					$inv = ntsObjectFactory::get('invoice');
					$inv->setId( $invoiceId );
					?>
					<a class="nts-no-ajax" target="_blank" href="<?php echo ntsLink::makeLink('admin/payments/invoices/edit/edit', '', array('_id' => $inv->getId())); ?>">
					<?php echo M('Invoice'); ?> <?php echo $inv->getProp('refno'); ?>
					</a>
				<?php endforeach; ?>
				</ul>
			</li>

			<li>
			<?php
			echo $this->makeInput(
				'radioSet',
				array(
					'id'		=> 'overpaid',
					'default'	=> 'delete',
					'options'	=> array(
						array( 'delete',	M('Delete Invoice and Payments') ),
						array( 'keep',		M('Move Paid Amount To Customer Balance') ),
						),
					)
				);
			?>
			</li>
		</ul>
	</div>
<?php endif; ?>

<INPUT class="btn btn-default" TYPE="submit" VALUE="<?php echo M('Confirm'); ?>">
