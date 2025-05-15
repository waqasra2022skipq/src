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

#foreach my $f ( sort keys %{$form} ) { warn "authPA: form-$f=$form->{$f}\n"; }
if (
    !(
           SysAccess->chkPriv( $form, 'ClinicManager' )
        || SysAccess->chkPriv( $form, 'Agent' )
    )
  )
{
    myDBI->error("Manual Auth / Access Denied!");
}
if ( $form->{'PrAuthID'} eq '' ) { myDBI->error("Manual Auth / NO ID!"); }

my $PrAuthID = $form->{'PrAuthID'};
my $sPrAuth  = $dbh->prepare("select * from ClientPrAuth where ID=?");
$sPrAuth->execute($PrAuthID)
  || myDBI->dberror("authPA: select PrAuth ${PrAuthID}");
my $rPrAuth = $sPrAuth->fetchrow_hashref;
my $sPrAuthCDC =
  $dbh->prepare("select * from ClientPrAuthCDC where ClientPrAuthID=?");
$sPrAuthCDC->execute($PrAuthID)
  || myDBI->dberror("authPA: select PrAuthCDC ${PrAuthID}");
my $rPrAuthCDC = $sPrAuthCDC->fetchrow_hashref;
if   ( $form->{submit} ) { print main->submit(); }
else                     { print main->html(); }

$sPrAuth->finish();
$sPrAuthCDC->finish();

myDBI->cleanup();
exit;

############################################################################
sub submit {
    my $Reason  = $form->{'Reason'};
    my $AuthNum = $form->{'AuthNum'};
    my $CDCKey  = $form->{'CDCKey'};
    my $html    = myHTML->close(1);
    if ( $Reason eq '' || $AuthNum eq '' ) {
        $html = main->html("Reason or AuthNum CANNOT be null!");
    }
    else {
        #warn qq|update....PrAuthID=$PrAuthID\n|;
        my $PAgroup   = $rPrAuth->{'PAgroup'};
        my $LinesAuth = DBA->getxref( $form, 'xPAgroups', $PAgroup, 'PAlines' );
        my $EffDate   = $rPrAuth->{'EffDate'};
        my ( $months, $days ) = DBA->calcLOS( $form, '100', $PAgroup );
        my $Age     = DBUtil->Date( $rPrAuth->{'DOB'}, 'age', $EffDate );
        my $which   = $Age < 21 ? 'ChildAmt' : 'AdultAmt';
        my $Cost    = DBA->getxref( $form, 'xPAgroups', $PAgroup, $which );
        my $Units   = DBA->getxref( $form, 'xPAgroups', $PAgroup, 'Units' );
        my $rUpdate = ();
        $rUpdate->{PAnumber}       = $AuthNum;
        $rUpdate->{'ExpDate'}      = DBUtil->Date( $EffDate, $months, $days );
        $rUpdate->{'LOS'}          = $months;
        $rUpdate->{'LinesAuth'}    = $LinesAuth;
        $rUpdate->{'AuthAmt'}      = $Cost * $LinesAuth;
        $rUpdate->{'UnitsAuth'}    = $Units;    # used if >0 (Inv.pm)
        $rUpdate->{'Locked'}       = 1;
        $rUpdate->{'ChangeProvID'} = $form->{'LOGINPROVID'};

#foreach my $f ( sort keys %{$rUpdate} ) { warn "authPA 1: rUpdate-$f=$rUpdate->{$f}\n"; }
        my $ID1 =
          DBA->doUpdate( $form, 'ClientPrAuth', $rUpdate, "ID='${PrAuthID}'" );
        my $rUpdateCDC = ();
        $rUpdateCDC->{Status}         = 'Approved';
        $rUpdateCDC->{StatusDate}     = $form->{TODAY};
        $rUpdateCDC->{Reason}         = 'Manual: ' . $Reason;
        $rUpdateCDC->{Fail}           = '';
        $rUpdateCDC->{CDCKey}         = $CDCKey if ( $CDCKey ne '' );
        $rUpdateCDC->{'ChangeProvID'} = $form->{'LOGINPROVID'};

#foreach my $f ( sort keys %{$rUpdateCDC} ) { warn "authPA 2: rUpdateCDC-$f=$rUpdateCDC->{$f}\n"; }
        my $ID2 = DBA->doUpdate( $form, 'ClientPrAuthCDC', $rUpdateCDC,
            "ClientPrAuthID='${PrAuthID}'" );

        Inv->setPALines( $form, $PrAuthID );

        delete $rPrAuthCDC->{"ClientPrAuthID"};    # remove ID to the PrAuth.
        $rPrAuthCDC->{"ClientPrAuthCDCID"} = $ID2;    # attach to the CDC.
        $rPrAuthCDC->{'Status'}            = $rUpdateCDC->{'Status'};
        $rPrAuthCDC->{'StatusDate'}        = $rUpdateCDC->{'StatusDate'};
        $rPrAuthCDC->{'Reason'}            = $rUpdateCDC->{'Reason'};
        $rPrAuthCDC->{'CDCKey'}            = $rUpdateCDC->{'CDCKey'};
        $rPrAuthCDC->{'ChangeProvID'}      = $rUpdateCDC->{'ChangeProvID'};
        my $LogID = DBA->doUpdate( $form, "ClientPrAuthCDCSent", $rPrAuthCDC );
        CDC->Lock( $form, 'ClientPrAuth', $PrAuthID, 1 );
    }
    return ($html);
}

sub html {
    my ( $self, $Client, $Dates ) = @_;
    my $sClient = $dbh->prepare("select * from Client where ClientID=?");
    $sClient->execute( $rPrAuth->{'ClientID'} )
      || myDBI->dberror("authPA: select Client $rPrAUth->{'ClientID'}");
    my $rClient = $sClient->fetchrow_hashref;
    $sClient->finish();
    my $MAINHDR = qq|Manually Authorize PA|;
    my $SUBHDR1 = qq|$rClient->{FName} $rClient->{LName}|;
    my $SUBHDR2 = qq|$rPrAuth->{EffDate}/$rPrAuth->{ExpDate}|;

    # Start out the display.
    my $html =
      myHTML->newHTML( $form, 'Manual Auth',
        'CheckPopupWindow noclock countdown_2' )
      . qq|
<TABLE CLASS="main" >
  <TR><TD CLASS="hdrcol banner" >${MAINHDR}</TD></TR>
  <TR> <TD CLASS="hdrcol title" >${SUBHDR1}</TD> </TR>
  <TR> <TD CLASS="hdrcol title" >${SUBHDR2}</TD> </TR>
</TABLE>
<SCRIPT LANGUAGE="JavaScript" >
function validate(form)
{
  if( form.Reason.value == "" ) { myAlert("Reason cannot be null",'Validation Alert!'); form.Reason.focus(); return false; }
  if( form.AuthNum.value == "" ) { myAlert("Auth# cannot be null",'Validation Alert!'); form.AuthNum.focus(); return false; }
  return true;
}
</SCRIPT>
<FORM NAME="submit" ACTION="/cgi/bin/authPA.cgi" METHOD="POST">
  <TABLE CLASS="home fullsize" >
    <TR><TD CLASS="hdrtxt" COLSPAN="2" >Please enter both Reason and Auth#</TD></TR>
    <TR>
      <TD CLASS="strcol" > Reason:</TD>
      <TD CLASS="strcol" > <INPUT TYPE="text" NAME="Reason" VALUE="" ONFOCUS="select()" SIZE="30" > </TD>
    </TR>
    <TR>
      <TD CLASS="strcol" > Auth#: </TD>
      <TD CLASS="strcol" > <INPUT TYPE="text" NAME="AuthNum" VALUE="" ONFOCUS="select()" SIZE="15" > </TD>
    </TR>
    <TR>
      <TD CLASS="strcol" > CDCKey: </TD>
      <TD CLASS="strcol" > <INPUT TYPE="text" NAME="CDCKey" VALUE="" ONFOCUS="select()" SIZE="15" > </TD>
    </TR>
    <TR>
      <TD CLASS="numcol" COLSPAN="2" >
        <INPUT TYPE="submit" ONCLICK="return validate(this.form);" NAME="submit" VALUE="authorize" >
        <INPUT TYPE="button" NAME="cancel" VALUE="cancel" ONCLICK="javascript: window.close()" >
      </TD>
    </TR>
  </TABLE>
  <INPUT TYPE="hidden" NAME="PrAuthID" VALUE="$form->{PrAuthID}" >
  <INPUT TYPE="hidden" NAME="mlt" VALUE="$form->{mlt}" >
  <SCRIPT LANGUAGE="JavaScript">
    document.submit.elements[0].focus();
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
############################################################################
