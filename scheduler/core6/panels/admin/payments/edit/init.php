<?php
$transId = $_NTS['REQ']->getParam('transid');
ntsView::setPersistentParams( array('transid' => $transId), 'admin/payments/edit' );

ntsLib::setVar( 'admin/payments/edit::transId', $transId );
?>