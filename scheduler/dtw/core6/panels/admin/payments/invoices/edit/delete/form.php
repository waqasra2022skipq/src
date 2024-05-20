<H3><?php echo M('Are you sure?'); ?></H3>

<p>
<?php echo $this->makePostParams('-current-', 'delete' ); ?>
<input class="btn btn-danger" type="submit" VALUE="<?php echo M('Delete'); ?>">
</p>