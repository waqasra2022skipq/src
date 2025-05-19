#!C:/Strawberry/perl/bin/perl.exe
use lib 'C:/xampp/htdocs/src/lib';
use DBI;
use DBUtil;
use myForm;
use myHTML;
use gHTML;
use SysAccess;

############################################################################
my $form = myForm->new();
my $dbh  = myDBI->dbconnect( $form->{'DBNAME'} );
print qq|Location: https://time.paycheckrecords.com/login.jsf\n\n|
  if ( $form->{'DBNAME'} eq 'okmis_mms' );
my $query  = qq|select * from Timesheet where ProvID=? order by LoginTime desc|;
my $select = $dbh->prepare($query);

my $ForProvID =
  $form->{Provider_ProvID} ? $form->{Provider_ProvID} : $form->{LOGINPROVID};
$form->{Provider_ProvID} = $ForProvID;
my $qProvider = qq|select * from Provider where ProvID=?|;
my $sProvider = $dbh->prepare($qProvider);
$sProvider->execute($ForProvID);
my $rProvider = $sProvider->fetchrow_hashref;
############################################################################
if ( $form->{UpdateTables} ) {
    unless ( DBA->updSQLdone($form) ) {
        my $stamp = DBUtil->Date( '', 'stamp' );
        if ( $form->{Type} =~ /login/i ) {
            my $query =
qq|insert into Timesheet (ProvID,LoginTime,InIP,CreateDate,CreateProvID) values (${ForProvID},'${stamp}','$ENV{REMOTE_ADDR}','$form->{TODAY}',$form->{LOGINPROVID})|;
            my $insert = $dbh->prepare($query);
            $insert->execute();
            $insert->finish();
        }
        else {
            my $f = ();    # find on ProvID/LogoutTime is null.
            $f->{ProvID} = ${ForProvID};
            my $u = ();
            $u->{ProvID}       = ${ForProvID};
            $u->{LogoutTime}   = ${stamp};
            $u->{OutIP}        = $ENV{REMOTE_ADDR};
            $u->{CreateDate}   = $form->{TODAY};
            $u->{CreateProvID} = $form->{LOGINPROVID};
            $u->{ChangeProvID} = $form->{LOGINPROVID};
            DBA->update( $form, 'Timesheet', 'ProvID:LogoutTime', $f, $u );
        }
    }
}
############################################################################
# The display.
my $url =
  myForm->genLink('Provider') . "&mlt=$form->{mlt}&misLINKS=$form->{misLINKS}";
my $cnt = 0;
$form->{'FORMID'} = myDBI->getFORMID($form);
my $Edit;
if ( SysAccess->verify( $form, 'Privilege=Agent' ) ) {
    $Edit =
qq|      <INPUT TYPE="submit" ONCLICK="return validate(this.form);" NAME="view=ListProviderTimesheet.cgi&${url}&fwdTABLE=Provider&pushID=$form->{LINKID}&NONAVIGATION=1" VALUE="Edit Entries">|;
}

# Start out the display.
my $html =
  myHTML->newHTML( $form, 'TimeClock', 'CheckPopupWindow noclock countdown_10' )
  . qq|
<SCRIPT LANGUAGE="JavaScript1.2" > function validate() { return(1); } </SCRIPT>
<TABLE CLASS="main fullsize" >
  <TR ALIGN="left" >
    <TD >
<A NAME="top">
<TABLE CLASS="main fullsize" >
  <TR >
    <TD CLASS="strcol" >
      $rProvider{FName} $rProvider->{'FName'} $rProvider->{'LName'} ($rProvider->{'ProvID'})
      <BR>Time Clock Entries
    </TD>
    <TD CLASS="numcol" >&nbsp;</TD>
  </TR>
</TABLE>
<FORM NAME="TimeClock" ACTION="/src/cgi/bin/TimeClock.cgi" METHOD="POST" >
| . main->genList( ${ForProvID} ) . qq|
<TABLE CLASS="port fullsize" >
  <TR >
    <TD CLASS="hdrcol" >
|;
$html .= qq|
      <INPUT TYPE="submit" ONCLICK="return validate(this.form);" NAME="Type=Login&UpdateTables=all${url}" VALUE="Clock In">
      <INPUT TYPE="submit" ONCLICK="return validate(this.form);" NAME="Type=Logout&UpdateTables=all${url}" VALUE="Clock Out">
| if ( $form->{LOGINPROVID} == $ForProvID );
$html .= qq|
      <INPUT TYPE="submit" ONCLICK="return validate(this.form);" NAME="${url}" VALUE="Refresh">
|;
$html .= qq|
    </TD>
  </TR>
  <TR CLASS="hdrcol" ><TD >Click on the appropriate link to clock in or clock out.</TD></TR>
  <TR CLASS="hdrcol" ><TD ><FONT COLOR=red >Note:</FONT> If you forget to clock in or clock out for a given period just simply do it now AND THEN clock in/clock out to start/end the new period. You may clock out as many times as it takes to fix any times forgotten to clock out.</TD></TR>
  <TR CLASS="hdrcol" ><TD ><FONT COLOR=red >DO NOT</FONT> use the Browser Refresh or an extra clock in or clock out will be created.</TD></TR>
  <TR CLASS="hdrcol" ><TD > [<A HREF="#top" >top</A>] </TD></TR>
</TABLE>
<INPUT TYPE=hidden NAME="FORMID" VALUE="$form->{FORMID}" >
<INPUT TYPE=hidden NAME="LINKID" VALUE="$form->{LINKID}" >
</FORM>
<FORM NAME="TimeClock" ACTION="/src/cgi/bin/mis.cgi" METHOD="POST" >
<TABLE CLASS="main fullsize" >
  <TR > <TD CLASS="numcol" > ${Edit} </TD> </TR>
</TABLE>
<INPUT TYPE=hidden NAME="FORMID" VALUE="$form->{FORMID}" >
<INPUT TYPE=hidden NAME="LINKID" VALUE="$form->{LINKID}" >
</FORM>
|;

$select->finish();
$sProvider->finish();
myDBI->cleanup();

#warn qq|TimeClock:\n${html}\n|;
print $html;
exit;
############################################################################
sub genList {
    my ( $self, $ProvID ) = @_;
    my $out = qq|
<HR WIDTH="90%" >
<TABLE CLASS="port fullsize" >
  <TR >
    <TD CLASS="hdrcol" COLSPAN="7" >
      Time Sheet Information<BR>(last 20 by decending datetime)
    </TD>
  </TR>
  <TR CLASS=${cls} >
    <TD ALIGN="center" COLSPAN=3 >Clock In</TD>
    <TD ALIGN="center" COLSPAN=3 >Clock Out</TD>
    <TD ALIGN="center" >&nbsp;</TD>
  </TR>
  <TR CLASS=${cls} >
    <TD ALIGN="left" >Date</TD>
    <TD ALIGN="left" >Time</TD>
    <TD ALIGN="left" >IP</TD>
    <TD ALIGN="left" >Date</TD>
    <TD ALIGN="left" >Time</TD>
    <TD ALIGN="left" >IP</TD>
    <TD ALIGN="left" >Hours</TD>
  </TR>
<TR ><TD COLSPAN=2 >&nbsp;</TD></TR>
|;
    $select->execute($ProvID);
    while ( my $record = $select->fetchrow_hashref ) {
        $cnt++;
        last if ( $cnt > 20 );
        my $even = int( $cnt / 2 ) == $cnt / 2 ? '1' : '0';
        if   ($even) { $cls = qq|rpteven|; }
        else         { $cls = qq|rptodd|; }
        my $indate, $intime;
        if ( $record->{LoginTime} ne '' ) {
            $indate =
                substr( $record->{LoginTime}, 4, 2 ) . '/'
              . substr( $record->{LoginTime}, 6, 2 ) . '/'
              . substr( $record->{LoginTime}, 0, 4 );
            $intime =
                substr( $record->{LoginTime}, 8, 2 ) . ':'
              . substr( $record->{LoginTime}, 10, 2 ) . ':'
              . substr( $record->{LoginTime}, 12, 2 );
        }
        my $outdate, $outtime, $Hours;
        if ( $record->{LogoutTime} ne '' ) {
            $outdate =
                substr( $record->{LogoutTime}, 4, 2 ) . '/'
              . substr( $record->{LogoutTime}, 6, 2 ) . '/'
              . substr( $record->{LogoutTime}, 0, 4 );
            $outtime =
                substr( $record->{LogoutTime}, 8, 2 ) . ':'
              . substr( $record->{LogoutTime}, 10, 2 ) . ':'
              . substr( $record->{LogoutTime}, 12, 2 );
            my $Duration = DBUtil->getDurationTS( $record->{LoginTime},
                $record->{LogoutTime} );
            $Hours = sprintf( "%.2f", $Duration / 3600 );
        }
        $out .= qq|
  <TR CLASS=${cls} >
    <TD ALIGN="left" >${indate}</TD>
    <TD ALIGN="left" >${intime}</TD>
    <TD ALIGN="left" >$record->{InIP}</TD>
    <TD ALIGN="left" >${outdate}</TD>
    <TD ALIGN="left" >${outtime}</TD>
    <TD ALIGN="left" >$record->{OutIP}</TD>
    <TD ALIGN="left" >${Hours}</TD>
  </TR>
|;
    }
    $out .= qq|
</TABLE>\n
<HR WIDTH="90%" >
|;
    return ($out);
}
#####################################################################
