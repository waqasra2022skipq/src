<?php
$ntsdb =& dbWrapper::getInstance();

$uif =& ntsUserIntegratorFactory::getInstance();
$integrator =& $uif->getIntegrator();

$users = $integrator->getAdmins();

ntsLib::setVar( 'admin/company/staff::entries', $users );

?>