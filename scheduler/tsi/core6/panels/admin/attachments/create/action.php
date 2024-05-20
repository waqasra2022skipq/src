<?php
$parent = ntsLib::getVar( 'admin/attachments::PARENT' );
$parentId = $parent->getId();
$parentClass = $parent->getClassName();

$ff =& ntsFormFactory::getInstance();
$formFile = dirname( __FILE__ ) . '/form';
$NTS_VIEW['form'] =& $ff->makeForm( $formFile );

switch( $action )
{
	case 'create':
		if( $NTS_VIEW['form']->validate() )
		{
			$formValues = $NTS_VIEW['form']->getValues();

			$am = new ntsAttachManager;
			$am->add( $formValues['attach'], $parentClass, $parentId );

			$error = $am->get_error();
			if( ! $error )
			{
				$msg = array( M('Attachment'), M('Add'), M('OK') );
				$msg = join( ': ', $msg );
				ntsView::addAnnounce( $msg, 'ok' );
				ntsView::getBack();
				exit;
			}
			else
			{
				$NTS_VIEW['form']->errors['attach'] = $error;
//				ntsView::addAnnounce( $error, 'error' );
			}
		}
		else
		{
		/* form not valid, continue to create form */
		}
		break;
	default:
		break;
}
?>