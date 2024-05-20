package SysAccess;
use DBI;
use DBForm;
use DBA;
use myDBI;
use MgrTree;

my $debug = 0;
############################################################################
sub verify
{ 
  my ($self, $form, $Function, @Args) = @_;
#warn "ENTER->SysAccess: verify: Function=$Function, Args=@Args\n";
  if ( $Function =~ /^privilege=/i )
  {
    my ($Type,$Privilege) = split('=',$Function);
    return(1) if ( ! ${Privilege} );
    return(0) if ( ${Privilege} eq 'SKIP' );
    return(1) if ( $self->chkPriv($form,$Privilege) ); 
    return(0);
  }

#warn "SysAccess: verify: Function=$Function, Args=@Args\n";
  my $code = $self->$Function($form,@Args);
  return($code);
}
############################################################################
# Check out the Provider access to Client.
##
sub hasClientAccess
{
  my ($self,$form,$CID) = @_;
  my $ClientID = $CID ? $CID : $form->{Client_ClientID};
#warn "ENTER->SysAccess: hasClientAccess: ClientID=$ClientID, LOGINPROVID=$form->{LOGINPROVID}, LOGINUSERDB=$form->{LOGINUSERDB}\n";
  return(1) if ( $ClientID =~ /new/i );
  return(0) if ( !$ClientID );
#foreach my $f ( sort keys %{$form} ) { warn "hasClientAccess: form-$f=$form->{$f}\n"; }
#warn qq|SysAccess: hasClientAccess: call myDBI->dbconnect($form->{'LOGINUSERDB'})\n|;
  my $dbh = myDBI->dbconnect($form->{'LOGINUSERDB'});
  my $sClientACL = $dbh->prepare("select * from ClientACL where ClientID=? and ProvID=?");
  $sClientACL->execute($ClientID,$form->{LOGINPROVID}) || myDBI->dberror("hasClientAccess: select $ClientID,$form->{LOGINPROVID}");
  $rClientACL = $sClientACL->fetchrow_hashref;
  $sClientACL->finish();
  my $cnt = $sClientACL->rows();
#warn "ENTER->SysAccess: hasClientAccess: ClientID=$ClientID, cnt=$cnt\n";
  return($cnt);
}
############################################################################
# Check out the Provider access to Provider.
##
sub hasProviderAccess
{
  my ($self, $form, $inProvID) = @_;
  my $ProvID = $inProvID ? $inProvID : $form->{Provider_ProvID};
  return(1) if ( ${ProvID} =~ /new/i );
  ##
  # check if access was setup for this Provider to this Provider/Clinic/Agency.
  ##
  return($self->hasACL($form,$ProvID));
}
sub chkProvACL
{
  my ($self, $form, $Type) = @_;
  my $code = 0;
  if ( $Type > 2 && $self->verify($form,'Privilege=Agent') ) { $code = 1; }
  elsif ( $Type > 3 && $self->verify($form,'Privilege=ProviderACL') ) { $code = 1; }
  return($code);
}
############################################################################
sub isAdmin
{ 
  my ($self,$form) = @_;
  #return(1) if ( $form->{LOGINPROVID} == 89 && $form->{'DBNAME'} eq 'okmis_mms' );
  return(1) if ( $form->{LOGINPROVID} =~ /89|90/ && $form->{'DBNAME'} eq 'okmis_mms' );
  return(0);
}
sub isHelpDesk
{ 
  my ($self,$form) = @_;
  #Is Help Desk
  return(1) if ( $form->{LOGINPROVID} =~ /89|90|91/);
  return(0);
}
sub ChkPriv
{ 
  my ($self,$form,$Type,$ProvIDs) = @_;
  return(0) if ( $Type eq 'SKIP' );
  return(1) if ( $Type eq '' );
  return(1) if ( $form->{'LOGINPROVID'} =~ /:${ProvIDs}:/ );     # for Type OR LOGINPROVID (HelpDesk?)
  return($self->chkPriv($form,$Type)); 
}
# select ProviderPriv for Provider, returns yes or no
##
sub chkPriv
{
  my ($self, $form, $Type, $inProvID) = @_;
  my $ProvID = $inProvID ? $inProvID : $form->{LOGINPROVID};
#warn "chkPriv: Type=$Type, ProvID=$ProvID, code=$code\n"; 
  return(1) if ( $Type eq 'root' && $form->{LOGINPROVID} == 91 );
  my $code = 0;
  my $dbh = myDBI->dbconnect($form->{'DBNAME'});
  my $q = qq|select * from ProviderPrivs where Type=? and ProvID=?|;
  my $s = $dbh->prepare($q);
  $s->execute($Type,$ProvID) || myDBI->dberror($q);
  if ( my $r = $s->fetchrow_hashref ) { $code = 1; } else { $code = 0; }
  $s->finish;
#warn "chkPriv: Type=$Type, ProvID=$ProvID, code=$code\n"; 
  return($code);
}
##
# select Emails for all Providers with Priv=Type, returns all the Emails
##
sub getPrivEmail
{
  my ($self, $form, $Type) = @_;
  my $Emails='';
  my $dbh = myDBI->dbconnect($form->{'DBNAME'});
  my $q = qq|select Provider.Email from ProviderPrivs left join Provider on Provider.ProvID=ProviderPrivs.ProvID where Provider.Active=1 and Provider.NoMail=0 and ProviderPrivs.Type=?|;
  my $s = $dbh->prepare($q);
  $s->execute($Type) || myDBI->dberror($q);
  while ( my ($Email) = $s->fetchrow_array ) { $Emails .= $Email . ' '; }
  $s->finish;
  $Emails = $form->{LOGINEMAIL} unless ( $Emails );
  return($Emails);
}
############################################################################
# only for LOGINPROVID
# test for existance of ACL
sub tstACL
{ 
  my ($self,$form,$id) = @_;
  my $list = SysAccess->selACL($form);
#my $e = exists($list->{$id});
#warn qq|tstACL: return 1? exists=${e}, id=${id}=$list->{$id}\n|;
  return(1) if ( exists($list->{$id}) );
#warn qq|tstACL: return 0! $id\n|;
  return(0);
}
# only for LOGINPROVID 
# test for positive access to ACL
sub hasACL
{ 
  my ($self,$form,$id) = @_;
  my $list = SysAccess->selACL($form);
#warn qq|hasACL: return 1? id=${id}=$list->{$id}\n|;
# stores the AccessOK 1|0 in $id.
  return(1) if ( $list->{$id} );
#warn qq|hasACL: return 0! $id\n|;
  return(0);
}
sub selACL
{ 
  my ($self,$form) = @_;                  # only for LOGINPROVID
  my $ACCESSLIST = ();
  my $dbh = myDBI->dbconnect($form->{'DBNAME'});
  my $sSiteACL=$dbh->prepare("select * from SiteACL where ProvID=?");
  $sSiteACL->execute($form->{'LOGINPROVID'}) || myDBI->dberror("selACL: select $form->{'LOGINPROVID'}");
  while ( my $rSiteACL = $sSiteACL->fetchrow_hashref )
  { $ACCESSLIST->{$rSiteACL->{'AccessID'}} = $rSiteACL->{'AccessOK'}; }
#foreach my $f ( sort keys %{$ACCESSLIST} ) { warn "selACL: ACCESSLIST-$f=$ACCESSLIST->{$f}\n"; }
  $sSiteACL->finish();
  return($ACCESSLIST);
}
# for any Provider ID, with or without AccessOK
sub getACL
{ 
  my ($self, $form, $ProvID, $Types) = @_;
#warn "ENTER->SysAccess-getACL: ProvID=${ProvID}, Types=$Types\n";
#foreach my $f ( sort keys %{$form} ) { warn "getACL: form-$f=$form->{$f}\n"; }
  my @List = ();
  my $dbh = myDBI->dbconnect($form->{'DBNAME'});
  my $qSiteACL=qq|select * from SiteACL where ProvID=? and Type=?|;
  my $sSiteACL=$dbh->prepare($qSiteACL);
  foreach my $Type ( split(':',$Types) )
  {
    $sSiteACL->execute($ProvID,$Type) || myDBI->dberror($qSiteACL);
    while ( my $rSiteACL = $sSiteACL->fetchrow_hashref )
#HUH??? need way to limit, see EmailList though
#       { push(@List,$rSiteACL->{AccessID}) if ( $rSiteACL->{AccessOK} ); }
    { push(@List,$rSiteACL->{AccessID}); }
  }
  $sSiteACL->finish();
#warn "getACL: return=@List\n";
  return(@List);
}
############################################################################
sub getRule
{ 
  my ($self, $form, $Type, $inProvID) = @_;
  my $ProvID = $inProvID ? $inProvID : $form->{LOGINPROVID};
  my $AgencyID = $self->getAgency($form,$ProvID);
#warn qq|getRule: Type=$Type, inProvID=$inProvID, ProvID=$ProvID\n|;
#warn qq|getRule: AgencyID=$AgencyID\n|;
  my $dbh = myDBI->dbconnect($form->{'DBNAME'});
  my $q = qq|select * from ProviderControl where ProvID=?|;
  my $s = $dbh->prepare($q);
  $s->execute($AgencyID) || myDBI->dberror($q);
  my $r = $s->fetchrow_hashref();
  my $code = $r->{$Type};
#warn qq|getRule: Type=$Type, code=$code\n|;
  $s->finish();
  return($code);
}
sub getAgency
{
  my ($self, $form, $ProvID) = @_;
  my $ForProvID = $ProvID ? $ProvID : $form->{LOGINPROVID};
  my @Agencys = SysAccess->getACL($form,$ForProvID,'Agency');
  my $AgencyID=$Agencys[0];
#warn qq|AID=$AgencyID, @Agencys\n|;
  return($AgencyID);
}
sub getAgencys
{
  my ($self, $form, $ProvID) = @_;
  my $ForProvID = $ProvID ? $ProvID : $form->{LOGINPROVID};
  my @Agencys = SysAccess->getACL($form,$ForProvID,'Agency');
  return(@Agencys);
}
############################################################################
############################################################################
sub getClinics
{
  my ($self,$form,$ReqProvID) = @_;
  my $ForProvID = $ReqProvID ? $ReqProvID : $form->{LOGINPROVID};
  my @List = ();
  my $dbh = myDBI->dbconnect($form->{'DBNAME'});
  my $q = qq|select SiteACL.*,Provider.ProvID,Provider.Name from SiteACL left join Provider on Provider.ProvID=SiteACL.AccessID where SiteACL.ProvID=? and SiteACL.AccessOK=1 and SiteACL.Type='Clinic' order by Provider.ProvID|;
  my $s = $dbh->prepare($q);
  $s->execute($ForProvID) || myDBI->dberror($q);
  while ( my $r = $s->fetchrow_hashref )
  { push(@List,$r->{AccessID}); }
  $s->finish();
  return(@List);
}
sub getProviders
{
  my ($self,$form,$ReqProvID) = @_;
  my $ForProvID = $ReqProvID ? $ReqProvID : $form->{LOGINPROVID};
  my @List = ();
  my $dbh = myDBI->dbconnect($form->{'DBNAME'});
  my $q = qq|select SiteACL.*,Provider.ProvID,Provider.Name from SiteACL left join Provider on Provider.ProvID=SiteACL.AccessID where SiteACL.ProvID=? and SiteACL.AccessOK=1 and SiteACL.Type='Provider' order by Provider.ProvID|;
  my $s = $dbh->prepare($q);
  $s->execute($ForProvID) || myDBI->dberror($q);
  while ( my $r = $s->fetchrow_hashref )
  { push(@List,$r->{AccessID}); }
  $s->finish();
  return(@List);
}
############################################################################
# Provider Access List routines
sub setSiteACL
{
  my ($self,$form,$ProvID) = @_;
warn "ENTER->SysAccess: setSiteACL: ProvID=${ProvID}\n" if ( $debug );
  my $dbh = myDBI->dbconnect($form->{'DBNAME'});
  my $cnt=0;
  my $with = $ProvID ? qq|where ProvID='${ProvID}'| : '';
  my $sProvider=$dbh->prepare("select * from Provider ${with} order by LName, FName");
  $sProvider->execute();
  while (my $rProvider = $sProvider->fetchrow_hashref)
  {
warn qq|setSiteACL: $rProvider->{ProvID}, $rProvider->{LName}, $rProvider->{FName}\n| if ( $debug );
    $cnt++;
    $self->rebldSiteACL($form,$rProvider->{'ProvID'});
  }
  $sProvider->finish();
  return($cnt);
}
######################################################
# SiteACL is table of provider access to manager tree.
# based on Provider->ACLID
# Saves access UP/DOWN Tree for quick retrieval without walking the Tree.
##
sub rebldSiteACL
{
  my ($self,$form,$ProvID) = @_;
warn "ENTER->SysAccess: rebldSiteACL: ProvID=${ProvID}\n" if ( $debug );
  my $dbh = myDBI->dbconnect($form->{'DBNAME'});

  my $sDelete = $dbh->prepare("delete from SiteACL where ProvID=?");
  $sDelete->execute($ProvID) || myDBI->dberror("rebldSiteACL: delete SiteACL");
  $sDelete->finish();

  my $sProvider = $dbh->prepare("select * from Provider where ProvID=?");
  $sProvider->execute($ProvID) || myDBI->dberror("rebldSiteACL: select Provider ProvID=${ProvID}");
  my $rProvider = $sProvider->fetchrow_hashref;

  my  @AIDS = ( $ProvID,split(chr(253),$rProvider->{ACLID}) );

  if ($rProvider->{ACLID} =~ /\?/i) {
    # Code to execute if the string contains a question mark
    @AIDS = split(/\?/, $rProvider->{ACLID});
  }
  


  warn qq|SysAccess-rebldSiteACL: ($ProvID + $rProvider->{ACLID}), @AIDS\n| if ( $debug );
  foreach my $AID ( @AIDS )
  {
    next unless ( $AID );
    $sProvider->execute($AID) || myDBI->dberror("rebldSiteACL: select Provider AID=${AID}");
    my $rAccess = $sProvider->fetchrow_hashref;
warn qq|  SysAccess-rebldSiteACL: BEGIN: $ProvID: for $AID,$rAccess->{FName},$rAccess->{LName},t=$rAccess->{Type}\n| if ( $debug );
#                                                                           set this to AccessOK if Active.
    $self->rebldSiteACLType($form,$ProvID,$rAccess->{ProvID},$rAccess->{Type},$rProvider->{Active});

warn qq|  SysAccess-rebldSiteACL: UP: $AID\n| if ( $debug );
    # go up the tree.
    for my $branch ( MgrTree->getManagers($form,$AID,0) ) 
    { $self->rebldSiteACLType($form,$ProvID,$branch->{ProvID},$branch->{Type},0); }

#   stop after setting Clinic/Agency for Inactive Providers.
    last unless ( $rProvider->{Active} );

    # go down the tree.
warn qq|  SysAccess-rebldSiteACL: DOWN: $AID\n| if ( $debug );
    for my $branch ( MgrTree->getProviders($form,$AID,0) ) 
    { $self->rebldSiteACLType($form,$ProvID,$branch->{ProvID},$branch->{Type},1); }
warn qq|  SysAccess-rebldSiteACL: END: $ProvID: for $AID,$rAccess->{FName},$rAccess->{LName},t=$rAccess->{Type}\n| if ( $debug );
  }
warn qq|SysAccess-rebldSiteACL: DONE: ProvID=$ProvID\n| if ( $debug );
  $sProvider->finish();
  return(1);
}
sub rebldSiteACLType
{
  my ($self,$form,$ProvID,$AccessID,$Type,$AccessOK) = @_;
#warn "ENTER->SysAccess: rebldSiteACLType: ProvID=${ProvID}, AccessID=${AccessID}, Type=${Type}, AccessOK=${AccessOK}\n";
  my $Descr = '';
  if ( $Type == 1 && $AccessOK ) { $Descr='Group'; }
  elsif ( $Type == 1 ) { return(0); }
  elsif ( $Type == 2 ) { $Descr='Agency'; }
  elsif ( $Type == 3 ) { $Descr='Clinic'; }
  elsif ( $Type == 4 ) { $Descr='Provider'; }
  else { $Descr='unknown'; }
#warn qq|    SysAccess-rebldSiteACLType: p=$ProvID, i=$AccessID, t=$Type, d=$Descr\n|;

  my $dbh = myDBI->dbconnect($form->{'DBNAME'});
  my $sExist = $dbh->prepare("select * from SiteACL where ProvID=? and AccessID=? and Type=?");
  $sExist->execute($ProvID,$AccessID,$Descr) || myDBI->dberror("rebldSiteACL: exist SiteACL");
  if ( $rExist = $sExist->fetchrow_hashref )
  { 
    # only change the record if changing to 1=AccessOK, was either 1 or 0 already.
    # if record is there, since we delete all, some access was given previously
    # we don't want to undo that access (might have been given access by ACLID.
    if ( $AccessOK )
    {
#warn qq|    SysAccess-rebldSiteACLType: update: ID=$rExist->{ID}: $AccessOK,$ProvID,$AccessID,$Descr\n|;
      my $s=$dbh->prepare("update SiteACL set AccessOK=? where ProvID=? and AccessID=? and Type=?");
      $s->execute($AccessOK,$ProvID,$AccessID,$Descr) || myDBI->dberror("rebldSiteACLType: update SiteACL");
      $s->finish();
    }
  }
  else
  {
#warn qq|    SysAccess-rebldSiteACLType: insert: $ProvID,$AccessID,$Descr,$AccessOK\n|;
    my $sInsert = $dbh->prepare("insert into SiteACL (ProvID,AccessID,Type,AccessOK,CreateProvID)
                                              values ('$ProvID','$AccessID','$Descr','$AccessOK','$form->{LOGINPROVID}')");
    $sInsert->execute() || myDBI->dberror("rebldSiteACLType: insert SiteACL");
    $sInsert->finish();
  }
  $sExist->finish();
  return(1);
}
############################################################################
# set/recreate ClientACL records for all Clients
sub setClientACL
{
  my ($self,$form,$Active,$ProvID) = @_;
#warn "ENTER->SysAccess: setClientACL: Active=${Active}, ProvID=${ProvID}\n";
  my $dbh = myDBI->dbconnect($form->{'DBNAME'});
  my $cnt = 0;
  $sClient=$dbh->prepare("select * from Client order by LName, FName");
  $sClient->execute();
  while (my $rClient = $sClient->fetchrow_hashref)
  {
#warn qq|$rClient->{ClientID}, ${ProvID}\n|;
    $cnt++;
    $self->rebldClientACL($form,$rClient->{ClientID},$rClient->{ProvID},$Active,$ProvID);
  }
  $sClient->finish();
  return($cnt);
}
##
# recreate ClientACL records for ClientID
#  if given a ProvID, only select and delete with that ProvID
##
sub rebldClientACL
{
  my ($self,$form,$ClientID,$PrimaryProvID,$Active,$ProvID) = @_;
#warn "ENTER->SysAccess: rebldClientACL: ClientID=${ClientID}, PrimaryProvID=${PrimaryProvID}, Active=${Active}, ProvID=${ProvID}\n";
  my $dbh = myDBI->dbconnect($form->{'DBNAME'});
  my $ClientACL_ProvIDs = ();    # hash so as not to duplicate ProvID.

# ProvID of Provider, AccessID to PrimaryProvider.
# because if ProvID has access to PrimaryProvider they get ClientACL.
  my $q = qq|select SiteACL.ProvID from SiteACL left join Provider on Provider.ProvID=SiteACL.ProvID where SiteACL.AccessOK=1|;
  $q .= $Active ? qq| and Provider.Active=1| : '';
  $q .= $ProvID && $PrimaryProvID
        ? qq| and SiteACL.ProvID='${ProvID}' and SiteACL.AccessID='${PrimaryProvID}'|
        : $PrimaryProvID
          ? qq| and SiteACL.AccessID='${PrimaryProvID}'|
          : return(0);
#warn "rebldClientACL: select SiteACL:\nq=${q}\n";
  my $sSiteACL = $dbh->prepare($q);
  $sSiteACL->execute() || myDBI->dberror("rebldClientACL: ${q}");
  while ( my ($pid) = $sSiteACL->fetchrow_array )
  { $ClientACL_ProvIDs->{$pid} = $pid; }
  $sSiteACL->finish();

# select from ClientAccess list maintained to give away access to Providers.
  my $q = qq|select * from ClientAccess where ClientID=?|;
  $q .= $ProvID ? qq| and ProvID='${ProvID}'| : '';
#warn "rebldClientACL: select ClientAccess: ClientID=${ClientID}\nq=${q}\n";
  my $sClientAccess = $dbh->prepare($q);
  $sClientAccess->execute($ClientID) || myDBI->dberror("rebldClientACL: ${q}");
  while ( my $rClientAccess = $sClientAccess->fetchrow_hashref )
  { $ClientACL_ProvIDs->{$rClientAccess->{'ProvID'}} = $rClientAccess->{'ProvID'}; }
  $sClientAccess->finish();
#foreach my $f ( sort keys %{$ClientACL_ProvIDs} ) { warn "ClientACL_ProvIDs-$f=$ClientACL_ProvIDs->{$f}\n"; }

# update the ClientACL table...
  my $qDelete = qq|delete from ClientACL where ClientID=?|;
  $qDelete .= $ProvID ? qq| and ProvID='${ProvID}'| : '';
#warn "rebldClientACL: Delete ClientACL...\n$qDelete\n";
  my $sDelete = $dbh->prepare($qDelete);
  $sDelete->execute($ClientID) || myDBI->dberror("rebldClientACL: ${qDelete}");
  $sDelete->finish();

  my $cnt = 0;
  my $sInsert = $dbh->prepare("insert into ClientACL (ClientID,ProvID) values (?,?)");
  foreach my $ListProvID ( sort keys %{ $ClientACL_ProvIDs } )
  { $cnt++; $sInsert->execute($ClientID,$ListProvID) || myDBI->dberror("rebldClientACL: insert (${ClientID},${ListProvID})"); }
  $sInsert->finish();
  return($cnt);
}
############################################################################
# Manager Tree routines...
sub setManagerTree
{
  my ($self,$form,$ProvID) = @_;
#warn "ENTER->SysAccess: setManagerTree: ProvID=${ProvID}\n";
  my $dbh = myDBI->dbconnect($form->{'DBNAME'});
  my $cnt=0;
  my $with = $ProvID ? qq|and ProvID='${ProvID}'| : '';
  my $sProvider=$dbh->prepare("select * from Provider where Active=1 ${with} order by LName, FName");
  $sProvider->execute();
  while (my $rProvider = $sProvider->fetchrow_hashref)
  {
#warn qq|$rProvider->{ProvID}, $rProvider->{LName}, $rProvider->{FName}\n|;
    $cnt++;
    $self->rebldManagerTree($form,$rProvider->{'ProvID'});
  }
  $sProvider->finish();
  return($cnt);
}
sub rebldManagerTree
{
  my ($self,$form,$ProvID) = @_;

#warn "ENTER->SysAccess: rebldManagerTree: ProvID=${ProvID}\n";
  my $dbh = myDBI->dbconnect($form->{'DBNAME'});
  my $table = 'ManagerTree';
  my ($Cnt,$AgencyCnt,$ClinicCnt,$GotMe) = (0,0,0,0);

  my $sDelete = $dbh->prepare("delete from ${table} where TreeProvID=?");
  $sDelete->execute($ProvID) || myDBI->dberror("rebldManagerTree: delete ${table}");
  $sDelete->finish();

  my $qTree = qq|update ${table} set AgencyCnt=?,ClinicCnt=? where TreeProvID=? and Cnt=1|;
  my $sTree = $dbh->prepare($qTree);

  my $qProvider = qq|select * from Provider where ProvID=?|;
  my $sProvider = $dbh->prepare($qProvider);
  $sProvider->execute($ProvID) || myDBI->dberror($qProvider);
  my $rProvider = $sProvider->fetchrow_hashref;
  
  my  @AIDS = ( $ProvID,split(chr(253),$rProvider->{ACLID}) );

  if ($rProvider->{ACLID} =~ /\?/i) {
    # Code to execute if the string contains a question mark
    @AIDS = split(/\?/, $rProvider->{ACLID});
  }

  foreach my $AID ( @AIDS )
  {
    next unless ( $AID );
    # write out this Provider
    $sProvider->execute($AID) || myDBI->dberror($qProvider);
    my $rProvider = $sProvider->fetchrow_hashref;
    next unless ( $rProvider->{Active} );
    $Cnt++; 
    $AgencyCnt++ if ( $rProvider->{Type} == 2 );
    $ClinicCnt++ if ( $rProvider->{Type} == 3 );
    $self->insTree($form,$table,$ProvID,$rProvider,$Cnt);
    $GotMe = 1 if ( $branch->{ProvID} == $ProvID );
    # go down the tree.
    for my $branch ( MgrTree->getProviders($form,$AID,0) ) 
    { 
      next unless ( $branch->{Active} );
      $Cnt++; 
      $AgencyCnt++ if ( $branch->{Type} == 2 );
      $ClinicCnt++ if ( $branch->{Type} == 3 );
      $self->insTree($form,$table,$ProvID,$branch,$Cnt); 
      $GotMe = 1 if ( $branch->{ProvID} == $ProvID ); 
    }
  }
  # unless ( $GotMe )
  # { 
  #   # put me out there.
  #   $sProvider->execute($ProvID) || myDBI->dberror($qProvider);
  #   my $rProvider = $sProvider->fetchrow_hashref;
  #   $Cnt++; 
  #   $AgencyCnt++ if ( $rProvider->{Type} == 2 );
  #   $ClinicCnt++ if ( $rProvider->{Type} == 3 );
  #   $self->insTree($form,$table,$ProvID,$rProvider,$Cnt);
  #   # go down the tree.
  #   for my $branch ( MgrTree->getProviders($form,$ProvID,0) ) 
  #   { 
  #     next unless ( $branch->{Active} );
  #     $Cnt++; 
  #     $AgencyCnt++ if ( $branch->{Type} == 2 );
  #     $ClinicCnt++ if ( $branch->{Type} == 3 );
  #     $self->insTree($form,$table,$ProvID,$branch,$Cnt); 
  #   }
  # }
  $sProvider->finish();
  $sTree->execute($AgencyCnt,$ClinicCnt,$ProvID) || myDBI->dberror($qTree);
  $sTree->finish();
  return(1);
}
sub insTree
{
  my ($self,$form,$table,$TreeProvID,$r,$Cnt) = @_;

  my $record = ();
  my $dbh = myDBI->dbconnect($form->{'DBNAME'});
  $record->{TreeProvID} = $TreeProvID;
  $record->{Cnt} = $Cnt;
  $record->{ListProvID} = $r->{ProvID};
  $record->{Type} = $r->{Type};
  $record->{Indent} = 10 + (20 * $r->{Index});
  my $Prefix = $r->{'Prefix'} eq '' ? '' : $r->{'Prefix'}.' ';
  $record->{Name} = $r->{'Name'} ne '' ? qq|$r->{'Name'}|
                  : $r->{'ScreenName'} ne '' ? qq|$r->{'ScreenName'}*|
                  : qq|${Prefix}$r->{'LName'}, $r->{'FName'} $r->{'Suffix'}|;
  $record->{Email} = $r->{Email};
  $record->{CreateProvID} = $form->{LOGINPROVID};
  my $qClinicProvider=qq|select Type from ProviderPrivs where ProvID=? and Type='ClinicProvider'|;
  my $sClinicProvider=$dbh->prepare($qClinicProvider);
  $sClinicProvider->execute($r->{ProvID}) || myDBI->dberror($qClinicProvider);
  if ( my ($ClinicProvider) = $sClinicProvider->fetchrow_array ) 
  { $record->{Clinician} = 1; }
  elsif ( $r->{Type} == 4 )
  { $record->{Name} .= qq| ($r->{JobTitle})|; }
  $sClinicProvider->finish();
#warn qq|write: $TreeProvID: $TreeProvID, $record->{ListProvID}=$record->{Name} ($Cnt/$record->{Indent})\n|;
  my $qInsert = DBA->genInsert($form,$table,$record);
  my $sInsert = $dbh->prepare($qInsert);
  $sInsert->execute() || myDBI->dberror("insTree: $qInsert");
  $sInsert->finish();
  return(1);
}
############################################################################
1;
