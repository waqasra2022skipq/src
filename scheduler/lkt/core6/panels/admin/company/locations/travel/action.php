<?php
$ff =& ntsFormFactory::getInstance();

$entries = ntsObjectFactory::getAll( 'location', 'ORDER BY show_order ASC, title ASC' );
ntsLib::setVar( 'admin/company/locations::entries', $entries );

$currentTravel = array();

$formParams = array();
reset( $entries );
for( $ii = 0; $ii < count($entries); $ii++ ){
	$travel = $entries[$ii]->getProp('_travel');
	$currentTravel[ $entries[$ii]->getId() ] = $travel;

	$key = 'travel-' . 0 . '-' . $entries[$ii]->getId();
	$value = isset( $travel[0] ) ? $travel[0] : 0;
	$formParams[ $key ] = $value;
	}
for( $ii = 0; $ii < count($entries); $ii++ ){
	$travel = $entries[$ii]->getProp('_travel');
	for( $jj = ($ii + 1); $jj < count($entries); $jj++ ){
		$key = 'travel-' . $entries[$ii]->getId() . '-' . $entries[$jj]->getId();
		$value = isset($travel[$entries[$jj]->getId()]) ? $travel[$entries[$jj]->getId()] : 0;
		$formParams[ $key ] = $value;
		}
	}

$formFile = dirname( __FILE__ ) . '/form';
$NTS_VIEW['form'] =& $ff->makeForm( $formFile, $formParams );

switch( $action ){
	case 'update':
		if( $NTS_VIEW['form']->validate() ){
			$cm =& ntsCommandManager::getInstance();
			$formValues = $NTS_VIEW['form']->getValues();
			$formValues = $NTS_VIEW['form']->getValues();

			reset( $formValues );
			foreach( $formValues as $key => $value ){
				list( $lala, $fromId, $toId ) = explode( '-', $key );

				if( $fromId > 0 ){
					$currentTravel[ $fromId ][ $toId ] = $value;
					}
				$currentTravel[ $toId ][ $fromId ] = $value;
				}

			for( $ii = 0; $ii < count($entries); $ii++ ){
				$entries[$ii]->setProp( '_travel', $currentTravel[$entries[$ii]->getId()] ); 
				$cm->runCommand( $entries[$ii], 'update' );
				}
			$msg = array( M('Travel Time'), M('Update'), M('OK') );
			$msg = join( ': ', $msg );
			ntsView::addAnnounce( $msg, 'ok' );
			}
	break;
	}
?>