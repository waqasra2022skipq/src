#!/usr/bin/perl
###########################################
use lib '/var/www/okmis/src/lib';
use Cwd;
use DBI;
use DBForm;
use DBUtil;

###########################################
$form = DBForm->new();

#foreach my $f ( sort keys %{$form} ) { warn "genInvoices.cgi: form-$f=$form->{$f}\n"; }
chdir("$form->{DOCROOT}/tmp");
$pwd = cwd();
warn qq|genInvoices.cgi: pwd=$pwd, file=$file\n|;
my $cmd =
qq|/var/www/okmis/src/bin/genInvoices DBNAME=$form->{DBNAME}\\&ClientID=$form->{Client_ClientID}\\&mlt=$form->{mlt}|;
warn "cmd=$cmd\n";
my $diskfile = DBUtil->ExecCmd( $cmd, '.err' );
warn qq|diskfile=$diskfile\n|;
my $out = DBUtil->ReadFile($diskfile);
warn qq|out=$out\n|;
$out =~ s/\r//g;
warn qq|r-out=$out\n|;
$out =~ s/\n/\\n/g;
warn qq|n-out=$out\n|;
DBA->setAlert( $form, $out );
############################################################################
print
qq|Location: /cgi/bin/mis.cgi?view=ListInvoices.cgi&Client_ClientID=$form->{Client_ClientID}&mlt=$form->{mlt}&misLINKS=$form->{misLINKS}\n\n|;
$form->complete();
exit;
