<?php
$conf =& ntsConf::getInstance();
$commonHeader = $conf->get('emailCommonHeader');
$commonFooter = $conf->get('emailCommonFooter');

$customer_email = $this->getValue( 'to' );
$refno = $this->getValue( 'refno' );
$sendLink = $this->getValue( 'sendLink' );
$sendLink = '<a href="' . $sendLink . '">' . $sendLink . '</a>';

$text = M('Invoice') . ' ' . $refno;
$text .= "\n" . $sendLink;
?>
<?php
echo ntsForm::wrapInput(
	M('To'),
	$customer_email
	);
?>

<?php
echo ntsForm::wrapInput(
	M('Subject'),
	$this->buildInput (
	/* type */
		'text',
	/* attributes */
		array(
			'id'		=> 'subject',
			'attr'		=> array(
				'size'	=> 48,
				),
			'required'	=> 1,
			'default'	=> M('Invoice') . ' ' . $refno,
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

<?php
echo ntsForm::wrapInput(
	M('Message'),
	$this->buildInput (
	/* type */
		'textarea',
	/* attributes */
		array(
			'id'		=> 'body',
			'attr'		=> array(
				'cols'	=> 56,
				'rows'	=> 16,
				),
			'required'	=> 1,
			'default'	=> $text,
			'before'	=> '<span class="help-block">' . $commonHeader . '</span>',
			'after'		=> '<span class="help-block">' . nl2br($commonFooter) . '</span>',
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

<?php echo $this->makePostParams('-current-', 'send', array('display' => 'send') ); ?>
<?php
echo ntsForm::wrapInput(
	'',
	'<INPUT class="btn btn-default" TYPE="submit" VALUE="' . M('Send') . '">'
	);
?>
