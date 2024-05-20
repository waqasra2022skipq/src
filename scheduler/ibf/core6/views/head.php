<!DOCTYPE html>
<html xmlns="http://www.w3.org/1999/xhtml">
<head>
<?php require( dirname(__FILE__) . '/title.php' ); ?>
<title><?php echo ntsView::getTitle(); ?></title>
<?php require( dirname(__FILE__) . '/head-content.php' ); ?>

<?php
global $NTS_CURRENT_USER;
$lang = $NTS_CURRENT_USER->getLanguage();
?>
<?php if( $lang == 'fa' ) : ?>
<style>
#nts {
direction: rtl;
}
</style>
<?php endif; ?>

</head>
<body>