<?php
$object = ntsLib::getVar( 'admin/manage/appointments/edit::OBJECT' );

$cost = $object->getCost();
$due_amount = $object->getDue();
$back = - $due_amount;

$params = array(
	'back'			=> $back,
	'created_at'	=> time(),
	);

$cm =& ntsCommandManager::getInstance();
$cm->runCommand( $object, 'refund', $params );

if( $cm->isOk() )
{
	$msg = join( ': ',
		array(
			M('Appointment'),
			M('Refund'),
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

$forwardTo = ntsLink::makeLink( '-current-' );
ntsView::redirect( $forwardTo );
exit;
?>