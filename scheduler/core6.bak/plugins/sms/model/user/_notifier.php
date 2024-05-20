<?php
if( isset($params['_silent']) && $params['_silent'] )
	return;

$conf =& ntsConf::getInstance();
$enableRegistration = $conf->get('enableRegistration');

if( ! $enableRegistration )
{
	if( $mainActionName == 'require_approval' )
		return;
}

if( ! class_exists('ntsSmsTemplateManager') )
	include_once( dirname(__FILE__) . '/../../lib/ntsSmsTemplateManager.php' );

$stm =& ntsSmsTemplateManager::getInstance();
$om =& objectMapper::getInstance();

$lm =& ntsLanguageManager::getInstance();
$defaultLanguage = $lm->getDefaultLanguage();

$plm =& ntsPluginManager::getInstance();

$plugin = 'sms';

/* --- RETURN IF SMS DISABLED --- */
$smsDisabled = $plm->getPluginSetting($plugin, 'disabled');
if( $smsDisabled )
	return;

require( dirname(__FILE__) . '/_notifier_customer.php' );
?>