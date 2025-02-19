#!/usr/bin/perl
use lib '/var/www/okmis/src/lib';
use DBI;
use DBForm;
use DBA;
use myHTML;
use gHTML;
use uHTML;
use SysAccess;

############################################################################
my $form = DBForm->new();
my $dbh  = $form->dbconnect();
foreach my $f ( sort keys %{$form} ) { warn "setPT: form-$f=$form->{$f}\n"; }
unless ( $form->{LOGINPROVID} == 91 ) { $form->error("Alert Page / DENIED"); }
if     ( !$form->{Client_ClientID} ) {
    $form->error("Alert Page / denied ClientID NULL");
}
if ( !SysAccess->verify( $form, 'hasClientAccess' ) ) {
    $form->error("Alert Page / Not Client.");
}

############################################################################
warn qq|setPT: submit=$form->{submit}\n|;
my $ClientID = $form->{'Client_ClientID'};

my ( $title, $msg ) = main->CDSrules( $form, $ClientID );
my $html = main->pophtml( $form, $title, $msg );
$form->complete();
print $html;
exit;
############################################################################
sub CDSrules {
    my ( $self, $form, $ClientID ) = @_;
    my ( $title, $msg ) = ( '', '' );
    $title = qq|Clinical Descsion Alert|;
    my $sClientRuleAlerts = $dbh->prepare(
"select * from ClientRuleAlerts left join CDSrules on CDSrules.RuleID=ClientRuleAlerts.RuleID where ClientRuleAlerts.ClientID=?"
    );
    $sClientRuleAlerts->execute($ClientID)
      || $form->dberror("pop: CDArules: select: ClientRuleAlerts ${ClientID}");
    while ( my $rClientRuleAlerts = $sClientRuleAlerts->fetchrow_hashref ) {
        $msg .= qq|
<DIV CLASS="blackonwhite" >
  <H1 CLASS="txtheader" >Alert Response Required</H1>
  <H2 CLASS="txtleft" >
    Name: $rClientRuleAlerts->{'Name'}
  </H2>
  <DIV CLASS="blackonwhite txtleft" STYLE="overflow-y:scroll; overflow-x:hidden; height:100px;" >
    AlertMessage:<BR>$rClientRuleAlerts->{'AlertMessage'}
  </DIV>
  <DIV CLASS="txtleft" >
    RowVersion: $rClientRuleAlerts->{'RowVersion'}
  </DIV>
  <DIV CLASS="txtleft" >
    <A HREF="$rClientRuleAlerts->{'Referencelink'}" >
      $rClientRuleAlerts->{'Referencelink'}
    </A>
  </DIV>
  <DIV CLASS="blackonwhite txtleft" STYLE="overflow-y:scroll; overflow-x:hidden; height:100px;" >
    Biblio: $rClientRuleAlerts->{'Biblio'}
  </DIV>
</DIV>
|;
    }
    $sClientRuleAlerts->finish();
    return ( $title, $msg );
}

sub pophtml {
    my ( $self, $form, $title, $msg ) = @_;
    my $html =
      myHTML->newHTML( $form, $title, "CheckPopupWindow noclock countdown_10" )
      . qq|
<LINK REL="STYLESHEET" TYPE="text/css" HREF="/cfg/mis.css" />
<BODY>
<FIELDSET>
  <LEGEND>
  ${title}
  </LEGEND>
  ${msg}
  <INPUT TYPE="button" NAME="cancel" VALUE="close" ONCLICK="javascript: window.close()" >
</FIELDSET>
</BODY>
</HTML>
|;
    return ($html);
}
############################################################################
