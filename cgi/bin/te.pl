#!/usr/bin/perl
use lib '/var/www/okmis/src/lib';
use DBI;
use myDBI;
use myHTML;

############################################################################
my $form = myForm->new();
foreach my $f ( sort keys %{$form} ) { warn "te1: form-$f=$form->{$f}\n"; }
my $dbh = myDBI->dbconnect( $form->{'DBNAME'} );
unless ( $form->{LOGINPROVID} == 91 ) { myDBI->error("Page DENIED!"); }

my $table = $form->{'action'};
my $ID    = $form->{'IDs'};
my $RECID = myDBI->getTableConfig( $table, 'RECID' );
warn qq|select * from ${table} where ${RECID}=?, ID=${ID}\n|;
my $s1 = $dbh->prepare("select * from ${table} where ${RECID}=?");
$s1->execute($ID);
my $r1 = $s1->fetchrow_hashref;
$s1->finish();

#------------------------------------
# this section of code will simulate the...
#   setup backward-links
#   and getHTML-read/open all tables
#   and write out form variable
foreach my $f ( sort keys %{$form} ) { warn "te2: form-$f=$form->{$f}\n"; }
main->setIDs( $table, $ID );    # set the form uplink table ids..
foreach my $f ( sort keys %{$form} ) { warn "te3: form-$f=$form->{$f}\n"; }
myForm->TBLread($table);        # set the form hdrtables.
foreach my $f ( sort keys %{$form} ) { warn "te4: form-$f=$form->{$f}\n"; }
my $hidden = myDBI->TMPwrite( $form, $skip );
warn qq|CHECK: hidden=$hidden\n|;

#------------------------------------
############################################################################
# Start out the display.
my $html =
  myHTML->newHTML( $form, 'Edit Record',
    'CheckPopupWindow noclock countdown_1' )
  . qq|
<SCRIPT LANGUAGE="JavaScript" >
function validate(form)
{
  return true;
}
</SCRIPT>

<TABLE CLASS="main" >
  <TR> <TD CLASS="hdrcol title" >Edit ${table}-${ID}</TD> </TR>
</TABLE>
<FORM NAME="TableEdit" ACTION="/cgi/bin/mis.cgi" METHOD="POST">
<TABLE CLASS="home fullsize" >
|;
foreach my $f ( sort keys %{$r1} ) {
    ( my $text = $r1->{$f} ) =~ s/"/&quot;/g;
    $html .= qq|
  <TR>
    <TD>$f</TD>
    <TD>
      <INPUT TYPE="text" NAME="${table}_${f}_1" VALUE="${text}" SIZE="60" >
    </TD>
  </TR>|;
}
$html .= qq|
</TABLE>
<TABLE CLASS="main fullsize" >
  <TR>
    <TD CLASS="numcol" >
      <INPUT TYPE="submit" ONCLICK="return validate(this.form);" NAME="UpdateTables=all" VALUE="Add/Update">
    </TD>
  </TR>
</TABLE>
${hidden}
<INPUT TYPE="hidden" NAME="CLOSEWINDOW" VALUE="CLOSE">
<BR><BR><BR><BR><BR><BR><BR><BR><BR><BR><BR><BR>
</FORM>
    </TD>
  </TR>
</TABLE>
</BODY>
</HTML>
|;

#<INPUT TYPE="hidden" NAME="mlt" VALUE="$form->{mlt}" >
#<INPUT TYPE="hidden" NAME="LINKID" VALUE="$form->{LINKID}" >
#<INPUT TYPE="hidden" NAME="misLINKS" VALUE="$form->{misLINKS}" >
myDBI->cleanup();
print $html;
exit;
############################################################################
# sets the table/id up the tree...
# ie: for: ClientPrAuth/35762
#   set: form-ClientPrAuth_ID=35762
#   set: form-Insurance_InsNumID=39867
#   set: form-Client_ClientID=33339
sub setIDs {
    my ( $self, $table, $id ) = @_;
    return ('') if ( $table eq '' );
    return ('') if ( $id eq '' );
    warn qq|main:setIDs: table=$table, id=$id\n|;
    my $RECID = myDBI->getTableConfig( $table, 'RECID' );
    my $q     = qq|select * from ${table} where ${RECID}='${id}'|;
    my $s     = $dbh->prepare($q);
    $s->execute() || myDBI->dberror($q);
    my $r = $s->fetchrow_hashref;
    $form->{"${table}_${RECID}"} = $r->{$RECID};

#warn qq|first: ${table}-${RECID}: $form->{"${table}_${RECID}"} = $r->{$RECID};\n|;
    my $DETID = myDBI->getTableConfig( $table, 'DETAILID' );

    #warn qq| next: DETID=${DETID}, VAL=$r->{$DETID}\n|;
    my $hdrtable = $table;    # find HeaderTable for Table
    while ( defined( myConfig->tbl( $hdrtable, 'HEADERTABLE' ) ) ) {
        $hdrtable = myConfig->tbl( $hdrtable, 'HEADERTABLE' );
        $RECID    = myDBI->getTableConfig( $hdrtable, 'RECID' );

      #warn qq| next: hdrtable=${hdrtable}, RECID=${RECID}, VAL=$r->{$DETID}\n|;
        my $q = qq|select * from ${hdrtable} where ${RECID}='$r->{$DETID}'|;
        my $s = $dbh->prepare($q);
        $s->execute() || myDBI->dberror($q);
        $r = $s->fetchrow_hashref;
        $form->{"${hdrtable}_${RECID}"} = $r->{$RECID};

#warn qq| next: ${hdrtable}-${RECID}: $form->{"${hdrtable}_${RECID}"} = $r->{$RECID};\n|;
        $DETID = myDBI->getTableConfig( $hdrtable, 'DETAILID' );

        #warn qq| next: DETID=${DETID}, VAL=$r->{$DETID}\n|;
    }
    $s->finish();
    return ();
}
