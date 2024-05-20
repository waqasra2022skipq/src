<?php
echo ntsForm::wrapInput(
	M('Label'),
	$this->buildInput (
	/* type */
		'text',
	/* attributes */
		array(
			'id'		=> 'label',
			'default'	=> 'Pay At Our Office',
			'attr'		=> array(
				'size'	=> 24
				),
			),
	/* validators */
		array(
			array(
				'code'		=> 'notEmpty.php', 
				'error'		=> M('Required'),
				),
			)
		)
	);
?>