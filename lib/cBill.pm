package cBill;
use myDBI;
use DBUtil;
use MgrTree;
use Inv;

#############################################################################
# 7 rNotes used...
#  $rNote->{ClientID}
#  $rNote->{ContLogDate}
#  $rNote->{SCID}
#  $rNote->{TrID});
#  $rNote->{BillDate};
#  $Duration = DBUtil->getDuration($rNote->{ContLogBegTime},$rNote->{ContLogEndTime});
#############################################################################
sub CheckNote
{
  my ($self,$form,$TrID) = @_;
#warn qq|CheckNote: TrID=$TrID\n|;
  return(1,'MISSING TrID!') unless ( $TrID );
  my ($code, $msg) = (0,'');
  my ($chkcode, $chkmsg) = (0,'');
  my $dbh = myDBI->dbconnect($form->{'DBNAME'});
  my $q = qq|select *, Treatment.ProvID as ProvID, Client.ProvID as PrimaryProvID from Treatment left join Client on Client.ClientID=Treatment.ClientID left join xSC on xSC.SCID=Treatment.SCID where TrID='${TrID}'|;
  my $s = $dbh->prepare("select *, Treatment.ProvID as ProvID, Client.ProvID as PrimaryProvID from Treatment left join Client on Client.ClientID=Treatment.ClientID where Treatment.TrID=?");
  $s->execute($TrID) || $form->dberror("ChkNote: select Treatment (${TrID})");
  my $r = $s->fetchrow_hashref;
  $s->finish();
#foreach my $f ( sort keys %{$r} ) { warn "CheckNote: r-${f}=$r->{$f}\n"; }
#warn qq|CheckNote: ClientID=$r->{'ClientID'}, TrID=$r->{'TrID'}\n|;
  my $rxSC = $self->getServiceCode($form,$r->{SCID},$r->{ContLogDate},$r->{ContLogBegTime},$r->{ContLogEndTime},$r->{TrID},$r->{BillDate});
#foreach my $f ( sort keys %{$rxSC} ) { warn "CheckNote: rxSC-${f}=$rxSC->{$f}\n"; }

# Check for missing Contact Date...
  if ( $r->{'ContLogDate'} eq '' || $r->{'ContLogDate'} eq '0000-00-00' )
  { $msg .= qq| MISSING Contact Date! |; $code++; }

# Check for valid Service Code and rates...
  ($chkcode,$chkmsg) = $self->CheckServiceCode
                  ($form,$r->{SCID},$r->{ContLogDate},$r->{ContLogBegTime},$r->{ContLogEndTime},$r->{TrID},$r->{BillDate});
  if ( $chkcode && $chkmsg ) { $msg .= $chkmsg; $code++; } elsif ( $chkmsg ) { $msg .= $chkmsg; }
# Check for Duplicate Service Code for Client on same date...
  ($chkcode,$chkmsg) = $self->CheckClientDUP($form,$r->{ClientID},$r->{ProvID},$r->{TrID},$r->{SCID},$r->{ContLogDate});
  if ( $chkcode && $chkmsg ) { $msg .= $chkmsg; $code++; } elsif ( $chkmsg ) { $msg .= $chkmsg; }
# Check for valid Client name and such...
  ($chkcode,$chkmsg) = $self->CheckClient($form,$r->{ClientID});
  if ( $chkcode && $chkmsg ) { $msg .= $chkmsg; $code++; } elsif ( $chkmsg ) { $msg .= $chkmsg; }
  return($code,$msg) if ( $rxSC->{UnitLbl} eq 'NonBill' );

# Check for valid Primary Provider name and such...
  ($chkcode,$chkmsg) = $self->CheckProvider($form,$r->{ProvID});
  if ( $chkcode && $chkmsg ) { $msg .= $chkmsg; $code++; } elsif ( $chkmsg ) { $msg .= $chkmsg; }

# Check for valid Client Insurance
  ($chkcode,$chkmsg) = $self->CheckInsurance($form,$r->{ClientID},$rxSC->{'InsID'},$r->{ContLogDate});
  if ( $chkcode && $chkmsg ) { $msg .= $chkmsg; $code++; } elsif ( $chkmsg ) { $msg .= $chkmsg; }

# Check for valid Clinic Contract
  ($chkcode,$chkmsg) = $self->CheckContract($form,$r->{ClinicID},$rxSC->{'InsID'},$r->{ProvID},$r->{ClientID},$r->{ContLogDate});
  if ( $chkcode && $chkmsg ) { $msg .= $chkmsg; $code++; } elsif ( $chkmsg ) { $msg .= $chkmsg; }

# Check for valid Authorization
  if ( $rxSC->{PAReq} )
  {
    ($chkcode,$chkmsg) = $self->CheckAuth($form,$r->{ClientID},$rxSC->{'InsID'},$r->{ContLogDate},$r->{SCID});
    if ( $chkcode && $chkmsg ) { $msg .= $chkmsg; $code++; } elsif ( $chkmsg ) { $msg .= $chkmsg; }
  }

# Check for AdmitDate if Inpatient Place of Service...
  my $POSFederal = DBA->getxref($form,'xPOS',$r->{'POS'},'Federal');
#warn qq|CheckNote: POS=$r->{'POS'}/${POSFederal}\n|;
  if ( $POSFederal =~ /21|51|61/ )
  {
    my $sClientRelations = $dbh->prepare("select * from ClientRelations where ClientID=?");
    $sClientRelations->execute($r->{'ClientID'}) || $form->dberror("ChkNote: select ClientRelations ($r->{'ClientID'}");
    my $rClientRelations = $sClientRelations->fetchrow_hashref;
#warn qq|CheckNote: ResAdmitDate=$rClientRelations->{'ResAdmitDate'}\n|;
    if ( $rClientRelations->{'ResAdmitDate'} eq '' )
    {
      my $POSDescr = DBA->getxref($form,'xPOS',$r->{'POS'},'Descr');
      $msg .= qq| MISSING Admit Date for PlaceOfService: ${POSDescr} (change Date on Relations screen)|; $code++; 
#warn qq|CheckNote: POS=${POS}, msg=${msg}\n|;
    }
    $sClientRelations->finish();
  }

# Check for Problems exists...
  ($chkcode,$chkmsg) = $self->CheckProblems($form,$r->{ClientID},$r->{TrID});
#warn qq|CheckProblems: chkcode=$chkcode, chkmsg=$chkmsg\n|;
  if ( $chkcode && $chkmsg ) { $msg .= $chkmsg; $code++; } elsif ( $chkmsg ) { $msg .= $chkmsg; }

## Check for valid Diagnosis
#  ($chkcode,$chkmsg) = $self->CheckDiag($form,$r->{ClientID},$rxSC->{'InsID'},$r->{ContLogDate});
#  if ( $chkcode && $chkmsg ) { $msg .= $chkmsg; $code++; } elsif ( $chkmsg ) { $msg .= $chkmsg; }

  return($code,$msg);
}
sub CheckServiceCode
{
  my ($self,$form,$SCID,$ContDate,$BegTime,$EndTime,$TrID,$BillDate) = @_;

  my $rxSC = $self->getServiceCode($form,$SCID,$ContDate,$BegTime,$EndTime,$TrID,$BillDate);
  if ( $rxSC->{ServiceRate} eq '' )
  { return(1,'Service Code does NOT have ServiceRate! '); }
  elsif ( $rxSC->{HrsPerUnit} eq '' )
  { return(1,'Service Code does NOT have HrsPerUnit! '); }
  elsif ( $rxSC->{UnitLbl} ne 'NonBill' && $rxSC->{Units} <= 0 ) 
  { return(1,'Units are less than or equal to 0! '); }
  elsif ( $rxSC->{UnitLbl} eq '' )
  { return(1,'Service Code does NOT have UnitLbl! '); }
  elsif ( $rxSC->{SCName} eq '' )
  { return(1,'Service Code does NOT have Name! '); }
  elsif ( $rxSC->{SCNum} eq '' )
  { return(1,'Service Code does NOT have Number! '); }
  elsif ( $rxSC->{POS} eq '' )
  { return(1,'Service Code does NOT have Place of Service! '); }
  elsif ( int($rxSC->{Units}) != $rxSC->{Units} ) 
  { return(0,'Partial Units are being billed. '); }
  return(0,'');
}
# check duplicate note for Provider/Client/ContDate/ServiceCode
#  NO TrID is ok...still check for duplicate...
sub CheckClientDUP
{
  my ($self,$form,$ClientID,$ProvID,$TrID,$SCID,$ContDate) = @_;
#warn qq|CheckClientDUP: $ClientID,$ProvID,$TrID,$SCID,$ContDate\n|;
  return(0,'') unless ( $ClientID );
  return(0,'') if ( $ClientID < 10  || $ClientID == 67585);    # ODMH and NONID Clients
  return(0,'') unless ( $ProvID );
  return(0,'') unless ( $SCID );
  return(0,'') if ( $SCID == 3591 );     # CARS Travel Code
  return(0,'') unless ( $ContDate );
  my $SCNum = DBA->getxref($form,'xSC',$SCID,'SCNum');
  return(0,'') if ( $SCNum =~ /^X/ );              # forget X codes (Non-Billable).
  return(0,'') if ( $SCNum eq 'S0215 HF TG' );     # Medicaid Home/Community Based Travel.
  return(0,'') if ( $SCNum eq 'H0001 HF TG U1');   # Medicaid Residential Screening and Referral (ODASL).
  return(0,'') if ( $SCNum eq 'H0001 HF QJ');      # Drug Court (2nd & 3rd evemts) (Prison codes)
  return(0,'') if ( $SCNum eq 'T1017 TS' );        # HealthHome Targeted Case Management.
  return(0,'') if ( $SCNum eq 'S9482 HE' );        # HealthHome Clinical Evaluation and Assessment Children
# KLS Check for these from validateNote.pl sub DUP...
# Skip Health Home and Meaningful Use (InPatient Procedures) Insurance codes
#  my $SKIPINS = "and xSC.InsID !='356' and xSC.InsID !='391'";
# Skip T1012 HF codes for Providers (because both Group and Individual are ok)...
#  my $T1012 = "and xSC.SCNum NOT LIKE 'T1012 HF%'";

#warn qq|CheckClientDUP: ClientID=${ClientID},ProvID=${ProvID},TrID=${TrID},SCNum=${SCNum},ContDate=${ContDate}\n|;
  my $dbh = myDBI->dbconnect($form->{'DBNAME'});
  my $addInsCheck = '';
  ##my $addInsCheck = 'and';
  if ( $addInsCheck eq 'and' )      ## NO DUPlicate on different Insurances. (added 8/10/17)
  {
    my $sTreatment = $dbh->prepare("select * from Treatment left join xSC on xSC.SCID=Treatment.SCID where Treatment.TrID='${TrID}'");
    $sTreatment->execute() || $form->dberror("CheckClientDUP: select error ($ClientID/$ContDate/$SCNum}");
    my $rTreatment = $sTreatment->fetchrow_hashref;
    $addInsCheck .= qq| xSC.InsID='$rTreatment->{'InsID'}'|;
  }
  my $s = $dbh->prepare("select * from Treatment left join xSC on xSC.SCID=Treatment.SCID where Treatment.ClientID='${ClientID}' and Treatment.ProvID='${ProvID}' and Treatment.TrID!='${TrID}' and Treatment.ContLogDate='${ContDate}' and Treatment.BillStatus!=4 and xSC.SCNum='${SCNum}' ${addInsCheck}");
  $s->execute() || $form->dberror("CheckClientDUP: select error (${ClientID}/${ContDate}/${SCNum}/${addInsCheck}");
#my $cnt = $s->rows(); warn qq|CheckClientDUP: $r->{TrID},$cnt\n|;
  my $r = $s->fetchrow_hashref;
  $s->finish();
  if ( $r->{TrID} )
  { return(1,"Duplicate Note: $r->{TrID}! Same Service Code for Client on same day! Combine duplicate notes into 1 note for Client for same Service Code on the same Contact Date. Document services inside of note. "); }
  return(0,'');
}
sub CheckClient
{
  my ($self,$form,$ClientID) = @_;
  my $dbh = myDBI->dbconnect($form->{'DBNAME'});
  my $s = $dbh->prepare("select * from Client where ClientID=?");
  $s->execute($ClientID) || $form->dberror("CheckClient: select error ($ClientID}");
  my $r = $s->fetchrow_hashref;
  $s->finish();
  if ( $r->{clinicClinicID} eq '' )
  { return(1,'Client Clinic is NULL! ',$r); }
  if ( $r->{FName} eq '' )
  { return(1,'Client FName is NULL! ',$r); }
  if ( length($r->{FName}) < 2 )
  { 
    unless ( $r->{FName} =~ /[A-Z]/ )
    { return(1,'Client FName invalid! ',$r); }
  }
  if ( $r->{LName} eq '' )
  { return(1,'Client LName is NULL! ',$r); }
  if ( length($r->{LName}) < 2 )
  { 
    unless ( $r->{LName} =~ /[A-Z]/ )
    { return(1,'Client LName invalid! ',$r); }
  }
  (my $Addr1 = uc substr($r->{Addr1},0,55)) =~ s/^\s*(.*?)\s*$/$1/g;
# trim this weird thing from MS...
  $Addr1 =~ s:�:1/2:g; $Addr1 =~ s:`::g;
  if ( $Addr1 eq '' )
  { return(1,'Client Address is NULL or invalid! ',$r); }
  if ( $r->{Addr1} eq '.' )
  { return(1,'Client Address is a period! ',$r); }

  if($r->{Homeless} ne 1 && $r->{Zip} ne "99999") {
    # Do city/state checks only if the Client is Not Homeless and Client Zip is Not 
    if ( $r->{City} eq '' )
    { return(1,'Client City is NULL! ',$r); }
    if ( $r->{City} eq '.' )
    { return(1,'Client City is a period! ',$r); }
    if ( $r->{ST} eq '' )
    { return(1,'Client State is NULL! ',$r); }    
  }

  if ( $r->{Zip} eq '' )
  { return(1,'Client Zip is NULL! ',$r); }
  if ( $r->{Zip} !~ /^(\d{5})$/ && $r->{Zip} !~ /^(\d{5})(-)(\d{4})$/ )
  { return(1,"Client Zip is INVALID! ($r->{Zip}) ",$r); }
  if ( $r->{Gend} ne 'M' and $r->{Gend} ne 'F' )
  { return(1,"Client Gender is INVALID! ($r->{Gend}) ",$r); }
  if ( $r->{DOB} eq '' || $r->{DOB} eq '0000-00-00' )
  { return(1,"Client DOB is INVALID! ($r->{DOB}) ",$r); }
  if ( $r->{SSN} eq '' || $r->{SSN} !~ /(\d{3})-(\d{2})-(\d{4})/ )
  { return(1,"Client SSN is INVALID! ($r->{SSN}) ",$r); }
  return(0,'');
}
sub CheckProvider
{
  my ($self,$form,$ProvID) = @_;
  my ($code, $msg) = (0,'');
  my $dbh = myDBI->dbconnect($form->{'DBNAME'});
  my $sProvider=$dbh->prepare("select * from Provider where ProvID=?");
  $sProvider->execute($ProvID);
  my $rProvider = $sProvider->fetchrow_hashref;
  if ( $rProvider->{LName} eq '' ) { $code++; $msg .= " Primary Provider LName is NULL! "; }
  if ( $rProvider->{FName} eq '' ) { $code++; $msg .= " Primary Provider FName is NULL! "; }
  if ( $rProvider->{SSN} eq '' ) { $code++; $msg .= " Primary Provider SSN is NULL! "; }
  $sProvider->finish();
  return($code,$msg);
}
# need SCID, ContLogDate, ContLogBegTime, ContLogEndTime
# with TrID then return IncAmt/AmtDue (also BillDate from in/NoteTrans)
sub getServiceCode
{
  my ($self,$form,$SCID,$ContDate,$BegTime,$EndTime,$TrID,$BillDate) = @_;
#warn qq|getServiceCode: SCID=$SCID, ContDate=$ContDate, BegTime=$BegTime, EndTime=$EndTime, TrID=$TrID, BillDate=$BillDate\n|;
  return() unless ( $SCID );
  return() unless ( $ContDate );

  my $dbh = myDBI->dbconnect($form->{'DBNAME'});
  my $q = qq|select xSC.*, xSCRates.*, xInsurance.Descr as InsDescr, xInsurance.Name as InsName,xInsurance.InsCode, xInsurance.Email as InsEmail from xSC left join xInsurance on xInsurance.ID=xSC.InsID left join xSCRates on xSCRates.SCID=xSC.SCID where xSC.SCID='${SCID}' and xSCRates.EffDate<='${ContDate}'  and ('${ContDate}'<=xSCRates.ExpDate or xSCRates.ExpDate is null) |;
  my $s = $dbh->prepare($q);
  $s->execute() || $form->dberror($q);
  my $rxSC = $s->fetchrow_hashref;
  if ( !$rxSC->{SCID} )       # at least get the Number/Name...
  {
    $q = qq|select xSC.*, xInsurance.Descr as InsDescr, xInsurance.Name as InsName ,xInsurance.InsCode, xInsurance.Email as InsEmail from xSC left join xInsurance on xInsurance.ID=xSC.InsID where xSC.SCID = ${SCID}|;
    $s = $dbh->prepare($q);
    $s->execute() || $form->dberror($q);
    $rxSC = $s->fetchrow_hashref;
    $rxSC->{InsDescr} .= ' (NO RATES!)';
  }
  $s->finish();
  my $Duration = DBUtil->getDuration($BegTime,$EndTime);
  my $Units = 0;
  if ( $rxSC->{UnitLbl} eq 'Each' )
  { $Units = 1; }
  elsif ( $rxSC->{UnitLbl} eq 'NonBill' || $rxSC->{HrsPerUnit} == 0 )
  { $Units = 0; }
  elsif ( $rxSC->{UnitLbl} eq 'Hour' )
  { $Units = $Duration / 3600 / $rxSC->{HrsPerUnit}; }
  elsif ( $rxSC->{UnitLbl} eq 'Minutes' )
  { $Units = $Duration / 60; }
  else
  { $Units = int(($Duration / 3600 / $rxSC->{HrsPerUnit}) + .5); }
#warn qq|getServiceCode: Units=$Units, Duration=$Duration\n|;
##was chop 6/7/2005  { $Units = int($Duration / 3600 / $rxSC->{HrsPerUnit}); }
  $rxSC->{Duration} = $Duration;
  $rxSC->{Units} = sprintf("%.2f", $Units);
  $rxSC->{BillAmt} = sprintf("%.2f", $rxSC->{Units} * $rxSC->{ServiceRate});
#warn qq|getServiceCode: Units=${Units} $rxSC->{Units}, ServiceRate=$rxSC->{ServiceRate}\n|;
  if ( $TrID )
  {
    my $sTreatment = $dbh->prepare("select BilledAmt,IncAmt,SchAmt,AmtDue from Treatment where TrID=?");
    $sTreatment->execute($TrID) || $form->dberror("getServiceCode: select Treatment (${TrID})");
    my ($BilledAmt,$IncAmt,$SchAmt,$AmtDue) = $sTreatment->fetchrow_array;
    $sTreatment->finish();
    $rxSC->{IncAmt} = sprintf("%.2f", $IncAmt);
    $rxSC->{SchAmt} = sprintf("%.2f", $SchAmt);
    $rxSC->{RecAmt} = sprintf("%.2f", $IncAmt + $SchAmt);
  }
# Paid more than owed: nothing owed
  if ( $rxSC->{RecAmt} > $rxSC->{BillAmt} ) { $rxSC->{AmtDue} = 0.00; }
# Recouped more than billed: (trans: +25,-35)=-10 paid) then 25-(-10) = 35 owed
  else { $rxSC->{AmtDue} = sprintf("%.2f", $rxSC->{BillAmt} - abs($rxSC->{RecAmt})); }
  $rxSC->{AmtDue} = 0 if ( $rxSC->{AmtDue} < 0 );
#warn qq|TrID=$TrID,Duration=$Duration, Units=$Units,$rxSC->{Units},$rxSC->{ServiceRate}, BillAmt=$rxSC->{BillAmt},$rxSC->{AmtDue}\n|;
  return($rxSC);
}
sub CheckInsurance
{
  my ($self,$form,$ClientID,$InsID,$InDate) = @_;
  return(1,'No ClientID! ') unless ( $ClientID );
  return(1,'No Insurance found! ') unless ( $InsID );
  return(1,'No Date! ') unless ( $InDate );

  my ($code, $msg) = (0,'');
  if ( my $rInsurance = $self->getInsurance($form,$ClientID,$InsID,$InDate) )
  {
    if ( $rInsurance->{InsIDNum} eq '' ) { $code = 1; $msg = "InsNum is NULL! "; }
    if ( $rInsurance->{InsDescr} =~ /medicaid/i )
    {
#warn qq|InsIDNum=$rInsurance->{InsIDNum}=\n|;
      if ( $rInsurance->{InsIDNum} !~ /^B\d{8}$/ && $rInsurance->{InsIDNum} !~ /^\d{9}$/ )
      { $code = 1; $msg = "InsNum MUST BE 9 digits or B followed by 8 digits! "; }
    }
  }
  else { $code = 1; $msg = "Client Insurance not found around ${InDate}! Check Client Insurance Effective Date is before Note Contact Date. "; }
  return($code,$msg);
}
sub CheckContract
{
  my ($self,$form,$ClinicID,$InsID,$ProvID,$ClientID,$InDate) = @_;
#warn qq|CheckContract: ClinicID=${ClinicID}, InsID=$InsID, ProvID=$ProvID, ClientID=$ClientID\n|;
  return(1,'No Clinic given! ') unless ( $ClinicID );
  return(1,'No Insurance given! ') unless ( $InsID );
  my ($code, $msg) = (0,'');
  my ($chkcode, $chkmsg) = (0,'');
  my $dbh = myDBI->dbconnect($form->{'DBNAME'});
  my $qContracts = qq|
select Contracts.*, Clinic.Name as ClinicName, Clinic.ProvID as ClinicID, Control.NPI
      ,xInsurance.Descr as InsDescr, xInsurance.Name as InsName
  from Contracts
    left join Provider as Clinic on Clinic.ProvID=Contracts.ProvID
    left join ProviderControl as Control on Control.ProvID=Contracts.ProvID
    left join xInsurance on xInsurance.ID=Contracts.InsID
  where Contracts.ProvID=${ClinicID} and Contracts.InsID=${InsID}
|;
#warn qq|qContracts=\n$qContracts\n| if ( $form->{'LOGINPROVID'} == 91 );
  my $sContracts = $dbh->prepare($qContracts);
  $sContracts->execute() || $form->dberror($qContracts);
  if ( $rContracts = $sContracts->fetchrow_hashref )
  {
    unless ( $rContracts->{BillFlag} ) { $code++; $msg .= "Contract not set to BILL! "; }

#   Use the Agency as the BillTo/PayTo Provider Address? (not the incoming Clinic?)
    my $UseClinicID = $rContracts->{UseAgency} ? MgrTree->getAgency($form,$ClinicID) : $ClinicID;
    my $sProvider=$dbh->prepare("select * from Provider where ProvID=?");
    $sProvider->execute($UseClinicID);
    my $rProvider = $sProvider->fetchrow_hashref;
    (my $ZIP = $rProvider->{Zip}) =~ s/[- ]//g;
    if ( length($ZIP) < 9 ) { $code++; $msg .= "Contract Zip NOT Zip+4! "; }

    # Check for valid Client Referring Physician...
    if ( $rContracts->{UseReferring} )
    {
      my $s = $dbh->prepare("select RefPhysNPI from ClientReferrals where ClientID='${ClientID}'");
      $s->execute() || $self->dberror("CheckContract: ERROR: select RefPhysNPI (${ClientID}");
      my ($NPI) = $s->fetchrow_array;
      $s->finish();
#warn qq|CheckClient: NPI=${NPI}, Referring\n| if ( $form->{'LOGINPROVID'} == 91 );
      ($chkcode,$chkmsg) = $self->CheckNPI($form,$NPI,'Referring Physician');
      if ( $chkcode && $chkmsg ) { $msg .= $chkmsg; $code++; } elsif ( $chkmsg ) { $msg .= $chkmsg; }
    }

    # Check for valid Client Rendering Provider...
    if ( $rContracts->{UseRendering} )
    {
      # use the Designated Provider or the in Provider (note provider)...
      my $rInsurance = $self->getInsurance($form,$ClientID,$InsID,$InDate);
      my $UseProvID = $rInsurance->{DesigProvID} ? $rInsurance->{DesigProvID} : $ProvID;
      ($chkcode,$chkmsg) = $self->CheckCredentials($form,$UseProvID,$InsID,$rContracts->{NPI});
      if ( $chkcode && $chkmsg ) { $msg .= $chkmsg; $code++; } elsif ( $chkmsg ) { $msg .= $chkmsg; }
    }

    # Check for valid Client Service Facility...
    if ( $rContracts->{UseSFacility} )
    {
      my $s = $dbh->prepare("select FacIDNPI,Residence from ClientRelations where ClientID='${ClientID}'");
      $s->execute() || $self->dberror("CheckContract: ERROR: select FacIDNPI (${ClientID}");
      my ($NPI,$Residence) = $s->fetchrow_array;
#warn qq|CheckClient: NPI=${NPI}, Residence=$Residence\n| if ( $form->{'LOGINPROVID'} == 91 );
      $s->finish();
      my $ResCDC = DBA->getxref($form,'xResidence',$Residence,'CDC');
      if ( $ResCDC =~ /F|G/ )
      {
        ($chkcode,$chkmsg) = $self->CheckNPI($form,$NPI,'Service Facility');
        if ( $chkcode && $chkmsg ) { $msg .= $chkmsg; $code++; } elsif ( $chkmsg ) { $msg .= $chkmsg; }
      }
    }
    $sProvider->finish();
  }
  else { $code++; $msg .= "Contract for Insurance not found (${InsID})! "; }
  $sContracts->finish();
  return($code,$msg);
}
sub CheckCredentials
{
  my ($self,$form,$ProvID,$InsID,$ClinicNPI) = @_;
#warn qq|CheckCredentials: ProvID=${ProvID}, InsID=$InsID, ClinicNPI=$ClinicNPI\n|;
  my ($code, $msg) = (0,'');
  my $dbh = myDBI->dbconnect($form->{'DBNAME'});
  my $sProvider=$dbh->prepare("select Provider.ProvID,Provider.LName,Provider.FName,Provider.SSN,ProviderControl.NPI from Provider left join ProviderControl on ProviderControl.ProvID=Provider.ProvID where Provider.ProvID=?");
  $sProvider->execute($ProvID);
  my $rProvider = $sProvider->fetchrow_hashref;
  if ( $rProvider->{LName} eq '' ) { $code++; $msg.='Provider LName is NULL! '; }
  if ( $rProvider->{FName} eq '' ) { $code++; $msg.='Provider FName is NULL! '; }
  if ( $rProvider->{SSN} eq '' ) { $code++; $msg.='Provider SSN is NULL! '; }
  if ( $rProvider->{NPI} eq '' ) { $code++; $msg.='Provider NPI is NULL! '; }
#my $e = $rProvider->{NPI} eq $ClinicNPI ? 'ERROR>> YES!' : '';
#warn qq|$rProvider->{NPI}, $ClinicNPI ${e}\n|;

  my $sCredentials = $dbh->prepare("select Credentials.* from Credentials left join okmis_config.xCredentials on xCredentials.ID=Credentials.CredID where ProvID=? and InsID=? order by Credentials.Rank");
  $sCredentials->execute($ProvID,$InsID);
  my $rCredentials = $sCredentials->fetchrow_hashref;
  if ( $rCredentials->{Taxonomy} eq '' ) { $code++; $msg.='Provider Credential Taxonomy is NULL! '; }
  if ( $code ) { $msg .= qq| $rProvider->{FName} $rProvider->{LName} ($ProvID) |; }
  $sCredentials->finish();
  $sProvider->finish();

  return($code,$msg);
}
sub CheckNPI
{
  my ($self,$form,$NPI,$Type) = @_;
#warn qq|NPI=$NPI\n| if ( $form->{'LOGINPROVID'} == 91 );
  my ($code, $msg) = (0,'');
  my $dbh = myDBI->dbconnect($form->{'DBNAME'});
  my $rxNPI = DBA->selxref($form,'xNPI','NPI',$NPI);
  if ( $rxNPI->{'NPI'} ne '' )
  {
    if ( $Type =~ /physician/i )
    {
      if ( $rxNPI->{ProvLastName} eq '' ) { $msg .= qq|${Type} LName is NULL! |; $code=1; }
      if ( $rxNPI->{ProvFirstName} eq '' ) { $msg .= qq|${Type} FName is NULL! |; $code=1; }
    }
    else
    {
      if ( $rxNPI->{ProvOrgName} eq '' ) { $msg .= qq|${Type} NPI ProvOrgName is NULL! |; $code=1; }
      if ( $rxNPI->{Addr1} eq '' ) { $msg .= qq|${Type} NPI Address is NULL! |; $code=1; }
      if ( $rxNPI->{City} eq '' ) { $msg .= qq|${Type} NPI City is NULL! |; $code=1; }
      if ( $rxNPI->{ST} eq '' ) { $msg .= qq|${Type} NPI State is NULL! |; $code=1; }
      if ( $rxNPI->{Zip} eq '' ) { $msg .= qq|${Type} NPI Zip is NULL! |; $code=1; }
      #if ( length($rxNPI->{Zip}) < 9 ) { $msg .= qq|${Type} NPI Zip NOT +4! |; $code=1; }
    }
  }
  else { $msg .= qq|${Type} NPI is Missing! ($NPI)|; $code=1; }
  return($code,$msg);
}
sub CheckProblems
{
  my ($self,$form,$ClientID,$TrID) = @_;
#warn qq|CheckProblems: ClientID=$ClientID, TrID=$TrID\n|;
  return(1,'No ClientID! ') unless ( $ClientID );
  return(0,'') if ( $ClientID < 10 );    # ODMH and NONID Clients
  return(0,'') unless ( $TrID );

  my ($code, $msg) = (0,'');
  my $dbh = myDBI->dbconnect($form->{'DBNAME'});
  my $sCheckF = $dbh->prepare("
select Treatment.TrID
 from ClientNoteProblems 
  left join Treatment on Treatment.TrID = ClientNoteProblems.TrID
  left join okmis_config.misICD10 on misICD10.ID = ClientNoteProblems.UUID
 where Treatment.TrID = ? and misICD10.ICD10 LIKE 'F%'
");
  my $sClientNoteProblems = $dbh->prepare("
select ClientNoteProblems.ID,ClientNoteProblems.TrID,xSC.SCNum,xSC.InsID,xInsurance.InsType
 from ClientNoteProblems
  left join Treatment on Treatment.TrID = ClientNoteProblems.TrID
  left join xSC on xSC.SCID = Treatment.SCID
  left join xInsurance on xInsurance.ID = xSC.InsID
 where ClientNoteProblems.TrID=?
");
  $sClientNoteProblems->execute($TrID) || $form->dberror("CheckNoteProblems: select ClientNoteProblems ($TrID)");
  my $rClientNoteProblems = $sClientNoteProblems->fetchrow_hashref;
#foreach my $f ( sort keys %{$rClientNoteProblems} ) { warn "CheckProblems: CNP-${f}=$rClientNoteProblems->{$f}\n"; }
  return(0,'') unless ( $rClientNoteProblems->{InsType} eq 'public' );
  return(0,'') if ( substr($rClientNoteProblems->{SCNum},0,1) eq 'X' );
  my $rows = $sClientNoteProblems->rows;
#warn qq|CheckProblems: TrID=$TrID, rows=$rows\n|;
  if ( $rows )
  {
    $sCheckF->execute($TrID) || $form->dberror("CheckNoteProblems: select ClientNoteProblems ($TrID) for F");
    my $Fs = $sCheckF->rows;
#warn qq|CheckProblems: TrID=$TrID, Fs=$Fs\n|;
    unless ( $Fs )
    { $code = 1; $msg = qq|NO Mental Health Problems Addressed on Note, please check at least 1 ICD10 starting with F!|; }
  }
  $sClientNoteProblems->finish();
  $sCheckF->finish();
  return($code,$msg);
}
sub CheckAuth()
{
  my ($self,$form,$ClientID,$InsID,$InDate,$SCID) = @_;

  my ($code, $msg) = (0,'');
#warn qq|ClientID=$ClientID,InsID=$InsID,InDate=$InDate,SCID=$SCID\n|;
  if ( my $rPrAuth = $self->getAuth($form,$ClientID,$InsID,$InDate) )
  {
    my $MatchSCID = 0;
#warn qq|ID=$rPrAuth->{ID}, PAgroup=$rPrAuth->{PAgroup}, SCID=$SCID\n|;
#foreach my $f ( sort keys %{$rPrAuth} ) { warn "CheckAuth: ${f}=$rPrAuth->{$f}\n"; }
    if ( $rPrAuth->{PAgroup} )
    { $MatchSCID = Inv->chkSCIDinPA($form,$rPrAuth->{PAgroup},$SCID); }
    else
# FIX FIX FIX - not passing note to chkRVUSC!!!
    { $MatchSCID = Inv->chkRVUSC($form,$rPrAuth->{ID},$SCID); }
#warn qq|MatchSCID=$MatchSCID\n|;

    if ( !$MatchSCID ) { $msg .= 'NO Prior Authorization for Service Code. '; }
    elsif ( $rPrAuth->{PAnumber} eq '' ) { $msg .= 'Prior Authorization Number is NULL. '; }
    elsif ( $rPrAuth->{InsDescr} != /medicaid/i && $rPrAuth->{InsDescr} ne 'medicare' ) { $code = 0; }
    elsif ( $rPrAuth->{PAnumber} =~ /^\d{10}$/ ) { $code = 0; }
    elsif ( $rPrAuth->{PAnumber} =~ /^(PB|MC)\d{8}$/ ) { $code = 0; }   # DDSD waiver
    elsif ( $rPrAuth->{PAnumber} eq 'APPROVED' ) { $code = 0; }
    elsif ( $rPrAuth->{PAnumber} eq 'AUTOAUTH' ) { $code = 0; }
    elsif ( $rPrAuth->{PAnumber} =~ /^multiple$/i ) { $code = 0; }
    else { $code = 1; $msg .= 'Prior Authorization NOT valid! '; }
  }
  else { $msg = 'Prior Authorization not found. '; }
  return($code,$msg);
}
sub CheckDiag()
{
  my ($self,$form,$ClientID,$InsID,$InDate) = @_;

  my ($code, $msg) = (0,'');
  if ( my $rPDDiag = $self->getDiag($form,$ClientID,$InsID,$InDate) )
  {
    my $tAxis1ACode = DBA->getxref($form,'xAxis1',$rPDDiag->{Axis1ACode},'ICD9');
    if ( $tAxis1ACode eq '' ) { $msg .= 'Missing Diagnosis code. '; }
    elsif ( $tAxis1ACode !~ /^(?:[vVmM]\d{2}|\d{3})\.?\d{0,3}$/ )
    { $code = 1; $msg .= "1: Diagnosis 1A Code format error! ($rPDDiag->{Axis1ACode}: =${tAxis1ACode}=)"; }
    elsif ( $rPDDiag->{access} =~ /notfordate/i ) { $msg .= 'Diagnosis record not for Contact Date. '; }
    elsif ( $rPDDiag->{access} =~ /default/i ) { $msg .= 'Default Diagnosis record. '; }
    $code = 0 unless ( $rPDDiag->{InsDescr} =~ /medicaid/i );
  }
  else { $msg .= 'Diagnosis not found. '; }
  return($code,$msg);
}
sub getInsurance
{
  my ($self,$form,$ClientID,$InsID,$InDate) = @_;
  return('') unless ( $ClientID );
  return('') unless ( $InsID );
  return('') unless ( $InDate );
  my $InsPriority = $InsID =~ /primary/ ? qq| and Insurance.Priority=1 |
                  : $InsID =~ /secondary/ ? qq| and Insurance.Priority=2 |
                  : $InsID =~ /tertiary/ ? qq| and Insurance.Priority=3 |
                  : qq| and Insurance.InsID='${InsID}' |;

#warn qq|getInsurance: InsPriority=$InsPriority\n|;
  my $dbh = myDBI->dbconnect($form->{'DBNAME'});
  my $qInsurance = qq|
select Insurance.*,xInsurance.Descr as InsDescr from Insurance 
  left join xInsurance on xInsurance.ID=Insurance.InsID 
  where ClientID='${ClientID}'
    ${InsPriority}
    and Insurance.InsNumEffDate<='${InDate}'
    and ('${InDate}'<=Insurance.InsNumExpDate or Insurance.InsNumExpDate is null)
  order by Priority
|;
  my $sInsurance = $dbh->prepare($qInsurance);
  $sInsurance->execute() || $form->dberror($qInsurance);
  my $rInsurance = $sInsurance->fetchrow_hashref;
  $sInsurance->finish();
  return($rInsurance);
}
sub getAuth
{
  my ($self,$form,$ClientID,$InsID,$InDate) = @_;
  return('') unless ( $ClientID && $InsID && InDate );
  my $dbh = myDBI->dbconnect($form->{'DBNAME'});
  my $qPrAuth = qq|
select ClientPrAuth.*,xInsurance.Descr as InsDescr from ClientPrAuth
  left join Insurance on Insurance.InsNumID=ClientPrAuth.InsuranceID
  left join xInsurance on xInsurance.ID=Insurance.InsID
  where ClientPrAuth.ClientID='${ClientID}'
    and '${InDate}' between ClientPrAuth.EffDate and ClientPrAuth.ExpDate 
    and Insurance.InsID='${InsID}'
  order by ClientPrAuth.EffDate desc, ClientPrAuth.ExpDate desc
|;
  my $sPrAuth = $dbh->prepare($qPrAuth);
  $sPrAuth->execute() || $form->dberror($qPrAuth);
  my $rPrAuth = $sPrAuth->fetchrow_hashref;
  $sPrAuth->finish();
  return($rPrAuth);
}
sub getDiag()
{
  my ($self,$form,$ClientID,$InsID,$InDate) = @_;
  return('') unless ( $ClientID && $InsID && InDate );
  my $rPDDiag = ();
  my $dbh = myDBI->dbconnect($form->{'DBNAME'});
  my $qPDDiag = qq|
select PDDiag.*,xInsurance.Descr as InsDescr from PDDiag 
  left join ClientPrAuth on ClientPrAuth.ID=PDDiag.PrAuthID
  left join Insurance on Insurance.InsNumID=ClientPrAuth.InsuranceID
  left join xInsurance on xInsurance.ID=Insurance.InsID
  where PDDiag.ClientID='${ClientID}'
    and Insurance.InsID='${InsID}'
    and '${InDate}' between ClientPrAuth.EffDate and ClientPrAuth.ExpDate
  order by ClientPrAuth.EffDate desc
|;
  my $sPDDiag = $dbh->prepare($qPDDiag);
  $sPDDiag->execute() || $form->dberror($qPDDiag);
  if ( $rPDDiag = $sPDDiag->fetchrow_hashref ) { $rPDDiag->{access} = 'ok'; }
  else
  {
    $qPDDiag = qq|
select PDDiag.*,xInsurance.Descr as InsDescr from PDDiag 
  left join ClientPrAuth on ClientPrAuth.ID=PDDiag.PrAuthID
  left join Insurance on Insurance.InsNumID=ClientPrAuth.InsuranceID
  left join xInsurance on xInsurance.ID=Insurance.InsID
  where PDDiag.ClientID='${ClientID}'
  order by ClientPrAuth.EffDate desc
|;
    $sPDDiag = $dbh->prepare($qPDDiag);
    $sPDDiag->execute() || $form->dberror($qPDDiag);
    if ( $rPDDiag = $sPDDiag->fetchrow_hashref ) { $rPDDiag->{access} = 'notfordate'; }
    else
    {
      $rPDDiag->{'Axis1ACode'} = 390;       # V71.09
      $rPDDiag->{'access'} = 'default';
    }
  }
  $sPDDiag->finish();
  return($rPDDiag);
}
#############################################################################
# Calculation routines
##
sub getBillDate()
{
  my ($self) = @_;
  my @Time = localtime();
#   Time[6] makes it all rotate around Sunday before moving to the next cycle.
  my $Monday = 1 - $Time[6];
  my $THISBILLDATE = DBUtil->Date('',0,$Monday);
  my $NEXTBILLDATE = DBUtil->Date('',0,$Monday+7);
  return($THISBILLDATE,$NEXTBILLDATE);
}
##
# 2 week pay cycle beginning Friday, 1/2/2004 - Thursday 1/15/2004 and every 2 weeks after.
##
sub getPayDates()
{
  my ($self,$form,$ENDDOW,$DIC,$SD) = @_;
  my $enddow = $ENDDOW eq '' ? 4 : $ENDDOW;        # end on    4=Thursday.
  my $daysincycle = $DIC eq '' ? 14 : $DIC;        # duration 14=2 weeks.
  my $backup = -($daysincycle-1);                  # days to backup (-1 for start date).
  my $enddate = $SD ? $SD : DBUtil->Date('',0,-1); # start backup from ...
  my $startdate = $enddate;                        # both start out same.
  if ( $daysincycle == 30 )
  { ($startdate,$enddate) = DBUtil->Date($SD,'monthly',-1); }
  else
  {
    my $dow = DBUtil->Date($enddate,'dow');
    my $cnt = 0;
    until ( $dow == $enddow )
    {
      $cnt--;
      $dow = $dow == 0 ? 6 : $dow-1;
    }
    $enddate = DBUtil->Date($enddate,0,$cnt);        # found end of pay cycle
    $startdate = DBUtil->Date($enddate,0,$backup);
  }
  return($startdate,$enddate);
}
### DELETE
sub isPayDay()
{
  my ($self, $Type, $SDate, $CDate) = @_;
  my $StartDate = $SDate ? $SDate : '2004-01-02';
  my $CheckDate = $CDate ? $CDate : DBUtil->Date();
  my $flg = 0;
  if ( $Type =~ /bi-monthly/i )
  {
    my $year = substr($CheckDate,0,4);
    my $mon = substr($CheckDate,5,2);
    my $day = substr($CheckDate,8,2);
    my $max = 30;
    $max = DBUtil->daysInMonth($year,$mon) if ( $mon == 2 );
    $flg = $day == 15 || $day == $max ? 1 : 0;
  }
  elsif ( $Type =~ /bi-weekly/i )
  {
    $flg = 0;
    my $days = DBUtil->Date($CheckDate,'diff',$StartDate);
    $flg = $days/14 == int($days/14) ? 1 : 0;
  }
  elsif ( $Type =~ /monthly/i )
  {
    my $payday = substr($StartDate,8,2);
    my $day = substr($CheckDate,8,2);
    $flg = $day == $payday ? 1 : 0;
  }
  elsif ( $Type =~ /weekly/i )
  {
    my $days = DBUtil->Date($CheckDate,'diff',$StartDate);
    $flg = $days/7 == int($days/7) ? 1 : 0;
  }
  return($flg);
}
### DELETE
sub getPayCycle()
{
  my ($self, $SDate, $CDate) = @_;
  my $StartDate = $SDate ? $SDate : '2004-01-02';
  my $CheckDate = $CDate ? $CDate : 'today';
  my $days = DBUtil->Date($CheckDate,'diff',$StartDate);    # Friday
  my $weeks = int($days / 7);
# 1 = odd number of whole weeks past. 0 = even number of whole weeks past.
  my $odd = $weeks/2 == int($weeks/2) ? 0 : 1;
  return($odd);
}
sub getAmtDue
{
  my ($self, $form, $ClientID, $TrID) = @_;
  my $AmtDue = 0;
  my $dbh = myDBI->dbconnect($form->{'DBNAME'});
  my $q = qq|select AmtDue from Treatment where AmtDue > 0 |;
  $q .= qq| and TrID=${TrID} | if ( $TrID );
  $q .= qq| and ClientID=${ClientID} | if ( $ClientID );
  $q .= qq| order by ContLogDate|;
  my $s = $dbh->prepare($q);
  $s->execute();
  while ( my $r = $s->fetchrow_hashref ) { $AmtDue += $r->{AmtDue}; }
  $s->finish();
  $AmtDue = sprintf("%.2f",$AmtDue);
  return($AmtDue);
}
#############################################################################
1;
