#!/usr/bin/perl
# This is also a new file
############################################################################
use lib '/home/okmis/mis/src/lib';
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


my $sPDMed = $dbh->prepare("select * from PDMed where PDMedID=?");
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
my $sProvider = $dbh->prepare("select * from Provider where ProvID=?");


my $pagewidth = 612;
my $pageheight = 592;

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
  $p->set_info("Title", "PDMed");

  main->printPDMed($p);

  $p->end_document("");

};



if ($@) {
  die("$0: PDFlib Exception occurred:\n$@");
}

$sPDMed->finish();
$sClient->finish();
$sProvider->finish();

myDBI->cleanup();

if ( $form->{'file'} eq '' )                # create and print pdf.
{ print qq|Location: ${filename}\n\n|; }

exit;



############################################################################
sub printPDMed {
  my ($self, $p) = @_;

  foreach my $ID ( split(' ',$IDs) )
  { 
    #warn "PrintPDMed: ID=${ID}\n";
    $sPDMed->execute($ID) || myDBI->dberror("PrintPDMed: select ClientPrAuth $ID");
    while ( my $rPDMed = $sPDMed->fetchrow_hashref )
    { 
      $sClient->execute($rPDMed->{ClientID}) || myDBI->dberror($qClient);
      my $rClient = $sClient->fetchrow_hashref;
      my $ProvID=$rClient->{ProvID};
      $sProvider->execute($ProvID) || myDBI->dberror("PrintPDMed: select Provider $ProvID");
      my $rPrimaryProvider = $sProvider->fetchrow_hashref;

      main->createPages($p, $rPDMed, $rClient, $rPrimaryProvider);
    }
  }
  if ($pagecount) {
    main->createPageCount($p);
  } else {
    main->createEmptyPage($p);
  }

}


sub createPages {
  my ($self, $p, $rPDMed, $rClient, $rPrimaryProvider) = @_;

  my $optlist;
  my $tf;
  my $h_tf;
  my $row;
  my $col;
  my $tbl;
  my $h_tbl;


  
  my $ProviderName = qq|$rPrimaryProvider->{'FName'} $rPrimaryProvider->{'LName'}|;


  # Client info...
  my $ClientName = qq|$rClient->{'FName'} $rClient->{'MName'} $rClient->{'LName'} ($rClient->{'ClientID'})|;
  my $ClientID = $rPDMed->{ClientID};
  my $PrAuthID = $rPDMed->{ID};
  ##


  #####################
  # Page variables
  my $cname = $ClientName;
  my $ssn = $rClient->{'SSN'};
  my $pname = $ProviderName;

  my %MedFreqArr = (
                    "p.c.","after meals","u.d.","as directed","ad lib","as much as needed","p.r.n.","as needed",
                    "h.s.","bedtime","a.c.","before meals","a.c. &amp; h.s.","after meals","p.c.","before meals &amp; bedtime",
                    "non. rep.","do not repeat","q. 2h","every 2 hours","q. 3 days","every 3 days","q. 3h","every 3 hours",
                    "q. 3 months","every 3 months","q. 3 weeks","every 3 weeks","q.q.h.","every 4 hours","q.d.","every day",
                    "q.p.m.","every evening","q.m.","every month","q.a.m.","every morning","e.o.d.","every other day",
                    "e.o.w.","every other week","e.w.","every week","q.i.d.", "four times a day","p.c. &amp; h.s.","p.c. &amp; h.s.",
                    "t.i.d.", "three times a day","b.i.d.","twice a day","t.w.","twice a week",
                  );




  my %RouteArr = (

                    "102" , "AN,SYMPATHETIC NBLK","101" , "AN,SURFACE","100" , "AN,INFILTRATION","099" , "MISCELLANEOUS","098" , "NONHUMAN STUDY",
                    "097" , "SURGICAL", "096" , "SUBCONJUNCTIVAL","095" , "ROUTE NOT GIVEN","094" , "SEE PHARM ACTIVITY","093" , "IM - SC",
                    "092" , "IV - SC", "091" , "IM - IV", "090" , "IM - IV - SC", "089" , "IV(INFUSION)","088" , "INTERSTITIAL", "072" , "INTRAESOPHAGEAL",
                    "071" , "NASOGASTRIC","069" , "END","068" , "CONJUNCTIVAL","067" , "INTRABRONCHIAL","066" , "SUBARACHNOID",
                    "065" , "INVITRO","061" , "INTRAPROSTATIC","060" , "INTRA-AMNIOTIC","059" , "NERVE BLOCK","058" , "THROAT",
                    "057" , "EXTRACORPOREAL","056" , "INTRA-ABDOMINAL","055" , "IONTOPHORESIS","054" , "VOCAL CORDS","053" , "SUBMUCOSAL",
                    "052" , "INTRADURAL","051" , "INTRACERVICAL","050" , "PERIDURAL","049" , "INTRATENDINOUS","048" , "INTRAVENTRICULAR",
                    "047" , "INTRADUODENAL","046" , "INTRAGASTRIC","045" , "PERIARTICULAR","043" , "INTRAPLEURAL","042" , "INTRALESIONAL",
                    "041" , "IMPLANTATION","040" , "PERIODONTAL","038" , "DENTAL","037" , "INTRA-ARTERIAL","036" , "INTRAOCULAR",
                    "035" , "INTRATRACHEAL","034" , "RETROBULBAR","033" , "AN,CNBLK INTRATHECAL","032" , "IRRIGATION","031" , "SEE DOSAGE FORM",
                    "030" , "BUCCAL","029" , "CAUDAL BLOCK","028" , "INTRAUTERINE","027" , "INTRACARDIAC","026" , "DIAGNOSTIC",
                    "025" , "INTRABURSAL","024" , "SUBLINGUAL","023" , "INTRACAVITARY","022" , "INTRASPINAL","021" , "INTRAVASCULAR",
                    "020" , "INTRATUMOR","019" , "INTRASYNOVIAL","018" , "INHALATION","017" , "URETHRAL","016" , "RECTAL",
                    "015" , "VAGINAL","014" , "NASAL","013" , "AURICULAR (OTIC)","012" , "OPHTHALMIC","011" , "TOPICAL",
                    "010" , "INTRASINAL","009" , "EPIDURAL","008" , "INTRADERMAL","007" , "INTRA-ARTICULAR","006" , "INTRATHORACIC",
                    "005" , "INTRAMUSCULAR","004" , "INTRAPERITONEAL","003" , "SUBCUTANEOUS","002" , "INTRAVENOUS","001" , "ORAL",
                    "000","N/A",  "N/A","N/A","888","ROUTE","425","TRANSENDOCARDIAL","424","SUBRETINAL","423", "SUBGINGIVAL",
                    "422","INTRARUMINAL","421","INTRAOMENTUM","420","INTRANODAL","419", "INTRAMAMMARY",
                    "418","INTRALINGUAL","417","INTRAHEPATIC","416","INTRAEPICARDIAL","415", "TRANSPLACENTAL",
                    "414","INTRAPULMONARY","413","INTRACAUDAL","412","PERINEURAL","411", "PARENTERAL",
                    "410","OROPHARYNGEAL","409","INTRAMENINGEAL","408","INTRAMEDULLARY","406", "INTRACORNEAL",
                    "405","INTRACISTERNAL","404","INTRACEREBRAL","403","INTRACORPORUS CAVERNOSUM","402", "EXTRA-AMNIOTIC",
                    "401","ENDOTRACHEAL","400","UNASSIGNED","366","INTRATYMPANIC","365", "INTRATYMPANIC",
                    "360","PHOTOPHERESIS","363","INTRACARTILAGINOUS","362","INTRABILIARY","361", "INFILTRATION",
                    "358","TRANSDERMAL","357","ELECTRO-OSMOSIS","356","SPINAL","355", "TRANSTRACHEAL","354", "INTRAOVARIAN",
                    "353","INTRATUBULAR","352","INTRALYMPHATIC","315","INTRAVESICAL","314", "INTRAPERICARDIAL","313", "ENTERAL",
                    "312","NOT APPLICABLE","311","INTRAVITREAL","310","INTRALUMINAL","307", "INTRAGINGIVAL","140", "HEMODIALYSIS",
                    "139","UNKNOWN","138","INTRAVENOUS BOLUS","137","INTRAVENOUS DRIP","136", "RESPIRATORY (INHALATION)","135", "OTHER",
                    "134","OCCLUSIVE DRESSING TECHNIQUE","133","ENDOSINUSIAL","132","INTRACAVERNOUS","314", "INTRAPERICARDIAL","313", "ENTERAL",
                    "131","ENDOCERVICAL","130","CUTANEOUS","129","AURICULAR","128", "INTRAVESICAL","127", "INTRAEPIDERMAL","120","ENDOCAVITARY",
                    "125","PERFUSION, BILIARY","124","TRANSTYMPANIC","123","INTRADUCTAL","122", "TRANSMUCOSAL","121", "INTRADISCAL",
                    "119","INTRACORONARY","118","PERFUSION/CARDIAC","117" , "INTRACORONAL, DENTAL","116" , "PERFUSION","115" , "INHALATION, NASAL",
                    "114" , "SC (INFUSION)","113" , "PERCUTANEOUS","106" , "ORAL-28","105" , "ORAL-21","104" , "FOR RX COMPOUNDING",
                    "103" , "INTRATHECAL",
                    "112","URETERAL","110","INTRATESTICULAR","109","SOFT TISSUE","108", "BUCCAL/SUBLINGUAL","107", "ORAL-20",

                  );

      my %MedTypeArr = ("O", "over-the-counter", "P", "prescreption");
      my %ActiveArr = ("1", "Yes", "0", "No");
      my $physician = DBA->selxref($form,'xNPI','NPI',$rPDMed->{'PhysNPI'});
      my $MedName = DBA->getxref($form,'xMedNames',$rPDMed->{MedID},'TradeName');


  main->createHeader($p, $rClient);

  $ypos += 29.3;
  $p->fit_textline("Client Name :", 37, $ypos, $baseboldmidfontoptions);
  $p->fit_textline($cname, 105, $ypos, $basefontoptions);
  $p->fit_textline("Provider Name :", 253.2, $ypos, $baseboldmidfontoptions);
  $p->fit_textline($pname, 333.6, $ypos, $basefontoptions);
  $p->fit_textline("Start Date:", 433.3, $ypos, $baseboldmidfontoptions);
  $p->fit_textline($rPDMed->{'StartDate'}, 500.3, $ypos, $basefontoptions);

  

  $ypos += 20;

  $p->fit_textline("Pills/Tabs:", 37, $ypos, $baseboldmidfontoptions);
  $p->fit_textline($rPDMed->{'Pills'}, 105, $ypos, $basefontoptions);
  $p->fit_textline("Type:", 253.2, $ypos, $baseboldmidfontoptions);
  $p->fit_textline($MedTypeArr{$rPDMed->{'MedType'}}, 320, $ypos, $basefontoptions);
  $p->fit_textline("Active:", 433.3, $ypos, $baseboldmidfontoptions);
  $p->fit_textline($ActiveArr{$rPDMed->{'MedActive'}}, 480, $ypos, $basefontoptions);

  $ypos += 20;

  $p->fit_textline("Benefits:", 37, $ypos, $baseboldmidfontoptions);
  $p->fit_textline($rPDMed->{'Benefits'}, 105, $ypos, $basefontoptions);
  $p->fit_textline("Refills:", 253.2, $ypos, $baseboldmidfontoptions);
  $p->fit_textline($rPDMed->{'Refills'}, 320, $ypos, $basefontoptions); 
  $p->fit_textline("Dispensed:", 433.3, $ypos, $baseboldmidfontoptions);
  $p->fit_textline($rPDMed->{'Count'}, 500.3, $ypos, $basefontoptions);


  $ypos += 20;

  $p->fit_textline("Dosage:", 37, $ypos, $baseboldmidfontoptions);
  $p->fit_textline($rPDMed->{'MedDos'}, 90, $ypos, $basefontoptions);
  $p->fit_textline("Frequency:", 150.2, $ypos, $baseboldmidfontoptions);
  $p->fit_textline($MedFreqArr{$rPDMed->{'MedFreq'}}, 220, $ypos, $basefontoptions);
  $p->fit_textline("Route:", 333.3, $ypos, $baseboldmidfontoptions);
  $p->fit_textline($RouteArr{$rPDMed->{'Route'}}, 380, $ypos, $basefontoptions);
  $p->fit_textline("Physician:", 433.3, $ypos, $baseboldmidfontoptions);
  $p->fit_textline($physician->{'ProvLastName'}, 500, $ypos, $basefontoptions);

  $ypos += 20;

  $p->fit_textline("Side Effects:", 37, $ypos, $baseboldmidfontoptions);
  $p->fit_textline($rPDMed->{'MedSEff'}, 105, $ypos, $basefontoptions);


  $ypos += 20;


  $p->fit_textline("Prescription:", 37, $ypos, $baseboldmidfontoptions);
  $p->fit_textline($MedName, 105, $ypos, $basefontoptions);

  main->createFooter($p);

}



sub createHeader {
  my ($self, $p,$rClient) = @_;

  ##
  # Header info...
  $sProvider->execute($rClient->{'clinicClinicID'})
       || myDBI->dberror("PrintPDMed: select Provider $rClient->{'clinicClinicID'}");
  my $rClinic = $sProvider->fetchrow_hashref;
  my $ClinicName = $rClinic->{'Name'};
  my $ClinicAddr = $rClinic->{'Addr1'} . ', ';
  $ClinicAddr .= $rClinic->{'Addr2'} . ', ' if ( $rClinic->{'Addr2'} );
  $ClinicAddr .= $rClinic->{'City'} . ', ' . $rClinic->{'ST'} . '  ' . $rClinic->{'Zip'};
  my $ClinicPh = 'Office: ' . $rClinic->{'WkPh'} . '  Fax: ' . $rClinic->{'Fax'};
  my $Title = "Client Medications";

  my $Address = qq|${ClinicName}\n${ClinicAddr}\n${ClinicPh}\n${Title}|;

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
