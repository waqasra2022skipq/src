#!/usr/bin/perl
use lib '/home/okmis/mis/src/lib';
use CGI qw(:standard escape);
use DBI;
use myForm;
use myDBI;
use SysAccess;
use DBA;
use DBUtil;
use myHTML;
use gHTML;
use cBill;
use uBill;
use Time::Local;

############################################################################
#use Time::HiRes qw(time);
#$t_start=Time::HiRes::time;
#warn "ChartList   curtime: $t_start\n";
my $form = myForm->new();
my $dbh = myDBI->dbconnect($form->{'DBNAME'});
my $ForProvID = $form->{ForProvID} ? $form->{ForProvID} : $form->{LOGINPROVID};
my $DT=localtime();
my $addLinks = qq|mlt=$form->{mlt}&misLINKS=$form->{misLINKS}|;
my $addMessage = '';
my $addHelp = '';

my $ForTrID = $form->{ForTrID} ? $form->{ForTrID} : $form->{Treatment_TrID};
(my $ProviderID = $form->{Provider_ProvID}) =~ s/\D+//g;
(my $ClientID = $form->{'Client_ClientID'}) =~ s/\D+//g;

############################################################################
my $sProvider = $dbh->prepare("select * from Provider where ProvID=?");
my $sxInsurance = $dbh->prepare("select * from xInsurance where PayID=?");
#warn qq|ADJUST_TRANSID=$form->{ADJUST_TRANSID},ADJUST_TRID=$form->{ADJUST_TRID},ADJUST_AMT=$form->{ADJUST_AMT},ADJUST_REASON=$form->{ADJUST_REASON}|;
#warn qq|DENYNOTE_TRANSID=$form->{DENYNOTE_TRANSID}, DENYNOTE_TRID=$form->{DENYNOTE_TRID}, WRITEOFF_TRID=$form->{WRITEOFF_TRID},UNREVIEW_TRID=$form->{UNREVIEW_TRID}|;
if ( $form->{ADJUST_TRANSID} )
{
  unless ( DBA->updSQLdone($form) )
  {
    main->adjTrans($form,$form->{ADJUST_TRANSID},$form->{ADJUST_AMT},$form->{ADJUST_REASON});
    $form->{prompt} .= chr(253) . qq|Transaction: $form->{ADJUST_TRANSID} for TrID: $form->{ADJUST_TRID} adjusted for: $form->{ADJUST_AMT}.\\n($form->{ADJUST_REASON})|;
  }
}
if ( $form->{WRITEOFF_TRID} )
{
  unless ( DBA->updSQLdone($form) )
  {
    my $r835 = ();
    $r835->{'TrID'}      = $form->{'WRITEOFF_TRID'};
    $r835->{'RecDate'}   = $form->{TODAY};
    $r835->{'PaidDate'}  = $form->{TODAY};
    $r835->{'RefID'}     = $form->{WRITEOFF_REASON};
    $r835->{'PaidAmt'}   = $form->{WRITEOFF_AMT};
    my ($TrID,$SCID,$code,$type) = uBill->postClaim($form,$r835,'CL','SR',$form->{WRITEOFF_REASON});
    $form->{prompt} .= chr(253) . qq|TrID: $form->{WRITEOFF_TRID} written-off for: $form->{WRITEOFF_AMT}.\\n($form->{WRITEOFF_REASON})|;
  }
}
if ( $form->{DENYNOTE_TRID} )
{
#warn qq|DENYNOTE_TRANSID=$form->{DENYNOTE_TRANSID}, DENYNOTE_TRID=$form->{DENYNOTE_TRID}, DENYNOTE_CLIENTID=$form->{DENYNOTE_CLIENTID},DENYNOTE_CONTDATE=$form->{DENYNOTE_CONTDATE}|;
  unless ( DBA->updSQLdone($form) )
  {
    my $r835 = ();
    $r835->{'TransID'}   = $form->{'DENYNOTE_TRANSID'};
    $r835->{'TrID'}      = $form->{'DENYNOTE_TRID'};
    $r835->{'ClientID'}  = $form->{'DENYNOTE_CLIENTID'};
    $r835->{'ContDate'}  = $form->{'DENYNOTE_CONTDATE'};
    $r835->{'ServCode'}  = $form->{'DENYNOTE_SCNUM'};
    $r835->{'RecDate'}   = $form->{TODAY};
    $r835->{'RefID'}     = $form->{DENYNOTE_REASON};
    $r835->{'PaidAmt'}   = 0;                        # postClaim: deny if 0
    $r835->{'DenCode'}   = 'A1';
    my ($TrID,$SCID,$code,$type) = uBill->postClaim($form,$r835,'CL','MD',$form->{DENYNOTE_REASON});
    $form->{prompt} .= chr(253) . qq|Transaction: $form->{DENYNOTE_TRANSID} for TrID: $form->{DENYNOTE_TRID} for: $form->{DENYNOTE_CONTDATE}/$form->{DENYNOTE_SCNUM} Denied.\\n($form->{DENYNOTE_REASON})|;
  }
}
if ( $form->{UNREVIEW_TRID} )
{
  unless ( DBA->updSQLdone($form) )
  {
    my $sTreatment = $dbh->prepare("select * from Treatment where TrID=?");
    $sTreatment->execute($form->{UNREVIEW_TRID});
    my $rTreatment = $sTreatment->fetchrow_hashref;
    $sTreatment->finish();
    my $StatusMsg = $rTreatment->{'StatusMsg'} . ' ' .$form->{UNREVIEW_REASON};
    my $sUnReview = $dbh->prepare("update Treatment set RevStatus=2, MgrProvID=NULL, MgrRevDate=NULL, MgrRevTime=NULL, StatusMsg=? where TrID=?");
    $sUnReview->execute($StatusMsg,$form->{UNREVIEW_TRID});
    $sUnReview->finish();
    $form->{prompt} .= chr(253) . qq|TrID: $form->{UNREVIEW_TRID} has been UNREVIEWED. Manager APPROVAL backed-out.\\n(${StatusMsg})|;
  }
}
############################################################################
my $WithSelect = '';
my $SortOptions = qq|&AddDetail=$form->{AddDetail}|;
my $AddDetail = $form->{AddDetail} ? 'CHECKED' : '';
my $NoDetail = $form->{AddDetail} ? '' : 'CHECKED';
$form->{'FORMID'} = myDBI->getFORMID($form);

my ($SortTypeAll,$SortTypeInprocess,$SortTypeScholarshipped,$SortTypeReconciled,$SortTypeNotReconciled,$SortTypeNotBilled)
   = ('','','','','','');
if ( $ForTrID ) { null; }             # for a specfic TrID we DON'T NEED the SortOptions.
elsif ( $form->{SortType} eq 'all' )
{ 
  $WithSelect .= qq| |;
  $SortOptions .= qq|&SortType=all|;
  $SortTypeAll = 'CHECKED';
}
elsif ( $form->{SortType} eq 'inprocess' )
{ 
  $WithSelect .= qq| and Treatment.BillStatus = 3 |;
  $SortOptions .= qq|&SortType=inprocess|;
  $SortTypeInprocess = 'CHECKED';
}
elsif ( $form->{SortType} eq 'scholarshipped' )
{ 
  $WithSelect .= qq| and Treatment.BillStatus = 4 |;
  $SortOptions .= qq|&SortType=scholarshipped|;
  $SortTypeScholarshipped = 'CHECKED';
}
elsif ( $form->{SortType} eq 'reconciled' )
{ 
  $WithSelect .= qq| and Treatment.BillStatus = 5 |;
  $SortOptions .= qq|&SortType=reconciled|;
  $SortTypeReconciled = 'CHECKED';
}
elsif ( $form->{SortType} eq 'notreconciled' )
{ 
  $WithSelect .= qq| and (Treatment.BillStatus != 4 and Treatment.BillStatus != 5) |;
  $SortOptions .= qq|&SortType=notreconciled|;
  $SortTypeNotReconciled = 'CHECKED';
}
else
{ 
  $WithSelect .= qq| and Treatment.BillStatus < 3 |;
  $SortOptions .= qq|&SortType=notbilled|;
  $SortTypeNotBilled = 'CHECKED';
}
my ($SinceDate,$SortRangeL1M,$SortRangeL3M,$SortRangeL6M,$SortRangeL9M
   ,$SortRangeL1Y,$SortRangeL2Y,$SortRangeALL) = ('','','','','','','','');
#warn qq|form-SortRange=$form->{SortRange}\n|;
if ( $form->{SortRange} =~ /l1m/i )
{
  $SinceDate = DBUtil->Date('',-1,0);    # 1 month ago
  $WithSelect .= qq| and Treatment.ContLogDate >= '${SinceDate}'|;
  $SortOptions .= qq|&SortRange=L1M|;
  $SortRangeL1M = 'CHECKED';
}
elsif ( $form->{SortRange} =~ /l3m/i )
{
  $SinceDate = DBUtil->Date('',-3,0);    # 3 months ago
  $WithSelect .= qq| and Treatment.ContLogDate >= '${SinceDate}'|;
  $SortOptions .= qq|&SortRange=L3M|;
  $SortRangeL3M = 'CHECKED';
}
elsif ( $form->{SortRange} =~ /l6m/i )
{
  $SinceDate = DBUtil->Date('',-6,0);    # 6 months ago
  $WithSelect .= qq| and Treatment.ContLogDate >= '${SinceDate}'|;
  $SortOptions .= qq|&SortRange=L6M|;
  $SortRangeL6M = 'CHECKED';
}
elsif ( $form->{SortRange} =~ /l9m/i )
{
  $SinceDate = DBUtil->Date('',-9,0);    # 9 months ago
  $WithSelect .= qq| and Treatment.ContLogDate >= '${SinceDate}'|;
  $SortOptions .= qq|&SortRange=L9M|;
  $SortRangeL9M = 'CHECKED';
}
elsif ( $form->{SortRange} =~ /l1y/i )
{
  $SinceDate = DBUtil->Date('',-12,0);    # 12 months ago
  $WithSelect .= qq| and Treatment.ContLogDate >= '${SinceDate}'|;
  $SortOptions .= qq|&SortRange=L1Y|;
  $SortRangeL1Y = 'CHECKED';
}
elsif ( $form->{SortRange} =~ /l2y/i )
{
  $SinceDate = DBUtil->Date('',-24,0);    # 24 months ago
  $WithSelect .= qq| and Treatment.ContLogDate >= '${SinceDate}'|;
  $SortOptions .= qq|&SortRange=L2Y|;
  $SortRangeL2Y = 'CHECKED';
}
else
{ 
  $SortOptions .= qq|&SortRange=ALL|;
  $SortRangeALL = 'CHECKED';
}
my $order = qq|Treatment.ContLogDate,Treatment.ContLogBegTime,Treatment.ContLogEndTime|;

my $qNotes = '';
my $rClient = '';
my $rProvider = '';
my $ChartType = '';
my $ChartName = '';
my $SearchName = '';
my $ClientInsURL = '';
my $Rebill_Button = '';

if ( $ForTrID )
{
  (my $TrID = $ForTrID) =~ s/\D+//g;
  $sClient = $dbh->prepare("select Treatment.*, Client.FName, Client.LName, Client.SSN, Client.ProvID as PrimaryProvID from Treatment left join Client on Client.ClientID=Treatment.ClientID where TrID=?");
  $sClient->execute($TrID);
  if ( $rClient = $sClient->fetchrow_hashref )
  {
    $ChartName = qq|$rClient->{FName} $rClient->{LName}|;
    $SearchName = qq|$rClient->{FName} $rClient->{LName} ($rClient->{ClientID}) $rClient->{SSN}|;
    $qNotes = qq|select Treatment.*, xBillStatus.Descr as BillStatusDescr
        , Client.LName, Client.FName, Client.Suffix, Client.SSN
        , Clinic.Name as ClinicName
        , Counselor.FName as ProviderFName, Counselor.LName as ProviderLName, Counselor.ScreenName as ProviderScreenName
        , Reviewer.FName as ReviewerFName, Reviewer.LName as ReviewerLName, Reviewer.ScreenName as ReviewerScreenName
        , xSC.SCNum
      from Treatment
      left join ClientACL on ClientACL.ClientID=Treatment.ClientID
      left join Client on Client.ClientID=Treatment.ClientID
      left join Provider as Clinic on Clinic.ProvID=Treatment.ClinicID
      left join Provider as Counselor on Counselor.ProvID=Treatment.ProvID
      left join Provider as Reviewer on Reviewer.ProvID=Treatment.MgrProvID
      left join xSC on xSC.SCID=Treatment.SCID
      left join xBillStatus on xBillStatus.ID=Treatment.BillStatus
      where Treatment.TrID='${TrID}'
|;
    $hidden = qq|<INPUT TYPE="hidden" NAME="Client_ClientID" VALUE="$rClient->{ClientID}" >|;
    $ChartType = 'by Note';
    $sProvider->execute($rClient->{PrimaryProvID});
    $rProvider = $sProvider->fetchrow_hashref;
#warn qq|\n TrID=$ForTrID, ProvID=$rClient->{PrimaryProvID}, ClientID=$rClient->{ClientID}\n|;
    if ( SysAccess->verify($form,'hasClientAccess',$rClient->{ClientID}) )
    {
      if ( $form->{LOGINPROVID} != $rClient->{ProvID} )
      { $addMessage .= 'Chart List / Access Denied!' unless ( SysAccess->verify($form,'Privilege=OtherProvNotes') ); }
    } else { $addMessage .= 'Chart List / Access Denied!'; }
  }
  $sClient->finish();
  unless ( $rClient->{ClientID} ) { myDBI->error("Chart List / $ForTrID Not Found!"); }
}
elsif ( $ProviderID )
{
  $ProviderID = $form->{LOGINPROVID} if ( !$ProviderID );
  if ( ! SysAccess->verify($form,'hasProviderAccess',$ProviderID) )
  { myDBI->error("Provider Access Charts / Access Denied"); }
  $sProvider->execute($ProviderID);
  $rProvider = $sProvider->fetchrow_hashref;
  $ChartName = qq|$rProvider->{FName} $rProvider->{LName}|;
  $SearchName = qq|$rProvider->{FName} $rProvider->{LName}|;

  $qNotes = qq|select Treatment.*, xBillStatus.Descr as BillStatusDescr
      , Client.LName, Client.FName, Client.Suffix, Client.SSN
      , Clinic.Name as ClinicName
      , Counselor.FName as ProviderFName, Counselor.LName as ProviderLName, Counselor.ScreenName as ProviderScreenName
      , Reviewer.FName as ReviewerFName, Reviewer.LName as ReviewerLName, Reviewer.ScreenName as ReviewerScreenName
      , xSC.SCNum
    from Treatment
    left join ClientACL on ClientACL.ClientID=Treatment.ClientID
    left join Client on Client.ClientID=Treatment.ClientID
    left join Provider as Clinic on Clinic.ProvID=Treatment.ClinicID
    left join Provider as Counselor on Counselor.ProvID=Treatment.ProvID
    left join Provider as Reviewer on Reviewer.ProvID=Treatment.MgrProvID
    left join xSC on xSC.SCID=Treatment.SCID
    left join xBillStatus on xBillStatus.ID=Treatment.BillStatus
    where Treatment.ProvID='$ProviderID'
|;

  $hidden = qq|<INPUT TYPE="hidden" NAME="Provider_ProvID" VALUE="${ProviderID}" >|;
  $ChartType = 'by Provider';
  if($form->{LOGINPROVID} == 90 || $form->{LOGINPROVID} == 91) {
    $Rebill_Button = qq|<FONT COLOR="red"><A STYLE="background-color:white; padding:0.2em;"  HREF="javascript:ReportWindow('/cgi/bin/runCMDBash.pl?AgencyID=${ProviderID}&mlt=$form->{mlt}','adjNote')"  TITLE="Click here to change In Process notes to Rebill" >Rebill Notes</A></FONT>|;
  }
# per Chris...look at them by date/time, to check for conflicts.
#  $order = qq|Client.LName,Client.FName,Treatment.ContLogDate,Treatment.ContLogBegTime,Treatment.ContLogEndTime|;
}
elsif ( $ClientID )
{
  if ( ! SysAccess->verify($form,'hasClientAccess',$ClientID) )
  { myDBI->error("Client Access Charts / Not Client"); }
  $sClient = $dbh->prepare("select * from Client where ClientID=? ");
  $sClient->execute($ClientID);
  $rClient = $sClient->fetchrow_hashref;
  $ChartName = qq|$rClient->{FName} $rClient->{LName}|;
  $SearchName = qq|$rClient->{FName} $rClient->{LName} ($rClient->{ClientID}) $rClient->{SSN}|;
  $qNotes = qq|select Treatment.*, xBillStatus.Descr as BillStatusDescr
      , Client.LName, Client.FName, Client.Suffix, Client.SSN
      , Clinic.Name as ClinicName
      , Counselor.FName as ProviderFName, Counselor.LName as ProviderLName, Counselor.ScreenName as ProviderScreenName
      , Reviewer.FName as ReviewerFName, Reviewer.LName as ReviewerLName, Reviewer.ScreenName as ReviewerScreenName
      , xSC.SCNum
    from Treatment
    left join ClientACL on ClientACL.ClientID=Treatment.ClientID
    left join Client on Client.ClientID=Treatment.ClientID
    left join Provider as Clinic on Clinic.ProvID=Treatment.ClinicID
    left join Provider as Counselor on Counselor.ProvID=Treatment.ProvID
    left join Provider as Reviewer on Reviewer.ProvID=Treatment.MgrProvID
    left join xSC on xSC.SCID=Treatment.SCID
    left join xBillStatus on xBillStatus.ID=Treatment.BillStatus
    where Client.ClientID='$ClientID'
|;
  $hidden = qq|<INPUT TYPE="hidden" NAME="Client_ClientID" VALUE="${ClientID}" >|;
  $ChartType = 'by Client';
  (my $ClientName = qq|$rClient->{FName} $rClient->{LName}|) =~ s/'/\\'/g;
  $ClientInsURL = qq|<A HREF="javascript:ReportWindow('/cgi/bin/ListInsPaid.cgi?Client_ClientID=${ClientID}&${addLinks}','ClientInsPaid')" TITLE="Click here for <BR>${ClientName}\'s Manual Insurance Payments." ><IMG SRC="/images/piggybank.gif" BORDER="0" HEIGHT="20" WIDTH="20" ALT="Manual Insurance Payments" ></A>|;
  $sClient->finish();
  $sProvider->execute($rClient->{ProvID});
  $rProvider = $sProvider->fetchrow_hashref;
}
else { myDBI->error("Chart List / Error on Access!"); }
#warn "ChartList: WithSelect=${WithSelect}\n";
$qNotes .= qq| ${WithSelect} |
        .  ' and ' . DBA->withNoteAccess($form,$ForProvID,'Treatment') 
        .  qq|  order by ${order}|;

(my $ClientName = qq|$rClient->{FName} $rClient->{LName}|) =~ s/'/\\'/g;
(my $ProviderName = qq|$rProvider->{FName} $rProvider->{LName}|) =~ s/'/\\'/g;
#warn "ChartList: qNotes=${qNotes}\n" if ( $form->{LOGINPROVID} == 91 );
############################################################################
my $BackLinks = gHTML->setLINKS($form,'back');
my $ClientListByProv = qq|<A HREF="/cgi/bin/ClientList.cgi?Provider_ProvID=$rProvider->{ProvID}&${addLinks}" TITLE="Click here for <BR>${ProviderName}\'s Client List." ><IMG BORDER=0 SRC="/images/icon_folder.gif" HEIGTH="30" WIDTH="30" ></A>|;
my $AddNote = $ClientID ? qq|      <A HREF="/cgi/bin/mis.cgi?MIS_Action=Note&Client_ClientID=${ClientID}&Treatment_TrID=new&${addLinks}" TITLE="Click here to <BR>add a Note for <BR>${ClientName}." ><IMG SRC="/images/edit.gif" CLASS="site" HEIGHT="35" WIDTH="35" ></A>| : '';
my $PhysNote = $ClientID && DBA->isPhysician($form) ? qq|     <A HREF="/cgi/bin/mis.cgi?MIS_Action=Note&NoteType=2&Client_ClientID=${ClientID}&Treatment_TrID=new&${addLinks}" TITLE="Click here to <BR>add a Physician Note for <BR>${ClientName}." > <IMG SRC="/cgi/images/caduceuswhite.png" WIDTH="24" HEIGHT="24" > </A>| : '';
my $TestNote = $form->{'LOGINPROVID'}==91 ? qq|     <A HREF="/cgi/bin/mis.cgi?MIS_Action=Note&NoteType=5&Client_ClientID=${ClientID}&Treatment_TrID=new&${addLinks}" TITLE="Click here to <BR>add a Physician Note for <BR>${ClientName}." > <IMG SRC="/cgi/images/caduceuswhite.png" WIDTH="24" HEIGHT="24" > </A>| : '';
$sProgNotes = $dbh->prepare("select * from ProgNotes where NoteID=? ");
$sPhysNotes = $dbh->prepare("select * from PhysNotes where NoteID=? ");
$sNoteTrans = $dbh->prepare("select * from NoteTrans where TrID=? order by ID");
$sClientInsRemarksDetail = $dbh->prepare("select * from ClientInsRemarksDetail where TrID=? order by CheckDate desc");
###$sClientNoteAmendments = $dbh->prepare("select * from ClientNoteAmendments where TrID=? ");
my $AgentACCESS = SysAccess->chkPriv($form,'Agent');
my $ADDTransACCESS = SysAccess->chkPriv($form,'ADDTrans');
##$AgentACCESS = 1 if ( $form->{LOGINPROVID} == 103 && $form->{DBNAME} eq 'okmis_cti' );   # Janet Cizek
my $BillingRemitACCESS = SysAccess->chkPriv($form,'BillingRemit');
my $BillingAdmin = SysAccess->chkPriv($form,'BillingAdmin');
my $ShowAmountsACCESS = SysAccess->chkPriv($form,'ShowAmounts');
my $Client_TrIDs = ();
my $printstr = qq|Chart List ${ChartType}: ${SearchName} ${DT}|;
my $printfile = '/tmp/pfnl_' . DBUtil->genToken() . '.html';
my $pathname = $form->{DOCROOT} . $printfile;
my $field_count = 15;

# Start out the display.
my $html = myHTML->new($form) . qq|
<TABLE CLASS="main" >
  <TR ALIGN="center" >
| . myHTML->leftpane($form,'clock mail managertree collapseipad') . qq|
    <TD WIDTH="84%" ALIGN="center" >
| . myHTML->hdr($form) . myHTML->menu($form) . qq|
<FORM NAME="ChartList" ACTION="/cgi/bin/ChartList.cgi" METHOD="POST" >
<SCRIPT LANGUAGE="JavaScript" SRC="/cgi/js/vEntry.js"> </SCRIPT>
<SCRIPT LANGUAGE="JavaScript" SRC="/cgi/js/vChartList.js"> </SCRIPT>
<SCRIPT LANGUAGE="JavaScript" SRC="/cgi/js/vNum.js"> </SCRIPT>
<SCRIPT LANGUAGE="JavaScript" SRC="/cgi/js/tablesort.js"> </SCRIPT>
<LINK HREF="/cgi/css/tablesort.css" REL="stylesheet" TYPE="text/css">
<A NAME="top">
<TABLE CLASS="main fullsize" >
  <TR >
    <TD CLASS="strcol" >
      <SPAN CLASS="header" >Chart List</SPAN> <BR> 
      ${ChartType}: ${SearchName}
      <SPAN STYLE="position: fixed; top: 0; left: 130px; color: orange; background-color: black; font-weight: bold; padding: 5px; border: 2px solid green; " >${ChartType}: ${SearchName}</SPAN>
      $Rebill_Button
      <BR>
    </TD>
    <TD CLASS="info numcol" >
      ${BackLinks} ${ClientListByProv} ${AddNote} ${PhysNote} ${TestNote}
    </TD>
  </TR>
</TABLE>

<TABLE CLASS="home fullsize" >
| . main->hdr();

my $RecCount=0;
$sNotes = $dbh->prepare($qNotes);
$sNotes->execute();
while ( $rNotes = $sNotes->fetchrow_hashref )
{
  $RecCount+=1;
  $html .= main->prtNote($RecCount,$rNotes);
  $html .= main->prtNoteTrans($RecCount,$rNotes) if ( $form->{AddDetail} );
  my $ClientKey = qq|$rNotes->{LName}_$rNotes->{FName}_$rNotes->{ClientID}|;
  $Client_TrIDs->{$ClientKey}->{$rNotes->{TrID}} = $rNotes->{TrID};
}
if ( $form->{SortType} eq 'notreconciled' )
{
  $addHelp = qq|
<DIV CLASS="port hdrcol" >
  <A CLASS="port" HREF="javascript:ReportWindow('http://okmis.helpdocsonline.com/working-denied-claims-2','PrintWindow')" >
    <B>Use it 'Add Detail' for ICN:</B>
    Working Denied Claims
  </A>
</DIV>
|;
}
#warn "ChartList: RecCount=${RecCount}\n";
$html .= qq|
</TBODY>
</TABLE>
<DIV><FONT COLOR="red" >${addMessage}</FONT></DIV>
${addHelp}
<P>
${hidden}
<INPUT TYPE="hidden" NAME="ForTrID" VALUE="$ForTrID" >
<INPUT TYPE="hidden" NAME="DENYNOTE_TRANSID" VALUE="" >
<INPUT TYPE="hidden" NAME="DENYNOTE_TRID" VALUE="" >
<INPUT TYPE="hidden" NAME="DENYNOTE_CLIENTID" VALUE="" >
<INPUT TYPE="hidden" NAME="DENYNOTE_CONTDATE" VALUE="" >
<INPUT TYPE="hidden" NAME="DENYNOTE_SCNUM" VALUE="" >
<INPUT TYPE="hidden" NAME="DENYNOTE_REASON" VALUE="" >
<INPUT TYPE="hidden" NAME="ADJUST_TRANSID" VALUE="" >
<INPUT TYPE="hidden" NAME="ADJUST_TRID" VALUE="" >
<INPUT TYPE="hidden" NAME="ADJUST_AMT" VALUE="" >
<INPUT TYPE="hidden" NAME="ADJUST_REASON" VALUE="" >
<INPUT TYPE="hidden" NAME="WRITEOFF_TRID" VALUE="" >
<INPUT TYPE="hidden" NAME="WRITEOFF_AMT" VALUE="" >
<INPUT TYPE="hidden" NAME="WRITEOFF_REASON" VALUE="" >
<INPUT TYPE="hidden" NAME="UNREVIEW_TRID" VALUE="" >
<INPUT TYPE="hidden" NAME="UNREVIEW_REASON" VALUE="" >
<INPUT TYPE="hidden" NAME="FORMID" VALUE="$form->{FORMID}" >
<INPUT TYPE="hidden" NAME="mlt" VALUE="$form->{mlt}" >
<INPUT TYPE="hidden" NAME="misLINKS" VALUE="$form->{misLINKS}" >
<INPUT TYPE="hidden" NAME="LINKID" VALUE="$form->{LINKID}" >
</FORM >
  <A NAME="bottom">
|;

if ( $BillingRemitACCESS )
{
  $html .= main->setInsPaid();
  $html .= myHTML->ListSel($form,'ListClientInsRemarks',$ClientID,$form->{'LINKID'},0) if ( $ClientID );
}
$html .= qq|
  <BR>
  <DIV CLASS="port" >
    <A HREF="#top" >
      <IMG SRC="/img/arrow_up.png" HEIGHT="21" WIDTH="21" BORDER=0" >
      top
    </A>
  </DIV>
|;
$html .= myHTML->rightpane($form,'search');

# Complete the printer friendly version.
if ( open(TEMPLATE, ">$pathname") ) 
{
  my $detail = $form->{AddDetail} ? qq|
    <TR >
      <TD ALIGN="center" >&nbsp;</TD>
      <TD ALIGN="right" >Cnt.</TD>
      <TD ALIGN="right" >TransID</TD>
      <TD ALIGN="center" >&nbsp;</TD>
      <TD ALIGN="center" >&nbsp;</TD>
      <TD ALIGN="center" >&nbsp;</TD>
      <TD ALIGN="center" >&nbsp;</TD>
      <TD ALIGN="center" >RefID</TD>
      <TD ALIGN="center" >&nbsp;</TD>
      <TD ALIGN="center" >ICN</TD>
      <TD ALIGN="center" >Hours</TD>
      <TD ALIGN="center" >BillAmt</TD>
      <TD ALIGN="center" >PaidAmt</TD>
      <TD ALIGN="center" >RecDate</TD>
      <TD ALIGN="center" >DenCode</TD>
      <TD ALIGN="center" >TransType</TD>
    </TR>
| : '';
  print TEMPLATE qq|<HTML>
<TABLE>
  <TR >
    <TD >LastName</TD>
    <TD >FirstName</TD>
    <TD >ClientID</TD>
    <TD >TrID</TD>
    <TD >RevMsg</TD>
    <TD ALIGN="center" >ContactDate</TD>
    <TD ALIGN="center" >SCNum</TD>
    <TD ALIGN="center" >Progress</TD>
    <TD ALIGN="center" >Units</TD>
    <TD ALIGN="center" >BegTime</TD>
    <TD ALIGN="center" >EndTime</TD>
    <TD ALIGN="center" >BillDate</TD>
    <TD ALIGN="center" >BillStatus</TD>
    <TD ALIGN="center" >StatusDate</TD>
    <TD ALIGN="center" >AmtDue</TD>
  </TR>
  ${detail}
  ${printstr}
</TABLE>
</HTML>|;
  close(TEMPLATE);
}
#$t_diff=Time::HiRes::time-$t_start;
#warn "ChartList end     time: $t_diff seconds!\n";
# Close the SQL statments.
$sProvider->finish();
$sxInsurance->finish();
$sProgNotes->finish();
$sPhysNotes->finish();
$sNoteTrans->finish();
$sNotes->finish();
###$sClientNoteAmendments->finish();
$sClientInsRemarksDetail->finish();
myDBI->cleanup();
print $html;
exit;
############################################################################
sub hdr
{
  my ($self) = @_;

  my $HelpDenials = $form->{SortType} eq 'notreconciled' ?
    qq|<BR><B>Use 'Add Detail' for ICN:</B> <A CLASS="port" HREF="javascript:ReportWindow('http://okmis.helpdocsonline.com/working-denied-claims-2','PrintWindow')" >Working Denied Claims</A>| : '';
##
# could be (was) 5 used in      TABLE table-autosort: 5
##
  my $out .= qq|
<TABLE CLASS="port fullsize" >
  <TR CLASS="port" >
    <TH CLASS="strcol" COLSPAN="2" >
      <A HREF="javascript:ReportWindow('${printfile}','PrintWindow')" TITLE="Click here for a printer friendly screen for this Chart List." ><IMG SRC="/images/icon_print.gif" BORDER="0" ></A>
      Choose Range, Sort Type then click 
      <INPUT TYPE="button" ONCLICK="this.form.submit();" VALUE="here" >.
      ${HelpDenials}
    </TH>
    <TH CLASS="strcol" COLSPAN="2" >
      <A HREF="#bottom" >
        <IMG SRC="/img/arrow_down.png" HEIGHT="21" WIDTH="21" BORDER=0" >
        bottom
      </A>
    </TH>
    <TH CLASS="strcol" > <INPUT TYPE="radio" NAME="AddDetail" VALUE="0" ${NoDetail} >No Detail</TH>
    <TH CLASS="strcol" > <INPUT TYPE="radio" NAME="AddDetail" VALUE="1" ${AddDetail} >Add Detail</TH>
  </TR>
  <TR CLASS="port" >
    <TH CLASS="strcol" >Range Contact Date Back:</TH>
    <TH CLASS="strcol" > <INPUT TYPE="radio" NAME="SortRange" VALUE="L1M" ${SortRangeL1M} >1 Month</TH>
    <TH CLASS="strcol" > <INPUT TYPE="radio" NAME="SortRange" VALUE="L3M" ${SortRangeL3M} >3 Months</TH>
    <TH CLASS="strcol" > <INPUT TYPE="radio" NAME="SortRange" VALUE="L6M" ${SortRangeL6M} >6 Months</TH>
    <TH CLASS="strcol" > <INPUT TYPE="radio" NAME="SortRange" VALUE="L1Y" ${SortRangeL1Y} >12 Months</TH>
    <TH CLASS="strcol" > <INPUT TYPE="radio" NAME="SortRange" VALUE="ALL" ${SortRangeALL} >All Dates</TH>
  </TR>
  <TR CLASS="port" >
    <TH CLASS="strcol" >Sort Type: &nbsp; &nbsp; &nbsp;
      <INPUT TYPE="radio" NAME="SortType" VALUE="notbilled" ${SortTypeNotBilled} >Not Billed
    </TH>
    <TH CLASS="strcol" > <INPUT TYPE="radio" NAME="SortType" VALUE="inprocess" ${SortTypeInprocess} >InProcess</TH>
    <TH CLASS="strcol" > <INPUT TYPE="radio" NAME="SortType" VALUE="scholarshipped" ${SortTypeScholarshipped} >Scholarshipped</TH>
    <TH CLASS="strcol" > <INPUT TYPE="radio" NAME="SortType" VALUE="reconciled" ${SortTypeReconciled} >Reconciled</TH>
    <TH CLASS="strcol" > <INPUT TYPE="radio" NAME="SortType" VALUE="notreconciled" ${SortTypeNotReconciled} >NotReconciled</TH>
    <TH CLASS="strcol" > <INPUT TYPE="radio" NAME="SortType" VALUE="all" ${SortTypeAll} >All Notes</TH>
  </TR>
</TABLE>
<TABLE class="chartsort table-autosort table-stripeclass:alternate">
<THEAD>
  <TR >
    <TH class="table-sortable:default" >Last Name</TH>
    <TH class="table-sortable:numeric" >TrID</TH>
    <TH >PDF</TH>
    <TH class="table-sortable:numeric" >PrAuthID</TH>
    <TH class="table-sortable:date" >Contact Date</TH>
    <TH class="table-sortable:alphanumeric" >Service Code</TH>
    <TH class="table-sortable:numeric" >Progress</TH>
    <TH class="table-sortable:numeric" >Units</TH>
    <TH class="table-sortable:alphanumeric" >Begin Time</TH>
    <TH class="table-sortable:alphanumeric" >End Time</TH>
    <TH class="table-sortable:date" >Org Billed</TH>
    <TH class="table-sortable:default" >Status</TH>
    <TH class="table-sortable:date" >Date</TH>
    <TH class="table-sortable:currency" >AmtDue</TH>
    <TH >HCFA</TH>
  </TR>
</THEAD>
|;
  $out .= qq|
  <TR CLASS="alternate2" >
    <TH >-</TH>
    <TH >-</TH>
    <TH >-</TH>
    <TH >Detail#</TH>
    <TH >Contact Date</TH>
    <TH >Service Code</TH>
    <TH >RefID</TH>
    <TH >Units</TH>
    <TH >ICN</TH>
    <TH >Hours</TH>
    <TH >Billed</TH>
    <TH >Paid</TH>
    <TH >Date</TH>
    <TH >Denied</TH>
    <TH >Code</TH>
  </TR>
| if ( $form->{AddDetail} );
  $out .= qq|<TBODY>\n|;
  return($out);
}
############################################################################
sub prtNote
{
  my ($self,$count,$r) = @_;
  my $out = '';
  my ($NoteIMG,$Progress,$TrIDColor,$TrIDMesg,$NoteMsg) = ('','','black','Note billed/reconciled.','');
  if ( $r->{Type} == 3 )
  { 
    $NoteIMG = qq|<IMG SRC="/images/lightning.gif" BORDER="0" >|;
    $NoteMsg = 'No document attached?' if ( $r->{Path} eq '' );
  }
  elsif ( $r->{Type} == 2 )
  { $NoteIMG = qq|<IMG SRC="/cgi/images/caduceuswhite.png" WIDTH="24" HEIGHT="24" >|; }
  else          # Type = 1,4,5
  { 
    $sProgNotes->execute($r->{TrID});
    $rProgNotes = $sProgNotes->fetchrow_hashref;
    $Progress = $rProgNotes->{Progress};
    $NoteIMG = qq|<IMG SRC="/images/facesicon.gif" BORDER="0" >|;
  }
#warn qq|TrID=$r->{TrID}, BillStatus=$r->{BillStatus}, RevStatus=$r->{RevStatus}\n|;
  if ( $r->{BillStatus} > 1 )
  {
    if ( $r->{BillStatus} == 2 ) { $TrIDColor = 'red'; }
    elsif ( $r->{BillStatus} > 5 ) { $TrIDColor = 'red'; }
    else { $TrIDColor = 'black'; }
    $TrIDMesg = qq|Note $r->{BillStatusDescr}.|
  }
  elsif ( $r->{RevStatus} == 0 )
  { $TrIDColor = 'blue'; $TrIDMesg = qq|Provider approval needed.| }
  elsif ( $r->{RevStatus} == 1 )
  { $TrIDColor = 'orange'; $TrIDMesg = qq|Provider approval of Manager changes needed.| }
  elsif ( $r->{RevStatus} == 2 )
  { $TrIDColor = 'red'; $TrIDMesg = qq|Manager review/approval needed.| }
  elsif ( $r->{RevStatus} == 3 )
  { $TrIDColor = 'darkgreen'; $TrIDMesg = qq|Note approved for billing.| }
  $TrIDMesg .= qq| $r->{StatusMsg} ${NoteMsg}|;

#foreach my $f ( sort keys %{ $r } ) { warn qq|: r-$f=$r->{$f}\n|; }
  my $ProvLName = $r->{ProviderScreenName} ? $r->{ProviderScreenName} : $r->{ProviderLName};
  my $ProvName = $r->{ProviderScreenName} ? $r->{ProviderScreenName} : qq|$r->{ProviderFName} $r->{ProviderLName}|;
  (my $Name = qq|$r->{FName} $r->{LName}|) =~ s/'/\\'/g;
  my $TrIDProvider = qq|Note by ${ProvName} for $r->{ClinicName}|;
#foreach my $f ( sort keys %{ $r } ) { warn qq|: r-$f=$r->{$f}\n|; }
  my $rxSC = cBill->getServiceCode($form,$r->{SCID},$r->{ContLogDate},$r->{ContLogBegTime},$r->{ContLogEndTime},$r->{TrID});
  my $rInsurance = cBill->getInsurance($form,$r->{ClientID},$rxSC->{InsID},$r->{ContLogDate});
  my $ContLogDate = DBUtil->Date($r->{ContLogDate},'fmt','MM/DD/YY');
  my $ContLogBegTime = substr($r->{ContLogBegTime},0,5);
  my $ContLogEndTime = substr($r->{ContLogEndTime},0,5);
  my $BillDate = $r->{BillDate} ? DBUtil->Date($r->{BillDate},'fmt','MM/DD/YY') : 'No';
  my $BillStatus = $r->{BillStatusDescr};
  my ($DenCode,$DenCodeDescr) = ('&nbsp;','');
  my $ClientPageAcc = '';
#warn qq|ProvLName: $ProvLName = $r->{ProviderScreenName} : $r->{ProviderLName}\n|;
#warn qq|ProvName:  $ProvName = $r->{ProviderScreenName} : $r->{ProviderFName} $r->{ProviderLName}\n|;
#warn qq|ClientPageAcc=$ClientPageAcc=\n|;
  if ( $ProviderID )
  {
#warn qq|ProviderID=$ProviderID=, LName=$r->{LName}=\n|;
      $ClientPageAcc = qq|
      <A HREF="/cgi/bin/ClientPage.cgi?Client_ClientID=$r->{ClientID}&${addLinks}" TITLE="Click here for <BR>${Name}\'s Client Page <BR>(${TrIDProvider})" >$r->{LName}</A>
|;
  }
  else
  {
#warn qq|else: ClientID=$ClientID=, ProvLName=$r->{ProvLName}=\n|;
    $ClientPageAcc = qq|
      <A HREF="javascript:void(0)" TITLE="${TrIDProvider}" >${ProvLName}</A>
|;
  }
#warn qq|AND: ClientPageAcc=$ClientPageAcc\n|;

  my $even = int($count/2) == $count/2 ? '1' : '0';
  my $class = $even ? qq|CLASS="alternate"| : '';
  if ( $BillStatus =~ /Denied|Recoupment/ )
  { 
    ($DenCodeDescr = DBA->getxref($form,'xDenCodes',$r->{DenCode},'Descr')) =~ s/'//g;
    $BillStatus = qq|<FONT COLOR="red"><A HREF="javascript:void(0)" TITLE="${DenCodeDescr}" >${BillStatus} $r->{DenCode}</A></FONT>|;
#warn qq|DenCode=$r->{DenCode}=, =${DenCodeDescr}=\n|;
  }

  if ( $BillStatus eq 'Scholarship' )
  { 
    $BillStatus = qq|<FONT COLOR="red"><A  HREF="javascript:ReportWindow('/cgi/bin/unRecNoteForm.pl?submit=1&TrIDs=$r->{TrID}&mlt=$form->{mlt}&noteType=Sch','adjNote')" onclick="return getConsent('Are you SURE you want to UnScholarship $r->{TrID} ')" TITLE="Click here to UnScholarship $r->{TrID}" >${BillStatus}</A></FONT>|;
  }

  my $sNoteTransHere = $dbh->prepare("select * from NoteTrans WHERE TrID='$r->{TrID}'");
  $sNoteTransHere->execute();
  my $nTrans = $sNoteTransHere->fetchrow_hashref;
  my $nTransCode = $nTrans->{Code};

 
  if ( $BillStatus eq 'Reconciled' && $nTransCode eq 'AR' ) { 
    $BillStatus = qq|<FONT COLOR="red"><A  HREF="javascript:ReportWindow('/cgi/bin/unRecNoteForm.pl?submit=1&TrIDs=$r->{TrID}&mlt=$form->{mlt}&noteType=Auto','adjNote')" onclick="return getConsent('Are you SURE you want to UnAutoReconcile $r->{TrID} ')" TITLE="Click here to UnAutoReconcile $r->{TrID}" >${BillStatus}</A></FONT>|;
  } elsif ( $BillStatus eq 'Reconciled' && $nTransCode eq 'MR') { 
    $BillStatus = qq|<FONT COLOR="red"><A  HREF="javascript:ReportWindow('/cgi/bin/unRecNoteForm.pl?submit=1&TrIDs=$r->{TrID}&mlt=$form->{mlt}&noteType=','adjNote')" onclick="return getConsent('Are you SURE you want to UnReconcile $r->{TrID} ')" TITLE="Click here to UnReconcile $r->{TrID}" >${BillStatus}</A></FONT>|;
  }

  $sNoteTransHere->finish();

  if ( $BillStatus eq 'Inprocess' )
  { 
    $BillStatus = qq|<FONT COLOR="red"><A  HREF="javascript:ReportWindow('/cgi/bin/unRecNoteForm.pl?submit=1&TrIDs=$r->{TrID}&mlt=$form->{mlt}&noteType=New','adjNote')" onclick="return getConsent('Are you SURE you want to UnBill $r->{TrID} ')" TITLE="Click here to UnBill $r->{TrID}" >${BillStatus}</A></FONT>|;
  }

  my $StatusDate = $r->{StatusDate} ? DBUtil->Date($r->{StatusDate},'fmt','MM/DD/YY') : '&nbsp;';
  # trim leading/trailing spaces to run together and stay on 1 line...
  (my $MgrRevName = $r->{ReviewerLName}) =~ s/\s*/$1/g;
  my $MgrRevDate = $r->{MgrRevDate} ? ':'.DBUtil->Date($r->{MgrRevDate},'fmt','MM/DD/YY') : '&nbsp;';
  my $MgrRevStatus = $r->{RevStatus} == 3 && ($MgrRevName eq '' || $MgrRevDate eq '')
                   ? qq|<SPAN CLASS="hotmsg" >error! Status Reviewed but missing info</SPAN>|
                   : $r->{RevStatus} == 3 ? '' : 'none';
  my $UnReviewLabel = qq|<SPAN CLASS="sublabel" >review:${MgrRevName}${MgrRevDate}${MgrRevStatus}</SPAN>|;
  my $UnReviewButton = $r->{BillStatus} < 3 && $r->{RevStatus} == 3 && ($AgentACCESS || $BillingAdmin)
                     ? qq| <A HREF="javascript:void(0)" TITLE="Click here to <BR>Unreview the Manager approval of this note." > <INPUT TYPE="submit" ONCLICK="return vUnReview(this.form,'$r->{TrID}','$r->{RevStatus}')" NAME="UNREVIEW" VALUE="UnReview" > </A> |
                     : '';
#warn qq|ChartList: TrID=$r->{TrID}, RevStatus=$r->{RevStatus},MgrRevName=$MgrRevName,MgrRevDate$MgrRevDate,MgrRevStatus=$MgrRevStatus\n|;
  my $AmtDueButton = $r->{BillStatus} > 3 && $r->{AmtDue} > 0 && $BillingRemitACCESS 
                   ? qq| <A HREF="javascript:void(0)" TITLE="Click here to <BR>Scholarship or Write-Off remainder of note." > <INPUT TYPE="submit" ONCLICK="return vWriteOff(this.form,'$r->{TrID}','$r->{AmtDue}')" NAME="WRITEOFF_AMTDUE" VALUE="\$$r->{AmtDue}" > </A> |
                   : $ShowAmountsACCESS ? sprintf("%.2f",$r->{AmtDue}) : $r->{AmtDue} > 0 ? 'yes' : 'no';
  my $AmtDue = $ShowAmountsACCESS ? sprintf("%.2f",$r->{AmtDue}) : $r->{AmtDue} > 0 ? 'yes' : 'no';
  my $adjNoteURL = $ADDTransACCESS
                  ? qq|<BR><A HREF="javascript:ReportWindow('/cgi/bin/adjNote.pl?TrID=$r->{TrID}&InsID=$rxSC->{InsID}&${addLinks}','adjNote')" TITLE="Click here to <BR>add Transaction<BR>for $r->{TrID}" ><IMG SRC="/img/dollarsign.png" HEIGHT="21" WIDTH="21" BORDER="0" ></A>|
                  : '';
#warn qq|ChartList: TrID=$r->{TrID}, AmtDue=$r->{AmtDue},$AmtDue\n|;
  my $prtBlackHCFA = qq|<A HREF="javascript:ReportWindow('/cgi/bin/printHCFA.pl?TrIDs=$r->{TrID}&InsID=$rxSC->{InsID}&HCFAtype=black&${addLinks}','HCFAB')" TITLE="Click here to <BR>generate HCFA 1500 on blank paper <BR>for $r->{TrID}" ><IMG SRC="/img/print-ok.png" HEIGHT="21" WIDTH="21" BORDER="0" ></A>|;
  my $prtRedHCFA = qq|<A HREF="javascript:ReportWindow('/cgi/bin/printHCFA.pl?TrIDs=$r->{TrID}&InsID=$rxSC->{InsID}&HCFAtype=red&${addLinks}','HCFAR')" TITLE="Click here to <BR>generate HCFA 1500 on pre-printed forms <BR>for $r->{TrID}" ><IMG SRC="/img/print-ok.png" HEIGHT="21" WIDTH="21" BORDER="0" ></A>|;
  my $Remarks = '';
  if ( $BillingRemitACCESS )
  {
    if ( $sClientInsRemarksDetail->execute($r->{TrID}) )
    {
      if ( my $rClientInsRemarksDetail = $sClientInsRemarksDetail->fetchrow_hashref )
      { $Remarks = qq|<A HREF="javascript:ReportWindow('/cgi/bin/disHTML.cgi?${addLinks}&IDs=$rClientInsRemarksDetail->{ID}&action=ClientInsRemarksDetail&page=HTMLText','PrintWindow',1000,1440)" TITLE="Click here to view." ><IMG SRC="/images/note.jpg" BORDER="5" ></A>|; }
    }
  }
  my ($NoteNmbrLink, $NotePrintLink, $NoteCCDALink) = ('','','');
  $NoteNmbrLink = qq|<A HREF="/cgi/bin/mis.cgi?MIS_Action=Note&Client_ClientID=$r->{ClientID}&Treatment_TrID=$r->{TrID}&${addLinks}&pushID=$form->{LINKID}" TITLE="${TrIDMesg} <BR>Click here to <BR>Edit Note $r->{TrID}" >${NoteIMG}|;
  $NotePrintLink .= qq|<A HREF="javascript:ReportWindow('/cgi/bin/printNotes.pl?TrIDs=$r->{TrID}&${addLinks}','printNote')" TITLE="Click here to <BR>New print Note $r->{TrID} as pdf file." ><IMG SRC="/images/adobelogo_bt.gif" BORDER="0" HEIGHT="18" WIDTH="18" ></A>|;
  $NotePrintLink .= qq|<A HREF="javascript:ReportWindow('$r->{Path}','PrintNote')" TITLE="Click here to <BR>Print the attachment for Note $r->{TrID}." ><IMG SRC="/images/paperclip_black.png" BORDER="0" HEIGHT="18" WIDTH="18" ></A>| if ( $r->{'Type'} == 3 );
  $NoteCCDALink = qq|<A HREF="javascript:ReportWindow('/cgi/bin/genCCDA.pl?ProvID=$r->{ProvID}&ClientID=$r->{ClientID}&TrIDs=$r->{TrID}&${addLinks}','genCCDA',500,1200)" TITLE="Click here to <BR>generate the CCDA." ><IMG SRC="/img/document-export.png" HEIGHT="21" WIDTH="21" BORDER="0" ></A>| if ( $AgentACCESS );
  $NoteAmendLink = qq|<A HREF="javascript:ReportWindow('/cgi/bin/mis.cgi?view=ClientNoteAmendmentInp.cgi&Client_ClientID=$r->{ClientID}&Treatment_TrID=$r->{TrID}&${addLinks}','setNoteAmend')" TITLE="Click here to <BR>add or update the Ammendment to this note." ><IMG SRC="/img/notepad-info.png" HEIGHT="21" WIDTH="21" BORDER="0" ></A><BR>| if ( $AgentACCESS );
  my ($PrAuthLink) = ('');
  if ( $r->{PrAuthID} )
  { $PrAuthLink = qq|<A HREF="javascript:ReportWindow('/cgi/bin/printClientPrAuth.cgi?IDs=$r->{PrAuthID}&mlt=$form->{mlt}','PrAuth')" TITLE="Click here to <BR>print the Prior Authorization this Note is associated with." >$r->{PrAuthID}</A>|; }
#warn qq|ChartList: SCID=$rxSC->{SCID}, InsDescr=$rxSC->{InsDescr}\n|;
#warn qq|ChartList: Priority=$rInsurance->{Priority}, InsID=$rInsurance->{InsID}/$rxSC->{InsID}, InsDescr=$rxSC->{InsDescr}\n|;
  (my $CredDescr = DBA->getxref($form,'xCredentials',$rxSC->{CredID},'Descr')) =~ s/'//g;
  my $Priority = $rInsurance->{'Priority'} == 1 ? 'Primary' 
               : $rInsurance->{'Priority'} == 2 ? 'Secondary'
               : $rInsurance->{'Priority'} == 3 ? 'Tertiary' : 'NoPriority';
  (my $scpopup = qq|${Priority} $rxSC->{InsName} <BR>[$rInsurance->{InsIDNum}] <BR>$rxSC->{SCName} <BR>[$CredDescr]|) =~ s/'/\\'/g;
  $out .= qq|
  <TR ${class} >
    <TD >${ClientPageAcc}</TD>
    <TD >${NoteNmbrLink}<FONT COLOR=${TrIDColor} >$r->{TrID}</FONT></A><BR>${UnReviewLabel} ${UnReviewButton}</TD>
    <TD >${NotePrintLink} ${NoteAmendLink} ${NoteCCDALink}</TD>
    <TD >${PrAuthLink}</TD>
    <TD >${ContLogDate}</TD>
    <TD ><A HREF="javascript:void(0)" TITLE="${scpopup}" >$rxSC->{SCNum}</A></TD>
    <TD >${Progress}</TD>
    <TD >$r->{Units}</TD>
    <TD >${ContLogBegTime}</TD>
    <TD >${ContLogEndTime}</TD>
    <TD >${BillDate}</TD>
    <TD >${BillStatus}${adjNoteURL}</TD>
    <TD >${StatusDate}</TD>
    <TD >${AmtDueButton}</TD>
    <TD >${prtBlackHCFA} ${prtRedHCFA} ${Remarks}</TD>
  </TR>
|;
  $printstr .= qq|
  <TR >
    <TD ALIGN="left" >$r->{LName}</TD>
    <TD ALIGN="left" >$r->{FName}</TD>
    <TD ALIGN="right" >$r->{ClientID}</TD>
    <TD ALIGN="right" >$r->{TrID}</TD>
    <TD ALIGN="left" >${TrIDMesg}</TD>
    <TD ALIGN="center" >${ContLogDate}</TD>
    <TD ALIGN="center" >$rxSC->{SCNum}</TD>
    <TD ALIGN="center" >${Progress}</TD>
    <TD ALIGN="right" >$r->{Units}</TD>
    <TD ALIGN="center" >${ContLogBegTime}</TD>
    <TD ALIGN="center" >${ContLogEndTime}</TD>
    <TD ALIGN="center" >${BillDate}</TD>
    <TD ALIGN="center" >${BillStatus}</TD>
    <TD ALIGN="center" >${StatusDate}</TD>
    <TD ALIGN="right" >${AmtDue}</TD>
  </TR>
|;
  return($out);
}
############################################################################
sub prtNoteTrans
{
  my ($self,$count,$r) = @_;
  my $out = '';
  my $class = qq|CLASS=alternate2|;
  my $NoteTransCnt = 0;
#warn qq|TrID=$r->{TrID}\n|;
  $sNoteTrans->execute($r->{TrID});
  while ( $rNoteTrans = $sNoteTrans->fetchrow_hashref )
  {
    $NoteTransCnt+=1;
#warn qq|ID=$rNoteTrans->{ID}\n|;
    my $rxSC = cBill->getServiceCode($form,$rNoteTrans->{SCID},$r->{ContLogDate},$r->{ContLogBegTime},$r->{ContLogEndTime},$r->{TrID});
    my $ICN = $rNoteTrans->{ICN} ? $rNoteTrans->{ICN} : '&nbsp;';
    my $RefID = $rNoteTrans->{RefID} ? $rNoteTrans->{RefID} : '&nbsp;';
    my $ContDate = DBUtil->Date($rNoteTrans->{ContDate},'fmt','MM/DD/YY');
    my $Hours = sprintf("%.2f",$rNoteTrans->{Duration} / 3600);
    my $BillAmt = sprintf("%.2f",$rNoteTrans->{BillAmt});
    my $PaidAmt = sprintf("%.2f",$rNoteTrans->{PaidAmt});
    my $RecDate = DBUtil->Date($rNoteTrans->{RecDate},'fmt','MM/DD/YY');
    my $TCodeDescr = $rNoteTrans->{Code} eq 'ER' ? 'Electronic Reconcile' :
                     $rNoteTrans->{Code} eq 'ER-I' ? 'Electronic Reconcile - from previous ID' :
                     $rNoteTrans->{Code} eq 'ER-T' ? 'Electronic Reconcile - from previous Transaction' :
                     $rNoteTrans->{Code} eq 'ER-R' ? 'Electronic Reconcile - from previous Reconciled transaction' :
                     $rNoteTrans->{Code} eq 'ER-N' ? 'Electronic Reconcile - from Note (no billed transaction)' :
                     $rNoteTrans->{Code} eq 'IR' ? 'Insurance Reconcile' :
                     $rNoteTrans->{Code} eq 'SR' ? 'Scholarship Reconcile' :
                     $rNoteTrans->{Code} eq 'BI' ? 'Billed (inprocess)' :
                     $rNoteTrans->{Code} eq 'AR' ? 'Auto Reconcile' :
                     $rNoteTrans->{Code} eq 'ADJ' ? 'Adjustment' :
                     $rNoteTrans->{Code} eq 'COR' ? 'Correction' :
                     $rNoteTrans->{Code} eq 'FR' ? 'Fix Reconcile' :
                     $rNoteTrans->{Code} eq 'MR' ? 'Manual Reconcile' :
                     $rNoteTrans->{Code} eq 'MD' ? 'Manual Denied' : 'xx';
    my $TCode = $rNoteTrans->{Code} eq '' ? '&nbsp;' : qq|<FONT COLOR="red"><A HREF="javascript:void(0)" TITLE="${TCodeDescr}" >$rNoteTrans->{Code}</A></FONT>|;
    my ($dlm,$ReasonCodes) = ('','&nbsp;');
    my $rcode = $rNoteTrans->{DenCode};
    (my $id = $rcode) =~ s/^\s*(.*?)\s*$/$1/g;              # trim the spaces.
     $id = $id =~ /^A|^B/ ? $id : length($id) == 1 ? '00'.$id : length($id) == 2 ? '0'.$id : $id;
    (my $rcodedescr = DBA->getxref($form,'xDenCodes',$id,'Descr')) =~ s/'//g;
    $ReasonCodes .= qq|<FONT COLOR="red"><A HREF="javascript:void(0)" TITLE="${rcodedescr}" >${dlm}${id}</A></FONT>|;
    $dlm = '<BR>';
    foreach my $rcode ( split('/',$rNoteTrans->{ReasonCode}) )
    {
      (my $id = $rcode) =~ s/^\s*(.*?)\s*$/$1/g;              # trim the spaces.
       $id = $id =~ /^A|^B/ ? $id : length($id) == 1 ? '00'.$id : length($id) == 2 ? '0'.$id : $id;
      (my $rcodedescr = DBA->getxref($form,'xDenCodes',$id,'Descr')) =~ s/'//g;
      $ReasonCodes .= qq|<FONT COLOR="red"><A HREF="javascript:void(0)" TITLE="${rcodedescr}" >${dlm}${id}</A></FONT>|;
      $dlm = '<BR>';
#warn qq|+ =$rNoteTrans->{ReasonCode}: rcode=${rcode}= id=${id}= descr=${rcodedescr}=\n|;
    }
    my $AdjAmt = $rNoteTrans->{Code} eq 'COR' ? 0 : -${PaidAmt};
    my $AdjButton = $PaidAmt == 0 || $rNoteTrans->{Code} =~ /^ER/ || $rNoteTrans->{AdjCode} || !$BillingRemitACCESS 
                    ? "\$${PaidAmt}"
                    : qq| <INPUT TYPE="submit" ONCLICK="return vAdjust(this.form,'$rNoteTrans->{ID}','$r->{TrID}','${AdjAmt}')" NAME="ADJUST" VALUE="\$${PaidAmt}" >|;
    my $DenyButton = $rNoteTrans->{Code} eq 'BI' && ($AgentACCESS || $BillingAdmin)
                     ? qq| <A HREF="javascript:void(0)" TITLE="Click here to Deny this transaction." > <INPUT TYPE="submit" ONCLICK="return vDenyNote(this.form,'$rNoteTrans->{ID}','$r->{TrID}','$r->{ClientID}','$r->{ContLogDate}','$rNoteTrans->{SCNum}','$rNoteTrans->{Code}')" NAME="DENYNOTE" VALUE="DenyNote" > </A> | : '';
##
# can align text in sort:      <TD STYLE="text-align:right" >${NoteTransCnt}.</TD>
##
    (my $scntpopup = qq|$rxSC->{InsDescr} <BR>$rxSC->{SCName}|) =~ s/'/\\'/g;
    $sxInsurance->execute($rNoteTrans->{PayerID});
    $rxInsurance = $sxInsurance->fetchrow_hashref;
    (my $refppopup = qq|$rxInsurance->{Name}|) =~ s/'/\\'/g;
    $out .= qq|
    <TR ${class} >
      <TD >&nbsp;</TD>
      <TD >&nbsp;</TD>
      <TD >&nbsp;</TD>
      <TD >$rNoteTrans->{ID}</TD>
      <TD >${ContDate}</TD>
      <TD ><A HREF="javascript:void(0)" TITLE="${scntpopup}" >$rNoteTrans->{SCNum}</A></TD>
      <TD ><A HREF="javascript:void(0)" TITLE="${refppopup}" >${RefID}</A></TD>
      <TD >$rNoteTrans->{Units}</TD>
      <TD >${ICN}</TD>
      <TD >${Hours}Hrs</TD>
      <TD >\$${BillAmt}</TD>
      <TD >${AdjButton}</TD>
      <TD >${RecDate}</TD>
      <TD >${ReasonCodes}</TD>
      <TD >${TCode} ${DenyButton}</TD>
    </TR>
|;
    $printstr .= qq|
    <TR >
      <TD ALIGN=center >&nbsp;</TD>
      <TD ALIGN=right >#${NoteTransCnt}.</TD>
      <TD ALIGN=right >$rNoteTrans->{ID}</TD>
      <TD ALIGN=right >$r->{TrID}</TD>
      <TD ALIGN=center >&nbsp;</TD>
      <TD ALIGN=center >${ContDate}</TD>
      <TD ALIGN=center >$rNoteTrans->{SCNum}</TD>
      <TD ALIGN=center >${RefID}</TD>
      <TD ALIGN=right >$rNoteTrans->{Units}</TD>
      <TD ALIGN=center >${ICN}</TD>
      <TD ALIGN=right >${Hours}</TD>
      <TD ALIGN=right >\$${BillAmt}</TD>
      <TD ALIGN=right >\$${PaidAmt}</TD>
      <TD ALIGN=center >${RecDate}</TD>
      <TD ALIGN=center >${ReasonCodes}</TD>
      <TD ALIGN=center >${TCodeDescr}</TD>
    </TR>
|;
  }
  return($out);
}
############################################################################
sub adjTrans
{
  my ($self,$form,$id,$amt,$reason) = @_;
  my $code = 0;
  my $sNoteTrans = $dbh->prepare("select * from NoteTrans where ID=?");
  $sNoteTrans->execute($id);
  if ( my $rNoteTrans = $sNoteTrans->fetchrow_hashref )
  {
#warn qq|adjTrans: $id, $amt, $reason\n|;
#warn qq|adjTrans: $rNoteTrans->{ID}, $rNoteTrans->{PaidAmt}\n|;
     $code = 1;
     my $InsPaidID = $rNoteTrans->{'InsPaidID'};
     my $InsPaidAMT = $rNoteTrans->{'PaidAmt'};
     if ( $amt == 0 )
     {
       my $sZeroTrans = $dbh->prepare("update NoteTrans set PaidAmt=0, Code='COR' where ID=?");
       $sZeroTrans->execute($id);
       $sZeroTrans->finish();
       my $sAdjTrans = $dbh->prepare("update NoteTrans set AdjCode=0 where ID=?");
       $sAdjTrans->execute($rNoteTrans->{RefID});   # set it so they can adjust the associated transaction.
       $sAdjTrans->finish();
#warn qq|adjTrans: $id, ZERO: $rNoteTrans->{TrID}: $amt\n|;
     }
     else
     {
#warn qq|adjTrans: $id, INSERT: $rNoteTrans->{TrID}: $amt, $reason\n|;
       $rNoteTrans->{RefID} = $id;                  # backward link
#warn qq|adjTrans: $id, 1=RefID=$rNoteTrans->{RefID}\n|;
       $rNoteTrans->{ICN} = $reason;                # Note/Reason.
       $rNoteTrans->{BillAmt} = 0;                  # 2nd transaction, 0 billed amount
       $rNoteTrans->{RecDate} = $form->{TODAY};
       $rNoteTrans->{PaidAmt} = $amt;
       $rNoteTrans->{Code} = 'COR';
       $rNoteTrans->{SRC} = 'MA';
       $rNoteTrans->{InsPaidID} = $InsPaidID;       # reverse/backout negative amount
       $rNoteTrans->{CreateDate} = $form->{TODAY};
       $rNoteTrans->{CreateProvID} = $form->{LOGINPROVID};
       $rNoteTrans->{ChangeProvID} = $form->{LOGINPROVID};
       delete $rNoteTrans->{ID};
       delete $rNoteTrans->{DenCode};
       delete $rNoteTrans->{ReasonCode};
       delete $rNoteTrans->{ChangeDate};            # this ones a timestamp.
#warn qq|adjTrans: $id, 2=RefID=$rNoteTrans->{RefID}\n|;
       DBA->xSQL($form,'insert','NoteTrans',$rNoteTrans);
       my $sAdjTrans = $dbh->prepare("update NoteTrans set AdjCode=1 where ID=?");
       $sAdjTrans->execute($id);
       $sAdjTrans->finish();
     }
#warn qq|adjTrans: TrID=$rNoteTrans->{'TrID'}\n|;
     # fix these adjusted amounts and status...
     my ($BilledAmt,$IncAmt,$SchAmt,$AmtDue) = uBill->setBilledAmt($form,$rNoteTrans->{'TrID'});
#warn qq|adjTrans: BilledAmt=$BilledAmt, IncAmt=$IncAmt, SchAmt=$SchAmt, AmtDue=$AmtDue\n|;
     uBill->fixBillStatus($form,$rNoteTrans->{TrID},$reason);
     uBill->fixRevStatus($form,$rNoteTrans->{TrID});
     if ( $InsPaidID )
     {
       my $sInsPaid = $dbh->prepare("select * from InsPaid where ID=?");
       $sInsPaid->execute($InsPaidID);
       if ( my $rInsPaid = $sInsPaid->fetchrow_hashref )
       {
         my $sRecInsPaidAmt=$dbh->prepare("update InsPaid set RecAmt=? where ID=?");
         my $RecAmt = $rInsPaid->{RecAmt} - $InsPaidAMT;  # +amt adds back, -amt takes out
#warn qq|adjTrans: InsPaid: ID=$InsPaidID, InsPaidAmt=$InsPaidAMT, RecAmt=$RecAmt\n|;
         $sRecInsPaidAmt->execute($RecAmt,$InsPaidID);
         $sRecInsPaidAmt->finish();
       }
       $sInsPaid->finish();
     }
  }
  $sNoteTrans->finish();
  return($code);
}
########################
# InsPaid lines
########################
sub setInsPaid
{
  my ($self) = @_;
  my $html .= qq|
<FORM NAME="Reconcile" ACTION="/cgi/bin/Reconcile.cgi" METHOD="POST" >
<TABLE CLASS="port fullsize" >
  <TR ><TD COLSPAN="12" >Insurance Payments unreconciled (for notes listed above) ${ClientInsURL}<BR>Wait to apply these to a note until the note is billed/reconciled. If you apply a payment to a note it 'Reconciles' the note and then the note cannot be billed.</TD></TR>
</TABLE>
<TABLE CLASS="chartsort table-autosort table-stripeclass:alternate fullsize">
<THEAD >
  <TR >
    <TH >List</TD>
    <TH CLASS="table-sortable:default" >LName</TD>
    <TH CLASS="table-sortable:default" >FName</TD>
    <TH CLASS="table-sortable:date" >StartDate</TD>
    <TH CLASS="table-sortable:date" >EndDate</TD>
    <TH CLASS="table-sortable:default" >InsCode</TD>
    <TH CLASS="table-sortable:default" >RefID</TD>
    <TH CLASS="table-sortable:date" >TransDate</TD>
    <TH CLASS="table-sortable:currency" >BillAmt</TD>
    <TH CLASS="table-sortable:currency" >PaidAmt</TD>
    <TH CLASS="table-sortable:numeric" >ICN</TD>
    <TH CLASS="table-sortable:currency" >RecAmt</TD>
    <TH >TrID</TD>
    <TH CLASS="table-sortable:currency" >Amount</TD>
  </TR>
</THEAD>
<TBODY>
|;
  my $count = 0;
  my $qInsPaid = qq|select InsPaid.*, Client.LName, Client.FName
    from InsPaid
    left join Client on Client.ClientID=InsPaid.ClientID
    where Client.ClientID=? and PaidAmt!=RecAmt
|;
#warn qq|q=$qInsPaid\n|;
#warn qq|Client_TrIDs=$Client_TrIDs\n|;
  $sInsPaid = $dbh->prepare($qInsPaid);
  foreach my $ClientKey ( sort keys %{ $Client_TrIDs } )
  {
#warn qq|ClientKey=$ClientKey\n|;
    my ($LName,$FName,$ClientID) = split('_',$ClientKey);
    my $ClientList = qq|<A HREF="/cgi/bin/ClientList.cgi?SearchType=ClientID&SearchString=${ClientID}&${addLinks}" ONMOUSEOVER="window.status='Client List this Client only'; return true;" ONMOUSEOUT="window.status='';" ><IMG BORDER=0 ALT="Client-List" SRC="/images/icon_folder.gif" ></A>|;
#warn qq|q=\n$qInsPaid\nClientID=$ClientID\n|;
    $sInsPaid->execute($ClientID);
    while ( $rInsPaid = $sInsPaid->fetchrow_hashref )
    {
      $count+=1;
      my $even = int($count/2) == $count/2 ? '1' : '0';
      my $class = $even ? qq|CLASS="alternate"| : '';
      my $StartDate = DBUtil->Date($rInsPaid->{StartDate},'fmt','MM/DD/YY');
      my $EndDate = DBUtil->Date($rInsPaid->{EndDate},'fmt','MM/DD/YY');
      my $TransDate = DBUtil->Date($rInsPaid->{TransDate},'fmt','MM/DD/YY');
      my $TrIDs = qq|<OPTION SELECTED VALUE="" >unselected|;
      foreach my $TrID ( sort keys %{ $Client_TrIDs->{$ClientKey} } )
      { $TrIDs .= qq|<OPTION VALUE="$TrID" >$TrID|; }
      my $amt = $rInsPaid->{PaidAmt} - $rInsPaid->{RecAmt};
      $sxInsurance->execute($rNoteTrans->{PayerID});
      $rxInsurance = $sxInsurance->fetchrow_hashref;
      (my $refppopup = qq|$rxInsurance->{Name}|) =~ s/'/\\'/g;
      $html .= qq|
  <TR ${class} >
    <TD >${ClientList}</TD>
    <TD >$rInsPaid->{LName}</TD>
    <TD >$rInsPaid->{FName}</TD>
    <TD >${StartDate}</TD>
    <TD >${EndDate}</TD>
    <TD >$rInsPaid->{InsCode}</TD>
    <TD ><A HREF="javascript:void(0)" TITLE="${refppopup}" >$rInsPaid->{RefID}</A></TD>
    <TD >${TransDate}</TD>
    <TD >$rInsPaid->{BillAmt}</TD>
    <TD >$rInsPaid->{PaidAmt}</TD>
    <TD >$rInsPaid->{ICN}</TD>
    <TD >$rInsPaid->{RecAmt}</TD>
    <TD >
      <SELECT NAME="TRID_$rInsPaid->{ID}" >${TrIDs}</SELECT>
    </TD>
    <TD >
      <INPUT TYPE=text NAME="AMT_$rInsPaid->{ID}" VALUE="" ONFOCUS="select" ONCHANGE="return vNum(this,0,${amt})" SIZE=10 >
    </TD>
  </TR>
|;
    }
    $sInsPaid->finish();
  }
  $html .= qq|
</TBODY>
  <TR CLASS="port" >
    <TD COLSPAN="14" >
      <INPUT TYPE="button" ONCLICK="this.form.submit();" VALUE="Reconcile" >
    </TD>
  </TR>
| if ( $count > 0 );
  $html .= qq|
</TABLE>
${hidden}
<INPUT TYPE="hidden" NAME="ForTrID" VALUE="$ForTrID" >
<INPUT TYPE="hidden" NAME="SortOptions" VALUE="${SortOptions}" >
<INPUT TYPE="hidden" NAME="FORMID" VALUE="$form->{FORMID}" >
<INPUT TYPE="hidden" NAME="mlt" VALUE="$form->{mlt}" >
<INPUT TYPE="hidden" NAME="misLINKS" VALUE="$form->{misLINKS}" >
<INPUT TYPE="hidden" NAME="LINKID" VALUE="$form->{LINKID}" >
<INPUT TYPE="hidden" NAME="pushID" VALUE="$form->{LINKID}" >
</FORM >
<P>
|;
  return($html);
}
############################################################################
