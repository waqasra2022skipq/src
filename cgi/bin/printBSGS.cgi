#!/usr/bin/perl
use lib 'C:/xampp/htdocs/src/lib';
use myConfig;
use DBI;
use myForm;
use myDBI;
use DBA;
use MgrTree;
use DBUtil;
use Time::Local;

use PDFlib::PDFlib;
use strict;
############################################################################
my $form = myForm->new();
my $dbh  = myDBI->dbconnect( $form->{'DBNAME'} );

#warn "printBSGS: IDs=$form->{'IDs'}\n";
##
# prepare selects...
##
my $sGambling  = $dbh->prepare("select * from Gambling where ID=?");
my $sClient    = $dbh->prepare("select * from Client where ClientID=?");
my $sInsurance = $dbh->prepare(
"select * from Insurance left join xInsurance on xInsurance.ID=Insurance.InsID where Insurance.ClientID=? and xInsurance.Descr LIKE '%medicaid%' order by Insurance.InsNumEffDate desc"
);
my $sProvider = $dbh->prepare("select * from Provider where ProvID=?");

############################################################################
my $searchpath = "../data";

my $pagewidth         = 612;
my $pageheight        = 792;
my $fontname          = "Arial";
my $boldfontname      = "Arial-BoldMT";
my $fontsizesmall     = 8;
my $fontsize          = 9;
my $fontsizemid       = 10;
my $fontsizelarge     = 11;
my $fontsizemidlarge  = 12;
my $fontsizexlarge    = 13;
my $fontsizemidxlarge = 14;
my $fontsizexxlarge   = 15;
my $basefontoptions =
    "fontname="
  . $fontname
  . " fontsize="
  . $fontsize
  . " embedding encoding=unicode charref charspacing=0.3";
my $basefontoptions_i = $basefontoptions . " fontstyle=italic";
my $basefontoptions_u = $basefontoptions
  . " underline=true underlineposition=-15% underlinewidth=0.3";
my $baseboldfontoptions =
    "fontname="
  . $boldfontname
  . " fontsize="
  . $fontsize
  . " embedding encoding=unicode";
my $baseboldfontoptions_u = $baseboldfontoptions
  . " underline=true underlineposition=-15% underlinewidth=0.3";
my $basemidfontoptions   = $basefontoptions . " fontsize=" . $fontsizemid;
my $basemidfontoptions_i = $basemidfontoptions . " fontstyle=italic";
my $basemidfontoptions_u = $basemidfontoptions
  . " underline=true underlineposition=-15% underlinewidth=0.3";
my $baseboldmidfontoptions = $baseboldfontoptions . " fontsize=" . $fontsizemid;
my $baseboldmidfontoptions_u = $baseboldmidfontoptions
  . " underline=true underlineposition=-15% underlinewidth=0.3";
my $baseboldmidfontoptions_i = $baseboldmidfontoptions . " fontstyle=italic";
my $baselargefontoptions     = $basefontoptions . " fontsize=" . $fontsizelarge;
my $baseboldlargefontoptions =
  $baseboldfontoptions . " fontsize=" . $fontsizelarge;
my $baseboldlargefontoptions_u = $baseboldlargefontoptions
  . " underline=true underlineposition=-15% underlinewidth=0.3";
my $baseboldlargefontoptions_ui =
  $baseboldlargefontoptions_u . " fontstyle=italic";
my $baseboldlargefontoptions_i =
  $baseboldlargefontoptions . " fontstyle=italic";
my $basesmallfontoptions   = $basefontoptions . " fontsize=" . $fontsizesmall;
my $basesmallfontoptions_i = $basesmallfontoptions . " fontstyle=italic";
my $baseboldsmallfontoptions =
  $baseboldfontoptions . " fontsize=" . $fontsizesmall;
my $basemidlargefontoptions =
  $basefontoptions . " fontsize=" . $fontsizemidlarge;
my $basemidlargefontoptions_i = $basemidlargefontoptions . " fontstyle=italic";
my $basemidxlargefontoptions =
  $basefontoptions . " fontsize=" . $fontsizemidxlarge;
my $baseboldmidxlargefontoptions =
  $baseboldfontoptions . " fontsize=" . $fontsizemidxlarge;
my $basemidxlargefontoptions_i =
  $basemidxlargefontoptions . " fontstyle=italic";
my $baseboldmidlargefontoptions =
  $baseboldfontoptions . " fontsize=" . $fontsizemidlarge;
my $baseboldmidlargefontoptions_u = $baseboldmidlargefontoptions
  . " underline=true underlineposition=-15% underlinewidth=0.3";
my $baseboldxlargefontoptions =
  $baseboldfontoptions . " fontsize=" . $fontsizexlarge;
my $baseboldxlargefontoptions_i =
  $baseboldxlargefontoptions . " fontstyle=italic";
my $basecheckfontoptions =
  "fontname={DejaVuSans} encoding=unicode fontsize=10 charref";

my $marginleft        = 30;
my $margintop         = 35;
my $marginbottom      = $pageheight - 40;
my $contentwidth      = $pagewidth - 2 * $marginleft;
my $h_header          = 85;
my $h_footer          = 4 * $fontsizelarge;
my $y_footer          = $marginbottom - $h_footer;
my $innermarginleft   = 74;
my $innermarginright  = 81;
my $innercontentwidth = $pagewidth - $innermarginleft - $innermarginright;

my $pagecount = 0;

my ( $sec, $min, $hrs, $day, $month, $year, $wday, $julian ) = localtime();
my $formid   = $hrs . $min;
my $filename = '/tmp/'
  . $form->{'LOGINID'} . '_'
  . DBUtil->genToken() . '_'
  . DBUtil->Date( '', 'stamp' ) . '.pdf';
my $outfile = $form->{'file'} eq ''    # create and print pdf else just create.
  ? $form->{'DOCROOT'} . $filename
  : $form->{'file'};

#my $outfile = "kls.pdf";

############################################################################
eval {

    # create a new PDFlib object
    my $p = new PDFlib::PDFlib;

    $p->set_option( "SearchPath={{" . $searchpath . "}}" );

    # This mean we don't have to check error return values, but will
    # get an exception in case of runtime problems.

    $p->set_option("errorpolicy=exception");

    # all strings are expected as utf8
    $p->set_option("stringformat=utf8");

    $p->begin_document( $outfile, "" );

    $p->set_info( "Creator", "Millennium Information Services" );
    $p->set_info( "Author",  "Keith Stephenson" );
    $p->set_info( "Title",   "BBGS" );

    main->printBSGS($p);

    $p->end_document("");

};

if ($@) {
    die("$0: PDFlib Exception occurred:\n$@");
}

$sGambling->finish();
$sClient->finish();
$sInsurance->finish();
$sProvider->finish();

myDBI->cleanup();

if ( $form->{'file'} eq '' )    # create and print pdf.
{ print qq|Location: ${filename}\n\n|; }

exit;

############################################################################
sub printBSGS {
    my ( $self, $p ) = @_;

    foreach my $ID ( split( ' ', $form->{IDs} ) ) {

        #warn "printBSGS: ID=${ID}\n";
        $sGambling->execute($ID) || $form->dberror("select Gambling: ${ID}");
        while ( my $rGambling = $sGambling->fetchrow_hashref ) {
            main->createPages( $p, $rGambling );
            main->createPageCount($p);
        }
    }

}

sub createPages {
    my ( $self, $p, $r ) = @_;

    my $ClientID = $r->{'ClientID'};

    #warn qq|ClientID=$ClientID\n|;
    $sClient->execute($ClientID)
      || $form->dberror("select Client: ${ClientID}");
    my $rClient = $sClient->fetchrow_hashref;
##
    # Header info...
    my $AgencyID = MgrTree->getAgency( $form, $rClient->{clinicClinicID} );
    $sProvider->execute($AgencyID)
      || $form->dberror("select Provider: $AgencyID");
    my $rAgency    = $sProvider->fetchrow_hashref;
    my $AgencyName = $rAgency->{Name};
    my $AgencyAddr = $rAgency->{Addr1};
    $AgencyAddr .= ', ' . $rAgency->{Addr2} if ( $rAgency->{Addr2} );
    my $AgencyCSZ .=
      $rAgency->{City} . ', ' . $rAgency->{ST} . '  ' . $rAgency->{Zip};
    my $AgencyPh  = 'Office: ' . $rAgency->{WkPh};
    my $AgencyFax = 'Fax: ' . $rAgency->{Fax};
##
    $sInsurance->execute($ClientID)
      || $form->dberror("select Insurance: ${ClientID}");
    my $rInsurance = $sInsurance->fetchrow_hashref;

    my $HeaderInfo = {
        'companyname'  => $AgencyName,
        'companyaddr'  => $AgencyAddr,
        'companycsz'   => $AgencyCSZ,
        'companyphone' => $AgencyPh,
        'companyfax'   => $AgencyFax,
        'LOGO'         => $rAgency->{'LOGO'}
    };

    my $BBGSData = {
        'medicaid'     => $rInsurance->{'InsIDNum'},
        'restlessyes'  => $r->{'Anxious'}  ? 1 : 0,
        'restlessno'   => $r->{'Anxious'}  ? 0 : 1,
        'gambledyes'   => $r->{'KeepFrom'} ? 1 : 0,
        'gambledno'    => $r->{'KeepFrom'} ? 0 : 1,
        'financialyes' => $r->{'FinHelp'}  ? 1 : 0,
        'financialno'  => $r->{'FinHelp'}  ? 0 : 1,
    };

#####################
    my $xpos;
    my $ypos;
    my $h_tf;

    main->createHeader( $p, $HeaderInfo );

    $ypos = $margintop + $h_header;

    $ypos += $fontsizexxlarge;

    $ypos += 60;

    $ypos += 13;
    $p->fit_textline( "Medicaid ID:", $innermarginleft, $ypos,
        $basemidfontoptions );
    main->renderLine( $p, 134.6, $ypos + 3, 288.5, $ypos + 3, undef,
        $BBGSData->{"medicaid"} );

    $ypos += 40;
    $h_tf = main->renderTextflow(
        $p,
"During the past 12 months, have you become restless irritable or anxious when trying to stop/cut down on gambling?",
        $innermarginleft,
        $ypos,
        $innermarginleft + $innercontentwidth
    );
    $ypos += $h_tf;
    main->renderRect( $p, 166, $ypos + 3, "Yes", $BBGSData->{"restlessyes"} );
    main->renderRect( $p, 238, $ypos + 3, "No",  $BBGSData->{"restlessno"} );

    $ypos += 40;
    $h_tf = main->renderTextflow(
        $p,
"During the past 12 months, have you tried to keep your family or friends from knowing how much you gambled?",
        $innermarginleft,
        $ypos,
        $innermarginleft + $innercontentwidth
    );
    $ypos += $h_tf;
    main->renderRect( $p, 166, $ypos + 3, "Yes", $BBGSData->{"gambledyes"} );
    main->renderRect( $p, 238, $ypos + 3, "No",  $BBGSData->{"gambledno"} );

    $ypos += 40;
    $h_tf = main->renderTextflow(
        $p,
"During the past 12 months did you have such financial trouble as a result of your gambling that you had to get help with living expenses from family, friends or welfare?",
        $innermarginleft,
        $ypos,
        $innermarginleft + $innercontentwidth
    );
    $ypos += $h_tf;
    main->renderRect( $p, 382, $ypos + 3, "Yes", $BBGSData->{"financialyes"} );
    main->renderRect( $p, 454, $ypos + 3, "No",  $BBGSData->{"financialno"} );

    $ypos += 54;
    $p->fit_textline(
        "Can J Psychiatry. 2010 Feb;55(2):82-90.",
        $innermarginleft,
        $ypos,
        $basemidfontoptions
          . " boxsize={$innercontentwidth 13} position={center right}"
    );

    $ypos += 64;
    $h_tf = main->renderTextflow(
        $p,
        "Fax to:\n"
          . "<leading=140%>John L. Hostetler, M.S. Ed.\n"
          . "<leading=120%>Problem Gambling Field Services Coordinator\n"
          . "Oklahoma Department of Mental Health And Substance Abuse Services 1200 NE 13th Street\n"
          . "P.O. Box 53277\n"
          . "Oklahoma City, OK 73152\n"
          . "Phone (405) 522-1429\n"
          . "Fax (405) 522-3767\n"
          . "<fillcolor={rgb 0.17 0.31 0.64}>John.Hostetler\@odmhsas.org",
        $innermarginleft,
        $ypos,
        397
    );
    $ypos += $h_tf;

    main->createFooter($p);
    ##
}
############################################################################
sub createHeader {
    my ( $self, $p, $HeaderInfo ) = @_;

    my $Company  = $HeaderInfo->{'companyname'};
    my $Address  = "$HeaderInfo->{'companyaddr'}\n$HeaderInfo->{'companycsz'}";
    my $OffceFax = "$HeaderInfo->{'companyphone'} $HeaderInfo->{'companyfax'}";
    my $title    = "Brief BioSocial Gambling Screen (BBGS)";

    my $tf;

    $p->begin_page_ext( $pagewidth, $pageheight, "topdown" );
    my $ypos = $margintop;

    $ypos += $fontsizelarge;
    $p->fit_textline( $Company, $pagewidth / 2,
        $ypos, $baseboldlargefontoptions . " position={center bottom}" );

    my $h_address = 2 * $fontsizexxlarge;
    $ypos += $h_address;
    my $w_address = 150;
    my $x_address = $pagewidth / 2 - $w_address / 2;
    $tf = $p->create_textflow( $Address,
        $baseboldlargefontoptions
          . " leading=110% alignment=justify lastalignment=center" );
    $p->fit_textflow(
        $tf, $x_address, $ypos,
        $x_address + $w_address,
        $ypos - $h_address,
        "verticalalign=center"
    );

    $ypos += $fontsizelarge;
    $p->fit_textline( $OffceFax, $pagewidth / 2,
        $ypos, $baseboldlargefontoptions . " position={center bottom}" );

    # -----------------------------------
    # Place image of logo
    # -----------------------------------
    my $y_offsetlogo = 2;
    $ypos += $y_offsetlogo;
    my $h_logo = $ypos - $margintop;
    my $w_logo = 150;

    my ( $logodirectory, $logofilename ) =
      $HeaderInfo->{'LOGO'} =~ m/(.*\/)(.*)$/;
    if    ( $logofilename eq '' ) { $logofilename = 'logo.png'; }
    elsif ( not -e "/usr/local/PDFlib/${logofilename}" ) {
        $logofilename = 'logo.png';
    }
    my $logoimage = $p->load_image( "auto", $logofilename, "" );
    $p->fit_image( $logoimage, $marginleft, $ypos,
        "boxsize={" . $w_logo . " " . $h_logo . "} fitmethod=meet" );
    $p->close_image($logoimage);
    ##

    $ypos += 2 * $fontsizexxlarge;
    $p->fit_textline( $title, $pagewidth / 2,
        $ypos, $baseboldxlargefontoptions . " position={center bottom}" );
}

sub createFooter {
    my ( $self, $p ) = @_;

    my $tf;
    my $optlist;

    my $footertext =
"<fontname=$boldfontname encoding=unicode>Confidentiality of drug/alcohol abuse records is protected by Federal Law."
      . "<fontname=$fontname encoding=unicode> Federal regulations (42 CFR, Part 2 prohibits making any further disclosure of this information unless further disclosure is expressively permitted by written consent of the person to whom it pertains or as otherwise permitted by 42 CFR, Part 2. A GENERAL AUTHORIZATION FOR RELEASE OF MEDICAL OR OTHER INFORMATION IS NOT SUFFICIENT FOR THIS PURPOSE. The Federal rules restrict any use of the information to criminally investigate or prosecute any alcohol/drug abuse client.";

    $optlist = $basesmallfontoptions . " leading=120% alignment=justify";
    $tf      = $p->create_textflow( $footertext, $optlist );
    $p->fit_textflow( $tf, $marginleft, $marginbottom,
        $marginleft + $contentwidth,
        $y_footer, "verticalalign=bottom" );

    $p->fit_textline(
        "Page " . ( ++$pagecount ),
        268.4, $marginbottom + 14,
        $baseboldmidfontoptions
    );
    $p->suspend_page("");
}

sub createPageCount {
    my ( $self, $p ) = @_;

    for ( my $i = 1 ; $i < $pagecount + 1 ; $i++ ) {

        # Revisit page $i
        $p->resume_page("pagenumber $i");

        # Add the total number of pages
        $p->fit_textline(
            " of " . $pagecount,
            306, $marginbottom + 14,
            $baseboldmidfontoptions
        );
        $p->end_page_ext("");
    }
}

sub renderTextflow {
    my ( $self, $p, $text, $xpos_start, $ypos, $xpos_end, $optlist ) = @_;

    my $tf;
    my $h_tf;
    my $result;

    $tf = $p->create_textflow( $text,
        $basefontoptions . " leading=130% " . ( $optlist ? $optlist : "" ) );
    $result =
      $p->fit_textflow( $tf, $xpos_start, $y_footer, $xpos_end, $ypos, "" );
    $h_tf = $p->info_textflow( $tf, "textheight" );

    return $h_tf;
}

sub renderRect {
    my ( $self, $p, $xpos, $ypos, $label, $data ) = @_;

    my $w_rect        = 9.6;
    my $h_rect        = 9.6;
    my $x_offset_data = 1.2;
    my $y_offset_data = 1.4;
    my $char;

    $p->setlinewidth(0.5);
    $p->set_graphics_option("linejoin=0");
    $p->set_graphics_option("dasharray=none");

    $p->rect( $xpos, $ypos, $w_rect, $h_rect );
    $p->stroke();
    $p->fit_textline(
        $data ? '&#x2713;' : '',
        $xpos + $x_offset_data,
        $ypos - $y_offset_data,
        $basecheckfontoptions
    );
    $p->fit_textline(
        $label,
        $xpos + $w_rect + 4.8,
        $ypos - 1.5,
        $basemidfontoptions
    );
}

sub renderLine {
    my (
        $self,     $p,         $xpos_start, $ypos_start, $xpos_end,
        $ypos_end, $linewidth, $text,       $textopt
    ) = @_;

    my $x_offset_text = 3;
    my $y_offset_text = 3;

    $p->set_graphics_option("dasharray=none");
    $p->setlinewidth( ( $linewidth ? $linewidth : 0.5 ) );
    $p->moveto( $xpos_start, $ypos_start );
    $p->lineto( $xpos_end, $ypos_end );
    $p->stroke();
    $p->fit_textline(
        $text,
        $xpos_start + $x_offset_text,
        $ypos_start - $y_offset_text,
        $textopt ? $textopt : $basefontoptions
    );
}
