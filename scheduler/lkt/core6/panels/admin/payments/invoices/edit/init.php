<?php
$id = $_NTS['REQ']->getParam( '_id' );
ntsView::setPersistentParams( array('_id' => $id), 'admin/payments/invoices/edit' );

$object = ntsObjectFactory::get( 'invoice' );
$object->setId( $id );
if( $object->notFound() )
{
	$msg = array( M('Invoice'), M('Not Found') );
	$msg = join( ': ', $msg );
	ntsView::addAnnounce( $msg, 'error' );
	$forwardTo = ntsLink::makeLink();
	ntsView::redirect( $forwardTo );
	exit;
}

ntsLib::setVar( 'admin/payments/invoices/edit::OBJECT', $object );
ntsLib::setVar( 'admin/payments/transactions::invoice', $object );

ntsView::setBack( ntsLink::makeLink('admin/payments/invoices/edit/edit', '', array('_id' => $id)), true );
?>