#!/usr/bin/perl
use lib 'C:/xampp/htdocs/src/lib';
use CGI qw(:standard escape);
use Cwd;
use DBI;
use DBA;
use DBForm;
use PDF;
use Time::Local;

############################################################################
$form = DBForm->new();
$DT   = localtime();

#foreach my $f ( sort keys %{$form} ) { warn ": form-$f=$form->{$f}\n"; }
############################################################################
#chdir("$form->{DOCROOT}/tmp");
#$pwd=cwd();
$dbh = $form->dbconnect();
my $ProvID =
  $form->{Provider_ProvID} ? $form->{Provider_ProvID} : $form->{LOGINPROVID};
my $AgencyID = MgrTree->getAgency( $form, $ProvID );
my $s = $dbh->prepare("select * from Provider where ProvID='${AgencyID}'");
$s->execute() || $form->dberror("savDocs: select Provider where $AgencyID");
my $rProvider = $s->fetchrow_hashref;
$form->{SUBORGNAME}       = $rProvider->{Name};
$form->{SUBORGNAMEUPCASE} = uc $rProvider->{Name};
$form->{SUBORGCITY}       = $rProvider->{City};
$form->{SUBORGDATE}       = DBUtil->Date( $form->{TODAY}, 'fmt', 'MM/DD/YYYY' );
$form->{SUBORGBY}         = qq|$rProvider->{FName} $rProvider->{LName}|;
$form->{SUBORGJOBTITLE}   = $rProvider->{JobTitle};
$s->finish();
my $pdffile = qq|https://$ENV{HTTP_HOST}/pdf/OPAMemberContract.pdf|;
my $fdfText = &PDF::genFDF( $pdffile, $form );
print qq|Content-Type: application/vnd.fdf\n\n$fdfText|;
$form->complete();
############################################################################
exit;
