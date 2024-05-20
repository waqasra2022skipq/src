<?php
$ff =& ntsFormFactory::getInstance();
$aam =& ntsAccountingAssetManager::getInstance();
$object = ntsLib::getVar( 'admin/company/services/packs/edit::OBJECT' );

$formParams = $object->getByArray();
$asset = $aam->get_asset_by_id( $object->getProp('asset_id') );

$formParams = array_merge($formParams, $asset);
if( isset($asset['time']) )
{
	$formParams['time_all'] = 0;
	$formParams['from_time'] = $asset['time'][0];
	$formParams['to_time'] = $asset['time'][1];
}

if( isset($asset['date']) )
{
	$formParams['date_all'] = 0;
	if( isset($asset['date']['from']) )
	{
		$formParams['date_type'] = 'range';
		$formParams['from_date'] = $asset['date']['from'];
		$formParams['to_date'] = $asset['date']['to'];
	}
	else
	{
		$formParams['date_type'] = 'fixed';
		$formParams['fixed_date'] = $asset['date'];
		$formParams['weekday'] = '';
	}
}

$formParams['service_id'] = isset($asset['service']) ? $asset['service'] : array(0);
if( ! is_array($formParams['service_id']) )
{
//	$formParams['service_id'] = array( $formParams['service_id'] );
	$formParams['service_id'] = explode( '-', $formParams['service_id'] );
}
$formParams['service_type'] = $aam->get_service_type($asset);
$formParams['pack_type'] = $asset['type'];
$formParams[ $asset['type'] ] = $formParams['asset_value'];

if( $formParams['service_type'] == 'fixed' )
{
	$formParams['fixed_service_id'] = $formParams['service_id'];
}
else
{
	if( in_array(0, $formParams['service_id']) )
		$formParams['service_id_all'] = 1;
}


$formFile = NTS_APP_DIR . '/app/forms/pack';
$NTS_VIEW['form'] =& $ff->makeForm( $formFile, $formParams );

switch( $action ){
	case 'save':
		$removeValidation = $aam->asset_form_remove_validation( $_NTS['REQ'] );

		if( $NTS_VIEW['form']->validate($removeValidation) ){
			$formValues = $NTS_VIEW['form']->getValues();
			if( $formValues['notForSale'] )
				$formValues['price'] = '';
			if( isset($formValues['neverExpires']) && $formValues['neverExpires'] )
			{
				$formValues['expires_in'] = '';
			}

			$pack = array(
				'title'			=> $formValues['title'],
				'price'			=> $formValues['price'],
				'expires_in'	=> $formValues['expires_in'],
				'asset_value'	=> '',
				);
			$asset = $aam->asset_form_grab( $formValues );
			$pack['asset_value'] = isset($formValues[$asset['type']]) ? $formValues[$asset['type']] : 0;

			$cm =& ntsCommandManager::getInstance();

			$object->setByArray( $pack );
			$object->setProp( 'asset', $asset );

			$cm->runCommand( $object, 'update' );

			if( $cm->isOk() ){
				$msg = array( ntsView::objectTitle($object), M('Update'), M('OK') );
				$msg = join( ': ', $msg );
				ntsView::addAnnounce( $msg, 'ok' );

			/* continue to the list with anouncement */
				$forwardTo = ntsLink::makeLink( '-current-/../browse' );
				ntsView::redirect( $forwardTo );
				exit;
				}
			else {
				$errorText = $cm->printActionErrors();
				ntsView::addAnnounce( $errorText, 'error' );
				}
			}
		else {
		/* form not valid, continue to create form */
			}

		break;
	default:
		break;
	}
?>