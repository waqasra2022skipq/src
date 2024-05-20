<?php
$conf =& ntsConf::getInstance();

$confFlow = $conf->get('appointmentFlow');
$confAppointmentFlowJustOne = $conf->get('appointmentFlowJustOne');

reset( $confFlow );
$currentFlow = array();
$currentFlowSetting = array();
foreach( $confFlow as $f )
{
	if( $f[0] == 'seats' )
		continue;
	$currentFlow[] = $f;
	$currentFlowSetting[] = $f[0];
}
reset( $currentFlow );

$possibleFlows = array(
	'service'	=> M('Service'),
	'time'		=> M('Date and Time'),
	'location'	=> M('Location'),
	'resource'	=> M('Bookable Resource'),
	);

$assignOptions = array(
	'service'	=> array(),
	'time'		=> array(),
	'location'	=> array(),
	'resource'	=> array(),
/*
	'location'	=> array( 
		array( 'manual',		M('Let Customer Select') ),
		array( 'manualplus',	M('Let Customer Select With Auto Assign Option') ),
		array( 'auto',			M('Automatically Select Any Available') ),
		),
	'resource'	=> array( 
		array( 'manual',		M('Let Customer Select') ),
		array( 'manualplus',	M('Let Customer Select With Auto Assign Option') ),
		array( 'auto',			M('Automatically Select Any Available') ),
		),
*/
	);

$has_assign_options = FALSE;
reset( $assignOptions );
foreach( $assignOptions as $k => $v )
{
	if( $v )
	{
		$has_assign_options = TRUE;
		break;
	}
}
$count = 0;
?>

<?php foreach( $currentFlow as $f ) : ?>
	<?php $count++; ?>
	<div id="nts-flow-option-<?php echo $count; ?>">
		<?php
		echo ntsForm::wrapInput(
			$possibleFlows[$f[0]],
			array(
				'<ul class="list-inline list-hori-separated">',
					'<li>',
						'<a class="btn btn-default" href="#" title="' . M('Up') . '" id="nts-move-up-' . $f[0] . '">' . '<i class="fa fa-fw fa-arrow-up"></i>' . '</a>',
					'</li>',
					'<li>',
						'<a class="btn btn-default" href="#" title="' . M('Down') . '" id="nts-move-down-' . $f[0] . '">' . '<i class="fa fa-fw fa-arrow-down"></i>' . '</a>',
					'</li>',
				'</ul>'
				)
			);
		?>
	</div>
<?php endforeach; ?>

<?php
echo ntsForm::wrapInput(
	M('Just One Option Per Page'),
	$this->buildInput (
	/* type */
		'checkbox',
	/* attributes */
		array(
			'id'	=> 'appointmentFlowJustOne',
			'value'	=> $confAppointmentFlowJustOne
			)
		)
	);
?>


<?php
echo $this->makeInput (
/* type */
	'hidden',
/* attributes */
	array(
		'id'	=> 'current-flow-setting',
		'value'	=> join( $currentFlowSetting, '|' )
		)
	);
echo $this->makePostParams('-current-', 'update');
?>

<?php
echo ntsForm::wrapInput(
	'',
	'<input type="submit" class="btn btn-default" value="' . M('Save') . '">'
	);
?>

<script language="javascript">
ntsUpPrefix = "nts-move-up-";
ntsDownPrefix = "nts-move-down-";
ntsRowPrefix = "nts-flow-option-";

var ntsCurrentRows = new Array();
var ntsCurrentHandles = new Array();
<?php 
reset( $currentFlow );
$count = 0;
foreach( $currentFlow as $f ) :
$count++;
?>
ntsCurrentRows["<?php echo $f[0]; ?>"] = <?php echo $count; ?>;
ntsCurrentHandles[<?php echo $count; ?>] = "<?php echo $f[0]; ?>";
<?php endforeach; ?>

/* move up */
jQuery("a[id^=" + ntsUpPrefix + "]").live("click", function() {
	var srcRowHandle = this.id.substring(ntsUpPrefix.length);
	var srcRowId = parseInt( ntsCurrentRows[srcRowHandle] );
	if( srcRowId > 1 ){
		var trgRowId = parseInt( srcRowId - 1 );
		var trgRowHandle = ntsCurrentHandles[ trgRowId ]
		var srcRowHtmlId = ntsRowPrefix + srcRowId;
		var trgRowHtmlId = ntsRowPrefix + trgRowId; 

		var tmp = jQuery('#' + srcRowHtmlId).html();
		jQuery('#' + srcRowHtmlId).html( jQuery('#' + trgRowHtmlId).html() );
		jQuery('#' + trgRowHtmlId).html( tmp );

		ntsCurrentRows[ srcRowHandle ] = trgRowId;
		ntsCurrentRows[ trgRowHandle ] = srcRowId;
		ntsCurrentHandles[ trgRowId ] = srcRowHandle;
		ntsCurrentHandles[ srcRowId ] = trgRowHandle;

		document.forms["<?php echo $this->getName(); ?>"]["nts-current-flow-setting"].value = ntsCurrentHandles.join('|');
		}
	return true;
	});

jQuery("a[id^=" + ntsDownPrefix + "]").live("click", function() {
	var srcRowHandle = this.id.substring(ntsDownPrefix.length);
	var srcRowId = parseInt( ntsCurrentRows[srcRowHandle] );
	if( srcRowId < 4 ){
		var trgRowId = parseInt( srcRowId + 1 );
		var trgRowHandle = ntsCurrentHandles[ trgRowId ]
		var srcRowHtmlId = ntsRowPrefix + srcRowId;
		var trgRowHtmlId = ntsRowPrefix + trgRowId; 
		
		var tmp = jQuery('#' + srcRowHtmlId).html();
		jQuery('#' + srcRowHtmlId).html( jQuery('#' + trgRowHtmlId).html() );
		jQuery('#' + trgRowHtmlId).html( tmp );

		ntsCurrentRows[ srcRowHandle ] = trgRowId;
		ntsCurrentRows[ trgRowHandle ] = srcRowId;
		ntsCurrentHandles[ trgRowId ] = srcRowHandle;
		ntsCurrentHandles[ srcRowId ] = trgRowHandle;

		document.forms["<?php echo $this->getName(); ?>"]["nts-current-flow-setting"].value = ntsCurrentHandles.join('|');
		}
	return true;
	});
</script>
