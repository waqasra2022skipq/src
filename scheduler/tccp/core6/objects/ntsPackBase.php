<?php
class ntsPackBase extends ntsObject {
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

	function getServiceId(){
		$serviceId = $this->getProp('service_id');
		$serviceType = $this->getServiceType();
		switch( $serviceType ){
			case 'one':
				$serviceId = trim( $serviceId, ',' );
				$return = explode( ',', $serviceId );
//				$return = $serviceId;
				break;
			case 'fixed':
				$serviceId = trim( $serviceId, '-' );
				$return = explode( '-', $serviceId );
				break;
			}
		return $return;
		}

	function getServiceType(){
		$serviceId = $this->getProp('service_id');
		if( strpos($serviceId, '-') === FALSE )
			$return = 'one';
		else
			$return = 'fixed';
		return $return;
		}

	function getType(){
		$return = '';
		$qty = $this->getProp('qty');
		$amount = $this->getProp('amount'); 
		$duration = $this->getProp('duration'); 
		if( $qty ){
			$return = 'qty';
			}
		elseif( $amount ){
			$return = 'amount';
			}
		elseif( $duration ){
			$return = 'duration';
			}
		else {
			$return = 'unlimited';
			}
		return $return;
		}
	}
?>