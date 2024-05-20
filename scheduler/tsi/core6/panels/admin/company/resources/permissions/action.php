<?php
$entries = array();

$ntsdb =& dbWrapper::getInstance();
$ids = $ntsdb->get_select_flat( 
	array('id'),
	'resources',
	array(),
	'ORDER BY archive ASC, show_order ASC, title ASC'
	);

//$entries = ntsObjectFactory::getAll( 'resource', 'ORDER BY show_order ASC, title ASC' );

$ff =& ntsFormFactory::getInstance();
$formParams = array();

foreach( $ids as $id ){
	$obj = ntsObjectFactory::get('resource');
	$obj->setId( $id );
	$entries[] = $obj;

	$formParams['order_' . $obj->getId()] = $obj->getProp('show_order');
}

ntsLib::setVar( 'admin/company/resources/permissions::entries', $entries );
?>