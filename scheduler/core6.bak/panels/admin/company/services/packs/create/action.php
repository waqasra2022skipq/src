<?php
$ff =& ntsFormFactory::getInstance();
$aam =& ntsAccountingAssetManager::getInstance();
$formParams = array(
	'pack_type'			=> 'qty', // can be qty|duration|amount|unlimited
	'service_type'		=> 'one', // can be one|fixed
	'service_id_all'	=> 1,
	'date_type'			=> 'range', // can be range|fixed
	);
$formFile = NTS_APP_DIR . '/app/forms/pack';
$NTS_VIEW['form'] =& $ff->makeForm( $formFile, $formParams );

switch( $action )
{
	case 'save':
		$removeValidation = $aam->asset_form_remove_validation( $_NTS['REQ'] );

		if( $NTS_VIEW['form']->validate($removeValidation) )
		{
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
			if( $asset['type'] == 'unlimited' )
				$pack['asset_value'] = 1;
			else
				$pack['asset_value'] = $formValues[ $asset['type'] ];

			$cm =& ntsCommandManager::getInstance();

			$object = ntsObjectFactory::get( 'pack' );
			$object->setByArray( $pack );
			$object->setProp( 'asset', $asset );

			$cm->runCommand( $object, 'create' );

			if( $cm->isOk() )
			{
				$id = $object->getId();

				$msg = array( ntsView::objectTitle($object), M('Create'), M('OK') );
				$msg = join( ': ', $msg );
				ntsView::addAnnounce( $msg, 'ok' );

			/* continue to the list with anouncement */
				$forwardTo = ntsLink::makeLink( '-current-/../browse' );
				ntsView::redirect( $forwardTo );
				exit;
			}
			else
			{
				$errorText = $cm->printActionErrors();
				ntsView::addAnnounce( $errorText, 'error' );
			}
		}
		else
		{
		/* form not valid, continue to create form */
		}
		break;
	default:
		break;
}
?>