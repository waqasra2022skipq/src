<?php
include_once( dirname(__FILE__) . '/lib/ntsSmsTemplateManager.php' );

$om =& objectMapper::getInstance();
$om->registerProp( 'user',	'mobile_phone',		false,	0,	'' );

global $NTS_MENU;
$NTS_MENU['admin/sms']				= M('SMS');
$NTS_MENU['admin/sms/settings']		= M('Settings');
$NTS_MENU['admin/sms/templates']	= M('Templates');
$NTS_MENU['admin/sms/logs']			= M('Logs');
$NTS_MENU['admin/sms/send']			= M('Send');
?>