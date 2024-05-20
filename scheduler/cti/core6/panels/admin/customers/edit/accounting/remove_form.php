<?php
$aam =& ntsAccountingAssetManager::getInstance();
$balance_id = $this->getValue('balance_id');
$asset_id = $this->getValue('asset_id');
$asset_value = $this->getValue('asset_value');
$total_asset_value = $this->getValue('total_asset_value');
$asset_type = $aam->asset_type( $asset_id );

switch( $asset_type ){
	case 'qty':
		echo ntsForm::wrapInput(
			M('Number of appointments'),
			$this->buildInput (
			/* type */
				'text',
			/* attributes */
				array(
					'id'		=> 'asset_value',
					'attr'		=> array(
						'size'	=> 4,
						),
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
					array(
						'code'		=> 'lessEqualThan.php', 
						'error'		=> M('Too Much'),
						'params'	=> array(
							'compareWith'	=> $total_asset_value,
							)
						),
					)
				)
			);
		break;

	case 'duration':
		echo ntsForm::wrapInput(
			M('Duration'),
			$this->buildInput (
			/* type */
				'period/MinHour',
			/* attributes */
				array(
					'id'		=> 'asset_value',
					'default'	=> 2 * 60 * 60,
					),
			/* validators */
				array(
					array(
						'code'		=> 'notEmpty.php', 
						'error'		=> M('Required'),
						),
					array(
						'code'		=> 'lessEqualThan.php', 
						'error'		=> M('Too Much'),
						'params'	=> array(
							'compareWith'	=> $total_asset_value,
							)
						),
					)
				)
			);
		break;

	case 'amount':
		echo ntsForm::wrapInput(
			M('Amount'),
			$this->buildInput (
			/* type */
				'text',
			/* attributes */
				array(
					'id'		=> 'asset_value',
					'attr'		=> array(
						'size'	=> 8,
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
						'code'		=> 'number.php', 
						'error'		=> M('Numbers only'),
						),
					array(
						'code'		=> 'greaterThan.php', 
						'error'		=> M('Required'),
						'params'	=> array(
							'compareWith'	=> 0,
							)
						),
					array(
						'code'		=> 'lessEqualThan.php', 
						'error'		=> M('Too Much'),
						'params'	=> array(
							'compareWith'	=> $total_asset_value,
							)
						),
					)
				)
			);
		break;

	case 'unlimited':
		break;

	default:
		echo $this->makeInput(
		/* type */
			'hidden',
		/* attributes */
			array(
				'id'	=> 'asset_value',
				)
			);
		break;
}
?>
<?php 
echo $this->makePostParams(
	'-current-',
	'remove',
	array(
		'balance_id'	=> $balance_id,
		)
	);
?>
<?php
echo ntsForm::wrapInput(
	'',
	'<INPUT class="btn btn-default" TYPE="submit" VALUE="' . M('Remove') . '">'
	);
?>