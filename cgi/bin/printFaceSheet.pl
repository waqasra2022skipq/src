#!/usr/bin/perl
############################################################################
use lib '/home/okmis/mis/src/lib';
use myForm;
use myDBI;
use Config;
use MgrTree;
use DBA;
use cBill;

use PDFlib::PDFlib;
use strict;
############################################################################
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
my $basefontoptions = "fontname=" . $fontname . " fontsize=" . $fontsize . " embedding encoding=unicode charref";
my $basefontoptions_i = $basefontoptions . " fontstyle=italic";
my $baseboldfontoptions = "fontname=" . $boldfontname . " fontsize=" . $fontsize . " embedding encoding=unicode";
my $baseboldfontoptions_u = $baseboldfontoptions . " underline=true underlineposition=-15% underlinewidth=0.3";
my $basemidfontoptions = $basefontoptions . " fontsize=" . $fontsizemid;
my $basemidfontoptions_i = $basemidfontoptions . " fontstyle=italic";
my $baseboldmidfontoptions = $baseboldfontoptions . " fontsize=" . $fontsizemid;
my $baseboldmidfontoptions_u = $baseboldmidfontoptions . " underline=true underlineposition=-15% underlinewidth=0.3";
my $baselargefontoptions = $basefontoptions . " fontsize=" . $fontsizelarge;
my $baseboldlargefontoptions = $baseboldfontoptions . " fontsize=" . $fontsizelarge;
my $baseboldlargefontoptions_u = $baseboldlargefontoptions . " underline=true underlineposition=-15% underlinewidth=0.3";
my $baseboldlargefontoptions_ui = $baseboldlargefontoptions_u . " fontstyle=italic";
my $baseboldlargefontoptions_i = $baseboldlargefontoptions . " fontstyle=italic";
my $basesmallfontoptions = $basefontoptions . " fontsize=" . $fontsizesmall;
my $baseboldsmallfontoptions = $baseboldfontoptions . " fontsize=" . $fontsizesmall;
my $basemidlargefontoptions = $basefontoptions . " fontsize=" . $fontsizemidlarge;
my $baseboldmidlargefontoptions = $baseboldfontoptions . " fontsize=" . $fontsizemidlarge;
my $baseboldmidlargefontoptions_u = $baseboldmidlargefontoptions . " underline=true underlineposition=-15% underlinewidth=0.3";
my $baseboldxlargefontoptions = $baseboldfontoptions . " fontsize=" . $fontsizexlarge;
my $basecheckfontoptions = "fontname={DejaVuSans} encoding=unicode fontsize=10 charref";

my $marginleft = 32.4;
my $margintop = 35;
my $marginbottom = $pageheight - 33.8;
my $contentwidth = $pagewidth - 2 * $marginleft;
my $h_footer = 4 * $fontsizelarge;
my $y_footer = $marginbottom - $h_footer;

my $ypos = $margintop;
my $pagecount = 0;
############################################################################

my $form = myForm->new();

#warn "printFaceSheet: IDs=$form->{'IDs'}\n";
my $IDs = $form->{'IDs'};
# $IDs = '30099';

my $dbh = myDBI->dbconnect($form->{'DBNAME'});
my $sClient = $dbh->prepare("select * from Client where ClientID=?");
my $sClientIntake = $dbh->prepare("select * from ClientIntake where ClientID=?");
my $sClientReferrals = $dbh->prepare("select * from ClientReferrals where ClientID=?");
# get the last Admission Date...
my $sClientAdmit = $dbh->prepare("select * from ClientAdmit where ClientID=? order by AdmitDate desc");
my $sClientVitalSigns = $dbh->prepare("select * from ClientVitalSigns where ClientID=? order by VDate desc");
my $sClientFamily = $dbh->prepare("select * from ClientFamily where ClientID=? and EmerContact=1");
my $sClientEmergency = $dbh->prepare("select * from ClientEmergency where ClientID=?");
my $sInsurance = $dbh->prepare("
select * from Insurance 
  left join Guarantor on Insurance.InsNumID=Guarantor.InsuranceID
 where Insurance.ClientID=? and Insurance.Priority=? 
 order by Insurance.InsNumEffDate desc, Insurance.InsNumExpDate
");
my $sProvider = $dbh->prepare("select * from Provider where ProvID=?");

my $filename = '/tmp/'.$form->{'LOGINID'}.'_'.DBUtil->genToken().'_'.DBUtil->Date('','stamp').'.pdf';
my $outfile = $form->{'file'} eq ''                # create and print pdf else just create.
              ? $form->{'DOCROOT'}.$filename
              : $form->{'file'};
# $outfile = 'kls.pdf';
#warn qq|outfile=${outfile}\n|;
############################################################################

eval
{
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
    $p->set_info("Author", "Vladimir Martyshov");
    $p->set_info("Title", "Face Sheet");

    main->printFS($p);

    $p->end_document("");

};

if ($@) {
  die("$0: PDFlib Exception occurred:\n$@");
}

$sClient->finish();
$sClientIntake->finish();
$sClientReferrals->finish();
$sClientAdmit->finish();
$sClientVitalSigns->finish();
$sClientFamily->finish();
$sClientEmergency->finish();
$sInsurance->finish();
$sProvider->finish();
myDBI->cleanup();
if ( $form->{'file'} eq '' )                # create and print pdf.
{ print qq|Location: ${filename}\n\n|; }
exit;
############################################################################
sub printFS
{
  my ($self,$p) = @_;

  foreach my $ClientID ( split(' ', $IDs) )
  {
    #warn qq|test ID: |.$ClientID."\n";
    $sClient->execute($ClientID) || myDBI->dberror("printFaceSheet: select Client ${ClientID}");
    if (my $rClient = $sClient->fetchrow_hashref) {
      main->createPages($p, $rClient);
    }
  }

  if ($pagecount) {
    main->createPageCount($p);
  } else {
    main->createEmptyPage($p);
  }
}

sub createPages {
  my ($self, $p, $rClient) = @_;

  my $AgencyID = MgrTree->getAgency($form,$rClient->{'clinicClinicID'});
  my $sProvider = $dbh->prepare("select * from Provider where ProvID=?");
  $sProvider->execute($AgencyID) || myDBI->dberror("setAgency: select Provider ${AgencyID}");
  my $rAgency = $sProvider->fetchrow_hashref;
  my $AgencyName = $rAgency->{'Name'};
  my $AgencyAddr = $rAgency->{'Addr1'} . ', ';
  $AgencyAddr .= $rAgency->{'Addr2'} . ', ' if ( $rAgency->{'Addr2'} );
  my $AgencyCSZ .= $rAgency->{'City'} . ', ' . $rAgency->{'ST'} . '  ' . $rAgency->{'Zip'};
  my $AgencyPh = 'Office: ' . $rAgency->{'WkPh'} . '  Fax: ' . $rAgency->{'Fax'};
##
# Client info...
my $ClientID = $rClient->{'ClientID'};

#warn qq|add ID: |.$ClientID."\n";
  $sClientIntake->execute($ClientID) || myDBI->dberror("printFaceSheet: select ClientIntake ${ClientID}");
  my $rClientIntake = $sClientIntake->fetchrow_hashref;
  $sClientReferrals->execute($ClientID) || myDBI->dberror("printFaceSheet: select ClientReferrals ${ClientID}");
  my $rClientReferrals = $sClientReferrals->fetchrow_hashref;
  $sClientAdmit->execute($ClientID) || myDBI->dberror("printFaceSheet: select ClientAdmit ${ClientID}");
  my $rClientAdmit = $sClientAdmit->fetchrow_hashref;
# IntakeProvID
  my $IntakeProvID = $rClientAdmit->{'ProvID'};
  $sProvider->execute($IntakeProvID) || myDBI->dberror("printFaceSheet: select IntakeProvID ${IntakeProvID}");
  my $rIntakeProvider = $sProvider->fetchrow_hashref;
# Set Emergency Information (from Family desinated Emergency member)
  $sClientFamily->execute($ClientID);
  my $rClientEmergency = $sClientFamily->fetchrow_hashref;
# Physician 
  $sClientEmergency->execute($ClientID);
  my $rClientEmergencyCare = $sClientEmergency->fetchrow_hashref;  # NOT rClientEmergency, see above.
  $sClientVitalSigns->execute($ClientID);
  my $rClientVitalSigns = $sClientVitalSigns->fetchrow_hashref;

# KLS
  my $RefSourceID = $rClientReferrals->{'ReferredBy1NPI'};
  my $rReferral = $RefSourceID ? DBA->selxref($form,'xNPI','NPI',$RefSourceID) : ();

######################################

  my $HeaderInfo = { 
    'companyname' => $AgencyName, 
    'companyaddr' =>  $AgencyAddr, 
    'companycsz' => $AgencyCSZ, 
    'companyphone' => $AgencyPh,
                   };
  my $tf;
  my $h_tf;
######################################

  main->createHeader($p, $HeaderInfo);

  $ypos += $fontsizexxlarge;
  $p->fit_textline("REFERRAL SOURCE / REASON", $marginleft, $ypos, $baseboldmidlargefontoptions);

  $ypos += 18;
  $p->fit_textline("Referred Date:", $marginleft, $ypos, $baseboldfontoptions);
  $p->fit_textline($rClientReferrals->{'RefDate'}, 97.9, $ypos, $basefontoptions);
  $p->fit_textline("Referred By:", 151.8, $ypos, $baseboldfontoptions);
  $p->fit_textline("$rReferral->{'ProvOrgName'} $rReferral->{'ProvPrefix'} $rReferral->{'ProvFirstName'} $rReferral->{'ProvLastName'}", 208, $ypos, $basefontoptions);
  $p->fit_textline("Phone:", 393.2, $ypos, $baseboldfontoptions);
  $p->fit_textline($rReferral->{'WkPh'}, 426, $ypos, $basefontoptions);

  $ypos += 14.8;
  $p->fit_textline("Reason for Referral:", $marginleft, $ypos, $baseboldfontoptions);
  $tf = $p->create_textflow($rClientReferrals->{'RefReason'}, $basefontoptions . " leading=120% alignment=justify");
  $h_tf = main->renderTextflow($p, $tf, $marginleft, $contentwidth, $HeaderInfo);
  $ypos += $h_tf;

  main->renderTextline($p, "Initial Intake Information", $marginleft, 18, $baseboldfontoptions_u, $HeaderInfo);

  main->renderTextline($p, "Intake Date:", $marginleft, 14.8, $baseboldfontoptions, $HeaderInfo);
  my $admitdate = DBUtil->Date($rClientAdmit->{AdmitDate},'fmt','MM/DD/YYYY');
  my $admittime = substr($rClientAdmit->{AdmitTime},0,5);
  $p->fit_textline("${admitdate} @ ${admittime}", 87, $ypos, $basefontoptions);
  $p->fit_textline("Staff:", 180, $ypos, $baseboldfontoptions);
  (my $staff = qq|$rIntakeProvider->{'Pref'} $rIntakeProvider->{'FName'} $rIntakeProvider->{'LName'}|) =~ s/\d//g;
  $p->fit_textline(${staff}, 206, $ypos, $basefontoptions);

  main->renderTextline($p, "IDENTIFYING INFORMATION", $marginleft, 27, $baseboldmidlargefontoptions, $HeaderInfo);

  my $name = qq|$rClient->{'LName'}, $rClient->{'FName'} $rClient->{'MName'} (${ClientID})|;
  my $addr = $rClient->{'Addr1'};
  $addr .= $rClient->{'Addr2'} if ( $rClient->{'Addr2'} ne '' );
  $addr .= qq|, $rClient->{'City'}| if ( $rClient->{'City'} ne '' );
  $addr .= qq|, $rClient->{'ST'}| if ( $rClient->{'ST'} ne '' );
  $addr .= qq| $rClient->{'Zip'}| if ( $rClient->{'Zip'} ne '' );
  my $age = DBUtil->Date($rClient->{'DOB'},'age');
  my $dob = DBUtil->Date($rClient->{'DOB'},'fmt','MM/DD/YYYY');
  main->renderTextline($p, "Name:", $marginleft, 18, $baseboldfontoptions);
  $p->fit_textline(${name}, 63, $ypos, $basefontoptions);
  
  main->renderTextline($p, "Address:", $marginleft, 14.8, $baseboldfontoptions);
  $p->fit_textline(${addr}, 75, $ypos, $basefontoptions);

  main->renderTextline($p, "Home Phone:", $marginleft, 14.8, $baseboldfontoptions);
  $p->fit_textline($rClient->{'HmPh'}, 93, $ypos, $basefontoptions);
  $p->fit_textline("Work Phone:", 213, $ypos, $baseboldfontoptions);
  $p->fit_textline($rClient->{'WkPh'}, 271, $ypos, $basefontoptions);
  $p->fit_textline("Email:", 393, $ypos, $baseboldfontoptions);
  $p->fit_textline($rClient->{'Email'}, 423, $ypos, $basefontoptions);

  main->renderTextline($p, "Place of Birth:", $marginleft, 14.8, $baseboldfontoptions);
  $p->fit_textline($rClientIntake->{'POB'}, 96, $ypos, $basefontoptions);
  $p->fit_textline("SSN:", 213, $ypos, $baseboldfontoptions);
  $p->fit_textline($rClient->{'SSN'}, 238, $ypos, $basefontoptions);
  $p->fit_textline("DOB:", 393, $ypos, $baseboldfontoptions);
  $p->fit_textline(${dob}, 419, $ypos, $basefontoptions);

  my $weight = qq|$rClientVitalSigns->{'Weight'} lbs|;
  my $height = qq|$rClientVitalSigns->{'HeightFeet'} ft. $rClientVitalSigns->{'HeightInches'} in.|;
  main->renderTextline($p, "Height:", $marginleft, 14.8, $baseboldfontoptions);
  $p->fit_textline(${height}, 68, $ypos, $basefontoptions);
  $p->fit_textline("Weight:", 213, $ypos, $baseboldfontoptions);
  $p->fit_textline(${weight}, 250, $ypos, $basefontoptions);
  $p->fit_textline("Age:", 393, $ypos, $baseboldfontoptions);
  $p->fit_textline(${age}, 417, $ypos, $basefontoptions);
  $p->fit_textline("Gender:", 440, $ypos, $baseboldfontoptions);
  $p->fit_textline($rClient->{'Gend'}, 478, $ypos, $basefontoptions);

  main->renderTextline($p, "GUARANTOR INFORMATION", $marginleft, 27, $baseboldmidlargefontoptions);

  my $rGuarantor = ();
  $sInsurance->execute($ClientID,1);
  if ( my $rInsurance = $sInsurance->fetchrow_hashref )
  {
    $rGuarantor = $rInsurance->{'ClientRel'} eq 'I' || $rInsurance->{'ClientRel'} eq '' ? $rClient : $rInsurance;
    my $gtorname = qq|$rGuarantor->{'FName'} $rGuarantor->{'LName'}|;
    my $gtoraddr = $rGuarantor->{'Addr1'};
    $gtoraddr .= $rGuarantor->{'Addr2'} if ( $rGuarantor->{'Addr2'} ne '' );
    $gtoraddr .= qq|, $rGuarantor->{'City'}| if ( $rGuarantor->{'City'} ne '' );
    $gtoraddr .= qq|, $rGuarantor->{'ST'}| if ( $rGuarantor->{'ST'} ne '' );
    $gtoraddr .= qq| $rGuarantor->{'Zip'}| if ( $rGuarantor->{'Zip'} ne '' );
    my $gtorwkph = $rGuarantor->{'WkPh'};
    my $gtorage = DBUtil->Date($rGuarantor->{'DOB'},'age');
    my $gtordob = DBUtil->Date($rGuarantor->{'DOB'},'fmt','MM/DD/YYYY');

    main->renderTextline($p, "Name:", $marginleft, 18, $baseboldfontoptions);
    $p->fit_textline(${gtorname}, 63, $ypos, $basefontoptions);

    main->renderTextline($p, "Address:", $marginleft, 14.8, $baseboldfontoptions);
    $p->fit_textline(${gtoraddr}, 75, $ypos, $basefontoptions);

    main->renderTextline($p, "Home Phone:", $marginleft, 14.8, $baseboldfontoptions);
    $p->fit_textline($rGuarantor->{'HmPh'}, 93, $ypos, $basefontoptions);
    $p->fit_textline("Work Phone:", 213, $ypos, $baseboldfontoptions);
    $p->fit_textline($rGuarantor->{'WkPh'}, 271, $ypos, $basefontoptions);
    $p->fit_textline("Email:", 393, $ypos, $baseboldfontoptions);
    $p->fit_textline($rGuarantor->{'Email'}, 423, $ypos, $basefontoptions);

    main->renderTextline($p, "Employer:", $marginleft, 14.8, $baseboldfontoptions);
    $p->fit_textline($rGuarantor->{'Empl'}, 80, $ypos, $basefontoptions);
    $p->fit_textline("SSN:", 213, $ypos, $baseboldfontoptions);
    $p->fit_textline($rGuarantor->{'SSN'}, 238, $ypos, $basefontoptions);
    $p->fit_textline("DOB:", 393, $ypos, $baseboldfontoptions);
    $p->fit_textline(${gtordob}, 419, $ypos, $basefontoptions);
  }
  else
  { main->renderTextline($p, "No Primary Insurance reported.", $marginleft, 14.8, $HeaderInfo); }

  main->renderTextline($p, "IN CASE OF AN EMERGENCY", $marginleft, 27, $baseboldmidlargefontoptions);
  $p->fit_textline('(Parent/Guarantor if client is under 18 or under legal guardianship)', 207, $ypos - 1, $basemidfontoptions);

  my $emername = qq|$rClientEmergency->{'FName'} $rClientEmergency->{'LName'}|;
  my $emeraddr = $rClientEmergency->{'Addr1'};
  $emeraddr .= $rClientEmergency->{'Addr2'} if ( $rClientEmergency->{'Addr2'} ne '' );
  $emeraddr .= qq|, $rClientEmergency->{'City'}| if ( $rClientEmergency->{'City'} ne '' );
  $emeraddr .= qq|, $rClientEmergency->{'ST'}| if ( $rClientEmergency->{'ST'} ne '' );
  $emeraddr .= qq| $rClientEmergency->{'Zip'}| if ( $rClientEmergency->{'Zip'} ne '' );
  my $emerwkph = $rClientEmergency->{'WkPh'};
  my $erelation = DBA->getxref($form,'xRelationship',$rClientEmergency->{'Rel'},'Descr');

  main->renderTextline($p, "Name:", $marginleft, 18, $baseboldfontoptions);
  $p->fit_textline(${emername}, 63, $ypos, $basefontoptions);
  $p->fit_textline("Phone:", 393, $ypos, $baseboldfontoptions);
  $p->fit_textline(${emerwkph}, 427, $ypos, $basefontoptions);

  main->renderTextline($p, "Address:", $marginleft, 14.8, $baseboldfontoptions);
  $p->fit_textline(${emeraddr}, 75, $ypos, $basefontoptions);

  main->renderTextline($p, "Relationship:", $marginleft, 14.8, $baseboldfontoptions);
  $p->fit_textline(${erelation}, 93, $ypos, $basefontoptions);
  $p->fit_textline("Special Instructions:", 213, $ypos, $baseboldfontoptions);
  $p->fit_textline($rClientEmergency->{'Comments'}, 305, $ypos, $basefontoptions);

  main->renderTextline($p, "Health Care Information / Resources", 235, 27, $baseboldfontoptions_u, $HeaderInfo);

  my $PhysNPI = $rClientEmergencyCare->{'PhysNPI'};
  my $physname = '';
  my $physaddr = '';
  my $physwkph = '';
  if ( $PhysNPI eq '' )
  {
    $physname = qq|No Primary Care Physician reported by Client.|;
    $physaddr = qq|A list of Primary Care Physician was given to Client.|;
  }
  else
  {
    my $rPhysician = DBA->selxref($form,'xNPI','NPI',$PhysNPI);
    $physname = qq|$rPhysician->{'ProvPrefix'} $rPhysician->{'ProvFirstName'} $rPhysician->{'ProvLastName'}|;
    $physaddr = $rPhysician->{'Addr1'};
    $physaddr .= $rPhysician->{'Addr2'} if ( $rPhysician->{'Addr2'} ne '' );
    $physaddr .= qq|, $rPhysician->{'City'}| if ( $rPhysician->{'City'} ne '' );
    $physaddr .= qq|, $rPhysician->{'ST'}| if ( $rPhysician->{'ST'} ne '' );
    $physaddr .= qq| $rPhysician->{'Zip'}| if ( $rPhysician->{'Zip'} ne '' );
    $physwkph = $rPhysician->{'WkPh'};
  }

  main->renderTextline($p, "Primary Care Physician:", $marginleft, 18, $baseboldfontoptions);
  $p->fit_textline(${physname}, 140, $ypos, $basefontoptions);
  $p->fit_textline("Phone:", 393, $ypos, $baseboldfontoptions);
  $p->fit_textline(${physwkph}, 427, $ypos, $basefontoptions);

  main->renderTextline($p, "Address:", $marginleft, 14.8, $baseboldfontoptions);
  $p->fit_textline(${physaddr}, 75, $ypos, $basefontoptions);

  my $HospNPI = $rClientEmergencyCare->{'DesigHospNPI'};
  my $hospname = '';
  my $hospaddr = '';
  my $hospwkph = '';
  if ( $HospNPI eq '' )
  {
    $hospname = qq|No Designated Hospital reported by Client.|;
    $hospaddr = qq|A list of Hospitals was given to Client.|;
  }
  else
  {
    my $rHospital = DBA->selxref($form,'xNPI','NPI',$HospNPI);
    $hospname = $rHospital->{'ProvOrgName'};
    $hospaddr = $rHospital->{'Addr1'};
    $hospaddr .= $rHospital->{'Addr2'} if ( $rHospital->{'Addr2'} ne '' );
    $hospaddr .= qq|, $rHospital->{'City'}| if ( $rHospital->{'City'} ne '' );
    $hospaddr .= qq|, $rHospital->{'ST'}| if ( $rHospital->{'ST'} ne '' );
    $hospaddr .= qq| $rHospital->{'Zip'}| if ( $rHospital->{'Zip'} ne '' );
    $hospwkph = $rHospital->{'WkPh'};
  }

  main->renderTextline($p, "Hospital:", $marginleft, 27, $baseboldfontoptions);
  $p->fit_textline(${hospname}, 75, $ypos, $basefontoptions);
  $p->fit_textline("Phone:", 393, $ypos, $baseboldfontoptions);
  $p->fit_textline(${hospwkph}, 427, $ypos, $basefontoptions);

  main->renderTextline($p, "Address:", $marginleft, 14.8, $baseboldfontoptions);
  $p->fit_textline(${hospaddr}, 75, $ypos, $basefontoptions);

  main->renderTextline($p, "Insurance", 287, 27, $baseboldfontoptions_u, $HeaderInfo);

  my @Ins = ();
  for (my $Priority = 1; $Priority <= 3; $Priority++)
  {
#warn qq|ClientID=${ClientID}, Priority=${Priority}\n|;
    $sInsurance->execute($ClientID,$Priority);
    if ( my $rInsurance = $sInsurance->fetchrow_hashref )
    {
#foreach my $f ( sort keys %{$rInsurance} ) { warn ": rInsurance-$f=$rInsurance->{$f}\n"; }
      $Ins[$Priority][1] = DBA->getxref($form,'xInsurance',$rInsurance->{'InsID'},'Name');
      $Ins[$Priority][2] = $rInsurance->{'InsIDNum'};
      $Ins[$Priority][3] = $rInsurance->{'ClientRel'} eq '' || $rInsurance->{'ClientRel'} eq 'I'
                          ? qq|self| : qq|$rInsurance->{'FName'} $rInsurance->{'MName'} $rInsurance->{'LName'}|;
    }
#warn qq|Ins=$Ins[$Priority][1]\n|;
  }

  main->renderTextline($p, "Primary:", $marginleft, 18, $baseboldfontoptions);
  $p->fit_textline($Ins[1][1], 74, $ypos, $basefontoptions);
  $p->fit_textline("Secondary:", 213, $ypos, $baseboldfontoptions);
  $p->fit_textline($Ins[2][1], 266, $ypos, $basefontoptions);
  $p->fit_textline("Tertiary:", 393, $ypos, $baseboldfontoptions);
  $p->fit_textline($Ins[3][1], 433, $ypos, $basefontoptions);

  main->renderTextline($p, "Policy Number:", $marginleft, 14.8, $baseboldfontoptions);
  $p->fit_textline($Ins[1][2], 102, $ypos, $basefontoptions);
  $p->fit_textline("Policy Number:", 213, $ypos, $baseboldfontoptions);
  $p->fit_textline($Ins[2][2], 282, $ypos, $basefontoptions);
  $p->fit_textline("Policy Number:", 393, $ypos, $baseboldfontoptions);
  $p->fit_textline($Ins[3][2], 463, $ypos, $basefontoptions);

  main->renderTextline($p, "Policy Holder:", $marginleft, 14.8, $baseboldfontoptions);
  $p->fit_textline($Ins[1][3], 96, $ypos, $basefontoptions);
  $p->fit_textline("Policy Holder:", 213, $ypos, $baseboldfontoptions);
  $p->fit_textline($Ins[2][3], 277, $ypos, $basefontoptions);
  $p->fit_textline("Policy Holder:", 393, $ypos, $baseboldfontoptions);
  $p->fit_textline($Ins[3][3], 457, $ypos, $basefontoptions);

  main->createFooter($p);
}

sub createHeader {
  my ($self, $p, $HeaderInfo) = @_;

  my $Company = $HeaderInfo->{'companyname'};
  my $Address = "$HeaderInfo->{'companyaddr'}\n$HeaderInfo->{'companycsz'}";
  my $OffceFax = $HeaderInfo->{'companyphone'};
  my $title = "Client Information";

  my $tf;

  $p->begin_page_ext($pagewidth, $pageheight, "topdown");
  $ypos = $margintop;

  $ypos += $fontsizelarge;
  $p->fit_textline($Company, $pagewidth / 2, $ypos, $baseboldlargefontoptions . " position={center bottom}");

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
  
  my ($logodirectory, $logofilename) = $HeaderInfo->{'LOGO'} =~ m/(.*\/)(.*)$/;
  if ( $logofilename eq '' ) { $logofilename = 'logo.png'; }
  elsif ( not -e "/usr/local/PDFlib/${logofilename}" ) { $logofilename = 'logo.png'; }
  my $logoimage = $p->load_image("auto", $logofilename, "");
  $p->fit_image($logoimage, $marginleft, $ypos, "boxsize={" . $w_logo . " " .  $h_logo . "} fitmethod=meet");
  $p->close_image($logoimage);
##

  $ypos += 2 * $fontsizexxlarge;
  $p->fit_textline($title, $pagewidth / 2, $ypos, $baseboldxlargefontoptions . " position={center bottom}");

  $ypos += $fontsizexxlarge;
}

sub createEmptyPage {
  my ($self, $p) = @_;

  $p->begin_page_ext($pagewidth, $pageheight, "topdown");
  $p->fit_textline("NOT FOUND", $marginleft, 50, $basefontoptions);
  $p->end_page_ext("");
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

  ++$pagecount;
  my $xpos = $pagecount < 10 ? 274 : 268.4;
  $p->fit_textline("Page " . $pagecount, $xpos, $marginbottom + 14, $baseboldmidfontoptions);
  $p->suspend_page("");
}

sub createPageCount {
  my ($self, $p) = @_;

  for(my $i = 1; $i < $pagecount+1; $i++) {
    # Revisit page $i
    $p->resume_page("pagenumber $i");

    # Add the total number of pages
    $p->fit_textline(" of " . $pagecount, 306, $marginbottom + 14, $baseboldmidfontoptions);
    $p->end_page_ext("");
  }
}
############################################################################

sub renderTextflow {
  my ($self, $p, $tf, $xpos, $width, $HeaderInfo) = @_;
  my $result;
  my $h_tf;

  do {
    $result = $p->fit_textflow($tf, $xpos, $y_footer, $xpos + $width, $ypos, "");
    if ($result eq "_boxfull" || $result eq "_boxempty") {
      main->createFooter($p);
      main->createHeader($p, $HeaderInfo);
    }
  } while ($result ne "_stop");
  $h_tf = $p->info_textflow($tf, "textheight");

  return $h_tf;
}

sub renderTextline {
  my ($self, $p, $text, $xpos, $h_tl, $optlist, $HeaderInfo, $TitleInfo, $bg, $h_bg, $margin) = @_;

  if ($ypos + $h_tl > $y_footer) {
    main->createFooter($p);
    main->createHeader($p, $HeaderInfo);

    if ($TitleInfo) {
      $ypos += $TitleInfo->{"h_title"};
      
      if ($bg) {
        main->renderTextlineBackground($p, $h_bg, $margin);
      }

      $p->fit_textline($TitleInfo->{"title"}, $xpos, $ypos, $TitleInfo->{"optlist"});
    }
  }
  $ypos += $h_tl;

  if ($bg) {
    main->renderTextlineBackground($p, $h_bg, $margin);
  }

  $p->fit_textline($text, $xpos, $ypos, $optlist);
}

sub renderTextlineBackground {
  my ($self, $p, $h_bg, $margin) = @_;

  unless($h_bg) {
    $h_bg = 18;
  }

  unless($margin) {
    $margin = 5;
  }

  $p->setcolor("fill", "cmyk", 0.09, 0.06, 0.06, 0.0);
  $p->set_graphics_option("linejoin=0");
  $p->rect($marginleft, $ypos + $margin, $contentwidth, $h_bg);
  $p->fill();
  $p->setcolor("fill", "cmyk", 0.70, 0.68, 0.64, 0.74);
}
