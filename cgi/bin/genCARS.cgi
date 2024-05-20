#!/usr/bin/perl
use lib '/home/okmis/mis/src/lib';
use CGI qw(:standard escape);
use Cwd;
use DBI;
use myForm;
use myDBI;
use DBA;
use DBUtil;
use PDF;
use Time::Local;

############################################################################
my $form = myForm->new();
my $dbh = myDBI->dbconnect($form->{'DBNAME'});
chdir("$form->{DOCROOT}/tmp");
$pwd=cwd();
$DT=localtime();

############################################################################
# usage:
############################################################################
#warn qq|CARS Summary PDF: $DT, pwd=$pwd\n|;
############################################################################
%Months = (
    '01' => 'JANUARY',
    '02' => 'FEBRUARY',
    '03' => 'MARCH',
    '04' => 'APRIL',
    '05' => 'MAY',
    '06' => 'JUNE',
    '07' => 'JULY',
    '08' => 'AUGUST',
    '09' => 'SEPTEMBER',
    '10' => 'OCTOBER',
    '11' => 'NOVEMBER',
    '12' => 'DECEMBER',
);
############################################################################
my $sClinic = $dbh->prepare('select * from Provider where ProvID=?');
my $sContracts = $dbh->prepare('select * from Contracts left join xInsurance on xInsurance.ID=Contracts.InsID where ProvID=? and xInsurance.Descr=?');
my $sProvider = $dbh->prepare('select * from Provider where ProvID=?');
$qClient = qq|select * from Client left join ClientIntake on ClientIntake.ClientID=Client.ClientID where Client.ClientID=?|;
my $sClient = $dbh->prepare($qClient);
my $sClientLegalPP = $dbh->prepare('select * from ClientLegalPP where ClientID=? order by CreateDate');
my $sClientReferrals = $dbh->prepare('select * from ClientReferrals where ClientID=?');
warn "ClientCARSReview_ID=$form->{'ClientCARSReview_ID'}\n";
############################################################################
if ( $form->{ClientCARSReview_ID} )
{
  my $sCARSReviewMonth = $dbh->prepare("select * from ClientCARSReview where ID=?");
  $sCARSReviewMonth->execute($form->{ClientCARSReview_ID}) || myDBI->dberror("select CARSReviewMonth");
  my $rCARSReviewMonth = $sCARSReviewMonth->fetchrow_hashref;
foreach my $f ( sort keys %{$rCARSReviewMonth} ) { warn ": rCARSReviewMonth-$f=$rCARSReviewMonth->{$f}\n"; }
  $form->{YYYYMM} = $rCARSReviewMonth->{Month};
  $sCARSReviewMonth->finish;
}
my $TheDate = $form->{YYYYMM} ? $form->{YYYYMM} . '-01' : $form->{TODAY};
my $YearMonth = substr($TheDate,0,7);
my ($FromDate,$ToDate) = DBUtil->Date($TheDate,'monthly',0);
($Year, $month, $day) = split(/-/, ${TheDate});
my $MonthName = $Months{$month};
warn "TheDate=$TheDate, YearMonth=$YearMonth\n";
warn "FromDate=$FromDate, ToDate=$ToDate\n";
warn "Year=$Year, month=$month, day=$day, MonthName=$MonthName\n";
my $sClientCARSReview = $dbh->prepare("select * from ClientCARSReview where ClientID=? and Month='${YearMonth}'");
my $qFirstContact = qq|select ContLogDate from Treatment where ClientID=? order by ContLogDate|;
#warn "qFirstContact=\n$qFirstContact\n";
my $sFirstContact = $dbh->prepare($qFirstContact);
my $qHours = qq|
select * 
  from Treatment
    left join xSC on xSC.SCID=Treatment.SCID
    left join xSCRates on xSCRates.SCID=xSC.SCID
    left join xInsurance on xInsurance.ID=xSC.InsID
  where (xInsurance.Descr='cars' or xInsurance.Descr LIKE '%medicaid%')
    and ClientID=? 
    and xSCRates.EffDate <= Treatment.ContLogDate
    and ( Treatment.ContLogDate <= xSCRates.ExpDate or xSCRates.ExpDate is null)
    and Treatment.ContLogDate >= '${FromDate}'
    and Treatment.ContLogDate <= '${ToDate}'
 order by ContLogDate
|;
#warn "qHours=\n$qHours\n";
my $sHours = $dbh->prepare($qHours);

############################################################################
# this is the pdf template we need
#   it is the first 3 objects with 2 font objects and the content object
$pdtpath = '/home/okmis/mis/src/pdf/CARS.pdt';
if ( $form->{Client_ClientID} )
{
  $pdf = PDF->start($pdtpath);
  $sClient->execute($form->{Client_ClientID}) || myDBI->dberror($qClient);
  while ( my $r = $sClient->fetchrow_hashref ) { &printPDF($r); }
  $sClient->finish;
  $pdf->finish();
print qq|Content-Type: application/pdf\n\n$pdf->{outText}|;
#  my $file = 'genCARS_' . DBUtil->genToken() . '_' . DBUtil->Date('','stamp') . '.pdf';
#  open PDFFILE, ">${file}" or die "Couldn't open file: $!";
#  print PDFFILE $pdf->{outText};
#  close(PDFFILE);
## html file is /tmp -> https:://DOCROOT/tmp
#  print qq|Content-Type: text/html
#
#
#<HTML><TITLE>Print PDF</TITLE>
#<BODY>
#Click <A HREF="/tmp/${file}">here</A> to download pdf.
#</BODY>
#</HTML>
#          |;
}
else
{
  $pdf = PDF->start($pdtpath);
##
# entire selection changed to just pull off CustAgency
#   for Tausha Mayberry (ETI); ok with Chris Dhoku and Wade
#   1/11/2007
##
  my $ForProvID = $form->{Provider} ? $form->{Provider} : $form->{LOGINPROVID};
  my $ClinicSelection = DBA->getClinicSelection($form,$ForProvID,'Client.clinicClinicID');
  my $qBySelect = qq|
select Client.ClientID, Provider.ProvID, ClientLegal.JOLTS, ClientLegal.CustAgency
  from Client
    left join ClientLegal on ClientLegal.ClientID=Client.ClientID
    left join Provider on Provider.ProvID=Client.ProvID
  where Client.Active=1
    and (ClientLegal.CustAgency='JSUC' or ClientLegal.CustAgency='JBDC')
    ${ClinicSelection}
  group by Provider.LName, Provider.FName, Client.LName, Client.FName 
|;
#warn "q=$qBySelect\n";
  my $sBySelect = $dbh->prepare($qBySelect);
  $sBySelect->execute() || myDBI->dberror($qBySelect);
  while (my $rBySelect = $sBySelect->fetchrow_hashref) 
  { 
#warn "Client is = $rBySelect->{ClientID}\n";
    $sClient->execute($rBySelect->{ClientID}) || myDBI->dberror($qClient);
    while ( my $r = $sClient->fetchrow_hashref ) { &printPDF($r); }
  }
  $sClient->finish;
  $sBySelect->finish();
  $pdf->finish();
print qq|Content-Type: application/pdf\n\n$pdf->{outText}|;
#  my $file = 'genCARS_' . DBUtil->genToken() . '_' . DBUtil->Date('','stamp') . '.pdf';
#  open PDFFILE, ">${file}" or die "Couldn't open file: $!";
#  print PDFFILE $pdf->{outText};
#  close(PDFFILE);
## html file is /tmp -> https:://DOCROOT/tmp
#  print qq|Content-Type: text/html
#
#
#<HTML><TITLE>Print PDF</TITLE>
#<BODY>
#Click <A HREF="/tmp/${file}">here</A> to download pdf.
#</BODY>
#</HTML>
#          |;
}
$sClinic->finish();
$sContracts->finish();
$sProvider->finish();
$sHours->finish();
$sFirstContact->finish();
$sClientCARSReview->finish();
$sClientLegalPP->finish();
$sClientReferrals->finish();
myDBI->cleanup();
exit;

############################################################################
sub printPDF(\%)
{
  my ($rClient) = @_;

  my $ClientID=$rClient->{ClientID};
  my $ClinicID=$rClient->{clinicClinicID};
  my $ClientProvID=$rClient->{ProvID};
  $sClinic->execute($ClinicID);
  my $rClinic = $sClinic->fetchrow_hashref;
  $sContracts->execute($ClinicID,'cars');
  my $hdr = qq|Monthly Case Summary Report|;
  $hdr = qq|CARS Monthly Report| if ( my $rContracts = $sContracts->fetchrow_hashref );
#warn "$ClinicID: $rClinic->{Name} ($rClient->{FName} $rClient->{LName})\n";
  $AgencyName = $rClinic->{Name};
  $AgencyAddr = $rClinic->{Addr1} . ', ';
  $AgencyAddr .= $rClinic->{Addr2} . ', ' if ( $rClinic->{Addr2} );
  $AgencyAddr .= $rClinic->{City} . ', ' . $rClinic->{ST} . '  ' . $rClinic->{Zip};
  $AgencyPh = 'Office: ' . $rClinic->{WkPh} . '  Fax: ' . $rClinic->{Fax};
  $sProvider->execute($ClientProvID);
  my $rProvider = $sProvider->fetchrow_hashref;
  my $ProvName = qq|$rProvider->{FName} $rProvider->{LName}|;
  $sClientLegalPP->execute($ClientID) || myDBI->dberror("select ClientLegalPP ${ClientID}");
  my $rClientLegalPP = $sClientLegalPP->fetchrow_hashref;
  $sClientReferrals->execute($ClientID) || myDBI->dberror("select ClientReferrals ${ClientID}");
  my $rClientReferrals = $sClientReferrals->fetchrow_hashref;
  my $RefAgency = DBA->getxref($form,'xReferralTypes',$rClientReferrals->{'ReferredBy1Type'},'Descr');
#warn "RefAgency=${RefAgency}: $rClientReferrals->{Name} ($rClientReferrals->{'ReferredBy1NPI'} $rClientReferrals->{'ReferredBy1Type'})\n";
  if ( $rClientReferrals->{'ReferredBy1NPI'} ne '' )
  {
    my $rxNPI = DBA->selxref($form,'xNPI','NPI',$rClientReferrals->{'ReferredBy1NPI'});
    $RefAgency = $rxNPI->{'ProvOrgName'};
  }
#warn "RefAgency=${RefAgency}: $rClientReferrals->{Name} ($rClientReferrals->{'ReferredBy1NPI'} $rClientReferrals->{'ReferredBy1Type'})\n";
#warn "$ClientID\t$rClient->{LName}\t$rClient->{FName}\n";

  my $Client_DOBAmr = DBUtil->Date($rClient->{DOB},'fmt','MM/DD/YYYY');

  $sFirstContact->execute($ClientID);
  my ($FirstContDate) = $sFirstContact->fetchrow_array; 
  my ($Ind,$IndRehab,$Grp,$GrpRehab,$Fam,$TPDevel,$TPReview,$Para,$Assess,$Others,$TotHrs) = (0,0,0,0,0,0,0,0,0,0,0);
  my $NoShows = (); my $NSCnt = 0;
#warn qq|\n$qHours\n$ClientID\n|;
  $sHours->execute($ClientID);
  while (my $rHours = $sHours->fetchrow_hashref) 
  { 
    my $Duration = DBUtil->getDuration($rHours->{ContLogBegTime},$rHours->{ContLogEndTime});
    my $Hrs = ($Duration / 3600);
    $TotHrs += $Hrs;
#warn "$rHours->{TrID}, $rHours->{SCID}, $rHours->{SCNum}, $rHours->{SCName}, $rHours->{Type}, ContLogDate=$rHours->{ContLogDate}, TotHrs=$TotHrs\n";
    if ( $rHours->{Type} eq 'IC' ) { $Ind += $Hrs; }
    elsif ( $rHours->{Type} eq 'IR' ) { $IndRehab += $Hrs; }
    elsif ( $rHours->{Type} eq 'GC' ) { $Grp += $Hrs; }
    elsif ( $rHours->{Type} eq 'GR' ) { $GrpRehab += $Hrs; }
    elsif ( $rHours->{Type} eq 'FC' ) { $Fam += $Hrs; }
    elsif ( $rHours->{Type} eq 'TP' )
    {
      if ( $rHours->{SCName} =~ /Review/ ) { $TPReview += $Hrs; }
      elsif ( $rHours->{SCName} =~ /Assessment/ ) { $Assess += $Hrs; }
      else { $TPDevel += $Hrs; }
    }
    elsif ( $rHours->{SCNum} eq 'PARA' ) { $Para += $Hrs; }
    elsif ( $rHours->{SCName} =~ /Assessment/ ) { $Assess += $Hrs; }
    else { $Others += $Hrs; }
    if ( $rHours->{SCNum} eq 'XNOSHOW' )
    {
      $NSCnt++;
      $NoShows->{$NSCnt} = DBUtil->Date($rHours->{ContLogDate},'fmt','MM/DD/YYYY')
    }
  }
#warn "1.TotHrs=$TotHrs\n";
  my $FirstContDateAmr = DBUtil->Date(${FirstContDate},'fmt','MM/DD/YYYY');
  $Ind = sprintf("%.2f", $Ind);
  $IndRehab = sprintf("%.2f", $IndRehab);
  $Grp = sprintf("%.2f", $Grp);
  $GrpRehab = sprintf("%.2f", $GrpRehab);
  $Fam = sprintf("%.2f", $Fam);
  $TPDevel = sprintf("%.2f", $TPDevel);
  $TPReview = sprintf("%.2f", $TPReview);
  $Para = sprintf("%.2f", $Para);
  $Assess = sprintf("%.2f", $Assess);
  $Others = sprintf("%.2f", $Others);
  $TotHrs = sprintf("%.2f", $TotHrs);
#warn "2.TotHrs=$TotHrs\n";

  my $out = '';
  $out .= "/R10 14 Tf\n";
##
# 290 (width of page) / 2 (in half) * 5 (boldness&size of font)
  my $x = (290 - ((length($AgencyName) / 2) * 5));
  $out .= "1 0 0 1 " . $x . " 740 Tm ($AgencyName) Tj\n";
  $out .= "/R10 11 Tf\n";
  $x = (290 - ((length($AgencyAddr) / 2) * 4));
  $out .= "1 0 0 1 " . $x . " 730 Tm ($AgencyAddr) Tj\n";
  $x = (290 - ((length($AgencyPh) / 2) * 4));
  $out .= "1 0 0 1 " . $x . " 720 Tm ($AgencyPh) Tj\n";
  $out .= "/R5 12 Tf\n";
  $Title = qq|${MonthName} ${hdr}|;
  $x = (290 - ((length($Title) / 2) * 6));
  $out .= "1 0 0 1 " . $x . " 700 Tm ($Title) Tj\n";
  $out .= "/R10 11 Tf\n";
  $out .= "1 0 0 1 120 666 Tm ($rClient->{LName}) Tj\n";
  $out .= "1 0 0 1 325 666 Tm ($rClient->{FName}) Tj\n";
  my $MI = substr($rClient->{MName},0,1);
  $out .= "1 0 0 1 540 666 Tm (${MI}) Tj\n";
  my $JOLTS = $rClient->{JOLTS} ? $rClient->{JOLTS} : '*';
  $out .= "1 0 0 1 80 655 Tm ($JOLTS) Tj\n";
  $out .= "1 0 0 1 190 655 Tm ($Client_DOBAmr) Tj\n";
  $out .= "1 0 0 1 360 655 Tm (${FirstContDateAmr}) Tj\n";
  $out .= "1 0 0 1 120 644 Tm ($rClientLegalPP->{'Name'}) Tj\n";
  $out .= "1 0 0 1 325 644 Tm (${ProvName}) Tj\n";

  $out .= "1 0 0 1 170 588 Tm (${Ind}) Tj\n";
  $out .= "1 0 0 1 170 575 Tm (${IndRehab}) Tj\n";
  $out .= "1 0 0 1 170 563 Tm (${Assess}) Tj\n";
  $out .= "1 0 0 1 170 550 Tm (${TotHrs}) Tj\n";
  $out .= "1 0 0 1 355 588 Tm (${Grp}) Tj\n";
  $out .= "1 0 0 1 355 575 Tm (${GrpRehab}) Tj\n";
  $out .= "1 0 0 1 355 563 Tm (${TPDevel}) Tj\n";
  $out .= "1 0 0 1 530 588 Tm (${Fam}) Tj\n";
  $out .= "1 0 0 1 530 575 Tm (${Para}) Tj\n";
  $out .= "1 0 0 1 530 563 Tm (${TPReview}) Tj\n";
  $out .= "1 0 0 1 530 551 Tm (${Others}) Tj\n";

  $out .= "1 0 0 1 80 510 Tm ($NoShows->{1}) Tj\n";
  $out .= "1 0 0 1 210 510 Tm ($NoShows->{2}) Tj\n";
  $out .= "1 0 0 1 350 510 Tm ($NoShows->{3}) Tj\n";
  $out .= "1 0 0 1 490 510 Tm ($NoShows->{4}) Tj\n";
  $out .= "1 0 0 1 80 497 Tm ($NoShows->{5}) Tj\n";
  $out .= "1 0 0 1 210 497 Tm ($NoShows->{6}) Tj\n";
  $out .= "1 0 0 1 350 497 Tm ($NoShows->{7}) Tj\n";
  $out .= "1 0 0 1 490 497 Tm ($NoShows->{8}) Tj\n";

  $sClientCARSReview->execute($rClient->{ClientID}) || myDBI->dberror("select ClientCARSReview");
  my $rClientCARSReview = $sClientCARSReview->fetchrow_hashref;
  my $fontsize = main->sizefont($rClientCARSReview->{ProgEvidence},190);
  $out .= "/R10 ${fontsize} Tf\n";
  $out .= $pdf->flowText(42, 419, 529, 190, $rClientCARSReview->{ProgEvidence}, $fontsize);
  $fontsize = main->sizefont($rClientCARSReview->{Issues},100);
  $out .= "/R10 ${fontsize} Tf\n";
  $out .= $pdf->flowText(42, 189, 529, 100, $rClientCARSReview->{Issues}, $fontsize);

  $out .= "1 0 0 1 30 55 Tm ($RefAgency) Tj\n";
#  $out .= "ET\n";
#foreach my $f ( sort keys %{$rClient} ) { warn ": rClient-$f=$rClient->{$f}\n"; }

# add a page 'deflate' or not ''.
  $pdf->add('deflate', $out);
  return(1);
}
sub sizefont
{
  my ($self,$str,$boxheight) = @_;
  my $l=length($str);
  my $m11 = 950 * ($boxheight/100);
  my $m10 = 1160 * ($boxheight/100);
  my $m9 = 1420 * ($boxheight/100);
  my $m8 = 1730 * ($boxheight/100);
  my $m7 = 2320 * ($boxheight/100);
  my $m6 = 3100 * ($boxheight/100);
  my $m5 = 4660 * ($boxheight/100);
  if ( $l <= $m11 ) { return(11); }
  elsif ( $l <= $m10 ) { return(10); }
  elsif ( $l <= $m9 ) { return(9); }
  elsif ( $l <= $m8 ) { return(8); }
  elsif ( $l <= $m7 ) { return(7); }
  elsif ( $l <= $m6 ) { return(6); }
  elsif ( $l <= $m5 ) { return(6); }
  return(4);
}
############################################################################
