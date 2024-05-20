<?php
if( ! $slot_rid )
	return;

$plugin = 'appointment-blocks-day';

$this->companyT->setTimestamp( $ts );
$dayStart = $this->companyT->getStartDay();

if( ! isset($this->plugins_data[$plugin]) )
	$this->plugins_data[$plugin] = array();

if( ! isset($this->plugins_data[$plugin][$dayStart][$slot_rid]) )
{
	$dayEnd = $this->companyT->getEndDay();
	// ok now count appointments
	$where = array(
		'(starts_at+duration+lead_out)'	=> array( '>=', $dayStart ),
		'(starts_at-lead_in)'			=> array( '<', $dayEnd ),
		// 'completed'						=> array( 'IN', array(0, HA_STATUS_CANCELLED, HA_STATUS_NOSHOW) ),
		'completed'						=> array( 'IN', array(0) ),
		'resource_id'					=> array( '=', $slot_rid )
		);
	$apps = $this->getAppointments( $where, 'ORDER BY starts_at ASC' );
	$this->plugins_data[$plugin][$dayStart][$slot_rid] = $apps;
}

$this_slots_apps = $this->plugins_data[$plugin][$dayStart][$slot_rid];



if( $this->skip_id ){
	foreach( $this->skip_id as $this_skip_id ){
		unset( $this_slots_apps[$this_skip_id] );
	}
}

$count = count($this_slots_apps);

if( $count > 0 )
{
	/* OK REMOVE */
	$return_seats = array();

	$t = new ntsTime;
	$t->setTimestamp($ts);
	$text = M('Appointment Blocks Day');
	$this->throwSlotError( array('time' => $text) );
}
?>