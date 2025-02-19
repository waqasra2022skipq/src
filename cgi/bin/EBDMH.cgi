#!/usr/bin/perl
############################################################################
use lib '/var/www/okmis/src/lib';
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

#foreach my $f ( sort keys %{$form} ) { warn "EBDMH: form-$f=$form->{$f}\n"; }

unless ( SysAccess->hasClientAccess( $form, $form->{ClientID} ) ) {
    myDBI->error("DMH Eligible Access Page / Not Client");
}

my $out = qq|Legend: 
TXIX = Recipient is shown to be eligible for Medicaid by ODMHSAS records
DMH = Recipient is shown to be eligible for ODMHSAS services by ODMHSAS records
OCH = Recipient is shown to be eligible for Oklahoma Complete Health by ODMHSAS records
HUM = Recipient is shown to be eligible for Humana by ODMHSAS records
AET = Recipient is shown to be eligible for Aetna by ODMHSAS records
REHAB = Recipient is eligible for rehab services
CASEMGMT = Recipient is eligible for the old case mgmt units (25 per month) otherwise the customer is only eligible for 16 a year
CASEMGMTUNITS 0-16 Amount of units ODMHSAS can see the customer has already used on/after 9/1/2017 for the rolling year. Will always be 0 if CASEMGMT = 1.
CCBHC = Recipient is active in a CCBHC as of today
DMH Eligibility for: $form->{FName} $form->{LName} ($form->{ClientID})
InsIDNum\tTXIX\tDBH\tOCH\tHUM\tAET\tREHAB\tCASEMGMT\tCASEMGMTUNITS\tCCBHC\tBAD ADDRESS\tLastChecked\tStatus
|;
my ( $cnt, $hdrline ) = ( 0, 10 );

my $qEligible = qq|select * from EligibleDMH where RECIPIENTID=?|;

#warn qq|q=\n${qEligible}\n$form->{InsNumID}\n|;
my $sEligible = $dbh->prepare($qEligible);
$sEligible->execute( $form->{InsNumID} ) || myDBI->dberror($qEligible);
while ( my $rEligible = $sEligible->fetchrow_hashref ) {
    $cnt++;
    my $TXIX     = $rEligible->{'TXIX'}       ? 'true'   : 'false';
    my $DMH      = $rEligible->{'DMH'}        ? 'true'   : 'false';
    my $REHAB    = $rEligible->{'REHAB'}      ? 'true'   : 'false';
    my $CASEMGMT = $rEligible->{'CASEMGMT'}   ? 'true'   : 'false';
    my $CCBHC    = $rEligible->{'CCBHC'}      ? 'true'   : 'false';
    my $BADADDR  = $rEligible->{'BADADDRESS'} ? 'true'   : 'false';
    my $Status = $rEligible->{'Fail'} eq '' ? 'Received' : $rEligible->{'Fail'};
    my $OCH    = $rEligible->{'OCH'}        ? 'true'     : 'false';
    my $HUM    = $rEligible->{'HUM'}        ? 'true'     : 'false';
    my $AET    = $rEligible->{'AET'}        ? 'true'     : 'false';

    $out .=
qq|$rEligible->{RECIPIENTID}\t${TXIX}\t${DMH}\t${OCH}\t${HUM}\t${AET}\t${REHAB}\t${CASEMGMT}\t$rEligible->{CASEMGMTUNITS}\t${CCBHC}\t${BADADDR}\t$rEligible->{StatusDate}\t${Status}\n|;
}
$out .= qq|None found! Click the Check DMH button| if ( $cnt == 0 );
my $html = gHTML->htmlReport( $out, $hdrline );
print
qq|Content-type: text/html\n\n<HTML>\n<HEAD><TITLE>Eligibility Report</TITLE></HEAD>\n<BODY >\n|
  . $html
  . qq|\n</BODY>\n</HTML>\n|;

myDBI->cleanup();
exit;
############################################################################
