#!/usr/bin/perl
use lib '/home/okmis/mis/src/lib';
use myConfig;
use DBI;
use myForm;
use myDBI;
use DBA;
use MgrTree;
use DBUtil;
use PDF;
use Time::Local;
my $DT=localtime();

############################################################################
my $form = myForm->new();
my $dbh = myDBI->dbconnect($form->{'DBNAME'});
my $cdbh = myDBI->dbconnect('okmis_config');
#warn "PrintClientIntakePre2017: ClientID=$form->{'ClientID'}\n";
#warn "PrintClientIntakePre2017: IDs=$form->{'IDs'}\n";

# get the last Admission Date...
if ( $form->{'ClientID'} )
{
  my $sGet = $dbh->prepare("select * from ClientAdmit where ClientID=? order by AdmitDate desc");
  $sGet->execute($form->{'ClientID'}) || myDBI->dberror("PrintClientIntakePre2017: Get: select ClientAdmit $form->{'ClientID'}");
  my $rGet = $sGet->fetchrow_hashref;
  $form->{'IDs'} = $rGet->{ID};
  $sGet->finish();
}
#warn "PrintClientIntakePre2017: IDs=$form->{'IDs'}\n";
##
# prepare selects...
##
my $qClientAdmit = qq|select * from ClientAdmit where ID=?|;
my $sClientAdmit = $dbh->prepare($qClientAdmit);
my $qProvider = qq|select * from Provider where ProvID=?|;
my $sProvider = $dbh->prepare($qProvider);
my $qClient = qq|select * from Client where Client.ClientID=?|;
my $sClient = $dbh->prepare($qClient);
my $qClientIntake = qq|select * from ClientIntake where ClientID=?|;
my $sClientIntake = $dbh->prepare($qClientIntake);
my $sClientReferrals = $dbh->prepare("select * from ClientReferrals where ClientID=?");
my $sClientLegal = $dbh->prepare("select * from ClientLegal where ClientID=?");
my $sClientRelations = $dbh->prepare("select * from ClientRelations where ClientID=?");
my $sClientResources = $dbh->prepare("select * from ClientResources where ClientID=?");
my $qClientEmergency = qq|select * from ClientEmergency where ClientID=?|;
my $sClientEmergency = $dbh->prepare($qClientEmergency);
my $sClientEducation = $dbh->prepare("select * from ClientEducation where ClientID=?");
my $qClientMHProblems = qq|select * from ClientMHProblems where ClientID=?|;
my $sClientMHProblems = $dbh->prepare($qClientMHProblems);
my $qMedHx = qq|select * from MedHx where ClientID=?|;
my $sMedHx = $dbh->prepare($qMedHx);
my $qClientHealth = qq|select * from ClientHealth where ClientID=?|;
my $sClientHealth = $dbh->prepare($qClientHealth);
my $qClientDevl = qq|select * from ClientDevl where ClientID=?|;
my $sClientDevl = $dbh->prepare($qClientDevl);
my $qGambling = qq|select * from Gambling where ClientID=?|;
my $sGambling = $dbh->prepare($qGambling);
my $qClientTrauma = qq|select * from ClientTrauma where ClientID=?|;
my $sClientTrauma = $dbh->prepare($qClientTrauma);
my $qGuardianHistory = qq|select * from GuardianHistory where ClientID=?|;
my $sGuardianHistory = $dbh->prepare($qGuardianHistory);
my $qClientSocial = qq|select * from ClientSocial where ClientID=?|;
my $sClientSocial = $dbh->prepare($qClientSocial);
my $qMentalStat = qq|select * from MentalStat where ClientID=?|;
my $sMentalStat = $dbh->prepare($qMentalStat);
my $qClientSummary = qq|select * from ClientSummary where ClientID=?|;
my $sClientSummary = $dbh->prepare($qClientSummary);
my $sDischarge=$dbh->prepare("select * from ClientDischarge left join ClientDischargeCDC on ClientDischargeCDC.ClientDischargeID=ClientDischarge.ID where ClientDischarge.ClientID=? and ClientDischargeCDC.TransDate<? order by ClientDischargeCDC.TransDate desc");
my $sInsurance = $dbh->prepare("select Insurance.*,xInsurance.Ph1 from Insurance left join xInsurance on xInsurance.ID=Insurance.InsID where Insurance.ClientID=? and Insurance.Priority=? order by Insurance.InsNumEffDate desc, Insurance.InsNumExpDate");
my $sCRAFFT = $dbh->prepare("select * from ClientCRAFFT where ClientID=? and TestDate is not null order by TestDate desc");

############################################################################
##
# for now...select the incoming ClientID...
#warn "PrintClientIntakePre2017: IDs=$form->{'IDs'}\n";
##
my $xdp = qq|<?xml version="1.0" encoding="UTF-8" ?> 
<?xfa generator="XFA2_0" APIVersion="2.2.4333.0" ?>
<xdp:xdp xmlns:xdp="http://ns.adobe.com/xdp/" >
<xfa:datasets xmlns:xfa="http://www.xfa.org/schema/xfa-data/1.0/" >
<xfa:data>
<TopmostSubform>
|;
foreach my $ID ( split(' ',$form->{'IDs'}) )
{ 
#warn "PrintClientIntakePre2017: ID=$ID\n";
  $sClientAdmit->execute($ID) || myDBI->dberror("PrintClientIntakePre2017: select ClientAdmit ${ID}");
  while ( my $rClientAdmit = $sClientAdmit->fetchrow_hashref )
  { 
    $sClient->execute($rClientAdmit->{'ClientID'}) || myDBI->dberror("PrintClientIntakePre2017: select Client $rClientAdmit->{'ClientID'}");
    my $rClient = $sClient->fetchrow_hashref;
    $xdp .= main->printIntake($rClientAdmit,$rClient); 
  }
}
my $pdfpath = myConfig->cfg('FormsPrintURL')."/PrintClientIntake_Pre2017.pdf";
$xdp .= qq|
</TopmostSubform>
</xfa:data>
</xfa:datasets>
<pdf href="${pdfpath}" xmlns="http://ns.adobe.com/xdp/pdf/" />
</xdp:xdp>
|;
$sClientAdmit->finish();
$sProvider->finish();
$sClient->finish();
$sClientIntake->finish();
$sClientReferrals->finish();
$sClientLegal->finish();
$sClientRelations->finish();
$sClientResources->finish();
$sClientEmergency->finish();
$sClientEducation->finish();
$sClientMHProblems->finish();
$sMedHx->finish();
$sClientHealth->finish();
$sClientDevl->finish();
$sGambling->finish();
$sClientTrauma->finish();
$sGuardianHistory->finish();
$sClientSocial->finish();
$sMentalStat->finish();
$sClientSummary->finish();
$sDischarge->finish();
$sInsurance->finish();
$sCRAFFT->finish();
if ( $form->{file} )
{
  open OUT, ">$form->{file}" || die "Couldn't open '$form->{file}' file: $!"; 
#warn qq|print to file: $form->{'file'}\n|;
  print OUT ${xdp};
  close(OUT);
}
else { print qq|Content-Type: application/vnd.adobe.xdp+xml\n\n${xdp}|; }

myDBI->cleanup();

exit;
############################################################################
sub printIntake
{
  my ($self,$rClientAdmit,$rClient) = @_;
##
# Header info...
  #my $AgencyID = MgrTree->getAgency($form,$rClient->{clinicClinicID});
  my $AdmitID = $rClientAdmit->{ProvID}
                 ? $rClientAdmit->{'ProvID'}      # set after Note entered
                 : $rClient->{'clinicClinicID'};  # otherwise clinic assigned to
  my $AgencyID = MgrTree->getAgency($form,$AdmitID);
  $sProvider->execute($AgencyID) || myDBI->dberror($qProvider);
  my $rAgency = $sProvider->fetchrow_hashref;
  my $AgencyName = DBA->subxml($rAgency->{Name});
  my $AgencyAddr = $rAgency->{Addr1};
  $AgencyAddr .= ', ' . $rAgency->{Addr2} if ( $rAgency->{Addr2} );
  my $AgencyCSZ .= $rAgency->{City} . ', ' . $rAgency->{ST} . '  ' . $rAgency->{Zip};
  my $AgencyPh = 'Office: ' . $rAgency->{WkPh} . '  Fax: ' . $rAgency->{Fax};
##
# Client info...
  my $ClientID = $rClient->{'ClientID'};
  my $ClientName = qq|$rClient->{FName} $rClient->{LName}|;

# other Client information...
  $sClientIntake->execute($ClientID) || myDBI->dberror($qClientIntake);
  my $rClientIntake = $sClientIntake->fetchrow_hashref;
  $sClientReferrals->execute($ClientID) || myDBI->dberror("select: ClientReferrals");
  my $rClientReferrals = $sClientReferrals->fetchrow_hashref;
  $sClientLegal->execute($ClientID) || myDBI->dberror("select: ClientLegal");
  my $rClientLegal = $sClientLegal->fetchrow_hashref;
  $sClientRelations->execute($ClientID) || myDBI->dberror("select: ClientRelations");
  my $rClientRelations = $sClientRelations->fetchrow_hashref;
  $sClientResources->execute($ClientID) || myDBI->dberror("select: ClientResources");
  my $rClientResources = $sClientResources->fetchrow_hashref;
  $sClientEmergency->execute($ClientID) || myDBI->dberror($qClientEmergency);
  my $rClientEmergency = $sClientEmergency->fetchrow_hashref;
  $sClientEducation->execute($ClientID) || myDBI->dberror("select ClientEducation");
  my $rClientEducation = $sClientEducation->fetchrow_hashref;
  $sClientMHProblems->execute($ClientID) || myDBI->dberror($qClientMHProblems);
  my $rClientMHProblems = $sClientMHProblems->fetchrow_hashref;
  $sMedHx->execute($ClientID) || myDBI->dberror($qMedHx);
  my $rMedHx = $sMedHx->fetchrow_hashref;
  $sClientHealth->execute($ClientID) || myDBI->dberror($qClientHealth);
  my $rClientHealth = $sClientHealth->fetchrow_hashref;
  $sClientDevl->execute($ClientID) || myDBI->dberror($qClientDevl);
  my $rClientDevl = $sClientDevl->fetchrow_hashref;
  $sGambling->execute($ClientID) || myDBI->dberror($qGambling);
  my $rGambling = $sGambling->fetchrow_hashref;
  $sClientTrauma->execute($ClientID) || myDBI->dberror($qClientTrauma);
  my $rClientTrauma = $sClientTrauma->fetchrow_hashref;
  $sGuardianHistory->execute($ClientID) || myDBI->dberror($qGuardianHistory);
  my $rGuardianHistory = $sGuardianHistory->fetchrow_hashref;
  $sClientSocial->execute($ClientID) || myDBI->dberror($qClientSocial);
  my $rClientSocial = $sClientSocial->fetchrow_hashref;
  $sMentalStat->execute($ClientID) || myDBI->dberror($qMentalStat);
  my $rMentalStat = $sMentalStat->fetchrow_hashref;
  $sClientSummary->execute($ClientID) || myDBI->dberror($qClientSummary);
  my $rClientSummary = $sClientSummary->fetchrow_hashref;
  $sDischarge->execute($ClientID,$rClientAdmit->{AdmitDate});
  my $rReAdmit = $sDischarge->fetchrow_hashref;
  my $ReAdmit = $rReAdmit->{TransDate} eq '' ? 0 : 1;
#warn qq|ReAdmit: $ClientID,$rClientAdmit->{AdmitDate},ReAdmit=$ReAdmit\n|;
  $sInsurance->execute($ClientID,1);       # select the Primary Insurance for this client.
  my $rInsurance = $sInsurance->fetchrow_hashref;
  $sCRAFFT->execute($ClientID) || myDBI->dberror("PrintClientIntakePre2017: select ClientCRAFFT ${ClientID}");
  my $rCRAFFT = $sCRAFFT->fetchrow_hashref;

  my $headings = qq|
  <companyname>${AgencyName}</companyname> 
  <companyaddr>${AgencyAddr}</companyaddr> 
  <companycsz>${AgencyCSZ}</companycsz> 
  <companyphone>${AgencyPh}</companyphone> 
  <companyfax></companyfax> 
  <assessmenttype>Initial Assessment</assessmenttype> 
|;
  my $referraldetails = main->getreferraldetails($rClientReferrals);
  my $referringphysician = main->getNPIs($rClientReferrals->{'RefPhysNPI'},'referringphysician','None');
  my $transportedby = "  <transportedby>$rClientReferrals->{'TransBy'} $rClientReferrals->{'TransAddr'} $rClientReferrals->{'TransCity'} $rClientReferrals->{'TransST'} $rClientReferrals->{'TransZip'}</transportedby>";
  my $reasonforreferral = qq|     <reasonforreferral>|.DBA->subxml($rClientReferrals->{'RefReason'}).qq|</reasonforreferral>|;
  my $referredto = main->getNPIs($rClientReferrals->{'ReferredToNPI'},'referredto','None');
  my $intakedate = qq|     <intakedate>| . DBUtil->Date($rClientAdmit->{AdmitDate},'fmt','MM/DD/YYYY') . " " . substr($rClientAdmit->{AdmitTime},0,5) . qq|</intakedate>|;
  my $readmission = qq|     <readmission>${ReAdmit}</readmission>|;
  my $csz = '';
  $csz .= qq|$rClient->{City}, | if ( $rClient->{City} ne '' );
  $csz .= qq|$rClient->{ST} | if ( $rClient->{ST} ne '' );
  $csz .= qq|$rClient->{Zip}| if ( $rClient->{Zip} ne '' );
  my ($Race,$dummy) = split(chr(253),$rClient->{'Race'});
#warn qq|PrintClientIntakePre2017: Race=${Race}\n|;
  my $identifyinfo .= qq|     <contactinfo>$rClient->{FName} $rClient->{MName} $rClient->{LName}</contactinfo>|;
  $identifyinfo    .= qq|     <contactinfo>$rClient->{Addr1}</contactinfo>| if ( $rClient->{Addr1} ne '' );
  $identifyinfo    .= qq|     <contactinfo>$rClient->{Addr2}</contactinfo>| if ( $rClient->{Addr2} ne '' );
  $identifyinfo    .= qq|     <contactinfo>${csz}</contactinfo>\n| if ( $csz ne '' );
  $identifyinfo    .= qq|     <ssn>$rClient->{SSN}</ssn>\n|;
  $identifyinfo    .= qq|     <email>$rClient->{Email}</email>\n|;
  $identifyinfo    .= qq|     <hair>| . DBA->getxref($form,'xHair',$rClient->{Hair},'Descr') . qq|</hair>\n|;
  $identifyinfo    .= qq|     <eyes>| . DBA->getxref($form,'xEyes',$rClient->{Eyes},'Descr') . qq|</eyes>\n|;
  $identifyinfo    .= qq|     <pstatus>| . DBA->getxref($form,'xParentsStatus',$rClientRelations->{'ParStat'},'Descr') . qq|</pstatus>\n|;
  $identifyinfo    .= qq|     <race>| . DBA->getxref($form,'xRaces',$Race,'Descr') . qq|</race>\n|;
  $identifyinfo    .= qq|     <gender>| . DBA->getxref($form,'xGend',$rClient->{Gend},'Descr') . qq|</gender>\n|;
  $identifyinfo    .= qq|     <carrier>| . DBA->getxref($form,'xCarrier',$rClient->{Carrier},'Descr') . qq|</carrier>\n|;
  $identifyinfo    .= qq|     <weight>$rClient->{Weight}</weight>\n|;
  $identifyinfo    .= qq|     <height>$rClient->{Height}</height>\n|;
  $identifyinfo    .= qq|     <age>| . DBUtil->Date($rClient->{DOB},'age') . qq|</age>\n|;
  $identifyinfo    .= qq|     <pob>$rClientIntake->{POB}</pob>\n|;
  $identifyinfo    .= qq|     <dob>$rClient->{DOB}</dob>\n|;
  $identifyinfo    .= qq|     <cellphn>$rClient->{MobPh}</cellphn>\n|;
  $identifyinfo    .= qq|     <workphn>$rClient->{WkPh}</workphn>\n|;
  $identifyinfo    .= qq|     <homephn>$rClient->{HmPh}</homephn>\n|;
  $identifyinfo    .= qq|     <mstatus>| . DBA->getxref($form,'xMarStat',$rClientRelations->{'MarStat'},'Descr') . qq|</mstatus>\n|;
  my $emergencycontact = main->getEmerContact($ClientID);
  my $pregnant = $rClientIntake->{PregnantDate} eq '' ? '' : ' PREGNANT';
  my $alert = qq|       <alert>| . DBA->subxml($rClientEmergency->{Alert}) . qq|${pregnant}</alert>\n|;
  my $primarycarephysician = main->getNPIs($rClientEmergency->{'PhysNPI'},'contactinfo','None');
  my $designatedhospital = main->getNPIs($rClientEmergency->{'DesigHospNPI'},'contactinfo','None');
  my $designatedpharmacy = main->getNPIs($rClientEmergency->{'PharmacyNPI'},'contactinfo','None');
  my $medicaldocs = qq|      <advdirective>$rClientEmergency->{AD}</advdirective><dnr>$rClientEmergency->{DNR}</dnr><livingwill>$rClientEmergency->{LW}</livingwill>\n|;
  my $insurancedetails = main->getInsurance($ClientID);
  my $problem1 = DBA->getxref($form,'xProblems',$rClientIntake->{Problem1},'Catagory Descr');
  my $presentingproblem = qq|      <primary>| . DBA->subxml($problem1) . qq|</primary>\n|;
  my $problem2 = DBA->getxref($form,'xProblems',$rClientIntake->{Problem2},'Catagory Descr');
  $presentingproblem   .= qq|      <secondary>| . DBA->subxml($problem2) . qq|</secondary>\n|;
  my $problem3 = DBA->getxref($form,'xProblems',$rClientIntake->{Problem3},'Catagory Descr');
  $presentingproblem   .= qq|      <tertiary>| . DBA->subxml($problem3) . qq|</tertiary>\n|;
  $presentingproblem   .= qq|      <history>| . DBA->subxml($rClientIntake->{'Problem'}) . qq|</history>\n|;
  $presentingproblem   .= DBA->setTextxrefMF($form,'xProblemSolutions',$rClientMHProblems,'','solutions','      ');
  $presentingproblem   .= qq|      <description>| . DBA->subxml($rClientMHProblems->{'OtherTherapyText'}) . qq|</description>\n|;
  my $healthhistory = qq|      <medicalhistory>\n|;
  $healthhistory   .= qq|       <t1>$rClientHealth->{'HospOverNight'}</t1>\n|;
  $healthhistory   .= qq|       <t2>| . DBA->subxml($rClientIntake->{'PhysHist'}) . qq|</t2>\n|;
  $healthhistory   .= qq|      </medicalhistory>\n|;
  $healthhistory   .= main->setXML('      ','biomedicalconditions',$rMedHx->{'BioMedical'},'','none reported');
  $healthhistory   .= qq|      <sexualhistory>\n|;
  $healthhistory   .= qq|       <sexques>$rClientHealth->{'RefusedQues'}</sexques>\n|;
  $healthhistory   .= qq|       <sexhistory>\n|;
  $healthhistory   .= qq|        <t0>| . DBUtil->Date($rClientIntake->{PregnantDate},'fmt','MM/DD/YYYY') . qq|</t0>\n|;
  $healthhistory   .= qq|        <t1>$rClientHealth->{'AgeDating'}</t1>\n|;
  if    ( $rClientHealth->{'SexPref'} eq 'H' ) { $healthhistory .= qq|        <t2>Heterosexual</t2>\n|; }
  elsif ( $rClientHealth->{'SexPref'} eq 'B' ) { $healthhistory .= qq|        <t2>Bisexual</t2>\n|; }
  elsif ( $rClientHealth->{'SexPref'} eq 'G' ) { $healthhistory .= qq|        <t2>Homosexual</t2>\n|; }
  elsif ( $rClientHealth->{'SexPref'} eq 'T' ) { $healthhistory .= qq|        <t2>Transgender</t2>\n|; }
  elsif ( $rClientHealth->{'SexPref'} eq 'Q' ) { $healthhistory .= qq|        <t2>Questioning</t2>\n|; }
  else                                  { $healthhistory .= qq|        <t2>Unknown</t2>\n|; }
  my $SexProbDescr = DBA->subxml($rClientHealth->{'SexProbDescr'});
  $healthhistory .= main->setYN('        ','t3',$rClientHealth->{'SexProb'},$SexProbDescr);
  $healthhistory   .= qq|        <t4>$rClientHealth->{'AgeSexual'}</t4>\n|;
  $healthhistory .= main->setYN('        ','t5',$rClientHealth->{'SexActive'});
  $healthhistory .= main->setYN('        ','t6',$rClientHealth->{'SexChems'});
  $healthhistory .= main->setYN('        ','t7',$rClientHealth->{'SexTrade'});
  $healthhistory .= main->setYN('        ','t8',$rClientHealth->{'SexGuilt'});
  $healthhistory   .= main->setXML('        ','std',$rClientHealth->{STD},'','none reported');
  $healthhistory   .= qq|       </sexhistory>\n|;
  $healthhistory   .= qq|      </sexualhistory>\n|;
  $healthhistory   .= main->setXML('      ','medicalallergies',$rClientIntake->{'MAR'},'','none reported');
  $healthhistory   .= main->setXML('      ','foodallergies',$rClientIntake->{'FAR'},'','none reported');
  $healthhistory   .= qq|      <neededimmunizations>| . DBA->subxml($rClientHealth->{'ImmunizeDesc'}) . qq|</neededimmunizations>\n|;
  my $medications = main->getMeds($ClientID);
  my $hdate = $rClientHealth->{'HearingDate'} eq '' ? '; Unknown date' 
            : '; '.DBUtil->Date($rClientHealth->{'HearingDate'},'fmt','MM/DD/YYYY');
  my $hearingvision = main->setYN('     ','hscreendate',$rClientHealth->{'HearingPass'},$hdate,'Unknown','Passed','Failed');
  my $vdate = $rClientHealth->{'VisionDate'} eq '' ? '; Unknown date' 
            : '; '.DBUtil->Date($rClientHealth->{'VisionDate'},'fmt','MM/DD/YYYY');
  $hearingvision .= main->setYN('     ','vscreendate',$rClientHealth->{'VisionPass'},$vdate,'Unknown','Passed','Failed');
  my $develop = main->setYN('    ','develop',$rMedHx->{'DevlFlag'},'','Unknown');
  my $prenatal = DBA->setTextxrefMF($form,'xPrenatal',$rClientDevl,'','prenatal','    ');
  my $perinatal = DBA->setTextxrefMF($form,'xPerinatal',$rClientDevl,'','perinatal','    ');
  my $postnatal = DBA->setTextxrefMF($form,'xPostnatal',$rClientDevl,'','postnatal','    ');
  my $toileting = $rClientDevl->{'ToiletProblems'} == 1 ? qq|    <problem>Bladder</problem>\n|
                : $rClientDevl->{'ToiletProblems'} == 2 ? qq|    <problem>Bowel</problem>\n|
                : $rClientDevl->{'ToiletProblems'} == 3 ? qq|    <problem>Both</problem>\n|
                : '';
  $toileting   .= $rClientDevl->{'ToiletSeverity'} == 1 ? qq|    <severity>Mild</severity>\n|
                : $rClientDevl->{'ToiletSeverity'} == 2 ? qq|    <severity>Moderate</severity>\n|
                : $rClientDevl->{'ToiletSeverity'} == 3 ? qq|    <severity>Sever</severity>\n|
                : '';
  $toileting   .= qq|    <daytime>$rClientDevl->{'ToiletDaytime'}</daytime>\n|;
  $toileting   .= qq|    <nighttime>$rClientDevl->{'ToiletNighttime'}</nighttime>\n|;
  my $emergencyroomvisits = main->setYN('     ','date',$rClientDevl->{'EmergencyRoom'},DBA->subxml($rClientDevl->{EmergencyRoomText}));
  my $motormilestones = $rClientDevl->{'MotorMilestones'} eq '1' ? qq|    <mm>Known</mm>\n| : qq|    <mm>Unknown</mm>\n|;
  $motormilestones   .= $rClientDevl->{'MMSitAlone'} ? qq|    <sit>Yes</sit>\n| : '';
  $motormilestones   .= $rClientDevl->{'MMCrawl'} ? qq|    <crawl>Yes</crawl>\n| : '';
  $motormilestones   .= $rClientDevl->{'MMWalk'} ? qq|    <walk>Yes</walk>\n| : '';
  $motormilestones   .= $rClientDevl->{'MMGoDownStairs'} ? qq|    <stairs>Yes</stairs>\n| : '';
  $motormilestones   .= $rClientDevl->{'MMRideTricycle'} ? qq|    <tricycle>Yes</tricycle>\n| : '';
  $motormilestones   .= $rClientDevl->{'MMRideBicycle'} ? qq|    <bicycle>Yes</bicycle>\n| : '';
  my $grossmotor = main->setYN('     ','t1',$rClientDevl->{'RidingToy'});
  $grossmotor   .= main->setYN('     ','t2',$rClientDevl->{'PumpingSelfOnSwing'});
  $grossmotor   .= main->setYN('     ','t3',$rClientDevl->{'LearningHowRideBike'});
  $grossmotor   .= main->setYN('     ','t4',$rClientDevl->{'ColoringPaperPencilTasks'});
  $grossmotor   .= main->setYN('     ','t5',$rClientDevl->{'EasilyFrustrated'});
  $grossmotor   .= main->setYN('     ','t6',$rClientDevl->{'PlayingSmallToys'});
  $grossmotor   .= main->setYN('     ','t7',$rClientDevl->{'UsingScissors'});
  $grossmotor   .= main->setYN('     ','t8',$rClientDevl->{'Weaker'});
  $grossmotor   .= main->setYN('     ','t9',$rClientDevl->{'AppearsStiff'});
  $grossmotor   .= main->setYN('     ','t10',$rClientDevl->{'NewMotorTasks'});
  $grossmotor   .= main->setYN('     ','t11',$rClientDevl->{'CatchingBall'});
  $grossmotor   .= main->setYN('     ','t12',$rClientDevl->{'KickingBall'});
  $grossmotor   .= main->setYN('     ','t13',$rClientDevl->{'LearningHowSwim'});
  my $selfhelpskills = main->setYN('     ','t1',$rClientDevl->{'UseOfSpoon'});
  $selfhelpskills .= main->setYN('     ','t2',$rClientDevl->{'CuttingWithKnife'});
  $selfhelpskills .= main->setYN('     ','t3',$rClientDevl->{'DressingSelf'});
  $selfhelpskills .= main->setYN('     ','t4',$rClientDevl->{'ClothingFasteners'});
  $selfhelpskills .= main->setYN('     ','t5',$rClientDevl->{'TyingShoes'});
  $selfhelpskills .= main->setYN('     ','t6',$rClientDevl->{'BrushingTeeth'});
  $selfhelpskills .= main->setYN('     ','t7',$rClientDevl->{'MakingSimpleSandwich'});
  $selfhelpskills .= main->setYN('     ','t8',$rClientDevl->{'CompletingChores'});
  $selfhelpskills .= main->setYN('     ','t9',$rClientDevl->{'MakingBed'});
  $selfhelpskills .= main->setYN('     ','t10',$rClientDevl->{'TakingBathShower'});
  $selfhelpskills .= main->setYN('     ','t11',$rClientDevl->{'WashingHair'});
  my $movementbalance = main->setYN('     ','t1',$rClientDevl->{'CarSickFrequently'});
  $movementbalance .= main->setYN('     ','t2',$rClientDevl->{'NauseaVomitsFromMovement'});
  $movementbalance .= main->setYN('     ','t3',$rClientDevl->{'WarningFeelingNausea'});
  $movementbalance .= main->setYN('     ','t4',$rClientDevl->{'SeeksSpinning'});
  $movementbalance .= main->setYN('     ','t5',$rClientDevl->{'SeeksParkrides'});
  $movementbalance .= main->setYN('     ','t6',$rClientDevl->{'HesitatesPlayground'});
  $movementbalance .= main->setYN('     ','t7',$rClientDevl->{'HasTroubleClimb'});
  $movementbalance .= main->setYN('     ','t8',$rClientDevl->{'LiftedUp'});
  $movementbalance .= main->setYN('     ','t9',$rClientDevl->{'PlacedOnAsInfant'});
  $movementbalance .= main->setYN('     ','t10',$rClientDevl->{'RocksSelfWhenStressed'});
  $movementbalance .= main->setYN('     ','t11',$rClientDevl->{'PeriodCrawling'});
  $movementbalance .= main->setYN('     ','t12',$rClientDevl->{'WalksOnToes'});
  $movementbalance .= main->setYN('     ','t13',$rClientDevl->{'ConstantlyMoving'});
  $movementbalance .= main->setYN('     ','t14',$rClientDevl->{'TripsFallsFrequently'});
  my $touch = main->setYN('     ','t1',$rClientDevl->{'UnawareBeingTouched'});
  $touch .= main->setYN('     ','t2',$rClientDevl->{'UnawareBeingHurt'});
  $touch .= main->setYN('     ','t3',$rClientDevl->{'OverlySensitive'});
  $touch .= main->setYN('     ','t4',$rClientDevl->{'ExcessivelyTicklish'});
  $touch .= main->setYN('     ','t5',$rClientDevl->{'ClothingTags'});
  $touch .= main->setYN('     ','t6',$rClientDevl->{'ResistsShorts'});
  $touch .= main->setYN('     ','t7',$rClientDevl->{'TransitioningSeasons'});
  $touch .= main->setYN('     ','t8',$rClientDevl->{'PuttingObjectsInMouth'});
  $touch .= main->setYN('     ','t9',$rClientDevl->{'BeingCuddled'});
  $touch .= main->setYN('     ','t10',$rClientDevl->{'AvoidsMessy'});
  $touch .= main->setYN('     ','t11',$rClientDevl->{'UnawareMessy'});
  $touch .= main->setYN('     ','t12',$rClientDevl->{'DislikesHairCutting'});
  $touch .= main->setYN('     ','t13',$rClientDevl->{'DislikesBath'});
  $touch .= main->setYN('     ','t14',$rClientDevl->{'VerySensitiveWater'});
  $touch .= main->setYN('     ','t15',$rClientDevl->{'DislikesNailCutting'});
  $touch .= main->setYN('     ','t16',$rClientDevl->{'PinchesBites'});
  $touch .= main->setYN('     ','t17',$rClientDevl->{'BangsHeadRepeatedly'});
  $touch .= main->setYN('     ','t18',$rClientDevl->{'CrawledFistedHands'});
  $touch .= main->setYN('     ','t19',$rClientDevl->{'SensitiveSlightBumpsScrapes'});
  $touch .= main->setYN('     ','t20',$rClientDevl->{'TendencyTouchThingsConstantly'});
  $touch .= main->setYN('     ','t21',$rClientDevl->{'FrequentlyPushesBitesHits'});
  my $auditory = main->setYN('     ','t1',$rClientDevl->{'RepeatedEarInfections'});
  $auditory .= main->setYN('     ','t2',$rClientDevl->{'DistractedBySounds'});
  $auditory .= main->setYN('     ','t3',$rClientDevl->{'OftenFailsListen'});
  $auditory .= main->setYN('     ','t4',$rClientDevl->{'SensitiveMildlyLoudNoises'});
  $auditory .= main->setYN('     ','t5',$rClientDevl->{'CoversEarsWhenSoundsAreLoud'});
  $auditory .= main->setYN('     ','t6',$rClientDevl->{'AfraidSomeNoises'});
  $auditory .= main->setYN('     ','t7',$rClientDevl->{'EnjoysHearingOwnVoice'});
  $auditory .= main->setYN('     ','t8',$rClientDevl->{'DelayedSpeechDevelopment'});
  $auditory .= main->setYN('     ','t9',$rClientDevl->{'DifficultUnderstand'});
  $auditory .= main->setYN('     ','t10',$rClientDevl->{'Stammers'});
  $auditory .= main->setYN('     ','t11',$rClientDevl->{'SpeaksIncompleteSentences'});
  $auditory .= main->setYN('     ','t12',$rClientDevl->{'ConfusedLocationSound'});
  $auditory .= main->setYN('     ','t13',$rClientDevl->{'HasDifficultyPayingAttention'});
  $auditory .= main->setYN('     ','t14',$rClientDevl->{'DoesNotSeemUnderstand'});
  $auditory .= main->setYN('     ','t15',$rClientDevl->{'TalksConstantly'});
  $auditory .= main->setYN('     ','t16',$rClientDevl->{'DiagnosisHearingLoss'});
  my $emotional = main->setYN('     ','t1',$rClientDevl->{'DoesNotAcceptChange'});
  $emotional .= main->setYN('     ','t2',$rClientDevl->{'BecomesEasilyFrustrated'});
  $emotional .= main->setYN('     ','t3',$rClientDevl->{'AptBeImpulsive'});
  $emotional .= main->setYN('     ','t4',$rClientDevl->{'MarkedMoodVariations'});
  $emotional .= main->setYN('     ','t5',$rClientDevl->{'TendsWithdrawFromGroups'});
  $emotional .= main->setYN('     ','t6',$rClientDevl->{'DoThingsHardway'});
  $emotional .= main->setYN('     ','t7',$rClientDevl->{'ChangesActivitiesFrequently'});
  $emotional .= main->setYN('     ','t8',$rClientDevl->{'BreaksToys'});
  $emotional .= main->setYN('     ','t9',$rClientDevl->{'Impatient'});
  $emotional .= main->setYN('     ','t10',$rClientDevl->{'CannotTolerateFrustration'});
  $emotional .= main->setYN('     ','t11',$rClientDevl->{'HumsTapsFingers'});
  $emotional .= main->setYN('     ','t12',$rClientDevl->{'DoesNotFinish'});
  $emotional .= main->setYN('     ','t13',$rClientDevl->{'TakesLongTimeSettledown'});
  $emotional .= main->setYN('     ','t14',$rClientDevl->{'ToysInOrder'});
  $emotional .= main->setYN('     ','t15',$rClientDevl->{'GenerallyDisorganized'});
  $emotional .= main->setYN('     ','t16',$rClientDevl->{'UnablePutThingsInOrder'});
  $emotional .= main->setYN('     ','t17',$rClientDevl->{'CannotSitThroughBoardgame'});
  $emotional .= main->setYN('     ','t18',$rClientDevl->{'DoesThingsWithoutThinking'});
  $emotional .= main->setYN('     ','t19',$rClientDevl->{'CannotPlayQuietly'});
  $emotional .= main->setYN('     ','t20',$rClientDevl->{'AlwaysOnGo'});
  $emotional .= main->setYN('     ','t21',$rClientDevl->{'RunsRatherThanWalks'});
  $emotional .= main->setYN('     ','t22',$rClientDevl->{'Fidgets'});
  $emotional .= main->setYN('     ','t23',$rClientDevl->{'CannotKeepHandsSelf'});
  $emotional .= main->setYN('     ','t24',$rClientDevl->{'DifficultVisit'});
  $emotional .= main->setYN('     ','t25',$rClientDevl->{'ResistsChangesInRoutine'});
  $emotional .= main->setYN('     ','t26',$rClientDevl->{'DifficultLeaveWithBabysitter'});
  $emotional .= main->setYN('     ','t27',$rClientDevl->{'OverlyCautious'});
  $emotional .= main->setYN('     ','t28',$rClientDevl->{'CriesSlightestReason'});
  $emotional .= main->setYN('     ','t29',$rClientDevl->{'ForgetSocialExpectations'});
  $emotional .= main->setYN('     ','t30',$rClientDevl->{'CannotTolerateNoisy'});
  $emotional .= main->setYN('     ','t31',$rClientDevl->{'NeedsCalm'});
  $emotional .= main->setYN('     ','t32',$rClientDevl->{'DoesSloppyWork'});
  $emotional .= main->setYN('     ','t33',$rClientDevl->{'IgnoresSocialRules'});
  $emotional .= main->setYN('     ','t34',$rClientDevl->{'HasNoGuilt'});
  $emotional .= main->setYN('     ','t35',$rClientDevl->{'BelievesRulesApplyOnlyOthers'});
  $emotional .= main->setYN('     ','t36',$rClientDevl->{'DoesNotSeemLearn'});
  $emotional .= main->setYN('     ','t37',$rClientDevl->{'CannotTellRight'});
  $emotional .= main->setYN('     ','t38',$rClientDevl->{'AlwaysHasExcuse'});
  $emotional .= main->setYN('     ','t39',$rClientDevl->{'ComplainsUnfairTreatment'});
  $emotional .= main->setYN('     ','t40',$rClientDevl->{'HasPoorSelfimage'});
  $emotional .= main->setYN('     ','t41',$rClientDevl->{'OverlyConcerned'});
  $emotional .= main->setYN('     ','t42',$rClientDevl->{'Irritable'});
  $emotional .= main->setYN('     ','t43',$rClientDevl->{'HasShortFuse'});
  $emotional .= main->setYN('     ','t44',$rClientDevl->{'HurtSome'});
  $emotional .= main->setYN('     ','t45',$rClientDevl->{'InsensitiveFeelingsOthers'});
  $emotional .= main->setYN('     ','t46',$rClientDevl->{'ResistsAuthority'});
  $emotional .= main->setYN('     ','t47',$rClientDevl->{'DefiantWhenDisciplined'});
  $emotional .= main->setYN('     ','t48',$rClientDevl->{'PurposelyDoesOpposite'});
  $emotional .= main->setYN('     ','t49',$rClientDevl->{'MakesUpUntruths'});
  $emotional .= main->setYN('     ','t50',$rClientDevl->{'PicksOnSmaller'});
  $emotional .= main->setYN('     ','t51',$rClientDevl->{'CannotBeTrustedAlone'});
  $emotional .= main->setYN('     ','t52',$rClientDevl->{'WantsFriends'});
  $emotional .= main->setYN('     ','t53',$rClientDevl->{'HasFewFriends'});
  $emotional .= main->setYN('     ','t54',$rClientDevl->{'HasNoCloseFriends'});
  $emotional .= main->setYN('     ','t55',$rClientDevl->{'PrefersPlayOlderChildren'});
  $emotional .= main->setYN('     ','t56',$rClientDevl->{'PrefersPlayAdults'});
  $emotional .= main->setYN('     ','t57',$rClientDevl->{'PrefersPlayYoungerChildren'});
  $emotional .= main->setYN('     ','t58',$rClientDevl->{'PhysicallyRoughOthers'});
  $emotional .= main->setYN('     ','t59',$rClientDevl->{'ExcessivelyBossy'});
  $emotional .= main->setYN('     ','t60',$rClientDevl->{'GetsIntoFights'});
  $emotional .= main->setYN('     ','t61',$rClientDevl->{'OverlySubmissive'});
  $emotional .= main->setYN('     ','t62',$rClientDevl->{'HasBeLeader'});
  $emotional .= main->setYN('     ','t63',$rClientDevl->{'ResistsSharing'});
  $emotional .= main->setYN('     ','t64',$rClientDevl->{'AssumesRoleClown'});
  $emotional .= main->setYN('     ','t65',$rClientDevl->{'AppearsDepressed'});
  my $academic = main->setYN('     ','t1',$rClientDevl->{'Scissors'});
  $academic .= main->setYN('     ','t2',$rClientDevl->{'FineHandWork'});
  $academic .= main->setYN('     ','t3',$rClientDevl->{'RecognizingLetters'});
  $academic .= main->setYN('     ','t4',$rClientDevl->{'RecognizingNumbers'});
  $academic .= main->setYN('     ','t5',$rClientDevl->{'DrawingColoringTasks'});
  $academic .= main->setYN('     ','t6',$rClientDevl->{'WritingNeatly'});
  $academic .= main->setYN('     ','t7',$rClientDevl->{'LearningMoney'});
  $academic .= main->setYN('     ','t8',$rClientDevl->{'TellingTime'});
  $handicaps .= qq|      <t1>| . DBA->subxml($rMedHx->{'AdjDis'}) . qq|</t1>\n|;
  my $mhhistory = main->getHospitalTreatments($ClientID,'MH','mhtdata');
  $mhhistory .= qq|      <suicide>\n|;
  $mhhistory .= qq|       <attempts>$rMedHx->{'AttSuicides'}</attempts>\n|;
  $mhhistory .= qq|       <last>| . DBUtil->Date($rMedHx->{'AttSuicideDate'},'fmt','MM/DD/YYYY') . qq|</last>\n|;
  $mhhistory .= main->setYN('       ','family',$rMedHx->{'FamilySuicideHx'});
  $mhhistory .= main->setYN('       ','firearms',$rMedHx->{'Firearms'});
  $mhhistory .= qq|       <noofselfharm>$rMedHx->{SelfHarm}</noofselfharm>\n|;
  $mhhistory .= qq|      </suicide>\n|;
  my $substancehistory = qq|     <timesperday>$rMedHx->{'DailyTobaccoUse'}</timesperday>\n|;
  my $alcoholhistory = $rMedHx->{AlcoholIntoxD} ? qq|I have been intoxicated. | : qq|I have not been intoxicated. |;
  $alcoholhistory .= $rMedHx->{AlcoholUseL} ? qq|I used alcohol in last 30 days.| : qq|I did not use alcohol in last 30 days.|;
  $substancehistory .= qq|     <history>${alcoholhistory}</history>\n|;
  $substancehistory .= main->setYN('       ','usedalcohol',$rMedHx->{'AlcoholIntoxL'});
  $substancehistory .= qq|     <nooftimes>$rMedHx->{'AlcoholDTs'}</nooftimes>\n|;
  $substancehistory .= main->getSA($ClientID);
  $substancehistory .= qq|     <historyofivdrug>\n|;
  $substancehistory .= main->setYN('      ','history',$rMedHx->{'DrugInject'});
  $substancehistory .= qq|      <noofdrug>$rMedHx->{'OD'}</noofdrug>\n|;
  $substancehistory .= qq|     </historyofivdrug>\n|;
  my $craftscreen = main->setYN('     ','t1',$rCRAFFT->{'q1'});
  $craftscreen .= main->setYN('     ','t2',$rCRAFFT->{'q2'});
  $craftscreen .= main->setYN('     ','t3',$rCRAFFT->{'q3'});
  $craftscreen .= main->setYN('     ','t4',$rCRAFFT->{'q4'});
  $craftscreen .= main->setYN('     ','t5',$rCRAFFT->{'q5'});
  $craftscreen .= main->setYN('     ','t6',$rCRAFFT->{'q6'});
  my $CRAFFT = $rCRAFFT->{'q1'}+$rCRAFFT->{'q2'}+$rCRAFFT->{'q3'}+$rCRAFFT->{'q4'}+$rCRAFFT->{'q5'}+$rCRAFFT->{'q6'};
  $craftscreen .= $CRAFFT > 1 ? qq|     <t7>Yes</t7>\n| : qq|     <t7>No</t7>\n|;
  my $sat = main->getHospitalTreatments($ClientID,'AA','satdata',1);
  $sat .= main->getHospitalTreatments($ClientID,'DA','sat2data',1);
  my $familyhistorydrug = $rMedHx->{'PrenatalExp'} eq '' ? qq|     <prenatal>No</prenatal>\n|
                        : qq|  <prenatal>| . DBA->subxml(DBA->getxref($form,'xDrugs',$rMedHx->{'PrenatalExp'},'Descr')) . qq|</prenatal>\n|;
  $familyhistorydrug .= main->getFamily($ClientID,'AbuseAlcohol=1 or AbuseDrugs=1','substanceabuse');
  $familyhistorydrug .= main->getFamily($ClientID,'AbusePsych=1','psychproblems');
  $familyhistorydrug .= qq|     <orientation> | . DBA->subxml($rMedHx->{'ToChange'}) . qq|</orientation>\n|;
  my $gambling = main->setYN('     ','t1',$rGambling->{'History'});
  $gambling .= main->setYN('     ','t2',$rGambling->{'BetMore'});
  $gambling .= main->setYN('     ','t3',$rGambling->{'Lie'});
  $gambling .= main->setYN('     ','t4',$rGambling->{'State'},'','','Positive','Negative');
  $gambling .= main->setYN('     ','t5',$rGambling->{'Debts'},DBA->subxml($rGambling->{DebtsText}));
  my $text = DBA->subxml($rGambling->{FinanceStatusText});
  if    ( $rGambling->{'FinanceStatus'} eq 'G' ) { $gambling .= qq|     <t6>Good ${text}</t6>\n|; }
  elsif ( $rGambling->{'FinanceStatus'} eq 'F' ) { $gambling .= qq|     <t6>Fair ${text}</t6>\n|; }
  elsif ( $rGambling->{'FinanceStatus'} eq 'P' ) { $gambling .= qq|     <t6>Poor ${text}</t6>\n|; }
  $gambling .= main->setYN('     ','t7',$rGambling->{'LostTime'});
  $gambling .= main->setYN('     ','t8',$rGambling->{'LifeUnhappy'});
  $gambling .= main->setYN('     ','t9',$rGambling->{'Reputation'});
  $gambling .= main->setYN('     ','t10',$rGambling->{'FeltRemorse'});
  $gambling .= main->setYN('     ','t11',$rGambling->{'PayDebts'});
  $gambling .= main->setYN('     ','t12',$rGambling->{'Ambition'});
  $gambling .= main->setYN('     ','t13',$rGambling->{'WinBack'});
  $gambling .= main->setYN('     ','t14',$rGambling->{'WinMore'});
  $gambling .= main->setYN('     ','t15',$rGambling->{'RunOut'});
  $gambling .= main->setYN('     ','t16',$rGambling->{'Borrowed'});
  $gambling .= main->setYN('     ','t17',$rGambling->{'Sold'});
  $gambling .= main->setYN('     ','t18',$rGambling->{'Reluctant'});
  $gambling .= main->setYN('     ','t19',$rGambling->{'Careless'});
  $gambling .= main->setYN('     ','t20',$rGambling->{'Longer'});
  $gambling .= main->setYN('     ','t21',$rGambling->{'Escape'});
  $gambling .= main->setYN('     ','t22',$rGambling->{'IllegalAct'});
  $gambling .= main->setYN('     ','t23',$rGambling->{'DifSleeping'});
  $gambling .= main->setYN('     ','t24',$rGambling->{'Arguments'});
  $gambling .= main->setYN('     ','t25',$rGambling->{'Celebrate'});
  $gambling .= main->setYN('     ','t26',$rGambling->{'SelfDestruct'});
##  $rGambling_Treatment    # yes/no then list
  $gambling .= main->getHospitalTreatments($ClientID,'GA','gamblingtdata');
##  $rGambling_Addictions   # yes/no then list
  $gambling .= DBA->setTextxrefMF($form,'xBehavioralAddictions',$rGambling,DBA->subxml($rGambling->{OtherAddictionsText}),'history','     ');
  $gambling .= qq|     <description>| . DBA->subxml($rGambling->{AddictionsText}) . qq|</description>\n|;
  my $traumaques .= main->setYN('     ','traumaques',$rClientTrauma->{'Psych'});
$traumaques .= qq|    <Table>\n|;
  $traumaques .= qq|    <Row>\n|;           # Row 0
  $traumaques .= main->setYN('     ','office',$rClientTrauma->{'ThreatOfForce'});
  $traumaques .= qq|     <office>$rClientTrauma->{'ThreatOfForceTimes'}</office>\n|;
  $traumaques .= qq|     <office>$rClientTrauma->{'ThreatOfForceAge'}</office>\n|;
  $traumaques .= qq|    </Row>\n|;
  $traumaques .= qq|    <Row>\n|;           # Row 1
  $traumaques .= main->setYN('     ','office',$rClientTrauma->{'Robbed'});
  $traumaques .= qq|     <office>$rClientTrauma->{'RobbedTimes'}</office>\n|;
  $traumaques .= qq|     <office>$rClientTrauma->{'RobbedAge'}</office>\n|;
  $traumaques .= qq|    </Row>\n|;
  $traumaques .= qq|    <Row>\n|;           # Row 2
  $traumaques .= main->setYN('     ','office',$rClientTrauma->{'BreakInHomeNT'});
  $traumaques .= qq|     <office>$rClientTrauma->{'BreakInHomeNTTimes'}</office>\n|;
  $traumaques .= qq|     <office>$rClientTrauma->{'BreakInHomeNTAge'}</office>\n|;
  $traumaques .= qq|    </Row>\n|;
  $traumaques .= qq|    <Row>\n|;           # Row 3
  $traumaques .= main->setYN('     ','office',$rClientTrauma->{'BreakInHome'});
  $traumaques .= qq|     <office>$rClientTrauma->{'BreakInHomeTimes'}</office>\n|;
  $traumaques .= qq|     <office>$rClientTrauma->{'BreakInHomeAge'}</office>\n|;
  $traumaques .= qq|    </Row>\n|;
  $traumaques .= qq|    <Row>\n|;           # Row 4,5
  $rClientTrauma->{'Accident'} = 1 if ( $rClientTrauma->{'AccidentText'} ne '' );
  $traumaques .= main->setYN('     ','office',$rClientTrauma->{'Accident'});
  $traumaques .= qq|     <office>$rClientTrauma->{'AccidentTimes'}</office>\n|;
  $traumaques .= qq|     <office>$rClientTrauma->{'AccidentAge'}</office>\n|;
  $traumaques .= qq|    </Row>\n|;
  $traumaques .= qq|    <Row><office>| . DBA->subxml($rClientTrauma->{'AccidentText'}) . qq|</office></Row>\n|;
  $traumaques .= qq|    <Row>\n|;           # Row 6,7
  $rClientTrauma->{'NaturalDisaster'} = 1 if ( $rClientTrauma->{'NaturalDisasterText'} ne '' );
  $traumaques .= main->setYN('     ','office',$rClientTrauma->{'NaturalDisaster'});
  $traumaques .= qq|     <office>$rClientTrauma->{'NaturalDisasterTimes'}</office>\n|;
  $traumaques .= qq|     <office>$rClientTrauma->{'NaturalDisasterAge'}</office>\n|;
  $traumaques .= qq|    </Row>\n|;
  $traumaques .= qq|    <Row><office>| . DBA->subxml($rClientTrauma->{'NaturalDisasterText'}) . qq|</office></Row>\n|;
  $traumaques .= qq|    <Row>\n|;           # Row 8,9
  $rClientTrauma->{'ManMadeDisaster'} = 1 if ( $rClientTrauma->{'ManMadeDisasterText'} ne '' );
  $traumaques .= main->setYN('     ','office',$rClientTrauma->{'ManMadeDisaster'});
  $traumaques .= qq|     <office>$rClientTrauma->{'ManMadeDisasterTimes'}</office>\n|;
  $traumaques .= qq|     <office>$rClientTrauma->{'ManMadeDisasterAge'}</office>\n|;
  $traumaques .= qq|    </Row>\n|;
  $traumaques .= qq|    <Row><office>| . DBA->subxml($rClientTrauma->{'ManMadeDisasterText'}) . qq|</office></Row>\n|;
  $traumaques .= qq|    <Row>\n|;           # Row 10
  $traumaques .= main->setYN('     ','office',$rClientTrauma->{'DangerChemicals'});
  $traumaques .= qq|     <office>$rClientTrauma->{'DangerChemicalsTimes'}</office>\n|;
  $traumaques .= qq|     <office>$rClientTrauma->{'DangerChemicalsAge'}</office>\n|;
  $traumaques .= qq|    </Row>\n|;
  $traumaques .= qq|    <Row>\n|;           # Row 11,12
  $rClientTrauma->{'Injured'} = 1 if ( $rClientTrauma->{'InjuredText'} ne '' );
  $traumaques .= main->setYN('     ','office',$rClientTrauma->{'Injured'});
  $traumaques .= qq|     <office>$rClientTrauma->{'InjuredTimes'}</office>\n|;
  $traumaques .= qq|     <office>$rClientTrauma->{'InjuredAge'}</office>\n|;
  $traumaques .= qq|    </Row>\n|;
  $traumaques .= qq|    <Row><office>| . DBA->subxml($rClientTrauma->{'InjuredText'}) . qq|</office></Row>\n|;
  $traumaques .= qq|    <Row>\n|;           # Row 13,14
  $rClientTrauma->{'FearKilled'} = 1 if ( $rClientTrauma->{'FearKilledText'} ne '' );
  $traumaques .= main->setYN('     ','office',$rClientTrauma->{'FearKilled'});
  $traumaques .= qq|     <office>$rClientTrauma->{'FearKilledTimes'}</office>\n|;
  $traumaques .= qq|     <office>$rClientTrauma->{'FearKilledAge'}</office>\n|;
  $traumaques .= qq|    </Row>\n|;
  $traumaques .= qq|    <Row><office>| . DBA->subxml($rClientTrauma->{'FearKilledText'}) . qq|</office></Row>\n|;
  $traumaques .= qq|    <Row>\n|;           # Row 15,16
  $rClientTrauma->{'SomeoneKilled'} = 1 if ( $rClientTrauma->{'SomeoneKilledText'} ne '' );
  $traumaques .= main->setYN('     ','office',$rClientTrauma->{'SomeoneKilled'});
  $traumaques .= qq|     <office>$rClientTrauma->{'SomeoneKilledTimes'}</office>\n|;
  $traumaques .= qq|     <office>$rClientTrauma->{'SomeoneKilledAge'}</office>\n|;
  $traumaques .= qq|    </Row>\n|;
  $traumaques .= qq|    <Row><office>| . DBA->subxml($rClientTrauma->{'SomeoneKilledText'}) . qq|</office></Row>\n|;
  $traumaques .= qq|    <Row>\n|;           # Row 17,18
  $rClientTrauma->{'DeadBody'} = 1 if ( $rClientTrauma->{'DeadBodyText'} ne '' );
  $traumaques .= main->setYN('     ','office',$rClientTrauma->{'DeadBody'});
  $traumaques .= qq|     <office>$rClientTrauma->{'DeadBodyTimes'}</office>\n|;
  $traumaques .= qq|     <office>$rClientTrauma->{'DeadBodyAge'}</office>\n|;
  $traumaques .= qq|    </Row>\n|;
  $traumaques .= qq|    <Row><office>| . DBA->subxml($rClientTrauma->{'DeadBodyText'}) . qq|</office></Row>\n|;
  $traumaques .= qq|    <Row>\n|;           # Row 19,20
  $rClientTrauma->{'CloseMurder'} = 1 if ( $rClientTrauma->{'CloseMurderText'} ne '' );
  $traumaques .= main->setYN('     ','office',$rClientTrauma->{'CloseMurder'});
  $traumaques .= qq|     <office>$rClientTrauma->{'CloseMurderTimes'}</office>\n|;
  $traumaques .= qq|     <office>$rClientTrauma->{'CloseMurderAge'}</office>\n|;
  $traumaques .= qq|    </Row>\n|;
  $traumaques .= qq|    <Row><office>| . DBA->subxml($rClientTrauma->{'CloseMurderText'}) . qq|</office></Row>\n|;
  $traumaques .= qq|    <Row>\n|;           # Row 21,22
  $rClientTrauma->{'CloseDie'} = 1 if ( $rClientTrauma->{'CloseDieText'} ne '' );
  $traumaques .= main->setYN('     ','office',$rClientTrauma->{'CloseDie'});
  $traumaques .= qq|     <office>$rClientTrauma->{'CloseDieTimes'}</office>\n|;
  $traumaques .= qq|     <office>$rClientTrauma->{'CloseDieAge'}</office>\n|;
  $traumaques .= qq|    </Row>\n|;
  $traumaques .= qq|    <Row><office>| . DBA->subxml($rClientTrauma->{'CloseDieText'}) . qq|</office></Row>\n|;
  $traumaques .= qq|    <Row>\n|;           # Row 23,24
  $rClientTrauma->{'SeriousIllness'} = 1 if ( $rClientTrauma->{'SeriousIllnessText'} ne '' );
  $traumaques .= main->setYN('     ','office',$rClientTrauma->{'SeriousIllness'});
  $traumaques .= qq|     <office>$rClientTrauma->{'SeriousIllnessTimes'}</office>\n|;
  $traumaques .= qq|     <office>$rClientTrauma->{'SeriousIllnessAge'}</office>\n|;
  $traumaques .= qq|    </Row>\n|;
  $traumaques .= qq|    <Row><office>| . DBA->subxml($rClientTrauma->{'SeriousIllnessText'}) . qq|</office></Row>\n|;
  $traumaques .= qq|    <Row>\n|;           # Row 25,26
  $rClientTrauma->{'CloseThreat'} = 1 if ( $rClientTrauma->{'CloseThreatText'} ne '' );
  $traumaques .= main->setYN('     ','office',$rClientTrauma->{'CloseThreat'});
  $traumaques .= qq|     <office>$rClientTrauma->{'CloseThreatTimes'}</office>\n|;
  $traumaques .= qq|     <office>$rClientTrauma->{'CloseThreatAge'}</office>\n|;
  $traumaques .= qq|    </Row>\n|;
  $traumaques .= qq|    <Row><office>| . DBA->subxml($rClientTrauma->{'CloseThreatText'}) . qq|</office></Row>\n|;
  $traumaques .= qq|    <Row>\n|;           # Row 27,28
#warn qq|Combat=$rClientTrauma->{'Combat'}\n|;
#warn qq|Combat=$rClientTrauma->{'CombatText'}\n|;
  $rClientTrauma->{'Combat'} = 1 if ( $rClientTrauma->{'CombatText'} ne '' );
#warn qq|Combat=$rClientTrauma->{'Combat'}\n|;
  $traumaques .= main->setYN('     ','office',$rClientTrauma->{'Combat'});
  $traumaques .= qq|     <office>$rClientTrauma->{'CombatTimes'}</office>\n|;
  $traumaques .= qq|     <office>$rClientTrauma->{'CombatAge'}</office>\n|;
  $traumaques .= qq|    </Row>\n|;
  $traumaques .= qq|    <Row><office>| . DBA->subxml($rClientTrauma->{'CombatText'}) . qq|</office></Row>\n|;
  $traumaques .= qq|    <Row>\n|;           # Row 29,30
  $rClientTrauma->{'ForcedSex'} = 1 if ( $rClientTrauma->{'ForcedSexText'} ne '' );
  $traumaques .= main->setYN('     ','office',$rClientTrauma->{'ForcedSex'});
  $traumaques .= qq|     <office>$rClientTrauma->{'ForcedSexTimes'}</office>\n|;
  $traumaques .= qq|     <office>$rClientTrauma->{'ForcedSexAge'}</office>\n|;
  $traumaques .= qq|    </Row>\n|;
  $traumaques .= qq|    <Row><office>| . DBA->subxml($rClientTrauma->{'ForcedSexText'}) . qq|</office></Row>\n|;
  $traumaques .= qq|    <Row>\n|;           # Row 31,32
  $rClientTrauma->{'ForcedTouch'} = 1 if ( $rClientTrauma->{'ForcedTouchText'} ne '' );
  $traumaques .= main->setYN('     ','office',$rClientTrauma->{'ForcedTouch'});
  $traumaques .= qq|     <office>$rClientTrauma->{'ForcedTouchTimes'}</office>\n|;
  $traumaques .= qq|     <office>$rClientTrauma->{'ForcedTouchAge'}</office>\n|;
  $traumaques .= qq|    </Row>\n|;
  $traumaques .= qq|    <Row><office>| . DBA->subxml($rClientTrauma->{'ForcedTouchText'}) . qq|</office></Row>\n|;
  $traumaques .= qq|    <Row>\n|;           # Row 33
  $traumaques .= main->setYN('     ','office',$rClientTrauma->{'ForcedContact'});
  $traumaques .= qq|     <office>$rClientTrauma->{'ForcedContactTimes'}</office>\n|;
  $traumaques .= qq|     <office>$rClientTrauma->{'ForcedContactAge'}</office>\n|;
  $traumaques .= qq|    </Row>\n|;
  $traumaques .= qq|    <Row>\n|;           # Row 34
  $traumaques .= main->setYN('     ','office',$rClientTrauma->{'CloseAttack'});
  $traumaques .= qq|     <office>$rClientTrauma->{'CloseAttackTimes'}</office>\n|;
  $traumaques .= qq|     <office>$rClientTrauma->{'CloseAttackAge'}</office>\n|;
  $traumaques .= qq|    </Row>\n|;
  $traumaques .= qq|    <Row>\n|;           # Row 35
  $traumaques .= main->setYN('     ','office',$rClientTrauma->{'CloseInjured'});
  $traumaques .= qq|     <office>$rClientTrauma->{'CloseInjuredTimes'}</office>\n|;
  $traumaques .= qq|     <office>$rClientTrauma->{'CloseInjuredAge'}</office>\n|;
  $traumaques .= qq|    </Row>\n|;
  $traumaques .= qq|    <Row>\n|;           # Row 36
  $traumaques .= main->setYN('     ','office',$rClientTrauma->{'HardSpank'});
  $traumaques .= qq|     <office>$rClientTrauma->{'HardSpankTimes'}</office>\n|;
  $traumaques .= qq|     <office>$rClientTrauma->{'HardSpankAge'}</office>\n|;
  $traumaques .= qq|    </Row>\n|;
  $traumaques .= qq|    <Row>\n|;           # Row 37,38
  $rClientTrauma->{'Other'} = 1 if ( $rClientTrauma->{'OtherDescr'} ne '' );
  $traumaques .= main->setYN('     ','office',$rClientTrauma->{'Other'});
  $traumaques .= qq|     <office>$rClientTrauma->{'OtherTimes'}</office>\n|;
  $traumaques .= qq|     <office>$rClientTrauma->{'OtherAge'}</office>\n|;
  $traumaques .= qq|    </Row>\n|;
  $traumaques .= qq|    <Row><office>| . DBA->subxml($rClientTrauma->{'OtherDescr'}) . qq|</office></Row>\n|;
$traumaques .= qq|    </Table>\n|;
  my $violent = main->getFamily($ClientID,"AbuseEmotion='V' or AbuseEmotion='P' or AbuseEmotion='B' or AbusePhysical='V' or AbusePhysical='P' or AbusePhysical='B' or AbuseSexual='V' or AbuseSexual='P' or AbuseSexual='B'",'violentdata');
  $violent .= main->setYN('     ','battered',$rMedHx->{'BatteredWP'});
  $violent .= main->setYN('     ','witnessed',$rClientIntake->{'WitnessDV'});
  my $trauma = main->getHospitalTreatments($ClientID,'TR','traumatdata');
  my $familyhistory = main->getFamilyHistory($ClientID,$rClient,$rClientRelations);
  my $familyrelations = main->getFamilyRelations($ClientID,$rClient,$rClientIntake,$rGuardianHistory,$rClientRelations);
  my $familysiblings = main->getFamily($ClientID,'xRelationship.Sibling=1','fsdata');
  my $residence = DBA->subxml(DBA->getxref($form,'xResidence',$rClientRelations->{'Residence'},'Descr'));
  my $currentliving = qq|     <type>${residence}</type>\n|;
  $currentliving .= main->getNPIs($rClientRelations->{'FacIDNPI'},'outofhome','None');
# Placement types...
# 1 Not in out-of-home treatment
# 2 Residential treatment
# 3 Specialized community group home
# 4 Foster home
# 5 Group home
# 6 Other
  my $placement = $residence =~ /residential care facility/i ? 'Residential treatment'
                : $residence =~ /specialized community group home/i ? 'Specialized community group home'
                : $residence =~ /foster/i ? 'Foster home'
                : $residence =~ /group home/i ? 'Group home' : 'Not in out-of-home treatment';
  $currentliving .= qq|     <placement>${placement}</placement>\n|;
  $currentliving .= qq|     <admit> | . DBUtil->Date($rClientRelations->{'ResAdmitDate'},'fmt','MM/DD/YYYY') . qq|</admit>\n|;
  $currentliving .= qq|     <level>|.DBA->getxref($form,'xGHLevel',$rClientRelations->{'GHLevel'},'Descr').qq|</level>\n|;
  $currentliving .= $rClientRelations->{'FacIDNPI'} ? qq|     <ppos>Yes</ppos>| : qq|     <ppos>No</ppos>|;
  $currentliving .= qq|     <placements>$rClientRelations->{'ResNum'}</placements>\n|;
  $currentliving .= qq|     <past90days>$rMedHx->{'RestrictivePlacement'}</past90days>\n|;
  my $correctional = $rClientLegal->{'InJail'} ? 'In Jail ' : '';
  $correctional .= $residence =~ /prison/i ? 'In Prison ' : ''; 
  $currentliving .= qq|     <correctional>${correctional}</correctional>\n|;
  $currentliving .= main->setYN('      ','chronic',$rClientRelations->{'HomelessLong'});
  $currentliving .= main->setYN('      ','frequent',$rClientRelations->{'HomelessMany'});
  my $familyinhome = main->getFamily($ClientID,'xRelationship.Sibling=0 and ClientFamily.Inhome=1','fidata');
  $familyinhome .= qq|     <arrangement>\n|;
  $familyinhome .= qq|      <usual>| . DBA->subxml(DBA->getxref($form,'xLivingArrASI',$rClientRelations->{'FamUsualLivArr'},'ID Descr')) . qq|</usual>\n|;
  $familyinhome .= main->setYN('      ','satisfied',$rClientRelations->{'SatUsualLivArr'},'','','Indifferent','No');
  $familyinhome .= qq|     </arrangement>\n|;
  my $resources = main->getIncome($ClientID);
  $resources .= qq|     <number>$rClientResources->{'IncomeDeps'}</number>\n|;
  $resources .= qq|     <able>$rClientResources->{'AbleToPay'}</able>\n|;
  $resources .= qq|     <concerns>\n|;
  $resources .= main->setYN('      ','t1',$rClientResources->{'ValidDL'});
  $resources .= main->setYN('      ','t2',$rClientResources->{'AutoForUse'});
  $resources .= main->setYN('      ','t3',$rClientResources->{'AbleToCare'});
  $resources .= main->setYN('      ','t4',$rClientResources->{'AbleToMeetNeeds'});
  $resources .= main->setYN('      ','t5',$rClientResources->{'AbleToMeetLegal'});
  $resources .= main->setYN('      ','t6',$rClientResources->{'RecoveryNeeds'});
  $resources .= main->setYN('      ','t7',$rClientResources->{'BasicNeeds'},DBA->subxml($rClientResources->{'FinDesc'}));
  $resources .= qq|     </concerns>\n|;
  $resources .= qq|     <currentsupport>\n|;
  my $active = $rClientResources->{'ActiveSupport'} ? 'Active' : 'Inactive';
  $resources .= main->setYN('      ','receives',$rClientResources->{'RegSupport'},$active);
  $resources .= main->setYN('      ','active',$rClientResources->{'ActiveSupport'});
  $resources .= main->setYN('      ','constitutes',$rClientResources->{'MajSupport'});
  $resources .= main->setYN('      ','family',$rClientResources->{'FamilySupport'});
  $resources .= main->setYN('      ','employer',$rClientResources->{'EmplSupport'});
  $resources .= main->setYN('      ','church',$rClientResources->{'ChurchSupport'});
  $resources .= main->setYN('      ','selfhelp',$rClientResources->{'SelfHelp'});
  $resources .= qq|      <days>$rClientResources->{'SelfHelp30'}</days>\n|;
  $resources .= qq|     </currentsupport>\n|;
  my $legal = main->getLegal($ClientID,$rClient,$rClientLegal);
  my ($Ethnicity,$dummy) = split(chr(253),$rClient->{'Ethnicity'});
#warn qq|PrintClientIntakePre2017: Ethnicity=${Ethnicity}\n|;
  my $cultural = qq|     <ethnicity>\n|;
  $cultural .= qq|      <origin>| . DBA->getxref($form,'xEthnicity',$Ethnicity,'Descr') . qq|</origin>\n|;
  $cultural .= qq|      <tribal>| . DBA->subxml(DBA->getxref($form,'xTribe',$rClientSocial->{'Tribe'},'Descr')) . qq|</tribal>\n|;
  $cultural .= qq|     </ethnicity>\n|;
#warn qq|Gang=$rClientSocial->{'Gang'}, Other=$rClientSocial->{'OtherAffiliation'}n|;
  $cultural .= qq|     <traditional>| . DBA->subxml($rClientSocial->{'TribePart'}) . qq|</traditional>\n|;
  $cultural .= qq|     <gang>| . DBA->subxml($rClientSocial->{'Gang'}) . qq|</gang>\n|;
  $cultural .= qq|     <gangvalues>| . DBA->subxml($rClientSocial->{'GangValue'}) . qq|</gangvalues>\n|;
  $cultural .= qq|     <other>| . DBA->subxml($rClientSocial->{'OtherAffiliation'}) . qq|</other>\n|;
  $cultural .= qq|     <othervalues>| . DBA->subxml($rClientSocial->{'OtherValue'}) . qq|</othervalues>\n|;
  $cultural .= qq|     <unique>| . DBA->subxml($rClientSocial->{'UniqueYou'}) . qq|</unique>\n|;
  $cultural .= qq|     <important>| . DBA->subxml($rClientSocial->{'ImportantYou'}) . qq|</important>\n|;
  my $language = qq|     <lang>\n|;
  $language .= qq|      <primary>| . DBA->getxref($form,'xLanguages',$rClientSocial->{'PreLang'},'English') . qq|</primary>\n|;
  $language .= qq|      <secondary>| . DBA->getxref($form,'xLanguages',$rClientSocial->{'SecLang'},'English') . qq|</secondary>\n|;
  $language .= main->setYN('      ','reads',$rClientSocial->{'ReadEnglish'});
  $language .= main->setYN('      ','writes',$rClientSocial->{'WriteEnglish'});
  $language .= main->setYN('      ','speaks',$rClientSocial->{'SpeakEnglish'});
  $language .= qq|     </lang>\n|;
  $language .= qq|     <detailed>| . DBA->subxml($rClientSocial->{'LangProbs'}) . qq|</detailed>\n|;
  my $religion = qq|     <population>$rClientSocial->{'RaisedIn'}</population>\n|;
  $religion .= qq|     <clientprefers>$rClientSocial->{'PreferLive'}</clientprefers>\n|;
  $religion .= main->setYN('     ','clientsees',$rClientSocial->{'Healer'});
  $religion .= $rClientSocial->{'ReligionDiff'} eq '' ? 
                qq|     <clientfeels>No</clientfeels>\n| : qq|     <clientfeels>Yes</clientfeels>\n|;
  $religion .= qq|     <howclientfeel>| . DBA->subxml($rClientSocial->{'ReligionDiff'}) . qq|</howclientfeel>\n|;
  $religion .= qq|     <meaninggod>| . DBA->subxml($rClientSocial->{'ReligionMean'}) . qq|</meaninggod>\n|;
  $religion .= main->setYN('     ','churchchild',$rClientSocial->{'ReligionChild'});
  $religion .= qq|     <religionchild>| . DBA->getxref($form,'xReligiousAffiliation',$rClientSocial->{'Religion'},'Descr') . qq|</religionchild>\n|;
  $religion .= main->setYN('     ','churchnow',$rClientSocial->{'ReligionAttend'});
  $religion .= qq|     <religionnow>| . DBA->getxref($form,'xReligiousAffiliation',$rClientSocial->{'ReligionName'},'Descr') . qq|</religionnow>\n|;
  $religion .= main->setYN('     ','clientbehav',$rClientSocial->{'ReligionViews'});
  $religion .= $rClientSocial->{'ReligionExp'} eq '' ? 
                qq|     <clientexp>No</clientexp>\n| : qq|     <clientexp>Yes</clientexp>\n|;
  $religion .= qq|     <howclientexp>| . DBA->subxml($rClientSocial->{'ReligionExp'}) . qq|</howclientexp>\n|;
  my $leisure = qq|     <recreational>\n|;
  if    ( $rClientSocial->{'WhoSpendTime'} eq '1' ) { $leisure .= qq|      <freetime>Family</freetime>\n|; }
  elsif ( $rClientSocial->{'WhoSpendTime'} eq '2' ) { $leisure .= qq|      <freetime>Friends</freetime>\n|; }
  elsif ( $rClientSocial->{'WhoSpendTime'} eq '3' ) { $leisure .= qq|      <freetime>Alone</freetime>\n|; }
  else                                              { $leisure .= qq|      <freetime></freetime>\n|; }
  $leisure .= main->setYN('      ','satisfied',$rClientSocial->{'SatSpendTime'},'','','Indifferent','No');
  $leisure .= qq|      <closefriends>$rClientSocial->{'NumCloseFriends'}</closefriends>\n|;
  $leisure .= qq|     </recreational>\n|;
  $leisure .= qq|     <interests>| . DBA->subxml($rClientSocial->{'Hobby'}) . qq|</interests>\n|;
  $leisure .= qq|     <preferred>| . DBA->subxml($rClientSocial->{'RecDesc'}) . qq|</preferred>\n|;
  my $eduhistory = qq|     <attainment>\n|;
  $eduhistory .= qq|      <highest>| . DBA->getxref($form,'xSchoolGrades',$rClientEducation->{SchoolGrade},'Concept') . qq|</highest>\n|;
  $eduhistory .= qq|      <repeated>| . DBA->getxref($form,'xSchoolGrades',$rClientEducation->{RepeatGrade},'Concept') . ' ' . DBA->subxml($rClientIntake->{'RepeatGradeDesc'}) . qq|</repeated>\n|;
  $eduhistory .= qq|      <lastschool>|.DBA->getxref($form,'xSchoolSites',$rClientIntake->{'LastSchoolName'},'SchoolSite').qq|</lastschool>\n|;
  $eduhistory .= qq|      <district>|.DBA->getxref($form,'xSchoolDistricts',$rClientIntake->{'LastSchoolDist'},'DistrictName').qq|</district>\n|;
  $eduhistory .= qq|      <number>$rClientEducation->{'MonthsTechEd'}</number>\n|;
  $eduhistory .= qq|      <subjectsliked>| . DBA->getxref($form,'xSubjects',$rClientIntake->{SubjectsLike},'Descr') . qq|</subjectsliked>\n|;
  $eduhistory .= qq|      <subjectsdisliked>| . DBA->getxref($form,'xSubjects',$rClientIntake->{SubjectsDisLike},'Descr') . qq|</subjectsdisliked>\n|;
  $eduhistory .= qq|     </attainment>\n|;
  $eduhistory .= qq|     <learning>\n|;
  $eduhistory .= qq|      <ability>| . DBA->getxref($form,'xLearnAbility',$rClientIntake->{LearnAbility},'Descr') . qq|</ability>\n|;
  $eduhistory .= qq|      <iqscore>$rClientIntake->{'IQ'}</iqscore>\n|;
  $eduhistory .= qq|     </learning>\n|;
  $eduhistory .= qq|     <daycare>\n|;
  $eduhistory .= qq|      <past90days>$rClientIntake->{'AbsentDayCare'}</past90days>\n|;
  $eduhistory .= qq|     </daycare>\n|;
  my $education = qq|     <school>\n|;
  $education .= qq|      <status>| . DBA->getxref($form,'xSchoolStat',$rClientIntake->{SchoolStat},'Descr') . qq|</status>\n|;
  $education .= qq|      <gpa>| . DBA->getxref($form,'xSchoolGrades',$rClientEducation->{CurrentGrade},'Concept') . ' ' . DBA->subxml($rClientIntake->{'GPA'}) . qq|</gpa>\n|;
  $education .= qq|      <special>| . DBA->getxref($form,'xSpecEd',$rClientIntake->{SpecEd},'Descr') . qq|</special>\n|;
  $education .= main->setYN('      ','iep',$rClientIntake->{'IEP'});
  $education .= qq|      <spedtime>| . DBA->getxref($form,'xPeriod',$rClientIntake->{SpecEdLength},'Descr') . qq|</spedtime>\n|;
  $education .= qq|      <spedgrade>| . DBA->getxref($form,'xSchoolGrades',$rClientEducation->{SpecEdStart},'Concept') . qq|</spedgrade>\n|;
  $education .= qq|     </school>\n|;
  $education .= qq|     <absent>$rClientIntake->{'AbsentSchool'}</absent>\n|;
  $education .= qq|     <suspended>$rClientIntake->{'SuspendedSchool'}</suspended>\n|;
  $education .= qq|     <collaboration>| . DBA->subxml($rClientIntake->{'SchoolCollab'}) . qq|</collaboration>\n|;
  my $vochistory = qq|     <employment>\n|;
  $vochistory .= qq|      <status>| . DBA->getxref($form,'xEmplStat',$rClient->{EmplStat},'Descr') . qq|</status>\n|;
  $vochistory .= qq|      <type>| . DBA->getxref($form,'xEmplType',$rClient->{EmplType},'Descr') . qq|</type>\n|;
  $vochistory .= qq|      <lastwork>| . DBA->subxml($rClientIntake->{'JobDesc'}) . qq|</lastwork>\n|;
  $vochistory .= qq|      <length>| . DBA->getxref($form,'xPeriod',$rClientIntake->{JobLength},'Descr') . qq|</length>\n|;
  $vochistory .= qq|      <last> | . DBUtil->Date($rClientIntake->{JobLengthLast},'fmt','MM/DD/YYYY') . qq|</last>\n|;
  $vochistory .= qq|      <typework>| . DBA->subxml($rClientIntake->{'JobDescLast'}) . qq|</typework>\n|;
  $vochistory .= qq|      <skills>| . DBA->subxml($rClientIntake->{'JobSkills'}) . qq|</skills>\n|;
  $vochistory .= qq|     </employment>\n|;
  if ( $rClientIntake->{'MilFlag'} eq '0' ) { $vochistory .= qq|      <military>None</military>\n|; }
  elsif ( $rClientIntake->{'MilFlag'} eq '1' ) { $vochistory .= qq|      <military>Active</military>\n|; }
  elsif ( $rClientIntake->{'MilFlag'} eq '2' ) { $vochistory .= qq|      <military>Reserved</military>\n|; }
  elsif ( $rClientIntake->{'MilFlag'} eq '3' ) { $vochistory .= qq|      <military>Discharged</military>\n|; }
  elsif ( $rClientIntake->{'MilFlag'} eq '4' ) { $vochistory .= qq|      <military>Retired</military>\n|; }
  $vochistory .= qq|      <branch>| . DBA->getxref($form,'xMilBranch',$rClientIntake->{MilBranch},'Descr') . qq|</branch>\n|;
  $vochistory .= qq|      <discharge>| . DBA->getxref($form,'xMilDis',$rClientIntake->{MilDis},'Descr') . qq|</discharge>\n|;
  $vochistory .= qq|      <relatives>| . DBA->getxref($form,'xRelationship',$rClientIntake->{MilRel},'Descr') . qq|</relatives>\n|;
  my $functionlevel = DBA->setTextxrefMF($form,'xStressors',$rClientSocial,'','stressors','     ');
  $functionlevel .= qq|     <level>| . DBA->subxml($rClientSocial->{'RelSocialDesc'}) . qq|</level>\n|;
  my $msexam = qq|     <physical>\n|;
  $msexam .= main->xText($form,'MHAppearance',$rMentalStat,'','','t1','      ');
  $msexam .= main->xText($form,'MHDress',$rMentalStat,'','','t2','      ');
  $msexam .= main->xText($form,'MHHygiene',$rMentalStat,'','','t3','      ');
  $msexam .= main->xText($form,'MHNutrition',$rMentalStat,'','','t4','      ');
  $msexam .= main->xText($form,'MHProstheticDevices',$rMentalStat,'','','t5','      ');
  $msexam .= qq|     </physical>\n|;
  $msexam .= qq|     <interviewbehavior>\n|;
  $msexam .= main->xText($form,'MHPosture',$rMentalStat,'','','t1','      ');
  $msexam .= main->xText($form,'MHFacial',$rMentalStat,'','','t2','      ');
  $msexam .= qq|     </interviewbehavior>\n|;
  $msexam .= qq|     <motoractivity>\n|;
  $msexam .= main->xText($form,'MHGait',$rMentalStat,'','','t1','      ');
  $msexam .= main->xText($form,'MHMotor',$rMentalStat,'','','t2','      ');
  $msexam .= qq|     </motoractivity>\n|;
  $msexam .= qq|     <speech>\n|;
  $msexam .= main->xText($form,'MHSpeechQuan',$rMentalStat,'','','t1','      ');
  $msexam .= main->xText($form,'MHSpeechQual',$rMentalStat,'','','t2','      ');
  $msexam .= main->xText($form,'MHSpeechImpair',$rMentalStat,'','','t3','      ');
  $msexam .= qq|     </speech>\n|;
  $msexam .= qq|     <iprelation>\n|;
  $msexam .= main->xText($form,'MHIPRel',$rMentalStat,'','','t1','      ');
  $msexam .= main->xText($form,'MHAffect',$rMentalStat,'','','t2','      ');
  $msexam .= main->xText($form,'MHMood',$rMentalStat,'','','t3','      ');
  $msexam .= main->xText($form,'MHThoughtProcesses',$rMentalStat,'','','t4','      ');
  $msexam .= main->xText($form,'MHPreoccupations',$rMentalStat,'','','t5','      ');
  $msexam .= main->xText($form,'MHDelusions',$rMentalStat,'','','t6','      ');
  $msexam .= main->xText($form,'MHHallucinations',$rMentalStat,'','','t7','      ');
  $msexam .= main->xText($form,'MHConsciousness',$rMentalStat,'','','t8','      ');
  $msexam .= main->xText($form,'MHOrientation',$rMentalStat,'','','t9','      ');
  $msexam .= main->xText($form,'MHAttention',$rMentalStat,'','','t10','      ');
  $msexam .= main->xText($form,'MHMemory',$rMentalStat,'','','t11','      ');
  $msexam .= main->xText($form,'MHIntAbility',$rMentalStat,'','','t12','      ');
  $msexam .= main->xText($form,'MHInsight',$rMentalStat,'','','t13','      ');
  $msexam .= main->xText($form,'MHJudgement',$rMentalStat,'','','t14','      ');
  $msexam .= main->xText($form,'MHIndependence',$rMentalStat,'','','t15','      ');
  $msexam .= main->xText($form,'MHMentalExam',$rMentalStat,'','','t16','      ');
  $msexam .= qq|     </iprelation>\n|;
  my $diagnoses = qq|     <conclusions>\n|;
  $diagnoses .= qq|     </conclusions>\n|;
  $diagnoses .= qq|     <axis11></axis11>\n|;
  $diagnoses .= qq|     <axis12></axis12>\n|;
  $diagnoses .= qq|     <axis13></axis13>\n|;
  $diagnoses .= qq|     <axis21></axis21>\n|;
  $diagnoses .= qq|     <axis22></axis22>\n|;
  $diagnoses .= qq|     <axis3></axis3>\n|;
  $diagnoses .= qq|     <axis4></axis4>\n|;
  $diagnoses .= qq|     <axis51></axis51>\n|;
  $diagnoses .= qq|     <axis52></axis52>\n|;
  my $summary = '';
  $summary .= qq|      <strengths>| . DBA->subxml($rClientSummary->{'S1'}) . qq|</strengths>\n| if ( $rClientSummary->{'S1'} ne '' );
  $summary .= qq|      <strengths>| . DBA->subxml($rClientSummary->{'S2'}) . qq|</strengths>\n| if ( $rClientSummary->{'S2'} ne '' );
  $summary .= qq|      <strengths>| . DBA->subxml($rClientSummary->{'S3'}) . qq|</strengths>\n| if ( $rClientSummary->{'S3'} ne '' );
  $summary .= qq|      <strengths>| . DBA->subxml($rClientSummary->{'S4'}) . qq|</strengths>\n| if ( $rClientSummary->{'S4'} ne '' );
  $summary .= qq|      <needs>| . DBA->subxml($rClientSummary->{'L1'}) . qq|</needs>\n| if ( $rClientSummary->{'L1'} ne '' );
  $summary .= qq|      <needs>| . DBA->subxml($rClientSummary->{'L2'}) . qq|</needs>\n| if ( $rClientSummary->{'L2'} ne '' );
  $summary .= qq|      <needs>| . DBA->subxml($rClientSummary->{'L3'}) . qq|</needs>\n| if ( $rClientSummary->{'L3'} ne '' );
  $summary .= qq|      <needs>| . DBA->subxml($rClientSummary->{'L4'}) . qq|</needs>\n| if ( $rClientSummary->{'L4'} ne '' );
  $summary .= qq|     <preferences>| . DBA->subxml($rClientSummary->{'Prefs'}) . qq|</preferences>\n|;
  $summary .= qq|     <goal>| . DBA->subxml($rClientSummary->{'Overall'}) . qq|</goal>\n|;
  $summary .= qq|     <stage>| . DBA->getxref($form,'xStageOfChange',$rClientSummary->{Stage},'Descr') . qq|</stage>\n|;
  my $isummary = qq|    <isummary>| . DBA->subxml($rClientIntake->{'Summary'}) . qq|</isummary>\n|;
  my $recommendations = qq|     <recommend>\n|;
  $recommendations .= qq|      <levelofcare>| . DBA->getxref($form,'xLOC',$rClientIntake->{LOC},'Descr') . qq|</levelofcare>\n|;
  $recommendations .= qq|      <servicefocus>| . DBA->getxref($form,'xServiceFocus',$rClientIntake->{'ServiceFocus'},'Descr') . qq|</servicefocus>\n|;
  $recommendations .= qq|     </recommend>\n|;
  $recommendations .= qq|     <services>| . DBA->getxref($form,'xServices',$rClientIntake->{Services},'Descr') . qq|</services>\n|;
  $recommendations .= main->getNPIs($rClientIntake->{ReferralsNPI},'referrals','None',1);
  my $completedby = qq|    <completedby>|.DBA->setProvCreds($form,$rClientAdmit->{'ProvID'},$rInsurance->{InsID},$rClientAdmit->{'AdmitDate'},$rClientAdmit->{'AdmitTime'}).qq|</completedby>\n|;
##
  my $html = qq|
  <fident>${ClientName} (${ClientID})</fident> 
  <fstamp>${DT}</fstamp> 
  <Page1>
    <recordid>$rClientAdmit->{'ID'}</recordid> 
${headings}
    <referraldetails>
${referraldetails}
    </referraldetails>
    <flowed>
${referringphysician}
${transportedby}
${reasonforreferral}
${referredto}
    </flowed>
    <intakeinfoheader>
${intakedate}
${readmission}
    </intakeinfoheader>
    <identifyinfo>
${identifyinfo}
    </identifyinfo>
    <emergencycontact>
${emergencycontact}
    </emergencycontact>
    <healthcareinfo>
      <healthcareinfoalert>
${alert}
      </healthcareinfoalert>
      <healthcareinfo>
        <primarycarephysician>
${primarycarephysician}
        </primarycarephysician>
        <designatedhospital>
${designatedhospital}
        </designatedhospital>
        <designatedpharmacy>
${designatedpharmacy}
        </designatedpharmacy>
      </healthcareinfo>
      <medicaldocs>
${medicaldocs}
      </medicaldocs>
    </healthcareinfo>
    <insurance>
      <insurancedetails>
${insurancedetails}
      </insurancedetails>
    </insurance>
    <presentingproblem>
${presentingproblem}
    </presentingproblem>
    <healthhistory>
${healthhistory}
    </healthhistory>
    <medications>
${medications}
    </medications>
    <hearingvision>
${hearingvision}
    </hearingvision>
${develop}
${prenatal}
${perinatal}
${postnatal}
    <toileting>
${toileting}
    </toileting>
    <emergencyroomvisits>
${emergencyroomvisits}
    </emergencyroomvisits>
    <motormilestones>
${motormilestones}
    </motormilestones>
    <grossmotor>
${grossmotor}
    </grossmotor>
    <selfhelpskills>
${selfhelpskills}
    </selfhelpskills>
    <movementbalance>
${movementbalance}
    </movementbalance>
    <touch>
${touch}
    </touch>
    <auditory>
${auditory}
    </auditory>
    <emotional>
${emotional}
    </emotional>
    <academic>
${academic}
    </academic>
    <handicaps>
${handicaps}
    </handicaps>
    <mhhistory>
${mhhistory}
    </mhhistory>
    <substancehistory>
${substancehistory}
    </substancehistory>
    <craftscreen>
${craftscreen}
    </craftscreen>
    <sat>
${sat}
    </sat>
    <familyhistorydrug>
${familyhistorydrug}
    </familyhistorydrug>
    <gambling>
${gambling}
    </gambling>
    <traumaques>
${traumaques}
    </traumaques>
    <violent>
${violent}
    </violent>
    <trauma>
${trauma}
    </trauma>
    <familyhistory>
${familyhistory}
    </familyhistory>
    <familyrelations>
${familyrelations}
    </familyrelations>
    <familysiblings>
${familysiblings}
    </familysiblings>
    <currentliving>
${currentliving}
    </currentliving>
    <familyinhome>
${familyinhome}
    </familyinhome>
    <resources>
${resources}
    </resources>
    <legal>
${legal}
    </legal>
    <cultural>
${cultural}
    </cultural>
    <language>
${language}
    </language>
    <religion>
${religion}
    </religion>
    <leisure>
${leisure}
    </leisure>
    <eduhistory>
${eduhistory}
    </eduhistory>
    <education>
${education}
    </education>
    <vochistory>
${vochistory}
    </vochistory>
    <functionlevel>
${functionlevel}
    </functionlevel>
    <msexam>
${msexam}
    </msexam>
    <diagnoses>
${diagnoses}
    </diagnoses>
    <summary>
${summary}
    </summary>
${isummary}
    <recommendations>
${recommendations}
    </recommendations>
${completedby}
   </Page1>
|;
  return($html);
}
############################################################################
sub getreferraldetails
{
  my ($self,$r) = @_;
  my ($out,$cnt) = ('',0);
  if ( $r->{'ReferredBy1NPI'} )
  {
    my $rxNPI = DBA->selxref($form,'xNPI','NPI',$r->{'ReferredBy1NPI'});
    $out .= qq|     <referral1>| . DBA->subxml($rxNPI->{'ProvOrgName'}) . qq|</referral1>\n|;
    $out .= qq|     <date1> | . DBUtil->Date($r->{'RefDate'},'fmt','MM/DD/YYYY') . qq|</date1>\n|;
    if ( $r->{ReferredCont1} )
    { $out .= qq|     <contact1>$r->{'ReferredCont1'}</contact1>\n|; }
    else
    { $out .= qq|     <contact1>$rxNPI->{'ProvPrefix'} $rxNPI->{'ProvFirstName'} $rxNPI->{'ProvLastName'}</contact1>\n|; }
    $out .= qq|     <phn1>$rxNPI->{'WkPh'}</phn1>\n|;
  }
  if ( $r->{'ReferredBy2NPI'} )
  {
    my $rxNPI = DBA->selxref($form,'xNPI','NPI',$r->{'ReferredBy2NPI'});
    $out .= qq|     <referral2>| . DBA->subxml($rxNPI->{'ProvOrgName'}) . qq|</referral2>\n|;
    $out .= qq|     <date2> | . DBUtil->Date($r->{'RefDate2'},'fmt','MM/DD/YYYY') . qq|</date2>\n|;
    if ( $r->{ReferredCont2} )
    { $out .= qq|     <contact2>$r->{'ReferredCont2'}</contact2>\n|; }
    else
    { $out .= qq|     <contact2>$rxNPI->{'ProvPrefix'} $rxNPI->{'ProvFirstName'} $rxNPI->{'ProvLastName'}</contact2>\n|; }
    $out .= qq|     <phn2>$rxNPI->{'WkPh'}</phn2>\n|;
  }
  return($out);
}
sub getNPIs
{
  my ($self,$NPIs,$Fld,$None,$Hdr) = @_;
  my ($out,$cnt) = ('',0);
#warn qq|getNPIs: NPIs=$NPIs\n|;
  $out = qq|     <${Fld}>Name / Address / Phone / NPI</${Fld}>\n| if ( $Hdr );
  foreach my $NPI ( split(chr(253),$NPIs) )
  {
#warn qq|getNPIs: NPI=$NPI\n|;
    my $rxNPI = DBA->selxref($form,'xNPI','NPI',$NPI);
    my $name = $rxNPI->{'EntityTypeCode'} == 1
             ? DBA->subxml("$rxNPI->{'ProvLastName'}, $rxNPI->{'ProvFirstName'}")
             : DBA->subxml($rxNPI->{'ProvOrgName'});
    my $zip = length($rxNPI->{Zip}) == 9 ? substr($rxNPI->{Zip},0,5).'-'.substr($rxNPI->{Zip},5,4) : $rxNPI->{Zip};
    my $addr = "$rxNPI->{'Addr1'}, $rxNPI->{'Addr2'}, $rxNPI->{'City'}, $rxNPI->{'ST'}, ${zip}";
    if ( $Fld eq 'contactinfo' )
    {
      $out .= qq|         <contactinfo>${name}</contactinfo>\n|;
      $out .= qq|         <contactinfo>$rxNPI->{Addr1}</contactinfo>\n| if ( $rxNPI->{Addr1} ne '' );
      $out .= qq|         <contactinfo>$rxNPI->{Addr2}</contactinfo>\n| if ( $rxNPI->{Addr2} ne '' );
      my $csz = '';
      $csz .= qq|$rxNPI->{City}, | if ( $rxNPI->{City} ne '' );
      $csz .= qq|$rxNPI->{ST} | if ( $rxNPI->{ST} ne '' );
      $csz .= $zip if ( $zip ne '' );
      $out .= qq|         <contactinfo>${csz}</contactinfo>\n| if ( $csz ne '' );
      $out .= qq|         <workphn>$rxNPI->{WkPh}</workphn>\n| if ( $rxNPI->{WkPh} ne '' );
      $out .= qq|         <fax>$rxNPI->{Fax}</fax>\n| if ( $rxNPI->{Fax} ne '' );
    }
    else { $out .= qq|     <${Fld}>${name} / ${addr} / $rxNPI->{WkPh} / $rxNPI->{NPI}</${Fld}>\n|; }
    $cnt++;
  }
  $out = qq|     <${Fld}>${None}</${Fld}>\n| unless ( $cnt );
  return($out);
}
# Parent/Guardian
# ---------------
sub getEmerContact
{
  my ($self,$ClientID) = @_;
  my ($out,$cnt) = ('',0);
  my $qClientFamily = qq|select * from ClientFamily where ClientID=? and (Guardian=1 or EmerContact=1) order by Age|;
  my $sClientFamily = $dbh->prepare($qClientFamily);
  $sClientFamily->execute($ClientID);
  my $fi = 0;
  while ( $rClientFamily = $sClientFamily->fetchrow_hashref )
  {
    $fi++;
    $out .= qq|     <ec${fi}>\n|;
    $out .= qq|      <contactinfo>$rClientFamily->{FName} $rClientFamily->{MName} $rClientFamily->{LName}</contactinfo>\n|;
    $out .= qq|      <contactinfo>$rClientFamily->{Addr1}</contactinfo>\n| if ( $rClientFamily->{Addr1} ne '' );
    $out .= qq|      <contactinfo>$rClientFamily->{Addr2}</contactinfo>\n| if ( $rClientFamily->{Addr2} ne '' );
    my $csz = '';
    $csz .= qq|$rClientFamily->{City}, | if ( $rClientFamily->{City} ne '' );
    $csz .= qq|$rClientFamily->{ST} | if ( $rClientFamily->{ST} ne '' );
    $csz .= qq|$rClientFamily->{Zip}| if ( $rClientFamily->{Zip} ne '' );
    $out .= qq|      <contactinfo>${csz}</contactinfo>\n| if ( $csz ne '' );
    $out .= qq|      <relationship>| . DBA->getxref($form,'xRelationship',$rClientFamily->{Rel},'Descr') . qq|</relationship>\n|;
    $out .= qq|      <email>$rClientFamily->{Email}</email>\n|;
    $out .= qq|      <homephn>$rClientFamily->{HmPh}</homephn>\n|;
    $out .= qq|      <workphn>$rClientFamily->{WkPh}</workphn>\n|;
    $out .= qq|      <cellphn>$rClientFamily->{Cell}</cellphn>\n|;
    $out .= qq|      <carrier>| . DBA->getxref($form,'xCarrier',$rClientFamily->{Carrier},'Descr') . qq|</carrier>\n|;
    $out .= qq|      <legalguardian>$rClientFamily->{Guardian}</legalguardian>\n|;
    $out .= qq|      <emergencycontact>$rClientFamily->{EmerContact}</emergencycontact>\n|;
    $out .= qq|      <specialinstructions>$rClientFamily->{Comments}</specialinstructions>\n|;
    $out .= qq|     </ec${fi}>\n|;
  }
  $sClientFamily->finish();
  $out .= qq|     <ec1>     <contactinfo>None</contactinfo></ec1>\n| unless ( $fi );
  return($out);
}
# Marriage / Significant Other
# ---------------
sub getFamilyHistory
{
  my ($self,$ClientID,$rClient,$rClientRelations) = @_;
  my ($out,$cnt) = ('',0);
  $out .= qq|     <fhdata>\n|;
  $out .= qq|      <marstat>| . DBA->getxref($form,'xMarStat',$rClientRelations->{'MarStat'},'Descr') . qq|</marstat>\n|;
  my $length = $rClientRelations->{'MarStatY'} eq '' && $rClientRelations->{'MarStatM'} eq '' ? 'unanswered'
             : $rClientRelations->{'MarStatY'} eq '' ? "$rClientRelations->{'MarStatM'} months"
             : $rClientRelations->{'MarStatM'} eq '' ? "$rClientRelations->{'MarStatY'} years"
             : "$rClientRelations->{'MarStatY'} years $rClientRelations->{'MarStatM'} months";
  $out .= qq|      <length>${length}</length>\n|;
  $out .= qq|      <number>$rClientRelations->{'MarStatTimes'}</number>\n|;
  $out .= qq|      <RelHistory>|.DBA->subxml($rClientRelations->{'RelHistory'}).qq|</RelHistory>\n|;
  my $qClientFamily = qq|select * from ClientFamily where ClientID=? and Rel='SO' order by Age|;
  my $sClientFamily = $dbh->prepare($qClientFamily);
  $sClientFamily->execute($ClientID);
  if ( $rClientFamily = $sClientFamily->fetchrow_hashref )
  {
    $out .= qq|      <sigother>$rClientFamily->{FName} $rClientFamily->{MName} $rClientFamily->{LName}</sigother>\n|;
    $out .= qq|      <sigother>$rClientFamily->{Addr1}</sigother>\n| if ( $rClientFamily->{Addr1} ne '' );
    $out .= qq|      <sigother>$rClientFamily->{Addr2}</sigother>\n| if ( $rClientFamily->{Addr2} ne '' );
    my $csz = '';
    $csz .= qq|$rClientFamily->{City}, | if ( $rClientFamily->{City} ne '' );
    $csz .= qq|$rClientFamily->{ST} | if ( $rClientFamily->{ST} ne '' );
    $csz .= qq|$rClientFamily->{Zip}| if ( $rClientFamily->{Zip} ne '' );
    $out .= qq|      <sigother>${csz}</sigother>\n| if ( $csz ne '' );
    #$out .= qq|      <relationship>| . DBA->getxref($form,'xRelationship',$rClientFamily->{Rel},'Descr') . qq|</relationship>\n|;
    #$out .= qq|      <email>$rClientFamily->{Email}</email>\n|;
    $out .= qq|      <homephn>$rClientFamily->{HmPh}</homephn>\n|;
    $out .= qq|      <workphn>$rClientFamily->{WkPh}</workphn>\n|;
    $out .= qq|      <cellphn>$rClientFamily->{Cell}</cellphn>\n|;
    #$out .= qq|      <carrier>| . DBA->getxref($form,'xCarrier',$rClientFamily->{Carrier},'Descr') . qq|</carrier>\n|;
    #$out .= qq|      <legalguardian>$rClientFamily->{Guardian}</legalguardian>\n|;
    #$out .= qq|      <emergencycontact>$rClientFamily->{EmerContact}</emergencycontact>\n|;
    #$out .= qq|      <specialinstructions>$rClientFamily->{Comments}</specialinstructions>\n|;
    $cnt++;
  }
  $out .= qq|      <sigother>None</sigother>\n| unless ( $cnt );
  $out .= qq|     </fhdata>\n|;
  $sClientFamily->finish();
  return($out);
}
sub getFamily
{
  my ($self,$ClientID,$type,$tag) = @_;
  my ($out,$cnt,$cntIP,$cntOP) = ('',0,0,0);
  my $qClientFamily = qq|select ClientFamily.*,xRelationship.Descr as Relation from ClientFamily left join okmis_config.xRelationship on xRelationship.ID=ClientFamily.Rel where ClientFamily.ClientID=? and (${type}) order by Age|;
#warn qq|getFamily: q=\n${qClientFamily}\n|;
  my $sClientFamily = $dbh->prepare($qClientFamily);
  $sClientFamily->execute($ClientID);
  while ( my $rClientFamily = $sClientFamily->fetchrow_hashref )
  {
    $out .= qq|     <${tag}>\n|;
    $out .= qq|      <name>$rClientFamily->{LName}, $rClientFamily->{FName} $rClientFamily->{MName}</name>\n|;
    $out .= qq|      <relation>$rClientFamily->{Relation}</relation>\n|;
    $out .= qq|      <age>$rClientFamily->{Age}</age>\n|;
    $out .= main->setYN('      ','inhome',$rClientFamily->{'Inhome'});
    $out .= qq|      <rating>$rClientFamily->{RelValue}</rating>\n|;
    $out .= qq|      <why>| . DBA->subxml($rClientFamily->{RelValueDesc}) . qq|</why>\n|;
    if ( $rClientFamily->{AbuseEmotion} eq 'V' ) { $out .= qq|      <emotional>Victim</emotional>\n|; }
    elsif ( $rClientFamily->{AbuseEmotion} eq 'P' ) { $out .= qq|      <emotional>Perpetrator</emotional>\n|; }
    elsif ( $rClientFamily->{AbuseEmotion} eq 'B' ) { $out .= qq|      <emotional>Both</emotional>\n|; }
    else { $out .= qq|      <emotional>None</emotional>\n|; }
    if ( $rClientFamily->{AbusePhysical} eq 'V' ) { $out .= qq|      <physical>Victim</physical>\n|; }
    elsif ( $rClientFamily->{AbusePhysical} eq 'P' ) { $out .= qq|      <physical>Perpetrator</physical>\n|; }
    elsif ( $rClientFamily->{AbusePhysical} eq 'B' ) { $out .= qq|      <physical>Both</physical>\n|; }
    else { $out .= qq|      <physical>None</physical>\n|; }
    if ( $rClientFamily->{AbuseSexual} eq 'V' ) { $out .= qq|      <sexual>Victim</sexual>\n|; }
    elsif ( $rClientFamily->{AbuseSexual} eq 'P' ) { $out .= qq|      <sexual>Perpetrator</sexual>\n|; }
    elsif ( $rClientFamily->{AbuseSexual} eq 'B' ) { $out .= qq|      <sexual>Both</sexual>\n|; }
    else { $out .= qq|      <sexual>None</sexual>\n|; }
    if ( $rClientFamily->{AbuseAlcohol} ) { $out .= qq|      <type>Alcohol</type>\n|; }
    elsif ( $rClientFamily->{AbuseDrugs} ) { $out .= qq|      <type>Drugs</type>\n|; }
    $out .= qq|     </${tag}>\n|;
    $cnt++;
  }
  $sClientFamily->finish();
  $out = qq|     <${tag}><name>None</name></${tag}>\n| unless ( $cnt );
  return($out);
}
sub getFamilyRelations
{
  my ($self,$ClientID,$rClient,$rClientIntake,$rGuardianHistory,$rClientRelations) = @_;
  my ($out,$cnt) = ('',0);
  $out .= qq|     <frdata>\n|;
  $out .= qq|      <cfs>| . DBA->getxref($form,'xLivesWith',$rClientRelations->{'LivesWith'},'Descr') . qq|</cfs>\n|;
  $out .= qq|      <description>| . DBA->subxml($rClientRelations->{'LivesWithDesc'}) . qq|</description>\n|;
  $out .= qq|      <parents>| . DBA->getxref($form,'xParentsStatus',$rClientRelations->{'ParStat'},'Descr') . qq|</parents>\n|;
  $out .= qq|      <lived>$rGuardianHistory->{FName} $rGuardianHistory->{MName} $rGuardianHistory->{LName}</lived>\n|;
  $out .= qq|      <length>| . DBA->subxml($rGuardianHistory->{GrdnComments}) . qq|</length>\n|;
  $out .= qq|      <usual>| . DBA->getxref($form,'xRelationship',$rClientRelations->{'DisciplineBy'},'Descr') . qq|</usual>\n|;
  $out .= qq|      <discipline>| . DBA->subxml($rClientRelations->{'DisciplineDesc'}) . qq|</discipline>\n|;
  $out .= qq|      <punishment>| . DBA->subxml($rClientrelations->{'PunishDesc'}) . qq|</punishment>\n|;
  $out .= qq|     </frdata>\n|;
  return($out);
}
# Insurance
# ---------
sub getInsurance
{
  my ($self,$ClientID) = @_;
  my ($out,$cnt) = ('',0);
  my @tags = ('','primary','secondary','tertiary');
  my $sGuarantor = $dbh->prepare("select * from Guarantor where InsuranceID=?");
  for ($i=1; $i<=3; $i++)
  {
    $sInsurance->execute($ClientID,$i);
    if ( my $rInsurance = $sInsurance->fetchrow_hashref )
    {
      $sGuarantor->execute($rInsurance->{InsNumID});
      my $rGuarantor = $sGuarantor->fetchrow_hashref;
      (my $pholder = qq|$rGuarantor->{FName} $rGuarantor->{MName} $rGuarantor->{LName}|) =~ s/^\s*(.*?)\s*$/$1/g;
      $out .= qq|     <@tags[$i]>\n|;
      $out .= qq|      <name>| . DBA->getxref($form,'xInsurance',$rInsurance->{InsID},'Name') . qq|</name>\n|;
      $out .= qq|      <paphn>$rInsurance->{Ph1}</paphn>\n|;
      $out .= qq|      <pholder>${pholder}</pholder>\n|;
      $out .= qq|      <pnumber>$rInsurance->{InsIDNum}</pnumber>\n|;
      $out .= qq|      <deductible>| . sprintf("%.2f",$rInsurance->{Deductible}) . qq|</deductible>\n|;
      $out .= qq|      <copay>| . sprintf("%.2f",$rInsurance->{Copay}) . qq|</copay>\n|;
      $out .= qq|     </@tags[$i]>\n|;
      if ( $i == 1 )
      {
        (my $name = qq|$rGuarantor->{FName} $rGuarantor->{MName} $rGuarantor->{LName}|) =~ s/^\s*(.*?)\s*$/$1/g;
        $out .= qq|     <guarantor>\n|;
        $out .= qq|      <name>${name}</name>\n|;
        $out .= qq|      <name>$rGuarantor->{Addr1}</name>\n| if ( $rGuarantor->{Addr1} ne '' );
        $out .= qq|      <name>$rGuarantor->{Addr2}</name>\n| if ( $rGuarantor->{Addr2} ne '' );
        my $csz = '';
        $csz .= qq|$rGuarantor->{City}, | if ( $rGuarantor->{City} ne '' );
        $csz .= qq|$rGuarantor->{ST} | if ( $rGuarantor->{ST} ne '' );
        $csz .= qq|$rGuarantor->{Zip}| if ( $rGuarantor->{Zip} ne '' );
        $out .= qq|      <name>${csz}</name>\n| if ( $csz ne '' );
        $out .= qq|      <relationship>| . DBA->getxref($form,'xRelationship',$rGuarantor->{ClientRel},'Descr') . qq|</relationship>\n|;
        $out .= qq|      <homephn>$rGuarantor->{HmPh}</homephn>\n|;
        $out .= qq|      <cellphn>$rGuarantor->{MobPh}</cellphn>\n|;
        $out .= qq|      <workphn>$rGuarantor->{WkPh}</workphn>\n|;
        $out .= qq|      <employer>$rGuarantor->{Empl}</employer>\n|;
        $out .= qq|      <email>$rGuarantor->{Email}</email>\n|;
        $out .= qq|      <deductible>| . sprintf("%.2f",$rInsurance->{Deductible}) . qq|</deductible>\n|;
        $out .= qq|      <copay>| . sprintf("%.2f",$rInsurance->{Copay}) . qq|</copay>\n|;
        $out .= qq|     </guarantor>\n|;
      }
    }
  }
  $sGuarantor->finish();
  return($out);
}
# set Medications
# ---------------
sub getMeds
{
  my ($self,$ClientID) = @_;
  my ($out,$cnt) = ('',0);
  my $rMeds = DBA->getMeds($form,$ClientID);
  foreach my $f ( sort keys %{ $rMeds } )
  {
#warn qq|rMeds: ${f} = $rMeds->{$f}\n|;
    my ($date,$time) = split(' ',$rMeds->{$f}->{'DrugDate'});
    my $drugdate = DBUtil->Date($date,'fmt','MM/DD/YYYY');
    $out .= qq|      <medications>\n|;
    $out .= qq|       <physician>$rMeds->{$f}->{'PhysicianName'}</physician>\n|;
    $out .= qq|       <medication>$rMeds->{$f}->{'DrugInfo'}</medication>\n|;
    $out .= qq|       <drugtype>$rMeds->{$f}->{'DrugType'}</drugtype>\n|;
    $out .= qq|       <drugdate>${drugdate}</drugdate>\n|;
    $out .= qq|       <reason></reason>\n|;
    $out .= qq|      </medications>\n|;
    $cnt++;
  }
  $out = qq|      <medications><physician>None</physician></medications>\n| unless ( $cnt );
  return($out);
}
# Mental Health Treatments
# ------------------------
sub getHospitalTreatments
{
  my ($self,$ClientID,$type,$tag,$totals) = @_;
  my ($out,$txt,$cnt,$cntDO,$cntIP,$cntOP) = ('','',0,0,0,0);
  my $qMH = qq|select * from Hospital where ClientID=? and Type like '${type}%' order by IntDate desc|;
  my $sMH = $dbh->prepare($qMH);
  $sMH->execute($ClientID);
  while ( my $rMH = $sMH->fetchrow_hashref )
  {
    $cntDO++ if ( $rMH->{'Type'} =~ /DO$/ );
    $cnt++;
#warn qq|getHospital ${cnt}: Type=$rMH->{'Type'}, cntDO=${cntDO}\n|;
    if ( $cnt <= 3 )
    {
      my $npi = $rMH->{HospIDNPI} ? $rMH->{HospIDNPI} : $rMH->{FacIDNPI};
      $cntIP++ if ( $rMH->{HospIDNPI} );
      $cntOP++ if ( $rMH->{FacIDNPI} );
      my $rxNPI = DBA->selxref($form,'xNPI','NPI',$npi);
      $txt .= qq|     <${tag}>\n|;
      $txt .= qq|      <where>| . DBA->subxml($rxNPI->{'ProvOrgName'}) . qq|</where>\n|;
      $txt .= qq|      <type>| . DBA->getxref($form,'xHospType',$rMH->{'Type'},'Text') . qq|</type>\n|;
      $txt .= qq|      <when>| . DBUtil->Date($rMH->{IntDate},'fmt','MM/DD/YYYY') . qq|</when>\n|;
      $txt .= qq|      <howlong>$rMH->{'Length'}</howlong>\n|;
      $txt .= qq|      <reason>| . DBA->subxml($rMH->{Reason}) . qq|</reason>\n|;
      $txt .= qq|     </${tag}>\n|;
    }
  }
  $sMH->finish();
  $out .= qq|     <${tag}hdr>\n      <total>${cnt}</total>\n      <detox>${cntDO}</detox>\n     </${tag}hdr>\n| if ( $totals );
  $out .= $txt;
#  $out .= qq|     <${tag}><where>None</where></${tag}>\n| unless ( $cnt );
  return($out);
}
# Substance Abuse Treatments
# --------------------------
sub getSA
{
  my ($self,$ClientID) = @_;
  my ($out,$cnt,$cntIP,$cntOP) = ('',0,0,0);
  my $qSA = qq|select * from SAbuse where ClientID=? order by Age|;
  my $sSA = $dbh->prepare($qSA);
  $sSA->execute($ClientID);
  while ( my $rSA = $sSA->fetchrow_hashref )
  {
    $out .= qq|     <currentdata>\n|;
    $out .= $rSA->{Active} ? qq|      <current>Yes</current>\n| : qq|      <current>No</current>\n|;
    $out .= qq|      <drug>| . DBA->getxref($form,'xDrugs',$rSA->{Drug},'Descr') . qq|</drug>\n|;
    $out .= qq|      <methodofuse>| . DBA->getxref($form,'xMethods',$rSA->{Method},'Descr') . qq|</methodofuse>\n|;
    $out .= qq|      <amount>$rSA->{'Amount'}</amount>\n|;
    $out .= qq|      <datefused>| . DBUtil->Date($rSA->{FromDate},'fmt','MM/DD/YYYY') . qq|</datefused>\n|;
    $out .= qq|      <datelused>| . DBUtil->Date($rSA->{ToDate},'fmt','MM/DD/YYYY') . qq|</datelused>\n|;
    $out .= qq|      <agefuse>$rSA->{Age}</agefuse>\n|;
    $out .= qq|      <ageruse>$rSA->{AgeReg}</ageruse>\n|;
    $out .= qq|      <drugofchoice>| . DBA->getxref($form,'xPriority',$rSA->{Priority},'Descr') . qq|</drugofchoice>\n|;
    $out .= qq|     </currentdata>\n|;
    $cnt++;
  }
  $sSA->finish();
  $out .= qq|     <currentdata><current>None</current></currentdata>\n| unless ( $cnt );
  return($out);
}
# Income for Client
sub getIncome
{
  my ($self,$ClientID) = @_;
  my ($out,$cnt,$Tot30,$Total) = ('',0,0,0);
  my $qClientIncome = qq|select * from ClientIncome where ClientID=? and (ExpDate<'$form->{TODAY}' or ExpDate is null) order by EffDate|;
#warn qq|getIncome: q=\n${qClientIncome}\n|;
  my $sClientIncome = $dbh->prepare($qClientIncome);
  $sClientIncome->execute($ClientID);
  while ( $rClientIncome = $sClientIncome->fetchrow_hashref )
  {
    $out .= qq|     <income>\n|;
    $out .= qq|      <source>| . DBA->getxref($form,'xIncome',$rClientIncome->{'Src'},'Descr') . qq|</source>\n|;
    $out .= qq|      <last>| . sprintf("%.2f",$rClientIncome->{'Amt30'}) . qq|</last>\n|;
    $out .= qq|      <yearly>| . sprintf("%.2f",$rClientIncome->{'Amt'}) . qq|</yearly>\n|;
    $out .= qq|     </income>\n|;
    $Tot30 += $rClientIncome->{'Amt30'};
    $Total += $rClientIncome->{'Amt'};
    $cnt++;
  }
  $out .= qq|     <income><source>None Reported</source></income>\n| unless ( $cnt );
  $out .= qq|     <total>\n|;
  $out .= qq|      <totalsource></totalsource>\n|;
  $out .= qq|      <totallast>| . sprintf("%.2f",$Tot30) . qq|</totallast>\n|;
  $out .= qq|      <totalyearly>| . sprintf("%.2f",$Total) . qq|</totalyearly>\n|;
  $out .= qq|     </total>\n|;
  $sClientIncome->finish();
  return($out);
}
sub getLegal
{
  my ($self,$ClientID,$rClient,$rClientLegal) = @_;
#foreach my $f ( sort keys %{$rClientLegal} ) { warn "ClientLegal: $f=$rClientLegal->{$f}\n"; }
  my ($out,$cnt) = ('',0);
  my $sClientLegalPP = $dbh->prepare("select * from ClientLegalPP where ClientID=?");
  $sClientLegalPP->execute($ClientID);
  $rClientLegalPP = $sClientLegalPP->fetchrow_hashref;
  $out .= qq|     <legalinfo>\n|;
  $out .= qq|      <status>| . DBA->getxref($form,'xLegalStatus',$rClientLegal->{'LegalStatus'},'Descr') . qq|</status>\n|;
  $out .= qq|      <county>| . DBA->getxref($form,'xCountyOK',$rClientLegal->{'CommitmentCounty'},'Descr') . qq|</county>\n|;
  $out .= qq|      <custody>| . DBA->getxref($form,'xCustAgency',$rClientLegal->{'CustAgency'},'Descr') . qq|</custody>\n|;
  my $CASEID = $rClientLegal->{'CASEID'} eq '' ? '' : qq|CASEID: | . $rClientLegal->{'CASEID'};
  $out .= qq|      <jolts>$rClientLegal->{'JOLTS'} ${CASEID}</jolts>\n|;
  $out .= main->setYN('      ','probation',$rClientLegal->{'OnPP'},$SexProbDescr);
  $out .= qq|      <caseworker>$rClientLegalPP->{'Name'}</caseworker>\n|;
  $out .= qq|      <workphn>$rClientLegalPP->{'WkPh'}</workphn>\n|;
  $out .= qq|      <cellphn>$rClientLegalPP->{'FIX'}</cellphn>\n|;       # FIX
  $out .= qq|      <arrests>$rClientLegal->{'Arrested'}</arrests>\n|;
  $out .= qq|      <last30days>$rClientLegal->{'Arrest1'}</last30days>\n|;
  $out .= qq|     </legalinfo>\n|;
  $out .= qq|     <legalhistory>\n|;
  my $sClientLegalHx = $dbh->prepare("select * from ClientLegalHx where ClientID=? order by Date");
  $sClientLegalHx->execute($ClientID);
  while ( $rClientLegalHx = $sClientLegalHx->fetchrow_hashref )
  {
    $out .= qq|      <lhdata>\n|;
    $out .= qq|       <date>| . DBUtil->Date($rClientLegalHx->{'Date'},'fmt','MM/DD/YYYY') . qq|</date>\n|;
    $out .= qq|       <location>$rClientLegalHx->{'City'}, $rClientLegalHx->{'ST'}</location>\n|;
    $out .= qq|       <type>| . DBA->getxref($form,'xLegalType',$rClientLegalHx->{'Type'},'Descr') . qq|</type>\n|;
    $out .= qq|       <charge>| . DBA->getxref($form,'xLegalCharge',$rClientLegalHx->{'Charge'},'Descr') . qq|</charge>\n|;
    $out .= qq|       <outcome>| . DBA->getxref($form,'xLegalOutCome',$rClientLegalHx->{'OutCome'},'Descr') . qq|</outcome>\n|;
    $out .= qq|      </lhdata>\n|;
    $cnt++;
  }
  $out .= qq|      <lhdata><date>None Reported</date></lhdata>\n| unless ( $cnt );
  $out .= qq|     </legalhistory>\n|;
  $sClientLegalHx->finish();
  return($out);
}
############################################################################
sub setYN
{
  my ($self,$spc,$tag,$val,$cat,$unk,$yes,$no) = @_;
#warn qq|setYN: tag=$tag= val=$val= cat=$cat= unk=$unk= yes=$yes= no=$no=\n|;
  $yes = 'Yes' if ( $yes eq '');
  $no = 'No' if ( $no eq '');
  my $v = $val eq '1' ? $yes : $val eq '0' ? $no 
        : $val eq '2' ? "Yes"              # for ASI values, 0=No,1=Indifferent,2=Yes
        : $val eq 'A' ? "Aided" 
        : $val eq 'R' ? "Refused to answer" 
        : $val eq 'S' ? "Sometimes" 
        : $val eq 'U' ? "Unknown" 
        : $unk;
  my $out = $cat eq '' ?  
            qq|${spc}<${tag}>${v}</${tag}>\n|
          : qq|${spc}<${tag}>${v} ${cat}</${tag}>\n|;
  return($out);
}
sub setXML
{
  my ($self,$spc,$tag,$val,$cat,$unk) = @_;
#warn qq|setXML: tag=$tag= val=$val= cat=$cat= unk=$unk=\n|;
  my $v = $val eq '' ? $unk : DBA->subxml($val);
  my $out = $cat eq '' ?  
            qq|${spc}<${tag}>${v}</${tag}>\n|
          : qq|${spc}<${tag}>${v} ${cat}</${tag}>\n|;
  return($out);
}
sub xText
{
  my ($self,$form,$category,$r,$dlm,$cat,$tag,$tab) = @_;
#warn qq|category=$category, dlm=$dlm, cat=$cat, tag=$tag, tab=$tab\n|; 
  my ($out,$spc,$vals) = ('','','');
  $dlm = '; ' unless ( $dlm );
  my $sx = $cdbh->prepare("select * from xMentalStat where Category='${category}' order by Num,Descr");
  $sx->execute();
  while ( $rx = $sx->fetchrow_hashref )
  { if ( $rx->{'Value'} eq $r->{$rx->{'Field'}} ) { $vals .= qq|${spc}$rx->{'Descr'}|; $spc = $dlm; } }
##warn qq|Descr=$rx->{'Descr'}, Value=$rx->{'Value'}, Field=$rx->{'Field'}, Field=$r->{$rx->{'Field'}}\n|; 
#warn qq|vals=$vals= cat=$cat=\n|; 
  $vals .= qq| ${cat}| unless ( $cat eq '' );
#warn qq|vals=$vals= \n|; 
  $out = $tag eq '' ? $vals : qq|${tab}<${tag}>|.DBA->subxml(${vals}).qq|</${tag}>\n|;
  return($out);
}
