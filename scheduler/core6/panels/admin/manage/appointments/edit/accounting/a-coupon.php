<?php
$object = ntsLib::getVar( 'admin/manage/appointments/edit::OBJECT' );

$ntspm =& ntsPaymentManager::getInstance();
$cm =& ntsCommandManager::getInstance();

$coupon = $_NTS['REQ']->getParam('coupon');

/* now check if we can apply promotions  */
$promotions = $ntspm->getPromotions( $object, $coupon );

if( $promotions ){
	foreach( $promotions as $pro ){
		$cm->runCommand( 
			$pro,
			'apply',
			array(
				'appointment'	=> $object,
				'coupon'		=> $coupon,
				)
			);
	}

	if( $cm->isOk() ){
		}
	else {
		$errorText = $cm->printActionErrors();
		$errorText = 'There is a problem with the coupon code';
		ntsView::addAnnounce( $errorText, 'error' );
	}
}
elseif( $coupon ){
	$errorText = 'No promotions found with this coupon code';
	ntsView::addAnnounce( $errorText, 'error' );
}

$forwardTo = ntsLink::makeLink( '-current-' );
ntsView::redirect( $forwardTo );
exit;
