<?php
$object->setProp( 'is_active', 1 );
$this->runCommand( $object, 'update' );
$actionResult = 1;

$packId = $object->getProp('pack_id');
$pack = ntsObjectFactory::get( 'pack' );
$pack->setId( $packId );
$packTitle = $pack->getFullTitle();

$msg = array( M('Package'), $packTitle, M('Active'), M('OK') );
$msg = join( ': ', $msg );

ntsView::addAnnounce( $msg, 'ok' );
?>