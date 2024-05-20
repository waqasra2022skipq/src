<?php
$keep = array(
	'pack',
	);

reset( $keep );
foreach( $keep as $k )
{
	$params[$k] = $_NTS['REQ']->getParam($k);
}
ntsView::setPersistentParams($params, 'customer/packs' );
?>