#!/usr/bin/perl
############################################################################
use lib '/home/okmis/mis/src/lib';
use DBI;
use myForm;
use myDBI;
use myConfig;
use DBA;
use DBUtil;
use uBill;
use kls;
use File::Copy;
use Time::Local;

############################################################################
my $form = myForm->new();
my $dbh = myDBI->dbconnect($form->{'DBNAME'});
my $debug = $form->{'debug'};

if ( $debug ) { foreach my $f ( sort keys %{$form} ) { print "pro999: form-$f=$form->{$f}\n"; } }

print qq|ENTER: pro999, DBNAME=$form->{'DBNAME'}, filepath=$form->{'filepath'}\n| if ( $debug );

my $HDR = '';
my $SE = '';

my $filepath = $form->{'filepath'};
my $Test = $form->{'test'};
my ($rptDir,$rptFile,$rptPath) = ("$form->{DOCROOT}/reports4","","");
if ( ${Test} ) { print qq|TEST RUN ONLY!\n|; }
############################################################################
print localtime()."\n";
print qq|open: ${filepath}\n| if ( $debug );

exit if ( $debug == 2 );

my $cnt = 0;
while ( my $line = kls->readFILE($filepath,'~') )
{
 $cnt++;
  chomp($line);
 print qq|while: line ${cnt}=${line}\n|;
}
myDBI->cleanup();
exit;
