<?php
$cm =& ntsCommandManager::getInstance();
$ntsdb =& dbWrapper::getInstance();

/* CUSTOMER - create field for last date  */
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

/* add field */
reset( $formIds );
foreach( $formIds as $formId ){
	$sql =<<<EOT
SELECT
	id
FROM
	{PRFX}form_controls
WHERE
	name = 'last_date' AND
	form_id = $formId
LIMIT 1
EOT;
	$result = $ntsdb->runQuery( $sql );
	$fieldInfo = $result->fetch();

	if( ! $fieldInfo ){
		/* field */
		$field = ntsObjectFactory::get( 'form_control' );
		$fieldValues = array(
			'name'			=> 'last_date',
			'title'			=> 'Last Date For Appointment',
			'ext_access'	=> 'read',
			'type'			=> 'date/Calendar',
			);

		$field->setByArray( $fieldValues );
		$field->setProp( 'form_id', $formId );
		$cm->runCommand( $field, 'create' );
		}
	}

/* add field for users table */
$columns = $ntsdb->getColumnsInTable('users');
if( ! isset($columns['last_date']) ){
	$sql = "ALTER TABLE {PRFX}users ADD COLUMN `last_date` int(11) NULL";
	$result = $ntsdb->runQuery( $sql );
}