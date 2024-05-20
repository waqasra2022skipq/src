<?php
$params = array(
	'attachEnableCompany',
	'attachMaxSize',
	'attachAllowed'
	);
$myDir = dirname(__FILE__);

$am = new ntsAttachManager;
$error = $am->get_error();
if( $error )
{
	$ntsConf = ntsConf::getInstance();
	$ff =& ntsFormFactory::getInstance();
	$formFile = $myDir . '/form';

	$default = array();
	reset( $params );
	foreach( $params as $p ){
		$default[ $p ] = $ntsConf->get( $p );
		}
	$NTS_VIEW['form'] =& $ff->makeForm( $formFile, $default ); 
}
else
{
	require( dirname(__FILE__) . '/../action_common.php' );
}
?>