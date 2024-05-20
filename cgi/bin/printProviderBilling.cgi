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
use cBill;
use Time::Local;
my $DT=localtime();

use PDFlib::PDFlib;
use strict;
############################################################################

my $form = myForm->new();
my $IDs = $form->{'IDs'};
my $dbh = myDBI->dbconnect($form->{'DBNAME'});


# my $ClinicSelection = DBA->getClinicSelection($form,$form->{Provider_ProvID},'Treatment.ClinicID', 'where');

my $qNotes = qq|
  select Treatment.*, Client.LName, Client.FName, Client.Suffix
        ,Provider.SSN, Provider.LName as PLName, Provider.FName as PFName, Provider.JobTitle
    from Treatment
      left join Client on Client.ClientID=Treatment.ClientID
      left join Provider on Provider.ProvID=Treatment.ProvID
    where Treatment.ClinicID = $form->{Provider_ProvID}
    order by Provider.SSN, Treatment.ContLogDate, Treatment.ContLogBegTime
    LIMIT 51
|;
#warn "qNotes=\n$qNotes\n";
my $sNotes = $dbh->prepare($qNotes);
$sNotes->execute() || $form->dberror($qNotes);

my $sProvider = $dbh->prepare("select * from Provider where ProvID=?");
$sProvider->execute($form->{Provider_ProvID});
my $rProvider = $sProvider->fetchrow_hashref;


my %ClinicList= ();
  my $s= $dbh->prepare("select * from Provider where Type=3");
  $s->execute();
  while (my $r = $s->fetchrow_hashref) { $ClinicList{$r->{ProvID}} = $r; }
my %xInsurance = ();
  $s= $dbh->prepare("select * from xInsurance");
  $s->execute();
  while (my $r = $s->fetchrow_hashref) { $xInsurance{$r->{ID}} = $r; }
$s->finish();


my $qInsurance = qq|select * from Insurance
  where ClientID=? and Insurance.Priority=1|;

my $sInsurance = $dbh->prepare($qInsurance);


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
  $p->set_info("Title", "Provider Billings");

  main->printProviderBillings($p);

  $p->end_document("");

};



if ($@) {
  die("$0: PDFlib Exception occurred:\n$@");
}

$sNotes->finish();
$sProvider->finish();
$sInsurance->finish();

myDBI->cleanup();

if ( $form->{'file'} eq '' )                # create and print pdf.
{ print qq|Location: ${filename}\n\n|; }

exit;



############################################################################
sub printProviderBillings {
  my ($self, $p) = @_;


  while(my $rNotes = $sNotes->fetchrow_hashref) {
    main->createPages($p, $rNotes, $rProvider); 
  }

  if ($pagecount) {
    main->createPageCount($p);
  } else {
    main->createEmptyPage($p);
  }
}

sub createPages {
  my ($self, $p, $rNotes, $rProvider) = @_;
  
  my $optlist;
  my $tf;
  my $h_tf;
  my $row;
  my $col;
  my $tbl;
  my $h_tbl;

  main->createHeader($p, $rProvider);

  my $rxSC = cBill->getServiceCode($form,$rNotes->{SCID},$rNotes->{ContLogDate},$rNotes->{ContLogBegTime},$rNotes->{ContLogEndTime},$rNotes->{TrID},$rNotes->{BillDate});

  my $SSN= $rNotes->{SSN};
  my $Client_Name = $rNotes->{LName};
  $Client_Name .= ", $rNotes->{FName}" if ( $rNotes->{FName} );
  $Client_Name .= " $rNotes->{Suffix}" if ( $rNotes->{Suffix} );
  my $Clinic_Name = $ClinicList{$rNotes->{ClinicID}}{Name};
  my $ContactDate = DBUtil->Date($rNotes->{ContLogDate},'fmt','MM/DD/YYYY');

  my $ContactDate = DBUtil->Date($rNotes->{ContLogDate},'fmt','MM/DD/YYYY');
  $sInsurance->execute($rNotes->{ClientID}) 
                    || $form->dberror($qInsurance);
  my $rInsurance = $sInsurance->fetchrow_hashref;
  my $InsName = $xInsurance{$rInsurance->{InsID}}{Name};
  my $SrcBilled = $xInsurance{$rxSC->{InsID}}{Name};
  my $BegTime = substr($rNotes->{ContLogBegTime},0,5);
  my $EndTime = substr($rNotes->{ContLogEndTime},0,5);

  my ($BilledHrs, $NonBilledHrs) = (0,0);
  if ( $rxSC->{UnitLbl} eq 'NonBill' )
  { $NonBilledHrs = sprintf("%.2f",$rxSC->{Duration} / 3600); }
  else { $BilledHrs = sprintf("%.2f",$rxSC->{Duration} / 3600); }


  my $IncAmt = $rNotes->{'IncAmt'};
  my $BillStatus=DBA->getxref($form,'xBillStatus',$rNotes->{'BillStatus'});
  my $Reason = qq|${BillStatus} on $rNotes->{StatusDate}|;

  $p->fit_textline("Date:", 37, $ypos, $baseboldfontoptions);
  $p->fit_textline($ContactDate, 70, $ypos, $basefontoptions);

  $p->fit_textline("Client Name:", 300, $ypos, $baseboldfontoptions);
  $p->fit_textline($Client_Name, 370, $ypos, $basefontoptions);

  $ypos += 25;

  $p->fit_textline("Source Billed:", 37, $ypos, $baseboldfontoptions);
  $p->fit_textline($SrcBilled, 100, $ypos, $basefontoptions);


  $p->fit_textline("Primary Billing Source:", 300, $ypos, $baseboldfontoptions);
  $p->fit_textline($InsName, 410, $ypos, $basefontoptions);

  $ypos += 25;

  $p->fit_textline("Service:", 37, $ypos, $baseboldfontoptions);
  $p->fit_textline($rxSC->{SCNum}, 80, $ypos, $basefontoptions);

  $p->fit_textline("Start:", 300, $ypos, $baseboldfontoptions);
  $p->fit_textline($BegTime, 340, $ypos, $basefontoptions);

  $p->fit_textline("End:", 400, $ypos, $baseboldfontoptions);
  $p->fit_textline($EndTime,440, $ypos, $basefontoptions);


  $ypos += 25;

  $p->fit_textline("Direct Billable Hours:", 37, $ypos, $baseboldfontoptions);
  $p->fit_textline($BilledHrs, 150, $ypos, $basefontoptions);

  $p->fit_textline("Direct Non Billable Hours:", 300, $ypos, $baseboldfontoptions);
  $p->fit_textline($NonBilledHrs, 430, $ypos, $basefontoptions);


  $ypos += 25;

  $p->fit_textline("Reimbursable Amount Expected:", 37, $ypos, $baseboldfontoptions);
  $p->fit_textline($IncAmt, 200, $ypos, $basefontoptions);

  $p->fit_textline("NOTES:", 300, $ypos, $baseboldfontoptions);
  $p->fit_textline($Reason, 350, $ypos, $basefontoptions);

  $ypos += 25;


  $p->fit_textline("Clinic:", 37, $ypos, $baseboldfontoptions);
  $p->fit_textline($Clinic_Name, 80, $ypos, $basefontoptions);
  main->createFooter($p);

}


sub createHeader {
  my ($self, $p,$rProvider) = @_;
  
  my $ProviderName = qq|$rProvider->{'FName'} $rProvider->{'MName'} $rProvider->{'LName'}|;
  my $ProviderAddr = $rProvider->{'Addr1'} . ', ';
  $ProviderAddr .= $rProvider->{'Addr2'} . ', ' if ( $rProvider->{'Addr2'} );
  $ProviderAddr .= $rProvider->{'City'} . ', ' . $rProvider->{'ST'} . '  ' . $rProvider->{'Zip'};
  my $ProviderPh = 'Office: ' . $rProvider->{'WkPh'} . '  Fax: ' . $rProvider->{'Fax'};
  my $Title = "Provider Billings";

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
