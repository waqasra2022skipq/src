<?php
$ntsdb =& dbWrapper::getInstance();
$locationId = $object->getId();

/* delete meta as child */
$childMetaClass = '_' . strtolower($className);
$result = $ntsdb->delete( 
	'objectmeta',
	array( 
		'meta_name'		=> array('=', '_assign_location_only'),
		'meta_value'	=> array('=', $locationId),
		)
	);

$t = new ntsTime();
$today = $t->formatDate_Db();
$todayTimestamp = $t->timestampFromDbDate( $today );

/* delete timeblocks */
$sql =<<<EOT
DELETE FROM
	{PRFX}timeblocks
WHERE
	location_id = $locationId
EOT;
$result = $ntsdb->runQuery( $sql );

/* reject appointments */
$result = $ntsdb->select(
	'id',
	'appointments',
	array(
		'location_id' => array( '=', $locationId ),
		)
	);

if( $result ){
	while( $e = $result->fetch() ){
		$subId = $e['id'];
		$subObject = ntsObjectFactory::get( 'appointment' );
		$subObject->setId( $subId );

		$params = array(
			'reason' => 'Location closed',
			);
		/* silent if app is earlier than today */
		if( $subObject->getProp('starts_at') < $todayTimestamp ){
			$params['_silent'] = true;
			}
		$this->runCommand( $subObject, 'reject', $params );
		}
	}
?>