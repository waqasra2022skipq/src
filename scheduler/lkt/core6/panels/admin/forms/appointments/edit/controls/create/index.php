<?php
$id = $_NTS['REQ']->getParam( '_id' );

$ff =& ntsFormFactory::getInstance();
$formParams = array(
	'form_id'	=> $id,
	);

$formFile = dirname( __FILE__ ) . '/form';
$form =& $ff->makeForm( $formFile, $formParams );
$form->display();
?>