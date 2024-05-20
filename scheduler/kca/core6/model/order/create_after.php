<?php
$ntspm =& ntsPaymentManager::getInstance();
$coupon = isset($params['coupon']) ? $params['coupon'] : '';
/* now check if we can apply promotions  */
$promotions = $ntspm->getPromotions( $object, $coupon );
foreach( $promotions as $pro ){
	$this->runCommand( 
		$pro,
		'apply',
		array(
			'order'		=> $object,
			'coupon'	=> $coupon,
			)
		);
}

/* check if we need to create invoice */
$price = $pack->getProp('price');
if( $price || (isset($params['forceInvoice']) && $params['forceInvoice']) )
{
	$forceAmount = (isset($params['forceInvoice']) && $params['forceInvoice']) ? $params['forceInvoice'] : 0;
	if( $coupon ){
		$forceAmount = $ntspm->getPrice( $object, $coupon );
	}

	if( $forceAmount )
	{
		// remove tax
		$forceAmount = $pack->getSubTotal( $forceAmount );
	}

	$pm =& ntsPaymentManager::getInstance();
	$invoice = $pm->makeInvoices( array($object), $forceAmount );
}
?>