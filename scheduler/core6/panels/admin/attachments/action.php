<?php
$parent = ntsLib::getVar( 'admin/attachments::PARENT' );
$parentClass = $parent->getClassName();
$parentId = $parent->getId();

$am = new ntsAttachManager;

$entries = $am->get( $parentClass, $parentId );
ntsLib::setVar( 'admin/attachments::entries', $entries );
?>