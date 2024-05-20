#!/usr/bin/perl
use lib '/home/okmis/mis/src/lib';
use DBI;
use myForm;
use myDBI;
use myHTML;
use SysAccess;

############################################################################
my $form = myForm->new();
my $dbh = myDBI->dbconnect($form->{'DBNAME'});
#foreach my $f ( sort keys %{$form} ) { warn "dupxTable: form-$f=$form->{$f}\n"; }
if ( ! SysAccess->chkPriv($form,'Agent') )
{ myDBI->error("Duplicate / Access Denied!"); }
if ( $form->{'ID'} eq '' )
{ myDBI->error("Duplicate / NO ID!"); }

my $PrAuthID = $form->{'PrAuthID'};
my $sPrAuth = $dbh->prepare("select * from ClientPrAuth where ID=?");
$sPrAuth->execute($PrAuthID) || myDBI->dberror("dupxTable: select PrAuth ${PrAuthID}");
my $rPrAuth = $sPrAuth->fetchrow_hashref;
my $sPrAuthCDC = $dbh->prepare("select * from ClientPrAuthCDC where ClientPrAuthID=?");
$sPrAuthCDC->execute($PrAuthID) || myDBI->dberror("dupxTable: select PrAuthCDC ${PrAuthID}");
my $rPrAuthCDC = $sPrAuthCDC->fetchrow_hashref;
if ( $form->{submit} ) { print main->submit(); }
else { print main->html(); }

$sPrAuth->finish();
$sPrAuthCDC->finish();

myDBI->cleanup();
exit;

############################################################################
sub submit
{
  my $Reason = $form->{'Reason'};
  my $AuthNum = $form->{'AuthNum'};
  my $CDCKey = $form->{'CDCKey'};
  my $html =  myHTML->close(1);
  if ( $Reason eq '' || $AuthNum eq '' )
  { $html = main->html("Reason or AuthNum CANNOT be null!"); }
  else
  {
#warn qq|update....PrAuthID=$PrAuthID\n|;
    my $PAgroup = $rPrAuth->{'PAgroup'};
    my $LinesAuth = DBA->getxref($form,'xPAgroups',$PAgroup,'PAlines');
    my $EffDate = $rPrAuth->{'EffDate'};
    my ($months,$days) = DBA->calcLOS($form,'100',$PAgroup);
    my $Age = DBUtil->Date($rPrAuth->{'DOB'},'age',$EffDate);
    my $which = $Age < 21 ? 'ChildAmt' : 'AdultAmt';
    my $Cost = DBA->getxref($form,'xPAgroups',$PAgroup,$which);
    my $Units = DBA->getxref($form,'xPAgroups',$PAgroup,'Units');
    my $rUpdate = ();
    $rUpdate->{PAnumber} = $AuthNum;
    $rUpdate->{'ExpDate'} = DBUtil->Date($EffDate,$months,$days);
    $rUpdate->{'LOS'} = $months;
    $rUpdate->{'LinesAuth'} = $LinesAuth;
    $rUpdate->{'AuthAmt'} = $Cost*$LinesAuth;
    $rUpdate->{'UnitsAuth'} = $Units;                     # used if >0 (Inv.pm)
    $rUpdate->{'Locked'} = 1;
    $rUpdate->{'ChangeProvID'} = $form->{'LOGINPROVID'};
#foreach my $f ( sort keys %{$rUpdate} ) { warn "dupxTable 1: rUpdate-$f=$rUpdate->{$f}\n"; }
    my $ID1 = DBA->doUpdate($form,'ClientPrAuth',$rUpdate,"ID='${PrAuthID}'");
    my $rUpdateCDC = ();
    $rUpdateCDC->{Status} = 'Approved';
    $rUpdateCDC->{StatusDate} = $form->{TODAY};
    $rUpdateCDC->{Reason} = 'Manual: '.$Reason;
    $rUpdateCDC->{Fail} = '';
    $rUpdateCDC->{CDCKey} = $CDCKey if ( $CDCKey ne '' );
    $rUpdateCDC->{'ChangeProvID'} = $form->{'LOGINPROVID'};
#foreach my $f ( sort keys %{$rUpdateCDC} ) { warn "dupxTable 2: rUpdateCDC-$f=$rUpdateCDC->{$f}\n"; }
    my $ID2 = DBA->doUpdate($form,'ClientPrAuthCDC',$rUpdateCDC,"ClientPrAuthID='${PrAuthID}'");

    Inv->setPALines($form,$PrAuthID);

    delete $rPrAuthCDC->{"ClientPrAuthID"};       # remove ID to the PrAuth.
    $rPrAuthCDC->{"ClientPrAuthCDCID"} = $ID2;    # attach to the CDC.
    $rPrAuthCDC->{'Status'} = $rUpdateCDC->{'Status'};
    $rPrAuthCDC->{'StatusDate'} = $rUpdateCDC->{'StatusDate'};
    $rPrAuthCDC->{'Reason'} = $rUpdateCDC->{'Reason'};
    $rPrAuthCDC->{'CDCKey'} = $rUpdateCDC->{'CDCKey'};
    $rPrAuthCDC->{'ChangeProvID'} = $rUpdateCDC->{'ChangeProvID'};
    my $LogID = DBA->doUpdate($form,"ClientPrAuthCDCSent",$rPrAuthCDC);
    CDC->Lock($form,'ClientPrAuth',$PrAuthID,1);
  }
  return($html);
}
############################################################################
