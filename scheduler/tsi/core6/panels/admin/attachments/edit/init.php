<?php
$attachId = $_NTS['REQ']->getParam('attachid');
ntsLib::setVar( 'admin/attachments/edit::attachId', $attachId );
?>