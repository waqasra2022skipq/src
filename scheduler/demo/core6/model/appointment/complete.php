<?php
$alreadyCompleted = $object->getProp( 'completed' );

if ( $alreadyCompleted ) {
	if ($alreadyCompleted == 4) {
		$object->setProp( 'completed', 1 );
		$this->runCommand( $object, 'update' );
		$actionResult = 1;
	} else {
		$actionResult = 0;
		$actionError = M('Appointment') . ' (id=' . $object->getId() .  '): ' . M('Already Completed');
		$actionStop = true;
		return;
	}
} else {
	$object->setProp( 'completed', 1 );
	$this->runCommand( $object, 'update' );
	$actionResult = 1;
}
?>