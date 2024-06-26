<meta name="viewport" content="width=device-width, initial-scale=1.0" />
<?php
$ri = ntsLib::remoteIntegration();
if( $ri == 'wordpress' ){
	$app = HC_Lib::app();

	$full_path = realpath( dirname(__FILE__) . '/..' );
	$web_dir = plugins_url('', $full_path);
	$happ_web_dir = plugins_url('core6', $full_path);
}
else {
	$web_dir = defined('NTS_ROOT_WEBDIR') ? NTS_ROOT_WEBDIR : ntsLib::webDirName( ntsLib::getFrontendWebpage() );
	if( defined('NTS_DEVELOPMENT') && NTS_DEVELOPMENT ){
		$happ_web_dir = 'http://localhost/wp/wp-content/plugins/hitappoint-legacy/core6/';
	}
	else {
		$happ_web_dir = $web_dir . '/core6';
	}
}

require( dirname(__FILE__) . '/../assets/happ_files.php' );
require( dirname(__FILE__) . '/../assets/files.php' );

$prfx = array('http://', 'https://', '//');
?>
<?php foreach( $css_files as $f ) : ?>
	<?php
	$file = is_array($f) ? $f[0] : $f;
	$full = FALSE;
	reset( $prfx );
	foreach( $prfx as $prf )
	{
		if( substr($file, 0, strlen($prf)) == $prf )
		{
			$full = TRUE;
			break;
		}
	}
	if( $full )
		$full_file = $f;
	else
		$full_file = (substr($file, 0, strlen('happ/')) == 'happ/') ? $happ_web_dir . '/' . $file : $web_dir . '/' . $file;

	$full_file = str_replace( 'https://', '//', $full_file );
	$full_file = str_replace( 'http://', '//', $full_file );
	?>
	<?php if( is_array($f) ) : ?>
		<!--[if <?php echo $f[1]; ?>]>
		<link rel="stylesheet" type="text/css" href="<?php echo $full_file; ?>" />
		<![endif]-->
	<?php else : ?>
		<link rel="stylesheet" type="text/css" href="<?php echo $full_file; ?>" />
	<?php endif; ?>
<?php endforeach; ?>

<?php foreach( $js_files as $f ) : ?>
	<?php
	$file = is_array($f) ? $f[0] : $f;
	$full = FALSE;
	reset( $prfx );
	foreach( $prfx as $prf )
	{
		if( substr($file, 0, strlen($prf)) == $prf )
		{
			$full = TRUE;
			break;
		}
	}
	if( $full )
		$full_file = $f;
	else
		$full_file = (substr($file, 0, strlen('happ/')) == 'happ/') ? $happ_web_dir . '/' . $file : $web_dir . '/' . $file;

	$full_file = str_replace( 'https://', '//', $full_file );
	$full_file = str_replace( 'http://', '//', $full_file );
	?>
	<?php if( is_array($f) ) : ?>
		<!--[if <?php echo $f[1]; ?>]>
		<script language="JavaScript" type="text/javascript" src="<?php echo $full_file; ?>"></script>
		<![endif]-->
	<?php else : ?>
		<script language="JavaScript" type="text/javascript" src="<?php echo $full_file; ?>"></script>
	<?php endif; ?>
<?php endforeach; ?>
