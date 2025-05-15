#!/usr/bin/perl
###########################################
use lib 'C:/xampp/htdocs/src/lib';
use Cwd;
use DBI;
use DBForm;
use DBUtil;

###########################################
$form = DBForm->new();

#foreach my $f ( sort keys %{$form} ) { warn "genReceipt.cgi: form-$f=$form->{$f}\n"; }
chdir("$form->{DOCROOT}/tmp");
$pwd = cwd();

#warn qq|genReceipt.cgi: pwd=$pwd, file=$file\n|;
my $cmd =
qq|C:/xampp/htdocs/src/bin/genReceipt DBNAME=$form->{DBNAME}\\&RecIDs=$form->{InsPaid_ID}\\&mlt=$form->{mlt}|;

#warn "cmd=$cmd\n";
my $diskfile = DBUtil->ExecCmd( $cmd, '.err' );

#warn qq|diskfile=$diskfile\n|;
my $out = DBUtil->ReadFile($diskfile);

#warn qq|out=$out\n|;
############################################################################
print qq|Content-Type: application/pdf\n\n${out}|;
$form->complete();
exit;
