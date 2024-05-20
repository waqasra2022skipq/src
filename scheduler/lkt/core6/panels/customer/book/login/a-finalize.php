<?php
$customer_id = $object->getId();

/* save it in session */
$session = new ntsSession;
$apps = $session->userdata('apps');

for( $ii = 0; $ii < count($apps); $ii++ )
{
	$apps[$ii]['customer_id'] = $customer_id;

	if( isset($formValues) ){
		reset( $formValues );
		foreach( $formValues as $k => $v ){
			// if( substr($k, 0, strlen('custom_')) == 'custom_' ){
				$apps[$ii][$k] = $v;
			// }
		}
	}
}
$session->set_userdata( 'apps', $apps );

require( dirname(__FILE__) . '/../confirm/a-finalize.php' );
?>