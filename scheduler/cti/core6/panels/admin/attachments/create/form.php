<?php
$am = new ntsAttachManager;
?>

<ul class="list-unstyled">
	<li class="text-warning">
		<?php echo M('Allowed Types'); ?>: <strong><?php echo join( ', ', $am->allowed_types ); ?></strong>
	</li>
	<?php if( $am->max_size > 0 ) : ?>
		<li class="text-warning">
			<?php echo M('Max Size'); ?>: <strong><?php echo ntsLib::humanFilesize($am->max_size * 1024, 0); ?></strong>
		</li>
	<?php endif; ?>
</ul>

<?php if( $error = $am->get_error() ) : ?>
	<p class="text-danger">
	<?php echo $error; ?>
<?php else : ?>
	<p>
	<?php
	echo $this->makeInput (
	/* type */
		'upload',
	/* attributes */
		array(
			'id'	=> 'attach',
			),
	/* validators */
		array(
			)
		);
	?>

	<p>
	<?php echo $this->makePostParams('-current-', 'create' ); ?>
	<INPUT class="btn btn-default" TYPE="submit" VALUE="<?php echo M('Add'); ?>">
<?php endif; ?>