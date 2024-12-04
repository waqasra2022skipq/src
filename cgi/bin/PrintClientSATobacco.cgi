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


my $sClientSATobacco = $dbh->prepare("select * from ClientSATobacco where ID=?");
my $sSATs = $dbh->prepare("select * from ClientSATobacco where ClientID=? and vdate < ? order by vdate desc");
my $sClient = $dbh->prepare("select * from Client where ClientID=?");
my $sProvider = $dbh->prepare("select * from Provider where ProvID=?");

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

my %YesNoArr = ("1", "Yes", "0", "No");


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
  $p->set_info("Title", "Client SATobacco");

  main->printClientSATobacco($p);

  $p->end_document("");

};



if ($@) {
  die("$0: PDFlib Exception occurred:\n$@");
}

$sClientSATobacco->finish();
$sClient->finish();
$sProvider->finish();

myDBI->cleanup();

if ( $form->{'file'} eq '' )                # create and print pdf.
{ print qq|Location: ${filename}\n\n|; }

exit;



############################################################################
sub printClientSATobacco {
  my ($self, $p) = @_;
  

    foreach my $ID ( split(' ',$form->{IDs}) )
    { 
        #warn "PrintClientSATobacco: ID=${ID}\n";
        $sClientSATobacco->execute($ID) || $form->dberror("select ClientSATobacco: ${ID}");
        while ( my $rClientSATobacco = $sClientSATobacco->fetchrow_hashref )
        { 
            $sClient->execute($rClientSATobacco->{'ClientID'});
            my $rClient = $sClient->fetchrow_hashref;
            main->createPages($p, $rClientSATobacco, $rClient); 
        }
    }

  if ($pagecount) {
    main->createPageCount($p);
  } else {
    main->createEmptyPage($p);
  }
}

sub createPages {
  my ($self, $p, $rClientSATobacco, $rClient) = @_;
  
  my $optlist;
  my $tf;
  my $h_tf;
  my $row;
  my $col;
  my $tbl;
  my $h_tbl;

  main->createHeader($p, $rClient);

  my $ClientName = qq|$rClient->{'FName'} $rClient->{'MName'} $rClient->{'LName'}|;
  $p->fit_textline("Client Name:", 37, $ypos, $baseboldfontoptions);
  $p->fit_textline($ClientName, 100, $ypos, $basefontoptions);


  my $ClientID = $rClientSATobacco->{'ClientID'};
  $p->fit_textline("Client ID:", 200, $ypos, $baseboldfontoptions);
  $p->fit_textline($ClientID, 250, $ypos, $basefontoptions);
  $ypos += 25;

  my $TheDate = $rClientSATobacco->{'vdate'};
  my $cnt = 0;
  my @SATs = ();
  push(@SATs,$rClientSATobacco);                   # store (because of 'desc') newest to oldest.
  $sSATs->execute($ClientID,$TheDate) || $form->dberror("select SATs: ${ClientID},${TheDate}");
  while ( my $rSATs = $sSATs->fetchrow_hashref )
  { $cnt++; push(@SATs,$rSATs); last if ( $cnt == 3 ); }

  my @REVSATs = reverse(@SATs);     # output in columns of oldest to newest.
  my $i = 0;
  foreach my $rSATs ( @REVSATs )
  {
    $i++;
    # conversations...
    my $vDate = DBUtil->Date($rSATs->{'vdate'},'fmt','MMDDYY');
    my $qDate = DBUtil->Date($rSATs->{'qdate'},'fmt','MMDDYY');
    my $sTime = substr($rSATs->{stime},0,2).substr($rSATs->{stime},3,2);
    my $eTime = substr($rSATs->{etime},0,2).substr($rSATs->{etime},3,2);
    # convert from SNOMED codes to 5 A's...
    $rSATs->{'smoke'} = $rSATs->{'SmokingStatus'} == 4 || $rSATs->{'SmokingStatus'} == 6
                      ? 1 : 0;
    $rSATs->{'quit'}  = $rSATs->{'SmokingStatus'} == 3 
                      ? 1 : 0;
    $rSATs->{'heavy'} = $rSATs->{'SmokingStatus'} == 1
                      ? 1 : 0;
    $rSATs->{'light'} = $rSATs->{'SmokingStatus'} == 2 || $rSATs->{'SmokingStatus'} == 5
                     || $rSATs->{'SmokingStatus'} == 7 || $rSATs->{'SmokingStatus'} == 8
                      ? 1 : 0;

    my $qyes = $rSATs->{'quit30'} ? 1 : 0;
    my $qno = $rSATs->{'quit30'} ? 0 : 1;

    $p->fit_textline("Visit Date $i:", 37, $ypos, $baseboldfontoptions);
    $p->fit_textline($vDate, 100, $ypos, $basefontoptions);

    $p->fit_textline("Start Time $i:", 150, $ypos, $baseboldfontoptions);
    $p->fit_textline($sTime, 210, $ypos, $basefontoptions);

    $p->fit_textline("smoke $i:", 240, $ypos, $baseboldfontoptions);
    $p->fit_textline($YesNoArr{$rSATs->{'smoke'}}, 280, $ypos, $basefontoptions);

    $p->fit_textline("quit $i:", 310, $ypos, $baseboldfontoptions);
    $p->fit_textline($YesNoArr{$rSATs->{'quit'}}, 340, $ypos, $basefontoptions);

    $p->fit_textline("light $i:", 370, $ypos, $baseboldfontoptions);
    $p->fit_textline($YesNoArr{$rSATs->{'light'}}, 400, $ypos, $basefontoptions);

    $p->fit_textline("heavy $i:", 430, $ypos, $baseboldfontoptions);
    $p->fit_textline($YesNoArr{$rSATs->{'heavy'}}, 470, $ypos, $basefontoptions);

    $ypos += 15;

    $p->fit_textline("Benefits $i:", 37, $ypos, $baseboldfontoptions);
    $p->fit_textline($YesNoArr{$rSATs->{'benefits'}}, 85, $ypos, $basefontoptions);

    $p->fit_textline("Harms $i:", 120, $ypos, $baseboldfontoptions);
    $p->fit_textline($YesNoArr{$rSATs->{'harms'}}, 160, $ypos, $basefontoptions);

    $p->fit_textline("Message $i:", 200, $ypos, $baseboldfontoptions);
    $p->fit_textline($YesNoArr{$rSATs->{'message'}}, 250, $ypos, $basefontoptions);

    $p->fit_textline("Difficulty $i:", 280, $ypos, $baseboldfontoptions);
    $p->fit_textline($YesNoArr{$rSATs->{'difficulty'}}, 335, $ypos, $basefontoptions);

    $p->fit_textline("Quit30 $i:", 365, $ypos, $baseboldfontoptions);
    $p->fit_textline($YesNoArr{$qyes}, 405, $ypos, $basefontoptions);


    $tf = $p->create_textflow("<$baseboldfontoptions>Reason $i: <$basefontoptions> $rSATs->{'reason'}", $basefontoptions . " leading=120% alignment=justify");
    $h_tf = render_textflow($p, $tf, $rClient);

    $ypos += $h_tf;

    $p->fit_textline("Quit Date $i:", 435, $ypos, $baseboldfontoptions);
    $p->fit_textline($qDate, 490, $ypos, $basefontoptions);

    $ypos += 15;

    $p->fit_textline("Problem solving $i:", 37, $ypos, $baseboldfontoptions);
    $p->fit_textline($YesNoArr{$rSATs->{'problem'}}, 120, $ypos, $basefontoptions);

    $p->fit_textline("Provider materials $i:", 150, $ypos, $baseboldfontoptions);
    $p->fit_textline($YesNoArr{$rSATs->{'materials'}}, 240, $ypos, $basefontoptions);

    $p->fit_textline("Identify Support $i:", 270, $ypos, $baseboldfontoptions);
    $p->fit_textline($YesNoArr{$rSATs->{'identify'}}, 360, $ypos, $basefontoptions);

    $p->fit_textline("Pharmacotherapy $i:", 390, $ypos, $baseboldfontoptions);
    $p->fit_textline($YesNoArr{$rSATs->{'pharma'}}, 480, $ypos, $basefontoptions);

    $ypos += 15;
    
    $p->fit_textline("Refer to 1 800 QUIT NOW $i:", 37, $ypos, $baseboldfontoptions);
    $p->fit_textline($YesNoArr{$rSATs->{'refer'}}, 170, $ypos, $basefontoptions);

    $ypos += 15;
    
    $p->fit_textline("Assess smoking status at every visit $i:", 37, $ypos, $baseboldfontoptions);
    $p->fit_textline($YesNoArr{$rSATs->{'assess'}}, 220, $ypos, $basefontoptions); 

    $ypos += 15;
    
    $p->fit_textline("Ask client about the quitting process $i:", 37, $ypos, $baseboldfontoptions);
    $p->fit_textline($YesNoArr{$rSATs->{'ask'}}, 220, $ypos, $basefontoptions);

    $ypos += 15;
    
    $p->fit_textline("Reinforce the steps the client is taking to quit $i:", 37, $ypos, $baseboldfontoptions);
    $p->fit_textline($YesNoArr{$rSATs->{'reinforce'}}, 280, $ypos, $basefontoptions);

    $ypos += 15;
    
    $p->fit_textline("Provider encouragement $i:", 37, $ypos, $baseboldfontoptions);
    $p->fit_textline($YesNoArr{$rSATs->{'encourage'}}, 160, $ypos, $basefontoptions);

    $p->fit_textline("Set follow up appointment $i:", 190, $ypos, $baseboldfontoptions);
    $p->fit_textline($YesNoArr{$rSATs->{'followup'}}, 320, $ypos, $basefontoptions);

    $ypos += 15;
    
    $tf = $p->create_textflow("<$baseboldfontoptions>Comments $i: <$basefontoptions> $rSATs->{'comments'}", $basefontoptions . " leading=120% alignment=justify");
    $h_tf = render_textflow($p, $tf, $rClient);

    $ypos +=  25 + $h_tf;

    $p->fit_textline("End Time $i:", 37, $ypos, $baseboldfontoptions);
    $p->fit_textline($YesNoArr{$rSATs->{'etime'}}, 100, $ypos, $basefontoptions);

    $ypos += 25;

  }

  main->createFooter($p);

}

sub render_textflow {
    my ($p, $tf, $rClient) = @_;
    my $ClientID = $rClient->{ClientID};
    my $ClientName = qq|$rClient->{FName} $rClient->{LName}|;
    my $result;
    my $h_tf;

    do {
        $result = $p->fit_textflow($tf, $marginleft, $y_footer, $marginleft + $contentwidth, $ypos, "");
        if ($result eq "_boxfull" || $result eq "_boxempty") {
            main->createFooter($p);
            main->createHeader($p, $rClient);
        }
    } while ($result ne "_stop");
    $h_tf = $p->info_textflow($tf, "textheight");

    return $h_tf;
}


sub createHeader {
  my ($self, $p, $rClient) = @_;
  my $AgencyID = MgrTree->getAgency($form,$rClient->{clinicClinicID});
  $sProvider->execute($AgencyID) || myDBI->dberror("printClientSATobacco: select Provider AgencyID=${AgencyID}");
  my $rProvider = $sProvider->fetchrow_hashref;
  my $ProviderName = qq|$rProvider->{'FName'} $rProvider->{'MName'} $rProvider->{'LName'}|;
  my $ProviderAddr = $rProvider->{'Addr1'} . ', ';
  $ProviderAddr .= $rProvider->{'Addr2'} . ', ' if ( $rProvider->{'Addr2'} );
  $ProviderAddr .= $rProvider->{'City'} . ', ' . $rProvider->{'ST'} . '  ' . $rProvider->{'Zip'};
  my $ProviderPh = 'Office: ' . $rProvider->{'WkPh'} . '  Fax: ' . $rProvider->{'Fax'};
  my $Title = "Client SATobacco";

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


sub createEmptyPage {
  my ($self, $p) = @_;

  $p->begin_page_ext($pagewidth, $pageheight, "topdown");
  $p->fit_textline("NOT FOUND", $marginleft, 50, $basefontoptions);
  $p->end_page_ext("");
}
