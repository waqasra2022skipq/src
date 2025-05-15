#!/usr/bin/perl
############################################################################
use lib 'C:/xampp/htdocs/src/lib';
use DBI;
use myForm;
use myDBI;
use DBA;
use MgrTree;
use myConfig;
use DBUtil;
use utf8;
use Time::Local;
my $DT=localtime();

use PDFlib::PDFlib;
use strict;
############################################################################

my $form = myForm->new();
my $IDs = $form->{'IDs'};
my $dbh = myDBI->dbconnect($form->{'DBNAME'});
#$IDs = "35757";
#$IDs = "107887";
##
# prepare selects...
##
my $sPrAuth = $dbh->prepare("select * from ClientPrAuth where ID=?");
my $sPDDiag = $dbh->prepare("select * from PDDiag where PrAuthID=?");
my $sPDDom = $dbh->prepare("select * from PDDom where PrAuthID=?");
my $sClientPrAuthCDC = $dbh->prepare("select * from ClientPrAuthCDC where ClientPrAuthID=?");
my $sInsurance = $dbh->prepare("select Insurance.ClientID,Insurance.InsIDNum,Insurance.InsID,xInsurance.Name,xInsurance.Addr1,xInsurance.Addr2,xInsurance.City,xInsurance.ST,xInsurance.Zip,xInsurance.Ph1,xInsurance.Fax from Insurance left join xInsurance on xInsurance.ID=Insurance.InsID where Insurance.InsNumID=?");
my $sContracts = $dbh->prepare("select * from Contracts where ProvID=? and InsID=?");

my $qClient = qq|select 
Client.*,
ClientIntake.SchoolCollab,
ClientRelations.Residence,
ClientRelations.GHLevel,
ClientRelations.ResAdmitDate,
ClientRelations.LivesWith,
ClientRelations.LivesWithDesc,
ClientReferrals.ReferredToNPI
 from Client
  left join ClientIntake on ClientIntake.ClientID=Client.ClientID 
  left join ClientRelations on ClientRelations.ClientID=Client.ClientID 
  left join ClientReferrals on ClientReferrals.ClientID=Client.ClientID 
 where Client.ClientID=?|;
my $sClient = $dbh->prepare($qClient);
my $sGuardian = $dbh->prepare("select * from ClientFamily where ClientID=? and Guardian=1 order by Age");
my $sProvider = $dbh->prepare("select * from Provider where ProvID=?");
my $sCredentials = $dbh->prepare("select PIN,Abbr from Credentials left join okmis_config.xCredentials on xCredentials.ID=Credentials.CredID where ProvID=? and InsID=? order by Credentials.Rank");

my $pagewidth = 612;
my $pageheight = 792;

my $searchpath = "../data";

my $fontname= "Arial";
my $boldfontname= "Arial-BoldMT";
my $fontsizesmall = 8;
my $fontsize = 9;
my $fontsizemid = 10;
my $fontsizelarge = 11;
my $fontsizemidlarge = 12;
my $fontsizexlarge = 13;
my $fontsizexxlarge = 15;
my $basefontoptions = "fontname=" . $fontname . " fontsize=" . $fontsize . " embedding encoding=unicode";
my $baseboldfontoptions = "fontname=" . $boldfontname . " fontsize=" . $fontsize . " embedding encoding=unicode";
my $basemidfontoptions = $basefontoptions . " fontsize=" . $fontsizemid;
my $baseboldmidfontoptions = $baseboldfontoptions . " fontsize=" . $fontsizemid;
my $baselargefontoptions = $basefontoptions . " fontsize=" . $fontsizelarge;
my $baseboldlargefontoptions = $baseboldfontoptions . " fontsize=" . $fontsizelarge;
my $baseboldlargefontoptions_u = $baseboldfontoptions . " fontsize=" . $fontsizelarge . " underline=true underlineposition=-15% underlinewidth=0.03";
my $baseboldlargefontoptions_ui = $baseboldlargefontoptions_u . " fontstyle=italic";
my $baseboldlargefontoptions_i = $baseboldlargefontoptions . " fontstyle=italic";
my $basesmallfontoptions = $basefontoptions . " fontsize=" . $fontsizesmall;
my $baseboldsmallfontoptions = $baseboldfontoptions . " fontsize=" . $fontsizesmall;
my $baseboldmidlargefontoptions = $baseboldfontoptions . " fontsize=" . $fontsizemidlarge;
my $baseboldxlargefontoptions = $baseboldfontoptions . " fontsize=" . $fontsizexlarge;

my $marginleft = 37.5;
my $margintop = 35;
my $marginbottom = $pageheight - 33.8;
my $contentwidth = $pagewidth - 2 * $marginleft;
my $h_footer = 4 * $fontsizemid;
my $y_footer = $marginbottom - $h_footer;
my $margintop2 = 44.6;

my $ypos = $margintop;
my $pagecount = 0;
my $c253 = chr(253);

############################################################################
my %xDom1 =
(
   'Dom1Mood'          => { Descr => 'Mood lability' },
   'Dom1Coping'        => { Descr => 'Coping skills' },
   'Dom1Suicidal'      => { Descr => 'Suicidal/homicidal ideation/plan' },
   'Dom1Depression'    => { Descr => 'Depression' },
   'Dom1Anger'         => { Descr => 'Anger' },
   'Dom1Anxiety'       => { Descr => 'Anxiety' },
   'Dom1Euphoria'      => { Descr => 'Euphoria' },
   'Dom1Change'        => { Descr => 'Change in appetite/sleep patterns' },
);
my %xDom2 =
(
   'Dom2Memory'        => { Descr => 'Memory' },
   'Dom2Cognitive'     => { Descr => 'Cognitive process' },
   'Dom2Concentration' => { Descr => 'Concentration' },
   'Dom2Judgment'      => { Descr => 'Judgement' },
   'Dom2Obsessions'    => { Descr => 'Obsessions' },
   'Dom2Delusions'     => { Descr => 'Delusions/hallucinations' },
   'Dom2Belief'        => { Descr => 'Belief system' },
   'Dom2Learning'      => { Descr => 'Learning disabilities' },
   'Dom2Impulse'       => { Descr => 'Impulse Control' },
);
my %xDom5 =
(
   'Dom5Parenting'     => { Descr => 'Parenting' },
   'Dom5Conflict'      => { Descr => 'Conflict' },
   'Dom5Violence'      => { Descr => 'Abuse/violence' },
   'Dom5Communication' => { Descr => 'Communication' },
   'Dom5Marital'       => { Descr => 'Marital' },
   'Dom5Sibling'       => { Descr => 'Sibling' },
   'Dom5ParentChild'   => { Descr => 'Parent/child' },
);
my %xDom6 =
(
   'Dom6Peers'         => { Descr => 'Peers/friends' },
   'Dom6Social'        => { Descr => 'Social interaction' },
   'Dom6Withdrawal'    => { Descr => 'Withdrawal' },
   'Dom6Friends'       => { Descr => 'Make/keep friends' },
   'Dom6Conflict'      => { Descr => 'Conflict' },
);
my %xDom7 =
(
   'Dom7Employment'    => { Descr => 'Employment/Volunteer' },
   'Dom7School'        => { Descr => 'School/daycare' },
   'Dom7Home'          => { Descr => 'Home management' },
   'Dom7Other'         => { Descr => 'Other' },
);
my %xDom8 =
(
   'Dom8Rules'         => { Descr => 'Ability to follow rules/laws' },
   'Dom8Authority'     => { Descr => 'Authority issues' },
   'Dom8Legal'         => { Descr => 'Legal issues' },
   'Dom8Aggression'    => { Descr => 'Agression' },
   'Dom8Probation'     => { Descr => 'Probation/parole' },
   'Dom8Moral'         => { Descr => 'Abides by personal ethical/moral value system' },
   'Dom8Antisocial'    => { Descr => 'Antisocial behaviors' },
);
my %xDom9 =
(
   'Dom9Hygiene'       => { Descr => 'Hygiene' },
   'Dom9Food'          => { Descr => 'Food' },
   'Dom9Clothing'      => { Descr => 'Clothing' },
   'Dom9Shelter'       => { Descr => 'Shelter' },
   'Dom9Medical'       => { Descr => 'Medical/dental needs' },
   'Dom9Transportation'=> { Descr => 'Transportation' },
);
my %xDom12 =
(
   'Dom12ESL'          => { Descr => 'ESL' },
   'Dom12Hearing'      => { Descr => 'Hearing impaired' },
   'Dom12Nonverbal'    => { Descr => 'Non-verbal' },
   'Dom12Interpreter'  => { Descr => 'Uses interpreter' },
   'Dom12Signs'        => { Descr => 'Signs' },
   'Dom12Mechanical'   => { Descr => 'Uses mechanical device' },
   'Dom12Speech'       => { Descr => 'Speech impaired' },
   'Dom12Fluency'      => { Descr => 'Fluency' },
);

my $filename = '/tmp/'.$form->{'LOGINID'}.'_'.DBUtil->genToken().'_'.DBUtil->Date('','stamp').'.pdf';
my $outfile = $form->{'file'} eq ''                # create and print pdf else just create.
        ? $form->{'DOCROOT'}.$filename
        : $form->{'file'};
############################################################################

eval {

  # create a new PDFlib object 
  my $p = new PDFlib::PDFlib;

  $p->set_option("SearchPath={{" . $searchpath . "}}");

  # This mean we don't have to check error return values, but will
  # get an exception in case of runtime problems.
  
  $p->set_option("errorpolicy=exception");

  # all strings are expected as utf8
  $p->set_option("stringformat=utf8");

  $p->begin_document($outfile, "");

  $p->set_info("Creator", "Millennium Information Services");
  $p->set_info("Author", "Keith Stephenson");
  $p->set_info("Title", "Prior Authorization");

  main->printPrAuth($p);

  $p->end_document("");

};

if ($@) {
  die("$0: PDFlib Exception occurred:\n$@");
}

$sPrAuth->finish();
$sPDDiag->finish();
$sPDDom->finish();
$sClientPrAuthCDC->finish();
$sInsurance->finish();
$sContracts->finish();
$sClient->finish();
$sProvider->finish();
$sGuardian->finish();
$sCredentials->finish();

myDBI->cleanup();

if ( $form->{'file'} eq '' )                # create and print pdf.
{ print qq|Location: ${filename}\n\n|; }
exit;

############################################################################
sub printPrAuth {
  my ($self, $p) = @_;

  foreach my $ID ( split(' ',$IDs) )
  { 
    #warn "PrintPrAuth: ID=${ID}\n";
    $sPrAuth->execute($ID) || myDBI->dberror("PrintPrAuth: select ClientPrAuth $ID");
    while ( my $rPrAuth = $sPrAuth->fetchrow_hashref )
    { 
      $sClient->execute($rPrAuth->{ClientID}) || myDBI->dberror($qClient);
      my $rClient = $sClient->fetchrow_hashref;
      my $ProvID=$rClient->{ProvID};
      $sProvider->execute($ProvID) || myDBI->dberror("PrintPrAuth: select Provider $ProvID");
      my $rPrimaryProvider = $sProvider->fetchrow_hashref;

      main->createPages($p, $rPrAuth, $rClient, $rPrimaryProvider);
    }
  }
  if ($pagecount) {
    main->createPageCount($p);
  } else {
    main->createEmptyPage($p);
  }

}

sub createPages {
  my ($self, $p, $rPrAuth, $rClient, $rPrimaryProvider) = @_;

  my $optlist;
  my $tf;
  my $h_tf;
  my $row;
  my $col;
  my $tbl;
  my $h_tbl;

  ##
# Header info...
  my $AgencyID = MgrTree->getAgency($form,$rClient->{'clinicClinicID'});
  $sProvider->execute($AgencyID) || myDBI->dberror("PrintPrAuth: select Provider");
  my $rAgency = $sProvider->fetchrow_hashref;
  my $AgencyName = $rAgency->{'Name'};
  my $AgencyAddr = $rAgency->{Addr1} . ', ';
  $AgencyAddr .= $rAgency->{Addr2} . ', ' if ( $rAgency->{Addr2} );
  my $AgencyCSZ .= $rAgency->{City} . ', ' . $rAgency->{ST} . '  ' . $rAgency->{Zip};
  my $AgencyPh = 'Office: ' . $rAgency->{'WkPh'} . '  Fax: ' . $rAgency->{'Fax'};
  $sProvider->execute($rClient->{'clinicClinicID'})
       || myDBI->dberror("PrintPrAuth: select Provider $rClient->{'clinicClinicID'}");
  my $rClinic = $sProvider->fetchrow_hashref;
  my $ClinicName = $rClinic->{'Name'};
  my $ClinicAddr = $rClinic->{'Addr1'} . ', ';
  $ClinicAddr .= $rClinic->{'Addr2'} . ', ' if ( $rClinic->{'Addr2'} );
  $ClinicAddr .= $rClinic->{'City'} . ', ' . $rClinic->{'ST'} . '  ' . $rClinic->{'Zip'};
  my $ClinicPh = 'Office: ' . $rClinic->{'WkPh'} . '  Fax: ' . $rClinic->{'Fax'};
##
# Client info...
  my $ClientName = qq|$rClient->{'FName'} $rClient->{'MName'} $rClient->{'LName'} ($rClient->{'ClientID'})|;
  my $ClientID = $rPrAuth->{ClientID};
  my $PrAuthID = $rPrAuth->{ID};
##
# Other Client information...
  $sPDDiag->execute($PrAuthID) || myDBI->dberror("PrintPrAuth: select PDDiag $PrAuthID");
  my $rPDDiag = $sPDDiag->fetchrow_hashref;
  $sPDDom->execute($PrAuthID) || myDBI->dberror("PrintPrAuth: select PDDom $PrAuthID");
  my $rPDDom = $sPDDom->fetchrow_hashref;
  $sClientPrAuthCDC->execute($PrAuthID) || myDBI->dberror("PrintPrAuth: select ClientPrAuthCDC $PrAuthID");
  my $rClientPrAuthCDC = $sClientPrAuthCDC->fetchrow_hashref;
#foreach my $f ( sort keys %{ $rClientPrAuthCDC } ) { warn qq|: rClientPrAuthCDC-$f=$rClientPrAuthCDC->{$f}\n|; }
  $sInsurance->execute($rPrAuth->{'InsuranceID'}) || myDBI->dberror("PrintPrAuth: select Insurance $rPrAuth->{InsuranceID}");
  my $rInsurance = $sInsurance->fetchrow_hashref;
  $sContracts->execute($rClinic->{'ProvID'},$rInsurance->{'InsID'}) || myDBI->dberror("PrintPrAuth: select Insurance $rClinic->{'ProvID'},$rInsurance->{InsID}");
  my $rContracts = $sContracts->fetchrow_hashref;
  $sGuardian->execute($ClientID);
  my $rGuardian = $sGuardian->fetchrow_hashref;
  my $PastPrAuthID = DBA->getLASTID($form,$PrAuthID,"ClientPrAuth","where ClientPrAuth.ClientID='$ClientID' and Insurance.InsID='$rInsurance->{InsID}'","order by ClientPrAuth.EffDate desc, ClientPrAuth.ExpDate desc");
  $sPDDom->execute($PastPrAuthID) || myDBI->dberror("PrintPrAuth: select PDDom $PastPrAuthID");
  my $rPastPDDom = $sPDDom->fetchrow_hashref;
  my $ProviderName = qq|$rPrimaryProvider->{'FName'} $rPrimaryProvider->{'LName'}|;
  $sCredentials->execute($rPrimaryProvider->{ProvID},$rInsurance->{InsID});
  my ($RendProvPIN,$RendProvCred) = $sCredentials->fetchrow_array;

  my $residence = DBA->getxref($form,'xResidence',$rClient->{'Residence'},'Descr');
  my $placement = $residence =~ /residential care facility/i ? 'Residential treatment'
        : $residence =~ /specialized community group home/i ? 'Specialized community group home'
        : $residence =~ /foster/i ? 'Foster home'
        : $residence =~ /group home/i ? 'Group home' : 'Not in out-of-home treatment';

  my $level = qq|${placement} |.DBA->getxref($form,'xGHLevel',$rClient->{'GHLevel'},'Descr');

# KLS AFTER THE ADDENDUM ...
# KLS  add these TITLES with text flow boxes below the TITLE ...
# KLS  these should only display (TITLE and variable) IF something in variable ...
# KLS title: COMMUNITY INTEGRATION:
  my $community = $rPDDom->{'Dom10Text'};
# KLS title: CAREGIVER RESOURCES (for clients under age of 21):
  my $caregiver = $rPDDom->{'Dom11Text'};
# KLS title: COLLABORATION WITH SCHOOL SYSTEM (SCHOOL agechildren only):
  my $collaboration = $rClient->{'SchoolCollab'};
# KLS title: REFERRALS TO OTHER COMMUNITY SERVICES
  my $rReferredTo = DBA->selxref($form,'xNPI','NPI',$rClient->{'ReferredToNPI'});
  my $referrals = $rReferredTo->{'ProvOrgName'};

#####################
# Page variables
  my $cname = $ClientName;
  my $ssn = $rClient->{'SSN'};
  my $pname = $ProviderName;
  my $dcompleted = DBUtil->Date($rClientPrAuthCDC->{'StatusDate'},'fmt','MM/DD/YYYY');
  my $typeoffax = DBA->getxref($form,'xPrAuthType',$rPrAuth->{'Type'},'Descr');

  my $submissiondate = "";     # these next 3 are written on the pdf by hand
  my $submissiontime = "";
  my $attention = "";
  my $to = $rInsurance->{'Name'};
  my $tofaxnumber = $rInsurance->{'Fax'};

  my $from = $AgencyName;
  my $faciltyagency = $ClinicName;
  my $contactname = "$rClinic->{'FName'} $rClinic->{'LName'}";
  my $faddress = $ClinicAddr;
  my $faxnumber = $rClinic->{Fax};
  my $phonenumber = $rClinic->{WkPh};
  my $legalgname = "$rGuardian->{'FName'} $rGuardian->{'LName'}";
  my $relationtoclient = DBA->getxref($form,'xRelationship',$rGuardian->{Rel},'Descr');
  my $currentresidence = ${residence};
  my $admitdate = DBUtil->Date($rClient->{'ResAdmitDate'},'fmt','MM/DD/YYYY');
  my $dob = $rClient->{DOB};
  my $age = DBUtil->Date($rClient->{DOB},'age');
  my $sex = DBA->getxref($form,'xGend',$rClient->{Gend},'Descr');

  my $recipientID = $rInsurance->{'InsIDNum'};
  my $paNumber = $rPrAuth->{'PAnumber'};
  my $comments = $rPrAuth->{'ReqComments'} eq '' && $rPrAuth->{'OthComments'} eq ''
         ? 'None'
         : $rPrAuth->{'ReqComments'}."\n".$rPrAuth->{'OthComments'};

  my $Header2Info = { "clientName" => $cname, "groupProvider" => $rContracts->{'PIN'}, "dateCompleted" => $dcompleted, "recipientID" => $recipientID, "renderingProvider" => $RendProvPIN };

  my @TreatmentHistoryHeaders = ("Admit/Discharge dates", "Facility", "IP or OP", "Reason for treatment");
  my @TreatmentHistoryHeaderWidths = (30, 40, 30, 30);
  my @TreatmentHistory = main->getHospitalTreatments($ClientID);
       
  my $FeelingsScorePast = $rPastPDDom->{'Dom1Score'};
  my $FeelingsScoreCurrent = $rPDDom->{'Dom1Score'};
  my $FeelingsProblem = main->xText(\%xDom1,$rPDDom);
  my $FeelingsEvidencedBy = $rPDDom->{'Dom1Text'};

  my $ThinkingScorePast = $rPastPDDom->{'Dom2Score'};
  my $ThinkingScoreCurrent = $rPDDom->{'Dom2Score'};
  my $ThinkingProblem = main->xText(\%xDom2,$rPDDom);
  my $ThinkingEvidencedBy = $rPDDom->{'Dom2Text'};

  my @SubstancesHeaders = ("Drug of Choice", "Amount Used", "Frequence of Use", "Age First Used", "Date Last Used");
  my @SubstancesHeaderWidths = (40, 20, 20, 20, 20);
  my $SubstanceScorePast = $rPastPDDom->{'Dom3Score'};
  my $SubstanceScoreCurrent = $rPDDom->{'Dom3Score'};
  my @Substances = main->getSubstanceAbuse($ClientID,$rPrAuth->{'EffDate'});
  my $SubstanceImpact = $rPDDom->{'Dom3Text'};

  my $MedicalScorePast = $rPastPDDom->{'Dom4Score'};
  my $MedicalScoreCurrent = $rPDDom->{'Dom4Score'};
# KLS instead of single line of text...output list...
  my @MedicalConditionsHeaders = ("ICD10", "Sct Name");
  my @MedicalConditionsHeaderWidths = (30, 70);
  my @MedicalConditions = main->getProblems($ClientID,$rPrAuth->{'EffDate'});
  my $MedicalImpact = $rPDDom->{'Dom4Text'};
  my @MedicationsHeaders = ("Physician", "Medication", "Type", "Date", "Reason");
  my @MedicationsHeaderWidths = (20, 30, 30, 20, 20);
  my @Medications = main->getMedications($ClientID);

  my $FamilyScorePast = $rPastPDDom->{'Dom5Score'};
  my $FamilyScoreCurrent = $rPDDom->{'Dom5Score'};
  my $FamilyResides = DBA->getxref($form,'xLivesWith',$rClient->{'LivesWith'},'Descr').' '.$rClient->{'LivesWithDesc'};
  my $FamilyProblem = main->xText(\%xDom5,$rPDDom);
  my $FamilyEvidencedBy = $rPDDom->{'Dom5Text'};

  my $InterpersonalScorePast = $rPastPDDom->{'Dom6Score'};
  my $InterpersonalScoreCurrent = $rPDDom->{'Dom6Score'};
  my $InterpersonalProblem = main->xText(\%xDom6,$rPDDom);
  my $InterpersonalEvidencedBy = $rPDDom->{'Dom6Text'};

  my $RoleScorePast = $rPastPDDom->{'Dom7Score'};
  my $RoleScoreCurrent = $rPDDom->{'Dom7Score'};
  my $RoleFrole = main->xText(\%xDom7,$rPDDom);
  my $RoleEffectiveness = $rPDDom->{'Dom7Descr'};
  my $RoleEvidencedBy = $rPDDom->{'Dom7Text'};

  my $SocioScorePast = $rPastPDDom->{'Dom8Score'};
  my $SocioScoreCurrent = $rPDDom->{'Dom8Score'};
  my $SocioProblem = main->xText(\%xDom8,$rPDDom);
  my $SocioEvidencedBy = $rPDDom->{'Dom8Text'};

  my $SelfScorePast = $rPastPDDom->{'Dom9Score'};
  my $SelfScoreCurrent = $rPDDom->{'Dom9Score'};
  my $SelfProblem = main->xText(\%xDom9,$rPDDom);
  my $SelfEvidencedBy = $rPDDom->{'Dom9Text'};

  my $Communication = main->xText(\%xDom12,$rPDDom);
  my $CommunicationComm1 = $rPDDom->{'Dom12Text'};

# ASI
  my $ASIMedical = $rClientPrAuthCDC->{'ASIMedical'} == 9
                 ? ''
                 : $rClientPrAuthCDC->{'ASIMedical'}.'-'.DBA->getxref($form,'xRaces',$rClientPrAuthCDC->{ASIMedical},'Descr');
  my $ASIemploy = $rClientPrAuthCDC->{'ASIEmploy'} == 9
                 ? ''
                 : $rClientPrAuthCDC->{'ASIEmploy'}.'-'.DBA->getxref($form,'xRaces',$rClientPrAuthCDC->{ASIEmploy},'Descr');
  my $ASIAlcohol = $rClientPrAuthCDC->{'ASIAlcohol'} == 9
                 ? ''
                 : $rClientPrAuthCDC->{'ASIAlcohol'}.'-'.DBA->getxref($form,'xRaces',$rClientPrAuthCDC->{ASIAlcohol},'Descr');
  my $ASIDrug = $rClientPrAuthCDC->{'ASIDrug'} == 9
                 ? ''
                 : $rClientPrAuthCDC->{'ASIDrug'}.'-'.DBA->getxref($form,'xRaces',$rClientPrAuthCDC->{ASIDrug},'Descr');
  my $ASILegal = $rClientPrAuthCDC->{'ASILegal'} == 9
                 ? ''
                 : $rClientPrAuthCDC->{'ASILegal'}.'-'.DBA->getxref($form,'xRaces',$rClientPrAuthCDC->{ASILegal},'Descr');
  my $ASIFamily = $rClientPrAuthCDC->{'ASIFamily'} == 9
                 ? ''
                 : $rClientPrAuthCDC->{'ASIFamily'}.'-'.DBA->getxref($form,'xRaces',$rClientPrAuthCDC->{ASIFamily},'Descr');
  my $ASIPsych = $rClientPrAuthCDC->{'ASIPsych'} == 9
                 ? ''
                 : $rClientPrAuthCDC->{'ASIPsych'}.'-'.DBA->getxref($form,'xRaces',$rClientPrAuthCDC->{ASIPsych},'Descr');

# TASI
  my $TASIChemical = $rClientPrAuthCDC->{'TASIChemical'} == 9
                 ? ''
                 : $rClientPrAuthCDC->{'TASIChemical'}.'-'.DBA->getxref($form,'xRaces',$rClientPrAuthCDC->{TASIChemical},'Descr');
  my $TASISchool = $rClientPrAuthCDC->{'TASISchool'} == 9
                 ? ''
                 : $rClientPrAuthCDC->{'TASISchool'}.'-'.DBA->getxref($form,'xRaces',$rClientPrAuthCDC->{TASISchool},'Descr');
  my $TASIEmploy = $rClientPrAuthCDC->{'TASIEmploy'} == 9
                 ? ''
                 : $rClientPrAuthCDC->{'TASIEmploy'}.'-'.DBA->getxref($form,'xRaces',$rClientPrAuthCDC->{TASIEmploy},'Descr');
  my $TASIFamily = $rClientPrAuthCDC->{'TASIFamily'} == 9
                 ? ''
                 : $rClientPrAuthCDC->{'TASIFamily'}.'-'.DBA->getxref($form,'xRaces',$rClientPrAuthCDC->{TASIFamily},'Descr');
  my $TASIPeer = $rClientPrAuthCDC->{'TASIPeer'} == 9
                 ? ''
                 : $rClientPrAuthCDC->{'TASIPeer'}.'-'.DBA->getxref($form,'xRaces',$rClientPrAuthCDC->{TASIPeer},'Descr');
  my $TASILegal = $rClientPrAuthCDC->{'TASILegal'} == 9
                 ? ''
                 : $rClientPrAuthCDC->{'TASILegal'}.'-'.DBA->getxref($form,'xRaces',$rClientPrAuthCDC->{TASILegal},'Descr');
  my $TASIPsych = $rClientPrAuthCDC->{'TASIPsych'} == 9
                 ? ''
                 : $rClientPrAuthCDC->{'TASIPsych'}.'-'.DBA->getxref($form,'xRaces',$rClientPrAuthCDC->{TASIPsych},'Descr');

# KLS use this variable for SERVICES REQUESTED...
  my $servicesreq = DBA->getxref($form,'xPAgroups',$rPrAuth->{'PAgroup'},'Descr').' ('.DBA->getxref($form,'xPAgroups',$rPrAuth->{'PAgroup'},'Length2').' '.DBA->getxref($form,'xPAgroups',$rPrAuth->{'PAgroup'},'Length1').')';
#####################

  main->createHeader($p, $rAgency, $rInsurance);

  $ypos += 13;
  $p->fit_textline("OUTPATIENT REQUEST FOR PRIOR AUTHORIZATION", $pagewidth / 2, $ypos, $baseboldmidlargefontoptions . " position={center bottom}");

  $ypos += 29.3;
  $p->fit_textline("Client Name :", 37, $ypos, $baseboldmidfontoptions);
  $p->fit_textline($cname, 105, $ypos, $basefontoptions);
  $p->fit_textline("Provider Name :", 253.2, $ypos, $baseboldmidfontoptions);
  $p->fit_textline($pname, 333.6, $ypos, $basefontoptions);
  $p->fit_textline("Date Completed:", 433.3, $ypos, $baseboldmidfontoptions);
  $p->fit_textline($dcompleted, 518.2, $ypos, $basefontoptions);

  $ypos += 18;
  $p->fit_textline("Submission Date:", 37, $ypos, $baseboldmidfontoptions);
  $p->fit_textline($submissiondate, 127.4, $ypos, $basefontoptions);
  $p->fit_textline("Time:", 198.7, $ypos, $baseboldmidfontoptions);
  $p->fit_textline($submissiontime, 231.6, $ypos, $basefontoptions);
  $p->fit_textline("Type of Fax:", 311.3, $ypos, $baseboldmidfontoptions);
  $p->fit_textline($typeoffax, 376.6, $ypos, $basefontoptions);

  $ypos += 36;
  $p->fit_textline("To :", 37, $ypos, $baseboldmidfontoptions);
  $p->fit_textline($to, 59.3, $ypos, $basefontoptions);
  $p->fit_textline("Attention:", 311.3, $ypos, $baseboldmidfontoptions);
  $p->fit_textline($attention, 365.8, $ypos, $basefontoptions);

  $ypos += 21.7;
  $p->fit_textline("Fax Number:", 37, $ypos, $baseboldmidfontoptions);
  $p->fit_textline($tofaxnumber, 104.6, $ypos, $basefontoptions);
  $p->fit_textline("(Reviewer)", 383, $ypos - 3.3, $baseboldmidfontoptions);

  $ypos += 18;
  $p->fit_textline("From :", 37, $ypos, $baseboldmidfontoptions);
  $p->fit_textline($from, 72.2, $ypos, $basefontoptions);

  $ypos += 18;
  $p->fit_textline("Facility / Agency :", 37, $ypos, $baseboldmidfontoptions);
  $p->fit_textline($faciltyagency, 126, $ypos, $basefontoptions);
  $p->fit_textline("Contact Name :", 311.3, $ypos, $baseboldmidfontoptions);
  $p->fit_textline($contactname, 389.3, $ypos, $basefontoptions);

  $ypos += 37.2;
  $p->fit_textline("Facility Address :", 37, $ypos, $baseboldmidfontoptions);
  $p->fit_textline($faddress, 122.4, $ypos, $basefontoptions);

  $ypos += 16.3;
  $p->fit_textline("Fax Number :", 37, $ypos, $baseboldmidfontoptions);
  $p->fit_textline($faxnumber, 104.6, $ypos, $basefontoptions);
  $p->fit_textline("Phone Number :", 311.3, $ypos, $baseboldmidfontoptions);
  $p->fit_textline($phonenumber, 393, $ypos, $basefontoptions);

  $ypos += 35.9;
  $p->fit_textline("Legal Guardian Name :", 37, $ypos, $baseboldmidfontoptions);
  $legalgname = utf8::encode($legalgname);
  $p->fit_textline($legalgname, 151.7, $ypos, $basefontoptions);
  $p->fit_textline("Relationship to Client :", 311.3, $ypos, $baseboldmidfontoptions);
  $p->fit_textline($relationtoclient, 426.7, $ypos, $basefontoptions);

  $ypos += 18;
  $p->fit_textline("Social Security # :", 37, $ypos, $baseboldmidfontoptions);
  $p->fit_textline($ssn, 128.6, $ypos, $basefontoptions);

  $ypos += 18;
  $p->fit_textline("Current Residence :", 37, $ypos, $baseboldmidfontoptions);
  $p->fit_textline($currentresidence, 138.2, $ypos, $basefontoptions);

  $ypos += 18;
  $p->fit_textline("Level :", 37, $ypos, $baseboldmidfontoptions);
  $p->fit_textline($level, 74.6, $ypos, $basefontoptions);

  $ypos += 18;
  $p->fit_textline("Admit Date To Current Facility :", 37, $ypos, $baseboldmidfontoptions);
  $p->fit_textline($admitdate, 193.2, $ypos, $basefontoptions);
  $p->fit_textline("Date of Birth :", 253.3, $ypos, $baseboldmidfontoptions);
  $p->fit_textline($dob, 324.7, $ypos, $basefontoptions);
  $p->fit_textline("Age :", 380.7, $ypos, $baseboldmidfontoptions);
  $p->fit_textline($age, 412.2, $ypos, $basefontoptions);
  $p->fit_textline("Sex :", 453, $ypos, $baseboldmidfontoptions);
  $p->fit_textline($sex, 483, $ypos, $basefontoptions);

  $ypos += 18;
  $p->fit_textline("Treatment History:", 37, $ypos, $baseboldmidfontoptions);
  $p->fit_textline("(Admit - Discharge dates, facility, IP or OP, reason for treatment)", 128.6, $ypos, $baseboldsmallfontoptions);

  $ypos += 7;

  $row = 1;
  $col = 1;
  $tbl = -1;
  for ($col=1; $col <= $#TreatmentHistoryHeaders+1; $col++) {
    $optlist =  "fittextline={position={left center} $baseboldfontoptions}";
    $tbl = $p->add_table_cell($tbl, $col, $row, $TreatmentHistoryHeaders[$col-1], $optlist . " colwidth=$TreatmentHistoryHeaderWidths[$col-1]%");
  }
  $row++;
  # ---------- Data rows: one for each item 
  $optlist =  "fittextline={position={left center} " . $basefontoptions . "} marginright=2";
  for (my $i = 0; $i <  $#TreatmentHistory+1; $i++) {
    $col = 1;
    # column 1: Admit/Discharge dates 
    $tbl = $p->add_table_cell($tbl, $col++, $row, $TreatmentHistory[$i]{dates}, $optlist);
    # column 2: Facility
    $tbl = $p->add_table_cell($tbl, $col++, $row, $TreatmentHistory[$i]{facility}, $optlist);
    # column 3: IP or OP 
    $tbl = $p->add_table_cell($tbl, $col++, $row, $TreatmentHistory[$i]{ip}, $optlist);
    # column 4: reason for treatment 
    $tbl = $p->add_table_cell($tbl, $col++, $row, $TreatmentHistory[$i]{reason}, $optlist);
    $row++;
  }
  $h_tbl = main->renderTable($p, $tbl, 59.5, $Header2Info);

  $ypos += $h_tbl;

  main->renderTextline($p, "Recipient ID# :", $marginleft, 18, $baseboldmidfontoptions, $Header2Info);
  $p->fit_textline($recipientID, 117.6, $ypos, $basefontoptions);
  $p->fit_textline("PA #:", 311.3, $ypos, $baseboldmidfontoptions);
  $p->fit_textline($paNumber, 344.6, $ypos, $basefontoptions);

#KLS not sure how to tell how many pages are created before hand??
  main->renderTextline($p, "Number of Pages Including This Page :", $marginleft, 18, $baseboldmidfontoptions, $Header2Info);

  main->renderTextline($p, "Comments :", $marginleft, 18, $baseboldmidfontoptions, $Header2Info);
  $p->fit_textline("(NO clinical information)", 97.4, $ypos, $baseboldsmallfontoptions);

  $tf = $p->create_textflow($comments, $basefontoptions . " leading=120% alignment=justify");
  $h_tf = main->renderTextflow($p, $tf, $marginleft, $Header2Info);

  $ypos += $h_tf;

  main->renderTextline($p, "CLIENT ASSESSMENT RECORD :", $marginleft, 20, $baseboldlargefontoptions_u, $Header2Info);

  $p->fit_textline("Past", 500.9, $ypos, $baseboldlargefontoptions);
  $p->fit_textline("Current", 532.1, $ypos, $baseboldlargefontoptions);

  main->renderTextline($p, "1. Feelings / Affect :", $marginleft, 20.6, $baseboldlargefontoptions, $Header2Info);
  $p->fit_textline("SCORE", 445.9, $ypos, $baseboldlargefontoptions);
  $p->fit_textline($FeelingsScorePast, 508.5, $ypos, $basefontoptions);
  $p->fit_textline($FeelingsScoreCurrent, 547.2, $ypos, $basefontoptions);
  main->renderTextline($p, "Problem areas :", $marginleft, 15, $baseboldfontoptions, $Header2Info);
  $p->fit_textline($FeelingsProblem, 118, $ypos, $basefontoptions);
  main->renderTextline($p, "Evidenced by (specific examples, symptom frequency, duration and intensity, impact on daily functioning):", $marginleft, 15, $baseboldfontoptions, $Header2Info);
  $tf = $p->create_textflow($FeelingsEvidencedBy, $basefontoptions . " leading=120% alignment=justify");
  $h_tf = main->renderTextflow($p, $tf, $marginleft, $Header2Info);

  $ypos += $h_tf;

  main->renderTextline($p, "2. Thinking :", $marginleft, 24, $baseboldlargefontoptions, $Header2Info);
  $p->fit_textline("SCORE", 445.9, $ypos, $baseboldlargefontoptions);
  $p->fit_textline($ThinkingScorePast, 508.5, $ypos, $basefontoptions);
  $p->fit_textline($ThinkingScoreCurrent, 547.2, $ypos, $basefontoptions);
  main->renderTextline($p, "Problem areas :", $marginleft, 15, $baseboldfontoptions, $Header2Info);
  $p->fit_textline($ThinkingProblem, 118, $ypos, $basefontoptions);
  main->renderTextline($p, "Evidenced by (specific examples, symptom frequency, duration and intensity, impact on daily functioning):", $marginleft, 15, $baseboldfontoptions, $Header2Info);
  $tf = $p->create_textflow($ThinkingEvidencedBy, $basefontoptions . " leading=120% alignment=justify");
  $h_tf = main->renderTextflow($p, $tf, $marginleft, $Header2Info);

  $ypos += $h_tf;

  main->renderTextline($p, "3. Substance Use :", $marginleft, 24, $baseboldlargefontoptions, $Header2Info);
  $p->fit_textline("SCORE", 445.9, $ypos, $baseboldlargefontoptions);
  $p->fit_textline($SubstanceScorePast, 508.5, $ypos, $basefontoptions);
  $p->fit_textline($SubstanceScoreCurrent, 547.2, $ypos, $basefontoptions);

  $ypos += 7;

  $row = 1;
  $col = 1;
  $tbl = -1;
  for ($col=1; $col <= $#SubstancesHeaders+1; $col++) {
    $optlist =  "fittextline={position={left center} $baseboldfontoptions}";
    $tbl = $p->add_table_cell($tbl, $col, $row, $SubstancesHeaders[$col-1], $optlist . " colwidth=$SubstancesHeaderWidths[$col-1]%");
  }
  $row++;
  # ---------- Data rows: one for each item 
  $optlist =  "fittextline={position={left center} " . $basefontoptions . "} marginright=2";
  for (my $i = 0; $i <  $#Substances+1; $i++) {
    $col = 1;
    # column 1: Drug of Chice
    $tbl = $p->add_table_cell($tbl, $col++, $row, $Substances[$i]{drug}, $optlist);
    # column 2: Amount Used
    $tbl = $p->add_table_cell($tbl, $col++, $row, $Substances[$i]{amount}, $optlist);
    # column 3: Frequency of Use
    $tbl = $p->add_table_cell($tbl, $col++, $row, $Substances[$i]{freq}, $optlist);
    # column 4: Age First Used 
    $tbl = $p->add_table_cell($tbl, $col++, $row, $Substances[$i]{age}, $optlist);
    # column 5: Date Last Used 
    $tbl = $p->add_table_cell($tbl, $col++, $row, $Substances[$i]{age}, $optlist);
    $row++;
  }
  $h_tbl = main->renderTable($p, $tbl, $marginleft, $Header2Info);
  $ypos += $h_tbl;
  main->renderTextline($p, "Functional impact of current use, give examples of level of dependency :", $marginleft, 15, $baseboldfontoptions, $Header2Info);
  $tf = $p->create_textflow($SubstanceImpact, $basefontoptions . " leading=120% alignment=justify");
  $h_tf = main->renderTextflow($p, $tf, $marginleft, $Header2Info);

  $ypos += $h_tf;

  main->renderTextline($p, "4. Medical / Physical :", $marginleft, 24, $baseboldlargefontoptions, $Header2Info);
  $p->fit_textline("SCORE", 445.9, $ypos, $baseboldlargefontoptions);
  $p->fit_textline($MedicalScorePast, 508.5, $ypos, $basefontoptions);
  $p->fit_textline($MedicalScoreCurrent, 547.2, $ypos, $basefontoptions);
  main->renderTextline($p, "Current Medical/ Physical conditions :", 59.5, 18.2, $baseboldfontoptions, $Header2Info);

# KLS instead of $medicalConditions, see MedicalConditions array ... output like Medications array
  $ypos += 4;
  $row = 1;
  $col = 1;
  $tbl = -1;
  for ($col=1; $col <= $#MedicalConditionsHeaders+1; $col++) {
    $optlist =  "fittextline={position={left center} $baseboldfontoptions}";
    $tbl = $p->add_table_cell($tbl, $col, $row, $MedicalConditionsHeaders[$col-1], $optlist . " colwidth=$MedicalConditionsHeaderWidths[$col-1]%");
  }
  $row++;
  # ---------- Data rows: one for each item 
  $optlist =  "fittextline={position={left center} " . $basefontoptions . "} marginright=2";
  for (my $i = 0; $i <  $#MedicalConditions+1; $i++) {
    $col = 1;
    # column 1: ICD10
    $tbl = $p->add_table_cell($tbl, $col++, $row, $MedicalConditions[$i]{icd10}, $optlist);
    # column 2: Sct Name
    $tbl = $p->add_table_cell($tbl, $col++, $row, $MedicalConditions[$i]{sctName}, $optlist);
    $row++;
  }
  $h_tbl = main->renderTable($p, $tbl, 59.5, $Header2Info);
  $ypos += $h_tbl;
  main->renderTextline($p, "Impact/ limitations on day-to-day function :", 59.5, 18.2, $baseboldfontoptions, $Header2Info);
  $tf = $p->create_textflow($MedicalImpact, $basefontoptions . " leading=120% alignment=justify");
  $h_tf = main->renderTextflow($p, $tf, 59.5, $Header2Info);
  $ypos += $h_tf;
  main->renderTextline($p, "Medications:", 59.5, 20, $baseboldmidfontoptions, $Header2Info);

  $ypos += 4;

  $row = 1;
  $col = 1;
  $tbl = -1;
  for ($col=1; $col <= $#MedicationsHeaders+1; $col++) {
    $optlist =  "fittextline={position={left center} $baseboldfontoptions}";
    $tbl = $p->add_table_cell($tbl, $col, $row, $MedicationsHeaders[$col-1], $optlist . " colwidth=$MedicationsHeaderWidths[$col-1]%");
  }
  $row++;
  # ---------- Data rows: one for each item 
  $optlist =  "fittextline={position={left center} " . $basefontoptions . "} marginright=2";
  for (my $i = 0; $i <  $#Medications+1; $i++) {
    $col = 1;
    # column 1: Physician
    $tbl = $p->add_table_cell($tbl, $col++, $row, $Medications[$i]{physician}, $optlist);
    # column 2: Medication
    $tbl = $p->add_table_cell($tbl, $col++, $row, $Medications[$i]{medication}, $optlist);
    # column 3: Type
    $tbl = $p->add_table_cell($tbl, $col++, $row, $Medications[$i]{type}, $optlist);
    # column 4: Date
    $tbl = $p->add_table_cell($tbl, $col++, $row, $Medications[$i]{date}, $optlist);
    # column 5: Reason
    $tbl = $p->add_table_cell($tbl, $col++, $row, $Medications[$i]{reason}, $optlist);
    $row++;
  }
  $h_tbl = main->renderTable($p, $tbl, 59.5, $Header2Info);

  $ypos += $h_tbl;

  main->renderTextline($p, "5. Family :", $marginleft, 24, $baseboldlargefontoptions, $Header2Info);
  $p->fit_textline("SCORE", 445.9, $ypos, $baseboldlargefontoptions);
  $p->fit_textline($FamilyScorePast, 508.5, $ypos, $basefontoptions);
  $p->fit_textline($FamilyScoreCurrent, 547.2, $ypos, $basefontoptions);
  main->renderTextline($p, "Currently resides with :", $marginleft, 15, $baseboldfontoptions, $Header2Info);
  $p->fit_textline($FamilyResides, 145, $ypos, $basefontoptions);
  main->renderTextline($p, "Problem areas :", $marginleft, 15, $baseboldfontoptions, $Header2Info);
  $p->fit_textline($FamilyProblem, 110, $ypos, $basefontoptions);
  main->renderTextline($p, "Evidenced by (specific examples, symptom frequency, duration and intensity, impact on daily functioning):", $marginleft, 15, $baseboldfontoptions, $Header2Info);
  $tf = $p->create_textflow($FamilyEvidencedBy, $basefontoptions . " leading=120% alignment=justify");
  $h_tf = main->renderTextflow($p, $tf, $marginleft, $Header2Info);

  $ypos += $h_tf;

  main->renderTextline($p, "6. Interpersonal :", $marginleft, 24, $baseboldlargefontoptions, $Header2Info);
  $p->fit_textline("SCORE", 445.9, $ypos, $baseboldlargefontoptions);
  $p->fit_textline($InterpersonalScorePast, 508.5, $ypos, $basefontoptions);
  $p->fit_textline($InterpersonalScoreCurrent, 547.2, $ypos, $basefontoptions);
  main->renderTextline($p, "Problem areas :", $marginleft, 15, $baseboldfontoptions, $Header2Info);
  $p->fit_textline($InterpersonalProblem, 110, $ypos, $basefontoptions);
  main->renderTextline($p, "Evidenced by (specific examples, symptom frequency, duration and intensity, impact on daily functioning):", $marginleft, 15, $baseboldfontoptions, $Header2Info);
  $tf = $p->create_textflow($InterpersonalEvidencedBy, $basefontoptions . " leading=120% alignment=justify");
  $h_tf = main->renderTextflow($p, $tf, $marginleft, $Header2Info);

  $ypos += $h_tf;

  main->renderTextline($p, "7. Role Performance :", $marginleft, 24, $baseboldlargefontoptions, $Header2Info);
  $p->fit_textline("SCORE", 445.9, $ypos, $baseboldlargefontoptions);
  $p->fit_textline($RoleScorePast, 508.5, $ypos, $basefontoptions);
  $p->fit_textline($RoleScoreCurrent, 547.2, $ypos, $basefontoptions);
  main->renderTextline($p, "Functional role :", $marginleft, 15, $baseboldfontoptions, $Header2Info);
  $p->fit_textline($RoleFrole, 115, $ypos, $basefontoptions);
  main->renderTextline($p, "Effectiveness of functionaing in identified role :", $marginleft, 15, $baseboldfontoptions, $Header2Info);
  $p->fit_textline($RoleEffectiveness, 250, $ypos, $basefontoptions);
  main->renderTextline($p, "Evidenced by (specific examples, symptom frequency, duration and intensity, impact on daily functioning):", $marginleft, 15, $baseboldfontoptions, $Header2Info);
  $tf = $p->create_textflow($RoleEvidencedBy, $basefontoptions . " leading=120% alignment=justify");
  $h_tf = main->renderTextflow($p, $tf, $marginleft, $Header2Info);

  $ypos += $h_tf;

  main->renderTextline($p, "8. Socio-Legal :", $marginleft, 24, $baseboldlargefontoptions, $Header2Info);
  $p->fit_textline("SCORE", 445.9, $ypos, $baseboldlargefontoptions);
  $p->fit_textline($SocioScorePast, 508.5, $ypos, $basefontoptions);
  $p->fit_textline($SocioScoreCurrent, 547.2, $ypos, $basefontoptions);
  main->renderTextline($p, "Problem areas :", $marginleft, 15, $baseboldfontoptions, $Header2Info);
  $p->fit_textline($SocioProblem, 110, $ypos, $basefontoptions);
  main->renderTextline($p, "Evidenced by (specific examples, symptom frequency, duration and intensity, impact on daily functioning):", $marginleft, 15, $baseboldfontoptions, $Header2Info);
  $tf = $p->create_textflow($SocioEvidencedBy, $basefontoptions . " leading=120% alignment=justify");
  $h_tf = main->renderTextflow($p, $tf, $marginleft, $Header2Info);

  $ypos += $h_tf;

  main->renderTextline($p, "9. Self-Care / Basic Needs :", $marginleft, 24, $baseboldlargefontoptions, $Header2Info);
  $p->fit_textline("SCORE", 445.9, $ypos, $baseboldlargefontoptions);
  $p->fit_textline("SCORE", 445.9, $ypos, $baseboldlargefontoptions);
  $p->fit_textline($SelfScorePast, 508.5, $ypos, $basefontoptions);
  $p->fit_textline($SelfScoreCurrent, 547.2, $ypos, $basefontoptions);
  main->renderTextline($p, "Problem areas :", $marginleft, 15, $baseboldfontoptions, $Header2Info);
  $p->fit_textline($SelfProblem, 110, $ypos, $basefontoptions);
  main->renderTextline($p, "Evidenced by (specific examples, symptom frequency, duration and intensity, impact on daily functioning):", $marginleft, 15, $baseboldfontoptions, $Header2Info);
  $tf = $p->create_textflow($SelfEvidencedBy, $basefontoptions . " leading=120% alignment=justify");
  $h_tf = main->renderTextflow($p, $tf, $marginleft, $Header2Info);

  $ypos += $h_tf;

  main->renderTextline($p, "COMMUNICATION (required for ICF/MR level of care)", $marginleft, 24, $baseboldlargefontoptions, $Header2Info);
  $p->fit_textline($Communication, 322, $ypos, $basefontoptions);
  $tf = $p->create_textflow($CommunicationComm1, $basefontoptions . " leading=120% alignment=justify");
  $h_tf = main->renderTextflow($p, $tf, $marginleft, $Header2Info);

  $ypos += $h_tf;

  main->renderTextline($p, "SUBSTANCE ABUSE", $marginleft, 24, $baseboldlargefontoptions_u, $Header2Info);

# KLS use above variables for output...
  if ( $rClientPrAuthCDC->{'Age'} <= 11 || $rClientPrAuthCDC->{'Age'} >= 18 )    # print the ASI 
  {
    main->renderTextline($p, "ASI:", $marginleft, 20.5, $baseboldlargefontoptions_u, $Header2Info);
    main->renderTextline($p, "Medical ", $marginleft, 20.5, $baseboldlargefontoptions, $Header2Info);
    $p->fit_textline($ASIMedical, 157, $ypos, $basefontoptions);
    main->renderTextline($p, "Employ / Support ", $marginleft, 20.5, $baseboldlargefontoptions, $Header2Info);
    $p->fit_textline($ASIemploy, 157, $ypos, $basefontoptions);
    main->renderTextline($p, "Alcohol Use ", $marginleft, 20.5, $baseboldlargefontoptions, $Header2Info);
    $p->fit_textline($ASIAlcohol, 157, $ypos, $basefontoptions);
    main->renderTextline($p, "Drug Use ", $marginleft, 20.5, $baseboldlargefontoptions, $Header2Info);
    $p->fit_textline($ASIDrug, 157, $ypos, $basefontoptions);
    main->renderTextline($p, "Legal Status ", $marginleft, 20.5, $baseboldlargefontoptions, $Header2Info);
    $p->fit_textline($ASILegal, 157, $ypos, $basefontoptions);
    main->renderTextline($p, "Family / Social Rel ", $marginleft, 20.5, $baseboldlargefontoptions, $Header2Info);
    $p->fit_textline($ASIFamily, 157, $ypos, $basefontoptions);
    main->renderTextline($p, "Psychiatric Status ", $marginleft, 20.5, $baseboldlargefontoptions, $Header2Info);
    $p->fit_textline($ASIPsych, 157, $ypos, $basefontoptions);
  }
  else                                                                           # print the TASI
  {
    main->renderTextline($p, "TASI:", $marginleft, 20.5, $baseboldlargefontoptions_u, $Header2Info);
    main->renderTextline($p, "Chemical ", $marginleft, 20.5, $baseboldlargefontoptions, $Header2Info);
    $p->fit_textline($TASIChemical, 157, $ypos, $basefontoptions);
    main->renderTextline($p, "School ", $marginleft, 20.5, $baseboldlargefontoptions, $Header2Info);
    $p->fit_textline($TASISchool, 157, $ypos, $basefontoptions);
    main->renderTextline($p, "Emp / Sup ", $marginleft, 20.5, $baseboldlargefontoptions, $Header2Info);
    $p->fit_textline($TASIEmploy, 157, $ypos, $basefontoptions);
    main->renderTextline($p, "Family ", $marginleft, 20.5, $baseboldlargefontoptions, $Header2Info);
    $p->fit_textline($TASIFamily, 157, $ypos, $basefontoptions);
    main->renderTextline($p, "Peer / Soc ", $marginleft, 20.5, $baseboldlargefontoptions, $Header2Info);
    $p->fit_textline($TASIPeer, 157, $ypos, $basefontoptions);
    main->renderTextline($p, "Legal ", $marginleft, 20.5, $baseboldlargefontoptions, $Header2Info);
    $p->fit_textline($TASILegal, 157, $ypos, $basefontoptions);
    main->renderTextline($p, "Psychiatric ", $marginleft, 20.5, $baseboldlargefontoptions, $Header2Info);
    $p->fit_textline($TASIPsych, 157, $ypos, $basefontoptions);
  }

  main->createFooter($p);
  main->createHeader2($p, $Header2Info);

  main->renderTextline($p, "SERVICES REQUESTED ", $pagewidth / 2, 35.6, $baseboldlargefontoptions_ui . " position={center bottom}", $Header2Info);
  $ypos += $fontsizexlarge;
  $tf = $p->create_textflow($servicesreq, $basemidfontoptions . " leading=130% alignment=justify");
  $h_tf = main->renderTextflow($p, $tf, $marginleft, $Header2Info);
  $ypos += $h_tf;
  main->createFooter($p);
  main->createHeader2($p, $Header2Info);

  $ypos += 22.1;
  $p->fit_textline("ADDENDUM", $pagewidth / 2, $ypos, $baseboldxlargefontoptions . " position={center bottom}");
  $ypos += $fontsizelarge;
  $tf = $p->create_textflow("Completion of this page of the request packet is optional for the provider. The items listed on this page, however, may be required documentation for SURS reviews, CARF certification and/or JCAHO certification. Please do not submit this form as part of the request packet unless instructed to do so on a specific request by a review coordinator.",
    $basemidfontoptions . " leading=130% alignment=justify");
  $h_tf = main->renderTextflow($p, $tf, $marginleft, $Header2Info);
  $ypos += $h_tf;

  main->renderTextline($p, "COMMUNITY INTEGRATION:", $marginleft, 20.5, $baseboldlargefontoptions, $Header2Info);
  $tf = $p->create_textflow($community, $basefontoptions . " leading=120% alignment=justify");
  $h_tf = main->renderTextflow($p, $tf, $marginleft, $Header2Info);
  $ypos += $h_tf;
  main->renderTextline($p, "CAREGIVER RESOURCES (for clients under age of 21):", $marginleft, 20.5, $baseboldlargefontoptions, $Header2Info);
  $tf = $p->create_textflow($caregiver, $basefontoptions . " leading=120% alignment=justify");
  $h_tf = main->renderTextflow($p, $tf, $marginleft, $Header2Info);
  $ypos += $h_tf;
  main->renderTextline($p, "COLLABORATION WITH SCHOOL SYSTEM (SCHOOL agechildren only):", $marginleft, 20.5, $baseboldlargefontoptions, $Header2Info);
  $tf = $p->create_textflow($collaboration, $basefontoptions . " leading=120% alignment=justify");
  $h_tf = main->renderTextflow($p, $tf, $marginleft, $Header2Info);
  $ypos += $h_tf;
  main->renderTextline($p, "REFERRALS TO OTHER COMMUNITY SERVICES", $marginleft, 20.5, $baseboldlargefontoptions, $Header2Info);
  $tf = $p->create_textflow($referrals, $basefontoptions . " leading=120% alignment=justify");
  $h_tf = main->renderTextflow($p, $tf, $marginleft, $Header2Info);
  $ypos += $h_tf;

  main->createFooter($p);
}

sub createEmptyPage {
  my ($self, $p) = @_;

  $p->begin_page_ext($pagewidth, $pageheight, "topdown");
  $p->fit_textline("NOT FOUND", $marginleft, 50, $basefontoptions);
  $p->end_page_ext("");
}

sub createHeader {
  my ($self, $p, $rAgency, $rInsurance) = @_;

  my $InsuranceName = $rInsurance->{'Name'};
  my $Address = "$rInsurance->{'Addr1'} $rInsurance->{'Addr2'}\n$rInsurance->{'City'}, $rInsurance->{'ST'} $rInsurance->{'Zip'}";
  my $OffceFax = "Office: $rInsurance->{'Ph1'}  Fax: $rInsurance->{'Fax'}";

  my $tf;

  $p->begin_page_ext($pagewidth, $pageheight, "topdown");
  $ypos = $margintop;

  $ypos += $fontsizelarge;
  $p->fit_textline($InsuranceName, $pagewidth / 2, $ypos, $baseboldlargefontoptions . " position={center bottom}");

  my $h_address = 2 * $fontsizexxlarge;
  $ypos += $h_address;
  my $w_address = 150;
  my $x_address = $pagewidth / 2 - $w_address / 2;
  $tf = $p->create_textflow($Address, $baseboldlargefontoptions . " leading=110% alignment=justify lastalignment=center");
  $p->fit_textflow($tf, $x_address, $ypos, $x_address+$w_address, $ypos - $h_address, "verticalalign=center");

  $ypos += $fontsizelarge;
  $p->fit_textline($OffceFax, $pagewidth / 2, $ypos, $baseboldlargefontoptions . " position={center bottom}");

  # -----------------------------------
  # Place image of logo
  # -----------------------------------
  my $y_offsetlogo = 2;
  $ypos += $y_offsetlogo;
  my $h_logo = $ypos - $margintop;
  my $w_logo = 150;
  
  my ($logodirectory, $logofilename) = $rAgency->{'LOGO'} =~ m/(.*\/)(.*)$/;
  if ( $logofilename eq '' ) { $logofilename = 'logo.png'; }
  elsif ( not -e "/usr/local/PDFlib/${logofilename}" ) { $logofilename = 'logo.png'; }
  my $logoimage = $p->load_image("auto", $logofilename, "");
  $p->fit_image($logoimage, $marginleft, $ypos, "boxsize={" . $w_logo . " " .  $h_logo . "} fitmethod=meet");
  $p->close_image($logoimage);
  ##

  $ypos += $fontsizexxlarge;

}

sub createHeader2 {
  my ($self, $p, $Header2Info) = @_;

  $p->begin_page_ext($pagewidth, $pageheight, "topdown");
  $ypos = $margintop2;

  $ypos += 7.6;
  $p->fit_textline("Client Name :", 37, $ypos, $baseboldmidfontoptions);
# KLS I DON'T KNOW HOW YOU WANT TO PASS THESE INTO THIS ROUTINE??
# KLS use cname variable
  $p->fit_textline($Header2Info->{"clientName"}, 108.5, $ypos, $basefontoptions);
  $p->fit_textline("Group Provider # :", 257.5, $ypos, $baseboldmidfontoptions);
# KLS use $rContracts->{'PIN'} variable
  $p->fit_textline($Header2Info->{"groupProvider"}, 353.3, $ypos, $basefontoptions);
  $p->fit_textline("Date Completed :", 433.2, $ypos, $baseboldmidfontoptions);
# KLS use $dcompleted variable
  $p->fit_textline($Header2Info->{"dateCompleted"}, 523.7, $ypos, $basefontoptions);
  $ypos += 20.3;
  $p->fit_textline("Recipient ID# :", 37, $ypos, $baseboldmidfontoptions);
# KLS use $recipientID variable
  $p->fit_textline($Header2Info->{"recipientID"}, 113.8, $ypos, $basefontoptions);
  $p->fit_textline("Rendering Provider # :", 257.5, $ypos, $baseboldmidfontoptions);
# KLS use $RendProvPIN variable
  $p->fit_textline($Header2Info->{"renderingProvider"}, 373, $ypos, $basefontoptions);
  $ypos += $fontsizesmall;

}

sub createFooter {
  my ($self, $p) = @_;

  my $tf;
  my $optlist;

  my $footertext = "<fontname=$boldfontname encoding=unicode>Confidentiality of drug/alcohol abuse records is protected by Federal Law." .
    "<fontname=$fontname encoding=unicode> Federal regulations (42 CFR, Part 2 prohibits making any further disclosure of this information unless further disclosure is expressively permitted by written consent of the person to whom it pertains or as otherwise permitted by 42 CFR, Part 2. A GENERAL AUTHORIZATION FOR RELEASE OF MEDICAL OR OTHER INFORMATION IS NOT SUFFICIENT FOR THIS PURPOSE. The Federal rules restrict any use of the information to criminally investigate or prosecute any alcohol/drug abuse client.";

  $optlist = $basesmallfontoptions . " leading=120% alignment=justify";
  $tf = $p->create_textflow($footertext, $optlist);
  $p->fit_textflow($tf, $marginleft, $marginbottom,
      $marginleft+$contentwidth, $y_footer, "verticalalign=bottom");

  $p->fit_textline("Page " . (++$pagecount), 268.4, $marginbottom + 14, $baseboldmidfontoptions);
  $p->suspend_page("");
}

sub createPageCount {
  my ($self, $p) = @_;

  for(my $i = 1; $i < $pagecount+1; $i++) {
    # Revisit page $i
    $p->resume_page("pagenumber $i");

    # Add the total number of pages
    $p->fit_textline(" of " . $pagecount, 303, $marginbottom + 14, $baseboldmidfontoptions);
    $p->end_page_ext("");
  }
}

sub renderTextflow {
  my ($self, $p, $tf, $xpos, $Header2Info) = @_;
  my $result;
  my $h_tf;

  do {
    $result = $p->fit_textflow($tf, $xpos, $y_footer, $marginleft + $contentwidth, $ypos, "");
    if ($result eq "_boxfull" || $result eq "_boxempty") {
      main->createFooter($p);
      main->createHeader2($p, $Header2Info);
    }
  } while ($result ne "_stop");
  $h_tf = $p->info_textflow($tf, "textheight");

  return $h_tf;
}


sub renderTable {
  my ($self, $p, $tbl, $xpos, $Header2Info) = @_;
  my $result;
  my $h_tbl;
  my $RowHeightLimit = 10;
  my $diff;

  $diff = $y_footer - $ypos;
  if ($diff <= $RowHeightLimit) {
    main->createFooter($p);
    main->createHeader2($p, $Header2Info);
  }
  do {
    $result = $p->fit_table($tbl, $xpos, $y_footer, $marginleft + $contentwidth, $ypos, "");
    if ($result eq "_boxfull") {
      main->createFooter($p);
      main->createHeader2($p, $Header2Info);
    }
  } while ($result eq "_boxfull");
  $h_tbl = $p->info_table($tbl, "height");
  
  return $h_tbl;
}

sub renderTextline {
  my ($self, $p, $text, $xpos, $h_tl, $optlist, $Header2Info) = @_;

  if ($ypos + $h_tl > $y_footer) {
    main->createFooter($p);
    main->createHeader2($p, $Header2Info);
  }
  $ypos += $h_tl;
  $p->fit_textline($text, $xpos, $ypos, $optlist);
}

############################################################################
sub getHospitalTreatments            # can't used IntDate because it may be partial date
{
  my ($self,$ClientID) = @_;
  my @HospitalTreatments = ();
  my $cnt = 0;
  my $sHospital = $dbh->prepare("select * from Hospital where ClientID=? order by IntDate desc");
  $sHospital->execute($ClientID);
  while ( my $rHospital = $sHospital->fetchrow_hashref )
  {
    $cnt++;
    my $HospitalTreatment = ();
    $HospitalTreatment->{'dates'} = DBUtil->Date($rHospital->{IntDate},'fmt','MM/DD/YYYY') . ' - '
                                  . DBUtil->Date($rHospital->{RelDate},'fmt','MM/DD/YYYY');
    my $npi = $rHospital->{HospIDNPI} ? $rHospital->{HospIDNPI} : $rHospital->{FacIDNPI};
    my $rxNPI = DBA->selxref($form,'xNPI','NPI',$npi);
    $HospitalTreatment->{'facility'} => $rxNPI->{'ProvOrgName'};
    $HospitalTreatment->{'ip'} = DBA->getxref($form,'xHospType',$rHospital->{'Type'},'Text');
    $HospitalTreatment->{'reason'} = $rHospital->{'Reason'};
    push(@HospitalTreatments,$HospitalTreatment);
  }
  $sHospital->finish();
  return(@HospitalTreatments);
}
sub getSubstanceAbuse
{
  my ($self,$ClientID,$TheDate) = @_;
  my @Substances = ();
  my $cnt = 0;
  my $sSAbuse = $dbh->prepare("select * from SAbuse where ClientID=? and ( FromDate<='${TheDate}' and '${TheDate}'<=ToDate ) order by ToDate desc");
  $sSAbuse->execute($ClientID);
  while ( my $rSAbuse = $sSAbuse->fetchrow_hashref )
  {
    $cnt++;
    my $Substance = ();
    $Substance->{'drug'} = DBA->getxref($form,'xDrugs',$rSAbuse->{'Drug'},'Descr');
    $Substance->{'amount'} = $rSAbuse->{'Amount'};
    $Substance->{'freq'} = DBA->getxref($form,'xFreqs',$rSAbuse->{'Freq'},'Descr');
    $Substance->{'age'} = $rSAbuse->{'Age'};
    $Substance->{'date'} = DBUtil->Date($rSAbuse->{'FromDate'},'fmt','MM/DD/YYYY');
    push(@Substances,$Substance);
  }
  $sSAbuse->finish();
  return(@Substances);
}
sub getMedications            # can't used StartDate because PDMed may be partial date. PrescriptDate is datetime?
{
  my ($self,$ClientID) = @_;
  my @Medications = ();
  my $cnt = 0;
  my $rMeds = DBA->getMeds($form,$ClientID);
  foreach my $f ( sort keys %{ $rMeds } )
  {
    $cnt++;
    my $Medication = ();
#warn qq|rMeds: ${f} = $rMeds->{$f}\n|;
    my ($date,$time) = split(' ',$rMeds->{$f}->{'DrugDate'});
    my $drugdate = DBUtil->Date($date,'fmt','MM/DD/YYYY');
    $Medication->{'physician'} = $rMeds->{$f}->{'PhysicianName'};
    $Medication->{'medication'} = $rMeds->{$f}->{'DrugInfo'};
    $Medication->{'type'} = $rMeds->{$f}->{'DrugType'};
    $Medication->{'date'} = $drugdate;
    $Medication->{'reason'} = '';
    push(@Medications,$Medication);
  }
  return(@Medications);
}
sub getProblems
{
  my ($self,$ClientID,$TheDate) = @_;
  my @Problems = ();
  my $cnt = 0;
  my $sClientProblems = $dbh->prepare("
select ClientProblems.ClientID,ClientProblems.Priority,misICD10.ICD10,misICD10.icdName,misICD10.sctName
 from ClientProblems
  left join okmis_config.misICD10 on misICD10.ID=ClientProblems.UUID
 where ClientProblems.ClientID=? and misICD10.ICD10 NOT LIKE 'F%'
   and ( InitiatedDate<='${TheDate}' and '${TheDate}'<=ResolvedDate ) 
 order by ClientProblems.Priority
");
  $sClientProblems->execute($ClientID);
  while ( my $rClientProblems = $sClientProblems->fetchrow_hashref )
  {
    $cnt++;
    my $Problem = ();
    $Problem->{'icd10'} = $rClientProblems->{'ICD10'};
    $Problem->{'sctName'} = $rClientProblems->{'sctName'};
    push(@Problems,$Problem);
  }
  $sClientProblems->finish();
  return(@Problems);
}
sub xText
{
  my ($self,$xref,$r) = @_;
  my ($out,$dlm) = ('','');
  foreach my $f ( sort keys %{ $xref } )
  { 
    if ( $r->{$f} == 1 )
    { $out .= qq|${dlm}$xref->{$f}{'Descr'}|; $dlm = qq|; |; }
  }
  return($out);
}
############################################################################
