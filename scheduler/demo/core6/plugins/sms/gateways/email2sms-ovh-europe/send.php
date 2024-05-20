<?php
include_once( NTS_BASE_DIR . '/lib/email/ntsEmail.php' );

/* receives $msg, $to */
/* returns $success, $response */

/* see http://guides.ovh.com/EmailToSms */

$ovhsmsnick = $plm->getPluginSetting( $plugin, 'ovhsmsnick' );
$user = $plm->getPluginSetting( $plugin, 'username' );
$password = $plm->getPluginSetting( $plugin, 'password' );
$from = $plm->getPluginSetting( $plugin, 'from' );

/* add plus sign to $to */
if( substr($to, 0, 1) != '+' )
{
	$to = '+' . $to;
}

$subject = "$ovhsmsnick:$user:$password:$to:$from";

$mailer = new ntsEmail;
$mailer->setSubject( $subject );
$mailer->isHtml = FALSE;
$mailer->setBody( $msg );
$mailer->sendToOne('email2sms@ovh.net');

$success = 1;
$response = "Sent email to email2sms@ovh.net";
?>