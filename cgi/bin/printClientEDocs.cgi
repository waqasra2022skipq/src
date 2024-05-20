#!/usr/bin/perl
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


my $sClientEDocs = $dbh->prepare("select * from ClientEDocs where ID=?");
my $sClient = $dbh->prepare("select * from Client where ClientID=?");
my $sProvider = $dbh->prepare("select Provider.*, ProviderControl.LOGO from Provider left join ProviderControl on ProviderControl.ProvID=Provider.ProvID where Provider.ProvID=?");

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
  $p->set_info("Title", "Client EDocs");

  main->printClientEDocs($p);

  $p->end_document("");

};



if ($@) {
  die("$0: PDFlib Exception occurred:\n$@");
}

$sClientEDocs->finish();
$sClient->finish();
$sProvider->finish();

myDBI->cleanup();

if ( $form->{'file'} eq '' )                # create and print pdf.
{ print qq|Location: ${filename}\n\n|; }

exit;



############################################################################
sub printClientEDocs {
  my ($self, $p) = @_;

  foreach my $ID (split(' ', $IDs)) {
    $sClientEDocs->execute($ID);
    while(my $rClientEDocs = $sClientEDocs->fetchrow_hashref) {
      $sClient->execute($rClientEDocs->{'ClientID'});
      my $rClient = $sClient->fetchrow_hashref;
      main->createPages($p, $rClientEDocs, $rClient); 
    }
  }

  if ($pagecount) {
    main->createPageCount($p);
  } else {
    main->createEmptyPage($p);
  }
}

sub createPages {
  my ($self, $p, $rClientEDocs, $rClient) = @_;
  
  my $optlist;
  my $tf;
  my $h_tf;
  my $row;
  my $col;
  my $tbl;
  my $h_tbl;

  main->createHeader($p, $rClient);

  my $ClientName = qq|$rClient->{'FName'} $rClient->{'MName'} $rClient->{'LName'}|;

  $p->fit_textline("Client:", 37, $ypos, $baseboldfontoptions);
  $p->fit_textline($ClientName, 100, $ypos, $basefontoptions);


  $p->fit_textline("Loinc Description:", 200, $ypos, $baseboldfontoptions);
  $p->fit_textline($YesNoArr{$rClientEDocs->{"Loinc"}}, 300, $ypos, $basefontoptions);


  my $type = DBA->getxrefWithDef($form, 'xEDocType',  $rClientEDocs->{"Type"}, 'Descr');
  $p->fit_textline("Type:", 380, $ypos, $baseboldfontoptions);
  $p->fit_textline($type, 410, $ypos, $basefontoptions);


  $ypos += 20;

  $p->fit_textline("Title:", 37, $ypos, $baseboldfontoptions);
  $p->fit_textline($rClientEDocs->{"Title"}, 100, $ypos, $basefontoptions);


  $ypos += 20;

  $p->fit_textline("Description:", 37, $ypos, $baseboldfontoptions);
  $p->fit_textline($rClientEDocs->{"Descr"}, 100, $ypos, $basefontoptions);


  $ypos += 20;
  
  $p->fit_textline("Create Date:", 37, $ypos, $baseboldfontoptions);
  $p->fit_textline($rClientEDocs->{"CreateDate"}, 120, $ypos, $basefontoptions);

  main->createFooter($p);
  my $PDF_FilePath = $form->{DOCROOT} . $rClientEDocs->{"Path"}; 
  my $pattern = '.pdf';
  if ($PDF_FilePath =~ /$pattern/) {} 
  else {
    return;
  }

  if(!(-f $PDF_FilePath)) {
    # If File Does not exit
    main->createHeader($p, $rClient);
    $p->fit_textline("FILE NOT FOUND:", 37, $ypos, $baseboldfontoptions);
    $p->fit_textline("$PDF_FilePath Not Found", 80, $ypos + 15, $basefontoptions);

    main->createFooter($p);
    return;
  }
  my $doc = $p->open_pdi_document($PDF_FilePath, "");

  my $page_count = $p->pcos_get_number($doc, "length:pages");

  for (my $page_number = 1; $page_number <= $page_count; $page_number++) {
      my $page = $p->open_pdi_page($doc, $page_number, "");
      $p->begin_page_ext(0, 0, "width=612 height=780");

      if ($page == -1) {
          die("Error: " . $p->get_errmsg());
      }

      $p->fit_pdi_page($page, 0, 0, "");

      $p->close_pdi_page($page);
      $p->suspend_page("");
      ++$pagecount;

  }

  $p->close_pdi_document($doc);
}


sub createHeader {
  my ($self, $p, $rClient) = @_;
  my $AgencyID = MgrTree->getAgency($form,$rClient->{clinicClinicID});
  $sProvider->execute($AgencyID) || myDBI->dberror("printClientEDocs: select Provider AgencyID=${AgencyID}");
  my $rProvider = $sProvider->fetchrow_hashref;
  my $ProviderName = qq|$rProvider->{'FName'} $rProvider->{'MName'} $rProvider->{'LName'}|;
  my $ProviderAddr = $rProvider->{'Addr1'} . ', ';
  $ProviderAddr .= $rProvider->{'Addr2'} . ', ' if ( $rProvider->{'Addr2'} );
  $ProviderAddr .= $rProvider->{'City'} . ', ' . $rProvider->{'ST'} . '  ' . $rProvider->{'Zip'};
  my $ProviderPh = 'Office: ' . $rProvider->{'WkPh'} . '  Fax: ' . $rProvider->{'Fax'};
  my $Title = "Client EDocs";

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
    #$p->fit_textline(" of " . $pagecount, 303, $marginbottom + 14, $baseboldmidfontoptions);
    $p->end_page_ext("");
  }
}

sub createEmptyPage {
  my ($self, $p) = @_;

  $p->begin_page_ext($pagewidth, $pageheight, "topdown");
  $p->fit_textline("NOT FOUND", $marginleft, 50, $basefontoptions);
  $p->end_page_ext("");
}


sub createEmptyPage {
  my ($self, $p) = @_;

  $p->begin_page_ext($pagewidth, $pageheight, "topdown");
  $p->fit_textline("NOT FOUND", $marginleft, 50, $basefontoptions);
  $p->end_page_ext("");
}
