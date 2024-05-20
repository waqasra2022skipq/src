<?php
// payment types
$gateways = array();
$ntsdb =& dbWrapper::getInstance();
$result = $ntsdb->select( 'DISTINCT(pgateway)', 'transactions' );
while( $i = $result->fetch() )
{
	$gtw = trim( $i['pgateway'] );
	if( $gtw )
		$gateways[] = array( $gtw, M(ntsLib::upperCaseMe($gtw)) );
}
?>
<ul class="list-inline">

<?php if( $gateways ) : ?>
	<li>
		<?php echo M('Paid Through'); ?>: 
		<?php
		array_unshift( $gateways, array('', ' - ' . M('Any') . ' - ') );
		echo $this->makeInput (
		/* type */
			'select',
		/* attributes */
			array(
				'id'		=> 'gateway',
				'options'	=> $gateways
				)
			);
		?>
	</li>
<?php endif; ?>

<li>
<?php
echo $this->makeInput (
/* type */
	'date/Calendar',
/* attributes */
	array(
		'id'		=> 'from',
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
 - 
<?php
echo $this->makeInput (
/* type */
	'date/Calendar',
/* attributes */
	array(
		'id'		=> 'to',
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
</li>

<li>
<?php 
echo $this->makePostParams('-current-', 'dates');
?>
<INPUT class="btn btn-default" TYPE="submit" VALUE="<?php echo M('Go'); ?>">
&nbsp;&nbsp;
<?php
$params = array(
	'from'		=> $this->getValue('from'),
	'to'		=> $this->getValue('to'),
	'gateway'	=> $this->getValue('gateway'),
	);
?>
</li>

<li class="pull-right">
	<a class="btn btn-default" href="<?php echo ntsLink::makeLink('-current-', 'export', $params ); ?>">
	<i class="fa fa-download-alt"></i> <?php echo M('Download'); ?>
	</a>
</li>
</ul>
