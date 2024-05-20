<?php
$object = ntsLib::getVar( 'admin/company/resources/edit::OBJECT' );
$objId = $object->getId();

$tm2 = ntsLib::getVar( 'admin::tm2' );
$ntsdb =& dbWrapper::getInstance();

$schView = ntsLib::getVar( 'admin/manage:schView' );

$sers = array();
$locs = array();
$ress = array();
$tm2->setResource( $object->getId() );
$tm2->resetLrs();
$lrss = $tm2->getLrs( TRUE );

reset( $lrss );
foreach( $lrss as $lrs )
{
	if( ! in_array($lrs[0], $locs) )
		$locs[] = $lrs[0];
	if( ! in_array($lrs[1], $ress) )
		$ress[] = $lrs[1];
	if( ! in_array($lrs[2], $sers) )
		$sers[] = $lrs[2];
}
$sers_count = $ntsdb->count( 'services' );
$locs_count = $ntsdb->count( 'locations' );
$ress_count = $ntsdb->count( 'resources' );
?>
<div class="row">
	<div class="col-sm-7">
		<?php $NTS_VIEW['form']->display(); ?>
	</div>

	<?php if( in_array($objId, $schView) ) : ?>
		<div class="col-sm-5">
			<?php if( ! $sers ) : ?>
				<p class="alert alert-danger">
					<?php echo M('No availability configured'); ?>
				</p>
			<?php endif; ?>

			<?php if( $sers ) : ?>
				<h4><?php echo M('Services'); ?> [<?php echo count($sers); ?>/<?php echo $sers_count; ?>]</h4>
				<ul class="list-unstyled">
					<?php foreach( $sers as $sid ) : ?>
						<li>
							<?php
							$obj = ntsObjectFactory::get('service');
							$obj->setId( $sid );
							?>
							<?php echo ntsView::objectTitle( $obj, TRUE ); ?> [<?php echo ntsTime::formatPeriodShort($obj->getProp('duration')); ?>]
						</li>
					<?php endforeach; ?>
				</ul>
			<?php endif; ?>

			<?php if( $locs ) : ?>
				<h4><?php echo M('Locations'); ?> [<?php echo count($locs); ?>/<?php echo $locs_count; ?>]</h4>
				<ul class="list-unstyled">
					<?php foreach( $locs as $lid ) : ?>
						<li>
							<?php
							$obj = ntsObjectFactory::get('location');
							$obj->setId( $lid );
							?>
							<?php echo ntsView::objectTitle( $obj, TRUE ); ?>
						</li>
					<?php endforeach; ?>
				</ul>
			<?php endif; ?>

			<p>
				<a href="<?php echo ntsLink::makeLink('admin/manage/schedules', '', array('filter' => 'r'. $object->getId())); ?>" class="btn btn-default">
					<i class="fa fa-bar-chart-o fa-fw"></i><?php echo M('Availability'); ?>
				</a>
			</p>
		</div>
	<?php endif; ?>
</div>
