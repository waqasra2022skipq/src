<?php
class ntsObserverAssignPackage extends ntsObserver
{
	public function info()
	{
		$return = array(
			'title'			=> M('Automatically add a package to a new customer'),
			'description'	=> M('This one will automatically assign a specified package to a newly created or registered customer (after being activated).'),
			);
		return $return;
	}

	public function is_not_valid()
	{
		$return = parent::is_not_valid();
		$packs = ntsObjectFactory::getAll( 'pack' );
		if( ! $packs )
		{
			$return = M('Missing') . ': ' . M('Packages');
		}
		return $return;
	}

	public function form()
	{
		$return = array();

		$packs = ntsObjectFactory::getAll( 'pack' );
		if( ! $packs )
		{
			return $return;
		}

		foreach( $packs as $p )
		{
			$pack_options[] = array( $p->getId(), ntsView::objectTitle($p) );
		}
		$return = array(
			array(
				M('Package'),
				array(
					'select',
					array(
						'id'		=> 'pack_id',
						'options'	=> $pack_options
						)
					),
				)
			);
		return $return;
	}

	function run( $action_name, $object, $main_action_name, $params )
	{
		if( $action_name != 'customer::activate' )
		{
			return;
		}

		$customer_id = $object->getId();
		$pack_id = isset($this->params['pack_id']) ? $this->params['pack_id'] : 0;
		if( ! $pack_id )
		{
			return;
		}

		$pack = ntsObjectFactory::get( 'pack' );
		$pack->setId( $pack_id );
		if( $pack->notFound() )
		{
			return;
		}

		/* check if the customer already had this package */
		$ntsdb =& dbWrapper::getInstance();
		$where = array(
			'customer_id'	=> array( '=', $customer_id ),
			'pack_id'		=> array( '=', $pack_id ),
			);

		$already = $ntsdb->get_select( 
			'id',
			'orders', 
			$where
			);
		if( $already )
		{
			return;
		}

		$cm =& ntsCommandManager::getInstance();

		$order = ntsObjectFactory::get( 'order' );
		$order->setProp( 'customer_id', $customer_id );
		$order->setProp( 'pack_id', $pack_id );

		$cm->runCommand( $order, 'create' );
		$cm->runCommand( $order, 'request' );
	}
}
?>