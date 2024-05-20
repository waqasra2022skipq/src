<?php
$uif =& ntsUserIntegratorFactory::getInstance();
$integrator =& $uif->getIntegrator();

list( $objectInfo, $metaInfo ) = $object->getByArray( true );

$created = $object->getProp( 'created' );
if( ! $created ){
	$created = time();
	$object->setProp( 'created', $created );
	$objectInfo['created'] = $created;

	$newPassword = $objectInfo['password'];
	if( ! $newPassword ){
		$newPassword = ntsLib::generateRand( 8 );
		}
	$object->setProp( 'new_password', $newPassword );
	$objectInfo['new_password'] = $newPassword;
	}

$username = $object->getProp( 'username' );
if( ! $username ){
	if( $objectInfo['email'] )
		$objectInfo['username'] = $objectInfo['email'];
	else {
		$username = strtolower( $objectInfo['first_name'] . $objectInfo['last_name'] ) .  mt_rand(1000,9999);
		$username = ntsLib::removeAccents( $username );
		$objectInfo['username'] = $username;
		}
	}

$objectInfo = checkIfRequestFromEHR($objectInfo);

// This function call createUser() of ntsUser.php file class and create user....
$newId = $integrator->createUser( $objectInfo, $metaInfo );
if( $newId ){
	$object->setId( $newId, false );
	$skipMainTable = true;
}
else {
	$actionResult = 0;
	$actionError = $integrator->getError();
	$actionStop = true;
	return;
}

function checkIfRequestFromEHR($objectInfo) {
	if (isset($_POST['nts-source']) && $_POST['nts-source'] == 'EHR') {
		$objectInfo['source'] = 'EHR';
		$objectInfo['ehr_login_token'] = $_POST['nts-ehr_login_token'];
	}
	return $objectInfo;
}

?>