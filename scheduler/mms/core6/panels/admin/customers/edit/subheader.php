<?php
$object = ntsLib::getVar( 'admin/customers/edit::OBJECT' );
$t = new ntsTime;
?>

<div class="row">
	<div class="col-md-4 col-xs-12 pull-right">
		<ul class="list-unstyled pull-right">
			<li>
				<ul class="list-inline">
					<li>
						ID: <?php echo $object->getId(); ?>
					</li>
					<li>
						<?php echo $object->statusLabel(); ?>
					</li>
				</ul>
			</li>
			<li class="text-muted text-smaller">
				<?php
				$t->setTimestamp($object->getProp('created'));
				?>
				<?php echo M('Created'); ?>: <?php echo $t->formatDate(); ?>
			</li>
		</ul>
	</div>

	<div class="col-md-8 col-xs-12">
		<h2><?php echo ntsView::objectTitle($object, TRUE); ?></h2>
	</div>
</div>