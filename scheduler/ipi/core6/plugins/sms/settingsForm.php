<?php
$plugin = 'sms';
$new = $_NTS['REQ']->getParam( 'new' );

$gateway = $plm->getPluginSetting( $plugin, 'gateway' );
$suppliedGateway = $_NTS['REQ']->getParam( 'gateway' );

if( $suppliedGateway && ($suppliedGateway != $gateway) )
	$gateway = $suppliedGateway;

$this->setValue( 'gateway', $gateway );

// available gateways
$dir = dirname(__FILE__) . '/gateways';
$folders = ntsLib::listSubfolders( $dir );

$gatewaysOptions = array();
$gatewaysOptions[] = array( "", M('Select') );
reset( $folders );
foreach( $folders as $f ){
	$gatewaysOptions[] = array( $f, $f );
	}
?>

<table>
<tr>
	<th>SMS Gateway</th>
	<TD>
	<?php
	echo $this->makeInput (
	/* type */
		'select',
	/* attributes */
		array(
			'id'		=> 'gateway',
			'options'	=> $gatewaysOptions,
			'attr'		=> array (
				'onChange'	=> "document.location.href='" . ntsLink::makeLink('-current-', '', array('plugin' => $plugin, 'new' => $new) ) . "&nts-gateway=' + this.value",
				),
			)
		);
	?>
	</TD>
</TR>
</TABLE>

<?php if( $gateway ) : ?>
	<h3><?php echo ucfirst($gateway); ?> Gateway Settings</h3>
	<?php
	$formFile = dirname(__FILE__) . '/gateways/' . $gateway . '/form.php';
	require( $formFile );
	?>

<h3>Misc Settings</h3>

<?php
echo ntsForm::wrapInput(
	'Automatically Convert Numbers',
	array(
		'<ul class="list-unstyled">',
			'<li>',
				'<ul class="list-inline list-separated">',
					'<li>',
						$this->buildInput (
						/* type */
							'radio',
						/* attributes */
							array(
								'id'	=> 'convert',
								'value'	=> '',
								)
							),
					'</li>',
					'<li>',
						'None',
					'</li>',
				'</ul>',
			'</li>',

			'<li>',
				'<ul class="list-inline list-separated">',
					'<li>',
						$this->buildInput (
						/* type */
							'radio',
						/* attributes */
							array(
								'id'	=> 'convert',
								'value'	=> 'us',
								)
							),
					'</li>',
					'<li>',
						'USA',
						'<br>',
						'<em>Add <strong>+1</strong> before every 10 digit number</em>',
					'</li>',
				'</ul>',
			'</li>',

			'<li>',
				'<ul class="list-inline list-separated">',
					'<li>',
						$this->buildInput (
						/* type */
							'radio',
						/* attributes */
							array(
								'id'	=> 'convert',
								'value'	=> 'aus',
								)
							),
					'</li>',
					'<li>',
						'Australia',
						'<br>',
						'<em><strong>0410 123 456</strong> becomes <strong>+61 410 123 456</strong></em>',
					'</li>',
				'</ul>',
			'</li>',
		'</ul>',
		)
	);
?>


<?php
echo ntsForm::wrapInput(
	'Disable Log',
	$this->buildInput (
	/* type */
		'checkbox',
	/* attributes */
		array(
			'id'	=> 'nolog',
			)
		)
	);
?>

<?php
echo ntsForm::wrapInput(
	'SMS Test Mode',
	$this->buildInput (
	/* type */
		'checkbox',
	/* attributes */
		array(
			'id'	=> 'debug',
			'help'	=> "If set, SMS messages will be printed on screen rather than sent"
			)
		)
	);
?>

<?php
echo ntsForm::wrapInput(
	'Disable SMS',
	$this->buildInput (
	/* type */
		'checkbox',
	/* attributes */
		array(
			'id'	=> 'disabled',
			)
		)
	);
?>

<?php else : ?>
	<?php $skipSubmit = true; ?>
<?php endif; ?>
