<?php
$params = array(
	'autoActivatePackage',
	);
$myDir = dirname(__FILE__);
//$getBack = TRUE;
$forwardTo = ntsLink::makeLink( '-current-/../browse' );
require( NTS_APP_DIR . '/panels/admin/conf/action_common.php' );
?>