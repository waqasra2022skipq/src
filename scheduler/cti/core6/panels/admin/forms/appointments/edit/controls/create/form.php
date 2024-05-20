<?php
/* form params - used later for validation */
$this->setParams(
	array(
		'formId'	=> $this->getValue('form_id'),
		)
	);
$formId = $this->getValue('form_id');
?>
<table class="ntsForm">
<tbody>
<TR>
	<td class="ntsFormLabel"><?php echo M('System Name'); ?> *</td>
	<td class="ntsFormValue">
	<?php
	echo $this->makeInput (
	/* type */
		'text',
	/* attributes */
		array(
			'id'		=> 'name',
			'attr'		=> array(
				'size'	=> 16,
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
				'code'		=> 'lowercaseLetterNumberUnderscore.php', 
				'error'		=> M('Only lowercase English letters, numbers, and underscores please!'),
				),
			array(
				'code'		=> 'checkUniqueProperty.php',
				'error'		=> M('Already in use'),
				'params'	=> array(
					'class'	=> 'form_control',
					'prop'	=> 'name',
					'prefix' => 'custom_',
					'also'	=> array( 'form_id' => array('=', $formId) ),
					),
				),
			)
		);
	?>
	<i><?php echo M('Only lowercase English letters, numbers, and underscores please!'); ?></i>
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
				'size'	=> 42,
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
//					'skipMe'	=> 1,
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

<tbody>
<tr>
<td>&nbsp;</td>
<td>
<?php echo $this->makePostParams('-current-', 'create', array('formId' => $formId) ); ?>
<INPUT TYPE="submit" VALUE="<?php echo M('Create'); ?>">
</td>
</tr>
</tbody>
</table>

<SCRIPT LANGUAGE="JavaScript">
	toggleSizeControl( document.forms["<?php echo $this->getName(); ?>"]["nts-type"].value );
</SCRIPT>