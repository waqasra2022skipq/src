<?php
$object = ntsLib::getVar( 'admin/payments/invoices/edit::OBJECT' );
$items = $object->getItems();

$ntsconf =& ntsConf::getInstance();
$taxTitle = $ntsconf->get('taxTitle');
$taxRate = $ntsconf->get('taxRate');
$t = $NTS_VIEW['t'];
$ff =& ntsFormFactory::getInstance();
$printView = ($NTS_VIEW[NTS_PARAM_VIEW_MODE] == 'print') ? TRUE : FALSE;

$customer = $object->getCustomer();
?>

<?php if ( $printView ) : ?>
	<h2>
		<?php echo M('Invoice'); ?> #<?php echo $object->getProp('refno'); ?>
	</h2>
<?php endif; ?>

<div class="row">
	<div class="col-sm-4">
		<ul class="list-inline">
			<li>
				<?php echo M('Due Date'); ?>:
			</li>
			<li>
<?php
$NTS_VIEW['formDueDate']->display(array());
?>
			</li>
		</ul>
	</div>

	<div class="col-sm-4">
		<?php echo M('Created'); ?>: <strong><?php echo $t->formatDateFull( $object->getProp('created_at') ); ?></strong>
	</div>

	<?php if( $customer ) : ?>
		<div class="col-sm-4">
			<?php if ( $printView ) : ?>
				<?php echo M('Customer'); ?>: <strong><?php echo ntsView::objectTitle($customer); ?></strong>
			<?php else : ?>
				<?php echo M('Customer'); ?>: 
				<a target="_blank" class="nts-no-ajax" href="<?php echo ntsLink::makeLink('admin/customers/edit/edit', '', array('_id' => $customer->getId())); ?>">
					<?php echo ntsView::objectTitle($customer); ?>
				</a>
			<?php endif; ?>
		</div>
	<?php endif; ?>
</div>

<h3>
	<?php echo M('Items'); ?>
</h3>

<?php
$colspan = $taxRate ? 4 : 3;

$table = new ntsHtmlTable;
$table->configView( 
	array(
		'name'			=> 'text',
		'description'	=> 'text',
		'quantity'		=> 'integer',
		'unitCost'		=> 'price',
		)
	);

$header = array();
$header[] = M('Description');
$header[] = array(
	'value'		=>  M('Quantity'),
	'style'		=> 'text-align: center;',
	);
$header[] = array(
	'value'		=>  M('Unit Price'),
	'style'		=> 'text-align: center;',
	);
if( $taxRate )
{
	$header[] = array(
		'value'		=>  M('Taxable'),
		'style'		=> 'text-align: center;',
		);
}
$header[] = array(
	'value'		=>  M('Total'),
	'style'		=> 'text-align: left;',
	);

reset( $items );
foreach( $items as $e )
{
	$view = $table->prepareView($e);
	$row = array();

	$title = $view['name'] . '<br>' . $view['description'];
	if( ! $printView )
	{
		if( $e['object'] )
		{
			switch( $e['object']->getClassName() )
			{
				case 'appointment':
					$title = '';
					$title .= $view['name'] . '<br>';
					$title .= '<a href="' . ntsLink::makeLink('admin/manage/appointments/edit/overview', '', array('_id' => $e['object']->getId())) . '" target="_blank" class="nts-no-ajax">' . "\n" . $view['description'] . "\n" . '</a>';
					break;
			}
		}
		else
		{
			$deleteLink = ntsLink::makeLink( 
				'-current-/delete_item',
				'', 
				array(
					'item_id'			=> $e['id'],
					NTS_PARAM_VIEW_RICH	=> 'basic',
					)
				);

			$title = '';
			$title .= '<span class="nts-ajax-parent">';
			$title .= '<a class="nts-ajax-loader btn btn-default btn-xs" href="' . $deleteLink . '" title="' . M('Delete') . '">';
			$title .= '<span class="close2 text-danger">&times;</span>';
			$title .= '</a>';
			$title .= '<span class="nts-ajax-container">';
			$title .= '</span>';
			$title .= '</span>';
			$title .= ' ' . $view['name'];
		}
	}
	$row[] = $title;

	$row[] = array(
		'value'		=> $view['quantity'],
		'style'		=> 'text-align: center;',
		);
	$row[] = array(
		'value'		=> $view['unitCost'],
		'style'		=> 'text-align: center;',
		);
	if( $taxRate )
	{
		$value = $e['unitTaxRate'] ? M('Yes') : M('No');
		$row[] = array(
			'value'	=> $value,
			'style'	=> 'text-align: center;',
			);
	}
	$row[] = array(
		'value'		=> ntsCurrency::formatPrice($e['quantity'] * $e['unitCost']),
		'style'		=> 'text-align: left;',
		);
	$table->addRow( $row );
}

/* add new item form */
if( ! $printView )
{
	$row = array();
	$NTS_VIEW['formNew']->noprint = TRUE;
	$table->addRow( $NTS_VIEW['formNew']->display(array(), TRUE, TRUE) );
}
?>

<?php
$subTotal = $object->getSubTotal();
$taxAmount = $object->getTaxAmount();

$calc = new ntsMoneyCalc;
$calc->add( $subTotal );
$calc->add( $taxAmount );
$total = $calc->result();

$paidAmount = $object->getPaidAmount();

$calc = new ntsMoneyCalc;
$calc->add( $total );
$calc->add( -$paidAmount );
$totalDue = $calc->result();

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
				'style'		=> 'text-align: left;',
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
				'style'		=> 'text-align: left;',
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
				'style'		=> 'text-align: left;',
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

$table->setHeader( $header );
?>

<?php echo ntsForm::start( $NTS_VIEW['formNew']->formId ); ?>
<?php $table->display(); ?>
</form>

<h3>
<?php echo M('Payments'); ?>
</h3>

<p>
<?php require( dirname(__FILE__) . '/../../../transactions/browse/index.php' ); ?>
