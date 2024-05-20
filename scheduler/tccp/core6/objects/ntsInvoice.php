<?php
class ntsInvoice extends ntsObject
{
	public $_items = NULL;

	function __construct()
	{
		parent::__construct( 'invoice' );
	}

	function getItemsObjects()
	{
		$return = array();

		$ntsdb =& dbWrapper::getInstance();
		$where = array(
			'invoice_id'	=> array( '=', $this->getId() ),
			);

		$rows = $ntsdb->get_select(
			array( 'id', 'amount', 'qty', 'title', 'taxable', 'obj_class', 'obj_id' ),
			'invoice_items',
			$where
			);

		reset( $rows );
		$raw_items = array();
		foreach( $rows as $r )
		{
			if( $r['obj_class'] && $r['obj_id'] )
			{
				$item_class = $r['obj_class'];
				$item_id = $r['obj_id'];

				$item = ntsObjectFactory::get( $item_class );
				$item->setId( $item_id );
				$return[] = $item;
			}
		}
		return $return;
	}

	function getItems()
	{
		if( $this->_items === NULL ){
			$this->_items = $this->_loadItems();
		}
		return $this->_items;
	}

	function _loadItems()
	{
		$invoice_id = $this->getId();
		$pm =& ntsPaymentManager::getInstance();
		$return = $pm->getInvoiceItems( $invoice_id );
		return $return;
	}

	function getTaxAmount()
	{
		$return = 0;
		$calc = new ntsMoneyCalc;

		$items = $this->getItems();
		foreach( $items as $item )
		{
			$tax_rate = $item['unitTaxRate'];
			$item_amount = $item['unitCost'];
			$item_tax = ntsLib::calcTax( $item_amount, $tax_rate, FALSE ); // no round
			$calc->add( $item_tax );
		}
		$return = $calc->result();
		return $return;
	}

	function getSubTotal()
	{
		$return = 0;
		$calc = new ntsMoneyCalc;

		$items = $this->getItems();
		foreach( $items as $item )
		{
			$item_amount = $item['quantity'] * $item['unitCost'];
			$calc->add( $item_amount );
		}
		$return = $calc->result();
		return $return;
	}

	function getPaidAmount()
	{
		$return = 0;
		$calc = new ntsMoneyCalc;

		$trs = $this->getTransactions();
		reset( $trs );
		foreach( $trs as $tr )
		{
			$trAmount = $tr->getProp( 'amount' );
			$calc->add( $trAmount );
		}
		$return = $calc->result();
		return $return;
	}

	function getTransactions()
	{
		$pm =& ntsPaymentManager::getInstance();
		$invoice_id = $this->getId();
		$return = $pm->getInvoiceTransactions( $invoice_id );
		return $return;
	}

	function updateItemCost( $itemClass, $itemId, $newCost )
	{
		$ntsdb =& dbWrapper::getInstance();
		$itemClass = strtolower($itemClass);
		$where = array(
			'obj_class'		=> array('=', 'invoice'),
			'obj_id'		=> array('=', $this->getId()),
			'meta_name'		=> array('=', '_' . $itemClass),
			'meta_value'	=> array('=', $itemId),
			);
		$what = array(
			'meta_data'	=> $newCost
			);
		$ntsdb->update( 'objectmeta', $what, $where );

		$pm =& ntsPaymentManager::getInstance();
		$pm->updateInvoice( $this );
	}

	function getItemDiscount( $item )
	{
		$discounts = $this->getProp('_discount');
		$key = $item->getClassName() . ':' . $item->getId();
		$return = isset($discounts[$key]) ? $discounts[$key] : 0;
		return $return;
	}

	function updateItemDiscount( $itemClass, $itemId, $newDiscount )
	{
		$item = ntsObjectFactory::get( $itemClass );
		$item->setId( $itemId );
		$currentCost = $this->getItemAmount( $item );
		$currentDiscount = $this->getItemDiscount( $item );
		if( $newDiscount != $currentDiscount )
		{
			$discounts = $this->getProp('_discount');
			$key = $item->getClassName() . ':' . $item->getId();
			$discounts[ $key ] = $newDiscount;
			$this->setProp( '_discount', $discounts );

			$cm =& ntsCommandManager::getInstance();
			$cm->runCommand( $this, 'update' );

			$newCost = $currentCost + $currentDiscount - $newDiscount;
			$this->updateItemCost( $itemClass, $itemId, $newCost );
		}
	}

	function getFullTitle()
	{
		$depDetails = array(
			'appointment'	=> '',
			'order'	=> '',
			);
		$items = $this->getItemsObjects();
		reset( $items );
		foreach( $items as $dep )
		{
			$className = $dep->getClassName();
			switch( $className ){
				case 'appointment':
					$depDetails['appointments'][] = $dep->getId();
					break;
				case 'order':
					$depDetails['order'] = $dep;
					break;
				}
		}

		$return = '';
		$items = $this->getItems();

		if( $items )
		{
			if( count($items) == 1 )
			{
				if( isset($depDetails['order']) && $depDetails['order'] )
				{
					$return = $depDetails['order']->getFullTitle();
				}
				elseif( isset($depDetails['appointments']) && $depDetails['appointments'] )
				{
					$return = count($depDetails['appointments']) . ' ' . ( (count($depDetails['appointments'])>1) ? M('Appointments') : M('Appointment') );
				}
				else
				{
					$return = $items[0]['name'];
				}
			}
			else
			{
				$return = count($items) . ' ' . M('Items');
			}
		}

		return $return;
	}

	function getItemAmount( $item )
	{
		$return = 0;
		$items = $this->getItems();

		foreach( $items as $i )
		{
			if( ! isset($i['object']) )
				continue;

			if( 
				( $item->getClassName() == $i['object']->getClassName() ) &&
				( $item->getId() == $i['object']->getId() )
				)
			{
				$return = $i['unitCost'];
				break;
			}
		}
		return $return;
	}

	/* includes tax */
	function getTotalAmount(){
		$subtotal = $this->getSubTotal();
		$tax = $this->getTaxAmount();

		$return = 0;
		$calc = new ntsMoneyCalc;

		$calc->add( $subtotal );
		$calc->add( $tax );

		$return = $calc->result();
		return $return;
		}

	function getCustomerId()
	{
		$customer_id = 0;
		$customer_id = $this->getProp('customer_id');
		if( ! $customer_id )
		{
			$invoice_items = $this->getItemsObjects();
			if( $invoice_items )
			{
				$customer_id = $invoice_items[0]->getProp('customer_id');
			}
		}
		return $customer_id;
	}

	function getCustomer()
	{
		$return = new ntsUser;

		$customer_id = $this->getCustomerId();
		if( $customer_id )
		{
			$return->setId( $customer_id );
		}
		return $return;
	}
}

class ntsInvoiceItem extends ntsObject
{
}
?>