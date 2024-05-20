<table class="ntsForm">
<tr>
	<th>OVH sms Nick *</th>
	<TD>
	<?php
	echo $this->makeInput (
	/* type */
		'text',
	/* attributes */
		array(
			'id'		=> 'ovhsmsnick',
			'default'	=> 'sms-xxxxx-1',
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
	<th>Utilisateur *</th>
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
	<th>Mot de passe *</th>
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
	<td class="ntsFormLabel">Numéro qui envoie *</td>
	<td class="ntsFormValue">
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

</TABLE>