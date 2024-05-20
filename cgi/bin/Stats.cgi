#!/usr/bin/perl
use lib '/home/okmis/mis/src/lib';
use Cwd;
use DBI;
use DBForm;
use DBUtil;
use SysAccess;
############################################################################
$form = DBForm->new;
if ( ! SysAccess->verify($form,'Privilege=QAReports') )
{ $form->error("Access Denied (Stats.cgi)"); }
#foreach my $f ( sort keys %{$form} ) { warn "Stats: form-$f=$form->{$f}\n"; }
#warn qq|QTR=$form->{QTR}\n|;
#warn qq|YEAR=$form->{YEAR}\n|;
#warn qq|FromDate=$form->{FromDate}\n|;
#warn qq|ToDate=$form->{ToDate}\n|;
chdir("$form->{DOCROOT}/tmp");
my $cmd = qq|/home/okmis/mis/src/reports/Stats DBNAME=$form->{DBNAME}\\&QTR=$form->{QTR}\\&YEAR=$form->{YEAR}\\&FromDate=$form->{FromDate}\\&ToDate=$form->{ToDate}\\&output=$form->{output}\\&BHO=$form->{BHO}\\&PDF=$form->{PDF}\\&Report_Clinics=$form->{Report_Clinics}\\&InsID=$form->{InsID}\\&ReferredBy1=$form->{ReferredBy1}\\&Race=$form->{Race}\\&Gend=$form->{Gend}\\&MISAge=$form->{MISAge}\\&CARFAge=$form->{CARFAge}\\&MS=$form->{MS}\\&mlt=$form->{mlt}|;
#warn qq|$cmd|;
my $diskfile = DBUtil->ExecCmd($cmd);
my $out = DBUtil->ReadFile($diskfile);
#warn qq|${out}|;
if ( $form->{PDF} ) { print  qq|Content-Type: application/vnd.adobe.xdp+xml\n\n|; }
#if ( $form->{PDF} ) { print qq|Content-Type: application/vnd.fdf\n\n|; }
elsif ( $form->{output} eq 'text' ) { print qq|Content-Type: text/html\n\n|; }
else { print qq|Content-Type: application/vnd.ms-excel\n\n|; }
if ( $form->{LOGINPROVID} == 91 )
{
  open OUT, ">/home/okmis/mis/src/debug/Stats.out" or die "Couldn't open file: $!";
  print OUT qq|${out}|;
  close(OUT);
}
print qq|${out}|;
$form->complete();
exit;
