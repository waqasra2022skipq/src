#!/usr/bin/perl
############################################################################
use lib '/var/www/okmis/src/lib';
use CGI qw(:standard escape);
use DBI;
use myForm;
use myDBI;
use SysAccess;
use myHTML;
use gHTML;

############################################################################
#my $form = DBForm->new();
my $form = myForm->new();
my $dbh  = myDBI->dbconnect( $form->{'DBNAME'} );
myForm->pushLINK();    # save this link/page to return to.

#warn qq|ProviderPage: ENTER\n|;

# Access Required.
if ( !$form->{Provider_ProvID} ) {
    myDBI->error("Provider Page / denied ProvID NULL");
}
if ( !SysAccess->verify( $form, 'hasProviderAccess' ) ) {
    myDBI->error("Provider Page / denied Provider Access");
}

#############################################################################
$backURL = "/cgi/bin/mis.cgi?MIS_Action=MgrTree&mlt=$form->{mlt}";
my $BackLinks =
  gHTML->setLINKS( $form, 'back', 2 );    # don't pop back to here on this page.

############################################################################
# get Provider record for summary output.
my $sProvider = $dbh->prepare("select * from Provider where ProvID=?");
$sProvider->execute( $form->{Provider_ProvID} );
my $rProvider = $sProvider->fetchrow_hashref;
my $sProviderControl =
  $dbh->prepare("select * from ProviderControl where ProvID=?");
$sProviderControl->execute( $form->{Provider_ProvID} );
my $rProviderControl = $sProviderControl->fetchrow_hashref;
$sEmplInfo = $dbh->prepare("select * from EmplInfo where ProvID=?");
$sEmplInfo->execute( $form->{Provider_ProvID} );
$rEmplInfo = $sEmplInfo->fetchrow_hashref;
my $Alert =
  $rEmplInfo->{Alert} eq ''
  ? ''
  : qq|<BR><FONT COLOR="red" >Alert: $rEmplInfo->{Alert}</FONT>|;
$sEmplInfo->finish();
my $sProviderHrs = $dbh->prepare("select * from ProviderHrs where ProvID=?");
$sProviderHrs->execute( $form->{Provider_ProvID} );
my $rProviderHrs = $sProviderHrs->fetchrow_hashref;
my $ClinicName =
  $rProvider->{'Name'} eq ''
  ? ''
  : qq|      <DIV > $rProvider->{Name} &nbsp;</DIV>|;
my $ProvName = $rProvider->{Prefix};
$ProvName .= " $rProvider->{FName}"  if ( $rProvider->{FName} );
$ProvName .= " $rProvider->{LName}"  if ( $rProvider->{LName} );
$ProvName .= " $rProvider->{Suffix}" if ( $rProvider->{Suffix} );

if ( $rProvider->{Addr2} ) {
    $Addr2 = $rProvider->{Addr2};
    $CSZ   = "$rProvider->{City}, $rProvider->{ST} $rProvider->{Zip}";
}
else {
    $Addr2 = "$rProvider->{City}, $rProvider->{ST} $rProvider->{Zip}";
    $CSZ   = '';
}
$Active = $rProvider->{Active} ? 'Active' : 'InActive';

my $PageDescr = qq|NO TYPE|;
if ( $rProvider->{Type} == 1 ) {
    $PageDescr = qq|$rProvider->{'Name'}<BR>Group/Association Page|;
}
elsif ( $rProvider->{Type} == 2 ) {
    $PageDescr = qq|$rProvider->{'Name'}<BR>Agency Page|;
}
elsif ( $rProvider->{Type} == 3 ) {
    $PageDescr = qq|$rProvider->{'Name'}<BR>Clinic Page|;
}
elsif ( $rProvider->{Type} == 4 ) {
    $PageDescr = qq|${ProvName}<BR>Provider Page|;
}

my $Agent        = SysAccess->verify( $form, 'Privilege=Agent' );
my $ProviderInfo = SysAccess->verify( $form, 'Privilege=ProviderInfo' );
my $ProviderSelf = SysAccess->verify( $form, 'Privilege=ProviderSelf' );

#warn qq|ProviderPage: ProviderInfo=$ProviderInfo, ProviderSelf=$ProviderSelf\n|;
# Start out the display.
my $html = myHTML->newHTML(
    $form,
    'Provider Page',
    'clock mail managertree collapseipad mismenu checkinputwindow'
  )
  . qq|
<LINK HREF="|
  . myConfig->cfgfile( 'menuV2.css', 1 )
  . qq|" REL="stylesheet" TYPE="text/css" >
<script src="/cgi/menu/js/menuV2.js" type="text/javascript"></script>
<SCRIPT LANGUAGE="JavaScript" SRC="/cgi/js/vEntry.js"> </SCRIPT>
<SCRIPT LANGUAGE="JavaScript">
<!--
function validate(form)
{ return(1); }
// -->
</SCRIPT>

<FORM NAME="ProviderPage" ACTION="/cgi/bin/mis.cgi" METHOD="POST" >
|;

#warn qq|LOGINPROVID=$form->{LOGINPROVID}\n|;
#warn qq|Agent=$Agent\n|;
#warn qq|ProvID=$form->{Provider_ProvID},$rProvider->{ProvID}\n|;
#warn qq|Type=$rProvider->{Type}\n|;
#warn qq|ProviderSelf=$ProviderSelf\n|;
#warn qq|ProviderInfo=$ProviderInfo\n|;
if (   ( $rProvider->{Type} < 3 && $Agent )
    || ( $form->{Provider_ProvID} == $form->{LOGINPROVID} && $ProviderSelf )
    || ( $form->{Provider_ProvID} != $form->{LOGINPROVID} && $ProviderInfo ) )
{
    $html .= main->updhtml();
}
else { $html .= main->viewhtml(); }
$html .= main->hrshtml() if ( $rProvider->{Type} == 4 );
$html .= myHTML->rightpane( $form, 'search' );

# Close the SQL statments.
$sProvider->finish();
$sProviderControl->finish();
$sProviderHrs->finish();

myDBI->cleanup();
print $html;
exit;

############################################################################
# output the HTML
sub updhtml {
    my ($self) = @_;
    $form->{'FORMID'} = myDBI->getFORMID($form);

# only Agencies should have a scheduler, ProviderPage.menu on displays if Type=2(Agency)

    $form->{provType} = 'Provider';
    $form->{rollUpMessage} =
      'This will roll up Electronic Documents, Provider Credentials';

    if ( $rProvider->{Type} == 2 ) {
        $form->{provType} = 'Agency';
        $form->{rollUpMessage} .= ', Agency Pay and Agency Treatments';

    }
    elsif ( $rProvider->{Type} == 3 ) {
        $form->{provType} = 'Clinic';
        $form->{rollUpMessage} .= ' and Provider(Clinic) Billing';

    }
    elsif ( $rProvider->{Type} == 3 ) {
        $form->{provType} = 'Group/Association';
    }

    $form->{SchedulerPath} =
      $rProviderControl->{'Scheduler'} eq ''
      ? 'NONE'
      : $rProviderControl->{Scheduler};
    my $ProviderPageMenu = myHTML->getHTML( $form, 'ProviderPage.menu', 1 );
    my $out              = qq|
<TABLE CLASS="site fullsize" >
  <TR >
    <TD CLASS="strcol" >${PageDescr} ($form->{Provider_ProvID})</TD>
    <TD CLASS="numcol" >${BackLinks}</TD>
  </TR>
</TABLE>
<TABLE CLASS="home fullsize" >
  <TR >
    <TD CLASS="hdrcol" >
      <DIV CLASS="port" >Provider Menu</DIV>
      <DIV ALIGN="center" ><BR>${ProviderPageMenu}<BR></DIV>
    </TD> | . main->ProvInfo() . qq|
  </TR>
</TABLE>
<P>
|;
    if ( $rProvider->{Type} == 1 ) {
        $out .= qq|<HR WIDTH="90%">|;
        $out .=
          myHTML->ListSel( $form, 'ListSiteMessages', $rProvider->{'ProvID'},
            $form->{'LINKID'}, $rProvider->{'Locked'} );
        $out .=
          myHTML->ListSel( $form, 'ListSiteProjects', $rProvider->{'ProvID'},
            $form->{'LINKID'}, $rProvider->{'Locked'} );
    }
    elsif ( $rProvider->{Type} == 2 ) {
        $out .= qq|<HR WIDTH="90%">|;
        $out .=
          myHTML->ListSel( $form, 'ListAgencyInsurance', $rProvider->{'ProvID'},
            $form->{'LINKID'}, $rProvider->{'Locked'} );
    }
    elsif ( $rProvider->{Type} == 3 ) {
        $out .= qq|<HR WIDTH=90%>
<TABLE CLASS="port fullsize" >
  <TR >
    <TD ALIGN="left" >
      Contracts are needed to bill an insurance.
    </TD>
    <TD ALIGN="right" >
      <A CLASS="port subtitle" HREF="javascript:ReportWindow('http://okmis.helpdocsonline.com/establishing-third-party','HelpWindow')" >Establishing Third Party Insurance Participation</A>
    </TD>
  </TR>
</TABLE>
|;
        $out .=
          myHTML->ListSel( $form, 'ListProviderContracts',
            $rProvider->{'ProvID'},
            $form->{'LINKID'}, $rProvider->{'Locked'} );
    }
    elsif ( $rProvider->{Type} == 4 ) {
        $out .= qq|<HR WIDTH=90%>|;
        $out .=
          myHTML->ListSel( $form, 'ListProviderLicenses',
            $rProvider->{'ProvID'},
            $form->{'LINKID'}, $rProvider->{'Locked'} );
        $out .= qq|<HR WIDTH=90%>|;
        $out .=
          myHTML->ListSel( $form, 'ListProviderCredentials',
            $rProvider->{'ProvID'},
            $form->{'LINKID'}, $rProvider->{'Locked'} );
    }
    $out .= qq|

<INPUT TYPE="hidden" NAME="mlt" VALUE="$form->{mlt}" >
<INPUT TYPE="hidden" NAME="FORMID" VALUE="$form->{FORMID}" >
<INPUT TYPE="hidden" NAME="LINKID" VALUE="$form->{LINKID}" >
<INPUT TYPE="hidden" NAME="misLINKS" VALUE="$form->{misLINKS}" >

</FORM>
|;
    return ($out);
}
############################################################################
# view only
##
sub viewhtml {
    my ($self) = @_;

    my $out = qq|
<TABLE CLASS="site fullsize" >
  <TR >
    <TD CLASS="strcol" >View ${PageDescr} ($form->{Provider_ProvID})</TD>
    <TD CLASS="numcol" >
      <A HREF="${backURL}" ><IMG BORDER=0 ALT="" SRC="/images/chartback.gif" WIDTH=40 HEIGHT=40 ></A>
    </TD>
  </TR>
</TABLE>
<TABLE CLASS="home fullsize" >
  <TR> | . main->ProvInfo() . qq|
  </TR>
</TABLE>
<INPUT TYPE="hidden" NAME="mlt" VALUE="$form->{mlt}" >
<INPUT TYPE="hidden" NAME="FORMID" VALUE="$form->{FORMID}" >
<INPUT TYPE="hidden" NAME="LINKID" VALUE="$form->{LINKID}" >
<INPUT TYPE="hidden" NAME="misLINKS" VALUE="$form->{misLINKS}" >
|;
    return ($out);
}

sub hrshtml {
    my ($self) = @_;
    my $out = qq|
<HR WIDTH="90%" >
<TABLE CLASS="home fullsize" >
  <TR ><TD CLASS="home title" COLSPAN="5" >Vacation / Sick Hours</TD></TR>
  <TR >
    <TD >Accrual Rate</TD>
    <TD >Accrued Hours YTD</TD>
    <TD >Utilized Leave YTD</TD>
    <TD >Credit Hours YTD</TD>
    <TD >Core Work Hours</TD>
  </TR>
  <TR >
    <TD > $rProviderHrs->{AccrRate} </TD>
    <TD > $rProviderHrs->{AccrHrs} </TD>
    <TD > $rProviderHrs->{UtilHrs} </TD>
    <TD > $rProviderHrs->{CredHrs} </TD>
    <TD > $rProviderHrs->{CoreHrs} </TD>
  </TR>
</TABLE>
|;
    return ($out);
}

sub ProvInfo {
    my ($self) = @_;
    my $NoMail = $rProvider->{'NoMail'} ? qq|Turned Off| : '';
    my $out    = qq|
    <TD CLASS="strcol" >
      <DIV CLASS="port hdrtxt" >Name & Address</DIV>
${ClinicName}
      <DIV >${ProvName} $rProvider->{NName} &nbsp;</DIV>
      <DIV STYLE="float:left;" >
        <DIV >$rProvider->{Addr1} &nbsp;</DIV>
        <DIV >${Addr2} &nbsp;</DIV>
        <DIV >${CSZ} &nbsp;</DIV>
      </DIV>
|;
    $out .= qq|
      <DIV STYLE="float:right; clear:right;">
        <img src="/images/check.jpg" width="20" height="20" style="vertical-align: middle;">
        <span>Verified</span>
      </DIV>
| if $rProvider->{addressVerified} eq 1;
    $out .= qq|
      <BR STYLE="clear: both;">
      <DIV CLASS="port hdrtxt" >NPI (ContractZip)</DIV>
      <DIV >$rProviderControl->{NPI} ($rProviderControl->{ContractZip})</DIV>
      <BR>
      <DIV CLASS="port hdrtxt" STYLE="color: red" >Emergency Name/Phone</DIV>
      <DIV >$rProvider->{EmCont}/$rProvider->{EmPh} &nbsp;</DIV>
      <DIV >${Alert} &nbsp;</DIV>
    </TD>
    <TD CLASS="strcol" >
      <DIV CLASS="port hdrtxt" >Phone Numbers</DIV>
      <DIV >Home: $rProvider->{HmPh} &nbsp;</DIV>
      <DIV >Work: $rProvider->{WkPh} &nbsp;</DIV>
      <DIV >Cell: $rProvider->{MobPh} &nbsp;</DIV>
      <DIV >$rProvider->{OthPhLbl} $rProvider->{OthPh} &nbsp;</DIV>
      <DIV >Fax: $rProvider->{Fax} &nbsp;</DIV>
      <DIV >Pager: $rProvider->{Pgr} &nbsp;</DIV>
      <DIV >Email: <A HREF="mailto:$rProvider->{Email}">$rProvider->{Email}</A><FONT COLOR="red" >${NoMail}</FONT></DIV>
      <BR>
    </TD>
|;
    return ($out);
}
############################################################################
