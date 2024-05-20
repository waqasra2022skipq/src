<?php
$object = ntsLib::getVar( 'admin/customers/edit::OBJECT' );
$objId = $object->getId();
ntsView::setBack( ntsLink::makeLink('admin/customers/edit/promotions', '', array('_id' => $objId)) );

ntsLib::setVar( 'admin/company/services/promotions::customer', $object );

// $iCanEdit = TRUE;
// ntsLib::setVar( 'admin/notes::iCanEdit', $iCanEdit );


$promotion_id = $_NTS['REQ']->getParam( 'promotion_id' );
if( $promotion_id ){
	ntsView::setPersistentParams( array('promotion_id' => $promotion_id), 'admin/customers/edit/promotions/edit' );

	$promotion = ntsObjectFactory::get( 'promotion' );
	$promotion->setId( $promotion_id );
	ntsLib::setVar( 'admin/company/services/promotions/edit::OBJECT', $promotion );
}

$alias = 'admin/company/services/promotions';
?>