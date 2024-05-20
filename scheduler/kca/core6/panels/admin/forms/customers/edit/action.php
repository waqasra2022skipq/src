<?php
$ntsdb =& dbWrapper::getInstance();
$ff =& ntsFormFactory::getInstance();
$cm =& ntsCommandManager::getInstance();

$id = $_NTS['REQ']->getParam( 'id' );
$addValidator = $_NTS['REQ']->getParam( 'add_validator' );

/* control info */
$sql =<<<EOT
SELECT
	{PRFX}form_controls.*,
	{PRFX}forms.title AS form_title
FROM
	{PRFX}form_controls
INNER JOIN
	{PRFX}forms 
ON
	{PRFX}forms.id = {PRFX}form_controls.form_id
WHERE
	{PRFX}form_controls.id = $id
EOT;
$result = $ntsdb->runQuery( $sql );
$controlInfo = $result->fetch();
$formId = $controlInfo['form_id'];

$controlInfo['default_value-' . $controlInfo['type']] = $controlInfo['default_value'];

if( isset($controlInfo['attr']) && $controlInfo['attr'] )
	$controlInfo['attr'] = hc_mb_unserialize($controlInfo['attr']);
else
	$controlInfo['attr'] = array();
reset( $controlInfo['attr'] );
foreach( $controlInfo['attr'] as $name => $value ){
	$controlInfo[ 'attr-' . $name ] = $value;
	}
	
if( isset($controlInfo['validators']) && $controlInfo['validators'] ){
	$validators = hc_mb_unserialize($controlInfo['validators']);
	reset( $validators );
	$controlInfo['validators'] = array();
	foreach( $validators as $v ){
		$controlInfo['validators'][] = $v;
		}
	}
else {
	$controlInfo['validators'] = array();
	}
$controlInfo['add_validator'] = $addValidator;

switch( $action ){
	case 'delete_validator':
		$validatorId = $_NTS['REQ']->getParam('validator');
		$count = 1;
		$validators = array();
		reset( $controlInfo['validators'] );
		foreach( $controlInfo['validators'] as $va ){
			if( $count != $validatorId ){
				$validators[] = $va;
				}
			$count++;
			}

	/* update field */
		$object = ntsObjectFactory::get( 'form_control' );
		$object->setId( $id );
		$object->setProp( 'validators', $validators );

		$cm->runCommand( $object, 'update' );
		if( $cm->isOk() ){
			ntsView::setAnnounce( M('Deleted'), 'ok' );

		/* continue to the list with anouncement */
			$forwardTo = ntsLink::makeLink( '-current-', '', array('id' => $id ) );
			ntsView::redirect( $forwardTo );
			exit;
			}
		else {
			$errorText = $cm->printActionErrors();
			ntsView::addAnnounce( $errorText, 'error' );
			}
		exit;
		break;

	case 'update':
		$ff =& ntsFormFactory::getInstance();
		$formFile = dirname( __FILE__ ) . '/form';

		$form =& $ff->makeForm( $formFile, $controlInfo );

		$removeValidation = array();
		$suppliedType = $controlInfo['type'];
		switch( $suppliedType ){
			case 'date/Calendar':
				$removeValidation[] = 'attr-size';
				$removeValidation[] = 'default_value-text';

				$removeValidation[] = 'attr-options';
				$removeValidation[] = 'attr-cols';
				$removeValidation[] = 'attr-rows';
				$removeValidation[] = 'default_value-textarea';
				break;
			case 'textarea':
				$removeValidation[] = 'attr-size';
				$removeValidation[] = 'default_value-text';

				$removeValidation[] = 'attr-options';
				break;
			case 'text':
			case 'mobilephone':
				$removeValidation[] = 'attr-cols';
				$removeValidation[] = 'attr-rows';
				$removeValidation[] = 'default_value-textarea';

				$removeValidation[] = 'attr-options';
				break;
			case 'checkbox':
				$removeValidation[] = 'attr-cols';
				$removeValidation[] = 'attr-rows';
				$removeValidation[] = 'default_value-textarea';

				$removeValidation[] = 'attr-size';
				$removeValidation[] = 'default_value-text';

				$removeValidation[] = 'attr-options';
				break;
			case 'select':
				$removeValidation[] = 'attr-cols';
				$removeValidation[] = 'attr-rows';
				$removeValidation[] = 'default_value-textarea';

				$removeValidation[] = 'attr-size';
				$removeValidation[] = 'default_value-text';
				break;
			}

		if( $form->validate($removeValidation) ){
			$formValues = $form->getValues();
			reset( $formValues );

		/* attributes */
			$prefix = 'attr-';
			$attr = array();
			reset( $formValues );
			foreach( $formValues as $k => $v ){
				if( substr($k, 0, strlen($prefix)) == $prefix ){
					$shortName = substr($k, strlen($prefix) );
					$attr[ $shortName ] = $v;
					}
				}
			$formValues['attr'] = $attr;

		/* validators code and error messages */
			$validators = array();
			$prefix = 'vld-';
			$attr = array();
			reset( $formValues );
			foreach( $formValues as $k => $v ){
				if( substr($k, 0, strlen($prefix)) == $prefix ){
					preg_match( "/^$prefix(\d+)$/", $k, $ma );
					$index = $ma[1];
					$validators[] = array(
						'code'	=> $formValues[ $k ],
						'error'	=> $formValues[ 'error-' . $index ],
						);
					}
				}
			$formValues['validators'] = $validators;

			if( isset($formValues['default_value-' . $formValues['type']]) ){
				$formValues['default_value'] = $formValues['default_value-' . $formValues['type']];
				}

		/* update field */
			$object = ntsObjectFactory::get( 'form_control' );
			$object->setId( $id );
			$object->setByArray( $formValues );

			$cm->runCommand( $object, 'update' );
			if( $cm->isOk() ){
				ntsView::setAnnounce( M('Form Field') . ': ' . M('Update') . ': ' . M('OK'), 'ok' );

			/* continue to the list with anouncement */
				$forwardTo = ntsLink::makeLink( '-current-', '', array('id' => $id ) );
				ntsView::redirect( $forwardTo );
				exit;
				}
			else {
				$errorText = $cm->printActionErrors();
				ntsView::addAnnounce( $errorText, 'error' );
				}
			}
		else {
		/* form not valid, continue to edit form */
			}
		break;
	}

if( ! isset($form) ){
	$formFile = dirname( __FILE__ ) . '/form';
	$form =& $ff->makeForm( $formFile, $controlInfo );
	}
$NTS_VIEW['form'] = $form;
?>