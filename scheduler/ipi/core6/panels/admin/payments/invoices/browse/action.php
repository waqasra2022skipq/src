<?php
$ntsdb =& dbWrapper::getInstance();

$customerId = ntsLib::getVar( 'admin/payments/invoices::customer' );
$where = ntsLib::getVar( 'admin/payments/invoices::where' );

if( $customerId )
{
	$pm =& ntsPaymentManager::getInstance();
	$ids = $pm->getInvoicesOfCustomer( $customerId );
	if( $ids )
	{
		$where['id'] = array('IN', $ids);
	}
	else
	{
		$where['id'] = array('=', 0);
	}
}

$ff =& ntsFormFactory::getInstance();
$searchFormParams = array();
if( $search = $_NTS['REQ']->getParam('search') )
{
	$searchFormParams['search'] = $search;
}
$NTS_VIEW['search'] = $search;
$formFile = dirname( __FILE__ ) . '/searchForm';
$NTS_VIEW['searchForm'] =& $ff->makeForm( $formFile, $searchFormParams );
if( $search )
{
	$where['refno'] = array( 'LIKE', '%' . $search . '%' );
}

if( ! isset($where['id']) )
{
	$showPerPage = 10;
	$currentPage = $_NTS['REQ']->getParam('p');
	if( ! $currentPage )
		$currentPage = 1;
	$limit = ( ($currentPage - 1) * $showPerPage ) . ',' . $showPerPage;
}
else
{
	$limit = '';
	$showPerPage = 'all';
	$currentPage = 1;
}

// remove, too slow
//$where['exists'] = array( '', '(' . 'SELECT id FROM {PRFX}invoice_items WHERE {PRFX}invoice_items.invoice_id = {PRFX}invoices.id' . ')', TRUE );

$addOn = '';
$addOn .= 'ORDER BY due_at DESC';
if( $limit )
	$addOn .= " LIMIT $limit";

$ids = $ntsdb->get_select( 
	'id',
	'invoices',
	$where,
	$addOn
	);

$entries = array();
ntsObjectFactory::preload( 'invoice', $ids );
reset( $ids );
foreach( $ids as $id )
{
	$e = ntsObjectFactory::get( 'invoice' );
	$e->setId( $id );
	$entries[] = $e;
}

$totalCount = $ntsdb->count( 'invoices', $where );
if( $totalCount > 0 )
{
	if( $showPerPage == 'all' )
	{
		$showFrom = 1;
		$showTo = $totalCount;
	}
	else
	{
		$showFrom = 1 + ($currentPage - 1) * $showPerPage;
		$showTo = $showFrom + $showPerPage - 1;
		if( $showTo > $totalCount )
			$showTo = $totalCount;
	}
}
else
{
	$showFrom = 0;
	$showTo = 0;
}

ntsLib::setVar( 'admin/payments/invoices::search', $search );
ntsLib::setVar( 'admin/payments/invoices::entries', $entries );
ntsLib::setVar( 'admin/payments/invoices::currentPage', $currentPage );
ntsLib::setVar( 'admin/payments/invoices::showFrom', $showFrom );
ntsLib::setVar( 'admin/payments/invoices::showTo', $showTo );
ntsLib::setVar( 'admin/payments/invoices::totalCount', $totalCount );
ntsLib::setVar( 'admin/payments/invoices::showPerPage', $showPerPage );
?>