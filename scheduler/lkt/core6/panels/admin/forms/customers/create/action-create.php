<?php
$ntsdb =& dbWrapper::getInstance();
$ff =& ntsFormFactory::getInstance();
$cm =& ntsCommandManager::getInstance();

$ntsdb =& dbWrapper::getInstance();
/* form id */
$sql =<<<EOT
	SELECT
		*
	FROM
		{PRFX}forms
	WHERE
		class = 'customer'
	LIMIT 1
EOT;
$result = $ntsdb->runQuery( $sql );
$formInfo = $result->fetch();
$formId = $formInfo['id'];

$formParams = array(
	'form_id'	=> $formId,
	);

$ff =& ntsFormFactory::getInstance();
$formFile = dirname( __FILE__ ) . '/form';
$form =& $ff->makeForm( $formFile, $formParams );

$removeValidation = array();
$suppliedType = $_NTS['REQ']->getParam( 'type' );
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

	if( isset($formValues['default_value-' . $formValues['type']]) ){
		$formValues['default_value'] = $formValues['default_value-' . $formValues['type']];
		}

/* create field */
	$object = ntsObjectFactory::get( 'form_control' );
	$formValues['name'] = 'custom_' . $formValues['name'];
	$object->setByArray( $formValues );

/* class name */
	$object->setProp( 'class', 'customer' );
/* form id */
	$sql =<<<EOT
		SELECT
			*
		FROM
			{PRFX}forms
		WHERE
			class = 'customer'
		LIMIT 1
EOT;
	$result = $ntsdb->runQuery( $sql );
	$formInfo = $result->fetch();
	$formId = $formInfo['id'];
	$object->setProp( 'form_id', $formId );

	$cm->runCommand( $object, 'create' );
	if( $cm->isOk() ){
		ntsView::setAnnounce( M('Form Field') . ': ' . M('Created'), 'ok' );

		$id = $object->getId();
	/* continue to the list with anouncement */
		$forwardTo = ntsLink::makeLink( '-current-/../edit', '', array('id' => $id ) );
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
?>