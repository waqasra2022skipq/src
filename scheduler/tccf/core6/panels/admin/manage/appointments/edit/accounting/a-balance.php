<?php
$object = ntsLib::getVar( 'admin/manage/appointments/edit::OBJECT' );

/* pay by balance */
$asset_id = $_NTS['REQ']->getParam( 'asset_id' );
$asset_value = $_NTS['REQ']->getParam( 'asset_value' );

$am =& ntsAccountingManager::getInstance();

$customer_id = $object->getProp('customer_id');
$customer_balance = $am->get_balance( 'customer', $customer_id );

if( isset($customer_balance[$asset_id]) && ($customer_balance[$asset_id] >= $asset_value) )
{
	$params = array(
		'asset_id'		=> $asset_id,
		'asset_value'	=> $asset_value,
		);
	$cm =& ntsCommandManager::getInstance();
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

$forwardTo = ntsLink::makeLink( '-current-' );
ntsView::redirect( $forwardTo );
exit;
?>