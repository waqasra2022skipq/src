<?php
if( ! isset($returnBackAsRequest) )
	$returnBackAsRequest = 1;

$ntsdb =& dbWrapper::getInstance();
$cm =& ntsCommandManager::getInstance();

$display = $_NTS['REQ']->getParam( 'display' ); 
$invoiceRefNo = $_NTS['REQ']->getParam( 'refno' );
$offline = $_NTS['REQ']->getParam( 'offline' );
if( ! $invoiceRefNo )
{
	echo "invoiceRefNo required!";
	exit;
}

$invoiceId = 0;
$result = $ntsdb->select( 
	'id', 
	'invoices', 
	array(
		'refno' => array('=', $invoiceRefNo)
		)
	);

if( $i = $result->fetch() )
{
	$invoiceId = $i['id'];
}

if( ! $invoiceId )
{
	echo "invoice '$invoiceRefNo' not found!";
	exit;
}

$invoice = ntsObjectFactory::get( 'invoice' );
$invoice->setId( $invoiceId );
$invoiceId = $invoice->getId();
$invoiceInfo = $invoice->getByArray();
$invoiceInfo['totalAmount'] = $invoice->getTotalAmount();
$invoiceInfo['object'] = $invoice;

/* payments for this invoice */
$NTS_VIEW['paidAmount'] = $invoice->getPaidAmount();
$invoiceId = $invoiceInfo['id'];

if( ($display == 'ok') && (! $offline) && ($NTS_VIEW['paidAmount'] <= 0) )
{
	$display = 'fail';
	$_REQUEST['nts-display'] = $display;

	$NTS_VIEW['payments'] = array();
	$transactions = $invoice->getTransactions();
	foreach( $transactions as $tra )
	{
		$NTS_VIEW['payments'][] = $tra->getByArray();
	}
}

$forwardTo = '';
/* find dependants */
if( $display == 'ok' )
{
	$deps = $invoice->getItemsObjects();
	$packName = '';

	if( $deps )
	{
		reset( $deps );
		foreach( $deps as $dep )
		{
			$className = $dep->getClassName();
			switch( $className ){
				case 'appointment':
					$cm->runCommand( $dep, 'payonline' );

					$group_ref = $dep->getProp('group_ref');
					$forwardTo = ntsLink::makeLink( 
						'customer/appointments/view',
						'',
						array(
							'ref' => $group_ref
							)
						);
					break;

				case 'order':
					$customer_id = ntsLib::getCurrentUserId();
					if( $customer_id )
					{
						$forwardTo = ntsLink::makeLink( 
							'customer/accounting'
							);
					}
					else
					{
						$pack = ntsObjectFactory::get( 'pack' );
						$pack->setId( $dep->getProp('pack_id') );
						$packName = $pack->getFullTitle();
						if( $packName )
						{
							$invoiceInfo['item_name'] = $packName;
						}
					}
					break;
				}
		}
	}
}

if( $forwardTo )
{
	ntsView::redirect( $forwardTo );
	exit;
}

$NTS_VIEW['invoiceInfo'] = $invoiceInfo;
?>