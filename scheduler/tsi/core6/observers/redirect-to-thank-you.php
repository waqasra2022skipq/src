<?php
class ntsObserverRedirectToThankYou extends ntsObserver
{
	public function info()
	{
		$return = array(
			'title'			=> M('Redirect to a Thank You page'),
			'description'	=> M('This one will redirect a customer to a specified Thank You page upon an appointment booking.'),
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
							array( 'first', M('First Appointment Only') ),
							array( 'all', M('All Appointments') ),
							),
						)
					),
				),
			array(
				'URL',
				array(
					'text',
					array(
						'id'		=> 'href',
						'default'	=> 'http://www.yahoo.com',
						'attr'		=> array(
							'size'		=> 42,
							),
						)
					),
				),
			);
		return $return;
	}

	function run( $action_name, $object, $main_action_name, $params )
	{
		// if( $action_name != 'appointment::_request' ){
		$actions = array('appointment::request', 'appointment::payoffline', 'appointment::payonline');
		// $actions = array('appointment::payoffline', 'appointment::payonline');
		if( ! in_array($action_name, $actions) ){
			return;
		}

		$current_user =& ntsLib::getCurrentUser();
		if( $current_user->hasRole('admin') ){
			return;
		}

		$when = isset($this->params['when']) ? $this->params['when'] : 'first';
		$href = isset($this->params['href']) ? $this->params['href'] : '';

		if( ! strlen($href) ){
			return;
		}

		switch( $when ){
			case 'first':
			/* check if it is the first appointment of the customer */
				$customer_id = $object->getProp('customer_id');

				$apps_count = ntsObjectFactory::count(
					'appointment', 
					array(
						'customer_id'	=> array('=', $customer_id)
						)
					);

				if( $apps_count > 1 ){
					return;
				}
				break;
			default:
				break;
		}

		// ok redirect
		ntsView::redirect_later( $href );
	}
}
?>