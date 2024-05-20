package MgrTree;
use DBI;
use myDBI;
use SysAccess;
use DBUtil;
############################################################################
# Recursive routine to get all the sub-Managers.
sub getProviders
{
  my ($self,$form,$MgrProvID,$Index) = @_;
#warn "enter->getProviders: $MgrProvID, $Index\n";

  my @ProvList = ();
  my $dbh = myDBI->dbconnect($form->{'DBNAME'});
  $Index += 1;
  my $sManager = $dbh->prepare("
     select * from Manager
       left join Provider on Provider.ProvID=Manager.ProviderID
       where Manager.ManagerID=?
       order by Provider.Name,Provider.LName,Provider.FName,Provider.Suffix
");
#warn qq|getProviders: select with $MgrProvID\n|;
  $sManager->execute($MgrProvID);
  while (my $r = $sManager->fetchrow_hashref) 
  { 
    if ( $r->{ProvID} )      # test for matching Provider record with Manager record.
    {
      $r->{'Index'} = $Index;
      push @ProvList, $r;
#warn "recall->getProviders: ProvID=$r->{'ProvID'}, $r->{FName} $r->{LName}\n";
      push @ProvList, $self->getProviders($form,$r->{'ProvID'},$Index);
    }
  }
  $sManager->finish;
#warn "getProviders: done\n\n";
  return(@ProvList);
}
############################################################################
sub getManagers
{
  my ($self,$form,$ProvID,$Index) = @_;
#warn qq|ENTER getManagers: ProvID=${ProvID}, Index=${Index}\n|;
  my @MgrList = ();
  $Index += 1;
  my $dbh = myDBI->dbconnect($form->{'DBNAME'});
  my $q = qq|select ManagerID from Manager where ProviderID='${ProvID}'|;
#warn qq|getManagers: q=\n${q}\n|;
  my $s = $dbh->prepare($q);
  $s->execute() || myDBI->dberror($q);
  if ( my $ManagerID = $s->fetchrow_array )
  {
    my $qProvider = qq|select * from Provider where ProvID=?|;
    my $sProvider = $dbh->prepare($qProvider);
    $sProvider->execute($ManagerID) || myDBI->dberror($qProvider);
    if ( my $rProvider = $sProvider->fetchrow_hashref )
    {
      $rProvider->{'Index'} = $Index;
#warn "getManagers: push=$rProvider->{'ProvID'}, $rProvider->{FName} $rProvider->{LName}\n";
      push @MgrList, $rProvider;
      push @MgrList, $self->getManagers($form,$rProvider->{ProvID},$Index);
    }
  }
#foreach my $f ( @MgrList ) { warn "getManagers: $Index=$f->{ProvID}\n"; }
  return(@MgrList);
}
############################################################################
# get the Immediate Manager for Provider.
##
sub getManager
{
  my ($self, $form, $ProvID) = @_;
# NOT OK if called with a NULL Provider.

  my $ManagerID = '';
  if ( $ProvID )
  {
    my $dbh = myDBI->dbconnect($form->{'DBNAME'});
    my $q = qq|select ManagerID from Manager where ProviderID=${ProvID}|;
#warn qq|q=\n$q\n|;
    my $s = $dbh->prepare($q);
    $s->execute() || myDBI->dberror($q);
    ($ManagerID) = $s->fetchrow_array;
#warn "getManager: returning $ManagerID\n";
  }
  return($ManagerID);
}
sub getClinic
{
  my ($self, $form, $ProvID) = @_;
  my $ClinicID = '';
  foreach my $Mgr ( $self->getManagers($form,$ProvID,0) )
  { 
    $ClinicID = $Mgr->{ProvID} if ( $Mgr->{Type} == 3 ); 
#warn qq|getClinic: check: ProvID=$ProvID, Mgr=$Mgr->{ProvID}, ClinicID=$ClinicID\n|; 
    last if ( $ClinicID );
  }
  return($ClinicID);
}
sub getAgency
{
  my ($self, $form, $ProvID) = @_;
#warn qq|getAgency ProvID=$ProvID\n|;
  my $AgencyID = '';
  foreach my $Mgr ( $self->getManagers($form,$ProvID,0) )
  { 
    $AgencyID = $Mgr->{ProvID} if ( $Mgr->{Type} == 2 ); 
#warn qq|getAgency: check: ProvID=$ProvID, Mgr=$Mgr->{ProvID}, AgencyID=$AgencyID\n|; 
    last if ( $AgencyID );
  }
  $AgencyID = $ProvID unless ( $AgencyID );
  return($AgencyID);
}
############################################################################
sub AgencyList
{
  my ($self,$form) = @_;

  my $alist = ();
  my $clist = ();
  my $dbh = myDBI->dbconnect($form->{'DBNAME'});
  my $sAgency = $dbh->prepare("select ManagerID, ProvID, Name, LName, FName, Email, City, Type from Provider left join Manager on ProviderID=ProvID where Provider.Type=2");
  my $sClinic = $dbh->prepare("select ManagerID, ProvID, Name, LName, FName, Email, City, Type from Provider left join Manager on ProviderID=ProvID where ManagerID=? and Provider.Type=3");
  $sAgency->execute() || myDBI->dberror("get Agency->select");
  while ( my $rAgency = $sAgency->fetchrow_hashref )
  {
    my $AID = $rAgency->{ProvID};
    $alist->{$AID} = $rAgency;
#warn qq|AgencyList: Agency: $rAgency->{ManagerID}, $rAgency->{ProvID}, $rAgency->{Name}, $rAgency->{Type}\n|;
#foreach my $f ( sort keys %{$rAgency} ) { warn "tst: rAgency-$f=$rAgency->{$f}\n"; }
    $sClinic->execute($rAgency->{ProvID}) || myDBI->dberror("get Clinic->select");
    while ( my $rClinic = $sClinic->fetchrow_hashref )
    {
      my $CID = $rClinic->{ProvID};
      $alist->{$AID}->{$CID} = $rClinic;
      $clist->{$CID} = $AID;
#warn qq|AgencyList: Clinic: $rClinic->{ManagerID}, $rClinic->{ProvID}, $rClinic->{Name}, $rClinic->{Type}\n|;
    }
  }
  $sClinic->finish();
  $sAgency->finish();
#foreach my $f ( sort keys %{$alist} ) { warn "tst: alist-$f=$alist->{$f}\n"; }
  return($alist,$clist);
}
############################################################################
1;
