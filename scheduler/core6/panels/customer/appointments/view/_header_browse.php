<?php
$current_user = ntsLib::getCurrentUser();
$ff =& ntsFormFactory::getInstance();
$datesShown = array();
?>
<div class="page-header">
	<h2><i class="fa fa-check-square-o"></i> <?php echo M('Appointments'); ?></h2>
</div>

<ul class="nav nav-pills">
	<li<?php if( $show != 'old'){ echo ' class="active"';}; ?>>
		<a href="<?php echo ntsLink::makeLink('-current-', '', array('show' => 'upcoming') ); ?>">
			<?php echo M('Upcoming'); ?>
		</a>
	</li>

	<li<?php if( $show == 'old'){ echo ' class="active"';}; ?>>
		<a href="<?php echo ntsLink::makeLink('-current-', '', array('show' => 'old') ); ?>">
			<?php echo M('Past'); ?>
		</a>
	</li>

	<?php if( NTS_ENABLE_TIMEZONES > 0 ) : ?>
		<li>
			<a class="dropdown-toggle" data-toggle="dropdown" href="#">
				<i class="fa fa-fw fa-globe"></i> 
				<?php echo ntsTime::timezoneTitle($current_user->getTimezone()); ?> <b class="caret"></b>
			</a>
			<ul class="dropdown-menu">
				<li>
					<span>
					<?php
					$formTimezoneParams = array(
						'tz'	=> $current_user->getTimezone(),
						);
					$formTimezone =& $ff->makeForm( dirname(__FILE__) . '/formTimezone', $formTimezoneParams );
					$formTimezone->display();
					?>
					</span>
				</li>
			</ul>
		</li>
	<?php elseif( NTS_ENABLE_TIMEZONES < 0 ) : ?>

	<?php else : ?>
		<li>
			<span>
				<i class="fa fa-fw fa-globe"></i> 
				<?php echo ntsTime::timezoneTitle($current_user->getTimezone()); ?>
			</span>
		</li>
	<?php endif; ?>

	<?php if( $objects ) : ?>
		<li>
			<?php 
			$overParams = array(
				'show'	=> $show,
				);
			?>
			<ul class="nav nav-pills">
				<li>
					<?php $overParams['display'] = 'ical'; ?>
					<a href="<?php echo ntsLink::makeLink('-current-', 'export', $overParams ); ?>"><i class="fa fa-fw fa-download"></i> <?php echo M('Download'); ?>: iCal</a>
				</li>
				<li>
					<?php $overParams['display'] = 'excel'; ?>	
					<a href="<?php echo ntsLink::makeLink('-current-', 'export', $overParams ); ?>"><i class="fa fa-fw fa-download"></i> <?php echo M('Download'); ?>: Excel</a>
				</li>
			</ul>
		</li>
	<?php endif; ?>
</ul>
