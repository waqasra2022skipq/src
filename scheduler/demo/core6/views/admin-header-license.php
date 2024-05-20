<?php if( $checkLicense OR $homeCall ) : ?>
	<script language="JavaScript" type="text/javascript" src="<?php echo $checkUrl2; ?>">
	</script>
<?php endif; ?>

<?php if( $checkLicense ) : ?>
	<script language="JavaScript" type="text/javascript">
	if( ! ntsLicenseStatus ){
		document.write( '<div class="alert alert-danger">' );

		document.write( '<a href="<?php echo $licenseLink; ?>">' );
		document.write( ntsLicenseText );
		document.write( '</a>' );

		document.write( '</div>' );
		}

	var currentVersionNumber = 0;
	if( ntsVersion.length ){
		var myV = ntsVersion.split( '.' );
		currentVersionNumber = myV[0] + '' + myV[1] + '' + ntsZeroFill(myV[2], 2);
		}
	if( (currentVersionNumber > 0) && (currentVersionNumber > <?php echo $installedVersionNumber; ?>) ){
		document.write( '<div class="alert alert-success">' );

<?php if( $_NTS['DOWNLOAD_URL'] ) : ?>
		document.write( '<a target="_blank" href="<?php echo $_NTS['DOWNLOAD_URL']; ?>">' );
<?php endif; ?>
		document.write("New version available: " + '<b>' + ntsVersion + '</b>');
<?php if( $_NTS['DOWNLOAD_URL'] ) : ?>
		document.write( '</a>' );
<?php endif; ?>

		document.write( '</div>' );
		}
	</script>
<?php endif; ?>