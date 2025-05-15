#!/usr/bin/perl
use lib 'C:/xampp/htdocs/src/lib';
use DBI;
use DBForm;
use DBA;
use myHTML;
use gHTML;
use CGI qw(:standard escape);

############################################################################
$form = DBForm->new();
$dbh  = $form->dbconnect();

my $ForProvID = $form->{ForProvID} ? $form->{ForProvID} : $form->{LOGINPROVID};
my $BackLinks = gHTML->setLINKS( $form, 'back' );
my $hidden    = $form->TMPwrite($skip);

# set the cross references
$xref = 'ClinicList';
$s    = $dbh->prepare("select * from Provider where Type=3");
$s->execute();
while ( my $r = $s->fetchrow_hashref ) { $$xref{ $r->{ProvID} } = $r; }
$s->finish;

############################################################################
# Start out the display.
my $html = myHTML->new($form) . qq|
<SCRIPT LANGUAGE="JavaScript" SRC="/src/cgi/js/novalidate.js"> </SCRIPT>
<TABLE CLASS="main" >
  <TR ALIGN="center" >
| . myHTML->leftpane( $form, 'clock mail managertree collapseipad' ) . qq|
    <TD WIDTH="84%" ALIGN="center" >
| . myHTML->hdr($form) . myHTML->menu($form) . qq|
<FORM NAME="Surveys" ACTION="/cgi/bin/mis.cgi" METHOD="POST" >
<TABLE CLASS="main fullsize" >
  <TR ALIGN="left" >
    <TD CLASS="strcol" >
      Satisfaction Surveys
      <BR>Entered by Survey Date
    </TD>
    <TD CLASS="numcol" >${BackLinks}</TD>
  </TR>
</TABLE>
<TABLE CLASS="port fullsize" >
  <TR>
    <TD CLASS="strcol" >
      Satisfaction Surveys available to $form->{LOGINUSERNAME}.
      <BR>The following surveys are entered.
    </TD>
    <TD CLASS="numcol" >
      <INPUT TYPE="submit" ONCLICK="return validate(this.form)" NAME="view=Surveys.cgi&UpdateTables=all&fwdTABLE=Surveys&Surveys_ID=new&pushID=$form->{LINKID}" VALUE="Add New Appointment" ONMOUSEOVER="window.status='new';return true;" ONMOUSEOUT="window.status=''" >
    </TD>
  </TR>
</TABLE>
<TABLE CLASS="home fullsize" >
  <TR>
    <TD CLASS="port hdrtxt" >Survey Date</TD>
    <TD CLASS="port hdrtxt" >Entered by</TD>
    <TD CLASS="port hdrtxt" >Entered on</TD>
    <TD CLASS="port hdrtxt" >1.</TD>
    <TD CLASS="port hdrtxt" >2.</TD>
    <TD CLASS="port hdrtxt" >3.</TD>
    <TD CLASS="port hdrtxt" >4.</TD>
    <TD CLASS="port hdrtxt" >5.</TD>
    <TD CLASS="port hdrtxt" >Explained.</TD>
    <TD CLASS="port hdrtxt" >Received.</TD>
    <TD CLASS="port hdrtxt" >&nbsp</TD>
  </TR>
|;

my $cls = '';
my $qSurveys =
qq|select Surveys.*,Provider.LName,Provider.FName from Surveys left join Provider on Provider.ProvID=Surveys.CreateProvID |
  . DBA->getProviderSelection( $form, $ForProvID, 'Surveys.CreateProvID',
    'where' )
  . qq| order by Date, LName, FName|;
my $sSurveys = $dbh->prepare($qSurveys);

#warn "qSurveys=\n$qSurveys\n";
$sSurveys->execute();
while ( $rSurveys = $sSurveys->fetchrow_hashref ) {
    if   ( $cls eq 'rptodd' ) { $cls = qq|rpteven|; }
    else                      { $cls = qq|rptodd|; }

    my $ClinicID = MgrTree->getClinic( $form, $rSurveys->{ProvID} );
    my $Exp      = $rSurveys->{RightsExp} == 1 ? 'yes' : 'no';
    my $Rec      = $rSurveys->{RightsRec} == 1 ? 'yes' : 'no';
    $ClinicName = $ClinicList{$ClinicID}{Name};
    $html .= qq|
  <TR CLASS="$cls" >
    <TD ALIGN="center" >$rSurveys->{Date}</TD>
    <TD ALIGN="left" >$rSurveys->{FName} $rSurveys->{LName}</TD>
    <TD ALIGN="center" >$rSurveys->{CreateDate}</TD>
    <TD ALIGN="center" >$rSurveys->{SessionsOK}</TD>
    <TD ALIGN="center" >$rSurveys->{TrPlan}</TD>
    <TD ALIGN="center" >$rSurveys->{Respected}</TD>
    <TD ALIGN="center" >$rSurveys->{Helped}</TD>
    <TD ALIGN="center" >$rSurveys->{Recommend}</TD>
    <TD ALIGN="center" >${Exp}</TD>
    <TD ALIGN="center" >${Rec}</TD>
    <TD ALIGN="center" >
      <INPUT TYPE="submit" ONCLICK="return validate(this.form)" NAME="view=Surveys.cgi&UpdateTables=all&fwdTABLE=Surveys&Surveys_ID=$rSurveys->{ID}&pushID=$form->{LINKID}" VALUE="View/Edit" ONMOUSEOVER="window.status='$rSurveys->{ID}';return true;" ONMOUSEOUT="window.status=''" >
    </TD>
  </TR>
|;
}

$html .= qq|
</TABLE>
${hidden}
</FORM>
| . myHTML->rightpane( $form, 'search' );

$form->complete();
print $html;
exit;
############################################################################
