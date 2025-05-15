#!/usr/bin/perl
use lib 'C:/xampp/htdocs/src/lib';
use DBI;
use DBForm;
use SysAccess;
use DBA;
use DBUtil;
use myHTML;
use gHTML;

############################################################################
my $form      = DBForm->new();
my $dbh       = $form->dbconnect();
my $ForProvID = $form->{ForProvID} ? $form->{ForProvID} : $form->{LOGINPROVID};
my $BackLinks = gHTML->setLINKS( $form, 'back' );
my $hidden    = $form->TMPwrite($skip);

############################################################################
# output the HTML
# Start out the display.
my $html = myHTML->new($form) . qq|
<TABLE CLASS="main" >
  <TR ALIGN="center" >
| . myHTML->leftpane( $form, 'clock mail managertree collapseipad' ) . qq|
    <TD WIDTH="84%" ALIGN="center" >
| . myHTML->hdr($form) . myHTML->menu($form) . qq|
<SCRIPT LANGUAGE="JavaScript" SRC="/src/cgi/js/novalidate.js"> </SCRIPT>
<FORM NAME="Appointments" ACTION="/cgi/bin/mis.cgi" METHOD="POST" >
<TABLE CLASS="main fullsize" >
  <TR ALIGN="left" >
    <TD >
<TABLE CLASS="port fullsize" >
  <TR >
    <TD CLASS="strcol" >Provider/Client Appointments<BR>Listed by Contact Date and Provider</TD>
    <TD CLASS="numcol" >${BackLinks}</TD>
  </TR>
</TABLE>
<TABLE CLASS="port fullsize" >
  <TR >
    <TD CLASS="strcol" >Appointments available to $form->{LOGINUSERNAME}<\TD>
    <TD CLASS="numcol" >
      <INPUT TYPE="submit" ONCLICK="return validate(this.form)" NAME="view=Appointments.cgi&UpdateTables=all&fwdTABLE=Appointments&Appointments_ID=new&pushID=$form->{LINKID}" VALUE="Add New Appointment" ONMOUSEOVER="window.status='new';return true;" ONMOUSEOUT="window.status=''" >
    </TD>
  </TR>
</TABLE>
<TABLE CLASS="home fullsize" >
  <TR >
    <TD CLASS="port hdrtxt" >Provider</TD>
    <TD CLASS="port hdrtxt" >Client</TD>
    <TD CLASS="port hdrtxt" >Contact Date</TD>
    <TD CLASS="port hdrtxt" >Begin Time</TD>
    <TD CLASS="port" >&nbsp;</TD>
  </TR>
| . main->genList() . qq|
</TABLE>
    </TD>
  </TR>
</TABLE>
${hidden}
</FORM >
| . myHTML->rightpane( $form, 'search' );
$form->complete();
print $html;
exit;

############################################################################
sub genList {
    my ($self) = @_;
    my ( $out, $cnt ) = ( '', 0 );
    my $qAppointments =
qq|select Appointments.*,Provider.LName,Provider.FName from Appointments left join Provider on Provider.ProvID=Appointments.ProvID |
      . DBA->getProviderSelection( $form, $ForProvID, 'Appointments.ProvID',
        'where' )
      . qq| order by ContactDate, LName, FName|;

    #warn qq|q=\n$qAppointments\n|;
    my $sAppointments = $dbh->prepare($qAppointments);
    $sAppointments->execute();
    while ( my $r = $sAppointments->fetchrow_hashref ) {
        $cnt += 1;
        $even = int( $cnt / 2 ) == $cnt / 2 ? '1' : '0';
        my $cls = 'rptodd';
        if ($even) { $cls = 'rpteven'; }
        my $ProviderName = $r->{'FName'} . ' ' . $r->{'LName'};
        my $ClientName =
            DBA->getxref( $form, 'Client', $r->{ClientID},   'FName' ) . ' '
          . DBA->getxref( $form, 'Client', $r->{'ClientID'}, 'LName' );
        my $ContactDate =
          DBUtil->Date( $r->{'ContactDate'}, 'fmt', 'MM/DD/YYYY' );
        $out .= qq|
  <TR CLASS="${cls}" >
    <TD CLASS="strcol" >${ProviderName}</TD>
    <TD CLASS="strcol" >${ClientName}</TD>
    <TD CLASS="hdrcol" >${ContactDate}</TD>
    <TD CLASS="hdrcol" >$r->{BeginTime}</TD>
    <TD CLASS="hdrcol" >
      <INPUT TYPE="submit" ONCLICK="return validate(this.form)" NAME="view=Appointments.cgi&fwdTABLE=Appointments&Appointments_ID=$r->{ID}&pushID=$form->{LINKID}" VALUE="View/Edit" ONMOUSEOVER="window.status='$r->{ID}';return true;" ONMOUSEOUT="window.status=''" >
    </TD>
  </TR>
|;
    }
    $sAppointments->finish();
    return ($out);
}
############################################################################
