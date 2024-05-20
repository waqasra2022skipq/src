<?php
$packs = ntsObjectFactory::getAll( 'pack' );
$packOptions = array();
reset( $packs );
foreach( $packs as $pack ){
	$packOptions[] = array( $pack->getId(), $pack->getFullTitle() );
	}
array_unshift( $packOptions, array('', ' - ' . M('Select') . ' - ') );
?>

<?php
echo ntsForm::wrapInput(
	M('Package'),
	$this->buildInput (
	/* type */
		'select',
	/* attributes */
		array(
			'id'		=> 'pack_id',
			'options'	=> $packOptions
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