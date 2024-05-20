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
my $DT=localtime();

############################################################################
my $form = DBForm->new();
my $dbh = $form->dbconnect();
#warn "PrintSOGSGSI: IDs=$form->{'IDs'}\n";
#my $test=$form->{IDs}++;
#$form->{'IDs'} = qq|$form->{IDs} $test| if ( $form->{LOGINPROVID} == 91 );

##
# prepare selects...
##
my $sSOGSGSI = $dbh->prepare("select * from SOGSGSI where ID=?");
my $sClient = $dbh->prepare("select * from Client where ClientID=?");
my $qProvider = qq|select * from Provider where ProvID=?|;
my $sProvider = $dbh->prepare($qProvider);
############################################################################
my $xdp = qq|<?xml version="1.0" encoding="UTF-8" ?> 
<?xfa generator="XFA2_0" APIVersion="2.2.4333.0" ?>
<xdp:xdp xmlns:xdp="http://ns.adobe.com/xdp/" >
<xfa:datasets xmlns:xfa="http://www.xfa.org/schema/xfa-data/1.0/" >
<xfa:data>
<topmostSubform>
|;
foreach my $ID ( split(' ',$form->{IDs}) )
{ 
  $sSOGSGSI->execute($ID) || $form->dberror("PrintSOGSGSI: select SOGSGSI $ID");
  while ( my $rSOGSGSI = $sSOGSGSI->fetchrow_hashref )
  { $xdp .= main->printSOGSGSI($rSOGSGSI); }
}
my $pdfpath = myConfig->cfg('FormsPrintURL')."/PrintSOGSGSI_Rev2.pdf";
#warn qq|PrintSOGSGSI: pdfpath=$pdfpath\n|;
$xdp .= qq|
</topmostSubform>
</xfa:data>
</xfa:datasets>
<pdf href="${pdfpath}" xmlns="http://ns.adobe.com/xdp/pdf/" />
</xdp:xdp>
|;
$sSOGSGSI->finish();
$sClient->finish();
$sProvider->finish();

if ( $form->{LOGINPROVID} == 91 )
{
  open XML, ">/home/okmis/mis/src/debug/PrintSOGSGSI.out" or die "Couldn't open file: $!";
  print XML $xdp;
  close(XML);
}
if ( $form->{file} )
{
  open OUT, ">$form->{file}" || die "Couldn't open '$form->{file}' file: $!"; 
  print OUT ${xdp};
  close(OUT);
}
else { print qq|Content-Type: application/vnd.adobe.xdp+xml\n\n${xdp}|; }
$form->complete();
exit;
############################################################################
sub printSOGSGSI
{
  my ($self,$r) = @_;
#foreach my $f ( sort keys %{$r} ) { warn "1: r-$f=$r->{$f}\n"; }
##
# Client info...
  my $ClientID = $r->{'ClientID'};
  $sClient->execute($ClientID) || $form->dberror("PrintSOGSGSI: select Client $ClientID");
  my $rClient = $sClient->fetchrow_hashref;
  my $memberid = qq|$rClient->{FName} $rClient->{LName} ($rClient->{ClientID})|;
##
# Header info...
  my $AgencyID = MgrTree->getAgency($form,$rClient->{clinicClinicID});
  $sProvider->execute($AgencyID) || $form->dberror($qProvider);
  my $rAgency = $sProvider->fetchrow_hashref;
  my $AgencyName = DBA->subxml($rAgency->{Name});
  my $AgencyAddr = $rAgency->{Addr1} . ', ';
  $AgencyAddr .= $rAgency->{Addr2} . ', ' if ( $rAgency->{Addr2} );
  my $AgencyCSZ .= $rAgency->{City} . ', ' . $rAgency->{ST} . '  ' . $rAgency->{Zip};
  my $AgencyPh = 'Office: ' . $rAgency->{WkPh} . '  Fax: ' . $rAgency->{Fax};
##
# Translate...
  $sProvider->execute($r->{ProvID}) || $form->dberror("PrintSOGSGSI: select Provider $r->{'ProvID'}");
  my $rProvider = $sProvider->fetchrow_hashref;
  my $providerid = qq|$rProvider->{'FName'} $rProvider->{'LName'} ($rProvider->{'ProvID'})|;
  my $mm = substr($r->{'TransDate'},5,2);
  my $dd = substr($r->{'TransDate'},8,2);
  my $yyyy = substr($r->{'TransDate'},0,4);
  my $TransDate = DBUtil->Date($r->{'TransDate'},'fmt','MM/DD/YYYY');
  my $admit = $r->{'TransType'} eq 'A' ? 1 : 0;
  my $update = $r->{'TransType'} eq 'U' ? 1 : 0;
  my $discharge = $r->{'TransType'} eq 'D' ? 1 : 0;
  $r->{G20} = sprintf("%.0f",$r->{G20});
  my $G25M = $r->{'G25M'} < 3 ? 0 : 1;
  my $G26M = $r->{'G26M'} < 2 ? 0 : 1;
  my $G27M = $r->{'G27M'} < 2 ? 0 : 1;
  my $totalpage6 = ${G25M}
                 + ${G26M}
                 + ${G27M}
                 + $r->{'G28M'}
                 + $r->{'G29M'}
                 + $r->{'G30M'}
                 + $r->{'G31M'}
                 + $r->{'G32M'}    # not G33M
                 + $r->{'G34M'}
                 + $r->{'G35M'}
                 + $r->{'G36M'}
                 + $r->{'G37aM'}
                 + $r->{'G37bM'}
                 + $r->{'G37cM'}
                 + $r->{'G37dM'}
                 + $r->{'G37eM'}
                 + $r->{'G37fM'}
                 + $r->{'G37gM'}
                 + $r->{'G37hM'}
                 + $r->{'G37iM'};
  my ($txt,$page1,$page2,$page3,$page4,$page5,$page6) = ('','','','','','','');
  my $flds = DBA->getFieldDefs($form,'SOGSGSI');
  my $sshow = $dbh->prepare("show fields from SOGSGSI");
  $sshow->execute() || $form->dberror("PrintSOGSGSI: select SOGSGSI fields");
  while ( my $rshow = $sshow->fetchrow_hashref )
  {
    my $f = $rshow->{'Field'};
    if ( $f eq 'ACOM' )
    { $txt = qq|   <$f>|.DBA->subxml($r->{$f}).qq|</$f>\n|; }
    elsif ( $f eq 'G8COM' )
    { $page1 = $txt; $txt = qq|   <$f>|.DBA->subxml($r->{$f}).qq|</$f>\n|; }
    elsif ( $f eq 'G25COM' )
    { $page2 = $txt; $txt = qq|   <$f>|.DBA->subxml($r->{$f}).qq|</$f>\n|; }
    elsif ( $f eq 'G37COM' )
    { $page3 = $txt; $txt = qq|   <$f>|.DBA->subxml($r->{$f}).qq|</$f>\n|; }
    else
    { $txt .= qq|   <$f>|.DBA->subxml($r->{$f}).qq|</$f>\n|; }
  }
  $page4 = $txt;
  $sshow->finish();
  my $rInsurance = cBill->getInsurance($form,$r->{ClientID},'primary',$r->{TransDate});
  my $staffsig1 = DBA->setProvCreds($form,$r->{'ProvID'},$rInsurance->{InsID});
warn qq|ProvID=$r->{ProvID},InsID=$rInsurance->{InsID},staffsig1=$staffsig1\n|;

  my $html = qq|
 <Page>
  <recordid>$r->{'ID'}</recordid>
   <memberid>${memberid}</memberid>
   <providerid>${providerid}</providerid>
   <mm>${mm}</mm>
   <dd>${dd}</dd>
   <yyyy>${yyyy}</yyyy>
   <admit>${admit}</admit>
   <update>${update}</update>
   <discharge>${discharge}</discharge>
${page1}
   <medicaidid>$rInsurance->{'InsIDNum'}</medicaidid>
${page2}
   <medicaidid>$rInsurance->{'InsIDNum'}</medicaidid>
${page3}
   <medicaidid>$rInsurance->{'InsIDNum'}</medicaidid>
${page4}
   <staffsig1>${staffsig1}</staffsig1>
   <staffsig2>$r->{'XXX'}</staffsig2>
   <date>${TransDate}</date>
   <medicaidid>$rInsurance->{'InsIDNum'}</medicaidid>
${page5}
   <l13>$r->{'G13D'}</l13>
   <l14>$r->{'G14D'}</l14>
   <l22>$r->{'G22'}</l22>
   <l1>$r->{'XXX'}</l1>
   <l20>$r->{'G20'}</l20>
   <l24>$r->{'XXX'}</l24>
   <q25>${G25M}</q25>
   <q26>${G26M}</q26>
   <q27>${G27M}</q27>
${page6}
   <q28>$r->{'G28M'}</q28>
   <q29>$r->{'G29M'}</q29>
   <q30>$r->{'G30M'}</q30>
   <q31>$r->{'G31M'}</q31>
   <q32>$r->{'G32M'}</q32>
   <q33>$r->{'G33M'}</q33>
   <q34>$r->{'G34M'}</q34>
   <q35>$r->{'G35M'}</q35>
   <q36>$r->{'G36M'}</q36>
   <q37a>$r->{'G37aM'}</q37a>
   <q37b>$r->{'G37bM'}</q37b>
   <q37c>$r->{'G37cM'}</q37c>
   <q37d>$r->{'G37dM'}</q37d>
   <q37e>$r->{'G37eM'}</q37e>
   <q37f>$r->{'G37fM'}</q37f>
   <q37g>$r->{'G37gM'}</q37g>
   <q37h>$r->{'G37hM'}</q37h>
   <q37i>$r->{'G37iM'}</q37i>
   <totalpage6>${totalpage6}</totalpage6>
   <l38>$r->{'G38'}</l38>
   <l39>$r->{'G39'}</l39>
 </Page>
|;
  return($html);
}
############################################################################
