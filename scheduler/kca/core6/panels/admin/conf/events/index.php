<div class="page-header">
	<h2>
	<?php echo M('Event Actions'); ?>
	</h2>
</div>

<?php
$form = new ntsForm2;
?>

<?php echo $form->start(TRUE); ?>

<ul class="list-unstyled list-separated">
<?php foreach( $observers as $key => $obs ) : ?>
	<?php
	$info = $obs->info();
	$this_form = $obs->form();
	$is_on = in_array($key, $active_observers) ? 1 : 0;
	$no_valid = $obs->is_not_valid();
	if( $is_on OR $no_valid )
	{
		$collapse_in = ' in';
	}
	else
	{
		$collapse_in = '';
	}

	if( $no_valid )
	{
		$is_on = 0;
	}
	?>
	<li>
		<div class="collapse-panel panel panel-default">

			<div class="panel-heading">
				<label>
					<?php if( ! $no_valid ) : ?>
						<?php
						echo $form->input(
							'checkbox',
							array(
								'id'			=> 'enable_' . $key,
								'value'			=> $is_on,
								'attr'	=> array(
									'data-toggle'	=> 'collapse-next',
									)
								)
							);
						?>
					<?php endif; ?>
					<?php echo $info['title']; ?>
				</label>
			</div>

			<div class="panel-collapse collapse<?php echo $collapse_in; ?>">
				<div class="panel-body">
					<?php if( ! $no_valid ) : ?>
						<p>
							<?php echo $info['description']; ?>
						</p>
					<?php else : ?>
						<p class="text-danger">
							<?php echo $no_valid; ?>
						</p>
					<?php endif; ?>

					<?php if( $this_form ) : ?>
						<?php foreach( $this_form as $fi ) : ?>
							<?php
							if( isset($observer_params[$key][$fi[1][1]['id']]) )
							{
								$fi[1][1]['value'] = $observer_params[$key][$fi[1][1]['id']];
							}
							$fi[1][1]['id'] = 'param_' . $key . '_' . $fi[1][1]['id'];

							echo ntsForm::wrapInput(
								$fi[0],
								$form->build_input(
									$fi[1][0],
									$fi[1][1]
									)
								);
							?>
						<?php endforeach; ?>
					<?php endif; ?>
				</div>
			</div>
		</div>
	</li>
<?php endforeach; ?>
</ul>


<?php
echo $form->make_post_params('admin/conf/events', 'update');
?>
<input class="btn btn-default" type="submit" value="<?php echo M('Save'); ?>">
<?php echo $form->end(); ?>

