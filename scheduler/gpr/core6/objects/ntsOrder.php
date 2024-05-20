<?php
include_once( dirname(__FILE__) . '/ntsPackBase.php' );
class ntsOrder extends ntsPackBase {
	private $_invoices = NULL;

	function __construct(){
		parent::__construct( 'order' );
		}

	function statusLabel( $force_text = NULL )
	{
		$active = $this->getProp('is_active');
		return ntsOrder::_statusLabel( $active, $force_text );
	}

	static function _statusLabel( $active, $force_text = NULL )
	{
		$class = array();
		$main = 'label';
		$class[] = $main;
		$class[] = $main . '-large';
		$message = '';

		if( $active )
		{
			$class[] = $main . '-success';
			$message = M('Approved');
		}
		else
		{
			$class[] = $main . '-warning';
			$message = M('Pending');
		}

		$class = join( ' ', $class );
		$out = '<span class="' . $class . '" title="' . $message . '"';
		$out .= '>';
		if( $force_text === NULL )
			$out .= $message;
		else
		{
			if( ! strlen($force_text) )
				$force_text = '&nbsp';
			$out .= $force_text;
		}
		$out .= '</span>';
		return $out;
	}

	function getFilter( $what )
	{
		$return = array();
		$rule = $this->getRule();
		switch( $what )
		{
			case 'resource':
				$orderResourceId = $this->getProp('resource_id');
				$return = $orderResourceId ? array($orderResourceId) : array();
				break;

			case 'service':
				$packType = $this->getServiceType();
				switch( $packType )
				{
					case 'fixed':
						$return = $this->getLeft();
						break;
					case 'one':
						$return = $this->getServiceId();
						break;
				}
				break;

			default:
				if( isset($rule[$what]) )
				{
					$return = $rule[$what];
				}
				break;
		}
		return $return;
	}

	function getItems(){
		return $this->getParents();
		}

	function getInvoices()
	{
		$ntsconf =& ntsConf::getInstance();
		$taxRate = $ntsconf->get('taxRate');

		if( ! is_array($this->_invoices) )
		{
			$this->_invoices = array();

			$ntsdb =& dbWrapper::getInstance();
			$objId = $this->getId();

			$invoices = array();
			$where = array(
				'obj_class'	=> array('=', 'order'),
				'obj_id'	=> array('=', $objId),
				);
			$join = array(
				array( 'invoices', array('invoice_items.invoice_id' => array('=', '{PRFX}invoices.id', 1)) )
				);
			$addon = 'ORDER BY {PRFX}invoices.due_at ASC';
			$result = $ntsdb->select( 
				array(
					'invoice_id',
					'{PRFX}invoice_items.amount',
					'taxable',
					'{PRFX}invoices.due_at AS due_at'
					),
				'invoice_items',
				$where,
				$addon,
				$join
				);

			while( $i = $result->fetch() )
			{
				$calc = new ntsMoneyCalc;
				$calc->add( $i['amount'] );
				if( $i['taxable'] && $taxRate )
				{
					$tax = ntsLib::calcTax( $i['amount'], $taxRate );
					$calc->add( $tax );
				}
				$total = $calc->result();
				$this->_invoices[] = array( $i['invoice_id'], $total, $i['due_at'] );
			}
		}
		return $this->_invoices;
	}

	function getCost()
	{
		return $this->getBasePrice();
	}

	function getBasePrice()
	{
		$packId = $this->getProp( 'pack_id' );
		$pack = ntsObjectFactory::get( 'pack' );
		$pack->setId( $packId );

		$price = $pack->getProp('price');
		return $price;
	}

	function getPaidAmount()
	{
		$return = 0;
		$postings = $this->get_accounting_postings();
		if( $postings )
		{
			$calc = new ntsMoneyCalc;
			reset( $postings );
			foreach( $postings as $p )
			{
				if( $p['asset_id'] != 0 )
					continue;
				$calc->add( $p['asset_value'] );
			}
			$return = $calc->result();
		}
		return $return;
	}

	function getFullTitle()
	{
		$pack_id = $this->getProp( 'pack_id' );
		$pack = ntsObjectFactory::get( 'pack' );
		$pack->setId( $pack_id );
		$return = $pack->getFullTitle();
		return $return;
	}

	function getUsageText(){
		$return = '';

		$left = $this->getLeft();
		$usage = $this->getUsage();

		$qty = $this->getProp( 'qty' );
		$amount = $this->getProp( 'amount' );
		$duration = $this->getProp( 'duration' );

		$serviceType = $this->getServiceType();
		$type = $this->getType();
		switch( $serviceType ){
			case 'fixed':
				$serviceId = $this->getServiceId();
				$qty = count($serviceId);
				$usage = count( $usage );
				$left = count( $left );
				break;
			case 'one':
				break;
			}

		if( $usage > 0 )
			$usageText = M('Used') . ': ';
		else
			$usageText = M('Not Used');
		$leftText = M('Remain') . ': ';

		if( $left == -1 ){
			if( $usage > 0 )
				$usageText .= $usage;
			$leftText .= M('Unlimited');
			}
		elseif( $left > 0 ){
			if( $duration ){
				if( $usage > 0 )
					$usageText .= ntsTime::formatPeriod($usage);
				$leftText .= ntsTime::formatPeriod($left);
				}
			elseif( $amount ){
				if( $usage > 0 )
					$usageText .= ntsCurrency::formatPrice($usage);
				$leftText .= ntsCurrency::formatPrice($left);
				}
			elseif( $qty ){
				if( $usage > 0 )
					$usageText .= $usage;
				$leftText .= $left;
				}
			}
		else {
			$usageText .= M('Full');
			}

		if( $left )
			$return = $usageText . ', ' . $leftText;
		else
			$return = $usageText;
		return $return;
		}

	function getLeft(){
		$return = 0;

		$serviceType = $this->getServiceType();
		$type = $this->getType();
		switch( $serviceType ){
			case 'fixed':
				$return = $this->getServiceId();
				$usage = $this->getUsage();
				for( $ii = 0; $ii < count($usage); $ii++ ){
					for( $jj = 0; $jj < count($return); $jj++ ){
						if( $usage[$ii] == $return[$jj] ){
							array_splice( $return, $jj, 1 );
							break;
							}
						}
					}
				break;
			case 'one':
				switch( $type ){
					case 'unlimited':
						$return = -1;
						break;
					case 'qty':
						$qty = $this->getProp('qty');
						$return = $qty;
						break;
					case 'amount':
						$amount = $this->getProp('amount');
						$return = $amount;
						break;
					case 'duration':
						$duration = $this->getProp('duration');
						$return = $duration;
						break;
					}
				break;
			}

		if( $return == -1 ){
			}
		elseif( is_array($return) ){
			}
		else {
			$used = $this->getUsage();
			$return = $return - $used;
			if( $return < 0 )
				$return = 0;
			}

		return $return;
		}

	function getUsage(){
		$return = 0;

		$serviceType = $this->getServiceType();
		$type = $this->getType();
		switch( $serviceType ){
			case 'fixed':
				$return = array();
				$what = 'combo';
				break;
			case 'one':
				$qty = $this->getProp( 'qty' );
				$amount = $this->getProp( 'amount' );
				$duration = $this->getProp( 'duration' );

				if( $duration ){
					$what = 'duration';
					}
				elseif( $amount ){
					$what = 'amount';
					}
				else{
					$what = 'qty';
					}
				break;
			}

		$items = $this->getItems();
		foreach( $items as $item ){
			$className = $item->getClassName();
			if( $className != 'appointment' ){
				continue;
				}
			$completeStatus = $item->getProp('completed');
			if( in_array($completeStatus, array(HA_STATUS_CANCELLED, HA_STATUS_NOSHOW)) ){
				continue;
				}

			switch( $what ){
				case 'combo':
					$return[] = $item->getProp('service_id');
					break;
				case 'duration':
					$return += $item->getProp('duration');
					break;
				case 'amount':
					$return += $item->getProp('price');
					break;
				case 'qty':
				case 'unlimited':
					$return += $item->getProp('seats');
					break;
				}
			}
		return $return;
		}

	function getCustomer(){
		$customerId = $this->getProp( 'customer_id' );
		$return = new ntsUser;
		$return->setId( $customerId );
		return $return;
		}

	function isAvailable()
	{
		$return = FALSE;
	/* is not disabled */
		$isActive = $this->getProp( 'is_active' );
		if( ! $isActive )
		{
			return $return;
		}

	/* is expired */
		$expired = FALSE;
		$validTo = $this->getProp('valid_to');
		if( $validTo > 0 )
		{
			$t = new ntsTime;
			$t->setNow();
			$today = $t->formatDate_Db();

			$t->setTimestamp( $validTo );
			$validToDate = $t->formatDate_Db();
			if( $today > $validToDate )
			{
				$expired = TRUE;
			}
		}
		if( $expired )
		{
			return $return;
		}

	/* is anything left */
		$left = $this->getLeft();
		if( ! $left )
		{
			return $return;
		}

		$return = TRUE;
		return $return;
	}
}
?>