<?php
$is_object = ! in_array($obj_class, array('time') );
if( ! isset($per_row) )
	$per_row = 4;
$generic_child_file = dirname(__FILE__) . '/_object_child.php';
$my_child_file = dirname(__FILE__) . '/_' . $obj_class . '_child.php';
$child_file = file_exists($my_child_file) ? $my_child_file : $generic_child_file;

if( ! isset($promotions) ){
	$promotions = NULL;
}
?>

<?php if( ($obj_class == 'customer') && (! $this_id) ) : ?>
	<div class="alert alert-danger-o squeeze-in">
		<a href="<?php echo ntsLink::makeLink(); ?>">
			<?php echo M('Customer'); ?> <span class="caret"></span>
		</a>
	</div>
<?php elseif( $this_id ) : ?>
	<?php
	if( ! isset($obj) ){
		if( $is_object ){
			$obj = ntsObjectFactory::get( $obj_class );
			$obj->setId( $this_id );
		}
		else {
			$obj = $this_id;
		}
	}
	$my_errors = array();
	$alert_class = 'archive';
	if( isset($available[$this_id]) ){
		if( is_array($available[$this_id]) && $available[$this_id] ){
			$alert_class = 'danger';
			$my_errors = $available[$this_id];
		}
		elseif( $available[$this_id] )
			$alert_class = 'success';
	}
	?>
	<div class="alert alert-<?php echo $alert_class; ?> squeeze-in">
		<?php
		$info_link = '';
		if( ($obj_class == 'customer') && ($this_id) ){
			$info_link = ntsLink::makeLink('admin/customers/edit/edit', '', array('_id' => $this_id));
		}
		$params = array(
			'info_link'		=> $info_link,
			'link'			=> 0,
			'obj'			=> $obj,
			'alert_class'	=> $alert_class,
			'errors'		=> $my_errors,
			'a'				=> isset($a) ? $a : array(),
			);
		if( isset($obj_class) )
			$params['obj_class'] = $obj_class;
		echo $this->render_file(
			$child_file,
			$params
			);
		?>

		<?php if( $promotions ) : ?>
			<ul class="list-unstyled list-separated" style="margin-left: 1em;">
				<?php foreach( $promotions as $promo ) : ?>
					<?php
					$rule = $promo->getRuleView();
					?>
					<li>
						<a href="<?php echo ntsLink::makeLink('admin/company/services/promotions/browse'); ?>" target="_blank">
							<?php echo ntsView::objectTitle($promo, TRUE); ?>
						</a>
						<?php if( isset($rule['time']) ) : ?>
							<br>
							<?php echo $rule['time'][0]; ?>: <?php echo join(' ', $rule['time'][1]); ?>
						<?php endif; ?>
					</li>
				<?php endforeach; ?>
			</ul>
		<?php endif; ?>

	</div>

<?php else : ?>

	<?php if( $promotions ) : ?>
		<ul class="list-unstyled list-separated">
			<?php foreach( $promotions as $promo ) : ?>
				<?php
				$rule = $promo->getRuleView();
				?>
				<li>
					<a href="<?php echo ntsLink::makeLink('admin/company/services/promotions/browse'); ?>" target="_blank">
						<?php echo ntsView::objectTitle($promo, TRUE); ?>
					</a>
					<?php if( isset($rule['time']) ) : ?>
						<br>
						<?php echo $rule['time'][0]; ?>: <?php echo join(' ', $rule['time'][1]); ?>
					<?php endif; ?>
				</li>
			<?php endforeach; ?>
		</ul>
	<?php endif; ?>

	<?php
	$objects = array();
	if( $is_object ){
		foreach( $all_ids as $sub_id ){
			$obj = ntsObjectFactory::get( $obj_class );
			$obj->setId( $sub_id );
			if( $obj->notFound )
				continue;
			$objects[] = $obj;
		}
	}
	else {
		$objects = $all_ids;
	}
	?>
	<?php
	echo $this->render_file(
		dirname(__FILE__) . '/_object_options.php',
		array(
			'objects'	=> $objects,
			'obj_class'	=> $obj_class,
			'available'	=> $available,
			'per_row'	=> $per_row,
			'a'			=> $a,
			)
		);
	?>
<?php endif; ?>