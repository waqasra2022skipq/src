#!/usr/bin/perl
###########################################
use lib '/home/okmis/mis/src/lib';
use DBI;
use DBForm;
use DBUtil;

###########################################
my $form = DBForm->new();
my $ID = $form->{'IDs'};   # DO WE NEED A LOOP?
#foreach my $f ( sort keys %{$form} ) { warn "PrintClientCARSReview.cgi: form-$f=$form->{$f}\n"; }
chdir("$form->{DOCROOT}/tmp");
##
# calls TrSum: uses pdf/CARS.pdt
##
my $cmd = qq|/home/okmis/mis/src/reports/TrSum DBNAME=$form->{DBNAME}\\&Type=cars\\&output=pdf\\&ClientCARSReview_ID=${ID}\\&sYearMonth=$form->{'YYYYMM'}\\&submit=1\\&mlt=$form->{mlt}|;
#warn "cmd=$cmd\n";
my $diskfile = DBUtil->ExecCmd($cmd,'.err');
#warn qq|diskfile=$diskfile\n|;
my $out = DBUtil->ReadFile($diskfile);
#warn qq|out=$out\n|;
############################################################################
print qq|Content-Type: application/pdf\n\n${out}|;
$form->complete();
exit;
