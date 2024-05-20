<?php
/* --- RETURN IF EMAIL DISABLED --- */
$conf =& ntsConf::getInstance();
if( $conf->get('emailDisabled') )
	return;

$userLang = $customer->getLanguage();
if( ! $userLang )
	$userLang = $defaultLanguage;

/* --- GET TEMPLATE --- */
$key = 'order-' . $mainActionName . '-admin';

/* --- SKIP IF THIS NOTIFICATION DISABLED --- */
$currentlyDisabled = $conf->get( 'disabledNotifications' );
if( in_array($key, $currentlyDisabled) ){
	return;
	}

$templateInfo = $etm->getTemplate( $userLang, $key );

/* --- SKIP IF NO TEMPLATE --- */
if( ! $templateInfo )
{
	return;
}

/* --- FIND PROVIDERS --- */
$notify_admins = array();
$resourceId = $object->getProp( 'resource_id' );

if( $resourceId )
{
	$resource = ntsObjectFactory::get( 'resource' );
	$resource->setId( $resourceId );

	list( $appsAdmins, $scheduleAdmins ) = $resource->getAdmins();
	reset( $appsAdmins );
	foreach( $appsAdmins as $admId => $access )
	{
		if( $access['notified'] )
		{
			$notify_admins[ $admId ] = 1;
		}
	}
}
else
{
	$allResources = ntsObjectFactory::getAll( 'resource' );
	reset( $allResources );
	foreach( $allResources as $resource )
	{
		list( $appsAdmins, $scheduleAdmins ) = $resource->getAdmins();
		reset( $appsAdmins );
		foreach( $appsAdmins as $admId => $access )
		{
			if( $access['notified'] )
			{
				$notify_admins[ $admId ] = 1;
			}
		}
	}
}

/* check if "filter-customers" plugin is on */
$plgm =& ntsPluginManager::getInstance();
if( $plgm->isActive('filter-customers') )
{
	$this_customer_id = $object->getProp( 'customer_id' );
	/* filter customers */
	$current_admin_ids = array_keys( $notify_admins );
	reset( $current_admin_ids );
	foreach( $current_admin_ids as $admId )
	{
		$admin_customers = ntsPluginFilterCustumers_AllowCustomers( $admId );
		if( ! in_array($this_customer_id, $admin_customers) )
		{
			unset( $notify_admins[$admId] );
		}
	}
}

$providers = array();
reset( $notify_admins );
foreach( $notify_admins as $admId => $ttt )
{
	$provider = new ntsUser;
	$provider->setId( $admId );
	$providers[] = $provider;
}

if( ! $providers )
{
	return;
}

/* --- PREPARE MESSAGE --- */
/* build tags */
$tags = array();

$orderTitle = $object->getFullTitle();
$tags[0][] = '{ORDER.TITLE}';
$tags[1][] = $orderTitle;

/* customer fields */
$om =& objectMapper::getInstance();
$fields = $om->getFields( 'customer', 'external' );
$allCustomerInfo = '';
foreach( $fields as $f ){
	$value = $customer->getProp( $f[0] );
	if( $f[2] == 'checkbox' ){
		$value = $value ? M('Yes') : M('No');
		}

	$tags[0][] = '{ORDER.CUSTOMER.' . strtoupper($f[0]) . '}';
	$tags[1][] = $value;

	$allCustomerInfo .= M($f[1]) . ': ' . $value . "\n";
	}
$tags[0][] = '{ORDER.CUSTOMER.-ALL-}';
$tags[1][] = $allCustomerInfo;

/* replace tags */
$subject = str_replace( $tags[0], $tags[1], $templateInfo['subject'] );
$body = str_replace( $tags[0], $tags[1], $templateInfo['body'] );

/* --- SEND EMAIL --- */
reset( $providers );
foreach( $providers as $provider ){
	$this->runCommand( $provider, 'email', array('body' => $body, 'subject' => $subject) );
	}
?>