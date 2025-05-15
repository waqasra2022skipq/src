#!/usr/bin/perl
############################################################################
use lib 'C:/xampp/htdocs/src/lib';
use CGI qw(:standard escape);
use DBI;
use myForm;
use myDBI;
use DBA;
use SysAccess;
use DBUtil;
use gHTML;
use Inv;

############################################################################
my $form = myForm->new();
my $dbh  = myDBI->dbconnect( $form->{'DBNAME'} );

unless ( SysAccess->hasClientAccess( $form, $form->{ClientID} ) ) {
    myDBI->error("Eligible Access Page / Not Client");
}

my $EBDate = DBA->EligibleDate($form);
my $out =
qq|Eligibility for: $form->{FName} $form->{LName} ($form->{ClientID}) ${EBDate}
InsCode\tBenefit\tBenefitDescr\tPlanDescr\tPolicyID\tPolicyName\tOtherInsCode\tOtherInsName\tPhone\tFromDate\tToDate\tRenewDate\n|;
my ( $cnt, $hdrline ) = ( 0, 2 );

my $qEligible =
qq|select * from Eligible where ClientID=? and (? between FromDate and ToDate) order by InsCode,Benefit,PlanDescr|;
my $sEligible = $dbh->prepare($qEligible);
$sEligible->execute( $form->{ClientID}, $EBDate ) || myDBI->dberror($qEligible);
while ( my $rEligible = $sEligible->fetchrow_hashref ) {
    $cnt++;
    $out .=
qq|$rEligible->{InsCode}\t$rEligible->{Benefit}\t$rEligible->{BenefitDescr}\t$rEligible->{PlanDescr}\t$rEligible->{PolicyID}\t$rEligible->{PolicyName}\t$rEligible->{OtherInsCode}\t$rEligible->{OtherInsName}\t$rEligible->{Ph}\t$rEligible->{FromDate}\t$rEligible->{ToDate}\t$rEligible->{RenewDate}\n|;
}
my $html = gHTML->htmlReport( $out, $hdrline );
print
qq|Content-type: text/html\n\n<HTML>\n<HEAD><TITLE>Eligibility Report</TITLE></HEAD>\n<BODY >\n|
  . $html
  . qq|\n</BODY>\n</HTML>\n|;

myDBI->cleanup();
exit;
############################################################################
