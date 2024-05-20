#!/usr/bin/perl
use lib '/home/okmis/mis/src/lib';
use DBI;
use DBForm;
use SysAccess;
use DBA;
use cBill;
use uBill;

############################################################################
# get parameters and check access.
my $form = DBForm->new();
#warn qq|ENTER: Reconcile.cgi\n|;
my $dbh = $form->dbconnect();
if ( ! SysAccess->verify($form,'Privilege=BillingRemit') )
{ $form->error("Remittance Access / Not Found!"); }

my $NextLOC = qq|/cgi/bin/mis.cgi?misPOP=1&mlt=$form->{mlt}&misLINKS=$form->{misLINKS}&prompt=$form->{prompt}\n\n|;

############################################################################
if ( DBA->updSQLdone($form) )
{
#  $NextLOC = qq|/cgi/bin/ChartList.cgi?Client_ClientID=$form->{Client_ClientID}$form->{SortOptions}&mlt=$form->{mlt}&prompt=$form->{prompt}\n\n|;
#warn qq|Reconcile: Location: ${NextLOC}|;
  print qq|Location: ${NextLOC}|;
  $form->complete();
  exit;
}
############################################################################
# process
$qInsPaid="select * from InsPaid where ID=?";
$sInsPaid=$dbh->prepare($qInsPaid);
$qTreatment="select * from Treatment where TrID=?";
$sTreatment=$dbh->prepare($qTreatment);
$qNoteTrans="select * from NoteTrans where TrID=? and (InsCode=? or InsCode='09') and RecDate is null order by ID";
$sNoteTrans=$dbh->prepare($qNoteTrans);
$qRecTrans="update NoteTrans set InsCode=?,RefID=?,RecDate=?,PaidAmt=?,ICN=?,InsPaidID=?,Code='IR',DenCode=NULL where ID=?";
$sRecTrans=$dbh->prepare($qRecTrans);
$qRecInsPaidAmt="update InsPaid set RecAmt=? where ID=?";
$sRecInsPaidAmt=$dbh->prepare($qRecInsPaidAmt);
$qRecTreatment="update Treatment set BillStatus=5, StatusDate=?, RecDate=?, CIPDate=NULL, DenDate=NULL, DenCode=NULL where TrID=? and RecDate is null";
$sRecTreatment=$dbh->prepare($qRecTreatment);

foreach my $f ( sort keys %{$form} )
{ 
  if ( $f =~ /^TRID_/ )
  {
    my ($flag, $ID) = split('_',$f);
    my $TRID = $form->{"TRID_${ID}"};
    my $AMT = $form->{"AMT_${ID}"};
    my $TransID = '';
#warn "Reconcile: ID: ${ID} TRID: ${TRID} AMT: ${AMT}<BR>\n"; 
    if ( $TRID > 0 && $AMT ne '' )
    {
      $sInsPaid->execute($ID) || $form->dberror($qInsPaid);
      if ( my $rInsPaid = $sInsPaid->fetchrow_hashref )
      {
        $sTreatment->execute($TRID) || $form->dberror($qTreatment);
        if ( my $rTreatment = $sTreatment->fetchrow_hashref )
        {
#foreach $f (sort keys %{ $rTreatment }) { warn "Treatment-$f = $rTreatment->{$f}<BR>\n"; }
          $sNoteTrans->execute($TRID,$rInsPaid->{InsCode}) || $form->dberror($qNoteTrans);
          if ( my $rNoteTrans = $sNoteTrans->fetchrow_hashref )
          { $TransID = $rNoteTrans->{'ID'}; }
          my $r835 = ();
          $r835->{'TransID'}   = $TransID;
          $r835->{'TrID'}      = $TRID;
          $r835->{'ClientID'}  = $rInsPaid->{'ClientID'};
          $r835->{'ContDate'}  = $rTreatment->{'ContLogDate'};
          $r835->{'SCID'}      = $rTreatment->{'SCID'};
          $r835->{'RecDate'}   = $rInsPaid->{'TransDate'};
          $r835->{'RefID'}     = $rInsPaid->{'RefID'};
          $r835->{'PaidAmt'}   = $AMT;
          $r835->{'ICN'}       = $rInsPaid->{'ICN'};
          $r835->{'InsCode'}   = $rInsPaid->{'InsCode'};
          $r835->{'InsPaidID'} = $rInsPaid->{'ID'};
          my ($TrID,$SCID,$code,$type) = uBill->postClaim($form,$r835,'CL','IR');
          my $RecAmt = $rInsPaid->{RecAmt} + $AMT;
          $sRecInsPaidAmt->execute($RecAmt,$ID) || $form->dberror($qRecInsPaidAmt);
#warn qq|sRecInsPaidAmt($RecAmt,$ID)<BR>\n|;
        }
        else { warn qq|NO Treatment: ${TRID}<BR>\n|; }
      }
      else { warn qq|NO InsPaid: ${ID}<BR>\n|; }
    }
    else { warn qq|TRID<=0 and AMT<=0<BR>\n|; }
  }
}
$sInsPaid->finish();
$sTreatment->finish();
$sNoteTrans->finish();
$sRecTrans->finish();
$sRecInsPaidAmt->finish();
$sRecTreatment->finish();

print qq|Location: ${NextLOC}|;
$form->complete();
exit;
############################################################################
