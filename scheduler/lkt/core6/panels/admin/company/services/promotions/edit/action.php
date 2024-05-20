<?php
$ff =& ntsFormFactory::getInstance();
if( ! ntsLib::hasVar('admin/company/services/promotions/edit::OBJECT') ){
	$promotion_id = $_NTS['REQ']->getParam( 'promotion_id' );

	if( $promotion_id ){
		ntsView::setPersistentParams( array('promotion_id' => $id), 'admin/company/services/promotions/edit' );

		$promotion = ntsObjectFactory::get( 'promotion' );
		$promotion->setId( $promotion_id );
		ntsLib::setVar( 'admin/company/services/promotions/edit::OBJECT', $promotion );
	}
}
$object = ntsLib::getVar( 'admin/company/services/promotions/edit::OBJECT' );

$formParams = array();
$rule = $object->getRule();

$formParams = $rule;

$tab = 'appointments';
if( isset($rule['pack']) ){
	$tab = 'packs';
}

$formParams['tab'] = $tab;
$formParams['id'] = $object->getId();
$formParams['title'] = $object->getProp( 'title' );

if( isset($rule['time']) )
{
	$formParams['time_all'] = 0;
	$formParams['from_time'] = $rule['time'][0];
	$formParams['to_time'] = $rule['time'][1];
}

if( isset($rule['date']) )
{
	$formParams['date_all'] = 0;
	if( isset($rule['date']['from']) )
	{
		$formParams['date_type'] = 'range';
		$formParams['from_date'] = $rule['date']['from'];
		$formParams['to_date'] = $rule['date']['to'];
	}
	else
	{
		$formParams['date_type'] = 'fixed';
		$formParams['fixed_date'] = $rule['date'];
	}
}

$formParams['sign'] = $object->getSign();
$formParams['amount'] = $object->getAmount();
$formParams['measure'] = $object->getMeasure();

$currentCoupons = $object->getCoupons();
$currentCodes = $object->getCouponCodes();

$formParams['coupon_required'] = $currentCoupons ? 1 : 0;
$formParams['coupon'] = join( "\n", $currentCodes );
$formParams['coupon_limit'] = $currentCoupons ? $currentCoupons[0]->getProp('use_limit') : 0;

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
						'code'			=> array( '=', $c ),
						'promotion_id'	=> array( '<>', $object->getId() ),
						);
					$cCount = $ntsdb->count( 'coupons', $where );
					if( $cCount )
					{
						$msg = $c . ': ' . M('Already in use');
						ntsView::addAnnounce( $msg, 'error' );
						$couponError = TRUE;
					}
				}
			}

			if( $couponError )
			{
				break;
			}

		/* rules */
			// $rule = array();
			switch( $tab ){
				case 'appointments':
					unset($rule['pack']);
					$grab = array('location', 'resource', 'service', 'weekday');
					foreach( $grab as $gr )
					{
						if( isset($formValues[$gr]) )
						{
							if( in_array(-1, $formValues[$gr]) ){
								unset($rule[$gr]);
							}
							else {
								$rule[$gr] = $formValues[$gr];
							}
						}
					}

					if( (! isset($formValues['time_all'])) OR (! $formValues['time_all']) )
					{
						$rule['time'] = array($formValues['from_time'], $formValues['to_time']);
					}

					if( isset($formValues['time_all']) && $formValues['time_all']){
						unset($rule['time']);
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
					$rule = array();
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
				$object->setProp( 'price', $price );
				$object->setRule( $rule );
				$object->setProp( 'title', $formValues['title'] );

				$cm->runCommand( $object, 'update' );

				if( $cm->isOk() ){
				/* delete missing */
					$where = array(
						'code'			=> array( 'NOT IN', $finalCoupons, '', TRUE ),
						'promotion_id'	=> array( '=', $object->getId() ),
						);
					$ntsdb->delete( 'coupons', $where );
					$deletedCount = $ntsdb->affectedRows();

				/* update current */
					$what = array(
						'use_limit'	=> $formValues['coupon_limit'],
						);
					$where = array(
						'code'			=> array( 'IN', $finalCoupons, '', TRUE ),
						'promotion_id'	=> array( '=', $object->getId() ),
						'use_limit'		=> array( '<>', $formValues['coupon_limit'] ),
						);
					$ntsdb->update( 'coupons', $what, $where );
					$updatedCount = $ntsdb->affectedRows();

				/* add new */
					$addedCount = 0;
					reset( $finalCoupons );
					foreach( $finalCoupons as $c )
					{
						if( ! in_array($c, $currentCodes) )
						{
							$coupon = ntsObjectFactory::get( 'coupon' );
							$coupon->setProp( 'code', $c );
							$coupon->setProp( 'use_limit', $formValues['coupon_limit'] );
							$coupon->setProp( 'promotion_id', $object->getId() );
							$cm->runCommand( $coupon, 'create' );
							$addedCount++;
						}
					}

					if( $addedCount > 0 )
					{
						$msg = array( $addedCount, M('Coupon Codes'), M('Create'), M('OK') );
						$msg = join( ': ', $msg );
						ntsView::addAnnounce( $msg, 'ok' );
					}
					if( $deletedCount > 0 )
					{
						$msg = array( $deletedCount, M('Coupon Codes'), M('Delete'), M('OK') );
						$msg = join( ': ', $msg );
						ntsView::addAnnounce( $msg, 'ok' );
					}
					if( $updatedCount > 0 )
					{
						$msg = array( $updatedCount, M('Coupon Codes'), M('Update'), M('OK') );
						$msg = join( ': ', $msg );
						ntsView::addAnnounce( $msg, 'ok' );
					}

					$msg = array( M('Promotion'), M('Update'), M('OK') );
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