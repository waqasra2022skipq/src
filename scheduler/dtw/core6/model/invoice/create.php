<?php
$conf =& ntsConf::getInstance();

/* init some params */
$now = time();
$createdAt = $object->getProp( 'created_at' );
if( ! $createdAt )
	$object->setProp( 'created_at', $now );

$dueAt = $object->getProp( 'due_at' );
if( ! $dueAt )
	$object->setProp( 'due_at', $now );

$object->setProp( 'currency', $conf->get('currency') );

/* generate refno */
$how = $conf->get('invoiceRef');
$ref_start_with = $conf->get('invoiceRefStartWith');
$ntsdb =& dbWrapper::getInstance();

switch( $how ){
	case 'seq':
		$max = $ntsdb->get_select( 'MAX( CAST(refno AS UNSIGNED) )', 'invoices', array('refno' => array('>', 0)) );
		if( ! $max ){
			$refNo = $ref_start_with;
		}
		else {
			$refNo = $max + 1;
		}

		$exists = $ntsdb->get_select( 'refno', 'invoices', array('refno' => array('=', $refNo)) );
		while( $exists ){
			$refNo++;
			$exists = $ntsdb->get_select( 'refno', 'invoices', array('refno' => array('=', $refNo)) );
		}
		break;

	default:
		$exists = array(1);
		while( $exists ){
			$refNoParts = array();
			$refNoParts[] = ntsLib::generateRand( 3, array('letters' => false, 'caps' => true, 'digits' => false) );
			$refNoParts[] = ntsLib::generateRand( 3, array('letters' => false, 'caps' => false, 'digits' => true) );
			$refNo = join( '-', $refNoParts );
			$exists = $ntsdb->get_select( 'refno', 'invoices', array('refno' => array('=', $refNo)) );
		}
		break;
}

$object->setProp( 'refno', $refNo );
?>