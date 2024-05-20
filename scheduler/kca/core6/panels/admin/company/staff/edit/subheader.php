<?php
$object = ntsLib::getVar( 'admin/company/staff/edit::OBJECT' );
?>
<h2>
<?php echo ntsView::objectTitle( $object, TRUE ); ?>
<br><small class="text-muted" style="font-size: 1rem;">id: <?php echo $object->getId(); ?></small>
</h2>