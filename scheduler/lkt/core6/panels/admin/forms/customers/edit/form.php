<?php
/* form params - used later for validation */
$this->setParams(
	array(
		'myId'		=> $this->getValue('id'),
		'formId'	=> $this->getValue('form_id'),
		)
	);
$formId = $this->getValue('form_id');
$addValidator = $this->getValue('add_validator');
?>
<table class="ntsForm">
<tbody>
<TR>
	<td class="ntsFormLabel"><?php echo M('System Name'); ?></td>
	<td class="ntsFormValue">
	<?php echo $this->getValue( 'name' ); ?>
	</TD>
</TR>
<TR>
	<td class="ntsFormLabel"><?php echo M('Title'); ?> *</td>
	<td class="ntsFormValue">
	<?php
	echo $this->makeInput (
	/* type */
		'text',
	/* attributes */
		array(
			'id'		=> 'title',
			'attr'		=> array(
				'size'	=> 32,
				),
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
					'class'	=> 'form_control',
					'prop'	=> 'title',
					'skipMe'	=> 1,
					'also'	=> array( 'form_id' => array('=', $formId) ),
					),
				),
			)
		);
	?>
	</TD>
</TR>

<TR>
	<td class="ntsFormLabel"><?php echo M('Help Text'); ?> (<?php echo M('Optional'); ?>)</td>
	<td class="ntsFormValue">
	<?php
	echo $this->makeInput (
	/* type */
		'text',
	/* attributes */
		array(
			'id'		=> 'description',
			'attr'		=> array(
				'size'	=> 42,
				),
			)
		);
	?>
	</TD>
</TR>

<TR>
	<td class="ntsFormLabel"><?php echo M('External User Access'); ?></td>
	<td class="ntsFormValue">
	<?php
	echo $this->makeInput (
	/* type */
		'accessType',
	/* attributes */
		array(
			'id'		=> 'ext_access',
			)
		);
	?>
	</TD>
</TR>

<TR>
	<td class="ntsFormLabel"><?php echo M('Type'); ?></td>
	<td class="ntsFormValue">
<?php
echo $this->makeInput (
/* type */
	'fieldType',
/* attributes */
	array(
		'id'	=> 'type',
		)
	);
?>
</td>
</tr>
</tbody>

<?php
$fieldTypeOptionsFile = NTS_LIB_DIR . '/lib/form/inputs/requireFieldTypeOptions.php';
require( $fieldTypeOptionsFile );
?>

<?php $myType = $this->getValue('type'); ?>
<?php if( 1 || $myType != 'checkbox' ) : ?>

<tbody>
<tr>
<td class="ntsFormValue" colspan="2">

<p>
<h3><?php echo M('Input Validation'); ?></h3>
<p>
<table>
<tr class="listing-header">
	<th><?php echo M('Validation'); ?></th>
	<th><?php echo M('Error Message If Validation Fails'); ?></th>
	<th>&nbsp;</th>
</tr>
<?php
$ntsValidator = new ntsValidator;
$allValidators = $ntsValidator->getValidatorsFor( $this->getValue('type') );

$currentValidators = $this->getValue('validators');

$currentValidatorsNames = array_map( create_function('$a', 'return $a["code"];'), $currentValidators );
$remainValidators = array();
reset( $allValidators );
foreach( $allValidators as $vn => $va ){
	if( ! in_array($vn, $currentValidatorsNames) )
	$remainValidators[] = $va;
	}

reset( $currentValidators );
$vCount = 0;
?>
<?php $count = 0; ?>
<?php foreach( $currentValidators as $cv ) : ?>
<tr>
	<?php
	if( ! isset($allValidators[$cv['code']]) )
		continue;
	$vi = $allValidators[$cv['code']];
	$vCount++;
	$title = $vi[1];
	?>
	<td>
		<b><?php echo $title; ?></b>
	</td>
	<td>
	<?php
	echo $this->makeInput (
	/* type */
		'hidden',
	/* attributes */
		array(
			'id'		=> 'vld-' . 	$vCount,
			'default'	=> $cv['code'],
			)
		);
	?>
	<?php
	echo $this->makeInput (
	/* type */
		'text',
	/* attributes */
		array(
			'id'		=> 'error-' . 	$vCount,
			'default'	=> $cv['error'],
			'attr'		=> array(
				'size'	=> 42,
				),
			'required'	=> 1,
			),
	/* validators */
		array(
			array(
				'code'		=> 'notEmpty.php', 
				'error'		=> 'Please enter the error message text',
				),
			)
		);
	?>
	</td>
	<td>
		<a class="alert" href="<?php echo ntsLink::makeLink('-current-', 'delete_validator', array('id' => $this->getValue('id'), 'validator' => $vCount) ); ?>"><?php echo M('Delete'); ?></a>
	</td>
</tr>
<?php endforeach; ?>
<tr>
<?php if( $addValidator ) : ?>
	<?php 
		$vCount++;
		reset( $remainValidators );
		$chooseOptions = array();
		foreach( $remainValidators as $rv ){
			$chooseOptions[] = array( $rv[0], $rv[1] );
			}
	?>
	<td class="ntsFormLabel">
		<?php
		echo $this->makeInput (
		/* type */
			'select',
		/* attributes */
			array(
				'id'		=> 'vld-' . $vCount,
				'options'	=> $chooseOptions,
				'required'	=> 1,
				),
		/* validators */
			array(
				array(
					'code'		=> 'notEmpty.php', 
					'error'		=> 'Please enter the error message text',
					),
				)
			);
		?>
	</td>
	<td>
		<?php
		echo $this->makeInput (
		/* type */
			'text',
		/* attributes */
			array(
				'id'		=> 'error-' . 	$vCount,
				'attr'		=> array(
					'size'	=> 42,
					),
				'required'	=> 1,
				),
		/* validators */
			array(
				array(
					'code'		=> 'notEmpty.php', 
					'error'		=> 'Please enter the error message text',
					),
				)
			);
		?>
	</td>
	<td>
		&nbsp;
	</td>	
<?php else : ?>
	<td colspan="3">
		<?php if( count($remainValidators) ) : ?>
			<a class="ok" href="<?php echo ntsLink::makeLink('-current-', '', array('id' => $this->getValue('id'), 'add_validator' => 1) ); ?>"><?php echo M('Add'); ?></a>
		<?php endif; ?>
	</td>
<?php endif; ?>
</tr>
</table>

<?php endif; ?>

</td>
</tr>


<tbody>
<tr>
<td>&nbsp;</td>
<td>
<?php echo $this->makePostParams('-current-', 'update', array('id' => $this->getValue('id'), 'add_validator' => $addValidator) ); ?>
<input class="btn btn-default" type="submit" value="<?php echo M('Save'); ?>">
</td>
</tr>
</tbody>
</table>

<SCRIPT LANGUAGE="JavaScript">
	toggleSizeControl( document.forms["<?php echo $this->getName(); ?>"]["nts-type"].value );
</SCRIPT>