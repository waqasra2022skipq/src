<?php
class ntsObserverAddInvoice extends ntsObserver
{
	public function info()
	{
		$return = array(
			'title'			=> M('Automatically add a new invoice to a customer'),
			'description'	=> M('Automatically add a new invoice to a customer'),
			);
		return $return;
	}

	public function form()
	{
		$return = array();

		$return = array(
			array(
				M('When'),
				array(
					'select',
					array(
						'id'		=> 'when',
						'options'	=> array(
							array( 'invoice', M('First Invoice') ),
							array( 'purchase', M('First Purchase') ),
							array( 'activate', join(': ', array( M('Customer'), M('Activated'))) ),
							),
						)
					),
				),
			array(
				M('Item Name'),
				array(
					'text',
					array(
						'id'		=> 'item_name',
						'default'	=> 'Registration Fee',
						'attr'		=> array(
							'size'		=> 42,
							),
						)
					),
				),
			array(
				M('Quantity'),
				array(
					'text',
					array(
						'id'	=> 'quantity',
						'default'	=> 1,
						'attr'		=> array(
							'size'	=> 2,
							),
						)
					),
				),
			array(
				M('Unit Price'),
				array(
					'text',
					array(
						'id'		=> 'unit_price',
						'default'	=> 49,
						'attr'		=> array(
							'size'	=> 4,
							),
						)
					),
				),
			);
		return $return;
	}

	function run( $action_name, $object, $main_action_name, $params )
	{
		$when = isset($this->params['when']) ? $this->params['when'] : '';
		if( ! $when )
		{
			return;
		}

		switch( $when )
		{
			case 'invoice':
				$target_action = 'invoice::create';
				break;

			case 'purchase':
				$target_action = 'transaction::create';
				break;

			case 'activate':
				$target_action = 'customer::activate';
				break;
		}

		if( $action_name != $target_action )
		{
			return;
		}

		$customer_id = 0;
		$invoice = NULL;

		switch( $action_name )
		{
			case 'invoice::create':
				$customer_id = $object->getCustomerId();

				$pm =& ntsPaymentManager::getInstance();
				$already_invoices = $pm->getInvoicesOfCustomer( $customer_id );

			// only on first invoice - add this item to the invoice
			// also check if it has only cancelled appointments then add it anyway
				$ok_invoices = 0;

				foreach( $already_invoices as $iid ){
					$this_ok = 0;
					$this_invoice = ntsObjectFactory::get('invoice');
					$this_invoice->setId( $iid );

					$this_ok = 1;
					$this_invoice_items = $this_invoice->getItemsObjects();

					foreach( $this_invoice->getItemsObjects() as $inv_item ){
						switch( $inv_item->getClassName() ){
							case 'appointment':
								if( in_array($inv_item->getProp('completed'), array(HA_STATUS_CANCELLED, HA_STATUS_NOSHOW)) ){
									$this_ok = 0;
								}
								break;
						}
						if( $this_ok ){
							break;
						}
					}
					if( $this_ok ){
						$ok_invoices++;
					}

					if( $ok_invoices > 1 ){
						break;
					}
				}

				if( $ok_invoices != 1 ){
					$customer_id = 0;
				}
				$invoice = $object;
				break;

			case 'transaction::create':
				$parent_invoice = ntsObjectFactory::get('invoice');
				$parent_invoice->setId( $object->getProp('invoice_id') );
				$customer_id = $parent_invoice->getCustomerId();

				$pm =& ntsPaymentManager::getInstance();
				$already_transactions = $pm->getTransactionsOfCustomer( $customer_id );
				// only on first transaction
				if( count($already_transactions) != 1 )
				{
					$customer_id = 0;
				}
				break;

			case 'customer::activate':
				$customer_id = $object->getId();
				break;
		}

		if( ! $customer_id )
		{
			return;
		}

		$item_name = isset($this->params['item_name']) ? $this->params['item_name'] : '';
		$quantity = isset($this->params['quantity']) ? $this->params['quantity'] : '';
		$unit_price = isset($this->params['unit_price']) ? $this->params['unit_price'] : '';

		if( ! ($item_name && $quantity && $unit_price) )
		{
			return;
		}

		$cm =& ntsCommandManager::getInstance();
	/* create new or use existing */
		$new_invoice = FALSE;
		if( ! $invoice )
		{
			$new_invoice = TRUE;
			$invoice = ntsObjectFactory::get( 'invoice' );
			//$invoice->setProp( 'due_at', $due );
			$invoice->setProp( 'customer_id', $customer_id );
			$cm->runCommand( $invoice, 'create' );
		}

		$invoice_id = $invoice->getId();

		$item_array = array(
			'amount'	=> $unit_price,
			'title'		=> $item_name,
			'qty'		=> $quantity,
			'taxable'	=> 1,
			'obj_class'	=> '',
			'obj_id'	=> 0,
			);

		$cm->runCommand( 
			$invoice, 
			'add_item',
			array(
				'item'	=> $item_array
				)
			);

		if( $new_invoice )
		{
			$invoice_title = $invoice->getFullTitle();
			$msg = array( M('Invoice'), $invoice_title, M('Add'), M('OK') );
			$msg = join( ': ', $msg );
			ntsView::addAnnounce( $msg, 'ok' );
		}
	}
}
?>