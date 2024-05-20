<?php
$invoice = ntsLib::getVar( 'system/invoice::OBJECT' );
$ntsconf =& ntsConf::getInstance();
$taxTitle = $ntsconf->get('taxTitle');
$taxRate = $ntsconf->get('taxRate');
$refno = $invoice->getProp('refno');

$invoiceInfo = $NTS_VIEW['invoiceInfo'];

$pgm =& ntsPaymentGatewaysManager::getInstance();
$paymentGateways = ntsLib::getVar( 'system/invoice::paymentGateways' );

$t = $NTS_VIEW['t'];
$t->setNow();
$today = $t->formatDate_Db();
$due_date = $t->formatDate_Db( $invoice->getProp('due_at') );

$ff =& ntsFormFactory::getInstance();
$printView = ($NTS_VIEW[NTS_PARAM_VIEW_MODE] == 'print') ? TRUE : FALSE;

$customer = $invoice->getCustomer();

$invoiceHeader = $ntsconf->get('invoiceHeader');
$invoiceFooter = $ntsconf->get('invoiceFooter');

$subTotal = $invoice->getSubTotal();
$taxAmount = $invoice->getTaxAmount();
$total = $subTotal + $taxAmount;
$paidAmount = $invoice->getPaidAmount();
$totalDue = $total - $paidAmount;

if( $totalDue > 0 )
{
	$status_class = ($due_date > $today) ? 'danger' : 'warning';
	$status_text = ( $paidAmount > 0 ) ? M('Partially Paid') : M('Not Paid');
	$status_view = array($status_class, $status_text);
}
else
{
	$status_view = array('success', M('Paid'));
}
$status_view = '<span class="btn btn-' . $status_view[0] . '">' . $status_view[1] . '</span>';
?>

<?php if( ! $printView ) : ?> 
<p>
	<a class="btn btn-default" target="_blank" href="<?php echo ntsLink::makeLink('-current-', '', array('refno' => $refno, NTS_PARAM_VIEW_MODE => 'print')); ?>">
		<i class="fa fa-print"></i> <?php echo M('Print'); ?>
	</a>
</p>
<?php endif; ?>

<p>
<?php echo nl2br($invoiceHeader); ?>
</p>

<div class="page-header">
	<h2>
		<?php echo M('Invoice'); ?> #<?php echo $invoice->getProp('refno'); ?> <?php echo $status_view; ?>
	</h2>
</div>

<dl class="dl-horizontal">
	<?php if( $customer ) : ?>
		<dt><?php echo M('Customer'); ?></dt>
		<dd><?php echo ntsView::objectTitle($customer); ?></dd>

<?php
$skip_custom = array('username', 'first_name', 'last_name');
$om =& objectMapper::getInstance();
$details = $om->makeDetails_Customer( $customer, 'external' );
// $details = array();
?>
<?php foreach( $details as $dn => $da ) : ?>
	<?php
	if( in_array($dn, $skip_custom) ){
		continue;
	}
	if( ! strlen($da[1]) ){
		continue;
	}
	?>
		<dt><?php echo $da[0]; ?></dt>
		<dd><?php echo $da[1]; ?></dd>

<?php endforeach; ?>

	<?php endif; ?>

	<dt><?php echo M('Due Date'); ?></dt>
	<dd><?php echo $t->formatDateFull( $invoice->getProp('due_at') ); ?></dd>
</dl>

<h3>
<?php echo M('Items'); ?>
</h3>

<?php
$items = $invoice->getItems();

$table = new ntsHtmlTable;
$table->configView( 
	array(
		'status'		=> 'text',
		'name'			=> 'text',
		'description'	=> 'text',
		'quantity'		=> 'integer',
		'unitCost'		=> 'price',
		)
	);

$header = array();
$header[] = M('Description');
$header[] = array(
	'value'	=> M('Quantity'),
	'style'	=> 'text-align: center;',
	);
if( $taxRate )
{
	$header[] = array(
		'value'		=>  M('Taxable'),
		'style'		=> 'text-align: center;',
		);
}
$header[] = array(
	'value'	=> M('Unit Price'),
	'style'	=> 'text-align: left;',
	);

$discounts = $invoice->getProp('_discount');
$totalDiscount = 0;
reset( $discounts );
foreach( $discounts as $k => $da )
{
	$totalDiscount += $da;
}

if( $totalDiscount )
{
	$header[] = M('Discount');
	$header[] = M('Total');
}

$table->setHeader( $header );

reset( $items );
foreach( $items as $e )
{
	$view = $table->prepareView( $e );

	$row = array();
	$row[] = $view['name'] . '<br>' . $view['description'];
	$row[] = array(
		'value'	=> $view['quantity'],
		'style'	=> 'text-align: center;',
		);

	if( $taxRate )
	{
		$value = $e['unitTaxRate'] ? M('Yes') : M('No');
		$row[] = array(
			'value'	=> $value,
			'style'	=> 'text-align: center;',
			);
	}

	if( $totalDiscount )
	{
		$key = $e['object']->getClassName() . ':' . $e['object']->getId();
		if( isset($discounts[$key]) )
		{
			$row[] = ntsCurrency::formatPrice( $e['unitCost'] + $discounts[$key] );
			$row[] = ntsCurrency::formatPrice($discounts[$key]);
		}
		else
		{
			$row[] = array(
				'value'	=> $view['unitCost'],
				'style'	=> 'text-align: left;',
				);
			$row[] = '';
		}
	}

// edit cost
	$row[] = $view['unitCost'];
	$table->addRow( $row );
}

$colspan = $taxRate ? 3 : 2;

if( $totalDiscount )
	$colspan += 2;

if( $totalDiscount )
{
	$table->addRow(
		array(
			array(
				'colspan'	=> $colspan,
				'value'		=> M('Total'),
				'style'		=> 'text-align: right;',
				'class'		=> 'subtotal',
				),
			array(
				'value'		=> ntsCurrency::formatPrice($subTotal + $totalDiscount),
				'class'		=> 'subtotal',
				),
			)
		);
	$table->addRow(
		array(
			array(
				'colspan'	=> $colspan,
				'value'		=> M('Discount'),
				'style'		=> 'text-align: right;',
				),
			array(
				'value'		=> ntsCurrency::formatPrice($totalDiscount),
				),
			)
		);
}

if( $taxAmount )
{
	$table->addRow(
		array(
			array(
				'colspan'	=> $colspan,
				'value'		=> M('Subtotal'),
				'style'		=> 'text-align: right;',
				'class'		=> 'subtotal',
				),
			array(
				'value'		=> ntsCurrency::formatPrice($subTotal),
				'class'		=> 'subtotal',
				),
			)
		);

	$table->addRow(
		array(
			array(
				'colspan'	=> $colspan,
				'value'		=> $taxTitle,
				'style'		=> 'text-align: right;',
				),
			array(
				'value'		=> ntsCurrency::formatPrice($taxAmount),
				'style'		=> '',
				),
			)
		);
}

if( $paidAmount )
{
	$table->addRow(
		array(
			array(
				'colspan'	=> $colspan,
				'value'		=> '<strong>' . M('Total') . '</strong>',
				'style'		=> 'text-align: right;',
				'class'		=> 'subtotal',
				),
			array(
				'value'		=> '<strong>' . ntsCurrency::formatPrice($total) . '</strong>',
				'class'		=> 'subtotal',
				),
			)
		);

	$table->addRow(
		array(
			array(
				'colspan'	=> $colspan,
				'value'		=> M('Paid'),
				'style'		=> 'text-align: right;',
				),
			array(
				'value'		=> ntsCurrency::formatPrice($paidAmount),
				'style'		=> '',
				),
			)
		);
	}

$table->addRow(
	array(
		array(
			'colspan'	=> $colspan,
			'value'		=> '<strong>' . M('Total Due') . '</strong>',
			'style'		=> 'text-align: right;',
			'class'		=> 'subtotal',
			),
		array(
			'value'		=> '<strong>' . ntsCurrency::formatPrice($totalDue) . '</strong>',
			'class'		=> 'subtotal',
			),
		)
	);
?>
<?php if( $items ) : ?>
<?php 	$table->display(); ?>
<?php else : ?>
<?php 	echo M('None'); ?>
<?php endif; ?>

<?php require( dirname(__FILE__) . '/transactions.php' ); ?>

<?php if( ($totalDue > 0) && $paymentGateways && (! $printView) ) : ?>
	<?php
	/* prepare some common data for payment forms */
	$paymentAmount = $totalDue;
	$paymentCurrency = $ntsconf->get( 'currency' );

	$items = $invoice->getItems(); 
	$invoiceRefNo = $invoice->getProp('refno');
	$paymentOrderRefNo = $invoiceRefNo;

	$paymentItemName = array();
	reset( $items );
	foreach( $items as $item ){
		if( count($items) > 1 )
			$paymentItemName[] = $item['name'];
		else
			$paymentItemName[] = $item['description'];
		}
	$paymentItemName = join( '<br>', $paymentItemName );
	?>

	<h2>
		<?php echo M('Total Due'); ?> <?php echo ntsCurrency::formatPrice($totalDue); ?>
	</h2>

	<ul class="list-inline">
		<li class="text-strong">
			<span class="btn btn-info">
				<?php echo M('Please Select'); ?> &raquo;
			</span>
		</li>
		<?php foreach( $paymentGateways as $gateway ) : ?>
			<?php
			$gatewayFolder = $pgm->getGatewayFolder( $gateway );
			$gatewayFile = $gatewayFolder . '/paymentForm.php';

			$paymentGatewaySettings = $pgm->getGatewaySettings( $gateway );

			if( $gateway == 'paypal' )
			{
				$objects = $invoice->getItemsObjects();
				reset( $objects );
				foreach( $objects as $obj )
				{
					$resourceId = $obj->getProp( 'resource_id' );
					$resource = ntsObjectFactory::get( 'resource' );
					$resource->setId( $resourceId );
					$myPaypal = $resource->getProp( '_paypal' );
					if( $myPaypal )
					{
						$paymentGatewaySettings['email'] = $myPaypal;
					}
				}
			}

			/* some links */
			if( defined('NTS_PAYMENT_LINK') )
			{
				$paymentNotifyUrl = ntsLink::makeLinkFull( NTS_PAYMENT_LINK, '', '', array('gateway' => $gateway) ) . '&nts-refno=' . $invoiceRefNo;
			}
			else
			{
				$paymentNotifyUrl = ntsLink::makeLink( 'system/payment', '', array('gateway' => $gateway) ) . '&nts-refno=' . $invoiceRefNo;
			}
			$paymentOkUrl = ntsLink::makeLink( 'customer/invoices/view', '', array('refno' => $invoiceRefNo, 'display' => 'ok') );
			$paymentFailedUrl = ntsLink::makeLink( 'customer/invoices/view', '', array('refno' => $invoiceRefNo, 'display' => 'fail') );
			?>
			<li>
			<?php require( $gatewayFile ); ?>
			</li>
		<?php endforeach; ?>
	</ul>
<?php endif; ?>

<p>
<?php echo nl2br($invoiceFooter); ?>
