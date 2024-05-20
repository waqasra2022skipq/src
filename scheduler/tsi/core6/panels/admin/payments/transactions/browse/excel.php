<?php
$count = ntsLib::getVar( 'admin/payments/transactions::totalCount' );
$limit = ntsLib::getVar( 'admin/payments/transactions::limit' );
$invoice = ntsLib::getVar( 'admin/payments/transactions::invoice' );
$entries = ntsLib::getVar( 'admin/payments/transactions::entries' );
$transactionsAmount = ntsLib::getVar( 'admin/payments/transactions::transactionsAmount' );

$fields = array(
	'id'			=> '#',
	'created_at'	=> M('Date'),
	'amount'		=> M('Amount'),
	'invoice'		=> M('Invoice'),
	'paid_through'	=> M('Paid Through'),
	'notes'			=> M('Notes'),
	);
$appHeader = array(
	'location'	=> M('Appointment') . ': ' . M('Location'),
	'resource'	=> M('Appointment') . ': ' . M('Bookable Resource'),
	'service'	=> M('Appointment') . ': ' . M('Service'),
	'customer'	=> M('Appointment') . ': ' . M('Customer'),
	'date'		=> M('Appointment') . ': ' . M('Date'),
	'time'		=> M('Appointment') . ': ' . M('Time'),
	'app_id'	=> M('Appointment') . ': ' . 'ID',
	);
$appHeaderAdded = FALSE;
$out = array();
	
$out[] = array_values($fields);

$t = $NTS_VIEW['t'];

reset( $entries );
foreach( $entries as $tra ){
	$objId = $tra->getId();
	$output = array();
	$output['id'] = '#' . $objId;

	$t->setTimestamp( $tra->getProp('created_at') );
	$output['created_at'] = $t->formatFull();
	$output['amount'] = ntsCurrency::formatPrice($tra->getProp('amount'));
	
	$thisInvoiceId = $tra->getProp('invoice_id');
	if( $thisInvoiceId )
	{
		$thisInvoice = ntsObjectFactory::get('invoice');
		$thisInvoice->setId( $thisInvoiceId );
		$output['invoice'] = $thisInvoice->getProp('refno');
		$output['paid_through'] = $tra->getProp('pgateway');
		$output['paid_through'] = M(ntsLib::upperCaseMe($output['paid_through']));

		if( $tra->getProp('pgateway_ref') )
		{
			$output['notes'] = $tra->getProp('pgateway_ref') . '<br>' . $tra->getProp('pgateway_response');
		}
		else
		{
			$output['notes'] = $tra->getProp('pgateway_response');
		}

	/* check if invoice contains only one item */
		$items = $thisInvoice->getItems();

		if( count($items) == 1 )
		{
			switch( $items[0]['object']->getClassName() )
			{
				case 'appointment':
					if( ! $appHeaderAdded )
					{
						$appHeaderAdded = TRUE;
						$fields = array_merge( $fields, $appHeader );
						$out[0] = array_merge( $out[0], array_values($appHeader) );
					}

					$rid = $items[0]['object']->getProp('resource_id');
					$resource = ntsObjectFactory::get('resource');
					$resource->setId( $rid );
					$output['resource'] = ntsView::objectTitle( $resource );

					$lid = $items[0]['object']->getProp('location_id');
					$location = ntsObjectFactory::get('location');
					$location->setId( $lid );
					$output['location'] = ntsView::objectTitle( $location );

					$cid = $items[0]['object']->getProp('customer_id');
					$customer = new ntsUser;
					$customer->setId( $cid );
					$output['customer'] = ntsView::objectTitle( $customer );

					$sid = $items[0]['object']->getProp('service_id');
					$service = ntsObjectFactory::get('service');;
					$service->setId( $sid );
					$output['service'] = ntsView::objectTitle( $service );

					$t->setTimestamp( $items[0]['object']->getProp('starts_at') );
					$output['date'] = $t->formatDate();
					$output['time'] = $t->formatTime();

					$output['app_id'] = $items[0]['object']->getId();
					break;
			}
		}
	}
	else
	{
		$output['invoice'] = M('N/A');
		$output['paid_through'] = '';
		$output['notes'] = '';
	}

	$outLines = array();
	reset( $fields );
	foreach( array_keys($fields) as $f ){
		$outLines[] = isset($output[$f]) ? $output[$f] : '';
		}
	$out[] = $outLines;
	}

reset( $out );
foreach( $out as $o )
{
	echo ntsLib::buildCsv( $o );
	echo "\n";
}
?>