package uHTML;
use myDBI;

############################################################################
sub hClientRuleAlerts
{
  my ($self,$form,$ClientID) = @_;
  return() unless ( SysAccess->chkPriv($form,'CDSAlerts') );
  my ($html,$cnt) = ('',0);
  my $dbh = myDBI->dbconnect($form->{'DBNAME'});
  my $sClientRuleAlerts = $dbh->prepare("select * from ClientRuleAlerts left join CDSrules on CDSrules.RuleID=ClientRuleAlerts.RuleID where ClientRuleAlerts.ClientID=?");
  $sClientRuleAlerts->execute($ClientID) || $form->dberror("pop: CDArules: select: ClientRuleAlerts ${ClientID}");
  my $total = $sClientRuleAlerts->rows;
  while ( my $rClientRuleAlerts = $sClientRuleAlerts->fetchrow_hashref )
  {
    $cnt++;
    $html .= qq|
<DIV CLASS="dialog-onload" ALERTTITLE="Alert Notification ${cnt} of ${total}" >
  <DIV CLASS="blackonwhite" >
    <DIV CLASS="txtcenter txtlarge hotmsg" >
      Alert: $rClientRuleAlerts->{'Name'}
    </DIV>
    <DIV CLASS="txtleft" >
      Condition:
    </DIV>
    <DIV CLASS="blackonwhite txtleft" STYLE="overflow-y:scroll; overflow-x:hidden; height:100px;" >
      $rClientRuleAlerts->{'AlertMessage'}
    </DIV>
    <DIV CLASS="txtleft" >
      Funding By: $rClientRuleAlerts->{'Funding'}
    </DIV>
    <DIV CLASS="txtleft" >
      Developer: Millennium Information Services
    </DIV>
    <DIV CLASS="txtleft" >
      Release: $rClientRuleAlerts->{'ReleaseDate'}
    </DIV>
    <DIV CLASS="txtleft" >
      Bibilo: $rClientRuleAlerts->{'Biblio'}
    </DIV>
    <DIV CLASS="txtleft" >
      Reference Link:
      <A HREF="javascript:ReportWindow('$rClientRuleAlerts->{'ReferenceLink'}','ReferenceLink');" TITLE="Click here for Reference." ><IMG SRC="|.myConfig->cfgfile('window-info.png',1).qq|" HEIGHT="30" WIDTH="30" BORDER="0" ></A>
    </DIV>
    <DIV CLASS="txtleft" >
      Information Link:
      <A HREF="javascript:ReportWindow('$rClientRuleAlerts->{'InfoLink'}','InfoLink');" TITLE="Click here for Information reguarding this client." ><IMG SRC="|.myConfig->cfgfile('user-info.png',1).qq|" HEIGHT="30" WIDTH="30" BORDER="0" ></A>
    </DIV>
  </DIV>
</DIV>
|;
  }
#warn qq|hClientRuleAlerts: ClientID=${ClientID}=${cnt}\n|;
  $sClientRuleAlerts->finish();
  return($html);
}
#############################################################################
1;
