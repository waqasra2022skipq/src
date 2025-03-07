package myHTML;
use SysAccess;
use DBForm;
use DBA;
use myDBI;
use myConfig;
use gHTML;
use DBUtil;

############################################################################
sub list_zip_files_in_table {
    my ( $self, $form, $type, $id ) =
      @_;    # The folder path where zip files are located

    my $dbh = myDBI->dbconnect( $form->{'DBNAME'} );
    my $qEdocs =
      qq|Select Title,Path From ProviderEDocs Where ProvID = ? and Type = ?|;

    my $sEdocs = $dbh->prepare($qEdocs);
    $sEdocs->execute( $id, '40' );

    # Create an HTML table
    my $html = '<table border="1" id="TABLE_5" class="port fullsize">';
    $html .= '<tr> <th>File Name</th> <th>Download</th> <th>Delete</th></tr>';
    my $count = 0;
    while ( my ( $Title, $Path ) = $sEdocs->fetchrow_array ) {
        $count++;

# In Path we have like C:/wamp64/www/Agency/EDocs/92/Clinics/101/Providers/353/353_RollUP_2023-11-10T11_14_49.zip
# So we need to get the after Agency part
        my @pathArr = split( 'Agency', $Path );

        $html .= "<tr id='$count'>";
        $html .= '<td>' . $Title . '</td>';
        $html .= "<td><a href='/Agency/$pathArr[1]' download>Download</td>";
        $html .=
"<td> <a STYLE='cursor:pointer;' onclick=\"deleteFile('$Path', '$form->{DBNAME}', '$count')\">Delete</a> </td>";
        $html .= '</tr>';
    }

    $html .= '</table>';

    $sEdocs->finish();
    return $html;
}

sub newPage {
    my ( $self, $form, $title, $addHEAD, $argBODY, $addBODY, $reqLOAD, $flags )
      = @_;

#warn qq|myHTML-newPage: flags=$flags\n|;
#warn qq|myHTML-newPage: addHEAD=${addHEAD}, argBODY=${argBODY}, addBODY=${addBODY}\n|;
    my $html = $self->new( $form, $title, $flags ) . qq|
<TABLE CLASS="main" >
  <TR ALIGN="center" >
| . $self->leftpane( $form, 'clock mail managertree collapseipad' ) . qq|
    <TD WIDTH="84%" >
| . $self->hdr($form) . $self->menu($form);
    return ($html);
}

sub newHTML {
    my ( $self, $form, $title, $flags, $BODYARGS ) = @_;

    #warn qq|myHTML-newHTML: flags=$flags\n|;
    #warn qq|myHTML-newHTML: NONAVIGATION=$form->{'NONAVIGATION'}\n|;
    my $navflags = $form->{'NONAVIGATION'} ? 'countdown_10' : $flags;
    my $html     = $self->new( $form, $title, $navflags, $BODYARGS );
    my $mismenu  = $navflags =~ /mismenu/ ? $self->menu($form) : '';
    $html .= qq|
<TABLE CLASS="main" >
  <TR ALIGN="center" >
| . $self->leftpane( $form, $navflags ) . qq|
    <TD WIDTH="84%" >
| . $self->hdr($form) . $mismenu;
    return ($html);
}

sub new {
    my ( $self, $form, $title, $flags, $BODYARGS ) = @_;

    #foreach my $f ( sort keys %{$form} ) { warn "new: form-$f=$form->{$f}\n"; }
    #warn qq|myHTML-new: BODYARGS=$BODYARGS\n|;
    #warn qq|myHTML-new: flags=${flags}\n|;
    #warn qq|myHTML-new: NONAVIGATION=$form->{'NONAVIGATION'}\n|;
    my $dbh = myDBI->dbconnect( $form->{'DBNAME'} );

    #warn qq|myHTML: LOGINAGENCY=$form->{'LOGINAGENCY'}\n|;
    my $sAgency = $dbh->prepare(
"select Scheduler,ShiftExec from ProviderControl where ProvID='$form->{LOGINAGENCY}'"
    );
    $sAgency->execute()
      || myDBI->dberror("myHTML: new: select Agency $form->{'LOGINAGENCY'}");
    my ( $Scheduler, $ShiftExec ) = $sAgency->fetchrow_array;
    $form->{SchedulerPath} = $Scheduler;
    $form->{ShiftExecPath} = $ShiftExec;

    #warn qq|myHTML: Scheduler=$Scheduler\n|;
    #warn qq|myHTML: minToLogOut=${minToLogOut}\n|;
    $sAgency->finish();
    my $sProviderControl = $dbh->prepare(
        "select * from ProviderControl where ProvID='$form->{LOGINPROVID}'");
    $sProviderControl->execute()
      || myDBI->dberror("new: select ProviderControl $form->{LOGINPROVID}");
    my $rProviderControl = $sProviderControl->fetchrow_hashref;
    $sProviderControl->finish();

    # the subtitle since we start the html as a FRAMESET
    my $Title = $title eq '' ? 'Millennium Information Services' : $title;

    my $myAlert = '';
    foreach my $prompt ( split( chr(253), $form->{prompt} ) ) {
        $myAlert .= qq|  myAlert("$prompt");\n| if ( $prompt ne '' );
    }

    foreach my $alert ( DBA->getAlert($form) ) {
        $myAlert .= qq|  myAlert("$alert");\n| if ( $alert ne '' );
    }

    my $myClockONLOAD = $flags =~ /noclock/i ? '' : qq|myClock();|;
    my $accordion =
        $flags =~ /accordionopen/i ? 'init_accordion(1);'
      : $flags =~ /accordion/i     ? 'init_accordion(0);'
      :                              '';
    my $myMedAlerts = $flags =~ /medalerts/i ? qq|myMedAlerts(500,600);| : '';
    my $lhcautocomplete = $flags =~ /lhcautocomplete/i
      ? qq|
<LINK href='/cgi/lhc/autocomplete-lhc-17.0.3/autocomplete-lhc.min.css' REL="stylesheet">
<STYLE>
.form_auto_complete {
  text-align: left;
}
</STYLE>
  |
      : '';
    my $lhcform = $flags =~ /lhcform/i
      ? qq|
<link href="/cgi/lhc/lforms-24.1.4/styles/lforms.min.css" media="screen" rel="stylesheet" />
<STYLE>
body {
  display: block;
  margin: 8px;
}
table {
  border-spacing: 2px;
  border-collapse: separate;
}
button, html input[type=button], input[type=reset], input[type=submit] {
  color: black;
}
</STYLE>
  |
      : '';

    my $countdownONLOAD = '';
    if ( $flags =~ /countdown/i ) {
        my ( $s1, $s2 ) = split( 'countdown', $flags, 2 );

        #warn qq|s1=${s1}, s2=${s2}\n|;
        my ( $w1, $w2 ) = split( ' ', $s2, 2 );

        #warn qq|w1=${w1}, w2=${w2}\n|;
        my $min = substr( $w1, 1 );

        #warn qq|min=${min}\n|;
        $countdownONLOAD =
          qq|countdown(${min},'Close after ${min} minutes<BR>%%M%%:%%S%%.');\n|;
        $myClockONLOAD = '';    # countdown conflicts with the clock.
    }
    my $countdown = $flags =~ /countdown/i
      ? qq|
  <SCRIPT TYPE="text/javascript" SRC="/cgi/js/countdown.js?v=20161101"></SCRIPT>
|
      : '';

    my $d3lib = $flags =~ /setd3lib/i
      ? qq|
  <SCRIPT TYPE="text/javascript" charset="utf-8" SRC="/cgi/d3lib/d3.js"></SCRIPT>
  <LINK HREF="/cgi/d3lib/nv.d3.css" REL="stylesheet">
  <SCRIPT TYPE="text/javascript" charset="utf-8" SRC="/cgi/d3lib/nv.d3.js"></SCRIPT>
|
      : '';

#warn qq|myHTML: setd3lib=${d3lib}\n|;
#  my $jquery = $flags =~ /jquery/i ? qq|
#  <LINK REL="stylesheet" HREF="https://code.jquery.com/mobile/1.4.5/jquery.mobile-1.4.5.min.css">
#  <SCRIPT SRC="https://code.jquery.com/mobile/1.4.5/jquery.mobile-1.4.5.min.js"></SCRIPT>
    my $jquery = qq|
  <!-- JQuery Dependencies -->
  <LINK REL="stylesheet" HREF="/cgi/jquery/jquery.mobile-1.4.5.min.css" >
  <LINK REL="stylesheet" HREF="/cgi/jquery/jquery-ui-1.12.1/jquery-ui.css" >
  <SCRIPT TYPE="text/javascript" SRC="/cgi/jquery/jquery-1.12.4.js" ></SCRIPT>
  <SCRIPT TYPE="text/javascript" SRC="/cgi/jquery/jquery-ui-1.12.1/jquery-ui.js" ></SCRIPT>
  <LINK HREF="|
      . myConfig->cfgfile( 'jquery.css', 1 )
      . qq|" REL="stylesheet" TYPE="text/css" >
  <SCRIPT TYPE="text/javascript" SRC="/cgi/jquery/myJQuery.js" ></SCRIPT>
  <LINK REL="stylesheet" HREF="/cgi/jquery/timepicker/jquery.timepicker.css" />
  <SCRIPT TYPE="text/javascript" SRC="/cgi/jquery/timepicker/jquery.timepicker.js" ></SCRIPT>
|;

    #| : '';
    #warn qq|myHTML: jquery=${jquery}\n|;
    my $usetabs = $flags =~ /usetabs/i
      ? qq|
  <!-- Tabs Dependencies -->
  <LINK HREF="|
      . myConfig->cfgfile( 'tabcontent/template6/tabcontent.css', 1 )
      . qq|" REL="stylesheet" TYPE="text/css" >
  <SCRIPT TYPE="text/javascript" SRC="|
      . myConfig->cfgfile( 'tabcontent/tabcontent.js', 1 ) . qq|" ></SCRIPT>
  <SCRIPT TYPE="text/javascript" SRC="/cgi/js/tabs.js"></SCRIPT>
|
      : '';

   # if set 'checkinputwindow' then when focus goes to Parent, Child will close.
    my $checkInputWindow =
      $flags =~ /checkinputwindow|checkpopupwindow/i
      ? qq|ONCLICK="checkInputWindow();" ONUNLOAD="checkInputWindow();"|
      : '';

    #warn qq|myHTML: checkInputWindow=${checkInputWindow}\n|;
    my $minTOlogout =
      $rProviderControl->{'minToLogOut'} eq ''
      ? 60
      : $rProviderControl->{'minToLogOut'};
    my $minBefore = $minTOlogout * .1;

    #warn qq|myHTML: minTOlogout=${minTOlogout}\n|;
    #warn qq|myHTML: minBefore=${minBefore}\n|;
    my $html = qq|Content-Type: text/html; charset=UTF-8

<!DOCTYPE html>
<HTML lang="en" >
<HEAD>
  <meta charset="UTF-8" >
  <meta http-equiv="Cache-control" content="no-cache" >
  <meta http-equiv="expires" content="0" >
  <meta http-equiv="pragma" content="no-cache" >
  <TITLE>${Title}</TITLE>
  ${lhcautocomplete}
  ${lhcform}
  <LINK HREF="|
      . myConfig->cfgfile( 'main.css', 1 )
      . qq|?v=20171208" REL="stylesheet" TYPE="text/css" >
  <LINK HREF="|
      . myConfig->cfgfile( 'mis.css', 1 )
      . qq|?v=20160321" REL="stylesheet" TYPE="text/css" >
  <LINK HREF="|
      . myConfig->cfgfile( 'menuTemplate1.css', 1 )
      . qq|" REL="stylesheet" TYPE="text/css" >
  <LINK HREF="|
      . myConfig->cfgfile( 'blink.css', 1 )
      . qq|" REL="stylesheet" TYPE="text/css" >
  <STYLE>
    .itemBorder { border: 1px solid red }
    .itemText { text-align: center; text-decoration: none; color: black; font: 12px Arial, Helvetica }
  </STYLE>
  <SCRIPT TYPE="text/javascript" SRC="/cgi/js/Login.js?v=20160628" ></SCRIPT>
  <SCRIPT TYPE="text/javascript" >setCookie('MillenniumIS','$form->{mlt}','60');</SCRIPT>
  <SCRIPT TYPE="text/javascript" >javascript:window.history.forward(1);</SCRIPT>
  <SCRIPT TYPE="text/javascript" SRC="/cgi/menu/js/centerAlign.js?v=20200911"> </SCRIPT>
  <SCRIPT TYPE="text/javascript" SRC="/cgi/js/utils.js?v=20170828" ></SCRIPT>
  <SCRIPT TYPE="text/javascript" SRC="/cgi/js/NoEnter.js" ></SCRIPT>
  <SCRIPT TYPE="text/javascript" SRC="/cgi/js/accordion.js" ></SCRIPT>
  ${addHEAD}
  <SCRIPT TYPE="text/javascript" >window.focus();</SCRIPT>
  ${countdown}
  <SCRIPT TYPE="text/javascript" >
    function alertTimeOut(min) {
      myAlert("Logout in less than " + min + " minutes.\\nPlease click the Update button or goto another screen.","LOGOUT Notice");
    }
    function refreshCurrentPage() {
      window.location = logoutURL('$form->{HTTPSERVER}/cgi/bin/mis.cgi?logout=1&mlt=$form->{mlt}');
    }
    function logoutURL(url) { return url; }
    var minTOlogout = ${minTOlogout}
    var minBefore = ${minBefore}
    var alertTOlogout = minTOlogout - minBefore
    var sessionTimer = setTimeout("refreshCurrentPage()", minTOlogout*60000);
    var alertTimer = setTimeout("alertTimeOut(minBefore)", alertTOlogout*60000);
  </SCRIPT>
  <SCRIPT TYPE="text/javascript" >
    function loadup()
    {
      ${myAlert}
      ${reqLOAD}
      ${accordion}
      ${myClockONLOAD}
      ${countdownONLOAD}
      ${myMedAlerts}
    }
  </SCRIPT>
  ${d3lib}
  ${jquery}
  ${usetabs}
</HEAD>
<DIV ALIGN="center" >
<BODY ${BODYARGS} ONLOAD="loadup();" ${checkInputWindow} >
  <DIV ID="textMsgLayer" STYLE="position: absolute; z-index: 1000; visibility: hidden; left: 0px; top: 0px; width: 10px">&nbsp;</DIV>
|;
    return ($html);
}

sub hdr {
    my ( $self, $form ) = @_;
    my $dbh = myDBI->dbconnect( $form->{'DBNAME'} );
    my $s   = $dbh->prepare(
        "select Name from Provider where ProvID='$form->{LOGINAGENCY}'");
    $s->execute() || myDBI->dberror("myHTML: hdr: $form->{'LOGINAGENCY'}");
    my ($AgencyName) = $s->fetchrow_array;
    my $MAINHDR = $AgencyName eq '' ? 'Group/Agency' : $AgencyName;
    $s->finish();
    if ( substr( $form->{DBNAME}, 0, 3 ) eq 'dev' ) {
        $MAINHDR =
"DEVELOPMENT<BR>${MAINHDR}<BR>DEVELOPMENT<BR>DO NOT USE THIS SITE FOR PRODUCTION";
    }
    elsif ( $form->{DBNAME} =~ /_dev/ ) {
        $MAINHDR =
"DEVELOPMENT<BR>${MAINHDR}<BR>DEVELOPMENT<BR>DO NOT USE THIS SITE FOR PRODUCTION<BR>$form->{DBNAME}";
    }

    #my $viewedby = $form->{LOGINUSERTYPE} > 3 && $form->{LOGINNAME} eq '' ?
    #               $form->{LOGINUSERNAME} : $form->{LOGINNAME};
    my $viewedby =
      $form->{LOGINNAME} eq '' ? $form->{LOGINUSERNAME} : $form->{LOGINNAME};
    my $html = qq|
<TABLE CLASS="main" >
  <TR><TD CLASS="hdrcol banner" >${MAINHDR}</TD></TR>
  <TR> <TD CLASS="hdrcol title" > viewed by ${viewedby} $form->{LOGINPROVID} </TD> </TR>
</TABLE>
|;
    return ($html);
}

sub menu {
    my ( $self, $form ) = @_;
    my $MENU = myHTML->getHTML( $form, 'mis.menu', 1 );
    $MENU = $self->setHistory( $form, $MENU );
    my $html = qq|
<TABLE CLASS="main" >
  <TR><TD>${MENU}</TD></TR>
</TABLE>
|;
    return ($html);
}

sub leftpane {
    my ( $self, $form, $lpflags )        = @_;
    my ( $ClockLink, $TreeLink )         = ( '', '' );
    my ( $MailLink, $MailMsg, $MailImg ) = ( '', '', '/img/mail-ok.png' );
    my ( $ApptLink, $ApptMsg )           = ( '', '' );
    my ( $RenewLink, $RenewMsg )         = ( '', '' );
    my ( $IPADLink, $CountDown )         = ( '', '' );
    my $dbh = myDBI->dbconnect( $form->{'DBNAME'} );

    #warn qq|leftpane: lpflags=${lpflags}\n|;
    if ( $lpflags !~ /noclock/
        && ( $lpflags =~ /clock/i || $lpflags =~ /allleft/i ) )
    {
        my $DateNow = DBUtil->Date( 'today', 'fmt', 'MM/DD/YY' );
        $ClockLink = qq|
      <DIV CLASS="clock" >
        ${DateNow}
        <SPAN ID="clock" STYLE="position: relative;" ></SPAN>
      </DIV>|;
    }
    if ( $lpflags =~ /managertree/i || $lpflags =~ /allleft/i ) {
        $TreeLink = qq|
      <A HREF="/cgi/bin/mis.cgi?MIS_Action=ManagerTree&mlt=$form->{mlt}" TITLE="Click here to return to the <BR><STRONG>MANAGERIAL TREE</STRONG>" >
        <IMG ALT="tree" SRC="/cgi/images/tree.png" WIDTH="30" HEIGHT="30" >
      </A>|;
    }
    if ( $lpflags =~ /mail/i || $lpflags =~ /allleft/i ) {

        #warn "myHTML-leftpane: ProvID=$form->{LOGINPROVID}, q=$q\n";
        my $sProvider = $dbh->prepare(
"select Email,NoMail from Provider where ProvID='$form->{LOGINPROVID}'"
        );
        $sProvider->execute() || myDBI->dberror("leftpane: select Provider");
        my ( $Email, $NoMail ) = $sProvider->fetchrow_array;
        my $sProviderMail = $dbh->prepare(
"select ID from ProviderMail where ProvID='$form->{LOGINPROVID}' and Flag='inbox'"
        );
        $sProviderMail->execute()
          || myDBI->dberror("leftpane: select ProviderMail");
        if ( my ($ID) = $sProviderMail->fetchrow_array ) {
            $MailMsg = qq|You have mail.|;
        }
        if ( $NoMail == 1 ) {
            $MailMsg .= qq|<BR><FONT COLOR="red">Mail turned off</FONT>|;
            $MailImg = '/img/mail-warn.png';
        }
        if ( $Email eq '' ) {
            $MailMsg .= qq|<BR><FONT COLOR="red">Missing Email Address</FONT>|;
            $MailImg = '/img/mail-error.png';
        }
        $MailLink = qq|
      <BR>
      <A HREF="/cgi/bin/ProviderMail.cgi?mlt=$form->{mlt}" TITLE="Click here for you <BR><STRONG>MAIL LISTING</STRONG>" ><IMG ALT="your mail" SRC="${MailImg}" HEIGHT="40" WIDTH="40" >
      </A>${MailMsg}|;
        $sProvider->finish();
        $sProviderMail->finish();
    }
    if ( $lpflags =~ /countdown/i ) {
        $CountDown = qq|
      <BR>
  <DIV CLASS="title" >Timeout</DIV>
  <DIV CLASS="home subtitle" >
    <span id='cntdwn' style='background-color: palegreen; color:black'></span>
    <BR>
    <INPUT TYPE="button" NAME="close" VALUE="close" ONCLICK="javascript: window.close()" >
  </DIV>|;
        $ClockLink = '';    # countdown conflicts with the clock.
    }
## not used
#  if ( $lpflags =~ /appointments/i || $lpflags =~ /allleft/i )
#  {
#    $ApptLink = qq|
#      <BR>
#      <A HREF="javascript:ReportWindow('/cgi/bin/GenReport.cgi?Name=Appointments&Type=Appointments&daterange=today&submit=1&output=html&mlt=$form->{mlt}&ProvIDs=$form->{LOGINPROVID}','Appointments',300,600)" TITLE="Click here to <BR><STRONG>LIST APPOINTMENTS</STRONG>" ><IMG ALT="your appointments" SRC="/images/appointment.jpg" WIDTH="30" HEIGHT="30" >
#      </A>| if ( $form->{LOGINPROVID} == 91 );
#  }
## not used
#  if ( $lpflags =~ /renewals/i || $lpflags =~ /allleft/i )
#  {
#    my $sClientRenewals = $dbh->prepare("select count(*) as num from ClientRenewals where ProvID='$form->{LOGINPROVID}' group by ProvID");
#    $sClientRenewals->execute() || myDBI->dberror("leftpane: select ClientRenewals");
#    if ( my ($num) = $sClientRenewals->fetchrow_array )
#    {
#      $RenewMsg = qq|You have ${num} renewals.|;
#      $RenewLink = qq|
#      <BR>
#      <A HREF="javascript:ReportWindow('/cgi/bin/GenReport.cgi?Name=Renewals&Type=renewals&submit=1&output=html&mlt=$form->{mlt}&ProvIDs=$form->{LOGINPROVID}','Renewals',400,1200)" CLASS="tooltip" ><IMG ALT="your renewals" SRC="/img/basic/document_text-import.png" WIDTH="30" HEIGHT="30" >
#        <SPAN>
#          <IMG CLASS="callout" SRC="/img/tooltip_callout.gif" />
#          Click here to
#          <STRONG>List Renewals.</STRONG><br />
#        </SPAN>
#      </A>${RenewMsg}|;
##warn qq|RenewMsg=${RenewMsg}\nRenewLink=\n${RenewLink}\n|;
    #    }
    #    $sClientRenewals->finish();
    #  }
    if ( $lpflags =~ /collapseipad/i || $lpflags =~ /allleft/i ) {
        $IPADLink = qq|
      <BR>
      <A HREF="javascript: void(0)" TITLE="Click here to collapse the menus <BR><STRONG>left open on your iPAD</STRONG>" ><IMG ALT="close ipad menu" SRC="/images/redx.gif" >
      </A>|;
    }
    my $html = qq|
    <TD CLASS="main" WIDTH="8%" >
${ClockLink}
${TreeLink}
${MailLink}
${ApptLink}
${RenewLink}
${IPADLink}
${CountDown}
    </TD>
|;
    return ($html);
}

sub setHistory {
    my ( $self, $form, $menu ) = @_;
    return () unless ( $menu =~ /HISTORY/ );
    my $dbh = myDBI->dbconnect( $form->{'DBNAME'} );
    my $html;
    my $cnt = 0;
    my $q =
qq|select * from History where ProvID='$form->{LOGINPROVID}' order by ID desc|;
    my $s = $dbh->prepare($q);
    $s->execute() || myDBI->dberror($q);

    while ( my $r = $s->fetchrow_hashref ) {
        $cnt++;
        $html .=
qq|      <A HREF="$r->{Link}" ONMOUSEOVER="window.status='$r->{Name} $r->{Descr}'; return true;" ONMOUSEOUT="window.status=''" >$r->{Name} $r->{Descr}</A><BR />\n|;
        last if ( $cnt == 15 );
    }
    $s->finish();

    #warn qq|setHistory: html=$html\n|;
    $menu =~ s/HISTORY/$html/;
    return ($menu);
}

sub rightpane {
    my ( $self, $form, $rpflags, $addtopane ) = @_;
    my $flags = $form->{'NONAVIGATION'} ? '' : $rpflags;
    my ( $RightLink, $SearchLink ) = ( '', '' );
    if ( $flags =~ /search/i ) {
        my $ok  = SysAccess->verify( $form, 'Privilege=ClinicManager' );
        my $msg = qq|Use the Search below to find Clients |;
        $msg        .= qq|and Providers| if ($ok);
        $msg        .= qq|.|;
        $SearchLink .= qq|
      <FORM NAME="Search" ACTION="/cgi/bin/Search.cgi" METHOD="POST">
      <DIV CLASS="main subtitle" >${msg}</DIV>
      <DIV CLASS="port subtitle hdrcol" >
        <A HREF="javascript:void(0)" TITLE="Enter search string into the text box.<BR>Then select the type of search needed by clicking on one of the radio buttons.<BR>wildcards such as John... may also be used except in the ID#." >
          Search
        </A>
        <BR>
        <INPUT TYPE="text" NAME="SearchString" ONFOCUS="select()" SIZE="15" >
        <BR>
        <A HREF="javascript:void(0)" TITLE="Wildcards such as Smith... or ...son may also be used.<BR>Do not use wildcards in the ID#." >
          Client
        </A>
      </DIV>
      <DIV CLASS="port subtitle strcol" >
            <INPUT TYPE="radio" NAME="SearchType" VALUE="ClientID" ONCLICK="javascript: this.form.submit()" >
            ID #
            <BR>
            <INPUT TYPE="radio" NAME="SearchType" VALUE="ClientSSN" ONCLICK="javascript: this.form.submit()" >
            SSN
        <BR>
            <INPUT TYPE="radio" NAME="SearchType" VALUE="ClientFirstName" ONCLICK="javascript: this.form.submit()" >
            First Name
        <BR>
            <INPUT TYPE="radio" NAME="SearchType" VALUE="ClientLastName" ONCLICK="javascript: this.form.submit()" >
            Last Name
        <BR>
            <INPUT TYPE="radio" NAME="SearchType" VALUE="ClientInsNum" ONCLICK="javascript: this.form.submit()" >
            Insurance #
        <BR>
            <INPUT TYPE="radio" NAME="SearchType" VALUE="ClientNote" ONCLICK="javascript: this.form.submit()" >
            Note #
      </DIV>
|;
        if ($ok) {
            $SearchLink .= qq|
      <DIV CLASS="port subtitle hdrcol" >
        <A HREF="javascript:void(0)" TITLE="Wildcards such as Smith... or ...son may also be used.<BR>Do not use wildcards in the ID #." >
          Provider
        </A>
      </DIV>
      <DIV CLASS="port subtitle strcol" >
        <INPUT TYPE="radio" NAME="SearchType" VALUE="ProviderFirstName" ONCLICK="javascript: this.form.submit()" >
        First Name
        <BR>
        <INPUT TYPE="radio" NAME="SearchType" VALUE="ProviderLastName" ONCLICK="javascript: this.form.submit()" >
        Last Name
      </DIV>
|;
        }
        $SearchLink .= qq|
      <DIV CLASS="main strcol subtitle">
        Remember: if you use the search to commit any pending updates first.  Commit updates first by using the update button.
      </DIV>
      <INPUT TYPE="hidden" NAME="mlt" VALUE="$form->{mlt}" >
      <INPUT TYPE="hidden" NAME="misLINKS" VALUE="$form->{misLINKS}" >
      </FORM >
|;
    }
##
  # THE ABOVE </FORM > HAS A SPACE SO DBForm.pm WILL NOT PUT THE hidden VARS IN!
  #  WITHOUT THE SPACE IT WOULD ADD THE hidden VARIBLES. getHTML()
  # fix with ADDHIDDEN
##
    if ( $flags =~ /search/i || $flags =~ /login/i ) {
        $SearchLink = qq|
      <DIV CLASS="main hdrcol" >
           <A HREF="/cgi/bin/mis.cgi?logout=1&mlt=$form->{mlt}" ONMOUSEOVER="ImgShow('logout')" ONMOUSEOUT="ImgHide()" ><IMG ALT="logout" NAME="logout" BORDER=0 SRC="/images/logout_hide.gif"></A>
        <BR>${SearchLink}
      </DIV>
      <SCRIPT LANGUAGE="JavaScript" >document.Search.elements[0].focus();</SCRIPT>
|;
    }
    my $html = qq|
    </TD>
    <TD CLASS="main" WIDTH="8%" > ${SearchLink} ${addtopane} </TD>
  </TR>
</TABLE>

<BR>
<BR>
<BR>
<BR>
<BR>
<BR>
<BR>
<BR>
<BR>
<BR>
</BODY>
</HTML>
</DIV>|;
    return ($html);
}
############################################################################
# sub = used for sublist call, not necessary on first or primary call.
# Use: SCREENS definition in tables.cfg
# sort types are: default, alphanumeric, numeric, ignorecase, currency, currency_comma, date.
sub ListSel {
    my ( $self, $form, $screen_name, $id, $pushID, $islocked, $tabnum,
        $addWHERE )
      = @_;

#warn qq|\nENTER ListSel: screen_name=${screen_name}, id=${id}\n|;
#warn qq|\nENTER ListSel: pushID=${pushID}, islocked=${islocked}, tabnum=${tabnum}\n|;
#warn qq|\nENTER ListSel: addWHERE=${addWHERE}\n|;
    my $table   = myConfig->scr( $screen_name, 'STABLE' );
    my $RECID   = myDBI->getTableConfig( $table, 'RECID' );
    my $TABLEID = $table . '_' . $RECID;
    my $mainid  = $id eq 'new' ? '' : $id;
    my $links   = $self->setLINK( $form, $table, $mainid );
    my $access  = myConfig->scr( $screen_name, 'SACCESS' );

    #warn qq|ListSel: access=$access\n|;
    if ( $access eq '' ) { $access = 1; }
    else {
        my $func = $access;
        $func =~ s/_TABNUM_/$tabnum/g;
        $func =~ s/_MAINID_/$mainid/g;
        $func =~ s/_LINKS_/$links/g;
        $access = $func eq '' ? 1 : myDBI->exFunc( $form, $func );

        #warn qq|ListSel: func=$func, row=$row, access=$access\n|;
    }

# 2 kinds of access, 1) access defined in List, 2) hasaccess defined in TABLES cfg
    return () unless ($access);

    #warn qq|ENTER ListSel: table=$table\n|;
    if (
        !SysAccess->verify( $form, myDBI->getTableConfig( $table, 'ACCESS' ) ) )
    {
        myDBI->error("Access Denied to ${table} (myHTML->ListSel)");
    }

    my $title = myConfig->scr( $screen_name, 'STITLE' );
    $title = $screen_name if ( $title eq '' );

#warn qq|ENTER ListSel: screen_name=$screen_name, mainid=$mainid, pushID=$pushID\n|;
#warn qq|ENTER ListSel: screen_name=$screen_name, RECID=$RECID, TABLEID=$TABLEID\n|;
    my $updall = $islocked ? '' : qq|&UpdateTables=all|;

    #warn qq|ENTER ListSel: TABLEID=${TABLEID}, links=$links, updall=$updall\n|;
    my $only1 = myConfig->scr( $screen_name, 'SONLY1' );
    $only1 = $only1 eq 'yes' || $only1 == 1 ? 1 : 0;
    my $addnew    = myConfig->scr( $screen_name, 'SADDNEW' );
    my $addhtml   = myConfig->scr( $screen_name, 'SADDHTML' );
    my $tabs      = myConfig->scr( $screen_name, 'STABS' );
    my $separator = $tabnum || $tabs =~ /yes/i ? '' : qq|<HR WIDTH="50%" >|;
    my @TOTALCOLS = ();
    my $TOTALCOL  = 0;
    my @TabList   = ();
    my @TabHdrs   = ();
    my ( $row, $cols, $theheader, $thebody, $scripts, $td1, $tdr ) =
      ( 0, 0, "        <THEAD>\n", "        <TBODY>\n", '', '', '' );

    foreach my $tablehdrdefs ( @{ myConfig->scr( $screen_name, 'SHEADER' ) } ) {
        $cols++;
        my ( $fld, $jst, $fldDef, $hdrlabel, $sortable ) =
          split( ':', $tablehdrdefs );
        my $sortclass =
          $sortable eq '' ? 'table-nosort' : 'table-sortable:' . $sortable;
        if ( $jst =~ /total/ ) { $TOTALCOLS[$cols] = 0; $TOTALCOL = 1; }
        $hdrlabel = $fld if ( $hdrlabel eq '' );    # default the header
        if ( $hdrlabel eq 'none' ) { $hdrlabel = '&nbsp;'; }    # or no header
        else                       { $hdrlabel = "<B><U>${hdrlabel}</U></B>"; }
        $jst =~ s/flag//g;     # could describe a yes/no flag?
        $jst =~ s/total//g;    # could be a total column?
        $theheader .=
qq|          <TH CLASS="${sortclass}" STYLE="text-align: ${jst}" >${hdrlabel}</TH>\n|;
    }
    $theheader .= qq|        </THEAD>\n|;
    ( my $sql = myConfig->scr( $screen_name, 'SSELECT' ) ) =~
      s/_MAINSELECTID_/${mainid}/g;
    $sql =~ s/order by/${addWHERE} order by/g;

    #warn qq|sql=\n$sql\n|;
    my @list  = DBA->doSQL( $form, $sql );
    my $total = scalar(@list);
    foreach my $r (@list) {
        $row++;

    #if ( $table eq 'xSCRates' ){
    #foreach my $f ( sort keys %{$r} ) { warn "ListSel: r-$f=$r->{$f}\n"; }
    #}
    #warn qq|ListSel: tabnum=$tabnum, row=$row\n|;
    # _RECID_ is the defined 'id' in the tables.cfg for record (may not be 'ID')
    # _FLDID_ is always the literal 'ID' for record
    #warn qq|ListSel: _RECID_${RECID}=$r->{$RECID}, _FLDID_=$r->{'ID'}\n|;
        my $class   = int( $row / 2 ) == $row / 2 ? 'rpteven' : 'rptodd';
        my $thistab = qq|        <TR CLASS="${class}" >\n|;
        my $fldcnt  = 0;
        foreach
          my $tablehdrdefs ( @{ myConfig->scr( $screen_name, 'SHEADER' ) } )
        {
            #warn qq|NEXT.............\n|;
            $fldcnt++;
            my ( $fld, $jst, $fldDef, $hdrlabel, $sortable ) =
              split( ':', $tablehdrdefs );

      #warn qq|ListSel: fld=$fld, jst=$jst, fldDef=$fldDef, display=$display\n|;
            my $fldval = $r->{$fld};    # original field value
            if ( $jst =~ /total/ ) { $TOTALCOLS[$fldcnt] += $fldval; }
            if ( $jst =~ /flag/i )      # change original field value
            { $fldval = $fldval eq 1 ? 'yes' : 'no'; }
            $jst =~ s/flag//g;          # could describe a yes/no flag?
            $jst =~ s/total//g;         # could be a total column?
            my $display = $fldval;      # default for display

            #warn qq|ListSel: fld=$fld, jst=$jst, fldval=$fldval\n|;
            my $style = '';
            my ( $isFunc, $typeFunc ) = split( '', $fldDef );

        #warn qq|ListSel: fldDef=$fldDef, isFunc=$isFunc, typeFunc=$typeFunc\n|;
            if ( $isFunc eq 'F' )       # FUNCTION CALL
            {
                my $func = myConfig->scr( $screen_name, 'F' . $fld );
                $func =~ s/_RECID_/$r->{$RECID}/g;
                $func =~ s/_FLDID_/$r->{'ID'}/g;
                $func =~ s/_TABNUM_/$tabnum/g;
                $func =~ s/_MAINID_/$mainid/g;
                $func =~ s/_LINKS_/$links/g;

                #warn qq|ListSel: func=$func, row=$row, text=$text\n|;
                # WATCH: if null, then blows out: Can't locate object method ""
                my $text = $func eq '' ? '' : myDBI->exFunc( $form, $func, $r );

                #warn qq|ListSel: func=$func, row=$row, text=$text\n|;
                if ( $typeFunc eq 'M' )    # ON MOUSEOVER
                {
                    $display =
qq|<A HREF="javascript:void(0)" TITLE="${text}" >${fldval}</A>|;
                }
                elsif (
                    $typeFunc eq 'S' ) # STYLE-some functions return value^style
                { ( $display, $style ) = split( chr(253), $text ); }
                elsif ( $typeFunc eq 'E' ) # EDIT or VIEW (calculated View/Edit)
                {
                    my $editbutton = $r->{'Locked'} ? 'View' : qq|View/Edit|;
                    my $editlocked =
                      myConfig->scr( $screen_name, 'Blockededit' )
                      ;                    # allow button for LOCKED records
                    my ( $lockededit, $lockededitbuttonvalue ) =
                      split( ':', $editlocked );
                    my $lockededitbutton = '';
                    if ( $lockededit ne '' && $r->{'Locked'} ) {
                        $lockededitbutton =
qq|            <INPUT TYPE="submit" ONCLICK="return validate(this.form)" NAME="${lockededit}&${TABLEID}=$r->{$RECID}&${links}&fwdTABLE=${table}${updall}&pushID=${pushID}" VALUE="${lockededitbuttonvalue}" >|;
                    }

#warn qq|ListSel: Locked=$Locked, updall=${updall}, editbutton=${editbutton}\n|;
                    $display = qq|
            <INPUT TYPE="submit" ONCLICK="return validate(this.form)" NAME="${text}&${TABLEID}=$r->{$RECID}&${links}&fwdTABLE=${table}${updall}&pushID=${pushID}" VALUE="${editbutton}" >
            ${lockededitbutton}
|;
                }
                else {
                    $display = qq|${text} ${fldval}|;
                }    # otherwise-display text from func call and field value
            }
            elsif ( $isFunc eq 'B' )    # BUTTON
            {
                my $button = myConfig->scr( $screen_name, 'B' . $fld );
                $button =~ s/_RECID_/$r->{$RECID}/g;
                $button =~ s/_FLDID_/$r->{'ID'}/g;
                $button =~ s/_TABNUM_/$tabnum/g;
                $button =~ s/_MAINID_/$mainid/g;
                $button =~ s/_LINKS_/$links/g;

                #warn qq|ListSel: BUTTON: button=$button, typeFunc=$typeFunc\n|;
                if ( $typeFunc eq 'P' )    # PRINT
                {
                    #             ie:   PrintPHQ:Scores
                    my ( $print_routine, $page, $msg ) = split( ':', $button );
                    $msg = 'click to print' if ( $msg eq '' );    # ON MOUSEOVER
                    $display =
qq|<A HREF="javascript:ReportWindow('/cgi/bin/${print_routine}.cgi?IDs=$r->{$RECID}&mlt=$form->{mlt}&action=${table}\&page=${page}','PrintWindow')" TITLE="${msg}" ><IMG ALT="print" SRC="/img/print-ok.png" HEIGHT="21" WIDTH="21" BORDER="0" ></A><BR>${fldval}|;
                }
                elsif ( $typeFunc eq 'D' )    # DISPLAY (EDocs)
                {
                  #warn qq|ListSel: DISPLAY: fldval=$fldval, $fld=$r->{$fld}\n|;
                    $display =
                      $fldval eq ''
                      ? qq|<A HREF="javascript:void()" TITLE="NO LINK AVAILABLE!" ><IMG ALT="print" SRC="/img/print-warn.png" HEIGHT="21" WIDTH="21" BORDER="0" ></A><BR>|
                      : qq|<A HREF="javascript:ReportWindow('${fldval}','display')" TITLE="Click here to view." ><IMG ALT="print" SRC="/img/print-ok.png" HEIGHT="21" WIDTH="21" BORDER="0" ></A><BR>|;
                }
                elsif ( $typeFunc eq 'O' )    # ORDER
                {
                    my $arrowup      = myConfig->cfgfile( 'arrow_up.png',   1 );
                    my $arrowdown    = myConfig->cfgfile( 'arrow_down.png', 1 );
                    my $priorityup   = $r->{$fld} - 15;
                    my $prioritydown = $r->{$fld} + 15;
                    my $up =
qq|<A HREF="javascript:callAjax('${screen_name}','${priorityup}','${screen_name}','&id=$r->{$RECID}&row=${tabnum}&Locked=${islocked}&${links}&LOGINPROVID=$form->{LOGINPROVID}&LOGINUSERID=$form->{LOGINUSERID}&LOGINUSERDB=$form->{LOGINUSERDB}&mlt=$form->{mlt}&misLINKS=$form->{misLINKS}&LINKID=$form->{LINKID}','popup.pl');" TITLE="move up"><IMG ALT="up" SRC="${arrowup}" HEIGHT="20" WIDTH="20" ></A>|;
                    my $down =
qq|<A HREF="javascript:callAjax('${screen_name}','${prioritydown}','${screen_name}','&id=$r->{$RECID}&row=${tabnum}&Locked=${islocked}&${links}&LOGINPROVID=$form->{LOGINPROVID}&LOGINUSERID=$form->{LOGINUSERID}&LOGINUSERDB=$form->{LOGINUSERDB}&mlt=$form->{mlt}&misLINKS=$form->{misLINKS}&LINKID=$form->{LINKID}','popup.pl');" TITLE="move down"><IMG ALT="down" SRC="${arrowdown}" HEIGHT="20" WIDTH="20" ></A>|;
                    if ( $total == 1 ) {
                        $up   = '&nbsp;&nbsp;&nbsp;';
                        $down = '&nbsp;&nbsp;&nbsp;';
                    }
                    elsif ( $row == 1 )      { $up   = '&nbsp;&nbsp;&nbsp;'; }
                    elsif ( $row == $total ) { $down = '&nbsp;&nbsp;&nbsp;'; }
                    $display = qq|${up}${down}|;
                }
                elsif ( $typeFunc eq 'T' )    # TOGGLE
                {
                    my $arrowup   = myConfig->cfgfile( 'arrow_up.png',   1 );
                    my $arrowdown = myConfig->cfgfile( 'arrow_down.png', 1 );
                    my $toggle    = $r->{$fld} == 1 ? 'off' : 'on';
                    my $switch =
                      $toggle eq 'on'
                      ? qq|<A HREF="javascript:callAjax('${screen_name}T','${toggle}','${screen_name}','&id=$r->{$RECID}&row=${tabnum}&Locked=${islocked}&${links}&LOGINPROVID=$form->{LOGINPROVID}&LOGINUSERID=$form->{LOGINUSERID}&LOGINUSERDB=$form->{LOGINUSERDB}&mlt=$form->{mlt}&misLINKS=$form->{misLINKS}&LINKID=$form->{LINKID}','popup.pl');" TITLE="toggle on"><IMG ALT="up" SRC="${arrowup}" HEIGHT="20" WIDTH="20" ></A>|
                      : qq|<A HREF="javascript:callAjax('${screen_name}T','${toggle}','${screen_name}','&id=$r->{$RECID}&row=${tabnum}&Locked=${islocked}&${links}&LOGINPROVID=$form->{LOGINPROVID}&LOGINUSERID=$form->{LOGINUSERID}&LOGINUSERDB=$form->{LOGINUSERDB}&mlt=$form->{mlt}&misLINKS=$form->{misLINKS}&LINKID=$form->{LINKID}','popup.pl');" TITLE="toggle off"><IMG ALT="down" SRC="${arrowdown}" HEIGHT="20" WIDTH="20" ></A>|;
                    $display = qq|${fldval}${switch}|;
                }
                elsif ( $typeFunc eq 'E' )    # EDIT or VIEW (given View/Edit)
                {
                    #warn qq|button=${button}\n|;
                    my ( $editbutton, $editbuttonvalue ) =
                      split( ':', $button );

                    #warn qq|edit=${edit}\n|;
                    #warn qq|editbuttonvalue=${editbuttonvalue}\n|;
                    my $editbuttonvalue =
                        $editbuttonvalue eq ''
                      ? $r->{'Locked'}
                          ? 'View'
                          : qq|View/Edit|
                      : $editbuttonvalue;

                    #warn qq|editbutton=${editbutton}\n|;
                    my $editlocked =
                      myConfig->scr( $screen_name, 'Blockededit' )
                      ;    # allow button for LOCKED records
                    my ( $lockededit, $lockededitbuttonvalue ) =
                      split( ':', $editlocked );
                    my $lockededitbutton = '';
                    if ( $lockededit ne '' && $r->{'Locked'} ) {
                        $lockededitbutton =
qq|            <INPUT TYPE="submit" ONCLICK="return validate(this.form)" NAME="${lockededit}&${TABLEID}=$r->{$RECID}&${links}&fwdTABLE=${table}${updall}&pushID=${pushID}" VALUE="${lockededitbuttonvalue}" >|;
                    }

#warn qq|ListSel: Locked=$Locked, updall=${updall}, editbutton=${editbutton}\n|;
                    $display = qq|
            <INPUT TYPE="submit" ONCLICK="return validate(this.form)" NAME="${editbutton}&${TABLEID}=$r->{$RECID}&${links}&fwdTABLE=${table}${updall}&pushID=${pushID}" VALUE="${editbuttonvalue}" >
            ${lockededitbutton}
|;
                }

                #warn qq|ListSel: BUTTON: display=$display\n|;
            }
            my $show_id = '';

            #warn qq|ListSel: CHECK: Privilege=Agent\n|;
            if ( $fldcnt == 1 && SysAccess->verify( $form, 'Privilege=Agent' ) )
            {
                $show_id =
qq|<A HREF="javascript:ReportWindow('/cgi/bin/show_id.cgi?IDs=$r->{$RECID}&mlt=$form->{mlt}&action=${table}\&page=${page}','PrintWindow')" TITLE="${TABLEID}: $r->{$RECID}" ><IMG ALT="show" SRC="/img/zoom.png" HEIGHT="20" WIDTH="20" ></A>|
                  if ( $form->{'LOGINPROVID'} == 91 );
                $show_id .=
qq|<A HREF="javascript:ReportWindow('/cgi/bin/show_log.cgi?IDs=$r->{$RECID}&mlt=$form->{mlt}&action=${table}\&page=${page}','PrintWindow')" TITLE="${TABLEID}: $r->{$RECID}" ><IMG ALT="history" SRC="/img/history.png" HEIGHT="20" WIDTH="20" ></A>|
                  if ( myDBI->getTableLogFlag( $form, $table ) );
            }
            if ( $fldcnt == 1
                && ( $table eq 'ClientProblems' || $table eq 'ClientMeds' ) )
            {
                my $dbh  = myDBI->dbconnect( $form->{'DBNAME'} );
                my $sAge = $dbh->prepare(
                    "select DOB from Client where ClientID='$r->{ClientID}'");
                $sAge->execute()
                  || myDBI->dberror("InfoLink: select DOB ($r->{ClientID})");
                my ($DOB) = $sAge->fetchrow_array;
                my $Age = DBUtil->Date( $DOB, 'age', $form->{'TODAY'} );
                $show_id .=
qq|<A HREF="javascript:ReportWindow('http://apps2.nlm.nih.gov/medlineplus/services/mpconnect.cfm?mainSearchCriteria.v.cs=2.16.840.1.113883.6.90&mainSearchCriteria.v.c=$r->{'ICD10'}&informationRecipient.languageCode.c=en&age.v.u=a&age.v.v=${Age}','InfoLink')" TITLE="${TABLEID}: $r->{$RECID}" ><IMG ALT="info" SRC="/img/user-info.png" HEIGHT="20" WIDTH="20" ></A>|
                  if ( $table eq 'ClientProblems' );
                $show_id .=
qq|<A HREF="javascript:ReportWindow('http://apps2.nlm.nih.gov/medlineplus/services/mpconnect.cfm?mainSearchCriteria.v.cs=2.16.840.1.113883.6.88&mainSearchCriteria.v.c=$r->{'rxcui'}&informationRecipient.languageCode.c=en&age.v.u=a&age.v.v=${Age}','InfoLink')" TITLE="${TABLEID}: $r->{$RECID}" ><IMG ALT="info" SRC="/img/user-info.png" HEIGHT="20" WIDTH="20" ></A>|
                  if ( $table eq 'ClientMeds' );
                $sAge->finish();
            }

#warn qq|ListSel: style=${style}, jst=${jst}, display=${display}, show_id=${show_id}\n|;
            $thistab .=
qq|          <TD ${style} STYLE="text-align: ${jst}" >${show_id}${display}</TD>\n|;
        }
        $thistab .= qq|        </TR>\n|;
        my $subcnt = 0;
        foreach my $sublist ( @{ myConfig->scr( $screen_name, 'SUBLIST' ) } ) {
            $subcnt++;

            #warn qq|sublist=$sublist\n|;
            $thistab .= qq|
        <TR>
          <TD ALIGN="left" COLSPAN="${cols}" >
            <TABLE CLASS="port fullsize" >
              <TR>
                <TD ALIGN="left" >
<SPAN ID="${sublist}${row}" >
|
              . myHTML->ListSel( $form, $sublist, $r->{$RECID},
                $form->{'LINKID'}, $r->{'Locked'}, $row )
              . qq|
</SPAN>
                </TD>
              </TR>
            </TABLE>
            ${separator}
          </TD>
        </TR>
|;
        }

       #warn qq|KLS1: row=${row}, total=${total}, screen_name=${screen_name}\n|;
        if ( $row < $total && $subcnt ) {
            $thistab .= qq|        <TR>\n${theheader}\n        </TR>\n|
              if ( $tabs =~ /no/i );
        }
        $thebody .= $thistab;
        push( @TabList, $theheader . $thistab );
        push( @TabHdrs, "${row}: $r->{EffDate}-$r->{ExpDate}" );
        $tdr = $r;    # save for DATA1FLDS...

        #warn qq|ListSel: save: ${RECID}=$tdr->{$RECID}, TABLEID=$TABLEID\n|;
    }
    if ( $TOTALCOL && $form->{'LOGINPROVID'} == 91 ) {
        $thebody .= qq|        <TR >\n|;
        foreach
          my $tablehdrdefs ( @{ myConfig->scr( $screen_name, 'SHEADER' ) } )
        {
            $fldcnt++;

            #warn qq|TOTALCOLS: ${fldcnt}: $TOTALCOLS[$fldcnt]\n|;
            if ( $TOTALCOLS[$fldcnt] eq '' ) {
                $thebody .=
                  qq|          <TD STYLE="text-align: right" >&nbsp;</TD>\n|;
            }
            else {
                my $total = sprintf( "%.2f", $TOTALCOLS[$fldcnt] );
                $thebody .=
                  qq|          <TD STYLE="text-align: right" >${total}</TD>\n|;
            }

            #warn qq|TOTALCOLS: ${fldcnt}: NOT NULL: $TOTALCOLS[$fldcnt]\n|;
        }
        $thebody .= qq|        </TR>\n|;
    }

    #warn qq|addhtml=$addhtml\n|;
    $thebody .= $addhtml eq '' ? '' : myDBI->exFunc( $form, $addhtml );
    $thebody .= qq|        </TBODY>|;
    if ( $tabs =~ /yes/i ) {
        my @Tabs  = ();
        my $tabid = DBUtil->genToken();
        for ( $c = 0 ; $c <= $#TabHdrs ; $c++ ) {
            my $tab =
              qq|<TABLE CLASS="port fullsize" > | . $TabList[$c] . qq|</TABLE>|;
            my $tabcontent = $TabHdrs[$c] . chr(253) . $tab;

            #warn qq|\n\nc=$c\ntabcontent=$tabcontent\n|;
            push( @Tabs, $tabcontent );
        }
        $thebody = qq|
  <TR>
    <TD CLASS="home" >
| . gHTML->setTab( '', '', @Tabs ) . qq|
    </TD>
  </TR>
|;
    }
    else { $thebody = $theheader . $thebody; }

    #warn qq|KLS2: row=${row}, total=${total}, screen_name=${screen_name}\n|;
    my $td = myConfig->scr( $screen_name, 'SDATA1' );

    #warn qq|ListSel: CHECK: td=$td\n|;
    if ( $td ne '' ) {

  #warn qq|ListSel: SDATA1: tabnum=$tabnum, row=$row\n|;
  #warn qq|ListSel: SDATA1: mainid=$mainid, links=$links\n|;
  #warn qq|ListSel: screen_name=$screen_name, RECID=$RECID, TABLEID=$TABLEID\n|;
        my $i = 0;

#warn qq|ListSel: tdr: ${RECID}=$tdr->{$RECID}, TABLEID=$TABLEID\n|;
#foreach my $f ( sort keys %{$tdr} ) { warn qq|ListSel: ${screen_name}: tdr: $f=$tdr->{$f}\n|; }
        $td =~ s/_TABNUM_/$tabnum/g;
        $td =~ s/_MAINID_/$mainid/g;
        $td =~ s/_LINKS_/$links/g;
        foreach
          my $f ( split( ' ', myConfig->scr( $screen_name, 'SDATA1FLDS' ) ) )
        {
            $i++;
            $td =~ s/_FLD${i}_/$tdr->{$f}/g;
        }

        #warn qq|ListSel: td=$td\n|;
        $td1 = myDBI->exFunc( $form, $td );

        #warn qq|ListSel: td1=$td1\n|;
    }

#warn qq|ListSel: addnew=${addnew}, islocked=${islocked}, only1=${only1}, row=${row}\n|;
    $addnew =~ s/_TABNUM_/$tabnum/g;
    $addnew =~ s/_MAINID_/$mainid/g;
    $addnew =~ s/_LINKS_/$links/g;
    my $newbutton =
      $addnew eq '' || $islocked || ( $only1 && $row > 0 )
      ? ''
      : qq|<INPUT TYPE="submit" ONCLICK="return validate(this.form,'Add New information','')" ONMOUSEOVER="window.status='add button'; return true;" ONMOUSEOUT="window.status=''" NAME="${addnew}&${TABLEID}=new&${links}&fwdTABLE=${table}${updall}&pushID=${pushID}" VALUE="Add New" >|;
    my $html = qq|
${scripts}
<SCRIPT LANGUAGE="JavaScript" SRC="/cgi/js/tablesort.js"> </SCRIPT>
<LINK HREF="/cgi/css/tablesort.css" REL="stylesheet" TYPE="text/css">
<TABLE CLASS="port fullsize" >
  <TR>
    <TD ALIGN="left" ><B>${title}</B> ${newbutton}</TD>
    <TD ALIGN="right" >&nbsp;</TD>
  </TR>
  <TR>
${td1}
    <TD ALIGN="center" COLSPAN="2" >
      <TABLE class="chartsort table-autosort table-stripeclass:alternate port fullsize">
${thebody}
      </TABLE>
    </TD>
  </TR>
</TABLE>
|;

#warn qq|EXIT  ListSel: screen_name=$screen_name, id=$id, pushID=$pushID, islocked=$islocked, tabnum=$tabnum\n|;
#warn qq|EXIT  ListSel: links=${links}\n|;
    return ($html);
}

sub setLINK {
    my ( $self, $form, $table, $hdrid ) = @_;
    return ('') if ( $table eq '' );

    #warn qq|myHTML: setLINK: table=$table, hdrid=${hdrid}\n|;
    my ( $link, $dlm, $hdrtable, $hdrcnt ) = ( '', '', $table, 0 );
    while ( defined( myConfig->tbl( $hdrtable, 'HEADERTABLE' ) ) ) {
        $hdrtable = myConfig->tbl( $hdrtable, 'HEADERTABLE' );
        $hdrcnt++;    # 1,2,3... header table of table.
        my $ID  = myDBI->getTableConfig( $hdrtable, 'RECID' );
        my $fld = qq|${hdrtable}_${ID}|;

        #   either use the incoming ID or it SHOULD BE in the form...
        my $val = $hdrcnt == 1 ? $hdrid : $form->{$fld};

        #warn qq|myHTML: setLINK: fld=$fld=$form->{$fld}, val=${val}\n|;
        $link .= "${dlm}${fld}=${val}";
        $dlm = '&';

        #warn qq|myHTML: setLINK: link=${link}\n|;
    }

    #warn qq|myHTML: setLINK: END: link=$link\n|;
    return ($link);
}
############################################################################
# READ THE HTML TEMPLATE FROM DISK along with the SQL data
#   This routine is called my mis.cgi.
# Arguments: $htmlname  --  name of html template on disk
#                           will be prefixed with 'DocRoot/html/'
#                           where DocRoot is sites' home directory
#
#   This routine does the actual read from disk of the html template,
#   then
#     searches for include files identified as ((filename))
#     and
#     searches for tables identified as 'TABLE_FIELD_INDEX'
#     These tables identified will be read from the database based on
#                                       'TABLE_ID'
#   The SQL tables are read once per session and the
#     associative array %form is filled in with the SQL data.
#     when a Table is later updated it is closed logically.
############################################################################
sub getHTML {
    my ( $self, $form, $htmlname, $NoTMP ) = @_;
    ####################################
    # Open the html file and parse each line
    ####################################
    my $SRC          = myConfig->cfg('SRC');
    my $htmlpathname = $SRC . "/html/" . $htmlname;
    if ( !open( TEMPLATE, $htmlpathname ) ) {
        myDBI->error("Can't open $htmlname ($!).");
    }

    ####################################
    # MAIN loop goes through the html template we just opened
    #   $html is string returned.
    ####################################
    my $html      = '';
    my $line      = '';
    my $line_copy = '';
    while ( $line = <TEMPLATE> ) {
        ####################################
        # 1st Search for Table Names
        #   so we can read the records from the SQL database.
        #   and open all the tables.
        ####################################
        $line_copy = '';
        while ( $line =~ /<<([^>]+)>>/ ) {
            $whatmatch = $1;    # what matched
            $prematch  = $`;    # before what matched
            $line      = $';    # now set to after what matched
                                # put back what we found, we are only looking.
            $line_copy .= $prematch . '<<' . $whatmatch . '>>';
            my ( $table, $field, $num ) = $whatmatch =~ /<?(.+?)_(.+?)_(\d+)/;
            next if ( $table eq '' );
            if ( !$form->{"OPENTABLE:${table}"} ) { myForm->TBLread($table); }
        }
        $html .= $line_copy . $line;
    }

    ####################################
    # next search for any prepare functions...
    ####################################
    $line      = $html;
    $line_copy = '';
    while ( $line =~ /\[\[\[(.+?)\]\]\]/ ) {
        $whatmatch = $1;            # what matched
        $prematch  = $`;            # before what matched
        $line      = $';            # now set to after what matched
        $line_copy .= $prematch;    # copy set to before what matched
        $line_copy .=
          myDBI->exFunc( $form, $whatmatch ); #   plus what the function returns
        ####################################
    }
    $html = $line_copy . $line;

    ####################################
    # SET THE 'Display Only' VARIABLES.
    # These are variables identified as <<<VARIABLE>>> on the html page.
    #   They are used for Text only display on the html page. They are not
    #   used for any data input or updates to the SQL database,
    #   but are for display only on the html page, such as LOGINUSERNAME.
    #   they ARE written to the TMPfile, unless skipped in the <<>> section.
    ####################################
    $line      = $html;
    $line_copy = '';
    while ( $line =~ /<<<([^>]+)>>>/ ) {
        $whatmatch = $1;    # what matched
        $prematch  = $`;    # before what matched
        $line      = $';    # now set to after what matched
                            #   (check %form, then %ENV for match)
        if ( defined( $form->{$whatmatch} ) ) {
            ( $text = $form->{$whatmatch} ) =~ s/"/&quot;/g;
            $line_copy .= $prematch . $text;
        }
        elsif ( defined( $ENV{$whatmatch} ) ) {
            ( $text = $ENV{$whatmatch} ) =~ s/"/&quot;/g;
            $line_copy .= $prematch . $text;
        }
        else { $line_copy .= $prematch; }
    }
    $html = $line_copy . $line;

    ####################################
    # SET THE HTML PAGE INPUT VARIABLES.
    # These are variables identified as <<VARIABLE>> on the html page.
    #   They are substituted with the corresponding key/value from the
    #   associative arrays %form (SQL database), or %ENV (server environment)
    # Anywhere in the html page <<...>> is found is checked for
    #   1. ... in the %form associative array
    #   2. ... in the %ENV associative array
    #   3. ... being some form of name=checkbox for INPUT TYPE=checkbox
    #   4. ... being some for of name=value for INPUT TYPE=radio
    # See above in &FormSet description for some examples.
    ####################################
    # Initialize our variables
    ####################################
    my $skip  = {};
    my $radio = {};

    #warn qq|\n\ngetHTML CHECK skip:\n|;
    #foreach my $f ( sort keys %{$skip} ) { warn qq|skip: $f=$skip->{$f}\n|; }

    ####################################
    # Search for variables in the current html
    #   these are FORM INPUT variables in html,
    #   they DO NOT get written in data 'session' template.
    ####################################
    $line      = $html;
    $line_copy = '';
    while ( $line =~ /<<([^>]+)>>/ ) {
        $whatmatch = $1;    # what matched
        $prematch  = $`;    # before what matched
        $line      = $';    # now set to after what matched
        ####################################
        # Check %form, then %ENV for match
        # FIELD_SET is set to know which fields are INPUT on the FORM
        #     or not session template fields
        #     and which fields are NOT sent by the form so must be
        #     read from the session template.
        #   CheckBoxes are always set as session template so if not
        #     transmitted by the form they will be set to 0
        #     from the session template
        ####################################
        if ( defined( $form->{$whatmatch} ) ) {
            ( $text = $form->{$whatmatch} ) =~ s/"/&quot;/g;
            $line_copy .= $prematch . $text;
            $skip->{$whatmatch} = 1;
        }
        elsif ( defined( $ENV{$whatmatch} ) ) {
            ( $text = $ENV{$whatmatch} ) =~ s/"/&quot;/g;
            $line_copy .= $prematch . $text;
            $skip->{$whatmatch} = 1;
        }
        elsif ( $whatmatch =~ /(.+?)=checkbox/ ) {
            $line_copy .= $prematch;    # copy set to before what matched
            $line_copy .= "CHECKED" if ( $form->{$1} == 1 );
            $form->{$1} = 0;            # set to NOT CHECKED (1=CHECKED)
            $whatmatch = $1;
        }
        elsif ( $whatmatch =~
            /(.+?)=(.*)=selectlist/ ) # selectlist, CANNOT use a NULL for match!
        {
            $line_copy .= $prematch;    # copy set to before what matched
            $whatmatch = $1;
            if ( $form->{$1} eq $2 ) {
                $line_copy .= "SELECTED";
            }
        }
        elsif ( $whatmatch =~
            /(.+?)=(.*)/ )    # radio button, CANNOT use a NULL for match!
        {
            $line_copy .= $prematch;    # copy set to before what matched
            $whatmatch = $1;
            if ( $form->{$1} eq $2 && !$radio{$1} ) {
                $line_copy .= "CHECKED";
                $form->{$1} = '';       # set to NOT CHECKED (null)
                $radio{$1} = 1;
            }
        }
        else {
            $line_copy .= $prematch;    # copy set to before what matched
            $skip->{$whatmatch} = 1;
        }
    }
    $html = $line_copy . $line;

    ####################################
    # EXECUTES ANY FUNCTIONS WITHIN THE HTML PAGE.
    # first new: [[myHTML->rightpane(%form+search)]]
    ####################################
    $line      = $html;
    $line_copy = '';
    while ( $line =~ /\[\[(.+?)\]\]/ ) {
        $whatmatch = $1;
        $prematch  = $`;
        $line      = $';            # now set to after what matched
        $line_copy .= $prematch;    # copy set to before what matched
        $line_copy .=
          myDBI->exFunc( $form, $whatmatch ); #   plus what the function returns
    }
    $html = $line_copy . $line;
    close(TEMPLATE);

    ####################################
    # Convert any Tabs in html (<!--TAB:   )
    ####################################
    $html = gHTML->setTabs( $form, $html );

    ####################################
    # Save / write out to TMP file
    #   and add in hidden vars.
    ####################################
    my $hidden = myDBI->TMPwrite( $form, $skip ) unless ($NoTMP);
    $html =~ s|</LOADHIDDEN>|${hidden}|g;

    return ($html);
}
############################################################################
# set INPUT HTML form from xTables/xTableFields definitions.
sub setHTML {
    my ( $self, $form, $table ) = @_;
    my $html = qq|  <TABLE CLASS="home fullsize" >|;

    #$html .= qq| /* START */\n|;
    my $cdbh =
      myDBI->dbconnect('okmis_config');    # connect to the config database.

#  my $s=$cdbh->prepare("select * from misTables where theTable='${table}' order by seq");
    my $sxTables = $cdbh->prepare(
"select xTables.theTable,xTableFields.* from xTables left join xTableFields on xTableFields.TableID=xTables.ID where xTables.theTable=? order by theSeq"
    );
    $sxTables->execute($table);
    while ( my $rxTables = $sxTables->fetchrow_hashref ) {
        $html .=
qq|<SCRIPT LANGUAGE="JavaScript">newtextMsg('help$rxTables->{theField}','$rxTables->{Defn}');</SCRIPT>\n|;

#foreach my $f ( sort keys %{$rxTables} ) { warn "setHTML: rxTables-${f}=$rxTables->{$f}\n"; }
        my $type = $rxTables->{'theType'};
        my $text = $rxTables->{'theText'};

#warn qq|theTable=$rxTables->{'theTable'}, theField=$rxTables->{'theField'}, theType=$rxTables->{'theType'}, theText=$rxTables->{'theText'} \n|;
        my $name = $table . '_' . $rxTables->{'theField'} . '_1';
        my $onchange =
            $rxTables->{'onchange'} eq '' ? ''
          : $type  =~ 'radio'
          || $type =~ 'checkbox' ? qq|ONCLICK="$rxTables->{'onchange'}"|
          : qq|ONCHANGE="$rxTables->{'onchange'}"|;
        my $colspan =
          $rxTables->{'colspan'} eq ''
          ? ''
          : qq|COLSPAN="$rxTables->{'colspan'}"|;
        my $size =
          $rxTables->{'theSize'} eq '' ? '' : qq|SIZE="$rxTables->{'theSize'}"|;
        my $style =
          $rxTables->{'theStyle'} eq ''
          ? ''
          : qq|STYLE="$rxTables->{'theStyle'}"|;

        #warn qq|theValues=$rxTables->{'theValues'}\n|;
        my @v = ();
        my @d = ();
        my ( $xref, $xtable, $fld, $id ) =
          split( ':', $rxTables->{'theValues'} );
        if ( $xref =~ /^xrefTable/ ) {
            my $ID  = $id eq ''  ? 'ID'    : $id;
            my $FLD = $fld eq '' ? 'Descr' : $fld;
            push( @v, "" );
            push( @d, 'unselected' );
            my $s = $cdbh->prepare(
                "select * from ${xtable} where Active=1 order by ${FLD}");
            $s->execute();
            while ( my $r = $s->fetchrow_hashref ) {
                push( @v, $r->{$ID} );
                push( @d, $r->{$FLD} );
            }
            $s->finish();
        }
        else {
            @v = split( /\|/, $rxTables->{'theValues'} );
            @d = split( /\|/, $rxTables->{'descriptors'} );
        }
        $html .= qq|    <TR ><TD CLASS="strcol" >&nbsp;</TD></TR>\n|
          if ( $rxTables->{'theArgs'} =~ /break-before/i );
        if ( $rxTables->{'theArgs'} =~ /print-descriptors/i
          )    # any thePreText we print with the descriptors if ask.
        {
            if ( $rxTables->{'theType'} ne 'selectlist' ) {
                $html .= qq|
      <TR >
        <TD CLASS="strcol heading" >$rxTables->{'thePreText'}&nbsp;</TD>|;
                foreach my $descriptor (@d) {
                    $html .= qq|      <TD CLASS="hdrtxt" >${descriptor}</TD>\n|;
                }
                $html .= qq|    </TR>\n|;
            }
        }
        elsif ( $rxTables->{'thePreText'} ne '' ) {
            $html .=
qq|    <TR >\n      <TD CLASS="strcol heading" >$rxTables->{'thePreText'}</TD></TR>\n|;
        }

        $html .= qq|    <TR ><TD ><TABLE >\n|
          if ( $rxTables->{'theArgs'} =~ /in-table/ );

        my ( $textrow, $textcol, $textlbl ) = ( '', '', '' );
        if ( $rxTables->{'theArgs'} =~ /separate-rows/ ) {
            $html .= qq|
    <TR > <TD CLASS="strcol" ${style} > $rxTables->{theText} </TD> </TR>
    <TR >|;
        }
        elsif ( $rxTables->{'theArgs'} =~ /separate-columns/ ) {
            $html .= qq|
    <TR >
      <TD CLASS="strcol" ${style} >$rxTables->{theText}</TD>|;
        }
        else {
            $textlbl = $rxTables->{theText};
            $html .= qq|
    <TR >|;
        }
        if ( $type eq 'textonly' ) {
            $html .= qq|
      <TD CLASS="strcol" ${style} >
        ${textlbl}
        &nbsp;
      </TD>|;
        }
        elsif ( $type eq 'text' ) {
            $html .= qq|
      <TD CLASS="strcol" ${style} >
        ${textlbl}
        <INPUT TYPE="text" NAME="${name}" VALUE="<<${name}>>" ONFOCUS="select()" ${onchange} ${size} >
      </TD>|;
        }
        elsif ( $type eq 'textarea' ) {
            $html .= qq|
      <TD CLASS="strcol" ${style} >
        ${textlbl}
        <TEXTAREA NAME="${name}" COLS="80" ROWS="$rxTables->{'theSize'}" WRAP="virtual" ><<${name}>></TEXTAREA>
      </TD>|;
        }
        elsif ( $type eq 'radio' ) {
            $html .= qq|
      <TD CLASS="strcol" ${style} >${textlbl}</TD>
|;
            foreach my $value (@v) {
                $html .= qq|
      <TD CLASS="hdrcol" >
        <INPUT TYPE="radio" NAME="${name}" ${onchange} VALUE="${value}" <<${name}=${value}>> >
      </TD>
|;
            }
        }
        elsif ( $type eq 'checkbox' ) {
            my $value = $rxTables->{'theValues'};
            $html .= qq|
      <TD CLASS="strcol" ${style} >
        <INPUT TYPE="checkbox" NAME="${name}" ${onchange} VALUE="${value}" <<${name}=${value}>> >
        ${textlbl}
      </TD>|;
        }
        elsif ( $type eq 'vradio' ) {
            $html .= qq|
      <TD>
  <TABLE >
    <TR> <TD CLASS="strcol" ${style} >${textlbl}</TD> </TR>
|;
            my $i = 0;
            foreach my $value (@v) {
                my $desc = $d[$i];
                $i++;
                $html .= qq|
    <TR>
      <TD CLASS="strcol" ${style} >
        <INPUT TYPE="radio" NAME="${name}" ${onchange} VALUE="${value}" <<${name}=${value}>> > ${desc}
      </TD>
    </TR>
|;
            }
            $html .= qq|
  </TABLE >
      </TD>
|;
        }
        elsif ( $type eq 'selectlist' ) {
            my $i    = 0;
            my $opts = '';
            foreach my $value (@v) {
                my $desc = $d[$i];
                $i++;
                $opts .=
qq|          <OPTION VALUE="${value}" <<${name}=${value}=selectlist>> >${desc}\n|;
            }
            $html .= qq|
      <TD CLASS="strcol" ${style}>
        ${textlbl}
        <SELECT ID="${name}" NAME="${name}" style="max-width: 800px;">
          ${opts}
        </SELECT>
      </TD>
|;
        }
        $html .= qq|\n    </TR>\n|;
        $html .= qq|    </TABLE></TD></TR>\n|
          if ( $rxTables->{'theArgs'} =~ /in-table/ );
        $html .=
qq|    <TR >\n      <TD CLASS="strcol" >$rxTables->{'thePostText'}</TD>\n|
          if ( $rxTables->{'thePostText'} ne '' );
        $html .= qq|    <TR ><TD CLASS="strcol" >&nbsp;</TD></TR>\n|
          if ( $rxTables->{'theArgs'} =~ /break-after/i );
    }
    $html .= qq|  </TABLE>\n|;
    $sxTables->finish();
    return ($html);
}
############################################################################
sub close {
    my ( $self, $reload ) = @_;
    my $opener =
      $reload eq ''
      ? ''
      : qq|
<SCRIPT>
    window.onunload = refreshParent;
    function refreshParent() {
        window.opener.location.reload();
    }
</SCRIPT>
|;
    my $html = qq|Content-Type: text/html; charset=ISO-8859-1

<HTML>
<HEAD> <TITLE>CLOSE</TITLE>
${opener}
</HEAD>
<BODY ONLOAD="javascript: window.close()" >
<INPUT TYPE="button" NAME="cancel" VALUE="close" ONCLICK="javascript: window.close()" >
</BODY>
</HTML>
|;
    return ($html);
}
############################################################################
sub setxTable {
    my ( $self, $form, $xtable, $SelectedIDs, $inpname, $inptype, $detail ) =
      @_;
    my $title = substr( $xtable, 1 );

    #warn qq|setxTable: xtable=${xtable}, IDs=${SelectedIDs}, title=${title}\n|;
    my $html = qq|<TABLE CLASS="home" >
  <TR><TD CLASS="txtheader">${title}</TD></TR>|;
    my $cdbh =
      myDBI->dbconnect('okmis_config');    # connect to the config database.
    my $q =
qq|select * from ${xtable} where Active=1 and ((CHAR_LENGTH(Code) - CHAR_LENGTH(REPLACE(Code, '.', ''))) / CHAR_LENGTH('.')) DIV 1 = 0 order by Code|;

    #warn qq|setxTable:\nq=${q}\n|;
    my $s = $cdbh->prepare($q);
    $s->execute();
    while ( my $r = $s->fetchrow_hashref ) {
        my $match   = PopUp->matchSelect( $SelectedIDs, $r->{'ID'} );
        my $checked = $match eq '' ? '' : 'CHECKED';
        my $onchange =
          qq|ONCHANGE="doShow('${inpname}','${inpname}_display');"|;
        if ( $r->{'ID'} =~
            /0000-0|2186-5/ )    # 2186-5 is xEthnicity, not in xRaces
        {
            $onchange =
              qq|ONCHANGE="doDisable(this,'${inpname}','${inpname}_display');"|;
        }
        $html .= qq|
      <TR>
        <TD CLASS="strcol" >
          <INPUT TYPE="${inptype}" NAME="${inpname}" ID="$r->{'Descr'}" VALUE="$r->{'ID'}" ${onchange} ${checked} > $r->{'Descr'} ($r->{'Code'} $r->{'ID'})
        </TD>
        <TD CLASS="strcol" >|
          . $self->setChild( $form, $xtable, $SelectedIDs, $inpname, $inptype,
            $r->{'Code'}, $detail )
          . qq|
        </TD>
      </TR>
|;
    }
    $html .= '</TABLE>';
    $s->finish();
    return ($html);
}

sub setChild {
    my ( $self, $form, $xtable, $SelectedIDs, $inpname, $inptype, $parent,
        $detail )
      = @_;

    #warn qq|setChild: SelectedIDs=${SelectedIDs}, parent=${parent}\n|;
    return () if ( $parent eq '' || !$detail );
    my $children = '';
    my $cdbh =
      myDBI->dbconnect('okmis_config');    # connect to the config database.
    my $q =
qq|select * from ${xtable} where SUBSTRING_INDEX(Code,'.',((CHAR_LENGTH(Code) - CHAR_LENGTH(REPLACE(Code, '.', ''))) / CHAR_LENGTH('.')) DIV 1)=? order by Code|;

    #warn qq|setChild:\nq=${q}\n|;
    my $s = $cdbh->prepare($q);
    $s->execute($parent);
    my $rows = $s->rows();
    while ( my $r = $s->fetchrow_hashref ) {
        my $match   = PopUp->matchSelect( $SelectedIDs, $r->{'ID'} );
        my $checked = $match eq '' ? '' : 'CHECKED';

        #warn qq|setChild: ID=$r->{ID}, match=${match}, checked=${checked}\n|;
        $children .= qq|
<li>
<TABLE>
      <TR>
        <TD CLASS="strcol" >
          <INPUT TYPE="${inptype}" NAME="${inpname}" ID="$r->{'Descr'}" VALUE="$r->{'ID'}" ONCHANGE="doShow('${inpname}','${inpname}_display');" ${checked} > $r->{'Descr'} ($r->{'Code'} $r->{'ID'})
        </TD>
        <TD CLASS="strcol" >|
          . $self->setChild( $form, $xtable, $SelectedIDs, $inpname, $inptype,
            $r->{'Code'}, $detail )
          . qq|
        </TD>
      </TR>
</TABLE>
</li>
|;
    }
    my $html = $rows == 0 ? '' : qq|
          <div class="accordion">
            <h3>&nbsp;</h3>
            <ul>
            ${children}
            </ul> 
          </div>
|;
    $s->finish();
    return ($html);
}
############################################################################
# set Category INPUT HTML checkboxes from table.
sub setCheckBoxRows {
    my ( $self, $form, $table, $list, $title, $group, $with ) = @_;
    my $where = $group eq '' ? '' : qq|where Category='${group}'|;
    my $legend =
        $group eq ''
      ? $title eq ''
          ? 'Select from below'
          : $title
      : $group;
    my $preCategory = $group;
    ( my $class = $legend ) =~ s/ /-/g;
    my $html = qq|
  <FIELDSET>
    <LEGEND>
      <U>${legend}</U><BR >
        <INPUT TYPE="checkbox" ID="${class}" CLASS="js-checkbox-group-toggle" data-group-target=".${class}" >
      Select/UnSelect All
      <BR >
    </LEGEND>
|;
    my $cdbh =
      myDBI->dbconnect('okmis_config');    # connect to the config database.
    my $s =
      $cdbh->prepare("select * from ${table} ${where} order by Category,Descr");
    $s->execute();

    while ( my $r = $s->fetchrow_hashref ) {
        my $ID       = $r->{'ID'};
        my $Category = $r->{'Category'};
        if ( $Category ne $preCategory ) {
            if ( $preCategory ne '' ) {
                $html .= qq|
  </FIELDSET>
  <FIELDSET>
|;
            }
            $preCategory = $Category;
        }
        my $Descr = $r->{'Descr'};
        my $Defn  = $r->{'Defn'};
        my $Type  = $r->{'Type'};
        my $Name  = $r->{'Name'};
        my $Value = $r->{'Value'};
        $Defn .= '<BR>[' . $ID . ']' if ( $form->{'LOGINPROVID'} == 91 );
        my $label =
            $Defn eq ''
          ? $Descr
          : qq|      <A HREF="javascript:void(0)" TITLE="${Defn}" >${Descr}</A>|;
        $html .= qq|
    <LABEL FOR="${ID}" >
      <INPUT TYPE="${Type}" ID="${ID}" CLASS="${class}" NAME="${Name}" VALUE="${Value}" $list->{$ID} >
      ${label}
    </LABEL>
|;
    }
    $s->finish();
    $html .= qq|
  </FIELDSET>
|;
    return ($html);
}

sub setCheckBoxColumns {
    my ( $self, $form, $table, $sel, $title )        = @_;
    my ( $html, $out, $cols )                        = ( '', '', 0 );
    my ( $myColumns, $preRowName, $preDefn, $preID ) = ( '', '', '', '' );
    my $Title = $title eq '' ? 'Selections' : $title;

    # set the 'checked' list from those records that exist already...
    my $dbh  = myDBI->dbconnect( $form->{'DBNAME'} );
    my $list = ();
    if ( $sel ne '' ) {
        my $s = $dbh->prepare($sel);
        $s->execute() || myDBI->dberror("setCheckBoxColumns: ${sel}");
        while ( my $r = $s->fetchrow_hashref ) {
            $list->{ $r->{'ID'} } = 'CHECKED';
        }
        $s->finish();
    }

    my $cdbh =
      myDBI->dbconnect('okmis_config');    # connect to the config database.
    my @SetClass = ();
    my $ClassSet = ();
    my $NameSet  = ();

    # set the class's to check an entire column.
    my $s = $cdbh->prepare(
"select ColName,count(*) as colcount from ${table} ${where} group by ColName"
    );
    $s->execute();
    while ( my $r = $s->fetchrow_hashref ) {
        $cols++;
        my $ColName =
          $r->{'ColName'} eq '' ? 'Select from below' : $r->{'ColName'};
        ( my $class = $ColName ) =~ s/ /-/g;
        $ClassSet->{$ColName} = $class;
        $NameSet->{$class}    = $ColName;
        push( @SetClass, $class );
    }
    $s->finish();
    my $html = qq|
<!-- START GRID with 2 COLUMNS -->
  <DIV CLASS="ui-grid-a ui-responsive">
    <DIV CLASS="ui-block-a" >
      <SPAN>${Title}</SPAN>
    </DIV>
    <DIV CLASS="ui-block-b" >
|;
    foreach my $class (@SetClass) {
        $html .= qq|
      <SPAN>
        <INPUT TYPE="checkbox" ID="${class}" CLASS="js-checkbox-group-toggle" data-group-target=".${class}" >
        $NameSet->{$class}
      </SPAN>
|;
    }
    $html .= qq|
    </DIV>
|;
    my $s =
      $cdbh->prepare("select * from ${table} ${where} order by Seq,RowName");
    $s->execute();
    while ( my $r = $s->fetchrow_hashref ) {
        $cnt++;
        my $RowName = $r->{'RowName'};
        my $Defn    = $r->{'Defn'} eq '' ? $RowName : $r->{'Defn'};
        my $ID      = $r->{'ID'};

        # only first time through...
        $preRowName = $RowName if ( $preRowName eq '' );
        $preDefn    = $Defn    if ( $preDefn eq '' );
        $preID      = $ID      if ( $preID eq '' );

        #   save COLS until ROW name change (order by RowName)
        #     then set this ROW and begin new (out='')...
        #warn qq|setCheckBoxColumns: RowName=${RowName}/${preRowName}=\n|;
        if ( $RowName ne $preRowName ) {

            #warn qq|setCheckBoxColumns: RowName=${RowName}/${preRowName}=\n|;
            $preDefn .= '<BR>[' . $preID . ']'
              if ( $form->{'LOGINPROVID'} == 91 );
            my $label =
                $preDefn eq ''
              ? $preRowName
              : qq|      <A HREF="javascript:void(0)" TITLE="${preDefn}" >${preRowName}</A>|;

            #warn qq|setCheckBoxColumns: label=${label}=\n|;
            $myColumns .= qq|
    <!-- START ROW -->
    <!-- START COLUMN 1 -->
    <DIV CLASS="ui-block-a" >
      ${label}
    </DIV>
    <!-- START COLUMN 2 -->
    <DIV CLASS="ui-block-b" >
    ${out}
    </DIV>
    <!-- END ROW -->
|;
            $out        = '';
            $preRowName = $RowName;
            $preDefn    = $Defn;
            $preID      = $ID;
        }
        my $ColName =
          $r->{'ColName'} eq '' ? 'Select from below' : $r->{'ColName'};
        my $class = $ClassSet->{$ColName};
        $out .= qq|
      <SPAN STYLE="color: transparent" >
        <INPUT TYPE="$r->{Type}" ID="${ID}" CLASS="${class}" NAME="$r->{Name}" VALUE="$r->{Value}" $list->{$ID} >
        $NameSet->{$class}
      </SPAN>
|;
    }
    $s->finish();

    # and the last saved record for row...
    $preDefn .= '<BR>[' . $preID . ']' if ( $form->{'LOGINPROVID'} == 91 );
    my $label =
        $preDefn eq ''
      ? $preRowName
      : qq|      <A HREF="javascript:void(0)" TITLE="${preDefn}" >${preRowName}</A>|;
    $html .= $myColumns . qq|
    <!-- START COLUMN 1 -->
    <DIV CLASS="ui-block-a" >
      ${label}
    </DIV>
    <!-- START COLUMN 2 -->
    <DIV CLASS="ui-block-b" >
    ${out}
    </DIV>
  </DIV>
  <!-- END GRID with COLUMNS -->
|;
    return ($html);
}

sub set1CheckBoxColumn {
    my ( $self, $form, $sel, $checkboxname, $rowid, $colnames, $title,
        $SelectedIDs )
      = @_;

    #warn qq|myHTML-set1CheckBoxColumn: sel=${sel}\n|;
    #warn qq|myHTML-set1CheckBoxColumn: checkboxname=${checkboxname}\n|;
    #warn qq|myHTML-set1CheckBoxColumn: rowid=${rowid}\n|;
    #warn qq|myHTML-set1CheckBoxColumn: colnames=${colnames}\n|;
    #warn qq|myHTML-set1CheckBoxColumn: title=${title}\n|;
    #warn qq|myHTML-set1CheckBoxColumn: SelectedIDs=${SelectedIDs}\n|;
    my $dbh     = myDBI->dbconnect( $form->{'DBNAME'} );
    my $numcols = split( ':', $colnames );
    $numcols++;    # add 1 for checkbox.
    my $Title     = $title eq '' ? 'Selections' : $title;
    my @grids     = ( '0', 'solo', 'a', 'b', 'c', 'd' );
    my @blocks    = ( '0', 'a',    'b', 'c', 'd', 'e' );
    my $gridltr   = $grids[$numcols];
    my $column    = 1;
    my $columnltr = $blocks[$column];
    my $html      = qq|
<DIV data-role="header" >
  <DIV CLASS="txtheader" >${Title}</DIV>
</DIV>
|;
    return ($html) if ( $sel eq '' );

    $html .= qq|<DIV data-role="main" class="ui-content">
<!-- START GRID with ${numcols} COLUMNS -->
  <DIV CLASS="ui-grid-${gridltr} ui-responsive">
    <DIV CLASS="ui-block-${columnltr}" STYLE="text-align: center; text-decoration: underline;" >
      <SPAN >
        &nbsp;
        <INPUT TYPE="checkbox" NAME="set1CheckBoxColumn" VALUE="1" ONCHANGE="setCheckBox(this.checked,'${checkboxname}')" >
        &nbsp;
      </SPAN>
    </DIV>
|;
    foreach my $col ( split( ':', $colnames ) ) {
        $column++;
        my $columnltr = $blocks[$column];
        my ( $fld, $name, $just ) = split( '~', $col );
        my $label = $name eq '' ? $fld : $name;

        #warn qq|myHTML-set1CheckBoxColumn: fld=${fld}, name=${name}\n|;
        $html .= qq|
    <DIV CLASS="ui-block-${columnltr} ${just}" STYLE="text-decoration: underline;" >
      <SPAN >
        ${label}
      </SPAN>
    </DIV>
|;
    }
    my $s = $dbh->prepare($sel);
    $s->execute();
    while ( my $r = $s->fetchrow_hashref ) {
        $cnt++;
        my $column    = 1;
        my $columnltr = $blocks[$column];
        my $match     = PopUp->matchSelect( $SelectedIDs, $r->{$rowid} );
        my $checked   = $match eq '' ? '' : 'CHECKED';
        $html .= qq|
    <!-- START ROW -->
    <!-- START COLUMN -->
    <DIV CLASS="ui-block-${columnltr} hdrcol" >
      <SPAN STYLE="color: transparent" >
        &nbsp;
        <INPUT TYPE="checkbox" NAME="${checkboxname}" VALUE="$r->{$rowid}" ${checked} >
        &nbsp;
      </SPAN>
    </DIV>|;
        foreach my $col ( split( ':', $colnames ) ) {
            $column++;
            my $columnltr = $blocks[$column];
            my ( $fld, $name, $just ) = split( '~', $col );

            #warn qq|myHTML-set1CheckBoxColumn: fld=${fld}, name=${name}\n|;
            $html .= qq|
    <!-- START COLUMN -->
    <DIV CLASS="ui-block-${columnltr} ${just}" >
      <SPAN >
        $r->{$fld}
      </SPAN>
    </DIV>|;
        }
        $html .= qq|
    <!-- END ROW -->
|;
    }
    $s->finish();
    $html .= qq|
  </DIV>
  <!-- END GRID with COLUMNS -->
</DIV>
|;
    return ($html);
}

sub clientAddressForm {
    my ( $self, $form, $dlgid, $prefix, $addrsize ) = @_;

    if (   $form->{LOGINPROVID} ne 91
        && $form->{LOGINPROVID} ne 90
        && $form->{LOGINPROVID} ne 89 )
    {
        return;
    }

    my $html = qq|
<div id="$dlgid" title="Update address" style="display:none;">
  <form>
  <table>
|;
    if ( $addrsize eq 1 ) {
        $html .= qq|
    <tr>
      <td>Address</td>
      <td>
        <input type="text" id="${prefix}ClientAddrForm_address" class="text ui-widget-content ui-corner-all">
      </td>
    </tr>
|;
    }
    if ( $addrsize eq 2 ) {
        $html .= qq|
    <tr>
      <td>Address 1</td>
      <td>
        <input type="text" id="${prefix}ClientAddrForm_address1" class="text ui-widget-content ui-corner-all">
      </td>
    </tr>
    <tr>
      <td>Enter PO Box or Apt #</td>
      <td>
        <input type="text" id="${prefix}ClientAddrForm_address2" class="text ui-widget-content ui-corner-all">
      </td>
    </td>
|;
    }
    $html .= qq|
    <tr>
      <td>City</td>
      <td>
        <input type="text" id="${prefix}ClientAddrForm_city" class="text ui-widget-content ui-corner-all">
      </td>
    <tr>
      <td>County</td>
      <td>
        <input type="text" id="${prefix}ClientAddrForm_county" class="text ui-widget-content ui-corner-all">
      </td>
    </tr>
    <tr>
      <td>State</td>
      <td>
        <input type="text" id="${prefix}ClientAddrForm_state" class="text ui-widget-content ui-corner-all">
      </td>
    </tr>
    <tr>
      <td>Zip</td>
      <td>
        <input type="text" id="${prefix}ClientAddrForm_zip" class="text ui-widget-content ui-corner-all">
      </td>
    </tr>

    <!-- Allow form submission with keyboard without duplicating the dialog button -->
    <input type="submit" tabindex="-1" style="position:absolute; top:-1000px">
  </table>
  </form>
</div>  
|;

    return ($html);
}
############################################################################
1;
