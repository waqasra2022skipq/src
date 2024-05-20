<p>
	<strong>Latest version</strong>:
<?php
$myUrl = ntsLink::makeLinkFull( ntsLib::getFrontendWebpage() );
// strip started http:// as apache seems to have troubles with it
$myUrl = preg_replace( '/https?\:\/\//', '', $myUrl );

$checkUrl2 = ntsLib::checkLicenseUrl();
//echo $checkUrl2 . '<br>';
$installedVersionNumber = ntsLib::parseVersion( $currentVersion );
?>
<script language="JavaScript" type="text/javascript" src="<?php echo $checkUrl2; ?>">
</script>
<script language="JavaScript" type="text/javascript">
var currentVersionNumber = 0;
if( ntsVersion.length )
{
	var myV = ntsVersion.split( '.' );
	var currentVersion = myV[0] + '' + myV[1] + '' + ntsZeroFill(myV[2], 2);

	var currentVersionNumber = parseInt(currentVersion);
//	currentVersionNumber = currentVersionNumber + (<?php echo $appInfo['modify_version']; ?>);

	currentVersion = String(currentVersionNumber);
	currentVersion = ntsZeroFill(currentVersion, 4);

	ntsVersion = currentVersion.substring(0,1) + '.' + currentVersion.substring(1,2);
	var v3 = currentVersion.substring(2,4);
	v3 = parseInt(v3);
	v3 = String(v3);
	ntsVersion = ntsVersion + '.' + v3;

	document.write(ntsVersion);
}
</script>

<script language="JavaScript" type="text/javascript">
if( (currentVersionNumber > 1000) && (currentVersionNumber > <?php echo $dgtFileVersion; ?>) )
{
	<?php if( $_NTS['DOWNLOAD_URL'] ) : ?>
		document.write( '<a target="_blank" href="<?php echo $_NTS['DOWNLOAD_URL']; ?>">' );
	<?php endif; ?>
	document.write( "<?php echo M('Please Upgrade'); ?>" );
	<?php if( $_NTS['DOWNLOAD_URL'] ) : ?>
		document.write( '</a>' );
	<?php endif; ?>
}
</script>
</p>
