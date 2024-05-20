<?php
$ntsdb =& dbWrapper::getInstance();
$customerId = ntsLib::getCurrentUserId();

$entries = array();

$pm =& ntsPaymentManager::getInstance();
$ids = $pm->getInvoicesOfCustomer( $customerId );

if( $ids )
{
	ntsObjectFactory::preload( 'invoice', $ids );
	reset( $ids );
	foreach( $ids as $id )
	{
		$e = ntsObjectFactory::get( 'invoice' );
		$e->setId( $id );
		$items = $e->getItems();
		if( $items )
		{
			$entries[] = $e;
		}
	}
}
ntsLib::setVar( 'customer/invoices/browse::entries', $entries );
?>