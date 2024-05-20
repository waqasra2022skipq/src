<p class="text-danger">
<?php echo M('Are you sure?'); ?>
<?php echo $this->makePostParams('-current-', 'delete' ); ?>
<input class="btn btn-danger" type="submit" VALUE="<?php echo M('Delete'); ?>">