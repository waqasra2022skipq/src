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
my $form = DBForm->new();
my $dbh  = $form->dbconnect();
if ( $form->{'LOGINUSERID'} != 91 ) {
    $form->error(
        "Access Denied / Contact the MIS Help Desk for assistance or access.");
}

my $addLinks = qq|mlt=$form->{mlt}&misLINKS=$form->{misLINKS}|;

#foreach my $f ( sort keys %{$form} ) { warn "ManagePortal: form-$f=$form->{$f}\n"; }
my $flags = qq|noclock|;

# Start out the display.
## TEST NEW html = CALL
## TEST NEW html = CALL
## TEST NEW html = CALL
my $html = myHTML->new( $form, $title, 'noclock' ) . qq|
<TABLE CLASS="main" >
  <TR ALIGN="center" >
    <TD WIDTH="84%" >
| . myHTML->hdr($form) . qq|
<LINK HREF="|
  . myConfig->cfgfile( 'menuV2.css', 1 )
  . qq|" REL="stylesheet" TYPE="text/css" >
<script src="/cgi/menu/js/menuV2.js" type="text/javascript"></script>
<SCRIPT LANGUAGE="JavaScript" SRC="/src/cgi/js/vEntry.js"> </SCRIPT>
<SCRIPT LANGUAGE="JavaScript" SRC="/src/cgi/js/ajaxrequest.js"> </SCRIPT>
<LINK HREF="|
  . myConfig->cfgfile( 'tabcontent/template6/tabcontent.css', 1 )
  . qq|" REL="stylesheet" TYPE="text/css" >
<SCRIPT SRC="|
  . myConfig->cfgfile( 'tabcontent/tabcontent.js', 1 )
  . qq|" TYPE="text/javascript" ></SCRIPT>
<SCRIPT LANGUAGE="JavaScript" TYPE="text/javascript" SRC="/src/cgi/js/tabs.js"></SCRIPT>
<LINK REL="STYLESHEET" TYPE="text/css" HREF="/src/cgi/css/tabs.css" />
<FORM NAME="ClientPage" ACTION="/src/cgi/bin/mis.cgi" METHOD="POST" >
<TABLE CLASS="main fullsize" >
  <TR >
    <TD CLASS="strcol" >Manage Client Portal Page:<BR>$form->{'LOGINUSERNAME'} </TD>
    <TD CLASS="info numcol" > ${BackLinks} ${AddNote} ${PhysNote}</TD>
  </TR>
</TABLE>
<TABLE CLASS="home fullsize" >
  <TR >
    <TD CLASS="strcol" >
      <DIV CLASS="port hdrcol" >Current Clients</DIV>
      <DIV><A HREF="/src/cgi/bin/mis.cgi?logout=1&mlt=<<mlt>>" ONMOUSEOVER="window.status='Logout of MIS'; return true;" ONMOUSEOUT="window.status=''" >Logout</A></DIV>
    </TD>
  </TR>
</TABLE>
| . main->listUsers();

$form->complete();
print $html;
exit;

############################################################################
sub listUsers {
    my ($self) = @_;
    my $s = $dbh->prepare("select * from UserLogin where type=1 order by ID");
    $s->execute() || $form->dberror("listUsers: select UserLogin");
    my $rows = $s->rows;
    my $html = qq|
<TABLE CLASS="home fullsize" >
  <TR >
    <TD CLASS="strcol" >
      <DIV CLASS="port hdrcol" >rows: ${rows}</DIV>
|;
    while ( my $r = $s->fetchrow_hashref ) {
        my $ref = qq|/cgi/bin/ClientPortal.cgi?THEUSER=$r->{'ID'}&${addLinks}|;
        $html .= qq|
      <DIV CLASS="port hdrcol" >id: $r->{ID}</DIV>
        <DIV >
          loginid:
          <A HREF="${ref}" ONMOUSEOVER="window.status=''; return true;" ONMOUSEOUT="window.status=''" >$r->{'loginid'}</A>
        </DIV> 
        <DIV >UserID: $r->{'UserID'} renew: $r->{'renew'}</DIV> 
        <DIV >dbname: $r->{'dbname'}</DIV> 
        <DIV >password: $r->{'Password'}</DIV> 
        <DIV >loginscreen: $r->{'loginscreen'}</DIV> 
|;
    }
    $html .= qq|
    </TD>
  </TR>
</TABLE>
|;
    $s->finish();
    return ($html);
}
############################################################################
