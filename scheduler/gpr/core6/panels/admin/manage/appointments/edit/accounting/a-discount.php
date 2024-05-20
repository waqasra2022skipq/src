<?php
$object = ntsLib::getVar( 'admin/manage/appointments/edit::OBJECT' );

/* add payment */
$ff =& ntsFormFactory::getInstance();
$discount_form_file = dirname(__FILE__) . '/form-discount';
$form_params = array(
	);
$discount_form =& $ff->makeForm( $discount_form_file );

if( $discount_form->validate() )
{
	$form_values = $discount_form->getValues();
	$discount = $form_values['discount'];
	$params = array(
		'discount'		=> $discount,
		'created_at'	=> time(),
		);

	$cm =& ntsCommandManager::getInstance();
	$cm->runCommand( $object, 'discount', $params );

	if( $cm->isOk() ){
		}
	else {
		$errorText = $cm->printActionErrors();
		ntsView::addAnnounce( $errorText, 'error' );
		}

	$forwardTo = ntsLink::makeLink( '-current-' );
	ntsView::redirect( $forwardTo );
	exit;
}
else
{
	require( dirname(__FILE__) . '/a.php' );
}
?>