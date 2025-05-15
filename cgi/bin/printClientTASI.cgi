#!/usr/bin/perl
use lib 'C:/xampp/htdocs/src/lib';
use DBI;
use DBA;
use myForm;
use myDBI;
use DBA;
use myConfig;
use MgrTree;
use DBUtil;
use Time::Local;

use PDFlib::PDFlib;
use strict;

############################################################################
my $form = myForm->new();
my $dbh  = myDBI->dbconnect( $form->{'DBNAME'} );
my $IDs  = $form->{'IDs'};

my $sClientTASI = $dbh->prepare("select * from ClientTASI where ID=?");
my $sClient     = $dbh->prepare("select * from Client where ClientID=?");
my $sProvider   = $dbh->prepare("select * from Provider where ProvID=?");

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
  . " embedding encoding=unicode charref";
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

my $marginleft   = 30;
my $margintop    = 35;
my $marginbottom = 30;
my $contentwidth = $pagewidth - 2 * $marginleft;
my $y_top        = $pageheight - $margintop;
my $y_bottom     = $marginbottom;

my $indoc;
my $no_of_input_pages;
my @pagehandles = ();
my $pagecount   = 0;

my ( $sec, $min, $hrs, $day, $month, $year, $wday, $julian ) = localtime();
my $pdfpath  = myConfig->cfg('FORMDIR') . "/printing/PrintClientTASI.pdf";
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
    $p->set_info( "Title",   "TASI" );

    # Open the Block template which contains PDFlib Blocks
    $indoc = $p->open_pdi_document( $pdfpath, "" );
    if ( $indoc == -1 ) { die( "Error: " . $p->get_errmsg() ); }

    $no_of_input_pages = $p->pcos_get_number( $indoc, "length:pages" );

    main->openPdiPages($p);

    main->printClientTASI($p);

    main->closePdiPages($p);

    $p->end_document("");

};

if ($@) {
    die("$0: PDFlib Exception occurred:\n$@");
}

$sClientTASI->finish();
$sClient->finish();
$sProvider->finish();

myDBI->cleanup();

if ( $form->{'file'} eq '' )    # create and print pdf.
{ print qq|Location: ${filename}\n\n|; }
exit;

##########################################################################################################
sub printClientTASI {
    my ( $self, $p ) = @_;

    foreach my $ID ( split( ' ', $IDs ) ) {

        #warn "PrintClientASI: ID=${ID}\n";
        $sClientTASI->execute($ID) || myDBI->dberror("select ClientTASI ${ID}");
        while ( my $rClientTASI = $sClientTASI->fetchrow_hashref ) {
            $sClient->execute( $rClientTASI->{'ClientID'} )
              || myDBI->dberror("select Client: $rClientTASI->{'ClientID'}");
            my $rClient = $sClient->fetchrow_hashref;
            main->createPages( $p, $rClientTASI, $rClient );
        }
    }
    ##print($pagecount);
    if ( $pagecount eq 0 ) {
        main->createEmptyPage($p);
    }
}

sub createEmptyPage {
    my ( $self, $p ) = @_;

    $p->begin_page_ext( $pagewidth, $pageheight, "topdown" );
    $p->fit_textline( "NOT FOUND", $marginleft, 50, $basefontoptions );
    $p->end_page_ext("");
}

sub createPages {
    my ( $self, $p, $rClientTASI, $rClient ) = @_;

    # Header info...
    my $AgencyID = MgrTree->getAgency( $form, $rClient->{'clinicClinicID'} );
    $sProvider->execute($AgencyID)
      || myDBI->dberror("printClientTASI: select Provider $AgencyID");
    my $rAgency    = $sProvider->fetchrow_hashref;
    my $AgencyName = $rAgency->{Name};
    my $AgencyAddr = $rAgency->{Addr1} . ', ';
    $AgencyAddr .= $rAgency->{Addr2} . ', ' if ( $rAgency->{Addr2} );
    my $AgencyCSZ =
      $rAgency->{City} . ', ' . $rAgency->{ST} . ' ' . $rAgency->{Zip};
    my $AgencyPh = 'Office: ' . $rAgency->{WkPh} . ' Fax: ' . $rAgency->{Fax};

    # Page 2
    $rClientTASI->{Addr1} = "$rClientTASI->{Addr1} $rClientTASI->{Addr2}";
    $rClientTASI->{Addr2} =
      "$rClientTASI->{City}, $rClientTASI->{ST}  $rClientTASI->{Zip}";
    $rClientTASI->{InfRel} =
      DBA->getxref( $form, 'xRelationship', $rClientTASI->{InfRel} );
    $sProvider->execute( $rClientTASI->{StaffID} )
      || myDBI->dberror("ERROR: select Provider $rClientTASI->{StaffID}");
    my $rStaff = $sProvider->fetchrow_hashref;
    $rClientTASI->{StaffID} =
        substr( $rStaff->{FName}, 0, 1 )
      . substr( $rStaff->{LName}, 0, 1 )
      . " ($rStaff->{FName} $rStaff->{LName})";
    $rClientTASI->{AdmMo}  = substr( $rClientTASI->{AdmDate}, 5, 2 );
    $rClientTASI->{AdmDay} = substr( $rClientTASI->{AdmDate}, 8, 2 );
    $rClientTASI->{AdmYr}  = substr( $rClientTASI->{AdmDate}, 0, 4 );
    $rClientTASI->{IntMo}  = substr( $rClientTASI->{IntDate}, 5, 2 );
    $rClientTASI->{IntDay} = substr( $rClientTASI->{IntDate}, 8, 2 );
    $rClientTASI->{IntYr}  = substr( $rClientTASI->{IntDate}, 0, 4 );
    $rClientTASI->{DOBMo}  = substr( $rClientTASI->{DOB},     5, 2 );
    $rClientTASI->{DOBDay} = substr( $rClientTASI->{DOB},     8, 2 );
    $rClientTASI->{DOBYr}  = substr( $rClientTASI->{DOB},     0, 4 );
    $rClientTASI->{Race} =
      DBA->getxref( $form, 'xRaces', $rClientTASI->{Race} );
    $rClientTASI->{Religion} = DBA->getxref( $form, 'xReligiousAffiliation',
        $rClientTASI->{'Religion'} );

    # Page 4
    $rClientTASI->{D1D1} =
      DBA->getxref( $form, 'xDrugs', $rClientTASI->{D1D1} );
    $rClientTASI->{D1D2} =
      DBA->getxref( $form, 'xDrugs', $rClientTASI->{D1D2} );
    $rClientTASI->{D1D3} =
      DBA->getxref( $form, 'xDrugs', $rClientTASI->{D1D3} );
    $rClientTASI->{D1R1} =
      DBA->getxref( $form, 'xDrugRoutes', $rClientTASI->{D1R1} );
    $rClientTASI->{D1R2} =
      DBA->getxref( $form, 'xDrugRoutes', $rClientTASI->{D1R2} );
    $rClientTASI->{D1R3} =
      DBA->getxref( $form, 'xDrugRoutes', $rClientTASI->{D1R3} );
    $rClientTASI->{D2D1} =
      DBA->getxref( $form, 'xDrugs', $rClientTASI->{D2D1} );
    $rClientTASI->{D2D2} =
      DBA->getxref( $form, 'xDrugs', $rClientTASI->{D2D2} );
    $rClientTASI->{D2D3} =
      DBA->getxref( $form, 'xDrugs', $rClientTASI->{D2D3} );
    $rClientTASI->{D2D4} =
      DBA->getxref( $form, 'xDrugs', $rClientTASI->{D2D4} );
    $rClientTASI->{D2R1} =
      DBA->getxref( $form, 'xDrugRoutes', $rClientTASI->{D2R1} );
    $rClientTASI->{D2R2} =
      DBA->getxref( $form, 'xDrugRoutes', $rClientTASI->{D2R2} );
    $rClientTASI->{D2R3} =
      DBA->getxref( $form, 'xDrugRoutes', $rClientTASI->{D2R3} );
    $rClientTASI->{D2R4} =
      DBA->getxref( $form, 'xDrugRoutes', $rClientTASI->{D2R4} );
    $rClientTASI->{D3D1} =
      DBA->getxref( $form, 'xDrugs', $rClientTASI->{D3D1} );
    $rClientTASI->{D3D2} =
      DBA->getxref( $form, 'xDrugs', $rClientTASI->{D3D2} );
    $rClientTASI->{D3D3} =
      DBA->getxref( $form, 'xDrugs', $rClientTASI->{D3D3} );
    $rClientTASI->{D3D4} =
      DBA->getxref( $form, 'xDrugs', $rClientTASI->{D3D4} );

    # Page 5
    $rClientTASI->{D4D1} =
      DBA->getxref( $form, 'xDrugs', $rClientTASI->{D4D1} );
    $rClientTASI->{D4D2} =
      DBA->getxref( $form, 'xDrugs', $rClientTASI->{D4D2} );
    $rClientTASI->{D4D3} =
      DBA->getxref( $form, 'xDrugs', $rClientTASI->{D4D3} );
    $rClientTASI->{D4D4} =
      DBA->getxref( $form, 'xDrugs', $rClientTASI->{D4D4} );

    # Page 10
    $rClientTASI->{E5} = DBA->getxref( $form, 'xEmplStat', $rClientTASI->{E5} );
    $rClientTASI->{E6} = DBA->getxref( $form, 'xEmplStat', $rClientTASI->{E6} );

    # Page 17
    $rClientTASI->{L7} =
      DBA->getxref( $form, 'xLegalCharge', $rClientTASI->{L7} );
    $rClientTASI->{L3O1} =
      DBA->getxref( $form, 'xLegalCharge', $rClientTASI->{L3O1} );
    $rClientTASI->{L3O2} =
      DBA->getxref( $form, 'xLegalCharge', $rClientTASI->{L3O2} );
    $rClientTASI->{L3O3} =
      DBA->getxref( $form, 'xLegalCharge', $rClientTASI->{L3O3} );
    $rClientTASI->{L3O4} =
      DBA->getxref( $form, 'xLegalCharge', $rClientTASI->{L3O4} );

##
    my @PageData = (
        {
            "descr" => "page 1",
            "data"  => []
        },
        {
            "descr" => "page 2",
            "data"  => [
                {
                    "type" => "textline",
                    "ypos" => 606,
                    "xpos" => 202.4,
                    "text" => $rClientTASI->{Name}
                },    # Name
                {
                    "type" => "textline",
                    "ypos" => 589,
                    "xpos" => 202.4,
                    "text" => $rClientTASI->{InfName}
                },    # Informant(s) Name
                {
                    "type" => "textline",
                    "ypos" => 572,
                    "xpos" => 202.4,
                    "text" => $rClientTASI->{InfRel}
                },    # Relationship
                {
                    "type" => "textline",
                    "ypos" => 555,
                    "xpos" => 202.4,
                    "text" => $rClientTASI->{Addr1}
                },    # Current Address 1
                {
                    "type" => "textline",
                    "ypos" => 538,
                    "xpos" => 202.4,
                    "text" => $rClientTASI->{Addr2}
                },    # Current Address 2
                {
                    "type" => "textline",
                    "ypos" => 521,
                    "xpos" => 202.4,
                    "text" => ""
                },    # Current Address 3
                {
                    "type" => "textline",
                    "ypos" => 504,
                    "xpos" => 202.4,
                    "text" => $rClientTASI->{ClientID}
                },    # ID Number
                {
                    "type" => "textline",
                    "ypos" => 486,
                    "xpos" => 202.4,
                    "text" => $rClientTASI->{AdmMo}
                },    # Admission Date (month)
                {
                    "type" => "textline",
                    "ypos" => 486,
                    "xpos" => 268,
                    "text" => $rClientTASI->{AdmDay}
                },    # Admission Date (day)
                {
                    "type" => "textline",
                    "ypos" => 486,
                    "xpos" => 334.6,
                    "text" => $rClientTASI->{AdmYr}
                },    # Admission Date (year)
                {
                    "type" => "textline",
                    "ypos" => 451,
                    "xpos" => 202.4,
                    "text" => $rClientTASI->{IntMo}
                },    # Interview Date (month)
                {
                    "type" => "textline",
                    "ypos" => 451,
                    "xpos" => 268,
                    "text" => $rClientTASI->{IntDay}
                },    # Interview Date (day)
                {
                    "type" => "textline",
                    "ypos" => 451,
                    "xpos" => 334.6,
                    "text" => $rClientTASI->{IntYr}
                },    # Interview Date (year)
                {
                    "type" => "textline",
                    "ypos" => 416.5,
                    "xpos" => 202.4,
                    "text" => $rClientTASI->{Class}
                },    # Class
                {
                    "type" => "textline",
                    "ypos" => 399,
                    "xpos" => 202.4,
                    "text" => $rClientTASI->{Contact}
                },    # Contact
                {
                    "type" => "textline",
                    "ypos" => 376,
                    "xpos" => 202.4,
                    "text" => $rClientTASI->{Gend}
                },    # Gender
                {
                    "type" => "textline",
                    "ypos" => 353,
                    "xpos" => 202.4,
                    "text" => $rClientTASI->{StaffID}
                },    # Interview Initials
                {
                    "type" => "textline",
                    "ypos" => 330,
                    "xpos" => 137,
                    "text" => $rClientTASI->{Status}
                },    # Status
                {
                    "type" => "textline",
                    "ypos" => 307.5,
                    "xpos" => 202.4,
                    "text" => $rClientTASI->{DOBMo}
                },    # Birthdate (month)
                {
                    "type" => "textline",
                    "ypos" => 307.5,
                    "xpos" => 268,
                    "text" => $rClientTASI->{DOBDay}
                },    # Birthdate (day)
                {
                    "type" => "textline",
                    "ypos" => 307.5,
                    "xpos" => 334.6,
                    "text" => $rClientTASI->{DOBYr}
                },    # Birthdate (year)
                {
                    "type" => "textline",
                    "ypos" => 272.4,
                    "xpos" => 144,
                    "text" => $rClientTASI->{Race}
                },    # Race
                {
                    "type" => "textline",
                    "ypos" => 151.7,
                    "xpos" => 202,
                    "text" => $rClientTASI->{Religion}
                },    # Religious Preference
            ]
        },

        {
            "descr" => "page 3",
            "data"  => [
                {
                    "type" => "textline",
                    "ypos" => 721.7,
                    "xpos" => 339,
                    "text" => $rClientTASI->{ContEnvi}
                }, # Have you been in a controlled environment in the past year?
                {
                    "type" => "textline",
                    "ypos" => 637.2,
                    "xpos" => 162,
                    "text" => $rClientTASI->{CEDays}
                },    # How many days
                {
                    "type" => "textline",
                    "ypos" => 612.7,
                    "xpos" => 153,
                    "text" => $rClientTASI->{CEDates}
                },    # Record dates:
                {
                    "type"    => "textline",
                    "ypos"    => 540,
                    "text"    => "&#x2713;",
                    "optlist" => $basecheckfontoptions . " fontsize=12",
                    "xpos"    => 187 + 60 * int( $rClientTASI->{SPChemical} )
                },    # Chemical e.g. 0
                {
                    "type"    => "textline",
                    "ypos"    => 515.8,
                    "text"    => "&#x2713;",
                    "optlist" => $basecheckfontoptions . " fontsize=12",
                    "xpos"    => 187 + 60 * int( $rClientTASI->{SPSchool} )
                },    # School e.g. 3
                {
                    "type"    => "textline",
                    "ypos"    => 491.5,
                    "text"    => "&#x2713;",
                    "optlist" => $basecheckfontoptions . " fontsize=12",
                    "xpos"    => 187 + 60 * int( $rClientTASI->{SPEmpSup} )
                },    # Emp/Sup e.g. 1
                {
                    "type"    => "textline",
                    "ypos"    => 467.5,
                    "text"    => "&#x2713;",
                    "optlist" => $basecheckfontoptions . " fontsize=12",
                    "xpos"    => 187 + 60 * int( $rClientTASI->{SPFamily} )
                },    # Family e.g. 2
                {
                    "type"    => "textline",
                    "ypos"    => 443.5,
                    "text"    => "&#x2713;",
                    "optlist" => $basecheckfontoptions . " fontsize=12",
                    "xpos"    => 187 + 60 * int( $rClientTASI->{SPPeerSoc} )
                },    # Peer/Soc e.g. 4
                {
                    "type"    => "textline",
                    "ypos"    => 419.3,
                    "text"    => "&#x2713;",
                    "optlist" => $basecheckfontoptions . " fontsize=12",
                    "xpos"    => 187 + 60 * int( $rClientTASI->{SPLegal} )
                },    # Legal e.g. 0
                {
                    "type"    => "textline",
                    "ypos"    => 398,
                    "text"    => "&#x2713;",
                    "optlist" => $basecheckfontoptions . " fontsize=12",
                    "xpos"    => 187 + 60 * int( $rClientTASI->{SPPsych} )
                },    # Psychiatric e.g. 2
            ]
        },

        {
            "descr" => "page 4",
            "data"  => [
                {
                    "type"   => "table",
                    "fields" => [
                        { "key" => "drugs",      "xpos" => 134 },
                        { "key" => "route",      "xpos" => 219 },
                        { "key" => "noofdays",   "xpos" => 276 },
                        { "key" => "agestarted", "xpos" => 397 },
                    ],
                    "ypos"  => 620.3,
                    "h_row" => 12,
                    "data"  => [
                        {
                            "drugs"      => $rClientTASI->{D1D1},
                            "route"      => $rClientTASI->{D1R1},
                            "noofdays"   => $rClientTASI->{D1C1},
                            "agestarted" => $rClientTASI->{D1A1}
                        },
                        {
                            "drugs"      => $rClientTASI->{D1D2},
                            "route"      => $rClientTASI->{D1R2},
                            "noofdays"   => $rClientTASI->{D1C2},
                            "agestarted" => $rClientTASI->{D1A2}
                        },
                        {
                            "drugs"      => $rClientTASI->{D1D3},
                            "route"      => $rClientTASI->{D1R3},
                            "noofdays"   => $rClientTASI->{D1C3},
                            "agestarted" => $rClientTASI->{D1A3}
                        },
                    ]
                },
                {
                    "type"   => "table",
                    "fields" => [
                        { "key" => "drugs",      "xpos" => 126 },
                        { "key" => "route",      "xpos" => 198 },
                        { "key" => "agestarted", "xpos" => 262 },
                        { "key" => "agestopped", "xpos" => 347 },
                        { "key" => "frequency",  "xpos" => 432 },
                    ],
                    "ypos"  => 481,
                    "h_row" => 12,
                    "data"  => [
                        {
                            "drugs"      => $rClientTASI->{D2D1},
                            "route"      => $rClientTASI->{D2R1},
                            "agestarted" => $rClientTASI->{D2B1},
                            "agestopped" => $rClientTASI->{D2E1},
                            "frequency"  => $rClientTASI->{D2F1}
                        },
                        {
                            "drugs"      => $rClientTASI->{D2D2},
                            "route"      => $rClientTASI->{D2R2},
                            "agestarted" => $rClientTASI->{D2B2},
                            "agestopped" => $rClientTASI->{D2E2},
                            "frequency"  => $rClientTASI->{D2F2}
                        },
                        {
                            "drugs"      => $rClientTASI->{D2D3},
                            "route"      => $rClientTASI->{D2R3},
                            "agestarted" => $rClientTASI->{D2B3},
                            "agestopped" => $rClientTASI->{D2E3},
                            "frequency"  => $rClientTASI->{D2F3}
                        },
                        {
                            "drugs"      => $rClientTASI->{D2D4},
                            "route"      => $rClientTASI->{D2R4},
                            "agestarted" => $rClientTASI->{D2B4},
                            "agestopped" => $rClientTASI->{D2E4},
                            "frequency"  => $rClientTASI->{D2F4}
                        },
                    ]
                },
                {
                    "type"   => "table",
                    "fields" => [
                        { "key" => "drugs",    "xpos" => 155 },
                        { "key" => "noofdays", "xpos" => 311 },
                    ],
                    "ypos"  => 264.2,
                    "h_row" => 12,
                    "data"  => [
                        {
                            "drugs"    => $rClientTASI->{D3D1},
                            "noofdays" => $rClientTASI->{D3C1}
                        },
                        {
                            "drugs"    => $rClientTASI->{D3D2},
                            "noofdays" => $rClientTASI->{D3C2}
                        },
                        {
                            "drugs"    => $rClientTASI->{D3D3},
                            "noofdays" => $rClientTASI->{D3C3}
                        },
                        {
                            "drugs"    => $rClientTASI->{D3D4},
                            "noofdays" => $rClientTASI->{D3C4}
                        },
                    ]
                },
                {
                    "type"       => "textflow",
                    "ypos"       => 197.8,
                    "xpos_start" => 64.8,
                    "xpos_end"   => 568,
                    "text"       => $rClientTASI->{D3COM}
                },    # D3 Comments
            ]
        },

        {
            "descr" => "page 5",
            "data"  => [
                {
                    "type"   => "table",
                    "fields" => [ { "key" => "drugs", "xpos" => 66.6 }, ],
                    "ypos"   => 656.6,
                    "h_row"  => 12,
                    "data"   => [
                        { "drugs" => $rClientTASI->{D4D1} },
                        { "drugs" => $rClientTASI->{D4D2} },
                        { "drugs" => $rClientTASI->{D4D3} },
                        { "drugs" => $rClientTASI->{D4D4} },
                    ]
                },
                {
                    "type" => "textline",
                    "ypos" => 548,
                    "xpos" => 101.5,
                    "text" => $rClientTASI->{D5COM}
                },    # 5 Comments
                {
                    "type" => "textline",
                    "ypos" => 467,
                    "xpos" => 455.4,
                    "text" => $rClientTASI->{D5C}
                },    # 6
                {
                    "type" => "textline",
                    "ypos" => 425,
                    "xpos" => 315,
                    "text" => $rClientTASI->{D7C}
                },    # 7
                {
                    "type" => "textline",
                    "ypos" => 382.8,
                    "xpos" => 360.2,
                    "text" => $rClientTASI->{D8A}
                },    # 8-1
                {
                    "type" => "textline",
                    "ypos" => 368.4,
                    "xpos" => 358.2,
                    "text" => $rClientTASI->{D8O}
                },    # 8-2
                {
                    "type" => "textline",
                    "ypos" => 329,
                    "xpos" => 387.1,
                    "text" => $rClientTASI->{D9A}
                },    # 9-1
                {
                    "type" => "textline",
                    "ypos" => 316.6,
                    "xpos" => 387.1,
                    "text" => $rClientTASI->{D9D}
                },    # 9-2
                {
                    "type" => "textline",
                    "ypos" => 303.8,
                    "xpos" => 387.1,
                    "text" => $rClientTASI->{D9AD}
                },    # 9-3
                {
                    "type" => "textline",
                    "ypos" => 253.2,
                    "xpos" => 352.1,
                    "text" => $rClientTASI->{D10A}
                },    # 10-1
                {
                    "type" => "textline",
                    "ypos" => 240.5,
                    "xpos" => 353.8,
                    "text" => $rClientTASI->{D10D}
                },    # 10-2
                {
                    "type"       => "textflow",
                    "ypos"       => 186,
                    "xpos_start" => 65.3,
                    "xpos_end"   => 568,
                    "text"       => $rClientTASI->{D10COM}
                },    # Comments
            ]
        },

        {
            "descr" => "page 6",
            "data"  => [
                {
                    "type" => "textline",
                    "ypos" => 705.4,
                    "xpos" => 256,
                    "text" => $rClientTASI->{D11A}
                },    # 11-1
                {
                    "type" => "textline",
                    "ypos" => 693,
                    "xpos" => 253,
                    "text" => $rClientTASI->{D11D}
                },    # 11-2
                {
                    "type" => "textline",
                    "ypos" => 667.4,
                    "xpos" => 360,
                    "text" => $rClientTASI->{D12S}
                },    # 12-1
                {
                    "type" => "textline",
                    "ypos" => 654.5,
                    "xpos" => 362,
                    "text" => $rClientTASI->{D12I}
                },    # 12-2
                {
                    "type" => "textline",
                    "ypos" => 613,
                    "xpos" => 182,
                    "text" => $rClientTASI->{D13D}
                },    # 13
                {
                    "type" => "textline",
                    "ypos" => 572.4,
                    "xpos" => 182,
                    "text" => $rClientTASI->{D14M}
                },    # 14
                {
                    "type" => "textline",
                    "ypos" => 532.1,
                    "xpos" => 217.2,
                    "text" => $rClientTASI->{D15D}
                },    # 15
                {
                    "type" => "textline",
                    "ypos" => 491.5,
                    "xpos" => 253.4,
                    "text" => $rClientTASI->{D16D}
                },    # 16
                {
                    "type" => "textline",
                    "ypos" => 451,
                    "xpos" => 324.2,
                    "text" => $rClientTASI->{D17D}
                },    # 17
                {
                    "type" => "textline",
                    "ypos" => 425,
                    "xpos" => 456,
                    "text" => $rClientTASI->{D18A}
                },    # 18-1
                {
                    "type" => "textline",
                    "ypos" => 405,
                    "xpos" => 454,
                    "text" => $rClientTASI->{D18D}
                },    # 18-2
                {
                    "type"       => "textflow",
                    "ypos"       => 374.6,
                    "xpos_start" => 73.2,
                    "xpos_end"   => 568,
                    "text"       => $rClientTASI->{D18COM}
                },    # Comments
            ]
        },

        {
            "descr" => "page 7",
            "data"  => [
                {
                    "type" => "textline",
                    "ypos" => 597.4,
                    "xpos" => 294.2,
                    "text" => $rClientTASI->{D19A}
                },    # 19-1
                {
                    "type" => "textline",
                    "ypos" => 583.9,
                    "xpos" => 295.2,
                    "text" => $rClientTASI->{D19D}
                },    # 19-2
                {
                    "type" => "textline",
                    "ypos" => 543.4,
                    "xpos" => 288.5,
                    "text" => $rClientTASI->{D20A}
                },    # 20-1
                {
                    "type" => "textline",
                    "ypos" => 530,
                    "xpos" => 282.5,
                    "text" => $rClientTASI->{D20D}
                },    # 20-2
                {
                    "type" => "textline",
                    "ypos" => 470.2,
                    "xpos" => 339,
                    "text" => $rClientTASI->{D21A}
                },    # 21-1
                {
                    "type" => "textline",
                    "ypos" => 458.6,
                    "xpos" => 326.4,
                    "text" => $rClientTASI->{D21D}
                },    # 21-2
                {
                    "type" => "textline",
                    "ypos" => 362.9,
                    "xpos" => 261,
                    "text" => $rClientTASI->{D22}
                },    # 22
                {
                    "type" => "textline",
                    "ypos" => 332.4,
                    "xpos" => 261,
                    "text" => $rClientTASI->{D23}
                },    # 23
                {
                    "type"       => "textflow",
                    "ypos"       => 287,
                    "xpos_start" => 77.3,
                    "xpos_end"   => 568,
                    "text"       => $rClientTASI->{D23COM}
                },    # Comments
            ]
        },

        {
            "descr" => "page 8",
            "data"  => [
                {
                    "type" => "textline",
                    "ypos" => 656.4,
                    "xpos" => 201.1,
                    "text" => $rClientTASI->{S1}
                },    # 1
                {
                    "type" => "textline",
                    "ypos" => 627.6,
                    "xpos" => 284.6,
                    "text" => $rClientTASI->{S2}
                },    # 2
                {
                    "type" => "textline",
                    "ypos" => 597.8,
                    "xpos" => 259,
                    "text" => $rClientTASI->{S3}
                },    # 3
                {
                    "type" => "textline",
                    "ypos" => 568.6,
                    "xpos" => 270.7,
                    "text" => $rClientTASI->{S4}
                },    # 4
                {
                    "type" => "textline",
                    "ypos" => 539.3,
                    "xpos" => 246,
                    "text" => $rClientTASI->{S5}
                },    # 5
                {
                    "type" => "textline",
                    "ypos" => 497.3,
                    "xpos" => 350,
                    "text" => $rClientTASI->{S6}
                },    # 6
                {
                    "type" => "textline",
                    "ypos" => 469.4,
                    "xpos" => 225,
                    "text" => $rClientTASI->{S7}
                },    # 7
                {
                    "type" => "textline",
                    "ypos" => 440.2,
                    "xpos" => 300,
                    "text" => $rClientTASI->{S8}
                },    # 8
                {
                    "type" => "textline",
                    "ypos" => 410.9,
                    "xpos" => 224.6,
                    "text" => $rClientTASI->{S9}
                },    # 9
                {
                    "type" => "textline",
                    "ypos" => 381.6,
                    "xpos" => 340.8,
                    "text" => $rClientTASI->{S10}
                },    # 10
                {
                    "type" => "textline",
                    "ypos" => 352.3,
                    "xpos" => 224,
                    "text" => $rClientTASI->{S11}
                },    # 11
                {
                    "type" => "textline",
                    "ypos" => 322.8,
                    "xpos" => 254,
                    "text" => $rClientTASI->{S12}
                },    # 12
                {
                    "type" => "textline",
                    "ypos" => 293.5,
                    "xpos" => 225,
                    "text" => $rClientTASI->{S13}
                },    # 13
                {
                    "type" => "textline",
                    "ypos" => 264.7,
                    "xpos" => 454,
                    "text" => $rClientTASI->{S14}
                },    # 14
                {
                    "type" => "textline",
                    "ypos" => 235,
                    "xpos" => 428,
                    "text" => $rClientTASI->{S15}
                },    # 15
                {
                    "type"       => "textflow",
                    "ypos"       => 197.5,
                    "xpos_start" => 78.5,
                    "xpos_end"   => 568,
                    "text"       => $rClientTASI->{S15COM}
                },    # Comments
            ]
        },

        {
            "descr" => "page 9",
            "data"  => [
                {
                    "type" => "textline",
                    "ypos" => 639.8,
                    "xpos" => 178,
                    "text" => $rClientTASI->{S16}
                },    # 16
                {
                    "type" => "textline",
                    "ypos" => 611.8,
                    "xpos" => 445,
                    "text" => $rClientTASI->{S17}
                },    # 17
                {
                    "type" => "textline",
                    "ypos" => 526.3,
                    "xpos" => 378,
                    "text" => $rClientTASI->{S18}
                },    # 18
                {
                    "type" => "textline",
                    "ypos" => 458.2,
                    "xpos" => 270,
                    "text" => $rClientTASI->{S19}
                },    # 19
                {
                    "type" => "textline",
                    "ypos" => 420.2,
                    "xpos" => 279,
                    "text" => $rClientTASI->{S20}
                },    # 20
                {
                    "type"       => "textflow",
                    "ypos"       => 366.2,
                    "xpos_start" => 107,
                    "xpos_end"   => 568,
                    "text"       => $rClientTASI->{S20COM}
                },    # Comments
            ]
        },

        {
            "descr" => "page 10",
            "data"  => [
                {
                    "type" => "textline",
                    "ypos" => 676.1,
                    "xpos" => 251,
                    "text" => $rClientTASI->{E1}
                },    # 1
                {
                    "type" => "textline",
                    "ypos" => 649.2,
                    "xpos" => 351,
                    "text" => $rClientTASI->{E2}
                },    # 2
                {
                    "type" => "textline",
                    "ypos" => 608.4,
                    "xpos" => 353,
                    "text" => $rClientTASI->{E3}
                },    # 3
                {
                    "type" => "textline",
                    "ypos" => 565,
                    "xpos" => 317,
                    "text" => $rClientTASI->{E4}
                },    # 4
                {
                    "type" => "textline",
                    "ypos" => 535.2,
                    "xpos" => 170,
                    "text" => $rClientTASI->{E4S}
                },    # 4 Specify
                {
                    "type" => "textline",
                    "ypos" => 439.2,
                    "xpos" => 350,
                    "text" => $rClientTASI->{E5}
                },    # 5
                {
                    "type" => "textline",
                    "ypos" => 409.9,
                    "xpos" => 262,
                    "text" => $rClientTASI->{E6}
                },    # 6
                {
                    "type" => "textline",
                    "ypos" => 380.6,
                    "xpos" => 443,
                    "text" => $rClientTASI->{E7}
                },    # 7
                {
                    "type" => "textline",
                    "ypos" => 351.1,
                    "xpos" => 432,
                    "text" => $rClientTASI->{E8}
                },    # 8
                {
                    "type" => "textline",
                    "ypos" => 321.8,
                    "xpos" => 269,
                    "text" => $rClientTASI->{E9}
                },    # 9
                {
                    "type" => "textline",
                    "ypos" => 292.6,
                    "xpos" => 409,
                    "text" => $rClientTASI->{E10}
                },    # 10
                {
                    "type" => "textline",
                    "ypos" => 263.3,
                    "xpos" => 269,
                    "text" => $rClientTASI->{E11}
                },    # 11
                {
                    "type"       => "textflow",
                    "ypos"       => 203.3,
                    "xpos_start" => 99.6,
                    "xpos_end"   => 568,
                    "text"       => $rClientTASI->{E11COM}
                },    # Comments
            ]
        },

        {
            "descr" => "page 11",
            "data"  => [
                {
                    "type" => "textline",
                    "ypos" => 708.7,
                    "xpos" => 374,
                    "text" => $rClientTASI->{E12}
                },    # 12
                {
                    "type" => "textline",
                    "ypos" => 679.4,
                    "xpos" => 254,
                    "text" => $rClientTASI->{E13}
                },    # 13
                {
                    "type" => "textline",
                    "ypos" => 651.4,
                    "xpos" => 458,
                    "text" => $rClientTASI->{E14}
                },    # 14
                {
                    "type" => "textline",
                    "ypos" => 621.1,
                    "xpos" => 254,
                    "text" => $rClientTASI->{E15}
                },    # 15
                {
                    "type" => "textline",
                    "ypos" => 591.6,
                    "xpos" => 415,
                    "text" => $rClientTASI->{E16}
                },    # 16
                {
                    "type" => "textline",
                    "ypos" => 562.3,
                    "xpos" => 215,
                    "text" => $rClientTASI->{E17}
                },    # 17
                {
                    "type" => "textline",
                    "ypos" => 533.3,
                    "xpos" => 378,
                    "text" => $rClientTASI->{E18}
                },    # 18
                {
                    "type" => "textline",
                    "ypos" => 504,
                    "xpos" => 253,
                    "text" => $rClientTASI->{E19}
                },    # 19
                {
                    "type" => "textline",
                    "ypos" => 393.4,
                    "xpos" => 450,
                    "text" => $rClientTASI->{E20}
                },    # 20
                {
                    "type" => "textline",
                    "ypos" => 364.5,
                    "xpos" => 216,
                    "text" => $rClientTASI->{E21}
                },    # 21
                {
                    "type" => "textline",
                    "ypos" => 335,
                    "xpos" => 484,
                    "text" => $rClientTASI->{E22}
                },    # 22
                {
                    "type" => "textline",
                    "ypos" => 305.5,
                    "xpos" => 254,
                    "text" => $rClientTASI->{E23}
                },    # 23
                {
                    "type" => "textline",
                    "ypos" => 263.3,
                    "xpos" => 175,
                    "text" => $rClientTASI->{E24}
                },    # 24
                {
                    "type" => "textline",
                    "ypos" => 235.4,
                    "xpos" => 255,
                    "text" => $rClientTASI->{E25}
                },    # 25
                {
                    "type" => "textline",
                    "ypos" => 206.4,
                    "xpos" => 472,
                    "text" => $rClientTASI->{E26}
                },    # 26
                {
                    "type" => "textline",
                    "ypos" => 177,
                    "xpos" => 382,
                    "text" => $rClientTASI->{E27}
                },    # 27
                {
                    "type"       => "textflow",
                    "ypos"       => 142.6,
                    "xpos_start" => 83.5,
                    "xpos_end"   => 568,
                    "text"       => $rClientTASI->{E27COM}
                },    # Comments
            ]
        },

        {
            "descr" => "page 12",
            "data"  => [
                {
                    "type" => "textline",
                    "ypos" => 711.1,
                    "xpos" => 427,
                    "text" => $rClientTASI->{E28}
                },    # 28
                {
                    "type" => "textline",
                    "ypos" => 681.4,
                    "xpos" => 480,
                    "text" => $rClientTASI->{E29}
                },    # 29
                {
                    "type" => "textline",
                    "ypos" => 554.9,
                    "xpos" => 193,
                    "text" => $rClientTASI->{E30}
                },    # 30
                {
                    "type" => "textline",
                    "ypos" => 529.9,
                    "xpos" => 422,
                    "text" => $rClientTASI->{E31}
                },    # 31
                {
                    "type" => "textline",
                    "ypos" => 393.6,
                    "xpos" => 433,
                    "text" => $rClientTASI->{E32}
                },    # 32
                {
                    "type" => "textline",
                    "ypos" => 295.7,
                    "xpos" => 258,
                    "text" => $rClientTASI->{E33}
                },    # 33
                {
                    "type" => "textline",
                    "ypos" => 268.3,
                    "xpos" => 270,
                    "text" => $rClientTASI->{E34}
                },    # 34
                {
                    "type"       => "textflow",
                    "ypos"       => 189.4,
                    "xpos_start" => 69.5,
                    "xpos_end"   => 568,
                    "text"       => $rClientTASI->{E34COM}
                },    # Comments
            ]
        },

        {
            "descr" => "page 13",
            "data"  => [
                {
                    "type" => "textline",
                    "ypos" => 683.3,
                    "xpos" => 299,
                    "text" => $rClientTASI->{F1}
                },    # 1
                {
                    "type" => "textline",
                    "ypos" => 559.9,
                    "xpos" => 321,
                    "text" => $rClientTASI->{F2}
                },    # 2
                {
                    "type" => "textline",
                    "ypos" => 529.9,
                    "xpos" => 296,
                    "text" => $rClientTASI->{F3}
                },    # 3
                {
                    "type" => "textline",
                    "ypos" => 487.9,
                    "xpos" => 351,
                    "text" => $rClientTASI->{F4M}
                },    # 4-1
                {
                    "type" => "textline",
                    "ypos" => 474.2,
                    "xpos" => 345,
                    "text" => $rClientTASI->{F4F}
                },    # 4-2
                {
                    "type" => "textline",
                    "ypos" => 460.6,
                    "xpos" => 353,
                    "text" => $rClientTASI->{F4S}
                },    # 4-3
                {
                    "type" => "textline",
                    "ypos" => 447.4,
                    "xpos" => 416,
                    "text" => $rClientTASI->{F4O}
                },    # 4-4
                {
                    "type" => "textline",
                    "ypos" => 433.9,
                    "xpos" => 357,
                    "text" => $rClientTASI->{F4C}
                },    # 4-5
                {
                    "type" => "textline",
                    "ypos" => 406.1,
                    "xpos" => 262,
                    "text" => $rClientTASI->{F5a}
                },    # 5a
                {
                    "type" => "textline",
                    "ypos" => 376.8,
                    "xpos" => 292,
                    "text" => $rClientTASI->{F5b}
                },    # 5b
                {
                    "type" => "textline",
                    "ypos" => 264.2,
                    "xpos" => 427,
                    "text" => $rClientTASI->{F6}
                },    # 6
                {
                    "type" => "textline",
                    "ypos" => 234.7,
                    "xpos" => 477,
                    "text" => $rClientTASI->{F7}
                },    # 7
                {
                    "type" => "textline",
                    "ypos" => 205.7,
                    "xpos" => 423,
                    "text" => $rClientTASI->{F8}
                },    # 8
                {
                    "type" => "textline",
                    "ypos" => 176.4,
                    "xpos" => 305,
                    "text" => $rClientTASI->{F9}
                },    # 9
                {
                    "type" => "textline",
                    "ypos" => 146.6,
                    "xpos" => 365,
                    "text" => $rClientTASI->{F10}
                },    # 10
                {
                    "type" => "textline",
                    "ypos" => 117.6,
                    "xpos" => 416,
                    "text" => $rClientTASI->{F11}
                },    # 11
                {
                    "type"       => "textflow",
                    "ypos"       => 87.6,
                    "xpos_start" => 70.1,
                    "xpos_end"   => 568,
                    "text"       => $rClientTASI->{F11COM}
                },    # Comments
            ]
        },

        {
            "descr" => "page 14",
            "data"  => [
                {
                    "type" => "textline",
                    "ypos" => 724.6,
                    "xpos" => 474,
                    "text" => $rClientTASI->{F12}
                },    # 12
                {
                    "type" => "textline",
                    "ypos" => 695,
                    "xpos" => 217,
                    "text" => $rClientTASI->{F13}
                },    # 13
                {
                    "type" => "textline",
                    "ypos" => 651.4,
                    "xpos" => 195,
                    "text" => $rClientTASI->{F14}
                },    # 14
                {
                    "type" => "textline",
                    "ypos" => 621.8,
                    "xpos" => 217,
                    "text" => $rClientTASI->{F15}
                },    # 15
                {
                    "type" => "textline",
                    "ypos" => 506.9,
                    "xpos" => 448,
                    "text" => $rClientTASI->{F16}
                },    # 16
                {
                    "type" => "textline",
                    "ypos" => 477.6,
                    "xpos" => 426,
                    "text" => $rClientTASI->{F17}
                },    # 17
                {
                    "type" => "textline",
                    "ypos" => 340.8,
                    "xpos" => 375,
                    "text" => $rClientTASI->{F18}
                },    # 18
                {
                    "type" => "textline",
                    "ypos" => 270.7,
                    "xpos" => 264,
                    "text" => $rClientTASI->{F19}
                },    # 19
                {
                    "type" => "textline",
                    "ypos" => 227,
                    "xpos" => 288,
                    "text" => $rClientTASI->{F20}
                },    # 20
                {
                    "type"       => "textflow",
                    "ypos"       => 165.1,
                    "xpos_start" => 65.8,
                    "xpos_end"   => 568,
                    "text"       => $rClientTASI->{F20COM}
                },    # Comments
            ]
        },

        {
            "descr" => "page 15",
            "data"  => [
                {
                    "type" => "textline",
                    "ypos" => 698.2,
                    "xpos" => 275,
                    "text" => $rClientTASI->{R1}
                },    # 1
                {
                    "type" => "textline",
                    "ypos" => 648,
                    "xpos" => 215,
                    "text" => $rClientTASI->{R2A}
                },    # 2-1
                {
                    "type" => "textline",
                    "ypos" => 635,
                    "xpos" => 226,
                    "text" => $rClientTASI->{R2M}
                },    # 2-2
                {
                    "type" => "textline",
                    "ypos" => 622.6,
                    "xpos" => 216,
                    "text" => $rClientTASI->{R2C}
                },    # 2-3
                {
                    "type" => "textline",
                    "ypos" => 610.1,
                    "xpos" => 258,
                    "text" => $rClientTASI->{R2O}
                },    # 2-4
                {
                    "type" => "textline",
                    "ypos" => 571.9,
                    "xpos" => 199,
                    "text" => $rClientTASI->{R3}
                },    # 3
                {
                    "type" => "textline",
                    "ypos" => 546.2,
                    "xpos" => 216,
                    "text" => $rClientTASI->{R4}
                },    # 4
                {
                    "type" => "textline",
                    "ypos" => 427.5,
                    "xpos" => 431,
                    "text" => $rClientTASI->{R5}
                },    # 5
                {
                    "type" => "textline",
                    "ypos" => 389,
                    "xpos" => 238,
                    "text" => $rClientTASI->{R6}
                },    # 6
                {
                    "type" => "textline",
                    "ypos" => 351.1,
                    "xpos" => 373,
                    "text" => $rClientTASI->{R7}
                },    # 7
                {
                    "type" => "textline",
                    "ypos" => 313.4,
                    "xpos" => 358,
                    "text" => $rClientTASI->{R8}
                },    # 8
                {
                    "type" => "textline",
                    "ypos" => 262.8,
                    "xpos" => 215,
                    "text" => $rClientTASI->{R9A}
                },    # 9-1
                {
                    "type" => "textline",
                    "ypos" => 249.6,
                    "xpos" => 225,
                    "text" => $rClientTASI->{R9M}
                },    # 9-2
                {
                    "type" => "textline",
                    "ypos" => 237.4,
                    "xpos" => 215,
                    "text" => $rClientTASI->{R9C}
                },    # 9-3
                {
                    "type" => "textline",
                    "ypos" => 224.4,
                    "xpos" => 257,
                    "text" => $rClientTASI->{R9O}
                },    # 9-4
                {
                    "type" => "textline",
                    "ypos" => 199.4,
                    "xpos" => 480,
                    "text" => $rClientTASI->{R10}
                },    # 10
                {
                    "type" => "textline",
                    "ypos" => 161.5,
                    "xpos" => 217,
                    "text" => $rClientTASI->{R11}
                },    # 11
                {
                    "type"       => "textflow",
                    "ypos"       => 120.2,
                    "xpos_start" => 65.3,
                    "xpos_end"   => 568,
                    "text"       => $rClientTASI->{R11COM}
                },    # Comments
            ]
        },

        {
            "descr" => "page 16",
            "data"  => [
                {
                    "type" => "textline",
                    "ypos" => 614.2,
                    "xpos" => 439,
                    "text" => $rClientTASI->{R12}
                },    # 12
                {
                    "type" => "textline",
                    "ypos" => 584.9,
                    "xpos" => 325,
                    "text" => $rClientTASI->{R13}
                },    # 13
                {
                    "type" => "textline",
                    "ypos" => 388.8,
                    "xpos" => 483,
                    "text" => $rClientTASI->{R14}
                },    # 14
                {
                    "type" => "textline",
                    "ypos" => 337.9,
                    "xpos" => 462,
                    "text" => $rClientTASI->{R15}
                },    # 15
                {
                    "type" => "textline",
                    "ypos" => 203.5,
                    "xpos" => 400,
                    "text" => $rClientTASI->{R16}
                },    # 16
                {
                    "type" => "textline",
                    "ypos" => 137,
                    "xpos" => 226,
                    "text" => $rClientTASI->{R17}
                },    # 17
                {
                    "type" => "textline",
                    "ypos" => 111.6,
                    "xpos" => 246,
                    "text" => $rClientTASI->{R18}
                },    # 18
                {
                    "type"       => "textflow",
                    "ypos"       => 69.6,
                    "xpos_start" => 69.4,
                    "xpos_end"   => 568,
                    "text"       => $rClientTASI->{R18COM}
                },    # Comments
            ]
        },

        {
            "descr" => "page 17",
            "data"  => [
                {
                    "type" => "textline",
                    "ypos" => 687.8,
                    "xpos" => 240,
                    "text" => $rClientTASI->{L1}
                },    # 1
                {
                    "type" => "textline",
                    "ypos" => 649.9,
                    "xpos" => 247,
                    "text" => $rClientTASI->{L2}
                },    # 2
                {
                    "type" => "textline",
                    "ypos" => 612,
                    "xpos" => 528,
                    "text" => $rClientTASI->{L3}
                },    # 3
                {
                    "type"   => "table",
                    "fields" => [
                        { "key" => "offense", "xpos" => 66 },
                        { "key" => "age",     "xpos" => 311 },
                    ],
                    "ypos"  => 559.4,
                    "h_row" => 13.2,
                    "data"  => [
                        {
                            "offense" => $rClientTASI->{L3O1},
                            "age"     => $rClientTASI->{L3A1}
                        },
                        {
                            "offense" => $rClientTASI->{L3O2},
                            "age"     => $rClientTASI->{L3A2}
                        },
                        {
                            "offense" => $rClientTASI->{L3O3},
                            "age"     => $rClientTASI->{L3A3}
                        },
                        {
                            "offense" => $rClientTASI->{L3O4},
                            "age"     => $rClientTASI->{L3A4}
                        },
                        { "offense" => "", "age" => "" },
                        { "offense" => "", "age" => "" },
                        { "offense" => "", "age" => "" },
                    ]
                },
                {
                    "type" => "textline",
                    "ypos" => 430.1,
                    "xpos" => 335,
                    "text" => $rClientTASI->{L4}
                },    # 4
                {
                    "type" => "textline",
                    "ypos" => 379.7,
                    "xpos" => 246,
                    "text" => $rClientTASI->{L5}
                },    # 5
                {
                    "type" => "textline",
                    "ypos" => 354,
                    "xpos" => 274,
                    "text" => $rClientTASI->{L6}
                },    # 6
                {
                    "type" => "textline",
                    "ypos" => 311.5,
                    "xpos" => 178,
                    "text" => $rClientTASI->{L7}
                },    # 7
                {
                    "type" => "textline",
                    "ypos" => 266.9,
                    "xpos" => 343,
                    "text" => $rClientTASI->{L8}
                },    # 8
                {
                    "type" => "textline",
                    "ypos" => 222.7,
                    "xpos" => 178,
                    "text" => $rClientTASI->{L9}
                },    # 9
                {
                    "type"       => "textflow",
                    "ypos"       => 181.9,
                    "xpos_start" => 65.5,
                    "xpos_end"   => 568,
                    "text"       => $rClientTASI->{L9COM}
                },    # Comments
            ]
        },

        {
            "descr" => "page 18",
            "data"  => [
                {
                    "type" => "textline",
                    "ypos" => 724.4,
                    "xpos" => 413,
                    "text" => $rClientTASI->{L10}
                },    # 10
                {
                    "type" => "textline",
                    "ypos" => 694.8,
                    "xpos" => 470,
                    "text" => $rClientTASI->{L11}
                },    # 11
                {
                    "type" => "textline",
                    "ypos" => 595.2,
                    "xpos" => 470,
                    "text" => $rClientTASI->{L12}
                },    # 12
                {
                    "type" => "textline",
                    "ypos" => 566.2,
                    "xpos" => 446,
                    "text" => $rClientTASI->{L13}
                },    # 13
                {
                    "type" => "textline",
                    "ypos" => 436.6,
                    "xpos" => 420,
                    "text" => $rClientTASI->{L14}
                },    # 14
                {
                    "type" => "textline",
                    "ypos" => 364.1,
                    "xpos" => 248,
                    "text" => $rClientTASI->{L15}
                },    # 15
                {
                    "type" => "textline",
                    "ypos" => 334.8,
                    "xpos" => 248,
                    "text" => $rClientTASI->{L16}
                },    # 16
                {
                    "type"       => "textflow",
                    "ypos"       => 290.6,
                    "xpos_start" => 68.6,
                    "xpos_end"   => 568,
                    "text"       => $rClientTASI->{L16COM}
                },    # Comments
            ]
        },

        {
            "descr" => "page 19",
            "data"  => [
                {
                    "type" => "textline",
                    "ypos" => 684.2,
                    "xpos" => 293,
                    "text" => $rClientTASI->{P1I}
                },    # 1-1
                {
                    "type" => "textline",
                    "ypos" => 670.8,
                    "xpos" => 329,
                    "text" => $rClientTASI->{P1O}
                },    # 1-2
                {
                    "type" => "textline",
                    "ypos" => 657.4,
                    "xpos" => 200,
                    "text" => $rClientTASI->{P1T}
                },    # 1-3
                {
                    "type" => "textline",
                    "ypos" => 589.7,
                    "xpos" => 248,
                    "text" => $rClientTASI->{P2}
                },    # 2
                {
                    "type" => "textline",
                    "ypos" => 564.2,
                    "xpos" => 279,
                    "text" => $rClientTASI->{P3}
                },    # 3
                {
                    "type" => "textline",
                    "ypos" => 539,
                    "xpos" => 208,
                    "text" => $rClientTASI->{P4}
                },    # 4
                {
                    "type" => "textline",
                    "ypos" => 513.8,
                    "xpos" => 229,
                    "text" => $rClientTASI->{P5}
                },    # 5
                {
                    "type" => "textline",
                    "ypos" => 463,
                    "xpos" => 404,
                    "text" => $rClientTASI->{P6}
                },    # 6
                {
                    "type" => "textline",
                    "ypos" => 437.8,
                    "xpos" => 324,
                    "text" => $rClientTASI->{P7}
                },    # 7
                {
                    "type" => "textline",
                    "ypos" => 412.8,
                    "xpos" => 285,
                    "text" => $rClientTASI->{P8}
                },    # 8
                {
                    "type" => "textline",
                    "ypos" => 361.9,
                    "xpos" => 189,
                    "text" => $rClientTASI->{P9}
                },    # 9
                {
                    "type" => "textline",
                    "ypos" => 311.3,
                    "xpos" => 466,
                    "text" => $rClientTASI->{P10}
                },    # 10
                {
                    "type" => "textline",
                    "ypos" => 260.9,
                    "xpos" => 152,
                    "text" => $rClientTASI->{P11}
                },    # 11
                {
                    "type" => "textline",
                    "ypos" => 137.5,
                    "xpos" => 188,
                    "text" => $rClientTASI->{P12}
                },    # 12
                {
                    "type" => "textline",
                    "ypos" => 111.6,
                    "xpos" => 434,
                    "text" => $rClientTASI->{P13}
                },    # 13
                {
                    "type"       => "textflow",
                    "ypos"       => 73.9,
                    "xpos_start" => 70.1,
                    "xpos_end"   => 568,
                    "text"       => $rClientTASI->{P13COM}
                },    # Comments
            ]
        },

        {
            "descr" => "page 20",
            "data"  => [
                {
                    "type" => "textline",
                    "ypos" => 650.2,
                    "xpos" => 251,
                    "text" => $rClientTASI->{P14}
                },    # 14
                {
                    "type" => "textline",
                    "ypos" => 610.1,
                    "xpos" => 186,
                    "text" => $rClientTASI->{P15}
                },    # 15
                {
                    "type" => "textline",
                    "ypos" => 570.2,
                    "xpos" => 229,
                    "text" => $rClientTASI->{P16}
                },    # 16
                {
                    "type" => "textline",
                    "ypos" => 530.2,
                    "xpos" => 425,
                    "text" => $rClientTASI->{P17}
                },    # 17
                {
                    "type" => "textline",
                    "ypos" => 490.1,
                    "xpos" => 375,
                    "text" => $rClientTASI->{P18}
                },    # 18
                {
                    "type" => "textline",
                    "ypos" => 450,
                    "xpos" => 219,
                    "text" => $rClientTASI->{P19}
                },    # 19
                {
                    "type" => "textline",
                    "ypos" => 320.4,
                    "xpos" => 455,
                    "text" => $rClientTASI->{P20}
                },    # 20
                {
                    "type" => "textline",
                    "ypos" => 237.8,
                    "xpos" => 252,
                    "text" => $rClientTASI->{P21}
                },    # 21
                {
                    "type" => "textline",
                    "ypos" => 197.5,
                    "xpos" => 252,
                    "text" => $rClientTASI->{P22}
                },    # 22
                {
                    "type"       => "textflow",
                    "ypos"       => 166.8,
                    "xpos_start" => 68.6,
                    "xpos_end"   => 568,
                    "text"       => $rClientTASI->{P22COM}
                },    # Comments
            ]
        },

        {
            "descr" => "page 21",
            "data"  => []
        },

        {
            "descr" => "page 22",
            "data"  => []
        },

    );

#####################
    for ( my $pageno = 1 ; $pageno <= $no_of_input_pages ; $pageno++ ) {
        $p->begin_page_ext( $pagewidth, $pageheight, "" );
        $p->fit_pdi_page( $pagehandles[$pageno], 0, 0, "cloneboxes" );
        foreach ( @{ $PageData[ $pageno - 1 ]->{"data"} } ) {
            main->renderObject( $p, $_ );
        }
        $p->end_page_ext("");
        $pagecount++;
    }
}

############################################################################
sub renderObject {
    my ( $self, $p, $obj ) = @_;

    if ( $obj->{"type"} eq "textline" ) {
        main->renderTextline( $p,
            $obj->{"text"}, $obj->{"xpos"}, $obj->{"ypos"}, $obj->{"optlist"} );
    }

    if ( $obj->{"type"} eq "textflow" ) {
        main->renderTextflow( $p,
            $obj->{"text"}, $obj->{"xpos_start"}, $obj->{"xpos_end"},
            $obj->{"ypos"}, $obj->{"optlist"},    $obj->{"optlist2"} );
    }

    if ( $obj->{"type"} eq "table" ) {
        main->renderTable( $p,
            $obj->{"fields"}, $obj->{"ypos"}, $obj->{"h_row"}, $obj->{"data"} );
    }

}

sub openPdiPages {
    my ( $self, $p ) = @_;

    #warn qq|no_of_input_pages: ${no_of_input_pages}\n|;
    # Prepare all pages of the input document. We assume a small
    # number of input pages and a large number of generated output
    # pages. Therefore it makes sense to keep the input pages
    # open instead of opening the pages again for each encounter.

    for ( my $pageno = 1 ; $pageno <= $no_of_input_pages ; $pageno++ ) {

        # Open the first page and clone the page size
        $pagehandles[$pageno] =
          $p->open_pdi_page( $indoc, $pageno, "cloneboxes" );
        if ( $pagehandles[$pageno] == -1 ) {
            die( "Error: " . $p->get_errmsg() );
        }
    }
}

sub closePdiPages {
    my ( $self, $p ) = @_;

    # Close all input pages
    for ( my $pageno = 1 ; $pageno <= $no_of_input_pages ; $pageno++ ) {
        $p->close_pdi_page( $pagehandles[$pageno] );
    }
    $p->close_pdi_document($indoc);
}

sub renderTextline {
    my ( $self, $p, $text, $xpos, $ypos, $optlist ) = @_;

    $p->fit_textline( $text, $xpos, $ypos,
        ( $optlist ? $optlist : $basesmallfontoptions ) );
}

sub renderTextflow {
    my ( $self, $p, $text, $xpos_start, $xpos_end, $ypos, $optlist, $optlist2 )
      = @_;

    my $tf;
    my $result;

    $tf = $p->create_textflow( $text,
        $basefontoptions . " leading=120% " . ( $optlist ? $optlist : "" ) );
    $p->fit_textflow( $tf, $xpos_start, $y_bottom, $xpos_end, $ypos,
        ( $optlist2 ? $optlist2 : "" ) );
}

sub renderTable {
    my ( $self, $p, $fields, $ypos, $h_row, $data ) = @_;

    my $i = 0;

    foreach ( @{$data} ) {
        foreach my $field ( @{$fields} ) {
            main->renderTextline( $p, $_->{ $field->{"key"} },
                $field->{"xpos"}, $ypos - $h_row * $i );
        }
        $i++;
    }

}
