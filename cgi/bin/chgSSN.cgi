#!/usr/bin/perl
use lib 'C:/xampp/htdocs/src/lib';
use DBI;
use myForm;
use myDBI;
use myHTML;
use SysAccess;

############################################################################
my $form = myForm->new();
my $dbh  = myDBI->dbconnect( $form->{'DBNAME'} );

#foreach my $f ( sort keys %{$form} ) { warn "chgSSN: form-$f=$form->{$f}\n"; }
if ( !SysAccess->chkPriv( $form, 'NewClient' ) ) {
    myDBI->error("New Client / Change SSN / Access Denied!");
}
if ( $form->{'ClientID'} eq '' ) { myDBI->error("Chanage SSN / NO ID!"); }

my $ClientID = $form->{'ClientID'};
my $sClient  = $dbh->prepare("select * from Client where ClientID=?");
$sClient->execute($ClientID)
  || myDBI->dberror("chgSSN: select Client ${ClientID}");
my $rClient = $sClient->fetchrow_hashref;
if   ( $form->{change} ) { print main->change(); }
else                     { print main->html(); }

$sClient->finish();

myDBI->cleanup();
exit;

############################################################################
sub validSSN {
    my ( $self, $SSN ) = @_;
    my $err = '';
    ( my $ssn = $SSN ) =~ s/^\s*(.*?)\s*$/$1/g;    # trim both leading/trailing
    warn qq|validSSN: ssn=${ssn}\n|;
    if    ( $ssn eq '' ) { $err = "SSN cannot be NULL! "; }
    elsif ( $ssn !~ /^\d{3}-\d{2}-\d{4}$/ ) {
        $err = qq|SSN MUST BE in the format ddd-dd-dddd!|;
    }
    else {
        warn qq|validSSN: READ: ssn=${ssn}\n|;
        my $sClient = $dbh->prepare("select * from Client where SSN='${ssn}'");
        $sClient->execute()
          || myDBI->dberror("validate: SSN: select Client (${ssn})");
        my $rClient = $sClient->fetchrow_hashref;
        my $rows    = $sClient->rows;
        warn qq|validSSN: ClientID=$rClient->{'ClientID'}, rows=${rows}\n|;
        $err = qq|SSN already exists! (${ssn})| if ( $rows > 0 );
        $sClient->finish();
    }
    return ($err);
}

sub html {
    my ( $self, $err ) = @_;
    my $MAINHDR = qq|CHANGE Social Security Number (SSN)|;
    my $SUBHDR1 = qq|$rClient->{FName} $rClient->{LName}|;

    # Start out the display.
    my $html =
      myHTML->newHTML( $form, 'Check SSN',
        'CheckPopupWindow noclock countdown_2' )
      . qq|
<TABLE CLASS="main" >
  <TR><TD CLASS="hdrcol banner" >${MAINHDR}</TD></TR>
  <TR> <TD CLASS="hdrcol title" >${SUBHDR1}</TD> </TR>
</TABLE>
<script TYPE="text/javascript" SRC="/src/cgi/js/ajaxrequest.js"></script>
<SCRIPT LANGUAGE="JavaScript" >
function validate(form)
{
  if ( form.SSN.value == "" ) { myAlert("SSN cannot be null",'Validation Alert!'); form.SSN.focus(); return false; }
  var ssnPat = /^\\d{3}-\\d{2}-\\d{4}\$/;
  var ssnMatch = form.SSN.value.match(ssnPat);
  if ( ssnMatch == null )
  { myAlert("SSN pattern MISmatch!",'Validation Alert!'); form.SSN.focus(); return false; }
  return true;
}
</SCRIPT>
<FORM NAME="ClientSSN" ACTION="/src/cgi/bin/chgSSN.cgi" METHOD="POST">
  <TABLE CLASS="home fullsize" >
    <TR><TD CLASS="hdrtxt" COLSPAN="2" >ORIGINAL SSN # $rClient->{'SSN'}</TD></TR>
    <TR><TD CLASS="hdrtxt" COLSPAN="2" >Please enter NEW SSN #</TD></TR>
    <TR><TD CLASS="hdrtxt" COLSPAN="2" ><SPAN ID="msgClientSSN" ><FONT COLOR="red" >${err}</FONT></SPAN></TD></TR>
    <TR>
      <TD CLASS="strcol" >NEW SSN:</TD>
      <TD CLASS="strcol" >
        <INPUT TYPE="text" ID="SSN" NAME="SSN" VALUE="" SIZE="11" ONFOCUS="select();" >
      </TD>
    </TR>
    <TR>
      <TD CLASS="numcol" COLSPAN="2" >
        <INPUT TYPE="submit" ONCLICK="return validate(this.form);" NAME="change" VALUE="change" >
        <INPUT TYPE="button" NAME="cancel" VALUE="cancel" ONCLICK="javascript: window.close()" >
      </TD>
    </TR>
  </TABLE>
  <INPUT TYPE="hidden" NAME="ClientID" VALUE="$form->{'ClientID'}" >
  <INPUT TYPE="hidden" NAME="mlt" VALUE="$form->{'mlt'}" >
  <SCRIPT LANGUAGE="JavaScript">
    document.ClientSSN.elements[0].focus();
  </SCRIPT>
</FORM>
    </TD>
  </TR>
</TABLE>
</BODY>
</HTML>
|;
    return ($html);
}

sub change {
    my $SSN  = $form->{'SSN'};
    my $err  = main->validSSN($SSN);
    my $html = myHTML->close(1);
    if ( $err eq '' ) {

        #warn qq|chgnSSN: update....ClientID=$ClientID\n|;
        my $rUpdate = ();
        $rUpdate->{'SSN'}          = $SSN;
        $rUpdate->{'ChangeProvID'} = $form->{'LOGINPROVID'};

#foreach my $f ( sort keys %{$rUpdate} ) { warn "chgSSN 1: rUpdate-$f=$rUpdate->{$f}\n"; }
        my $ID1 =
          DBA->doUpdate( $form, 'Client', $rUpdate, "ClientID='${ClientID}'" );
    }
    else { $html = main->html($err); }
    return ($html);
}
############################################################################
