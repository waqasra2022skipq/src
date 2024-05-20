<?php
$object = ntsLib::getVar( 'admin/manage/appointments/edit::OBJECT' );

include_once( NTS_APP_DIR . '/helpers/ical.php' );
$ntsCal = new ntsIcal();
// $ntsCal->setTimezone( NTS_COMPANY_TIMEZONE );
$current_user =& ntsLib::getCurrentUser();
$ntsCal->setTimezone( $current_user->getTimezone() );
$ntsCal->addAppointment( $object );
$str = $ntsCal->printOut();

$fileName = 'appointment-' . $object->getId() . '.ics';
ntsLib::startPushDownloadContent( $fileName );
echo $str;
exit;
?>