<?php
$ntsdb =& dbWrapper::getInstance();

// remove custom field
$formIds = array();

/* customer forms */
$sql =<<<EOT
	SELECT
		*
	FROM
		{PRFX}forms
	WHERE
		class = 'customer'
	LIMIT 1
EOT;
$result = $ntsdb->runQuery( $sql );
while( $formInfo = $result->fetch() ){
	$formIds[] = $formInfo['id'];
}

/* remove field */
reset( $formIds );
foreach( $formIds as $formId ){
	$sql =<<<EOT
DELETE FROM
	{PRFX}form_controls
WHERE
	name = 'last_date' AND
	form_id = $formId
LIMIT 1
EOT;
	$result = $ntsdb->runQuery( $sql );
	}

/* add field for users table */
$columns = $ntsdb->getColumnsInTable('users');
if( isset($columns['last_date']) ){
	$sql = "ALTER TABLE {PRFX}users DROP COLUMN `last_date`";
	$result = $ntsdb->runQuery( $sql );
}
