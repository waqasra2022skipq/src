<?php
if( isset($conf) && is_array($conf) ){
	$conf['attr']['size'] = 8;
}
?>
<?php
switch( $inputAction ){
	case 'display':
		$htmlId = $conf['htmlId'];
		$hiddenHtmlId = $htmlId . '_' . 2;
		$currentValue = $conf['value'];

		$input .= '<input type="hidden" NAME="' . $conf['id'] . '" ID="' . $hiddenHtmlId . '" VALUE="' . $currentValue . '">';
		$t = new ntsTime;

		if( $currentValue ){
			$t->setDateDb( $currentValue );
			$currentDisplay = $t->formatDate();

			list( $year, $month, $day ) = ntsTime::splitDate( $currentValue );
			$month = ltrim($month, 0);
			$month = $month - 1;
			$day = ltrim($day, 0);
		}
		else {
			$currentDisplay = M('N/A');
		}

		$input .= '<a class="btn btn-default" href="#" ID="' . $htmlId . '">';
		$input .= $currentDisplay;
		$input .= '</a>';

		$dateFormat = NTS_DATE_FORMAT;
		$input .=<<<EOT

<script language="javascript">
jQuery("#$htmlId").glDatePicker({
	onChange: function(target, newDate){
		jQuery("#$hiddenHtmlId").val( newDate.format('Ymd') );
		target.html( newDate.format('$dateFormat') );
		},
EOT;

		if( $currentValue ){
			$input .=<<<EOT

	startDate: new Date( $year, $month, $day ),
	selectedDate: new Date( $year, $month, $day ),

EOT;
		}

		$input .=<<<EOT

	});
</script>

EOT;

		break;

	default:
		require( NTS_LIB_DIR . '/lib/form/inputs/hidden.php' );
		break;
	}
?>