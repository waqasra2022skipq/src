<?php
$object = ntsLib::getVar( 'admin/manage/appointments/edit::OBJECT' );

$nam =& ntsAccountingManager::getInstance();

$coupon_id = $_NTS['REQ']->getParam('coupon_id');
$appointment_id = $object->getId();

// bug: this deletes all these coupon applies
// $where = array(
	// 'obj_class'	=> array('=', 'coupon'),
	// 'obj_id'	=> array('=', $coupon_id),
	// 'action'	=> array('=', 'apply'),
	// );

// find journal entries
$where = array(
	'obj_class'	=> array('=', 'coupon'),
	'obj_id'	=> array('=', $coupon_id),
	'action'	=> array('=', 'apply'),
	);

$ntsdb =& dbWrapper::getInstance();
$all_journal_ids = $ntsdb->get_select( 'id', 'accounting_journal', $where );

$where = array(
	'journal_id'	=> array('IN', $all_journal_ids),
	'account_type'	=> array('=', 'appointment'),
	'account_id'	=> array('=', $appointment_id),
	);

$journal_ids = $ntsdb->get_select( 'journal_id', 'accounting_posting', $where );

$where = array(
	'id'	=> array('IN', $journal_ids),
	);
$nam->delete_journal( $where );

$msg = M('OK');
ntsView::addAnnounce( $msg, 'ok' );

$forwardTo = ntsLink::makeLink( '-current-' );
ntsView::redirect( $forwardTo );
exit;
?>