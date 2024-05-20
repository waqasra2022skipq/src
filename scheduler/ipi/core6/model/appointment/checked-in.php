<?php
$alreadyCheckedIn = $object->getProp( 'completed' );

if ( $alreadyCheckedIn ) {
	$actionResult = 0;
	$actionError = M('Appointment') . ' (id=' . $object->getId() .  ') : ' . M('Checked In');
	$actionStop = true;
	return;
} else {
	$object->setProp( 'completed', 4 );
	$this->runCommand( $object, 'update' );
	$actionResult = 1;
	}
?>