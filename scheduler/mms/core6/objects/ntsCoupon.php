<?php
class ntsCoupon extends ntsObject 
{
	function __construct()
	{
		parent::__construct( 'coupon' );
	}

	function getUseCount()
	{
		$ntsdb =& dbWrapper::getInstance();

		$id = $this->getId();
		$promotion_id = $this->getProp('promotion_id'); 
		$where = array(
				array(
					'obj_class'	=> array('=', 'promotion'),
					'action'	=> array('=', 'apply'),
					'obj_id'	=> array('=', $promotion_id),
				),
				array(
					'obj_class'	=> array('=', 'coupon'),
					'action'	=> array('=', 'apply'),
					'obj_id'	=> array('=', $id ),
				),
			);
		$return = $ntsdb->count( 'accounting_journal', $where );
		return $return;
	}
}
?>