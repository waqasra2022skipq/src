<?php
$item = $params['item'];

if( ! isset($item['taxable']) )
	$item['taxable'] = 1;
$item['title'] = trim($item['title']);
if( strlen($item['title']) )
{
	$item['obj_class'] = '';
	$item['obj_id'] = 0;
}

$props = array( 'amount', 'qty', 'title', 'obj_class', 'obj_id', 'taxable' );
reset( $props );

$error = FALSE;
foreach( $props as $p )
{
	if( ! isset($item[$p]) )
	{
		$actionResult = 0;
		$actionError = "'$p' not set in invoice item!";
		$actionStop = true;
		return;
	}
}

$my_keys = array_keys( $item );
foreach( $my_keys as $k )
{
	if( ! in_array($k, $props) )
		unset($item[$k]);
}

$item['invoice_id'] = $object->getId();

$ntsdb =& dbWrapper::getInstance();
$new_item_id = $ntsdb->insert(
	'invoice_items',
	$item
	);

if( ! $new_item_id )
{
	$actionResult = 0;
	$actionError = 'database error: ' . $ntsdb->getError();
	$actionStop = true;
	return;
}

$pm =& ntsPaymentManager::getInstance();
$pm->updateInvoice( $object );

$actionResult = 1;
?>
