#!/usr/bin/perl
############################################################################
use lib '/var/www/okmis/src/lib';
use DBI;
use myForm;
use myDBI;
use DBA;
use MgrTree;
use myConfig;
use DBUtil;
use Time::Local;
my $DT=localtime();

use PDFlib::PDFlib;
use strict;
############################################################################

my $form = myForm->new();
my $IDs = $form->{'IDs'};
my $dbh = myDBI->dbconnect($form->{'DBNAME'});


my $sProviderCreds = $dbh->prepare("select * from ProviderCreds where ID=?");

my $sProvider = $dbh->prepare("select * from Provider where ProvID=?");

my %YesNoArr = ("1", "Yes", "0", "No");

my $pagewidth = 612;
my $pageheight = 692;

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
my $basecheckfontoptions = "fontname={DejaVuSans} encoding=unicode fontsize=10 charref";

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
  $p->set_info("Title", "Provider Credentials");

  main->printProviderCreds($p);

  $p->end_document("");

};



if ($@) {
  die("$0: PDFlib Exception occurred:\n$@");
}

$sProviderCreds->finish();
$sProvider->finish();

myDBI->cleanup();

if ( $form->{'file'} eq '' )                # create and print pdf.
{ print qq|Location: ${filename}\n\n|; }

exit;



############################################################################
sub printProviderCreds {
  my ($self, $p) = @_;


  foreach my $ID (split(' ', $IDs)) {
    $sProviderCreds->execute($ID);
    while(my $rProviderCreds = $sProviderCreds->fetchrow_hashref) {
      $sProvider->execute($rProviderCreds->{'ProvID'});
      my $rProvider = $sProvider->fetchrow_hashref;
      main->createPages($p, $rProviderCreds, $rProvider); 
    }
  }

  if ($pagecount) {
    main->createPageCount($p);
  } else {
    main->createEmptyPage($p);
  }

}


sub createPages {
  my ($self, $p, $rProviderCreds, $rProvider) = @_;
  
  my $optlist;
  my $tf;
  my $h_tf;
  my $row;
  my $col;
  my $tbl;
  my $h_tbl;

  main->createHeader($p, $rProvider);


  # PERSONAL INFORMATION
  # my $ = $rProviderCreds->{''};

  # Get PERSONAL INFORMATION
  my $Suffix = $rProviderCreds->{'Suff'}; 
  my $FName = $rProviderCreds->{'FName'};
  my $MName = $rProviderCreds->{'MName'};
  my $LName = $rProviderCreds->{'LName'};
  my $fullName = qq|$Suffix $FName $MName $LName|;

  my $ProfDegree = $rProviderCreds->{'Degree'};
  my $Gender = $rProviderCreds->{'Gend'};


  my $Alias1 = $rProviderCreds->{'Alias1'};
  my $Alias1DateFrom = $rProviderCreds->{'Alias1DateFrom'};
  my $Alias1DateEnd = $rProviderCreds->{'Alias1DateEnd'};

  my $Alias2 = $rProviderCreds->{'Alias2'};
  my $Alias2DateFrom = $rProviderCreds->{'Alias2DateFrom'};
  my $Alias2DateEnd = $rProviderCreds->{'Alias2DateEnd'};


  my $SSN = $rProviderCreds->{'SSN'};
  my $NPI = $rProviderCreds->{'NPI'};
  my $DOB = $rProviderCreds->{'DOB'};
  my $PlaceOfBirth = $rProviderCreds->{'PlaceOfBirth'};
  my $Citizenship = $rProviderCreds->{'Citizenship'};
  my $VisaType = $rProviderCreds->{'VisaType'};
  my $VisaNum = $rProviderCreds->{'VisaNum'};
  my $VisaExpire = $rProviderCreds->{'VisaExpire'};
  
  my $MedicarePIN = $rProviderCreds->{'MedicarePIN'};
  my $MedicaidPIN = $rProviderCreds->{'MedicaidPIN'};
  my $DesigProvID = $rProviderCreds->{'DesigProvID'};

  $sProvider->execute($rProviderCreds->{'DesigProvID'});
  my $rDesigProv = $sProvider->fetchrow_hashref;

  # Print PERSONAL INFORMATION

  $p->fit_textline("PERSONAL INFORMATION:", 37, $ypos, $baseboldlargefontoptions_u);
  $ypos += 25;


  $p->fit_textline("Name:", 37, $ypos, $baseboldfontoptions);
  $p->fit_textline($fullName, 70, $ypos, $basefontoptions);


  $p->fit_textline("Degree:", 200, $ypos, $baseboldfontoptions);
  $p->fit_textline($ProfDegree, 250, $ypos, $basefontoptions);


  $p->fit_textline("Gender:", 350, $ypos, $baseboldfontoptions);
  $p->fit_textline($Gender, 400, $ypos, $basefontoptions);

  $ypos += 15;

  $p->fit_textline("Other Name By Which You Have Been Known:", 37, $ypos, $baseboldfontoptions);
  $ypos += 15;
  $p->fit_textline("Name 2:", 37, $ypos, $baseboldfontoptions);
  $p->fit_textline($Alias1, 75, $ypos, $basefontoptions);

  $p->fit_textline("From:", 200, $ypos, $baseboldfontoptions);
  $p->fit_textline($Alias1DateFrom, 250, $ypos, $basefontoptions);

  $p->fit_textline("To:", 350, $ypos, $baseboldfontoptions);
  $p->fit_textline($Alias1DateEnd, 400, $ypos, $basefontoptions);

  $ypos += 15;

  $p->fit_textline("Other Name By Which You Have Been Known:", 37, $ypos, $baseboldfontoptions);
  $ypos += 15;
  $p->fit_textline("Name 3:", 37, $ypos, $baseboldfontoptions);
  $p->fit_textline($Alias2, 75, $ypos, $basefontoptions);

  $p->fit_textline("From:", 200, $ypos, $baseboldfontoptions);
  $p->fit_textline($Alias2DateFrom, 250, $ypos, $basefontoptions);

  $p->fit_textline("To:", 350, $ypos, $baseboldfontoptions);
  $p->fit_textline($Alias2DateEnd, 400, $ypos, $basefontoptions);



  $ypos += 25;

  $p->fit_textline("SSN:", 37, $ypos, $baseboldfontoptions);
  $p->fit_textline($SSN, 60, $ypos, $basefontoptions);

  $p->fit_textline("NPI:", 140, $ypos, $baseboldfontoptions);
  $p->fit_textline($NPI, 160, $ypos, $basefontoptions);

  $p->fit_textline("DOB:", 230, $ypos, $baseboldfontoptions);
  $p->fit_textline($DOB, 260, $ypos, $basefontoptions);

  $p->fit_textline("Place Of Birth:", 320, $ypos, $baseboldfontoptions);
  $p->fit_textline($PlaceOfBirth, 390, $ypos, $basefontoptions);

  $p->fit_textline("Citizenship:", 430, $ypos, $baseboldfontoptions);
  $p->fit_textline($Citizenship, 490, $ypos, $basefontoptions);

  $ypos += 25;


  $p->fit_textline("Visa Type:", 37, $ypos, $baseboldfontoptions);
  $p->fit_textline($VisaType, 90, $ypos, $basefontoptions);


  $p->fit_textline("Visa Number:", 200, $ypos, $baseboldfontoptions);
  $p->fit_textline($VisaNum, 270, $ypos, $basefontoptions);


  $p->fit_textline("Visa Expire Date:", 350, $ypos, $baseboldfontoptions);
  $p->fit_textline($VisaExpire, 430, $ypos, $basefontoptions);

  $ypos += 25;


  $p->fit_textline("Your Medicare PIN:", 37, $ypos, $baseboldfontoptions);
  $p->fit_textline($MedicarePIN, 120, $ypos, $basefontoptions);


  $p->fit_textline("Your Medicaid PIN:", 200, $ypos, $baseboldfontoptions);
  $p->fit_textline($MedicaidPIN, 290, $ypos, $basefontoptions);


  $p->fit_textline("Designated Provider:", 350, $ypos, $baseboldfontoptions);
  $p->fit_textline("$rDesigProv->{FName} $rDesigProv->{MName} $rDesigProv->{LName}", 450, $ypos, $basefontoptions);




  # DIRECTORY INFORMATION
  $ypos += 30;

  $p->fit_textline("Mailing Address For All ProviderCreds Correspondence:", 37, $ypos, $baseboldlargefontoptions_u);
  $ypos += 20;


  my $DirectoryAddr1 = $rProviderCreds->{"DirectoryAddr1"};
  $p->fit_textline("Street Address:",  37, $ypos, $baseboldfontoptions);
  $p->fit_textline($DirectoryAddr1,   120, $ypos, $basefontoptions);


  my $DirectoryAddr2 = $rProviderCreds->{"DirectoryAddr2"};
  $p->fit_textline("Suite Number:",  280, $ypos, $baseboldfontoptions);
  $p->fit_textline($DirectoryAddr2,   350, $ypos, $basefontoptions);


  $ypos += 15;

  my $DirectoryCity = $rProviderCreds->{"DirectoryCity:"};
  $p->fit_textline("City:",  37, $ypos, $baseboldfontoptions);
  $p->fit_textline($DirectoryCity,   70, $ypos, $basefontoptions);

  my $DirectoryST = $rProviderCreds->{"DirectoryST"};
  $p->fit_textline("State:",  150, $ypos, $baseboldfontoptions);
  $p->fit_textline($DirectoryST,   180, $ypos, $basefontoptions);


  my $DirectoryZIP = $rProviderCreds->{"DirectoryZIP"};
  $p->fit_textline("ZIP:",  220, $ypos, $baseboldfontoptions);
  $p->fit_textline($DirectoryZIP,   240, $ypos, $basefontoptions); 


  my $DirectoryPh = $rProviderCreds->{"DirectoryPh"};
  $p->fit_textline("Phone:",  270, $ypos, $baseboldfontoptions);
  $p->fit_textline($DirectoryPh,   310, $ypos, $basefontoptions);


  my $DirectoryFax = $rProviderCreds->{"DirectoryFax"};
  $p->fit_textline("Fax:",  400, $ypos, $baseboldfontoptions);
  $p->fit_textline($DirectoryFax,   430, $ypos, $basefontoptions);

  $ypos += 15;

  my $DirectoryPgr = $rProviderCreds->{"DirectoryPgr"};
  $p->fit_textline("Emergency or Pager:", 37, $ypos, $baseboldfontoptions);
  $p->fit_textline($DirectoryPgr, 130, $ypos, $basefontoptions);

  my $DirectoryAnsSvc = $rProviderCreds->{"DirectoryAnsSvc"};
  $p->fit_textline("Answering Service Number:", 200, $ypos, $baseboldfontoptions);
  $p->fit_textline($DirectoryAnsSvc, 330, $ypos, $basefontoptions);


  my $DirectoryEmail = $rProviderCreds->{"DirectoryEmail"};
  $p->fit_textline("Email:",  400, $ypos, $baseboldfontoptions);
  $p->fit_textline($DirectoryEmail,   440, $ypos, $basefontoptions);


  # Office Mailing Address
  $ypos += 30;

  $p->fit_textline("Office Mailing Address:", 37, $ypos, $baseboldlargefontoptions_u);
  $ypos += 20;

  my $Off2Addr1 = $rProviderCreds->{"Off2Addr1"};
  $p->fit_textline("Street Address:", 37, $ypos, $baseboldfontoptions);
  $p->fit_textline($Off2Addr1, 120, $ypos, $basefontoptions);

  my $Off2Addr2 = $rProviderCreds->{"Off2Addr2"};
  $p->fit_textline("Suite Number:", 280, $ypos, $baseboldfontoptions);
  $p->fit_textline($Off2Addr2, 350, $ypos, $basefontoptions);

  $ypos += 15;

  my $Off2City = $rProviderCreds->{"Off2City:"};
  $p->fit_textline("City:",  37, $ypos, $baseboldfontoptions);
  $p->fit_textline($Off2City,   70, $ypos, $basefontoptions);

  my $Off2ST = $rProviderCreds->{"Off2ST"};
  $p->fit_textline("State:",  150, $ypos, $baseboldfontoptions);
  $p->fit_textline($Off2ST,   180, $ypos, $basefontoptions);


  my $Off2ZIP = $rProviderCreds->{"Off2ZIP"};
  $p->fit_textline("ZIP:",  220, $ypos, $baseboldfontoptions);
  $p->fit_textline($Off2ZIP,   240, $ypos, $basefontoptions); 


  my $Off2Ph = $rProviderCreds->{"Off2Ph"};
  $p->fit_textline("Phone:",  270, $ypos, $baseboldfontoptions);
  $p->fit_textline($Off2Ph,   310, $ypos, $basefontoptions);


  my $Off2Fax = $rProviderCreds->{"Off2Fax"};
  $p->fit_textline("Fax:",  400, $ypos, $baseboldfontoptions);
  $p->fit_textline($Off2Fax,   430, $ypos, $basefontoptions);

  $ypos += 15;

  my $Off2Pgr = $rProviderCreds->{"Off2Pgr"};
  $p->fit_textline("Emergency or Pager:", 37, $ypos, $baseboldfontoptions);
  $p->fit_textline($Off2Pgr, 130, $ypos, $basefontoptions);

  my $Off2AnsSvc = $rProviderCreds->{"Off2AnsSvc"};
  $p->fit_textline("Answering Service Number:", 200, $ypos, $baseboldfontoptions);
  $p->fit_textline($Off2AnsSvc, 330, $ypos, $basefontoptions);


  my $Off2Email = $rProviderCreds->{"Off2Email"};
  $p->fit_textline("Email:",  400, $ypos, $baseboldfontoptions);
  $p->fit_textline($Off2Email,   440, $ypos, $basefontoptions);

  main->createFooter($p);
  # Start Page 2 

  $p->begin_page_ext($pagewidth, $pageheight, "topdown");


  # Office Billing Address
  $ypos = $margintop;

  $p->fit_textline("Office Billing Address (If Different From Claims Payment Address):", 37, $ypos, $baseboldlargefontoptions_u);
  $ypos += 20;

  my $Off3Addr1 = $rProviderCreds->{"Off3Addr1"};
  $p->fit_textline("Street Address:", 37, $ypos, $baseboldfontoptions);
  $p->fit_textline($Off3Addr1, 120, $ypos, $basefontoptions);

  my $Off3Addr2 = $rProviderCreds->{"Off3Addr2"};
  $p->fit_textline("Suite Number:", 280, $ypos, $baseboldfontoptions);
  $p->fit_textline($Off3Addr2, 350, $ypos, $basefontoptions);

  $ypos += 15;

  my $Off3City = $rProviderCreds->{"Off3City:"};
  $p->fit_textline("City:",  37, $ypos, $baseboldfontoptions);
  $p->fit_textline($Off3City,   70, $ypos, $basefontoptions);

  my $Off3ST = $rProviderCreds->{"Off3ST"};
  $p->fit_textline("State:",  150, $ypos, $baseboldfontoptions);
  $p->fit_textline($Off3ST,   180, $ypos, $basefontoptions);


  my $Off3ZIP = $rProviderCreds->{"Off3ZIP"};
  $p->fit_textline("ZIP:",  220, $ypos, $baseboldfontoptions);
  $p->fit_textline($Off3ZIP,   240, $ypos, $basefontoptions); 


  my $Off3Ph = $rProviderCreds->{"Off3Ph"};
  $p->fit_textline("Phone:",  270, $ypos, $baseboldfontoptions);
  $p->fit_textline($Off3Ph,   310, $ypos, $basefontoptions);


  my $Off3Fax = $rProviderCreds->{"Off3Fax"};
  $p->fit_textline("Fax:",  400, $ypos, $baseboldfontoptions);
  $p->fit_textline($Off3Fax,   430, $ypos, $basefontoptions);

  $ypos += 15;

  my $Off3Pgr = $rProviderCreds->{"Off3Pgr"};
  $p->fit_textline("Emergency or Pager:", 37, $ypos, $baseboldfontoptions);
  $p->fit_textline($Off3Pgr, 130, $ypos, $basefontoptions);

  my $Off3AnsSvc = $rProviderCreds->{"Off3AnsSvc"};
  $p->fit_textline("Answering Service Number:", 200, $ypos, $baseboldfontoptions);
  $p->fit_textline($Off3AnsSvc, 330, $ypos, $basefontoptions);


  my $Off3Email = $rProviderCreds->{"Off3Email"};
  $p->fit_textline("Email:",  400, $ypos, $baseboldfontoptions);
  $p->fit_textline($Off3Email,   440, $ypos, $basefontoptions);


  # Claims Payment Address
  $ypos += 30;

  $p->fit_textline("Claims Payment Address (If Different From Office Billing Address):", 37, $ypos, $baseboldlargefontoptions_u);
  $ypos += 20;

  my $Off4Addr1 = $rProviderCreds->{"Off4Addr1"};
  $p->fit_textline("Street Address:", 37, $ypos, $baseboldfontoptions);
  $p->fit_textline($Off4Addr1, 120, $ypos, $basefontoptions);

  my $Off4Addr2 = $rProviderCreds->{"Off4Addr2"};
  $p->fit_textline("Suite Number:", 280, $ypos, $baseboldfontoptions);
  $p->fit_textline($Off4Addr2, 350, $ypos, $basefontoptions);

  $ypos += 15;

  my $Off4City = $rProviderCreds->{"Off4City:"};
  $p->fit_textline("City:",  37, $ypos, $baseboldfontoptions);
  $p->fit_textline($Off4City,   70, $ypos, $basefontoptions);

  my $Off4ST = $rProviderCreds->{"Off4ST"};
  $p->fit_textline("State:",  150, $ypos, $baseboldfontoptions);
  $p->fit_textline($Off4ST,   180, $ypos, $basefontoptions);


  my $Off4ZIP = $rProviderCreds->{"Off4ZIP"};
  $p->fit_textline("ZIP:",  220, $ypos, $baseboldfontoptions);
  $p->fit_textline($Off4ZIP,   240, $ypos, $basefontoptions); 


  my $Off4Ph = $rProviderCreds->{"Off4Ph"};
  $p->fit_textline("Phone:",  270, $ypos, $baseboldfontoptions);
  $p->fit_textline($Off4Ph,   310, $ypos, $basefontoptions);


  my $Off4Fax = $rProviderCreds->{"Off4Fax"};
  $p->fit_textline("Fax:",  400, $ypos, $baseboldfontoptions);
  $p->fit_textline($Off4Fax,   430, $ypos, $basefontoptions);

  $ypos += 15;

  my $Off4Pgr = $rProviderCreds->{"Off4Pgr"};
  $p->fit_textline("Emergency or Pager:", 37, $ypos, $baseboldfontoptions);
  $p->fit_textline($Off4Pgr, 130, $ypos, $basefontoptions);

  my $Off4AnsSvc = $rProviderCreds->{"Off4AnsSvc"};
  $p->fit_textline("Answering Service Number:", 200, $ypos, $baseboldfontoptions);
  $p->fit_textline($Off4AnsSvc, 330, $ypos, $basefontoptions);


  my $Off4Email = $rProviderCreds->{"Off4Email"};
  $p->fit_textline("Email:",  400, $ypos, $baseboldfontoptions);
  $p->fit_textline($Off4Email,   440, $ypos, $basefontoptions);


  $ypos += 25;

  my $Off1Mgr = $rProviderCreds->{"Off1Mgr"};
  $p->fit_textline("Make Checks Payble to:", 37, $ypos, $baseboldfontoptions);
  $p->fit_textline($Off1Mgr, 140, $ypos, $basefontoptions);


  # SECTION 3: CURRENT PROFESSIONAL PRACTICE
  $ypos += 30;

  $p->fit_textline("CURRENT PROFESSIONAL PRACTICE:", 37, $ypos, $baseboldlargefontoptions_u);
  $ypos += 20;

  my $SpecialtyPrimary = $rProviderCreds->{"SpecialtyPrimary"};
  $p->fit_textline("Primary Specialty:", 37, $ypos, $baseboldfontoptions);
  $p->fit_textline($SpecialtyPrimary, 140, $ypos, $basefontoptions);


  my $SubspecialtyPrimary = $rProviderCreds->{"SubspecialtyPrimary"};
  $p->fit_textline("Sub Specialty:", 200, $ypos, $baseboldfontoptions);
  $p->fit_textline($SubspecialtyPrimary, 270, $ypos, $basefontoptions);


  my $SpecailtyPrimaryTime = $rProviderCreds->{"SpecailtyPrimaryTime"};
  $p->fit_textline("% Of Time:", 350, $ypos, $baseboldfontoptions);
  $p->fit_textline($SpecailtyPrimaryTime, 400, $ypos, $basefontoptions);


  $ypos += 15;

  my $SpecialtySecondary = $rProviderCreds->{"SpecialtySecondary"};
  $p->fit_textline("Secondary Specialty:", 37, $ypos, $baseboldfontoptions);
  $p->fit_textline($SpecialtySecondary, 140, $ypos, $basefontoptions);


  my $SubspecialtySecondary = $rProviderCreds->{"SubspecialtySecondary"};
  $p->fit_textline("Sub Specialty:", 200, $ypos, $baseboldfontoptions);
  $p->fit_textline($SubspecialtySecondary, 270, $ypos, $basefontoptions);


  my $SpecialtySecondaryTime = $rProviderCreds->{"SpecialtySecondaryTime"};
  $p->fit_textline("% Of Time:", 350, $ypos, $baseboldfontoptions);
  $p->fit_textline($SpecialtySecondaryTime, 400, $ypos, $basefontoptions);



  $ypos += 15;
  my $ProviderListTypeSpecify = $rProviderCreds->{"ProviderListTypeSpecify"};
  my $ProviderListType = $rProviderCreds->{"ProviderListType"};

  my %ProviderListTypeArr = (
      "P", "Primary Care Provider",
      "S", "Specialist",
      "H", "Hospitalist",
      "C", "On-Call",
      "O", $ProviderListTypeSpecify,
    );

  $p->fit_textline("You wish to be listed as:", 37, $ypos, $baseboldfontoptions);
  $p->fit_textline($ProviderListTypeArr{$ProviderListType}, 150, $ypos, $basefontoptions);


  $ypos += 15;
  $p->fit_textline("If you are a primary care physician, list special diagnostic or treatment procedures performed in your office(s):", 37, $ypos, $baseboldfontoptions);
  $ypos += 15;

  if($ProviderListType eq "P") {
    my $SpecialProcedureSpecify = $rProviderCreds->{"SpecialProcedureSpecify"};
    # $p->fit_textline($SpecialProcedureSpecify, 37, $ypos, $basefontoptions);

    my $h_address = 10 * $fontsizexxlarge;
    $ypos += $h_address;
    my $w_address = $pagewidth - 10;
    my $x_address = $pagewidth / 2 - $w_address / 2;
    $tf = $p->create_textflow($SpecialProcedureSpecify, $baselargefontoptions . " leading=110% alignment=justify lastalignment=justify");
    $p->fit_textflow($tf, 37, $ypos, $x_address+$w_address, $ypos - $h_address, "verticalalign=center");
  }


  main->createFooter($p);


  # Start Page 3
  $p->begin_page_ext($pagewidth, $pageheight, "topdown");
  $ypos = $margintop;


  my $NewPt = $rProviderCreds->{"NewPt"};
  $p->fit_textline("Are you accepting new patients:", 37, $ypos, $baseboldfontoptions);
  $p->fit_textline($YesNoArr{$NewPt}, 180, $ypos, $basefontoptions);

  my $FuturePt = $rProviderCreds->{"FuturePt"};
  $p->fit_textline("Are you willing, in the future to accept new patients:", 220, $ypos, $baseboldfontoptions);
  $p->fit_textline($YesNoArr{$FuturePt}, 450, $ypos, $basefontoptions);
  $ypos += 15;


  my $AdmitPt = $rProviderCreds->{"AdmitPt"};
  $p->fit_textline("Do you admit your own patients to hospitals:", 37, $ypos, $baseboldfontoptions);
  $p->fit_textline($YesNoArr{$AdmitPt}, 250, $ypos, $basefontoptions);
  $ypos += 15;

  my $CurrentPt = $rProviderCreds->{"CurrentPt"};
  $p->fit_textline("Are you willing to accept current patients if they convert to the healthcare plan to which you are applying?:", 37, $ypos, $baseboldfontoptions);
  $p->fit_textline($YesNoArr{$CurrentPt}, 500, $ypos, $basefontoptions);
  $ypos += 15;


  my $IPHPHAMember = $rProviderCreds->{"IPHPHAMember"};
  $p->fit_textline("Are you a member of an Independent Practice Association or a Physician Hospital Association:", 37, $ypos, $baseboldfontoptions);
  $p->fit_textline($YesNoArr{$IPHPHAMember}, 500, $ypos, $basefontoptions);
  $ypos += 10;
  $p->fit_textline("If yes, complete the following:", 37, $ypos, $baseboldfontoptions);


  $ypos += 15;

  my $IPHPHA1 = $rProviderCreds->{"IPHPHA1"};
  $p->fit_textline("Name:",  37, $ypos, $baseboldfontoptions);
  $p->fit_textline($IPHPHA1, 70, $ypos, $basefontoptions);

  my $IPHPHA1Addr1 = $rProviderCreds->{"IPHPHA1Addr1"};
  $p->fit_textline("Street Address:",  140, $ypos, $baseboldfontoptions);
  $p->fit_textline($IPHPHA1Addr1,   240, $ypos, $basefontoptions);

  my $IPHPHA1Addr2 = $rProviderCreds->{"IPHPHA1Addr2"};
  $p->fit_textline("Suite Number:",  350, $ypos, $baseboldfontoptions);
  $p->fit_textline($IPHPHA1Addr2,   420, $ypos, $basefontoptions);
  $ypos += 15;

  my $IPHPHA1City = $rProviderCreds->{"IPHPHA1City"};
  $p->fit_textline("City:",  37, $ypos, $baseboldfontoptions);
  $p->fit_textline($IPHPHA1City,   70, $ypos, $basefontoptions);

  my $IPHPHA1ST = $rProviderCreds->{"IPHPHA1ST"};
  $p->fit_textline("State:",  150, $ypos, $baseboldfontoptions);
  $p->fit_textline($IPHPHA1ST,   180, $ypos, $basefontoptions);


  my $IPHPHA1ZIP = $rProviderCreds->{"IPHPHA1ZIP"};
  $p->fit_textline("ZIP:",  220, $ypos, $baseboldfontoptions);
  $p->fit_textline($IPHPHA1ZIP,   240, $ypos, $basefontoptions); 


  my $IPHPHA1Ph = $rProviderCreds->{"IPHPHA1Ph"};
  $p->fit_textline("Phone:",  270, $ypos, $baseboldfontoptions);
  $p->fit_textline($IPHPHA1Ph,   310, $ypos, $basefontoptions);


  my $IPHPHA1Fax = $rProviderCreds->{"IPHPHA1Fax"};
  $p->fit_textline("Fax:",  400, $ypos, $baseboldfontoptions);
  $p->fit_textline($IPHPHA1Fax,   430, $ypos, $basefontoptions);
  $ypos += 15;

  my $IPHPHA1AnsSvc = $rProviderCreds->{"IPHPHA1AnsSvc"};
  $p->fit_textline("Answering Service Number:", 37, $ypos, $baseboldfontoptions);
  $p->fit_textline($IPHPHA1AnsSvc, 170, $ypos, $basefontoptions);



  $ypos += 25;

  my $IPHPHA2 = $rProviderCreds->{"IPHPHA2"};
  $p->fit_textline("Name:",  37, $ypos, $baseboldfontoptions);
  $p->fit_textline($IPHPHA2, 70, $ypos, $basefontoptions);

  my $IPHPHA2Addr1 = $rProviderCreds->{"IPHPHA2Addr1"};
  $p->fit_textline("Street Address:",  140, $ypos, $baseboldfontoptions);
  $p->fit_textline($IPHPHA2Addr1,   240, $ypos, $basefontoptions);

  my $IPHPHA2Addr2 = $rProviderCreds->{"IPHPHA2Addr2"};
  $p->fit_textline("Suite Number:",  350, $ypos, $baseboldfontoptions);
  $p->fit_textline($IPHPHA2Addr2,   420, $ypos, $basefontoptions);
  $ypos += 15;

  my $IPHPHA2City = $rProviderCreds->{"IPHPHA2City"};
  $p->fit_textline("City:",  37, $ypos, $baseboldfontoptions);
  $p->fit_textline($IPHPHA2City,   70, $ypos, $basefontoptions);

  my $IPHPHA2ST = $rProviderCreds->{"IPHPHA2ST"};
  $p->fit_textline("State:",  150, $ypos, $baseboldfontoptions);
  $p->fit_textline($IPHPHA2ST,   180, $ypos, $basefontoptions);


  my $IPHPHA2ZIP = $rProviderCreds->{"IPHPHA2ZIP"};
  $p->fit_textline("ZIP:",  220, $ypos, $baseboldfontoptions);
  $p->fit_textline($IPHPHA2ZIP,   240, $ypos, $basefontoptions); 


  my $IPHPHA2Ph = $rProviderCreds->{"IPHPHA2Ph"};
  $p->fit_textline("Phone:",  270, $ypos, $baseboldfontoptions);
  $p->fit_textline($IPHPHA2Ph,   310, $ypos, $basefontoptions);


  my $IPHPHA2Fax = $rProviderCreds->{"IPHPHA2Fax"};
  $p->fit_textline("Fax:",  400, $ypos, $baseboldfontoptions);
  $p->fit_textline($IPHPHA2Fax,   430, $ypos, $basefontoptions);
  $ypos += 15;

  my $IPHPHA2AnsSvc = $rProviderCreds->{"IPHPHA2AnsSvc"};
  $p->fit_textline("Answering Service Number:", 37, $ypos, $baseboldfontoptions);
  $p->fit_textline($IPHPHA2AnsSvc, 170, $ypos, $basefontoptions);


  my $Restrictions = $rProviderCreds->{"Restrictions"};
  $p->fit_textline("List any restrictions on your practice:", 220, $ypos, $baseboldfontoptions);
  $p->fit_textline($Restrictions, 400, $ypos, $basefontoptions);




  # SECTION 4: EDUCATION
  $ypos += 25;

  $p->fit_textline("SECTION 4: EDUCATION:", 37, $ypos, $baseboldlargefontoptions_u);
  $ypos += 15;

  $p->fit_textline("Medical/Dental/Graduate Professional Schools:", 37, $ypos, $baseboldfontoptions);
  $p->fit_textline("(List all, completed or not. Continue in Section 14 if needed)", 270, $ypos, $basefontoptions);
  $ypos += 15;

  my $School1 = $rProviderCreds->{"School1"};
  $p->fit_textline("(1) Institution:", 37, $ypos, $baseboldmidfontoptions);
  $p->fit_textline($School1, 110, $ypos, $basefontoptions);

  my $School1Degree = $rProviderCreds->{"School1Degree"};
  $p->fit_textline("Degree Awarded:", 400, $ypos, $baseboldmidfontoptions);
  $p->fit_textline($School1Degree, 490, $ypos, $basefontoptions);
  $ypos += 15;

  my $School1Addr = $rProviderCreds->{"School1Addr"};
  $p->fit_textline("Mailing Address:", 37, $ypos, $baseboldmidfontoptions);
  $p->fit_textline($School1Addr, 120, $ypos, $basefontoptions);
  $ypos += 15;

  my $School1City = $rProviderCreds->{"School1City"};
  $p->fit_textline("City:", 37, $ypos, $baseboldmidfontoptions);
  $p->fit_textline($School1City, 70, $ypos, $basefontoptions);


  my $School1ST = $rProviderCreds->{"School1ST"};
  $p->fit_textline("State:", 120, $ypos, $baseboldmidfontoptions);
  $p->fit_textline($School1ST, 160, $ypos, $basefontoptions);

  my $School1Zip = $rProviderCreds->{"School1Zip"};
  $p->fit_textline("Zip:", 200, $ypos, $baseboldmidfontoptions);
  $p->fit_textline($School1Zip, 230, $ypos, $basefontoptions);

  my $School1Ph = $rProviderCreds->{"School1Ph"};
  $p->fit_textline("Phone:", 270, $ypos, $baseboldmidfontoptions);
  $p->fit_textline($School1Ph, 310, $ypos, $basefontoptions);
  $ypos += 25;

  # School2
  my $School2 = $rProviderCreds->{"School2"};
  $p->fit_textline("(2) Institution:", 37, $ypos, $baseboldmidfontoptions);
  $p->fit_textline($School2, 110, $ypos, $basefontoptions);

  my $School2Degree = $rProviderCreds->{"School2Degree"};
  $p->fit_textline("Degree Awarded:", 400, $ypos, $baseboldmidfontoptions);
  $p->fit_textline($School2Degree, 490, $ypos, $basefontoptions);
  $ypos += 15;

  my $School2Addr = $rProviderCreds->{"School2Addr"};
  $p->fit_textline("Mailing Address:", 37, $ypos, $baseboldmidfontoptions);
  $p->fit_textline($School2Addr, 120, $ypos, $basefontoptions);
  $ypos += 15;

  my $School2City = $rProviderCreds->{"School2City"};
  $p->fit_textline("City:", 37, $ypos, $baseboldmidfontoptions);
  $p->fit_textline($School2City, 70, $ypos, $basefontoptions);


  my $School2ST = $rProviderCreds->{"School2ST"};
  $p->fit_textline("State:", 120, $ypos, $baseboldmidfontoptions);
  $p->fit_textline($School2ST, 160, $ypos, $basefontoptions);

  my $School2Zip = $rProviderCreds->{"School2Zip"};
  $p->fit_textline("Zip:", 200, $ypos, $baseboldmidfontoptions);
  $p->fit_textline($School2Zip, 230, $ypos, $basefontoptions);

  my $School2Ph = $rProviderCreds->{"School2Ph"};
  $p->fit_textline("Phone:", 270, $ypos, $baseboldmidfontoptions);
  $p->fit_textline($School2Ph, 310, $ypos, $basefontoptions);



  $ypos += 25;

  # School3
  my $School3 = $rProviderCreds->{"School3"};
  $p->fit_textline("(2) Institution:", 37, $ypos, $baseboldmidfontoptions);
  $p->fit_textline($School3, 110, $ypos, $basefontoptions);

  my $School3Degree = $rProviderCreds->{"School3Degree"};
  $p->fit_textline("Degree Awarded:", 400, $ypos, $baseboldmidfontoptions);
  $p->fit_textline($School3Degree, 490, $ypos, $basefontoptions);
  $ypos += 15;

  my $School3Addr = $rProviderCreds->{"School3Addr"};
  $p->fit_textline("Mailing Address:", 37, $ypos, $baseboldmidfontoptions);
  $p->fit_textline($School3Addr, 120, $ypos, $basefontoptions);
  $ypos += 15;

  my $School3City = $rProviderCreds->{"School3City"};
  $p->fit_textline("City:", 37, $ypos, $baseboldmidfontoptions);
  $p->fit_textline($School3City, 70, $ypos, $basefontoptions);


  my $School3ST = $rProviderCreds->{"School3ST"};
  $p->fit_textline("State:", 120, $ypos, $baseboldmidfontoptions);
  $p->fit_textline($School3ST, 160, $ypos, $basefontoptions);

  my $School3Zip = $rProviderCreds->{"School3Zip"};
  $p->fit_textline("Zip:", 200, $ypos, $baseboldmidfontoptions);
  $p->fit_textline($School3Zip, 230, $ypos, $basefontoptions);

  my $School3Ph = $rProviderCreds->{"School3Ph"};
  $p->fit_textline("Phone:", 270, $ypos, $baseboldmidfontoptions);
  $p->fit_textline($School3Ph, 310, $ypos, $basefontoptions);
  
  main->createFooter($p);


  # Start Page 4 

  $p->begin_page_ext($pagewidth, $pageheight, "topdown");
  # Office Billing Address
  $ypos = $margintop;

  $p->fit_textline("SECTION 5: TRAINING Internship/Residency/Fellowship/Preceptorship/Other", 37, $ypos, $baseboldlargefontoptions_u);
  $ypos += 25;
  $p->fit_textline("List all , completed or not. If you require additional space, continue in Section 14, or attach a separate sheet.", 37, $ypos, $baseboldmidfontoptions);
  $ypos += 15;

  # Training 1
  my $Train1Intern = $rProviderCreds->{"Train1Intern"};
  my $Train1Res = $rProviderCreds->{"Train1Res"};
  my $Train1Fellow = $rProviderCreds->{"Train1Fellow"};
  my $Train1Precept = $rProviderCreds->{"Train1Precept"};
  my $Train1Other = $rProviderCreds->{"Train1Other"};
  my $Train1Specify = $rProviderCreds->{"Train1Specify"};
  $p->fit_textline("(1) Type of Program:", 37, $ypos, $baseboldfontoptions);
  $ypos += 10;
  if($Train1Intern) {
    $p->fit_textline("&#x2713;", 37, $ypos, $basecheckfontoptions);
  } else {
    $p->fit_textline("&#x25a2;", 37, $ypos, $basecheckfontoptions);
  }
  $p->fit_textline("Internship", 50, $ypos, $basefontoptions);


  if($Train1Res) {
    $p->fit_textline("&#x2713;", 110, $ypos, $basecheckfontoptions);
  } else {
    $p->fit_textline("&#x25a2;", 110, $ypos, $basecheckfontoptions);
  }
  $p->fit_textline("Residency", 125, $ypos, $basefontoptions);

  if($Train1Fellow) {
    $p->fit_textline("&#x2713;", 180, $ypos, $basecheckfontoptions);
  } else {
    $p->fit_textline("&#x25a2;", 180, $ypos, $basecheckfontoptions);
  }

  $p->fit_textline("Fellowship", 195, $ypos, $basefontoptions);


  if($Train1Precept) {
    $p->fit_textline("&#x2713;", 260, $ypos, $basecheckfontoptions);
  } else {
    $p->fit_textline("&#x25a2;", 260, $ypos, $basecheckfontoptions);
  }

  $p->fit_textline("Preceptorship", 275, $ypos, $basefontoptions);


  if($Train1Other) {
    $p->fit_textline("&#x2713;", 350, $ypos, $basecheckfontoptions);
  } else {
    $p->fit_textline("&#x25a2;", 350, $ypos, $basecheckfontoptions);
  }

  $p->fit_textline("Other", 365, $ypos, $basefontoptions);
  if($Train1Other) {
    $p->fit_textline("$Train1Specify (Other)", 400, $ypos, $basefontoptions);
  }

  $ypos += 15;
  my $Train1Complete = $rProviderCreds->{"Train1Complete"};
  $p->fit_textline("Was program successfully completed: ", 37, $ypos, $baseboldfontoptions);
  $p->fit_textline($YesNoArr{$Train1Complete}, 210, $ypos, $basefontoptions);

  my $Train1Specialty = $rProviderCreds->{"Train1Specialty"};
  my $Train1SpecialtyName = DBA->getxrefWithDef($form,'xOccupationSnomed',$Train1Specialty,'Description');
  $p->fit_textline("Specialty: ", 300, $ypos, $baseboldfontoptions);
  $p->fit_textline($Train1SpecialtyName, 360, $ypos, $basefontoptions);
  $ypos += 15;


  my $Train1 = $rProviderCreds->{"Train1"};
  $p->fit_textline("Institution: ", 37, $ypos, $baseboldfontoptions);
  $p->fit_textline($Train1, 100, $ypos, $basefontoptions);

  my $Train1Director = $rProviderCreds->{"Train1Director"};
  $p->fit_textline("Program Director:", 300, $ypos, $baseboldfontoptions);
  $p->fit_textline($Train1Director, 400, $ypos, $basefontoptions);
  
  $ypos += 15;

  my $Train1Addr = $rProviderCreds->{"Train1Addr"};
  $p->fit_textline("Address: ", 37, $ypos, $baseboldfontoptions);
  $p->fit_textline($Train1Addr, 100, $ypos, $basefontoptions);

  my $Train1City = $rProviderCreds->{"Train1City"};
  $p->fit_textline("City: ", 300, $ypos, $baseboldfontoptions);
  $p->fit_textline($Train1City, 400, $ypos, $basefontoptions);

  $ypos += 15;


  my $Train1ST = $rProviderCreds->{"Train1ST"};
  $p->fit_textline("State: ", 37, $ypos, $baseboldfontoptions);
  $p->fit_textline($Train1ST, 70, $ypos, $basefontoptions);

  my $Train1Zip = $rProviderCreds->{"Train1Zip"};
  $p->fit_textline("Zip: ", 100, $ypos, $baseboldfontoptions);
  $p->fit_textline($Train1Zip, 130, $ypos, $basefontoptions);



  my $Train1Ph = $rProviderCreds->{"Train1Ph"};
  $p->fit_textline("Phone: ", 170, $ypos, $baseboldfontoptions);
  $p->fit_textline($Train1Ph, 210, $ypos, $basefontoptions);


  my $Train1Start = $rProviderCreds->{"Train1Start"};
  $p->fit_textline("From: ", 270, $ypos, $baseboldfontoptions);
  $p->fit_textline($Train1Start, 300, $ypos, $basefontoptions);



  my $Train1End = $rProviderCreds->{"Train1End"};
  $p->fit_textline("To: ", 380, $ypos, $baseboldfontoptions);
  $p->fit_textline($Train1End, 410, $ypos, $basefontoptions);


  $ypos += 25;



  # Training 1
  my $Train1Intern = $rProviderCreds->{"Train1Intern"};
  my $Train1Res = $rProviderCreds->{"Train1Res"};
  my $Train1Fellow = $rProviderCreds->{"Train1Fellow"};
  my $Train1Precept = $rProviderCreds->{"Train1Precept"};
  my $Train1Other = $rProviderCreds->{"Train1Other"};
  my $Train1Specify = $rProviderCreds->{"Train1Specify"};
  $p->fit_textline("(1) Type of Program:", 37, $ypos, $baseboldfontoptions);
  $ypos += 10;
  if($Train1Intern) {
    $p->fit_textline("&#x2713;", 37, $ypos, $basecheckfontoptions);
  } else {
    $p->fit_textline("&#x25a2;", 37, $ypos, $basecheckfontoptions);
  }
  $p->fit_textline("Internship", 50, $ypos, $basefontoptions);


  if($Train1Res) {
    $p->fit_textline("&#x2713;", 110, $ypos, $basecheckfontoptions);
  } else {
    $p->fit_textline("&#x25a2;", 110, $ypos, $basecheckfontoptions);
  }
  $p->fit_textline("Residency", 125, $ypos, $basefontoptions);

  if($Train1Fellow) {
    $p->fit_textline("&#x2713;", 180, $ypos, $basecheckfontoptions);
  } else {
    $p->fit_textline("&#x25a2;", 180, $ypos, $basecheckfontoptions);
  }

  $p->fit_textline("Fellowship", 195, $ypos, $basefontoptions);


  if($Train1Precept) {
    $p->fit_textline("&#x2713;", 260, $ypos, $basecheckfontoptions);
  } else {
    $p->fit_textline("&#x25a2;", 260, $ypos, $basecheckfontoptions);
  }

  $p->fit_textline("Preceptorship", 275, $ypos, $basefontoptions);


  if($Train1Other) {
    $p->fit_textline("&#x2713;", 350, $ypos, $basecheckfontoptions);
  } else {
    $p->fit_textline("&#x25a2;", 350, $ypos, $basecheckfontoptions);
  }

  $p->fit_textline("Other", 365, $ypos, $basefontoptions);
  if($Train1Other) {
    $p->fit_textline("$Train1Specify (Other)", 400, $ypos, $basefontoptions);
  }

  $ypos += 15;
  my $Train1Complete = $rProviderCreds->{"Train1Complete"};
  $p->fit_textline("Was program successfully completed: ", 37, $ypos, $baseboldfontoptions);
  $p->fit_textline($YesNoArr{$Train1Complete}, 210, $ypos, $basefontoptions);

  my $Train1Specialty = $rProviderCreds->{"Train1Specialty"};
  my $Train1SpecialtyName = DBA->getxrefWithDef($form,'xOccupationSnomed',$Train1Specialty,'Description');
  $p->fit_textline("Specialty: ", 300, $ypos, $baseboldfontoptions);
  $p->fit_textline($Train1SpecialtyName, 360, $ypos, $basefontoptions);
  $ypos += 15;


  my $Train1 = $rProviderCreds->{"Train1"};
  $p->fit_textline("Institution: ", 37, $ypos, $baseboldfontoptions);
  $p->fit_textline($Train1, 100, $ypos, $basefontoptions);

  my $Train1Director = $rProviderCreds->{"Train1Director"};
  $p->fit_textline("Program Director:", 300, $ypos, $baseboldfontoptions);
  $p->fit_textline($Train1Director, 400, $ypos, $basefontoptions);
  
  $ypos += 15;

  my $Train1Addr = $rProviderCreds->{"Train1Addr"};
  $p->fit_textline("Address: ", 37, $ypos, $baseboldfontoptions);
  $p->fit_textline($Train1Addr, 100, $ypos, $basefontoptions);

  my $Train1City = $rProviderCreds->{"Train1City"};
  $p->fit_textline("City: ", 300, $ypos, $baseboldfontoptions);
  $p->fit_textline($Train1City, 400, $ypos, $basefontoptions);

  $ypos += 15;


  my $Train1ST = $rProviderCreds->{"Train1ST"};
  $p->fit_textline("State: ", 37, $ypos, $baseboldfontoptions);
  $p->fit_textline($Train1ST, 70, $ypos, $basefontoptions);

  my $Train1Zip = $rProviderCreds->{"Train1Zip"};
  $p->fit_textline("Zip: ", 100, $ypos, $baseboldfontoptions);
  $p->fit_textline($Train1Zip, 130, $ypos, $basefontoptions);



  my $Train1Ph = $rProviderCreds->{"Train1Ph"};
  $p->fit_textline("Phone: ", 170, $ypos, $baseboldfontoptions);
  $p->fit_textline($Train1Ph, 210, $ypos, $basefontoptions);


  my $Train1Start = $rProviderCreds->{"Train1Start"};
  $p->fit_textline("From: ", 270, $ypos, $baseboldfontoptions);
  $p->fit_textline($Train1Start, 300, $ypos, $basefontoptions);



  my $Train1End = $rProviderCreds->{"Train1End"};
  $p->fit_textline("To: ", 380, $ypos, $baseboldfontoptions);
  $p->fit_textline($Train1End, 410, $ypos, $basefontoptions);

  $ypos += 25;








  # Training 2
  my $Train2Intern = $rProviderCreds->{"Train2Intern"};
  my $Train2Res = $rProviderCreds->{"Train2Res"};
  my $Train2Fellow = $rProviderCreds->{"Train2Fellow"};
  my $Train2Precept = $rProviderCreds->{"Train2Precept"};
  my $Train2Other = $rProviderCreds->{"Train2Other"};
  my $Train2Specify = $rProviderCreds->{"Train2Specify"};
  $p->fit_textline("(2) Type of Program:", 37, $ypos, $baseboldfontoptions);
  $ypos += 10;
  if($Train2Intern) {
    $p->fit_textline("&#x2713;", 37, $ypos, $basecheckfontoptions);
  } else {
    $p->fit_textline("&#x25a2;", 37, $ypos, $basecheckfontoptions);
  }
  $p->fit_textline("Internship", 50, $ypos, $basefontoptions);


  if($Train2Res) {
    $p->fit_textline("&#x2713;", 110, $ypos, $basecheckfontoptions);
  } else {
    $p->fit_textline("&#x25a2;", 110, $ypos, $basecheckfontoptions);
  }
  $p->fit_textline("Residency", 125, $ypos, $basefontoptions);

  if($Train2Fellow) {
    $p->fit_textline("&#x2713;", 180, $ypos, $basecheckfontoptions);
  } else {
    $p->fit_textline("&#x25a2;", 180, $ypos, $basecheckfontoptions);
  }

  $p->fit_textline("Fellowship", 195, $ypos, $basefontoptions);


  if($Train2Precept) {
    $p->fit_textline("&#x2713;", 260, $ypos, $basecheckfontoptions);
  } else {
    $p->fit_textline("&#x25a2;", 260, $ypos, $basecheckfontoptions);
  }

  $p->fit_textline("Preceptorship", 275, $ypos, $basefontoptions);


  if($Train2Other) {
    $p->fit_textline("&#x2713;", 350, $ypos, $basecheckfontoptions);
  } else {
    $p->fit_textline("&#x25a2;", 350, $ypos, $basecheckfontoptions);
  }

  $p->fit_textline("Other", 365, $ypos, $basefontoptions);
  if($Train2Other) {
    $p->fit_textline("$Train2Specify (Other)", 400, $ypos, $basefontoptions);
  }

  $ypos += 15;
  my $Train2Complete = $rProviderCreds->{"Train2Complete"};
  $p->fit_textline("Was program successfully completed: ", 37, $ypos, $baseboldfontoptions);
  $p->fit_textline($YesNoArr{$Train2Complete}, 210, $ypos, $basefontoptions);

  my $Train2Specialty = $rProviderCreds->{"Train2Specialty"};
  my $Train2SpecialtyName = DBA->getxrefWithDef($form,'xOccupationSnomed',$Train2Specialty,'Description');
  $p->fit_textline("Specialty: ", 300, $ypos, $baseboldfontoptions);
  $p->fit_textline($Train2SpecialtyName, 360, $ypos, $basefontoptions);
  $ypos += 15;


  my $Train2 = $rProviderCreds->{"Train2"};
  $p->fit_textline("Institution: ", 37, $ypos, $baseboldfontoptions);
  $p->fit_textline($Train2, 100, $ypos, $basefontoptions);

  my $Train2Director = $rProviderCreds->{"Train2Director"};
  $p->fit_textline("Program Director:", 300, $ypos, $baseboldfontoptions);
  $p->fit_textline($Train2Director, 400, $ypos, $basefontoptions);
  
  $ypos += 15;

  my $Train2Addr = $rProviderCreds->{"Train2Addr"};
  $p->fit_textline("Address: ", 37, $ypos, $baseboldfontoptions);
  $p->fit_textline($Train2Addr, 100, $ypos, $basefontoptions);

  my $Train2City = $rProviderCreds->{"Train2City"};
  $p->fit_textline("City: ", 300, $ypos, $baseboldfontoptions);
  $p->fit_textline($Train2City, 400, $ypos, $basefontoptions);

  $ypos += 15;


  my $Train2ST = $rProviderCreds->{"Train2ST"};
  $p->fit_textline("State: ", 37, $ypos, $baseboldfontoptions);
  $p->fit_textline($Train2ST, 70, $ypos, $basefontoptions);

  my $Train2Zip = $rProviderCreds->{"Train2Zip"};
  $p->fit_textline("Zip: ", 100, $ypos, $baseboldfontoptions);
  $p->fit_textline($Train2Zip, 130, $ypos, $basefontoptions);



  my $Train2Ph = $rProviderCreds->{"Train2Ph"};
  $p->fit_textline("Phone: ", 170, $ypos, $baseboldfontoptions);
  $p->fit_textline($Train2Ph, 210, $ypos, $basefontoptions);


  my $Train2Start = $rProviderCreds->{"Train2Start"};
  $p->fit_textline("From: ", 270, $ypos, $baseboldfontoptions);
  $p->fit_textline($Train2Start, 300, $ypos, $basefontoptions);



  my $Train2End = $rProviderCreds->{"Train2End"};
  $p->fit_textline("To: ", 380, $ypos, $baseboldfontoptions);
  $p->fit_textline($Train2End, 410, $ypos, $basefontoptions);



  # Training 3
  $ypos += 25;
  my $Train3Intern = $rProviderCreds->{"Train3Intern"};
  my $Train3Res = $rProviderCreds->{"Train3Res"};
  my $Train3Fellow = $rProviderCreds->{"Train3Fellow"};
  my $Train3Precept = $rProviderCreds->{"Train3Precept"};
  my $Train3Other = $rProviderCreds->{"Train3Other"};
  my $Train3Specify = $rProviderCreds->{"Train3Specify"};
  $p->fit_textline("(3) Type of Program:", 37, $ypos, $baseboldfontoptions);
  $ypos += 10;
  if($Train3Intern) {
    $p->fit_textline("&#x2713;", 37, $ypos, $basecheckfontoptions);
  } else {
    $p->fit_textline("&#x25a2;", 37, $ypos, $basecheckfontoptions);
  }
  $p->fit_textline("Internship", 50, $ypos, $basefontoptions);


  if($Train3Res) {
    $p->fit_textline("&#x2713;", 110, $ypos, $basecheckfontoptions);
  } else {
    $p->fit_textline("&#x25a2;", 110, $ypos, $basecheckfontoptions);
  }
  $p->fit_textline("Residency", 125, $ypos, $basefontoptions);

  if($Train3Fellow) {
    $p->fit_textline("&#x2713;", 180, $ypos, $basecheckfontoptions);
  } else {
    $p->fit_textline("&#x25a2;", 180, $ypos, $basecheckfontoptions);
  }

  $p->fit_textline("Fellowship", 195, $ypos, $basefontoptions);


  if($Train3Precept) {
    $p->fit_textline("&#x2713;", 260, $ypos, $basecheckfontoptions);
  } else {
    $p->fit_textline("&#x25a2;", 260, $ypos, $basecheckfontoptions);
  }

  $p->fit_textline("Preceptorship", 275, $ypos, $basefontoptions);


  if($Train3Other) {
    $p->fit_textline("&#x2713;", 350, $ypos, $basecheckfontoptions);
  } else {
    $p->fit_textline("&#x25a2;", 350, $ypos, $basecheckfontoptions);
  }

  $p->fit_textline("Other", 365, $ypos, $basefontoptions);
  if($Train3Other) {
    $p->fit_textline("$Train3Specify (Other)", 400, $ypos, $basefontoptions);
  }

  $ypos += 15;
  my $Train3Complete = $rProviderCreds->{"Train3Complete"};
  $p->fit_textline("Was program successfully completed: ", 37, $ypos, $baseboldfontoptions);
  $p->fit_textline($YesNoArr{$Train3Complete}, 210, $ypos, $basefontoptions);

  my $Train3Specialty = $rProviderCreds->{"Train3Specialty"};
  my $Train3SpecialtyName = DBA->getxrefWithDef($form,'xOccupationSnomed',$Train3Specialty,'Description');
  $p->fit_textline("Specialty: ", 300, $ypos, $baseboldfontoptions);
  $p->fit_textline($Train3SpecialtyName, 360, $ypos, $basefontoptions);
  $ypos += 15;


  my $Train3 = $rProviderCreds->{"Train3"};
  $p->fit_textline("Institution: ", 37, $ypos, $baseboldfontoptions);
  $p->fit_textline($Train3, 100, $ypos, $basefontoptions);

  my $Train3Director = $rProviderCreds->{"Train3Director"};
  $p->fit_textline("Program Director:", 300, $ypos, $baseboldfontoptions);
  $p->fit_textline($Train3Director, 400, $ypos, $basefontoptions);
  
  $ypos += 15;

  my $Train3Addr = $rProviderCreds->{"Train3Addr"};
  $p->fit_textline("Address: ", 37, $ypos, $baseboldfontoptions);
  $p->fit_textline($Train3Addr, 100, $ypos, $basefontoptions);

  my $Train3City = $rProviderCreds->{"Train3City"};
  $p->fit_textline("City: ", 300, $ypos, $baseboldfontoptions);
  $p->fit_textline($Train3City, 400, $ypos, $basefontoptions);

  $ypos += 15;


  my $Train3ST = $rProviderCreds->{"Train3ST"};
  $p->fit_textline("State: ", 37, $ypos, $baseboldfontoptions);
  $p->fit_textline($Train3ST, 70, $ypos, $basefontoptions);

  my $Train3Zip = $rProviderCreds->{"Train3Zip"};
  $p->fit_textline("Zip: ", 100, $ypos, $baseboldfontoptions);
  $p->fit_textline($Train3Zip, 130, $ypos, $basefontoptions);



  my $Train3Ph = $rProviderCreds->{"Train3Ph"};
  $p->fit_textline("Phone: ", 170, $ypos, $baseboldfontoptions);
  $p->fit_textline($Train3Ph, 210, $ypos, $basefontoptions);


  my $Train3Start = $rProviderCreds->{"Train3Start"};
  $p->fit_textline("From: ", 260, $ypos, $baseboldfontoptions);
  $p->fit_textline($Train3Start, 300, $ypos, $basefontoptions);



  my $Train3End = $rProviderCreds->{"Train3End"};
  $p->fit_textline("To: ", 370, $ypos, $baseboldfontoptions);
  $p->fit_textline($Train3End, 410, $ypos, $basefontoptions);




  # Training 3
  $ypos += 25;
  my $Train4Intern = $rProviderCreds->{"Train4Intern"};
  my $Train4Res = $rProviderCreds->{"Train4Res"};
  my $Train4Fellow = $rProviderCreds->{"Train4Fellow"};
  my $Train4Precept = $rProviderCreds->{"Train4Precept"};
  my $Train4Other = $rProviderCreds->{"Train4Other"};
  my $Train4Specify = $rProviderCreds->{"Train4Specify"};
  $p->fit_textline("(4) Type of Program:", 37, $ypos, $baseboldfontoptions);
  $ypos += 10;
  if($Train4Intern) {
    $p->fit_textline("&#x2713;", 37, $ypos, $basecheckfontoptions);
  } else {
    $p->fit_textline("&#x25a2;", 37, $ypos, $basecheckfontoptions);
  }
  $p->fit_textline("Internship", 50, $ypos, $basefontoptions);


  if($Train4Res) {
    $p->fit_textline("&#x2713;", 110, $ypos, $basecheckfontoptions);
  } else {
    $p->fit_textline("&#x25a2;", 110, $ypos, $basecheckfontoptions);
  }
  $p->fit_textline("Residency", 125, $ypos, $basefontoptions);

  if($Train4Fellow) {
    $p->fit_textline("&#x2713;", 180, $ypos, $basecheckfontoptions);
  } else {
    $p->fit_textline("&#x25a2;", 180, $ypos, $basecheckfontoptions);
  }

  $p->fit_textline("Fellowship", 195, $ypos, $basefontoptions);


  if($Train4Precept) {
    $p->fit_textline("&#x2713;", 260, $ypos, $basecheckfontoptions);
  } else {
    $p->fit_textline("&#x25a2;", 260, $ypos, $basecheckfontoptions);
  }

  $p->fit_textline("Preceptorship", 275, $ypos, $basefontoptions);


  if($Train4Other) {
    $p->fit_textline("&#x2713;", 350, $ypos, $basecheckfontoptions);
  } else {
    $p->fit_textline("&#x25a2;", 350, $ypos, $basecheckfontoptions);
  }

  $p->fit_textline("Other", 365, $ypos, $basefontoptions);
  if($Train4Other) {
    $p->fit_textline("$Train4Specify (Other)", 400, $ypos, $basefontoptions);
  }

  $ypos += 15;
  my $Train4Complete = $rProviderCreds->{"Train4Complete"};
  $p->fit_textline("Was program successfully completed: ", 37, $ypos, $baseboldfontoptions);
  $p->fit_textline($YesNoArr{$Train4Complete}, 210, $ypos, $basefontoptions);

  my $Train4Specialty = $rProviderCreds->{"Train4Specialty"};
  my $Train4SpecialtyName = DBA->getxrefWithDef($form,'xOccupationSnomed',$Train4Specialty,'Description');
  $p->fit_textline("Specialty: ", 300, $ypos, $baseboldfontoptions);
  $p->fit_textline($Train4SpecialtyName, 360, $ypos, $basefontoptions);
  $ypos += 15;


  my $Train4 = $rProviderCreds->{"Train4"};
  $p->fit_textline("Institution: ", 37, $ypos, $baseboldfontoptions);
  $p->fit_textline($Train4, 100, $ypos, $basefontoptions);

  my $Train4Director = $rProviderCreds->{"Train4Director"};
  $p->fit_textline("Program Director:", 300, $ypos, $baseboldfontoptions);
  $p->fit_textline($Train4Director, 400, $ypos, $basefontoptions);
  
  $ypos += 15;

  my $Train4Addr = $rProviderCreds->{"Train4Addr"};
  $p->fit_textline("Address: ", 37, $ypos, $baseboldfontoptions);
  $p->fit_textline($Train4Addr, 100, $ypos, $basefontoptions);

  my $Train4City = $rProviderCreds->{"Train4City"};
  $p->fit_textline("City: ", 300, $ypos, $baseboldfontoptions);
  $p->fit_textline($Train4City, 400, $ypos, $basefontoptions);

  $ypos += 15;


  my $Train4ST = $rProviderCreds->{"Train4ST"};
  $p->fit_textline("State: ", 37, $ypos, $baseboldfontoptions);
  $p->fit_textline($Train4ST, 70, $ypos, $basefontoptions);

  my $Train4Zip = $rProviderCreds->{"Train4Zip"};
  $p->fit_textline("Zip: ", 100, $ypos, $baseboldfontoptions);
  $p->fit_textline($Train4Zip, 130, $ypos, $basefontoptions);



  my $Train4Ph = $rProviderCreds->{"Train4Ph"};
  $p->fit_textline("Phone: ", 170, $ypos, $baseboldfontoptions);
  $p->fit_textline($Train4Ph, 210, $ypos, $basefontoptions);


  my $Train4Start = $rProviderCreds->{"Train4Start"};
  $p->fit_textline("From: ", 270, $ypos, $baseboldfontoptions);
  $p->fit_textline($Train4Start, 300, $ypos, $basefontoptions);



  my $Train4End = $rProviderCreds->{"Train4End"};
  $p->fit_textline("To: ", 380, $ypos, $baseboldfontoptions);
  $p->fit_textline($Train4End, 410, $ypos, $basefontoptions);

  main->createFooter($p);


  # Start Page 5 

  $p->begin_page_ext($pagewidth, $pageheight, "topdown");
  # Office Billing Address
  $ypos = $margintop;

  $p->fit_textline("SECTION 6: ACADEMIC APPOINTMENTS", 37, $ypos, $baseboldlargefontoptions_u);
  $ypos += 25;
  $p->fit_textline("List all, past and present. If additional space is needed, copy this sheet or continue in Section 14.", 37, $ypos, $baseboldmidfontoptions);
  $ypos += 15;

  # (1) Institution
  my $Academic1 = $rProviderCreds->{"Academic1"};
  $p->fit_textline("(1) Institution:", 37, $ypos, $baseboldmidfontoptions);
  $p->fit_textline($Academic1, 110, $ypos, $basefontoptions);


  my $Academic1Addr = $rProviderCreds->{"Academic1Addr"};
  $p->fit_textline("Address:", 300, $ypos, $baseboldmidfontoptions);
  $p->fit_textline($Academic1Addr, 350, $ypos, $basefontoptions);

  $ypos += 15;

  my $Academic1City = $rProviderCreds->{"Academic1City"};
  $p->fit_textline("City:", 37, $ypos, $baseboldmidfontoptions);
  $p->fit_textline($Academic1City, 70, $ypos, $basefontoptions);


  my $Academic1ST = $rProviderCreds->{"Academic1ST"};
  $p->fit_textline("State:", 130, $ypos, $baseboldmidfontoptions);
  $p->fit_textline($Academic1ST, 170, $ypos, $basefontoptions);


  my $Academic1Zip = $rProviderCreds->{"Academic1Zip"};
  $p->fit_textline("Zip:", 200, $ypos, $baseboldmidfontoptions);
  $p->fit_textline($Academic1Zip, 230, $ypos, $basefontoptions);

  my $Academic1Ph = $rProviderCreds->{"Academic1Ph"};
  $p->fit_textline("Phone:", 300, $ypos, $baseboldmidfontoptions);
  $p->fit_textline($Academic1Ph, 340, $ypos, $basefontoptions);

  $ypos += 15;


  my $Academic1Postion = $rProviderCreds->{"Academic1Postion"};
  $p->fit_textline("Position/Rank:", 37, $ypos, $baseboldmidfontoptions);
  $p->fit_textline($Academic1Postion, 120, $ypos, $basefontoptions);

  my $Academic1Start = $rProviderCreds->{"Academic1Start"};
  $p->fit_textline("From: ", 200, $ypos, $baseboldfontoptions);
  $p->fit_textline($Academic1Start, 230, $ypos, $basefontoptions);



  my $Academic1End = $rProviderCreds->{"Academic1End"};
  $p->fit_textline("To: ", 300, $ypos, $baseboldfontoptions);
  $p->fit_textline($Academic1End, 330, $ypos, $basefontoptions);

  $ypos += 25;

  # (2) Institution


  my $Academic2 = $rProviderCreds->{"Academic2"};
  $p->fit_textline("(2) Institution:", 37, $ypos, $baseboldmidfontoptions);
  $p->fit_textline($Academic2, 110, $ypos, $basefontoptions);


  my $Academic2Addr = $rProviderCreds->{"Academic2Addr"};
  $p->fit_textline("Address:", 300, $ypos, $baseboldmidfontoptions);
  $p->fit_textline($Academic2Addr, 350, $ypos, $basefontoptions);

  $ypos += 15;

  my $Academic2City = $rProviderCreds->{"Academic2City"};
  $p->fit_textline("City:", 37, $ypos, $baseboldmidfontoptions);
  $p->fit_textline($Academic2City, 70, $ypos, $basefontoptions);


  my $Academic2ST = $rProviderCreds->{"Academic2ST"};
  $p->fit_textline("State:", 130, $ypos, $baseboldmidfontoptions);
  $p->fit_textline($Academic2ST, 170, $ypos, $basefontoptions);


  my $Academic2Zip = $rProviderCreds->{"Academic2Zip"};
  $p->fit_textline("Zip:", 200, $ypos, $baseboldmidfontoptions);
  $p->fit_textline($Academic2Zip, 230, $ypos, $basefontoptions);

  my $Academic2Ph = $rProviderCreds->{"Academic2Ph"};
  $p->fit_textline("Phone:", 300, $ypos, $baseboldmidfontoptions);
  $p->fit_textline($Academic2Ph, 340, $ypos, $basefontoptions);

  $ypos += 15;


  my $Academic2Postion = $rProviderCreds->{"Academic2Postion"};
  $p->fit_textline("Position/Rank:", 37, $ypos, $baseboldmidfontoptions);
  $p->fit_textline($Academic2Postion, 120, $ypos, $basefontoptions);

  my $Academic2Start = $rProviderCreds->{"Academic2Start"};
  $p->fit_textline("From: ", 200, $ypos, $baseboldfontoptions);
  $p->fit_textline($Academic2Start, 230, $ypos, $basefontoptions);



  my $Academic2End = $rProviderCreds->{"Academic2End"};
  $p->fit_textline("To: ", 300, $ypos, $baseboldfontoptions);
  $p->fit_textline($Academic2End, 330, $ypos, $basefontoptions);




  $ypos += 25;

  # (3) Institution


  my $Academic3 = $rProviderCreds->{"Academic3"};
  $p->fit_textline("(3) Institution:", 37, $ypos, $baseboldmidfontoptions);
  $p->fit_textline($Academic3, 110, $ypos, $basefontoptions);


  my $Academic3Addr = $rProviderCreds->{"Academic3Addr"};
  $p->fit_textline("Address:", 300, $ypos, $baseboldmidfontoptions);
  $p->fit_textline($Academic3Addr, 350, $ypos, $basefontoptions);

  $ypos += 15;

  my $Academic3City = $rProviderCreds->{"Academic3City"};
  $p->fit_textline("City:", 37, $ypos, $baseboldmidfontoptions);
  $p->fit_textline($Academic3City, 70, $ypos, $basefontoptions);


  my $Academic3ST = $rProviderCreds->{"Academic3ST"};
  $p->fit_textline("State:", 130, $ypos, $baseboldmidfontoptions);
  $p->fit_textline($Academic3ST, 170, $ypos, $basefontoptions);


  my $Academic3Zip = $rProviderCreds->{"Academic3Zip"};
  $p->fit_textline("Zip:", 200, $ypos, $baseboldmidfontoptions);
  $p->fit_textline($Academic3Zip, 230, $ypos, $basefontoptions);

  my $Academic3Ph = $rProviderCreds->{"Academic3Ph"};
  $p->fit_textline("Phone:", 300, $ypos, $baseboldmidfontoptions);
  $p->fit_textline($Academic3Ph, 340, $ypos, $basefontoptions);

  $ypos += 15;


  my $Academic3Postion = $rProviderCreds->{"Academic3Postion"};
  $p->fit_textline("Position/Rank:", 37, $ypos, $baseboldmidfontoptions);
  $p->fit_textline($Academic3Postion, 120, $ypos, $basefontoptions);

  my $Academic3Start = $rProviderCreds->{"Academic3Start"};
  $p->fit_textline("From: ", 200, $ypos, $baseboldfontoptions);
  $p->fit_textline($Academic3Start, 230, $ypos, $basefontoptions);



  my $Academic3End = $rProviderCreds->{"Academic3End"};
  $p->fit_textline("To: ", 300, $ypos, $baseboldfontoptions);
  $p->fit_textline($Academic3End, 330, $ypos, $basefontoptions);

  $ypos += 25;

  $p->fit_textline("SECTION 7: HEALTH CARE AFFILIATIONS", 37, $ypos, $baseboldlargefontoptions_u);
  my $h_address = 4 * $fontsizexxlarge;
  $ypos += $h_address;
  my $w_address = $pagewidth - 10;
  my $x_address = $pagewidth / 2 - $w_address / 2;
  $tf = $p->create_textflow("List, in chronological order, all hospital/health system affiliations where you have ever been employed, practiced, associated, or privileged for the purpose of providing patient care. Do not list affiliations that were part of your training (Section 5). If additional space is required, copy this sheet or continue in Section 14", $baselargefontoptions . " leading=110% alignment=justify lastalignment=justify");
  $p->fit_textflow($tf, 37, $ypos, $x_address+$w_address, $ypos - $h_address, "verticalalign=center");
  $ypos += 15;
  $p->fit_textline('Indicate which of these is your "current primary and secondary admitting facility" (where you currently spend the greatest portion of your time)', 37, $ypos, $basefontoptions);
  $ypos += 15;

  # (1) Facility Name
  my $Hospital1 = $rProviderCreds->{"Hospital1"};
  $p->fit_textline("(1) Facility Name:", 37, $ypos, $baseboldfontoptions);
  $p->fit_textline($Hospital1, 120, $ypos, $basefontoptions);

  my %Hospital1PriorityArr = ("P", "Primary", "S", "Secondary");
  my $Hospital1Priority = $rProviderCreds->{"Hospital1Priority"};
  $p->fit_textline("Priority:", 400, $ypos, $baseboldfontoptions);
  $p->fit_textline($Hospital1PriorityArr{$Hospital1Priority}, 460, $ypos, $basefontoptions);


  $ypos += 15;
  my $Hospital1Addr = $rProviderCreds->{"Hospital1Addr"};
  $p->fit_textline("Complete Mailing Address:", 37, $ypos, $baseboldfontoptions);
  $p->fit_textline($Hospital1Addr, 150, $ypos, $basefontoptions);

  $ypos += 15;

  my $Hospital1City = $rProviderCreds->{"Hospital1City"};
  $p->fit_textline("City:", 37, $ypos, $baseboldmidfontoptions);
  $p->fit_textline($Hospital1City, 70, $ypos, $basefontoptions);


  my $Hospital1ST = $rProviderCreds->{"Hospital1ST"};
  $p->fit_textline("State:", 150, $ypos, $baseboldmidfontoptions);
  $p->fit_textline($Hospital1ST, 190, $ypos, $basefontoptions);


  my $Hospital1Zip = $rProviderCreds->{"Hospital1Zip"};
  $p->fit_textline("Zip:", 220, $ypos, $baseboldmidfontoptions);
  $p->fit_textline($Hospital1Zip, 250, $ypos, $basefontoptions);

  my $Hospital1Ph = $rProviderCreds->{"Hospital1Ph"};
  $p->fit_textline("Phone:", 320, $ypos, $baseboldmidfontoptions);
  $p->fit_textline($Hospital1Ph, 360, $ypos, $basefontoptions);

  $ypos += 15;


  my $Hospital1StaffCategory = $rProviderCreds->{"Hospital1StaffCategory"};
  $p->fit_textline("Staff Category:", 37, $ypos, $baseboldmidfontoptions);
  $p->fit_textline($Hospital1StaffCategory, 120, $ypos, $basefontoptions);


  my $Hospital1Start = $rProviderCreds->{"Hospital1Start"};
  $p->fit_textline("From: ", 200, $ypos, $baseboldfontoptions);
  $p->fit_textline($Hospital1Start, 230, $ypos, $basefontoptions);



  my $Hospital1End = $rProviderCreds->{"Hospital1End"};
  $p->fit_textline("To: ", 290, $ypos, $baseboldfontoptions);
  $p->fit_textline($Hospital1End, 320, $ypos, $basefontoptions);


  my $Hospital1Dept = $rProviderCreds->{"Hospital1Dept"};
  $p->fit_textline("Department or Service:",370, $ypos, $baseboldmidfontoptions);
  $p->fit_textline($Hospital1Dept, 490, $ypos, $basefontoptions);

  $ypos += 15;
  my $Hospital1Reason = $rProviderCreds->{"Hospital1Reason"};
  $p->fit_textline("Reason for Discontinuance:", 37, $ypos, $baseboldmidfontoptions);
  $p->fit_textline($Hospital1Reason, 170, $ypos, $basefontoptions);




  # (2) Facility Name
  $ypos += 20;

  my $Hospital2 = $rProviderCreds->{"Hospital2"};
  $p->fit_textline("(2) Facility Name:", 37, $ypos, $baseboldfontoptions);
  $p->fit_textline($Hospital2, 120, $ypos, $basefontoptions);

  my %Hospital2PriorityArr = ("P", "Primary", "S", "Secondary");
  my $Hospital2Priority = $rProviderCreds->{"Hospital2Priority"};
  $p->fit_textline("Priority:", 400, $ypos, $baseboldfontoptions);
  $p->fit_textline($Hospital2PriorityArr{$Hospital2Priority}, 460, $ypos, $basefontoptions);


  $ypos += 15;
  my $Hospital2Addr = $rProviderCreds->{"Hospital2Addr"};
  $p->fit_textline("Complete Mailing Address:", 37, $ypos, $baseboldfontoptions);
  $p->fit_textline($Hospital2Addr, 150, $ypos, $basefontoptions);

  $ypos += 15;

  my $Hospital2City = $rProviderCreds->{"Hospital2City"};
  $p->fit_textline("City:", 37, $ypos, $baseboldmidfontoptions);
  $p->fit_textline($Hospital2City, 70, $ypos, $basefontoptions);


  my $Hospital2ST = $rProviderCreds->{"Hospital2ST"};
  $p->fit_textline("State:", 150, $ypos, $baseboldmidfontoptions);
  $p->fit_textline($Hospital2ST, 190, $ypos, $basefontoptions);


  my $Hospital2Zip = $rProviderCreds->{"Hospital2Zip"};
  $p->fit_textline("Zip:", 220, $ypos, $baseboldmidfontoptions);
  $p->fit_textline($Hospital2Zip, 250, $ypos, $basefontoptions);

  my $Hospital2Ph = $rProviderCreds->{"Hospital2Ph"};
  $p->fit_textline("Phone:", 320, $ypos, $baseboldmidfontoptions);
  $p->fit_textline($Hospital2Ph, 360, $ypos, $basefontoptions);

  $ypos += 15;


  my $Hospital2StaffCategory = $rProviderCreds->{"Hospital2StaffCategory"};
  $p->fit_textline("Staff Category:", 37, $ypos, $baseboldmidfontoptions);
  $p->fit_textline($Hospital2StaffCategory, 120, $ypos, $basefontoptions);


  my $Hospital2Start = $rProviderCreds->{"Hospital2Start"};
  $p->fit_textline("From: ", 200, $ypos, $baseboldfontoptions);
  $p->fit_textline($Hospital2Start, 230, $ypos, $basefontoptions);



  my $Hospital2End = $rProviderCreds->{"Hospital2End"};
  $p->fit_textline("To: ", 290, $ypos, $baseboldfontoptions);
  $p->fit_textline($Hospital2End, 320, $ypos, $basefontoptions);


  my $Hospital2Dept = $rProviderCreds->{"Hospital2Dept"};
  $p->fit_textline("Department or Service:",370, $ypos, $baseboldmidfontoptions);
  $p->fit_textline($Hospital2Dept, 490, $ypos, $basefontoptions);

  $ypos += 15;
  my $Hospital2Reason = $rProviderCreds->{"Hospital2Reason"};
  $p->fit_textline("Reason for Discontinuance:", 37, $ypos, $baseboldmidfontoptions);
  $p->fit_textline($Hospital2Reason, 170, $ypos, $basefontoptions);




  # (3) Facility Name
  $ypos += 20;

  my $Hospital3 = $rProviderCreds->{"Hospital3"};
  $p->fit_textline("(3) Facility Name:", 37, $ypos, $baseboldfontoptions);
  $p->fit_textline($Hospital3, 120, $ypos, $basefontoptions);

  my %Hospital3PriorityArr = ("P", "Primary", "S", "Secondary");
  my $Hospital3Priority = $rProviderCreds->{"Hospital3Priority"};
  $p->fit_textline("Priority:", 400, $ypos, $baseboldfontoptions);
  $p->fit_textline($Hospital3PriorityArr{$Hospital3Priority}, 460, $ypos, $basefontoptions);


  $ypos += 15;
  my $Hospital3Addr = $rProviderCreds->{"Hospital3Addr"};
  $p->fit_textline("Complete Mailing Address:", 37, $ypos, $baseboldfontoptions);
  $p->fit_textline($Hospital3Addr, 150, $ypos, $basefontoptions);

  $ypos += 15;

  my $Hospital3City = $rProviderCreds->{"Hospital3City"};
  $p->fit_textline("City:", 37, $ypos, $baseboldmidfontoptions);
  $p->fit_textline($Hospital3City, 70, $ypos, $basefontoptions);


  my $Hospital3ST = $rProviderCreds->{"Hospital3ST"};
  $p->fit_textline("State:", 150, $ypos, $baseboldmidfontoptions);
  $p->fit_textline($Hospital3ST, 190, $ypos, $basefontoptions);


  my $Hospital3Zip = $rProviderCreds->{"Hospital3Zip"};
  $p->fit_textline("Zip:", 220, $ypos, $baseboldmidfontoptions);
  $p->fit_textline($Hospital3Zip, 250, $ypos, $basefontoptions);

  my $Hospital3Ph = $rProviderCreds->{"Hospital3Ph"};
  $p->fit_textline("Phone:", 320, $ypos, $baseboldmidfontoptions);
  $p->fit_textline($Hospital3Ph, 360, $ypos, $basefontoptions);

  $ypos += 15;


  my $Hospital3StaffCategory = $rProviderCreds->{"Hospital3StaffCategory"};
  $p->fit_textline("Staff Category:", 37, $ypos, $baseboldmidfontoptions);
  $p->fit_textline($Hospital3StaffCategory, 120, $ypos, $basefontoptions);


  my $Hospital3Start = $rProviderCreds->{"Hospital3Start"};
  $p->fit_textline("From: ", 200, $ypos, $baseboldfontoptions);
  $p->fit_textline($Hospital3Start, 230, $ypos, $basefontoptions);



  my $Hospital3End = $rProviderCreds->{"Hospital3End"};
  $p->fit_textline("To: ", 290, $ypos, $baseboldfontoptions);
  $p->fit_textline($Hospital3End, 320, $ypos, $basefontoptions);


  my $Hospital3Dept = $rProviderCreds->{"Hospital3Dept"};
  $p->fit_textline("Department or Service:",370, $ypos, $baseboldmidfontoptions);
  $p->fit_textline($Hospital3Dept, 490, $ypos, $basefontoptions);

  $ypos += 15;
  my $Hospital3Reason = $rProviderCreds->{"Hospital3Reason"};
  $p->fit_textline("Reason for Discontinuance:", 37, $ypos, $baseboldmidfontoptions);
  $p->fit_textline($Hospital3Reason, 170, $ypos, $basefontoptions);

  main->createFooter($p);


  # Page 6
  $ypos = $margintop;
  $p->begin_page_ext($pagewidth, $pageheight, "topdown");
  $p->fit_textline("SECTION 8: OTHER PROFESSIONAL WORK HISTORY", 37, $ypos, $baseboldlargefontoptions_u);
  my $h_address = 4 * $fontsizexxlarge;
  $ypos += $h_address;
  my $w_address = $pagewidth - 10;
  my $x_address = $pagewidth / 2 - $w_address / 2;
  $tf = $p->create_textflow("List, chronologically, all professional work history (i.e. clinics, partnerships, solo/group practices, employment). Include secondary agencies or clinics such as public health and family planning where you perform duties. Account for all time gaps of thirty (30) days or more. If additional space is needed, copy this page or continue in Section 14.", $baselargefontoptions . " leading=110% alignment=justify lastalignment=justify");
  $p->fit_textflow($tf, 37, $ypos, $x_address+$w_address, $ypos - $h_address, "verticalalign=center");
  $ypos += 15;


  #  Other 1

  my $Work1 = $rProviderCreds->{"Work1"};
  $p->fit_textline("(1) Name:", 37, $ypos, $baseboldmidfontoptions);
  $p->fit_textline($Work1, 100, $ypos, $basefontoptions);

  my $Work1Nature = $rProviderCreds->{"Work1Nature"};
  $p->fit_textline("(1) Nature of Affiliation:", 250, $ypos, $baseboldmidfontoptions);
  $p->fit_textline($Work1Nature, 370, $ypos, $basefontoptions);

  $ypos += 15;

  my $Work1Addr = $rProviderCreds->{"Work1Addr"};
  $p->fit_textline("Mailing Address:", 37, $ypos, $baseboldmidfontoptions);
  $p->fit_textline($Work1Addr, 120, $ypos, $basefontoptions);

  $ypos += 15;

  my $Work1City = $rProviderCreds->{"Work1City"};
  $p->fit_textline("City:",  37, $ypos, $baseboldfontoptions);
  $p->fit_textline($Work1City,   70, $ypos, $basefontoptions);

  my $Work1ST = $rProviderCreds->{"Work1ST"};
  $p->fit_textline("State:",  150, $ypos, $baseboldfontoptions);
  $p->fit_textline($Work1ST,   180, $ypos, $basefontoptions);


  my $Work1Zip = $rProviderCreds->{"Work1Zip"};
  $p->fit_textline("ZIP:",  250, $ypos, $baseboldfontoptions);
  $p->fit_textline($Work1Zip,   280, $ypos, $basefontoptions); 


  my $Work1Ph = $rProviderCreds->{"Work1Ph"};
  $p->fit_textline("Phone:",  370, $ypos, $baseboldfontoptions);
  $p->fit_textline($Work1Ph,   410, $ypos, $basefontoptions);
  $ypos += 15;


  $p->fit_textline("Dates of Affiliation:", 37, $ypos, $baseboldmidfontoptions);

  my $Work1Start = $rProviderCreds->{"Work1Start"};
  $p->fit_textline("From: ", 200, $ypos, $baseboldfontoptions);
  $p->fit_textline($Work1Start, 230, $ypos, $basefontoptions);


  my $Work1End = $rProviderCreds->{"Work1End"};
  $p->fit_textline("To: ", 300, $ypos, $baseboldfontoptions);
  $p->fit_textline($Work1End, 330, $ypos, $basefontoptions);

  $ypos += 15;

  my $Work1Reason = $rProviderCreds->{"Work1Reason"};
  $p->fit_textline("Reason for Discontinuance:", 37, $ypos, $baseboldfontoptions);
  $p->fit_textline($Work1Reason, 170, $ypos, $basefontoptions);  




  #  Other 2
  $ypos += 25;

  my $Work2 = $rProviderCreds->{"Work2"};
  $p->fit_textline("(2) Name:", 37, $ypos, $baseboldmidfontoptions);
  $p->fit_textline($Work2, 100, $ypos, $basefontoptions);

  my $Work2Nature = $rProviderCreds->{"Work2Nature"};
  $p->fit_textline("(2) Nature of Affiliation:", 250, $ypos, $baseboldmidfontoptions);
  $p->fit_textline($Work2Nature, 370, $ypos, $basefontoptions);

  $ypos += 15;

  my $Work2Addr = $rProviderCreds->{"Work2Addr"};
  $p->fit_textline("Mailing Address:", 37, $ypos, $baseboldmidfontoptions);
  $p->fit_textline($Work2Addr, 120, $ypos, $basefontoptions);

  $ypos += 15;

  my $Work2City = $rProviderCreds->{"Work2City"};
  $p->fit_textline("City:",  37, $ypos, $baseboldfontoptions);
  $p->fit_textline($Work2City,   70, $ypos, $basefontoptions);

  my $Work2ST = $rProviderCreds->{"Work2ST"};
  $p->fit_textline("State:",  150, $ypos, $baseboldfontoptions);
  $p->fit_textline($Work2ST,   180, $ypos, $basefontoptions);


  my $Work2Zip = $rProviderCreds->{"Work2Zip"};
  $p->fit_textline("ZIP:",  250, $ypos, $baseboldfontoptions);
  $p->fit_textline($Work2Zip,   280, $ypos, $basefontoptions); 


  my $Work2Ph = $rProviderCreds->{"Work2Ph"};
  $p->fit_textline("Phone:",  370, $ypos, $baseboldfontoptions);
  $p->fit_textline($Work2Ph,   410, $ypos, $basefontoptions);
  $ypos += 15;


  $p->fit_textline("Dates of Affiliation:", 37, $ypos, $baseboldmidfontoptions);

  my $Work2Start = $rProviderCreds->{"Work2Start"};
  $p->fit_textline("From: ", 200, $ypos, $baseboldfontoptions);
  $p->fit_textline($Work2Start, 230, $ypos, $basefontoptions);


  my $Work2End = $rProviderCreds->{"Work2End"};
  $p->fit_textline("To: ", 300, $ypos, $baseboldfontoptions);
  $p->fit_textline($Work2End, 330, $ypos, $basefontoptions);

  $ypos += 15;

  my $Work2Reason = $rProviderCreds->{"Work2Reason"};
  $p->fit_textline("Reason for Discontinuance:", 37, $ypos, $baseboldfontoptions);
  $p->fit_textline($Work2Reason, 170, $ypos, $basefontoptions);  


  #  Other 3
  $ypos += 25;

  my $Work3 = $rProviderCreds->{"Work3"};
  $p->fit_textline("(3) Name:", 37, $ypos, $baseboldmidfontoptions);
  $p->fit_textline($Work3, 100, $ypos, $basefontoptions);

  my $Work3Nature = $rProviderCreds->{"Work3Nature"};
  $p->fit_textline("(3) Nature of Affiliation:", 250, $ypos, $baseboldmidfontoptions);
  $p->fit_textline($Work3Nature, 370, $ypos, $basefontoptions);

  $ypos += 15;

  my $Work3Addr = $rProviderCreds->{"Work3Addr"};
  $p->fit_textline("Mailing Address:", 37, $ypos, $baseboldmidfontoptions);
  $p->fit_textline($Work3Addr, 120, $ypos, $basefontoptions);

  $ypos += 15;

  my $Work3City = $rProviderCreds->{"Work3City"};
  $p->fit_textline("City:",  37, $ypos, $baseboldfontoptions);
  $p->fit_textline($Work3City,   70, $ypos, $basefontoptions);

  my $Work3ST = $rProviderCreds->{"Work3ST"};
  $p->fit_textline("State:",  150, $ypos, $baseboldfontoptions);
  $p->fit_textline($Work3ST,   180, $ypos, $basefontoptions);


  my $Work3Zip = $rProviderCreds->{"Work3Zip"};
  $p->fit_textline("ZIP:",  250, $ypos, $baseboldfontoptions);
  $p->fit_textline($Work3Zip,   280, $ypos, $basefontoptions); 


  my $Work3Ph = $rProviderCreds->{"Work3Ph"};
  $p->fit_textline("Phone:",  370, $ypos, $baseboldfontoptions);
  $p->fit_textline($Work3Ph,   410, $ypos, $basefontoptions);
  $ypos += 15;


  $p->fit_textline("Dates of Affiliation:", 37, $ypos, $baseboldmidfontoptions);

  my $Work3Start = $rProviderCreds->{"Work3Start"};
  $p->fit_textline("From: ", 200, $ypos, $baseboldfontoptions);
  $p->fit_textline($Work3Start, 230, $ypos, $basefontoptions);


  my $Work3End = $rProviderCreds->{"Work3End"};
  $p->fit_textline("To: ", 300, $ypos, $baseboldfontoptions);
  $p->fit_textline($Work3End, 330, $ypos, $basefontoptions);

  $ypos += 15;

  my $Work3Reason = $rProviderCreds->{"Work3Reason"};
  $p->fit_textline("Reason for Discontinuance:", 37, $ypos, $baseboldfontoptions);
  $p->fit_textline($Work3Reason, 170, $ypos, $basefontoptions);  

  $ypos += 25;
  $p->fit_textline("US Military/Public Health Service", 37, $ypos, $baseboldmidfontoptions);
  $p->fit_textline("(List all medical and surgical locations and dates)", 210, $ypos, $basemidfontoptions);
  $ypos += 15;

  $p->fit_textline("Dates:", 37, $ypos, $baseboldmidfontoptions);

  my $MilPH1Start = $rProviderCreds->{"MilPH1Start"};
  $p->fit_textline("From: ", 200, $ypos, $baseboldfontoptions);
  $p->fit_textline($MilPH1Start, 230, $ypos, $basefontoptions);


  my $MilPH1End = $rProviderCreds->{"MilPH1End"};
  $p->fit_textline("To: ", 300, $ypos, $baseboldfontoptions);
  $p->fit_textline($MilPH1End, 330, $ypos, $basefontoptions);
  $ypos += 15;


  my $MilPH1Loc = $rProviderCreds->{"MilPH1Loc"};
  $p->fit_textline("Location: ", 37, $ypos, $baseboldfontoptions);
  $p->fit_textline($MilPH1Loc, 100, $ypos, $basefontoptions);


  my $MilPH1Branch = $rProviderCreds->{"MilPH1Branch"};
  $p->fit_textline("Branch: ", 300, $ypos, $baseboldfontoptions);
  $p->fit_textline($MilPH1Branch, 360, $ypos, $basefontoptions);



  $ypos += 20;

  $p->fit_textline("Dates:", 37, $ypos, $baseboldmidfontoptions);

  my $MilPH2Start = $rProviderCreds->{"MilPH2Start"};
  $p->fit_textline("From: ", 200, $ypos, $baseboldfontoptions);
  $p->fit_textline($MilPH2Start, 230, $ypos, $basefontoptions);


  my $MilPH2End = $rProviderCreds->{"MilPH2End"};
  $p->fit_textline("To: ", 300, $ypos, $baseboldfontoptions);
  $p->fit_textline($MilPH2End, 330, $ypos, $basefontoptions);
  $ypos += 15;


  my $MilPH2Loc = $rProviderCreds->{"MilPH2Loc"};
  $p->fit_textline("Location: ", 37, $ypos, $baseboldfontoptions);
  $p->fit_textline($MilPH2Loc, 100, $ypos, $basefontoptions);


  my $MilPH2Branch = $rProviderCreds->{"MilPH2Branch"};
  $p->fit_textline("Branch: ", 300, $ypos, $baseboldfontoptions);
  $p->fit_textline($MilPH2Branch, 360, $ypos, $basefontoptions);


  main->createFooter($p);


  # Page 6
  $ypos = $margintop;
  $p->begin_page_ext($pagewidth, $pageheight, "topdown");
  $p->fit_textline("SECTION 9: PROFESSIONAL LICENSE:", 37, $ypos, $baseboldlargefontoptions_u);
  my $h_address = 3 * $fontsizexxlarge;
  $ypos += $h_address;
  my $w_address = $pagewidth - 10;
  my $x_address = $pagewidth / 2 - $w_address / 2;
  $tf = $p->create_textflow('List all pending, current, and past professional licenses, registrations, and certifications to practice in your field. Include states where you have ever applied to practice. Examples of "type" of license are MD, DO, DDS, PA, DC, CRNA, MSW, etc.', $baselargefontoptions . " leading=110% alignment=justify lastalignment=justify");
  $p->fit_textflow($tf, 37, $ypos, $x_address+$w_address, $ypos - $h_address, "verticalalign=center");
  $ypos += 15;

  my $License1ST = $rProviderCreds->{"License1ST"};
  my $License1STVal = DBA->selxref($form, 'xState', 'ID', $License1ST, 'Descr');
  $p->fit_textline("State: ", 37, $ypos, $baseboldfontoptions);
  $p->fit_textline($License1STVal, 80, $ypos, $basefontoptions);

  my $License1Type = $rProviderCreds->{"License1Type"};
  $p->fit_textline("Type: ", 150, $ypos, $baseboldfontoptions);
  $p->fit_textline($License1Type, 180, $ypos, $basefontoptions);

  my $License1Num = $rProviderCreds->{"License1Num"};
  $p->fit_textline("Number: ", 250, $ypos, $baseboldfontoptions);
  $p->fit_textline($License1Num, 300, $ypos, $basefontoptions);
  $ypos += 15;

  my $License1Start = $rProviderCreds->{"License1Start"};
  $p->fit_textline("Original Date of Issue: ", 37, $ypos, $baseboldfontoptions);
  $p->fit_textline($License1Start, 170, $ypos, $basefontoptions);


  my $License1Expire = $rProviderCreds->{"License1Expire"};
  $p->fit_textline("Expiration Date: ", 250, $ypos, $baseboldfontoptions);
  $p->fit_textline($License1Expire, 350, $ypos, $basefontoptions);




  $ypos += 25;
  $p->fit_textline("License 2 Information: ", 37, $ypos, $baseboldfontoptions);
  $ypos += 15;

  my $License2ST = $rProviderCreds->{"License2ST"};
  my $License2STVal = DBA->selxref($form, 'xState', 'ID', $License2ST, 'Descr');
  $p->fit_textline("State: ", 37, $ypos, $baseboldfontoptions);
  $p->fit_textline($License2STVal, 80, $ypos, $basefontoptions);

  my $License2Type = $rProviderCreds->{"License2Type"};
  $p->fit_textline("Type: ", 150, $ypos, $baseboldfontoptions);
  $p->fit_textline($License2Type, 180, $ypos, $basefontoptions);

  my $License2Num = $rProviderCreds->{"License2Num"};
  $p->fit_textline("Number: ", 250, $ypos, $baseboldfontoptions);
  $p->fit_textline($License2Num, 300, $ypos, $basefontoptions);
  $ypos += 15;

  my $License2Start = $rProviderCreds->{"License2Start"};
  $p->fit_textline("Original Date of Issue: ", 37, $ypos, $baseboldfontoptions);
  $p->fit_textline($License2Start, 170, $ypos, $basefontoptions);


  my $License2Expire = $rProviderCreds->{"License2Expire"};
  $p->fit_textline("Expiration Date: ", 250, $ypos, $baseboldfontoptions);
  $p->fit_textline($License2Expire, 350, $ypos, $basefontoptions);



  $ypos += 25;
  $p->fit_textline("License 3 Information: ", 37, $ypos, $baseboldfontoptions);
  $ypos += 15;

  my $License3ST = $rProviderCreds->{"License3ST"};
  my $License3STVal = DBA->selxref($form, 'xState', 'ID', $License3ST, 'Descr');
  $p->fit_textline("State: ", 37, $ypos, $baseboldfontoptions);
  $p->fit_textline($License3STVal, 80, $ypos, $basefontoptions);

  my $License3Type = $rProviderCreds->{"License3Type"};
  $p->fit_textline("Type: ", 150, $ypos, $baseboldfontoptions);
  $p->fit_textline($License3Type, 180, $ypos, $basefontoptions);

  my $License3Num = $rProviderCreds->{"License3Num"};
  $p->fit_textline("Number: ", 250, $ypos, $baseboldfontoptions);
  $p->fit_textline($License3Num, 300, $ypos, $basefontoptions);
  $ypos += 15;

  my $License3Start = $rProviderCreds->{"License3Start"};
  $p->fit_textline("Original Date of Issue: ", 37, $ypos, $baseboldfontoptions);
  $p->fit_textline($License3Start, 170, $ypos, $basefontoptions);


  my $License3Expire = $rProviderCreds->{"License3Expire"};
  $p->fit_textline("Expiration Date: ", 250, $ypos, $baseboldfontoptions);
  $p->fit_textline($License3Expire, 350, $ypos, $basefontoptions);

  $ypos += 25;

  my $USMLEECFMG = $rProviderCreds->{"USMLEECFMG"};
  $p->fit_textline("USMLE/ECFMG Number: ", 37, $ypos, $baseboldfontoptions);
  $p->fit_textline($USMLEECFMG, 150, $ypos, $basefontoptions);


  my $USMLEECFMGDate = $rProviderCreds->{"USMLEECFMGDate"};
  $p->fit_textline("Certification Date: ", 250, $ypos, $baseboldfontoptions);
  $p->fit_textline($USMLEECFMGDate, 350, $ypos, $basefontoptions);


  $ypos += 30;
  $p->fit_textline("SECTION 10: CERTIFICATIONS AND REGISTRATIONS:", 37, $ypos, $baseboldlargefontoptions_u);
  $ypos += 15;
  $p->fit_textline("List all other current certifications and registrations: ", 37, $ypos, $basemidfontoptions);
  $ypos += 15;
  $p->fit_textline("(DEA=Federal Drug Enforcement Administration; BNDD=the Oklahoma CDS; CDS=Controlled Dangerous Substances) ", 37, $ypos, $basemidfontoptions);

  my $DEA1ST = $rProviderCreds->{"DEA1ST"};
  my $Type = "DEA";
  my $DEA1Num = $rProviderCreds->{"DEA1Num"};
  my $DEA1Start = $rProviderCreds->{"DEA1Start"};
  my $DEA1Expire = $rProviderCreds->{"DEA1Expire"};
  main->printStateTypeNumberAndDates($p, $DEA1ST, $Type, $DEA1Num, $DEA1Start, $DEA1Expire);
  $ypos += 10;

  $p->fit_textline("CERTIFICATIONS AND REGISTRATIONS 2: ", 37, $ypos, $baseboldfontoptions);

  my $DEA2ST = $rProviderCreds->{"DEA2ST"};
  my $Type = "DEA";
  my $DEA2Num = $rProviderCreds->{"DEA2Num"};
  my $DEA2Start = $rProviderCreds->{"DEA2Start"};
  my $DEA2Expire = $rProviderCreds->{"DEA2Expire"};
  main->printStateTypeNumberAndDates($p, $DEA2ST, $Type, $DEA2Num, $DEA2Start, $DEA2Expire);
  $ypos += 10;


  $p->fit_textline("CERTIFICATIONS AND REGISTRATIONS 3: ", 37, $ypos, $baseboldfontoptions);
  
  my $BNDDST = $rProviderCreds->{"BNDDST"};
  my $Type = "BNDD";
  my $BNDDNum = $rProviderCreds->{"BNDDNum"};
  my $BNDDStart = $rProviderCreds->{"BNDDStart"};
  my $BNDDExpire = $rProviderCreds->{"BNDDExpire"};
  main->printStateTypeNumberAndDates($p, $BNDDST, $Type, $BNDDNum, $BNDDStart, $BNDDExpire);
  $ypos += 10;


  $p->fit_textline("CERTIFICATIONS AND REGISTRATIONS 4: ", 37, $ypos, $baseboldfontoptions);
  
  my $CDSST = $rProviderCreds->{"CDSST"};
  my $Type = "CDS";
  my $CDSNum = $rProviderCreds->{"CDSNum"};
  my $CDSStart = $rProviderCreds->{"CDSStart"};
  my $CDSExpire = $rProviderCreds->{"CDSExpire"};
  main->printStateTypeNumberAndDates($p, $CDSST, $Type, $CDSNum, $CDSStart, $CDSExpire);
  $ypos += 10;

  $p->fit_textline("BOARD CERTIFICATION: ", 37, $ypos, $baseboldmidfontoptions);
  $ypos += 15;

  my $Board1Cert = $rProviderCreds->{"Board1Cert"};
  $p->fit_textline("Are you Board Certified: ", 37, $ypos, $baseboldfontoptions);
  $p->fit_textline($YesNoArr{$Board1Cert}, 150, $ypos, $basefontoptions);

  #Board 1 
  my $Board1 = $rProviderCreds->{"Board1"};
  my $Board1Start = $rProviderCreds->{"Board1Start"};
  my $Board1Renewed = $rProviderCreds->{"Board1Renewed"};
  my $Board1Expire = $rProviderCreds->{"Board1Expire"};

  main->printBoardCerts($p, $Board1, $Board1Start, $Board1Renewed, $Board1Expire);

  $p->fit_textline("Have you ever been examined by any specialty board but failed to pass? If yes, provide details: ", 37, $ypos, $baseboldfontoptions);
  

  main->createFooter($p);


  # Page 8
  $ypos = $margintop;
  $p->begin_page_ext($pagewidth, $pageheight, "topdown");


  $p->fit_textline("SUBSPECIALTY CERTIFICATION AND ADDED QUALIFICATIONS: ", 37, $ypos, $baseboldmidfontoptions);
  $ypos += 15;

  #Board 2 

  $p->fit_textline("Subspecialty or Added Qualification 1: ", 37, $ypos, $baseboldfontoptions);
  $p->fit_textline($rProviderCreds->{"Board2Specialty"}, 210, $ypos, $basefontoptions);

  my $Board2 = $rProviderCreds->{"Board2"};
  my $Board2Start = $rProviderCreds->{"Board2Start"};
  my $Board2Renewed = $rProviderCreds->{"Board2Renewed"};
  my $Board2Expire = $rProviderCreds->{"Board2Expire"};

  main->printBoardCerts($p, $Board2, $Board2Start, $Board2Renewed, $Board2Expire);

  #Board 3 

  $p->fit_textline("Subspecialty or Added Qualification 2: ", 37, $ypos, $baseboldfontoptions);
  $p->fit_textline($rProviderCreds->{"Board3Specialty"}, 210, $ypos, $basefontoptions);

  my $Board3 = $rProviderCreds->{"Board3"};
  my $Board3Start = $rProviderCreds->{"Board3Start"};
  my $Board3Renewed = $rProviderCreds->{"Board3Renewed"};
  my $Board3Expire = $rProviderCreds->{"Board3Expire"};

  main->printBoardCerts($p, $Board3, $Board3Start, $Board3Renewed, $Board3Expire);


  $p->fit_textline("BOARD QUALIFICATIONS: ", 37, $ypos, $baseboldmidfontoptions);
  $ypos += 15;  

  $p->fit_textline("If you are not certified, are you qualified to sit for the exam in a primary or subspecialty board or added qualification: ", 37, $ypos, $baseboldfontoptions);
  main->printYesNo($p, $rProviderCreds->{"BoardQEligible"}, 550);
  $ypos += 15;  

  $p->fit_textline("Are you planning to take the exam: ", 37, $ypos, $baseboldfontoptions);
  main->printYesNo($p, $rProviderCreds->{"BoardQPlan"}, 230);
  $ypos += 15;  

  $p->fit_textline("Are you scheduled to take the exam? If yes, attach confirmation letter: ", 37, $ypos, $baseboldfontoptions);
  main->printYesNo($p, $rProviderCreds->{"BoardQSched"}, 350);

  $ypos += 15;  

  $p->fit_textline("Date Scheduled: ", 37, $ypos, $baseboldmidfontoptions);
  $ypos += 15;

  $p->fit_textline("Oral: ", 37, $ypos, $baseboldfontoptions);
  $p->fit_textline($rProviderCreds->{"BoardQOral"}, 80, $ypos, $basefontoptions);

  $p->fit_textline("Written: ", 150, $ypos, $baseboldfontoptions);
  $p->fit_textline($rProviderCreds->{"BoardQWritten"}, 200, $ypos, $basefontoptions);


  $p->fit_textline("Other: ", 270, $ypos, $baseboldfontoptions);
  $p->fit_textline($rProviderCreds->{"BoardQOther"}, 320, $ypos, $basefontoptions);



  #Board 4 
  $ypos += 15;

  $p->fit_textline("Subspecialty or Added Qualification 3: ", 37, $ypos, $baseboldfontoptions);
  $p->fit_textline($rProviderCreds->{"BoardQSpecialty"}, 210, $ypos, $basefontoptions);

  my $BoardQ = $rProviderCreds->{"BoardQ"};
  my $BoardQStart = $rProviderCreds->{"BoardQStart"};
  my $BoardQRenewed = $rProviderCreds->{"BoardQRenewed"};
  my $BoardQExpire = $rProviderCreds->{"BoardQExpire"};

  main->printBoardCerts($p, $BoardQ, $BoardQStart, $BoardQRenewed, $BoardQExpire);



  # Classifications
  $ypos += 10;

  $p->fit_textline("Classifications: ", 37, $ypos, $baseboldmidfontoptions);
  $ypos += 20;

  main->printClassifications($p, "Are you certified in CPR:", $rProviderCreds->{"CPR"}, $rProviderCreds->{"CPRExpire"}, 210);
  main->printClassifications($p, "Basic Life Support (BLS):", $rProviderCreds->{"BLS"}, $rProviderCreds->{"BLSExpire"}, 210);
  main->printClassifications($p, "Advanced Cardiac Life Support (ACLS):", $rProviderCreds->{"ACLS"}, $rProviderCreds->{"ACLSExpire"}, 210);

  main->printClassifications($p, "Health Care Provider (CoreC):", $rProviderCreds->{"CoreC"}, $rProviderCreds->{"CoreCExpire"}, 210);
  main->printClassifications($p, "Advanced Trauma Life Support (ATLS):", $rProviderCreds->{"ATLS"}, $rProviderCreds->{"ATLSExpire"}, 210);
  main->printClassifications($p, "Neonatal Advanced Life Support (NALS):", $rProviderCreds->{"NALS"}, $rProviderCreds->{"NALSExpire"}, 210);
  main->printClassifications($p, "Pediatric Advanced Life Support (PALS):", $rProviderCreds->{"PALS"}, $rProviderCreds->{"PALSExpire"}, 210);


  $ypos += 15;
  $p->fit_textline("Other", 37, $ypos, $baseboldfontoptions);
  $p->fit_textline($rProviderCreds->{"OtherCertSpecify"}, 80, $ypos, $basefontoptions);

  $p->fit_textline("Expires:", 150, $ypos, $baseboldfontoptions);
  $p->fit_textline($rProviderCreds->{"OtherCertExpire"}, 330, $ypos, $basefontoptions);

  main->createFooter($p);

  # Start Page 9 

  $p->begin_page_ext($pagewidth, $pageheight, "topdown");


  # SECTION 11: OFFICE INFORMATION
  $ypos = $margintop;

  $p->fit_textline("SECTION 11: OFFICE INFORMATION:", 37, $ypos, $baseboldlargefontoptions_u);
  $ypos += 20;
  $p->fit_textline("Primary Office:", 37, $ypos, $baseboldmidfontoptions);

  main->printOfficeInfo($p,1, $rProviderCreds);


  main->createFooter($p);



  # Start Page 10 

  $p->begin_page_ext($pagewidth, $pageheight, "topdown");

  # SECTION 11: OFFICE INFORMATION
  $ypos = $margintop;

  $p->fit_textline("SECTION 11: OFFICE INFORMATION:", 37, $ypos, $baseboldlargefontoptions_u);
  $ypos += 20;
  $p->fit_textline("Secondary Office:", 37, $ypos, $baseboldmidfontoptions);

  main->printOfficeInfo($p,2, $rProviderCreds);
  
  main->createFooter($p);



  # Start Page 11 

  $p->begin_page_ext($pagewidth, $pageheight, "topdown");

  # SECTION 12: COPIES OF REQUIRED DOCUMENT
  $ypos = $margintop;

  $p->fit_textline("SECTION 12: COPIES OF REQUIRED DOCUMENT:", 37, $ypos, $baseboldlargefontoptions_u);
  $ypos += 20;
  $p->fit_textline("Please include a copy of the following with this application. Practitioner should check off needed items that are being attached to this application:", 37, $ypos, $basefontoptions);
  $ypos += 15;
  $p->fit_textline("Attached Items:", 37, $ypos, $baseboldfontoptions);

  $ypos += 15;

  $p->fit_textline("Oklahoma Bureau of Narcotics and Dangerous Drugs Registration (BNDD):", 37, $ypos, $baseboldfontoptions);
  $p->fit_textline($YesNoArr{$rProviderCreds->{"BNDDAttachment"}}, 380, $ypos, $basefontoptions);



  $p->fit_textline("Curriculum Vitae:", 410, $ypos, $baseboldfontoptions);
  $p->fit_textline($YesNoArr{$rProviderCreds->{"VitaeAttachment"}}, 490, $ypos, $basefontoptions);


  $ypos += 15;

  $p->fit_textline("Current Federal DEA Registration Certificate:", 37, $ypos, $baseboldfontoptions);
  $p->fit_textline($YesNoArr{$rProviderCreds->{"DEAAttachment"}}, 270, $ypos, $basefontoptions);



  $p->fit_textline("Tax Identification Information Form W-9:", 300, $ypos, $baseboldfontoptions);
  $p->fit_textline($YesNoArr{$rProviderCreds->{"W9Attachment"}}, 480, $ypos, $basefontoptions);


  $ypos += 15;

  $p->fit_textline("Emergency Care Training Certificates (CPR, etc., if certified):", 37, $ypos, $baseboldfontoptions);
  $p->fit_textline($YesNoArr{$rProviderCreds->{"CPRAttachment"}}, 300, $ypos, $basefontoptions);

  $p->fit_textline("Photo Identification:", 340, $ypos, $baseboldfontoptions);
  $p->fit_textline($YesNoArr{$rProviderCreds->{"PhotoAttachment"}}, 430, $ypos, $basefontoptions);

  $ypos += 20;
  $p->fit_textline("SECTION 13: ATTESTATION:", 37, $ypos, $baseboldlargefontoptions_u);
  $ypos += 15;
  
  $h_address = 3 * $fontsizexxlarge;
  $ypos += $h_address;
  $w_address = $pagewidth - 10;
  $x_address = $pagewidth / 2 - $w_address / 2;
  $tf = $p->create_textflow("All information and documentation contained in this application is true, correct and complete to my best knowledge and belief. I further acknowledge that any material misstatements in or omissions from this application may constitute cause for denial of my application for staff membership, privileges, or participation", $baselargefontoptions . " leading=110% alignment=justify lastalignment=justify");
  $p->fit_textflow($tf, 37, $ypos, $x_address+$w_address, $ypos - $h_address, "verticalalign=center");
  $ypos += 15;


  $p->fit_textline("Name (printed):", 37, $ypos, $baseboldfontoptions);
  $p->fit_textline($rProviderCreds->{"FullName"}, 130, $ypos, $basefontoptions);

  $p->fit_textline("Signature Date:", 300, $ypos, $baseboldfontoptions);
  $p->fit_textline($rProviderCreds->{"AttestationDate"}, 380, $ypos, $basefontoptions);

  $ypos += 15;
  $p->fit_textline("NOTE:", 37, $ypos, $baseboldfontoptions);
  $p->fit_textline("Practitioners are reminded that each organization will require submission of additional information", 80, $ypos, $basefontoptions);


  $ypos += 20;
  $p->fit_textline("SECTION 14: ADDITIONAL INFORMATION:", 37, $ypos, $baseboldlargefontoptions_u);
  $ypos += 15;
  
  $h_address = 3 * $fontsizexxlarge;
  $ypos += $h_address;
  $w_address = $pagewidth - 10;
  $x_address = $pagewidth / 2 - $w_address / 2;
  $tf = $p->create_textflow("This page is furnished for your convenience in completing questions or providing additional information. Please make as many copies of this page as you require to fully answer all questions", $baselargefontoptions . " leading=110% alignment=justify lastalignment=justify");
  $p->fit_textflow($tf, 37, $ypos, $x_address+$w_address, $ypos - $h_address, "verticalalign=center");
  $ypos += 15;
  $p->fit_textline("As appropriate, note section number and question number that you are addressing:", 37, $ypos, $baselargefontoptions);
  $ypos += 15;


  $h_address = 4 * $fontsizexxlarge;
  $ypos += $h_address;
  $w_address = $pagewidth - 10;
  $x_address = $pagewidth / 2 - $w_address / 2;
  $tf = $p->create_textflow($rProviderCreds->{"AdditionalInfo1"}, $baselargefontoptions . " leading=110% alignment=justify lastalignment=justify");
  $p->fit_textflow($tf, 37, $ypos, $x_address+$w_address, $ypos - $h_address, "verticalalign=center");
  $ypos += 15;


  $h_address = 4 * $fontsizexxlarge;
  $ypos += $h_address;
  $w_address = $pagewidth - 10;
  $x_address = $pagewidth / 2 - $w_address / 2;
  $tf = $p->create_textflow($rProviderCreds->{"AdditionalInfo2"}, $baselargefontoptions . " leading=110% alignment=justify lastalignment=justify");
  $p->fit_textflow($tf, 37, $ypos, $x_address+$w_address, $ypos - $h_address, "verticalalign=center");
  $ypos += 15;





  main->createFooter($p);
}
sub printOfficeInfo {
  my ($self, $p, $num,$rProviderCreds) = @_;

  $ypos += 20;
  my $Office = $rProviderCreds->{"Office$num"};
  $p->fit_textline("Group Name:", 37, $ypos, $baseboldfontoptions);
  $p->fit_textline($Office, 100, $ypos, $basefontoptions);

  $p->fit_textline("Name As It Appears On Your W-9 (if applicable):", 250, $ypos, $baseboldfontoptions);
  $p->fit_textline($rProviderCreds->{"Office${num}W9ID"}, 460, $ypos, $basefontoptions);
  $ypos += 15;
  
  $p->fit_textline("Business Owned By:", 37, $ypos, $baseboldfontoptions);
  $p->fit_textline($rProviderCreds->{"Office${num}Owner"}, 130, $ypos, $basefontoptions);



  my $OfficePracticeTypeOther = $rProviderCreds->{"Office${num}PracticeTypeOther"};
  my $OfficePracticeType = $rProviderCreds->{"Office${num}PracticeType"};

  my %OfficePracticeTypeArr = (
      "P", "Partnership",
      "S", "Solo",
      "G", "Single-Specialty Group",
      "M", "Multi-Specialty Group ",
      "O", $OfficePracticeTypeOther,
    );

  $p->fit_textline("Type of Practice:", 250, $ypos, $baseboldfontoptions);
  $p->fit_textline($OfficePracticeTypeArr{$OfficePracticeType}, 330, $ypos, $basefontoptions);

  $ypos += 15;


  $p->fit_textline("Office Manager:", 37, $ypos, $baseboldfontoptions);
  $p->fit_textline($rProviderCreds->{"Office${num}Manager"}, 130, $ypos, $basefontoptions);



  $p->fit_textline("Nurse Coordinator:", 250, $ypos, $baseboldfontoptions);
  $p->fit_textline($rProviderCreds->{"Office${num}Nurse"}, 340, $ypos, $basefontoptions);
  
  $ypos += 15;


  $p->fit_textline("Group Medicare Number:", 37, $ypos, $baseboldfontoptions);
  $p->fit_textline($rProviderCreds->{"Office${num}MedicarePIN"}, 150, $ypos, $basefontoptions);



  $p->fit_textline("Group Medicaid Number:", 250, $ypos, $baseboldfontoptions);
  $p->fit_textline($rProviderCreds->{"Office${num}MedicaidPIN"}, 370, $ypos, $basefontoptions);


  
  $ypos += 15;


  $p->fit_textline("IRS Tax ID Number:", 37, $ypos, $baseboldfontoptions);
  $p->fit_textline($rProviderCreds->{"Office${num}TaxID"}, 130, $ypos, $basefontoptions);



  $p->fit_textline("Does this office have lab service:", 250, $ypos, $baseboldfontoptions);
  $p->fit_textline($YesNoArr{$rProviderCreds->{"Office${num}Lab"}}, 400, $ypos, $basefontoptions);


  $p->fit_textline("Reference lab:", 430, $ypos, $baseboldfontoptions);
  $p->fit_textline($YesNoArr{$rProviderCreds->{"Office${num}RefLab"}}, 500, $ypos, $basefontoptions);

  $ypos += 15;


  $p->fit_textline("On Site:", 37, $ypos, $baseboldfontoptions);
  $p->fit_textline($YesNoArr{$rProviderCreds->{"Office${num}OnSiteLab"}}, 100, $ypos, $basefontoptions);



  $p->fit_textline("CLIA ID #:", 140, $ypos, $baseboldfontoptions);
  $p->fit_textline($rProviderCreds->{"Office${num}CLIANum"}, 190, $ypos, $basefontoptions);


  $p->fit_textline("CLIA Waiver #:", 320, $ypos, $baseboldfontoptions);
  $p->fit_textline($rProviderCreds->{"Office${num}CLIAWaiverNum"}, 400, $ypos, $basefontoptions);
  $ypos += 20;

  $p->fit_textline("Does your office have the following:", 37, $ypos, $baseboldfontoptions);

  $ypos += 20;


  $p->fit_textline("Radiology:", 37, $ypos, $baseboldfontoptions);
  $p->fit_textline($YesNoArr{$rProviderCreds->{"Office${num}Rad"}}, 90, $ypos, $basefontoptions);


  $p->fit_textline("EKG:", 120, $ypos, $baseboldfontoptions);
  $p->fit_textline($YesNoArr{$rProviderCreds->{"Office${num}EKG"}}, 150, $ypos, $basefontoptions);


  $p->fit_textline("Audiology:", 180, $ypos, $baseboldfontoptions);
  $p->fit_textline($YesNoArr{$rProviderCreds->{"Office${num}Aud"}}, 230, $ypos, $basefontoptions);


  $p->fit_textline("Treadmill:", 260, $ypos, $baseboldfontoptions);
  $p->fit_textline($YesNoArr{$rProviderCreds->{"Office${num}Treadmill"}}, 310, $ypos, $basefontoptions);


  $p->fit_textline("Sigmoidoscopy:", 340, $ypos, $baseboldfontoptions);
  $p->fit_textline($YesNoArr{$rProviderCreds->{"Office${num}Sigmoid"}}, 420, $ypos, $basefontoptions);

  $ypos += 15;



  $p->fit_textline("Wheelchair/handicapped access?:", 37, $ypos, $baseboldfontoptions);
  $p->fit_textline($YesNoArr{$rProviderCreds->{"Office${num}Access"}}, 185, $ypos, $basefontoptions);



  $p->fit_textline("Other services for the disabled?:", 210, $ypos, $baseboldfontoptions);
  $p->fit_textline($YesNoArr{$rProviderCreds->{"Office${num}OtherDisabilitySvcs"}}, 360, $ypos, $basefontoptions);


  $ypos += 15;


  $p->fit_textline("If yes, please list:", 37, $ypos, $baseboldfontoptions);
  $p->fit_textline($rProviderCreds->{"Office${num}OtherDisabilitySvcsSpecify"}, 120, $ypos, $basefontoptions);

  $ypos += 15;



  $p->fit_textline("Other:", 37, $ypos, $baseboldfontoptions);
  $p->fit_textline($YesNoArr{$rProviderCreds->{"Office${num}OtherSvcs"}}, 80, $ypos, $basefontoptions);



  $p->fit_textline("Other Specify:", 110, $ypos, $baseboldfontoptions);
  $p->fit_textline($YesNoArr{$rProviderCreds->{"Office${num}OtherSvcsSpecify"}}, 200, $ypos, $basefontoptions);


  $ypos += 20;



  $p->fit_textline("List all independent licensed non-physicians working in this office:", 37, $ypos, $baseboldfontoptions);
  main->nameTypeLicence($p, $rProviderCreds->{"Office${num}Prov1"}, $rProviderCreds->{"Office${num}Prov1Type"}, $rProviderCreds->{"Office${num}Prov1LicNum"});
  main->nameTypeLicence($p, $rProviderCreds->{"Office${num}Prov2"}, $rProviderCreds->{"Office${num}Prov2Type"}, $rProviderCreds->{"Office${num}Prov2LicNum"});
  main->nameTypeLicence($p, $rProviderCreds->{"Office${num}Prov3"}, $rProviderCreds->{"Office${num}Prov3Type"}, $rProviderCreds->{"Office${num}Prov3LicNum"});
  $ypos += 15;

  $p->fit_textline("Fluent Languages:", 37, $ypos, $baseboldfontoptions);
  $ypos += 15;

  $p->fit_textline("You:", 37, $ypos, $baseboldfontoptions);
  $p->fit_textline($rProviderCreds->{"Office${num}Language"}, 70, $ypos, $basefontoptions);


  $p->fit_textline("Your Staff:", 190, $ypos, $baseboldfontoptions);
  $p->fit_textline($rProviderCreds->{"Office${num}LanguageStaff"}, 250, $ypos, $basefontoptions);


  $p->fit_textline("Other Resources:", 370, $ypos, $baseboldfontoptions);
  $p->fit_textline($rProviderCreds->{"Office${num}Resources"}, 440, $ypos, $basefontoptions);

  $ypos += 15;

  $p->fit_textline("Office Hours:", 37, $ypos, $baseboldfontoptions);
  main->printOfficeHours($p, "Monday", $rProviderCreds->{"Office${num}MonStart"}, $rProviderCreds->{"Office${num}MonEnd"});
  main->printOfficeHours($p, "Tuesday", $rProviderCreds->{"Office${num}TueStart"}, $rProviderCreds->{"Office${num}TueEnd"});
  main->printOfficeHours($p, "Wednesday", $rProviderCreds->{"Office${num}WedsStart"}, $rProviderCreds->{"Office${num}WedsEnd"});
  main->printOfficeHours($p, "Thursday", $rProviderCreds->{"Office${num}ThurStart"}, $rProviderCreds->{"Office${num}ThurEnd"});
  main->printOfficeHours($p, "Friday", $rProviderCreds->{"Office${num}FriStart"}, $rProviderCreds->{"Office${num}FriEnd"});
  main->printOfficeHours($p, "Saturday", $rProviderCreds->{"Office${num}SatStart"}, $rProviderCreds->{"Office${num}SatEnd"});
  main->printOfficeHours($p, "Sunday", $rProviderCreds->{"Office${num}SunStart"}, $rProviderCreds->{"Office${num}SunEnd"});

  $ypos += 25;
  $p->fit_textline("List name, specialty, and phone number of physicians covering your practice in your absence. Attach an additional sheet if necessary:", 37, $ypos, $baseboldfontoptions);
  $ypos += 15;
  $p->fit_textline("Note: These practitioners must be affiliated with the organization to which you are applying:", 37, $ypos, $baseboldfontoptions);

  my $OfficeDr1Specialty = DBA->getxrefWithDef($form,'xOccupationSnomed',$rProviderCreds->{"Office${num}Dr1Specialty"},'Description');
  my $OfficeDr2Specialty = DBA->getxrefWithDef($form,'xOccupationSnomed',$rProviderCreds->{"Office${num}Dr2Specialty"},'Description');
  my $OfficeDr3Specialty = DBA->getxrefWithDef($form,'xOccupationSnomed',$rProviderCreds->{"Office${num}Dr3Specialty"},'Description');

  main->printNameSpecialityTelephone($p, $rProviderCreds->{"Office${num}Dr1"}, $OfficeDr1Specialty, $rProviderCreds->{"Office${num}Dr1Ph"});
  main->printNameSpecialityTelephone($p, $rProviderCreds->{"Office${num}Dr2"}, $OfficeDr2Specialty, $rProviderCreds->{"Office${num}Dr2Ph"});
  main->printNameSpecialityTelephone($p, $rProviderCreds->{"Office${num}Dr3"}, $OfficeDr3Specialty, $rProviderCreds->{"Office${num}Dr3Ph"});
  $ypos += 25;

  $p->fit_textline("Do you or your business own, operate, manage or participate in any medical enterprise or business?:", 37, $ypos, $baseboldfontoptions);
  
  $ypos += 15;
  
  $p->fit_textline("If yes, explain on a separate attachment.:", 37, $ypos, $basefontoptions);
  
  $ypos += 15;
  $p->fit_textline($YesNoArr{$rProviderCreds->{"Office${num}Chain"}}, 70, $ypos, $basefontoptions);



}


sub printNameSpecialityTelephone {
  my ($self, $p, $Name, $Specialty, $Telephone) = @_;
  $ypos += 15;


  $p->fit_textline("Name:", 37, $ypos, $baseboldfontoptions);
  $p->fit_textline($Name, 70, $ypos, $basefontoptions);


  $p->fit_textline("Specialty:", 220, $ypos, $baseboldfontoptions);
  $p->fit_textline($Specialty, 280, $ypos, $basefontoptions);


  $p->fit_textline("Telephone:", 400, $ypos, $baseboldfontoptions);
  $p->fit_textline($Telephone, 470, $ypos, $basefontoptions);
}

sub printOfficeHours {
  my ($self, $p, $day, $start, $end) = @_;

  $ypos += 15;
  $p->fit_textline($day, 37, $ypos, $baseboldfontoptions);

  $p->fit_textline("From:", 200, $ypos, $baseboldfontoptions);
  $p->fit_textline($start, 250, $ypos, $basefontoptions);

  $p->fit_textline("To:", 350, $ypos, $baseboldfontoptions);
  $p->fit_textline($end, 400, $ypos, $basefontoptions);

}

sub nameTypeLicence {
  my ($self, $p, $name, $type, $licNum) = @_;
  $ypos += 15;
  
  $p->fit_textline("Name:", 37, $ypos, $baseboldfontoptions);
  $p->fit_textline($name, 80, $ypos, $basefontoptions);
  
  $p->fit_textline("Provider Type:", 180, $ypos, $baseboldfontoptions);
  $p->fit_textline($type, 250, $ypos, $basefontoptions);

  
  $p->fit_textline("License Number:", 350, $ypos, $baseboldfontoptions);
  $p->fit_textline($licNum, 430, $ypos, $basefontoptions);

}

sub printClassifications {
  my ($self, $p, $Question, $OneOrZero, $Expires, $xpos) = @_;
  
  $ypos += 15;
  $p->fit_textline($Question, 37, $ypos, $baseboldfontoptions);
  $p->fit_textline($YesNoArr{$OneOrZero}, $xpos, $ypos, $basefontoptions);

  $p->fit_textline("Expires:", $xpos+ 40, $ypos, $baseboldfontoptions);
  $p->fit_textline($Expires, $xpos + 80, $ypos, $basefontoptions);

}

sub printYesNo {
  my ($self, $p, $OneOrZero, $xpos) = @_;
  $p->fit_textline($YesNoArr{$OneOrZero}, $xpos, $ypos, $basefontoptions);
}

sub printBoardCerts {
  my ($self, $p, $Board, $BoardStart, $BoardRenewed, $BoardExpire) = @_;

  $ypos += 15;
  $p->fit_textline("Name: ", 37, $ypos, $baseboldfontoptions);
  $p->fit_textline($Board, 70, $ypos, $basefontoptions);

  $p->fit_textline("Initially Certified: ", 200, $ypos, $baseboldfontoptions);
  $p->fit_textline($BoardStart, 300, $ypos, $basefontoptions);

  $p->fit_textline("Date Most Recently Recertified: ", 380, $ypos, $baseboldfontoptions);
  $p->fit_textline($BoardRenewed, 520, $ypos, $basefontoptions);
  $ypos += 15;

  $p->fit_textline("Date Certification Expires: ", 37, $ypos, $baseboldfontoptions);
  $p->fit_textline($BoardExpire, 180, $ypos, $basefontoptions);

  $ypos += 15;
}


sub printStateTypeNumberAndDates {
  my ($self, $p, $State, $Type, $Num, $Start, $Expire) = @_;
  $ypos += 15;

  $p->fit_textline("State: ", 37, $ypos, $baseboldfontoptions);
  $p->fit_textline($State, 80, $ypos, $basefontoptions);

  $p->fit_textline("Type: ", 150, $ypos, $baseboldfontoptions);
  $p->fit_textline($Type, 180, $ypos, $basefontoptions);

  $p->fit_textline("Number: ", 250, $ypos, $baseboldfontoptions);
  $p->fit_textline($Num, 300, $ypos, $basefontoptions);
  $ypos += 15;

  $p->fit_textline("Original Date of Issue: ", 37, $ypos, $baseboldfontoptions);
  $p->fit_textline($Start, 170, $ypos, $basefontoptions);


  $p->fit_textline("Expiration Date: ", 250, $ypos, $baseboldfontoptions);
  $p->fit_textline($Expire, 350, $ypos, $basefontoptions);

  $ypos += 15;

}
sub createHeader {
  my ($self, $p,$rProvider) = @_;
  
  my $ProviderName = qq|$rProvider->{'FName'} $rProvider->{'MName'} $rProvider->{'LName'}|;
  my $ProviderAddr = $rProvider->{'Addr1'} . ', ';
  $ProviderAddr .= $rProvider->{'Addr2'} . ', ' if ( $rProvider->{'Addr2'} );
  $ProviderAddr .= $rProvider->{'City'} . ', ' . $rProvider->{'ST'} . '  ' . $rProvider->{'Zip'};
  my $ProviderPh = 'Office: ' . $rProvider->{'WkPh'} . '  Fax: ' . $rProvider->{'Fax'};
  my $Title = "Provider Credentials";

  my $Address = qq|${ProviderName}\n${ProviderAddr}\n${ProviderPh}\n${Title}|;

  my $tf;

  $p->begin_page_ext($pagewidth, $pageheight, "topdown");
  $ypos = $margintop;


  my $h_address = 5 * $fontsizexxlarge;
  $ypos += $h_address;
  my $w_address = 200;
  my $x_address = $pagewidth / 2 - $w_address / 2;
  $tf = $p->create_textflow($Address, $baselargefontoptions . " leading=110% alignment=justify lastalignment=center");
  $p->fit_textflow($tf, $x_address, $ypos, $x_address+$w_address, $ypos - $h_address, "verticalalign=center");


  $ypos += $fontsizexxlarge;

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

sub createEmptyPage {
  my ($self, $p) = @_;

  $p->begin_page_ext($pagewidth, $pageheight, "topdown");
  $p->fit_textline("NOT FOUND", $marginleft, 50, $basefontoptions);
  $p->end_page_ext("");
}
