<?php
require( dirname(__FILE__) . '/_action.php' );

$cm->runCommand( $object, 'cancel' );
$msg = M('Appointment') . ': ' . M('Cancel');
ntsView::addAnnounce( $msg, 'ok' );
ntsView::redirect( $forwardTo );
exit;
?>