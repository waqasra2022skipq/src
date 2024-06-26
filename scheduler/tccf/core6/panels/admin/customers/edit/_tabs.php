<?php
$object = ntsLib::getVar( 'admin/customers/edit::OBJECT' );
$customerId = $object->getId();

$ntsConf = ntsConf::getInstance();
$canEditLogin = TRUE;
$current_user =& ntsLib::getCurrentUser();
$admin_level = $current_user->getProp('_admin_level');
$staffCanEditCustomerLogin = $ntsConf->get('staffCanEditCustomerLogin');
if( ($admin_level != 'admin') && (! $staffCanEditCustomerLogin) ){
	$canEditLogin = FALSE;
}

$tabs = array();

$tabs['edit'] = array(
	'title'	=> '<i class="fa fa-edit"></i> ' . M('Edit'),
	);

$restrictions = $object->getProp( '_restriction' );
$status_actions = array();

if( $canEditLogin ){
	if( $restrictions ){
		$status_actions[] = array(
			'title'	=> ntsUser::_statusLabel(array(), '', 'i') . ' ' . M('Activate'),
			'href'	=> ntsLink::makeLink('-current-', 'activate'),
			);
	}
	else {
		$status_actions[] = array(
			'title'	=> ntsUser::_statusLabel(array('suspended'), '', 'i') . ' ' . M('Suspend'),
			'href'	=> ntsLink::makeLink('-current-', 'suspend'),
			);
	}
}

if( $status_actions ){
	$tabs['edit'] = array(
		$status_actions,
		'title'		=> $object->statusLabel('', 'i') . ' ' . $object->statusText(),
		'panel'		=> 'edit',
		);
}
else {
	$tabs['edit'] = array(
		'title'		=> $object->statusLabel('', 'i') . ' ' . $object->statusText(),
		);
}

$tm2 = ntsLib::getVar( 'admin::tm2' );
$where = array(
	'customer_id'	=> array( '=', $customerId ),
	'completed'		=> array( '>=', 0 ),
	);

/* addonWhere */
$locs = ntsLib::getVar( 'admin::locs' );
$ress = ntsLib::getVar( 'admin::ress' );
$sers = ntsLib::getVar( 'admin::sers' );
$addonWhere = array(
	'location_id'	=> array( 'IN', $locs ),
	'resource_id'	=> array( 'IN', $ress ),
	'service_id'	=> array( 'IN', $sers ),
	);
reset( $addonWhere );
foreach( $addonWhere as $k => $v ){
	if( (! isset($where[$k])) && (! isset($where['id'])) )
		$where[$k] = $v;
	}
$totalCount = $tm2->countAppointments( $where );
$tabs['appointments'] = array(
	'title'	=> '<i class="fa fa-check-square-o"></i> ' . M('Appointments') . ' [' . $totalCount . ']',
	);

$resCount = ntsObjectFactory::count( 'resource' );
$serCount = ntsObjectFactory::count( 'service' );
$locCount = ntsObjectFactory::count( 'location' );

$am =& ntsAccountingManager::getInstance();
$pack_count = ntsObjectFactory::count( 'pack' );
if( $pack_count OR $am->get_postings('customer', $customerId) )
{
	$tabs['accounting'] = array(
		'title'	=> '<i class="fa fa-suitcase"></i> ' . M('Balance'),
		);
}

$pm =& ntsPaymentManager::getInstance();
$ids = $pm->getInvoicesOfCustomer( $customerId );
if( 1 OR $ids )
{
	$tabs['payments'] = array(
		'title'	=> '<i class="fa fa-file-text-o"></i> ' . M('Invoices') . ' [' . count($ids) . ']',
		'panel'	=> 'payments/browse',
		);
}


$has_price = FALSE;
$all_services = ntsObjectFactory::getAll( 'service' );
reset( $all_services );
foreach( $all_services as $s ){
	$service_price = $s->getProp('price');
	if( strlen($service_price) && ($service_price > 0) ){
		$has_price = TRUE;
		break;
	}
}
if( $has_price ){
	$ids = $pm->getPromotionsOfCustomer( $customerId );
	$tabs['promotions'] = array(
		'title'	=> '<i class="fa fa-gift"></i> ' . M('Promotions') . ' [' . count($ids) . ']',
		'panel'	=> 'promotions/browse',
		);
}

if( ($resCount > 1) OR ($serCount > 1) OR ($locCount > 1) )
{
	$tabs['assign'] = array(
		'title'	=> '<i class="fa fa-link"></i> ' . M('Defaults'),
		);
}

$ntsConf =& ntsConf::getInstance();
$attachEnableCompany = $ntsConf->get('attachEnableCompany');
if( $attachEnableCompany )
{
	$atm = new ntsAttachManager;
	$attachments = $atm->get( $object->getClassName(), $object->getId() );
	$tabs['attachments'] = array(
		'title'	=> '<i class="fa fa-file-o"></i> ' . M('Attachments') . ' [' . count($attachments) . ']',
		);
}

$email = $object->getProp('email');
if( $email )
{
	$tabs['email'] = array(
		'title'	=> '<i class="fa fa-envelope"></i> ' . M('Email'),
		);
}

$tabs['password'] = array(
	'title'	=> '<i class="fa fa-key"></i> ' . M('Login'),
	);

$uif =& ntsUserIntegratorFactory::getInstance();
$integrator =& $uif->getIntegrator();
$where = array();
$where['_role'] = array( '=', 'customer' );
$customers_count = $integrator->countUsers( $where );
if( $customers_count > 1 )
{
	$tabs['merge'] = array(
		'title'	=> '<i class="fa fa-copy"></i> ' . M('Merge'),
		);
}

$tabs['admin'] = array(
	'title'	=> '<i class="fa fa-user"></i> ' . M('Role'),
	);

$tabs['delete'] = array(
	'title'	=> '<i class="fa fa-times text-danger"></i> ' . M('Delete'),
	'alert'	=> 1,
	);
?>