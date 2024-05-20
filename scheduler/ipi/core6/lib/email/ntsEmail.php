<?php
if( defined('WPINC') ){
	include_once( dirname(__FILE__) . '/ntsEmailWp.php' );
}
else {
	include_once( dirname(__FILE__) . '/ntsEmailOwn.php' );
}