#!/usr/bin/perl
use lib '/home/okmis/mis/src/lib';
use DBI;
use DBForm;
use DBA;
use myHTML;
use gHTML;
use SysAccess;

############################################################################
my $form = DBForm->new();
my $dbh = $form->dbconnect();
#foreach my $f ( sort keys %{$form} ) { warn "setPT: form-$f=$form->{$f}\n"; }
if ( ! $form->{Provider_ProvID} ) { $form->error("Provider Triggers Page / denied ProvID NULL"); }
if ( ! SysAccess->verify($form,'hasProviderAccess') )
{ $form->error("Provider Triggers Page / denied Provider Access)"); }
if ( ! SysAccess->verify($form,'Privilege=ProviderPrivs') )
{ $form->error("Provider Triggers Page / denied Access"); }

############################################################################
warn qq|setPT: submit=$form->{submit}\n|;
my $ProvID = $form->{'Provider_ProvID'};
my $html = '';
if ( $form->{submit} ) { $html = main->uPT($form,$ProvID); }
else { $html = main->hPT($form,$ProvID); }
$form->complete();
print $html;
exit;
############################################################################
# html: Provider Triggers: Decision Support Rules
sub hPT
{
  my ($self,$form,$ProvID) = @_;
  my $dbh = $form->dbconnect();
# select for the 'checked' list for setCheckBoxColumns...
  my $sProviderTriggers = qq|select * from ProviderTriggers where ProvID='${ProvID}'|;

# Start out the display.
  my $html = myHTML->newHTML($form,'Set Triggers',"checkinputwindow noclock countdown_1") . qq|
<FORM NAME="submit" ACTION="/cgi/bin/setPT.cgi" METHOD="POST">
<DIV CLASS="blackonwhite" >
  <DIV CLASS="blackonwhite txtleft" >
    <div data-role="header" >
      <DIV CLASS="txtheader" >Decision Support Rules</DIV>
    </div>
    <div data-role="main" class="ui-content"> |
. myHTML->setCheckBoxColumns($form,'zTriggers',$sProviderTriggers,'Available Triggers') . qq|
    </div>
  </DIV>
  <DIV CLASS="blackonwhite txtright" >
    <INPUT TYPE="submit" ONCLICK="return validate(this.form);" NAME="submit" VALUE="Update" >
    <INPUT TYPE="button" NAME="cancel" VALUE="cancel" ONCLICK="javascript: window.close()" >
  </DIV>
</DIV>
  <INPUT TYPE="hidden" NAME="Provider_ProvID" VALUE="${ProvID}" >
  <INPUT TYPE="hidden" NAME="mlt" VALUE="$form->{mlt}" >
</FORM>
    </TD>
  </TR>
</TABLE>
  <SCRIPT LANGUAGE="JavaScript">
    document.submit.elements[0].focus();
  </SCRIPT>
</BODY>
</HTML>
|;
  return($html);
}
# update: Provider Triggers: Decision Support Rules
sub uPT
{
  my ($self,$form,$ProvID) = @_;
  my $dbh = $form->dbconnect();
#warn qq|update....ProvID=${ProvID}\n|;
# first remove existing ones...
  my $sDelete = $dbh->prepare("delete from ProviderTriggers where ProvID='${ProvID}'");
  $sDelete->execute() || $form->dberror("delete ProviderTriggers ${ProvID}");
  my $cdbh = $form->connectdb('okmis_config');
  my $szTriggers = $cdbh->prepare("select * from zTriggers");
  $szTriggers->execute() || $form->dberror("uPT: select zTriggers");
  while ( my $r = $szTriggers->fetchrow_hashref )
  {
    my $ID = $r->{'ID'};
    if ( $form->{$ID} )
    {
      my $rProviderTriggers = ();
#warn qq|reset....${ID}\n|;
      $rProviderTriggers->{'CreateProvID'} = $form->{'LOGINPROVID'};
      $rProviderTriggers->{'CreateDate'} = $form->{'TODAY'};
      $rProviderTriggers->{'ChangeProvID'} = $form->{'LOGINPROVID'};
      $rProviderTriggers->{'ChangeDate'} = $form->{'TODAY'};
      $rProviderTriggers->{'ProvID'} = $ProvID;
      $rProviderTriggers->{'ID'} = $ID;
foreach my $f ( sort keys %{$rProviderTriggers} ) { warn "uPT: rProviderTriggers-$f=$rProviderTriggers->{$f}\n"; }
      my $Insert = DBA->genInsert($form,'ProviderTriggers',$rProviderTriggers);
      my $sql = $dbh->prepare($Insert);
      $sql->execute() || $form->dberror($Insert);
      my $NEWID = $sql->{'mysql_insertid'};
      $sql->finish();
    }
  }
  $szTriggers->finish();
  $cdbh->disconnect();
  my $html = myHTML->newHTML($form,'Set Triggers',"checkinputwindow noclock countdown_1") . qq|
<BODY>
<FIELDSET>
  <LEGEND>
  Triggers set for: <BR>$rProvider->{FName} $rProvider->{LName}
  </LEGEND>
<INPUT TYPE="button" NAME="cancel" VALUE="close" ONCLICK="javascript: window.close()" >
</FIELDSET>
</BODY>
</HTML>
|;
  return($html);
}
############################################################################
