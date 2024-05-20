<?php
$t = $NTS_VIEW['t'];

//$show_months = 1;
include_once( NTS_LIB_DIR . '/lib/datetime/ntsCalendar.php' );
$calendar = new ntsCalendar();

$selectedDay = $requested_cal;
list( $calYear, $calMonth, $calDay ) = ntsTime::splitDate( $selectedDay );

$t->setDateTime( $calYear, $calMonth - $show_months, 1, 0, 0, 0 );
$previousMo = $t->formatDate_Db();
$t->setDateTime( $calYear, $calMonth + $show_months, 1, 0, 0, 0 );
$nextMo = $t->formatDate_Db();

$selectedDate = $selectedDay;
list( $calYear, $calMonth, $calDay ) = ntsTime::splitDate( $selectedDay );
?>

<?php for( $k = 0; $k < $show_months; $k++ ) : ?>
	<?php
	$cssDates = array();
	$okDates = array();
	$linkedDates = array();
	$labelDates = array();
//	$changeI = $NTS_VIEW['isBundle'] ? 0 : $I;
	$changeI = 0;

	$monthMatrix = $calendar->getMonthMatrix( $calYear, $calMonth );

	foreach( $monthMatrix as $week => $days )
	{
		foreach( $days as $day )
		{
			if( $day )
			{
				$thisDate = ntsTime::formatDateParam( $calYear, $calMonth, $day );
				$ok = ( in_array($thisDate, $dates) ) ? true : false;
				$class = array();

				if( $ok )
				{
//					$class[] = 'alert-default-o';
					$class[] = 'btn-default';
					$linkedDates[] = $thisDate;
					$linkDates[$thisDate] = ntsLink::makeLink('-current-', '', array('cal' => $thisDate) );
				}
				else
				{
					$class[] = 'alert-archive';
				}
				$cssDates[ $thisDate ] = $class;
			}
		}
	}
	$linkDates[$previousMo] = ntsLink::makeLink('-current-', '', array('cal' => $previousMo));
	$linkDates[$nextMo] = ntsLink::makeLink('-current-', '', array('cal' => $nextMo));

	if( $show_months > 1 )
	{
		if( $k == 0 )
		{
			$skipPrevLink = FALSE;
			$skipNextLink = TRUE;
		}
		elseif( $k == ($show_months - 1) )
		{
			$skipPrevLink = TRUE;
			$skipNextLink = FALSE;
		}
		else
		{
			$skipPrevLink = TRUE;
			$skipNextLink = TRUE;
		}
	}

/* get promotions for dates */
	$datesWithPromotions = array();
	foreach( $dates as $this_date ){
		$r = $full_r;
		$r['date'] = $this_date;
		$this_promotions = $ntspm->getPromotions($r);
		if( $this_promotions ){
			$datesWithPromotions[$this_date] = 1;
		}
	}
	foreach( array_keys($datesWithPromotions) as $this_date ){
		$dayAddons[$this_date] = 
			'<span class="text-info" style="position: absolute; right: 0px; top: 0px; opacity: 0.8;">' . 
			HC_Html::icon('gift') .
			'</span>'
			;
	}

	$okDates = $linkedDates;
	require( NTS_APP_DIR . '/helpers/calendar2.php' );
	$currentCalendar = array();
	?>

	<?php
	$calMonth++;
	if( $calMonth > 12 ){
		$calMonth = 1;
		$calYear++;
		}
	?>
<?php endfor; ?>