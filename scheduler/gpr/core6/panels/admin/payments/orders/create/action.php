<?php
$ff =& ntsFormFactory::getInstance();
$formFile = dirname( __FILE__ ) . '/form';

$fParams = array();

$t = $NTS_VIEW['t'];

$fixCustomer = ntsLib::getVar( 'admin/payments/orders/create::fixCustomer' );
if( $fixCustomer ){
	$fParams['customer_id'] = $fixCustomer;
	}
else {
	$cid = $_NTS['REQ']->getParam( 'customer_id' );
	$fParams['customer_id'] = $cid ? $cid : 0;
	}

$fixPack = ntsLib::getVar( 'admin/payments/orders/create::fixPack' );
if( $fixPack ){
	$fParams['pack_id'] = $fixPack;
	}
else {
	$pid = $_NTS['REQ']->getParam( 'pack_id' );
	$fParams['pack_id'] = $pid ? $pid : 0;
	}

if( $fParams['pack_id'] ){
	$pack = ntsObjectFactory::get( 'pack' );
	$pack->setId( $fParams['pack_id'] );
	$packPrice = $pack->getTotalPrice();

	$fParams['amount'] = $packPrice ? $packPrice : '';
	}

$cm =& ntsCommandManager::getInstance();
$pm =& ntsPaymentManager::getInstance();
$NTS_VIEW['form'] =& $ff->makeForm( $formFile, $fParams );

switch( $action ){
	case 'create':
		if( $NTS_VIEW['form']->validate() ){
			$formValues = $NTS_VIEW['form']->getValues();

			$customerId = $formValues['customer_id'];
			$packId = $formValues['pack_id'];
			$pack = ntsObjectFactory::get( 'pack' );
			$pack->setId( $packId );

			$order = ntsObjectFactory::get( 'order' );
			$order->setProp( 'customer_id', $customerId );
			$order->setProp( 'pack_id', $packId );

			$cm->runCommand( $order, 'create' );
			$orderId = $order->getId();

			$cm->runCommand( $order, 'request' );

		/* forward to create appointment for this customer */
//			$forwardTo = ntsLink::makeLink( 'admin/customers/edit/create_appointment', '', array('_id' => $customerId, 'service_id' => $pack->getProp('service_id'))
			ntsView::getBack( true, true );
			exit;
			}
		else {
			/* form not valid, get back */
			}
		break;
	}
?>