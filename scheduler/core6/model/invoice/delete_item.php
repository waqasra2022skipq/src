<?php
$item_id = $params['item_id'];

$ntsdb =& dbWrapper::getInstance();

$item = $ntsdb->get_select(
	array( 'amount', 'qty' ),
	'invoice_items',
	array(
		'id' => array('=', $item_id)
		)
	);

if( ! isset($item[0]) )
	return;

$item = $item[0];
$params['item'] = $item;

$where = array(
	'id'	=> array('=', $item_id)
	);
$return = $ntsdb->delete(
	'invoice_items',
	$where
	);

if( ! $return )
{
	$actionResult = 0;
	$actionError = 'database error: ' . $ntsdb->getError();
	return;
}

$pm =& ntsPaymentManager::getInstance();
$pm->updateInvoice( $object );

$actionResult = 1;
?>
