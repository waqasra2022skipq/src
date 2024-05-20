#!/usr/bin/perl
#############################################################################
use lib '/home/okmis/mis/src/lib';
use DBI;
use myForm;
use DBA;
use SysAccess;
use DBUtil;
use utils;
use graphs;
use Time::Local;
use DateTime
my $DT=localtime();
my $multidel = chr(253);

#############################################################################
my $form = myForm->parse();
my $method = $form->{'method'};
my $value = $form->{'value'};
my $target = $form->{'target'};
my $newDates = $form->{'FromDate'} ne '' ? 1 : 0;    # if given a From/To Date then reset daterange.
#warn qq|ENTER: graphs.pl: method=${method} value=${value} target=${target}\n|;
#foreach my $f ( sort keys %{$form} ) { warn "ENTER: graphs.pl: form-$f=$form->{$f}\n"; }
  my $newform = ();
  foreach my $f ( sort keys %{$form} ) { $newform->{$f}=$form->{$f}; }
$form = utils->readsid($form);
# use method from saved sesid, unless input/given to us to change
$method = $form->{'method'} if ( $method eq '' );
if ( $value eq 'reset' )
{
  $form->{'daterange'} = '' if ( $newDates );
#warn "begin: value eq 'reset'\n";
  foreach my $f ( sort keys %{$newform} )
  {
#warn "loop: form-$f=$form->{$f},$newform->{$f}\n";
    next if ( $f eq 'method' );
    next if ( $f eq 'value' );
    next if ( $f eq 'target' );
#warn "set: BEFORE: form-$f=$form->{$f},$newform->{$f}\n";
    $form->{$f} = $newform->{$f};
#warn "set: AFTER: form-$f=$form->{$f},$newform->{$f}\n";
  }
  $form->{'method'} = $method;      # save new method input?
  $form = utils->writesid($form,$form->{'sesid'})
}
#foreach my $f ( sort keys %{$form} ) { warn "AFTER: graphs.pl: form-$f=$form->{$f}\n"; }
$form = DBUtil->setDates($form);

# Static global variables...
my $chartname = 'bar_chart';
my $ChartStyle = qq||;
my ($xLabel,$xFormat) = ('Clinics',',.d0');
my ($yLabel,$yFormat) = ('Population',',.d0');
my ($HEIGHT,$WIDTH) = (500,1000);
my $fdow = DBUtil->Date($form->{FromDate},'dow');
my $fdayname = (Sunday,Monday,Tuesday,Wednesday,Thursday,Friday,Saturday)[$fdow];
my $tdow = DBUtil->Date($form->{ToDate},'dow');
my $tdayname = (Sunday,Monday,Tuesday,Wednesday,Thursday,Friday,Saturday)[$tdow];
my $DateRange = qq|from ${fdayname} $form->{FromDateD} - ${tdayname} $form->{ToDateD}|;
my $addSelection = DBA->withClinicProvider($form,'and','Client.clinicClinicID','Treatment.ProvID');
my $ReportHeader = DBA->withSelectionHeader($form);
my $TITLE = $ReportHeader;
my $SUBTITLE = qq|Notes for ServiceDate from ${fdayname} $form->{FromDateD} - ${tdayname} $form->{ToDateD}|;
my $dbh = myDBI->dbconnect($form->{'DBNAME'});
if ( $form->{LOGINPROVID} == 91 )
{
  open OUT, ">/home/okmis/mis/src/debug/graphs.out" or die "Couldn't open file: $!";
  foreach my $f ( sort keys %{$form} ) { print OUT "graphs.cgi: form-$f=$form->{$f}\n"; }
  print OUT "addSelection: ${addSelection}\n";
  close(OUT);
}
############################################################################
my ($err,$iwarn,$msg,$out,$xml) = ('','','','','');

#foreach my $f ( sort keys %{$form} ) { warn "graphs: form-$f=$form->{$f}\n"; }
if ( $method eq 'reset' )       # NOT USED
{
  my $html = qq|
<SCRIPT TYPE="text/javascript" >
alert("this is the NEW test");
</SCRIPT>
|;
  my $ex = qq|javascript:execute_script('grapharea');|;
#warn qq|graphs.pl: html=\n${html}\n|;
  $out = $err eq '' ? qq|
  <command method="setcontent">
    <target>grapharea</target>
    <content><![CDATA[${html}]]></content>
  </command>
  <command method="setscript">
    <target>executeit</target>
    <content><![CDATA[${ex}]]></content>
  </command>
| : main->ierr($target,$err,,$msg,$id);
  $out .= main->iwarn($warn,$msg,$id);
}
else
{
  my $id = '';              # SPAN msg
  my $data = main->$method($form,$addSelection);
  my $parms = ();
  $parms->{'function'} = $chartname;
  $parms->{'style'} = $ChartStyle;
  $parms->{'title'} = $TITLE;
  $parms->{'subtitle'} = $SUBTITLE;
  $parms->{'xformat'} = $xFormat;
  $parms->{'xlabel'} = $xLabel;
  $parms->{'yformat'} = $yFormat;
  $parms->{'ylabel'} = $yLabel;
  $parms->{'height'} = $HEIGHT;
  $parms->{'width'} = $WIDTH;
#print qq|parms: are...\n|;
#foreach my $f ( keys %{$parms} ) { print ": parms-$f=$parms->{$f}\n"; }
  my $grapharea = graphs->d3_chart($parms,$data);

  my $ex = qq|javascript:execute_script('grapharea');|;
  my $optionsarea = qq|<P STYPE="color: red;" >LOOKS GOOD</P>|;
  $out = $err eq '' ? qq|
  <command method="setcontent">
    <target>grapharea</target>
    <content><![CDATA[${grapharea}]]></content>
  </command>
  <command method="setscript">
    <target>executeit</target>
    <content><![CDATA[${ex}]]></content>
  </command>
  <command method="setcontent">
    <target>optionsarea</target>
    <content><![CDATA[${optionsarea}]]></content>
  </command>
| : main->ierr($target,$err,,$msg,$id);
  $out .= main->iwarn($warn,$msg,$id);
}
$xml = qq|<response>\n${out}</response>|;
myDBI->cleanup();
#warn qq|graphs: xml=${xml}\n|;
print qq|Content-type: text/xml

<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
${xml}
|;
exit;
############################################################################
sub AmtDueByClient
{
  my ($self,$form,$addsel) = @_;
  my $ForProvID = $form->{ForProvID} ? $form->{ForProvID} : $form->{LOGINPROVID};
  $chartname = 'bar_chart';
  $xLabel = 'Amount Due By Client';
  $yLabel = 'Dollars'; $yFormat = ',.0f';
  $TITLE = qq|${ReportHeader} Amount Due by Client|;
  my $s = qq|
select 'Amount Due' as MyKey, CONCAT(Client.LName,', ',Client.FName,' ',Client.ClientID) as MyX, SUM(Treatment.AmtDue) as MyY
 from Treatment
  left join Client on Client.ClientID=Treatment.ClientID
  left join Provider on Provider.ProvID=Treatment.ProvID
  left join ClientACL on ClientACL.ClientID=Client.ClientID
  left join xSC on xSC.SCID=Treatment.SCID
  left join xInsurance on xInsurance.ID=xSC.InsID
 where Treatment.ContLogDate>="$form->{FromDate}" and Treatment.ContLogDate<="$form->{ToDate}"
   and | . DBA->withNoteAccess($form,$ForProvID,'Treatment') . $addsel . qq|
 group by MyKey, MyX
 order by MyY desc
 limit 10|;
#warn qq|graphs.pl: select=${s}\n|;
  my $dataset = ();
  ($cnt,$dataset) = graphs->selData($form,$s,$dataset,'MyY',$chartname);
  my $data = graphs->setData($dataset);
  return($data);
}
sub AmtDueByProvider
{
  my ($self,$form,$addsel) = @_;
  my $ForProvID = $form->{ForProvID} ? $form->{ForProvID} : $form->{LOGINPROVID};
  $chartname = 'bar_chart';
  $xLabel = 'Amount Due By Provider';
  $yLabel = 'Dollars'; $yFormat = ',.0f';
  $TITLE = qq|${ReportHeader} Amount Due by Provider|;
  my $s = qq|
select 'Amount Due' as MyKey, CONCAT(Provider.LName,', ',Provider.FName,' ',Provider.ProvID) as MyX, SUM(Treatment.AmtDue) as MyY
 from Treatment
  left join Provider on Provider.ProvID=Treatment.ProvID
  left join Client on Client.ClientID=Treatment.ClientID
  left join ClientACL on ClientACL.ClientID=Client.ClientID
  left join xSC on xSC.SCID=Treatment.SCID
  left join xInsurance on xInsurance.ID=xSC.InsID
 where Treatment.ContLogDate>="$form->{FromDate}" and Treatment.ContLogDate<="$form->{ToDate}"
   and | . DBA->withNoteAccess($form,$ForProvID,'Treatment') . $addsel . qq|
 group by MyKey, MyX
 order by MyY desc
 limit 10|;
#warn qq|graphs.pl: select=${s}\n|;
  my $dataset = ();
  ($cnt,$dataset) = graphs->selData($form,$s,$dataset,'MyY',$chartname);
  my $data = graphs->setData($dataset);
  return($data);
}
sub BilledvsIncome
{
  my ($self,$form,$addsel) = @_;
  my $ForProvID = $form->{ForProvID} ? $form->{ForProvID} : $form->{LOGINPROVID};
  $chartname = 'bar_chart';
  $xLabel = 'Billed vs Income';
  $yLabel = 'Dollars'; $yFormat = ',.0f';
  $TITLE = qq|${ReportHeader} Billed vs Income by Month|;
  my $s = qq|
select 'Amt' as MyKey, DATE_FORMAT(Treatment.ContLogDate,'%Y-%m') as MyX, SUM(Treatment.BilledAmt) as MyY1
, SUM(Treatment.IncAmt) as MyY2
 from Client
  left join ClientACL on ClientACL.ClientID=Client.ClientID
  left join Treatment on Treatment.ClientID=Client.ClientID
  left join Provider as Clinic on Clinic.ProvID=Client.clinicClinicID
  left join xSC on xSC.SCID=Treatment.SCID
  left join xInsurance on xInsurance.ID=xSC.InsID
 where Treatment.ContLogDate>="$form->{FromDate}" and Treatment.ContLogDate<="$form->{ToDate}"
   and | . DBA->withNoteAccess($form,$ForProvID,'Treatment') . $addsel . qq|
 group by MyKey, MyX |;
#warn qq|graphs.pl: select=${s}\n|;
  my $dataset = ();
  ($cnt,$dataset) = graphs->selData($form,$s,$dataset,'MyY1|BillAmt:MyY2|IncAmt',$chartname);
  my $data = graphs->setData($dataset);
  return($data);
}
sub BilledByStatus
{
  my ($self,$form,$addsel) = @_;
  my $ForProvID = $form->{ForProvID} ? $form->{ForProvID} : $form->{LOGINPROVID};
  $chartname = 'stackedbar_chart';
  $xLabel = 'Billed';
  $yLabel = 'Dollars'; $yFormat = ',.0f';
  $TITLE = qq|${ReportHeader} Billed by Status|;
  my $s = qq|
select xBillStatus.Descr as MyKey, DATE_FORMAT(Treatment.ContLogDate,'%Y-%m') as MyX, SUM(Treatment.BilledAmt) as MyY
 from Client
  left join ClientACL on ClientACL.ClientID=Client.ClientID
  left join Treatment on Treatment.ClientID=Client.ClientID
  left join xBillStatus on xBillStatus.ID=Treatment.BillStatus
  left join Provider as Clinic on Clinic.ProvID=Client.clinicClinicID
  left join xSC on xSC.SCID=Treatment.SCID
  left join xInsurance on xInsurance.ID=xSC.InsID
 where Treatment.ContLogDate>="$form->{FromDate}" and Treatment.ContLogDate<="$form->{ToDate}"
   and | . DBA->withNoteAccess($form,$ForProvID,'Treatment') . $addsel . qq|
 group by MyKey, MyX |;
  my $dataset = ();
  ($cnt,$dataset) = graphs->selData($form,$s,$dataset,'MyY',$chartname);
  my $data = graphs->setData($dataset);
  return($data);
}
sub StuckInProcess
{
  my ($self,$form,$addsel) = @_;
  my $ForProvID = $form->{ForProvID} ? $form->{ForProvID} : $form->{LOGINPROVID};
  $chartname = 'stackedbar_chart';
  $xLabel = 'Billed';
  $yLabel = 'Dollars'; $yFormat = ',.0f';
  $TITLE = qq|${ReportHeader} Stuck In Process 6 weeks or more|;
  my $s = qq|
select xBillStatus.Descr as MyKey, DATE_FORMAT(Treatment.ContLogDate,'%Y-%m') as MyX, SUM(Treatment.BilledAmt) as MyY
 from Client
  left join ClientACL on ClientACL.ClientID=Client.ClientID
  left join Treatment on Treatment.ClientID=Client.ClientID
  left join xBillStatus on xBillStatus.ID=Treatment.BillStatus
  left join Provider as Clinic on Clinic.ProvID=Client.clinicClinicID
  left join xSC on xSC.SCID=Treatment.SCID
  left join xInsurance on xInsurance.ID=xSC.InsID
 where Treatment.ContLogDate>="$form->{FromDate}" and Treatment.ContLogDate<="$form->{ToDate}"
   and (Treatment.BillStatus!=4 and Treatment.BillStatus!=5)
   and DATEDIFF(CURDATE(),Treatment.BillDate) > 42
   and | . DBA->withNoteAccess($form,$ForProvID,'Treatment') . $addsel . qq|
 group by MyKey, MyX |;
  my $dataset = ();
  ($cnt,$dataset) = graphs->selData($form,$s,$dataset,'MyY',$chartname);
  my $data = graphs->setData($dataset);
  return($data);
}
sub ClinicsByGender
{
  my ($self,$form,$addsel) = @_;
  my $ForProvID = $form->{ForProvID} ? $form->{ForProvID} : $form->{LOGINPROVID};
  $chartname = 'stackedbar_chart';
  $xLabel = 'Clinics';
  $yLabel = 'Population';
  $TITLE = qq|${ReportHeader} Clinics by Gender|;
  my $s = qq|
select REPLACE(REPLACE(Client.Gend,'M','Male'),'F','Female') as MyKey, Clinic.Name as MyX, count(DISTINCT Client.ClientID) as MyY
 from Client
  left join ClientACL on ClientACL.ClientID=Client.ClientID
  left join Treatment on Treatment.ClientID=Client.ClientID
  left join Provider as Clinic on Clinic.ProvID=Client.clinicClinicID
  left join xSC on xSC.SCID=Treatment.SCID
  left join xInsurance on xInsurance.ID=xSC.InsID
 where Treatment.ContLogDate>="$form->{FromDate}" and Treatment.ContLogDate<="$form->{ToDate}"
   and | . DBA->withNoteAccess($form,$ForProvID,'Treatment') . $addsel . qq|
 group by MyKey, MyX |;
  my $dataset = ();
  ($cnt,$dataset) = graphs->selData($form,$s,$dataset,'MyY',$chartname);
  my $data = graphs->setData($dataset);
  return($data);
}
sub SCClient
{
  my ($self,$form,$addsel) = @_;
  my $ForProvID = $form->{ForProvID} ? $form->{ForProvID} : $form->{LOGINPROVID};
  $chartname = 'stackedbar_chart';
  $xLabel = 'Clients';
  $yLabel = 'Count';
  $HEIGHT = 800;
  $WIDTH = 1000;
  $TITLE = qq|${ReportHeader} Service Codes by Client Population|;
  my $s = qq|
##select 'Service Code' as MyKey, CONCAT(Client.LName,', ',Client.FName,' ',Client.ClientID,' ',xSC.SCNum) as MyX, COUNT(xSC.SCNum) as MyY
select xSC.SCNum as MyKey, CONCAT(Client.LName,', ',Client.FName,' ',Client.ClientID) as MyX, COUNT(Treatment.TrID) as MyY
 from Client
  left join ClientACL on ClientACL.ClientID=Client.ClientID
  left join Treatment on Treatment.ClientID=Client.ClientID
  left join Provider as Clinic on Clinic.ProvID=Client.clinicClinicID
  left join xSC on xSC.SCID=Treatment.SCID
  left join xInsurance on xInsurance.ID=xSC.InsID
 where Treatment.ContLogDate>="$form->{FromDate}" and Treatment.ContLogDate<="$form->{ToDate}"
   and | . DBA->withNoteAccess($form,$ForProvID,'Treatment') . $addsel . qq|
 group by MyKey, MyX |;
  my $dataset = ();
  ($cnt,$dataset) = graphs->selData($form,$s,$dataset,'MyY',$chartname);
  $WIDTH = $cnt * 15 if ( $cnt > 65 );      # widen the graph is many elements.
  my $data = graphs->setData($dataset);
  return($data);
}
sub SCNote
{
  my ($self,$form,$addsel) = @_;
  my $ForProvID = $form->{ForProvID} ? $form->{ForProvID} : $form->{LOGINPROVID};
  $chartname = 'stackedbar_chart';
  $xLabel = 'Service Codes';
  $yLabel = 'Count';
  $HEIGHT = 1000;
  $WIDTH = 3000;
  $TITLE = qq|${ReportHeader} Service Codes by Note Count|;
  my $s = qq|
select xSC.SCNum as MyKey, DATE_FORMAT(Treatment.ContLogDate,'%Y-%m') as MyX, COUNT(Treatment.TrID) as MyY
 from Client
  left join ClientACL on ClientACL.ClientID=Client.ClientID
  left join Treatment on Treatment.ClientID=Client.ClientID
  left join Provider as Clinic on Clinic.ProvID=Client.clinicClinicID
  left join xSC on xSC.SCID=Treatment.SCID
  left join xInsurance on xInsurance.ID=xSC.InsID
 where Treatment.ContLogDate>="$form->{FromDate}" and Treatment.ContLogDate<="$form->{ToDate}"
   and | . DBA->withNoteAccess($form,$ForProvID,'Treatment') . $addsel . qq|
 group by MyKey, MyX |;
  my $dataset = ();
  ($cnt,$dataset) = graphs->selData($form,$s,$dataset,'MyY',$chartname);
  my $data = graphs->setData($dataset);
  return($data);
}
sub SCUnit
{
  my ($self,$form,$addsel) = @_;
  my $ForProvID = $form->{ForProvID} ? $form->{ForProvID} : $form->{LOGINPROVID};
  $chartname = 'stackedbar_chart';
  $xLabel = 'Service Codes';
  $yLabel = 'Count';
  $HEIGHT = 1000;
  $WIDTH = 1000;
  $TITLE = qq|${ReportHeader} Service Codes by Unit Summary|;
  my $s = qq|
select xSC.SCNum as MyKey, DATE_FORMAT(Treatment.ContLogDate,'%Y-%m') as MyX, SUM(Treatment.Units) as MyY
 from Client
  left join ClientACL on ClientACL.ClientID=Client.ClientID
  left join Treatment on Treatment.ClientID=Client.ClientID
  left join Provider as Clinic on Clinic.ProvID=Client.clinicClinicID
  left join xSC on xSC.SCID=Treatment.SCID
  left join xInsurance on xInsurance.ID=xSC.InsID
 where Treatment.ContLogDate>="$form->{FromDate}" and Treatment.ContLogDate<="$form->{ToDate}"
   and | . DBA->withNoteAccess($form,$ForProvID,'Treatment') . $addsel . qq|
 group by MyKey, MyX |;
  my $dataset = ();
  ($cnt,$dataset) = graphs->selData($form,$s,$dataset,'MyY',$chartname);
  my $data = graphs->setData($dataset);
  return($data);
}
sub ClinicsByClient
{
  my ($self,$form,$addsel) = @_;
  my $ForProvID = $form->{ForProvID} ? $form->{ForProvID} : $form->{LOGINPROVID};
  $chartname = 'stackedbar_chart';
  $xLabel = 'Clinics';
  $yLabel = 'Population';
  $TITLE = qq|${ReportHeader} Clinics by Client Population|;
  my $s = qq|
select Clinic.Name as MyKey, DATE_FORMAT(Treatment.ContLogDate,'%Y-%m') as MyX, COUNT(DISTINCT Client.ClientID) as MyY
 from Client
  left join ClientACL on ClientACL.ClientID=Client.ClientID
  left join Treatment on Treatment.ClientID=Client.ClientID
  left join Provider as Clinic on Clinic.ProvID=Client.clinicClinicID
  left join xSC on xSC.SCID=Treatment.SCID
  left join xInsurance on xInsurance.ID=xSC.InsID
 where Treatment.ContLogDate>="$form->{FromDate}" and Treatment.ContLogDate<="$form->{ToDate}"
   and | . DBA->withNoteAccess($form,$ForProvID,'Treatment') . $addsel . qq|
 group by MyKey, MyX |;
  my $dataset = ();
  ($cnt,$dataset) = graphs->selData($form,$s,$dataset,'MyY',$chartname);
  my $data = graphs->setData($dataset);
  return($data);
}
sub ClinicsByActiveClient
{
  my ($self,$form,$addsel) = @_;
  my $ForProvID = $form->{ForProvID} ? $form->{ForProvID} : $form->{LOGINPROVID};
  $chartname = 'stackedbar_chart';
  $xLabel = 'Clinics';
  $yLabel = 'Count';
  $TITLE = qq|${ReportHeader} Clinics by Active Client|;
  $ClinicSelection = DBA->getClinicSelection($form,$ForProvID,'Client.clinicClinicID','where');
  $ClinicSelection .= qq| and Client.Active=1| if ( $form->{Active} );
  my $s = qq|
select Provider.Name as MyKey, DATE_FORMAT(ClientReferrals.RefDate,'%Y-%m') as MyX, COUNT(DISTINCT Client.ClientID) as MyY
 from Client
  left join ClientACL on ClientACL.ClientID=Client.ClientID
  left join ClientIntake on ClientIntake.ClientID=Client.ClientID
  left join ClientLegal on ClientLegal.ClientID=Client.ClientID
  left join ClientReferrals on ClientReferrals.ClientID=Client.ClientID
  left join ClientRelations on ClientRelations.ClientID=Client.ClientID
  left join Provider on Provider.ProvID=Client.clinicClinicID
  left join ClientSocial on ClientSocial.ClientID=Client.ClientID
  ${ClinicSelection}
  and ClientReferrals.RefDate>="$form->{FromDate}" and ClientReferrals.RefDate<="$form->{ToDate}"
   and | . DBA->withNoteAccess($form,$ForProvID,'Treatment') . $addsel . qq|
 group by MyKey, MyX |;
  my $dataset = ();
  ($cnt,$dataset) = graphs->selData($form,$s,$dataset,'MyY',$chartname);
  my $data = graphs->setData($dataset);
  return($data);
}
sub ClinicsByAdmission
{
  my ($self,$form,$addsel) = @_;
  my $ForProvID = $form->{ForProvID} ? $form->{ForProvID} : $form->{LOGINPROVID};
  $chartname = 'stackedbar_chart';
  $xLabel = 'Clinics';
  $yLabel = 'Count';
  $TITLE = qq|${ReportHeader} Clinics by Admission|;
  $ClinicSelection = DBA->getClinicSelection($form,$ForProvID,'Client.clinicClinicID');
  my $s = qq|
select Clinic.Name as MyKey, DATE_FORMAT(ClientAdmit.AdmitDate,'%Y-%m') as MyX, COUNT(DISTINCT Client.ClientID) as MyY
from Client
  left join ClientACL on ClientACL.ClientID=Client.ClientID
  left join Provider as Clinic on Clinic.ProvID=Client.clinicClinicID
  left join Provider as Counselor on Counselor.ProvID=Client.ProvID
  left join ClientIntake on ClientIntake.ClientID=Client.ClientID
  left join ClientReferrals on ClientReferrals.ClientID=Client.ClientID
  left join ClientAdmit on ClientAdmit.ClientID=Client.ClientID
  left join ClientSocial on ClientSocial.ClientID=Client.ClientID
  left join okmis_config.xReligiousAffiliation on xReligiousAffiliation.ID=ClientSocial.ReligionName
  left join okmis_config.xLanguages on xLanguages.ID=ClientSocial.PreLang
  where Client.Active=1
    and ((ClientReferrals.RefDate >= '$form->{FromDate}' and ClientReferrals.RefDate <= '$form->{ToDate}')
    and (ClientAdmit.AdmitDate >= '$form->{FromDate}' and ClientAdmit.AdmitDate <= '$form->{ToDate}'))
  ${ClinicSelection}
 group by MyKey, MyX |;
  my $dataset = ();
  ($cnt,$dataset) = graphs->selData($form,$s,$dataset,'MyY',$chartname);
  my $data = graphs->setData($dataset);
  return($data);
}
sub ClinicsByDischargedClient
{
  my ($self,$form,$addsel) = @_;
  my $ForProvID = $form->{ForProvID} ? $form->{ForProvID} : $form->{LOGINPROVID};
  $chartname = 'stackedbar_chart';
  $xLabel = 'Clinics';
  $yLabel = 'Count';
  $TITLE = qq|${ReportHeader} Clinics by Discharged Clients|;
  $ClinicSelection = DBA->getClinicSelection($form,$ForProvID,'Client.clinicClinicID','where');
  $ClinicSelection .= qq| and Client.Active=1| if ( $form->{Active} );
  my $s = qq|
  select Clinic.Name as MyKey, DATE_FORMAT(ClientDischargeCDC.TransDate,'%Y-%m') as MyX, COUNT(DISTINCT Client.ClientID) as MyY
  from ClientDischarge
  left join Client on Client.ClientID=ClientDischarge.ClientID
  left join ClientACL on ClientACL.ClientID=Client.ClientID
  left join ClientDischargeCDC on ClientDischargeCDC.ClientDischargeID=ClientDischarge.ID
  left join ClientIntake on ClientIntake.ClientID=ClientDischarge.ClientID
  left join ClientReferrals on ClientReferrals.ClientID=ClientDischarge.ClientID
  left join Provider on Provider.ProvID=Client.ProvID
  left join Provider as Clinic on Clinic.ProvID=Client.clinicClinicID
  left join okmis_config.xNPI on xNPI.NPI=ClientReferrals.ReferredBy1NPI
  left join okmis_config.xCDCTransTypes on xCDCTransTypes.ID=ClientDischargeCDC.TransType
  ${ClinicSelection}
  and ClientDischargeCDC.TransDate>="$form->{FromDate}" and ClientDischargeCDC.TransDate<="$form->{ToDate}"
   and | . DBA->withNoteAccess($form,$ForProvID,'Treatment') . $addsel . qq|
 group by MyKey, MyX |;
  my $dataset = ();
  ($cnt,$dataset) = graphs->selData($form,$s,$dataset,'MyY',$chartname);
  my $data = graphs->setData($dataset);
  return($data);
}
sub ClinicsByRace
{
  my ($self,$form,$addsel) = @_;
  my $ForProvID = $form->{ForProvID} ? $form->{ForProvID} : $form->{LOGINPROVID};
  $chartname = 'stackedbar_chart';
  $xLabel = 'Clinics';
  $yLabel = 'Population';
  $TITLE = qq|${ReportHeader} Clinics by Race Population|;
  my $s = qq|
select xRaces.Descr as MyKey, Clinic.Name as MyX, COUNT(DISTINCT Client.ClientID) as MyY
 from Client
  left join ClientACL on ClientACL.ClientID=Client.ClientID
  left join okmis_config.xRaces on xRaces.ID=SUBSTRING_INDEX(Client.Race,'${multidel}',1)
  left join Provider as Clinic on Clinic.ProvID=Client.clinicClinicID
  left join Treatment on Treatment.ClientID=Client.ClientID
  left join xSC on xSC.SCID=Treatment.SCID
  left join xInsurance on xInsurance.ID=xSC.InsID
 where Treatment.ContLogDate>="$form->{FromDate}" and Treatment.ContLogDate<="$form->{ToDate}"
   and | . DBA->withNoteAccess($form,$ForProvID,'Treatment') . $addsel . qq|
 group by MyKey, MyX |;
  my $dataset = ();
  ($cnt,$dataset) = graphs->selData($form,$s,$dataset,'MyY',$chartname);
  my $data = graphs->setData($dataset);
  return($data);
}
sub ClinicsByEthnicity
{
  my ($self,$form,$addsel) = @_;
  my $ForProvID = $form->{ForProvID} ? $form->{ForProvID} : $form->{LOGINPROVID};
  $chartname = 'stackedbar_chart';
  $xLabel = 'Clinics';
  $yLabel = 'Population';
  $TITLE = qq|${ReportHeader} Clinics by Ethnicity Population|;
  my $s = qq|
select xEthnicity.Descr as MyKey, Clinic.Name as MyX, COUNT(DISTINCT Client.ClientID) as MyY
 from Client
  left join ClientACL on ClientACL.ClientID=Client.ClientID
  left join Provider as Clinic on Clinic.ProvID=Client.clinicClinicID
  left join Treatment on Treatment.ClientID=Client.ClientID
  left join xSC on xSC.SCID=Treatment.SCID
  left join xInsurance on xInsurance.ID=xSC.InsID
    left join ClientSocial on ClientSocial.ClientID=Treatment.ClientID
  left join okmis_config.xEthnicity on xEthnicity.ID=Client.Ethnicity
 where Treatment.ContLogDate>="$form->{FromDate}" and Treatment.ContLogDate<="$form->{ToDate}"
   and | . DBA->withNoteAccess($form,$ForProvID,'Treatment') . $addsel . qq|
 group by MyKey, MyX |;
  my $dataset = ();
  ($cnt,$dataset) = graphs->selData($form,$s,$dataset,'MyY',$chartname);
  my $data = graphs->setData($dataset);
  return($data);
}

sub BillingErrors
{
  my ($self,$form,$addsel) = @_;
  my $ForProvID = $form->{ForProvID} ? $form->{ForProvID} : $form->{LOGINPROVID};
  $chartname = 'stackedbar_chart';
  $xLabel = 'Client Name';
  $yLabel = 'Count of Fatal error';
  $TITLE = qq|${ReportHeader} Billing Errors - Unbillable Notes|;

    my $datetime = DateTime->now;
    $f_from = $datetime->ymd;


  $fdow = DBUtil->Date($f_from,'dow');
  my $fdayname = (Sunday,Monday,Tuesday,Wednesday,Thursday,Friday,Saturday)[$fdow];
  my $tdow = DBUtil->Date($f_to,'dow');
  $SUBTITLE = qq| Unbillable Notes visualization uptill ${fdayname} $f_from|;


  my $s = qq|
  select Count(DISTINCT Treatment.TrID) as MyY
      ,CONCAT(Client.FName,', ' ,Client.LName) as MyX, xInsurance.Name as MyKey
  from Treatment
    left join Provider as Clinic on Clinic.ProvID=Treatment.ClinicID
    left join Client on Client.ClientID=Treatment.ClientID
    left join xSC on xSC.SCID=Treatment.SCID
    left join xInsurance on xInsurance.ID=xSC.InsID
  where Treatment.BillStatus<3 and Treatment.MgrRevDate is not null and Treatment.BillDate is not null
  GROUP by MyX, MyKey |;
  my $dataset = ();
  ($cnt,$dataset) = graphs->selData($form,$s,$dataset,'MyY',$chartname);
  my $data = graphs->setData($dataset);
  return($data);
}

sub ClientsConflictUnbilledWeek
{
  my ($self,$form,$addsel) = @_;
  my $ForProvID = $form->{ForProvID} ? $form->{ForProvID} : $form->{LOGINPROVID};
  $chartname = 'stackedbar_chart';
  $xLabel = 'Providers Name';
  $yLabel = 'Counts of TrID';
  $TITLE = qq|${ReportHeader}  Note conflict- Client Unbillable (This week)|;

 my $daysRem = 7;

    $fromDate = $form->{'FromDate'};
    ($yyyy, $mm, $dd) = ($fromDate =~ /(\d+)-(\d+)-(\d+)/); 
    
    $fromDate = DateTime->new(  
          day        => $dd,  
          month      => $mm,  
          year       => $yyyy,  
          hour       => 23,
      );  
      
    $ToDate = $form->{'ToDate'};
    ($yyyy, $mm, $dd) = ($ToDate =~ /(\d+)-(\d+)-(\d+)/); 
    
    $ToDate = DateTime->new(  
          day        => $dd,  
          month      => $mm,  
          year       => $yyyy,  
          hour       => 23,
      );  

    my $datetime = DateTime->now;

    my $cmp = DateTime->compare($datetime, $fromDate);
    my $cmp2 = DateTime->compare($datetime, $ToDate);
    my $f_from = $datetime->ymd;;
    my $f_to = '';
    my $fdow = DBUtil->Date($f_from,'dow');
    my $Index = $fdow* (-1);
    if($cmp ==1 ){
      if($fdow > 0){
        $datetime = $datetime->add(days => $Index);
        $datetime = $datetime->add(days => 1);
      }
      $f_from = $datetime->ymd;
    }else{
      $f_from = $fromDate->ymd;
    }
    if($cmp2 ==1 ){
      $ToDate = $datetime->add(days => 6);
      $f_to = $ToDate->ymd;
    }else{
      $f_to = $ToDate->ymd;
    }

    $fdow = DBUtil->Date($f_from,'dow');
    my $fdayname = (Sunday,Monday,Tuesday,Wednesday,Thursday,Friday,Saturday)[$fdow];
    my $tdow = DBUtil->Date($f_to,'dow');
    my $tdayname = (Sunday,Monday,Tuesday,Wednesday,Thursday,Friday,Saturday)[$tdow];
    my $DateRange = qq|from ${fdayname} $f_from - ${tdayname} $f_to|;
    $SUBTITLE = qq| Note conflict- Client Unbillable (This week) ${fdayname} $f_from - ${tdayname} $f_to|;



  $ProviderSelection = DBA->getProviderSelection($form,$ForProvID,'Provider.ProvID','where');
  $ProviderSelection .= qq| and Provider.Active=1| if ( $form->{Active} );
  my $s = qq|
     select CONCAT(Client.LName,', ' ,Client.FName) as MyKey, Count(DISTINCT T2.TrID) as MyY
     , DATE_FORMAT(T2.ContLogDate,'%Y-%m') as MyX, T2.ContLogBegTime, T2.ContLogEndTime, T2.ClientID
     , xSC.Type as SCType, xSC.SCNum
  from Treatment T1
    join Treatment T2 on T2.TrID != T1.TrID and T2.ClientID = T1.ClientID and T2.ContLogDate = T1.ContLogDate and (( T2.ContLogBegTime >= T1.ContLogBegTime and T2.ContLogBegTime <= T1.ContLogEndTime) or (T2.ContLogEndTime >= T1.ContLogBegTime and T2.ContLogEndTime <= T1.ContLogEndTime))
    left join Provider on Provider.ProvID=T1.ProvID
    left join Client on Client.ClientID=T1.ClientID
    left join xSC on xSC.SCID=T1.SCID
    ${ProviderSelection}
    and T2.ContLogDate>="${f_from}" and T2.ContLogDate<="${f_to}"
    and T2.ContLogDate is not null and T2.ContLogBegTime is not null 
    and T2.ContLogEndTime is not null
    GROUP by MyKey, MyX|;
  my $dataset = ();
  ($cnt,$dataset) = graphs->selData($form,$s,$dataset,'MyY',$chartname);
  my $data = graphs->setData($dataset);
  return($data);
}
sub ClientsConflictUnbilledAll
{
  my ($self,$form,$addsel) = @_;
  my $ForProvID = $form->{ForProvID} ? $form->{ForProvID} : $form->{LOGINPROVID};
  $chartname = 'stackedbar_chart';
  $xLabel = 'Date Timeline';
  $yLabel = 'TrID Count';
  $TITLE = qq|${ReportHeader} Note conflict- Client all (Everything)|;
  $ProviderSelection = DBA->getProviderSelection($form,$ForProvID,'Provider.ProvID','where');
  $ProviderSelection .= qq| and Provider.Active=1| if ( $form->{Active} );
  my $s = qq|
    select CONCAT(Client.LName,', ' ,Client.FName) as MyKey, Count(DISTINCT T2.TrID) as MyY
     , DATE_FORMAT(T2.ContLogDate,'%Y-%m') as MyX, T2.ContLogBegTime, T2.ContLogEndTime, T2.ClientID
     , xSC.Type as SCType, xSC.SCNum
  from Treatment T1
    join Treatment T2 on T2.TrID != T1.TrID and T2.ClientID = T1.ClientID and T2.ContLogDate = T1.ContLogDate and (( T2.ContLogBegTime >= T1.ContLogBegTime and T2.ContLogBegTime <= T1.ContLogEndTime) or (T2.ContLogEndTime >= T1.ContLogBegTime and T2.ContLogEndTime <= T1.ContLogEndTime))
    left join Provider on Provider.ProvID=T1.ProvID
    left join Client on Client.ClientID=T1.ClientID
    left join xSC on xSC.SCID=T1.SCID
    ${ProviderSelection}
    and T2.ContLogDate is not null and T2.ContLogBegTime is not null 
    and T2.ContLogEndTime is not null   
    and T2.ContLogDate>="$form->{FromDate}"
      and T2.ContLogDate<="$form->{ToDate}"
    GROUP by MyKey, MyX |;
  my $dataset = ();
 my $filename = 'zlog.txt';
  open(my $fh, '>', $filename) or die "Could not open file '$filename' $!";
  print $fh $s;
  close $fh;
  ($cnt,$dataset) = graphs->selData($form,$s,$dataset,'MyY',$chartname);
  my $data = graphs->setData($dataset);
  return($data);
}
sub ProvidersConflictUnbilledWeek
{
  my ($self,$form,$addsel) = @_;
  my $ForProvID = $form->{ForProvID} ? $form->{ForProvID} : $form->{LOGINPROVID};
  $chartname = 'stackedbar_chart';
  $xLabel = 'Clients Name';
  $yLabel = 'Counts of TrID';
  $TITLE = qq|${ReportHeader}  Note conflict- Provider Unbillable (This week)|;


 my $daysRem = 7;

    $fromDate = $form->{'FromDate'};
    ($yyyy, $mm, $dd) = ($fromDate =~ /(\d+)-(\d+)-(\d+)/); 
    
    $fromDate = DateTime->new(  
          day        => $dd,  
          month      => $mm,  
          year       => $yyyy,  
          hour       => 23,
      );  
      
    $ToDate = $form->{'ToDate'};
    ($yyyy, $mm, $dd) = ($ToDate =~ /(\d+)-(\d+)-(\d+)/); 
    
    $ToDate = DateTime->new(  
          day        => $dd,  
          month      => $mm,  
          year       => $yyyy,  
          hour       => 23,
      );  

    my $datetime = DateTime->now;

    my $cmp = DateTime->compare($datetime, $fromDate);
    my $cmp2 = DateTime->compare($datetime, $ToDate);
    my $f_from = $datetime->ymd;;
    my $f_to = '';
    my $fdow = DBUtil->Date($f_from,'dow');
    my $Index = $fdow* (-1);
    if($cmp ==1 ){
      if($fdow > 0){
        $datetime = $datetime->add(days => $Index);
        $datetime = $datetime->add(days => 1);
      }
      $f_from = $datetime->ymd;
    }else{
      $f_from = $fromDate->ymd;
    }
    if($cmp2 ==1 ){
      $ToDate = $datetime->add(days => 6);
      $f_to = $ToDate->ymd;
    }else{
      $f_to = $ToDate->ymd;
    }

    my $fdow = DBUtil->Date($f_from,'dow');
    my $fdayname = (Sunday,Monday,Tuesday,Wednesday,Thursday,Friday,Saturday)[$fdow];
    my $tdow = DBUtil->Date($f_to,'dow');
    my $tdayname = (Sunday,Monday,Tuesday,Wednesday,Thursday,Friday,Saturday)[$tdow];
    my $DateRange = qq|from ${fdayname} $f_from - ${tdayname} $f_to|;
    $SUBTITLE = qq| Note conflict- Provider Unbillable (This week) ${fdayname} $f_from - ${tdayname} $f_to|;



  $ProviderSelection = DBA->getProviderSelection($form,$ForProvID,'Provider.ProvID','where');
  $ProviderSelection .= qq| and Provider.Active=1| if ( $form->{Active} );
  my $s = qq|
    select CONCAT(Provider.LName,', ', Provider.FName) as MyKey, 
	DATE_FORMAT(T2.ContLogDate,'%Y-%m') as MyX, 
	COUNT(DISTINCT T2.TrID) as MyY, T2.ContLogBegTime, T2.ContLogEndTime, T2.ClientID
     , xSC.Type as SCType, xSC.SCNum
  from Treatment T1
   join Treatment T2 on T2.TrID != T1.TrID and T1.ProvID = T2.ProvID and T2.ContLogDate = T1.ContLogDate and (( T2.ContLogBegTime >= T1.ContLogBegTime and T2.ContLogBegTime <= T1.ContLogEndTime) or (T2.ContLogEndTime >= T1.ContLogBegTime and T2.ContLogEndTime <= T1.ContLogEndTime))
    left join Provider on Provider.ProvID=T1.ProvID
    left join Client on Client.ClientID=T1.ClientID
    left join xSC on xSC.SCID=T1.SCID
    ${ProviderSelection}
    and T2.ContLogDate>="${f_from}" and T2.ContLogDate<="${f_to}"
    and T2.ContLogDate is not null and T2.ContLogBegTime is not null 
    and T2.ContLogEndTime is not null
    GROUP by MyKey, MyX|;
  my $dataset = ();
 my $filename = 'zlog.txt';
  open(my $fh, '>', $filename) or die "Could not open file '$filename' $!";
  print $fh $s;
  close $fh;
  ($cnt,$dataset) = graphs->selData($form,$s,$dataset,'MyY',$chartname);
  my $data = graphs->setData($dataset);
  return($data);
}
sub ProvidersConflictUnbilledAll
{
  my ($self,$form,$addsel) = @_;
  my $ForProvID = $form->{ForProvID} ? $form->{ForProvID} : $form->{LOGINPROVID};
  $chartname = 'stackedbar_chart';
  $xLabel = 'Date Timeline';
  $yLabel = 'TrID Count';
  $TITLE = qq|${ReportHeader} Note conflict- Provider all (Everything)|;
  $ProviderSelection = DBA->getProviderSelection($form,$ForProvID,'Provider.ProvID','where');
  $ProviderSelection .= qq| and Provider.Active=1| if ( $form->{Active} );
  my $s = qq| 
select CONCAT(Provider.LName,', ', Provider.FName) as MyKey, 
	DATE_FORMAT(T2.ContLogDate,'%Y-%m') as MyX, 
	COUNT(DISTINCT T2.TrID) as MyY, T2.ContLogBegTime, T2.ContLogEndTime, T2.ClientID
     , xSC.Type as SCType, xSC.SCNum
  from Treatment T1
   join Treatment T2 on T2.TrID != T1.TrID and T1.ProvID = T2.ProvID and T2.ContLogDate = T1.ContLogDate and (( T2.ContLogBegTime >= T1.ContLogBegTime and T2.ContLogBegTime <= T1.ContLogEndTime) or (T2.ContLogEndTime >= T1.ContLogBegTime and T2.ContLogEndTime <= T1.ContLogEndTime))
    left join Provider on Provider.ProvID=T1.ProvID
    left join Client on Client.ClientID=T1.ClientID
    left join xSC on xSC.SCID=T1.SCID
    ${ProviderSelection}
    and T2.ContLogDate is not null and T2.ContLogBegTime is not null 
    and T2.ContLogEndTime is not null
    and T2.ContLogDate>="$form->{FromDate}"
      and T2.ContLogDate<="$form->{ToDate}"
    GROUP by MyKey, MyX |;
  my $dataset = ();
 my $filename = 'zlog.txt';
  open(my $fh, '>', $filename) or die "Could not open file '$filename' $!";
  print $fh $s;
  close $fh;
  ($cnt,$dataset) = graphs->selData($form,$s,$dataset,'MyY',$chartname);
  my $data = graphs->setData($dataset);
  return($data);
}
sub ClinicsByIntDis
{
  my ($self,$form,$addsel) = @_;
  my $ForProvID = $form->{ForProvID} ? $form->{ForProvID} : $form->{LOGINPROVID};
  $chartname = 'stackedbar_chart';
  $xLabel = 'Clinics';
  $yLabel = 'Population';
  $TITLE = qq|${ReportHeader} Clinics by Intellectual Disability|;
  my $s = qq|
select misICD10.ICD10 as MyKey, Clinic.Name as MyX, COUNT(DISTINCT Client.ClientID) as MyY
 from Client
  left join ClientACL on ClientACL.ClientID=Client.ClientID
  left join Provider as Clinic on Clinic.ProvID=Client.clinicClinicID
  left join ClientProblems on ClientProblems.ClientID=Client.ClientID
  left join okmis_config.misICD10 on misICD10.ID=ClientProblems.UUID
 where ClientProblems.InitiatedDate>="$form->{FromDate}" and ClientProblems.InitiatedDate<="$form->{ToDate}"
   and ClientACL.ProvID='$form->{LOGINPROVID}'
   and (misICD10.ICD10='R41.83' or misICD10.ICD10='F70' or misICD10.ICD10='F71' or misICD10.ICD10='F72' or misICD10.ICD10='F73' or misICD10.ICD10='F79')
 group by MyKey, MyX |;
  my $dataset = ();
  ($cnt,$dataset) = graphs->selData($form,$s,$dataset,'MyY',$chartname);
  my $data = graphs->setData($dataset);
  return($data);
}
sub EducationStatus
{
  my ($self,$form,$addsel) = @_;
  my $ForProvID = $form->{ForProvID} ? $form->{ForProvID} : $form->{LOGINPROVID};
  $chartname = 'stackedbar_chart';
  $xLabel = 'Months';
  $yLabel = 'Count';
  $TITLE = qq|${ReportHeader} Clients by School Status|;
  my $s = qq|
      select DATE_FORMAT(Treatment.ContLogDate,'%Y-%m') as MyX, COALESCE(xSchoolStat.Descr,'No Response') as MyKey, Count(distinct(ClientIntake.ID)) as MyY from ClientIntake
      left join Treatment on ClientIntake.ClientID=Treatment.ClientID
      left join okmis_config.xSchoolStat on xSchoolStat.ID = ClientIntake.SchoolStat
      where
      Treatment.ContLogDate>="$form->{FromDate}"
      and Treatment.ContLogDate<="$form->{ToDate}"
      group by MyKey, MyX|;
  my $dataset = ();
  ($cnt,$dataset) = graphs->selData($form,$s,$dataset,'MyY',$chartname);
  my $data = graphs->setData($dataset);
  return($data);
}

sub EducationGrade
{
  my ($self,$form,$addsel) = @_;
  my $ForProvID = $form->{ForProvID} ? $form->{ForProvID} : $form->{LOGINPROVID};
  $chartname = 'stackedbar_chart';
  $xLabel = 'Months';
  $yLabel = 'Highest Grade';
  $TITLE = qq|${ReportHeader} Clients by Highest Grade Completed|;
  my $s = qq|
      select DATE_FORMAT(Treatment.ContLogDate,'%Y-%m') as MyX, COALESCE(ClientIntake.SchoolGrade,'No Response') as MyKey, Count(distinct(ClientIntake.ID)) as MyY from ClientIntake
      left join Treatment on ClientIntake.ClientID=Treatment.ClientID
      where
      Treatment.ContLogDate>="$form->{FromDate}"
      and Treatment.ContLogDate<="$form->{ToDate}"
      group by MyKey, MyX|;
  my $dataset = ();
  ($cnt,$dataset) = graphs->selData($form,$s,$dataset,'MyY',$chartname);
  my $data = graphs->setData($dataset);
  return($data);
}

sub AgeMis
{
  my ($self,$form,$addsel) = @_;
  my $ForProvID = $form->{ForProvID} ? $form->{ForProvID} : $form->{LOGINPROVID};
  $chartname = 'stackedbar_chart';
  $xLabel = 'Months';
  $yLabel = 'Count Category/Legend - MIS Age';
  $TITLE = qq|${ReportHeader} Clients by MIS Age|;
  my $dataset = ();
  my $dbh = myDBI->dbconnect($form->{'DBNAME'});
  my %PROG = ();
  my $cnt = 0;
  $ClinicSelection = DBA->getClinicSelection($form,$ForProvID,'Treatment.ClinicID');
  my $s = qq|
      select distinct 
        Treatment.ClientID, 
        Client.clinicClinicID as ClinicID,
				DATE_FORMAT(Treatment.ContLogDate,'%Y-%m') as MyX,
        DATE_FORMAT(FROM_DAYS(DATEDIFF(NOW(), Client.DOB)), '%Y') as MyKey,
        SUBSTRING_INDEX(Client.Race,'${multidel}',1) as Race
          from Treatment 
            left join Client on Client.ClientID=Treatment.ClientID
            left join ClientIntake on ClientIntake.ClientID=Treatment.ClientID
            left join ClientLegal on ClientLegal.ClientID=Treatment.ClientID
            left join ClientReferrals on ClientReferrals.ClientID=Treatment.ClientID
            left join ClientRelations on ClientRelations.ClientID=Treatment.ClientID
            left join ClientEducation on ClientEducation.ClientID=Treatment.ClientID
            left join ClientSocial on ClientSocial.ClientID=Treatment.ClientID
      where
          Treatment.ContLogDate>="$form->{FromDate}"
          and Treatment.ContLogDate<="$form->{ToDate}"
          ${ClinicSelection}
          GROUP by Treatment.ClientID
          ORDER BY MyX ASC, MyKey ASC| ;
  my $q = $dbh->prepare($s);
  $q->execute();
  my $rows = $q->rows;
  #warn qq|q=${q}\nrows=${rows}\n|;
    while ( $r = $q->fetchrow_hashref )
    {
      my $key = 'none';
      if ( $r->{'MyKey'} >=0 &&  $r->{'MyKey'} <= 3)    { 
        $key = '0 - 03'; 
      }
      elsif ($r->{'MyKey'} >=4 &&  $r->{'MyKey'} <= 7 ) {
         $key = '04 - 07';
         }
      elsif ($r->{'MyKey'} >=8 &&  $r->{'MyKey'} <= 11 ) { 
        $key = '08 - 11'; 
         }
      elsif ($r->{'MyKey'} >=12 &&  $r->{'MyKey'} <= 15)  { 
        $key = '12 - 15'; 
         }
      elsif ($r->{'MyKey'} >=16 &&  $r->{'MyKey'} <= 19)  { 
        $key = '16 - 19'; 
         }
      elsif ($r->{'MyKey'} >=20)  { 
        $key = '20+'; 
         }
      else { 
        $key = 'none'; 
         }
      $cnt++;
      $PROG{$key}{$r->{'MyX'}}++; #{'deterioration minimal':{'Y-M': 'count(10)'}}
    }
    $q->finish();
     foreach my $key ( sort keys %PROG )
        {
          foreach my $date ( sort keys %{ $PROG{$key} } )
          {
            my $x = $date;
            my $y = $PROG{$key}{$date};
            $key =~ s/'//g; $x =~ s/'//g; $y =~ s/'//g;
            push(@{$dataset->{$key}},$x,$y); $cnt++;
          }
        }
  my $data = graphs->setData($dataset);
  return($data);
}

sub AgeCARF
{
  my ($self,$form,$addsel) = @_;  
  my $ForProvID = $form->{ForProvID} ? $form->{ForProvID} : $form->{LOGINPROVID};
  $chartname = 'stackedbar_chart';
  $xLabel = 'Months';
  $yLabel = 'Count Category/Legend - CARF Age';
  $TITLE = qq|${ReportHeader} Clients by CARF Age|;
    my $dataset = ();
  my $dbh = myDBI->dbconnect($form->{'DBNAME'});
  my %PROG = ();
  my $cnt = 0;
   $ClinicSelection = DBA->getClinicSelection($form,$ForProvID,'Treatment.ClinicID');
  my $s = qq|
      select distinct 
        Treatment.ClientID, 
        Client.clinicClinicID as ClinicID,
				DATE_FORMAT(Treatment.ContLogDate,'%Y-%m') as MyX,
        DATE_FORMAT(FROM_DAYS(DATEDIFF(NOW(), Client.DOB)), '%Y') as MyKey,
        SUBSTRING_INDEX(Client.Race,'${multidel}',1) as Race
          from Treatment 
            left join Client on Client.ClientID=Treatment.ClientID
            left join ClientIntake on ClientIntake.ClientID=Treatment.ClientID
            left join ClientLegal on ClientLegal.ClientID=Treatment.ClientID
            left join ClientReferrals on ClientReferrals.ClientID=Treatment.ClientID
            left join ClientRelations on ClientRelations.ClientID=Treatment.ClientID
            left join ClientEducation on ClientEducation.ClientID=Treatment.ClientID
            left join ClientSocial on ClientSocial.ClientID=Treatment.ClientID
      where
          Treatment.ContLogDate>="$form->{FromDate}"
          and Treatment.ContLogDate<="$form->{ToDate}"
          ${ClinicSelection}
          GROUP by Treatment.ClientID
          ORDER BY MyX ASC, MyKey ASC| ;
  my $q = $dbh->prepare($s);
  $q->execute();
  my $rows = $q->rows;
  #warn qq|q=${q}\nrows=${rows}\n|;
    while ( $r = $q->fetchrow_hashref )
    {
      my $key = 'none';
      if ( $r->{'MyKey'} >=0 &&  $r->{'MyKey'} <= 5)    { 
        $key = '0 - 05'; 
      }
      elsif ($r->{'MyKey'} >=6 &&  $r->{'MyKey'} <= 17 ) {
         $key = '06 - 17';
         }
      elsif ($r->{'MyKey'} >=18 &&  $r->{'MyKey'} <= 40 ) { 
        $key = '18 - 40'; 
         }
      elsif ($r->{'MyKey'} >=41 &&  $r->{'MyKey'} <= 65)  { 
        $key = '41 - 65'; 
         }
      elsif ($r->{'MyKey'} >=66 &&  $r->{'MyKey'} <= 85)  { 
        $key = '66 - 85'; 
         }
      elsif ($r->{'MyKey'} >85)  { 
        $key = '85+'; 
         }
      else { 
        $key = 'none'; 
         }
      $cnt++;
      $PROG{$key}{$r->{'MyX'}}++; #{'deterioration minimal':{'Y-M': 'count(10)'}}
    }
    $q->finish();
     foreach my $key ( sort keys %PROG )
        {
          foreach my $date ( sort keys %{ $PROG{$key} } )
          {
            my $x = $date;
            my $y = $PROG{$key}{$date};
            $key =~ s/'//g; $x =~ s/'//g; $y =~ s/'//g;
            push(@{$dataset->{$key}},$x,$y); $cnt++;
          }
        }
  my $data = graphs->setData($dataset);
  return($data);
}

sub clientsByEmploymentStatus
{
  my ($self,$form,$addsel) = @_;
  my $ForProvID = $form->{ForProvID} ? $form->{ForProvID} : $form->{LOGINPROVID};
  $chartname = 'stackedbar_chart';
  $xLabel = 'Months';
  $yLabel = 'Count Category/Legend - Employment Status';
  $TITLE = qq|${ReportHeader} Clients by Employment Status|;
  my $s = qq|
      select DATE_FORMAT(Treatment.ContLogDate,'%Y-%m') as MyX, COALESCE(xEmplStat.Descr,'No Response') as MyKey, Count(distinct(Client.ClientID)) as MyY from Client
      left join Treatment on Client.ClientID=Treatment.ClientID
      left join xEmplStat on xEmplStat.ID = Client.EmplStat
      where
      Treatment.ContLogDate>="$form->{FromDate}"
      and Treatment.ContLogDate<="$form->{ToDate}"
      group by MyKey, MyX|;
  my $dataset = ();
  ($cnt,$dataset) = graphs->selData($form,$s,$dataset,'MyY',$chartname);
  my $data = graphs->setData($dataset);
  return($data);
}

sub clientsByEmploymentType
{
  my ($self,$form,$addsel) = @_;
  my $ForProvID = $form->{ForProvID} ? $form->{ForProvID} : $form->{LOGINPROVID};
  $chartname = 'stackedbar_chart';
  $xLabel = 'Months';
  $yLabel = 'Count Category/Legend - Employment Type';
  $TITLE = qq|${ReportHeader} Clients by Employment Type|;
  my $s = qq|
      select DATE_FORMAT(Treatment.ContLogDate,'%Y-%m') as MyX, COALESCE(xEmplType.Descr,'No Response') as MyKey, Count(distinct(Client.ClientID)) as MyY from Client
      left join Treatment on Client.ClientID=Treatment.ClientID
      left join xEmplType on xEmplType.ID = Client.EmplType
      where
      Treatment.ContLogDate>="$form->{FromDate}"
      and Treatment.ContLogDate<="$form->{ToDate}"
      group by MyKey, MyX|;
  my $dataset = ();
  ($cnt,$dataset) = graphs->selData($form,$s,$dataset,'MyY',$chartname);
  my $data = graphs->setData($dataset);
  return($data);
}

sub PAWait
{
  my ($self,$form,$addsel) = @_;
  my $ForProvID = $form->{ForProvID} ? $form->{ForProvID} : $form->{LOGINPROVID};
  $chartname = 'stackedbar_chart';
  $xLabel = 'Prior Authorization';
  $yLabel = 'Count';
  $TITLE = qq|${ReportHeader} PAs Waiting|;
  my $ActiveSelection = qq| and Client.Active=1| if ( $form->{Active} );
  my $s = qq|
  select xInsurance.Name as MyKey, DATE_FORMAT(ClientPrAuthCDC.StatusDate,'%Y-%m') as MyX, COUNT(DISTINCT Client.ClientID) as MyY
  from ClientPrAuth
    left join ClientPrAuthCDC on ClientPrAuthCDC.ClientPrAuthID=ClientPrAuth.ID
    left join Client on Client.ClientID=ClientPrAuth.ClientID
    left join ClientACL on ClientACL.ClientID=Client.ClientID
    left join Insurance on Insurance.InsNumID=ClientPrAuth.InsuranceID
    left join Contracts on Contracts.ProvID=Client.clinicClinicID and Contracts.InsID=Insurance.InsID
    left join Provider on Provider.ProvID=Client.ProvID
    left join xInsurance on xInsurance.ID=Insurance.InsID
  where (ClientPrAuthCDC.Status IN('Waiting','Send','New','Pending') or ClientPrAuthCDC.Status is null)
    and ClientPrAuthCDC.StatusDate between '$form->{FromDate}' and '$form->{ToDate}'
    and ClientACL.ProvID='${ForProvID}'
    ${ActiveSelection}
  group by MyKey, MyX |;
  my $dataset = ();
  ($cnt,$dataset) = graphs->selData($form,$s,$dataset,'MyY',$chartname);
  my $data = graphs->setData($dataset);
  return($data);
}
sub PAReject
{
  my ($self,$form,$addsel) = @_;
  my $ForProvID = $form->{ForProvID} ? $form->{ForProvID} : $form->{LOGINPROVID};
  $chartname = 'stackedbar_chart';
  $xLabel = 'Prior Authorization';
  $yLabel = 'Count';
  $TITLE = qq|${ReportHeader} PAs Pending/Rejected|;
  my $ActiveSelection = qq| and Client.Active=1| if ( $form->{Active} );
  my $s = qq|
  select xInsurance.Name as MyKey, DATE_FORMAT(ClientPrAuthCDC.StatusDate,'%Y-%m') as MyX, COUNT(DISTINCT Client.ClientID) as MyY
  from ClientPrAuth
    left join ClientPrAuthCDC on ClientPrAuthCDC.ClientPrAuthID=ClientPrAuth.ID
    left join Client on Client.ClientID=ClientPrAuth.ClientID
    left join ClientACL on ClientACL.ClientID=Client.ClientID
    left join Insurance on Insurance.InsNumID=ClientPrAuth.InsuranceID
    left join Contracts on Contracts.ProvID=Client.clinicClinicID and Contracts.InsID=Insurance.InsID
    left join Provider on Provider.ProvID=Client.ProvID
    left join xInsurance on xInsurance.ID=Insurance.InsID
    left join okmis_config.xCDCTransTypes on xCDCTransTypes.ID=ClientPrAuthCDC.TransType
  where ClientPrAuthCDC.Status IN('Pending','Rejected')
    and ClientPrAuthCDC.StatusDate between '$form->{FromDate}' and '$form->{ToDate}'
    and ClientACL.ProvID='${ForProvID}'
    ${ActiveSelection}
  group by MyKey, MyX |;
  my $dataset = ();
  ($cnt,$dataset) = graphs->selData($form,$s,$dataset,'MyY',$chartname);
  my $data = graphs->setData($dataset);
  return($data);
}
sub PAFinal
{
  my ($self,$form,$addsel) = @_;
  my $ForProvID = $form->{ForProvID} ? $form->{ForProvID} : $form->{LOGINPROVID};
  $chartname = 'stackedbar_chart';
  $xLabel = 'Prior Authorization';
  $yLabel = 'Count';
  $TITLE = qq|${ReportHeader} PAs Approved|;
  my $ActiveSelection = qq| and Client.Active=1| if ( $form->{Active} );
  my $s = qq|
  select xInsurance.Name as MyKey, DATE_FORMAT(ClientPrAuthCDC.StatusDate,'%Y-%m') as MyX, COUNT(DISTINCT Client.ClientID) as MyY
  from ClientPrAuth
    left join ClientPrAuthCDC on ClientPrAuthCDC.ClientPrAuthID=ClientPrAuth.ID
    left join Client on Client.ClientID=ClientPrAuth.ClientID
    left join ClientACL on ClientACL.ClientID=Client.ClientID
    left join Insurance on Insurance.InsNumID=ClientPrAuth.InsuranceID
    left join Contracts on Contracts.ProvID=Client.clinicClinicID and Contracts.InsID=Insurance.InsID
    left join Provider on Provider.ProvID=Client.ProvID
    left join xInsurance on xInsurance.ID=Insurance.InsID
  where ClientPrAuthCDC.Status IN('Approved','AUTOAUTH','CM_AUTH','Final-Approved')
    and ClientPrAuthCDC.StatusDate between '$form->{FromDate}' and '$form->{ToDate}'
    and ClientACL.ProvID='${ForProvID}'
    ${ActiveSelection}
 group by MyKey, MyX |;
  my $dataset = ();
  ($cnt,$dataset) = graphs->selData($form,$s,$dataset,'MyY',$chartname);
  my $data = graphs->setData($dataset);
  return($data);
}
sub PAFinal2
{
  my ($self,$form,$addsel) = @_;
  my $ForProvID = $form->{ForProvID} ? $form->{ForProvID} : $form->{LOGINPROVID};
  $chartname = 'stackedbar_chart';
  $xLabel = 'PAGroup';
  $yLabel = 'TL';
  $TITLE = qq|${ReportHeader} PAs Approved|;
  my $ActiveSelection = qq| and Client.Active=1| if ( $form->{Active} );
  my $s = qq|
  select ClientPrAuth.PAgroup as MyKey, DATE_FORMAT(ClientPrAuthCDC.StatusDate,'%Y-%m') as MyX, ClientPrAuth.TL as MyY
  from ClientPrAuth
    left join ClientPrAuthCDC on ClientPrAuthCDC.ClientPrAuthID=ClientPrAuth.ID
    left join Client on Client.ClientID=ClientPrAuth.ClientID
    left join ClientACL on ClientACL.ClientID=Client.ClientID
    left join Insurance on Insurance.InsNumID=ClientPrAuth.InsuranceID
    left join Contracts on Contracts.ProvID=Client.clinicClinicID and Contracts.InsID=Insurance.InsID
    left join Provider on Provider.ProvID=Client.ProvID
    left join xInsurance on xInsurance.ID=Insurance.InsID
  where ClientPrAuthCDC.Status IN('Approved','AUTOAUTH','CM_AUTH','Final-Approved')
    and ClientPrAuthCDC.StatusDate between '$form->{FromDate}' and '$form->{ToDate}'
    and ClientACL.ProvID='${ForProvID}'
    ${ActiveSelection}
 group by MyKey, MyX |;
  my $dataset = ();
  ($cnt,$dataset) = graphs->selData($form,$s,$dataset,'MyY',$chartname);
  my $data = graphs->setData($dataset);
  return($data);
}
sub PAExpire
{
  my ($self,$form,$addsel) = @_;
  my $ForProvID = $form->{ForProvID} ? $form->{ForProvID} : $form->{LOGINPROVID};
  $chartname = 'stackedbar_chart';
  $xLabel = 'Provider';
  $yLabel = 'Count';
  $TITLE = qq|${ReportHeader} Prior Authorization Expire Report|;
  my $daysRem = 14;

    $fromDate = $form->{'FromDate'};
    ($yyyy, $mm, $dd) = ($fromDate =~ /(\d+)-(\d+)-(\d+)/); 
    
    $fromDate = DateTime->new(  
          day        => $dd,  
          month      => $mm,  
          year       => $yyyy,  
          hour       => 23,
      );  
      
    $ToDate = $form->{'ToDate'};
    ($yyyy, $mm, $dd) = ($ToDate =~ /(\d+)-(\d+)-(\d+)/); 
    
    $ToDate = DateTime->new(  
          day        => $dd,  
          month      => $mm,  
          year       => $yyyy,  
          hour       => 23,
      );  

    my $datetime = DateTime->now;

    my $cmp = DateTime->compare($datetime, $fromDate);
    my $cmp2 = DateTime->compare($datetime, $ToDate);
    my $f_from = '';
    my $f_to = '';
    if($cmp ==1 ){
      $f_from = $datetime->ymd;
    }else{
      $f_from = $fromDate->ymd;
    }
    if($cmp2 ==1 ){
      $ToDate = $datetime->add(days => 14);
      $f_to = $ToDate->ymd;
    }else{
      $f_to = $ToDate->ymd;
    }

    ($yyyy, $mm, $dd) = ($f_from =~ /(\d+)-(\d+)-(\d+)/); 
    
    $dt_start = DateTime->new(  
          day        => $dd,  
          month      => $mm,  
          year       => $yyyy,  
          hour       => 00,
      );  
    ($yyyy, $mm, $dd) = ($f_to =~ /(\d+)-(\d+)-(\d+)/); 
    
    $dt_end = DateTime->new(  
          day        => $dd,  
          month      => $mm,  
          year       => $yyyy,  
          hour       => 00,
      ); 

    $daysRem = $dt_end->delta_days($dt_start);
    $daysRem = $daysRem->in_units('days');

    my $fdow = DBUtil->Date($f_from,'dow');
    my $fdayname = (Sunday,Monday,Tuesday,Wednesday,Thursday,Friday,Saturday)[$fdow];
    my $tdow = DBUtil->Date($f_to,'dow');
    my $tdayname = (Sunday,Monday,Tuesday,Wednesday,Thursday,Friday,Saturday)[$tdow];
    my $DateRange = qq|from ${fdayname} $f_from - ${tdayname} $f_to|;
    $SUBTITLE = qq| PA Expire Report form ${fdayname} $f_from - ${tdayname} $f_to|;

  my $ActiveSelection = qq| and Client.Active=1| if ( !$form->{Active} );

  my $dataset = ();
  my $dbh = myDBI->dbconnect($form->{'DBNAME'});
  my %PROG = ();
  my $cnt = 0;
#   to_days(ClientPrAuth.ExpDate) - to_days(curdate()) as Remaining
  my $ForProvID = $form->{ForProvID} ? $form->{ForProvID} : $form->{LOGINPROVID};
  my $qClient = qq|select Client.* from Client
      left join ClientACL on ClientACL.ClientID=Client.ClientID
    where Active=1 and ClientACL.ProvID='${ForProvID}' order by LName, FName|;
  my $sClient = $dbh->prepare($qClient);
  my $sProvider = $dbh->prepare("select LName, FName from Provider where ProvID=?");
  my $sInsurance = $dbh->prepare("
  select xInsurance.Name, Insurance.InsIDNum from Insurance 
      left join xInsurance on xInsurance.ID=Insurance.InsID
    where Insurance.ClientID=? 
      and Insurance.Priority=1 
      and (curdate()<=Insurance.InsNumExpDate or Insurance.InsNumExpDate is NULL)");
  my $sPrAuth = $dbh->prepare("select ID, PAnumber, ExpDate from ClientPrAuth
    where ClientID=? and EffDate <= curdate() and (curdate() <= ExpDate or ExpDate is null)
    order by ID desc");

$sClient->execute();
while (my $rClient = $sClient->fetchrow_hashref)
{ 
  $sProvider->execute($rClient->{ProvID});
  my ($ProvLName, $ProvFName) = $sProvider->fetchrow_array;
  $ProvName = qq|$ProvLName, $ProvFName ($rClient->{ProvID})|; 

  $sInsurance->execute($rClient->{ClientID});
  my ($InsName, $InsGrpNum) = $sInsurance->fetchrow_array;

  $sPrAuth->execute($rClient->{ClientID});
  my ($PrAuthID, $PAnumber, $PrAuthExpDate) = $sPrAuth->fetchrow_array;

  my $SubtractDays = $dbh->prepare("select to_days(?) - to_days(curdate())");
  $SubtractDays->execute($PrAuthExpDate);
  my $Remaining = $SubtractDays->fetchrow_array;
  $SubtractDays->finish();
  $Remaining = 0 if ( $Remaining eq '' );

  #warn qq|$rClient->{LName}, $rClient->{FName} ($rClient->{ClientID})\t${ProvName}\t${PAnumber}\t${PrAuthExpDate}\t${InsName}\t${InsGrpNum}\t${Remaining}\n| if ( $form->{'LOGINPROVID'} == 121 );
  # print qq|$rClient->{LName}, $rClient->{FName} ($rClient->{ClientID})\t${ProvName}\t${PAnumber}\t${PrAuthExpDate}\t${InsName}\t${InsGrpNum}\t${Remaining}\n| 
  #   if ( $Remaining <= ${Days_Remaining} );
  
  if($Remaining <= $daysRem ){
    $cnt++;
    my $key = $InsName;
    $PROG{$key}{$ProvName}++;
    }
}
$sClient->finish();
$sPrAuth->finish;
$sInsurance->finish;
$sProvider->finish;

    foreach my $key ( sort keys %PROG )
      {
        foreach my $ProvName ( sort keys %{ $PROG{$key} } )
        {
          my $x = $ProvName;
          my $y = $PROG{$key}{$ProvName};
          $key =~ s/'//g; $x =~ s/'//g; $y =~ s/'//g;
          push(@{$dataset->{$key}},$x,$y); $cnt++;
        }
      }
my $data = graphs->setData($dataset);
return($data);
}
sub Pachg
{
  my ($self,$form,$addsel) = @_;
  my $ForProvID = $form->{ForProvID} ? $form->{ForProvID} : $form->{LOGINPROVID};
  $chartname = 'stackedbar_chart';
  $xLabel = 'Provider';
  $yLabel = 'Count';
  $TITLE = qq|${ReportHeader} Change Prior Authorizations from Rehab to NO REHAB|;
  my $ActiveSelection = qq| and Client.Active=1| if ( $form->{Active} );
  my $s = qq|
  select xInsurance.Name as MyKey, Provider.LName as MyX, COUNT(DISTINCT Client.ClientID) as MyY
  from ClientPrAuth
    left join ClientPrAuthCDC on ClientPrAuthCDC.ClientPrAuthID=ClientPrAuth.ID
    left join Client on Client.ClientID=ClientPrAuth.ClientID
    left join ClientACL on ClientACL.ClientID=Client.ClientID
    left join Insurance on Insurance.InsNumID=ClientPrAuth.InsuranceID
    left join Contracts on Contracts.ProvID=Client.clinicClinicID and Contracts.InsID=Insurance.InsID
    left join Provider on Provider.ProvID=Client.ProvID
    left join xInsurance on xInsurance.ID=Insurance.InsID
    left join okmis_config.xCDCTransTypes on xCDCTransTypes.ID=ClientPrAuthCDC.TransType
  where ClientPrAuth.NotificationType=19
    and ClientACL.ProvID='${ForProvID}'
    ${ActiveSelection}
 group by MyKey, MyX |;
  my $dataset = ();
  ($cnt,$dataset) = graphs->selData($form,$s,$dataset,'MyY',$chartname);
  my $data = graphs->setData($dataset);
  return($data);
}
sub Over35
{
  my ($self,$form,$addsel) = @_;
  my $ForProvID = $form->{ForProvID} ? $form->{ForProvID} : $form->{LOGINPROVID};
  $chartname = 'stackedbar_chart';
  $xLabel = 'Month';
  $yLabel = 'Count';
  $TITLE = qq|${ReportHeader} Provider Over 35 Hours|;
  $ProviderSelection = DBA->getProviderSelection($form,$ForProvID,'Provider.ProvID','where');
  $ProviderSelection .= qq| and Provider.Active=1| if ( $form->{Active} );
  my $s = qq|
  select CONCAT(Provider.LName,', ',Provider.FName,' ',Provider.ProvID) as MyKey, DATE_FORMAT(Over35.Sunday,'%Y-%m') as MyX, COUNT(DISTINCT Over35.Sunday) as MyY
  from Over35
    left join Provider on Provider.ProvID=Over35.ProvID
  ${ProviderSelection}
    and Over35.Over = 'Yes'
    and Over35.Sunday between '$form->{FromDate}' and '$form->{ToDate}'
 group by MyKey, MyX |;
  my $dataset = ();
  ($cnt,$dataset) = graphs->selData($form,$s,$dataset,'MyY',$chartname);
  my $data = graphs->setData($dataset);
  return($data);
}
sub DISWait
{
  my ($self,$form,$addsel) = @_;
  my $ForProvID = $form->{ForProvID} ? $form->{ForProvID} : $form->{LOGINPROVID};
  $chartname = 'stackedbar_chart';
  $xLabel = 'Prior Authorization';
  $yLabel = 'Count';
  $TITLE = qq|${ReportHeader} Discharges Waiting|;
  my $ActiveSelection = qq| and Client.Active=1| if ( $form->{Active} );
  my $s = qq|
  select xInsurance.Name as MyKey, DATE_FORMAT(ClientDischargeCDC.StatusDate,'%Y-%m') as MyX, COUNT(DISTINCT Client.ClientID) as MyY
  from ClientDischarge
    left join ClientDischargeCDC on ClientDischargeCDC.ClientDischargeID=ClientDischarge.ID
    left join Client on Client.ClientID=ClientDischarge.ClientID
    left join ClientACL on ClientACL.ClientID=Client.ClientID
    left join Insurance on Insurance.InsNumID=ClientDischarge.InsuranceID
    left join Contracts on Contracts.ProvID=Client.clinicClinicID and Contracts.InsID=Insurance.InsID
    left join Provider on Provider.ProvID=Client.ProvID
    left join xInsurance on xInsurance.ID=Insurance.InsID
  where (ClientDischargeCDC.Status IN('Waiting','Send','New') or ClientDischargeCDC.Status is null)
    and ClientDischargeCDC.StatusDate between '$form->{FromDate}' and '$form->{ToDate}'
    and ClientACL.ProvID='${ForProvID}'
    ${ActiveSelection}
  group by MyKey, MyX |;
  my $dataset = ();
  ($cnt,$dataset) = graphs->selData($form,$s,$dataset,'MyY',$chartname);
  my $data = graphs->setData($dataset);
  return($data);
}
sub DISReject
{
  my ($self,$form,$addsel) = @_;
  my $ForProvID = $form->{ForProvID} ? $form->{ForProvID} : $form->{LOGINPROVID};
  $chartname = 'stackedbar_chart';
  $xLabel = 'Prior Authorization';
  $yLabel = 'Count';
  $TITLE = qq|${ReportHeader} Discharges Rejected|;
  my $ActiveSelection = qq| and Client.Active=1| if ( $form->{Active} );
  my $s = qq|
  select xInsurance.Name as MyKey, DATE_FORMAT(ClientDischargeCDC.StatusDate,'%Y-%m') as MyX, COUNT(DISTINCT Client.ClientID) as MyY
  from ClientDischarge
    left join ClientDischargeCDC on ClientDischargeCDC.ClientDischargeID=ClientDischarge.ID
    left join Client on Client.ClientID=ClientDischarge.ClientID
    left join ClientACL on ClientACL.ClientID=Client.ClientID
    left join Insurance on Insurance.InsNumID=ClientDischarge.InsuranceID
    left join Contracts on Contracts.ProvID=Client.clinicClinicID and Contracts.InsID=Insurance.InsID
    left join Provider on Provider.ProvID=Client.ProvID
    left join xInsurance on xInsurance.ID=Insurance.InsID
  where (ClientDischargeCDC.Status IN('Rejected','Pending') or ClientDischargeCDC.Status is null)
    and ClientDischargeCDC.StatusDate between '$form->{FromDate}' and '$form->{ToDate}'
    and ClientACL.ProvID='${ForProvID}'
    ${ActiveSelection}
  group by MyKey, MyX |;
  my $dataset = ();
  ($cnt,$dataset) = graphs->selData($form,$s,$dataset,'MyY',$chartname);
  my $data = graphs->setData($dataset);
  return($data);
}
############################################################################
# for CAR Scores (PDDom)
#   trend   = previous - current
#   overall = first - current     (default)
############################################################################
sub CARSByClient
{
  my ($self,$form,$addsel) = @_;
  my $ForProvID = $form->{ForProvID} ? $form->{ForProvID} : $form->{LOGINPROVID};
  $chartname = 'stackedbar_chart';
  $xLabel = 'Clients';
  $yLabel = 'Difference';
  $HEIGHT = 800;
  $WIDTH = 1000;
  $TITLE = qq|${ReportHeader} CARS by Client Population|;
  $SUBTITLE = $form->{'Type'} =~ /overall/i
            ? qq|Overall CAR Scores first - current|
            : qq|Trending CAR Scores previous - current|;
  my $dataset = ();
  ($cnt,$dataset) = main->selCARScores($form,$dataset,$addsel);
  $WIDTH = $cnt * 15 if ( $cnt > 65 );      # widen the graph is many elements.
  my $data = graphs->setData($dataset);
  return($data);
}
sub CARSByClinic
{
  my ($self,$form,$addsel) = @_;
  my $ForProvID = $form->{ForProvID} ? $form->{ForProvID} : $form->{LOGINPROVID};
  $chartname = 'stackedbar_chart';
  $xLabel = 'Clinics';
  $yLabel = 'Difference';
  $HEIGHT = 800;
  $WIDTH = 1000;
  $TITLE = qq|${ReportHeader} CARS by Clinics Population|;
  $SUBTITLE = $form->{'Type'} =~ /overall/i
            ? qq|Overall CAR Scores first - current|
            : qq|Trending CAR Scores previous - current|;
  my $dataset = ();
  ($cnt,$dataset) = main->selCARScores($form,$dataset,$addsel,1);
  $WIDTH = $cnt * 15 if ( $cnt > 65 );      # widen the graph is many elements.
  my $data = graphs->setData($dataset);
  return($data);
}
sub selCARScores
{
  my ($self,$form,$data_array,$addsel,$byClinic) = @_;
  my $dbh = myDBI->dbconnect($form->{'DBNAME'});
  my %Scores = ();
  my ($PrevClientID,$ClientName,$ClientCount) = ('','',0);
  my $cnt = 0;
# ignore incoming addsel because we don't select with Treatment table for Treatment.ProvID
  my $addSelection = DBA->withClinicProvider($form,'and','Client.clinicClinicID','Client.ProvID');
#                                                                    instead Client.ProvID  ^^
  my $sPDDom = $dbh->prepare("
  select PDDom.*,Client.LName,Client.FName,Clinic.Name as ClinicName
   from PDDom
    left join Client on Client.ClientID=PDDom.ClientID
    left join Provider as Clinic on Clinic.ProvID=Client.clinicClinicID
    left join ClientPrAuth on ClientPrAuth.ID=PDDom.PrAuthID
    where Client.Active=1 ${addSelection}
   order by Client.LName,Client.FName,Client.ClientID,ClientPrAuth.EffDate desc
  ");
if ( $form->{LOGINPROVID} == 91 )
{
my $sel = qq|
  select PDDom.*,Client.LName,Client.FName,Clinic.Name as ClinicName
   from PDDom
    left join Client on Client.ClientID=PDDom.ClientID
    left join Provider as Clinic on Clinic.ProvID=Client.clinicClinicID
    left join ClientPrAuth on ClientPrAuth.ID=PDDom.PrAuthID
    where Client.Active=1 ${addsel}
   order by Client.LName,Client.FName,Client.ClientID,ClientPrAuth.EffDate desc
|;
  open OUT, ">>/home/okmis/mis/src/debug/graphs.out" or die "Couldn't open file: $!";
  print OUT qq|sel=\n$sel\n|;
  print OUT qq|y_values=$y_values\n|;
  close(OUT);
}
  $sPDDom->execute();
  while ( $rPDDom = $sPDDom->fetchrow_hashref )
  {
    my $ClientID = $rPDDom->{ClientID};
    my $key = qq|$rPDDom->{LName}, $rPDDom->{FName}_$rPDDom->{ClientID}_$rPDDom->{ClinicName}|;
    if ( $PrevClientID eq $ClientID ) { $ClientCount++; }
    else
    {
      # save new/current Client information
      $PrevClientID = $ClientID;
      $ClientCount = 1;                    # reset back to first
    }
    if ( $ClientCount == 1 )
    {
      for ( my $i=1; $i<=9; $i++ )
      {
        my $fld = 'Dom'.$i.'Score';
        $Score = $rPDDom->{$fld};
        $Scores{$key}{Score1}{$fld} = $Score;
#warn "Score1: ${ClientID}, ${fld}=${Score}\n";
      }
    }
    # GET second(2) score for client...
    # skip if ClientCount > 2
    # unless its 'overall' then resets Client scores until first(last in list)
    elsif ( $ClientCount == 2 || $form->{'Type'} =~ /overall/i )
    {
      for ( my $i=1; $i<=9; $i++ )
      {
        my $fld = 'Dom'.$i.'Score';
        $Score = $rPDDom->{$fld};
        $Scores{$key}{Score2}{$fld} = $Score;
#warn "Score2: ${ClientID}, ${fld}=${Score}\n";
      }
    }
  }
  $sPDDom->finish();
  my %DIFF = ();
  foreach my $key ( sort keys %Scores )
  {
    my ($client,$id,$clinic) = split('_',$key);
    my ($Core1,$Core2) = (0,0);
    for my $i ( 1..9 )
    {
      my $fld = 'Dom'.$i.'Score';
      my $Score1 = $Scores{$key}{Score1}{$fld};
      my $Score2 = $Scores{$key}{Score2}{$fld};
      my $Diff = $Score1 && $Score2 ? sprintf("%.2f", $Score2 - $Score1) : 0;
#warn "${PrevClientID}, ${fld}=${Score1}/${Score2}\n";
      if ( $Diff != 0 )
      {
        my $name = $byClinic ? $clinic : $client;
        $DIFF{$name}{$fld} += $Diff;
      }
      if ( $i == 1 || $i == 2 || $i == 3 || $i == 6 || $i == 7 )
      { $Core1 += $Score1; $Core2 += $Score2; }
    }
    my $Diff = $Core1 && $Core2 ? sprintf("%.2f", $Core2 - $Core1) : 0;
    if ( $Diff != 0 )
    {
      my $name = $byClinic ? $clinic : $client;
      $DIFF{$name}{Core} += $Diff;
    }
  }
  foreach my $name ( sort keys %DIFF )
  {
    foreach my $fld ( sort keys %{$DIFF{$name}} )
    {
      my $key = $fld;
      my $x = $name;
      my $y = $DIFF{$x}{$key};
      $key =~ s/'//g; $x =~ s/'//g; $y =~ s/'//g;
      push(@{$data_array->{$key}},$x,$y); $cnt++;
    }
  }
  return($cnt,$data_array);
}
sub ProgressByDate
{
  my ($self,$form,$addsel) = @_;
  my $ForProvID = $form->{ForProvID} ? $form->{ForProvID} : $form->{LOGINPROVID};
  $chartname = 'stackedbar_chart';
  $xLabel = 'Progress';
  $yLabel = 'Visits';
  $HEIGHT = 800;
  $WIDTH = 1000;
  $TITLE = qq|${ReportHeader} Progress - Count|;
  my $dataset = ();
  ($cnt,$dataset) = main->selProgress($form,$dataset,$addsel);
  $WIDTH = $cnt * 15 if ( $cnt > 65 );      # widen the graph is many elements.
  my $data = graphs->setData($dataset);
  return($data);
}
sub selProgress
{
  my ($self,$form,$data_array,$addsel,$byClinic) = @_;
  my $dbh = myDBI->dbconnect($form->{'DBNAME'});
  my %PROG = ();
  my %TOTAL = ();
  my ($PrevClientID,$ClientName,$ClientCount) = ('','',0);
  my ($cnt,$oDate) = (0,'');
  my $avg = 0;
  my $q = qq|
select ProgNotes.*,Treatment.*,Client.LName,Client.FName,Clinic.Name as ClinicName
      ,DATE_FORMAT(Treatment.ContLogDate,'%Y-%m') as MyX
 from ProgNotes
  left join Treatment on Treatment.TrID=ProgNotes.NoteID
  left join Client on Client.ClientID=ProgNotes.ClientID
  left join ClientACL on ClientACL.ClientID=Client.ClientID
  left join Provider as Clinic on Clinic.ProvID=Treatment.ClinicID
  left join xSC on xSC.SCID=Treatment.SCID
  left join xInsurance on xInsurance.ID=xSC.InsID
 where Treatment.ContLogDate>="$form->{FromDate}" and Treatment.ContLogDate<="$form->{ToDate}"
  and | . DBA->withNoteAccess($form,$ForProvID,'Treatment') . $addsel . qq|
  order by ProgNotes.Progress|;
  my $s = $dbh->prepare($q);
if ( $form->{LOGINPROVID} == 91 )
{
  open OUT, ">>/home/okmis/mis/src/debug/graphs.out" or die "Couldn't open file: $!";
  print OUT qq|q=\n${q}\n|;
  close(OUT);
}
  $s->execute();
  my $rows = $s->rows;
#warn qq|q=${q}\nrows=${rows}\n|;
  while ( $r = $s->fetchrow_hashref )
  {
    my $key = 'none';
    if ( $r->{'Progress'} == -1 )    { $key = 'deterioration minimal'; }
    elsif ( $r->{'Progress'} == -2 ) { $key = 'deterioration  moderate'; }
    elsif ( $r->{'Progress'} == -3 ) { $key = 'deterioration   significant'; }
    elsif ( $r->{'Progress'} == 1 )  { $key = 'progress minimal'; }
    elsif ( $r->{'Progress'} == 2 )  { $key = 'progress moderate'; }
    elsif ( $r->{'Progress'} == 3 )  { $key = 'progress significant'; }
    else                             { $key = 'none'; }
    $PROG{$key}{$r->{'MyX'}}++; # {'deterioration minimal':{'Y-M': 'count(10)'}}
    $TOTAL{$r->{'MyX'}}++;
  }
  $s->finish();
  my @k = ("deterioration   significant", "deterioration  moderate", "deterioration minimal","none", "progress minimal", "progress moderate", "progress significant");

 for my $key (@k) {
#warn qq|selProgress: key=${key}\n|;
    foreach my $date ( keys %{ $PROG{$key} } )
    {
#warn qq|selProgress: key=${key}, date=${date}\n|;
      my $x = $date;
      my $y = $PROG{$key}{$date};
      $key =~ s/'//g; $x =~ s/'//g; $y =~ s/'//g;
#warn qq|selProgress: key=${key}, x=${x}, y=${y}\n|;
#warn qq|selProgress: date=${date}, TOTAL=$TOTAL{$date}\n|;
      push(@{$data_array->{$key}},$x,$y); $cnt++;
    }
  }
  return($cnt,$data_array);
}


sub ProgressByAverage
{
  my ($self,$form,$addsel) = @_;
  my $ForProvID = $form->{ForProvID} ? $form->{ForProvID} : $form->{LOGINPROVID};
  $chartname = 'line_chart';
  $xLabel = 'Average Progress by clinic by Monthly TimeLine';
  $yLabel = 'Progress ';
  $HEIGHT = 800;
  $WIDTH = 500;
  $TITLE = qq|${ReportHeader} Progress - Statistics|;
  my $dataset = ();

  $fromDate = $form->{'FromDate'};
   my ($yyyy, $mm, $dd) = ($fromDate =~ /(\d+)-(\d+)-(\d+)/); 
    
    $fromDate = DateTime->new(  
          day        => $dd,  
          month      => $mm,  
          year       => $yyyy,  
          hour       => 23,
      );  
      
    $ToDate = $form->{'ToDate'};
    my ($y1, $m1, $d1) = ($ToDate =~ /(\d+)-(\d+)-(\d+)/); 
    
    $ToDate = DateTime->new(  
          day        => $d1,  
          month      => $m1,  
          year       => $y1,  
          hour       => 23,
      );  

    my $month_starts = do {
      my $date1_month_start = $fromDate->clone;
      my $date2_month_start = $ToDate->clone;

      $_->truncate( to => 'month' )
          for $date1_month_start, $date2_month_start;

      $date2_month_start->delta_md($date1_month_start)->in_units('months')
    };

   my $month = 0;
   my $mon = $mm;
   my $year = $yyyy;  
   my $filename = 'zlog.txt';
  open(my $fh, '>', $filename) or die "Could not open file '$filename' $!";
  while($month <= $month_starts){
        $mon = $mon%12;
        $toMon = $mon +1;
        $toYear = $year;
        if($mon == 0){$mon = 12;$toYear++}

        my $fr = qq|$year-$mon-01|;
        my $to = qq|$toYear-$toMon-01|;
        
        $dbh->do('SET @row_index := -1');
         my $q1 = '
        SELECT AVG(subq.Progress) as MyY, subq.months as MyX
          FROM (
              SELECT @row_index:=@row_index + 1 AS row_index,';
        my $q2 = qq| Progress, DATE_FORMAT(Treatment.ContLogDate,'%Y-%m') as months
              FROM ProgNotes
                left join Treatment on Treatment.TrID=ProgNotes.NoteID
                left join Client on Client.ClientID=ProgNotes.ClientID
                left join ClientACL on ClientACL.ClientID=Client.ClientID
                left join Provider as Clinic on Clinic.ProvID=Treatment.ClinicID
                left join xSC on xSC.SCID=Treatment.SCID
                left join xInsurance on xInsurance.ID=xSC.InsID
                where Treatment.ContLogDate>="$fr" and Treatment.ContLogDate<="$to"
                and | . DBA->withNoteAccess($form,$ForProvID,'Treatment') . $addsel . qq|
                |;
        my $q3 = 'ORDER BY Progress
            ) AS subq
            WHERE subq.row_index 
            IN (FLOOR(@row_index / 2) , CEIL(@row_index / 2))';

        my $final = qq|$q1 $q2 $q3|;


      print $fh qq| .  final  $final -------  |;

          my $q = $dbh->prepare($final);
          $q->execute();
          my $rows = $q->rows;

            while ( $r = $q->fetchrow_hashref )
            {
              my $key = 'Median'; 
              my $x = $r->{'MyX'};
              my $y = $r->{'MyY'};
              $key =~ s/'//g; $x =~ s/'//g; $y =~ s/'//g;
              if($x!= ''){
              push(@{$dataset->{$key}},$x,$y); $cnt++;
              }
              # push(@{$dataset->{$key1}},$x,$y); $cnt++;
            }
            $q->finish();
        if($mon == 12){$year++;}
        $mon++;
        $month++;
  }




  my $s = qq|
      select DATE_FORMAT(Treatment.ContLogDate,'%Y-%m') as MyX, 
      ROUND(AVG(ProgNotes.Progress), 2)as MyY, 
      Treatment.ClientID
    from ProgNotes
      left join Treatment on Treatment.TrID=ProgNotes.NoteID
      left join Client on Client.ClientID=ProgNotes.ClientID
      left join ClientACL on ClientACL.ClientID=Client.ClientID
      left join Provider as Clinic on Clinic.ProvID=Treatment.ClinicID
      left join xSC on xSC.SCID=Treatment.SCID
      left join xInsurance on xInsurance.ID=xSC.InsID
    where Treatment.ContLogDate>="$form->{FromDate}" and Treatment.ContLogDate<="$form->{ToDate}"
      and | . DBA->withNoteAccess($form,$ForProvID,'Treatment') . $addsel . qq|
    GROUP by MyX|;

  print $fh $s;
  close $fh;

  my $q = $dbh->prepare($s);
  $q->execute();
  my $rows = $q->rows;
  #warn qq|q=${q}\nrows=${rows}\n|;
    while ( $r = $q->fetchrow_hashref )
    {
      my $key = 'Mean'; 
      my $key1 = 'Average'; 
      my $x = $r->{'MyX'};
      my $y = $r->{'MyY'};
      $key =~ s/'//g; $x =~ s/'//g; $y =~ s/'//g;
      push(@{$dataset->{$key}},$x,$y); $cnt++;
      # push(@{$dataset->{$key1}},$x,$y); $cnt++;
    }
    $q->finish();
    
    my $s = qq|
      select DATE_FORMAT(Treatment.ContLogDate,'%Y-%m') as MyX, 
      COUNT(ProgNotes.Progress)as MyY, 
      ProgNotes.Progress as prog
    from ProgNotes
      left join Treatment on Treatment.TrID=ProgNotes.NoteID
      left join Client on Client.ClientID=ProgNotes.ClientID
      left join ClientACL on ClientACL.ClientID=Client.ClientID
      left join Provider as Clinic on Clinic.ProvID=Treatment.ClinicID
      left join xSC on xSC.SCID=Treatment.SCID
      left join xInsurance on xInsurance.ID=xSC.InsID
    where Treatment.ContLogDate>="$form->{FromDate}" and Treatment.ContLogDate<="$form->{ToDate}"
      and | . DBA->withNoteAccess($form,$ForProvID,'Treatment') . $addsel . qq|
    GROUP by MyX, ProgNotes.Progress
    ORDER by MyX ASC|;
    my $q = $dbh->prepare($s);
    $q->execute();
    my $rows = $q->rows;
    #warn qq|q=${q}\nrows=${rows}\n|;
    my $maxExist = 0;
    my $month = '';
    my $prevMonth = '';
    my $mode = 0;
    my $index = 0;
    my $key = 'Mode';
      while ( $r = $q->fetchrow_hashref )
      {
        $key = 'Mode';
        $month = $r->{'MyX'};
        if($prevMonth eq ''){
          $prevMonth = $r->{'MyX'};
        }
        if($prevMonth ne $month){
          $maxExist = 0;
          my $x = $prevMonth;
          my $y = $mode;
          $key =~ s/'//g; $x =~ s/'//g; $y =~ s/'//g;
          push(@{$dataset->{$key}},$x,$y); $cnt++;
          $prevMonth = $r->{'MyX'};
        }
        if ($maxExist < $r->{'MyY'}){
          $mode = $r->{'prog'};
          $maxExist = $r->{'MyY'};
        }
      }
      $q->finish();
      my $x = $prevMonth;
      my $y = $mode;
      $key =~ s/'//g; $x =~ s/'//g; $y =~ s/'//g;
      push(@{$dataset->{$key}},$x,$y); $cnt++;
  my $data = graphs->setData($dataset);
  return($data);
}

sub ProgressByDatePercent
{
  my ($self,$form,$addsel) = @_;
  my $ForProvID = $form->{ForProvID} ? $form->{ForProvID} : $form->{LOGINPROVID};
  $chartname = 'stackedbar_chart';
  $xLabel = 'Progress';
  $yLabel = 'Percentage';
  $HEIGHT = 800;
  $WIDTH = 1000;
  $TITLE = qq|${ReportHeader} Progress - Percentage|;
  my $dataset = ();
  ($cnt,$dataset) = main->selProgressPercentage($form,$dataset,$addsel);
  $WIDTH = $cnt * 15 if ( $cnt > 65 );      # widen the graph is many elements.
  my $data = graphs->setData($dataset);
  return($data);
}
sub selProgressPercentage
{
  my ($self,$form,$data_array,$addsel,$byClinic) = @_;
  my $dbh = myDBI->dbconnect($form->{'DBNAME'});
  my %PROG = ();
  my %TOTAL = ();
  my ($PrevClientID,$ClientName,$ClientCount) = ('','',0);
  my ($cnt,$oDate) = (0,'');
  my $avg = 0;
  my $q = qq|
select ProgNotes.*
      ,DATE_FORMAT(Treatment.ContLogDate,'%Y-%m') as MyX
 from ProgNotes
  left join Treatment on Treatment.TrID=ProgNotes.NoteID
  left join Client on Client.ClientID=ProgNotes.ClientID
  left join ClientACL on ClientACL.ClientID=Client.ClientID
  left join Provider as Clinic on Clinic.ProvID=Treatment.ClinicID
  left join xSC on xSC.SCID=Treatment.SCID
  left join xInsurance on xInsurance.ID=xSC.InsID
 where Treatment.ContLogDate>="$form->{FromDate}" and Treatment.ContLogDate<="$form->{ToDate}"
  and | . DBA->withNoteAccess($form,$ForProvID,'Treatment') . $addsel . qq|
 order by ProgNotes.Progress|;
  my $s = $dbh->prepare($q);
if ( $form->{LOGINPROVID} == 91 )
{
  open OUT, ">>/home/okmis/mis/src/debug/graphs.out" or die "Couldn't open file: $!";
  print OUT qq|q=\n${q}\n|;
  close(OUT);
}
  $s->execute();
  my $rows = $s->rows;
#warn qq|q=${q}\nrows=${rows}\n|;
  while ( $r = $s->fetchrow_hashref )
  {
    my $key = 'none';
    if ( $r->{'Progress'} == -1 )    { $key = 'deterioration minimal'; }
    elsif ( $r->{'Progress'} == -2 ) { $key = 'deterioration  moderate'; }
    elsif ( $r->{'Progress'} == -3 ) { $key = 'deterioration   significant'; }
    elsif ( $r->{'Progress'} == 1 )  { $key = 'progress minimal'; }
    elsif ( $r->{'Progress'} == 2 )  { $key = 'progress moderate'; }
    elsif ( $r->{'Progress'} == 3 )  { $key = 'progress significant'; }
    else                             { $key = 'none'; }
    $PROG{$key}{$r->{'MyX'}}++; # {'deterioration minimal':{'Y-M': 'count(10)'}}
    $TOTAL{$r->{'MyX'}}++;
  }
  $s->finish();
  my @k = ("deterioration   significant", "deterioration  moderate", "deterioration minimal","none", "progress minimal", "progress moderate", "progress significant");

 for my $key (@k) {
#warn qq|selProgress: key=${key}\n|;
    foreach my $date ( keys %{ $PROG{$key} } )
    {
#warn qq|selProgress: key=${key}, date=${date}\n|;
      my $x = $date;
      my $y = $PROG{$key}{$date};
      my $y = $y/$TOTAL{$x} * 100;
      my $y = int($y);
      $key =~ s/'//g; $x =~ s/'//g; $y =~ s/'//g;
#warn qq|selProgress: key=${key}, x=${x}, y=${y}\n|;
#warn qq|selProgress: date=${date}, TOTAL=$TOTAL{$date}\n|;
      push(@{$data_array->{$key}},$x,$y); $cnt++;
    }
  }
  return($cnt,$data_array);
}
############################################################################
sub imsg
{
  my ($self,$msg,$id) = @_;
  return('') if ( $msg eq '' );
  my $out = qq|
  <command method="setcontent">
    <target>${id}</target>
    <content>${msg}</content>
  </command>
|;
  return($out);
}
sub iwarn
{
  my ($self,$warn,$msg,$id) = @_;
  return('') if ( $warn eq '' );
  my $out = qq|
  <command method="alert">
    <message>${warn}</message>
  </command>
|;
  $out .= main->imsg($msg,$id) if ( $id ne '' );
  return($out);
}
sub ierr
{
  my ($self,$target,$err,$msg,$id) = @_;
  my $out = qq|
  <command method="setdefault">
    <target>${target}</target>
  </command>
  <command method="alert">
    <message>${err}</message>
  </command>
  <command method="focus">
    <target>${target}</target>
  </command>
|;
  $out .= main->imsg($msg,$id) if ( $id ne '' );
  return($out);
}
############################################################################
