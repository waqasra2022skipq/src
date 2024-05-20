<?php
$ntsdb =& dbWrapper::getInstance();

/* entries */
$sql =<<<EOT
SELECT
	*,
	(
	SELECT
		COUNT(*)
	FROM
		{PRFX}form_controls
	WHERE
		{PRFX}form_controls.form_id = {PRFX}forms.id
	) AS count_fields,
	(
	SELECT
		COUNT(*)
	FROM
		{PRFX}objectmeta
	WHERE
		meta_name = "_form" AND
		obj_class = "service" AND
		meta_value = {PRFX}forms.id
	) AS count_services
FROM
	{PRFX}forms
WHERE 
	class="appointment"
ORDER BY
	title ASC
EOT;

$result = $ntsdb->runQuery( $sql );
$NTS_VIEW['entries'] = array();
if( $result ){
	while( $e = $result->fetch() ){
		$NTS_VIEW['entries'][] = $e;
		}
	}
?>