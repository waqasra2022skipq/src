<?php
$iCanEdit = ntsLib::getVar( 'admin/attachments::iCanEdit' );

if( ! $iCanEdit ){
	$msg = M('Edit') . ': ' . M('Permission Denied');
	ntsView::addAnnounce( $msg, 'error' );

	/* continue */
	ntsView::getBack( true );
	exit;
	}
?>