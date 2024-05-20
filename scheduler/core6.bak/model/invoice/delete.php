<?php
$ntsdb =& dbWrapper::getInstance();
$invoiceId = $object->getId();

/* delete transactions */
$where = array(
	'invoice_id'	=> array('=', $invoiceId)
	);
$transactions = ntsObjectFactory::find( 'transaction', $where );
reset( $transactions );
foreach( $transactions as $tra ){
	$this->runCommand( $tra, 'delete' );
}

/* delete invoice items */
/*
$items = $object->getItems();
reset( $items );
foreach( $items as $itm ){
	$this->runCommand(
		$object, 
		'delete_item',
		array(
			'item_id' => $itm['id']
			)
		);
}
*/

$where = array(
	'invoice_id'	=> array('=', $invoiceId)
	);
$ntsdb->delete(
	'invoice_items',
	$where
	);

$pmm =& ntsPaymentManager::getInstance();
$pmm->deleteInvoice( $object );
?>