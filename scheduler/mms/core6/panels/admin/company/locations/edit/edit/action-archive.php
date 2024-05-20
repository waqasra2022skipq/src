<?php
$cm =& ntsCommandManager::getInstance();
$object = ntsLib::getVar( 'admin/company/locations/edit::OBJECT' );

$value = $object->getProp('archive');
$value = $value ? 0 : 1;
$object->setProp('archive', $value );

$cm->runCommand( $object, 'update' );
if( $cm->isOk() )
{
	ntsView::setAnnounce( join( ': ', array(ntsView::objectTitle($object), M('Update'), M('OK')) ), 'ok' );
}
else
{
	$errorText = $cm->printActionErrors();
	ntsView::addAnnounce( $errorText, 'error' );
}
/* continue to the list with anouncement */
$forwardTo = ntsLink::makeLink( '-current-/../../browse' );
ntsView::redirect( $forwardTo );
exit;
?>