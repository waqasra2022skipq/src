#!/usr/bin/perl
use lib '/var/www/okmis/src/lib';
use DBI;
use myForm;
use myDBI;
use DBA;
use DBUtil;
use myHTML;

############################################################################
my $form = myForm->new();
my $dbh  = myDBI->dbconnect( $form->{'DBNAME'} );

# incoming or USERID?
my $THEUSER =
  $form->{'THEUSER'} eq '' ? $form->{'USERLOGINID'} : $form->{'THEUSER'};
warn qq|\nENTER ClientPortal: THEUSER=${THEUSER}\n|;

#foreach my $f ( sort keys %{$form} ) { warn "ClientPortal: form-$f=$form->{$f}\n"; }
my ( $DBNAME, $USERID ) = split( ':', $THEUSER );
warn qq|ClientPortal: DBNAME=${DBNAME}, USERID=${USERID}\n|;
$form->{'Client_ClientID'} = $USERID unless $form->{'Client_ClientID'};
my $ClientID = $form->{'Client_ClientID'};
warn qq|ClientPortal: ClientID=${ClientID}\n|;
my $MailList =
  myHTML->ListSel( $form, 'ShowClientMail', $ClientID, $form->{'LINKID'}, 0 );

# change to the client's database...
$form->{'DBNAME'} = $DBNAME;
warn
qq|ClientPortal: DBNAME=$form->{DBNAME}, ClientID=$form->{Client_ClientID}/${ClientID}\n|;
my $sClient = $dbh->prepare(
"select Client.*,ClientLegal.JOLTS,ClientEmergency.Alert from Client left join ClientLegal on ClientLegal.ClientID=Client.ClientID left join ClientEmergency on ClientEmergency.ClientID=Client.ClientID where Client.ClientID=?"
);
$sClient->execute($ClientID);
my $rClient = $sClient->fetchrow_hashref;
my $Alert =
  $rClient->{Active} ? '' : qq|<FONT COLOR="red" >Discharged Client</FONT>|;
$Alert .=
  $rClient->{Alert} eq ''
  ? ''
  : qq|<BR><FONT COLOR="red" >Alert: $rClient->{Alert}</FONT>|;
my $Age        = DBUtil->Date( $rClient->{DOB}, 'age' );
my $ClientName = $rClient->{Pref};
$ClientName .= " $rClient->{FName}"  if ( $rClient->{FName} );
$ClientName .= " $rClient->{MName}"  if ( $rClient->{MName} );
$ClientName .= " $rClient->{LName}"  if ( $rClient->{LName} );
$ClientName .= " $rClient->{Suffix}" if ( $rClient->{Suffix} );
$ClientName =~ s/'//g;
my $Addr2 = "$rClient->{City}, $rClient->{ST} $rClient->{Zip}";
my $CSZ   = '';

if ( $rClient->{Addr2} ) {
    $Addr2 = $rClient->{Addr2};
    $CSZ   = "$rClient->{City}, $rClient->{ST} $rClient->{Zip}";
}

# get Clinic Name
my $sClinic = $dbh->prepare('select * from Provider where ProvID=?');
$sClinic->execute( $rClient->{clinicClinicID} );
my $rClinic = $sClinic->fetchrow_hashref;
my $Clinic_Name =
    $rClinic->{Name}
  ? $rClinic->{Name}
  : "<FONT COLOR=red>NO CLINIC ASSIGNED</FONT>";

# Set Guardian Information
my $sGuardian =
  $dbh->prepare("select * from ClientFamily where ClientID=? and Guardian=1");
$sGuardian->execute($ClientID);
my $rGuardian    = $sGuardian->fetchrow_hashref;
my $GuardianName = $rGuardian->{Pref};
$GuardianName .= " $rGuardian->{FName}"  if ( $rGuardian->{FName} );
$GuardianName .= " $rGuardian->{MName}"  if ( $rGuardian->{MName} );
$GuardianName .= " $rGuardian->{LName}"  if ( $rGuardian->{LName} );
$GuardianName .= " $rGuardian->{Suffix}" if ( $rGuardian->{Suffix} );
my $GuardianRel =
  DBA->getxref( $form, 'xRelationship', $rGuardian->{Rel}, 'Descr' );
$GuardianName .= '/' . $GuardianRel unless ( $GuardianRel eq '' );
$GuardianNName = $rGuardian->{NName} if ( $rGuardian->{NName} );

# get Primary Provider.
my $sProvider = $dbh->prepare("select * from Provider where ProvID=?");
$sProvider->execute( $rClient->{ProvID} );
my $rProvider = $sProvider->fetchrow_hashref;

#my $PrimaryProvider = $rProvider->{ScreenName} eq '' ? qq|$rProvider->{'FName'} $rProvider->{'LName'} $rProvider->{'Suffix'}|
#                                                     : $rProvider->{'ScreenName'};;
my $PrimaryProvider =
  qq|$rProvider->{'FName'} $rProvider->{'LName'} $rProvider->{'Suffix'}|;
my $MailLink = qq|
<A HREF="/cgi/bin/ClientMail.cgi?Client_ClientID=${ClientID}&mlt=$form->{'mlt'}&misLINKS=$form->{'misLINKS'}">
  <IMG ALT="send mail" SRC="/cgi/images/user-mail.png">
</A>
|;

my $ClientPortalMenu = myHTML->getHTML( $form, 'ClientPortal.menu', 1 );
my $ClientDataInfo   = $form->{'LOGINUSERID'} == 91 ? $THEUSER : '';
$form->{'FORMID'} = $form->getFORMID;

# Start out the display.
## TEST NEW html = CALL
## TEST NEW html = CALL
## TEST NEW html = CALL
my $html = myHTML->new( $form, $title, 'noclock accordion' ) . qq|
<TABLE CLASS="main normsize" >
  <TR ALIGN="center" >
    <TD WIDTH="84%" >
| . myHTML->hdr($form) . qq|
<LINK HREF="|
  . myConfig->cfgfile( 'menuV2.css', 1 )
  . qq|" REL="stylesheet" TYPE="text/css" >
<script src="/cgi/menu/js/menuV2.js" type="text/javascript"></script>
<SCRIPT LANGUAGE="JavaScript" SRC="/cgi/js/vEntry.js"> </SCRIPT>
<SCRIPT LANGUAGE="JavaScript" SRC="/cgi/js/ajaxrequest.js"> </SCRIPT>
<LINK HREF="|
  . myConfig->cfgfile( 'tabcontent/template6/tabcontent.css', 1 )
  . qq|" REL="stylesheet" TYPE="text/css" >
<SCRIPT SRC="|
  . myConfig->cfgfile( 'tabcontent/tabcontent.js', 1 )
  . qq|" TYPE="text/javascript" ></SCRIPT>
<SCRIPT LANGUAGE="JavaScript" TYPE="text/javascript" SRC="/cgi/js/tabs.js"></SCRIPT>
<LINK REL="STYLESHEET" TYPE="text/css" HREF="/cgi/css/tabs.css" />
<FORM NAME="ClientPage" ACTION="/cgi/bin/mis.cgi" METHOD="POST" >
<TABLE CLASS="main normsize" >
  <TR >
    <TD CLASS="strcol" >
      ${ClientName} ($ClientID) $rClient->{'SSN'} $rClient->{'JOLTS'}<BR>Client Page:
    </TD>
    <TD CLASS="info numcol" > ${MailLink}</TD>
  </TR>
</TABLE>
<TABLE CLASS="home normsize" >
  <TR >
    <TD CLASS="hdrcol" >
      <DIV CLASS="port" >Client Menu</DIV>
      <DIV ALIGN="center" ><BR>${ClientPortalMenu}</DIV>
      <DIV ALIGN="center" ><BR>${ClientDataInfo}</DIV>
    </TD>
    <TD CLASS="strcol" >
      <DIV CLASS="port hdrcol" >Current Provider</DIV>
      <DIV >${PrimaryProvider} &nbsp;</DIV>
      <BR>
      <DIV CLASS="port hdrcol" >Name & Address</DIV>
      <DIV >${ClientName} $rClient->{NName} &nbsp;</DIV>
      <DIV >$rClient->{Addr1} &nbsp;</DIV>
      <DIV >${Addr2} &nbsp;</DIV>
      <DIV >${CSZ} &nbsp;</DIV>
      <DIV >${Alert} &nbsp;</DIV>
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

  <TR>
    <TD CLASS="port" COLSPAN="3" >
  <div class="accordionItem">
    <h2>Problems<IMG ALT="down" ID="accordionImageProblems" CLASS="accordionImage" SRC="/images/sorted_down.gif" ></h2>
    <div>
<SPAN ID="ShowClientProblems" >
|
  . myHTML->ListSel( $form, 'ShowClientProblems', $ClientID, $form->{'LINKID'},
    0 )
  . qq|
</SPAN>
    </div>
  </div>
    </TD>
  </TR>

  <TR>
    <TD CLASS="port" COLSPAN="3" >
  <div class="accordionItem">
    <h2>Vital Signs<IMG ALT="down" ID="accordionImageVitalSigns" CLASS="accordionImage" SRC="/images/sorted_down.gif" ></h2>
    <div>
<SPAN ID="ShowClientVitalSigns" >
|
  . myHTML->ListSel( $form, 'ShowClientVitalSigns', $ClientID,
    $form->{'LINKID'}, 0 )
  . qq|
</SPAN>
    </div>
  </div>
    </TD>
  </TR>

  <TR>
    <TD CLASS="port" COLSPAN="3" >
  <div class="accordionItem">
    <h2>Past Visit Summaries<IMG ALT="down" ID="accordionImageVisit" CLASS="accordionImage" SRC="/images/sorted_down.gif" ></h2>
    <div>
<SPAN ID="ShowClientNotes" >
|
  . myHTML->ListSel( $form, 'ShowClientNotes', $ClientID, $form->{'LINKID'}, 0 )
  . qq|
</SPAN>
    </div>
  </div>
    </TD>
  </TR>

  <TR>
    <TD CLASS="port" COLSPAN="3" >
  <div class="accordionItem">
    <h2>Secure Mail to Provider<IMG ALT="down" ID="accordionImageMail" CLASS="accordionImage" SRC="/images/sorted_down.gif" ></h2>
    <div>
<SPAN ID="ShowClientMail" >
| . ${MailList} . qq|
</SPAN>
    </div>
  </div>
    </TD>
  </TR>
</TABLE>
|;
$sClient->finish();
$sClinic->finish();
$sGuardian->finish();
$sProvider->finish();
myDBI->cleanup();
print $html;
exit;
############################################################################
