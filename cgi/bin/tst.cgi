#!/usr/bin/perl
use lib '/home/okmis/mis/src/lib';
use DBI;
use myForm;
use DBA;
use myDBI;
foreach my $f ( sort keys %ENV ) { warn qq|BEGIN: ENV: $f=$ENV{$f}\n|; }
my $form = myForm->new();
warn qq|ENTER: tst\n|;
foreach my $f ( sort keys %{$form} ) { warn qq|form: $f=$form->{$f}\n|; }
#myDBI->error('HELP TEST');
my $table = 'PDDom';
  foreach my $table ( $form->getDetTables($table) )
  { print qq|1: table=${table}\n|; }
  foreach my $table ( myDBI->getDetTables($table) )
  { print qq|2: table=${table}\n|; }
  if ( $form->getDetTables($table) )
  { print qq|1: YES\n|; } else { print qq|1: NO\n|; }
  if ( myDBI->getDetTables($table) )
  { print qq|2: YES\n|; } else { print qq|2: NO\n|; }
myDBI->cleanup();
exit;
my $v2 = myDBI->getTableConfig('Insurance','HEADERTABLE');
print qq|v1=${v1}, v2=${v2}\n|;
exit;
