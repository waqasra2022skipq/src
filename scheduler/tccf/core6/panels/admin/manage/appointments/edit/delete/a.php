<?php
$object = ntsLib::getVar( 'admin/manage/appointments/edit::OBJECT' );

$ff =& ntsFormFactory::getInstance();
$form_file = dirname( __FILE__ ) . '/form';
$form =& $ff->makeForm( $form_file );

$view = array(
	'form'	=> $form,
	);

$this->render(
	dirname(__FILE__) . '/index.php',
	$view
	);
