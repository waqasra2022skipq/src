<?php
$val = new ntsValidator;

$ntsdb =& dbWrapper::getInstance();
$ff =& ntsFormFactory::getInstance();
$cm =& ntsCommandManager::getInstance();

$id = $_NTS['REQ']->getParam( '_id' );
$form = new ntsObject('form');
$form->setId( $id );

/* super count */
$sql =<<<EOT
SELECT COUNT(*) AS count FROM {PRFX}form_controls WHERE form_id = $id
EOT;
$result = $ntsdb->runQuery( $sql );
if( $result ){
	$e = $result->fetch();
	$totalCount = $e['count'];
	}

$NTS_VIEW['fields'] = array();
/* fields info */
$sql =<<<EOT
SELECT
	*
FROM
	{PRFX}form_controls
WHERE
	form_id = $id
ORDER BY
	show_order ASC
EOT;
$result = $ntsdb->runQuery( $sql );
while( $c = $result->fetch() ){
	$NTS_VIEW['fields'][] = $c;
	}
?>
<?php
$om =& objectMapper::getInstance();

$fieldTypeNames = array(
	'text'		=>	M('Text'),
	'checkbox'	=>	M('Yes') . '/' . M('No'),
	'textarea'	=>	M('Textarea'),
	'select'	=>	M('Select'),
	);

$accessTypes = array(
	'hidden'	=>	M('Hidden'),
	'read'		=>	M('View Only'),
	'write'		=>	M('View and Update'),
	);

list( $coreProps, $metaProps ) = $om->getPropsForClass( 'user' );
$biltInFields = array_keys( $coreProps );
?>

<p>
<div class="nts-ajax-parent">
<?php
echo ntsLink::printLink(
	array(
		'panel'		=> '-current-/create',
		'title'		=> '<i class="fa fa-plus"></i> ' . M('Form Field') . ': ' . M('Add'),
		'attr'		=> array(
			'class'	=> 'nts-ajax-loader btn btn-success',
			),
		)
	);
?>
<div class="nts-ajax-container nts-child"></div>
</div>

<p>
<?php if( ! count($NTS_VIEW['fields'])) : ?>
	<?php echo M('None'); ?>
<?php else : ?>
	<table class="table table-striped2 table-condensed">
	<tbody class="nts-ajax-parent">
	<tbody>
	<tr class="listing-header">
		<th><?php echo M('Name'); ?></th>
		<th><?php echo M('Type'); ?></th>
		<th><?php echo M('External User Access'); ?></th>
		<th><?php echo M('Validation'); ?></th>
		<th><?php echo M('Actions'); ?></th>
	</tr>

	<?php $count = 0; ?>
	<?php foreach( $NTS_VIEW['fields'] as $e ) : ?>
	<tr>
		<td>
			<a href="<?php echo ntsLink::makeLink('-current-/edit', '', array('id' => $e['id']) ); ?>"><?php echo $e['title']; ?></a>
		</td>
		<td>
			<?php echo ( isset($fieldTypeNames[$e['type']]) ) ? $fieldTypeNames[$e['type']] : $e['type']; ?>
		</td>

		<td>
			<?php echo ( isset($accessTypes[$e['ext_access']]) ) ? $accessTypes[$e['ext_access']] : $e['ext_access']; ?>
		</td>

		<td>
			<?php if( $e['validators'] && ( $validators = hc_mb_unserialize($e['validators']) )) : ?>
				<?php if( count($validators) == 1 ) : ?>
					<?php
					$vi = $val->getValidatorInfo( $validators[0]['code'] );
					echo $vi[1];
					?>
				<?php else : ?>
					<?php echo M('Validations'); ?>: <?php echo count($validators); ?>
				<?php endif; ?>
			<?php else : ?>
				<?php echo M('None'); ?>
			<?php endif; ?>
		</td>

		<td>
			<a class="ok" href="<?php echo ntsLink::makeLink('-current-', 'control_up', array('control' => $e['id']) ); ?>"><?php echo M('Up'); ?></a>
			<a class="ok" href="<?php echo ntsLink::makeLink('-current-', 'control_down', array('control' => $e['id']) ); ?>"><?php echo M('Down'); ?></a>
		<?php if( ! in_array($e['name'], $biltInFields) ) : ?>
			<a class="alert" href="<?php echo ntsLink::makeLink('-current-/delete', '', array('id' => $e['id']) ); ?>"><?php echo M('Delete'); ?></a>
		<?php endif; ?>
		</td>
	</tr>
	<?php endforeach; ?>
	</tbody>
	</table>
<?php endif; ?>
