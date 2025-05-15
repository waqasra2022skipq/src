#!C:/Strawberry/perl/bin/perl.exe
############################################################################
use lib 'C:/xampp/htdocs/src/lib';
use CGI::Carp qw(warningsToBrowser fatalsToBrowser);

use DBI;
use myForm;
use myDBI;
use SysAccess;
use DBA;
use DBUtil;
use myHTML;
use gHTML;
use uHTML;

############################################################################
my $form     = myForm->new();
my $dbh      = myDBI->dbconnect( $form->{'DBNAME'} );
my $ClientID = $form->{'Client_ClientID'};

if ( !$form->{Client_ClientID} ) {
    myDBI->error("Client Page / denied ClientID NULL");
}
if ( !SysAccess->verify( $form, 'hasClientAccess' ) ) {
    myDBI->error(
"Client Access Page / Not Client\nPossible duplicate client exists\nContact Clinical Manager or the MIS Help Desk for assistance or access."
    );
}

myForm->pushLINK();                       # save this link/page to return to.
my $addLinks = qq|mlt=$form->{mlt}&misLINKS=$form->{misLINKS}|;
my $BackLinks =
  gHTML->setLINKS( $form, 'back', 2 );    # don't pop back to here on this page.
my $ClientInfo     = SysAccess->chkPriv( $form, 'ClientInfo' );
my $NewClient      = SysAccess->chkPriv( $form, 'NewClient' );
my $BillingReports = SysAccess->chkPriv( $form, 'BillingReports' );

#foreach my $f ( sort keys %{$form} ) { warn "ClientPage: form-$f=$form->{$f}\n"; }
############################################################################
# get Client record for summary output.
$stmt =
qq|select Client.*,ClientLegal.JOLTS,ClientEmergency.Alert, ClientEmergency.HospiceCheck from Client left join ClientLegal on ClientLegal.ClientID=Client.ClientID left join ClientEmergency on ClientEmergency.ClientID=Client.ClientID where Client.ClientID=?|;
$sClient = $dbh->prepare($stmt);
$sClient->execute( $form->{Client_ClientID} );
$rClient = $sClient->fetchrow_hashref;
my $Alert =
  $rClient->{Active} ? '' : qq|<FONT COLOR="red" >Discharged Client</FONT>|;

if ( $rClient->{HospiceCheck} == 1 ) {
    $Alert .=
      $rClient->{Alert} eq ''
      ? ''
      : qq|<BR><FONT COLOR="red" >Alert: *HOSPICE* $rClient->{Alert}</FONT>|;
}
else {
    $Alert .=
      $rClient->{Alert} eq ''
      ? ''
      : qq|<BR><FONT COLOR="red" >Alert: $rClient->{Alert}</FONT>|;
}

my $Age        = DBUtil->Date( $rClient->{DOB}, 'age' );
my $ClientName = $rClient->{Pref};
$ClientName .= " $rClient->{FName}"  if ( $rClient->{FName} );
$ClientName .= " $rClient->{MName}"  if ( $rClient->{MName} );
$ClientName .= " $rClient->{LName}"  if ( $rClient->{LName} );
$ClientName .= " $rClient->{Suffix}" if ( $rClient->{Suffix} );
$ClientName =~ s/'//g;
if ( $rClient->{Addr2} ) {
    $Addr2 = $rClient->{Addr2};
    $CSZ   = "$rClient->{City}, $rClient->{ST} $rClient->{Zip}";
}
else {
    $Addr2 = "$rClient->{City}, $rClient->{ST} $rClient->{Zip}";
    $CSZ   = '';
}
my $DOB    = DBUtil->Date( $rClient->{DOB}, 'fmt', 'MM/DD/YYYY' );
my $DOBSSN = $BillingReports ? qq|${DOB} $rClient->{'SSN'}| : '';
my $chgSSN = $NewClient
  ? qq|
          <A HREF="javascript:ReportWindow('/src/cgi/bin/chgSSN.cgi?ClientID=$rClient->{'ClientID'}&mlt=$form->{mlt}','PrintWindow')" TITLE="Click here to change the Social Security Number (SSN)" >
            $rClient->{'SSN'}
            <IMG SRC="/src/img/tab-edit.png" ALT="" BORDER="0" HEIGHT="20" WIDTH="20" >
          </A>
           |
  : qq|
            $rClient->{'SSN'}
           |;

# get Clinic Name
$sClinic = $dbh->prepare('select * from Provider where ProvID=?');
$sClinic->execute( $rClient->{clinicClinicID} );
$rClinic = $sClinic->fetchrow_hashref;
$Clinic_Name =
    $rClinic->{Name}
  ? $rClinic->{Name}
  : "<FONT COLOR=red>NO CLINIC ASSIGNED</FONT>";

# get Primary Insurance record for Demographic Information.
$stmt       = qq|select * from Insurance where ClientID=? and Priority=1|;
$sInsurance = $dbh->prepare($stmt);
$sInsurance->execute( $form->{Client_ClientID} );
$rInsurance = $sInsurance->fetchrow_hashref;
$form->{Insurance_InsNumID} = $rInsurance->{InsNumID};

# Set Guardian Information
$qGuardian = qq|select * from ClientFamily where ClientID=? and Guardian=1|;
$sGuardian = $dbh->prepare($qGuardian);
$sGuardian->execute( $form->{Client_ClientID} );
$rGuardian    = $sGuardian->fetchrow_hashref;
$GuardianName = $rGuardian->{Pref};
$GuardianName .= " $rGuardian->{FName}"  if ( $rGuardian->{FName} );
$GuardianName .= " $rGuardian->{MName}"  if ( $rGuardian->{MName} );
$GuardianName .= " $rGuardian->{LName}"  if ( $rGuardian->{LName} );
$GuardianName .= " $rGuardian->{Suffix}" if ( $rGuardian->{Suffix} );
my $GuardianRel =
  DBA->getxref( $form, 'xRelationship', $rGuardian->{Rel}, 'Descr' );
$GuardianName .= '/' . $GuardianRel unless ( $GuardianRel eq '' );
$GuardianNName = $rGuardian->{NName} if ( $rGuardian->{NName} );

#DBA->lockTrPlan($form,$form->{Client_ClientID});    # make sure all PGs are locked for this ClientID...

# get Primary Provider.
$stmt      = qq|select * from Provider where ProvID=?|;
$sProvider = $dbh->prepare($stmt);
$sProvider->execute( $rClient->{ProvID} );
$rProvider = $sProvider->fetchrow_hashref;
my $PrimaryProvider =
  $rProvider->{ScreenName} eq ''
  ? qq|$rProvider->{'FName'} $rProvider->{'LName'} $rProvider->{'Suffix'}|
  : $rProvider->{'ScreenName'};

# login provider is a Physician
my $Physician = DBA->isPhysician($form);

# Add a new note button...
my $AddNote =
  $ClientInfo
  ? qq|     <SCRIPT type="text/javascript" >newtextMsg('ClientNote','Use this button to enter a new note for ${ClientName}.');</SCRIPT> <A HREF="/src/cgi/bin/mis.cgi?MIS_Action=Note&Client_ClientID=$form->{Client_ClientID}&Treatment_TrID=new&${addLinks}" ONMOUSEOVER="textMsg.show('ClientNote');" ONMOUSEOUT="textMsg.hide()" ><IMG BORDER=0 SRC="/src/images/edit.gif" WIDTH="35" HEIGHT="35" ></A>|
  : '';
my $PhysNote =
  $Physician
  ? qq|     <A HREF="/src/cgi/bin/mis.cgi?MIS_Action=Note&NoteType=2&Client_ClientID=$form->{Client_ClientID}&Treatment_TrID=new&${addLinks}" ONMOUSEOVER="textMsg.show('physnote')" ONMOUSEOUT="textMsg.hide()" > <IMG SRC="/src/cgi/images/caduceuswhite.png" WIDTH="24" HEIGHT="24" > </A>|
  : '';

############################################################################
# output the HTML
$form->{Client_Age} = $Age;    # set for getHTML.
my $ClientPageMenu =
  $ClientInfo ? myHTML->getHTML( $form, 'ClientPage.menu', 1 ) : '';
$form->{'FORMID'} = myDBI->getFORMID($form);

my $medAlerts = '';

#warn qq|ClientPage: CHECK setClientRuleAlerts\n|;
PostUpd->setClientRuleAlerts( $form, $ClientID );
$medAlerts = uHTML->hClientRuleAlerts( $form, $ClientID );
if ( $medAlerts ne '' ) {
    $sClientRuleAlerts =
      $dbh->prepare("select count(*) from ClientRuleAlerts where ClientID=?");
    $sClientRuleAlerts->execute($ClientID);
    my ($cnt) = $sClientRuleAlerts->fetchrow_array;

    #warn qq|medAlerts: cnt=${cnt}\n|;
    $Alert .= qq|
      <A HREF="javascript: myMedAlerts(500,600);" ><FONT COLOR="red" >${cnt} Medical Alerts</FONT></A>
|;
    $sClientRuleAlerts->finish();
}

# Start out the display.
my $html =
  myHTML->newHTML( $form, 'Client Page',
    'clock mail managertree collapseipad mismenu' )
  . qq|
<LINK HREF="|
  . myConfig->cfgfile( 'menuV2.css', 1 )
  . qq|" REL="stylesheet" TYPE="text/css" >
<script type="text/javascript" src="/src/cgi/menu/js/menuV2.js" ></script>
<SCRIPT type="text/javascript" SRC="/src/cgi/js/vEntry.js"> </SCRIPT>
<SCRIPT type="text/javascript" SRC="/src/cgi/js/ajaxrequest.js"> </SCRIPT>
<SCRIPT type="text/javascript" >
<!--
function validate(form,ok,no)
{
  if ( ok )
  {
    return confirm("Are you sure you want to " + ok + "? If so, then click the OK button below. If NOT, and you wish to modify the current information, click the Cancel button below and then click the View/Edit button next to the section you want to View or Edit.");
  }
  return true;
}
// -->
</SCRIPT>
<LINK HREF="|
  . myConfig->cfgfile( 'tabcontent/template6/tabcontent.css', 1 )
  . qq|" REL="stylesheet" TYPE="text/css" >
<SCRIPT type="text/javascript" SRC="|
  . myConfig->cfgfile( 'tabcontent/tabcontent.js', 1 )
  . qq|" ></SCRIPT>
<SCRIPT type="text/javascript" SRC="/src/cgi/js/tabs.js"></SCRIPT>
<LINK REL="STYLESHEET" TYPE="text/css" HREF="/src/cgi/css/tabs.css" />
${medAlerts}
<FORM ID="form" NAME="ClientPage" ACTION="/src/cgi/bin/mis.cgi" METHOD="POST" >
<TABLE CLASS="main fullsize" >
  <TR >
    <TD CLASS="strcol" >
      ${ClientName} ($form->{'Client_ClientID'}) ${DOBSSN} $rClient->{'JOLTS'}<BR>Client Page:
    </TD>
    <TD CLASS="info numcol" > ${BackLinks} ${AddNote} ${PhysNote}</TD>
  </TR>
</TABLE>
<SCRIPT type="text/javascript" >newtextMsg('physnote','Use this button to enter a new Physician note for ${ClientName}.');</SCRIPT>
<TABLE CLASS="home fullsize" >
  <TR >
    <TD CLASS="hdrcol" >
      <DIV CLASS="port" >Client Menu</DIV>
      <DIV ALIGN="center" ><BR>${ClientPageMenu}<BR></DIV>
    </TD>
    <TD CLASS="strcol" >
      <DIV CLASS="port hdrcol" >Current Provider</DIV>
      <DIV >${PrimaryProvider} &nbsp;</DIV>
      <BR>
      <DIV CLASS="port hdrcol" >Name & Address</DIV>
      <DIV >${ClientName} $rClient->{'NName'} &nbsp; 
        <SPAN STYLE="float:right;" >${chgSSN}</SPAN>
      </DIV>
      <DIV STYLE="float: left;">
        <DIV >$rClient->{Addr1} &nbsp;</DIV>
        <DIV >${Addr2} &nbsp;</DIV>
        <DIV >${CSZ} &nbsp;</DIV>
      </DIV>
|;
$html .= qq|
      <DIV STYLE="float:right; clear:right;">
        <img src="/src/images/check.jpg" width="20" height="20" style="vertical-align: middle;">
        <span>Verified</span>
      </DIV>
| if $rClient->{addressVerified} eq 1;
$html .= qq|
      <DIV STYLE="clear:both;">${Alert} &nbsp;</DIV>
      <BR>
      <DIV CLASS="port hdrcol" >Guardian Name/Relationship</DIV>
      <DIV >${GuardianName} &nbsp;</DIV>
      <BR>
    </TD>
    <TD CLASS="strcol" >
      <DIV CLASS="port hdrcol" >Assigned Clinic</DIV>
      <DIV >${Clinic_Name} &nbsp;</DIV>
      <BR>
      <DIV CLASS="port hdrcol" >Phone Numbers</DIV>
      <DIV >Home: $rClient->{HmPh}</DIV>
      <DIV >Work: $rClient->{WkPh}</DIV>
      <DIV >Mobile: $rClient->{MobPh}</DIV>
      <DIV >Fax: $rClient->{Fax}</DIV>
      <DIV >Pager: $rClient->{Pgr}</DIV>
      <DIV >$rClient->{OthPhLbl} $rClient->{OthPh} &nbsp;</DIV>
      <DIV >Email: $rClient->{Email}</DIV>
    </TD>
  </TR>
</TABLE>
|;

############################################################################
if ($ClientInfo) {

    # Output the Insurance information.
    #warn qq|ClientPage: ClientID=$form->{'Client_ClientID'}\n|;
    $html .= qq|
<TABLE CLASS="home fullsize" >
  <TR >
    <TD CLASS="hdrtxt" >
      <A HREF="http://forms.okmis.com/misdocs/NewProcedures_TrPlan_Problems_PA.pdf" TARGET="popup" ONCLICK="window.open('http://forms.okmis.com/misdocs/NewProcedures_TrPlan_Problems_PA.pdf', 'popup', 'width=900,height=700,menubar=1,scrollbars=1,toolbar=1,status=1,resizable=1'); return false">Problems/Treatment Plan/Prior Authorizations New Procedures</A>
    </TD>
  </TR>
  <TR >
    <TD CLASS="port hdrcol" >
      Client Problems
      <A HREF="javascript:callAjax('ListClientProblems','','ListClientProblems','&active=1&Locked=0&Client_ClientID=$form->{'Client_ClientID'}&LOGINPROVID=$form->{'LOGINPROVID'}&LOGINUSERID=$form->{'LOGINUSERID'}&LOGINUSERDB=$form->{'LOGINUSERDB'}&mlt=$form->{'mlt'}&LINKID=$form->{'LINKID'}','popup.pl');" TITLE="Show ONLY Active Problems for Client" >Active Only</A>
      /
      <A HREF="javascript:callAjax('ListClientProblems','','ListClientProblems','&active=0&Locked=0&Client_ClientID=$form->{'Client_ClientID'}&LOGINPROVID=$form->{'LOGINPROVID'}&LOGINUSERID=$form->{'LOGINUSERID'}&LOGINUSERDB=$form->{'LOGINUSERDB'}&mlt=$form->{'mlt'}&LINKID=$form->{'LINKID'}','popup.pl');" TITLE="Show ALL Problems for Client" >Show All</A>
    </TD>
  </TR>
  <TR>
    <TD CLASS="port" >
<SPAN ID="ListClientProblems" >
|
      . myHTML->ListSel( $form, 'ListClientProblems',
        $form->{'Client_ClientID'},
        $form->{'LINKID'}, 0 )
      . qq|
</SPAN>
    </TD>
  </TR>
  <TR>
    <TD CLASS="port" >
<SPAN ID="ListClientTrPlan$form->{'FULL'}" >
|
      . myHTML->ListSel(
        $form,
        "ListClientTrPlan$form->{'FULL'}",
        $form->{'Client_ClientID'},
        $form->{'LINKID'}, 0
      )
      . qq|
</SPAN>
    </TD>
  </TR>
  <TR>
    <TD CLASS="port hdrcol" >
      <BR>To Display ALL the Treatment Plans click on the button below.
      <BR><INPUT TYPE="button" VALUE="List All Treatment Plans" ONCLICK="window.location='/cgi/bin/ClientPage.cgi?Client_ClientID=$form->{Client_ClientID}&FULL=ALL&mlt=$form->{mlt}&misLINKS=$form->{misLINKS}'">
    </TD>
  </TR>
</TABLE>
<TABLE CLASS="home fullsize" >
  <TR>
    <TD CLASS="port" >
<SPAN ID="ListClientInsurance$form->{'FULL'}" >
|
      . myHTML->ListSel(
        $form,
        "ListClientInsurance$form->{'FULL'}",
        $form->{'Client_ClientID'},
        $form->{'LINKID'}, 0
      )
      . qq|
</SPAN>
    </TD>
  </TR>
</TABLE>
|;

    # Output the bottom information.
    $html .= qq|
<TABLE CLASS="home fullsize" >
  <TR>
    <TD CLASS="port hdrcol" >
      <B>Outpatient Request for Prior Authorization</B>
      <BR>Prior Authorizations, Initial, and Extensions all describe the PA Packet.
      <BR>The PA Packet is layed out underneath each Prior Authorization above.
      <BR>Use the 'Add New' button to the right of the 'Prior Authorization' header 
      <BR>to add a Initial or New Extension.
      <BR>To modify the current Authorization, RVUs, Goals and CARS Scores
      <BR>use the 'View/Edit' button next to each.
      <BR>To PRINT the PA Packet 'Click On' the print icon link next to 'TransType'.
      <BR>Prior Authorizations are displayed listing the last 5 entered by date.
      <BR>To Display all the Prior Authorizations click on the button below.
      <BR><INPUT TYPE="button" VALUE="List All Prior Authorizations" ONCLICK="window.location='/src/cgi/bin/ClientPage.cgi?Client_ClientID=$form->{Client_ClientID}&FULL=ALL&mlt=$form->{mlt}&misLINKS=$form->{misLINKS}'">
    </TD>
  </TR>
</TABLE>
|;
}

$html .= qq|
<INPUT TYPE="hidden" NAME="mlt" VALUE="$form->{mlt}" >
<INPUT TYPE="hidden" NAME="FORMID" VALUE="$form->{FORMID}" >
<INPUT TYPE="hidden" NAME="LINKID" VALUE="$form->{LINKID}" >
<INPUT TYPE="hidden" NAME="misLINKS" VALUE="$form->{misLINKS}" >
</FORM>
| . myHTML->rightpane( $form, 'search' );

##
# Close the SQL statments.
$sClient->finish();
$sClinic->finish();
$sInsurance->finish();
$sGuardian->finish();
$sProvider->finish();

myDBI->cleanup();
print $html;
exit;
############################################################################
