<?php
$ntsdb =& dbWrapper::getInstance();
$ff =& ntsFormFactory::getInstance();
$cm =& ntsCommandManager::getInstance();

$id = $_NTS['REQ']->getParam( '_id' );

/* super count */
$sql =<<<EOT
SELECT COUNT(*) AS count FROM {PRFX}form_controls WHERE form_id = $id
EOT;
$result = $ntsdb->runQuery( $sql );
if( $result ){
	$e = $result->fetch();
	$totalCount = $e['count'];
	}

/*
if( ! $totalCount ){
	$forwardTo = ntsLink::makeLink( '-current-/create' );
	ntsView::redirect( $forwardTo );
	exit;
	}
*/
?>