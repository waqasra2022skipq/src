#!/usr/bin/perl
use lib '/home/okmis/mis/src/lib';
use DBI;
use DBForm;
use MgrTree;
use DBA;
use uCalc;
use PDF;
use Time::Local;
my $DT=localtime();

############################################################################
my $form = DBForm->new();
my $dbh = $form->dbconnect();
my $qProvider = qq|select * from Provider where ProvID=?|;
my $sProvider = $dbh->prepare($qProvider);
my $qInvItems = qq|select * from InvItems where InvItems.InvID=? order by InvItems.ContDate|;
#warn "qInvItems=\n$qInvItems\n";
my $sInvItems = $dbh->prepare($qInvItems);

############################################################################
my $qClientBasis32 = qq|select * from ClientBasis32 left join Client on Client.ClientID=ClientBasis32.ClientID where ClientBasis32.ID=?|;
#warn "qClientBasis32=\n$qClientBasis32\n";
my $sClientBasis32 = $dbh->prepare($qClientBasis32);
warn "\nGenerating ClientBasis32:\n";
$pdf = PDF->start("/home/okmis/mis/src/pdf/ClientBasis32.pdt");
my $Cnt = 0;
foreach my $ID ( split(' ',$form->{'IDs'}) )
{ 
  $sClientBasis32->execute($ID) || $form->dberror($qClientBasis32);
  if ( my $rClientBasis32 = $sClientBasis32->fetchrow_hashref ) { &genClientBasis32($rClientBasis32); $Cnt++; }
}
if ( ${Cnt} == 0 )
{ $pdf->add('',"/R5 14 Tf\n1 0 0 1 40 740 Tm (No Basis for selection.) Tj\n"); }
$pdf->finish();
#print $pdf->{outText};
warn "${Cnt} ClientBasis32 Generated\n";
print qq|Content-Type: application/pdf\n\n$pdf->{outText}|;

$sProvider->finish;
$sClientBasis32->finish;
$form->complete();
exit;
############################################################################
sub genClientBasis32
{
  my ($rClientBasis32) = @_;
##
# Agency Name and address.
##
  my $AgencyID = MgrTree->getManager($form,$rClientBasis32->{clinicClinicID});
  $sProvider->execute($AgencyID) || $form->dberror($qProvider);
  my $rAgency = $sProvider->fetchrow_hashref;
# 290 (width of page) / 2 (in half) * 5 (boldness&size of font)
  my $AgencyName = $rAgency->{Name};
  my $x = (290 - ((length($AgencyName) / 2) * 5));
  $pdf->addElement($x,740,$AgencyName,'/R5',14);
  my $AgencyAddr = $rAgency->{Addr1};
  my $x = (290 - ((length($AgencyAddr) / 2) * 4));
  $pdf->addElement($x,729,$AgencyAddr,'/R10',12);
  my $AgencyCSZ = qq|$rAgency->{City}, $rAgency->{ST}   $rAgency->{Zip}|;
  my $x = (290 - ((length($AgencyCSZ) / 2) * 4));
  $pdf->addElement($x,718,$AgencyCSZ,'/R10',12);
  my $AgencyPh1 = qq|Office: $rAgency->{WkPh}|;
  my $x = (290 - ((length($AgencyPh1) / 2) * 4));
  $pdf->addElement($x,707,$AgencyPh1,'/R10',12);
  my $AgencyPh2 = qq|Fax: $rAgency->{Fax}|;
  my $x = (290 - ((length($AgencyPh2) / 2) * 4));
  $pdf->addElement($x,696,$AgencyPh2,'/R10',12);
#  $pdf->addElement(510,655,"$rClientBasis32->{ID}",'/R5',12);
  $pdf->addElement(31,655,"$rClientBasis32->{FName} $rClientBasis32->{LName} ($rClientBasis32->{ClientID})",'/R5',12);
  my $EffDate = DBUtil->Date($rClientBasis32->{EffDate},'fmt','MM/DD/YY');
#  my $ExpDate = DBUtil->Date($rClientBasis32->{ExpDate},'fmt','MM/DD/YY');
#  $pdf->addElement(445,655,"Date: ${EffDate} - ${ExpDate}",'/R5',12);
  $pdf->addElement(445,655,"Date: ${EffDate}",'/R5',12);

  my @args = ();
  my $w = 11;            # line width.
  my $x = 564;           # 
  my $y = 556 + $w;      # start 1 up.
  $pdf->addElement(550,$y+$w,'Score','/R10',10);
  for ( $i=1; $i<=32; $i++ )
  {
    my $fld = length($i) == 1 ? 'B0' . $i : 'B' . $i;
    $pdf->addElement($x,$y-($w*$i),$rClientBasis32->{$fld},'/R10',10);
    #$y -= $w if ( $i==13 );     # skip a line after 13.
    push(@args,$rClientBasis32->{$fld});
  }
  my ($Avg,$Tot) = DBUtil->gTotal('not0',@args);
  $Tot = sprintf("%.2f",$Tot);
  $Avg = sprintf("%.2f",$Avg);
  $pdf->addElement(513,182,"Total:",'/R10',10);
  $pdf->addElement(550,182,"${Tot}",'/R10',10);
  $pdf->addElement(498,171,"Average:",'/R10',10);
  $pdf->addElement(553,171," ${Avg}",'/R10',10);

  my @counts = uCalc->calcB32($form,$rClientBasis32);
#for ($k=1; $k<=5; $k++) { warn qq|htmB32: cnt:${cnt} k=${k}, tot=$counts[$k][2] / cnt=$counts[$k][1]\n|; }
  my $Dom1 = sprintf("%.2f",$counts[1][1] ? $counts[1][2] / $counts[1][1] : 0);
  my $Dom2 = sprintf("%.2f",$counts[2][1] ? $counts[2][2] / $counts[2][1] : 0);
  my $Dom3 = sprintf("%.2f",$counts[3][1] ? $counts[3][2] / $counts[3][1] : 0);
  my $Dom4 = sprintf("%.2f",$counts[4][1] ? $counts[4][2] / $counts[4][1] : 0);
  my $Dom5 = sprintf("%.2f",$counts[5][1] ? $counts[5][2] / $counts[5][1] : 0);
#warn qq|1=$Dom1, 2=$Dom2, 3=$Dom3, 4=$Dom4, 5=$Dom5\n|;
  $pdf->addElement(31,150,"Relation to Self / Others",'/R10',10);
  $pdf->addElement(77,139,$Dom1,'/R10',10);
  $pdf->addElement(155,150,"Daily Living / Role Functioning",'/R10',10);
  $pdf->addElement(202,139,$Dom2,'/R10',10);
  $pdf->addElement(310,150,"Depression / Anxiety",'/R10',10);
  $pdf->addElement(350,139,$Dom3,'/R10',10);
  $pdf->addElement(414,150,"Impulsive / Addictive",'/R10',10);
  $pdf->addElement(450,139,$Dom4,'/R10',10);
  $pdf->addElement(535,150,"Psychosis",'/R10',10);
  $pdf->addElement(550,139,$Dom5,'/R10',10);

#  $pdf->add('deflate',$out);
  $pdf->add('','');
  return(1);
}
############################################################################
