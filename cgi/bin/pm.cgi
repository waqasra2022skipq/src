#!/usr/bin/perl
use lib '/home/okmis/mis/src/lib';
use CGI qw(:standard escape);
use DBI;
use DBForm;
############################################################################
$form = DBForm->new();
my $out = qq|
listpeople [
 {
   'medicaid': 'MEDICAID1',
   'restless': '0',
   'gambled': '1',
   'financial':'1'
 },
 { 'medicaid': 'MEDICAID2',
   'restless': '1',
   'gambled':'0',
   'financial':'1'
 }
]
|;
############################################################################
print $out;
$form->complete();
exit;
