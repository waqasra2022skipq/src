<?php
global $NTS_CURRENT_USER;
$authCode = $NTS_CURRENT_USER->getProp( '_auth_code' );

$link = ntsLink::makeLinkFull( ntsLib::getFrontendWebpage(), 'system/appointments/export', '', array('code' => $authCode) );
$link = preg_replace( '/^http(s)?\:\/\//', 'webcal://', $link );
?>
<h3>Outlook</h3>
<p>
<?php echo M('Outlook 2007 supports iCal subscriptions which will automatically update your Outlook calendar with new appointments.'); ?>
<p>
<a href="<?php echo $link; ?>"><?php echo M('Click this link to open Outlook and set it up.'); ?></a>

<h3>Google Calendar</h3>
<p>
Copy this address:
<br>
<input type="text" value="<?php echo $link; ?>" size="140" onClick="this.focus();this.select();">
<p>
<?php
echo M('Inside your Google Calendar on the left side under the [b]Other calendars[/b] click [b]Add[/b] then choose [b]Add by URL[/b]. 
Paste the above address then click [b]Add Calendar[/b]. This will automatically add your appointments to Google Calendar.');
?>

<p>
<?php
echo M('Please note that Google Calendar can take up to a day to update after an appointment is made here.');
?>
</p>

<?php
$ntsConf =& ntsConf::getInstance();
$params = array(
	'icalSummary',
	);
$default = array();
reset( $params );
foreach( $params as $p ){
	$default[ $p ] = $ntsConf->get( $p );
	}
$ff =& ntsFormFactory::getInstance();
$formFile = dirname( __FILE__ ) . '/form';
$form =& $ff->makeForm( $formFile, $default );
$form->display();
?>