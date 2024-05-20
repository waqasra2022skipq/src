<?php
class ntsPromotion extends ntsObject 
{
	/*
	location
	resource
	service
	weekday
	time

	pack
	*/
	public $_coupons = array();

	function __construct()
	{
		parent::__construct( 'promotion' );
	}

	function getRule()
	{
		$return = $this->getProp( 'rule', TRUE );
		if( ! $return )
		{
			$return = array();
		}
		return $return;
	}

	function setRule( $rule )
	{
		if( isset($rule['date'][0]) )
		{
			sort( $rule['date'] );
		}
		$this->setProp( 'rule', $rule );
	}

	function load()
	{
		parent::load();
	/* load coupons as well */
		$where = array(
			'promotion_id'	=> array('=', $this->getId()),
			);
		$this->_coupons = ntsObjectFactory::find( 'coupon', $where );
	}

	function getTitle()
	{
		return $this->getProp('title');
	}

	function getCoupons()
	{
		return $this->_coupons;
	}

	function getCouponCodes()
	{
		$currentCoupons = $this->getCoupons();
		$currentCodes = array_map( create_function('$a', 'return $a->getProp("code");'), $currentCoupons );
		return $currentCodes;
	}

	function getRuleView()
	{
		$return = array();
		$rule = $this->getRule();

		$objects = array( 
			array('location',	M('Location')),
			array('resource',	M('Bookable Resource')),
			array('service',	M('Service')),
			array('customer',	M('Customer')),
			array('pack',		M('Package')),
			);
		
		foreach( $objects as $o )
		{
			if( isset($rule[$o[0]]) )
			{
				$view = array();
				$view[] = $o[1];

				$view2 = array();
				reset( $rule[$o[0]] );
				foreach( $rule[$o[0]] as $oid )
				{
					if( $o[0] == 'customer' ){
						$o[0] = 'user';
					}
					if( $oid == -1 ){
						$view2[] = ' - ' . M('All') . ' - ';
					}
					else {
						$obj = ntsObjectFactory::get($o[0], $oid);
						$view2[] = ntsView::objectTitle( $obj );
					}
				}
				$view[] = $view2;
				$return[$o[0]] = $view;
			}
		}

		if( isset($rule['date']) )
		{
			$view = array();
			$view[] = M('Dates');

			$t = new ntsTime();
			if( isset($rule['date']['from']) )
			{
				$t->setDateDb( $rule['date']['from'] );
				$fromView = $t->formatDate();
				$t->setDateDb( $rule['date']['to'] );
				$toView = $t->formatDate();
				$view2 = array( join( ' - ', array($fromView, $toView) ) );
			}
			else
			{
				$view2 = array();
				foreach( $rule['date'] as $date )
				{
					$t->setDateDb( $date );
					$dateView = $t->formatDate();
					$view2[] = $dateView;
				}
			}

			$view[] = $view2;
			$return['date'] = $view;
		}

		if( isset($rule['weekday']) )
		{
			$view = array();
			$view[] = M('Weekday');

			$view2 = array();
			reset( $rule['weekday'] );
			foreach( $rule['weekday'] as $wdi )
			{
				$view2[] = ntsTime::weekdayLabelShort($wdi);
			}
			$view[] = $view2;
			$return['weekday'] = $view;
		}

		if( isset($rule['time']) )
		{
			$view = array();
			$view[] = M('Time');

			$t = new ntsTime();
			$view2 = array( join( ' - ', array($t->formatTimeOfDay($rule['time'][0]), $t->formatTimeOfDay($rule['time'][1])) ) );

			$view[] = $view2;
			$return['time'] = $view;
		}

		if( ! $rule )
		{
			$return['always'] = M('Always');
		}
		return $return;
	}

	function getSign()
	{
		$price = $this->getProp('price');
		if( substr($price, 0, 1) == '-' )
			$return = '-';
		else
			$return = '+';
		return $return;
	}

	function getMeasure()
	{
		$price = $this->getProp('price');
		$price = trim( $price );
		if( substr($price, -1) == '%' )
			$return = '%';
		else
			$return = '';
		return $return;
	}

	function getAmount()
	{
		$return = $this->getProp('price');
		$return = trim( $return );
		if( substr($return, 0, 1) == '-' )
			$return = substr($return, 1);
		if( substr($return, -1) == '%' )
			$return = substr($return, 0, -1);
		return $return;
	}

	function getModificationView()
	{
		$sign = $this->getSign();
		$amount = $this->getAmount();

		$thisView = array();
		if( $amount ){
			if( $this->getMeasure() == '%' ){
				$priceView = $amount . '%';
			}
			else {
				$priceView = ntsCurrency::formatPrice($amount);
			}
			$thisView[] = $priceView;
			$thisView = $sign . join( ' ', $thisView );
		}
		else {
			$thisView = M('Price Not Changed');
		}

		return $thisView;
	}

	function getUseCount()
	{
		$ntsdb =& dbWrapper::getInstance();

		$code = $this->getProp('code');
		$where = array(
			array(
				'obj_class'	=> array('=', 'promotion'),
				'action'	=> array('=', 'apply'),
				'obj_id'	=> array('=', $this->getId()),
			),
			array(
				'obj_class'	=> array('=', 'coupon'),
				'action'	=> array('=', 'apply'),
				'obj_id'	=> array('IN', '(SELECT id FROM {PRFX}coupons WHERE promotion_id=' . $this->getId() . ')', TRUE  ),
			),
			);
		$return = $ntsdb->count( 'accounting_journal', $where );
		return $return;
	}
}
?>