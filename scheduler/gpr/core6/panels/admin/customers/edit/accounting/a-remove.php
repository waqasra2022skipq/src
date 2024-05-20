<?php
$object = ntsLib::getVar( 'admin/customers/edit::OBJECT' );
$am =& ntsAccountingManager::getInstance();

$post = $_NTS['REQ']->getPostParams();
$balance_id = $post['balance_id'];
$asset_expires = 0;

$total_asset_value = 0;
$rex_balance_id = 0;
$balance = $am->get_balance( 'customer', $object->getId() );
foreach( $balance as $asset_key => $asset_value ){
	$rex_balance_id++;
	if( $rex_balance_id == $balance_id ){
		$total_asset_value = $asset_value;
		list( $asset_id, $asset_expires ) = explode( '-', $asset_key );
		break;
	}
}

$ff =& ntsFormFactory::getInstance();
$formFile = dirname( __FILE__ ) . '/remove_form';
$formParams = array(
	'asset_id'			=> $asset_id,
	'balance_id'		=> $balance_id,
	'total_asset_value'	=> $total_asset_value,
	// 'asset_value'	=> $asset_value,
	// 'total_asset_value'	=> $asset_value,
	);
$this_form = $ff->makeForm( $formFile, $formParams, 'balance_' . $balance_id );

if( $this_form->validate() ){
	$form_values = $this_form->getValues();
	$asset_value = isset($form_values['asset_value']) ? $form_values['asset_value'] : 1;

	$am->add(
		'customer::remove_balance',
		$object,
		array(
			'asset_id'		=> $asset_id,
			'asset_value'	=> $asset_value,
			'asset_expires'	=> $asset_expires,
			)
		);

	/* continue to customer edit */
	ntsView::addAnnounce( M('Remove Balance') . ': ' . M('OK'), 'ok' );

	$forwardTo = ntsLink::makeLink( 'admin/customers/edit/accounting', '', array('_id' => $object->getId()) );
	ntsView::redirect( $forwardTo );
	exit;
}
else {
	$expand = array( $balance_id );
	require( dirname(__FILE__) . '/a.php' );
}
?>