<?php
switch( $inputAction ){
	case 'display':
		$value = $conf['value'];
		if( is_array($value) ){
			$value = array_shift($value);
		}
		$input .= '<INPUT TYPE="hidden" ID="' . $conf['htmlId'] . '" NAME="' . $conf['id'] . '"' . ' VALUE="' . $value . '">';
		break;

	case 'submit':
		$input = $_NTS['REQ']->getParam( $handle );
		break;

	case 'check_submit':
		$input = isset( $_POST[$handle] ) ? true : false;
		break;
	}
?>