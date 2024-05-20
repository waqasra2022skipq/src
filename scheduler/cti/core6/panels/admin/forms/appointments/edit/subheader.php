<?php
$id = $_NTS['REQ']->getParam( '_id' );
ntsView::setPersistentParams( array('_id' => $id), 'admin/forms/appointments/edit' );

$object = new ntsObject( 'form' );
$object->setId( $id );
?>
<h2><small><?php echo M('Custom Form'); ?>: <?php echo M('Appointment'); ?></small> <?php echo ntsView::objectTitle($object); ?></h2>