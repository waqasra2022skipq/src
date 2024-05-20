package NewCrop;
use MgrTree;
use myDBI;
use DBA;
$AGENCY = ();
$CLINIC = ();
$PROVIDER = ();
$SUPERVISOR = ();
$PRESCRIBER = ();
############################################################################
sub new
{
  my ($self,$form,$UseClinicID,$UseProvID,$UseClientID) = @_;
#warn qq|ClientID=$ClientID, UseProvID=$UseProvID, UseClinicID=$UseClinicID\n|;
  my $ClinicID = $UseClinicID;                                    # could be null
  my $ProvID = $UseProvID ? $UseProvID : $form->{'LOGINPROVID'};  # could be null (default)
  my $ClientID = $UseClientID;                                    # could be null
  my $dbh = myDBI->dbconnect($form->{'DBNAME'});
  if ( $ClientID )
  {
    my $sClient = $dbh->prepare("select * from Client where ClientID=?");
    $sClient->execute($ClientID) || $form->dberror("NewCrop: new: select Client $ClientID");
    if ( $rClient = $sClient->fetchrow_hashref )
    {
      $ProvID = $rClient->{'ProvID'} unless ( $UseProvID );
      $ClinicID = $rClient->{'clinicClinicID'} unless ( $UseClinicID );
      $PROVIDER->{'PrimaryProviderID'} = $form->{'DBNAME'}.'-'.$rClient->{'ProvID'};
    }
    else { return('Client ($ClientID) missing!'); }
    $sClient->finish();
  }
  unless ( $ClinicID ) { return('ClinicID missing!'); }
  unless ( $ProvID ) { return('ProvID missing!'); }
  my $AgencyID = MgrTree->getAgency($form,$ClinicID);
#warn qq|ClinicID=${ClinicID}, AgencyID=${AgencyID}\n|;
  my $sProvider = $dbh->prepare("select * from Provider where ProvID=?");
  $sProvider->execute($AgencyID) || $form->dberror("NewCrop: select Agency $AgencyID");
  $AGENCY = $sProvider->fetchrow_hashref;
  $AGENCY->{'siteID'} = $form->{'DBNAME'};
  $AGENCY->{'AccountID'} = $form->{'DBNAME'}.'-'.$AgencyID;
  $AGENCY->{'accountName'} = $AGENCY->{'Name'};
  $AGENCY->{'ZipCode'} = substr($AGENCY->{Zip},0,5);
  $AGENCY->{'ZipPlus'} = substr($AGENCY->{Zip},6,4);
  ($AGENCY->{'accountPrimaryPhoneNumber'} = $AGENCY->{WkPh}) =~ s/[- ]//g;
  ($AGENCY->{'accountPrimaryFaxNumber'} = $AGENCY->{Fax}) =~ s/[- ]//g;
  #FIX $AGENCY->{'ZipPlus'} = '0000' unless ( $AGENCY->{'ZipPlus'} );
  $sProvider->execute($ClinicID) || $form->dberror("NewCrop: select Clinic $ClinicID");
  $CLINIC = $sProvider->fetchrow_hashref;
  $CLINIC->{'LocationID'} = $form->{'DBNAME'}.'-'.$AgencyID.'-'.$ClinicID;
  $CLINIC->{'locationName'} = $CLINIC->{'Name'};
  #FIX $CLINIC->{'FaxNum'} = '1234567890' unless ( $CLINIC->{'FaxNum'} );
  $CLINIC->{'ZipCode'} = substr($CLINIC->{Zip},0,5);
  $CLINIC->{'ZipPlus'} = substr($CLINIC->{Zip},6,4);
  #FIX $CLINIC->{'ZipPlus'} = '0000' unless ( $CLINIC->{'ZipPlus'} );
  ($CLINIC->{'primaryPhoneNumber'} = $CLINIC->{WkPh}) =~ s/[- ]//g;
  ($CLINIC->{'primaryFaxNumber'} = $CLINIC->{Fax}) =~ s/[- ]//g;
  $CLINIC->{'pharmacyContactNumber'} = $CLINIC->{'primaryPhoneNumber'}; # DEFAULT FIX
# define Provider Role (LOGIN or Primary)
  my $txt = $self->UserRole($form,$ProvID);
#warn qq|ProvID=$ProvID ($PROVIDER->{FName} $PROVIDER->{LName}), ClinicID=$ClinicID, AgencyID=$AgencyID\n|;
  $sProvider->finish();
  return();
}
sub name { return('a6d360ec-2159-4db6-b050-a6366fe89b4d'); }
sub password { return('b37c260d-88e0-4847-92f3-6fbb86c74a09'); }
sub partnerName { return('Millennium'); }
sub productName { return('MillenniumServices'); }
sub productVersion { return('V1.1'); }
sub siteID { return($AGENCY->{siteID}); }
sub AccountID { return($AGENCY->{AccountID}); }
sub agency { return($AGENCY->{$_[1]}); }
sub clinic { return($CLINIC->{$_[1]}); }
sub provider { return($PROVIDER->{$_[1]}); }
sub supervisor { return($SUPERVISOR->{$_[1]}); }
sub prescriber { return($PRESCRIBER->{$_[1]}); }
sub Credentials
{
  my ($self,$demo) = @_;
  my $xml = $demo eq 'demo' ? qq|
  <Credentials>
    <partnerName>|.$self->partnerName().qq|</partnerName>
    <name>demo</name>
    <password>demo</password>
    <productName>|.$self->productName().qq|</productName>
    <productVersion>|.$self->productVersion().qq|</productVersion>
  </Credentials>
|
  : qq|
  <Credentials>
    <partnerName>|.$self->partnerName().qq|</partnerName>
    <name>|.$self->name().qq|</name>
    <password>|.$self->password.qq|</password>
    <productName>|.$self->productName().qq|</productName>
    <productVersion>|.$self->productVersion().qq|</productVersion>
  </Credentials>
|;
  return($xml);
}
sub UserRole
{
  my ($self,$form,$ForProvID) = @_;
  my $ProvID = $ForProvID ? $ForProvID : $form->{LOGINPROVID};
#warn qq|UserRole: ForProvID=${ForProvID}, ProvID=${ProvID}\n|;
  my $xml = '';
  my $dbh = myDBI->dbconnect($form->{'DBNAME'});
  my $sProvider = $dbh->prepare("select * from Provider where Provider.ProvID=?");
  $sProvider->execute($ProvID) || $form->dberror("NewCrop: select UserRole $ProvID");
  if ( $PROVIDER = $sProvider->fetchrow_hashref )
  {
    $PROVIDER->{'UserRoleID'} = $form->{'DBNAME'}.'-'.$ProvID;
    $PROVIDER->{'role'} = DBA->getxref($form,'xNCRoles',$PROVIDER->{Role},'Role');
    $PROVIDER->{'user'} = DBA->getxref($form,'xNCRoles',$PROVIDER->{Role},'Type');
    $PROVIDER->{'code'} = DBA->getxref($form,'xNCRoles',$PROVIDER->{Role},'Code');
#warn qq|UserRole: $ProvID=YES: Role=$PROVIDER->{Role} ($PROVIDER->{FName} $PROVIDER->{LName})\n|;
    $xml = qq|
  <UserRole>
    <!-- See XML Schema: UserType for valid values -->
    <user>|.$PROVIDER->{user}.qq|</user>
    <!-- See XML Schema: RoleType for valid values -->
    <role>|.$PROVIDER->{role}.qq|</role>
  </UserRole>
|;
  }
  $sProvider->finish();
  return($xml);
}
sub SupervisingPhysician
{
  my ($self,$form) = @_;
#warn qq|SupervisingPhysician: SupervisingPhysician=$PROVIDER->{SupervisingPhysician}\n|;
  my $dbh = myDBI->dbconnect($form->{'DBNAME'});
  my $sProvider = $dbh->prepare("select * from Provider where ProvID=?");
  $sProvider->execute($PROVIDER->{SupervisingPhysician})
        || $form->dberror("NewCrop-SupervisingPhysician: select Provider $PROVIDER->{SupervisingPhysician}");
  $SUPERVISOR = $sProvider->fetchrow_hashref;
  my $sProviderControl = $dbh->prepare("select * from ProviderControl where ProvID=?");
  $sProviderControl->execute($PROVIDER->{SupervisingPhysician})
        || $form->dberror("NewCrop-SupervisingPhysician: select ProviderControl $PROVIDER->{SupervisingPhysician}");
  my $rProviderControl = $sProviderControl->fetchrow_hashref;
  my $sProviderLicenses = $dbh->prepare("select * from ProviderLicenses where ProvID=? and State='OK'");
  $sProviderLicenses->execute($PROVIDER->{SupervisingPhysician})
        || $form->dberror("NewCrop-SupervisingPhysician: select ProviderLicenses $PROVIDER->{SupervisingPhysician}");
  my $rProviderLicenses = $sProviderLicenses->fetchrow_hashref;
  $SUPERVISOR->{'UserRoleID'} = $form->{'DBNAME'}.'-'.$SUPERVISOR->{'ProvID'};
  $SUPERVISOR->{'npi'} = $rProviderControl->{'NPI'};
  $SUPERVISOR->{'dea'} = $rProviderLicenses->{'DEA'};
  $SUPERVISOR->{'licenseState'} = $rProviderLicenses->{'State'};
  $SUPERVISOR->{'licenseNumber'} = $rProviderLicenses->{'LicNumber'};
  $SUPERVISOR->{'upin'} = $SUPERVISOR->{'npi'};       ## FIX?
#warn qq|SupervisingPhysician: ProvID=$SUPERVISOR->{ProvID}, Name=$SUPERVISOR->{LName}, NPI=$SUPERVISOR->{npi}\n|;
  my $Type = DBA->getxref($form,'xNCRoles',$SUPERVISOR->{Role},'Type');
  my $xml = qq|
  <SupervisingDoctor ID="$SUPERVISOR->{UserRoleID}">
    <LicensedPrescriberName>
      <last>$SUPERVISOR->{'LName'}</last>
      <first>$SUPERVISOR->{'FName'}</first>
      <middle>$SUPERVISOR->{'MName'}</middle>
      <prefix>$SUPERVISOR->{'Pref'}</prefix>
      <suffix>$SUPERVISOR->{'Suffix'}</suffix>
    </LicensedPrescriberName>
    <dea>$SUPERVISOR->{'dea'}</dea>
    <upin>$SUPERVISOR->{'upin'}</upin>
    <licenseState>$SUPERVISOR->{'licenseState'}</licenseState>
    <licenseNumber>$SUPERVISOR->{'licenseNumber'}</licenseNumber>
    <npi>$SUPERVISOR->{'npi'}</npi>
  </SupervisingDoctor>
|;
  $sProvider->finish();
  $sProviderControl->finish();
  $sProviderLicenses->finish();
  return($xml);
}
sub isPrescriber
{
  my ($self,$form) = @_;
  my $dbh = myDBI->dbconnect($form->{'DBNAME'});
  my $sProvider = $dbh->prepare("select Role from Provider where ProvID=?");
  $sProvider->execute($form->{LOGINPROVID})
        || $form->dberror("NewCrop: isPrescriber: select Provider $form->{LOGINPROVID}");
  my ($Role) = $sProvider->fetchrow_array;
  my $Type = DBA->getxref($form,'xNCRoles',$Role,'Type');
#warn qq|isPrescriber: ProvID=$form->{LOGINPROVID}, Role=$Role, Type=$Type\n|;
  $sProvider->finish();
  return($Type eq '' || $Type eq 'Staff' ? 0 : 1);
}
sub hasRole
{
  my ($self,$form) = @_;
  my $dbh = myDBI->dbconnect($form->{'DBNAME'});
  my $sProvider = $dbh->prepare("select Role from Provider where ProvID=?");
  $sProvider->execute($form->{LOGINPROVID})
        || $form->dberror("NewCrop: hasRole: select Provider $form->{LOGINPROVID}");
  my ($Role) = $sProvider->fetchrow_array;
#warn qq|hasRole: Role=$Role= \n|;
  return($Role eq '' ? 0 : 1);
}
sub Staff
{
  my ($self,$form) = @_;
#warn qq|Staff: ProvID=$form->{LOGINPROVID}\n|;
  my $dbh = myDBI->dbconnect($form->{'DBNAME'});
  my $sProvider = $dbh->prepare("select * from Provider where ProvID=?");
  $sProvider->execute($form->{LOGINPROVID})
        || $form->dberror("NewCrop-Staff: select Provider $form->{LOGINPROVID}");
  $PRESCRIBER = $sProvider->fetchrow_hashref;
  my $sProviderControl = $dbh->prepare("select * from ProviderControl where ProvID=?");
  $sProviderControl->execute($form->{LOGINPROVID})
        || $form->dberror("NewCrop-Staff: select ProviderControl $form->{LOGINPROVID}");
  my $rProviderControl = $sProviderControl->fetchrow_hashref;
  my $sProviderLicenses = $dbh->prepare("select * from ProviderLicenses where ProvID=? and State='OK'");
  $sProviderLicenses->execute($form->{LOGINPROVID})
        || $form->dberror("NewCrop-Staff: select ProviderLicenses $form->{LOGINPROVID}");
  my $rProviderLicenses = $sProviderLicenses->fetchrow_hashref;
  $PRESCRIBER->{'PrescriberID'} = $form->{'DBNAME'}.'-'.$PRESCRIBER->{'ProvID'};
  $PRESCRIBER->{'npi'} = $rProviderControl->{'NPI'};
  $PRESCRIBER->{'dea'} = $rProviderLicenses->{'DEA'};
  $PRESCRIBER->{'licenseState'} = $rProviderLicenses->{'State'};
  $PRESCRIBER->{'licenseNumber'} = $rProviderLicenses->{'LicNumber'};
  $PRESCRIBER->{'upin'} = $PRESCRIBER->{'npi'};        # FIX?
#warn qq|Staff: ProvID=$PRESCRIBER->{ProvID}, Name=$PRESCRIBER->{LName}, NPI=$PRESCRIBER->{npi}\n|;
  my $Type = DBA->getxref($form,'xNCRoles',$PRESCRIBER->{Role},'Type');
  my $Role = DBA->getxref($form,'xNCRoles',$PRESCRIBER->{Role},'Role');
  my $xml = $Role eq 'nurse'
          ? qq|
  <${Type} ID="$PRESCRIBER->{PrescriberID}">
    <StaffName>
      <last>$PRESCRIBER->{'LName'}</last>
      <first>$PRESCRIBER->{'FName'}</first>
      <middle>$PRESCRIBER->{'MName'}</middle>
      <prefix>$PRESCRIBER->{'Pref'}</prefix>
      <suffix>$PRESCRIBER->{'Suffix'}</suffix>
    </StaffName>
    <license>$PRESCRIBER->{'licenseNumber'}</license>
  </${Type}>
|
          : qq|
  <${Type} ID="$PRESCRIBER->{PrescriberID}">
    <StaffName>
      <last>$PRESCRIBER->{'LName'}</last>
      <first>$PRESCRIBER->{'FName'}</first>
    </StaffName>
  </${Type}>
|;
  $sProvider->finish();
  $sProviderControl->finish();
  $sProviderLicenses->finish();
  return($xml);
}
sub Prescriber
{
  my ($self,$form) = @_;
#warn qq|Prescriber: ProvID=$form->{LOGINPROVID}\n|;
  my $dbh = myDBI->dbconnect($form->{'DBNAME'});
  my $sProvider = $dbh->prepare("select * from Provider where ProvID=?");
  $sProvider->execute($form->{LOGINPROVID})
        || $form->dberror("NewCrop-Prescriber: select Provider $form->{LOGINPROVID}");
  $PRESCRIBER = $sProvider->fetchrow_hashref;
  my $sProviderControl = $dbh->prepare("select * from ProviderControl where ProvID=?");
  $sProviderControl->execute($form->{LOGINPROVID})
        || $form->dberror("NewCrop-Prescriber: select ProviderControl $form->{LOGINPROVID}");
  my $rProviderControl = $sProviderControl->fetchrow_hashref;
  my $sProviderLicenses = $dbh->prepare("select * from ProviderLicenses where ProvID=? and State='OK'");
  $sProviderLicenses->execute($form->{LOGINPROVID})
        || $form->dberror("NewCrop-Prescriber: select ProviderLicenses $form->{LOGINPROVID}");
  my $rProviderLicenses = $sProviderLicenses->fetchrow_hashref;
  $PRESCRIBER->{'PrescriberID'} = $form->{'DBNAME'}.'-'.$PRESCRIBER->{'ProvID'};
  $PRESCRIBER->{'npi'} = $rProviderControl->{'NPI'};
  $PRESCRIBER->{'dea'} = $rProviderLicenses->{'DEA'};
  $PRESCRIBER->{'licenseState'} = $rProviderLicenses->{'State'};
  $PRESCRIBER->{'licenseNumber'} = $rProviderLicenses->{'LicNumber'};
  $PRESCRIBER->{'upin'} = $PRESCRIBER->{'npi'};        # FIX?
#warn qq|Prescriber: ProvID=$PRESCRIBER->{ProvID}, Name=$PRESCRIBER->{LName}, NPI=$PRESCRIBER->{npi}\n|;
  my $Type = DBA->getxref($form,'xNCRoles',$PRESCRIBER->{Role},'Type');
  my $xml = qq|
  <${Type} ID="$PRESCRIBER->{PrescriberID}">
    <LicensedPrescriberName>
      <last>$PRESCRIBER->{'LName'}</last>
      <first>$PRESCRIBER->{'FName'}</first>
      <middle>$PRESCRIBER->{'MName'}</middle>
    </LicensedPrescriberName>
    <dea>$PRESCRIBER->{'dea'}</dea>
    <upin>$PRESCRIBER->{'upin'}</upin>
    <licenseState>$PRESCRIBER->{'licenseState'}</licenseState>
    <licenseNumber>$PRESCRIBER->{'licenseNumber'}</licenseNumber>
    <npi>$PRESCRIBER->{'npi'}</npi>
  </${Type}>
|;
  $sProvider->finish();
  $sProviderControl->finish();
  $sProviderLicenses->finish();
  return($xml);
}
############################################################################
sub setRole
{
  my ($self,$form,$Access) = @_;
  my $OK = SysAccess->chkPriv($form,$Access);
#warn qq|setRole: Access=${Access}, OK=${OK}\n|;
  my $html = '';
  my $printdir = myConfig->cfg('FormsPrintURL');
  my $printdoc = $printdir.'/NewCrop_IDP_Process_and_Policy.pdf';
  if ( $OK ) 
  {
    $html = qq|
  <TR >
    <TD CLASS="strcol" >Medical Role</TD>
    <TD CLASS="strcol" >
      <SELECT NAME="Provider_Role_1">
        |.DBA->selxTable($form,'xNCRoles',$form->{'Provider_Role_1'},'ID Code').qq|
      </SELECT> 
    </TD>
    <TD CLASS="strcol" >Supervising Physician</TD>
    <TD CLASS="strcol" >
      <SELECT NAME="Provider_SupervisingPhysician_1">
        |.DBA->selSupervisingPhysicians($form,$form->{'Provider_SupervisingPhysician_1'}).qq|
      </SELECT> 
      (if MidLevel)
    </TD>
  </TR>
|;
  }
  else
  {
    $html = qq|
  <TR >
    <TD CLASS="strcol" >Medical Role</TD>
    <TD CLASS="hdrstr" >
        |.DBA->getxref($form,'xNCRoles',$form->{'Provider_Role_1'},'ID').qq|
    </TD>
    <TD CLASS="strcol" >Supervising Physician</TD>
    <TD CLASS="hdrstr" >
        |.DBA->getxref($form,'Provider',$form->{'Provider_SupervisingPhysician_1'},'FName LName').qq|
    </TD>
  </TR>
|;
  }
  $html .= qq|
  <TR>
    <TD CLASS="strcol" COLSPAN="4" >
      *To gain access to NewCrop Medications entry 
      <A HREF="javascript:ReportWindow('http://okmis.helpdocsonline.com/identity-proofing-idp','IDPlink')" TITLE="NewCrop Identity Proofing and Credentialing Service: Doctor’s Summary
" >click here</A>
    </TD>
  </TR>
|;
  return($html);
}
############################################################################
1;
