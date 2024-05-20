<?php
$uif =& ntsUserIntegratorFactory::getInstance();
$integrator =& $uif->getIntegrator();

$users = $integrator->getAdmins();
ntsLib::setVar( 'admin/company/staff/permissions::users', $users );
?>