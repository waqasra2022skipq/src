<?php
$packs = ntsObjectFactory::getAll( 'pack', 'WHERE price > 0' );

$view = array(
	'packs'	=> $packs,
	);

$this->render( 
	dirname(__FILE__) . '/index.php',
	$view
	);
?>