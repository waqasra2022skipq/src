<?php
$params = array(
	'autoResource',
	);
$myDir = dirname(__FILE__);
//$getBack = TRUE;
$forwardTo = ntsLink::makeLink( '-current-/../browse' );
$forwardTo = ntsLink::makeLink( '-current-' );
require( NTS_APP_DIR . '/panels/admin/conf/action_common.php' );
?>