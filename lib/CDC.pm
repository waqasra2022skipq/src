package CDC;
use DBA;
use SysAccess;
use myDBI;
use DBUtil;
use TLevel;
use CGI::Carp qw(fatalsToBrowser);
#############################################################################
###
# REMEMBER: add field to ...ORDER and hashed arrays.
#   AND TO  CDC.cgi html <<<table_fld_1>>> just to OPENTABLES
###
my @CDCORDER = ('CDCOK','OrgID','AgencySite','NPI','TransType','TransDate','TransTime','ServiceFocus','FamilyID','InsIDNum','DateOfBirth','Gend','FirstName','MaidenName','LastName','Addr1','City','CountyofRes','State','Zip','CurrentResidence','PriReferralType','PriReferralNPI','SecReferralType','SecReferralNPI','LevelOfCare','Problem1','Problem2','Problem3','LivingSituation','EmplStat','EmplType','MarStat','LangEnglish','LangOther','Education','InSchool','LegalStatus','CommitmentCounty','SelfHelp30','AbsentSchool','SuspendedSchool','AbsentDayCare','Arrested12','Arrested30','RestrictivePlacement','SelfHarm','CAR1','CAR2','CAR3','CAR4','CAR5','CAR6','CAR7','CAR8','CAR9','Harmfulintent');
my %CDC = (
  'CDCOK'       => { 'TRANSTYPE'=>'21', },
  'OrgID'       => { 'TRANSTYPE'=>'21','REQ'=>'0','CHG' => "NOT-HERE", },
  'AgencySite'  => { 'TRANSTYPE'=>'21','REQ'=>'1','CHG' => "NOT-HERE", },
  'NPI'         => { 'TRANSTYPE'=>'21','REQ'=>'1','CHG' => "NOT-HERE", },
  'TransType'   => { 'TRANSTYPE'=>'21','REQ'=>'1', },
  'TransDate'   => { 'TRANSTYPE'=>'21','REQ'=>'1','FIELDNAME'=>'Transaction Date', },
  'TransTime'   => { 'TRANSTYPE'=>'21','REQ'=>'1','FIELDNAME'=>'Transaction Time', },
  'ServiceFocus'=> { 'TRANSTYPE'=>'21','REQ'=>'1', },
  'FamilyID'    => { 'TRANSTYPE'=>'21','FIELDNAME'=>'FamilyID/Case Number', },
  'InsIDNum'    => { 'TRANSTYPE'=>'21','REQ'=>'1','CHG' => "NOT-HERE",'FIELDNAME'=>'Insurance ID', },
  'DateOfBirth' => { 'TRANSTYPE'=>'21','REQ'=>'1', },
  'Gend'        => { 'TRANSTYPE'=>'21','REQ'=>'1','FIELDNAME'=>'Gender', },
  'FirstName'   => { 'TRANSTYPE'=>'21','REQ'=>'1', },
  'MaidenName'  => { 'TRANSTYPE'=>'21', },
  'LastName'    => { 'TRANSTYPE'=>'21','REQ'=>'1', },
  'Addr1'       => { 'TRANSTYPE'=>'21','REQ'=>'1', },
  'City'        => { 'TRANSTYPE'=>'21','REQ'=>'1', },
  'CountyofRes' => { 'TRANSTYPE'=>'21','REQ'=>'1', },
  'State'       => { 'TRANSTYPE'=>'21','REQ'=>'1', },
  'Zip'         => { 'TRANSTYPE'=>'21','REQ'=>'1', },
  'CurrentResidence' => { 'TRANSTYPE'=>'21','REQ'=>'1','FIELDNAME'=>'Client Residence', },
  'PriReferralType'  => { 'TRANSTYPE'=>'21','REQ'=>'1','FIELDNAME'=>'Primary Referral Type', },
  'PriReferralNPI'   => { 'TRANSTYPE'=>'21','FIELDNAME'=>'Primary Referral', },
  'SecReferralType'  => { 'TRANSTYPE'=>'21','FIELDNAME'=>'Secondary Referral Type', },
  'SecReferralNPI'   => { 'TRANSTYPE'=>'21','FIELDNAME'=>'Secondary Referral', },
  'LevelOfCare' => { 'TRANSTYPE'=>'23','REQ'=>'1', },
  'Problem1'    => { 'TRANSTYPE'=>'23','REQ'=>'1','FIELDNAME'=>'Primary Problem', },
  'Problem2'    => { 'TRANSTYPE'=>'23','FIELDNAME'=>'Secondary Problem', },
  'Problem3'    => { 'TRANSTYPE'=>'23','FIELDNAME'=>'Tertiary Problem', },
  'LivingSituation'  => { 'TRANSTYPE'=>'23','REQ'=>'1', },
  'EmplStat'    => { 'TRANSTYPE'=>'23','REQ'=>'1','FIELDNAME'=>'Employee Status', },
  'EmplType'    => { 'TRANSTYPE'=>'23','REQ'=>'1','FIELDNAME'=>'Employee Type', },
  'MarStat'     => { 'TRANSTYPE'=>'23','REQ'=>'1','FIELDNAME'=>'Married Status', },
  'LangEnglish' => { 'TRANSTYPE'=>'23','FIELDNAME'=>'Does the client speak english?', },
  'LangOther'   => { 'TRANSTYPE'=>'23','FIELDNAME'=>'Primary Language', },
  'Education'   => { 'TRANSTYPE'=>'23','FIELDNAME'=>'School Grade', },
  'LegalStatus' => { 'TRANSTYPE'=>'23','REQ'=>'1','FIELDNAME'=>'Legal Status', },
  'CommitmentCounty' => { 'TRANSTYPE'=>'23', },
  'SelfHelp30'  => { 'TRANSTYPE'=>'23','REQ'=>'1','FIELDNAME'=>'past 30 days selfhelp support group', },
  'AbsentSchool'=> { 'TRANSTYPE'=>'23','REQ'=>'1','FIELDNAME'=>'past 30 days Absent School','AGELT'=>'18', },
  'SuspendedSchool'  => { 'TRANSTYPE'=>'23','REQ'=>'1','FIELDNAME'=>'past 30 days Suspended School','AGELT'=>'18', },
  'AbsentDayCare'    => { 'TRANSTYPE'=>'23','REQ'=>'1','FIELDNAME'=>'past 90 days Absent Day Care','AGELT'=>'18', },
  'Arrested12'  => { 'TRANSTYPE'=>'23','FIELDNAME'=>'Arrests past 12 months', },
  'Arrested30'  => { 'TRANSTYPE'=>'23','FIELDNAME'=>'Arrest past 30 days', },
  'RestrictivePlacement'=> { 'TRANSTYPE'=>'23','REQ'=>'1','FIELDNAME'=>'past 90 days # restrictive placements','AGELT'=>'18', },
  'SelfHarm'    => { 'TRANSTYPE'=>'23','REQ'=>'1','FIELDNAME'=>'past 90 days # incidents of self harm','AGELT'=>'18', },
  'CAR1'        => { 'TRANSTYPE'=>'23','FIELDNAME'=>'Feeling/Mood', },
  'CAR2'        => { 'TRANSTYPE'=>'23','FIELDNAME'=>'Thinking/Mental', },
  'CAR3'        => { 'TRANSTYPE'=>'23','FIELDNAME'=>'Substance Abuse', },
  'CAR4'        => { 'TRANSTYPE'=>'23','FIELDNAME'=>'Medical/Physical', },
  'CAR5'        => { 'TRANSTYPE'=>'23','FIELDNAME'=>'Family', },
  'CAR6'        => { 'TRANSTYPE'=>'23','FIELDNAME'=>'Interpersonal', },
  'CAR7'        => { 'TRANSTYPE'=>'23','FIELDNAME'=>'Role Performance', },
  'CAR8'        => { 'TRANSTYPE'=>'23','FIELDNAME'=>'Socio-Legal', },
  'CAR9'        => { 'TRANSTYPE'=>'23','FIELDNAME'=>'Self-Care/Basic Needs', },
  'Harmfulintent'=> { 'TRANSTYPE'=>'23','FIELDNAME'=>'Harmful Intent','AGELT'=>'18', },
);
my $EdErrorMsg = '';
#############################################################################
sub setPA
{
  my ($self,$form,$PrAuthID) = @_;
  return('NOT enabled!') unless ( SysAccess->getRule($form,'EnableCDC') );
  return('NO PrAuthID!') unless ($PrAuthID);
  return("Prior Auth LOCKED!") if ( $self->isLocked($form,$PrAuthID) );

# check for 23 yet...if not set this one to 23...
  $self->hasAdmission($form,$PrAuthID);

# read both PrAuth and CDC...
  my $dbh = myDBI->dbconnect($form->{'DBNAME'});
# separate because we update separately...
  my $sPrAuth = $dbh->prepare("select * from ClientPrAuth where ID=?");
  $sPrAuth->execute($PrAuthID) || myDBI->dberror("setPA: $PrAuthID");
  my $rPrAuth = $sPrAuth->fetchrow_hashref;
  my $sPrAuthCDC = $dbh->prepare("select * from ClientPrAuthCDC where ClientPrAuthID=?");
  $sPrAuthCDC->execute($PrAuthID) || myDBI->dberror("setPA: $PrAuthID");
  my $rPrAuthCDC = $sPrAuthCDC->fetchrow_hashref;
  $sPrAuth->finish();
  $sPrAuthCDC->finish();
#warn qq|setPA: Fail=$rPrAuthCDC->{Fail}\nReason=$rPrAuthCDC->{Reason}\n|;

# set some global vars...
  my $ClientID = $rPrAuth->{'ClientID'};
  my $InsuranceID = $rPrAuth->{'InsuranceID'};
# which Clinic and Insurance? (Primary or Designated Provider?)
  my $sInsurance = $dbh->prepare("select Client.clinicClinicID,Insurance.InsID,Insurance.InsIDNum,Client.ProvID,Insurance.DesigProvID from Insurance left join Client on Client.ClientID=Insurance.ClientID where Insurance.InsNumID=?" );
  $sInsurance->execute($InsuranceID) || myDBI->dberror("setPA: select InsID/Clinic ($InsuranceID)");
  my ($ClinicID,$InsID,$InsIDNum,$PrimaryProvID,$DesigProvID) = $sInsurance->fetchrow_array();
  $sInsurance->finish();

# set the Prior Auth fields...
  $rPrAuth->{'TL'} = TLevel->getTL($form,$ClientID,'18',$PrAuthID);
  $rPrAuth->{'PAgroup'} = $self->calcPG($form,$ClientID,$InsID,$PrAuthID);
  my ($months,$days) = DBA->calcLOS($form,$InsID,$rPrAuth->{'PAgroup'});
  $rPrAuth->{'LOS'} = $months;       # FIX get rid of LOS because it is only months FIX
  $rPrAuth->{'ExpDate'} = DBUtil->Date($rPrAuth->{'EffDate'},$months,$days);
  $rPrAuth->{'ReqType'} = DBA->setPrAuthReqType($form,$ClientID);  # ServiceFocus?
  $rPrAuth = $self->setPADiag($form,$rPrAuth);
  $rPrAuth->{'SOGSGSI'} = $self->calcSOGS($form,$ClientID);
#warn qq|setPA: Create=$rPrAuth->{CreateProvID}/$rPrAuth->{CreateDate},Change=$rPrAuth->{ChangeProvID}\n|;
  my $PAFail = $self->passfailPA($form,$InsID,$rPrAuth,$rPrAuthCDC);
#warn qq|setPA: PAFail=${PAFail}\n|;

# set the CDC fields...
  $rPrAuthCDC->{InsIDNum} = $InsIDNum;
  my $UseProvID = $DesigProvID ? $DesigProvID : $PrimaryProvID;
  $rPrAuthCDC = $self->setCDC($form,$ClinicID,$InsID,$UseProvID,$rPrAuth,$rPrAuthCDC);
  $rPrAuthCDC = $self->setCDCClient($form,$ClientID,$rPrAuthCDC);
  my $sClientDevl = $dbh->prepare("select * from ClientDevl where ClientID=?");
  $sClientDevl->execute($ClientID) || myDBI->dberror("setPA: ClientDevl: ${ClientID}");
  my $rClientDevl = $sClientDevl->fetchrow_hashref;
  $sClientDevl->finish();
  $rPrAuthCDC = $self->setCDCDisability($form,$ClientID,$rPrAuthCDC,$rClientDevl,'Handicap1','Handicap2','Handicap3','Handicap4');
  my $sPDDom = $dbh->prepare("select * from PDDom where PrAuthID=?");
  $sPDDom->execute($PrAuthID) || myDBI->dberror("setPA: PDDom: ${PrAuthID}");
  my $rPDDom = $sPDDom->fetchrow_hashref;
  $sPDDom->finish();
  $rPrAuthCDC = $self->setCDCCars($form,$ClientID,$rPrAuthCDC,$rPDDom);
  $rPrAuthCDC = $self->setCDCDrug($form,$ClientID,$rPrAuthCDC);
#foreach my $f ( sort keys %{$rPrAuthCDC} ) { warn "setPA: BEFORE: rPrAuthCDC-$f=$rPrAuthCDC->{$f}\n"; }
  $rPrAuthCDC = $self->setCDCASI($form,$ClientID,$rPrAuthCDC);
#foreach my $f ( sort keys %{$rPrAuthCDC} ) { warn "setPA: AFTER: rPrAuthCDC-$f=$rPrAuthCDC->{$f}\n"; }
  $rPrAuthCDC = $self->setCDCTASI($form,$ClientID,$rPrAuthCDC);
  my $CDCFail = $self->passfailCDC($form,$InsID,$rPrAuthCDC);
#warn qq|setPA: CDCFail=${CDCFail}\n|;

# Failed???
  my $Fail = $PAFail eq '' && $CDCFail eq '' ? ''
           : $PAFail eq '' ? " CDC issues: ".$CDCFail
           : "PA issues: ".$PAFail." CDC issues: ".$CDCFail;
#warn qq|setPA: Fail=${Fail}\n|;

  $rPrAuth->{'ChangeProvID'} = $form->{'LOGINPROVID'};
  my $PID = DBA->doUpdate($form,'ClientPrAuth',$rPrAuth,"ID='$PrAuthID'");

# set PrAuthCDC fields...
#  $rPrAuthCDC->{Status} = 'New';
#  $rPrAuthCDC->{StatusDate} = $form->{TODAY};
  $rPrAuthCDC->{'Fail'} = $Fail;     
#  $rPrAuthCDC->{CreateProvID} = $form->{LOGINPROVID};
#  $rPrAuthCDC->{CreateDate} = $form->{TODAY};
  $rPrAuthCDC->{'ChangeProvID'} = $form->{'LOGINPROVID'};
  my $CID = DBA->doUpdate($form,'ClientPrAuthCDC',$rPrAuthCDC,"ClientPrAuthID='$PrAuthID'");
#  DBA->setAlert($form,"$ClientID: $Fail") if ( $Fail ne '' && $sendflg );
#warn qq|END UPDATE PA: Fail=${Fail}\n|;
  return($Fail);
}
sub setPADiag
{
  my ($self,$form,$rPA) = @_;
  my $ClientID = $rPA->{'ClientID'};
#foreach my $f ( sort keys %{$rPA} ) { warn "setPADiag: BEFORE: rPA-$f=$rPA->{$f}\n"; }
  $rPA->{'Diag1Prim'} = '';
  $rPA->{'Diag1Sec'} = '';
  $rPA->{'Diag1Tert'} = '';
  $rPA->{'Diag2Prim'} = '';
  $rPA->{'Diag2Sec'} = '';
  my $cnt = 0;
  my $dbh = myDBI->dbconnect($form->{'DBNAME'});
  my $sClientProblems=$dbh->prepare("select ClientProblems.UUID,ClientProblems.Priority,misICD10.ICD10 from ClientProblems left join okmis_config.misICD10 on misICD10.ID=ClientProblems.UUID where ClientID=? and misICD10.ICD10 LIKE 'F%' order by ClientProblems.Priority");
  $sClientProblems->execute($ClientID) || myDBI->dberror("setPADiag: select ClientProblems ${ClientID}");
  while ( $rClientProblems = $sClientProblems->fetchrow_hashref )
  {
    my $ICD10 = $rClientProblems->{'ICD10'};
    $ICD10 =~ s/\.//g;                          # trim period .
    next unless ( $ICD10 =~ /^F/ );             # skip non-MH Diagnosis
    $cnt++;
    if    ( $cnt == 1 ) { $rPA->{'Diag1Prim'} = $ICD10; }
    elsif ( $cnt == 2 ) { $rPA->{'Diag1Sec'} = $ICD10; }
    elsif ( $cnt == 3 ) { $rPA->{'Diag1Tert'} = $ICD10; }
    elsif ( $cnt == 4 ) { $rPA->{'Diag2Prim'} = $ICD10; }
    elsif ( $cnt == 5 ) { $rPA->{'Diag2Sec'} = $ICD10; }
  }
#foreach my $f ( sort keys %{$rPA} ) { warn "setPADiag: AFTER: rPA-$f=$rPA->{$f}\n"; }
  return($rPA);
}
sub calcSOGS
{
  my ($self,$form,$ClientID) = @_;
# set SOGS score for PA...
  my $dbh = myDBI->dbconnect($form->{'DBNAME'});
  my $sSOGS = $dbh->prepare("select TotalScore from SOGS where ClientID=? order by TransDate desc");
  $sSOGS->execute($ClientID) || myDBI->dberror("setPA: select SOGS ${ClientID}");
  my ($TotalScore) = $sSOGS->fetchrow_array();
  $sSOGS->finish();
  return($TotalScore);
}
sub calcACE
{
  my ($self,$form,$ClientID) = @_;
# set ACE score for PA...
  my $Score = '';
  my $dbh = myDBI->dbconnect($form->{'DBNAME'});
  my $sClientACE = $dbh->prepare("select * from ClientACE where ClientID=? order by TestDate desc");
  $sClientACE->execute($ClientID) || myDBI->dberror("setPA: select ClientACE ${ClientID}");
  if ( my $rClientACE = $sClientACE->fetchrow_hashref )
  {
    my $TotalScore = $rClientACE->{'q1'}
                   + $rClientACE->{'q2'} 
                   + $rClientACE->{'q3'} 
                   + $rClientACE->{'q4'} 
                   + $rClientACE->{'q5'} 
                   + $rClientACE->{'q6'} 
                   + $rClientACE->{'q7'} 
                   + $rClientACE->{'q8'} 
                   + $rClientACE->{'q9'} 
                   + $rClientACE->{'q10'};
    $Score = $TotalScore == 10 ? 10 : '0'.$TotalScore;
  }
  $sClientACE->finish();
  return($Score);
}
#####################################################################
sub setDIS
{
  my ($self,$form,$DischargeID) = @_;
#warn qq|ENTER UPDATE DIS: DischargeID=$DischargeID\n|;
  return('NOT enabled!') unless ( SysAccess->getRule($form,'EnableCDC') );
  return('NO DischargeID!') unless ($DischargeID);

# read both Discharge and CDC...
  my $dbh = myDBI->dbconnect($form->{'DBNAME'});
# separate because we update separately...
  my $sDischarge = $dbh->prepare("select * from ClientDischarge where ID=?");
  $sDischarge->execute($DischargeID) || myDBI->dberror("setDIS: $DischargeID");
  my $rDischarge = $sDischarge->fetchrow_hashref;

  return("Discharge LOCKED!") if ( $rDischarge->{'Locked'} );

  ##$CDC{'Problem1'}{'REQ'} = 0;
  my $sDischargeCDC = $dbh->prepare("select * from ClientDischargeCDC where ClientDischargeCDC.ClientDischargeID=?");
  $sDischargeCDC->execute($DischargeID) || myDBI->dberror("setDIS: select ClientDischargeCDC ($DischargeID)");
  my $rDischargeCDC = $sDischargeCDC->fetchrow_hashref;
  $sDischarge->finish();
  $sDischargeCDC->finish();
#warn qq|setDIS: InsuranceID=$rDischarge->{InsuranceID}\n|;

# set some global vars...
  my $ClientID = $rDischarge->{'ClientID'};
  my $InsuranceID = $rDischarge->{'InsuranceID'};
# which Clinic and Insurance? (Primary or Designated Provider?) Primary Insurance only
  my $sInsurance = $dbh->prepare("select Client.clinicClinicID,Insurance.InsID,Insurance.InsIDNum,Client.ProvID,Insurance.DesigProvID from Insurance left join Client on Client.ClientID=Insurance.ClientID left join xInsurance on xInsurance.ID=Insurance.InsID where Insurance.InsNumID=?" );
  $sInsurance->execute($InsuranceID) || myDBI->dberror("setDIS: select InsID/Clinic");
  my ($ClinicID,$InsID,$InsIDNum,$PrimaryProvID,$DesigProvID) = $sInsurance->fetchrow_array();
  $sInsurance->finish();
#warn qq|setDIS: ClinicID=$ClinicID,InsID=$InsID,InsIDNum=$InsIDNum,PrimaryProvID=$PrimaryProvID,DesigProvID=$DesigProvID\n|;

# set Discharge fields...
# set CDC fields...
  my $UseProvID = $DesigProvID ? $DesigProvID : $PrimaryProvID;
  $rDischargeCDC->{InsIDNum} = $InsIDNum;
  $rDischargeCDC = $self->setCDC($form,$ClinicID,$InsID,$UseProvID,$rPrAuth,$rDischargeCDC);
  $rDischargeCDC = $self->setCDCClient($form,$ClientID,$rDischargeCDC);
  $rDischargeCDC = $self->setCDCDisability($form,$ClientID,$rDischargeCDC,$rDischarge,'Axis3ACode','Axis3BCode','Axis3CCode','Axis3DCode');
  $rDischargeCDC = $self->setCDCCars($form,$ClientID,$rDischargeCDC,$rDischarge);
  $rDischargeCDC = $self->setCDCDrug($form,$ClientID,$rDischargeCDC);
  $rDischargeCDC = $self->setCDCASI($form,$ClientID,$rDischargeCDC);
  $rDischargeCDC = $self->setCDCTASI($form,$ClientID,$rDischargeCDC);
  $rDischargeCDC->{ACEScore} = '';
  ## not needed $rDischargeCDC->{ACEScore} = $self->calcACE($form,$ClientID);     # rollup latest ClientACE score 1-10
#foreach my $f ( sort keys %{$rPrAuthCDC} ) { warn "setPA: AFTER: rPrAuthCDC-$f=$rPrAuthCDC->{$f}\n"; }
  my $CDCFail = $self->passfailCDC($form,$InsID,$rDischargeCDC);
  $rDischargeCDC->{'Fail'} = $CDCFail;     
#  $rDischargeCDC->{Status} = $Status;
#  $rDischargeCDC->{StatusDate} = $form->{TODAY};
  $rDischargeCDC->{'ChangeProvID'} = $form->{'LOGINPROVID'};
  my $CID = DBA->doUpdate($form,'ClientDischargeCDC',$rDischargeCDC,"ClientDischargeID='$DischargeID'");
#  DBA->setAlert($form,"$ClientID: $CDCFail") if ( $CDCFail ne '' && $sendflg );
#warn qq|END UPDATE DIS: CDCFail=${CDCFail}\n|;
  return($CDCFail);
}
#####################################################################
sub setCDC
{
  my ($self,$form,$ClinicID,$InsID,$UseProvID,$rPrAuth,$rCDC) = @_;
#foreach my $f ( sort keys %{$rCDC} ) { warn "setCDC: BEGIN: rCDC-$f=$rCDC->{$f}\n"; }
  my $ClientID = $rCDC->{'ClientID'};
#warn qq|setCDC: ClientID=$ClientID, TL=$rPrAuth->{TL}, ID=$rPrAuth->{ID}, CDCID=$rCDC->{ID}\n|;

  $rCDC->{ClinicID} = $ClinicID;
#warn qq|setCDC: ClinicID=$ClinicID, InsID=$InsID\n|;
  my $rContract = DBA->getContractInfo($form,$ClinicID,$InsID);
#foreach my $f ( sort keys %{$rContract} ) { warn "setCDC: rContract-$f=$rContract->{$f}\n"; }
  $rCDC->{OrgID} = $rContract->{'OrgID'};
# AgencyNum 1=Agency, 0=Individual
# AgencySite is the Agency PIN or Individual Provider PIN (sent to DMH)
  $rCDC->{AgencyNum} = 1;
  $rCDC->{AgencySite} = $rContract->{'PIN'};
  $rCDC->{NPI} = $rContract->{'NPI'};
#warn qq|setCDC: ClientID=$ClientID, Site=$rCDC->{AgencySite}, Num=$rCDC->{AgencyNum}\n|;
  if ( my $r=DBA->isIndMedicaid($form,$ClientID) )
  { $rCDC->{AgencySite} = $r->{'PIN'}; $rCDC->{'AgencyNum'} = 0; }
  #{ warn qq|setCDC: YES isIndMedicaid\n|; $rCDC->{AgencySite} = $r->{'PIN'}; $rCDC->{'AgencyNum'} = 0; }
#warn qq|setCDC: ClientID=$ClientID, Site=$rCDC->{AgencySite}, Agency=$rCDC->{AgencyNum}\n|;

  my $TL = $rPrAuth->{TL};
#warn qq|setCDC: isAdult=$isAdult, TL=$TL\n|;
  $rCDC->{ACEScore} = $self->calcACE($form,$ClientID);     # rollup latest ClientACE score 1-10
#warn qq|setCDC: ACEScore=$rCDC->{ACEScore}, ClientID=${ClientID}\n|;
  $rCDC->{SMI} = $rCDC->{Age} >= 18 ? $TL =~ /2|3|4/ ? '1' : '2' : '';
  $rCDC->{SED} = $rCDC->{Age} < 18 ? $TL =~ /2|3|4/ ? '1' : '2' : '';
#foreach my $f ( sort keys %{$rCDC} ) { warn "setCDC: END: rCDC-$f=$rCDC->{$f}\n"; }
  return($rCDC);
}
sub setCDCClient
{
  my ($self,$form,$ClientID,$rCDC) = @_;

warn qq|setCDCClient: ClientID=$ClientID\n|;
  my $dbh = myDBI->dbconnect($form->{'DBNAME'});
  my $clientHealth = $dbh->prepare("
	select ClientHealth.* from ClientHealth where ClientHealth.ClientID=? 
");
$clientHealth->execute(@ClientID) || myDBI->dberror("setCDCClient->select ClientID=$ClientID");

if ( my $ch = $clientHealth->fetchrow_hashref )
{
	warn qq|Prenatal Status: \n|;
	warn $ch->{PrenatalStatus}

}
  my $s = $dbh->prepare("
select Client.*, ClientIntake.*
     , ClientLegal.LegalStatus
     , ClientLegal.CASEID
     , ClientLegal.CommitmentCounty
     , ClientLegal.Arrest1
     , ClientLegal.Arrested
     , ClientLegal.InJail
     , ClientReferrals.ReferredBy1NPI as PrimaryReferral
     , ClientReferrals.ReferredBy1Type as PrimaryReferralType
     , ClientReferrals.ReferredBy2NPI as SecondaryReferral
     , ClientReferrals.ReferredBy2Type as SecondaryReferralType
     , ClientReferrals.Harmfulintent
     , ClientRelations.Residence
     , ClientRelations.MarStat
     , ClientRelations.LivesWith
     , ClientRelations.HomelessLong
     , ClientRelations.HomelessMany
     , ClientResources.IncomeDeps
     , ClientResources.SelfHelp30
     , ClientSocial.*, MedHx.*
     , ProviderControl.NPI 
     , ClientEmergency.Alert
     , ClientHealth.PrenatalStatus
  from Client 
    left join ClientEmergency on ClientEmergency.ClientID=Client.ClientID
    left join ClientIntake on ClientIntake.ClientID=Client.ClientID
    left join ClientLegal on ClientLegal.ClientID=Client.ClientID
    left join ClientReferrals on ClientReferrals.ClientID=Client.ClientID
    left join ClientRelations on ClientRelations.ClientID=Client.ClientID
    left join ClientResources on ClientResources.ClientID=Client.ClientID
    left join ClientHealth on ClientHealth.ClientID=Client.ClientID
    left join ClientSocial on ClientSocial.ClientID=Client.ClientID
    left join MedHx on MedHx.ClientID=Client.ClientID 
    left join ProviderControl on ProviderControl.ProvID=Client.ProvID 
  where Client.ClientID=?
");
  $s->execute($ClientID) || myDBI->dberror("setCDCClient->select ClientID=$ClientID");
  if ( my $r = $s->fetchrow_hashref )
  {
	warn qq|Prenatal Statusss: \n|;
        warn $r->{PrenatalStatus};
    # 0 neither, 1 suicidal, 2 homocidal, 3 both
    # 2 & 3 not allowed for children under the age of 8
    $rCDC->{'Harmfulintent'} = $r->{'Harmfulintent'} eq '1' ? 1
                             : $r->{'Harmfulintent'} eq '2' ? 2
                             : $r->{'Harmfulintent'} eq '3' ? 3
                             : 0;
    
    if ( $rCDC->{Age} < 8 )
    {
      $rCDC->{'Harmfulintent'} = 0; 
    }
#foreach my $f ( sort keys %{$r} ) { warn "setCDCClient: r-$f=$r->{$f}\n"; }
    $rCDC->{ServiceFocus} = DBA->getxref($form,'xServiceFocus',$r->{ServiceFocus},'CDC');
    $rCDC->{DateOfBirth} = $r->{'DOB'};
    $rCDC->{Age} = DBUtil->Date($r->{DOB},'age',$rCDC->{TransDate});        # Age at TransDate
#warn qq|DOB=$r->{DOB},TransDate=$TransDate,Age=$rCDC->{Age}\n|;
    $rCDC->{Gend} = $r->{Gend} eq 'F' ? '1' : '2';

    #$rCDC->{RaceWhite} = $r->{Race} eq 'C' ? '1'
    #                   : $r->{Race} eq 'H' ? '1'
    #                   : $r->{Race} eq 'M' ? '1' : '2';
    #$rCDC->{RaceIndian} = $r->{Race} eq 'I' ? '1'
    #                    : $r->{Race} eq 'E' ? '1' : '2';
    #$rCDC->{RaceAsian} = $r->{Race} eq 'A' ? '1' : '2';
    #$rCDC->{RaceBlack} = $r->{Race} eq 'B' ? '1' : '2';
    #$rCDC->{EthnicIslander} = $r->{Race} eq 'P' ? '1' : '2';
    #$rCDC->{EthnicHispanic} = $r->{Race} eq 'H' ? '1' : '2';
    my ($Race,$dummy) = split(chr(253),$r->{'Race'});
    $rCDC->{RaceWhite} = $Race eq '0000-0' || $Race eq '' ? '1' : '2';      # default to RaceWhite
    $rCDC->{RaceWhite} = $Race eq '2106-3' ? '1' : '2';
    $rCDC->{RaceIndian} = $Race eq '1002-5' ? '1' : '2';
    $rCDC->{RaceAsian} = $Race eq '2028-9' ? '1' : '2';
    $rCDC->{RaceBlack} = $Race eq '2054-5' ? '1' : '2';
# NATIVE HAWAIIAN OR OTHER PACIFIC ISLANDER (R4 2076-8)
    $rCDC->{EthnicIslander} = $Race eq '2076-8' ? '1' : '2';
    $rCDC->{EthnicHispanic} = $r->{Ethnicity} eq '2135-2' ? '1' : '2';

    $rCDC->{Alert} = $r->{Alert};
    $rCDC->{MHScreen} = $self->setMHScreen($form,$ClientID);
    $rCDC->{SAScreen} = $self->setSAScreen($form,$ClientID);
    $rCDC->{TraumaScreen} = $self->setTRScreen($form,$ClientID);
    $rCDC->{GamblingScreen} = $self->setGAScreen($form,$ClientID);
    $rCDC->{FirstName} = $r->{FName};
    $rCDC->{MiddleName} = substr($r->{MName},0,1);
# per email 6/2/10 10:15 from Sandy.
    $rCDC->{MaidenName} = $r->{MaidenName} eq '' && $r->{Gend} eq 'F' ? $r->{LName} : $r->{MaidenName};
    $rCDC->{LastName} = $r->{LName};
    $rCDC->{Suffix} = $r->{Suffix};
    $rCDC->{Addr1} = $r->{Addr1};
    $rCDC->{Addr2} = $r->{Addr2};
    $rCDC->{City} = $r->{City};
    $rCDC->{CountyofRes} = DBA->getxref($form,'xCountyOK',$r->{County},'CDC');
    $rCDC->{State} = $r->{ST};
#warn qq|CDC: Residence=$r->{'Residence'}\n|;
    my $ResCDC = DBA->getxref($form,'xResidence',$r->{'Residence'},'CDC');
#warn qq|CDC: ResCDC=${ResCDC}\n|;
    my $ResDescr = DBA->getxref($form,'xResidence',$r->{'Residence'},'Descr');
#warn qq|CDC: ResDescr=${ResDescr}\n|;
    my $AlertHomeless = $ResCDC eq 'I' || $ResCDC eq 'J' ? '1' : '0';
    $rCDC->{Zip} = $AlertHomeless ? '99999' : $r->{Zip};

    $rCDC->{PriReferralType} = DBA->getxref($form,'xReferralTypes',$r->{PrimaryReferralType},'CDC');
    if ( $rCDC->{PriReferralType} == 40 )    # 40 = DMHSAS or OHCA funded facility
    {
      my $rxNPI = DBA->selxref($form,'xNPI','NPI',$r->{'PrimaryReferral'});
      if ( $rxNPI->{'NPI'} )
      { $rCDC->{PriReferralNPI} = $rxNPI->{NPI} unless ( $rxNPI->{Type} =~ /non-clinical/i ); }
    }
    $rCDC->{SecReferralType} = DBA->getxref($form,'xReferralTypes',$r->{SecondaryReferralType},'CDC');
    if ( $rCDC->{SecReferralType} == 40 )    # 40 = DMHSAS or OHCA funded facility
    {
      my $rxNPI = DBA->selxref($form,'xNPI','NPI',$r->{'SecondaryReferral'});
      if ( $rxNPI->{'NPI'} )
      { $rCDC->{SecReferralNPI} = $rxNPI->{NPI} unless ( $rxNPI->{Type} =~ /non-clinical/i ); }
    }

    $rCDC->{CurrentResidence} = $ResCDC;
# IncarcerationStatus: 1=Prison, 2=No, 3=Jail
    $rCDC->{'IncarcerationStatus'} = $r->{'InJail'} ? '3' : $ResDescr =~ /prison/i ? '1' : '2';
    $rCDC->{'LivingSituation'} = DBA->getxref($form,'xLivesWith',$r->{'LivesWith'},'CDC');
#warn qq|CDC: LivesWith=$r->{'LivesWith'}, $rCDC->{'LivingSituation'}\n|;
    $rCDC->{EmplStat} = DBA->getxref($form,'xEmplStat',$r->{EmplStat},'CDC');
    $rCDC->{EmplType} = DBA->getxref($form,'xEmplType',$r->{EmplType},'CDC');
##
# calculate the income & set SSI/SSDI
    my $AnnualIncome = 0;
    $rCDC->{SSI} = '2';
    $rCDC->{SSDI} = '2';
    my $qClientIncome = qq|
select * from ClientIncome where ClientID=?
    and ClientIncome.EffDate<=curdate()
    and (ClientIncome.ExpDate>=curdate() or ClientIncome.ExpDate is null)
  order by EffDate
|;
    my $sClientIncome = $dbh->prepare($qClientIncome);
    $sClientIncome->execute($ClientID);
    while ( $rClientIncome = $sClientIncome->fetchrow_hashref )
    { 
#warn qq|Src=$rClientIncome->{Src}, Amt=$rClientIncome->{Amt}\n|;
      $AnnualIncome += $rClientIncome->{Amt};
      $rCDC->{SSI} = '1' if ( $rClientIncome->{Src} eq 'S' );
      $rCDC->{SSDI} = '1' if ( $rClientIncome->{Src} eq 'D' );
    }
    $rCDC->{AnnualIncome} = DBUtil->FmtStr(int($AnnualIncome),6,'R',0);
    $rCDC->{'IncomeDeps'} = $r->{'IncomeDeps'} eq '' ? '01' : DBUtil->FmtStr($r->{'IncomeDeps'},2,'R',0);    # something required
    $sClientIncome->finish();

    $rCDC->{'MarStat'} = DBA->getxref($form,'xMarStat',$r->{'MarStat'},'CDC');
#warn qq|CDC: MarStat=$r->{'MarStat'}, $rCDC->{'MarStat'}\n|;
#warn qq|Gend=$r->{Gend}, DOB=$r->{DOB}\n|;
    $rCDC->{'Pregnant'} = '';
    $rCDC->{'PregnantDate'} = '';
    if ( $r->{Gend} eq 'F' )
    {
      $rCDC->{Pregnant} = '0';
      if($r->{PrenatalStatus}){
        warn 'Pregnant Flag Value:';
        warn $r->{PrenatalStatus};
	$rCDC->{Pregnant} = $r->{PrenatalStatus};
      }
      if ( $r->{'PregnantDate'} ne '' && $r->{'PregnantDate'} ge $rCDC->{'TransDate'} )
      { $rCDC->{Pregnant} = '1'; $rCDC->{PregnantDate} = $r->{'PregnantDate'}; }
    }
#warn qq|Pregnant=$rCDC->{Pregnant}, PregnantDate=$rCDC->{PregnantDate}\n|;
##
    # MilFlag: 0=None, 1=Active, 2=Reserve, 3=Discharged, 4=Retired
    # MilitaryStatus: 1=Vetern, 2=None, 3=Active
    #$rCDC->{MilitaryStatus} = $r->{MilFlag} == 4 ? '1' : $r->{MilFlag} == 1 ? '3' : '2';
    # MilitaryStatus: A=Customer: Currently Active
    #                 B=Customer: Previously Active
    #                 C=Customer: National Guard/Reserve
    #                 D=Family Member: Currently Active
    #                 E=Family Member: Previously Active
    #                 F=Family Member: National Guard/Reserve
    #                 G=None 
    my $FamilyMilFlag = $self->setFamilyMilitaryStatus($form,$ClientID);
#warn qq|MilFlag=$r->{MilFlag}, FamilyMilFlag=${FamilyMilFlag}\n|;
    $rCDC->{MilitaryStatus} = $r->{MilFlag} == 1 ? 'A'
                            : $r->{MilFlag} == 3 || $r->{MilFlag} == 4 ? 'B'
                            : $r->{MilFlag} == 2 ? 'C'
                            : $FamilyMilFlag == 1 ? 'D'
                            : $FamilyMilFlag == 3 || $FamilyMilFlag == 4 ? 'E'
                            : $FamilyMilFlag == 2 ? 'F'
                            : 'G';
    $rCDC->{'LegalStatus'} = DBA->getxref($form,'xLegalStatus',$r->{'LegalStatus'},'CDC');

    # 01=Voluntary or 17=Protective Custody.
    $rCDC->{'CommitmentCounty'} = '';
    if ($rCDC->{'LegalStatus'} ne '01' && $rCDC->{'LegalStatus'} ne '17')
    { $rCDC->{'CommitmentCounty'} = DBA->getxref($form,'xCountyOK',$r->{'CommitmentCounty'},'CDC'); }
    $rCDC->{TobaccoUse} = DBUtil->FmtStr($r->{DailyTobaccoUse},2,'R','0');
    $rCDC->{Problem1} = DBA->getxref($form,'xProblems',$r->{Problem1},'CDC');
    $rCDC->{Problem2} = DBA->getxref($form,'xProblems',$r->{Problem2},'CDC');
    $rCDC->{Problem3} = DBA->getxref($form,'xProblems',$r->{Problem3},'CDC');
    $rCDC->{LevelOfCare} = DBA->getxref($form,'xLOC',$r->{LOC},'CDC');

# <FamilyID> (10 chars)= Family ID, Drug Court, DOC #, or DHS Case Number
#  Family ID: Nine Character Medicaid ID
#  Drug Court ID: Nine character ICIS ID (3 letters, 6 number birth date)
#  DOC Number: "DOC" then up to 7 numbers
#  DHS Case: Start with "C", "H", or "KK". KK must be 10 total, C/H don't have a limit, but 10 is probably max.
# (defined in the Required CDC fields documentation on the dmh web site.)
    if ( $rCDC->{ServiceFocus} eq '03'                # Drug Court, Drug Court # is required.
      || $rCDC->{ServiceFocus} eq '09'                # Special Problems, treatment unit, DOC# required
      || $rCDC->{PriReferralType} eq '12'             # 12 = Department Of Corrections
      || $rCDC->{PriReferralType} eq '33'             # 33 = Probation
      || $rCDC->{PriReferralType} eq '34'             # 34 = Parole
      || $rCDC->{PriReferralType} eq '49'             # 49 = TANF/child welfare, DHS# required
      || $rCDC->{Problem1} =~ /745|746|747/           # SA Dependant Child, Family ID required
      || $rCDC->{Problem2} =~ /745|746|747/           # SA Dependant Child, Family ID required
      || $rCDC->{Problem3} =~ /745|746|747/ )         # SA Dependant Child, Family ID required
    { ($rCDC->{FamilyID} = $r->{'CASEID'}) =~ s/[- ]//g; }             # all 4 in CASEID.
    $rCDC->{'Arrested30'} = DBUtil->FmtStr($r->{'Arrest1'},2,'R','0');
    $rCDC->{'Arrested12'} = DBUtil->FmtStr($r->{'Arrested'},2,'R','0');
    $rCDC->{'SelfHelp30'} = DBUtil->FmtStr($r->{'SelfHelp30'},2,'R','0');
# XXX until all Providers get their NPI.
    $rCDC->{ClinicianOfRecord} = $r->{NPI} eq '' ? $rCDC->{NPI} : $r->{NPI};

    $rCDC->{Placement} = '';
    $rCDC->{RestrictivePlacement} = '';
    $rCDC->{SelfHarm} = '';
    $rCDC->{AbsentSchool} = '';
    $rCDC->{SuspendedSchool} = '';
    $rCDC->{AbsentDayCare} = '';
    


    if ( $rCDC->{Age} < 18 )
    {
# Placement types...
# 1 Not in out-of-home treatment
# 2 Residential treatment
# 3 Specialized community group home
# 4 Foster home
# 5 Group home
# 6 Other
# Residence CDC: G=NH, H=Institutional Setting, I/J=Homeless
      $rCDC->{Placement} = $ResDescr =~ /residential care facility/i ? '2'
                         : $ResDescr =~ /specialized community group home/i ? '3'
                         : $ResDescr =~ /foster/i ? '4'
                         : $ResDescr =~ /group home/i ? '5' : '1';
      $rCDC->{RestrictivePlacement} = DBUtil->FmtStr($r->{RestrictivePlacement},2,'R','0');
      $rCDC->{SelfHarm} = DBUtil->FmtStr($r->{SelfHarm},2,'R','0');
# '99' is Not applicable.
      $rCDC->{AbsentSchool} = $r->{AbsentSchool} eq '' ? '99' : DBUtil->FmtStr($r->{AbsentSchool},2,'R','0');
      $rCDC->{SuspendedSchool} = $r->{SuspendedSchool} eq '' ? '99' : DBUtil->FmtStr($r->{SuspendedSchool},2,'R','0');
      $rCDC->{AbsentDayCare} = $r->{AbsentDayCare} eq '' ? '99' : DBUtil->FmtStr($r->{AbsentDayCare},2,'R','0');
    }
    $rCDC->{'AlertCHomeless'} = $r->{'HomelessLong'} == 1 || $r->{'HomelessMany'} == 1 ? '1' : '2';
#warn qq|CDC: HomelessMany=$r->{'HomelessMany'}, HomelessLong=$r->{'HomelessLong'}, $rCDC->{'AlertCHomeless'}\n|;

#-----------------------------------------------------------------------------
#     REMOVED...
#     ALTERED...
#     set PreferredLanguage (LangOther), English (LangEnglish) only if LangOther not English(0)...
#warn qq|CHECK Lang: PreLang=$r->{PreLang}, SpeakEnglish=$r->{SpeakEnglish}\n|;
      $rCDC->{LangOther} = DBA->getxref($form,'xLanguages',$r->{PreLang},'CDC');
      $rCDC->{LangEnglish} = $rCDC->{LangOther} == 0 ? '' : $r->{'SpeakEnglish'} ? '1' : '2';
#warn qq|CHECK Lang: LangOther=$rCDC->{LangOther}, LangEnglish=$rCDC->{LangEnglish}\n|;
      $rCDC->{InSchool} = $r->{SchoolLast3} == 1 ? '1' : '2';
      my $sClientEducation = $dbh->prepare("select * from ClientEducation where ClientID=?");
      $sClientEducation->execute($ClientID) || myDBI->dberror("setCDCClient->select ClientEducation ClientID=${ClientID}");
      my $rClientEducation = $sClientEducation->fetchrow_hashref;
#warn qq|CHECK Education: ClientID=${ClientID}, Age=$rCDC->{Age}, SchoolLast3=$r->{SchoolLast3}\n|;
#warn qq|CHECK Education: CurrentGrade=$rClientEducation->{CurrentGrade}, SchoolGrade=$rClientEducation->{SchoolGrade}\n|;
      $rCDC->{Education} = $rCDC->{Age} < 5
                         ? '00'
                         : $r->{SchoolLast3}
                           ? DBA->getxref($form,'xSchoolGrades',$rClientEducation->{CurrentGrade},'CDC')
                           : DBA->getxref($form,'xSchoolGrades',$rClientEducation->{SchoolGrade},'CDC');
      $EdErrorMsg = $r->{SchoolLast3} ? qq|Missing: What grade are you currently attending?| : qq|Missing: What is the highest grade in school you have satisfactorily completed?|;
#warn qq|CHECK Education: Education=$rCDC->{Education}\n|;
      $sClientEducation->finish();
      $rCDC->{Email} = $r->{'Email'};
#     if the trauma screen is given, regardless if positive or negative
#       a provider can give the CATS score for kids (3-17) 0-60 are the valid entries
#       a provider can give the PCL5 score for adults (18+) 0-80 are the valid entries
#warn qq|set traumaScore...Age=$rCDC->{Age}\n|;
      $rCDC->{traumaScore} = $rCDC->{Age} >= 3 && $rCDC->{Age} <= 17
                           ? $self->setCATS($form,$ClientID,$rCDC)
                           : $rCDC->{Age} >= 18
                             ? $self->setPCL5($form,$ClientID,$rCDC)
                             : '';
  }
  $s->finish();
  return($rCDC);
}
# next 4 subs calulate: 1=Positive, 2=Negative, 3=Not Administered
sub setMHScreen
{
  my ($self,$form,$ClientID) = @_;
  my $dbh = myDBI->dbconnect($form->{'DBNAME'});
  my $s = $dbh->prepare("select * from MentalStat where ClientID=?");
  $s->execute($ClientID) || myDBI->dberror("setMHScreen: select MentalStat $ClientID");
  my $r = $s->fetchrow_hashref;
  my $value = $r->{'MentalExam'} eq '' ? 3 : $r->{'MentalExam'} ? 1 : 2;
#warn qq|setMAScreen: value=$value, ClientID=$ClientID, $r->{'MentalExam'}\n|;
  $s->finish();
  return($value);
}
sub setSAScreen   # CRAFFT
{
  my ($self,$form,$ClientID) = @_;
  my $dbh = myDBI->dbconnect($form->{'DBNAME'});
  my $s = $dbh->prepare("select * from ClientCRAFFT where ClientID=? and TestDate is not null order by TestDate desc");
  $s->execute($ClientID) || myDBI->dberror("setSAScreen: select ClientCRAFFT ${ClientID}");
  my $r = $s->fetchrow_hashref;
  my ($value,$score) = (3,0);
  $score += 1 if ( $r->{'q1'} );
  $score += 1 if ( $r->{'q2'} );
  $score += 1 if ( $r->{'q3'} );
  $score += 1 if ( $r->{'q4'} );
  $score += 1 if ( $r->{'q5'} );
  $score += 1 if ( $r->{'q6'} );
  if ( $r->{'q1'} eq ''
    && $r->{'q2'}  eq ''
    && $r->{'q3'}  eq ''
    && $r->{'q4'}  eq ''
    && $r->{'q5'}  eq ''
    && $r->{'q6'} eq '' )
  { $value = 3; }
  else { $value = $score >= 2 ? 1 : 2; }
#warn qq|setSAScreen: value=$value, ClientID=$ClientID, score=$score, $r->{'q1'}, $r->{'q5'}\n|;
  $s->finish();
  return($value);
}
sub setTRScreen
{
  my ($self,$form,$ClientID) = @_;
  my $dbh = myDBI->dbconnect($form->{'DBNAME'});
  my $s = $dbh->prepare("select * from IES where ClientID=?");
  $s->execute($ClientID) || myDBI->dberror("setTRScreen: select IES $ClientID");
  my $r = $s->fetchrow_hashref;
  my $value = $r->{'Score'} == 0 ? 3 : $r->{'Score'} > 31 ? 1 : 2;
#warn qq|setTRScreen: value=$value, ClientID=$ClientID, $r->{'Score'}\n|;
  $s->finish();
  return($value);
}
sub setGAScreen
{
  my ($self,$form,$ClientID) = @_;
  my $dbh = myDBI->dbconnect($form->{'DBNAME'});
  my $s = $dbh->prepare("select * from Gambling where ClientID=?");
  $s->execute($ClientID) || myDBI->dberror("setGAScreen: select Gambling $ClientID");
  my $r = $s->fetchrow_hashref;
  my $value = $r->{'History'} == 0 ? 3
                 : $r->{'Anxious'}
                || $r->{'KeepFrom'}
                || $r->{'FinHelp'} ? 1
                                   : 2;
#warn qq|setGAScreen: value=$value, ClientID=$ClientID, $r->{'History'}, $r->{'Anxious'}, $r->{'KeepFrom'}, $r->{'FinHelp'}\n|;
  $s->finish();
  return($value);
}
sub setCDCDisability
{
  my ($self,$form,$ClientID,$rCDC,$rDiag,$h1,$h2,$h3,$h4) = @_;
#warn qq|setCDCDisability: ClientID=$ClientID\n|;
#foreach my $f ( sort keys %{$rDiag} ) { warn "setCDCDisability: rDiag-$f=$rDiag->{$f}\n"; }
##  CHECK: Handicap may not be needed for new CDC???
#warn qq|setCDCDisability: $rDiag->{ID}\n|;
    my $tmp = DBA->getxref($form,'xHandicap',$rDiag->{$h1},'CDC');
    $rCDC->{Handicap1} = $tmp eq '' ? '01' : $tmp;
    if ( $rCDC->{Handicap1} eq '01' )
    { $rCDC->{Handicap2} = ''; $rCDC->{Handicap3} = ''; $rCDC->{Handicap4} = ''; }
    else
    {
      $tmp = DBA->getxref($form,'xHandicap',$rDiag->{$h2},'CDC');
      $rCDC->{Handicap2} = $tmp eq '' ? '' : $tmp;
      if ( $rCDC->{Handicap2} eq '01' )
      { $rCDC->{Handicap3} = ''; $rCDC->{Handicap4} = ''; }
      else
      {
        $tmp = DBA->getxref($form,'xHandicap',$rDiag->{$h3},'CDC');
        $rCDC->{Handicap3} = $tmp eq '' ? '  ' : $tmp;
        if ( $rCDC->{Handicap3} eq '01' ) { $rCDC->{Handicap4} = ''; }
        else
        {
          $tmp = DBA->getxref($form,'xHandicap',$rDiag->{$h4},'CDC');
          $rCDC->{Handicap4} = $tmp eq '' ? '  ' : $tmp;
        }
      }
    }
  return($rCDC);
}
sub setCDCCars
{
  my ($self,$form,$ClientID,$rCDC,$rCARS) = @_;
#warn qq|setCDCCars: ClientID=$ClientID, CAR1=$rCARS->{Dom1Score}\n|;
  $rCDC->{CAR1}=$rCARS->{Dom1Score} eq '' ? '99' : DBUtil->FmtStr($rCARS->{Dom1Score},2,'R','0');
  $rCDC->{CAR2}=$rCARS->{Dom2Score} eq '' ? '99' : DBUtil->FmtStr($rCARS->{Dom2Score},2,'R','0');
  $rCDC->{CAR3}=$rCARS->{Dom3Score} eq '' ? '99' : DBUtil->FmtStr($rCARS->{Dom3Score},2,'R','0');
  $rCDC->{CAR4}=$rCARS->{Dom4Score} eq '' ? '99' : DBUtil->FmtStr($rCARS->{Dom4Score},2,'R','0');
  $rCDC->{CAR5}=$rCARS->{Dom5Score} eq '' ? '99' : DBUtil->FmtStr($rCARS->{Dom5Score},2,'R','0');
  $rCDC->{CAR6}=$rCARS->{Dom6Score} eq '' ? '99' : DBUtil->FmtStr($rCARS->{Dom6Score},2,'R','0');
  $rCDC->{CAR7}=$rCARS->{Dom7Score} eq '' ? '99' : DBUtil->FmtStr($rCARS->{Dom7Score},2,'R','0');
  $rCDC->{CAR8}=$rCARS->{Dom8Score} eq '' ? '99' : DBUtil->FmtStr($rCARS->{Dom8Score},2,'R','0');
  $rCDC->{CAR9}=$rCARS->{Dom9Score} eq '' ? '99' : DBUtil->FmtStr($rCARS->{Dom9Score},2,'R','0');
  return($rCDC);
}
sub setCDCDrug
{
  my ($self,$form,$ClientID,$rCDC) = @_;
#warn qq|setCDCDrug: ClientID=$ClientID\n|;
  my $dbh = myDBI->dbconnect($form->{'DBNAME'});
  my $cnt = 0;
  $rCDC->{Drug1} = '';
  $rCDC->{Route1} = '';
  $rCDC->{Freq1} = '';
  $rCDC->{Age1} = '';
  $rCDC->{Drug2} = '';
  $rCDC->{Route2} = '';
  $rCDC->{Freq2} = '';
  $rCDC->{Age2} = '';
  $rCDC->{Drug3} = '';
  $rCDC->{Route3} = '';
  $rCDC->{Freq3} = '';
  $rCDC->{Age3} = '';
  my $s = $dbh->prepare("select * from SAbuse where SAbuse.ClientID=? and SAbuse.EffDate<=curdate() and (SAbuse.ExpDate>=curdate() or SAbuse.ExpDate is null) order by Priority, FromDate");
  $s->execute($ClientID) || myDBI->dberror("setCDCDrug->select ClientID=$ClientID");
  while ( my $r = $s->fetchrow_hashref )
  {
#warn qq|setCDCDrug: Drug=$r->{Drug}, Route=$r->{Method}, Freq=$r->{Freq}, Age=$r->{Age}\n|;
    my $Drug = DBA->getxref($form,'xDrugs',$r->{Drug},'Descr');
    next if ( $Drug eq 'Nicotine' );
    $cnt++;
    if ( $cnt == 1 )
    {
      $rCDC->{Drug1} = DBA->getxref($form,'xDrugs',$r->{Drug},'CDC');
      unless ( $Drug =~ /none/i || $Drug =~ /unknown/i )
      {
        $rCDC->{Route1} = DBA->getxref($form,'xMethods',$r->{Method},'CDC');
        $rCDC->{Freq1} = DBA->getxref($form,'xFreqs',$r->{Freq},'CDC');
        $rCDC->{Age1} = DBUtil->FmtStr($r->{Age},2,'R','0');
      }
#warn qq|setCDCDrug: Drug1=$rCDC->{Drug1}, Route1=$rCDC->{Route1}, Freq1=$rCDC->{Freq1}, Age1=$rCDC->{Age1}\n|;
    }
    elsif ( $cnt == 2 )
    {
      $rCDC->{Drug2} = DBA->getxref($form,'xDrugs',$r->{Drug},'CDC');
      unless ( $Drug =~ /none/i || $Drug =~ /unknown/i )
      {
        $rCDC->{Route2} = DBA->getxref($form,'xMethods',$r->{Method},'CDC');
        $rCDC->{Freq2} = DBA->getxref($form,'xFreqs',$r->{Freq},'CDC');
        $rCDC->{Age2} = DBUtil->FmtStr($r->{Age},2,'R','0');
      }
    }
    elsif ( $cnt == 3 )
    {
      $rCDC->{Drug3} = DBA->getxref($form,'xDrugs',$r->{Drug},'CDC');
      unless ( $Drug =~ /none/i || $Drug =~ /unknown/i )
      {
        $rCDC->{Route3} = DBA->getxref($form,'xMethods',$r->{Method},'CDC');
        $rCDC->{Freq3} = DBA->getxref($form,'xFreqs',$r->{Freq},'CDC');
        $rCDC->{Age3} = DBUtil->FmtStr($r->{Age},2,'R','0');
      }
    }
  }
  $s->finish();
  $rCDC->{Drug1} = '01' if ( $cnt == 0 );
  return($rCDC);
}
sub setCDCASI
{
  my ($self,$form,$ClientID,$rCDC) = @_;
#warn qq|setCDCASI: Age=$rCDC->{Age}\n|;
# remove the ASI first so it won't be sent into DMH.
  $rCDC->{ASIMedical} = '';
  $rCDC->{ASIEmploy} = '';
  $rCDC->{ASIAlcohol} = '';
  $rCDC->{ASIDrug} = '';
  $rCDC->{ASILegal} = '';
  $rCDC->{ASIFamily} = '';
  $rCDC->{ASIPsych} = '';
  return($rCDC) if ( $rCDC->{Age} < 18 );
  my $dbh = myDBI->dbconnect($form->{'DBNAME'});
  my $q = qq|select SPMedical,SPEmpSup,SPAlcohol,SPDrugs,SPLegal,SPFamily,SPPsych from ClientASI where G1='$ClientID' and G5 is not null order by G5 desc|;
#warn qq|ASI: q=$q|;
  my $s = $dbh->prepare($q);
  $s->execute() || $self->dberror($q);
  my ($SPMedical,$SPEmpSup,$SPAlcohol,$SPDrugs,$SPLegal,$SPFamily,$SPPsych) = $s->fetchrow_array;
  $rCDC->{ASIMedical} = $SPMedical eq '' ? '9' : $SPMedical;
  $rCDC->{ASIEmploy} = $SPEmpSup eq '' ? '9' : $SPEmpSup;
  $rCDC->{ASIAlcohol} = $SPAlcohol eq '' ? '9' : $SPAlcohol;
  $rCDC->{ASIDrug} = $SPDrugs eq '' ? '9' : $SPDrugs;
  $rCDC->{ASILegal} = $SPLegal eq '' ? '9' : $SPLegal;
  $rCDC->{ASIFamily} = $SPFamily eq '' ? '9' : $SPFamily;
  $rCDC->{ASIPsych} = $SPPsych eq '' ? '9' : $SPPsych;
  $s->finish();
  return($rCDC);
}
sub setCDCTASI
{
  my ($self,$form,$ClientID,$rCDC) = @_;
#warn qq|setCDCTASI: Age=$rCDC->{Age}\n|;
# remove the TASI first so it won't be sent into DMH.
  $rCDC->{TASIChemical} = '';
  $rCDC->{TASISchool} = '';
  $rCDC->{TASIEmploy} = '';
  $rCDC->{TASIFamily} = '';
  $rCDC->{TASIPeer} = '';
  $rCDC->{TASILegal} = '';
  $rCDC->{TASIPsych} = '';
  return($rCDC) if ( $rCDC->{Age} <= 11 || $rCDC->{Age} >= 18 );
  my $dbh = myDBI->dbconnect($form->{'DBNAME'});
  my $q = qq|select SPChemical,SPSchool,SPEmpSup,SPFamily,SPPeerSoc,SPLegal,SPPsych from ClientTASI where ClientID='$ClientID' and AdmDate is not null order by AdmDate desc|;
#warn qq|TASI: q=$q|;
  my $s = $dbh->prepare($q);
  $s->execute() || $self->dberror($q);
  my ($SPChemical,$SPSchool,$SPEmpSup,$SPFamily,$SPPeerSoc,$SPLegal,$SPPsych) = $s->fetchrow_array;
#warn qq|TASI: SPChemical=$SPChemical,SPSchool=$SPSchool,SPEmpSup=$SPEmpSup,SPFamily=$SPFamily,SPPeerSoc=$SPPeerSoc,SPLegal=$SPLegal,SPPsych=$SPPsych|;
  $rCDC->{TASIChemical} = $SPChemical eq '' ? '9' : $SPChemical;
  $rCDC->{TASISchool} = $SPSchool eq '' ? '9' : $SPSchool;
  $rCDC->{TASIEmploy} = $SPEmpSup eq '' ? '9' : $SPEmpSup;
  $rCDC->{TASIFamily} = $SPFamily eq '' ? '9' : $SPFamily;
  $rCDC->{TASIPeer} = $SPPeerSoc eq '' ? '9' : $SPPeerSoc;
  $rCDC->{TASILegal} = $SPLegal eq '' ? '9' : $SPLegal;
  $rCDC->{TASIPsych} = $SPPsych eq '' ? '9' : $SPPsych;
  $s->finish();
  return($rCDC);
}
sub setCATS
{
  my ($self,$form,$ClientID,$rCDC) = @_;
  my $dbh = myDBI->dbconnect($form->{'DBNAME'});
  my $s = $dbh->prepare("select * from ClientCATS where ClientID=? and TestDate is not null order by TestDate desc");
  $s->execute($ClientID) || $self->dberror("setCATS: $ClientID");
  my $rPHQ = $s->fetchrow_hashref;
#foreach my $f ( sort keys %{$rPHQ} ) { warn "setCATS: form-$f=$rPHQ->{$f}\n"; }
  my $tA = $rPHQ->{'qA1'}
         + $rPHQ->{'qA2'} 
         + $rPHQ->{'qA3'} 
         + $rPHQ->{'qA4'} 
         + $rPHQ->{'qA5'} 
         + $rPHQ->{'qA6'} 
         + $rPHQ->{'qA7'} 
         + $rPHQ->{'qA8'} 
         + $rPHQ->{'qA9'} 
         + $rPHQ->{'qA10'}
         + $rPHQ->{'qA11'}
         + $rPHQ->{'qA12'}
         + $rPHQ->{'qA13'}
         + $rPHQ->{'qA14'}
         + $rPHQ->{'qA15'};
  my $tB = $rPHQ->{'qB1'}
         + $rPHQ->{'qB2'} 
         + $rPHQ->{'qB3'} 
         + $rPHQ->{'qB4'} 
         + $rPHQ->{'qB5'} 
         + $rPHQ->{'qB6'} 
         + $rPHQ->{'qB7'} 
         + $rPHQ->{'qB8'} 
         + $rPHQ->{'qB9'} 
         + $rPHQ->{'qB10'}
         + $rPHQ->{'qB11'}
         + $rPHQ->{'qB12'}
         + $rPHQ->{'qB13'}
         + $rPHQ->{'qB14'}
         + $rPHQ->{'qB15'}
         + $rPHQ->{'qB16'}
         + $rPHQ->{'qB17'}
         + $rPHQ->{'qB18'}
         + $rPHQ->{'qB19'}
         + $rPHQ->{'qB20'};
  my $tC = $rPHQ->{'qC1'}
         + $rPHQ->{'qC2'} 
         + $rPHQ->{'qC3'} 
         + $rPHQ->{'qC4'} 
         + $rPHQ->{'qC5'};
  my $score = $tB;
  $s->finish();
  return($score);
}
sub setPCL5
{
  my ($self,$form,$ClientID,$rCDC) = @_;
  my $dbh = myDBI->dbconnect($form->{'DBNAME'});
  my $s = $dbh->prepare("select * from ClientPCL5 where ClientID=? and TestDate is not null order by TestDate desc");
  $s->execute($ClientID) || $self->dberror("setPCL5: $ClientID");
  my $rPHQ = $s->fetchrow_hashref;
#foreach my $f ( sort keys %{$rPHQ} ) { warn "setPCL5: rPHQ-$f=$rPHQ->{$f}\n"; }
  my $tB = $rPHQ->{'q1'} + $rPHQ->{'q2'} + $rPHQ->{'q3'} + $rPHQ->{'q4'} + $rPHQ->{'q5'};
#warn qq|q1:$rPHQ->{'q1'} + q2:$rPHQ->{'q2'} + q3:$rPHQ->{'q3'} + q4:$rPHQ->{'q4'} + q5:$rPHQ->{'q5'} = ${tB}\n|;
  my $tC = $rPHQ->{'q6'} + $rPHQ->{'q7'};
#warn qq|q6:$rPHQ->{'q6'} + q7:$rPHQ->{'q7'} = ${tC}\n|;
  my $tD = $rPHQ->{'q8'} + $rPHQ->{'q9'} + $rPHQ->{'q10'} + $rPHQ->{'q11'} + $rPHQ->{'q12'} + $rPHQ->{'q13'} + $rPHQ->{'q14'};
#warn qq|q8:$rPHQ->{'q8'} + q9:$rPHQ->{'q9'} + q10:$rPHQ->{'q10'} + q11:$rPHQ->{'q11'} + q12:$rPHQ->{'q12'} = ${tD}\n|;
  my $tE = $rPHQ->{'q15'} + $rPHQ->{'q16'} + $rPHQ->{'q17'} + $rPHQ->{'q18'} + $rPHQ->{'q19'} + $rPHQ->{'q20'};
#warn qq|q15:$rPHQ->{'q15'} + q16:$rPHQ->{'q16'} + q17:$rPHQ->{'q17'} + q18:$rPHQ->{'q18'} + q19:$rPHQ->{'q19'} + q20:$rPHQ->{'q20'} = ${tE}\n|;
  my $score = $tB + $tC + $tD + $tE;
#warn qq|setPCL5: score=${score}, tB=${tB}, tC=${tC}, tD=${tD}, tE=${tE}\n|;
  $s->finish();
  return($score);
}
sub setFamilyMilitaryStatus
{
  my ($self,$form,$ClientID) = @_;
  my $dbh = myDBI->dbconnect($form->{'DBNAME'});
  my $MilFlag = 0;
  my $sClientFamily = $dbh->prepare("select * from ClientFamily where ClientID=? and MilFlag=1");
  $sClientFamily->execute($ClientID) || $self->dberror("setFamilyMilitaryStatus: $ClientID");
  if ( my $rClientFamily = $sClientFamily->fetchrow_hashref )
  { $MilFlag = $rClientFamily->{'MilFlag'}; }
  else
  {
    $sClientFamily = $dbh->prepare("select * from ClientFamily where ClientID=? and (MilFlag=3 || MilFlag=4)");
    $sClientFamily->execute($ClientID) || $self->dberror("setFamilyMilitaryStatus: $ClientID");
    if ( my $rClientFamily = $sClientFamily->fetchrow_hashref )
    { $MilFlag = $rClientFamily->{'MilFlag'}; }
    else
    {
      $sClientFamily = $dbh->prepare("select * from ClientFamily where ClientID=? and MilFlag=2");
      $sClientFamily->execute($ClientID) || $self->dberror("setFamilyMilitaryStatus: $ClientID");
      if ( my $rClientFamily = $sClientFamily->fetchrow_hashref )
      { $MilFlag = $rClientFamily->{'MilFlag'}; }
    }
  }
  $sClientFamily->finish();
#warn qq|setFamilyMilitaryStatus: MilFlag=${MilFlag}\n|;
  return($MilFlag);
}
# means we need to send in a CDC/PA
sub required
{
  my ($self,$form,$InsID,$PrAuthID) = @_;
#foreach my $f ( sort keys %{$form} ) { warn "required: form-$f=$form->{$f}\n"; }
  my $dbh = myDBI->dbconnect($form->{'DBNAME'});
  my $RecCDC = 0;
  if ( $InsID )
  {
    $sxInsurance = $dbh->prepare("select ReqCDC from xInsurance where ID=?");
    $sxInsurance->execute($InsID);
    ($ReqCDC) = $sxInsurance->fetchrow_array;
    $sxInsurance->finish();
  }
  elsif ( $PrAuthID )
  {
    $sxInsurance = $dbh->prepare("select xInsurance.ReqCDC from ClientPrAuth left join Insurance on Insurance.InsNumID=ClientPrAuth.InsuranceID left join xInsurance on xInsurance.ID=Insurance.InsID where ClientPrAuth.ID=?");
    $sxInsurance->execute($PrAuthID);
    ($ReqCDC) = $sxInsurance->fetchrow_array;
    $sxInsurance->finish();
  }
#warn qq|required: InsID=${InsID}, ReqCDC=${ReqCDC}\n|;
  $ReqCDC = 0 if ( $ReqCDC eq '');
  return($ReqCDC);
}
sub isLocked
{
  my ($self,$form,$PrAuthID) = @_;
#warn qq|isLocked: PrAuthID=$PrAuthID\n|;
  return(0) unless ($PrAuthID);
  my $dbh = myDBI->dbconnect($form->{'DBNAME'});
  my $sPrAuth = $dbh->prepare("select * from ClientPrAuth where ID='${PrAuthID}'");
  $sPrAuth->execute() || myDBI->dberror("isLocked ${PrAuthID}");
  my $rPrAuth = $sPrAuth->fetchrow_hashref;
#warn qq|isLocked: Locked=$rPrAuth->{'Locked'}, Status=$rPrAuth->{Status}, PAnumber=$rPrAuth->{PAnumber}\n|;
  $locked = $rPrAuth->{'Locked'};
  $sPrAuth->finish();
  return($locked);
}
sub hasAdmission
{
  my ($self,$form,$PrAuthID) = @_;
#warn qq|hasAdmission: BEGIN: PrAuthID=$PrAuthID\n|;
  return() unless ($PrAuthID);
  return() if ( $self->isLocked($form,$PrAuthID) );
  my $dbh = myDBI->dbconnect($form->{'DBNAME'});
  my $sPrAuthCDC = $dbh->prepare("select * from ClientPrAuthCDC where ClientPrAuthID='${PrAuthID}'");
  $sPrAuthCDC->execute() || myDBI->dberror("hasAdmission: select ClientPrAuthCDC=$PrAuthID");
  my $rPrAuthCDC = $sPrAuthCDC->fetchrow_hashref;
  $sPrAuthCDC->finish();
#warn qq|hasAdmission: TransType=$rPrAuthCDC->{TransType}\n|;
  return() unless ( $rPrAuthCDC->{TransType} == 40 || $rPrAuthCDC->{TransType} == 41 );
  #return() unless ( $rPrAuthCDC->{TransType} =~ /40|41|42/;

  my $sPrAuthTest = $dbh->prepare("select * from ClientPrAuth left join ClientPrAuthCDC on ClientPrAuthCDC.ClientPrAuthID=ClientPrAuth.ID where ClientPrAuth.ClientID='$rPrAuthCDC->{ClientID}' and ClientPrAuthCDC.TransType=23 and ClientPrAuth.PAnumber is not null");
  $sPrAuthTest->execute() || myDBI->dberror("hasAdmission: test for '23' ID=$PrAuthID");
  unless ( my $rPrAuthTest = $sPrAuthTest->fetchrow_hashref )
  {
#warn "hasAdmission: set to 23 (${PrAuthID}/$rPrAuthCDC->{ID})\n";
    my $sU = $dbh->prepare("update ClientPrAuthCDC set TransType='23' where ClientPrAuthID='${PrAuthID}'");
    $sU->execute() || myDBI->dberror("hasAdmission: set to '23' ClientPrAuthID=${PrAuthID}");
    $sU->finish();
  }
  $sPrAuthTest->finish();
#warn qq|hasAdmission: END: PrAuthID=$PrAuthID\n|;
  return();
}
sub calcPG
{
  my ($self,$form,$ClientID,$InsID,$PrAuthID,$forceTransType) = @_;
#warn qq|calcPG: BEGIN: ClientID=$ClientID, InsID=$InsID, PrAuthID=$PrAuthID\n|;
# only for valid Insurances...
  return() unless ( $self->required($form,$InsID) );

#warn qq|calcPG: forceTransType=$forceTransType\n|;
  my $dbh = myDBI->dbconnect($form->{'DBNAME'});
# separate select to get Age...
  my $sClient = $dbh->prepare("select Client.*,ClientIntake.ServiceFocus from Client left join ClientIntake on ClientIntake.ClientID=Client.ClientID where Client.ClientID=?");
  $sClient->execute($ClientID) || myDBI->dberror("calcPG: select Client ($ClientID)");
  my $rClient = $sClient->fetchrow_hashref();
  my $ServiceFocus = DBA->getxref($form,'xServiceFocus',$rClient->{ServiceFocus},'CDC');
  my $sPrAuth = $dbh->prepare("select ClientPrAuth.Type,ClientPrAuth.PAgroup,ClientPrAuthCDC.StatusDate,ClientPrAuthCDC.TransType,ClientPrAuthCDC.PriReferralType from ClientPrAuth left join ClientPrAuthCDC on ClientPrAuthCDC.ClientPrAuthID=ClientPrAuth.ID where ClientPrAuth.ID=?");
  $sPrAuth->execute($PrAuthID) || myDBI->dberror("calcPG: select PrAuth ($PrAuthID)");
  my ($Type,$CurPAgroup,$StatusDate,$TransType,$PriReferralType) = $sPrAuth->fetchrow_array();
#warn qq|calcPG: Type=$Type, StatusDate=$StatusDate, TransType=$TransType, CurPAgroup=$CurPAgroup, PriReferralType=$PriReferralType\n|;
  return($CurPAgroup) if ( $CurPAgroup =~ /^G9/ );
#warn qq|calcPG: NOT G9: CurPAgroup=$CurPAgroup\n|;
  $TransType = $forceTransType if ( $forceTransType );
# Contact cdc...
  return ('PG038') if ( $TransType == 21 );

  my $InsName = DBA->getxref($form,'xInsurance',$InsID,'Name');
  my $TL = TLevel->getTL($form,$ClientID,'18',$PrAuthID);
#warn qq|calcPG: TL=$TL, InsID=$InsID, InsName=$InsName\n|;
  my $PAgroup = '';
  if ( DBA->isIndMedicaid($form,$ClientID) )        # Individual LBHP / Psycholigist
  {
    my $Testing = $InsName =~ m/insure/i ? 'PG028' : 'PG029';
    my $AddUnit = $InsName =~ m/insure/i ? 'PG027' : 'PG040';
    my $IntUnit = $InsName =~ m/insure/i ? 'PG026' : 'PG030';
    $PAgroup = $Type eq 'TI' || $Type eq 'TE' ? $Testing
             : $TransType == 42 ? $AddUnit : $IntUnit;
#warn qq|calcPG: isIndMedicaid: Testing=$Testing, AddUnit=$AddUnit, IntUnit=$IntUnit, PAGroup=$PAgroup\n|;
  }
  elsif ( $TL eq 'I' ) { $PAgroup = 'PG019'; }         # ICF/MR
  elsif ( $TL eq 'P' ) { $PAgroup = 'PG001'; }         # Prevention and Recovery
  elsif ( $ServiceFocus eq '09' )                      # Special Populations Treatment Unit
  { $PAgroup = 'DH502'; }                              # Prison contract
  elsif ( $Type eq 'AU' ) { $PAgroup = 'PG033'; }      # Additional Units
  elsif ( $Type eq 'AD' ) { $PAgroup = 'PG050'; }      # Ambulatory Detox
  elsif ( DBA->isDMH($form,$ClientID,'TANF') )         # has a DMH TANF contract
  {
    if ( $TransType == 27 && $PriReferralType == 49 )  # TANF Re-Assessment
      { $PAgroup = 'DH519'; }
    elsif ( $TL eq '01' ) { $PAgroup = 'PG034'; }      # Treatment Level 1
    elsif ( $TL eq '02' ) { $PAgroup = 'PG035'; }      # Treatment Level 2
    elsif ( $TL eq '03' ) { $PAgroup = 'PG036'; }      # Treatment Level 3
    elsif ( $TL eq '04' ) { $PAgroup = 'PG037'; }      # Treatment Level 4
#warn qq|calcPG: isDMH: TransType=$TransType, PriReferralTypel=$PriReferralTypel, PAGroup=$PAgroup\n|;
  }
  elsif ( $Type =~ /DT|DR/ )
  {
    if ( $TL eq '03' ) { $PAgroup = $Type =~ /DR/ ? 'PG007' : 'PG053'; } # Level 3
    elsif ( $TL eq '04' ) { $PAgroup = $Type =~ /DR/ ? 'PG011' : 'PG054'; } # Level 4
  }
  else
  {
    #                                            Rehab?
    if    ( $TL eq '01' ) { $PAgroup = $Type =~ /RI|RE/ ? 'PG042' : 'PG046'; } # Level 1
    elsif ( $TL eq '02' ) { $PAgroup = $Type =~ /RI|RE/ ? 'PG043' : 'PG047'; } # Level 2
    elsif ( $TL eq '03' ) { $PAgroup = $Type =~ /RI|RE/ ? 'PG044' : 'PG048'; } # Level 3
    elsif ( $TL eq '04' ) { $PAgroup = $Type =~ /RI|RE/ ? 'PG045' : 'PG049'; } # Level 4
#warn qq|calcPG: else: TL=$TL, Type=$Type, PAgroup=$PAgroup\n|;
  }
  $sPrAuth->finish();
#warn qq|calcPG: END: TL=$TL, PAgroup=${PAgroup}\n|;
  return($PAgroup);
}
#############################################################################
sub passfailPA
{
  my ($self,$form,$InsID,$rPrAuth,$rPrAuthCDC) = @_;
  return() unless ( $self->required($form,$InsID) );
  return() if ( $rPrAuthCDC->{TransType} =~ /21|27/ );  # skip PA...
  my $failmsg = '';

  $StartDate = DBUtil->Date('today',0,-90);
#warn qq|passfailPA: StartDate=$StartDate, PAgroup=$rPrAuth->{PAgroup},TL=$rPrAuth->{TL}\n|;
  if ( $rPrAuth->{EffDate} lt $StartDate )
  { $failmsg .= " Effective Date too early (before $StartDate)."; }

  if ( $rPrAuth->{'TL'} eq '00' || $rPrAuth->{'PAgroup'} eq '' )
  { $failmsg .= " TreatmentLevel invalid ($rPrAuth->{'TL'})."; }

  my $dbh = myDBI->dbconnect($form->{'DBNAME'});
#warn qq|passfailPA: TransType=$rPrAuthCDC->{TransType}=, PrAuthID=$rPrAuth->{ID}\n|;
  
# Check Diagnosis
#warn qq|passfailPA: Client Problems\n|;
  if ( $rPrAuth->{'PAgroup'} eq 'DH502' ) { null; }
  else { $failmsg .= " No Problems for Client found!" if ( $rPrAuth->{'Diag1Prim'} eq '' ); }
  
# Check CARS
  my $qPDDom = qq|select * from PDDom where PDDom.PrAuthID=?|;
  my $sPDDom = $dbh->prepare($qPDDom);
  # skip this guy if no PDDom.
  $sPDDom->execute($rPrAuth->{ID}) || myDBI->dberror($qPDDom);
  unless ( my $rPDDom = $sPDDom->fetchrow_hashref )
  { $failmsg .= " No valid CARS Scores entered."; }
  $sPDDom->finish();
#warn qq|passfailPA: failmsg=$failmsg\n|;
  return($failmsg);
}
sub passfailCDC
{
  my ($self,$form,$InsID,$r) = @_;
  return() unless ( $self->required($form,$InsID) );
  return if ( $r->{TransType} == 21 && $form->{'DBNAME'} eq 'okmis_mms' );

  foreach my $f ( @CDCORDER ) { delete $CDC{$f}{'FAILMSG'}; }
#warn qq|passfailCDC: CDCOK=$r->{CDCOK}\n|;
  unless ( $r->{'CDCOK'} )
  {
    $CDC{'CDCOK'}{'REQ'} = 2;
    $CDC{'CDCOK'}{'FAILMSG'} .= " Please verify CDC information.";
#warn qq|passfailCDC: FAILMSG=$CDC{CDCOK}{FAILMSG}\n|;
  }
#warn qq|passfailCDC: AgencySite=$r->{'AgencySite'},AgencyNum=$r->{'AgencyNum'}\n|;
#foreach my $f ( sort keys %{$r} ) { warn "passfail: Agency r-$f=$r->{$f}\n"; }
  my ($userid2,$password2) = DBA->idDMH($form,$r->{'AgencySite'},$r->{'AgencyNum'});
#warn qq|passfailCDC: userid2=${userid2},password2=${password2}\n|;
#warn qq|passfailCDC: BEFORE: CDC-AgencySite-REQ=$CDC{'AgencySite'}{'REQ'}\n|;
#warn qq|passfailCDC: BEFORE: CDC-AgencySite-FAILMSG=$CDC{'AgencySite'}{'FAILMSG'}\n|;
  if ( $userid2 eq '' || $password2 eq '' )
  {
    $CDC{'AgencySite'}{'REQ'} = 2;
    $CDC{'AgencySite'}{'FAILMSG'} .= " Missing login for DMH Web Serivce.";
  }
#warn qq|passfailCDC: AFTER: CDC-AgencySite-REQ=$CDC{'AgencySite'}{'REQ'}\n|;
#warn qq|passfailCDC: AFTER: CDC-AgencySite-FAILMSG=$CDC{'AgencySite'}{'FAILMSG'}\n|;

#warn qq|passfailCDC: kls TransDate=$r->{TransDate}\n|;
  (my $TestDate = DBUtil->Date('today',-12,0)) =~ s/-//g;
  (my $TransDate = $r->{'TransDate'}) =~ s/-//g;
  if ( $TransDate lt $TestDate )
  { $CDC{'TransDate'}{'REQ'} = 2; $CDC{'TransDate'}{'FAILMSG'} .= " Transaction Date too early ($r->{TransDate})."; }
#warn qq|passfailCDC: kls TransDate=$r->{TransDate}, TestDate=${TestDate}\n|;
  (my $TestDate = DBUtil->Date('today')) =~ s/-//g;
  if ( $TransDate gt $TestDate )
  { $CDC{'TransDate'}{'REQ'} = 2; $CDC{'TransDate'}{'FAILMSG'} .= " Transaction Date cannot be after today ($r->{TransDate})."; }
#warn qq|passfailCDC: kls TransDate=$r->{TransDate}, TestDate=${TestDate}\n|;
#warn qq|passfailCDC: Age=$r->{Age}\n|;
#warn qq|passfailCDC: TransDate=$r->{TransDate}, TransTime=$r->{TransTime}\n|;
  if ( $r->{TransTime} eq '00:00:00' ) { $CDC{'TransDate'}{'REQ'} = 2; $CDC{'TransTime'}{'REQ'} = 2; $CDC{'TransDate'}{'FAILMSG'} .= " TransTime CANNOT be zero 00:00 (midnight)"; }

# Check City
  my $dbh = myDBI->dbconnect($form->{'DBNAME'});
  my $sTest = $dbh->prepare("select * from okmis_config.xOKCities where ID=?");
  $sTest->execute($r->{City}) || myDBI->dberror("select xOKCities $r->{City}");
  unless ( my $rTest = $sTest->fetchrow_hashref )
  { $CDC{'City'}{'REQ'} = 2; $CDC{'City'}{'FAILMSG'} .= " '$r->{City}' City NOT VALID spelling."; }
  $sTest->finish();
#warn qq|passfailCDC: MaidenName=$r->{MaidenName}, Gend=$r->{Gend}\n|;
  if ( $r->{MaidenName} ne '' && $r->{Gend} eq '02' ) { $CDC{'MaidenName'}{'REQ'} = 2; $CDC{'MaidenName'}{'FAILMSG'} .= " Maiden Name not used for male."; }
  if ( $r->{'CommitmentCounty'} eq '' &&
      ($r->{'LegalStatus'} ne '01' && $r->{'LegalStatus'} ne '17')
     )    # is required
  { $CDC{'LegalStatus'}{'REQ'} = 2; $CDC{'CommitmentCounty'}{'REQ'} = 2; $CDC{'CommitmentCounty'}{'FAILMSG'} .= " County of Commitment required [unless LegalStatus is 01 or 17]."; }

# 40 = DMHSAS or OHCA funded facility
  if ( $r->{PriReferralNPI} eq '' && $r->{PriReferralType} == 40 ) { $CDC{'PriReferralType'}{'REQ'} = 2; $CDC{'PriReferralNPI'}{'REQ'} = 2; $CDC{'PriReferralNPI'}{'FAILMSG'} .= " Primary Referral required for Type 40"; }
  if ( $r->{NPI} eq '' ) { $CDC{'PriReferralNPI'}{'REQ'} = 2; $CDC{'PriReferralNPI'}{'FAILMSG'} .= " Your Clinic NPI is null!"; }
  else
  {
    if ( $r->{PriReferralNPI} eq $r->{NPI} ) { $CDC{'PriReferralNPI'}{'REQ'} = 2; $CDC{'PriReferralNPI'}{'FAILMSG'} .= " Primary Referral cannot be your Agency."; }
#warn qq|SecReferralNPI=$r->{SecReferralNPI}, NPI=$r->{NPI} \n|;
    if ( $r->{SecReferralNPI} eq $r->{NPI} ) { $CDC{'SecReferralNPI'}{'REQ'} = 2; $CDC{'SecReferralNPI'}{'FAILMSG'} .= " Secondary Referral cannot be your Agency."; }
    if ( $r->{PriReferralType} eq $r->{SecReferralType} ) { $CDC{'PriReferralType'}{'REQ'} = 2; $CDC{'SecReferralType'}{'REQ'} = 2; $CDC{'SecReferralType'}{'FAILMSG'} .= " Secondary Referral Type cannot be equal to Primary."; }
    if ( $r->{PriReferralType} eq $r->{SecReferralType} && $r->{SecReferralType} eq '' ) { $CDC{'PriReferralType'}{'REQ'} = 2; $CDC{'SecReferralType'}{'REQ'} = 2; $CDC{'SecReferralType'}{'FAILMSG'} .= " Both are null."; }
  }

# Employed, then
#warn qq|EmplStat=$r->{EmplStat}, EmplType=$r->{EmplType} \n|;
  if ( $r->{EmplStat} =~ /[12]/ && $r->{EmplType} !~ /[12356]/ ) { $CDC{'EmplStat'}{'REQ'} = 2; $CDC{'EmplType'}{'REQ'} = 2; $CDC{'EmplStat'}{'FAILMSG'} .= " Employment Type should be 1-3,5 or 6 when Status is 1 or 2."; }
  if ( $r->{EmplType} =~ /[12356]/ && $r->{EmplStat} !~ /[12]/ ) { $CDC{'EmplStat'}{'REQ'} = 2; $CDC{'EmplType'}{'REQ'} = 2; $CDC{'EmplStat'}{'FAILMSG'} .= " Employment Status should be 1 or 2 when Type is 1-3,5 or 6."; }
# EmplStat is Unemployed, Type is not None.
  if ( $r->{EmplStat} == 3 && $r->{EmplType} != 4 ) { $CDC{'EmplStat'}{'REQ'} = 2; $CDC{'EmplType'}{'REQ'} = 2; $CDC{'EmplType'}{'FAILMSG'} .= " Employment Type should be None."; }
# EmplStat is Not in labor force, Type is A-F (Homemaker,Student,etc...)
  if ( $r->{EmplStat} == 4 && $r->{EmplType} !~ /[ABCDEF]/ ) { $CDC{'EmplStat'}{'REQ'} = 2; $CDC{'EmplType'}{'REQ'} = 2; $CDC{'EmplStat'}{'FAILMSG'} .= " Employment Type should be A-F."; }
# Prison/Jail and < 13
  if ( ($r->{IncarcerationStatus} == 1 || $r->{IncarcerationStatus} == 3) && $r->{Age} < 13 ) { $CDC{'CurrentResidence'}{'REQ'} = 2; $CDC{'DateOfBirth'}{'REQ'} = 2; $CDC{'CurrentResidence'}{'FAILMSG'} .= " Client cannot be in Prison/Jail if under 13."; }
# Institutional Setting must Live alone 
  if ( $r->{CurrentResidence} eq 'H' && $r->{LivingSituation} != 1 ) { $CDC{'CurrentResidence'}{'REQ'} = 2; $CDC{'LivingSituation'}{'REQ'} = 2; $CDC{'LivingSituation'}{'FAILMSG'} .= " Client lives alone if in Institutional Setting."; }
# Cannot be a Nursing Home.
  if ( $r->{CurrentResidence} eq 'G' ) { $CDC{'CurrentResidence'}{'REQ'} = 2; $CDC{'CurrentResidence'}{'REQ'} = 2; $CDC{'CurrentResidence'}{'FAILMSG'} .= " Medicaid Client cannot live in a Nursing Home."; }
# Education for those old enough
  if ( $r->{Education} eq '' && $r->{Age} >= 5 ) { $CDC{'Education'}{'REQ'} = 2; $CDC{'Education'}{'FAILMSG'} .= " Education required if over 4 (${EdErrorMsg})."; }
#warn qq|CHECK Education: ClientID=${ClientID}, Age=$rCDC->{Age}, SchoolLast3=$r->{SchoolLast3}\n|;
#warn qq|CHECK Education: CurrentGrade=$rClientEducation->{CurrentGrade}, SchoolGrade=$rClientEducation->{SchoolGrade}\n|;
# Arrests past 12 months must be >= Arrested 30 days
#warn qq|CHECK Arrests: Arrested12=$r->{Arrested12}, Arrested30=$r->{Arrested30}\n|;
  if ( $r->{Arrested12} < $r->{Arrested30} ) { $CDC{'Arrested12'}{'REQ'} = 2; $CDC{'Arrested30'}{'REQ'} = 2; $CDC{'Arrested12'}{'FAILMSG'} .= " Arrested past 12 months cannot be less than last 30 days."; }
#warn qq|CHECK Arrests: $CDC{'Arrested12'}{'REQ'}, $CDC{'Arrested30'}{'REQ'}, $CDC{'Arrested12'}{'FAILMSG'}\n|;

  unless ( $r->{TransType} == 21 )
  {
    # Check if School in last 3 months
    if ( $r->{InSchool} eq '' )
    {
      $CDC{'InSchool'}{'REQ'} = 2; $CDC{'InSchool'}{'REQ'} = 2; $CDC{'InSchool'}{'FAILMSG'} .= " Answer NEW question for In School last 3 months.";
    }
  }

# not all Service Focus valid
  unless ( $r->{ServiceFocus} =~ /01|02|03|06|09|11|12|13|14|15|16|17|18|19|20|21|22|23|24|27|30/ )
  { $CDC{'ServiceFocus'}{'REQ'} = 2; $CDC{'ServiceFocus'}{'FAILMSG'} .= " Invalid Service Focus."; }
  if ( $r->{ServiceFocus} eq '09' && $r->{'Age'} < 16 )
  { $CDC{'ServiceFocus'}{'REQ'} = 2; $CDC{'ServiceFocus'}{'FAILMSG'} .= " Age less than 16 for ServiceFocus=09 (DH502)"; }

# CAR Optional on Service Focus 02, 03, 09, 11, 21, 23, 30
#warn qq|CHECK CARs: ServiceFocus=$r->{ServiceFocus}\n|;
  unless ( $r->{ServiceFocus} =~ /02|03|09|11|21|23|30/ )
  {
#warn qq|      CAR1-$r->{CAR1}\n|;
    my $FAILMSG = '';
    if ( $r->{CAR1} eq '99' ) { $CDC{'CAR1'}{'REQ'} = 2; $FAILMSG .= " 1"; }
    if ( $r->{CAR2} eq '99' ) { $CDC{'CAR2'}{'REQ'} = 2; $FAILMSG .= " 2"; }
    if ( $r->{CAR3} eq '99' ) { $CDC{'CAR3'}{'REQ'} = 2; $FAILMSG .= " 3"; }
    if ( $r->{CAR4} eq '99' ) { $CDC{'CAR4'}{'REQ'} = 2; $FAILMSG .= " 4"; }
    if ( $r->{CAR5} eq '99' ) { $CDC{'CAR5'}{'REQ'} = 2; $FAILMSG .= " 5"; }
    if ( $r->{CAR6} eq '99' ) { $CDC{'CAR6'}{'REQ'} = 2; $FAILMSG .= " 6"; }
    if ( $r->{CAR7} eq '99' ) { $CDC{'CAR7'}{'REQ'} = 2; $FAILMSG .= " 7"; }
    if ( $r->{CAR8} eq '99' ) { $CDC{'CAR8'}{'REQ'} = 2; $FAILMSG .= " 8"; }
    if ( $r->{CAR9} eq '99' ) { $CDC{'CAR9'}{'REQ'} = 2; $FAILMSG .= " 9"; }
    $CDC{'CAR1'}{'FAILMSG'} = qq| Service Focus requires CAR Scores: ${FAILMSG}| unless ( $FAILMSG eq '' );
  }
#warn qq|CHECK FAILMSG=$FAILMSG\n|;
#warn qq|CHECK Problems: Problems=$r->{Problem1}, $r->{Problem2}, $r->{Problem3}; $r->{PriReferralType}\n|;
##
# TANF Edits...
  if ( $r->{'PriReferralType'} eq '49' || $r->{'SecReferralType'} eq '49' )
  {
    if ( $r->{Age} < 18 )
    { $CDC{'DateOfBirth'}{'REQ'} = 2; $CDC{'DateOfBirth'}{'FAILMSG'} = " Customer age must be greater than or equal to 18 for Referral 49."; }
    if ( $r->{'CountyofRes'} eq '' )
    { $CDC{'CountyofRes'}{'REQ'} = 2; $CDC{'CountyofRes'}{'FAILMSG'} = " Need County of Residence for Referral 49."; }
    if ( $r->{'Problem1'} eq '' )
    {
#warn qq|YES, Type=49...\n|;
      $CDC{'Problem1'}{'REQ'} = 2; 
      $CDC{'Problem1'}{'TRANSTYPE'} = 21;  # drop down to 21 required to.
      $CDC{'Problem1'}{'FAILMSG'} = " Presenting Problem required for Type 49.";
    }
## 4. DHS/TANF id must be reported (this edit was in place in APS and will be in place January 3rd)
##    a. TANF id should start with a 'C' or 'H' followed by six numbers
##    b. Child welfare customers should start with a 'KK' followed by 8 numbers
##  IS THIS FAMILY ID???
  }
# end TANF Edits.
  if ( $r->{'PriReferralType'} eq '63' || $r->{'SecReferralType'} eq '63' )
  {
    if ( $r->{Age} < 18 || $r->{Age} > 20 )
    { $CDC{'DateOfBirth'}{'REQ'} = 2; $CDC{'DateOfBirth'}{'FAILMSG'} = " Customer age must be 18 - 20 for Referral 63."; }
  }
  if ( $r->{'PriReferralType'} eq '64' || $r->{'SecReferralType'} eq '64' )
  {
    if ( $r->{Age} < 18 || $r->{Age} > 20 )
    { $CDC{'DateOfBirth'}{'REQ'} = 2; $CDC{'DateOfBirth'}{'FAILMSG'} = " Customer age must be 18 - 20 for Referral 64."; }
  }
##
# Family ID, 
  if ( $r->{FamilyID} eq '' )
  {
    if ( $r->{ServiceFocus} eq '03' )                  # Drug Court, Drug Court # is required.
    { $CDC{'FamilyID'}{'REQ'} = 2; $CDC{'FamilyID'}{'FAILMSG'} = " Drug Court # is required for Service Focus 03."; }
    elsif ( $r->{ServiceFocus} eq '09' )               # Special Problems, treatment unit, DOC # required
    { $CDC{'FamilyID'}{'REQ'} = 2; $CDC{'FamilyID'}{'FAILMSG'} = " DOC # is required for Service Focus 09."; }
    elsif ( $r->{PriReferralType} eq '12' )            # 12 = Department of Corrections
    { $CDC{'FamilyID'}{'REQ'} = 2; $CDC{'FamilyID'}{'FAILMSG'} = " DHS # is required for Primary Referral 12."; }
# DMH sometimes does not know if DOC # is needed until after the bill the Contract Code
    #elsif ( $r->{PriReferralType} eq '33' )            # 33 = Probation
    #{ $CDC{'FamilyID'}{'REQ'} = 2; $CDC{'FamilyID'}{'FAILMSG'} = " DHS # is required for Primary Referral 33."; }
    elsif ( $r->{PriReferralType} eq '34' )            # 34 = Parole
    { $CDC{'FamilyID'}{'REQ'} = 2; $CDC{'FamilyID'}{'FAILMSG'} = " DHS # is required for Primary Referral 34."; }
    elsif ( $r->{PriReferralType} eq '49' )            # 49 = TANF/child welfare, DHS # required
    { $CDC{'FamilyID'}{'REQ'} = 2; $CDC{'FamilyID'}{'FAILMSG'} = " DHS # is required for Primary Referral 49."; }
    elsif ( $r->{Problem1} =~ /745|746|747/ )          # SA Dependant Child, Family ID required
    { $CDC{'FamilyID'}{'REQ'} = 2; $CDC{'FamilyID'}{'FAILMSG'} = " Family ID is required for Presenting Problem 745,746,747."; }
    elsif ( $r->{Problem2} =~ /745|746|747/ )          # SA Dependant Child, Family ID required
    { $CDC{'FamilyID'}{'REQ'} = 2; $CDC{'FamilyID'}{'FAILMSG'} = " Family ID is required for Presenting Problem 745,746,747."; }
    elsif ( $r->{Problem3} =~ /745|746|747/ )          # SA Dependant Child, Family ID required
    { $CDC{'FamilyID'}{'REQ'} = 2; $CDC{'FamilyID'}{'FAILMSG'} = " Family ID is required for Presenting Problem 745,746,747."; }
  }
#warn qq|CHECK Problems: Problems=$r->{Problem1}, $r->{Problem2}, $r->{Problem3}; $r->{Drug1}\n|;
  if ( $r->{Problem1} =~ /710|711|720|721|730|731|741|742|743/ && $r->{Drug1} eq '01' )
  { $CDC{'Problem1'}{'REQ'} = 2; $CDC{'Problem1'}{'FAILMSG'} = " at least 1 Drug required for Presenting Problem1."; }
  if ( $r->{Problem2} =~ /710|711|720|721|730|731|741|742|743/ && $r->{Drug1} eq '01' )
  { $CDC{'Problem2'}{'REQ'} = 2; $CDC{'Problem2'}{'FAILMSG'} = " at least 1 Drug required for Presenting Problem2."; }
  if ( $r->{Problem3} =~ /710|711|720|721|730|731|741|742|743/ && $r->{Drug1} eq '01' )
  { $CDC{'Problem3'}{'REQ'} = 2; $CDC{'Problem3'}{'FAILMSG'} = " at least 1 Drug required for Presenting Problem3."; }
#warn qq|CHECK Problems: REQ=$CDC{Problem1}{REQ}, FAILMSG=$CDC{Problem1}{FAILMSG}\n|;

  my $failmsg = $self->checkForNulls($r);   ## NotNull check list...
#warn qq|passfailCDC: failmsg=$failmsg\n|;
  return($failmsg);
}
sub genHTML
{
  my ($self,$form,$InsID,$PrAuthID) = @_;
#warn qq|genHTML: ENTER: PrAuthID=$PrAuthID\n|;
#foreach my $f ( sort keys %{$form} ) { warn "genHTML: form-$f=$form->{$f}\n"; }
  my $dbh = myDBI->dbconnect($form->{'DBNAME'});
  my $html = qq|
<TABLE CLASS="home fullsize" >
  <TR >
    <TD CLASS="port hdrtxt" COLSPAN="3" >
      Data Required to be fixed or updated for CDC
    </TD>
  </TR>
|;
  my $sPrAuthCDC = $dbh->prepare("select * from ClientPrAuthCDC where ClientPrAuthID='$PrAuthID'");
  $sPrAuthCDC->execute() || myDBI->dberror("genHTML select ClientPrAuthCDC ($PrAuthID)");
  my $rPrAuthCDC = $sPrAuthCDC->fetchrow_hashref;
  my $failmsg = $self->passfailCDC($form,$InsID,$rPrAuthCDC);
#foreach my $f ( sort keys %{$rPrAuthCDC} ) { warn "genHTML: rPrAuthCDC-$f=$rPrAuthCDC->{$f}\n"; }
#warn qq|genHTML: failmsg=$failmsg\n|;
  foreach my $f ( $self->isRequired($rPrAuthCDC) )
  {
#warn qq|genHTML: CHG=$CDC{$f}{'CHG'}\n|;
    next if ( $CDC{$f}{'CHG'} eq 'NOT-HERE' );    # change from another screen.
    my $FIELDNAME = $CDC{$f}{'FIELDNAME'} eq '' ? $f : $CDC{$f}{'FIELDNAME'};
    my $FAILMSG = $CDC{$f}{'FAILMSG'} eq '' ? qq|(required)| : '('.$CDC{$f}{'FAILMSG'}.')';
    $html .= qq|
  <TR >
    <TD CLASS="strcol" >${FIELDNAME}</TD>
    <TD CLASS="strcol" >Please check below</TD>
    <TD CLASS="strcol" >${FAILMSG}</TD>
  </TR>
|;
  }
  $sPrAuthCDC->finish();
  $html .= qq|
</TABLE>
|;
  return($html);
}
sub checkForNulls
{
  my ($self,$r) = @_;
  my ($nullcnt,$nullfail,$failmsg) = (0,'','');
  foreach my $f ( $self->isRequired($r) )   ## NotNull field list...
  {
#warn qq|1:checkForNulls: ${f}: REQ=$CDC{$f}{'REQ'}, FAILMSG=$CDC{$f}{'FAILMSG'}\n|;
    if ( $CDC{$f}{'REQ'} == 2 )
    { $cnt++; $failmsg .= qq|$CDC{$f}{FAILMSG} | unless ( $CDC{$f}{'FAILMSG'} eq '' ); }
    else
    { $nullcnt++; $nullfail .= qq|'${f}' |; }
#warn qq|2:checkForNulls: ${f}: cnt=${cnt}, nullcnt=${nullcnt}\n|;
  }
  my $msg = $nullcnt == 0 ? $failmsg :
    qq|# |.$nullfail.qq| not found. Please select 'Correct' to fix. |.$failmsg;
  return($msg);
}
# Check for Nulls and Required in PrAuthCDC....
#   add to @CDCORDER to check variable, and %CDC.
#   check REQ=2 set in other passfail routines.
sub isRequired
{
  my ($self,$r) = @_;
  my @bad = ();
  foreach my $f ( @CDCORDER )
  {
#warn qq|1:isRequired: ${f}=$r->{$f}, REQ=$CDC{$f}{'REQ'}, TransType=$r->{TransType}, TYPE=$CDC{$f}{TRANSTYPE}, AGE=$r->{'Age'}\n|;
    next if ( $r->{'TransType'} ne '' && $r->{TransType} < $CDC{$f}{'TRANSTYPE'} );
    next if ( $r->{'TransType'} == 27 );
    next if ( $CDC{$f}{'AGELT'} && $r->{'Age'} >= $CDC{$f}{'AGELT'} );
    next unless ( $CDC{$f}{'REQ'} );
#warn qq|2:isRequired: $f=$r->{$f}, REQ=$CDC{$f}{'REQ'}\n|;
    push(@bad,$f) if ( $r->{$f} eq '' || $CDC{$f}{'REQ'} == 2 );
  }
#foreach my $f ( @bad ) { warn qq|isRequired: bad=$f\n|; }
  return(@bad);
}
#############################################################################
sub listPAStatus
{
  my ($self,$form,$PrAuthID,$links) = @_;
#warn qq|\nlistPAStatus: PrAuthID=${PrAuthID}, links=${links}\n|;
  return() unless ( $PrAuthID );
  my $dbh = myDBI->dbconnect($form->{'DBNAME'});
  my $sClientPrAuthCDC = $dbh->prepare("select Insurance.InsID,ClientPrAuth.Locked,ClientPrAuthCDC.ID,ClientPrAuthCDC.Status,ClientPrAuthCDC.CDCOK,ClientPrAuthCDC.TransType,ClientPrAuthCDC.TransDate,ClientPrAuthCDC.TransTime,ClientPrAuthCDC.AgencySite,ClientPrAuthCDC.Fail,ClientPrAuthCDC.Reason from ClientPrAuthCDC left join ClientPrAuth on ClientPrAuth.ID=ClientPrAuthCDC.ClientPrAuthID left join Insurance on Insurance.InsNumID=ClientPrAuth.InsuranceID where ClientPrAuthCDC.ClientPrAuthID=?");
  $sClientPrAuthCDC->execute($PrAuthID) || myDBI->dberror("listPAStatus: select ClientPrAuthCDC ${PrAuthID}");
  my ($InsID,$Locked,$ID,$Status,$CDCOK,$TransType,$td,$TransTime,$an,$Fail,$Reason) = $sClientPrAuthCDC->fetchrow_array;
  $Reason =~ s/\n/ /g;              # new line
#warn qq|listPAStatus: InsID=${InsID}, PrAuthID=${PrAuthID}, Locked=${Locked}, ID=${ID}\n|;
#warn qq|listPAStatus: Status=${Status}, CDCOK=${CDCOK}, td=${td}, TransTime=${TransTime}\n|;
#warn qq|listPAStatus: an=${an}, Fail=${Fail}, Reason=${Reason}\n|;
  $sClientPrAuthCDC->finish();
  my $listCARS = $TransType == 21 || $TransType == 27 ? '21' : '';
  $Reason .= qq|<BR>Check the log for Rejections| if ( $Status eq 'Rejected' );
  my $TransDate = DBUtil->Date($td,'fmt','MM/DD/YYYY');
  my $AgencyName = gHTML->getAgencyName($form,$an);
  my $token = DBUtil->genToken();
  $Fail =~ s/\n/<BR>/g;
  my $fail = qq|<BR>**<BR>${Fail}| if ( $Fail ne '' );
  my $reason = qq|<BR>**<BR>${Reason}<BR>**| if ( $Reason ne '' );
  my $popup = qq|TransDate/Time: ${TransDate} @ ${TransTime}<BR>${AgencyName}${reason}|;
#warn qq|listPAStatus: Reason=${Reason}, reason=${reason}, popup=${popup}\n|;
  my $print = qq|<A HREF="javascript:ReportWindow('/src/cgi/bin/PrintCDCLog.cgi?IDs=${PrAuthID}&mlt=$form->{mlt}&action=ClientPrAuth','PrintWindow')" TITLE="Click here to print the logged activity" ><IMG SRC="/img/print-ok.png" HEIGHT="21" WIDTH="21" BORDER="0" ></A>|;
  my $send = qq|MIS_Action=DMHws.pl&Client_ClientID=$form->{'Client_ClientID'}&myID=${PrAuthID}&action=ClientPrAuth&mlt=$form->{mlt}|;
  my $view = qq|view=CDC${listCARS}.cgi&fwdTABLE=ClientPrAuthCDC&ClientPrAuthCDC_ID=${ID}&ClientPrAuth_ID=${PrAuthID}&${links}&pushID=$form->{'LINKID'}&UpdateTables=all|;
#warn qq|listPAStatus: PrAuthID=${PrAuthID}, Agent=|.SysAccess->chkPriv($form,'Agent')."\n";
#warn qq|listPAStatus: PrAuthID=${PrAuthID}, Locked=${Locked}\n|;
  my $auth = (SysAccess->chkPriv($form,'ClinicManager') ||  SysAccess->chkPriv($form,'Agent')) && !$Locked 
           ? qq|<A HREF="javascript:ReportWindow('/src/cgi/bin/authPA.cgi?PrAuthID=${PrAuthID}&mlt=$form->{mlt}','PrintWindow')" TITLE="Click here to manually authorize this PA" ><IMG SRC="/img/tab-lock.png" ALT="" BORDER="0" HEIGHT="20" WIDTH="20" ></A>|
           : '';
  my $button = $fail eq ''
             ?  SysAccess->chkPriv($form,'AuthRVUs') && $CDCOK && CDC->required($form,$InsID) && !$Locked && $Status ne 'Closed'
               ? qq|<BR><button CLASS="confirmLINK" MYTEXT="Are you sure you want to send this Prior Authorization?<BR>If so, then click the OK button below. If NOT, click the Cancel button below." HREF="/src/src/cgi/bin/mis.cgi?${send}" MYBUSY="Sending..." >Send</button>|
               : ''
             : $CDCOK
               ? qq|<BR><INPUT TYPE="submit" ONCLICK="return validate(this.form)" NAME="${view}" VALUE="Correct" >|
               : qq|<BR><INPUT TYPE="submit" ONCLICK="return validate(this.form)" NAME="${view}" VALUE="Verify CDC" >|;
  my $val = qq|${print}
${auth}<BR>
<A HREF="javascript:void(0)" TITLE="${popup}" >
  ${Status}
  ${fail}
</A>
&nbsp;${button}&nbsp;
\n|;
  my $html = $fail eq '' ? $val : $val.chr(253).qq|STYLE="background-color: red"|;
  return($html);
}
sub listPAgroup
{
  my ($self,$form,$PrAuthID) = @_;
#warn qq|\nlistPAgroup: PrAuthID=${PrAuthID}\n|;
  return() unless ( $PrAuthID );
  my $dbh = myDBI->dbconnect($form->{'DBNAME'});
  my $sClientPrAuth = $dbh->prepare("select ClientPrAuth.PAgroup,ClientPrAuth.HHresponse,ClientPrAuth.CoPA,ClientPrAuthCDC.FamilyID from ClientPrAuth left join ClientPrAuthCDC on ClientPrAuthCDC.ClientPrAuthID=ClientPrAuth.ID where ClientPrAuth.ID=?");
  $sClientPrAuth->execute($PrAuthID) || myDBI->dberror("listPAgroup: select ClientPrAuth ${PrAuthID}");
  my ($PAgroup,$HHresponse,$CoPA,$FamilyID) = $sClientPrAuth->fetchrow_array;
  $sClientPrAuth->finish();
  my ($CodeDescr,$type,$span) = ('','','0');
  my $token = DBUtil->genToken();
  my $print = qq|<A HREF="javascript:ReportWindow('/src/cgi/bin/PAPeriods.cgi?IDs=${PrAuthID}&mlt=$form->{mlt}&action=ClientPrAuth','PrintWindow')" TITLE="Click here to print the Inventory for this Prior Authorization" ><IMG SRC="/img/print-ok.png" HEIGHT="21" WIDTH="21" BORDER="0" ></A>|;
  $print .= $form->{'LOGINPROVID'} == 91 ? qq|</SCRIPT><A HREF="javascript:ReportWindow('/src/cgi/bin/PrintPALines.cgi?IDs=${PrAuthID}&mlt=$form->{mlt}&action=ClientPrAuth','PrintWindow')" TITLE="Click here to print the Monthly Lines for this Prior Authorization" ><IMG SRC="/img/print-ok.png" HEIGHT="21" WIDTH="21" BORDER="0" ></A>| : '';
  my $setlines = $form->{'LOGINPROVID'} == 91 ? qq|<BR><A HREF="javascript:ReportWindow('/src/cgi/bin/setPALines.cgi?PrAuthID=${PrAuthID}&mlt=$form->{mlt}','PrintWindow')" TITLE="Click here to reset the PA Lines for this authorize" ><IMG SRC="/img/tab-lock.png" ALT="" BORDER="0" HEIGHT="20" WIDTH="20" ></A>| : '';
  my $response = $HHresponse eq '' ? '' : 'Health Home: '.$HHresponse.'<BR>(CoPA ID:'.$CoPA.')';
  if ( $PAgroup ne '' )
  {
    ($CodeDescr = DBA->getxref($form,'xPAgroups',$PAgroup,'Descr')) =~ s/'//g;
    $type = DBA->getxref($form,'xPAgroups',$PAgroup,'Length1');
    $span = DBA->getxref($form,'xPAgroups',$PAgroup,'Length2');
    my $CASEID = $FamilyID eq '' ? '' : qq|<BR>FamilyID: ${FamilyID}|;
    $CodeDescr .= qq|<BR>${span} ${type}${CASEID}|;
  }
  my $popup = qq|${CodeDescr}<BR>${response}|;
  my $html = qq|${print}<BR><A HREF="javascript:void(0)" TITLE="${popup}" >${PAgroup}${setlines}</A>\n|;
  return($html);
}
sub listDISStatus
{
  my ($self,$form,$DischargeID,$links) = @_;
#warn qq|\nlistDISStatus: DischargeID=${DischargeID}, links=${links}\n|;
  return() unless ( $DischargeID );
  my $dbh = myDBI->dbconnect($form->{'DBNAME'});
  my $sClientDischargeCDC = $dbh->prepare("select Insurance.InsID,ClientDischarge.Locked,ClientDischargeCDC.ID,ClientDischargeCDC.Status,ClientDischargeCDC.CDCOK,ClientDischargeCDC.TransDate,ClientDischargeCDC.TransTime,ClientDischargeCDC.AgencySite,ClientDischargeCDC.Fail,ClientDischargeCDC.Reason from ClientDischargeCDC left join ClientDischarge on ClientDischarge.ID=ClientDischargeCDC.ClientDischargeID left join Insurance on Insurance.InsNumID=ClientDischarge.InsuranceID where ClientDischargeCDC.ClientDischargeID=?");
  $sClientDischargeCDC->execute($DischargeID) || myDBI->dberror("listDISStatus: select ClientDischargeCDC ${DischargeID}");
  my ($InsID,$Locked,$ID,$Status,$CDCOK,$td,$TransTime,$an,$Fail,$Reason) = $sClientDischargeCDC->fetchrow_array;
  $Reason =~ s/\n/ /g;              # new line
#warn qq|listDISStatus: InsID=${InsID}, Locked=${Locked}, ID=${ID}\n|;
#warn qq|listDISStatus: Status=${Status}, CDCOK=${CDCOK}, td=${td}, TransTime=${TransTime}\n|;
#warn qq|listDISStatus: an=${an}, Fail=${Fail}, Reason=${Reason}\n|;
  $sClientDischargeCDC->finish();
  my $TransDate = DBUtil->Date($td,'fmt','MM/DD/YYYY');
  my $AgencyName = gHTML->getAgencyName($form,$an);
  my $token = DBUtil->genToken();
  $Fail =~ s/\n/<BR>/g;
  my $fail = qq|<BR>**<BR>${Fail}| if ( ${Fail} ne '' );
  my $reason = qq|<BR>**<BR>${Reason}<BR>**| if ( ${Reason} ne '' );
  my $popup = qq|TransDate/Time: ${TransDate} @ ${TransTime}<BR>${AgencyName}${reason}|;
  my $print = qq|<A HREF="javascript:ReportWindow('/src/cgi/bin/PrintCDCLog.cgi?IDs=${DischargeID}&mlt=$form->{mlt}&action=ClientDischarge','PrintWindow')" TITLE="Click here to print the logged activity" ><IMG SRC="/img/print-ok.png" HEIGHT="21" WIDTH="21" BORDER="0" ></A>|;
  my $send = qq|MIS_Action=DMHws.pl&Client_ClientID=$form->{'Client_ClientID'}&myID=${DischargeID}&action=ClientDischarge&mlt=$form->{mlt}|;
  my $view = qq|view=DISCDC.cgi&fwdTABLE=ClientDischargeCDC&ClientDischargeCDC_ID=${ID}&ClientDischarge_ID=${DischargeID}&${links}&pushID=$form->{'LINKID'}&UpdateTables=all|;
#warn qq|listDISStatus: fail=${fail}\n|;
#warn qq|listDISStatus: CDCOK=${CDCOK}\n|;
#warn qq|listDISStatus: Locked=${Locked}\n|;
#warn qq|listDISStatus: InsID=${InsID}\n|;
#warn qq|listDISStatus: req=|.CDC->required($form,$InsID)."\n";
#warn qq|listDISStatus: AuthRVUs=|.SysAccess->chkPriv($form,'AuthRVUs')."\n";
  my $button = $fail eq ''
             ? SysAccess->chkPriv($form,'AuthRVUs') && $CDCOK && CDC->required($form,$InsID) && !$Locked && $Status ne 'Closed'
               ? qq|<BR><button CLASS="confirmLINK" MYTEXT="Are you sure you want to send this Discharge?<BR>If so, then click the OK button below. If NOT, click the Cancel button below." HREF="/src/src/cgi/bin/mis.cgi?${send}" MYBUSY="Sending..." >Send</button>|
               : ''
             : $CDCOK
               ? qq|<BR><INPUT TYPE="submit" ONCLICK="return validate(this.form)" NAME="${view}" VALUE="Correct" >|
               : qq|<BR><INPUT TYPE="submit" ONCLICK="return validate(this.form)" NAME="${view}" VALUE="Verify CDC" >|;
  my $val = qq|${print}<BR><A HREF="javascript:void(0)" TITLE="${popup}" >${Status}${fail}</A>${button}\n|;
  my $html = $fail eq '' ? $val : $val.chr(253).qq|STYLE="background-color: red"|;
  return($html);
}
# means we need to list the CAR Scores
sub listCARS
{
  my ($self,$form,$PrAuthID) = @_;
#warn qq|listCARS: PrAuthID=$PrAuthID\n|;
# form only list CLient and ClientIntake
#foreach my $f ( sort keys %{$form} ) { warn "required: form-$f=$form->{$f}\n"; }
  my $dbh = myDBI->dbconnect($form->{'DBNAME'});
  my $flag = 1;
  if ( $PrAuthID )
  {
    $sClientPrAuthCDC = $dbh->prepare("select TransType from ClientPrAuthCDC where ClientPrAuthID=?");
    $sClientPrAuthCDC->execute($PrAuthID);
    ($TransType) = $sClientPrAuthCDC->fetchrow_array;
    $sClientPrAuthCDC->finish();
    $flag = $TransType == 21 || $TransType == 27 ? 0 : 1;
  }
  return($flag);
}
sub Lock
{
  my ($self,$form,$table,$ID,$lock) = @_;
#warn qq|Lock: ID=$ID, table=$table\n|;
  return() if ($table eq '');
  return() if ($ID eq '');
  my $dbh = myDBI->dbconnect($form->{'DBNAME'});
  my $qLock = $table eq 'ClientDischarge'
            ? qq|update ClientDischarge set Locked='${lock}' where ID=?|
            : qq|update ClientPrAuth left join PDDom on PDDom.PrAuthID=ClientPrAuth.ID set ClientPrAuth.Locked='${lock}',PDDom.Locked='${lock}' where ClientPrAuth.ID=?|;
  my $sLock = $dbh->prepare($qLock);
  $sLock->execute($ID) || myDBI->dberror("Lock: ${table}: ${ID}-Locked=${lock}");
  $sLock->finish();
  return();
}
sub setr
{
  my ($self,$form,$table) = @_;
  my $r = ();
  foreach my $f ( $self->gFields($form,$table) ) { $r->{$f} = ''; }
  return($r);
}
sub gFields
{
  my ($self,$form,$table) = @_;
  my @flds = ();
  my $dbh = myDBI->dbconnect($form->{'DBNAME'});
  my $s = $dbh->prepare("show fields from ${table}");
  $s->execute() || myDBI->dberror("show fields from ${table}");
  while ( my $r = $s->fetchrow_hashref )
  { push(@flds,$r->{'Field'}); }
  $s->finish();
#warn qq|flds=@flds\n|;
  return(@flds);
}
#############################################################################
1;
