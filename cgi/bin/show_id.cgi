#!/usr/bin/perl
use lib 'C:/xampp/htdocs/src/lib';
use DBI;
use myForm;
use myDBI;
use myHTML;

############################################################################
my $form = DBForm->new();
my $form = myForm->new();

#foreach my $f ( sort keys %{$form} ) { warn ": form-$f=$form->{$f}\n"; }
my $dbh = myDBI->dbconnect( $form->{'DBNAME'} );
unless ( $form->{LOGINPROVID} == 91 ) { myDBI->error("Page DENIED!"); }

my $table = $form->{'action'};
my $ID    = $form->{'IDs'};
my $RECID = myDBI->getTableConfig( $table, 'RECID' );

#warn qq|select * from ${table} where ${RECID}=?, ID=${ID}\n|;
my ( $printfile, $pathname, $url ) = ( '', '', '<TR><TD>no xml</TD></TR>' );
my $s1 = $dbh->prepare("select * from ${table} where ${RECID}=?");

# if table name starts with "x" then connect to okmis_config db

if ( $table =~ /^x/ ) {
    $s1 = $dbh->prepare("select * from okmis_config.${table} where ${RECID}=?");
}
$s1->execute($ID);
my $r1 = $s1->fetchrow_hashref;
$s1->finish();
my $table2 = '';
if ( $table eq 'ClientPrAuth' || $table eq 'ClientDischarge' ) {
    $table2 = $table . 'CDC';
    $s2     = $dbh->prepare("select * from ${table}CDC where ${table}ID=?");
    $s2->execute($ID);
    $r2 = $s2->fetchrow_hashref;
    $s2->finish();
    $s3 = $dbh->prepare(
"select * from ${table}CDCSent where ${table}CDCID=? and xmlstring is not null order by ChangeDate desc"
    );
    $s3->execute( $r2->{ID} );
    if ( $r3 = $s3->fetchrow_hashref ) {
        my ( $head, $xml ) = split( '\<', $r3->{xmlstring}, 2 );
        $printfile = '/tmp/show_' . DBUtil->genToken() . '.xml';
        $pathname  = $form->{DOCROOT} . $printfile;
        $url =
qq|<TR><TD>xmlfile: <A HREF="javascript:ReportWindow('${printfile}','PrintWindow')" ONMOUSEOVER="textMsg.show('print')" ONMOUSEOUT="textMsg.hide()" ><IMG ALT="print" SRC="/images/icon_print.gif" BORDER="0" ></A></TD></TR>|;
        if ( open( XML, ">$pathname" ) ) { print XML '<' . $xml; close(XML); }
    }
    $s3->finish();
}
############################################################################
# Start out the display.
my $html =
  myHTML->newHTML( $form, 'Show Record',
    'CheckPopupWindow noclock countdown_1' )
  . qq|
<TABLE CLASS="main" >
  <TR> <TD CLASS="hdrcol title" >Show ${table}-${ID}</TD> </TR>
</TABLE>
<TABLE CLASS="home fullsize" >
|;
foreach my $f ( sort keys %{$r1} ) {
    $html .= qq|\n  <TR><TD>$f</TD><TD>$r1->{$f}</TD></TR>|;
}
$html .= qq|
  <TR><TD>edit: <A HREF="javascript:ReportWindow('/src/cgi/bin/te.pl?action=${table}&IDs=$r1->{$RECID}&mlt=$form->{'mlt'}&misLINKS=$form->{'misLINKS'}','PrintWindow')" ONMOUSEOVER="textMsg.show('edit')" ONMOUSEOUT="textMsg.hide()" ><IMG ALT="edit" SRC="/img/application-edit.png" BORDER="0" HEIGHT="20" WIDTH="20" ></A></TD></TR>
</TABLE>
|;
if ( $table2 ne '' ) {
    $html .= qq|
<TABLE CLASS="main" >
  <TR> <TD CLASS="hdrcol title" >Show ${table2}-${ID}</TD> </TR>
</TABLE>
<TABLE CLASS="home fullsize" >
|;
    foreach my $f ( sort keys %{$r2} ) {
        $html .= qq|\n  <TR><TD>$f</TD><TD>$r2->{$f}</TD></TR>|;
    }
    $html .= qq|
  <TR><TD>edit: <A HREF="javascript:ReportWindow('/src/cgi/bin/te.pl?action=${table2}&IDs=$r2->{$RECID}&mlt=$form->{'mlt'}&misLINKS=$form->{'misLINKS'}','PrintWindow')" ONMOUSEOVER="textMsg.show('edit')" ONMOUSEOUT="textMsg.hide()" ><IMG ALT="edit" SRC="/img/application-edit.png" BORDER="0" HEIGHT="20" WIDTH="20" ></A></TD></TR>
${url}
</TABLE>
|;
}
$html .= qq|
<FORM NAME="submit" ACTION="/cgi/bin/mis.cgi" METHOD="POST">
<INPUT TYPE="hidden" NAME="mlt" VALUE="$form->{mlt}" >
<INPUT TYPE="hidden" NAME="LINKID" VALUE="$form->{LINKID}" >
<INPUT TYPE="hidden" NAME="misLINKS" VALUE="$form->{misLINKS}" >
<BR><BR><BR><BR><BR><BR><BR><BR><BR><BR><BR><BR>
</FORM>
    </TD>
  </TR>
</TABLE>
</BODY>
</HTML>
|;

myDBI->cleanup();

print $html;
exit;
############################################################################
