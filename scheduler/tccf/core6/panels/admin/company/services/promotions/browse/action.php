<?php
$entries = ntsObjectFactory::getAll( 'promotion' );
if( ntsLib::hasVar( 'admin/company/services/promotions::customer') ){
	$customer = ntsLib::getVar( 'admin/company/services/promotions::customer' );

	$final_entries = array();
	foreach( $entries as $e ){
		$rule = $e->getRule();
		if( isset($rule['customer']) && in_array($customer->getId(), $rule['customer']) ){
			$final_entries[] = $e;
		}
	}
	$entries = $final_entries;
}

ntsLib::setVar( 'admin/company/services/promotions::entries', $entries );
?>