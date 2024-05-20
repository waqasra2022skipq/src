package Accounts;
use myConfig;
use myForm;
use myDBI;
require(myConfig->cfg('CFG').'/accounts.cfg');
############################################################################
sub db { return($DATABASES{$_[1]}{$_[2]}); }
sub dbs { return($_[1]=~/all/i?@ALL_DBS : $_[1]=~/live/i?@LIVE_DBS : $_[1]=~/test/i?@TEST_DBS : $_[1]=~/demo/i?@DEMO_DBS : @ACTIVE_DBS); }
sub accts { return($_[1]=~/active/i?@ACTIVE_ACCTS : $_[1]=~/live/i?@LIVE_ACCTS : $_[1]=~/test/i?@TEST_ACCTS : $_[1]=~/demo/i?@DEMO_ACCTS : @ALL_ACCTS); }
# Build the list of PIN/NPI/OrganizationIDs.
sub PINs
{
  my ($self,@DBS) = @_;
  my $PINs = {};
  my $form;
  foreach my $DBNAME ( @DBS )
  {
warn qq|DBNAME=${DBNAME}\n|;
    $form = myForm->new("DBNAME=$DBNAME");
    my $dbh = myDBI->dbconnect($form->{'DBNAME'});
    my $sContracts = $dbh->prepare("select Contracts.PIN,Contracts.OrgID,ProviderControl.NPI,Provider.Name,xInsurance.Descr,xInsurance.RecID,xInsurance.SubID from Contracts left join xInsurance on xInsurance.ID=Contracts.InsID left join Provider on Provider.ProvID=Contracts.ProvID left join ProviderControl on ProviderControl.ProvID=Contracts.ProvID where Provider.Active=1 and xInsurance.Descr='medicaid' and Contracts.PIN is not null order by Contracts.PIN");
    $sContracts->execute();
    while ( my ($PIN,$OrgID,$NPI,$Name,$Descr,$RecID,$SubID) = $sContracts->fetchrow_array )
    {
      next if ( $PIN eq '' );
      $PINs->{$PIN}->{OrgID} = $OrgID;
      $PINs->{$PIN}->{DB} = $DBNAME;
      $PINs->{$PIN}->{NPI} = $NPI;
      $PINs->{$PIN}->{Name} = $Name;
    }
    $sContracts->finish();
  }
  return($PINs);
}
############################################################################
sub NPIs
{
  my ($self, @DBS) = @_;
  my $NPIs = {};
  my $form;
  foreach my $DBNAME ( @DBS )
  {
    $form = myForm->new("DBNAME=$DBNAME");
    my $dbh = myDBI->dbconnect($form->{'DBNAME'});
    #my $sContracts = $dbh->prepare("select Contracts.PIN,Contracts.OrgID,ProviderControl.NPI,Provider.Name from Contracts left join xInsurance on xInsurance.ID=Contracts.InsID left join Provider on Provider.ProvID=Contracts.ProvID left join ProviderControl on ProviderControl.ProvID=Contracts.ProvID where Provider.Active=1 and xInsurance.Descr='medicaid' order by ProviderControl.NPI");
    my $sContracts = $dbh->prepare("select Contracts.PIN,Contracts.OrgID,ProviderControl.NPI,Provider.Name from Contracts left join xInsurance on xInsurance.ID=Contracts.InsID left join Provider on Provider.ProvID=Contracts.ProvID left join ProviderControl on ProviderControl.ProvID=Contracts.ProvID where Provider.Active=1 order by ProviderControl.NPI");
    $sContracts->execute();
    while ( my ($PIN,$OrgID,$NPI,$Name) = $sContracts->fetchrow_array )
    {
      next if ( $NPI eq '' );
      $NPIs->{$NPI}->{OrgID} = $OrgID;
      $NPIs->{$NPI}->{DB} = $DBNAME;
      $NPIs->{$NPI}->{PIN} = $PIN;
      $NPIs->{$NPI}->{Name} = $Name;
    }
    $sContracts->finish();
  }
  return($NPIs);
}
############################################################################
# for bin/ProcessFTP
sub NPIRECs
{
  my ($self, @DBS) = @_;
  my $NPIs = {};
  my $form;
  foreach my $DBNAME ( @DBS )
  {
    $form = myForm->new("DBNAME=$DBNAME");
    my $dbh = myDBI->dbconnect($form->{'DBNAME'});
    my $sContracts = $dbh->prepare("select Contracts.PIN,Contracts.OrgID,ProviderControl.NPI,Provider.Name,xInsurance.Descr,xInsurance.RecID,xInsurance.SubID from Contracts left join xInsurance on xInsurance.ID=Contracts.InsID left join Provider on Provider.ProvID=Contracts.ProvID left join ProviderControl on ProviderControl.ProvID=Contracts.ProvID where Provider.Active=1 and ProviderControl.NPI is not null and Contracts.PIN is not null and xInsurance.RecID is not null and xInsurance.SubID is not null order by ProviderControl.NPI, xInsurance.Descr desc");
    $sContracts->execute();
    while ( my ($PIN,$OrgID,$NPI,$Name,$Descr,$RecID,$SubID) = $sContracts->fetchrow_array )
    {
      my $key = qq|${NPI}_${RecID}|;
      $NPIs->{$key}->{DB} = $DBNAME;
      $NPIs->{$key}->{NPI} = $NPI;
      $NPIs->{$key}->{RecID} = $RecID;
      $NPIs->{$key}->{SubID} = $SubID;
      $NPIs->{$key}->{Descr} = $Descr;
      $NPIs->{$key}->{PIN} = $PIN;
      $NPIs->{$key}->{OrgID} = $OrgID;
      $NPIs->{$key}->{Name} = $Name;
    }
    $sContracts->finish();
  }
  return($NPIs);
}
############################################################################
# for bin/ProcessFTP
sub PINRECs
{
  my ($self, @DBS) = @_;
  my $PINs = {};
  my $form;
  foreach my $DBNAME ( @DBS )
  {
    $form = myForm->new("DBNAME=$DBNAME");
    my $dbh = myDBI->dbconnect($form->{'DBNAME'});
    my $sContracts = $dbh->prepare("select Contracts.PIN,Contracts.OrgID,ProviderControl.NPI,Provider.Name,xInsurance.Descr,xInsurance.RecID,xInsurance.SubID from Contracts left join xInsurance on xInsurance.ID=Contracts.InsID left join Provider on Provider.ProvID=Contracts.ProvID left join ProviderControl on ProviderControl.ProvID=Contracts.ProvID where Provider.Active=1 and ProviderControl.NPI is not null and Contracts.PIN is not null and xInsurance.RecID is not null and xInsurance.SubID is not null order by ProviderControl.NPI, xInsurance.Descr desc");
    $sContracts->execute();
    while ( my ($PIN,$OrgID,$NPI,$Name,$Descr,$RecID,$SubID) = $sContracts->fetchrow_array )
    {
      $PIN =~ s/-//g;
      my $key = qq|${PIN}_${RecID}|;
      $PINs->{$key}->{DB} = $DBNAME;
      $PINs->{$key}->{NPI} = $NPI;
      $PINs->{$key}->{RecID} = $RecID;
      $PINs->{$key}->{SubID} = $SubID;
      $PINs->{$key}->{Descr} = $Descr;
      $PINs->{$key}->{PIN} = $PIN;
      $PINs->{$key}->{OrgID} = $OrgID;
      $PINs->{$key}->{Name} = $Name;
    }
    $sContracts->finish();
  }
  return($PINs);
}
############################################################################
sub OrgIDs
{
  my ($self, @DBS) = @_;
  my $OrgIDs = {};
  my $form;
  foreach my $DBNAME ( @DBS )
  {
    $form = myForm->new("DBNAME=$DBNAME");
    my $dbh = myDBI->dbconnect($form->{'DBNAME'});
    my $sContracts = $dbh->prepare("select Contracts.PIN,Contracts.OrgID,ProviderControl.NPI,Provider.Name from Contracts left join xInsurance on xInsurance.ID=Contracts.InsID left join Provider on Provider.ProvID=Contracts.ProvID left join ProviderControl on ProviderControl.ProvID=Contracts.ProvID where Provider.Active=1 and xInsurance.Descr='medicaid' order by Contracts.PIN");
    $sContracts->execute();
    while ( my ($PIN,$OrgID,$NPI,$Name) = $sContracts->fetchrow_array )
    {
#warn qq|PIN=$PIN,OrgID=$OrgID,NPI=$NPI,Name=$Name\n|;
      next if ( $OrgID eq '' );
      next if ( $OrgID eq '0000000158' );   # turn off Western Plains
      next if ( $OrgID eq '0200361190' );   # turn off Elizabeth Hooks
      $OrgIDs->{$OrgID}->{PIN} = $PIN;
      $OrgIDs->{$OrgID}->{DB} = $DBNAME;
      $OrgIDs->{$OrgID}->{NPI} = $NPI;
      $OrgIDs->{$OrgID}->{Name} = $Name;
    }
    $sContracts->finish();
  }
  return($OrgIDs);
}
############################################################################
sub TaxIDs
{
  my ($self, @DBS) = @_;
  my $TaxIDs = {};
  my $form;
  foreach my $DBNAME ( @DBS )
  {
    $form = myForm->new("DBNAME=$DBNAME");
    my $dbh = myDBI->dbconnect($form->{'DBNAME'});
    my $sContracts = $dbh->prepare("select Contracts.ProvID,xInsurance.Descr,Contracts.TaxID,Contracts.PIN,Contracts.OrgID,ProviderControl.NPI,Provider.Name from Contracts left join xInsurance on xInsurance.ID=Contracts.InsID left join Provider on Provider.ProvID=Contracts.ProvID left join ProviderControl on ProviderControl.ProvID=Contracts.ProvID where Provider.Active=1 order by Contracts.TaxID");
    $sContracts->execute();
    while ( my ($ProvID,$InsDescr,$TaxID,$PIN,$OrgID,$NPI,$Name) = $sContracts->fetchrow_array )
    {
      $TaxID =~ s/[- ]//g;
      next if ( $TaxID eq '' );
      my $key = $InsDescr.'_'.$TaxID;
      $TaxIDs->{$key}->{ProvID} = $ProvID;
      $TaxIDs->{$key}->{PIN} = $PIN;
      $TaxIDs->{$key}->{OrgID} = $OrgID;
      $TaxIDs->{$key}->{DB} = $DBNAME;
      $TaxIDs->{$key}->{NPI} = $NPI;
      $TaxIDs->{$key}->{Name} = $Name;
    }
    $sContracts->finish();
  }
  return($TaxIDs);
}
############################################################################
1;
