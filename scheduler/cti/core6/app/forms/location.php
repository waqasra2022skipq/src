<?php
$id = $this->getValue('id');
$object = $this->getValue('object');
$is_archive = $id ? $object->getProp('archive') : 0;
?>
<?php if( $id ) : ?>
	<?php
	$is_archive = $object->getProp('archive');

	$status_view = '<span class="label label-success">' . M('Active') . '</span>';
	if( $is_archive )
	{
		$status_view = '<span class="label label-archive">' . M('Archived') . '</span>';
	}
	echo ntsForm::wrapInput(
		M('Status'),
		$status_view
		);
	?>
<?php endif; ?>

<?php
echo ntsForm::wrapInput(
	M('Title') . ' *',
	$this->buildInput(
	/* type */
		'text',
	/* attributes */
		array(
			'id'		=> 'title',
			'attr'		=> array(
				'size'	=> 20,
				),
			'default'	=> '',
			'required'	=> 1,
			),
	/* validators */
		array(
			array(
				'code'		=> 'notEmpty.php', 
				'error'		=> M('Required'),
				),
			array(
				'code'		=> 'checkUniqueProperty.php', 
				'error'		=> M('Already in use'),
				'params'	=> array(
					'prop'	=> 'title',
					'class'	=> 'location',
					'skipMe'	=> 1
					),
				),
			)
		)
	);
?>
<?php
echo ntsForm::wrapInput(
	M('Description'),
	$this->buildInput (
	/* type */
		'textarea',
	/* attributes */
		array(
			'id'		=> 'description',
			'attr'		=> array(
				'cols'	=> 20,
				'rows'	=> 6,
				),
			'default'	=> '',
			),
	/* validators */
		array(
			)
		)
	);
?>
<?php
echo ntsForm::wrapInput(
	M('Capacity'),
	$this->buildInput (
	/* type */
		'text',
	/* attributes */
		array(
			'id'		=> 'capacity',
			'attr'		=> array(
				'size'	=> 3,
				),
			'default'	=> 0,
			'help'		=> M('Enter 0 for no limit'),
			'after'		=> M('Seats'),
			),
	/* validators */
		array(
			array(
				'code'		=> 'notEmpty.php', 
				'error'		=> M('Required'),
				),
			array(
				'code'		=> 'integer.php', 
				'error'		=> M('Numbers only'),
				),
			)
		)
	);
?>

<?php echo $this->makePostParams('-current-', 'save'); ?>
<?php
$btn_label = $id ? M('Save') : M('Add');

$buttons = array();
$buttons[] = '<ul class="list-inline">';
$buttons[] = '<li>';
$buttons[] = '<INPUT class="btn btn-success" TYPE="submit" value="' . $btn_label . '">';
$buttons[] = '</li>';
if( $id )
{
	$buttons[] = '<li class="divider"></li>';
	$buttons[] = '<li>';
	$archive_link = ntsLink::makeLink('-current-', 'archive');
	$buttons[] = '<a href="' . $archive_link . '" class="btn btn-sm btn-archive" TYPE="submit" title="' . M('Archive') . '">';

	if( $is_archive )
	{
		$buttons[] = M('Activate');
	}
	else
	{
		$buttons[] = M('Archive');
	}

	$buttons[] = '</a>';
	$buttons[] = '</li>';
}

$buttons[] = '</ul>';
?>
<?php 
echo ntsForm::wrapInput(
	'',
	$buttons
	);
?>