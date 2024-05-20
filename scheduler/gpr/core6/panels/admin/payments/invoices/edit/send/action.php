<?php
$cm =& ntsCommandManager::getInstance();
$ff =& ntsFormFactory::getInstance();

$customerLink = ntsLink::makeLinkFull(ntsLib::getFrontendWebpage(), 'system/invoice', '', array('refno' => $object->getProp('refno')));

$NTS_VIEW['customerLink'] = $customerLink;

$formParams = $object->getByArray();
$formParams['sendLink'] = $customerLink;

$customer = $object->getCustomer();
$customer_email = $customer->getProp('email');
$formParams['to'] = $customer_email;

$sendFormFile = dirname( __FILE__ ) . '/formSend';
$NTS_VIEW['formSend'] =& $ff->makeForm( $sendFormFile, $formParams );

switch( $action ){
	case 'send':
		if( $NTS_VIEW['formSend']->validate() ){
			$formValues = $NTS_VIEW['formSend']->getValues();

		/* send */
			$cm->runCommand( $customer, 'email', array('body' => $formValues['body'], 'subject' => $formValues['subject']) );

			if( $cm->isOk() ){
				$title = M('Customer') . ': ' . '<b>' . $customer->getProp('first_name') . ' ' . $customer->getProp('last_name') . '</b>';
				ntsView::setAnnounce( $title . ': ' . M('Send Email') . ': ' . M('OK'), 'ok' );

			/* continue to the list with anouncement */
				$forwardTo = ntsLink::makeLink( '-current-' );
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
?>