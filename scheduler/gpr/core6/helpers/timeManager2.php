<?php
class haTimeManager2 {
	public $completedFreeSlot = TRUE;

	public $_cache = array();
	public $_lrs = array();
	public $useCache = FALSE;
	public $dayMode = FALSE;
	public $blockMode = FALSE;
	public $conf = array();

	public $companyT = null;
	public $customerT = null;
	public $tempT = null;

	public $resourceIds = array();
	public $resourceSet = FALSE;
	public $locationIds = array();
	public $serviceIds = array();
	public $maxDuration = 0;
	public $_saveMaxDuration = 0;
	public $maxLeadin = 0;
	public $maxLeadOut = 0;

	public $services = array();
	public $locations = array();
	public $virtualIndex = 0;
	public $chunkSize = 1;

	public $checkNow = 0;

	public $customerSide = false;
	public $customerId = 0;
	public $timesIndex = array();

	public $slot_plugins = array();
	public $slot_errors = array();
	public $plugins_data = array();

	public $isBundle = false;
	public $bundleGap = 0;
	public $processCompleted = FALSE;	

	public $minBlockStart = 0;
	public $maxBlockEnd = 0;
	public $filters = array();
	public $internalResourceIds = array();
	public $dryRun = FALSE;
	public $appsOnly = FALSE;

	public $apps = array();
	public $timeoffs = array();
	public $timeblocks = array();
	public $slots = array();
	public $skip_id = array();

	public $init_start = 3019682800; // some distant future
	public $init_end = 0;
	public $infinity = 3019682800; // some distant future 
	public $global_limit = array();

	function __construct(){
		$this->max_duration = 24 * 60 * 60;
		$this->useCache = FALSE;
		$this->minDuration = 0;
		$this->maxDuration = 0;
		$this->_saveMaxDuration = 0;
		$this->maxLeadin = 0;
		$this->maxLeadOut = 0;

		$t = new ntsTime;
		$this->companyT = $t;
		$this->customerT = $t;

		$this->tempT = new ntsTime;

		$this->customerSide = false;
		$this->isBundle = false;
		$this->resourceSet = false;

		$this->SLT_INDX = array(
			'location_id'	=> 0,
			'resource_id'	=> 1,
			'service_id'	=> 2,
			'duration'		=> 3,
			'max_seats'		=> 4,
			);

		$this->chunkSize = 10;

		$this->allServiceIds = array();
		$services = ntsObjectFactory::getAll( 'service' );
		reset( $services );
		foreach( $services as $s ){
			$serviceId = $s->getId();
			$this->services[ $serviceId ] = $s->getByArray();

			$thisDuration = 
				$this->services[ $serviceId ]['duration'] + 
				$this->services[ $serviceId ]['lead_out'] +
				$this->services[ $serviceId ]['duration_break'] + 
				$this->services[ $serviceId ]['duration2']
				;

			if( $thisDuration > $this->maxDuration )
				$this->maxDuration = $thisDuration;
			if( (! $this->minDuration) OR ($thisDuration < $this->minDuration) )
				$this->minDuration = $thisDuration;

			$thisLeadin = $this->services[ $serviceId ]['lead_in'];
			if( $thisLeadin > $this->maxLeadin )
				$this->maxLeadin = $thisLeadin;

			$thisLeadOut = $this->services[ $serviceId ]['lead_out'];
			if( $thisLeadOut > $this->maxLeadOut )
				$this->maxLeadOut = $thisLeadOut;

		/* if second part exists */
			if( $this->services[ $serviceId ]['duration2'] ){
				$addon_serviceId = $serviceId . '_2';
				$this->services[ $addon_serviceId ] = $this->services[ $serviceId ];

				$this->services[ $serviceId ]['lead_out'] = 0;
				$this->services[ $addon_serviceId ]['lead_in'] = 0;
				$this->services[ $addon_serviceId ]['duration'] = $this->services[ $serviceId ]['duration2'];
			}

			$this->allServiceIds[] = $serviceId;
		}

		if( $this->maxDuration > $this->max_duration ){
			$this->max_duration = $this->maxDuration;
		}

		$maxTravel = 0;
		$locations = ntsObjectFactory::getAll( 'location' );
		reset( $locations );
		foreach( $locations as $l ){
			$locationId = $l->getId();
			$this->locations[ $locationId ] = $l->getByArray();

			$travel = $l->getProp('_travel');
			$thisMaxTravel = array_values($travel) ? max(array_values($travel)) : 0;
			if( $thisMaxTravel > $maxTravel ){
				$maxTravel = $thisMaxTravel;
			}
		}

		$this->maxDuration = $this->maxDuration + $maxTravel;
		$this->maxLeadin = $this->maxLeadin + $maxTravel;

		$this->allLocationIds = ntsObjectFactory::getAllIds( 'location' );
		$this->allResourceIds = ntsObjectFactory::getAllIds( 'resource' );

		$ntsdb =& dbWrapper::getInstance();

	/* get internal resources ids */
		$this->internalResourceIds = array();
		$where = array(
			'obj_class'		=> array('=', 'resource'),
			'meta_name'		=> array('=', '_internal'),
			'meta_value'	=> array( '<>', 0 )
			);
		$result = $ntsdb->select( 'obj_id', 'objectmeta', $where );
		while( $i = $result->fetch() ){
			$this->internalResourceIds[] = $i['obj_id'];
		}

		$this->checkNow = time();

	/* min/max block start/end */
		$this->minBlockStart = 0;
		$this->maxBlockEnd = 24 * 60 * 60;

		$sql =<<<EOT
		SELECT
			MIN(starts_at) AS min, MAX(ends_at) AS max, MAX(starts_at) AS maxstart
		FROM
			{PRFX}timeblocks
EOT;
		$result = $ntsdb->runQuery( $sql );
		if( $result && ($minmax = $result->fetch()) ){
			if( $minmax['min'] )
				$this->minBlockStart = $minmax['min'];
			
			$max1 = $minmax['max'];
			$max2 = $minmax['maxstart'] + $this->maxDuration;
			$this->maxBlockEnd = max( $max1, $max2 );
		}

		$ntsConf =& ntsConf::getInstance();
		$this->conf['minFromNowTomorrow'] = $ntsConf->get('minFromNowTomorrow');
		$this->conf['allowOverlapCustomer'] = $ntsConf->get('allowOverlapCustomer');
		$this->conf['allowSameAppCustomer'] = 0;

	/* load plugins if any */
		$plm =& ntsPluginManager::getInstance();
		$activePlugins = $plm->getActivePlugins();
		$this->plugins = array();
		reset( $activePlugins );
		foreach( $activePlugins as $plg ){
			$checkFile = $plm->getPluginFolder( $plg ) . '/checkSlot.php';
			if( file_exists($checkFile) )
				$this->slot_plugins[] = $checkFile;
		}
	}

	function getDatesWithSomething( $startDate, $howManyDates, $backward = 0 )
	{
		$ntsdb =& dbWrapper::getInstance();

		$return = array();
		$okDate = $startDate;

		$mainWhere = array();
		$mainWhere['location_id'] = array( 'IN', $this->locationIds );
		$mainWhere['resource_id'] = array( 'IN', $this->resourceIds ); 
		$mainWhere['service_id'] = array( 'IN', $this->serviceIds ); 
		if( $this->processCompleted )
		{
			$mainWhere['completed'] = array( '<>', HA_STATUS_CANCELLED );
			$mainWhere['completed '] = array( '<>', HA_STATUS_NOSHOW );
		}

		$this->companyT->setDateDb( $startDate );
		if( $backward )
		{
			$this->companyT->modify( '+1 day' );
		}
		else
		{
			$this->companyT->modify( '-1 day' );
		}
		$okDate = $this->companyT->formatDate_Db();

	// check with appointments
		while( $okDate )
		{
//			$return[] = $okDate;

		// ok full
			if( count($return) >= $howManyDates )
			{
				break;
			}

			$this->companyT->setDateDb( $okDate );
			$startTime = $this->companyT->getTimestamp();
			if( $backward )
				$this->companyT->modify( '-1 day' );
			else
				$this->companyT->modify( '+1 day' );
			$check_next_day = $this->companyT->formatDate_Db();

			$this->companyT->setDateDb( $okDate );
			$endTime = $this->companyT->getEndDay();

		// get next date to check
			$nextDate = '';

		// 1 - get nearest appointment which end is greater than the end of this day
			$nextDate1 = '';
			$where = $mainWhere;
			if( $backward )
			{
				$where['starts_at - lead_in'] = array('<', $startTime);
				$nextApp = $this->getAppointments( 
					$where,
					'ORDER BY (starts_at-lead_in) DESC',
					array(0,1),
					array('starts_at', 'lead_in')
					);
			}
			else
			{
				$where['starts_at + duration + lead_out + duration_break + duration2'] = array('>', $endTime);
				$nextApp = $this->getAppointments( 
					$where,
					'ORDER BY (starts_at-lead_in) ASC',
					array(0,1),
					array('starts_at', 'lead_in')
					);
			}

			if( $nextApp )
			{
				$nextApp = array_shift( $nextApp );
				$ts = $nextApp['starts_at'] - $nextApp['lead_in'];
				if( $backward )
				{
					if( $ts >= $startTime )
						$ts = $startTime - 1;
				}
				else
				{
					if( $ts <= $endTime )
						$ts = $endTime + 1;
				}
				$this->companyT->setTimestamp( $ts );
				$nextDate1 = $this->companyT->formatDate_Db();
			}

			$nextDate2 = '';
		// 2 - get nearest blocks
			if( $nextDate1 && ($nextDate1 == $check_next_day) )
			{
				$nextDate = $nextDate1;
			}
			else
			{
				$nextDate2 = '';
				$blocksWhere = array();
				if( $this->locationIds )
				{
					if( $blocksWhere )
						$blocksWhere[] = 'AND';
					$blocksWhere[] = array(
						array( 'location_id' => array( 'IN', $this->locationIds) ),
						array( 'location_id' => array( '=', 0 ) ),
						);
				}

				if( $this->resourceIds )
				{
					if( $blocksWhere )
						$blocksWhere[] = 'AND';
					$blocksWhere[] = array(
						array( 'resource_id' => array( 'IN', $this->resourceIds) ),
						array( 'resource_id' => array( '=', 0 ) ),
						);
				}

				if( $this->serviceIds )
				{
					if( $blocksWhere )
						$blocksWhere[] = 'AND';
					$blocksWhere[] = array(
						array( 'service_id' => array( 'IN', $this->serviceIds) ),
						array( 'service_id' => array( '=', 0 ) ),
						);
				}

				$where = $blocksWhere;
				if( $where )
					$where[] = 'AND';
				$where[] = array( 'valid_to' => array('>', $okDate) );

			/* first check if we have future blocks at all */
				if( $backward )
				{
					$result = $ntsdb->select( 'MAX(valid_from) AS max_valid_from, MIN(valid_to) AS min_valid_to', 'timeblocks', $where );
					$e = $result->fetch();
					if( $e && $e['max_valid_from'] )
					{
						if( $e['max_valid_from'] < $okDate )
							$checkFrom = $e['max_valid_from'];
						else {
							$checkFrom = $check_next_day;
							}
						$checkTo = $e['min_valid_to'];

						while( $checkFrom )
						{
							$this->companyT->setDateDb( $checkFrom );
							$checkFromWeekday = $this->companyT->getWeekday();

							$where = $blocksWhere;
							if( $where )
								$where[] = 'AND';
							$where[] = array( 'valid_from' => array('<=', $checkFrom) );
							$where[] = 'AND';
							$where[] = array( 'applied_on' => array('=', $checkFromWeekday) );

							/* ok, now find for exact date */
							$result2 = $ntsdb->select( 'MAX(valid_from) AS max_valid_from', 'timeblocks', $where );
							$e2 = $result2->fetch();

							if( $e2 && $e2['max_valid_from'] )
							{
								$nextDate2 = $checkFrom;
								break;
							}
							else
							{
								$this->companyT->modify( '-1 day' );
								$checkFrom = $this->companyT->formatDate_Db();
								if( $nextDate1 && ($checkFrom <= $nextDate1) )
								{
									break;
								}
								if( $checkFrom < $checkTo )
								{
									break;
								}
							}
						}
					}
				}
				else
				{
					$result = $ntsdb->select( 'MIN(valid_from) AS min_valid_from, MAX(valid_to) AS max_valid_to', 'timeblocks', $where );
					$e = $result->fetch();
					if( $e && $e['min_valid_from'] )
					{
						if( $e['min_valid_from'] > $okDate )
							$checkFrom = $e['min_valid_from'];
						else {
							$checkFrom = $check_next_day;
							}
						$checkTo = $e['max_valid_to'];

						while( $checkFrom )
						{
							$this->companyT->setDateDb( $checkFrom );
							$checkFromWeekday = $this->companyT->getWeekday();

							$where = $blocksWhere;
							if( $where )
								$where[] = 'AND';
							$where[] = array( 'valid_to' => array('>=', $checkFrom) );
							$where[] = 'AND';
							$where[] = array( 'applied_on' => array('=', $checkFromWeekday) );

							/* ok, now find for exact date */
							$result2 = $ntsdb->select( 'MIN(valid_from) AS min_valid_from', 'timeblocks', $where );
							$e2 = $result2->fetch();
							if( $e2 && $e2['min_valid_from'] )
							{
								if( $e2['min_valid_from'] > $checkFrom )
									$nextDate2 = $e2['min_valid_from'];
								else
									$nextDate2 = $checkFrom;
								break;
							}
							else
							{
								$this->companyT->modify( '+1 day' );
								$checkFrom = $this->companyT->formatDate_Db();
								if( $nextDate1 && ($checkFrom >= $nextDate1) )
								{
									break;
								}
								if( $checkFrom > $checkTo )
								{
									break;
								}
							}
						}
					}
				}

				if( $nextDate2 && $nextDate1 )
				{
					if( $backward )
						$nextDate = ($nextDate2 > $nextDate1) ? $nextDate2 : $nextDate1;
					else
						$nextDate = ($nextDate2 < $nextDate1) ? $nextDate2 : $nextDate1;
				}
				elseif( $nextDate2 )
				{
					$nextDate = $nextDate2;
				}
				elseif( $nextDate1 )
				{
					$nextDate = $nextDate1;
				}
			}

			$okDate = $nextDate;
			if( $okDate )
			{
				$return[] = $okDate;
			}
		}

		
		if( $backward )
		{
			sort( $return, SORT_NUMERIC );
		}
		return $return;
	}

	function setSkip( $skip_id )
	{
		if( ! is_array($skip_id) )
			$skip_id = array( $skip_id );
		$this->skip_id = $skip_id;
	}

	function addGlobalLimit( $key, $params, $error )
	{
		if( ! isset($this->global_limit[$key]) )
			$this->global_limit[$key] = array();
		$this->global_limit[$key][] = array( $params, $error );
	}

	function init( $start, $end )
	{
		if(
			($end <= $this->init_end) && 
			($start >= $this->init_start)
			)
		{
			return; // already loaded
		}

		$this->global_limit = array();

		$this->loadTimeblocks( $start, $end );
		$this->loadTimeoffs( $start, $end );
		if( ! $this->dryRun )
		{
			$this->loadAppointments( $start, $end );
		}

		$this->init_start = $start;
		$this->init_end = $end;
	}

	public function loadTimeblocks( $startTime, $endTime )
	{
		$ntsdb =& dbWrapper::getInstance();

		$this->timeblocks = array();
		$what = array(
			'id',
			'valid_from',
			'valid_to',
			'applied_on',
			'week_applied_on',
			'location_id',
			'resource_id',
			'service_id',
			'starts_at',
			'ends_at',
			'selectable_every',
			'capacity',
			'max_capacity',
			'min_from_now',
			'max_from_now'
			);

		$this->companyT->setTimestamp( $startTime );
		if( $this->max_duration >= 24*60*60 )
		{
			$this->companyT->modify( '-' . $this->max_duration . ' seconds' );
		}
		$this->companyT->modify( '-1 day' );
		$start_date = $this->companyT->formatDate_Db();

		$this->companyT->setTimestamp( $endTime );
		if( $this->max_duration >= 24*60*60 )
		{
			$this->companyT->modify( '+' . $this->max_duration . ' seconds' );
		}
		$this->companyT->modify( '+1 day' );
		$end_date = $this->companyT->formatDate_Db();

		$where = array(
			'valid_from'	=> array('<=', $end_date),
			'valid_to'		=> array('>=', $start_date),
			);
		$this->timeblocks = $ntsdb->get_select( $what, 'timeblocks', $where );
	}

	public function loadTimeoffs( $startTime, $endTime )
	{
		$this->timeoffs = array();
		$where = array(
			'(ends_at)'	=> array('>', ($startTime - $this->maxLeadin) ),
			'starts_at'	=> array('<', ($endTime + $this->maxDuration + $this->maxLeadOut) )
			);
		if( $result = $this->queryTimeoff($where) )
		{
			while( $to = $result->fetch() )
			{
				$rid = $to['resource_id'];
				if( ! isset($this->timeoffs[$rid]) )
				{
					$this->timeoffs[$rid] = array();
				}
				$this->timeoffs[$rid][] = $to;
			}
		}
	}

	function throwSlotError( $error_array )
	{
		if( is_array($error_array) ){
			foreach( $error_array as $k => $v ){
				if( ! isset($this->slot_errors[$k]) )
					$this->slot_errors[$k] = $v;
			}
		}
	}

	function getSlotErrors()
	{
		return $this->slot_errors;
	}
	function setSlotErrors( $slot_errors )
	{
		$this->slot_errors = $slot_errors;
	}

	function addVirtualAppointment( $a )
	{
		global $NTS_VIRTUAL_APPOINTMENTS;
		if( ! $NTS_VIRTUAL_APPOINTMENTS )
			$NTS_VIRTUAL_APPOINTMENTS = array();

		$new_id = - ( count($NTS_VIRTUAL_APPOINTMENTS) + 1 );
		$a['id'] = $new_id;
		$NTS_VIRTUAL_APPOINTMENTS[ $new_id ] = $a;
	}

	function addFilter( $key, $values )
	{
		switch( $key )
		{
			case 'resource':
				if( ! in_array(0, $values) )
				{
					if( $this->resourceIds )
						$this->resourceIds = array_intersect($this->resourceIds, $values);
					else
						$this->resourceIds = $values;
				}
				break;

			case 'service':
				if( ! in_array(0, $values) )
				{
					if( $this->serviceIds )
						$this->serviceIds = array_intersect($this->serviceIds, $values);
					else
						$this->serviceIds = $values;
				}
				break;

			case 'location':
				if( ! in_array(0, $values) )
				{
					if( $this->locationIds )
						$this->locationIds = array_intersect($this->locationIds, $values);
					else
						$this->locationIds = $values;
				}
				break;
		}
		$this->filters[ $key ] = $values;
	}

	function setResource( $res ){
		$resIds = array();

		if( is_object($res) )
			$resIds = array( $res->getId() );
		elseif( is_array($res) )
			$resIds = $res;
		elseif( $res )
			$resIds = array( $res );
		else
			$resIds = array();

		if( isset($this->filters['resource']) && $this->filters['resource'] )
		{
			if( $resIds )
				$resIds = array_intersect( $resIds, $this->filters['resource'] );
			else
				$resIds = $this->filters['resource'];
		}
		$this->resourceIds = $resIds;
		}

	function setLocation( $loc ){
		$locIds = array();

		if( is_object($loc) )
			$locIds = array( $loc->getId() );
		elseif( is_array($loc) )
			$locIds = $loc;
		elseif( $loc )
			$locIds = array( $loc );
		else
			$locIds = array();

		if( isset($this->filters['location']) && $this->filters['location'] )
		{
			if( $locIds )
				$locIds = array_intersect( $locIds, $this->filters['location'] );
			else
				$locIds = $this->filters['location'];
		}
		$this->locationIds = $locIds;
		}

	function setService( $ser ){
		$serIds = array();

		if( is_object($ser) )
			$serIds = array( $ser->getId() );
		elseif( is_array($ser) )
			$serIds = $ser;
		elseif( $ser )
			$serIds = array( $ser );
		else
			$serIds = array();

		if( isset($this->filters['service']) && $this->filters['service'] )
		{
			if( $serIds )
				$serIds = array_intersect( $serIds, $this->filters['service'] );
			else
				$serIds = $this->filters['service'];
		}
		$this->serviceIds = $serIds;
		}

	function getService(){
		return $this->serviceIds;
		}

	function countAppointments( $dateWhere = array(), $groupBy = '' ){
		if( ! isset($dateWhere['completed']) ){
			$dateWhere['completed'] = array( '=', 0 );
			}

		$lrsWhere = array();
		if( ! isset($dateWhere['location_id']) )
			$lrsWhere['location_id'] = array( '<>', 0 );
		if( ! isset($dateWhere['resource_id']) )
			$lrsWhere['resource_id'] = array( '<>', 0 );
		if( ! isset($dateWhere['service_id']) )
			$lrsWhere['service_id'] = array( '<>', 0 );

		$where = array_merge( $dateWhere, $lrsWhere );

		global $NTS_SKIP_APPOINTMENTS;
		if( $NTS_SKIP_APPOINTMENTS )
			$where[' id '] = array('NOT IN', $NTS_SKIP_APPOINTMENTS);

		if( isset($where['resource_id']) && ($where['resource_id'][0] == 'IN') && (! $where['resource_id'][1]) ){
			$return = 0;
			return $return;
			}
		
		$what = array();
		$what[] = 'COUNT(id) AS count';
		if( $groupBy )
			$what[] = $groupBy;
		$what = join( ',', $what );
		
		$ntsdb =& dbWrapper::getInstance();
		$other = $groupBy ? 'GROUP BY ' . $groupBy : '';
		$result = $ntsdb->select( $what, 'appointments', $where, $other );

		if( $groupBy ){
			$return = array();
			if( $result ){
				while( $e = $result->fetch() ){
					$return[ $e[$groupBy] ] = $e['count'];
					}
				}
			}
		else {
			$return = 0;
			if( $result ){
				$e = $result->fetch();
				$return = $e['count'];
				}
			}
		return $return;
		}

	function queryAppointments( $where = array(), $addon = '', $limit = array(), $fields = array() )
	{
		global $NTS_SKIP_APPOINTMENTS;
		if( $NTS_SKIP_APPOINTMENTS )
			$where[' id '] = array('NOT IN', $NTS_SKIP_APPOINTMENTS);
		if( ! isset($where['completed']) ){
			$where['completed'] = array( '=', 0 );
		}

		if( $limit ){
			$addon .= ' LIMIT ' . $limit[0] . ', ' . $limit[1];
		}

		$ntsdb =& dbWrapper::getInstance();
		if( $fields && ! in_array('id', $fields) ){
			$fields[] = 'id';
		}

		if( ! $fields ){
			$fields = 'id, starts_at, created_at, lead_in, duration, duration_break, duration2, lead_out, location_id, resource_id, service_id, seats, approved, completed, customer_id, price';
		}

		if( ! preg_match('/order by/i', $addon) ){
			$addon .= ' ORDER BY (starts_at-lead_in) ASC';
		}
		if( isset($where['resource_id']) && ($where['resource_id'][0] == 'IN') && (! $where['resource_id'][1]) ){
			$return = NULL;
		}
		else {
			$return = $ntsdb->select(
				$fields,
				'appointments',
				$where,
				$addon
				);
		}
		return $return;
	}

	function getBundleTimes( $startTime, $endTime )
	{
		$this->isBundle = FALSE;
		$saveServices = $this->serviceIds;

		$subReturn = array();
		reset( $saveServices );
		foreach( $saveServices as $sid ){
			$this->setService( $sid );
			$subReturn[] = $this->getAllTime( $startTime, $endTime );
		}

		$return = array();
		$thisIndex = 0;
		reset( $subReturn[$thisIndex] );
		foreach( $subReturn[$thisIndex] as $ts => $arr ){
			$duration = $this->services[ $saveServices[$thisIndex] ]['duration'];

			$finalTs = array();
			$finalTs[] = $ts;
			$ts2 = $ts;
			for( $thisIndex2 = 1; $thisIndex2 < count($subReturn); $thisIndex2++ ){
				$thisFound = false;

				$ts2 = $ts2 + $duration;
				$gap = 0;
				while( $gap <= $this->bundleGap )
				{
					if( isset($subReturn[$thisIndex2][$ts2]) )
					{
						$finalTs[] = $ts2;
						$duration = $this->services[ $saveServices[$thisIndex2] ]['duration'];
						$thisFound = true;
						continue 2;
					}
					$gap = $gap + $timeUnit;
					$ts2 = $ts2 + $timeUnit;
				}
				if( ! $thisFound )
					break;
				}
			if( count($finalTs) == count($subReturn) ){
				$return[ $ts ] = $finalTs;
			}
		}

	/* save back */
		$this->setService( $saveServices );
		$this->isBundle = TRUE;
		return $return;
	}

	function getBy( $what, $check, $slots )
	{
		$iis = array(
			'start' => 1,
			'end' => 2,
			'lid' => 3,
			'rid' => 4,
			'sid' => 5,
			);
		$ii = $iis[$what];

		$return = array();
		$current_ii = 0;
		foreach( $slots as $start_ts => $slots2 ){
			$current_ii = 1;
			if( ($current_ii == $ii) && ($check != $start_ts) )
				continue;
			foreach( $slots2 as $end_ts => $slots3 ){
				$current_ii = 2;
				if( ($current_ii == $ii) && ($check != $end_ts) )
					continue;
				foreach( $slots3 as $slot_lid => $slots4 ){
					$current_ii = 3;
					if( ($current_ii == $ii) && ($check != $slot_lid) )
						continue;
					foreach( $slots4 as $slot_rid => $slots5 ){
						$current_ii = 4;
						if( ($current_ii == $ii) && ($check != $slot_rid) )
							continue;
						foreach( $slots5 as $slot_sid => $seats ){
							$return[] = array( $start_ts, $end_ts, $slot_lid, $slot_rid, $slot_sid, $seats );
						}
					}
				}
			}
		}
		return $return;
	}

	protected function addSlot( $in_slot )
	{
		list( $start, $end, $lid, $rid, $sid, $seats, $max_seats ) = $in_slot;
		$slot = array( $lid, $rid, $sid, array($end => $seats), $max_seats );

		if( $this->blockMode ){
			$remain_seats = $seats;
		}
		else {
			$remain_seats = $this->checkSlot( $start, $slot, FALSE );
		}
		if( $remain_seats ){
			$slot[3] = $remain_seats;
			if( ! isset($this->slots[$start]) )
				$this->slots[$start] = array();
			$this->slots[$start][] = $slot;
		}
	}

	function buildSlots( $startTime, $endTime )
	{
		$this->slots = array();

		$now = time();
		$timeUnit = NTS_TIME_UNIT * 60;

		$ntsdb =& dbWrapper::getInstance();

		$this->companyT->setTimestamp( $endTime );
		$toDate = $this->companyT->formatDate_Db();
		$this->companyT->setTimestamp( $startTime );
		$fromDate = $this->companyT->formatDate_Db();

		$rexDate = $fromDate;
		$dates = array();
		$firstWeekdays = array();
		$di = 0;
		while( $rexDate <= $toDate ){
			$rexWeekday = $this->companyT->getWeekday();
			$rexWeekNo = $this->companyT->getWeekNo();
			$startDay = $this->companyT->getStartDay(); 
			
			if( ! isset($firstWeekdays[$rexWeekday]) )
				$firstWeekdays[$rexWeekday] = $di;
			$dates[ $rexDate ] = array( $startDay, $rexWeekNo );

			$this->companyT->setDateDb($rexDate);
			$this->companyT->modify( '+1 day' );
			$rexDate = $this->companyT->formatDate_Db();
			$di++;
		}
		$datesIndex = array_keys( $dates );
		$daysCount = count( $dates );

	/* build where */
		$where = array();

		$limitWeekdays = NULL;
		if( count($firstWeekdays) < 7 ){
			$limitWeekdays = array_keys($firstWeekdays);
		}
		if( isset($this->filters['weekday']) ){
			$limitWeekdays = is_array($limitWeekdays) ? array_intersect($limitWeekdays, $this->filters['weekday']) : $this->filters['weekday'];
		}

	/* go thru timeblocks */
		reset( $this->timeblocks );
		foreach( $this->timeblocks as $b1 ){
			if( ! isset($firstWeekdays[$b1['applied_on']]) )
				continue;

			if( 
				$this->locationIds && 
				($b1['location_id'] != 0) && 
				(! in_array($b1['location_id'], $this->locationIds))
			){
				continue;
			}

			if(
				$this->resourceIds && 
				($b1['resource_id'] != 0) && 
				(! in_array($b1['resource_id'], $this->resourceIds))
			){
				continue;
			}

			if(
				$this->serviceIds && 
				($b1['service_id'] != 0) && 
				(! in_array($b1['service_id'], $this->serviceIds))
			){
				continue;
			}

			if( 
				is_array($limitWeekdays) &&  
				(! in_array($b1['applied_on'], $limitWeekdays))
			){
				continue;
			}

			$block_starts_at = $b1['starts_at'];
			$block_ends_at = $b1['ends_at'];

		/* check time filter */
			if( isset($this->filters['time']) ){
				if( $this->filters['time'][0] > $block_starts_at ){
					$block_starts_at = $this->filters['time'][0];
				}
				if( $this->filters['time'][1] < $block_ends_at ){
					$block_ends_at = $this->filters['time'][1];
				}
				if( $block_ends_at <= $block_starts_at ){
					continue;
				}
			}

			$lids = ( $b1['location_id'] == 0 ) ? $this->allLocationIds : array( $b1['location_id'] );
			$rids = ( $b1['resource_id'] == 0 ) ? $this->allResourceIds : array( $b1['resource_id'] );
			$sids = ( $b1['service_id'] == 0 ) ? $this->allServiceIds : array( $b1['service_id'] );

			$bbs = array();
			reset( $lids );
			foreach( $lids as $lid ){
				if( $this->locationIds && (! in_array($lid, $this->locationIds))){
					continue;
				}
				reset( $rids );
				foreach( $rids as $rid ){
					if( $this->resourceIds && (! in_array($rid, $this->resourceIds))){
						continue;
					}
					if( 
						$this->customerSide && 
						$this->internalResourceIds && 
						in_array($rid, $this->internalResourceIds)
					){
						continue;
					}

					reset( $sids );
					foreach( $sids as $sid ){
						if( ! isset($this->services[$sid]) ){
							continue;
						}
						if( $this->serviceIds && (! in_array($sid, $this->serviceIds))){
							continue;
						}
						$b = array();
						$b['location_id'] = $lid; 
						$b['resource_id'] = $rid;
						$b['service_id'] = $sid;
						$bbs[] = $b;
					}
				}
			}

			$di = $firstWeekdays[ $b1['applied_on'] ];
			while( $di < $daysCount ){
				$thisDate = $datesIndex[$di];
				if( isset($this->filters['date']) ){
					if( isset($this->filters['date']['from']) ){
						if( $thisDate > $this->filters['date']['to'] )
							break;
						if( $thisDate < $this->filters['date']['from'] ){
							$di += 7;
							continue;
						}
					}
					else {
						if( $thisDate > max($this->filters['date']) )
							break;
						if( ! in_array($thisDate, $this->filters['date']) ){
							$di += 7;
							continue;
						}
					}
				}

				if( $thisDate > $b1['valid_to'] )
					break;
				if( $thisDate < $b1['valid_from'] ){
					$di += 7;
					continue;
				}

				$startDay = $dates[ $datesIndex[$di] ][0];
				$weekNo = $dates[ $datesIndex[$di] ][1];

				if( 
					$b1['week_applied_on']
					&&
					(
						( ($b1['week_applied_on'] == 2) && ($weekNo % 2) ) // want even
						OR
						( ($b1['week_applied_on'] == 1) && (! ($weekNo % 2)) ) // want odd
					)
					){
					$di += 7;
					continue;
				}

				foreach( $bbs as $b2 ){
					$rid = $b2['resource_id'];
					$lid = $b2['location_id'];
					$sid = $b2['service_id'];
					$seats = $b1['capacity'];
					$max_seats = $b1['max_capacity'];

					$leadIn = $this->services[$sid]['lead_in']; 
					$leadOut = $this->services[$sid]['lead_out'];
					$service_min_duration = $this->services[$sid]['duration'];
				/* second part */
					if( $this->services[$sid]['duration2'] ){
						$sid2 = $sid . '_2';
						$service_min_duration = $service_min_duration + $this->services[$sid]['duration_break'] + $this->services[$sid2]['duration'];
						$leadOut = $this->services[$sid2]['lead_out'];
					}

					$minFromNow = $b1['min_from_now'];
					$maxFromNow = $b1['max_from_now']; 

					$checkStart = $startTime;
					$checkEnd = $endTime;

					if( $this->customerSide ){
						/* 
						measure minFromNow from the block start rather than now
						applied on not fixed time blocks
						if it's today and todays block not yet started
						*/
						if(
							( $this->conf['minFromNowTomorrow'] == 'tomorrow' ) && 
							( $b1['selectable_every'] ) && 
							( $now < ($startDay + $block_starts_at) ) && 
							( ($now + 24*60*60) > ($startDay + $block_ends_at)  )
							){
							$serviceStartTime = ($startDay + $block_starts_at) + $minFromNow;
						}
						else {
							$serviceStartTime = $now + $minFromNow;
						}
						$serviceEndTime = $now + $maxFromNow;

						if( $serviceEndTime > $serviceStartTime){
							$checkStart = ($serviceStartTime > $startTime) ? $serviceStartTime : $startTime;
							$checkEnd = ($serviceEndTime < $endTime) ? $serviceEndTime : $endTime;
						}
					}

					$ts = $block_starts_at;

					if( $this->blockMode ){ // just check if we have blocks, that's all
						$this_block_start = $startDay + $block_starts_at;
						$this_block_end = $startDay + $block_ends_at;

						if( 
							( $this_block_start < $checkEnd )
							&&
							( $this_block_end > $checkStart )
							){
							$this->addSlot( 
								array($this_block_start, $this_block_end, $lid, $rid, $sid, $seats, $max_seats)
								);
							return;
						}
					}

					if( $b1['selectable_every'] ){
						$checkBlockEnd = $block_ends_at;
						$rex_block_ends_at = $block_ends_at;

						if( $rex_block_ends_at >= 24 * 60 * 60 ){
							$this->tempT->setDateDb( $datesIndex[$di] );
						}

						$how_many_days = 0;
						$target_check_end = $rex_block_ends_at + $this->max_duration;

						while( 
							($rex_block_ends_at >= 24 * 60 * 60)
							&&
							( $checkBlockEnd < $target_check_end )
							)
						{
						/* find next blocks */
							$need_start = ($rex_block_ends_at - 24*60*60);
							$how_many_days++;

						// ends at/after midnight, I should find a block tomorrow, 
						// and probably days after tomorrow if my max service is long
							$this->tempT->modify( '+1 day' );
							$tomorrow = $this->tempT->formatDate_Db();
							$tomorrowWeekday = $this->tempT->getWeekday();
							$tomorrowWeekNo = $this->tempT->getWeekNo();
							$tomorrowWeekType = ($tomorrowWeekNo % 2) ? 2 : 1;

/*
							$tomorrowWhere = array(
								'location_id'	=> array( '=', $b1['location_id'] ),
								'resource_id'	=> array( '=', $b1['resource_id'] ),
								'service_id'	=> array( '=', $b1['service_id'] ),
								'starts_at'		=> array( '<=', $need_start ),
								'valid_from'	=> array( '<=', $tomorrow ),
								'valid_to'		=> array( '>=', $tomorrow ),
								'applied_on'	=> array( '=', $tomorrowWeekday ),
								'week_applied_on'	=> array('IN', array(0, $tomorrowWeekType)),
								);
							$tomorrowBlocks = $this->getBlocksByWhere( $tomorrowWhere );
*/
							$tomorrowBlocks = array();
							reset( $this->timeblocks );
							foreach( $this->timeblocks as $tmb ){
								if( $tmb['location_id'] != $b1['location_id'] ){
									continue;
								}
								if( $tmb['resource_id'] != $b1['resource_id'] ){
									continue;
								}
								if( $tmb['service_id'] != $b1['service_id'] ){
									continue;
								}
								if( $tmb['starts_at'] > $need_start ){
									continue;
								}
								if( $tmb['valid_from'] > $tomorrow ){
									continue;
								}
								if( $tmb['valid_to'] < $tomorrow ){
									continue;
								}
								if( $tmb['applied_on'] != $tomorrowWeekday ){
									continue;
								}
								if( ! in_array($tmb['week_applied_on'], array(0, $tomorrowWeekType)) ){
									continue;
								}
								$tomorrowBlocks[] = $tmb;
							}

							$rex_block_ends_at = 0;
							if( $tomorrowBlocks ){
								$this_block_ends_at = 0;
								foreach( $tomorrowBlocks as $tb ){
									if( $tb['ends_at'] > $this_block_ends_at ){
										$this_block_ends_at = $tb['ends_at'];
									}
								}
								$rex_block_ends_at = $this_block_ends_at;
								$checkBlockEnd = $how_many_days * (24*60*60) + $rex_block_ends_at;
							}
						}

						$slot_ends_at = $checkBlockEnd;
						$slot_full_ends_at = $startDay + $slot_ends_at;

						$checkBlockEnd = $checkBlockEnd - $service_min_duration - $leadOut;

						while( $ts <= $checkBlockEnd ){
							if( ! isset($this->timesIndex[ ($startDay + $ts) ]) ){
								$this->companyT->setTimestamp( $startDay );
								$this->companyT->modify( '+' . $ts . ' seconds' );
								$this->timesIndex[ ($startDay + $ts) ] = $this->companyT->getTimestamp();
							}
							$addTs = $this->timesIndex[ ($startDay + $ts) ];
							if( $addTs > $checkEnd ){
								break;
							}
							if( $addTs < $checkStart ){
								$ts = $ts + $b1['selectable_every'];
								continue;
							}

							$this->addSlot( 
								array($addTs, $slot_full_ends_at, $lid, $rid, $sid, $seats, $max_seats)
								);
							if( $this->dayMode && $this->slots ){
								return;
							}
							$ts = $ts + $b1['selectable_every'];
							}
						}
				// fixed time
					else {
						if( ! isset($this->timesIndex[($startDay + $ts)]) ){
							$this->companyT->setTimestamp( $startDay );
							$this->companyT->modify( '+' . $ts . ' seconds' );
							$this->timesIndex[ ($startDay + $ts) ] = $this->companyT->getTimestamp();
						}
						$addTs = $this->timesIndex[ ($startDay + $ts) ];

						$slot_ends_at = $ts + $this->max_duration;

						if( ($addTs <= $checkEnd) && ($addTs >= $checkStart) ){
							$thisOk = TRUE;

							if( ! isset($return[$addTs]) )
								$return[$addTs] = array();

							if( ! isset($this->timesIndex[($startDay + $slot_ends_at)]) ){
								$this->companyT->setTimestamp( $startDay );
								$this->companyT->modify( '+' . $slot_ends_at . ' seconds' );
								$this->timesIndex[ ($startDay + $slot_ends_at) ] = $this->companyT->getTimestamp();
							}
							$addTsEnd = $this->timesIndex[ ($startDay + $slot_ends_at) ];

							$slot_duration = ($addTsEnd - $addTs);
							if( $slot_duration >= $service_min_duration ){
								$this->addSlot( 
									array($addTs, $addTsEnd, $lid, $rid, $sid, $seats, $max_seats)
									);
								if( $this->dayMode && $this->slots ){
									return;
								}
							}
							}
						}
					}
				$di += 7;
				}
			}
		if( ! array_keys($this->slots) ){
			return;
		}

		ksort( $this->slots );
		return;
	}

	protected function _buildTimeIndex( $startTime, $endTime )
	{
		$now = time();
		$timeUnit = NTS_TIME_UNIT * 60;

		$this->companyT->setTimestamp( $endTime );
		$toDate = $this->companyT->formatDate_Db();
		$this->companyT->setTimestamp( $startTime );
		$fromDate = $this->companyT->formatDate_Db();

		$rexDate = $fromDate;
		$this->timesIndex = array();
		while( $rexDate <= $toDate )
		{
			$rexWeekday = $this->companyT->getWeekday();
			$startDay = $this->companyT->getStartDay();

	/* build times index that means i will not need to call heavy time functions in the loop */
	/* it's for damn daylight savings time */
	/* probably we'll use the getTransitions() method by so far the dumb way */
			if( $this->minBlockStart )
				$this->companyT->modify( '+' . $this->minBlockStart . ' seconds' );
			for( $calcTs = ($startDay + $this->minBlockStart); $calcTs <= ($startDay + $this->maxBlockEnd); $calcTs += $timeUnit )
			{
				$this->timesIndex[ $calcTs ] = $this->companyT->getTimestamp();
				$this->companyT->modify( '+' . $timeUnit . ' seconds' );
			}

			$this->companyT->setDateDb($rexDate);
			$this->companyT->modify( '+1 day' );
			$rexDate = $this->companyT->formatDate_Db();
		}
	}

	function prepareReturn()
	{
		$return = array();
		reset( $this->slots );
		foreach( $this->slots as $start_ts => $slots2 )
		{
			$return[$start_ts] = array();
			foreach( $slots2 as $end_ts => $slots3 )
			{
				foreach( $slots3 as $slot_lid => $slots4 )
				{
					foreach( $slots4 as $slot_rid => $slots5 )
					{
						foreach( $slots5 as $slot_sid => $seats )
						{
							$return[$start_ts][] = array(
								$slot_lid,
								$slot_rid,
								$slot_sid,
								array(
									$end_ts	=> $seats
									)
								);
						}
					}
				}
			}
		}
		return $return;
	}

	function getAvailableSeats( $slots, $timestamp_to ){
		$return = 0;
		foreach( $slots as $slot ){
			foreach( $slot[$this->SLT_INDX['duration']] as $available_to => $this_seats ){
				if( $available_to >= $timestamp_to ){
					if( $this->customerSide ){
						$this_max_seats = $slot[$this->SLT_INDX['max_seats']];
						$this_seats = min( $this_seats, $this_max_seats );
					}

					if( $this_seats > $return ){
						$return = $this_seats;
					}
				}
			}
		}
		return $return;
	}

	/*
	returns array(
		'timestamp'	=> array(
			array(
				lid,
				rid,
				sid,
				array(
					timestamp_to	=> seats
					)
				)
			)
	*/
	function getAllTime( $startTime, $endTime ){
		$this->slots = array();

		$return = array();
		$now = time();
		$timeUnit = NTS_TIME_UNIT * 60;

		if( $this->isBundle ){
			$return = $this->getBundleTimes( $startTime, $endTime );
			return $return;
		}

		$this->_buildTimeIndex( $startTime, $endTime );

	/* load stuff */
		$this->init( $startTime, $endTime );

	/* generate slots */
		$this->slots = array();
		$this->buildSlots( $startTime, $endTime );
		return $this->slots;
		}

	public function loadAppointments( $startTime, $endTime )
	{
		$where = array(
			'(starts_at + duration + lead_out + duration_break + duration2)'	=> array('>', ($startTime - $this->maxLeadin)),
			'starts_at'							=> array('<', ($endTime + $this->maxDuration + $this->maxLeadOut))
			);
		if( $this->processCompleted ){
			$where['completed'] = array( '<>', HA_STATUS_CANCELLED );
			$where['completed '] = array( '<>', HA_STATUS_NOSHOW );
		}

		$this->apps = $this->getAppointments($where);

		global $NTS_VIRTUAL_APPOINTMENTS;
		if( ! $NTS_VIRTUAL_APPOINTMENTS )
			$NTS_VIRTUAL_APPOINTMENTS = array();
		if( $NTS_VIRTUAL_APPOINTMENTS ){
			$this->apps = array_merge( $this->apps, $NTS_VIRTUAL_APPOINTMENTS );
			// resort by (starts_at-lead_in)
//			$func = create_function('$a, $b', 'return ( ($a["starts_at"]-$a["lead_in"]) - ($b["starts_at"]-$b["lead_in"]) );');
			$func = create_function('$a, $b', 'return ( $a["starts_at"] - $b["starts_at"] );');
			usort( $this->apps, $func );
		}
	}

	public function checkSlot( $ts, $slot, $all = FALSE )
	{
		static $occupiedPerLocation;
		static $occupiedPerLocation_AppsProcessed;

		list( $slot_lid, $slot_rid, $slot_sid, $slot_seats ) = $slot;
		$original_slot_seats = $slot_seats;
		$slot_ends_ats = array_keys( $slot_seats );

		$return_seats = $slot_seats;
		$this->slot_errors = array();

		if( $this->dryRun ){
			return $return_seats;
		}

		$service_min_duration = isset($this->services[$slot_sid]) ? $this->services[$slot_sid]['duration'] + $this->services[$slot_sid]['lead_out'] : $this->minDuration;
		$slot_leadin = isset($this->services[$slot_sid]) ? $this->services[$slot_sid]['lead_in'] : 0;

	/* check global limits */
		if( ! $this->appsOnly ){
			foreach( $this->global_limit as $key => $limits ){
				foreach( $limits as $limit ){
					switch ( $key ){
						case 'time':
							list( $limit_from, $limit_to ) = $limit[0];
							if( ($ts >= $limit_from) && ($ts < $limit_to) ){
								$return_seats = array();
								$this->throwSlotError( $limit[1] );
							}
							break;
					}
					if( ! $return_seats ){
						break;
					}
				}
				if( ! $return_seats ){
					break;
				}
			}
		}

		if( ! $return_seats ){
			return $return_seats;
		}

	/* check timeoffs */
		if( ! $this->appsOnly ){
			if( isset($this->timeoffs[$slot_rid]) ){
				reset( $this->timeoffs[$slot_rid] );
				foreach( $this->timeoffs[$slot_rid] as $to ){
					if( $to['ends_at'] <= ($ts - $slot_leadin) )
						continue;

					$slot_ends_ats = array_keys($return_seats);
					foreach( $slot_ends_ats as $slot_ends_at ){
						if( $to['starts_at'] >= $slot_ends_at )
							continue;

						$new_ends_at = $to['starts_at'];
						if( ($new_ends_at - $ts) >= $service_min_duration ){
							if( ! isset($return_seats[$new_ends_at]) )
								$return_seats[$new_ends_at] = 0;
							$return_seats[$new_ends_at] += $return_seats[$slot_ends_at];
						}
						unset( $return_seats[$slot_ends_at] );

						if( $all && (! $return_seats) ){
							$this->throwSlotError( array('resource' => M('Timeoff')) );
						}
					}

					if( ! $return_seats ){
						break;
					}
				}
			}
		}

		if( ! $return_seats ){
			return $return_seats;
		}

		$max_ends_at = 0;
		$slot_seats = 0;
		foreach( $return_seats as $this_ends_at => $this_seats ){
			if( $this_ends_at > $max_ends_at )
				$max_ends_at = $this_ends_at;
			$slot_seats += $this_seats;
		}

	/* check appointments */
		$timeUnit = NTS_TIME_UNIT * 60;

	/* release occupied per location */
		if( $this->skip_id ){
			foreach( $this->skip_id as $skip_id ){
				if( ! isset($this->apps[$skip_id]) )
					continue;
				$a = $this->apps[$skip_id];
				$app_lid = $a['location_id'];

				if( ! $a['duration2'] ){
					$app_start = $a['starts_at'] - $a['lead_in'];
					$app_end = $a['starts_at'] + $a['duration'] + $a['lead_out'];
					$app_start2 = 0;
					$app_end2 = 0;
				}
				else {
					$app_start = $a['starts_at'] - $a['lead_in'];
					$app_end = $a['starts_at'] + $a['duration'];
					$app_start2 = $a['starts_at'] + $a['duration'] + $a['duration_break'];
					$app_end2 = $a['starts_at'] + $a['duration'] + $a['duration_break'] + $a['duration2'] + $a['lead_out'];
				}

				/* release occupied per location */
				if(
					isset($this->locations[$app_lid]['capacity']) && 
					($this->locations[$app_lid]['capacity'] > 0)
					)
				{
					if( isset($occupiedPerLocation_AppsProcessed[$a['id']]) ){
						unset($occupiedPerLocation_AppsProcessed[$a['id']]);

						for( $tts = $app_start; $tts < $app_end; $tts += $timeUnit ){
							if( isset($occupiedPerLocation[$tts][$app_lid]) ){
								$occupiedPerLocation[$tts][$app_lid] -= $a['seats'];
							}
						}
						for( $tts = $app_start2; $tts < $app_end2; $tts += $timeUnit ){
							if( isset($occupiedPerLocation[$tts][$app_lid]) ){
								$occupiedPerLocation[$tts][$app_lid] -= $a['seats'];
							}
						}
					}
				}
			}
		}

		foreach( $this->apps as $a )
		{
			if( $this->skip_id && (in_array($a['id'],$this->skip_id)) ){
				continue;
			}

			if( isset($a['completed']) && $a['completed'] ){
				if( $this->completedFreeSlot ){
					continue;
				}
			}

			if( ! isset($a['lead_in']) ){
				$a['lead_in'] = 0;
				}
			if( ! isset($a['lead_out']) ){
				$a['lead_out'] = 0;
				}
			if( ! isset($a['duration_break']) ){
				$a['duration_break'] = 0;
				}
			if( ! isset($a['duration2']) ){
				$a['duration2'] = 0;
				}

			$app_lid = $a['location_id'];

			if( ! $a['duration2'] ){
				$app_start = $a['starts_at'] - $a['lead_in'];
				$app_end = $a['starts_at'] + $a['duration'] + $a['lead_out'];
				$app_start2 = 0;
				$app_end2 = 0;
			}
			else {
				$app_start = $a['starts_at'] - $a['lead_in'];
				$app_end = $a['starts_at'] + $a['duration'];
				$app_start2 = $a['starts_at'] + $a['duration'] + $a['duration_break'];
				$app_end2 = $a['starts_at'] + $a['duration'] + $a['duration_break'] + $a['duration2'] + $a['lead_out'];
			}

			$app_rid = $a['resource_id'];
			$app_sid = $a['service_id'];
			$app_seats = isset($a['seats']) ? $a['seats'] : 1;

			if(
				isset($this->locations[$app_lid]['capacity']) && 
				($this->locations[$app_lid]['capacity'] > 0)
				)
			{
				if( ! isset($occupiedPerLocation_AppsProcessed[$a['id']]) ){
					$occupiedPerLocation_AppsProcessed[$a['id']] = 1;
					for( $tts = $app_start; $tts < $app_end; $tts += $timeUnit ){
						if( ! isset($occupiedPerLocation[$tts][$app_lid]) )
							$occupiedPerLocation[$tts][$app_lid] = 0;
						$occupiedPerLocation[$tts][$app_lid] += $app_seats;
					}
					for( $tts = $app_start2; $tts < $app_end2; $tts += $timeUnit ){
						if( ! isset($occupiedPerLocation[$tts][$app_lid]) )
							$occupiedPerLocation[$tts][$app_lid] = 0;
						$occupiedPerLocation[$tts][$app_lid] += $app_seats;
					}
				}
			}

			if( $slot_lid == $app_lid )
				$travel_time = 0;
			else
				$travel_time = isset($this->locations[$slot_lid]['_travel'][$app_lid]) ? $this->locations[$slot_lid]['_travel'][$app_lid] : 0;

			$cut_from = $app_start;
			if( $app_start2 && ($ts - $slot_leadin - $travel_time) >= $app_end ) {
				// $cut_from = $app_start2;
			}

			if( (! $app_start2) ){
				if( ($ts - $slot_leadin - $travel_time) >= $app_end ){
					continue;
				}
			}
			/* double part appointment */
			else {
				if( ($ts - $slot_leadin - $travel_time) >= $app_end2 ){
					continue;
				}

				if( 
					( ($ts) >= $app_end ) &&
					( ($ts + $service_min_duration) <= $app_start2 )
					){
					continue;
				}
			}

			if( $app_start >= ($max_ends_at + $travel_time) ){
				break;
			}

			$remove_seats = 0;

			if(
				( $this->locations[$slot_lid]['capacity'] > 0 )
				){
				// check out all occupied location for the whole duration of this slot
				foreach( $return_seats as $this_ends_at => $this_seats ){
					for( $tts = $ts; $tts <= $this_ends_at; $tts += $timeUnit ){
						if(
							isset($occupiedPerLocation[$tts][$slot_lid]) && 
							($occupiedPerLocation[$tts][$slot_lid] >= $this->locations[$slot_lid]['capacity'])
							)
						{
							$remove_seats = $this_seats;
							if( $slot_rid != $app_rid ){
								$cut_from = $tts;
							}
							if( $all ){
								$this->throwSlotError( array('location' => M('Location Fully Booked')) );
							}
							break;
						}
					}
				}
			}

		/* don't allow double booking by customer */
			if( ! $this->conf['allowOverlapCustomer'] ){
				if( $this->customerId && $this->customerId == $a['customer_id'] ){
					$remove_seats = $slot_seats;
				}
			}

		/* don't allow the same time, service, resource, location, customer */
			if( ! $this->conf['allowSameAppCustomer'] ){
				if(
					(isset($a['customer_id']) && ($this->customerId && $this->customerId == $a['customer_id'])) &&
					( $slot_rid == $app_rid ) &&
					( $slot_sid == $app_sid ) &&
					( $slot_lid == $app_lid ) &&
					( $ts == $a['starts_at'] )
					){
					$remove_seats = $slot_seats;
				}
			}

			if( ! $remove_seats )
			{
			/* this resource, blocks resource */
				if (
					( $slot_rid == $app_rid ) && 
					(
						( isset($this->services[ $app_sid ]) && $this->services[ $app_sid ]['blocks_resource'] ) OR
						( isset($this->services[ $slot_sid ]) && $this->services[ $slot_sid ]['blocks_resource'] )
					)
					){
						$remove_seats = $slot_seats;
					}
			/* this resource, this service - delete everything but the start at this location */
				elseif( 
					( $slot_rid == $app_rid ) &&
					( $slot_sid == $app_sid )
					){
						if( ($slot_lid == $app_lid) ){
						/* this slot */
							if(
								( isset($this->services[ $app_sid ]) ) OR
								($a['starts_at'] == $ts ) 
							){
								$remove_seats = $app_seats;
							}
						/* other slot */
							else {
								$remove_seats = $slot_seats;
							}
						}
						/* other location - remove everything */
						else {
							$remove_seats = $slot_seats;
						}
					}
			/* this resource, other service - delete everything  - UPDATE DON'T DELETE */
				elseif(
					( $slot_rid == $app_rid )
					){
						$remove_seats = $app_seats;
					}
			/* this location */
				elseif(
					( $slot_lid == $app_lid )
					){
					/* delete everything - if locks location */
						if (
							( isset($this->services[ $app_sid ]) && $this->services[ $app_sid ]['blocks_location'] ) OR
							( isset($this->services[ $slot_sid ]) && $this->services[ $slot_sid ]['blocks_location'] )
							){
							$remove_seats = $slot_seats;
						}

					/* if location has limited capacity */
						elseif(
							( $this->locations[$slot_lid]['capacity'] > 0 )
							){
							// check out all occupied location for the whole duration of this slot
							foreach( $return_seats as $this_ends_at => $this_seats ){
								for( $tts = $ts; $tts <= $this_ends_at; $tts += $timeUnit ){
									if(
										isset($occupiedPerLocation[$tts][$slot_lid]) && 
										($occupiedPerLocation[$tts][$slot_lid] >= $this->locations[$slot_lid]['capacity'])
										){
										$remove_seats = $this_seats;
										if( $slot_rid != $app_rid ){
											$cut_from = $tts;
										}
										if( $all ){
											$this->throwSlotError( array('location' => M('Location Fully Booked')) );
										}
										break;
									}
								}
							}
						}
					}
			/* any resource, any service - continue */
				else {
					// nothing
				}
			}

			if( $remove_seats ){
				$new_ends_at = $cut_from;

				foreach( $return_seats as $this_ends_at => $this_seats ){
					if( ! $remove_seats )
						break;
					if( $this_ends_at <= ($cut_from - $travel_time) )
						continue;

					$take_seats = $return_seats[$this_ends_at];
					if( $take_seats > $remove_seats )
						$take_seats = $remove_seats;

					$new_ends_at = ($cut_from - $travel_time);
					if( $new_ends_at >= ($ts + $service_min_duration) ){
						// if( ! isset($return_seats[$new_ends_at]) )
							// $return_seats[$new_ends_at] = 0;
						// $return_seats[$new_ends_at] += $take_seats;
						$return_seats[$new_ends_at] = $this_seats;
					}

					$return_seats[$this_ends_at] = $return_seats[$this_ends_at] - $take_seats;
					if( $return_seats[$this_ends_at] <= 0 ){
						unset( $return_seats[$this_ends_at] );
					}
					$remove_seats = $remove_seats - $take_seats;
				}

				if( $all && (! $return_seats) ){
					$this->throwSlotError( array('time' => M('Other Appointment')) );
				}
			}
			if( ! $return_seats ){
				break;
			}
		}

	/* check plugins */
		if( ! $this->appsOnly ){
			reset( $this->slot_plugins );
			foreach( $this->slot_plugins as $plg_file ){
				$remove_seats = 0;
				require( $plg_file );

				if( ! $return_seats ){
					break;
				}
			}
		}

	/* if has duration2 */
		$slot_sid2 = $slot_sid . '_2';
		if( $return_seats && isset($this->services[$slot_sid2]) ){
			$slot2 = array();
			$ts2 = $ts + $this->services[$slot_sid]['duration'] + $this->services[$slot_sid]['duration_break'];
			$slot2 = array( $slot_lid, $slot_rid, $slot_sid2, $original_slot_seats );

			$slot_errors = $this->getSlotErrors();
			$return_seats2 = $this->checkSlot( $ts2, $slot2, $all );
			$slot_errors2 = $this->getSlotErrors();
			$slot_errors = array_merge( $slot_errors, $slot_errors2 );
			$this->setSlotErrors( $slot_errors );

			if( ! $return_seats2 ){
				$return_seats = array();
			}
		}

		return $return_seats;
	}

	public function makeSlotFromAppointment( $app )
	{
		if( is_object($app) )
			$app = $app->getByArray();

		$seats = isset($app['seats']) ? $app['seats'] : 1;
		$duration = $app['duration'];
		$lead_out = isset($app['lead_out']) ? $app['lead_out'] : 0;
		$starts_at = $app['starts_at'];
		$customer_id = isset($app['customer_id']) ? $app['customer_id'] : 0;
		$slot = array( 
			$app['location_id'],
			$app['resource_id'],
			$app['service_id'],
			array(
				($starts_at + $duration + $lead_out) => $seats,
				),
			$customer_id
			);
		return $slot;
	}

/* returns the next available times according to current settings */
	function getNearestTimes( $start = 0 ){
		$ntsdb =& dbWrapper::getInstance();
		if( ! $start )
		{
			$start = time();
			if( isset($this->filters['date']) )
			{
				$this->companyT->setDateDb( min($this->filters['date']) );
				$thisStart = $this->companyT->getTimestamp();
				if( $thisStart > $start )
					$start = $thisStart;
			}
		}

		$now = time();
		$saveLids = $this->locationIds;
		$saveRids = $this->resourceIds;
		$saveSids = $this->serviceIds;

		$return = array(
			'location'	=> array(),
			'resource'	=> array(),
			'service'	=> array()
			);
		$shouldFind = array();

		$shouldFind['location'] = array();
		$allIds = $this->locationIds ? $this->locationIds : $this->allLocationIds;
		foreach( $allIds as $id )
			$shouldFind['location'][$id] = 1;

		$shouldFind['resource'] = array();
		$allIds = $this->resourceIds ? $this->resourceIds : $this->allResourceIds;
		foreach( $allIds as $id )
			$shouldFind['resource'][$id] = 1;
			
		$shouldFind['service'] = array();
		$allIds = $this->serviceIds ? $this->serviceIds : $this->allServiceIds;
		foreach( $allIds as $id )
			$shouldFind['service'][$id] = 1;

	/* first go */
		$first_days = 3;
	
		$this->companyT->setTimestamp( $start );
		$startRexDate = $this->companyT->formatDate_Db();
		$rexDate = $startRexDate;
		if( $first_days > 1 )
		{
			$this->companyT->modify( '+' . ($first_days - 1) . ' days' );
		}

		$timesEndCheck = $this->companyT->getEndDay();
		$this->companyT->setDateDb( $rexDate );
		$timesStartCheck = $this->companyT->getStartDay();
		if( $timesStartCheck < $start ){
			$timesStartCheck = $start;
			}
		$times = $this->getAllTime( $timesStartCheck, $timesEndCheck );

		reset( $times );
		foreach( $times as $ts => $slots ){
			reset( $slots );
			foreach( $slots as $slot ){
				list( $lid, $rid, $sid, $seats ) = $slot;
				if( ! isset($return['location'][$lid]) ){
					$return['location'][$lid] = $ts;
					unset( $shouldFind['location'][$lid] );
					}
				if( ! isset($return['resource'][$rid]) ){
					$return['resource'][$rid] = $ts;
					unset( $shouldFind['resource'][$rid] );
					}
				if( ! isset($return['service'][$sid]) ){
					$return['service'][$sid] = $ts;
					unset( $shouldFind['service'][$sid] );
					}
				}
			}

		$this->companyT->setDateDb( $rexDate );
		$this->companyT->modify( '+' . $first_days . ' day' );
		$startRexDate = $this->companyT->formatDate_Db();

	/* go check - location */
		if( $shouldFind['location'] )
		{
			$rexDate = $startRexDate;
			$this->setLocation( array_keys($shouldFind['location']) );
			$this->resourceIds = $saveRids;
			$this->serviceIds = $saveSids;

			while( $rexDate )
			{
				$checkThis = TRUE;
				if( isset($this->filters['date']) )
				{
					if( $rexDate > max($this->filters['date']) )
					{
						$rexDate = 0;
						continue;
					}

					if( isset($this->filters['date']['from']) )
					{
						if( $rexDate < $this->filters['date']['from'] )
						{
							$checkThis = FALSE;
						}
					}
					else
					{
						if( ! in_array($rexDate, $this->filters['date']) )
						{
							$checkThis = FALSE;
						}
					}
				}

				if( $checkThis )
				{
					$this->companyT->setDateDb( $rexDate );
					$timesEndCheck = $this->companyT->getEndDay();
					$this->companyT->setDateDb( $rexDate );
					$timesStartCheck = $this->companyT->getStartDay();
					if( $timesStartCheck < $start ){
						$timesStartCheck = $start;
						}
					$times = $this->getAllTime( $timesStartCheck, $timesEndCheck );

					reset( $times );
					foreach( $times as $ts => $slots ){
						reset( $slots );
						foreach( $slots as $slot ){
							list( $lid, $rid, $sid, $seats ) = $slot;
							if( ! isset($return['location'][$lid]) ){
								$return['location'][$lid] = $ts;
								unset( $shouldFind['location'][$lid] );
								}
							}
						}
				}

				if( $shouldFind['location'] )
				{
					$this->companyT->setDateDb( $rexDate );
					$this->companyT->modify( '+1 day' );
					$rexDate = $this->companyT->formatDate_Db();
					$rexTs = $this->companyT->getTimestamp();
					$diffSec = $rexTs - $now;
					if( $diffSec < 0 )
						$diffSec = 0;

					$where = array();
					$where[] = array(
						array( 'location_id' => array( 'IN', array_keys($shouldFind['location']) ) ),
						array( 'location_id' => array( '=', 0 ) ),
						);
					if( $this->resourceIds ){
						$where[] = 'AND';
						$where[] = array(
							array( 'resource_id' => array( 'IN', $this->resourceIds) ),
							array( 'resource_id' => array( '=', 0 ) ),
							);
						}
					if( $this->serviceIds ){
						$where[] = 'AND';
						$where[] = array(
							array( 'service_id' => array( 'IN', $this->serviceIds) ),
							array( 'service_id' => array( '=', 0 ) ),
							);
						}
					$where[] = 'AND';
					$where[] = array( 'valid_to' => array('>=', $rexDate) );
					$where[] = 'AND';
					$where[] = array( 'max_from_now' => array('>=', $diffSec) );

					$result = $ntsdb->select( 'MIN(valid_from) AS min_valid_from', 'timeblocks', $where );
					$e = $result->fetch();
					if( $e && $e['min_valid_from'] ){
						if( $e['min_valid_from'] > $rexDate )
							$rexDate = $e['min_valid_from'];
						$this->setLocation( array_keys($shouldFind['location']) );
						}
					else {
						$shouldFind['location'] = array();
						}
				}
				if( ! $shouldFind['location'] )
					$rexDate = 0;
			}
		}

	/* go check - resource */
		if( $shouldFind['resource'] )
		{
			$rexDate = $startRexDate;
			$this->setResource( array_keys($shouldFind['resource']) );
			$this->locationIds = $saveLids;
			$this->serviceIds = $saveSids;

			while( $rexDate )
			{
				$checkThis = TRUE;
				if( isset($this->filters['date']) )
				{
					if( $rexDate > max($this->filters['date']) )
					{
						$rexDate = 0;
						continue;
					}

					if( isset($this->filters['date']['from']) )
					{
						if( $rexDate < $this->filters['date']['from'] )
						{
							$checkThis = FALSE;
						}
					}
					else
					{
						if( ! in_array($rexDate, $this->filters['date']) )
						{
							$checkThis = FALSE;
						}
					}
				}

				if( $checkThis )
				{
					$this->companyT->setDateDb( $rexDate );
					$timesEndCheck = $this->companyT->getEndDay();
					$this->companyT->setDateDb( $rexDate );
					$timesStartCheck = $this->companyT->getStartDay();
					if( $timesStartCheck < $start ){
						$timesStartCheck = $start;
						}
					$times = $this->getAllTime( $timesStartCheck, $timesEndCheck );

					reset( $times );
					foreach( $times as $ts => $slots ){
						reset( $slots );
						foreach( $slots as $slot ){
							list( $lid, $rid, $sid, $seats ) = $slot;
							if( ! isset($return['resource'][$rid]) ){
								$return['resource'][$rid] = $ts;
								unset( $shouldFind['resource'][$rid] );
								}
							}
						}
				}

				if( $shouldFind['resource'] )
				{
					$this->companyT->setDateDb( $rexDate );
					$this->companyT->modify( '+1 day' );
					$rexDate = $this->companyT->formatDate_Db();
					$rexTs = $this->companyT->getTimestamp();
					$diffSec = $rexTs - $now;
					if( $diffSec < 0 )
						$diffSec = 0;

					$where = array();
					$where[] = array(
						array( 'resource_id' => array( 'IN', array_keys($shouldFind['resource']) ) ),
						array( 'resource_id' => array( '=', 0 ) ),
						);
					if( $this->locationIds ){
						$where[] = 'AND';
						$where[] = array(
							array( 'location_id' => array( 'IN', $this->locationIds) ),
							array( 'location_id' => array( '=', 0 ) ),
							);
						}
					if( $this->serviceIds ){
						$where[] = 'AND';
						$where[] = array(
							array( 'service_id' => array( 'IN', $this->serviceIds) ),
							array( 'service_id' => array( '=', 0 ) ),
							);
						}
					$where[] = 'AND';
					$where[] = array( 'valid_to' => array('>=', $rexDate) );
					$where[] = 'AND';
					$where[] = array( 'max_from_now' => array('>=', $diffSec) );

					$result = $ntsdb->select( 'MIN(valid_from) AS min_valid_from', 'timeblocks', $where );
					$e = $result->fetch();
					if( $e && $e['min_valid_from'] ){
						if( $e['min_valid_from'] > $rexDate )
							$rexDate = $e['min_valid_from'];
						$this->setResource( array_keys($shouldFind['resource']) );
						}
					else {
						$shouldFind['resource'] = array();
						}
				}
				if( ! $shouldFind['resource'] )
					$rexDate = 0;
			}
		}

	/* go check - service */
		if( $shouldFind['service'] )
		{
			$rexDate = $startRexDate;
			$this->setService( array_keys($shouldFind['service']) );
			$this->locationIds = $saveLids;
			$this->resourceIds = $saveRids;

			while( $rexDate )
			{
				$checkThis = TRUE;
				if( isset($this->filters['date']) )
				{
					if( $rexDate > max($this->filters['date']) )
					{
						$rexDate = 0;
						continue;
					}

					if( isset($this->filters['date']['from']) )
					{
						if( $rexDate < $this->filters['date']['from'] )
						{
							$checkThis = FALSE;
						}
					}
					else
					{
						if( ! in_array($rexDate, $this->filters['date']) )
						{
							$checkThis = FALSE;
						}
					}
				}

				if( $checkThis )
				{
					$this->companyT->setDateDb( $rexDate );
					$timesEndCheck = $this->companyT->getEndDay();
					$this->companyT->setDateDb( $rexDate );
					$timesStartCheck = $this->companyT->getStartDay();
					if( $timesStartCheck < $start ){
						$timesStartCheck = $start;
						}
					$times = $this->getAllTime( $timesStartCheck, $timesEndCheck );

					reset( $times );
					foreach( $times as $ts => $slots ){
						reset( $slots );
						foreach( $slots as $slot ){
							list( $lid, $rid, $sid, $seats ) = $slot;
							if( ! isset($return['service'][$sid]) ){
								$return['service'][$sid] = $ts;
								unset( $shouldFind['service'][$sid] );
								}
							}
						}
				}

				if( $shouldFind['service'] )
				{
					$this->companyT->setDateDb( $rexDate );
					$this->companyT->modify( '+1 day' );
					$rexDate = $this->companyT->formatDate_Db();
					$rexTs = $this->companyT->getTimestamp();
					$diffSec = $rexTs - $now;
					if( $diffSec < 0 )
						$diffSec = 0;

					$where = array();
					$where[] = array(
						array( 'service_id' => array( 'IN', array_keys($shouldFind['service']) ) ),
						array( 'service_id' => array( '=', 0 ) ),
						);
					if( $this->locationIds ){
						$where[] = 'AND';
						$where[] = array(
							array( 'location_id' => array( 'IN', $this->locationIds) ),
							array( 'location_id' => array( '=', 0 ) ),
							);
						}
					if( $this->resourceIds ){
						$where[] = 'AND';
						$where[] = array(
							array( 'resource_id' => array( 'IN', $this->resourceIds) ),
							array( 'resource_id' => array( '=', 0 ) ),
							);
						}
					$where[] = 'AND';
					$where[] = array( 'valid_to' => array('>=', $rexDate) );
					$where[] = 'AND';
					$where[] = array( 'max_from_now' => array('>=', $diffSec) );

					$result = $ntsdb->select( 'MIN(valid_from) AS min_valid_from', 'timeblocks', $where );
					$e = $result->fetch();
					if( $e && $e['min_valid_from'] ){
						if( $e['min_valid_from'] > $rexDate )
							$rexDate = $e['min_valid_from'];
						$this->setService( array_keys($shouldFind['service']) );
						}
					else {
						$shouldFind['service'] = array();
						}
				}
				if( ! $shouldFind['service'] )
					$rexDate = 0;
			}
		}

		$this->setLocation( $saveLids );
		$this->setResource( $saveRids );
		$this->setService( $saveSids );
		return $return;
		}

	function getNextTimes( $start = 0, $chunkSize = 0, $isBundle = FALSE )
	{
		$return = array();
		if( ! $start )
		{
			$start = time();
			if( isset($this->filters['date']) )
			{
				if( isset($this->filters['date']['from']) )
				{
					$this->companyT->setDateDb( $this->filters['date']['from'] );
				}
				else
				{
					$this->companyT->setDateDb( min($this->filters['date']) );
				}
				$thisStart = $this->companyT->getTimestamp();
				if( $thisStart > $start )
					$start = $thisStart;
			}
		}
		if( $start < 0 )
		{
			return $return;
		}

		if( ! $chunkSize )
			$chunkSize = $this->chunkSize;

		$ntsdb =& dbWrapper::getInstance();

		$lrsWhere = array();
		if( $this->locationIds )
			$lrsWhere[] = "(location_id IN (" . join(',', $this->locationIds) . ") OR location_id = 0)";
		if( $this->resourceIds )
			$lrsWhere[] = "resource_id IN (" . join(',', $this->resourceIds) . ")";
		if( $this->serviceIds )
			$lrsWhere[] = "(service_id IN (" . join(',', $this->serviceIds) . ") OR service_id = 0)";

		$this->companyT->setTimestamp( $start );
		$rexStart = $this->companyT->formatDate_Db();

		while( $rexStart ){
			$checkThis = TRUE;
			if( isset($this->filters['date']) )
			{
				if( isset($this->filters['date']['from']) )
				{
					if( $rexStart < $this->filters['date']['from'] )
					{
						$rexStart = $this->filters['date']['from'];
						continue;
					}
					if( $rexStart > $this->filters['date']['to'] )
					{
						$rexStart = 0;
						continue;
					}
				}
				else
				{
					if( $rexStart < min($this->filters['date']) )
					{
						$rexStart = min($this->filters['date']);
						continue;
					}
					if( $rexStart > max($this->filters['date']) )
					{
						$rexStart = 0;
						continue;
					}
				}
			}

			$this->companyT->setDateDb( $rexStart );
			$this->companyT->modify( '+' . ($chunkSize - 1) . ' days' );
			$timesEndCheck = $this->companyT->getEndDay();
			$this->companyT->setTimestamp( $timesEndCheck - 1 );
			$rexEnd = $this->companyT->formatDate_Db(); 

			$this->companyT->setDateDb( $rexStart );
			$timesStartCheck = $this->companyT->getStartDay();

			if( $timesStartCheck < $start ){
				$timesStartCheck = $start;
				}

			$times = $this->getAllTime( $timesStartCheck, $timesEndCheck );
			if( $times )
			{
				if( $isBundle ){
					$return = $times;
					}
				else {
					$return = array_keys($times);
					}
				$rexStart = 0;
			}
			else 
			{
			/* check next ones */
				$this->companyT->setDateDb( $rexEnd );
				$this->companyT->modify( '+1 day' );
				$rexStart = $this->companyT->formatDate_Db();
				$this->companyT->modify( '+' . ($chunkSize - 1) . ' days' );
				$rexEnd = $this->companyT->formatDate_Db(); 

				$lrsWhere2 = array();
				$where = array_merge( $lrsWhere, $lrsWhere2 );
				$where[] = "valid_to >= $rexStart";
				$where = join( ' AND ', $where );
				$sql =<<<EOT
				SELECT
					MIN(valid_from) AS min_valid_from
				FROM
					{PRFX}timeblocks
				WHERE
					$where
EOT;
				$result = $ntsdb->runQuery( $sql );
				if( $result && ($e = $result->fetch()) && $e['min_valid_from'] )
				{
					if( $e['min_valid_from'] > $rexStart )
						$rexStart = $e['min_valid_from'];
				}
				else
				{
					$rexStart = 0;
				}

				if( $rexStart && isset($this->filters['date']) )
				{
					if( $rexStart < min($this->filters['date']) )
						$rexStart = min($this->filters['date']);
					if( $rexStart > max($this->filters['date']) )
						$rexStart = 0;
				}
			}
		}
		return $return;
	}

/* REALIZATION SPECIFIC STUFF */
	function queryTimeoff( $where = array(), $addon = '' ){
		$ntsdb =& dbWrapper::getInstance();
		$keys = 'id, starts_at, ends_at, resource_id, location_id, description';

		$return = $ntsdb->select(
			$keys,
			'timeoffs',
			$where,
			$addon
			);
		return $return;
		}

	function getTimeoff( $rexDate = '', $endDate = '' ){
		$ntsdb =& dbWrapper::getInstance();

		$where = array();
		if( $rexDate ){
			$this->companyT->setDateDb( $rexDate );
			$startDay = $this->companyT->getStartDay();
			if( $endDate ){
				$this->companyT->setDateDb( $endDate );
				}
			$endDay = $this->companyT->getEndDay();

			$where['starts_at'] = array( '<', $endDay );
			$where['ends_at'] = array( '>', $startDay );
			}
		if( $this->resourceSet || $this->resourceIds ){
			$where['resource_id'] = array( 'IN', $this->resourceIds );
			}

		$return = array();
		if( isset($where['resource_id']) && ($where['resource_id'][0] == 'IN') && (! $where['resource_id'][1]) ){
			}
		else {
			$result = $this->queryTimeoff( $where );
			while( $e = $result->fetch() ){
				$return[] = $e;
				}
			}
		return $return;
		}

	function getBlocksByWhere( $where = array() ){
		$return = array();
		$ntsdb =& dbWrapper::getInstance();

		$keys = 'location_id, resource_id, service_id, starts_at, ends_at, selectable_every, capacity, group_id';
		$keys .= ', valid_from, valid_to, applied_on';

		$result = $ntsdb->select($keys, 'timeblocks', $where );
		$byGroup = array();
		$thisIndex = 0;
		while( $e = $result->fetch() ){
			if( isset($byGroup[$e['group_id']]) ){
				$myIndex = $byGroup[$e['group_id']];
				if( ! in_array($e['location_id'], $return[$myIndex]['location_id']) )
					$return[$myIndex]['location_id'][] = $e['location_id'];
				if( ! in_array($e['resource_id'], $return[$myIndex]['resource_id']) )
					$return[$myIndex]['resource_id'][] = $e['resource_id'];
				if( ! in_array($e['service_id'], $return[$myIndex]['service_id']) )
					$return[$myIndex]['service_id'][] = $e['service_id'];
				if( ! in_array($e['applied_on'], $return[$myIndex]['applied_on']) )
					$return[$myIndex]['applied_on'][] = $e['applied_on'];
				}
			else {
				$e['location_id'] = array($e['location_id']);
				$e['resource_id'] = array($e['resource_id']);
				$e['service_id'] = array($e['service_id']);
				$e['applied_on'] = array($e['applied_on']);
				$return[ $thisIndex ] = $e;
				$byGroup[$e['group_id']] = $thisIndex;
				$thisIndex++;
				}
			}
		return $return;
		}

	function getBlocks( $rexDate = '', $extendedKeys = false ){
		$return = array();
		$ntsdb =& dbWrapper::getInstance();

		$dateWhere = array();
		if( $rexDate )
		{
			$this->companyT->setDateDb( $rexDate );
			$weekday = $this->companyT->getWeekday();
			$dateWhere[] = "valid_from <= $rexDate AND valid_to >= $rexDate";
			$dateWhere[] = "applied_on = $weekday";

			$weekNo = $this->companyT->getWeekNo();
			$weekAppliedOn = ( $weekNo % 2 ) ? 1 : 2;
			$dateWhere[] = "week_applied_on IN(0, $weekAppliedOn)";
		}

		$lrsWhere = array();
		if( $this->locationIds ){
			$lrsWhere[] = "( location_id IN (" . join(',', $this->locationIds) . ") OR location_id=0 )";
			}
		if( $this->resourceIds ){
			$lrsWhere[] = "resource_id IN (" . join(',', $this->resourceIds) . ")";
			}
		if( $this->serviceIds ){
			$lrsWhere[] = "( service_id IN (" . join(',', $this->serviceIds) . ") OR service_id=0 )";
			}
		$where = array_merge( $dateWhere, $lrsWhere );
		$where = join( ' AND ', $where );

		$keys = 'location_id, resource_id, service_id, starts_at, ends_at, selectable_every, capacity, group_id';
		if( $extendedKeys )
			$keys .= ', id, valid_from, valid_to, applied_on';

		$sql =<<<EOT
		SELECT
			$keys
		FROM
			{PRFX}timeblocks
		WHERE
			$where
EOT;

		$result = $ntsdb->runQuery( $sql );
		while( $e = $result->fetch() ){
			$return[] = $e;
			}
		return $return;
		}

	function getAppointments( $where, $addon = '', $limit = array(), $fields = array() )
	{
		$return = array();
		$result = $this->queryAppointments( $where, $addon, $limit, $fields );
		if( $result )
		{
			while( $a = $result->fetch() )
			{
				$return[ $a['id'] ] = $a;
			}
		}
		return $return;
	}

	function resetLrs()
	{
		$this->_lrs = array();
	}

	function getLrs( $skip_apps = FALSE, $from_date = FALSE )
	{
		$return = array();
		if( ! $this->_lrs )
		{
			/* load lrs */
			$ntsdb =& dbWrapper::getInstance();

			$return = array();
			$lrs = array();

			$sql =<<<EOT
			SELECT
				DISTINCT( CONCAT(location_id, "-", resource_id, "-", service_id) ) AS lrs
			FROM
				{PRFX}timeblocks
EOT;

			if( $from_date )
			{
				$sql .= "\n";
				$sql .= "WHERE valid_to >= $from_date";
			}

			$result = $ntsdb->runQuery( $sql );
			if( $result )
			{
				while( $e = $result->fetch() )
				{
					$lrs[] = $e['lrs'];
				}
			}

			if( ! $skip_apps )
			{
				$sql =<<<EOT
				SELECT
					DISTINCT( CONCAT(location_id, "-", resource_id, "-", service_id) ) AS lrs
				FROM
					{PRFX}appointments
EOT;

				$result = $ntsdb->runQuery( $sql );
				while( $e = $result->fetch() )
				{
					$lrs[] = $e['lrs'];
				}
			}

			$lrs = array_unique( $lrs );
			$this->_lrs = $lrs;
		}

		reset( $this->_lrs );
		foreach( $this->_lrs as $e )
		{
			list( $lid, $rid, $sid ) = explode( '-', $e );
			if( $this->resourceIds && ! in_array($rid,$this->resourceIds) )
				continue;

			if( $this->customerSide && $this->internalResourceIds && in_array($rid, $this->internalResourceIds) )
			{
				continue;
			}

			$lids = ( $lid == 0 ) ? $this->allLocationIds : array( $lid );
			$sids = ( $sid == 0 ) ? $this->allServiceIds : array( $sid );

			reset( $lids );
			foreach( $lids as $lid2 )
			{
				if( $this->locationIds && ! in_array($lid2,$this->locationIds) )
				{
					continue;
				}
				reset( $sids );
				foreach( $sids as $sid2 )
				{
					if( $this->serviceIds && ! in_array($sid2,$this->serviceIds) )
						continue;
					$return[] = array( $lid2, $rid, $sid2 );
				}
			}
		}

		return $return;
	}

	function updateBlocks( $groupId, $params ){
		$toDelete = array();
		$toAdd = array();
		$toUpdate = array();

		$currentBlocks = $this->getBlocksByGroupId( $groupId );
		reset( $currentBlocks );

		$checkExist = array('location_id', 'resource_id', 'service_id', 'applied_on');
		$checkUpdate = array('week_applied_on', 'capacity', 'max_capacity', 'valid_from', 'valid_to', 'starts_at', 'ends_at', 'selectable_every', 'min_from_now', 'max_from_now');

		$currentOptions = array();
		foreach( $currentBlocks as $cb ){
			$key = join( '-', array($cb['location_id'], $cb['resource_id'], $cb['service_id'], $cb['applied_on']) );
			$currentOptions[ $key ] = $cb;
			}

//		_print_r( $params );
		$newOptions = array();
		if( ! is_array($params['location_id']) ){
			$params['location_id'] = array( $params['location_id'] );
			}
		if( ! is_array($params['resource_id']) ){
			$params['resource_id'] = array( $params['resource_id'] );
			}
		if( ! is_array($params['service_id']) ){
			$params['service_id'] = array( $params['service_id'] );
			}
		reset( $params['location_id'] );
		foreach( $params['location_id'] as $id1 ){
			reset( $params['resource_id'] );
			foreach( $params['resource_id'] as $id2 ){
				reset( $params['service_id'] );
				foreach( $params['service_id'] as $id3 ){
					reset( $params['applied_on'] );
					foreach( $params['applied_on'] as $id4 ){
						$key = join( '-', array($id1, $id2, $id3, $id4) );
						$newOptions[ $key ] = 1;
						}
					}
				}
			}
	// which to delete
		$keys2delete = array_diff( array_keys($currentOptions), array_keys($newOptions) );
		reset( $keys2delete );
		foreach( $keys2delete as $k ){
			$toDelete[] = $currentOptions[$k]['id'];
			}

	// which to add
		$keys2add = array_diff( array_keys($newOptions), array_keys($currentOptions) );
		reset( $keys2add );
		foreach( $keys2add as $k ){
			$nb = array();
			list( $nb['location_id'], $nb['resource_id'], $nb['service_id'], $nb['applied_on'] ) = explode( '-', $k );
			
			reset( $checkUpdate );
			foreach( $checkUpdate as $k2 )
				$nb[$k2] = $params[$k2];
			$nb['group_id'] = $groupId;
			$toAdd[] = $nb;
			}

	// which to update
		$keys2update = array_intersect( array_keys($newOptions), array_keys($currentOptions) );

		reset( $keys2update );
		foreach( $keys2update as $k )
		{
			$ub = array();

			reset( $checkUpdate );
			foreach( $checkUpdate as $k2 )
			{
				if( $currentOptions[$k][$k2] != $params[$k2] )
				{
					$ub[$k2] = $params[$k2];
				}
			}

			if( $ub )
			{
				$ub['id'] = $currentOptions[$k]['id'];
				$toUpdate[] = $ub;
			}
		}

//		_print_r( $toDelete );
//		_print_r( $toUpdate );
//		_print_r( $toAdd );
//		exit;

		$ntsdb =& dbWrapper::getInstance();
//		$ntsdb->_debug = true;
		reset( $toDelete );
		foreach( $toDelete as $id ){
			$ntsdb->delete( 'timeblocks', array('id' => array('=', $id)) );
			}

		reset( $toUpdate );
		foreach( $toUpdate as $a ){
			$id = $a['id'];
			unset( $a['id'] );
			$ntsdb->update( 'timeblocks', $a, array('id' => array('=', $id)) );
			}

		reset( $toAdd );
		foreach( $toAdd as $a ){
			$ntsdb->insert( 'timeblocks', $a );
			}
//		$ntsdb->_debug = false;
		}

	function addBlock( $b ){
		$ntsdb =& dbWrapper::getInstance();
		$t = new ntsTime;

		if( ! isset($b['selectable_every']))
			$b['selectable_every'] = 0;
		if( ! isset($b['ends_at']))
			$b['ends_at'] = 0;

		/* get new group id */
		$newGroupId = 0;
		$result = $ntsdb->select( 'MAX(group_id) AS group_id', 'timeblocks' );
		if( $result && ($i = $result->fetch()) ){
			$newGroupId = $i['group_id'];
			}
		if( $newGroupId )
			$newGroupId = $newGroupId + 1;
		else
			$newGroupId = 1;

		if( ! is_array($b['location_id']) )
			$b['location_id'] = array( $b['location_id'] );
		if( ! is_array($b['resource_id']) )
			$b['resource_id'] = array( $b['resource_id'] );
		if( ! is_array($b['service_id']) )
			$b['service_id'] = array( $b['service_id'] );
		if( ! is_array($b['applied_on']) )
			$b['applied_on'] = array( $b['applied_on'] );

		$toAdd = array();
		reset( $b['location_id'] );
		foreach( $b['location_id'] as $lid ){
			reset( $b['resource_id'] );
			foreach( $b['resource_id'] as $rid ){
				reset( $b['service_id'] );
				foreach( $b['service_id'] as $sid ){
					reset( $b['applied_on'] );
					foreach( $b['applied_on'] as $aon ){
						$newB = $b;
						$newB['location_id'] = $lid;
						$newB['resource_id'] = $rid;
						$newB['service_id'] = $sid;
						$newB['applied_on'] = $aon;
						$newB['group_id'] = $newGroupId;
						$toAdd[] = $newB;
						}
					}
				}
			}
		reset( $toAdd );
		foreach( $toAdd as $a ){
			$ntsdb->insert( 'timeblocks', $a );
			}
		}

	function getBlocksByGroupId( $groupId ){
		$return = array();
		$ntsdb =& dbWrapper::getInstance();
		$extendedKeys = true;

		$where = array();
		$where['group_id'] = array('=', $groupId);

		$what = array('location_id', 'resource_id', 'service_id', 'starts_at', 'ends_at', 'selectable_every', 'capacity', 'max_capacity', 'group_id', 'min_from_now', 'max_from_now' );
		if( $extendedKeys )
			$what = array_merge($what, array('id', 'valid_from', 'valid_to', 'applied_on', 'week_applied_on'));

		$result = $ntsdb->select( $what, 'timeblocks', $where );
		while( $i = $result->fetch() ){
			$return[] = $i;
			}
		return $return;
		}

	function deleteBlocks( $groupId ){
		$ntsdb =& dbWrapper::getInstance();

		$where = array();
		$where['group_id'] = array('=', $groupId);

		$result = $ntsdb->delete( 'timeblocks', $where );
		}

	function deleteBlocksByWhere( $where ){
		$ntsdb =& dbWrapper::getInstance();
		$result = $ntsdb->delete( 'timeblocks', $where );
		}
	}
?>