<TABLE>
<tr>
	<th>Username *</th>
	<TD>
	<?php
	echo $this->makeInput (
	/* type */
		'text',
	/* attributes */
		array(
			'id'		=> 'username',
			'default'	=> 'username',
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
			)
		);
	?>
	</TD>
</TR>

<tr>
	<th>Password *</th>
	<TD>
	<?php
	echo $this->makeInput (
	/* type */
		'text',
	/* attributes */
		array(
			'id'		=> 'password',
			'default'	=> 'password',
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
			)
		);
	?>
	</TD>
</TR>

<tr>
	<th>Sent From Number</th>
	<TD>
	<?php
	echo $this->makeInput (
	/* type */
		'text',
	/* attributes */
		array(
			'id'		=> 'from',
			'default'	=> '',
			'attr'		=> array(
				'size'	=> 32,
				),
			)
		);
	?>
	</TD>
</TR>

</TABLE>