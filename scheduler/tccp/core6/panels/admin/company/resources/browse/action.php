<?php
$entries = array();

$ntsdb =& dbWrapper::getInstance();
$ids = $ntsdb->get_select_flat( 
	array('id'),
	'resources',
	array(),
	'ORDER BY archive ASC, show_order ASC, title ASC'
	);

//$entries = ntsObjectFactory::getAll( 'resource', 'ORDER BY show_order ASC, title ASC' );

$ff =& ntsFormFactory::getInstance();
$formParams = array();

foreach( $ids as $id )
{
	$obj = ntsObjectFactory::get('resource');
	$obj->setId( $id );
	$is_archive = $obj->getProp('archive');
	if( ! isset($entries[$is_archive]) )
		$entries[$is_archive] = array();
	$entries[$is_archive][] = $obj;

	$formParams['order_' . $obj->getId()] = $obj->getProp('show_order');
}

ntsLib::setVar( 'admin/company/resources::entries', $entries );

$formFile = dirname( __FILE__ ) . '/form';
$NTS_VIEW['form'] =& $ff->makeForm( $formFile, $formParams );

switch( $action )
{
	case 'update':
		if( $NTS_VIEW['form']->validate() )
		{
			$cm =& ntsCommandManager::getInstance();
			$formValues = $NTS_VIEW['form']->getValues();
			reset( $formValues );
			foreach( $formValues as $key => $order )
			{
				$id = trim( substr( $key, strlen('order_') ) );
				$object = ntsObjectFactory::get( 'resource' );
				$object->setId( $id );
				$object->setProp( 'show_order', $order );
				$cm->runCommand( $object, 'update' );
			}

			$msg = array( M('Bookable Resources'), M('Update'), M('OK') );
			$msg = join( ': ', $msg );
			ntsView::addAnnounce( $msg, 'ok' );

		/* continue to the list with anouncement */
			$forwardTo = ntsLink::makeLink( '-current-' );
			ntsView::redirect( $forwardTo );
			exit;
		}

		break;
}
?>