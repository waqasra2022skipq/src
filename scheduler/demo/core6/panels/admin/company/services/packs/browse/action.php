<?php
$rawEntries = ntsObjectFactory::getAll( 'pack', 'ORDER BY show_order ASC' );
ntsLib::setVar( 'admin/company/services/packs::entries', $rawEntries );
?>