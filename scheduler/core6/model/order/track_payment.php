<?php
$object->reset_accounting_postings();
$amount = $object->getPaidAmount();

if( $amount < 0 ){
	$commandParams = array(
		'reason' => 'Refund',
		);
//	$this->runCommand( $object, 'cancel', $commandParams );
	}
elseif( $amount > 0 ){
	$this->runCommand( $object, 'request', array('amount' => $amount) );
	}
?>