<?php
$ntsdb =& dbWrapper::getInstance();
$om =& objectMapper::getInstance();

/* supplied username and password */
if( NTS_EMAIL_AS_USERNAME )
	$suppliedUsername = $object->getProp( 'email' );
else
	$suppliedUsername = $object->getProp( 'username' );
$suppliedPassword = $object->getProp( 'password' ); 

$ehr_login_token = '';
if ($object->getProp( 'ehr_login_token' ) != '') {
	$ehr_login_token = $object->getProp( 'ehr_login_token' );
}

if( strlen($suppliedUsername) < 1 && !$ehr_login_token){
	$actionResult = 0;
	$actionError = M("Wrong username or password1");
	}
else {
	$uif =& ntsUserIntegratorFactory::getInstance();
	$integrator =& $uif->getIntegrator();

	if ($ehr_login_token) {
		$ids = getUserByLoginToken($ehr_login_token);
		$userInfo = $integrator->getUserByEmail( $ids[0] );
		$object->setId( $userInfo['id'] );
	} elseif ($integrator->checkPassword($suppliedUsername, $suppliedPassword)) {
		$actionResult = 1;

		if( NTS_EMAIL_AS_USERNAME )
			$userInfo = $integrator->getUserByEmail( $suppliedUsername );
		else
			$userInfo = $integrator->getUserByUsername( $suppliedUsername );
		$object->setId( $userInfo['id'] );
		}
	else {
		$actionResult = 0;
		$actionError = M("Wrong username or password");
		}
	}

	function getUserByLoginToken($loginToken) {
		$sql =<<<EOT
		SELECT * FROM {PRFX}users WHERE ehr_login_token = '$loginToken'
EOT;
		$mainDb =& dbWrapper::getInstance();
		$result = $mainDb->runQuery( $sql );
		if ($result) {
			while ($u = $result->fetch()) {
				$ids[] = $u['email'];
			}
		}
		return $ids;
	}

?>