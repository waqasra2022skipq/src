<?php
$aam =& ntsAccountingAssetManager::getInstance();

$asset = $object->getProp('asset');
$asset_id = $aam->get_asset_id( $asset );
$object->setProp('asset_id', $asset_id);

$service_type = $aam->get_service_type( $asset );
/* fixed services */
switch( $service_type )
{
	case 'fixed':
		$services = explode( '-', $asset['service'] );
		$object->setProp( 'asset_value', count($services) );
		break;
}
?>