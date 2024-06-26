<?php
class ntsResource extends ntsObject {
	function __construct(){
		parent::__construct( 'resource' );
		}

	function getAdmins(){
		// static $return = NULL;
		static $return = array();

		$myId = $this->getId();

		// if( $return === NULL ){
		if( ! array_key_exists($myId, $return) ){
			$scheduleAdmins = array();
			$appsAdmins = array();

			$ntsdb =& dbWrapper::getInstance();

			/* appointments */
			$where = array(
				'obj_class'		=> array('=', 'user'),
				'meta_value'	=> array('=', $myId),
				'meta_name'		=> array('=', '_resource_apps')
				);
			$result = $ntsdb->select( array('obj_id', '	meta_data'), 'objectmeta', $where );
			if( $result )
			{
				while( $i = $result->fetch() )
				{
					$accLevel = $i['meta_data'];
					$admId = $i['obj_id']; 

					$perm = array( 'view' => 0, 'edit' => 0, 'notified' => 0 );
					if( $accLevel & 1 ){
						$perm['view'] = 1;
						}
					if( $accLevel & 2 ){
						$perm['edit'] = 1;
						}
					if( $accLevel & 4 ){
						$perm['notified'] = 1;
						}

					$appsAdmins[ $admId ] = $perm;
				}
			}

			/* schedule */
			$where = array(
				'obj_class'		=> array('=', 'user'),
				'meta_value'	=> array('=', $myId),
				'meta_name'		=> array('=', '_resource_schedules')
				);
			$result = $ntsdb->select( array('obj_id', '	meta_data'), 'objectmeta', $where );
			if( $result )
			{
				while( $i = $result->fetch() )
				{
					$accLevel = $i['meta_data'];
					$admId = $i['obj_id']; 

					$perm = array( 'view' => 0, 'edit' => 0 );
					if( $accLevel & 1 ){
						$perm['view'] = 1;
						}
					if( $accLevel & 2 ){
						$perm['edit'] = 1;
						}

					$scheduleAdmins[ $admId ] = $perm;
				}
			}
			$return[$myId] = array( $appsAdmins, $scheduleAdmins );
		}
		return $return[$myId];
		}
	}
?>