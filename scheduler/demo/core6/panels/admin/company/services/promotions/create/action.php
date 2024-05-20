<?php
$ntsdb =& dbWrapper::getInstance();
$ff =& ntsFormFactory::getInstance();

$rule = array();

$formParams = array(
	'date_type'		=> 'range', // can be range|fixed
	);

if( ntsLib::hasVar( 'admin/company/services/promotions::customer') ){
	$customer = ntsLib::getVar( 'admin/company/services/promotions::customer' );
	$rule['customer'] = array($customer->getId());
	$formParams['title'] = ntsView::objectTitle($customer) . ': ';
}

$formFile = dirname(__FILE__) . '/../form';
$NTS_VIEW['form'] =& $ff->makeForm( $formFile, $formParams );

switch( $action ){
	case 'save':
		$removeValidation = array();

		$couponRequired = $_NTS['REQ']->getParam( 'coupon_required' );
		if( ! $couponRequired )
		{
			$removeValidation[] = 'coupon';
			$removeValidation[] = 'coupon_limit';
		}

		$tab = $_NTS['REQ']->getParam( 'tab' );
		if( ! $tab ){
			$tab = 'appointments';
		}

		switch( $tab ){
			case 'appointments':
				if( $_NTS['REQ']->getParam( 'time_all' ) )
				{
					$removeValidation[] = 'from_time';
					$removeValidation[] = 'to_time';
				}
				if( $_NTS['REQ']->getParam( 'date_all' ) )
				{
					$removeValidation[] = 'from_date';
					$removeValidation[] = 'to_date';
					$removeValidation[] = 'fixed_date';
				}
				else
				{
					$dateType = $_NTS['REQ']->getParam( 'date_type' );
					switch( $dateType )
					{
						case 'fixed':
							$removeValidation[] = 'from_date';
							$removeValidation[] = 'to_date';
							break;
						case 'range':
							$removeValidation[] = 'fixed_date';
							break;
					}
				}
				break;

			case 'packs':
				$removeValidation[] = 'from_time';
				$removeValidation[] = 'to_time';
				$removeValidation[] = 'from_date';
				$removeValidation[] = 'to_date';
				$removeValidation[] = 'fixed_date';
				break;
		}

		if( $NTS_VIEW['form']->validate($removeValidation) ){
			$formValues = $NTS_VIEW['form']->getValues();

		/* price */
			$price = $formValues['sign'] . $formValues['amount'] . $formValues['measure'];

		/* coupons */
			$coupon = '';
			$couponRule = array();
			$couponError = FALSE;
			$finalCoupons = array();
			if( $couponRequired )
			{
				$couponRule['limit'] = $formValues['coupon_limit'];

				$coupons = trim( $formValues['coupon'] );
				$coupons = explode( "\n", $coupons );
				reset( $coupons );
				foreach( $coupons as $c )
				{
					$c = trim( $c );
					if( $c )
						$finalCoupons[] = $c;
				}

				reset( $finalCoupons );
				foreach( $finalCoupons as $c )
				{
					/* check if this code is already registered */
					$where = array(
						'code'	=> array( '=', $c )
						);
					$cCount = $ntsdb->count( 'coupons', $where );
					if( $cCount )
					{
						$msg = $c . ': ' . M('Already in use');
						ntsView::addAnnounce( $msg, 'error' );
						$couponError = TRUE;
						break;
					}
				}
			}

			if( $couponError )
			{
				break;
			}

		/* rules */
			switch( $tab ){
				case 'appointments':
					$grab = array('location', 'resource', 'service', 'weekday');
					foreach( $grab as $gr )
					{
						if( isset($formValues[$gr]) && (! in_array(-1, $formValues[$gr])) )
						{
							$rule[$gr] = $formValues[$gr];
						}
					}

					if( (! isset($formValues['time_all'])) OR (! $formValues['time_all']) )
					{
						$rule['time'] = array($formValues['from_time'], $formValues['to_time']);
					}

					if( (! isset($formValues['date_all'])) OR (! $formValues['date_all']) )
					{
						$dateType = $formValues['date_type'];
						switch( $dateType )
						{
							case 'fixed':
								$rule['date'] = $formValues['fixed_date'];
								break;
							case 'range':
								$rule['date'] = array(
									'from'	=> $formValues['from_date'],
									'to'	=> $formValues['to_date'],
									);
								break;
						}
					}
					break;

				case 'packs':
					$grab = array('pack');
					foreach( $grab as $gr )
					{
						if( isset($formValues[$gr]) )
						{
							$rule[$gr] = $formValues[$gr];
						}
					}
					break;
			}

			if( (! $rule) && (! $finalCoupons) ){
				$msg = M('Please choose at least 1 option');
				ntsView::addAnnounce( $msg, 'error' );
				}
			else {
				$cm =& ntsCommandManager::getInstance();
				$object = ntsObjectFactory::get( 'promotion' );
				$object->setProp( 'price', $price );

				$object->setRule( $rule );
				$object->setProp( 'title', $formValues['title'] );

				$cm->runCommand( $object, 'create' );

				if( $cm->isOk() ){
					$id = $object->getId();

				/* create coupons */
					$finalCouponsCount = 0;
					reset( $finalCoupons );
					foreach( $finalCoupons as $c )
					{
						$coupon = ntsObjectFactory::get( 'coupon' );
						$coupon->setProp( 'code', $c );
						$coupon->setProp( 'use_limit', $formValues['coupon_limit'] );
						$coupon->setProp( 'promotion_id', $id );
						$cm->runCommand( $coupon, 'create' );
						$finalCouponsCount++;
					}

					if( $finalCouponsCount )
					{
						$msg = array( $finalCouponsCount, M('Coupon Codes'), M('Create'), M('OK') );
						$msg = join( ': ', $msg );
						ntsView::addAnnounce( $msg, 'ok' );
					}

					$msg = array( M('Promotion'), M('Create'), M('OK') );
					$msg = join( ': ', $msg );
					ntsView::addAnnounce( $msg, 'ok' );

				/* continue to the list with anouncement */
					$forwardTo = ntsLink::makeLink( '-current-/../browse' );
					ntsView::redirect( $forwardTo );
					exit;
					}
				else {
					$errorText = $cm->printActionErrors();
					ntsView::addAnnounce( $errorText, 'error' );
					}
				}
			}
		else {
		/* form not valid, continue to create form */
			}
		break;
	default:
		break;
	}
?>