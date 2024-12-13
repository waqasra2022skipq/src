#!/usr/bin/perl
use lib '/home/okmis/mis/src/lib';
use CGI qw(:standard escape);
use DBI;
use myForm;
use myDBI;
use DBA;
use DBUtil;
use myHTML;
use Inv;
use cBill;
use Time::Local;
$DT=localtime();

############################################################################
#use Time::HiRes qw(time);
#$t_start=Time::HiRes::time;
#warn "ChartList   curtime: $t_start\n";
my $isEligible = 1;

my $form = myForm->new();
my $dbh = myDBI->dbconnect($form->{'DBNAME'});
myForm->pushLINK();       # save this link/page to return to.
my $addLinks = qq|mlt=$form->{mlt}&misLINKS=$form->{misLINKS}|;
my $ProviderID = $form->{'Provider_ProvID'};
$ProviderID =~ s/\D+//g;
my $ClientID = $form->{'Client_ClientID'};
$ClientID =~ s/\D+//g;
#warn qq|ClientList: ProviderID=$ProviderID, FORMProviderID=$form->{ProviderID}, LOGIN=$form->{LOGINPROVID}\n|;
my $SQLQuery = false;
############################################################################
# cross-reference tables.
##
$xref='ClinicList';
  $s=$dbh->prepare("select * from Provider where Type=3");
  $s->execute();
  while (my $r = $s->fetchrow_hashref) { $$xref{$r->{ProvID}} = $r; }
$s->finish();
##
# Selects needed.
##
my $sProvider = $dbh->prepare("select * from Provider where ProvID=?");
my $sInsurance = $dbh->prepare("select Insurance.InsIDNum, Insurance.InsID, Insurance.Copay, xInsurance.Descr, xInsurance.InsCode, xInsurance.Name, xInsurance.InsType from Insurance left join xInsurance on xInsurance.ID=Insurance.InsID where Insurance.ClientID=? and Insurance.Priority=1 and Insurance.InsNumEffDate<=curdate() and (curdate()<=Insurance.InsNumExpDate or Insurance.InsNumExpDate is NULL) order by Insurance.InsNumEffDate desc");
my $sMedicareInsurance = $dbh->prepare("select Insurance.InsIDNum, Insurance.Copay, xInsurance.Descr, xInsurance.InsCode, xInsurance.Name, xInsurance.InsType from Insurance left join xInsurance on xInsurance.ID=Insurance.InsID where Insurance.ClientID=? and xInsurance.Descr='medicare' and Insurance.InsNumEffDate<=curdate() and (curdate()<=Insurance.InsNumExpDate or Insurance.InsNumExpDate is NULL) order by Insurance.InsNumEffDate desc");
my $sTrPlan = $dbh->prepare("select * from TrPlan left join ClientPrAuth on ClientPrAuth.ID=TrPlan.PrAuthID where TrPlan.ClientID=? and ClientPrAuth.ExpDate > curdate() order by ClientPrAuth.EffDate, ClientPrAuth.ExpDate");
my $sTrPlanS = $dbh->prepare("select * from TrPlanS where TrPlanS.TrPlanID=? and TrPlanS.ProvID=?");
# first FromDate in ELigible file to test if Eligible current?
my $EBDate = DBA->EligibleDate($form);
#warn qq|EBDate=$EBDate\n|;
my $sEligible = $dbh->prepare("select * from Eligible where Eligible.ClientID=? and Eligible.Benefit=1 and Eligible.PlanDescr = ? and ('${EBDate}' between Eligible.FromDate and Eligible.ToDate)");
my $sClientReferrals = $dbh->prepare("select * from ClientReferrals where ClientID=?");
my $sClientLegal = $dbh->prepare("select * from ClientLegal where ClientID=?");
my $sClientJournals = $dbh->prepare("select * from ClientJournals where ClientID=? and Active=1");
my $sClientDischargeCDC = $dbh->prepare("select ClientID,Status,StatusDate,TransType,TransDate,TransTime from ClientDischargeCDC where ClientID=? and Status='Approved' order by StatusDate desc");

############################################################################
$ChartListByProv = '';
my $Physician = DBA->isPhysician($form);
my $TFCNotesFlag = SysAccess->verify($form,'Privilege=TFCNotes');
my $ElecNotesFlag = SysAccess->verify($form,'Privilege=ElecNotes');
my $CashTransFlag = SysAccess->verify($form,'Privilege=CashTrans');
my $Agent = SysAccess->verify($form,'Privilege=Agent');
my $ShowAmountsFlag = SysAccess->verify($form,'Privilege=ShowAmounts');

############################################################################
# Static varibles.
##
$SearchOptions = qq|&SearchType=$form->{SearchType}&SearchString=$form->{SearchString}|;
##
# some global varibles.
my ($HdrWidth,$NameWidth,$ColWidth) = ("5%","35%","20%");
my ($isDMH,$StatusColor,$InsColor) = (1,'','');
my ($PARemDays,$PAColor,$CurPAColor,$EBColor) = (0,'','','');
my ($StatusReason,$ActiveStatus,$PAStatus,$CurPAStatus) = ('','','','');
my ($rClient,$rInsurance,$rProvider,$rTrPlan,$rTrPlanS) = ('','','','','');
my ($ClientName,$ClientActiveStatus,$ClientHREF,$CustAgency,$PrimaryRef) = ('','','','','');
my ($ClinicName,$PrimaryProvName,$ClientSigned,$ProviderSigned) = ('','','','');
my ($UnitsPopup,$UnitsAvailable,$ClientDischargeStatus) = ('','','');
my ($qClient,$Title,$AddNewClientMsg,$AddNewClientHREF) = searchFor();
my ($AmtDue,$AmtDueStr,$AmtDueVal) = (0,'','');
my $printstr = qq|Client List: ${Title} ${DT}|;
my $printfile = '/tmp/pfcl_' . DBUtil->genToken() . '.html';
my $pathname = $form->{DOCROOT} . $printfile;
##
# Start out the display.
# Output the Client List part of the HTML.
##
#warn qq|\nBEGINCLIENTLIST: ProviderID=$ProviderID\n|;
my $html = myHTML->new($form) . qq|
<SCRIPT LANGUAGE="JavaScript">newtextMsg('AddNewClient','${AddNewClientMsg}');</SCRIPT>
<SCRIPT LANGUAGE="JavaScript">newtextMsg('print','Click here for a printer friendly screen to print this Client List from.');</SCRIPT>
<SCRIPT LANGUAGE="JavaScript">newtextMsg('chartlist','Click here for $rProvider->{FName} $rProvider->{LName} chart list.');</SCRIPT>
<SCRIPT LANGUAGE="JavaScript">newtextMsg('eligibility','Click here for an Eligibility list for this Client.');</SCRIPT>
<TABLE CLASS="main" >
  <TR ALIGN="center" >
| . myHTML->leftpane($form,'clock mail managertree collapseipad') . qq|
	<TD WIDTH="84%" ALIGN="center" >
| . myHTML->hdr($form) . myHTML->menu($form) . qq|
<TABLE CLASS="site fullsize" >
  <TR >
	<TD CLASS="strcol" >
	  <SPAN CLASS="header" >Client List</SPAN> <BR> 
	  ${Title}
	</TD>
	<TD CLASS="numcol" >
	  ${AddNewClientHREF}
	</TD>
  </TR>
</TABLE>

<TABLE CLASS="home fullsize" >
| . main->hdr();
#warn qq|qClient=\n$qClient\n|;
$sClient = $dbh->prepare($qClient);
$sClient->execute();
while ( $rClient = $sClient->fetchrow_hashref )
{
#warn qq|\nBEGIN: ClientID=$rClient->{ClientID}, StatusColor=$StatusColor, PAColor=$PAColor\n|;
  next if ( ! SysAccess->verify($form,'hasClientAccess',$rClient->{ClientID}) );
#warn qq|\nHAS ACCESS: ClientID=$rClient->{ClientID}\n|;
#$t_start=Time::HiRes::time;
#warn "ChartList   curtime: $t_start\n";

  $sInsurance->execute($rClient->{ClientID});
  $rInsurance = $sInsurance->fetchrow_hashref;
  $sMedicareInsurance->execute($rClient->{ClientID});
  $rMedicareInsurance = $sMedicareInsurance->fetchrow_hashref;
  $sProvider->execute($rClient->{ProvID});
  $rProvider = $sProvider->fetchrow_hashref;
  $sTrPlan->execute($rClient->{ClientID});
  $rTrPlan = $sTrPlan->fetchrow_hashref;
  $sClientLegal->execute($rClient->{ClientID});
  $rClientLegal = $sClientLegal->fetchrow_hashref;
  $sClientReferrals->execute($rClient->{ClientID});
  $rClientReferrals = $sClientReferrals->fetchrow_hashref;

  $isEligible = 1;

  ($ClientName = qq|$rClient->{LName}, $rClient->{FName} $rClient->{MName}|) =~ s/\"/&quot/g;
  $ClientName =~ s/\'//g;
  $ClientName .= ' ('.$rClient->{ClientID}.')';
  if ( $rClient->{'Active'} )
  { $ClientActiveStatus = ''; }
  else
  { $ClientActiveStatus = qq| <SPAN STYLE="color: red" >(NotActive)</SPAN><BR>|; }

  $sClientDischargeCDC->execute($rClient->{ClientID}) || myDBI->dberror("select ClientDischargeCDC $rClient->{ClientID}");
  if ( my $rClientDischargeCDC = $sClientDischargeCDC->fetchrow_hashref )
  {
	my $Active = $rClient->{'Active'} ? ' [ButActive]' : '';
	my $TransType = DBA->getxref($form,'xCDCTransTypes',$rClientDischargeCDC->{'TransType'},'Descr');
	my $TransDate = $rClientDischargeCDC->{'TransDate'} eq ''
					? 'Missing Date'
					: DBUtil->Date($rClientDischargeCDC->{'TransDate'},'fmt','MM/DD/YYYY');
	my $TransTime = substr($rClientDischargeCDC->{'TransTime'},0,5);
	my $DischargeStatus = qq|${TransType} Approved ${TransDate} ${TransTime}${Active}|;
	$ClientDischargeStatus = qq| <SPAN STYLE="color: red" >(${DischargeStatus})</SPAN><BR>|;
  } else { $ClientDischargeStatus = ''; }
  $ClientHREF = qq|/cgi/bin/ClientPage.cgi?Client_ClientID=$rClient->{ClientID}&${addLinks}|;
  $ClinicName = $rClient->{clinicClinicID} ? $ClinicList{$rClient->{clinicClinicID}}{Name} : qq|<SPAN STYLE="color: red" >NO CLINIC ASSIGNED</SPAN>|;
  $PrimaryProvName = "$rProvider->{LName}, $rProvider->{FName}";
  $CustAgency = $rClientLegal->{CustAgency} ? $rClientLegal->{CustAgency} : 'none';
  $PrimaryRef = 'none';
  if ( $rClientReferrals->{'ReferredBy1NPI'} )
  {
	my $rPriRef = DBA->selxref($form,'xNPI','NPI',$rClientReferrals->{'ReferredBy1NPI'});
	$PrimaryRef = $rPriRef->{'ProvOrgName'};
  }
  $ClientSigned = $rTrPlan->{TrPlanClSigDate};
  $ClientSigned = $ClientSigned ? DBUtil->Date($ClientSigned,'fmt','MM/DD/YYYY') : '';
  $ProviderSigned = $rTrPlan->{TrPlanPhSigDate};
  $ProviderSigned = $ProviderSigned ? DBUtil->Date($ProviderSigned,'fmt','MM/DD/YYYY') : '';

# reset all these...
  $isDMH = DBA->isDMH($form,$rClient->{ClientID});        # Client/Clinic is DMH Contract
if ( $rInsurance->{Descr} =~ /medicaid/i )
  { $StatusColor = $isDMH ? '#CC9966' : '#00CC00'; }                     # tan else green
  elsif ( $rInsurance->{Descr} eq 'medicare') { $StatusColor = '#C0C0C0'; }      # gray
  elsif ( $rInsurance->{Descr} eq 'tricare' ) { $StatusColor = '#6633CC'; }       # purple
  elsif ( $rInsurance->{Descr} eq 'bcbsok' ) { $StatusColor = '#0066FF'; }        # blue
  elsif ( $rInsurance->{Descr} eq 'bluelinc' ) { $StatusColor = '#0066FF'; }      # blue
  elsif ( $rInsurance->{Descr} eq 'healthchoice' ) { $StatusColor = '#87CEEB'; }  # skyblue

  elsif ( $rInsurance->{Descr} eq 'mcohhh' ) { $StatusColor = '#4C7838'; }     # green
  elsif ( $rInsurance->{Descr} eq 'mcookch' ) { $StatusColor = '#CB187D'; }     # pink
  elsif ( $rInsurance->{Descr} eq 'mcoaetnabhok' ) { $StatusColor = '#5B2E6F'; }     # purple
  
  elsif ( ($rInsurance->{Descr} eq 'dmhsas')  && !$SQLQuery) { $StatusColor = '#CC9966'; }        # tan if NOT 'Title 19, Expansion Health ..., Sooner Choice
  elsif ( $rInsurance->{InsType} eq 'private' ) { $StatusColor = '#FF66CC'; }     # pink
  else { $StatusColor = 'white'; $InsColor = 'black'; }
  $InsColor = $StatusColor eq 'white' ? 'black' : $StatusColor;
  ($PARemDays,$PAColor,$CurPAColor,$EBColor) = (0,'green','green','black');
  ($StatusReason,$ActiveStatus,$PAStatus,$CurPAStatus) = ('','','','');
#warn qq|call0: StatusColor=$StatusColor, PAColor=$PAColor\n|;
	if($rInsurance->{Descr} ne 'mcoaetnabhok' && $rInsurance->{Descr} ne 'mcookch' && $rInsurance->{Descr} ne 'mcohhh') {
	  ($UnitsPopup,$UnitsAvailable) = main->setInventory($rClient->{ClientID});
	}
#warn qq|call1: StatusColor=$StatusColor, PAColor=$PAColor\n|;
  $ActiveStatus = main->setEligibility();            # resets status colors
#warn qq|call2: StatusColor=$StatusColor, PAColor=$PAColor\n|;

  $AmtDue = cBill->getAmtDue($form,$rClient->{ClientID});
  $AmtDueStr = $ShowAmountsFlag ? "AmtDue all Notes: \$${AmtDue}" : $AmtDue > 0 ? "Some Notes Unpaid" : "Notes Paid";
  $AmtDueVal = $ShowAmountsFlag ? ${AmtDue} : $AmtDue > 0 ? 'Yes' : 'No';

  $html .= main->ClientList();

# now the print file...
  $ClinicName = $rClient->{clinicClinicID} ? $ClinicList{$rClient->{clinicClinicID}}{Name} : "NO CLINIC ASSIGNED";
  $printstr .= qq|
  <TR >
	<TD ALIGN="left" >$rClient->{LName}</TD>
	<TD ALIGN="left" >$rClient->{FName}</TD>
	<TD ALIGN="right" >$rClient->{ClientID}</TD>
	<TD ALIGN="left" >${PrimaryProvName}</TD>
	<TD ALIGN="left" >${ClinicName}</TD>
	<TD ALIGN="left" >$rInsurance->{Name}</TD>
	<TD ALIGN="left" >$rInsurance->{InsIDNum}</TD>
	<TD ALIGN="left" >$inv->{fPAEffDate}-$inv->{fPAExpDate}</TD>
	<TD ALIGN="left" >$inv->{fCurEffDate}-$inv->{fCurExpDate}</TD>
	<TD ALIGN="right" >${AmtDueVal}</TD>
	<TD ALIGN="left" >${ActiveStatus}</TD>
  </TR>
|;
}
$sClient->finish();
$html .= qq|
</TABLE>
| . myHTML->rightpane($form,'search');

############################################################################
# Complete the printer friendly version.
if ( open(TEMPLATE, ">$pathname") ) 
{
  print TEMPLATE qq|<HTML>
	<TABLE>
	  <TR >
		<TD ALIGN="left" >LastName</TD>
		<TD ALIGN="left" >FirstName</TD>
		<TD ALIGN="right" >ClientID</TD>
		<TD ALIGN="left" >Primary Provider</TD>
		<TD ALIGN="left" >Assigned Clinic</TD>
		<TD ALIGN="left" >Primary Insurance</TD>
		<TD ALIGN="left" >Insurance ID</TD>
		<TD ALIGN="left" >Primary PA Dates</TD>
		<TD ALIGN="left" >Current PA Dates</TD>
		<TD ALIGN="right" >AmtDue</TD>
		<TD ALIGN="left" >Active Status</TD>
	  </TR>
	  ${printstr}
	</TABLE>
	</HTML>|;
  close(TEMPLATE);
}

##
# Close the SQL statments.
##
$sProvider->finish();
$sInsurance->finish();
$sMedicareInsurance->finish();
$sTrPlan->finish();
$sTrPlanS->finish();
$sEligible->finish();
$sClientLegal->finish();
$sClientReferrals->finish();
$sClientJournals->finish();
$sClientDischargeCDC->finish();
#warn qq|ClientList html = \n$html\n|;
myDBI->cleanup();
print $html;
exit;

############################################################################
sub searchFor
{
  my ($self) = @_;
  my ($str,$hdr) = ('','');
  my $AddNewMsg = qq|New Clients can only be added from a Providers Client List, not from a Client search.  This is because the Client has to be added for a specific Provider.|;
  my $AddNewHREF = qq|    <A HREF="javascript:void(0);" ><IMG BORDER="0" SRC="/images/edit.gif" ONMOUSEOVER="textMsg.show('AddNewClient')" ONMOUSEOUT="textMsg.hide()" ></A>|;
  if ( $ProviderID )
  {
	$sProvider->execute($ProviderID);
	$rProvider = $sProvider->fetchrow_hashref;
	$hdr = "Provider: $rProvider->{FName} $rProvider->{LName}";
	$ChartListByProv = qq{<A HREF="/cgi/bin/ChartList.cgi?Provider_ProvID=${ProviderID}&SortType=Not Billed&${addLinks}" ONMOUSEOVER="textMsg.show('chartlist')" ONMOUSEOUT="textMsg.hide()" ><IMG BORDER="0" ALT="Chart-List by Provider" SRC="/images/clipboard.gif"></A>};
	if ( SysAccess->verify($form,'Privilege=NewClient') )
	{
	  $AddNewMsg = qq|Click here to add New Clients for $rProvider->{FName} $rProvider->{LName}.|;
	  $AddNewHREF = qq|
		  <A HREF=/cgi/bin/mis.cgi?view=vSSN.cgi&ProviderID=${ProviderID}&${addLinks}>
			<IMG BORDER="0" SRC="/images/edit.gif" ONMOUSEOVER="textMsg.show('AddNewClient')" ONMOUSEOUT="textMsg.hide()" >
		  </A>
		  <A HREF="javascript:ReportWindow('http://okmis.helpdocsonline.com/getting-started-2','HelpNewClient')" TITLE="Click here for Instructions on how to add a New Client" >
			<IMG SRC="/images/qm1.gif" ALT="" BORDER="0" HEIGHT="20" WIDTH="20" >
		  </A>
|;
	}
	else
	{ $AddNewMsg = qq|New Clients can be added with Data Entry Access.|; }
  
	$str = $form->{'SearchType'} eq 'ByAccess'
		 ? qq|select distinct Client.* from Client left join ClientAccess on ClientAccess.ClientID=Client.ClientID where (ClientAccess.ProvID='$ProviderID' or Client.ProvID='$ProviderID') and Client.Active=1 order by Client.LName, Client.FName|
		 : qq|select * from Client where ProvID='${ProviderID}' and Active=1 order by LName, FName|;
  }
  elsif ( $ClientID )
  {
	$hdr = qq|Client ID: ${ClientID}|;
	$str = qq|select * from Client where ClientID = '${ClientID}' order by LName, FName|;
  }
  elsif ( $form->{'SearchType'} eq 'ClientID' )
  {
	$hdr = qq|Client ID: $form->{SearchString}|;
	$str = qq|select * from Client where ClientID = '$form->{SearchString}' order by LName, FName|;
  }
  elsif ( $form->{'SearchType'} eq 'ClientSSN' )
  {
	$hdr = qq|Client SSN: $form->{SearchString}|;
	$str = qq|select * from Client where SSN = '$form->{SearchString}' order by LName, FName|;
  }
  elsif ( $form->{'SearchType'} eq 'ClientFirstName' )
  {
	($SearchStr = $form->{SearchString}) =~ s/\'//g;
	$hdr = qq|First Name: ${SearchStr}|;
	$SearchStr =~ s/\.{3}/\%/g;
	$str = qq|select * from Client where FName like '$SearchStr' order by LName, FName|;
  }
  elsif ( $form->{'SearchType'} eq 'ClientLastName' )
  {
	($SearchStr = $form->{SearchString}) =~ s/\'//g;
	$hdr = qq|Last Name: ${SearchStr}|;
	$SearchStr =~ s/\.{3}/\%/g;
	$str = qq|select * from Client where LName like '$SearchStr' order by LName, FName|;
  }
  elsif ( $form->{'SearchType'} eq 'ClientInsNum' )
  {
	($SearchStr = $form->{SearchString}) =~ s/\'//g;
	$hdr = qq|Insurance Number: ${SearchStr}|;
	$SearchStr =~ s/\.{3}/\%/g;
	my $op = $SearchStr eq $form->{SearchString} ? '=' : 'like';
	$str = qq|select distinct Client.* from Client left join Insurance on Insurance.ClientID=Client.ClientID where Insurance.InsIDNum ${op} '$SearchStr' and Insurance.InsNumEffDate<=curdate() and (curdate()<=Insurance.InsNumExpDate or Insurance.InsNumExpDate is NULL) order by Client.LName, Client.FName|;
  }
  else
  { myDBI->error("Client List / Access Denied"); }
  return($str,$hdr,$AddNewMsg,$AddNewHREF);
}
############################################################################
# This subroutine outputs the HTML for each Client Line.
sub ClientList
{
  my ($self) = @_;
  my $ElecNotesLink .= qq|<A HREF="/cgi/bin/mis.cgi?MIS_Action=Note&NoteType=3&Client_ClientID=$rClient->{ClientID}&Client_ClinicID=$rClient->{clinicClinicID}&Treatment_TrID=new&${addLinks}" > <IMG BORDER="0" HEIGHT="15" WIDTH="15" ALT="Electronic Note Entry" SRC="/images/lightning.gif"> </A> | if ( $ElecNotesFlag );
  my $TFCNotesLink = qq|<A HREF="/cgi/bin/mis.cgi?MIS_Action=Note&NoteType=tfc&Client_ClientID=$rClient->{ClientID}&Treatment_TrID=new&${addLinks}" > <IMG BORDER="0" HEIGHT="15" WIDTH="15" ALT="TFC Note Entry" SRC="/images/homeicon.gif"> </A> | if ( $TFCNotesFlag );
  my $pblink = $rInsurance->{Copay} > 0 ? qq|CLASS="blink-image"| : '';
  my $CashTransLink = qq|<A HREF="/cgi/bin/ListInsPaid.cgi?Client_ClientID=$rClient->{ClientID}&${addLinks}" ><IMG ${pblink} BORDER="0" HEIGHT="15" WIDTH="15" ALT="Insurance Payments Entry" SRC="/images/piggybank.gif"></A> | if ( $CashTransFlag );
  my $PhysNotesLink = qq|<A HREF="/cgi/bin/mis.cgi?MIS_Action=Note&NoteType=2&Client_ClientID=$rClient->{ClientID}&Treatment_TrID=new&${addLinks}" > <IMG SRC="/cgi/images/caduceusblack.png" WIDTH="24" HEIGHT="24" > </A> | if ( ${Physician} );
  my $MedicareLink = qq|<A HREF="/cgi/bin/mis.cgi?MIS_Action=Note&NoteType=4&Client_ClientID=$rClient->{ClientID}&Treatment_TrID=new&${addLinks}" > <IMG SRC="/img/note_medicare.png" WIDTH="24" HEIGHT="24" > </A> | if ( $rMedicareInsurance->{'Descr'} ne '' );
  my $InvPrintLink .= qq|<A HREF="/cgi/bin/mis.cgi?view=ListInvoices.cgi&Client_ClientID=$rClient->{ClientID}&${addLinks}" > <IMG BORDER="0" ALT="List Client Invoices" SRC="/images/invoice.gif"> </A> | if ( SysAccess->verify($form,'Privilege=Invoices2Print') );
  my $checkEB = $rInsurance->{'Descr'} =~ /medicaid/i ? qq|<BR><button STYLE="font-size:0.5em;" CLASS="confirmLINK" MYTEXT="Are you sure you want to check Eligibility?<BR>If so, then click the OK button below. If NOT, click the Cancel button below.<BR><BR>Eligibility information is obtained nightly through extracts from OHCA. Providers should keep in mind the following:<BR>ODMHSAS added this check onto its service as a way to help providers in giving them a quick idea of eligibility for the new Case Management rules.<BR>This is just a marker and is only what ODMHSAS has at the moment, ODMHSAS does not have live access to recipient eligibility.<BR>This is NOT a guarantee of payment and should not replace your checking OHCA for eligibility (MIS checks twice a month).<BR>As with any data extract, things can happen so this should be more of an helpful indicator for providers, not something you rely on." HREF="/cgi/bin/mis.cgi?MIS_Action=DMHcm.pl&Provider_ProvID=${ProviderID}&Client_ClientID=$rClient->{ClientID}&InsNumIDs=$rInsurance->{InsIDNum}&mlt=$form->{mlt}" MYBUSY="Checking..." >Check DMH</button>&nbsp;<A HREF="javascript: ReportWindow('/cgi/bin/EBDMH.cgi?ClientID=$rClient->{ClientID}&InsNumID=$rInsurance->{InsIDNum}&FName=$rClient->{FName}&LName=$rClient->{LName}&mlt=$form->{mlt}','EBDMH',400,1200)" TITLE="Click to view last DMH Eligibility Report"  ><SPAN CLASS="subtitle" >Last DMH Eligibility check</SPAN></A> | : '';
#warn qq|checkEB=${checkEB}\n|;
  $sClientJournals->execute($rClient->{ClientID}) || myDBI->dberror("select ClientJournals $rClient->{ClientID}");
  my $rClientJournals = $sClientJournals->fetchrow_hashref;
  my $jblink = $sClientJournals->rows() > 0 ? qq|CLASS="blink-image"| : '';
  my $HealthHomeImg = $rInsurance->{'Descr'} =~ /healthhome/i ?qq|<IMG BORDER="0" HEIGHT="15" WIDTH="15" ALT="HealthHome" SRC="/images/homeicon.gif">| : '';
  (my $ws = qq|$rClient->{FName} $rClient->{MName} $rClient->{LName} ($rClient->{ClientID})|) =~ s/\"//g;
my ($Found,$str,$Renew) = main->chkEligibility(1,0,$rInsurance->{InsCode});
  $StatusColor = $InsColor;
  if($rInsurance->{InsID} ne '451' && $rInsurance->{InsID} ne '452' && $rInsurance->{InsID} ne '453') {
	  if ( !$Founnd ) {
	   # $StatusColor = 'red'; 
	  }	
  } else {
  	$StatusReason = '';
  }

  if(!$isEligible) {
    $StatusColor = 'Red';
  }
  
  $ws =~ s/\'//g;
#foreach my $f ( sort keys %{ $rInsurance } ) { warn "  sub ClientList: rInsurance-${f} is $rInsurance->{$f}\n"; }
  my $str = qq|
${UnitsPopup}
  <TR >
	<TD STYLE="background-color: ${StatusColor}" WIDTH="${HdrWidth}" ROWSPAN="3" >
	  <A HREF="/cgi/bin/mis.cgi?MIS_Action=Note&Client_ClientID=$rClient->{ClientID}&Treatment_TrID=new&${addLinks}" > <IMG BORDER="0" ALT="General Chart Entry" SRC="/images/facesicon.gif"> </A>
	  <A HREF="/cgi/bin/ChartList.cgi?Client_ClientID=$rClient->{ClientID}&SortType=NotReconciled&${addLinks}" > <IMG BORDER="0" HEIGHT="15" WIDTH="15" ALT="Chart List by Client" SRC="/images/clipboard.gif"> </A>
	  <A HREF="/cgi/bin/mis.cgi?view=ListClientJournals.cgi&Client_ClientID=$rClient->{ClientID}&${addLinks}"> <IMG ${jblink} BORDER="0" HEIGHT="15" WIDTH="15" ALT="Journal List by Client" SRC="/images/journal.gif"> </A>
	  ${MedicareLink}
	  ${ElecNotesLink}
	  ${TFCNotesLink}
	  ${PhysNotesLink}
	  ${CashTransLink}
	  ${InvPrintLink}
	  <A HREF="javascript: ReportWindow('/cgi/bin/ClientSC.cgi?ClientID=$rClient->{ClientID}&mlt=$form->{mlt}','ClientSC',600,1100)" > <IMG BORDER="0" ALT="Service Codes for Clients Insurance" SRC="/images/paper.gif" > </A>
	</TD>
	<TD CLASS="strcol" WIDTH="${NameWidth}" >
		<A HREF="${ClientHREF}" ONMOUSEOVER="window.status='${ws}'; return true;" ONMOUSEOUT="window.status=''" >${ClientName}</A> / ${ClinicName} <BR> ${ClientActiveStatus}
		${PrimaryProvName} &nbsp; <BR>
		${CustAgency} / ${PrimaryRef} &nbsp; <BR>
		${AmtDueStr} &nbsp;
	</TD>
	<TD CLASS="strcol" WIDTH="${ColWidth}" >
	  ${ClientSigned} &nbsp; <BR>
	  ${ProviderSigned} &nbsp; <BR>
	</TD>
	<TD CLASS="strcol" WIDTH="${ColWidth}" VALIGN="top" >
	  <SPAN CLASS="subtitle" STYLE="color: ${InsColor}" >$rInsurance->{Name} &nbsp; </SPAN> ${HealthHomeImg}<BR>
	  $rInsurance->{InsIDNum} &nbsp; <BR>
	  <A HREF="javascript: ReportWindow('/cgi/bin/EBReport.cgi?ClientID=$rClient->{ClientID}&FName=$rClient->{FName}&LName=$rClient->{LName}&mlt=$form->{mlt}','EBReport',400,1200)" ONMOUSEOVER="textMsg.show('eligibility')" ONMOUSEOUT="textMsg.hide()" ><SPAN CLASS="subtitle" STYLE='color:${EBColor}' >${ActiveStatus}</SPAN></A>
	  ${checkEB}
	</TD>
  </TR>
  <TR >
	<TD CLASS="strcol" COLSPAN="3" > 
	  <SPAN CLASS="subtitle" >${UnitsAvailable} &nbsp; <BR>${ClientDischargeStatus}</SPAN>
	</TD>
  </TR>
  <TR >
	<TD CLASS="strcol" COLSPAN="3" > 
	  <SPAN CLASS="subtitle" STYLE="color: red" >${StatusReason} &nbsp;</SPAN>
	</TD>
  </TR>
|;
  return($str);
}
############################################################################
sub hdr
{
  my ($self) = @_;
  my $out = qq|
  <TR >
	<TD CLASS="port" WIDTH="$HdrWidth" ROWSPAN="3" >
	  <A HREF="javascript:ReportWindow('${printfile}','PrintWindow')" ONMOUSEOVER="textMsg.show('print')" ONMOUSEOUT="textMsg.hide()" ><IMG BORDER="0" SRC="/images/icon_print.gif" ></A>
	  &nbsp;${ChartListByProv}&nbsp;
	</TD>
	<TD CLASS="strcol" WIDTH="${NameWidth}" >
	  <B>Client Name (#) / Clinic</B><BR>
	  <B>Primary Provider</B><BR>
	  <B>Custody Agency / Referral</B>
	</TD>
	<TD CLASS="strcol" WIDTH="${ColWidth}" >
	  <B>Client Signed</B><BR>
	  <B>Physician Signed</B>
	</TD>
	<TD CLASS="strcol" WIDTH="${ColWidth}" >
	  <B>Insurance Type</B><BR>
	  <B>Insurance Num</B><BR>
	  <B>Eligibility</B>
	  <A HREF="javascript:ReportWindow('http://forms.okmis.com/misdocs/Eligible.htm','HelpWindow')" ><IMG BORDER="0" WIDTH="20" HEIGHT="20" SRC="/images/qm1.gif" ></A>
	</TD>
  </TR>
  <TR >
	<TD CLASS="strcol" COLSPAN="3" >
	  <B>Prior Authorizations: Auth Period: Auth #: Current Period: Inventory and Service Codes</B>
	</TD>
  </TR>
  <TR >
	<TD CLASS="strcol" COLSPAN="3" >
	  <B>Status<B>
	</TD>
  </TR>
|;
  return($out);
}

sub setEligibility
{
  my ($self) = @_;
  my ($Found,$str) = (0,'');
  # Insurance is DMH contract...
  #warn qq|setEligible: $rInsurance->{InsCode}, isDMH=$isDMH\n|;
  if ( $rInsurance->{InsCode} eq 'MC' )
  {
	
	# Check for PlanDesrc = 'Expansion Healthy Adult Program' is same as 'Title 19'
	my ($EHAP,$EHAPstr,$RenewEHAP) = main->chkEligibility(1,1,$rInsurance->{InsCode},'Expansion Healthy Adult Program');

	# Check for PlanDesrc = 'SoonerCare Choice' is same as 'Title 19'
	my ($SCC,$SCCstr,$RenewSCC) = main->chkEligibility(1,1,$rInsurance->{InsCode},'SoonerCare Choice');

	my ($Title19,$Title19str,$Renew) = main->chkEligibility(1,1,$rInsurance->{InsCode},'Title 19');

	$SQLQuery = ($Title19 || $EHAP || $SCC);
	
	$EBColor = 'orange' unless ( $Renew eq '' );
	my ($MHSA,$MHSAstr,$Renew) = main->chkEligibility(1,1,$rInsurance->{InsCode},'Mental Health and Substance Abuse');
	$EBColor = 'orange' unless ( $Renew eq '' );
	if ( ($Title19 || $EHAP || $SCC) && $MHSA )             # T19, Expansion Healthy Adult Program and MHSA eligibility, 
	{ 
	  $str = $Title19str . $EHAPstr . ' ' .$SCCstr; # . ' isDMH-' . $isDMH .' - '.$rInsurance->{Descr}.' '.$InsColor; 
		# $StatusColor = '#00CC00';  # Set color Green
		$InsColor = '#00CC00';  # Set color Green
		$EBColor = '#00CC00';
	}
	elsif ( ($Title19 || $EHAP || $SCC) && $isDMH )         # T19 and has DMH contract
	{ $str = $Title19str; $StatusReason .= ' no MH and SA Insurance'; }
	elsif ( $Title19 || $EHAP || $SCC)
	{ $str = $Title19str . $EHAPstr . ' ' .$SCCstr; }
	elsif ( $MHSA && $isDMH )            # MHSA eligibility and has DMH contract
	{ $str = $MHSAstr; $StatusReason .= ' Insurance not Title 19'; }
	elsif ( $MHSA )                      # MHSA eligibility (Title 19 contract)
	{ $str = $MHSAstr; $StatusReason .= ' Insurance not Title 19'; $StatusColor = 'red'; if ( $SQLQuery ) { $StatusColor = '#00CC00'; }}
	$Found = $str eq '' ? 0 : 1;

  }
  elsif ( $rInsurance->{InsCode} eq 'MB' )
  { ($Found,$str,$Renew) = main->chkEligibility(1,1,$rInsurance->{InsCode},'Medicare Part B'); }
  else { ($Found,$str,$Renew) = main->chkEligibility(1,1,$rInsurance->{InsCode}); }

  if ( !$Found )                                        # did not find primary insurance this month
  {
	$StatusColor = 'red' if ( $rInsurance->{InsCode} eq 'MC' || $rInsurance->{InsCode} eq 'MB' );
	($Found,$str,$Renew) = main->chkEligibility(1,0,$rInsurance->{InsCode}); # any date primary insurance
	if ( $Found ) { $StatusReason .= ' Eligibility Expired for Primary Ins '; $EBColor = 'red';$StatusColor = 'red'; }
	else
	{ 
	  ($Found,$str,$Renew) = main->chkEligibility(1,1);                      # this date any insurance
	  if ( $Found ) { $StatusReason .= ' Eligibility Not Primary Ins'; }
	  else
	  { 
		$StatusReason .= ' Eligibility not found.'; $EBColor = 'red';
		($Found,$str,$Renew) = main->chkEligibility(0,0);
		if ( $str eq '' ) { $str = ': none '; }
	  }
	}
  }
	#  $ActiveStatus = qq|$rEligible->{InsCode}: $rEligible->{Descr} ${EBDates}|;
  if($str =~ /Mental Health and Substance Abuse/i) {
		$EBColor = '#a0522d';
		$InsColor = '#CC9966';
  }elsif($str =~ /Expansion Healthy Adult Program/i) {
		$EBColor = '#00CC00';
  }
  return($str);
}

sub chkEligibility
{
  my ($self,$Active,$today,$code,$desc) = @_;
  

  my ($flag,$str,$renewdate) = (0,'','');
  my $qEligible = qq|select * from Eligible where Eligible.ClientID='$rClient->{ClientID}' and Eligible.Benefit=${Active}|;
  $qEligible .= qq| and ('${EBDate}' between Eligible.FromDate and Eligible.ToDate)| if ( $today );
  $qEligible .= qq| and Eligible.InsCode = '${code}'| if ( $code );
  $qEligible .= qq| and Eligible.PlanDescr = '${desc}'| if ( $desc );
  $qEligible .= qq| order by Eligible.FromDate desc, Eligible.ToDate desc|;
	#$SQLQuery .= $qEligible;
	#warn qq|qEligible=$qEligible\n|;
  $sEligible = $dbh->prepare($qEligible);
  $sEligible->execute();
  if ( $rEligible = $sEligible->fetchrow_hashref )
  {
	$flag = 1;
	$EBDates = DBUtil->Date($rEligible->{FromDate},'fmt','MM/DD/YYYY') . '-' . DBUtil->Date($rEligible->{ToDate},'fmt','MM/DD/YYYY'); 
	$str .= qq|Expired: | unless ( $today );
	$str .= qq|$rEligible->{InsCode}: $rEligible->{PlanDescr} ${EBDates}|;
	$renewdate = $rEligible->{'RenewDate'};
  }
  return($flag,$str,$renewdate);
}
sub setInventory
{
  my ($self,$ClientID) = @_;
  my ($POPUP,$HREF,$CNT) = ('','',0);
  my $dbh = myDBI->dbconnect($form->{'DBNAME'});
#warn qq|setInventory: ClientID=$ClientID\n|;
  my $q=qq|select ClientPrAuth.*,ClientPrAuthCDC.Reason,Insurance.Priority,Insurance.InsID from ClientPrAuth left join ClientPrAuthCDC on ClientPrAuthCDC.ClientPrAuthID=ClientPrAuth.ID left join Insurance on Insurance.InsNumID=ClientPrAuth.InsuranceID where ClientPrAuth.ClientID=? and ClientPrAuthCDC.TransType < 60 and (ClientPrAuthCDC.Status != 'Closed' or ClientPrAuthCDC.Status is NULL) and ( ('$form->{TODAY}' between ClientPrAuth.Effdate and ClientPrAuth.ExpDate) or ClientPrAuth.EffDate>='$form->{TODAY}' ) order by Insurance.Priority, ClientPrAuth.EffDate|;
  my $s = $dbh->prepare($q);
#warn qq|setInventory: q=$q\n|;
  $s->execute($ClientID) || myDBI->dberror($q);
  while ( my $r = $s->fetchrow_hashref )
  {
	$CNT++;
#warn qq|CNT=$CNT, DOB=$rClient->{DOB},ProvID=$rClient->{ProvID},ClinicID=$rClient->{clinicClinicID}\n|;
	my $PrAuthID = $r->{ID};
#warn qq|ClientList: CNT=$CNT, PrAuthID=${PrAuthID}, PAnumber=$r->{PAnumber}\n|;
	my $inv=Inv->InvPA($form,$r);
#warn "\n: check1=$inv->{PAgroup}\n";
	$inv=$inv->InvNotes($form,$r->{ClientID},$r->{InsID});
#foreach my $f ( sort keys %{ $inv } ) { warn "  main: inv-${f} is $inv->{$f}\n"; }
	main->setPA($inv,$r->{Priority});                    # sets status colors
	if ( $rInsurance->{Descr} =~ /medicaid/i
	  && $inv->{'PAgroup'} =~ /PG046|PG047|PG048|PG049/ )
	{ $StatusColor = '#99FF66'; }         # light green with Rehab
	if ( $r->{'Reason'} ne '' )
	{
	  if ( $r->{'NotificationType'} == 1
		|| $r->{'NotificationType'} == 2
		|| $r->{'NotificationType'} == 3
		|| $r->{'NotificationType'} == 5
		|| $r->{'NotificationType'} == 6
		|| $r->{'NotificationType'} == 8
		|| $r->{'NotificationType'} == 11
		|| $r->{'NotificationType'} == 12
		|| $r->{'NotificationType'} == 13
		|| $r->{'NotificationType'} == 14 )
	  {
		$StatusColor = 'yellow';
	  }
	  $StatusReason .= " $r->{'Reason'} ";
	}
#warn "\n: ClientID: $r->{ClientID}, D=$r->{EffDate}/$r->{ExpDate},$r->{NotificationType},$r->{Reason}\n";

# first the entire period of the PA...
#foreach my $f ( sort keys %{ $inv } ) { warn "  main: inv-${f} is $inv->{$f}\n"; }
	my $UnitsAuth = sprintf("%.2f",$inv->{UnitsAuth});
	my $UnitsUsed = sprintf("%.2f",$inv->{UnitsUsed});
	my $UnitsLeft = sprintf("%.2f",$inv->{UnitsAuth} - $inv->{UnitsUsed});
	my $AmtAuth = sprintf("%.2f",$inv->{AmtAuth});
	my $AmtUsed = sprintf("%.2f",$inv->{AmtUsed});
	my $AmtLeft = sprintf("%.2f",$inv->{AmtAuth} - $inv->{AmtUsed});
	my $PctLeft = $AmtAuth > 0 ?  sprintf("%.1f",(($AmtLeft / $AmtAuth) * 100)) : '0.0';
	my $HealthHome = $inv->{'InsDescr'} =~ /healthhome/i ? qq|<SPAN STYLE="color: green" >Health Home</SPAN>| : '';
	my $HealthHomeImg = $inv->{'InsDescr'} =~ /healthhome/i ?qq|<IMG BORDER="0" HEIGHT="15" WIDTH="15" ALT="HealthHome" SRC="/images/homeicon.gif"><SPAN STYLE="color: green" >Health Home| : '';
	my $text = qq|<BR>${HealthHomeImg} $inv->{'PAgroup'} <A HREF="javascript: ReportWindow('/cgi/bin/PAPeriods.cgi?IDs=${PrAuthID}&mlt=$form->{mlt}','PAPeriods',600,1100)" ONMOUSEOVER="textMsg.show('pa${ClientID}_${PrAuthID}')" ONMOUSEOUT="textMsg.hide()" ><SPAN STYLE="color: ${PAColor}" >$r->{Priority}-$inv->{InsDescr}: $inv->{fPAEffDate}-$inv->{fPAExpDate}: $inv->{PAnumber}: |;
	my $Length1 = DBA->getxref($form,'xPAgroups',$inv->{'PAgroup'},'Length1');
	$Length1 = 'month' if ( $Length1 eq '' );
	my $popmsg = qq|$inv->{LOS} ${Length1}s Inventory $inv->{PAgroup}|;
	if ( $UnitsAuth > 0 )
	{ $popmsg .= qq|$inv->{AUTHLIST}<BR>${UnitsAuth} - ${UnitsUsed} = ${UnitsLeft} left |; }
	elsif ( $AmtLeft == 0 && $ShowAmountsFlag )
	{ $popmsg .= qq|<BR>&#36;${AmtAuth} - &#36;${AmtUsed} = &#36;${AmtLeft} left (${PctLeft}&#37;) |; }
	elsif ( $AmtLeft == 0 )
	{ $popmsg .= qq|<BR>Nothing left (${PctLeft}&#37;) |; }
	elsif ( $ShowAmountsFlag )
	{ $popmsg .= qq|<BR>&#36;${AmtAuth} - &#36;${AmtUsed} = &#36;${AmtLeft} left (${PctLeft}&#37;) |; }
	else
	{ $popmsg .= qq|<BR>(${PctLeft}&#37; left)|; }
	$popmsg .= qq|<BR>${PAStatus}|;
	$POPUP .= qq|<SCRIPT LANGUAGE="JavaScript">newtextMsg('pa${ClientID}_${PrAuthID}','${popmsg}');</SCRIPT>\n|;
	$HREF .= qq|${text}</SPAN></A>|;

# now the current/monthly period of the PA...
	my $CurPeriod = $inv->{CurPeriod};
	next if ( $CurPeriod eq '-' || $CurPeriod eq '' );   # skip if '-' or FUTURE PA.
	my $INPA = scalar keys %{ $inv->{$CurPeriod}->{INPA} };
	my $NONPA = scalar keys %{ $inv->{$CurPeriod}->{NONPA} };
	next if ( $r->{PAnumber} eq '' && $INPA == 0 && $NONPA == 0 );    # skip status bar if NOT APPROVED

#warn qq|setInventory: PPACnt=$inv->{PPACnt}, Status=$StatusColor, $StatusReason\n|;
#warn qq|setInventory: PrAuthID=$PrAuthID, InsDescr=$inv->{InsDescr}, CurPeriod=$CurPeriod\n|;
#foreach my $f ( sort keys %{$inv->{$CurPeriod}} ) { warn "  main: inv-${CurPeriod}-${f} is $inv->{$CurPeriod}->{$f}\n"; }
#warn qq|setInventory: UnitsAuth=$inv->{$CurPeriod}->{UnitsAuth}, UnitsUsed=$inv->{$CurPeriod}->{UnitsUsed}\n|;
#warn qq|setInventory: AmtAuth=$inv->{$CurPeriod}->{AmtAuth}, AmtUsed=$inv->{$CurPeriod}->{AmtUsed}\n|;
	$UnitsAuth = sprintf("%.2f",$inv->{$CurPeriod}->{UnitsAuth});
	$UnitsUsed = sprintf("%.2f",$inv->{$CurPeriod}->{UnitsUsed});
	$UnitsLeft = sprintf("%.2f",$inv->{$CurPeriod}->{UnitsAuth} - $inv->{$CurPeriod}->{UnitsUsed});
	$AmtAuth = sprintf("%.2f",$inv->{$CurPeriod}->{AmtAuth});
	$AmtUsed = sprintf("%.2f",$inv->{$CurPeriod}->{AmtUsed});
	$AmtLeft = sprintf("%.2f",$inv->{$CurPeriod}->{AmtAuth} - $inv->{$CurPeriod}->{AmtUsed});
	$PctLeft = $AmtAuth > 0 ?  sprintf("%.1f",(($AmtLeft / $AmtAuth) * 100)) : '0.0';
#warn qq|setInventory: UnitsAuth=$UnitsAuth, UnitsUsed=$UnitsUsed, UnitsLeft=$UnitsLeft\n|;
#warn qq|setInventory: AmtAuth=$AmtAuth, AmtUsed=$AmtUsed, AmtLeft=$AmtLeft\n|;
#warn qq|setInventory: PctLeft=$PctLeft\n|;
	my $text = qq|<A HREF="javascript:void(0);" ONMOUSEOVER="textMsg.show('curpa${ClientID}_${PrAuthID}')" ONMOUSEOUT="textMsg.hide()" ><SPAN STYLE="color: ${CurPAColor}" >${CurPeriod}: |;
	my $popmsg = qq|Current Inventory|;
#warn qq|setInventory: PAgroup=$inv->{'PAgroup'}\n|;
	if ( $UnitsAuth > 0 )
	{ $text .= qq|${UnitsLeft} unitsleft |; $popmsg .= qq|<BR>${UnitsAuth} - ${UnitsUsed} = ${UnitsLeft} left |; }
	elsif ( $AmtLeft == 0 && $ShowAmountsFlag )
	{ $text .= qq|(${PctLeft}&#37; left) |; $popmsg .= qq|<BR>&#36;${AmtAuth} - &#36;${AmtUsed} = &#36;${AmtLeft} left (${PctLeft}&#37;) |; }
	elsif ( $AmtLeft == 0 )
	{ $text .= qq|zero left (${PctLeft}&#37;) |; $popmsg .= qq|<BR>Nothing left (${PctLeft}&#37;) |; }
	elsif ( $ShowAmountsFlag )
	{ $text .= qq|&#36;${AmtLeft} left (${PctLeft}&#37;) |; $popmsg .= qq|<BR>&#36;${AmtAuth} - &#36;${AmtUsed} = &#36;${AmtLeft} left (${PctLeft}&#37;) |; }
	else
	{ $text .= qq|(${PctLeft}&#37; left) |; $popmsg .= qq|<BR>(${PctLeft}&#37; left)|; }
	$HREF .= qq|${text}</SPAN></A>|;
	$popmsg .= qq|<BR>${CurPAStatus}|;
	$POPUP .= qq|<SCRIPT LANGUAGE="JavaScript">newtextMsg('curpa${ClientID}_${PrAuthID}','${popmsg}');</SCRIPT>\n|;
	next if ( $form->{'DBNAME'} eq 'okmis_anv' );
	foreach my $SCID ( sort keys %{ $inv->{$CurPeriod}->{INPA} } )
	{
	  my $SCNum = DBA->getxref($form,'xSC',$SCID,'SCNum');
	  next if ( $SCNum =~ /H2017/ );      # Rehab services...
	  my $UNITS = $inv->{$CurPeriod}->{$SCID}->{UNITS};
	  # check inventory required or getting low on inventory.
	  my ($Redpfx, $Redsfx) = ('','');
	  if ( $inv->{$SCID}->{UnitsAuth} > 0 )
	  {
		my $Type = DBA->getxref($form,'xSC',$SCID,'Type');
		my $PAReq = DBA->getxref($form,'xSC',$SCID,'PAReq');
		my $min = $Type eq 'TP' ? 0 : 1;
		my $UnitsLeft = sprintf("%.2f",$inv->{$SCID}->{UnitsAuth} - $inv->{$SCID}->{UnitsUsed});
		if ( $PAReq && $UnitsLeft <= $min )
		{ ($Redpfx, $Redsfx) = ('<FONT COLOR=red >','</FONT>'); }
	  }
	  my $popmsg = qq|INPA<BR>TrID  ContactDate  Units  Amount<BR>$inv->{$CurPeriod}->{$SCID}->{LIST} Total: ${UNITS} |;
	  $popmsg .= qq|$inv->{$CurPeriod}->{$SCID}->{AMT} | if ( $ShowAmountsFlag );
	  $POPUP .= qq|<SCRIPT LANGUAGE="JavaScript">newtextMsg('scid${ClientID}_${PrAuthID}_${SCID}','${popmsg}');</SCRIPT>\n|;
	  my $id = $Agent ? qq|[${SCID}]| : '';
	  $HREF .= qq|    <A HREF="javascript:void(0);" ONMOUSEOVER="textMsg.show('scid${ClientID}_${PrAuthID}_${SCID}')" ONMOUSEOUT="textMsg.hide()" >${Redpfx} $inv->{$CurPeriod}->{INPA}->{$SCID} ${id} ${Redsfx}</A>|;
	}
	foreach my $H2017 ( sort keys %{ $inv->{$CurPeriod}->{INPAH2017} } )
	{
	  my $UNITS = $inv->{$CurPeriod}->{H2017}->{UNITS};
	  # check inventory required or getting low on inventory.
	  my ($Redpfx, $Redsfx) = ('','');
	  if ( $inv->{'PAgroup'} =~ /PG002|PG042/ && $UNITS > 32 )       # Level 1
	  { ($Redpfx, $Redsfx) = ('<FONT COLOR=red >','</FONT>'); }
	  elsif ( $inv->{'PAgroup'} =~ /PG003|PG043/ && $UNITS > 48 )    # Level 2
	  { ($Redpfx, $Redsfx) = ('<FONT COLOR=red >','</FONT>'); }
	  elsif ( $inv->{'PAgroup'} =~ /PG004|PG044/ && $UNITS > 64 )    # Level 3
	  { ($Redpfx, $Redsfx) = ('<FONT COLOR=red >','</FONT>'); }
	  my $popmsg = qq|INPA<BR>TrID  ServiceCode  ContactDate  Units  Amount<BR>$inv->{$CurPeriod}->{H2017}->{LIST} Total: ${UNITS} |;
	  $popmsg .= qq|$inv->{$CurPeriod}->{H2017}->{AMT} | if ( $ShowAmountsFlag );
	  $POPUP .= qq|<SCRIPT LANGUAGE="JavaScript">newtextMsg('scid${ClientID}_${PrAuthID}_H2017','${popmsg}');</SCRIPT>\n|;
	  $HREF .= qq|    <A HREF="javascript:void(0);" ONMOUSEOVER="textMsg.show('scid${ClientID}_${PrAuthID}_H2017')" ONMOUSEOUT="textMsg.hide()" >${Redpfx} $inv->{$CurPeriod}->{INPAH2017}->{$H2017} [combined] ${Redsfx}</A>|;
	}
	foreach my $SCID ( sort keys %{ $inv->{$CurPeriod}->{NONPA} } )
	{
	  # Non PA Service Codes are always red.
	  my ($Redpfx, $Redsfx) = ('<FONT COLOR=red >','</FONT>');
	  my $popmsg = qq|NONPA<BR>TrID  ContactDate  Units  Amount<BR>$inv->{$CurPeriod}->{$SCID}->{LIST} Total: $inv->{$CurPeriod}->{$SCID}->{UNITS} |;
	  $popmsg .= qq|$inv->{$CurPeriod}->{$SCID}->{AMT} | if ( $ShowAmountsFlag );
	  $POPUP .= qq|<SCRIPT LANGUAGE="JavaScript">newtextMsg('scid${ClientID}_${PrAuthID}_${SCID}','${popmsg}');</SCRIPT>\n|;
	  my $id = $Agent ? qq|[${SCID}]| : '';
	  $HREF .= qq|    <A HREF="javascript:void(0);" ONMOUSEOVER="textMsg.show('scid${ClientID}_${PrAuthID}_${SCID}')" ONMOUSEOUT="textMsg.hide()" >${Redpfx} $inv->{$CurPeriod}->{NONPA}->{$SCID} ${id} ${Redsfx}</A>|;
	}
	foreach my $F2F ( sort keys %{ $inv->{$CurPeriod}->{INPAF2F} } )
	{
	  my $UNITS = $inv->{$CurPeriod}->{F2F}->{UNITS};
	  # check inventory required or getting low on inventory.
	  my ($Redpfx, $Redsfx) = ('<FONT COLOR=red >','</FONT>');
	  if ( $inv->{'PAgroup'} =~ /G9002/ && $UNITS > 0 )       # Adult Moderate
	  { ($Redpfx, $Redsfx) = ('<FONT COLOR=green >','</FONT>'); }
	  elsif ( $inv->{'PAgroup'} =~ /G9005/ && $UNITS > 1 )    # Adult High
	  { ($Redpfx, $Redsfx) = ('<FONT COLOR=green >','</FONT>'); }
	  elsif ( $inv->{'PAgroup'} =~ /G9009/ && $UNITS > 2 )    # Child Moderate
	  { ($Redpfx, $Redsfx) = ('<FONT COLOR=green >','</FONT>'); }
	  elsif ( $inv->{'PAgroup'} =~ /G9010/ && $UNITS > 4 )    # Child High
	  { ($Redpfx, $Redsfx) = ('<FONT COLOR=green >','</FONT>'); }
	  my $popmsg = qq|INPA<BR>TrID  ServiceCode  ContactDate  Units  Amount<BR>$inv->{$CurPeriod}->{F2F}->{LIST} Total: ${UNITS} |;
	  $popmsg .= qq|$inv->{$CurPeriod}->{F2F}->{AMT} | if ( $ShowAmountsFlag );
	  $POPUP .= qq|<SCRIPT LANGUAGE="JavaScript">newtextMsg('scid${ClientID}_${PrAuthID}_F2F','${popmsg}');</SCRIPT>\n|;
	  $HREF .= qq|    <A HREF="javascript:void(0);" ONMOUSEOVER="textMsg.show('scid${ClientID}_${PrAuthID}_F2F')" ONMOUSEOUT="textMsg.hide()" >${Redpfx} $inv->{$CurPeriod}->{INPAF2F}->{$F2F} [combined] ${Redsfx}</A>|;
	}
  }
  if ( $CNT == 0 )
  {
	$StatusColor = 'red'; $StatusReason .= ' No Primary PA ';
	$PAColor = "red"; $PAStatus = "No PA found!";
  }
  elsif ( $PARemDays > 15 ) { null; }
  elsif ( $PARemDays > 10 ) { $StatusColor = 'orange'; }
  elsif ( $PARemDays > 0 )  { $StatusColor = 'red'; $StatusReason .= ' PA less than 10 days '; }
  else { $StatusColor = 'red'; $StatusReason .= ' No Primary Authorized PA '; }
#warn qq|CNT=$CNT, PARemDays=$PARemDays\n|;
#warn qq|POPUP=$POPUP\nHREF=$HREF\n|;
  return($POPUP,$HREF);
}
sub setPA
{
  my ($self,$i,$Priority) = @_;

# this is Primary and has a PAnumber...then set the days remaining on the PA...
  if ( $Priority == 1 && $i->{PPACnt} )
  {
	# set until good PA found...
	if ( $PARemDays < 15 ) { $PARemDays = $i->{PARemDays}; }
  }
#warn qq|setPA: Priority=$Priority, PPACnt=$i->{PPACnt}, Color/msg=${PAColor}/${PAStatus}\n|;

  if ( $i->{PPACnt} == 0 )
  { $PAColor = "red"; $PAStatus = "No PA found!"; }
  elsif ( $i->{UnitsAuth} > 0 && $i->{UnitsLeft} <= 0 )
  { $PAColor = "red"; $PAStatus = "No Units available for PA."; }
  elsif ( $i->{UnitsAuth} == 0 && $i->{AmtAuth} > 0 && $i->{AmtLeft} <= 0 )
  { $PAColor = "red"; $PAStatus = "PA Authorized Amount used."; }
  elsif ( $i->{PARemDays} > 15 )
  { $PAColor = "green"; $PAStatus = "PA has more than 15 days ($i->{PARemDays} days)."; }
  elsif ( $i->{PARemDays} > 10 )
  { $PAColor = "red"; $PAStatus = "PA has less than 15 days ($i->{PARemDays} days)."; }
  else
  { $PAColor = "red"; $PAStatus = "PA has 10 days or less ($i->{PARemDays} days)."; }

  my $PctAmtNotify = sprintf("%.2f",($i->{CurAmtAuth} * .20));    # 20%
#warn qq|CurAmtAuth=$i->{CurAmtAuth}\n|;
#warn qq|CurAmtAuth=$i->{CurAmtLeft}\n|;
#warn qq|PctAmtNotify=$PctAmtNotify\n|;
  if ( $i->{CurUnitsAuth} > 0 )
  { $CurPAColor = $PAColor; $CurPAStatus = "Current PA has $i->{CurRemDays} days remaining."; }
  elsif ( $i->{CurAmtLeft} > $PctAmtNotify )
  { $CurPAColor = $PAColor; $CurPAStatus = "Current PA has more than 20&#37; left<BR>and $i->{CurRemDays} days remaining."; }
  elsif ( $i->{CurAmtLeft} > 0 )
  { $CurPAColor = "orange"; $CurPAStatus = "Current PA reached less than 20&#37; left<BR>and $i->{CurRemDays} days remaining."; }
  else
  { $CurPAColor = "red"; $CurPAStatus = "Current PA fell below zero(0)<BR>and $i->{CurRemDays} days remaining."; }
#warn qq|PAStatus=$PAStatus\n|;
#warn qq|CurPAStatus=$CurPAStatus\n|;
  return();
}
