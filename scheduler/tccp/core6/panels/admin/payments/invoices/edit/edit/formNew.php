<?php
$ntsconf =& ntsConf::getInstance();
$taxRate = $ntsconf->get('taxRate');
?>
<tr>
<td style="text-align: left;">
<?php
echo $this->makeInput (
/* type */
	'text',
/* attributes */
	array(
		'id'	=> 'title',
		'attr'		=> array(
			'size'	=> 42,
			),
		'errorBlock'	=> 1,
		'default'	=> M('New Item'),
		),
	/* validators */
	array(
		array(
			'code'		=> 'notEmpty.php', 
			'error'		=> M('Required'),
			)
		)
	);
?>
</td>

<td style="text-align: center;">
<?php
echo $this->makeInput (
/* type */
	'text',
/* attributes */
	array(
		'id'	=> 'qty',
		'attr'		=> array(
			'size'	=> 2,
			),
		'errorBlock'	=> 1,
		),
	/* validators */
	array(
		array(
			'code'		=> 'notEmpty', 
			'error'		=> M('Required'),
			),
		array(
			'code'		=> 'number', 
			'error'		=> M('Numbers only'),
			),
		)
	);
?>
</td>

<td style="text-align: center;">
<?php
echo $this->makeInput (
/* type */
	'text',
/* attributes */
	array(
		'id'	=> 'amount',
		'attr'		=> array(
			'size'	=> 5,
			),
		'errorBlock'	=> 1,
		),
	/* validators */
	array(
		array(
			'code'		=> 'notEmpty', 
			'error'		=> M('Required'),
			),
		array(
			'code'		=> 'number', 
			'error'		=> M('Numbers only'),
			),
		)
	);
?>
</td>

<?php if( $taxRate ) : ?>
	<td style="text-align: center;">
	<?php
	echo $this->makeInput (
	/* type */
		'checkbox',
	/* attributes */
		array(
			'id'		=> 'taxable',
			'default'	=> 1,
			)
		);
	?>
	</td>
<?php endif; ?>

<td>
<?php echo $this->makePostParams('-current-', 'add' ); ?>
<INPUT class="btn btn-default" TYPE="submit" VALUE="<?php echo M('Add'); ?>">
</td>

</tr>