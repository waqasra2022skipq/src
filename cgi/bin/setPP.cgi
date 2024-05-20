#!/usr/bin/perl
use lib '/home/okmis/mis/src/lib';
use DBI;
use myForm;
use myDBI;
use DBA;
use myHTML;
use SysAccess;

############################################################################
my $form = myForm->new();
my $dbh = myDBI->dbconnect($form->{'DBNAME'});
my $cdbh = myDBI->dbconnect('okmis_config');
#foreach my $f ( sort keys %{$form} ) { warn "setPP: form-$f=$form->{$f}\n"; }
if ( ! $form->{Provider_ProvID} ) { myDBI->error("Provider Privileges Page / denied ProvID NULL"); }
if ( ! SysAccess->verify($form,'hasProviderAccess') )
{ myDBI->error("Provider Privileges Page / denied Provider Access)"); }
if ( ! SysAccess->verify($form,'Privilege=ProviderPrivs') )
{ myDBI->error("Provider Privileges Page / denied Access"); }

############################################################################
my $Agent = SysAccess->verify($form,'Privilege=Agent');
#warn qq|setPP: Agent=${Agent}\n|;

my $html = '';
my $ProvID = $form->{'Provider_ProvID'};
# get this Provider Name...
my $sProvider = $dbh->prepare("select * from Provider where ProvID=?");
$sProvider->execute($ProvID) || myDBI->dberror("setPP: select Provider ${ProvID}");
my $rProvider = $sProvider->fetchrow_hashref;

my $sProviderPrivs = $dbh->prepare("select * from ProviderPrivs where ProvID=?");
if ( $form->{submit} ) { $html = main->submit(); }
else { $html = main->html(); }
$sProvider->finish();
$sProviderPrivs->finish();
myDBI->cleanup();
print $html;
exit;

############################################################################
sub submit
{
  my $list = ();
# before we delete look for Agent...
  if ( ! $Agent )       # did not put them on the screen to select
  {                     # so keep them checked
    my $sAgent = $dbh->prepare("select ProviderPrivs.ProvID,ProviderPrivs.Type from ProviderPrivs left join okmis_config.xPrivileges on xPrivileges.ID=ProviderPrivs.Type where ProviderPrivs.ProvID=? and xPrivileges.Category='Agent'");
    $sAgent->execute($ProvID) || myDBI->dberror("setPP: select ProviderPrivs Agent ${ProvID}");
    while ( my $r = $sAgent->fetchrow_hashref )
    { my $id = $r->{'Type'}; $list->{$id} = 'CHECKED'; }
    $sAgent->finish();
  }
# first remove existing ones...
  my $sDelete = $dbh->prepare("delete from ProviderPrivs where ProvID='${ProvID}'");
  $sDelete->execute() || myDBI->dberror("delete ProviderPrivs ${ProvID}");
  $sDelete->finish();
#warn qq|update....ProvID=${ProvID}\n|;
# first remove existing ones...
  my $sxPrivileges = $cdbh->prepare("select * from xPrivileges");
  $sxPrivileges->execute() || myDBI->dberror("setPP: select xPrivileges");
  while ( my $r = $sxPrivileges->fetchrow_hashref )
  {
    my $id = $r->{'ID'};
    if ( $form->{$id} )
    {
#warn qq|reset....${id}\n|;
      my $rProviderPrivs = ();
      $rProviderPrivs->{'CreateProvID'} = $form->{'LOGINPROVID'};
      $rProviderPrivs->{'CreateDate'} = $form->{'TODAY'};
      $rProviderPrivs->{'ChangeProvID'} = $form->{'LOGINPROVID'};
      $rProviderPrivs->{'ChangeDate'} = $form->{'TODAY'};
      $rProviderPrivs->{'ProvID'} = $ProvID;
      $rProviderPrivs->{'Type'} = $id;
      $rProviderPrivs->{'Rank'} = 1;
#foreach my $f ( sort keys %{$rProviderPrivs} ) { warn "setPP: rProviderPrivs-$f=$rProviderPrivs->{$f}\n"; }
      my $Insert = DBA->genInsert($form,'ProviderPrivs',$rProviderPrivs);
      my $sql = $dbh->prepare($Insert);
      $sql->execute() || myDBI->dberror($Insert);
      my $NEWID = $sql->{'mysql_insertid'};
      $sql->finish();
    }
  }
  $sxPrivileges->finish();
  # add back in Agent if this person (LOGINPROVID) is not an Agent
  foreach my $id ( sort keys %{$list} )
  {
#warn qq|reset: Agent: ...${id}\n|;
    my $rProviderPrivs = ();
    $rProviderPrivs->{'CreateProvID'} = $form->{'LOGINPROVID'};
    $rProviderPrivs->{'CreateDate'} = $form->{'TODAY'};
    $rProviderPrivs->{'ChangeProvID'} = $form->{'LOGINPROVID'};
    $rProviderPrivs->{'ChangeDate'} = $form->{'TODAY'};
    $rProviderPrivs->{'ProvID'} = $ProvID;
    $rProviderPrivs->{'Type'} = $id;
    $rProviderPrivs->{'Rank'} = 1;
#foreach my $f ( sort keys %{$rProviderPrivs} ) { warn "setPP Agent: rProviderPrivs-$f=$rProviderPrivs->{$f}\n"; }
    my $Insert = DBA->genInsert($form,'ProviderPrivs',$rProviderPrivs);
    my $sql = $dbh->prepare($Insert);
    $sql->execute() || myDBI->dberror($Insert);
    my $NEWID = $sql->{'mysql_insertid'};
    $sql->finish();
  }
  #DBA->setAlert($form,"Privileges set for: <BR>$rProvider->{FName} $rProvider->{LName}.<BR>Window will close in 1 minute.");
  my $html = myHTML->newHTML($form,'Authorize Privileges',"checkinputwindow noclock countdown_1") . qq|
<BODY>
<FIELDSET>
  <LEGEND>
  Privileges set for: <BR>$rProvider->{FName} $rProvider->{LName}
  </LEGEND>
<INPUT TYPE="button" NAME="cancel" VALUE="close" ONCLICK="javascript: window.close()" >
</FIELDSET>
</BODY>
</HTML>
|;
  return($html);
}
sub html
{
  my ($self) = @_;
  my $list = ();
# set the 'checked' list for setCheckBoxRows...
  $sProviderPrivs->execute($ProvID) || myDBI->dberror("setPP: select ProviderPrivs ${ProvID}");
  while ( my $r = $sProviderPrivs->fetchrow_hashref )
  { my $id = $r->{'Type'}; $list->{$id} = 'CHECKED'; }

# output the Agent Access if this person (LOGINPROVID) is an Agent...
  my $AgentAssigned = $Agent ? myHTML->setCheckBoxRows($form,'xPrivileges',$list,'','Agent') : '';

# Start out the display.
  my $MAINHDR = qq|Authorize Provider Privileges and Access|;
  my $SUBHDR1 = qq|$rProvider->{FName} $rProvider->{LName}|;
  my $html = myHTML->newHTML($form,'Authorize Privileges',"checkinputwindow noclock countdown_10") . qq|
<TABLE CLASS="main" >
  <TR><TD CLASS="hdrcol banner" >${MAINHDR}</TD></TR>
  <TR> <TD CLASS="hdrcol title" >${SUBHDR1}</TD> </TR>
</TABLE>
<SCRIPT LANGUAGE="JavaScript" >
function validate(form)
{
  //if( form.Reason.value == "" ) { myAlert("Reason cannot be null",'Validation Alert!'); form.Reason.focus(); return false; }
  //if( form.AuthNum.value == "" ) { myAlert("Auth# cannot be null",'Validation Alert!'); form.AuthNum.focus(); return false; }
  return true;
}
</SCRIPT>
<FORM NAME="submit" ACTION="/cgi/bin/setPP.cgi" METHOD="POST">
|
. myHTML->setCheckBoxRows($form,'xPrivileges',$list,'','Administration')
. myHTML->setCheckBoxRows($form,'xPrivileges',$list,'','Billing')
. myHTML->setCheckBoxRows($form,'xPrivileges',$list,'','Clinical Management')
. myHTML->setCheckBoxRows($form,'xPrivileges',$list,'','Data Entry')
. myHTML->setCheckBoxRows($form,'xPrivileges',$list,'','HR')
. myHTML->setCheckBoxRows($form,'xPrivileges',$list,'','Payroll')
. myHTML->setCheckBoxRows($form,'xPrivileges',$list,'','Prior Auth')
. myHTML->setCheckBoxRows($form,'xPrivileges',$list,'','Provider')
. $AgentAssigned
. qq| 
  <TABLE CLASS="home fullsize" >
    <TR>
      <TD CLASS="numcol" COLSPAN="2" >
        <INPUT TYPE="submit" ONCLICK="return validate(this.form);" NAME="submit" VALUE="Update" >
        <INPUT TYPE="button" NAME="cancel" VALUE="cancel" ONCLICK="javascript: window.close()" >
      </TD>
    </TR>
  </TABLE>
  <INPUT TYPE="hidden" NAME="Provider_ProvID" VALUE="${ProvID}" >
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
  return($html);
}
############################################################################
