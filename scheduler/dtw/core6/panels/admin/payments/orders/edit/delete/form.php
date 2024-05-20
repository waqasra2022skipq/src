<?php
$orderId = $this->getValue('order_id');
?>
<span class="text-danger"><?php echo M('Are you sure?'); ?></span>
<?php echo $this->makePostParams('-current-', 'delete', array('order_id' => $orderId) ); ?>
<input class="btn btn-danger" type="submit" VALUE="<?php echo M('Delete'); ?>">