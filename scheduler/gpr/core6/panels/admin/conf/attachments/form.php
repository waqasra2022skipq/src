<?php
$am = new ntsAttachManager;
$error = $am->get_error();
?>
<p>
<?php echo M('Uploads Directory'); ?>: <strong><?php echo $am->dir; ?></strong>
</p>

<?php if( $error ) : ?>
	<p class="text-danger">
		<?php echo $error; ?>
	</p>
<?php else : ?>
	<p class="text-success">
		<?php echo M('OK'); ?>
	</p>
<?php endif; ?>

<?php
echo ntsForm::wrapInput(
	M('Enable Company Side Attachments'),
	$this->buildInput (
	/* type */
		'checkbox',
	/* attributes */
		array(
			'id'	=> 'attachEnableCompany',
			)
		)
	);
?>

<?php
$options = array( 50, 100, 200, 500, 1024, 2048, 4*1024, 8*1024, 16*1024, 32*1024 );
$server_limit = ntsLib::returnBytes( ini_get('upload_max_filesize') );

$select_options = array();
reset( $options );
foreach( $options as $o )
{
	$o = $o * 1024;
	if( $o > $server_limit )
		break;
	$select_options[] = array( $o, ntsLib::humanFilesize($o, 0) );
}
echo ntsForm::wrapInput(
	M('Max Size'),
	$this->buildInput (
	/* type */
		'select',
	/* attributes */
		array(
			'id'		=> 'attachMaxSize',
			'options'	=> $select_options
			)
		)
	);
?>

<?php
$options = array( 'gif', 'jpg', 'png', 'doc', 'docx', 'pdf' );
$allowed_options = array();
reset( $options );
foreach( $options as $o )
{
	$allowed_options[] = array( $o, $o );
}

echo ntsForm::wrapInput(
	M('Allowed Types'),
	$this->buildInput (
	/* type */
		'checkboxSet',
	/* attributes */
		array(
			'id'		=> 'attachAllowed',
			'options'	=> $allowed_options
			),
	/* validators */
		array(
			array(
				'code'		=> 'notEmpty.php', 
				'error'		=> M('Required'),
				),
			)
		)
	);
?>


<?php echo $this->makePostParams('-current-', 'update'); ?>
<?php
echo ntsForm::wrapInput(
	'',
	'<input class="btn btn-default" type="submit" value="' . M('Save') . '">'
	);
?>