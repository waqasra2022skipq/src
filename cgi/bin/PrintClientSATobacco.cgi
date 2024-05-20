#!/usr/bin/perl
use lib '/home/okmis/mis/src/lib';
use myConfig;
use DBI;
use DBForm;
use DBA;
use MgrTree;
use DBUtil;
use PDF;
use Time::Local;
$DT=localtime();

############################################################################
my $form = DBForm->new();
my $dbh = $form->dbconnect();
#warn "PrintClientSATobacco: IDs=$form->{'IDs'}\n";
##
# prepare selects...
##
my $sClientSATobacco = $dbh->prepare("select * from ClientSATobacco where ID=?");
my $sSATs = $dbh->prepare("select * from ClientSATobacco where ClientID=? and vdate < ? order by vdate desc");
my $sClient = $dbh->prepare("select * from Client where ClientID=?");
my $sProvider = $dbh->prepare("select * from Provider where ProvID=?");

############################################################################
my $xdp = qq|<?xml version="1.0" encoding="UTF-8" ?> 
<?xfa generator="XFA2_0" APIVersion="2.2.4333.0" ?>
<xdp:xdp xmlns:xdp="http://ns.adobe.com/xdp/" >
<xfa:datasets xmlns:xfa="http://www.xfa.org/schema/xfa-data/1.0/" >
<xfa:data>
<root>
|;
foreach my $ID ( split(' ',$form->{IDs}) )
{ 
#warn "PrintClientSATobacco: ID=${ID}\n";
  $sClientSATobacco->execute($ID) || $form->dberror("select ClientSATobacco: ${ID}");
  while ( my $rClientSATobacco = $sClientSATobacco->fetchrow_hashref )
  { $xdp .= main->printClientSATobacco($rClientSATobacco); }
}
my $pdfpath = myConfig->cfg('FormsPrintURL')."/PrintClientSATobacco_Rev2.pdf";
warn qq|pdfpath=$pdfpath\n|;
$xdp .= qq|
</root>
</xfa:data>
</xfa:datasets>
<pdf href="${pdfpath}" xmlns="http://ns.adobe.com/xdp/pdf/" />
</xdp:xdp>
|;
if ( $form->{LOGINPROVID} == 91 )
{
  open XML, ">/home/okmis/mis/src/debug/PrintClientSATobacco.out" or die "Couldn't open file: $!";
  print XML ${xdp};
  close(XML);
}
if ( $form->{file} )
{
  open OUT, ">$form->{file}" || die "Couldn't open '$form->{file}' file: $!"; 
  print OUT ${xdp};
  close(OUT);
}
else { print qq|Content-Type: application/vnd.adobe.xdp+xml\n\n${xdp}|; }
$sClientSATobacco->finish();
$sClient->finish();
$sProvider->finish();
$form->complete();
exit;
############################################################################

sub printClientSATobacco
{
  my ($self,$r) = @_;
  my $ClientID = $r->{'ClientID'};
#warn qq|ClientID=$ClientID\n|;
  $sClient->execute($ClientID) || $form->dberror("select Client: ${ClientID}");
  my $rClient = $sClient->fetchrow_hashref;
  my $ClientName = qq|$rClient->{'FName'} $rClient->{'LName'}|;
##
# Header info...
  my $AgencyID = MgrTree->getAgency($form,$rClient->{clinicClinicID});
  $sProvider->execute($AgencyID) || $form->dberror("select Provider: $AgencyID");
  my $rAgency = $sProvider->fetchrow_hashref;
  my $AgencyName = DBA->subxml($rAgency->{Name});
  my $AgencyAddr = $rAgency->{Addr1};
  $AgencyAddr .= $rAgency->{Addr2} . ', ' if ( $rAgency->{Addr2} );
  my $AgencyCSZ .= $rAgency->{City} . ', ' . $rAgency->{ST} . '  ' . $rAgency->{Zip};
  my $AgencyPh = 'Office: ' . $rAgency->{WkPh};
  my $AgencyFax = 'Fax: ' . $rAgency->{Fax};
##
  my $TheDate = $r->{'vdate'};
  my $cnt = 0;
  my @SATs = ();
  push(@SATs,$r);                   # store (because of 'desc') newest to oldest.
  $sSATs->execute($ClientID,$TheDate) || $form->dberror("select SATs: ${ClientID},${TheDate}");
  while ( my $rSATs = $sSATs->fetchrow_hashref )
  { $cnt++; push(@SATs,$rSATs); last if ( $cnt == 3 ); }
  my @REVSATs = reverse(@SATs);     # output in columns of oldest to newest.
  my $i = 0;
  my ($row1,$row2,$row3,$row4,$row5,$row6) = ('','','','','','');
  my ($row7,$row8,$row9,$row10,$row11) = ('','','','','');
  foreach my $rSATs ( @REVSATs )
  {
    $i++;
    # conversations...
    my $vDate = DBUtil->Date($rSATs->{'vdate'},'fmt','MMDDYY');
    my $qDate = DBUtil->Date($rSATs->{'qdate'},'fmt','MMDDYY');
    my $sTime = substr($rSATs->{stime},0,2).substr($rSATs->{stime},3,2);
    my $eTime = substr($rSATs->{etime},0,2).substr($rSATs->{etime},3,2);
# convert from SNOMED codes to 5 A's...
    $rSATs->{'smoke'} = $rSATs->{'SmokingStatus'} == 4 || $rSATs->{'SmokingStatus'} == 6
                      ? 1 : 0;
    $rSATs->{'quit'}  = $rSATs->{'SmokingStatus'} == 3 
                      ? 1 : 0;
    $rSATs->{'heavy'} = $rSATs->{'SmokingStatus'} == 1
                      ? 1 : 0;
    $rSATs->{'light'} = $rSATs->{'SmokingStatus'} == 2 || $rSATs->{'SmokingStatus'} == 5
                     || $rSATs->{'SmokingStatus'} == 7 || $rSATs->{'SmokingStatus'} == 8
                      ? 1 : 0;
#warn qq|SmokingStatus=$rSATs->{'SmokingStatus'}\n|;
#warn qq|smoke=$rSATs->{'smoke'}\n|;
#warn qq|quit=$rSATs->{'quit'}\n|;
#warn qq|light=$rSATs->{'light'}\n|;
#warn qq|heavy=$rSATs->{'heavy'}\n|;
    my $qyes = $rSATs->{'quit30'} ? 1 : 0;
    my $qno = $rSATs->{'quit30'} ? 0 : 1;
    $row1 .= qq|    <vdate${i}>${vDate}</vdate${i}>\n|;
    $row2 .= qq|    <stime${i}>${sTime}</stime${i}>\n|;
    $row3 .= qq|    <smoke${i}>$rSATs->{'smoke'}</smoke${i}>
    <quit${i}>$rSATs->{'quit'}</quit${i}>
    <light${i}>$rSATs->{'light'}</light${i}>
    <heavy${i}>$rSATs->{'heavy'}</heavy${i}>\n|;
    $row4 .= qq|    <benefits${i}>$rSATs->{'benefits'}</benefits${i}>
    <harms${i}>$rSATs->{'harms'}</harms${i}>
    <message${i}>$rSATs->{'message'}</message${i}>
    <difficulty${i}>$rSATs->{'difficulty'}</difficulty${i}>\n|;
    $row5 .= qq|    <reason${i}>|.DBA->subxml($rSATs->{'reason'}).qq|</reason${i}>
    <qyes${i}>${qyes}</qyes${i}>
    <qno${i}>${qno}</qno${i}>\n|;
    $row6 .= qq|    <qdate${i}>${qDate}</qdate${i}>
    <problem${i}>$rSATs->{'problem'}</problem${i}>
    <materials${i}>$rSATs->{'materials'}</materials${i}>
    <identify${i}>$rSATs->{'identify'}</identify${i}>
    <refer${i}>$rSATs->{'refer'}</refer${i}>
    <pharma${i}>$rSATs->{'pharma'}</pharma${i}>\n|;
    $row7 .= qq|    <assess${i}>$rSATs->{'assess'}</assess${i}>
    <ask${i}>$rSATs->{'ask'}</ask${i}>
    <reinforce${i}>$rSATs->{'reinforce'}</reinforce${i}>
    <encourage${i}>$rSATs->{'encourage'}</encourage${i}>
    <set${i}>$rSATs->{'followup'}</set${i}>\n|;
    $row8 .= qq|    <comments${i}>|.DBA->subxml($rSATs->{'comments'}).qq|</comments${i}>\n|;
    $row9 .= qq|    <etime${i}>${eTime}</etime${i}>\n|;
    $row10 .= qq|    <sign${i}>sign here$rSATs->{'sign'}</sign${i}>\n|;
    $row11 .= qq|    <credentials${i}>credentials here$rSATs->{'credentials'}</credentials${i}>\n|;
  }

  my $html = qq|
  <record>
   <agencyname>${AgencyName}</agencyname>
   <agencyaddress>${AgencyAddr}</agencyaddress>
   <agencycsz>${AgencyCSZ}</agencycsz>
   <agencyphone>${AgencyPh}</agencyphone>
   <clientname>${ClientName}</clientname>
   <idnumber>${ClientID}</idnumber>
   <row1>\n${row1}</row1>
   <row2>\n${row2}</row2>
   <row3>\n${row3}</row3>
   <row4>\n${row4}</row4>
   <row5>\n${row5}</row5>
   <row6>\n${row6}</row6>
   <row7>\n${row7}</row7>
   <row8>\n${row8}</row8>
   <row9>\n${row9}</row9>
   <row10>\n${row10}</row10>
   <row11>\n${row11}</row11>
  </record>
|;
  return($html);
}
############################################################################
