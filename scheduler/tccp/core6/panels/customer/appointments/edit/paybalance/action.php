<?php
$id = $_NTS['REQ']->getParam( '_id' );

$object = ntsObjectFactory::get( 'appointment' );
$object->setId( $id );

/* pay by balance */
$asset_id = $_NTS['REQ']->getParam( 'asset_id' );
$asset_value = $_NTS['REQ']->getParam( 'asset_value' );

$am =& ntsAccountingManager::getInstance();

$customer_id = $object->getProp('customer_id');
$customer_balance = $am->get_balance( 'customer', $customer_id );

if( isset($customer_balance[$asset_id]) && ($customer_balance[$asset_id] >= $asset_value) )
{
	$cm =& ntsCommandManager::getInstance();
	$params = array(
		'asset_id'		=> $asset_id,
		'asset_value'	=> $asset_value,
		);
	$cm->runCommand( $object, 'fund', $params );

	if( $cm->isOk() )
	{
		$msg = join( ': ',
			array(
				M('Appointment'),
				M('Pay By Balance'),
				M('OK'),
				)
			);
		ntsView::addAnnounce( $msg, 'ok' );
	}
	else
	{
		$errorText = $cm->printActionErrors();
		ntsView::addAnnounce( $errorText, 'error' );
	}
}
else
{
	$msg = join( ': ',
		array(
			M('Appointment'),
			M('Pay By Balance'),
			M('Not Sufficient'),
			)
		);
	ntsView::addAnnounce( $msg, 'error' );
}

/* redirect back to the referrer */
$forwardTo = $_SERVER['HTTP_REFERER'];
ntsView::redirect( $forwardTo );
exit;
?>