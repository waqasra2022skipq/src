<?php
include_once( dirname(__FILE__) . '/ntsPackBase.php' );
class ntsPack extends ntsPackBase {
	function __construct(){
		parent::__construct( 'pack' );
		}

	function getAssetValue()
	{
		$return = $this->getProp('asset_value');

		$aam =& ntsAccountingAssetManager::getInstance();
		$asset_id = $this->getProp('asset_id');
		$asset = $aam->get_asset_by_id( $asset_id );
		$service_type = $aam->get_service_type( $asset );
		switch( $service_type )
		{
			case 'fixed':
				if( isset($asset['service']) )
				{
					$return = explode( '-', $asset['service'] );
				}
				break;
		}
		return $return;
	}

	function getTotalPrice()
	{
		$pm =& ntsPaymentManager::getInstance();
		$taxRate = $pm->getTaxRate( $this ); 

		$price = $this->getProp('price');
		$tax = ntsLib::calcTax( $price, $taxRate );
		$return = $price + $tax;
		return $return;
	}

	function getTaxAmount()
	{
		$pm =& ntsPaymentManager::getInstance();
		$taxRate = $pm->getTaxRate( $this ); 

		$subtotal = $this->getSubTotal(); 
		$return = ntsLib::calcTax( $subtotal, $taxRate );
		return $return;
	}

	function getSubTotal( $total = 0 )
	{
		if( $total )
		{
			$return = $total;

			$pm =& ntsPaymentManager::getInstance();
			$taxRate = $pm->getTaxRate( $this ); 

			if( $taxRate )
			{
				$return = ntsLib::removeTax( $total, $taxRate );
			}
		}
		else
		{
			$return = $this->getProp('price');
		}
		return $return;
	}

	function getServices(){
		$return = array();
		$serviceIds = $this->getServiceId();
		reset( $serviceIds );
		foreach( $serviceIds as $sid ){
			$service = ntsObjectFactory::get( 'service' );
			$service->setId( $sid );
			$return[] = $service;
			}
		return $return;
		}

	function getGroupedServices(){
		$return = array();
		$serviceIds = $this->getServiceId();

		$index = array();
		reset( $serviceIds );
		foreach( $serviceIds as $sid ){
			if( ! isset($index[$sid]) ){
				$index[$sid] = count($return);
				$service = ntsObjectFactory::get( 'service' );
				$service->setId( $sid );
				$return[] = array( $service, 0 );
				}
			$return[ $index[$sid] ][1]++;
			}
		return $return;
		}

	function getFullTitle()
	{
		$return = ntsView::objectTitle($this);
		return $return;
	}

	function getExpiresIn(){
		$return = $this->getProp('expires_in');
		return $return;
		}
}
?>