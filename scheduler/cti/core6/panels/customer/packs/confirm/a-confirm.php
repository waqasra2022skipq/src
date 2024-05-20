<?php
global $NTS_CURRENT_USER;
$customer_id = $NTS_CURRENT_USER->getId();
require( dirname(__FILE__) . '/a-finalize.php' );
?>