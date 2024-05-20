<?php
$session = new ntsSession;

require( dirname(__FILE__) . '/../_a_init_pack.php' );

$current_user_id = ntsLib::getCurrentUserId();
if( ! $current_user_id ){
	$forwardTo = ntsLink::makeLink('anon/login');
	ntsView::redirect( $forwardTo );
	exit;
}

$coupon = $session->userdata( 'coupon' );

$ff =& ntsFormFactory::getInstance();
$formFile = dirname(__FILE__) . '/form-coupon';
$formParams = array(
	'coupon'	=> $coupon,
	);
$NTS_VIEW['form_coupon'] =& $ff->makeForm( $formFile, $formParams );

$ntspm =& ntsPaymentManager::getInstance();

$show_coupon = FALSE;
$coupon_valid = FALSE;
$r = array(
	'pack_id'		=> $pack->getId(),
	'customer_id'	=> $current_user_id,
	);
$coupon_promotions = array();
if( $coupon ){
	$show_coupon = TRUE;

	$coupon_valid = TRUE;
	/* check if valid */
	$coupon_promotions = $ntspm->getPromotions( $r, $coupon );
	if( ! $coupon_promotions ){
		$coupon_valid = FALSE;
		$NTS_VIEW['form_coupon']->errors['coupon'] = M('Not Valid');
	}
}
else {
	/* check if we have promotions applied for this pack */
	$coupon_promotions = $ntspm->getPromotions( $r, '', TRUE );
	if( $coupon_promotions ){
		$show_coupon = TRUE;
	}
}

$view = array(
	'pack'			=> $pack,
	'coupon'		=> $coupon,
	'show_coupon'	=> $show_coupon,
	'coupon_valid'	=> $coupon_valid,
	'coupon_promotions'	=> $coupon_promotions,
	);
$this->render( 
	dirname(__FILE__) . '/index.php',
	$view
	);	
?>