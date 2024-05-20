<?php
global $NTS_VIEW;
$viewMode = $NTS_VIEW[NTS_PARAM_VIEW_MODE];
if( $viewMode == 'print' ){
	return;
}

$locs = ntsLib::getVar( 'admin::locs' );
$ress = ntsLib::getVar( 'admin::ress' );
$sers = ntsLib::getVar( 'admin::sers' );

$locs2 = ntsLib::getVar( 'admin::locs2' );
$ress2 = ntsLib::getVar( 'admin::ress2' );
$sers2 = ntsLib::getVar( 'admin::sers2' );

$locs_all = ntsLib::getVar( 'admin::locs_all' );
$ress_all = ntsLib::getVar( 'admin::ress_all' );
$sers_all = ntsLib::getVar( 'admin::sers_all' );

/* check out archived resources */
$ress_archive = ntsLib::getVar( 'admin::ress_archive' );
if( $ress_archive )
{
	$ress_all = array_diff( $ress_all, $ress_archive );
	$ress_all = array_values( $ress_all );
}

/* check out archived locations */
$locs_archive = ntsLib::getVar( 'admin::locs_archive' );
if( $locs_archive )
{
	$locs_all = array_diff( $locs_all, $locs_archive );
	$locs_all = array_values( $locs_all );
}
?>
<?php require( dirname(__FILE__) . '/_export.php' ); ?>
