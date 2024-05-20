#!/usr/bin/perl
use lib '/home/okmis/mis/src/lib';
use DBI;
use DBForm;
use SysAccess;
use DBA;
use DBUtil;
use myHTML;
use gHTML;

############################################################################
my $form = DBForm->new();
my $dbh = $form->dbconnect();
my $cdbh = $form->connectdb('okmis_client');
my $DBNAME = $form->{'DBNAME'};
my $AlertMessage = '';

if ( !$form->{Client_ClientID} ) { $form->error("Client Page / denied ClientID NULL"); }
if ( ! SysAccess->verify($form,'hasClientAccess') )
{ $form->error("Client Access Page / Not Client\nPossible duplicate client exists\nContact Clinical Manager or the MIS Help Desk for assistance or access."); }

warn qq|newportal: DBNAME=${DBNAME}\n|;
############################################################################
$sUserLogin = $cdbh->prepare("select * from UserLogin where ID=?");
$sUserLoginloginid = $cdbh->prepare("select * from UserLogin where loginid=?");
$sClient = $dbh->prepare("select * from Client where ClientID=?");
$sClient->execute($form->{Client_ClientID});
if ( $rClient = $sClient->fetchrow_hashref )
{
  my $ClientID = $rClient->{'ClientID'};
warn qq|newportal: ClientID=${ClientID}\n|;
  my $Email = $rClient->{'Email'};
  if ( $Email eq '' )
  { $AlertMessage = qq|NO EMAIL ADDRESS!\\nAborted setting login: ${ClientID}/${Email}|; }
  else
  {
    my $ID = $DBNAME.':'.$ClientID;
warn qq|newportal: ID=${ID}\n|;
    $sUserLogin->execute($ID);
    if ( $rUserLogin = $sUserLogin->fetchrow_hashref )
    { $AlertMessage = qq|USER ALREADY HAS A LOGIN!\\nAborted setting login: ${ClientID}/${Email}|; }
    else
    {
      $sUserLoginloginid->execute($Email);
      if ( $rUserLoginloginid = $sUserLoginloginid->fetchrow_hashref )
      { $AlertMessage = qq|LOGIN EXISTS!\\nAborted setting login: ${ClientID}/${Email}|; }
      else
      { $AlertMessage = main->setLogin($form,$ID,$Email); }
    }
  }
warn qq|newportal: AlertMessage=${AlertMessage}\n|;
  DBA->setAlert($form,$AlertMessage);
}
$sClient->finish();
$sUserLoginloginid->finish();
$sUserLogin->finish();
$form->complete();
$cdbh->disconnect();
warn qq|newportal: END=${AlertMessage}\n|;
$Location = $form->popLINK();
print qq|Location: ${Location}\n\n|;
exit;
############################################################################
sub setLogin
{
  my ($self,$form,$ID,$Email) = @_;
warn qq|setLogin: ID=${ID}\n|;
  my $Password = DBA->genPassword();
  my ($DBNAME,$ClientID) = split(':',$ID);
  my $rUpdate = ();
  $rUpdate->{'ID'} = $ID;
  $rUpdate->{'loginid'} = $Email;
  $rUpdate->{'Password'} = $Password;
  $rUpdate->{'dbname'} = 'okmis_client';
  $rUpdate->{'UserID'} = $ClientID;
  $rUpdate->{'loginscreen'} = 'ClientPortal';
  $rUpdate->{'type'} = 1;
  $rUpdate->{'renew'} = 1;
foreach my $f ( sort keys %{$rUpdate} ) { warn "$f=$rUpdate->{$f}\n"; }
  my $query = DBA->genReplace($form,$cdbh,'UserLogin',$rUpdate,"ID='${ID}'",'ID');
warn qq|newportal: query=${query}\n|;
  my $sUpdate = $cdbh->prepare($query);
  $sUpdate->execute() || $form->dberror($query);

  my $rUpdate = ();
  $rUpdate->{'ClientID'} = $ClientID;
  $rUpdate->{'ProvID'} = $ClientID;
  my $query = main->genReplace($form,$cdbh,'ClientACL',$rUpdate,"ClientID='${ClientID}' and ProvID='${ClientID}'");
warn qq|newportal: query=${query}\n|;
  my $sUpdate = $cdbh->prepare($query);
  $sUpdate->execute() || $form->dberror($query);
  $rUpdate->{'ProvID'} = 91;
  my $query = main->genReplace($form,$cdbh,'ClientACL',$rUpdate,"ClientID='${ClientID}' and ProvID='91'");
warn qq|newportal: query=${query}\n|;
  my $sUpdate = $cdbh->prepare($query);
  $sUpdate->execute() || $form->dberror($query);
  $sUpdate->finish();

  my $Subject = qq|Temporary Login|;
  my $Text = qq|Use '${Password}' to login and reset your password.\nPassword reset requested from IP: $ENV{REMOTE_ADDR}.\nIf you did not request this password reset for the Client Portal, please forward this email to: support\@okmis.com for review.|;
  DBUtil->email($form,'support@okmis.com',$Subject,$Text);
  #DBUtil->email($form,$Email,$Subject,$Text);

  my $msg = qq|Login set for: ${ClientID}/${Email}|;
  return($msg);
}
sub genReplace
{
  my ($self,$form,$dbh,$table,$record,$where,$recid) = @_;
  my $str = '';
  my $updwhere = $recid eq '' ? qq|where ${where}| : qq| where `${recid}`='$record->{$recid}'|;
  if ( $where eq '' ) { $str = DBA->genInsert($form,$table,$record); }
  else
  {
    my $s = $dbh->prepare("select * from ${table} where ${where}");
warn "genReplace: select * from ${table} where ${where}\n";
    $s->execute() || $form->dberror("replace: select ${table} where ${where}");
    if ( my $tst = $s->fetchrow_hashref )
    {
      my @flds = ();
      foreach my $fld ( sort keys %{$record} )
      {
        if ( $fld eq $recid ) { null; }
        elsif ( $record->{$fld} eq '' ) { push( @flds, "`${fld}`=NULL" ); }
        else { push( @flds, "`${fld}`=" . $dbh->quote($record->{$fld}) ); }
      }
      $str = qq|update $table set | . join(',', @flds) . $updwhere;
    }
    else { $str = DBA->genInsert($form,$table,$record); }
    $s->finish();
  }
  return($str);
}
############################################################################
