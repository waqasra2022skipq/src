<?php
$app = ntsLib::getAppProduct();

if( isset($_REQUEST['nts-integrate-url']) )
{
	$from = $_REQUEST['nts-integrate-url'];
	$from = ntsLib::restoreUrl( $from );

	$GLOBALS['NTS_CONFIG'][$app]['BASE_URL'] = $from;
	$GLOBALS['NTS_CONFIG'][$app]['INDEX_PAGE'] = '';
}
elseif( isset($_REQUEST['nts-integrate-file']) )
{
	$from = $_REQUEST['nts-integrate-file'];
	$from = ntsLib::restoreUrl( $from );

	$GLOBALS['NTS_CONFIG'][$app]['FRONTEND_WEBPAGE'] = $from;
}

global $NTS_VIEW;
$NTS_VIEW['isInside'] = 1;
$NTS_VIEW['called_remotely'] = 1;

ob_start();
require( dirname(__FILE__) . '/controller.php' );

if( ntsLib::isAjax() )
{
	$out['content'] = ob_get_contents();
	ob_end_clean();
}
else
{
	$head = NULL;
	$content = NULL;
	$is_theme = (isset($NTS_VIEW['isTheme']) && $NTS_VIEW['isTheme']) ? 1 : 0;

	if( $is_theme ){
		ob_start();
		require( dirname(__FILE__) . '/views/theme.php' );
		$full_content = ob_get_contents();
		ob_end_clean();

		$pos1 = strpos( $full_content, '<head' );
		if( $pos1 !== FALSE ){
			$pos2 = strpos( $full_content, '>', $pos1 );
			$pos3 = strpos( $full_content, '</head>', $pos2 );
			$head = substr( $full_content, $pos2 + 1, ($pos3 - $pos2) - 1 );
		}

		$pos1 = strpos( $full_content, '<body' );
		if( $pos1 !== FALSE ){
			$pos2 = strpos( $full_content, '>', $pos1 );
			$pos3 = strpos( $full_content, '</body>', $pos2 );
			$content = substr( $full_content, $pos2 + 1, ($pos3 - $pos2) - 1 );
		}
	}

	if( $head === NULL ){
		ob_start();
		require( dirname(__FILE__) . '/views/head-content.php' );
		$head = ob_get_contents();
		ob_end_clean();
	}

	if( $content === NULL ){
		ob_start();
		require( dirname(__FILE__) . '/views/normal-content.php' );
		$content = ob_get_contents();
		ob_end_clean();
	}

	$out['head'] = $head;
	$out['content'] = $content;
}

$out = json_encode( $out );
echo $out;
?>