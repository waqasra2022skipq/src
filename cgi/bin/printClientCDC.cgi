#!/usr/bin/perl
############################################################################
use lib '/var/www/okmis/src/lib';
use DBI;
use myForm;
use myDBI;
use DBA;
use MgrTree;
use DBUtil;
use Time::Local;
my $DT = localtime();

use PDFlib::PDFlib;
use strict;
############################################################################

my $form = myForm->new();
my $IDs  = $form->{'IDs'};
my $dbh  = myDBI->dbconnect( $form->{'DBNAME'} );

#warn "printClientCDC: IDs=${IDs}, type=${type}\n";

my $type = $form->{'Adult'} ? 'Adult' : 'Child';
##
# prepare selects...
##
my $sClient = $dbh->prepare("select DOB, Email from Client where ClientID=?");
my $sClientPrAuth = $dbh->prepare("select * from ClientPrAuth where ID=?");
my $sClientPrAuthCDC =
  $dbh->prepare("select * from ClientPrAuthCDC where ClientPrAuthID=?");
my $sPDDiag   = $dbh->prepare("select * from PDDiag where PrAuthID=?");
my $sProvider = $dbh->prepare("select * from Provider where ProvID=?");
############################################################################

my $pagewidth  = 842;
my $pageheight = 612;

my $searchpath = "../data";

my $fontname        = "Roboto-Light";
my $fontsizexxsmall = 6;
my $fontsizexsmall  = 7;
my $fontsizesmall   = 8;
my $fontsize        = 9;
my $fontsizemid     = 10;
my $fontsizelarge   = 11;
my $fontsizexlarge  = 13;
my $fontsizexxlarge = 15;
my $basefontoptions =
    "fontname="
  . $fontname
  . " fontsize="
  . $fontsize
  . " embedding encoding=unicode";
my $baseboldfontoptions    = $basefontoptions . " fakebold=true";
my $basexxsmallfontoptions = $basefontoptions . " fontsize=" . $fontsizexxsmall;
my $baseboldxxsmallfontoptions =
  $baseboldfontoptions . " fontsize=" . $fontsizexxsmall;
my $basexsmallfontoptions = $basefontoptions . " fontsize=" . $fontsizexsmall;
my $baseboldxsmallfontoptions =
  $baseboldfontoptions . " fontsize=" . $fontsizexsmall;
my $basemidfontoptions     = $basefontoptions . " fontsize=" . $fontsizemid;
my $baseboldmidfontoptions = $baseboldfontoptions . " fontsize=" . $fontsizemid;
my $baseboldmidfontoptions_u = $baseboldmidfontoptions
  . " underline=true underlineposition=-15% underlinewidth=1.0";
my $baselargefontoptions = $basefontoptions . " fontsize=" . $fontsizelarge;
my $baseboldlargefontoptions =
  $baseboldfontoptions . " fontsize=" . $fontsizelarge;
my $baseboldlargefontoptions_u =
    $baseboldfontoptions
  . " fontsize="
  . $fontsizelarge
  . " underline=true underlineposition=-15% underlinewidth=0.03";
my $baseboldlargefontoptions_ui =
  $baseboldlargefontoptions_u . " fontstyle=italic";
my $basesmallfontoptions = $basefontoptions . " fontsize=" . $fontsizesmall;
my $baseboldsmallfontoptions =
  $baseboldfontoptions . " fontsize=" . $fontsizesmall;

my $marginleft    = 46;
my $margintop     = 32;
my $marginbottom  = 32;
my $contentwidth  = $pagewidth - 2 * $marginleft;
my $contentheight = $pageheight - $margintop - $marginbottom;

my $marginleft_help    = 32;
my $margintop_help     = 40;
my $marginbottom_help  = 32;
my $contentwidth_help  = $pageheight - 2 * $marginleft_help;
my $contentheight_help = $pagewidth - $margintop_help - $marginbottom_help;

my $filename = '/tmp/'
  . $form->{'LOGINID'} . '_'
  . DBUtil->genToken() . '_'
  . DBUtil->Date( '', 'stamp' ) . '.pdf';
my $outfile = $form->{'file'} eq ''    # create and print pdf else just create.
  ? $form->{'DOCROOT'} . $filename
  : $form->{'file'};

#$outfile = 'kls.pdf';
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

    $p->set_info( "Title", "CDC Form" );

    printCDCForm($p);
    create_help_page($p);

    $p->end_document("");

};

if ($@) {
    die("$0: PDFlib Exception occurred:\n$@");
}

$sClient->finish();
$sClientPrAuth->finish();
$sClientPrAuthCDC->finish();
$sPDDiag->finish();
$sProvider->finish();
myDBI->cleanup();
if ( $form->{'file'} eq '' )    # create and print pdf.
{ print qq|Location: ${filename}\n\n|; }
exit;
############################################################################

sub printCDCForm {
    my ($p) = @_;

    foreach my $PrAuthID ( split( ' ', $form->{IDs} ) ) {

        #warn "PrintCDC: PrAuthID=${PrAuthID}\n";
        $sClientPrAuth->execute($PrAuthID)
          || myDBI->dberror("select ClientPrAuth: ${PrAuthID}");
        while ( my $rClientPrAuth = $sClientPrAuth->fetchrow_hashref ) {
            $sClientPrAuthCDC->execute($PrAuthID)
              || myDBI->dberror("select ClientPrAuthCDC: PrAuthID=${PrAuthID}");
            my $rCDC = $sClientPrAuthCDC->fetchrow_hashref;
            $sClient->execute( $rClientPrAuth->{'ClientID'} );
            my ( $DOB, $Email ) = $sClient->fetchrow_array;
            if ( $rCDC->{'Age'} eq '' ) {
                my $Age =
                  DBUtil->Date( $DOB, 'age', $rClientPrAuth->{'EffDate'} );
                $type = $Age < 18 ? 'Child' : 'Adult';
            }
            else {
                $type = $rCDC->{'Age'} < 18 ? 'Child' : 'Adult';
            }

            #warn "PrintCDC: PrAuthID=${PrAuthID}, type=${type}\n";
            $rCDC->{Email} = $Email;
            $rCDC->{SSN} =~ s/-//g;
            $rCDC->{Gend} =
              $rCDC->{Gend} == 1 ? 'F' : $rCDC->{Gend} == 2 ? 'M' : 'U';
            $rCDC->{chronic} =
              $rCDC->{AlertCHomeless} ? '1' : '2';    # 1=Yes, 2=No
            $rCDC->{customerschool} =
              $rCDC->{InSchool} ? '1' : '2';          # 1=Yes, 2=No
            $rCDC->{customerpreg} = $rCDC->{Pregnant} ? '1' : '2'; # 1=Yes, 2=No
            $rCDC->{custenglish} =
              $rCDC->{LangEnglish} ? '1' : '2';                    # 1=Yes, 2=No
            $rCDC->{SMI} = $rCDC->{SMI} ? '1' : '2';               # 1=Yes, 2=No
            $rCDC->{SED} = $rCDC->{SED} ? '1' : '2';               # 1=Yes, 2=No
            ( $rCDC->{'zip1'}, $rCDC->{'zip2'} ) =
              split( '-', $rCDC->{'Zip'}, 2 );
            ( $rClientPrAuth->{'startdate'} = $rClientPrAuth->{'EffDate'} ) =~
              s/-//g;

#warn "PrintCDC: PrAuthID=${PrAuthID}, Diag1Prim=$rClientPrAuth->{Diag1Prim}\n";
            $rClientPrAuth->{'axis1primary1'} =
              substr( $rClientPrAuth->{'Diag1Prim'}, 0, 3 );
            $rClientPrAuth->{'axis1primary2'} =
              substr( $rClientPrAuth->{'Diag1Prim'}, 3 );

  #warn "PrintCDC: PrAuthID=${PrAuthID}, Diag1Sec=$rClientPrAuth->{Diag1Sec}\n";
            $rClientPrAuth->{'axis1secondary1'} =
              substr( $rClientPrAuth->{'Diag1Sec'}, 0, 3 );
            $rClientPrAuth->{'axis1secondary2'} =
              substr( $rClientPrAuth->{'Diag1Sec'}, 3 );

#warn "PrintCDC: PrAuthID=${PrAuthID}, Diag1Tert=$rClientPrAuth->{Diag1Tert}\n";
            $rClientPrAuth->{'axis1tertiary1'} =
              substr( $rClientPrAuth->{'Diag1Tert'}, 0, 3 );
            $rClientPrAuth->{'axis1tertiary2'} =
              substr( $rClientPrAuth->{'Diag1Tert'}, 3 );

#warn "PrintCDC: PrAuthID=${PrAuthID}, Diag2Prim=$rClientPrAuth->{Diag2Prim}\n";
            $rClientPrAuth->{'axis2primary1'} =
              substr( $rClientPrAuth->{'Diag2Prim'}, 0, 3 );
            $rClientPrAuth->{'axis2primary2'} =
              substr( $rClientPrAuth->{'Diag2Prim'}, 3 );

  # Not set or sent to DMH starting 2015
  #warn "PrintCDC: PrAuthID=${PrAuthID}, Diag2Sec=$rClientPrAuth->{Diag2Sec}\n";
            $rClientPrAuth->{'axis2secondary1'} =
              substr( $rClientPrAuth->{'Diag2Sec'}, 0, 3 );
            $rClientPrAuth->{'axis2secondary2'} =
              substr( $rClientPrAuth->{'Diag2Sec'}, 3 );
            $sPDDiag->execute($PrAuthID)
              || myDBI->dberror("select PDDiag: $PrAuthID");
            if ( my $rPDDiag = $sPDDiag->fetchrow_hashref )    # pre 2015
            {
#foreach my $f ( sort keys %{$rPDDiag} ) { warn "PrintCDC2.cgi: rPDDiag-$f=$rPDDiag->{$f}\n"; }
                my $Axis1ACode =
                  DBA->getxref( $form, 'xAxis1', $rPDDiag->{Axis1ACode},
                    'ICD9' );
                my $Axis1BCode =
                  DBA->getxref( $form, 'xAxis1', $rPDDiag->{Axis1BCode},
                    'ICD9' );
                my $Axis1CCode =
                  DBA->getxref( $form, 'xAxis1', $rPDDiag->{Axis1CCode},
                    'ICD9' );
                my $Axis2ACode =
                  DBA->getxref( $form, 'xAxis2', $rPDDiag->{Axis2ACode},
                    'ICD9' );
                my $Axis2BCode =
                  DBA->getxref( $form, 'xAxis2', $rPDDiag->{Axis2BCode},
                    'ICD9' );
                (
                    $rClientPrAuth->{'axis1primary1'},
                    $rClientPrAuth->{'axis1primary2'}
                ) = split( /\./, $Axis1ACode, 2 );
                (
                    $rClientPrAuth->{'axis1secondary1'},
                    $rClientPrAuth->{'axis1secondary2'}
                ) = split( /\./, $Axis1BCode, 2 );
                (
                    $rClientPrAuth->{'axis1tertiary1'},
                    $rClientPrAuth->{'axis1tertiary2'}
                ) = split( /\./, $Axis1CCode, 2 );
                (
                    $rClientPrAuth->{'axis2primary1'},
                    $rClientPrAuth->{'axis2primary2'}
                ) = split( /\./, $Axis2ACode, 2 );

                # Not set or sent to DMH starting 2015
                (
                    $rClientPrAuth->{'axis2secondary1'},
                    $rClientPrAuth->{'axis2secondary2'}
                ) = split( /\./, $Axis2BCode, 2 );
                #
                # use PDDiag??    ...
                #
                # Diag4 WAS REMOVED  from PrAuth AND NO LONGER SENT INTO DMH
                $rClientPrAuth->{'Diag4Support'} = $rPDDiag->{'Diag4Support'};
                $rClientPrAuth->{'Diag4Social'}  = $rPDDiag->{'Diag4Social'};
                $rClientPrAuth->{'Diag4Education'} =
                  $rPDDiag->{'Diag4Education'};
                $rClientPrAuth->{'Diag4Occup'}  = $rPDDiag->{'Diag4Occup'};
                $rClientPrAuth->{'Diag4House'}  = $rPDDiag->{'Diag4House'};
                $rClientPrAuth->{'Diag4Econ'}   = $rPDDiag->{'Diag4Econ'};
                $rClientPrAuth->{'Diag4Health'} = $rPDDiag->{'Diag4Health'};
                $rClientPrAuth->{'Diag4Legal'}  = $rPDDiag->{'Diag4Legal'};
                $rClientPrAuth->{'Diag4Other'}  = $rPDDiag->{'Diag4Other'};
            }

         #warn qq|ID=$rCDC->{'ID'}: EthnicHispanic=$rCDC->{'EthnicHispanic'}\n|;

            main->$type( $p, $rCDC, $rClientPrAuth );
        }
    }
}

sub Adult {
    my ( $self, $p, $rCDC, $rClientPrAuth ) = @_;

##
    # Header info...
    my $AgencyID = MgrTree->getAgency( $form, $rCDC->{ClinicID} );
    $sProvider->execute($AgencyID)
      || myDBI->dberror("select Provider: $AgencyID");
    my $rAgency    = $sProvider->fetchrow_hashref;
    my $AgencyName = $rAgency->{Name};
    my $AgencyAddr = $rAgency->{Addr1} . ', ';
    $AgencyAddr .= $rAgency->{Addr2} . ', ' if ( $rAgency->{Addr2} );
    $AgencyAddr .=
      $rAgency->{City} . ', ' . $rAgency->{ST} . '  ' . $rAgency->{Zip};
    my $AgencyPh = 'Office: ' . $rAgency->{WkPh} . '  Fax: ' . $rAgency->{Fax};
##

##
    # Section 1 variables
    my $agency = $rCDC->{'AgencySite'};
    my $dot    = DBUtil->Date( $rCDC->{'TransDate'}, 'fmt', "MMDDYYYY" );
    my $transactiontime = main->convertDateTime( $rCDC->{'TransTime'} );
    my $transactiontype = $rCDC->{'TransType'};
    my $memberid        = $rCDC->{'InsIDNum'};
    my $dob      = DBUtil->Date( $rCDC->{'DateOfBirth'}, 'fmt', "MMDDYYYY" );
    my $sfocus   = $rCDC->{'ServiceFocus'};
    my $white    = $rCDC->{'RaceWhite'};
    my $black    = $rCDC->{'RaceBlack'};
    my $american = $rCDC->{'Race'};
    my $native   = $rCDC->{'RaceIndian'};
    my $asian    = $rCDC->{'RaceAsian'};
    my $emailaddress    = $rCDC->{'Email'};
    my $ethnicity       = $rCDC->{'EthnicHispanic'};
    my $gender          = $rCDC->{'Gend'};
    my $alert           = $rCDC->{'alertinfo'};
    my $traumascore     = $rCDC->{'traumaScore'};
    my $acescore        = $rCDC->{'ACEScore'};
    my $mentalscreen    = $rCDC->{'ScreenType1'};
    my $substancescreen = $rCDC->{'ScreenType2'};
    my $traumascreen    = $rCDC->{'ScreenType3'};
    my $gamblingscreen  = $rCDC->{'GamblingScreen'};
    my $preferral       = $rCDC->{'PriReferralType'};
    my $pragency        = $rCDC->{'PriReferralNPI'};
    my $sreferral       = $rCDC->{'SecReferralType'};
    my $sragency        = $rCDC->{'SecReferralNPI'};
    my $countyresidence = $rCDC->{'CountyofRes'};
    my $zip1            = $rCDC->{'zip1'};
    my $zip2            = $rCDC->{'zip2'};
##
##
    # Section 2 Variables
    my $residence        = $rCDC->{'CurrentResidence'};
    my $prison           = $rCDC->{'PrisonJail'};
    my $living           = $rCDC->{'LivingSituation'};
    my $chronic          = $rCDC->{'chronic'};
    my $employment       = $rCDC->{'EmplStat'};
    my $typeofemployment = $rCDC->{'EmplType'};
    my $customerschool   = $rCDC->{'customerschool'};
    my $education        = $rCDC->{'Education'};
    my $militarystatus   = $rCDC->{'MilitaryStatus'};
    my $maritalstatus    = $rCDC->{'MarStat'};
    my $customerpreg     = $rCDC->{'customerpreg'};
    my $pregnantdob =
      DBUtil->Date( $rCDC->{'PregnantDate'}, 'fmt', "MMDDYYYY" );
    my $annualincome     = $rCDC->{'AnnualIncome'};
    my $number           = $rCDC->{'IncomeDeps'};
    my $ssi              = $rCDC->{'SSI'};
    my $ssdi             = $rCDC->{'SSDI'};
    my $custother        = $rCDC->{'LangOther'};
    my $custenglish      = $rCDC->{'custenglish'};
    my $disability1      = $rCDC->{'Handicap1'};
    my $disability2      = $rCDC->{'Handicap2'};
    my $disability3      = $rCDC->{'Handicap3'};
    my $disability4      = $rCDC->{'Handicap4'};
    my $legalstatus      = $rCDC->{'LegalStatus'};
    my $countryc         = $rCDC->{'CommitmentCounty'};
    my $tobaccouse       = $rCDC->{'TobaccoUse'};
    my $presentingprblm1 = $rCDC->{'Problem1'};
    my $presentingprblm2 = $rCDC->{'Problem2'};
    my $presentingprblm3 = $rCDC->{'Problem3'};
    my $drugs1           = $rCDC->{'Drug1'};
    my $drugs2           = $rCDC->{'Drug2'};
    my $drugs3           = $rCDC->{'Drug3'};
    my $route1           = $rCDC->{'Route1'};
    my $route2           = $rCDC->{'Route2'};
    my $route3           = $rCDC->{'Route3'};
    my $frequency1       = $rCDC->{'Freq1'};
    my $frequency2       = $rCDC->{'Freq2'};
    my $frequency3       = $rCDC->{'Freq3'};
    my $agefirst1        = $rCDC->{'Age1'};
    my $agefirst2        = $rCDC->{'Age2'};
    my $agefirst3        = $rCDC->{'Age3'};
    my $levelofcare      = $rCDC->{'LevelOfCare'};
    my $feelingmood      = $rCDC->{'CAR1'};
    my $thinking         = $rCDC->{'CAR2'};
    my $substance        = $rCDC->{'CAR3'};
    my $medical          = $rCDC->{'CAR4'};
    my $family           = $rCDC->{'CAR5'};
    my $interpersonal    = $rCDC->{'CAR6'};
    my $roleperformance  = $rCDC->{'CAR7'};
    my $sociolegal       = $rCDC->{'CAR8'};
    my $selfcare         = $rCDC->{'CAR9'};
    my $asimedical       = $rCDC->{'ASIMedical'};
    my $asiemploy        = $rCDC->{'ASIEmploy'};
    my $asialcohol       = $rCDC->{'ASIAlcohol'};
    my $asidrug          = $rCDC->{'ASIDrug'};
    my $asilegal         = $rCDC->{'ASILegal'};
    my $asifamily        = $rCDC->{'ASIFamily'};
    my $asipsychiatric   = $rCDC->{'ASIPsych'};
    my $currentlof       = $rCDC->{'GAF'};
    my $smi              = $rCDC->{'SMI'};
    my $past30           = $rCDC->{'Arrested30'};
    my $past12           = $rCDC->{'Arrested12'};
    my $past1            = $rCDC->{'SelfHelp30'};
    my $dhscase          = $rCDC->{'FamilyID'};
    my $npi              = $rCDC->{'ClinicianOfRecord'};

    my $pagroup = $rClientPrAuth->{'PAgroup'};
    my $startdate =
      DBUtil->Date( $rClientPrAuth->{'startdate'}, 'fmt', "MMDDYYYY" );
    my $axis1primary1   = $rClientPrAuth->{'axis1primary1'};
    my $axis1primary2   = $rClientPrAuth->{'axis1primary2'};
    my $axis1secondary1 = $rClientPrAuth->{'axis1secondary1'};
    my $axis1secondary2 = $rClientPrAuth->{'axis1secondary2'};
    my $axis1tertiary1  = $rClientPrAuth->{'axis1tertiary1'};
    my $axis1tertiary2  = $rClientPrAuth->{'axis1tertiary2'};
    my $axis2primary1   = $rClientPrAuth->{'axis2primary1'};
    my $axis2primary2   = $rClientPrAuth->{'axis2primary2'};
    my $axis2secondary1 = $rClientPrAuth->{'axis2secondary1'};
    my $axis2secondary2 = $rClientPrAuth->{'axis2secondary2'};
    my $axis3           = $rClientPrAuth->{'Diag3'};
##
##
    # Contact Info
    my $lastname   = $rCDC->{'LastName'};
    my $maidenname = $rCDC->{'MaidenName'};
    my $firstname  = $rCDC->{'FirstName'};
    my $middlename = $rCDC->{'MiddleName'};
    my $suffixname = $rCDC->{'Suffix'};
    my $address1   = $rCDC->{'Addr1'};
    my $address2   = $rCDC->{'Addr2'};
    my $city       = $rCDC->{'City'};
    my $state      = $rCDC->{'State'};
##

    my $xpos         = $marginleft;
    my $ypos_base    = $pageheight - $margintop;
    my $ypos         = $ypos_base;
    my $h_legal      = 17;
    my $h_addr       = 15;
    my $size_sm_rect = 12;
    my $tf;
    my $x;
    my $char;
    my $str;

    $p->begin_page_ext( $pagewidth, $pageheight, "" );

    $p->setlinewidth(2.2);
    $p->set_graphics_option("linejoin=1");
    $p->rect( $marginleft, $marginbottom, $contentwidth, $contentheight );
    $p->stroke();

    ##
    # Create header and footer of first page
    ##
    $p->fit_textline(
        "ODMHSAS/OHCA BEHAVIORAL HEALTH CUSTOMER DATA CORE",
        $pagewidth / 2,
        $ypos + $fontsizesmall,
        $baseboldlargefontoptions . " position={center bottom}"
    );
    $p->fit_textline( "This form is for adults (18+) only.",
        $marginleft, $ypos + 4, $baseboldfontoptions );
    $p->fit_textline(
        "CDC Revised March 21, 2019 by LDR",
        $marginleft + 4,
        $marginbottom - $fontsizemid,
        $basexsmallfontoptions
    );
    $p->fit_textline(
"(*Some codes may be found on the back of the CDC form or check the manual for further information)",
        $pagewidth / 2 - 57,
        $marginbottom - $fontsizemid,
        $basexsmallfontoptions
    );
    ##

    ##
    # Section 1
    ##
    my $h_section1      = 36;
    my $y_section1_half = $ypos - $h_section1 / 2;

    $xpos += 3;
    $p->fit_textline( "SECTION I", $xpos, $ypos - $fontsizelarge,
        $baseboldfontoptions );

    $xpos += 57;
    $p->fit_textline( "Agency:", $xpos, $y_section1_half + 7,
        $baseboldxxsmallfontoptions );
    $p->fit_textline( "Member ID:", $xpos, $y_section1_half - 9,
        $baseboldxxsmallfontoptions );

    $xpos += 52;
    $p->setlinewidth(1.0);
    $p->set_graphics_option("linejoin=1");
    foreach my $i ( 0 .. 9 ) {
        $p->rect(
            $xpos + $i * $size_sm_rect,
            $y_section1_half + 2,
            $size_sm_rect, $size_sm_rect
        );
        $p->stroke();
        $char = substr( $agency, $i, 1 );
        if ( $char ne '' ) {
            $p->fit_textline(
                $char,
                $xpos + $i * $size_sm_rect + 3,
                $y_section1_half + 5,
                $basesmallfontoptions
            );
        }
    }
    foreach my $i ( 0 .. 8 ) {
        $p->rect(
            $xpos + $i * $size_sm_rect,
            $y_section1_half - 2 - $size_sm_rect,
            $size_sm_rect, $size_sm_rect
        );
        $p->stroke();
        $char = substr( $memberid, $i, 1 );
        if ( $char ne '' ) {
            $p->fit_textline(
                $char,
                $xpos + $i * $size_sm_rect + 3,
                $y_section1_half + 1 - $size_sm_rect,
                $basesmallfontoptions
            );
        }
    }

    $xpos += 10 * $size_sm_rect;
    $xpos += 11;
    $p->fit_textline(
        "Date of Transaction (MMDDYYYY):",
        $xpos, $y_section1_half + 7,
        $baseboldxxsmallfontoptions
    );
    $p->fit_textline(
        "Date of Birth (MMDDYYYY):",
        $xpos, $y_section1_half - 9,
        $baseboldxxsmallfontoptions
    );

    $xpos += 103;
    foreach my $i ( 0 .. 7 ) {
        $p->rect(
            $xpos + $i * $size_sm_rect,
            $y_section1_half + 2,
            $size_sm_rect, $size_sm_rect
        );
        $p->rect(
            $xpos + $i * $size_sm_rect,
            $y_section1_half - 2 - $size_sm_rect,
            $size_sm_rect, $size_sm_rect
        );
        $p->stroke();
        $char = substr( $dot, $i, 1 );
        if ( $char ne '' ) {
            $p->fit_textline(
                $char,
                $xpos + $i * $size_sm_rect + 3,
                $y_section1_half + 5,
                $basesmallfontoptions
            );
        }
        $char = substr( $dob, $i, 1 );
        if ( $char ne '' ) {
            $p->fit_textline(
                $char,
                $xpos + $i * $size_sm_rect + 3,
                $y_section1_half + 1 - $size_sm_rect,
                $basesmallfontoptions
            );
        }
    }

    $xpos += 8 * $size_sm_rect;
    $xpos += 22;
    $tf = $p->create_textflow(
        "Transaction Time\n" . "(0000-2359):",
        $baseboldxxsmallfontoptions . " leading=130%"
    );
    $p->fit_textflow( $tf, $xpos, $y_section1_half,
        $xpos + 60, $y_section1_half + 16,
        "verticalalign=bottom" );
    $p->fit_textline(
        "Service Focus*:",
        $xpos, $y_section1_half - 11,
        $baseboldxxsmallfontoptions
    );

    $xpos += 66.5;
    foreach my $i ( 0 .. 3 ) {
        $p->rect(
            $xpos + $i * $size_sm_rect,
            $y_section1_half + 2,
            $size_sm_rect, $size_sm_rect
        );
        $p->stroke();
        $char = substr( $transactiontime, $i, 1 );
        if ( $char ne '' ) {
            $p->fit_textline(
                $char,
                $xpos + $i * $size_sm_rect + 3,
                $y_section1_half + 5,
                $basesmallfontoptions
            );
        }
    }
    $xpos += 2 * $size_sm_rect;
    foreach my $i ( 0 .. 1 ) {
        $p->rect(
            $xpos + $i * $size_sm_rect,
            $y_section1_half - 2 - $size_sm_rect,
            $size_sm_rect, $size_sm_rect
        );
        $p->stroke();
        $char = substr( $sfocus, $i, 1 );
        if ( $char ne '' ) {
            $p->fit_textline(
                $char,
                $xpos + $i * $size_sm_rect + 3,
                $y_section1_half + 1 - $size_sm_rect,
                $basesmallfontoptions
            );
        }
    }

    $xpos += 2 * $size_sm_rect;
    $xpos += 17.5;
    $p->fit_textline( "Transaction Type:*",
        $xpos, $ypos - 9, $baseboldxsmallfontoptions );
    $xpos += 6;
    $tf = $p->create_textflow(
        "(Contacts: 21, 27)\n"
          . "(23, 40, 41, 42)\n"
          . "(60,61,62,63,64,65,66,67,68,69,70,71,72)",
        $basexxsmallfontoptions . " leading=130%"
    );
    $p->fit_textflow(
        $tf, $xpos,
        $ypos - $h_section1 + 4,
        $xpos + 100,
        $ypos - $h_section1 + 30,
        "verticalalign=bottom"
    );

    $xpos += 107;
    foreach my $i ( 0 .. 1 ) {
        $p->rect(
            $xpos + $i * $size_sm_rect,
            $y_section1_half + 2,
            $size_sm_rect, $size_sm_rect
        );
        $p->stroke();
        $char = substr( $transactiontype, $i, 1 );
        if ( $char ne '' ) {
            $p->fit_textline(
                $char,
                $xpos + $i * $size_sm_rect + 3,
                $y_section1_half + 5,
                $basesmallfontoptions
            );
        }
    }
    ##

    ##
    # Race Section
    ##
    $xpos = $marginleft;
    $ypos_base -= $h_section1;
    $ypos = $ypos_base;
    my $h_race       = 63;
    my $w_race_part1 = 233;
    my $w_race_part2 = 102;
    my $w_race_part3 = 121;

    $p->setlinewidth(0.5);
    $p->moveto( $xpos, $ypos );
    $p->lineto( $xpos + $contentwidth, $ypos );
    $p->stroke();

    # Race Part 1
    $ypos -= $fontsizesmall;
    $p->fit_textline( "RACE:", $xpos + 3, $ypos, $baseboldsmallfontoptions );
    $p->fit_textline( "(1=Yes for all that apply; Blank=No)",
        $xpos + 31, $ypos, $basexsmallfontoptions );

    $ypos -= 12;
    $p->setlinewidth(1.0);
    $p->fit_textline( "White", $xpos + 5, $ypos, $basexsmallfontoptions );
    $p->rect( $xpos + 27, $ypos - 3, $size_sm_rect, $size_sm_rect );
    $p->stroke();
    $p->fit_textline( $white, $xpos + 30, $ypos, $basesmallfontoptions );

    $p->fit_textline( "Black/African American",
        $xpos + 53, $ypos, $basexsmallfontoptions );
    $p->rect( $xpos + 134, $ypos - 3, $size_sm_rect, $size_sm_rect );
    $p->stroke();
    $p->fit_textline( $black, $xpos + 137, $ypos, $basesmallfontoptions );

    $p->fit_textline(
        "American Indian",
        $xpos + 157,
        $ypos, $basexsmallfontoptions
    );
    $p->rect( $xpos + 215.5, $ypos - 3, $size_sm_rect, $size_sm_rect );
    $p->stroke();
    $p->fit_textline( $american, $xpos + 218.5, $ypos, $basesmallfontoptions );

    $ypos -= 14;
    $p->fit_textline( "Native Hawaiian or Other Pac. Islander",
        $xpos + 5, $ypos, $basexsmallfontoptions );
    $p->rect( $xpos + 134, $ypos - 4, $size_sm_rect, $size_sm_rect );
    $p->stroke();
    $p->fit_textline( $native, $xpos + 137, $ypos - 1, $basesmallfontoptions );

    $p->fit_textline( "Asian", $xpos + 190, $ypos, $basexsmallfontoptions );
    $p->rect( $xpos + 215.5, $ypos - 4, $size_sm_rect, $size_sm_rect );
    $p->stroke();
    $p->fit_textline( $asian, $xpos + 218.5, $ypos - 1, $basesmallfontoptions );

    $ypos -= 12;
    $p->fit_textline( "Email Address:",
        $xpos + 3, $ypos, $baseboldsmallfontoptions );
    $p->fit_textline( "ETHNICITY:", $xpos + 133,
        $ypos, $baseboldsmallfontoptions );
    $p->fit_textline( "Hispanic/Latino", $xpos + 179,
        $ypos, $basexsmallfontoptions );

    $ypos -= 13.5;
    $p->moveto( $xpos + 4, $ypos );
    $p->lineto( $xpos + 132, $ypos );
    $p->stroke();
    $p->fit_textline( $emailaddress, $xpos + 4, $ypos + 3,
        $basesmallfontoptions );

    $p->fit_textline(
        "(1=Yes; 2=No)",
        $xpos + 152,
        $ypos + 3, $basexsmallfontoptions
    );
    $p->rect( $xpos + 215.5, $ypos - 1, $size_sm_rect, $size_sm_rect );
    $p->stroke();
    $p->fit_textline( $ethnicity, $xpos + 218.5,
        $ypos + 2, $basesmallfontoptions );

    # Race Part 2
    $xpos += $w_race_part1;
    $ypos = $ypos_base;
    $p->moveto( $xpos, $ypos );
    $p->lineto( $xpos, $ypos - $h_race );
    $p->stroke();

    $ypos -= 9;
    $p->fit_textline( "GENDER:", $xpos + 3, $ypos, $baseboldxsmallfontoptions );
    $p->rect( $xpos + 87, $ypos - 7.5, $size_sm_rect, $size_sm_rect );
    $p->stroke();
    $p->fit_textline( $gender, $xpos + 90, $ypos - 5.5, $basesmallfontoptions );

    $ypos -= 9;
    $p->fit_textline( "(F=Female; M=Male)",
        $xpos + 5, $ypos, $basexsmallfontoptions );
    $ypos -= 8;
    $p->fit_textline( "Alert Information:",
        $xpos + 3, $ypos, $baseboldxsmallfontoptions );

    $ypos -= 9;
    $p->moveto( $xpos + 3, $ypos );
    $p->lineto( $xpos + 99, $ypos );
    $p->stroke();
    $p->fit_textline( $alert, $xpos + 3, $ypos + 2, $basexxsmallfontoptions );

    $ypos -= 11;
    $p->fit_textline( "Trauma Score", $xpos + 3, $ypos,
        $basexsmallfontoptions );
    $ypos -= 13;
    $p->fit_textline( "ACE Score", $xpos + 3, $ypos, $basexsmallfontoptions );

    $ypos -= 2;
    foreach my $i ( 0 .. 1 ) {
        $p->rect( $xpos + 87, $ypos + $i * $size_sm_rect,
            $size_sm_rect, $size_sm_rect );
    }
    $p->stroke();
    $p->fit_textline( $traumascore, $xpos + 90, $ypos + 3 + $size_sm_rect,
        $basesmallfontoptions );
    $p->fit_textline( $acescore, $xpos + 90, $ypos + 3, $basesmallfontoptions );

    # Race Part 3
    $xpos += $w_race_part2;
    $ypos = $ypos_base;
    $p->moveto( $xpos, $ypos );
    $p->lineto( $xpos, $ypos - $h_race );
    $p->stroke();

    $ypos -= 10;
    $p->fit_textline( "SCREENS:", $xpos + 5, $ypos, $baseboldsmallfontoptions );
    $p->fit_textline( "(1=Yes; 2=No; 3=NA)",
        $xpos + 50, $ypos + 1, $basexsmallfontoptions );
    $ypos -= 11;
    $p->fit_textline( "Mental Health Screen",
        $xpos + 5, $ypos, $basexsmallfontoptions );
    $ypos -= 12;
    $p->fit_textline( "Substance Abuse Screen",
        $xpos + 5, $ypos, $basexsmallfontoptions );
    $ypos -= 12;
    $p->fit_textline( "Trauma Screen",
        $xpos + 5, $ypos, $basexsmallfontoptions );
    $ypos -= 12;
    $p->fit_textline( "Gambling Screen",
        $xpos + 5, $ypos, $basexsmallfontoptions );
    $ypos -= 3;

    foreach my $i ( 0 .. 3 ) {
        $p->rect( $xpos + 98, $ypos + $i * $size_sm_rect,
            $size_sm_rect, $size_sm_rect );
    }
    $p->stroke();
    $p->fit_textline( "", $xpos + 101, $ypos + 3, $basesmallfontoptions );
    $p->fit_textline(
        $mentalscreen,
        $xpos + 101,
        $ypos + 3 + 3 * $size_sm_rect,
        $basesmallfontoptions
    );
    $p->fit_textline(
        $substancescreen,
        $xpos + 101,
        $ypos + 3 + 2 * $size_sm_rect,
        $basesmallfontoptions
    );
    $p->fit_textline(
        $traumascreen,
        $xpos + 101,
        $ypos + 3 + $size_sm_rect,
        $basesmallfontoptions
    );
    $p->fit_textline( $gamblingscreen, $xpos + 101,
        $ypos + 3, $basesmallfontoptions );

    # Race Part 4
    $xpos += $w_race_part3;
    $ypos = $ypos_base;
    $p->moveto( $xpos, $ypos );
    $p->lineto( $xpos, $ypos - $h_race );
    $p->stroke();

    $ypos -= ( $size_sm_rect + 3 );
    $p->fit_textline( "PRIMARY REFERRAL:*",
        $xpos + 3, $ypos + 4, $baseboldxsmallfontoptions );
    foreach my $i ( 0 .. 1 ) {
        $p->rect( $xpos + 93 + $i * $size_sm_rect,
            $ypos, $size_sm_rect, $size_sm_rect );
        $p->stroke();
        $char = substr( $preferral, $i, 1 );
        if ( $char ne '' ) {
            $p->fit_textline(
                $char,     $xpos + 96 + $i * $size_sm_rect,
                $ypos + 3, $basesmallfontoptions
            );
        }
    }
    $p->fit_textline( "AGENCY #:", $xpos + 121,
        $ypos + 4, $baseboldxsmallfontoptions );
    foreach my $i ( 0 .. 9 ) {
        $p->rect( $xpos + 160 + $i * $size_sm_rect,
            $ypos, $size_sm_rect, $size_sm_rect );
        $p->stroke();
        $char = substr( $pragency, $i, 1 );
        if ( $char ne '' ) {
            $p->fit_textline( $char, $xpos + 163 + $i * $size_sm_rect,
                $ypos + 3, $basesmallfontoptions );
        }
    }

    $ypos -= ( $size_sm_rect + 3 );
    $p->fit_textline( "SECONDARY REFERRAL:*",
        $xpos + 3, $ypos + 4, $baseboldxsmallfontoptions );
    foreach my $i ( 0 .. 1 ) {
        $p->rect( $xpos + 93 + $i * $size_sm_rect,
            $ypos, $size_sm_rect, $size_sm_rect );
        $p->stroke();
        $char = substr( $sreferral, $i, 1 );
        if ( $char ne '' ) {
            $p->fit_textline(
                $char,     $xpos + 96 + $i * $size_sm_rect,
                $ypos + 3, $basesmallfontoptions
            );
        }
    }
    $p->fit_textline( "AGENCY #:", $xpos + 121,
        $ypos + 4, $baseboldxsmallfontoptions );
    foreach my $i ( 0 .. 9 ) {
        $p->rect( $xpos + 160 + $i * $size_sm_rect,
            $ypos, $size_sm_rect, $size_sm_rect );
        $p->stroke();
        $char = substr( $sragency, $i, 1 );
        if ( $char ne '' ) {
            $p->fit_textline( $char, $xpos + 163 + $i * $size_sm_rect,
                $ypos + 3, $basesmallfontoptions );
        }
    }
    $ypos -= ( $size_sm_rect + 4 );
    $p->fit_textline( "COUNTY OF RESIDENCE:",
        $xpos + 3, $ypos + 4, $baseboldxsmallfontoptions );
    $p->fit_textline( "(01-77 or Other State Initials)",
        $xpos + 90, $ypos + 4, $basexsmallfontoptions );
    foreach my $i ( 0 .. 1 ) {
        $p->rect( $xpos + 256 + $i * $size_sm_rect,
            $ypos, $size_sm_rect, $size_sm_rect );
        $p->stroke();
        $char = substr( $countyresidence, $i, 1 );
        if ( $char ne '' ) {
            $p->fit_textline( $char, $xpos + 259 + $i * $size_sm_rect,
                $ypos + 3, $basesmallfontoptions );
        }
    }

    $ypos -= ( $size_sm_rect + 3 );
    $p->fit_textline( "ZIP CODE:", $xpos + 3, $ypos + 6,
        $baseboldxsmallfontoptions );
    $p->fit_textline( "(99999 for Homeless-Streets)",
        $xpos + 40, $ypos + 6, $basexsmallfontoptions );
    foreach my $i ( 0 .. 4 ) {
        $p->rect( $xpos + 157 + $i * $size_sm_rect,
            $ypos, $size_sm_rect, $size_sm_rect );
        $p->stroke();
        $char = substr( $zip1, $i, 1 );
        if ( $char ne '' ) {
            $p->fit_textline( $char, $xpos + 160 + $i * $size_sm_rect,
                $ypos + 3, $basesmallfontoptions );
        }
    }
    $p->moveto( $xpos + 222, $ypos + 6 );
    $p->lineto( $xpos + 227, $ypos + 6 );
    foreach my $i ( 0 .. 3 ) {
        $p->rect( $xpos + 232 + $i * $size_sm_rect,
            $ypos, $size_sm_rect, $size_sm_rect );
        $p->stroke();
        $char = substr( $zip2, $i, 1 );
        if ( $char ne '' ) {
            $p->fit_textline( $char, $xpos + 235 + $i * $size_sm_rect,
                $ypos + 3, $basesmallfontoptions );
        }
    }
    ##

    ##
    # Section 2
    ##
    $xpos = $marginleft;
    $ypos_base -= $h_race;
    $ypos = $ypos_base;
    my $w_section2_part1 = $w_race_part1;
    my $w_section2_part2 = $w_race_part1 + 15;
    my $w_section2_part3 =
      $contentwidth - $w_section2_part1 - $w_section2_part2;
    my $h_section2_part3_pagroup = 247;

    # Section 2 Part 1
    $p->setlinewidth(1.7);
    $p->moveto( $xpos, $ypos );
    $p->lineto( $xpos + $contentwidth, $ypos );
    $p->stroke();

    $ypos -= $fontsize;
    $p->fit_textline( "SECTION II & III",
        $xpos + 4, $ypos, $baseboldfontoptions );

    $ypos -= $fontsizemid;
    $p->fit_textline( "CURRENT RESIDENCE:",
        $xpos + 4, $ypos, $baseboldsmallfontoptions );

    $p->setlinewidth(1.0);
    $p->rect( $xpos + 214, $ypos - 8, $size_sm_rect, $size_sm_rect );
    $p->stroke();
    $p->fit_textline( $residence, $xpos + 217,
        $ypos - 5, $basesmallfontoptions );

    $ypos -= $fontsizemid;
    $p->fit_textline( "A. Permanent Housing",
        $xpos + 7, $ypos, $basexsmallfontoptions );
    $p->fit_textline(
        "F. RC Facility/Group Home",
        $xpos + 115,
        $ypos, $basexsmallfontoptions
    );
    $ypos -= $fontsize;
    $p->fit_textline( "B. Perm Sup Hous-Non-Cong",
        $xpos + 7, $ypos, $basexsmallfontoptions );
    $p->fit_textline(
        "G. Nursing Home",
        $xpos + 115,
        $ypos, $basexsmallfontoptions
    );
    $ypos -= $fontsize;
    $p->fit_textline( "C. Perm Sup Hous-Cong",
        $xpos + 7, $ypos, $basexsmallfontoptions );
    $p->fit_textline(
        "H. Institutional Setting",
        $xpos + 115,
        $ypos, $basexsmallfontoptions
    );
    $ypos -= $fontsize;
    $p->fit_textline( "D. Transitional Housing",
        $xpos + 7, $ypos, $basexsmallfontoptions );
    $p->fit_textline(
        "I. Homeless-Shelter",
        $xpos + 115,
        $ypos, $basexsmallfontoptions
    );
    $ypos -= $fontsize;
    $p->fit_textline( "E. Temporary Housing",
        $xpos + 7, $ypos, $basexsmallfontoptions );
    $p->fit_textline(
        "J. Homeless-Streets",
        $xpos + 115,
        $ypos, $basexsmallfontoptions
    );

    $ypos -= 14;
    $p->fit_textline( "Is customer in PRISON/JAIL?:",
        $xpos + 4, $ypos, $baseboldsmallfontoptions );
    $p->fit_textline(
        "(If 1, Residence must=H)",
        $xpos + 120,
        $ypos, $basesmallfontoptions
    );
    $p->rect( $xpos + 214, $ypos - 7, $size_sm_rect, $size_sm_rect );
    $p->stroke();
    $p->fit_textline( $prison, $xpos + 217, $ypos - 4, $basesmallfontoptions );
    $ypos -= $fontsizemid;
    $p->fit_textline( "1. Prison", $xpos + 7,  $ypos, $basexsmallfontoptions );
    $p->fit_textline( "2. No",     $xpos + 49, $ypos, $basexsmallfontoptions );
    $p->fit_textline( "3. Jail",   $xpos + 81, $ypos, $basexsmallfontoptions );

    $ypos -= 12;
    $p->fit_textline( "LIVING SITUATION:",
        $xpos + 4, $ypos, $baseboldsmallfontoptions );
    $p->rect( $xpos + 95, $ypos - 7, $size_sm_rect, $size_sm_rect );
    $p->stroke();
    $p->fit_textline( $living, $xpos + 98, $ypos - 4, $basesmallfontoptions );
    $p->rect( $xpos + 214, $ypos - 7, $size_sm_rect, $size_sm_rect );
    $p->stroke();
    $p->fit_textline( $chronic, $xpos + 217, $ypos - 4, $basesmallfontoptions );

    $tf = $p->create_textflow( "CHRONIC\n" . "HOMELESSNESS:",
        $baseboldsmallfontoptions . " leading=130%" );
    $p->fit_textflow(
        $tf,        $xpos + 130,
        $ypos - 10, $xpos + 220,
        $ypos + 14, "verticalalign=bottom"
    );
    $p->fit_textline(
        "(1=Yes; 2=No)",
        $xpos + 134,
        $ypos - 20, $basexsmallfontoptions
    );

    $ypos -= $fontsize;
    $p->fit_textline( "1. Alone", $xpos + 7, $ypos, $basexsmallfontoptions );
    $ypos -= $fontsize;
    $p->fit_textline( "2. With Family/Relatives",
        $xpos + 7, $ypos, $basexsmallfontoptions );
    $ypos -= $fontsize;
    $p->fit_textline( "3. With Non-Related Persons",
        $xpos + 7, $ypos, $basexsmallfontoptions );

    $ypos -= 15;
    $p->fit_textline( "EMPLOYMENT:", $xpos + 4, $ypos,
        $baseboldsmallfontoptions );
    $p->rect( $xpos + 214, $ypos, $size_sm_rect, $size_sm_rect );
    $p->stroke();
    $p->fit_textline( $employment, $xpos + 217,
        $ypos + 3, $basesmallfontoptions );
    $ypos -= $fontsize;
    $p->fit_textline( "1. Full-time (35+ hrs.)",
        $xpos + 7, $ypos, $basexsmallfontoptions );
    $p->fit_textline( "3. Unemployed (looking for work in last 30 days)",
        $xpos + 81, $ypos, $basexsmallfontoptions );
    $ypos -= $fontsize;
    $p->fit_textline( "2. Part-time (<35 hrs.)",
        $xpos + 7, $ypos, $basexsmallfontoptions );
    $p->fit_textline( "4. Not in Labor Force = (A-F below)",
        $xpos + 81, $ypos, $basexsmallfontoptions );

    $ypos -= 13;
    $p->fit_textline( "TYPE OF EMPLOYMENT/ Not in Labor Force:",
        $xpos + 4, $ypos, $baseboldsmallfontoptions );
    $p->rect( $xpos + 214, $ypos - 8, $size_sm_rect, $size_sm_rect );
    $p->stroke();
    $p->fit_textline( $typeofemployment, $xpos + 217,
        $ypos - 5, $basesmallfontoptions );
    $ypos -= $fontsizemid;
    $p->fit_textline( "1. Competitive",
        $xpos + 7, $ypos, $basexsmallfontoptions );
    $p->fit_textline( "A. Homemaker", $xpos + 112,
        $ypos, $basexsmallfontoptions );
    $ypos -= $fontsizemid;
    $p->fit_textline( "2. Supported", $xpos + 7, $ypos,
        $basexsmallfontoptions );
    $p->fit_textline( "B. Student", $xpos + 112, $ypos,
        $basexsmallfontoptions );
    $ypos -= $fontsize;
    $p->fit_textline( "3. Volunteer", $xpos + 7, $ypos,
        $basexsmallfontoptions );
    $p->fit_textline( "C. Retired", $xpos + 112, $ypos,
        $basexsmallfontoptions );
    $ypos -= $fontsize;
    $p->fit_textline( "4. None", $xpos + 7, $ypos, $basexsmallfontoptions );
    $p->fit_textline( "D. Disabled", $xpos + 112,
        $ypos, $basexsmallfontoptions );
    $ypos -= $fontsize;
    $p->fit_textline( "5. Transitional",
        $xpos + 7, $ypos, $basexsmallfontoptions );
    $p->fit_textline( "E. Inmate", $xpos + 112, $ypos, $basexsmallfontoptions );
    $ypos -= $fontsize;
    $p->fit_textline( "6. Sheltered Workshop",
        $xpos + 7, $ypos, $basexsmallfontoptions );
    $p->fit_textline( "F. Other", $xpos + 112, $ypos, $basexsmallfontoptions );

    $ypos -= 9;
    $p->fit_textline( "Is customer currently IN SCHOOL?:",
        $xpos + 4, $ypos, $baseboldsmallfontoptions );
    $p->fit_textline(
        "(1=Yes; 2=No)",
        $xpos + 140,
        $ypos, $basesmallfontoptions
    );
    $p->rect( $xpos + 214, $ypos - 4, $size_sm_rect, $size_sm_rect );
    $p->stroke();
    $p->fit_textline( $customerschool, $xpos + 217,
        $ypos - 1, $basesmallfontoptions );

    $ypos -= 2 * $fontsizelarge;
    $tf = $p->create_textflow(
"<fakebold=true>EDUCATION: <fakebold=false>(Highest Grade Completed or Current Grade 00-25) "
          . "<fontsize=$fontsizexsmall>(00-Less Than 1 Grade Completed, GED = 12)",
        $basesmallfontoptions . " leading=130%"
    );
    $p->fit_textflow(
        $tf, $xpos + 4, $ypos,
        $xpos + 200,
        $ypos + 2 * $fontsizelarge,
        "verticalalign=bottom"
    );

    foreach my $i ( 0 .. 1 ) {
        $p->rect( $xpos + 202 + $i * $size_sm_rect,
            $ypos + 2, $size_sm_rect, $size_sm_rect );
        $p->stroke();
        $char = substr( $education, $i, 1 );
        if ( $char ne '' ) {
            $p->fit_textline( $char, $xpos + 205 + $i * $size_sm_rect,
                $ypos + 5, $basesmallfontoptions );
        }
    }

    $ypos -= ( 4 * $fontsizemid - 2 );
    $tf = $p->create_textflow(
        "<fakebold=true>MILITARY STATUS: "
          . "<fontsize=$fontsizexsmall fakebold=false>(A=Client-Currently Active; B=Client-Previously Active; C=Client-National Guard/Reserve; D=Family "
          . "Member-Currently Active; E=Family Member-Previously Active; "
          . "F=Family Member-National Guard/Reserve; G=None)",
        $basesmallfontoptions . " leading=135%"
    );
    $p->fit_textflow(
        $tf, $xpos + 4, $ypos,
        $xpos + 200,
        $ypos + 4 * $fontsizemid,
        "verticalalign=bottom"
    );
    $p->rect( $xpos + 214, $ypos + 23, $size_sm_rect, $size_sm_rect );
    $p->stroke();
    $p->fit_textline( $militarystatus, $xpos + 217,
        $ypos + 26, $basesmallfontoptions );

    $ypos -= 13;
    $p->fit_textline( "MARITAL STATUS:",
        $xpos + 4, $ypos, $baseboldsmallfontoptions );
    $p->rect( $xpos + 214, $ypos - 6, $size_sm_rect, $size_sm_rect );
    $p->stroke();
    $p->fit_textline( $maritalstatus, $xpos + 217,
        $ypos - 3, $basesmallfontoptions );
    $ypos -= $fontsizemid;
    $p->fit_textline( "1. Never Married",
        $xpos + 7, $ypos, $basexsmallfontoptions );
    $p->fit_textline( "3. Divorced", $xpos + 76, $ypos,
        $basexsmallfontoptions );
    $p->fit_textline(
        "5. Living as Married",
        $xpos + 148,
        $ypos, $basexsmallfontoptions
    );
    $ypos -= $fontsize;
    $p->fit_textline( "2. Married", $xpos + 7,  $ypos, $basexsmallfontoptions );
    $p->fit_textline( "4. Widowed", $xpos + 76, $ypos, $basexsmallfontoptions );
    $p->fit_textline( "6. Separated", $xpos + 148,
        $ypos, $basexsmallfontoptions );

    $ypos -= 10;
    $p->fit_textline( "Is customer PREGNANT?:",
        $xpos + 4, $ypos, $baseboldsmallfontoptions );
    $p->fit_textline(
        "(1=Yes; 2=No)",
        $xpos + 105,
        $ypos, $basesmallfontoptions
    );
    $p->rect( $xpos + 214, $ypos - 1, $size_sm_rect, $size_sm_rect );
    $p->stroke();
    $p->fit_textline( $customerpreg, $xpos + 217,
        $ypos + 2, $basesmallfontoptions );

    $ypos -= 2 * $fontsizemid;
    $tf = $p->create_textflow(
        "<fontsize=$fontsizexsmall>If Yes enter expected DOB, blank if No "
          . "<fontsize=$fontsizesmall>(MMDDYYYY)",
        $basesmallfontoptions . " leading=120%"
    );
    $p->fit_textflow(
        $tf, $xpos + 4, $ypos,
        $xpos + 128,
        $ypos + 2 * $fontsizemid,
        "verticalalign=bottom"
    );

    foreach my $i ( 0 .. 7 ) {
        $p->rect( $xpos + 130 + $i * $size_sm_rect,
            $ypos + 4, $size_sm_rect, $size_sm_rect );
        $p->stroke();
        $char = substr( $pregnantdob, $i, 1 );
        if ( $char ne '' ) {
            $p->fit_textline( $char, $xpos + 133 + $i * $size_sm_rect,
                $ypos + 7, $basesmallfontoptions );
        }
    }

    $ypos -= 9;
    $p->fit_textline( "ANNUAL INCOME:",
        $xpos + 4, $ypos, $baseboldsmallfontoptions );
    $p->fit_textline( "\$", $xpos + 142, $ypos, $baseboldsmallfontoptions );
    foreach my $i ( 0 .. 5 ) {
        $p->rect( $xpos + 154 + $i * $size_sm_rect,
            $ypos - 3, $size_sm_rect, $size_sm_rect );
        $p->stroke();
        $char = substr( $annualincome, $i, 1 );
        if ( $char ne '' ) {
            $p->fit_textline(
                $char, $xpos + 157 + $i * $size_sm_rect,
                $ypos, $basesmallfontoptions
            );
        }
    }

    $ypos -= 13;
    $p->fit_textline( "Number contributing to and/or dependent upon",
        $xpos + 4, $ypos, $basesmallfontoptions );
    foreach my $i ( 0 .. 1 ) {
        $p->rect( $xpos + 202 + $i * $size_sm_rect,
            $ypos - 6, $size_sm_rect, $size_sm_rect );
        $p->stroke();
        $char = substr( $number, $i, 1 );
        if ( $char ne '' ) {
            $p->fit_textline( $char, $xpos + 205 + $i * $size_sm_rect,
                $ypos - 3, $basesmallfontoptions );
        }
    }

    $ypos -= $fontsizelarge;
    $p->fit_textline( "“Annual Income” above: (01-15)",
        $xpos + 4, $ypos, $basesmallfontoptions );

    $ypos -= $fontsizelarge;
    $p->fit_textline( "SSI:", $xpos + 40, $ypos, $baseboldsmallfontoptions );
    $p->rect( $xpos + 64, $ypos - 4, $size_sm_rect, $size_sm_rect );
    $p->stroke();
    $p->fit_textline( $ssi, $xpos + 67, $ypos - 1, $basesmallfontoptions );
    $p->fit_textline( "(1=Yes; 2=No)",
        $xpos + 86, $ypos, $basesmallfontoptions );
    $p->fit_textline( "SSDI:", $xpos + 163, $ypos, $baseboldsmallfontoptions );
    $p->rect( $xpos + 193, $ypos - 4, $size_sm_rect, $size_sm_rect );
    $p->stroke();
    $p->fit_textline( $ssdi, $xpos + 196, $ypos - 1, $basesmallfontoptions );

    # Section 2 Part 2
    $xpos += $w_section2_part1;
    $ypos = $ypos_base;
    $p->setlinewidth(0.5);
    $p->moveto( $xpos, $ypos );
    $p->lineto( $xpos, $marginbottom + $h_legal + $h_addr );
    $p->stroke();

    $ypos -= $fontsizelarge;
    $p->fit_textline( "LANGUAGE PROFICIENCY:",
        $xpos + 4, $ypos, $baseboldsmallfontoptions );

    $ypos -= $fontsizemid;
    $p->fit_textline( "What language is preferred?:",
        $xpos + 4, $ypos, $baseboldxsmallfontoptions );
    $p->fit_textline( "(0-9)", $xpos + 102, $ypos, $basexsmallfontoptions );
    $p->setlinewidth(1.0);
    $p->rect( $xpos + 231.5, $ypos - 1, $size_sm_rect, $size_sm_rect );
    $p->stroke();
    $p->fit_textline( $custother, $xpos + 234.5,
        $ypos + 2, $basesmallfontoptions );

    $ypos -= $fontsizemid;
    $p->fit_textline( "Does customer speak English well?:",
        $xpos + 4, $ypos, $baseboldxsmallfontoptions );
    $p->fit_textline(
        "(1=Yes; 2=No)",
        $xpos + 126,
        $ypos, $basexsmallfontoptions
    );
    $p->rect( $xpos + 231.5, $ypos - 5, $size_sm_rect, $size_sm_rect );
    $p->stroke();
    $p->fit_textline( $custenglish, $xpos + 234.5,
        $ypos - 2, $basesmallfontoptions );

    $ypos -= 24;
    $p->fit_textline( "DISABILITY:", $xpos + 4, $ypos,
        $baseboldsmallfontoptions );
    $p->fit_textline( "(01-11 or Blank)",
        $xpos + 53, $ypos, $basesmallfontoptions );
    $x = $xpos + 122;
    foreach my $i ( 0 .. 7 ) {
        $x += $size_sm_rect;
        $x += 4.5 if $i % 2 eq 0 && $i > 0;
        $p->rect( $x, $ypos - 4, $size_sm_rect, $size_sm_rect );
        $p->stroke();
        $str = '';
        if ( $i < 2 ) {
            $str = $disability1;
        }
        elsif ( $i < 4 ) {
            $str = $disability2;
        }
        elsif ( $i < 6 ) {
            $str = $disability3;
        }
        else {
            $str = $disability4;
        }
        $char = substr( $str, $i % 2, 1 );
        if ( $char ne '' ) {
            $p->fit_textline( $char, $x + 3, $ypos - 1, $basesmallfontoptions );
        }
    }

    $ypos -= 2 * $fontsize;
    $p->fit_textline( "LEGAL STATUS:*",
        $xpos + 4, $ypos, $baseboldsmallfontoptions );
    foreach my $i ( 0 .. 1 ) {
        $p->rect( $xpos + 78.5 + $i * $size_sm_rect,
            $ypos - 1, $size_sm_rect, $size_sm_rect );
        $p->stroke();
        $char = substr( $legalstatus, $i, 1 );
        if ( $char ne '' ) {
            $p->fit_textline( $char, $xpos + 81.5 + $i * $size_sm_rect,
                $ypos + 2, $basesmallfontoptions );
        }
    }
    $p->fit_textline(
        "(01,03,05,07,09,12,13,15,17,20,21)",
        $xpos + 8, $ypos - $fontsize,
        $basexxsmallfontoptions
    );
    $p->fit_textline(
        "County of Commitment:",
        $xpos + 113,
        $ypos, $baseboldsmallfontoptions
    );
    foreach my $i ( 0 .. 1 ) {
        $p->rect( $xpos + 219.5 + $i * $size_sm_rect,
            $ypos - 1, $size_sm_rect, $size_sm_rect );
        $p->stroke();
        $char = substr( $countryc, $i, 1 );
        if ( $char ne '' ) {
            $p->fit_textline( $char, $xpos + 222.5 + $i * $size_sm_rect,
                $ypos + 2, $basesmallfontoptions );
        }
    }
    $tf = $p->create_textflow(
        "(If Legal Status = 01 or 17, County of Commitment not required)",
        $basexsmallfontoptions . " leading=120%" );
    $p->fit_textflow(
        $tf,
        $xpos + 118,
        $ypos - 2 * $fontsize,
        $xpos + 243,
        $ypos, "verticalalign=bottom"
    );

    $ypos -= ( 2 * $fontsizexxlarge - 1 );
    $p->fit_textline( "TOBACCO USE:", $xpos + 4, $ypos,
        $baseboldsmallfontoptions );
    $p->fit_textline( "Times tobacco used on a typical day (00-99)",
        $xpos + 64, $ypos, $basexsmallfontoptions );
    foreach my $i ( 0 .. 1 ) {
        $p->rect( $xpos + 219.5 + $i * $size_sm_rect,
            $ypos - 3, $size_sm_rect, $size_sm_rect );
        $p->stroke();
        $char = substr( $tobaccouse, $i, 1 );
        if ( $char ne '' ) {
            $p->fit_textline(
                $char, $xpos + 222.5 + $i * $size_sm_rect,
                $ypos, $basesmallfontoptions
            );
        }
    }
    $ypos -= $fontsizexlarge;
    $p->fit_textline( "Primary", $xpos + 128,
        $ypos, $baseboldxsmallfontoptions );
    $p->fit_textline( "Secondary", $xpos + 168,
        $ypos, $baseboldxsmallfontoptions );
    $p->fit_textline( "Tertiary", $xpos + 209,
        $ypos, $baseboldxsmallfontoptions );

    $ypos -= 2;

    $ypos -= $size_sm_rect;
    $p->fit_textline( "PRESENTING PROBLEM:*",
        $xpos + 4, $ypos + 3, $baseboldsmallfontoptions );
    $x = $xpos + 114.5;
    foreach my $i ( 0 .. 8 ) {
        $x += $size_sm_rect;
        $x += 4.5 if $i % 3 eq 0 && $i > 0;
        $p->rect( $x, $ypos, $size_sm_rect, $size_sm_rect );
        $p->stroke();
        $str = '';
        if ( $i < 3 ) {
            $str = $presentingprblm1;
        }
        elsif ( $i < 6 ) {
            $str = $presentingprblm2;
        }
        else {
            $str = $presentingprblm3;
        }
        $char = substr( $str, $i % 3, 1 );
        if ( $char ne '' ) {
            $p->fit_textline( $char, $x + 3, $ypos + 3, $basesmallfontoptions );
        }
    }

    $ypos -= $size_sm_rect;
    $p->fit_textline(
        "Drugs of Choice:",
        $xpos + 7, $ypos + 4.5,
        $baseboldxsmallfontoptions
    );
    $p->fit_textline(
        "(01-21)*",
        $xpos + 65.5,
        $ypos + 4.5,
        $basexsmallfontoptions
    );
    $x = $xpos + 126.5;
    foreach my $i ( 0 .. 5 ) {
        $x += $size_sm_rect;
        $x += 16.5 if $i % 2 eq 0 && $i > 0;
        $p->rect( $x, $ypos, $size_sm_rect, $size_sm_rect );
        $p->stroke();
        $str = '';
        if ( $i < 2 ) {
            $str = $drugs1;
        }
        elsif ( $i < 4 ) {
            $str = $drugs2;
        }
        else {
            $str = $drugs3;
        }
        $char = substr( $str, $i % 2, 1 );
        if ( $char ne '' ) {
            $p->fit_textline( $char, $x + 3, $ypos + 3, $basesmallfontoptions );
        }
    }

    $ypos -= $size_sm_rect;
    $p->fit_textline(
        "Usual Route of Administration:*",
        $xpos + 7, $ypos + 4.5,
        $baseboldxsmallfontoptions
    );
    $p->fit_textline(
        "(1-5)",
        $xpos + 164.5,
        $ypos + 4.5,
        $baseboldxsmallfontoptions
    );
    $p->fit_textline(
        "(1-5)",
        $xpos + 205,
        $ypos + 4.5,
        $baseboldxsmallfontoptions
    );
    $x = $xpos + 150.5;
    foreach my $i ( 0 .. 2 ) {
        $p->rect( $x, $ypos, $size_sm_rect, $size_sm_rect );
        $p->stroke();
        $str = '';
        if ( $i == 0 ) {
            $str = $route1;
        }
        elsif ( $i == 1 ) {
            $str = $route2;
        }
        else {
            $str = $route3;
        }
        $p->fit_textline( $str, $x + 3, $ypos + 3, $basesmallfontoptions );
        $x += ( 3 * $size_sm_rect + 4.5 );
    }

    $ypos -= $size_sm_rect;
    $p->fit_textline(
        "Frequency of Use in Last 30 days:*",
        $xpos + 7, $ypos + 4.5,
        $baseboldxsmallfontoptions
    );
    $p->fit_textline(
        "(1-5)",
        $xpos + 164.5,
        $ypos + 4.5,
        $baseboldxsmallfontoptions
    );
    $p->fit_textline(
        "(1-5)",
        $xpos + 205,
        $ypos + 4.5,
        $baseboldxsmallfontoptions
    );
    $x = $xpos + 150.5;
    foreach my $i ( 0 .. 2 ) {
        $p->rect( $x, $ypos, $size_sm_rect, $size_sm_rect );
        $p->stroke();
        $str = '';
        if ( $i == 0 ) {
            $str = $frequency1;
        }
        elsif ( $i == 1 ) {
            $str = $frequency2;
        }
        else {
            $str = $frequency3;
        }
        $p->fit_textline( $str, $x + 3, $ypos + 3, $basesmallfontoptions );
        $x += ( 3 * $size_sm_rect + 4.5 );
    }

    $ypos -= $size_sm_rect;
    $p->fit_textline(
        "Age First Used: (00-99)",
        $xpos + 7, $ypos + 4.5,
        $baseboldxsmallfontoptions
    );
    $x = $xpos + 126.5;
    foreach my $i ( 0 .. 5 ) {
        $x += $size_sm_rect;
        $x += 16.5 if $i % 2 eq 0 && $i > 0;
        $p->rect( $x, $ypos, $size_sm_rect, $size_sm_rect );
        $p->stroke();
        $str = '';
        if ( $i < 2 ) {
            $str = $agefirst1;
        }
        elsif ( $i < 4 ) {
            $str = $agefirst2;
        }
        else {
            $str = $agefirst3;
        }
        $char = substr( $str, $i % 2, 1 );
        if ( $char ne '' ) {
            $p->fit_textline( $char, $x + 3, $ypos + 3, $basesmallfontoptions );
        }
    }

    $ypos -= 3;

    $ypos -= $size_sm_rect;
    $p->fit_textline(
        "LEVEL OF CARE: ",
        $xpos + 4, $ypos + 3.5,
        $baseboldsmallfontoptions
    );
    $p->fit_textline(
        "(CI, CL, HA, OO, SC, or SN)*",
        $xpos + 68, $ypos + 3.5,
        $basesmallfontoptions
    );
    foreach my $i ( 0 .. 1 ) {
        $p->rect( $xpos + 219.5 + $i * $size_sm_rect,
            $ypos, $size_sm_rect, $size_sm_rect );
        $p->stroke();
        $char = substr( $levelofcare, $i, 1 );
        if ( $char ne '' ) {
            $p->fit_textline( $char, $xpos + 222.5 + $i * $size_sm_rect,
                $ypos + 3, $basesmallfontoptions );
        }
    }

    $ypos -= $fontsizemid;
    $p->fit_textline( "CAR: (Mental Health)",
        $xpos + 4, $ypos, $baseboldsmallfontoptions );
    $p->fit_textline( "(01-50)", $xpos + 114.5,
        $ypos + 1, $baseboldxsmallfontoptions );

    $p->rect( $xpos + 150, $ypos - 81.5, 95, 74 );
    $p->stroke();
    $tf = $p->create_textflow(
        "<fakebold=true>Note:\n"
          . "<fakebold=false>If CAR:Substance Use is scored 30 "
          . "or above, the customer should be "
          . "referred for a substance abuse "
          . "assessment.\n"
          . "If ASI/TASI:Psychiatric Status is "
          . "scored 4 or above, the customer "
          . "should be referred for a mental "
          . "health assessment.",
        $basexxsmallfontoptions
    );
    $p->fit_textflow(
        $tf,
        $xpos + 151,
        $ypos - 79.5,
        $xpos + 244,
        $ypos - 7.5,
        "verticalalign=justify"
    );

    $ypos -= 2;

    $ypos -= $size_sm_rect;
    $p->fit_textline( "Feeling Mood", $xpos + 7, $ypos + 3,
        $baseboldxsmallfontoptions );
    foreach my $i ( 0 .. 1 ) {
        $p->rect( $xpos + 113 + $i * $size_sm_rect,
            $ypos, $size_sm_rect, $size_sm_rect );
        $p->stroke();
        $char = substr( $feelingmood, $i, 1 );
        if ( $char ne '' ) {
            $p->fit_textline( $char, $xpos + 116 + $i * $size_sm_rect,
                $ypos + 3, $basesmallfontoptions );
        }
    }

    $ypos -= $size_sm_rect;
    $p->fit_textline( "Thinking", $xpos + 7, $ypos + 3,
        $baseboldxsmallfontoptions );
    foreach my $i ( 0 .. 1 ) {
        $p->rect( $xpos + 113 + $i * $size_sm_rect,
            $ypos, $size_sm_rect, $size_sm_rect );
        $p->stroke();
        $char = substr( $thinking, $i, 1 );
        if ( $char ne '' ) {
            $p->fit_textline( $char, $xpos + 116 + $i * $size_sm_rect,
                $ypos + 3, $basesmallfontoptions );
        }
    }

    $ypos -= $size_sm_rect;
    $p->fit_textline( "Substance Use",
        $xpos + 7, $ypos + 3, $baseboldxsmallfontoptions );
    foreach my $i ( 0 .. 1 ) {
        $p->rect( $xpos + 113 + $i * $size_sm_rect,
            $ypos, $size_sm_rect, $size_sm_rect );
        $p->stroke();
        $char = substr( $substance, $i, 1 );
        if ( $char ne '' ) {
            $p->fit_textline( $char, $xpos + 116 + $i * $size_sm_rect,
                $ypos + 3, $basesmallfontoptions );
        }
    }

    $ypos -= $size_sm_rect;
    $p->fit_textline( "Medical/Physical", $xpos + 7, $ypos + 3,
        $baseboldxsmallfontoptions );
    foreach my $i ( 0 .. 1 ) {
        $p->rect( $xpos + 113 + $i * $size_sm_rect,
            $ypos, $size_sm_rect, $size_sm_rect );
        $p->stroke();
        $char = substr( $medical, $i, 1 );
        if ( $char ne '' ) {
            $p->fit_textline( $char, $xpos + 116 + $i * $size_sm_rect,
                $ypos + 3, $basesmallfontoptions );
        }
    }

    $ypos -= $size_sm_rect;
    $p->fit_textline( "Family", $xpos + 7, $ypos + 3,
        $baseboldxsmallfontoptions );
    foreach my $i ( 0 .. 1 ) {
        $p->rect( $xpos + 113 + $i * $size_sm_rect,
            $ypos, $size_sm_rect, $size_sm_rect );
        $p->stroke();
        $char = substr( $family, $i, 1 );
        if ( $char ne '' ) {
            $p->fit_textline( $char, $xpos + 116 + $i * $size_sm_rect,
                $ypos + 3, $basesmallfontoptions );
        }
    }

    $ypos -= $size_sm_rect;
    $p->fit_textline( "Interpersonal", $xpos + 7, $ypos + 3,
        $baseboldxsmallfontoptions );
    foreach my $i ( 0 .. 1 ) {
        $p->rect( $xpos + 113 + $i * $size_sm_rect,
            $ypos, $size_sm_rect, $size_sm_rect );
        $p->stroke();
        $char = substr( $interpersonal, $i, 1 );
        if ( $char ne '' ) {
            $p->fit_textline( $char, $xpos + 116 + $i * $size_sm_rect,
                $ypos + 3, $basesmallfontoptions );
        }
    }

    $ypos -= $size_sm_rect;
    $p->fit_textline( "Role Performance",
        $xpos + 7, $ypos + 3, $baseboldxsmallfontoptions );
    foreach my $i ( 0 .. 1 ) {
        $p->rect( $xpos + 113 + $i * $size_sm_rect,
            $ypos, $size_sm_rect, $size_sm_rect );
        $p->stroke();
        $char = substr( $roleperformance, $i, 1 );
        if ( $char ne '' ) {
            $p->fit_textline( $char, $xpos + 116 + $i * $size_sm_rect,
                $ypos + 3, $basesmallfontoptions );
        }
    }

    $ypos -= $size_sm_rect;
    $p->fit_textline( "Socio-Legal", $xpos + 7, $ypos + 3,
        $baseboldxsmallfontoptions );
    foreach my $i ( 0 .. 1 ) {
        $p->rect( $xpos + 113 + $i * $size_sm_rect,
            $ypos, $size_sm_rect, $size_sm_rect );
        $p->stroke();
        $char = substr( $sociolegal, $i, 1 );
        if ( $char ne '' ) {
            $p->fit_textline( $char, $xpos + 116 + $i * $size_sm_rect,
                $ypos + 3, $basesmallfontoptions );
        }
    }

    $ypos -= $size_sm_rect;
    $p->fit_textline( "Self Care/Basic Needs",
        $xpos + 7, $ypos + 3, $baseboldxsmallfontoptions );
    foreach my $i ( 0 .. 1 ) {
        $p->rect( $xpos + 113 + $i * $size_sm_rect,
            $ypos, $size_sm_rect, $size_sm_rect );
        $p->stroke();
        $char = substr( $selfcare, $i, 1 );
        if ( $char ne '' ) {
            $p->fit_textline( $char, $xpos + 116 + $i * $size_sm_rect,
                $ypos + 3, $basesmallfontoptions );
        }
    }

    $ypos -= $fontsizelarge;
    $p->fit_textline( "ASI: (Substance Abuse)",
        $xpos + 4, $ypos, $baseboldsmallfontoptions );
    $p->fit_textline( "(0-9)", $xpos + 95.5, $ypos, $basexsmallfontoptions );

    $ypos -= 3;

    $ypos -= $size_sm_rect;
    $p->fit_textline( "Medical", $xpos + 7, $ypos + 3,
        $baseboldxsmallfontoptions );
    $p->rect( $xpos + 107, $ypos, $size_sm_rect, $size_sm_rect );
    $p->stroke();
    $p->fit_textline( $asimedical, $xpos + 110,
        $ypos + 3, $basesmallfontoptions );

    $ypos -= $size_sm_rect;
    $p->fit_textline( "Employ/Support", $xpos + 7, $ypos + 3,
        $baseboldxsmallfontoptions );
    $p->rect( $xpos + 107, $ypos, $size_sm_rect, $size_sm_rect );
    $p->stroke();
    $p->fit_textline( $asiemploy, $xpos + 110,
        $ypos + 3, $basesmallfontoptions );

    $ypos -= $size_sm_rect;
    $p->fit_textline( "Alcohol Use", $xpos + 7, $ypos + 3,
        $baseboldxsmallfontoptions );
    $p->rect( $xpos + 107, $ypos, $size_sm_rect, $size_sm_rect );
    $p->stroke();
    $p->fit_textline( $asialcohol, $xpos + 110,
        $ypos + 3, $basesmallfontoptions );

    $ypos -= $size_sm_rect;
    $p->fit_textline( "Drug Use", $xpos + 7, $ypos + 3,
        $baseboldxsmallfontoptions );
    $p->rect( $xpos + 107, $ypos, $size_sm_rect, $size_sm_rect );
    $p->stroke();
    $p->fit_textline( $asidrug, $xpos + 110, $ypos + 3, $basesmallfontoptions );

    $ypos -= $size_sm_rect;
    $p->fit_textline( "Legal Status", $xpos + 7, $ypos + 3,
        $baseboldxsmallfontoptions );
    $p->rect( $xpos + 107, $ypos, $size_sm_rect, $size_sm_rect );
    $p->stroke();
    $p->fit_textline( $asilegal, $xpos + 110, $ypos + 3,
        $basesmallfontoptions );

    $ypos -= $size_sm_rect;
    $p->fit_textline( "Family/Social Rel.",
        $xpos + 7, $ypos + 3, $baseboldxsmallfontoptions );
    $p->rect( $xpos + 107, $ypos, $size_sm_rect, $size_sm_rect );
    $p->stroke();
    $p->fit_textline( $asifamily, $xpos + 110,
        $ypos + 3, $basesmallfontoptions );

    $ypos -= $size_sm_rect;
    $p->fit_textline( "Psychiatric Status",
        $xpos + 7, $ypos + 3, $baseboldxsmallfontoptions );
    $p->rect( $xpos + 107, $ypos, $size_sm_rect, $size_sm_rect );
    $p->stroke();
    $p->fit_textline( $asipsychiatric, $xpos + 110,
        $ypos + 3, $basesmallfontoptions );

    # Section 2 Part 3
    $xpos += $w_section2_part2;
    $ypos = $ypos_base;
    $p->moveto( $xpos, $ypos );
    $p->lineto( $xpos, $marginbottom + $h_legal + $h_addr );
    $p->stroke();

    $ypos -= 35;
    $tf = $p->create_textflow(
        "SMI: <fakebold=false fontsize=$fontsizexsmall>(1=Yes; 2=No)\n"
          . "<fakebold=true fontsize=$fontsizesmall>(For customer 18 and older)",
        $baseboldsmallfontoptions . " leading=130%"
    );
    $p->fit_textflow( $tf, $xpos + 5, $ypos, $xpos + 110,
        $ypos + 25, "verticalalign=bottom" );
    $p->rect( $xpos + 118, $ypos + 0.5, $size_sm_rect, $size_sm_rect );
    $p->stroke();
    $p->fit_textline( $smi, $xpos + 121, $ypos + 3.5, $basesmallfontoptions );

    $ypos -= 22;
    $tf = $p->create_textflow(
"In the <underline=true underlineposition=-20%>past 30 days<underline=false>, how many <underline=true underlineposition=-20%>times<underline=false> has the customer been "
          . "<underline=true underlineposition=-20%>arrested<underline=false>, or since admission if less than 30 days ago? (00-99)",
        $basexsmallfontoptions . " leading=130%"
    );
    $p->fit_textflow( $tf, $xpos + 5, $ypos, $xpos + 210,
        $ypos + 20, "verticalalign=bottom" );

    foreach my $i ( 0 .. 1 ) {
        $p->rect( $xpos + 229 + $i * $size_sm_rect,
            $ypos + 1, $size_sm_rect, $size_sm_rect );
        $p->stroke();
        $char = substr( $past30, $i, 1 );
        if ( $char ne '' ) {
            $p->fit_textline( $char, $xpos + 232 + $i * $size_sm_rect,
                $ypos + 4, $basesmallfontoptions );
        }
    }

    $ypos -= 25;
    $tf = $p->create_textflow(
"In the <underline=true underlineposition=-20%>past 12 months<underline=false>, how many <underline=true underlineposition=-20%>times<underline=false> has the customer been "
          . "<underline=true underlineposition=-20%>arrested<underline=false>, or since admission if less than 12 months ago? (00-99)",
        $basexsmallfontoptions . " leading=130%"
    );
    $p->fit_textflow( $tf, $xpos + 5, $ypos, $xpos + 210,
        $ypos + 20, "verticalalign=bottom" );
    foreach my $i ( 0 .. 1 ) {
        $p->rect( $xpos + 229 + $i * $size_sm_rect,
            $ypos + 1, $size_sm_rect, $size_sm_rect );
        $p->stroke();
        $char = substr( $past12, $i, 1 );
        if ( $char ne '' ) {
            $p->fit_textline( $char, $xpos + 232 + $i * $size_sm_rect,
                $ypos + 4, $basesmallfontoptions );
        }
    }

    $ypos -= 33;
    $tf = $p->create_textflow(
"In the <underline=true underlineposition=-20%>past 30 days<underline=false>, how many <underline=true underlineposition=-20%>times<underline=false> has the customer <underline=true underlineposition=-20%>attended "
          . "self-help/support groups<underline=false>, or since admission if less than 30 days "
          . "ago? (00-99)",
        $basexsmallfontoptions . " leading=130%"
    );
    $p->fit_textflow( $tf, $xpos + 5, $ypos, $xpos + 210,
        $ypos + 28, "verticalalign=bottom" );
    foreach my $i ( 0 .. 1 ) {
        $p->rect( $xpos + 229 + $i * $size_sm_rect,
            $ypos + 11, $size_sm_rect, $size_sm_rect );
        $p->stroke();
        $char = substr( $past1, $i, 1 );
        if ( $char ne '' ) {
            $p->fit_textline( $char, $xpos + 232 + $i * $size_sm_rect,
                $ypos + 14, $basesmallfontoptions );
        }
    }

    $ypos -= 2 * $fontsizexlarge;
    $tf = $p->create_textflow(
        "FAMILY ID,\n" . "DOC # or DHS Case Number:",
        $baseboldsmallfontoptions . " leading=130%"
    );
    $p->fit_textflow( $tf, $xpos + 5, $ypos, $xpos + 130,
        $ypos + 24, "verticalalign=bottom" );
    foreach my $i ( 0 .. 9 ) {
        $p->rect( $xpos + 133 + $i * $size_sm_rect,
            $ypos, $size_sm_rect, $size_sm_rect );
        $p->stroke();
        $char = substr( $dhscase, $i, 1 );
        if ( $char ne '' ) {
            $p->fit_textline( $char, $xpos + 136 + $i * $size_sm_rect,
                $ypos + 3, $basesmallfontoptions );
        }
    }

    $ypos -= ( 2 * $fontsizemid - 1 );
    $p->fit_textline( "CLINICIAN OF RECORD (NPI):",
        $xpos + 5, $ypos + 3, $baseboldsmallfontoptions );
    foreach my $i ( 0 .. 9 ) {
        $p->rect( $xpos + 133 + $i * $size_sm_rect,
            $ypos, $size_sm_rect, $size_sm_rect );
        $p->stroke();
        $char = substr( $npi, $i, 1 );
        if ( $char ne '' ) {
            $p->fit_textline( $char, $xpos + 136 + $i * $size_sm_rect,
                $ypos + 3, $basesmallfontoptions );
        }
    }

    ## PA Group

    $ypos = $marginbottom + $h_legal + $h_addr + $h_section2_part3_pagroup;
    $p->setlinewidth(1.7);
    $p->set_graphics_option("linejoin=1");
    $p->rect( $xpos, $ypos - $h_section2_part3_pagroup,
        $w_section2_part3, $h_section2_part3_pagroup );
    $p->stroke();

    $ypos -= $fontsizexlarge;
    $p->fit_textline( "PA GROUP:", $xpos + 5, $ypos,
        $baseboldsmallfontoptions );
    $p->setlinewidth(1.2);
    $p->moveto( $xpos + 51.5, $ypos - 2 );
    $p->lineto( $xpos + 150, $ypos - 2 );
    $p->stroke();
    $p->fit_textline( $pagroup, $xpos + 51.5,
        $ypos + 1, $basexsmallfontoptions );

    $ypos -= 14.5;
    $p->fit_textline( "Start Date (MMDDYYYY):",
        $xpos + 5, $ypos, $baseboldsmallfontoptions );
    foreach my $i ( 0 .. 7 ) {
        $p->rect( $xpos + 110 + $i * $size_sm_rect,
            $ypos - 4, $size_sm_rect, $size_sm_rect );
        $p->stroke();
        $char = substr( $startdate, $i, 1 );
        if ( $char ne '' ) {
            $p->fit_textline( $char, $xpos + 113 + $i * $size_sm_rect,
                $ypos - 1, $basesmallfontoptions );
        }
    }

    $ypos -= 16;
    $p->fit_textline( "Diagnoses: ICD-10 Codes",
        $xpos + 5, $ypos, $baseboldsmallfontoptions );

    $ypos -= 19;
    $x = $xpos + 32;
    foreach my $i ( 0 .. 2 ) {
        $p->rect( $x + $i * $size_sm_rect, $ypos, $size_sm_rect,
            $size_sm_rect );
        $p->stroke();
        $char = substr( $axis1primary1, $i, 1 );
        if ( $char ne '' ) {
            $p->fit_textline(
                $char,     $x + 3 + $i * $size_sm_rect,
                $ypos + 3, $basesmallfontoptions
            );
        }
    }

    $x += ( 3 * $size_sm_rect + 8 );
    $p->set_graphics_option("linejoin=0");
    $p->rect( $x - 3.7, $ypos - 0.5, 3, 3 );
    $p->fill();
    $p->set_graphics_option("linejoin=1");
    foreach my $i ( 0 .. 1 ) {
        $p->rect( $x + $i * $size_sm_rect, $ypos, $size_sm_rect,
            $size_sm_rect );
        $p->stroke();
        $char = substr( $axis1primary2, $i, 1 );
        if ( $char ne '' ) {
            $p->fit_textline(
                $char,     $x + 3 + $i * $size_sm_rect,
                $ypos + 3, $basesmallfontoptions
            );
        }
    }

    $x += ( 2 * $size_sm_rect + 8 );
    foreach my $i ( 0 .. 2 ) {
        $p->rect( $x + $i * $size_sm_rect, $ypos, $size_sm_rect,
            $size_sm_rect );
        $p->stroke();
        $char = substr( $axis1secondary1, $i, 1 );
        if ( $char ne '' ) {
            $p->fit_textline(
                $char,     $x + 3 + $i * $size_sm_rect,
                $ypos + 3, $basesmallfontoptions
            );
        }
    }

    $x += ( 3 * $size_sm_rect + 8 );
    $p->set_graphics_option("linejoin=0");
    $p->rect( $x - 3.7, $ypos - 0.5, 3, 3 );
    $p->fill();
    $p->set_graphics_option("linejoin=1");
    foreach my $i ( 0 .. 1 ) {
        $p->rect( $x + $i * $size_sm_rect, $ypos, $size_sm_rect,
            $size_sm_rect );
        $p->stroke();
        $char = substr( $axis1secondary2, $i, 1 );
        if ( $char ne '' ) {
            $p->fit_textline(
                $char,     $x + 3 + $i * $size_sm_rect,
                $ypos + 3, $basesmallfontoptions
            );
        }
    }

    $x += ( 2 * $size_sm_rect + 8 );
    foreach my $i ( 0 .. 2 ) {
        $p->rect( $x + $i * $size_sm_rect, $ypos, $size_sm_rect,
            $size_sm_rect );
        $p->stroke();
        $char = substr( $axis1tertiary1, $i, 1 );
        if ( $char ne '' ) {
            $p->fit_textline(
                $char,     $x + 3 + $i * $size_sm_rect,
                $ypos + 3, $basesmallfontoptions
            );
        }
    }

    $x += ( 3 * $size_sm_rect + 8 );
    $p->set_graphics_option("linejoin=0");
    $p->rect( $x - 3.7, $ypos - 0.5, 3, 3 );
    $p->fill();
    $p->set_graphics_option("linejoin=1");
    foreach my $i ( 0 .. 1 ) {
        $p->rect( $x + $i * $size_sm_rect, $ypos, $size_sm_rect,
            $size_sm_rect );
        $p->stroke();
        $char = substr( $axis1tertiary2, $i, 1 );
        if ( $char ne '' ) {
            $p->fit_textline(
                $char,     $x + 3 + $i * $size_sm_rect,
                $ypos + 3, $basesmallfontoptions
            );
        }
    }

    $ypos -= 20;

    $x = $xpos + 32;
    foreach my $i ( 0 .. 2 ) {
        $p->rect( $x + $i * $size_sm_rect, $ypos, $size_sm_rect,
            $size_sm_rect );
        $p->stroke();
        $char = substr( $axis2primary1, $i, 1 );
        if ( $char ne '' ) {
            $p->fit_textline(
                $char,     $x + 3 + $i * $size_sm_rect,
                $ypos + 3, $basesmallfontoptions
            );
        }
    }

    $x += ( 3 * $size_sm_rect + 8 );
    $p->set_graphics_option("linejoin=0");
    $p->rect( $x - 3.7, $ypos - 0.5, 3, 3 );
    $p->fill();
    $p->set_graphics_option("linejoin=1");
    foreach my $i ( 0 .. 1 ) {
        $p->rect( $x + $i * $size_sm_rect, $ypos, $size_sm_rect,
            $size_sm_rect );
        $p->stroke();
        $char = substr( $axis2primary2, $i, 1 );
        if ( $char ne '' ) {
            $p->fit_textline(
                $char,     $x + 3 + $i * $size_sm_rect,
                $ypos + 3, $basesmallfontoptions
            );
        }
    }

    $x += ( 2 * $size_sm_rect + 8 );
    foreach my $i ( 0 .. 2 ) {
        $p->rect( $x + $i * $size_sm_rect, $ypos, $size_sm_rect,
            $size_sm_rect );
        $p->stroke();
        $char = substr( $axis2secondary1, $i, 1 );
        if ( $char ne '' ) {
            $p->fit_textline(
                $char,     $x + 3 + $i * $size_sm_rect,
                $ypos + 3, $basesmallfontoptions
            );
        }
    }

    $x += ( 3 * $size_sm_rect + 8 );
    $p->set_graphics_option("linejoin=0");
    $p->rect( $x - 3.7, $ypos - 0.5, 3, 3 );
    $p->fill();
    $p->set_graphics_option("linejoin=1");
    foreach my $i ( 0 .. 1 ) {
        $p->rect( $x + $i * $size_sm_rect, $ypos, $size_sm_rect,
            $size_sm_rect );
        $p->stroke();
        $char = substr( $axis2secondary2, $i, 1 );
        if ( $char ne '' ) {
            $p->fit_textline(
                $char,     $x + 3 + $i * $size_sm_rect,
                $ypos + 3, $basesmallfontoptions
            );
        }
    }

    $ypos -= 14.5;
    $p->fit_textline( "Medical", $xpos + 5, $ypos, $baseboldsmallfontoptions );

    $p->rect( $xpos + 5.5, $ypos - 76, 245, 72 );
    $p->stroke();
    $tf =
      $p->create_textflow( $axis3, $basexxsmallfontoptions . " leading=130%" );
    $p->fit_textflow( $tf, $xpos + 8, $ypos - 74, $xpos + 248,
        $ypos - 5, "verticalalign=top" );

    $p->fit_textline(
        "This form is for adults (18+) only.",
        $xpos + 4, $marginbottom + $h_addr + $h_legal + 5,
        $baseboldfontoptions
    );

    ##

    ##
    # LEGAL NAME AND ADDRESS SECTION
    ##
    $xpos      = $marginleft;
    $ypos_base = $marginbottom + $h_legal + $h_addr;
    $ypos      = $ypos_base;
    $p->setlinewidth(2.0);
    $p->moveto( $marginleft, $ypos );
    $p->lineto( $marginleft + $contentwidth, $ypos );
    $p->stroke();

    $ypos -= 12;
    $p->fit_textline( "LEGAL NAME:", $xpos + 3, $ypos, $baseboldfontoptions );
    $p->fit_textline( "Last:",   $xpos + 72,    $ypos, $basexsmallfontoptions );
    $p->fit_textline( $lastname, $xpos + 90,    $ypos, $basexsmallfontoptions );

    $xpos += $w_section2_part1;
    $p->fit_textline( "Maiden:", $xpos + 21.5,  $ypos, $basexsmallfontoptions );
    $p->fit_textline( $maidenname, $xpos + 50,  $ypos, $basexsmallfontoptions );
    $p->fit_textline( "First:",    $xpos + 166, $ypos, $basexsmallfontoptions );
    $p->fit_textline( $firstname,  $xpos + 184, $ypos, $basexsmallfontoptions );

    $xpos += $w_section2_part2;
    $p->fit_textline( "Middle:",   $xpos + 98,  $ypos, $basexsmallfontoptions );
    $p->fit_textline( $middlename, $xpos + 124, $ypos, $basexsmallfontoptions );
    $p->fit_textline( "Suffix:",   $xpos + 206, $ypos, $basexsmallfontoptions );
    $p->fit_textline( $suffixname, $xpos + 228, $ypos, $basexsmallfontoptions );

    $xpos = $marginleft;
    $ypos_base -= $h_legal;
    $ypos = $ypos_base;
    $p->setlinewidth(1.2);
    $p->moveto( $marginleft, $ypos );
    $p->lineto( $marginleft + $contentwidth, $ypos );
    $p->stroke();

    $ypos -= 10.5;
    $p->fit_textline( "ADDRESS:", $xpos + 3,  $ypos, $baseboldfontoptions );
    $p->fit_textline( "(1)",      $xpos + 50, $ypos, $basesmallfontoptions );
    $p->fit_textline( $address1,  $xpos + 63, $ypos, $basesmallfontoptions );

    $xpos += $w_section2_part1;
    $p->fit_textline( "(2)",     $xpos + 93,  $ypos, $basesmallfontoptions );
    $p->fit_textline( $address2, $xpos + 106, $ypos, $basesmallfontoptions );

    $xpos += $w_section2_part2;
    $p->fit_textline( "CITY:",  $xpos + 6,   $ypos, $baseboldsmallfontoptions );
    $p->fit_textline( $city,    $xpos + 30,  $ypos, $basesmallfontoptions );
    $p->fit_textline( "STATE:", $xpos + 170, $ypos, $baseboldsmallfontoptions );
    $p->fit_textline( $state,   $xpos + 200, $ypos, $basesmallfontoptions );
    ##

    $p->end_page_ext("");
}

sub Child {
    my ( $self, $p, $rCDC, $rClientPrAuth ) = @_;

##
    # Header info...
    my $AgencyID = MgrTree->getAgency( $form, $rCDC->{ClinicID} );
    $sProvider->execute($AgencyID)
      || myDBI->dberror("select Provider: $AgencyID");
    my $rAgency    = $sProvider->fetchrow_hashref;
    my $AgencyName = $rAgency->{Name};
    my $AgencyAddr = $rAgency->{Addr1} . ', ';
    $AgencyAddr .= $rAgency->{Addr2} . ', ' if ( $rAgency->{Addr2} );
    $AgencyAddr .=
      $rAgency->{City} . ', ' . $rAgency->{ST} . '  ' . $rAgency->{Zip};
    my $AgencyPh = 'Office: ' . $rAgency->{WkPh} . '  Fax: ' . $rAgency->{Fax};
##

##
    # Section 1 variables
    my $agency = $rCDC->{'AgencySite'};
    my $dot    = DBUtil->Date( $rCDC->{'TransDate'}, 'fmt', "MMDDYYYY" );
    my $transactiontime = main->convertDateTime( $rCDC->{'TransTime'} );
    my $transactiontype = $rCDC->{'TransType'};
    my $memberid        = $rCDC->{'InsIDNum'};
    my $dob      = DBUtil->Date( $rCDC->{'DateOfBirth'}, 'fmt', "MMDDYYYY" );
    my $sfocus   = $rCDC->{'ServiceFocus'};
    my $white    = $rCDC->{'RaceWhite'};
    my $black    = $rCDC->{'RaceBlack'};
    my $american = $rCDC->{'Race'};
    my $native   = $rCDC->{'RaceIndian'};
    my $asian    = $rCDC->{'RaceAsian'};
    my $emailaddress    = $rCDC->{'Email'};
    my $ethnicity       = $rCDC->{'EthnicHispanic'};
    my $gender          = $rCDC->{'Gend'};
    my $alert           = $rCDC->{'alertinfo'};
    my $traumascore     = $rCDC->{'traumaScore'};
    my $mentalscreen    = $rCDC->{'MHScreen'};
    my $substancescreen = $rCDC->{'SAScreen'};
    my $traumascreen    = $rCDC->{'TraumaScreen'};
    my $gamblingscreen  = $rCDC->{'GamblingScreen'};
    my $preferral       = $rCDC->{'PriReferralType'};
    my $pragency        = $rCDC->{'PriReferralNPI'};
    my $sreferral       = $rCDC->{'SecReferralType'};
    my $sragency        = $rCDC->{'SecReferralNPI'};
    my $countyresidence = $rCDC->{'CountyofRes'};
    my $zip1            = $rCDC->{'zip1'};
    my $zip2            = $rCDC->{'zip2'};
##
##
    # Section 2 Variables
    my $residence        = $rCDC->{'CurrentResidence'};
    my $living           = $rCDC->{'LivingSituation'};
    my $chronic          = $rCDC->{'chronic'};
    my $employment       = $rCDC->{'EmplStat'};
    my $typeofemployment = $rCDC->{'EmplType'};
    my $customerschool   = $rCDC->{'customerschool'};
    my $education        = $rCDC->{'Education'};
    my $militarystatus   = $rCDC->{'MilitaryStatus'};
    my $customerpreg     = $rCDC->{'customerpreg'};
    my $pregnantdob =
      DBUtil->Date( $rCDC->{'PregnantDate'}, 'fmt', "MMDDYYYY" );
    my $number           = $rCDC->{'IncomeDeps'};
    my $ssi              = $rCDC->{'SSI'};
    my $custother        = $rCDC->{'LangOther'};
    my $custenglish      = $rCDC->{'custenglish'};
    my $disability1      = $rCDC->{'Handicap1'};
    my $disability2      = $rCDC->{'Handicap2'};
    my $disability3      = $rCDC->{'Handicap3'};
    my $disability4      = $rCDC->{'Handicap4'};
    my $countryc         = $rCDC->{'CommitmentCounty'};
    my $tobaccouse       = $rCDC->{'TobaccoUse'};
    my $presentingprblm1 = $rCDC->{'Problem1'};
    my $presentingprblm2 = $rCDC->{'Problem2'};
    my $presentingprblm3 = $rCDC->{'Problem3'};
    my $drugs1           = $rCDC->{'Drug1'};
    my $drugs2           = $rCDC->{'Drug2'};
    my $drugs3           = $rCDC->{'Drug3'};
    my $route1           = $rCDC->{'Route1'};
    my $route2           = $rCDC->{'Route2'};
    my $route3           = $rCDC->{'Route3'};
    my $frequency1       = $rCDC->{'Freq1'};
    my $frequency2       = $rCDC->{'Freq2'};
    my $frequency3       = $rCDC->{'Freq3'};
    my $agefirst1        = $rCDC->{'Age1'};
    my $agefirst2        = $rCDC->{'Age2'};
    my $agefirst3        = $rCDC->{'Age3'};
    my $levelofcare      = $rCDC->{'LevelOfCare'};
    my $feelingmood      = $rCDC->{'CAR1'};
    my $thinking         = $rCDC->{'CAR2'};
    my $substance        = $rCDC->{'CAR3'};
    my $medical          = $rCDC->{'CAR4'};
    my $family           = $rCDC->{'CAR5'};
    my $interpersonal    = $rCDC->{'CAR6'};
    my $roleperformance  = $rCDC->{'CAR7'};
    my $sociolegal       = $rCDC->{'CAR8'};
    my $selfcare         = $rCDC->{'CAR9'};
    my $tasichemical     = $rCDC->{'TASIChemical'};
    my $tasischool       = $rCDC->{'TASISchool'};
    my $tasiemp          = $rCDC->{'TASIEmploy'};
    my $tasifamily       = $rCDC->{'TASIFamily'};
    my $tasipeer         = $rCDC->{'TASIPeer'};
    my $tasilegal        = $rCDC->{'TASILegal'};
    my $tasipsychiatric  = $rCDC->{'TASIPsych'};
    my $sed              = $rCDC->{'SED'};
    my $past30           = $rCDC->{'Arrested30'};
    my $past12           = $rCDC->{'Arrested12'};
    my $past1            = $rCDC->{'SelfHelp30'};
    my $dhscase          = $rCDC->{'FamilyID'};
    my $npi              = $rCDC->{'ClinicianOfRecord'};
    my $outofhome        = $rCDC->{'Placement'};
    my $past901          = $rCDC->{'RestrictivePlacement'};
    my $past902          = $rCDC->{'SelfHarm'};
    my $past903          = $rCDC->{'AbsentSchool'};
    my $past904          = $rCDC->{'SuspendedSchool'};
    my $past905          = $rCDC->{'AbsentDayCare'};

    my $pagroup = $rClientPrAuth->{'PAgroup'};
    my $startdate =
      DBUtil->Date( $rClientPrAuth->{'startdate'}, 'fmt', "MMDDYYYY" );
    my $axis1primary1   = $rClientPrAuth->{'axis1primary1'};
    my $axis1primary2   = $rClientPrAuth->{'axis1primary2'};
    my $axis1secondary1 = $rClientPrAuth->{'axis1secondary1'};
    my $axis1secondary2 = $rClientPrAuth->{'axis1secondary2'};
    my $axis1tertiary1  = $rClientPrAuth->{'axis1tertiary1'};
    my $axis1tertiary2  = $rClientPrAuth->{'axis1tertiary2'};
    my $axis2primary1   = $rClientPrAuth->{'axis2primary1'};
    my $axis2primary2   = $rClientPrAuth->{'axis2primary2'};
    my $axis2secondary1 = $rClientPrAuth->{'axis2secondary1'};
    my $axis2secondary2 = $rClientPrAuth->{'axis2secondary2'};
    my $axis3           = $rClientPrAuth->{'Diag3'};
##
##
    # Contact Info
    my $lastname   = $rCDC->{'LastName'};
    my $maidenname = $rCDC->{'MaidenName'};
    my $firstname  = $rCDC->{'FirstName'};
    my $middlename = $rCDC->{'MiddleName'};
    my $suffixname = $rCDC->{'Suffix'};
    my $address1   = $rCDC->{'Addr1'};
    my $address2   = $rCDC->{'Addr2'};
    my $city       = $rCDC->{'City'};
    my $state      = $rCDC->{'State'};
##

    my $xpos         = $marginleft;
    my $ypos_base    = $pageheight - $margintop;
    my $ypos         = $ypos_base;
    my $h_legal      = 17;
    my $h_addr       = 15;
    my $size_sm_rect = 12;
    my $tf;
    my $x;
    my $y;
    my $char;
    my $str;

    $p->begin_page_ext( $pagewidth, $pageheight, "" );

    $p->setlinewidth(2.2);
    $p->set_graphics_option("linejoin=1");
    $p->rect( $marginleft, $marginbottom, $contentwidth, $contentheight );
    $p->stroke();

    ##
    # Create header and footer of first page
    ##
    $p->fit_textline(
        "ODMHSAS/OHCA BEHAVIORAL HEALTH CUSTOMER DATA CORE",
        $pagewidth / 2,
        $ypos + $fontsizesmall,
        $baseboldlargefontoptions . " position={center bottom}"
    );
    $p->fit_textline( "This form is for Children only.",
        $marginleft, $ypos + 4, $basefontoptions );
    $p->fit_textline(
        "CDC Revised June 28, 2016 by LDR",
        $marginleft + 4,
        $marginbottom - $fontsizemid,
        $basexsmallfontoptions
    );
    $p->fit_textline(
"(*Some codes may be found on the back of the CDC form or check the manual for further information)",
        $pagewidth / 2 - 57,
        $marginbottom - $fontsizemid,
        $basexsmallfontoptions
    );
    ##

    ##
    # Section 1
    ##
    my $h_section1      = 36;
    my $y_section1_half = $ypos - $h_section1 / 2;

    $xpos += 3;
    $p->fit_textline( "SECTION I", $xpos, $ypos - $fontsizelarge,
        $baseboldfontoptions );

    $xpos += 57;
    $p->fit_textline( "Agency:", $xpos, $y_section1_half + 7,
        $baseboldxxsmallfontoptions );
    $p->fit_textline( "Member ID:", $xpos, $y_section1_half - 9,
        $baseboldxxsmallfontoptions );

    $xpos += 52;
    $p->setlinewidth(1.0);
    $p->set_graphics_option("linejoin=1");
    foreach my $i ( 0 .. 9 ) {
        $p->rect(
            $xpos + $i * $size_sm_rect,
            $y_section1_half + 2,
            $size_sm_rect, $size_sm_rect
        );
        $p->stroke();
        $char = substr( $agency, $i, 1 );
        if ( $char ne '' ) {
            $p->fit_textline(
                $char,
                $xpos + $i * $size_sm_rect + 3,
                $y_section1_half + 5,
                $basesmallfontoptions
            );
        }
    }
    foreach my $i ( 0 .. 8 ) {
        $p->rect(
            $xpos + $i * $size_sm_rect,
            $y_section1_half - 2 - $size_sm_rect,
            $size_sm_rect, $size_sm_rect
        );
        $p->stroke();
        $char = substr( $memberid, $i, 1 );
        if ( $char ne '' ) {
            $p->fit_textline(
                $char,
                $xpos + $i * $size_sm_rect + 3,
                $y_section1_half + 1 - $size_sm_rect,
                $basesmallfontoptions
            );
        }
    }

    $xpos += 10 * $size_sm_rect;
    $xpos += 11;
    $p->fit_textline(
        "Date of Transaction (MMDDYYYY):",
        $xpos, $y_section1_half + 7,
        $baseboldxxsmallfontoptions
    );
    $p->fit_textline(
        "Date of Birth (MMDDYYYY):",
        $xpos, $y_section1_half - 9,
        $baseboldxxsmallfontoptions
    );

    $xpos += 103;
    foreach my $i ( 0 .. 7 ) {
        $p->rect(
            $xpos + $i * $size_sm_rect,
            $y_section1_half + 2,
            $size_sm_rect, $size_sm_rect
        );
        $p->rect(
            $xpos + $i * $size_sm_rect,
            $y_section1_half - 2 - $size_sm_rect,
            $size_sm_rect, $size_sm_rect
        );
        $p->stroke();
        $char = substr( $dot, $i, 1 );
        if ( $char ne '' ) {
            $p->fit_textline(
                $char,
                $xpos + $i * $size_sm_rect + 3,
                $y_section1_half + 5,
                $basesmallfontoptions
            );
        }
        $char = substr( $dob, $i, 1 );
        if ( $char ne '' ) {
            $p->fit_textline(
                $char,
                $xpos + $i * $size_sm_rect + 3,
                $y_section1_half + 1 - $size_sm_rect,
                $basesmallfontoptions
            );
        }
    }

    $xpos += 8 * $size_sm_rect;
    $xpos += 22;
    $tf = $p->create_textflow(
        "Transaction Time\n" . "(0000-2359):",
        $baseboldxxsmallfontoptions . " leading=130%"
    );
    $p->fit_textflow( $tf, $xpos, $y_section1_half,
        $xpos + 60, $y_section1_half + 16,
        "verticalalign=bottom" );
    $p->fit_textline(
        "Service Focus*:",
        $xpos, $y_section1_half - 11,
        $baseboldxxsmallfontoptions
    );

    $xpos += 66.5;
    foreach my $i ( 0 .. 3 ) {
        $p->rect(
            $xpos + $i * $size_sm_rect,
            $y_section1_half + 2,
            $size_sm_rect, $size_sm_rect
        );
        $p->stroke();
        $char = substr( $transactiontime, $i, 1 );
        if ( $char ne '' ) {
            $p->fit_textline(
                $char,
                $xpos + $i * $size_sm_rect + 3,
                $y_section1_half + 5,
                $basesmallfontoptions
            );
        }
    }
    $xpos += 2 * $size_sm_rect;
    foreach my $i ( 0 .. 1 ) {
        $p->rect(
            $xpos + $i * $size_sm_rect,
            $y_section1_half - 2 - $size_sm_rect,
            $size_sm_rect, $size_sm_rect
        );
        $p->stroke();
        $char = substr( $sfocus, $i, 1 );
        if ( $char ne '' ) {
            $p->fit_textline(
                $char,
                $xpos + $i * $size_sm_rect + 3,
                $y_section1_half + 1 - $size_sm_rect,
                $basesmallfontoptions
            );
        }
    }

    $xpos += 2 * $size_sm_rect;
    $xpos += 17.5;
    $p->fit_textline( "Transaction Type:*",
        $xpos, $ypos - 9, $baseboldxsmallfontoptions );
    $xpos += 6;
    $tf = $p->create_textflow(
        "(Contacts: 21, 27)\n"
          . "(23, 40, 41, 42)\n"
          . "(60,61,62,63,64,65,66,67,68,69,70,71,72)",
        $basexxsmallfontoptions . " leading=130%"
    );
    $p->fit_textflow(
        $tf, $xpos,
        $ypos - $h_section1 + 4,
        $xpos + 100,
        $ypos - $h_section1 + 30,
        "verticalalign=bottom"
    );

    $xpos += 107;
    foreach my $i ( 0 .. 1 ) {
        $p->rect(
            $xpos + $i * $size_sm_rect,
            $y_section1_half + 2,
            $size_sm_rect, $size_sm_rect
        );
        $p->stroke();
        $char = substr( $transactiontype, $i, 1 );
        if ( $char ne '' ) {
            $p->fit_textline(
                $char,
                $xpos + $i * $size_sm_rect + 3,
                $y_section1_half + 5,
                $basesmallfontoptions
            );
        }
    }
    ##

    ##
    # Race Section
    ##
    $xpos = $marginleft;
    $ypos_base -= $h_section1;
    $ypos = $ypos_base;
    my $h_race       = 63;
    my $w_race_part1 = 233;
    my $w_race_part2 = 102;
    my $w_race_part3 = 121;

    $p->setlinewidth(0.5);
    $p->moveto( $xpos, $ypos );
    $p->lineto( $xpos + $contentwidth, $ypos );
    $p->stroke();

    # Race Part 1
    $ypos -= $fontsizesmall;
    $p->fit_textline( "RACE:", $xpos + 3, $ypos, $baseboldsmallfontoptions );
    $p->fit_textline( "(1=Yes for all that apply; Blank=No)",
        $xpos + 31, $ypos, $basexsmallfontoptions );

    $ypos -= 12;
    $p->setlinewidth(1.0);
    $p->fit_textline( "White", $xpos + 5, $ypos, $basexsmallfontoptions );
    $p->rect( $xpos + 27, $ypos - 3, $size_sm_rect, $size_sm_rect );
    $p->stroke();
    $p->fit_textline( $white, $xpos + 30, $ypos, $basesmallfontoptions );

    $p->fit_textline( "Black/African American",
        $xpos + 53, $ypos, $basexsmallfontoptions );
    $p->rect( $xpos + 134, $ypos - 3, $size_sm_rect, $size_sm_rect );
    $p->stroke();
    $p->fit_textline( $black, $xpos + 137, $ypos, $basesmallfontoptions );

    $p->fit_textline(
        "American Indian",
        $xpos + 157,
        $ypos, $basexsmallfontoptions
    );
    $p->rect( $xpos + 215.5, $ypos - 3, $size_sm_rect, $size_sm_rect );
    $p->stroke();
    $p->fit_textline( $american, $xpos + 218.5, $ypos, $basesmallfontoptions );

    $ypos -= 14;
    $p->fit_textline( "Native Hawaiian or Other Pac. Islander",
        $xpos + 5, $ypos, $basexsmallfontoptions );
    $p->rect( $xpos + 134, $ypos - 4, $size_sm_rect, $size_sm_rect );
    $p->stroke();
    $p->fit_textline( $native, $xpos + 137, $ypos - 1, $basesmallfontoptions );

    $p->fit_textline( "Asian", $xpos + 190, $ypos, $basexsmallfontoptions );
    $p->rect( $xpos + 215.5, $ypos - 4, $size_sm_rect, $size_sm_rect );
    $p->stroke();
    $p->fit_textline( $asian, $xpos + 218.5, $ypos - 1, $basesmallfontoptions );

    $ypos -= 12;
    $p->fit_textline( "Email Address:",
        $xpos + 3, $ypos, $baseboldsmallfontoptions );
    $p->fit_textline( "ETHNICITY:", $xpos + 133,
        $ypos, $baseboldsmallfontoptions );
    $p->fit_textline( "Hispanic/Latino", $xpos + 179,
        $ypos, $basexsmallfontoptions );

    $ypos -= 13.5;
    $p->moveto( $xpos + 4, $ypos );
    $p->lineto( $xpos + 132, $ypos );
    $p->stroke();
    $p->fit_textline( $emailaddress, $xpos + 4, $ypos + 3,
        $basesmallfontoptions );

    $p->fit_textline(
        "(1=Yes; 2=No)",
        $xpos + 152,
        $ypos + 3, $basexsmallfontoptions
    );
    $p->rect( $xpos + 215.5, $ypos - 1, $size_sm_rect, $size_sm_rect );
    $p->stroke();
    $p->fit_textline( $ethnicity, $xpos + 218.5,
        $ypos + 2, $basesmallfontoptions );

    # Race Part 2
    $xpos += $w_race_part1;
    $ypos = $ypos_base;
    $p->moveto( $xpos, $ypos );
    $p->lineto( $xpos, $ypos - $h_race );
    $p->stroke();

    $ypos -= 9;
    $p->fit_textline( "GENDER:", $xpos + 3, $ypos, $baseboldxsmallfontoptions );
    $p->rect( $xpos + 87, $ypos - 7.5, $size_sm_rect, $size_sm_rect );
    $p->stroke();
    $p->fit_textline( $gender, $xpos + 90, $ypos - 5.5, $basesmallfontoptions );

    $ypos -= 9;
    $p->fit_textline( "(F=Female; M=Male)",
        $xpos + 5, $ypos, $basexsmallfontoptions );
    $ypos -= 18;
    $p->fit_textline( "Alert Information:",
        $xpos + 3, $ypos, $baseboldxsmallfontoptions );

    $ypos -= 9;
    $p->moveto( $xpos + 3, $ypos );
    $p->lineto( $xpos + 99, $ypos );
    $p->stroke();
    $p->fit_textline( $alert, $xpos + 3, $ypos + 2, $basexxsmallfontoptions );

    $ypos -= 11;
    $p->fit_textline( "Trauma Score", $xpos + 3, $ypos,
        $basexsmallfontoptions );

    $ypos -= 4;
    $p->rect( $xpos + 87, $ypos, $size_sm_rect, $size_sm_rect );
    $p->stroke();
    $p->fit_textline( $traumascore, $xpos + 90, $ypos + 3,
        $basesmallfontoptions );

    # Race Part 3
    $xpos += $w_race_part2;
    $ypos = $ypos_base;
    $p->moveto( $xpos, $ypos );
    $p->lineto( $xpos, $ypos - $h_race );
    $p->stroke();

    $ypos -= 10;
    $p->fit_textline( "SCREENS:", $xpos + 5, $ypos, $baseboldsmallfontoptions );
    $p->fit_textline( "(1=Yes; 2=No; 3=NA)",
        $xpos + 50, $ypos + 1, $basexsmallfontoptions );
    $ypos -= 11;
    $p->fit_textline( "Mental Health Screen",
        $xpos + 5, $ypos, $basexsmallfontoptions );
    $ypos -= 12;
    $p->fit_textline( "Substance Abuse Screen",
        $xpos + 5, $ypos, $basexsmallfontoptions );
    $ypos -= 12;
    $p->fit_textline( "Trauma Screen",
        $xpos + 5, $ypos, $basexsmallfontoptions );
    $ypos -= 12;
    $p->fit_textline( "Gambling Screen",
        $xpos + 5, $ypos, $basexsmallfontoptions );
    $ypos -= 3;

    foreach my $i ( 0 .. 3 ) {
        $p->rect( $xpos + 98, $ypos + $i * $size_sm_rect,
            $size_sm_rect, $size_sm_rect );
    }
    $p->stroke();
    $p->fit_textline( "", $xpos + 101, $ypos + 3, $basesmallfontoptions );
    $p->fit_textline(
        $mentalscreen,
        $xpos + 101,
        $ypos + 3 + 3 * $size_sm_rect,
        $basesmallfontoptions
    );
    $p->fit_textline(
        $substancescreen,
        $xpos + 101,
        $ypos + 3 + 2 * $size_sm_rect,
        $basesmallfontoptions
    );
    $p->fit_textline(
        $traumascreen,
        $xpos + 101,
        $ypos + 3 + $size_sm_rect,
        $basesmallfontoptions
    );
    $p->fit_textline( $gamblingscreen, $xpos + 101,
        $ypos + 3, $basesmallfontoptions );

    # Race Part 4
    $xpos += $w_race_part3;
    $ypos = $ypos_base;
    $p->moveto( $xpos, $ypos );
    $p->lineto( $xpos, $ypos - $h_race );
    $p->stroke();

    $ypos -= ( $size_sm_rect + 3 );
    $p->fit_textline( "PRIMARY REFERRAL:*",
        $xpos + 3, $ypos + 4, $baseboldxsmallfontoptions );
    foreach my $i ( 0 .. 1 ) {
        $p->rect( $xpos + 93 + $i * $size_sm_rect,
            $ypos, $size_sm_rect, $size_sm_rect );
        $p->stroke();
        $char = substr( $preferral, $i, 1 );
        if ( $char ne '' ) {
            $p->fit_textline(
                $char,     $xpos + 96 + $i * $size_sm_rect,
                $ypos + 3, $basesmallfontoptions
            );
        }
    }
    $p->fit_textline( "AGENCY #:", $xpos + 121,
        $ypos + 4, $baseboldxsmallfontoptions );
    foreach my $i ( 0 .. 9 ) {
        $p->rect( $xpos + 160 + $i * $size_sm_rect,
            $ypos, $size_sm_rect, $size_sm_rect );
        $p->stroke();
        $char = substr( $pragency, $i, 1 );
        if ( $char ne '' ) {
            $p->fit_textline( $char, $xpos + 163 + $i * $size_sm_rect,
                $ypos + 3, $basesmallfontoptions );
        }
    }

    $ypos -= ( $size_sm_rect + 3 );
    $p->fit_textline( "SECONDARY REFERRAL:*",
        $xpos + 3, $ypos + 4, $baseboldxsmallfontoptions );
    foreach my $i ( 0 .. 1 ) {
        $p->rect( $xpos + 93 + $i * $size_sm_rect,
            $ypos, $size_sm_rect, $size_sm_rect );
        $p->stroke();
        $char = substr( $sreferral, $i, 1 );
        if ( $char ne '' ) {
            $p->fit_textline(
                $char,     $xpos + 96 + $i * $size_sm_rect,
                $ypos + 3, $basesmallfontoptions
            );
        }
    }
    $p->fit_textline( "AGENCY #:", $xpos + 121,
        $ypos + 4, $baseboldxsmallfontoptions );
    foreach my $i ( 0 .. 9 ) {
        $p->rect( $xpos + 160 + $i * $size_sm_rect,
            $ypos, $size_sm_rect, $size_sm_rect );
        $p->stroke();
        $char = substr( $sragency, $i, 1 );
        if ( $char ne '' ) {
            $p->fit_textline( $char, $xpos + 163 + $i * $size_sm_rect,
                $ypos + 3, $basesmallfontoptions );
        }
    }
    $ypos -= ( $size_sm_rect + 4 );
    $p->fit_textline( "COUNTY OF RESIDENCE:",
        $xpos + 3, $ypos + 4, $baseboldxsmallfontoptions );
    $p->fit_textline( "(01-77 or Other State Initials)",
        $xpos + 90, $ypos + 4, $basexsmallfontoptions );
    foreach my $i ( 0 .. 1 ) {
        $p->rect( $xpos + 256 + $i * $size_sm_rect,
            $ypos, $size_sm_rect, $size_sm_rect );
        $p->stroke();
        $char = substr( $countyresidence, $i, 1 );
        if ( $char ne '' ) {
            $p->fit_textline( $char, $xpos + 259 + $i * $size_sm_rect,
                $ypos + 3, $basesmallfontoptions );
        }
    }

    $ypos -= ( $size_sm_rect + 3 );
    $p->fit_textline( "ZIP CODE:", $xpos + 3, $ypos + 6,
        $baseboldxsmallfontoptions );
    $p->fit_textline( "(99999 for Homeless-Streets)",
        $xpos + 40, $ypos + 6, $basexsmallfontoptions );
    foreach my $i ( 0 .. 4 ) {
        $p->rect( $xpos + 157 + $i * $size_sm_rect,
            $ypos, $size_sm_rect, $size_sm_rect );
        $p->stroke();
        $char = substr( $zip1, $i, 1 );
        if ( $char ne '' ) {
            $p->fit_textline( $char, $xpos + 160 + $i * $size_sm_rect,
                $ypos + 3, $basesmallfontoptions );
        }
    }
    $p->moveto( $xpos + 222, $ypos + 6 );
    $p->lineto( $xpos + 227, $ypos + 6 );
    foreach my $i ( 0 .. 3 ) {
        $p->rect( $xpos + 232 + $i * $size_sm_rect,
            $ypos, $size_sm_rect, $size_sm_rect );
        $p->stroke();
        $char = substr( $zip2, $i, 1 );
        if ( $char ne '' ) {
            $p->fit_textline( $char, $xpos + 235 + $i * $size_sm_rect,
                $ypos + 3, $basesmallfontoptions );
        }
    }
    ##

    ##
    # Section 2
    ##
    $xpos = $marginleft;
    $ypos_base -= $h_race;
    $ypos = $ypos_base;
    my $w_section2_part1 = $w_race_part1;
    my $w_section2_part2 = $w_race_part1 + 15;
    my $w_section2_part3 =
      $contentwidth - $w_section2_part1 - $w_section2_part2;
    my $h_section2_part3_pagroup = 170;

    # Section 2 Part 1
    $p->setlinewidth(1.7);
    $p->moveto( $xpos, $ypos );
    $p->lineto( $xpos + $contentwidth, $ypos );
    $p->stroke();

    $ypos -= $fontsize;
    $p->fit_textline( "SECTION II & III",
        $xpos + 4, $ypos, $baseboldfontoptions );

    $ypos -= $fontsizemid;
    $p->fit_textline( "CURRENT RESIDENCE:",
        $xpos + 4, $ypos, $baseboldsmallfontoptions );

    $p->setlinewidth(1.0);
    $p->rect( $xpos + 214, $ypos - 8, $size_sm_rect, $size_sm_rect );
    $p->stroke();
    $p->fit_textline( $residence, $xpos + 217,
        $ypos - 5, $basesmallfontoptions );

    $ypos -= $fontsizemid;
    $p->fit_textline( "A. Permanent Housing",
        $xpos + 7, $ypos, $basexsmallfontoptions );
    $p->fit_textline(
        "F. RC Facility/Group Home",
        $xpos + 115,
        $ypos, $basexsmallfontoptions
    );
    $ypos -= $fontsize;
    $p->fit_textline( "B. Perm Sup Hous-Non-Cong",
        $xpos + 7, $ypos, $basexsmallfontoptions );
    $p->fit_textline(
        "G. Nursing Home",
        $xpos + 115,
        $ypos, $basexsmallfontoptions
    );
    $ypos -= $fontsize;
    $p->fit_textline( "C. Perm Sup Hous-Cong",
        $xpos + 7, $ypos, $basexsmallfontoptions );
    $p->fit_textline(
        "H. Institutional Setting",
        $xpos + 115,
        $ypos, $basexsmallfontoptions
    );
    $ypos -= $fontsize;
    $p->fit_textline( "D. Transitional Housing",
        $xpos + 7, $ypos, $basexsmallfontoptions );
    $p->fit_textline(
        "I. Homeless-Shelter",
        $xpos + 115,
        $ypos, $basexsmallfontoptions
    );
    $ypos -= $fontsize;
    $p->fit_textline( "E. Temporary Housing",
        $xpos + 7, $ypos, $basexsmallfontoptions );
    $p->fit_textline(
        "J. Homeless-Streets",
        $xpos + 115,
        $ypos, $basexsmallfontoptions
    );

    $ypos -= 12;
    $p->fit_textline( "LIVING SITUATION:",
        $xpos + 4, $ypos, $baseboldsmallfontoptions );
    $p->rect( $xpos + 95, $ypos - 7, $size_sm_rect, $size_sm_rect );
    $p->stroke();
    $p->fit_textline( $living, $xpos + 98, $ypos - 4, $basesmallfontoptions );
    $p->rect( $xpos + 214, $ypos - 7, $size_sm_rect, $size_sm_rect );
    $p->stroke();
    $p->fit_textline( $chronic, $xpos + 217, $ypos - 4, $basesmallfontoptions );

    $tf = $p->create_textflow( "CHRONIC\n" . "HOMELESSNESS:",
        $baseboldsmallfontoptions . " leading=130%" );
    $p->fit_textflow(
        $tf,        $xpos + 130,
        $ypos - 10, $xpos + 220,
        $ypos + 14, "verticalalign=bottom"
    );
    $p->fit_textline(
        "(1=Yes; 2=No)",
        $xpos + 134,
        $ypos - 20, $basexsmallfontoptions
    );

    $ypos -= $fontsize;
    $p->fit_textline( "1. Alone", $xpos + 7, $ypos, $basexsmallfontoptions );
    $ypos -= $fontsize;
    $p->fit_textline( "2. With Family/Relatives",
        $xpos + 7, $ypos, $basexsmallfontoptions );
    $ypos -= $fontsize;
    $p->fit_textline( "3. With Non-Related Persons",
        $xpos + 7, $ypos, $basexsmallfontoptions );

    $ypos -= 15;
    $p->fit_textline( "EMPLOYMENT:", $xpos + 4, $ypos,
        $baseboldsmallfontoptions );
    $p->rect( $xpos + 214, $ypos, $size_sm_rect, $size_sm_rect );
    $p->stroke();
    $p->fit_textline( $employment, $xpos + 217,
        $ypos + 3, $basesmallfontoptions );
    $ypos -= $fontsize;
    $p->fit_textline( "1. Full-time (35+ hrs.)",
        $xpos + 7, $ypos, $basexsmallfontoptions );
    $p->fit_textline( "3. Unemployed (looking for work in last 30 days)",
        $xpos + 81, $ypos, $basexsmallfontoptions );
    $ypos -= $fontsize;
    $p->fit_textline( "2. Part-time (<35 hrs.)",
        $xpos + 7, $ypos, $basexsmallfontoptions );
    $p->fit_textline( "4. Not in Labor Force = (A-F below)",
        $xpos + 81, $ypos, $basexsmallfontoptions );

    $ypos -= 13;
    $p->fit_textline( "TYPE OF EMPLOYMENT/ Not in Labor Force:",
        $xpos + 4, $ypos, $baseboldsmallfontoptions );
    $p->rect( $xpos + 214, $ypos - 8, $size_sm_rect, $size_sm_rect );
    $p->stroke();
    $p->fit_textline( $typeofemployment, $xpos + 217,
        $ypos - 5, $basesmallfontoptions );
    $ypos -= $fontsizemid;
    $p->fit_textline( "1. Competitive",
        $xpos + 7, $ypos, $basexsmallfontoptions );
    $p->fit_textline( "A. Homemaker", $xpos + 112,
        $ypos, $basexsmallfontoptions );
    $ypos -= $fontsizemid;
    $p->fit_textline( "2. Supported", $xpos + 7, $ypos,
        $basexsmallfontoptions );
    $p->fit_textline( "B. Student", $xpos + 112, $ypos,
        $basexsmallfontoptions );
    $ypos -= $fontsize;
    $p->fit_textline( "3. Volunteer", $xpos + 7, $ypos,
        $basexsmallfontoptions );
    $p->fit_textline( "C. Retired", $xpos + 112, $ypos,
        $basexsmallfontoptions );
    $ypos -= $fontsize;
    $p->fit_textline( "4. None", $xpos + 7, $ypos, $basexsmallfontoptions );
    $p->fit_textline( "D. Disabled", $xpos + 112,
        $ypos, $basexsmallfontoptions );
    $ypos -= $fontsize;
    $p->fit_textline( "5. Transitional",
        $xpos + 7, $ypos, $basexsmallfontoptions );
    $p->fit_textline( "E. Inmate", $xpos + 112, $ypos, $basexsmallfontoptions );
    $ypos -= $fontsize;
    $p->fit_textline( "6. Sheltered Workshop",
        $xpos + 7, $ypos, $basexsmallfontoptions );
    $p->fit_textline( "F. Other", $xpos + 112, $ypos, $basexsmallfontoptions );

    $ypos -= 9;
    $p->fit_textline( "Is customer currently IN SCHOOL?:",
        $xpos + 4, $ypos, $baseboldsmallfontoptions );
    $p->fit_textline(
        "(1=Yes; 2=No)",
        $xpos + 140,
        $ypos, $basesmallfontoptions
    );
    $p->rect( $xpos + 214, $ypos - 4, $size_sm_rect, $size_sm_rect );
    $p->stroke();
    $p->fit_textline( $customerschool, $xpos + 217,
        $ypos - 1, $basesmallfontoptions );

    $ypos -= 2 * $fontsizelarge;
    $tf = $p->create_textflow(
"<fakebold=true>EDUCATION: <fakebold=false>(Highest Grade Completed or Current Grade 00-25) "
          . "<fontsize=$fontsizexsmall>(00-Less Than 1 Grade Completed, GED = 12)",
        $basesmallfontoptions . " leading=130%"
    );
    $p->fit_textflow(
        $tf, $xpos + 4, $ypos,
        $xpos + 200,
        $ypos + 2 * $fontsizelarge,
        "verticalalign=bottom"
    );

    foreach my $i ( 0 .. 1 ) {
        $p->rect( $xpos + 202 + $i * $size_sm_rect,
            $ypos + 2, $size_sm_rect, $size_sm_rect );
        $p->stroke();
        $char = substr( $education, $i, 1 );
        if ( $char ne '' ) {
            $p->fit_textline( $char, $xpos + 205 + $i * $size_sm_rect,
                $ypos + 5, $basesmallfontoptions );
        }
    }

    $ypos -= ( 4 * $fontsizemid - 2 );
    $tf = $p->create_textflow(
        "<fakebold=true>MILITARY STATUS: "
          . "<fontsize=$fontsizexsmall fakebold=false>(A=Client-Currently Active; B=Client-Previously Active; C=Client-National Guard/Reserve; D=Family "
          . "Member-Currently Active; E=Family Member-Previously Active; "
          . "F=Family Member-National Guard/Reserve; G=None)",
        $basesmallfontoptions . " leading=135%"
    );
    $p->fit_textflow(
        $tf, $xpos + 4, $ypos,
        $xpos + 200,
        $ypos + 4 * $fontsizemid,
        "verticalalign=bottom"
    );
    $p->rect( $xpos + 214, $ypos + 23, $size_sm_rect, $size_sm_rect );
    $p->stroke();
    $p->fit_textline( $militarystatus, $xpos + 217,
        $ypos + 26, $basesmallfontoptions );

    $ypos -= 10;
    $p->fit_textline( "Is customer PREGNANT?:",
        $xpos + 4, $ypos, $baseboldsmallfontoptions );
    $p->fit_textline(
        "(1=Yes; 2=No)",
        $xpos + 105,
        $ypos, $basesmallfontoptions
    );
    $p->rect( $xpos + 214, $ypos - 1, $size_sm_rect, $size_sm_rect );
    $p->stroke();
    $p->fit_textline( $customerpreg, $xpos + 217,
        $ypos + 2, $basesmallfontoptions );

    $ypos -= 2 * $fontsizemid;
    $tf = $p->create_textflow(
        "<fontsize=$fontsizexsmall>If Yes enter expected DOB, blank if No "
          . "<fontsize=$fontsizesmall>(MMDDYYYY)",
        $basesmallfontoptions . " leading=120%"
    );
    $p->fit_textflow(
        $tf, $xpos + 4, $ypos,
        $xpos + 128,
        $ypos + 2 * $fontsizemid,
        "verticalalign=bottom"
    );

    foreach my $i ( 0 .. 7 ) {
        $p->rect( $xpos + 130 + $i * $size_sm_rect,
            $ypos + 4, $size_sm_rect, $size_sm_rect );
        $p->stroke();
        $char = substr( $pregnantdob, $i, 1 );
        if ( $char ne '' ) {
            $p->fit_textline( $char, $xpos + 133 + $i * $size_sm_rect,
                $ypos + 7, $basesmallfontoptions );
        }
    }

    $ypos -= 13;
    $p->fit_textline( "Number contributing to and/or dependent upon",
        $xpos + 4, $ypos, $basesmallfontoptions );
    foreach my $i ( 0 .. 1 ) {
        $p->rect( $xpos + 202 + $i * $size_sm_rect,
            $ypos - 6, $size_sm_rect, $size_sm_rect );
        $p->stroke();
        $char = substr( $number, $i, 1 );
        if ( $char ne '' ) {
            $p->fit_textline( $char, $xpos + 205 + $i * $size_sm_rect,
                $ypos - 3, $basesmallfontoptions );
        }
    }

    $ypos -= $fontsizelarge;
    $p->fit_textline( "“Annual Income” above: (01-15)",
        $xpos + 4, $ypos, $basesmallfontoptions );

    $ypos -= $fontsizelarge;
    $p->fit_textline( "SSI:", $xpos + 4, $ypos, $baseboldsmallfontoptions );
    $p->rect( $xpos + 28, $ypos - 4, $size_sm_rect, $size_sm_rect );
    $p->stroke();
    $p->fit_textline( $ssi, $xpos + 31, $ypos - 1, $basesmallfontoptions );
    $p->fit_textline( "(1=Yes; 2=No)",
        $xpos + 50, $ypos, $basesmallfontoptions );

    $ypos -= $fontsizelarge;
    $p->fit_textline( "LANGUAGE PROFICIENCY:",
        $xpos + 4, $ypos, $baseboldsmallfontoptions );

    $ypos -= $fontsizemid;
    $p->fit_textline( "What language is preferred?:",
        $xpos + 4, $ypos, $baseboldxsmallfontoptions );
    $p->fit_textline( "(0-9)", $xpos + 102, $ypos, $basexsmallfontoptions );
    $p->setlinewidth(1.0);
    $p->rect( $xpos + 214, $ypos - 1, $size_sm_rect, $size_sm_rect );
    $p->stroke();
    $p->fit_textline( $custother, $xpos + 217,
        $ypos + 2, $basesmallfontoptions );

    $ypos -= $fontsizemid;
    $p->fit_textline( "Does customer speak English well?:",
        $xpos + 4, $ypos, $baseboldxsmallfontoptions );
    $p->fit_textline(
        "(1=Yes; 2=No)",
        $xpos + 126,
        $ypos, $basexsmallfontoptions
    );
    $p->rect( $xpos + 214, $ypos - 5, $size_sm_rect, $size_sm_rect );
    $p->stroke();
    $p->fit_textline( $custenglish, $xpos + 217,
        $ypos - 2, $basesmallfontoptions );

    $ypos -= 24;
    $p->fit_textline( "DISABILITY:", $xpos + 4, $ypos,
        $baseboldsmallfontoptions );
    $p->fit_textline( "(01-11 or Blank)",
        $xpos + 53, $ypos, $basesmallfontoptions );
    $x = $xpos + 104.5;
    foreach my $i ( 0 .. 7 ) {
        $x += $size_sm_rect;
        $x += 4.5 if $i % 2 eq 0 && $i > 0;
        $p->rect( $x, $ypos - 4, $size_sm_rect, $size_sm_rect );
        $p->stroke();
        $str = '';
        if ( $i < 2 ) {
            $str = $disability1;
        }
        elsif ( $i < 4 ) {
            $str = $disability2;
        }
        elsif ( $i < 6 ) {
            $str = $disability3;
        }
        else {
            $str = $disability4;
        }
        $char = substr( $str, $i % 2, 1 );
        if ( $char ne '' ) {
            $p->fit_textline( $char, $x + 3, $ypos - 1, $basesmallfontoptions );
        }
    }

    $ypos -= $fontsizexxlarge;
    $p->fit_textline( "TOBACCO USE:", $xpos + 4, $ypos,
        $baseboldsmallfontoptions );
    $p->fit_textline( "Times tobacco used on a typical day (00-99)",
        $xpos + 64, $ypos, $basexsmallfontoptions );
    foreach my $i ( 0 .. 1 ) {
        $p->rect( $xpos + 202 + $i * $size_sm_rect,
            $ypos - 3, $size_sm_rect, $size_sm_rect );
        $p->stroke();
        $char = substr( $tobaccouse, $i, 1 );
        if ( $char ne '' ) {
            $p->fit_textline(
                $char, $xpos + 205 + $i * $size_sm_rect,
                $ypos, $basesmallfontoptions
            );
        }
    }

    # Section 2 Part 2
    $xpos += $w_section2_part1;
    $ypos = $ypos_base;
    $p->setlinewidth(0.5);
    $p->moveto( $xpos, $ypos );
    $p->lineto( $xpos, $marginbottom + $h_legal + $h_addr );
    $p->stroke();

    $ypos -= $fontsizemid;
    $p->fit_textline( "Primary", $xpos + 128,
        $ypos, $baseboldxsmallfontoptions );
    $p->fit_textline( "Secondary", $xpos + 168,
        $ypos, $baseboldxsmallfontoptions );
    $p->fit_textline( "Tertiary", $xpos + 209,
        $ypos, $baseboldxsmallfontoptions );

    $ypos -= 2;

    $ypos -= $size_sm_rect;
    $p->fit_textline( "PRESENTING PROBLEM:*",
        $xpos + 4, $ypos + 3, $baseboldsmallfontoptions );
    $x = $xpos + 114.5;
    foreach my $i ( 0 .. 8 ) {
        $x += $size_sm_rect;
        $x += 4.5 if $i % 3 eq 0 && $i > 0;
        $p->rect( $x, $ypos, $size_sm_rect, $size_sm_rect );
        $p->stroke();
        $str = '';
        if ( $i < 3 ) {
            $str = $presentingprblm1;
        }
        elsif ( $i < 6 ) {
            $str = $presentingprblm2;
        }
        else {
            $str = $presentingprblm3;
        }
        $char = substr( $str, $i % 3, 1 );
        if ( $char ne '' ) {
            $p->fit_textline( $char, $x + 3, $ypos + 3, $basesmallfontoptions );
        }
    }

    $ypos -= $size_sm_rect;
    $p->fit_textline(
        "Drugs of Choice:",
        $xpos + 7, $ypos + 4.5,
        $baseboldxsmallfontoptions
    );
    $p->fit_textline(
        "(01-21)*",
        $xpos + 65.5,
        $ypos + 4.5,
        $basexsmallfontoptions
    );
    $x = $xpos + 126.5;
    foreach my $i ( 0 .. 5 ) {
        $x += $size_sm_rect;
        $x += 16.5 if $i % 2 eq 0 && $i > 0;
        $p->rect( $x, $ypos, $size_sm_rect, $size_sm_rect );
        $p->stroke();
        $str = '';
        if ( $i < 2 ) {
            $str = $drugs1;
        }
        elsif ( $i < 4 ) {
            $str = $drugs2;
        }
        else {
            $str = $drugs3;
        }
        $char = substr( $str, $i % 2, 1 );
        if ( $char ne '' ) {
            $p->fit_textline( $char, $x + 3, $ypos + 3, $basesmallfontoptions );
        }
    }

    $ypos -= $size_sm_rect;
    $p->fit_textline(
        "Usual Route of Administration:*",
        $xpos + 7, $ypos + 4.5,
        $baseboldxsmallfontoptions
    );
    $p->fit_textline(
        "(1-5)",
        $xpos + 164.5,
        $ypos + 4.5,
        $baseboldxsmallfontoptions
    );
    $p->fit_textline(
        "(1-5)",
        $xpos + 205,
        $ypos + 4.5,
        $baseboldxsmallfontoptions
    );
    $x = $xpos + 150.5;
    foreach my $i ( 0 .. 2 ) {
        $p->rect( $x, $ypos, $size_sm_rect, $size_sm_rect );
        $p->stroke();
        $str = '';
        if ( $i == 0 ) {
            $str = $route1;
        }
        elsif ( $i == 1 ) {
            $str = $route2;
        }
        else {
            $str = $route3;
        }
        $p->fit_textline( $str, $x + 3, $ypos + 3, $basesmallfontoptions );
        $x += ( 3 * $size_sm_rect + 4.5 );
    }

    $ypos -= $size_sm_rect;
    $p->fit_textline(
        "Frequency of Use in Last 30 days:*",
        $xpos + 7, $ypos + 4.5,
        $baseboldxsmallfontoptions
    );
    $p->fit_textline(
        "(1-5)",
        $xpos + 164.5,
        $ypos + 4.5,
        $baseboldxsmallfontoptions
    );
    $p->fit_textline(
        "(1-5)",
        $xpos + 205,
        $ypos + 4.5,
        $baseboldxsmallfontoptions
    );
    $x = $xpos + 150.5;
    foreach my $i ( 0 .. 2 ) {
        $p->rect( $x, $ypos, $size_sm_rect, $size_sm_rect );
        $p->stroke();
        $str = '';
        if ( $i == 0 ) {
            $str = $frequency1;
        }
        elsif ( $i == 1 ) {
            $str = $frequency2;
        }
        else {
            $str = $frequency3;
        }
        $p->fit_textline( $str, $x + 3, $ypos + 3, $basesmallfontoptions );
        $x += ( 3 * $size_sm_rect + 4.5 );
    }

    $ypos -= $size_sm_rect;
    $p->fit_textline(
        "Age First Used: (00-99)",
        $xpos + 7, $ypos + 4.5,
        $baseboldxsmallfontoptions
    );
    $x = $xpos + 126.5;
    foreach my $i ( 0 .. 5 ) {
        $x += $size_sm_rect;
        $x += 16.5 if $i % 2 eq 0 && $i > 0;
        $p->rect( $x, $ypos, $size_sm_rect, $size_sm_rect );
        $p->stroke();
        $str = '';
        if ( $i < 2 ) {
            $str = $agefirst1;
        }
        elsif ( $i < 4 ) {
            $str = $agefirst2;
        }
        else {
            $str = $agefirst3;
        }
        $char = substr( $str, $i % 2, 1 );
        if ( $char ne '' ) {
            $p->fit_textline( $char, $x + 3, $ypos + 3, $basesmallfontoptions );
        }
    }

    $ypos -= 3;

    $ypos -= $size_sm_rect;
    $p->fit_textline(
        "LEVEL OF CARE: ",
        $xpos + 4, $ypos + 3.5,
        $baseboldsmallfontoptions
    );
    $p->fit_textline(
        "(CI, CL, HA, OO, SC, or SN)*",
        $xpos + 68, $ypos + 3.5,
        $basesmallfontoptions
    );
    foreach my $i ( 0 .. 1 ) {
        $p->rect( $xpos + 219.5 + $i * $size_sm_rect,
            $ypos, $size_sm_rect, $size_sm_rect );
        $p->stroke();
        $char = substr( $levelofcare, $i, 1 );
        if ( $char ne '' ) {
            $p->fit_textline( $char, $xpos + 222.5 + $i * $size_sm_rect,
                $ypos + 3, $basesmallfontoptions );
        }
    }

    $ypos -= $fontsizemid;

    $p->fit_textline( "CAR: (Mental Health)",
        $xpos + 4, $ypos, $baseboldsmallfontoptions );
    $p->fit_textline( "(01-50)", $xpos + 114.5,
        $ypos + 1, $baseboldxsmallfontoptions );

    $y = $ypos;

    $y -= 2;

    $y -= $size_sm_rect;
    $p->fit_textline( "Feeling Mood", $xpos + 7, $y + 3,
        $baseboldxsmallfontoptions );
    foreach my $i ( 0 .. 1 ) {
        $p->rect( $xpos + 113 + $i * $size_sm_rect,
            $y, $size_sm_rect, $size_sm_rect );
        $p->stroke();
        $char = substr( $feelingmood, $i, 1 );
        if ( $char ne '' ) {
            $p->fit_textline(
                $char,  $xpos + 116 + $i * $size_sm_rect,
                $y + 3, $basesmallfontoptions
            );
        }
    }

    $y -= $size_sm_rect;
    $p->fit_textline( "Thinking", $xpos + 7, $y + 3,
        $baseboldxsmallfontoptions );
    foreach my $i ( 0 .. 1 ) {
        $p->rect( $xpos + 113 + $i * $size_sm_rect,
            $y, $size_sm_rect, $size_sm_rect );
        $p->stroke();
        $char = substr( $thinking, $i, 1 );
        if ( $char ne '' ) {
            $p->fit_textline(
                $char,  $xpos + 116 + $i * $size_sm_rect,
                $y + 3, $basesmallfontoptions
            );
        }
    }

    $y -= $size_sm_rect;
    $p->fit_textline( "Substance Use",
        $xpos + 7, $y + 3, $baseboldxsmallfontoptions );
    foreach my $i ( 0 .. 1 ) {
        $p->rect( $xpos + 113 + $i * $size_sm_rect,
            $y, $size_sm_rect, $size_sm_rect );
        $p->stroke();
        $char = substr( $substance, $i, 1 );
        if ( $char ne '' ) {
            $p->fit_textline(
                $char,  $xpos + 116 + $i * $size_sm_rect,
                $y + 3, $basesmallfontoptions
            );
        }
    }

    $y -= $size_sm_rect;
    $p->fit_textline( "Medical/Physical", $xpos + 7, $y + 3,
        $baseboldxsmallfontoptions );
    foreach my $i ( 0 .. 1 ) {
        $p->rect( $xpos + 113 + $i * $size_sm_rect,
            $y, $size_sm_rect, $size_sm_rect );
        $p->stroke();
        $char = substr( $medical, $i, 1 );
        if ( $char ne '' ) {
            $p->fit_textline(
                $char,  $xpos + 116 + $i * $size_sm_rect,
                $y + 3, $basesmallfontoptions
            );
        }
    }

    $y -= $size_sm_rect;
    $p->fit_textline( "Family", $xpos + 7, $y + 3, $baseboldxsmallfontoptions );
    foreach my $i ( 0 .. 1 ) {
        $p->rect( $xpos + 113 + $i * $size_sm_rect,
            $y, $size_sm_rect, $size_sm_rect );
        $p->stroke();
        $char = substr( $family, $i, 1 );
        if ( $char ne '' ) {
            $p->fit_textline(
                $char,  $xpos + 116 + $i * $size_sm_rect,
                $y + 3, $basesmallfontoptions
            );
        }
    }

    $y -= $size_sm_rect;
    $p->fit_textline( "Interpersonal", $xpos + 7, $y + 3,
        $baseboldxsmallfontoptions );
    foreach my $i ( 0 .. 1 ) {
        $p->rect( $xpos + 113 + $i * $size_sm_rect,
            $y, $size_sm_rect, $size_sm_rect );
        $p->stroke();
        $char = substr( $interpersonal, $i, 1 );
        if ( $char ne '' ) {
            $p->fit_textline(
                $char,  $xpos + 116 + $i * $size_sm_rect,
                $y + 3, $basesmallfontoptions
            );
        }
    }

    $y -= $size_sm_rect;
    $p->fit_textline( "Role Performance",
        $xpos + 7, $y + 3, $baseboldxsmallfontoptions );
    foreach my $i ( 0 .. 1 ) {
        $p->rect( $xpos + 113 + $i * $size_sm_rect,
            $y, $size_sm_rect, $size_sm_rect );
        $p->stroke();
        $char = substr( $roleperformance, $i, 1 );
        if ( $char ne '' ) {
            $p->fit_textline(
                $char,  $xpos + 116 + $i * $size_sm_rect,
                $y + 3, $basesmallfontoptions
            );
        }
    }

    $y -= $size_sm_rect;
    $p->fit_textline( "Socio-Legal", $xpos + 7, $y + 3,
        $baseboldxsmallfontoptions );
    foreach my $i ( 0 .. 1 ) {
        $p->rect( $xpos + 113 + $i * $size_sm_rect,
            $y, $size_sm_rect, $size_sm_rect );
        $p->stroke();
        $char = substr( $sociolegal, $i, 1 );
        if ( $char ne '' ) {
            $p->fit_textline(
                $char,  $xpos + 116 + $i * $size_sm_rect,
                $y + 3, $basesmallfontoptions
            );
        }
    }

    $y -= $size_sm_rect;
    $p->fit_textline( "Self Care/Basic Needs",
        $xpos + 7, $y + 3, $baseboldxsmallfontoptions );
    foreach my $i ( 0 .. 1 ) {
        $p->rect( $xpos + 113 + $i * $size_sm_rect,
            $y, $size_sm_rect, $size_sm_rect );
        $p->stroke();
        $char = substr( $selfcare, $i, 1 );
        if ( $char ne '' ) {
            $p->fit_textline(
                $char,  $xpos + 116 + $i * $size_sm_rect,
                $y + 3, $basesmallfontoptions
            );
        }
    }

    $p->fit_textline( "TASI:*", $xpos + 150, $ypos, $baseboldsmallfontoptions );
    $p->fit_textline(
        "(Ages 12-17) (0-4)",
        $xpos + 175,
        $ypos + 1, $basesmallfontoptions
    );

    $y = $ypos;

    $y -= 5;

    $y -= $size_sm_rect;
    $p->fit_textline( "Chemical", $xpos + 153,
        $y + 3, $baseboldxsmallfontoptions );
    $p->rect( $xpos + 231.5, $y, $size_sm_rect, $size_sm_rect );
    $p->stroke();
    $p->fit_textline( $tasichemical, $xpos + 234.5,
        $y + 3, $basesmallfontoptions );

    $y -= $size_sm_rect;
    $p->fit_textline( "School", $xpos + 153,
        $y + 3, $baseboldxsmallfontoptions );
    $p->rect( $xpos + 231.5, $y, $size_sm_rect, $size_sm_rect );
    $p->stroke();
    $p->fit_textline( $tasischool, $xpos + 234.5,
        $y + 3, $basesmallfontoptions );

    $y -= $size_sm_rect;
    $p->fit_textline( "Emp/Sup", $xpos + 153,
        $y + 3, $baseboldxsmallfontoptions );
    $p->rect( $xpos + 231.5, $y, $size_sm_rect, $size_sm_rect );
    $p->stroke();
    $p->fit_textline( $tasiemp, $xpos + 234.5, $y + 3, $basesmallfontoptions );

    $y -= $size_sm_rect;
    $p->fit_textline( "Family", $xpos + 153,
        $y + 3, $baseboldxsmallfontoptions );
    $p->rect( $xpos + 231.5, $y, $size_sm_rect, $size_sm_rect );
    $p->stroke();
    $p->fit_textline( $tasifamily, $xpos + 234.5,
        $y + 3, $basesmallfontoptions );

    $y -= $size_sm_rect;
    $p->fit_textline( "Peer/Soc", $xpos + 153,
        $y + 3, $baseboldxsmallfontoptions );
    $p->rect( $xpos + 231.5, $y, $size_sm_rect, $size_sm_rect );
    $p->stroke();
    $p->fit_textline( $tasipeer, $xpos + 234.5, $y + 3, $basesmallfontoptions );

    $y -= $size_sm_rect;
    $p->fit_textline( "Legal", $xpos + 153, $y + 3,
        $baseboldxsmallfontoptions );
    $p->rect( $xpos + 231.5, $y, $size_sm_rect, $size_sm_rect );
    $p->stroke();
    $p->fit_textline( $tasilegal, $xpos + 234.5, $y + 3,
        $basesmallfontoptions );

    $y -= $size_sm_rect;
    $p->fit_textline( "Psychiatric", $xpos + 153,
        $y + 3, $baseboldxsmallfontoptions );
    $p->rect( $xpos + 231.5, $y, $size_sm_rect, $size_sm_rect );
    $p->stroke();
    $p->fit_textline( $tasipsychiatric, $xpos + 234.5,
        $y + 3, $basesmallfontoptions );

    $ypos -= ( 2 + 9 * $size_sm_rect );

    $ypos -= 35;
    $tf = $p->create_textflow(
        "SED: <fakebold=false fontsize=$fontsizexsmall>(1=Yes; 2=No)\n"
          . "<fakebold=true fontsize=$fontsizesmall>(For customer under 18)",
        $baseboldsmallfontoptions . " leading=130%"
    );
    $p->fit_textflow( $tf, $xpos + 5, $ypos, $xpos + 110,
        $ypos + 25, "verticalalign=bottom" );
    $p->rect( $xpos + 231.5, $ypos + 0.5, $size_sm_rect, $size_sm_rect );
    $p->stroke();
    $p->fit_textline( $sed, $xpos + 234.5, $ypos + 3.5, $basesmallfontoptions );

    $ypos -= 22;
    $tf = $p->create_textflow(
"In the <underline=true underlineposition=-20%>past 30 days<underline=false>, how many <underline=true underlineposition=-20%>times<underline=false> has the customer been "
          . "<underline=true underlineposition=-20%>arrested<underline=false>, or since admission if less than 30 days ago? (00-99)",
        $basexsmallfontoptions . " leading=130%"
    );
    $p->fit_textflow( $tf, $xpos + 5, $ypos, $xpos + 210,
        $ypos + 20, "verticalalign=bottom" );

    foreach my $i ( 0 .. 1 ) {
        $p->rect( $xpos + 219.5 + $i * $size_sm_rect,
            $ypos + 1, $size_sm_rect, $size_sm_rect );
        $p->stroke();
        $char = substr( $past30, $i, 1 );
        if ( $char ne '' ) {
            $p->fit_textline( $char, $xpos + 222.5 + $i * $size_sm_rect,
                $ypos + 4, $basesmallfontoptions );
        }
    }

    $ypos -= 25;
    $tf = $p->create_textflow(
"In the <underline=true underlineposition=-20%>past 12 months<underline=false>, how many <underline=true underlineposition=-20%>times<underline=false> has the customer been "
          . "<underline=true underlineposition=-20%>arrested<underline=false>, or since admission if less than 12 months ago? (00-99)",
        $basexsmallfontoptions . " leading=130%"
    );
    $p->fit_textflow( $tf, $xpos + 5, $ypos, $xpos + 210,
        $ypos + 20, "verticalalign=bottom" );
    foreach my $i ( 0 .. 1 ) {
        $p->rect( $xpos + 219.5 + $i * $size_sm_rect,
            $ypos + 1, $size_sm_rect, $size_sm_rect );
        $p->stroke();
        $char = substr( $past12, $i, 1 );
        if ( $char ne '' ) {
            $p->fit_textline( $char, $xpos + 222.5 + $i * $size_sm_rect,
                $ypos + 4, $basesmallfontoptions );
        }
    }

    $ypos -= 33;
    $tf = $p->create_textflow(
"In the <underline=true underlineposition=-20%>past 30 days<underline=false>, how many <underline=true underlineposition=-20%>times<underline=false> has the customer <underline=true underlineposition=-20%>attended "
          . "self-help/support groups<underline=false>, or since admission if less than 30 days "
          . "ago? (00-99)",
        $basexsmallfontoptions . " leading=130%"
    );
    $p->fit_textflow( $tf, $xpos + 5, $ypos, $xpos + 210,
        $ypos + 28, "verticalalign=bottom" );
    foreach my $i ( 0 .. 1 ) {
        $p->rect( $xpos + 219.5 + $i * $size_sm_rect,
            $ypos + 11, $size_sm_rect, $size_sm_rect );
        $p->stroke();
        $char = substr( $past1, $i, 1 );
        if ( $char ne '' ) {
            $p->fit_textline( $char, $xpos + 222.5 + $i * $size_sm_rect,
                $ypos + 14, $basesmallfontoptions );
        }
    }

    $ypos -= 2 * $fontsizexlarge;
    $tf = $p->create_textflow(
        "FAMILY ID,\n" . "DOC # or DHS Case Number:",
        $baseboldsmallfontoptions . " leading=130%"
    );
    $p->fit_textflow( $tf, $xpos + 5, $ypos, $xpos + 130,
        $ypos + 24, "verticalalign=bottom" );
    foreach my $i ( 0 .. 9 ) {
        $p->rect( $xpos + 123.5 + $i * $size_sm_rect,
            $ypos, $size_sm_rect, $size_sm_rect );
        $p->stroke();
        $char = substr( $dhscase, $i, 1 );
        if ( $char ne '' ) {
            $p->fit_textline( $char, $xpos + 126.5 + $i * $size_sm_rect,
                $ypos + 3, $basesmallfontoptions );
        }
    }

    $ypos -= ( 2 * $fontsizemid - 1 );
    $p->fit_textline( "CLINICIAN OF RECORD (NPI):",
        $xpos + 5, $ypos + 3, $baseboldsmallfontoptions );
    foreach my $i ( 0 .. 9 ) {
        $p->rect( $xpos + 123.5 + $i * $size_sm_rect,
            $ypos, $size_sm_rect, $size_sm_rect );
        $p->stroke();
        $char = substr( $npi, $i, 1 );
        if ( $char ne '' ) {
            $p->fit_textline( $char, $xpos + 126.5 + $i * $size_sm_rect,
                $ypos + 3, $basesmallfontoptions );
        }
    }

    # Section 2 Part 3
    $xpos += $w_section2_part2;
    $ypos = $ypos_base;
    $p->moveto( $xpos, $ypos );
    $p->lineto( $xpos, $marginbottom + $h_legal + $h_addr );
    $p->stroke();

    $ypos -= $fontsizelarge;
    $p->fit_textline( "SECTION IV", $xpos + 5, $ypos, $baseboldfontoptions );
    $ypos -= $fontsizelarge;
    $p->fit_textline( "(Required if under 18 years old)",
        $xpos + 9, $ypos, $baseboldsmallfontoptions );

    $ypos -= 48;
    $tf = $p->create_textflow(
"In what <underline=true underlineposition=-20%>type of <fakebold=true>out-of-home<fakebold=false> placement<underline=false> is the customer currently living?\n"
          . "(select only one from below)",
        $basexsmallfontoptions . " leading=130%"
    );
    $p->fit_textflow( $tf, $xpos + 8, $ypos, $xpos + 240,
        $ypos + 20, "verticalalign=bottom" );
    $p->rect( $xpos + 243, $ypos + 5, $size_sm_rect, $size_sm_rect );
    $p->stroke();
    $p->fit_textline( $outofhome, $xpos + 246,
        $ypos + 8, $basesmallfontoptions );

    $ypos -= $fontsizemid;
    $p->fit_textline( "1. Not in out-of-home placement",
        $xpos + 12, $ypos, $basexsmallfontoptions );
    $p->fit_textline(
        "4. Foster Care",
        $xpos + 152,
        $ypos, $basexsmallfontoptions
    );
    $ypos -= $fontsizemid;
    $p->fit_textline( "2. Residential Treatment",
        $xpos + 12, $ypos, $basexsmallfontoptions );
    $p->fit_textline(
        "5. Group Home",
        $xpos + 152,
        $ypos, $basexsmallfontoptions
    );
    $ypos -= $fontsizemid;
    $p->fit_textline( "3. Specialized Community Group Home",
        $xpos + 12, $ypos, $basexsmallfontoptions );
    $p->fit_textline( "6. Other", $xpos + 152, $ypos, $basexsmallfontoptions );

    $ypos -= 22;
    $tf = $p->create_textflow(
"In the <underline=true underlineposition=-20%>past 90 days<underline=false>, how many <underline=true underlineposition=-20%>days<underline=false> was the customer "
          . "in <underline=true underlineposition=-20% fakebold=true>restrictive<fakebold=false> placement<underline=false>? (00-99)",
        $basexsmallfontoptions . " leading=130%"
    );
    $p->fit_textflow( $tf, $xpos + 8, $ypos, $xpos + 175,
        $ypos + 20, "verticalalign=bottom" );

    foreach my $i ( 0 .. 1 ) {
        $p->rect( $xpos + 231 + $i * $size_sm_rect,
            $ypos + 2, $size_sm_rect, $size_sm_rect );
        $p->stroke();
        $char = substr( $past901, $i, 1 );
        if ( $char ne '' ) {
            $p->fit_textline( $char, $xpos + 234 + $i * $size_sm_rect,
                $ypos + 5, $basesmallfontoptions );
        }
    }

    $ypos -= 22;
    $tf = $p->create_textflow(
"In the <underline=true underlineposition=-20%>past 90 days<underline=false>, on how many <underline=true underlineposition=-20%>days<underline=false> did an "
          . "<underline=true underlineposition=-20%>Incident of self-harm occur<underline=false>? (00-99)",
        $basexsmallfontoptions . " leading=130%"
    );
    $p->fit_textflow( $tf, $xpos + 8, $ypos, $xpos + 170,
        $ypos + 20, "verticalalign=bottom" );
    foreach my $i ( 0 .. 1 ) {
        $p->rect( $xpos + 231 + $i * $size_sm_rect,
            $ypos + 2, $size_sm_rect, $size_sm_rect );
        $p->stroke();
        $char = substr( $past902, $i, 1 );
        if ( $char ne '' ) {
            $p->fit_textline( $char, $xpos + 234 + $i * $size_sm_rect,
                $ypos + 5, $basesmallfontoptions );
        }
    }

    $ypos -= 16;
    $p->fit_textline( "SCHOOL-AGED CHILDREN:",
        $xpos + 5, $ypos, $baseboldsmallfontoptions );
    $p->fit_textline(
        "(00-66 days OR 99 for not applicable)",
        $xpos + 113,
        $ypos, $basexsmallfontoptions
    );

    $ypos -= 22;
    $tf = $p->create_textflow(
"In the <underline=true underlineposition=-20%>past 90 days<underline=false> of the school year, how many <underline=true underlineposition=-20%>days<underline=false> was "
          . "the customer <underline=true underlineposition=-20%>absent from school<underline=false>?",
        $basexsmallfontoptions . " leading=130%"
    );
    $p->fit_textflow( $tf, $xpos + 8, $ypos, $xpos + 175,
        $ypos + 20, "verticalalign=bottom" );
    foreach my $i ( 0 .. 1 ) {
        $p->rect( $xpos + 231 + $i * $size_sm_rect,
            $ypos + 2, $size_sm_rect, $size_sm_rect );
        $p->stroke();
        $char = substr( $past903, $i, 1 );
        if ( $char ne '' ) {
            $p->fit_textline( $char, $xpos + 234 + $i * $size_sm_rect,
                $ypos + 5, $basesmallfontoptions );
        }
    }

    $ypos -= 22;
    $tf = $p->create_textflow(
"In the <underline=true underlineposition=-20%>past 90 days<underline=false> of the school year, how many <underline=true underlineposition=-20%>days<underline=false> was "
          . "the customer <underline=true underlineposition=-20%>suspended from school<underline=false>?",
        $basexsmallfontoptions . " leading=130%"
    );
    $p->fit_textflow( $tf, $xpos + 8, $ypos, $xpos + 175,
        $ypos + 20, "verticalalign=bottom" );
    foreach my $i ( 0 .. 1 ) {
        $p->rect( $xpos + 231 + $i * $size_sm_rect,
            $ypos + 2, $size_sm_rect, $size_sm_rect );
        $p->stroke();
        $char = substr( $past904, $i, 1 );
        if ( $char ne '' ) {
            $p->fit_textline( $char, $xpos + 234 + $i * $size_sm_rect,
                $ypos + 5, $basesmallfontoptions );
        }
    }

    $ypos -= 16;
    $p->fit_textline( "CHILDREN UNDER SCHOOL AGE:",
        $xpos + 5, $ypos, $baseboldsmallfontoptions );
    $p->fit_textline(
        "(00-66 days OR 99 for not applicable)",
        $xpos + 140,
        $ypos, $basexsmallfontoptions
    );

    $ypos -= 20;
    $tf = $p->create_textflow(
"In the <underline=true underlineposition=-20%>past 90 days<underline=false>, how many <underline=true underlineposition=-20%>days<underline=false> was "
          . "the customer <underline=true underlineposition=-20%>Not permitted to return to day care<underline=false>?",
        $basexsmallfontoptions . " leading=130%"
    );
    $p->fit_textflow( $tf, $xpos + 8, $ypos, $xpos + 175,
        $ypos + 20, "verticalalign=bottom" );
    foreach my $i ( 0 .. 1 ) {
        $p->rect( $xpos + 231 + $i * $size_sm_rect,
            $ypos + 2, $size_sm_rect, $size_sm_rect );
        $p->stroke();
        $char = substr( $past905, $i, 1 );
        if ( $char ne '' ) {
            $p->fit_textline( $char, $xpos + 234 + $i * $size_sm_rect,
                $ypos + 5, $basesmallfontoptions );
        }
    }

    ## PA Group

    $ypos = $marginbottom + $h_legal + $h_addr + $h_section2_part3_pagroup;
    $p->setlinewidth(1.7);
    $p->set_graphics_option("linejoin=1");
    $p->rect( $xpos, $ypos - $h_section2_part3_pagroup,
        $w_section2_part3, $h_section2_part3_pagroup );
    $p->stroke();

    $ypos -= $fontsizexlarge;
    $p->fit_textline( "PA GROUP:", $xpos + 5, $ypos,
        $baseboldsmallfontoptions );
    $p->setlinewidth(1.2);
    $p->moveto( $xpos + 51.5, $ypos - 2 );
    $p->lineto( $xpos + 150, $ypos - 2 );
    $p->stroke();
    $p->fit_textline( $pagroup, $xpos + 51.5,
        $ypos + 1, $basexsmallfontoptions );

    $ypos -= 14.5;
    $p->fit_textline( "Start Date (MMDDYYYY):",
        $xpos + 5, $ypos, $baseboldsmallfontoptions );
    foreach my $i ( 0 .. 7 ) {
        $p->rect( $xpos + 110 + $i * $size_sm_rect,
            $ypos - 4, $size_sm_rect, $size_sm_rect );
        $p->stroke();
        $char = substr( $startdate, $i, 1 );
        if ( $char ne '' ) {
            $p->fit_textline( $char, $xpos + 113 + $i * $size_sm_rect,
                $ypos - 1, $basesmallfontoptions );
        }
    }

    $ypos -= 16;
    $p->fit_textline( "Diagnoses: ICD-10 Codes",
        $xpos + 5, $ypos, $baseboldsmallfontoptions );

    $ypos -= 19;
    $x = $xpos + 32;
    foreach my $i ( 0 .. 2 ) {
        $p->rect( $x + $i * $size_sm_rect, $ypos, $size_sm_rect,
            $size_sm_rect );
        $p->stroke();
        $char = substr( $axis1primary1, $i, 1 );
        if ( $char ne '' ) {
            $p->fit_textline(
                $char,     $x + 3 + $i * $size_sm_rect,
                $ypos + 3, $basesmallfontoptions
            );
        }
    }

    $x += ( 3 * $size_sm_rect + 8 );
    $p->set_graphics_option("linejoin=0");
    $p->rect( $x - 3.7, $ypos - 0.5, 3, 3 );
    $p->fill();
    $p->set_graphics_option("linejoin=1");
    foreach my $i ( 0 .. 1 ) {
        $p->rect( $x + $i * $size_sm_rect, $ypos, $size_sm_rect,
            $size_sm_rect );
        $p->stroke();
        $char = substr( $axis1primary2, $i, 1 );
        if ( $char ne '' ) {
            $p->fit_textline(
                $char,     $x + 3 + $i * $size_sm_rect,
                $ypos + 3, $basesmallfontoptions
            );
        }
    }

    $x += ( 2 * $size_sm_rect + 8 );
    foreach my $i ( 0 .. 2 ) {
        $p->rect( $x + $i * $size_sm_rect, $ypos, $size_sm_rect,
            $size_sm_rect );
        $p->stroke();
        $char = substr( $axis1secondary1, $i, 1 );
        if ( $char ne '' ) {
            $p->fit_textline(
                $char,     $x + 3 + $i * $size_sm_rect,
                $ypos + 3, $basesmallfontoptions
            );
        }
    }

    $x += ( 3 * $size_sm_rect + 8 );
    $p->set_graphics_option("linejoin=0");
    $p->rect( $x - 3.7, $ypos - 0.5, 3, 3 );
    $p->fill();
    $p->set_graphics_option("linejoin=1");
    foreach my $i ( 0 .. 1 ) {
        $p->rect( $x + $i * $size_sm_rect, $ypos, $size_sm_rect,
            $size_sm_rect );
        $p->stroke();
        $char = substr( $axis1secondary2, $i, 1 );
        if ( $char ne '' ) {
            $p->fit_textline(
                $char,     $x + 3 + $i * $size_sm_rect,
                $ypos + 3, $basesmallfontoptions
            );
        }
    }

    $x += ( 2 * $size_sm_rect + 8 );
    foreach my $i ( 0 .. 2 ) {
        $p->rect( $x + $i * $size_sm_rect, $ypos, $size_sm_rect,
            $size_sm_rect );
        $p->stroke();
        $char = substr( $axis1tertiary1, $i, 1 );
        if ( $char ne '' ) {
            $p->fit_textline(
                $char,     $x + 3 + $i * $size_sm_rect,
                $ypos + 3, $basesmallfontoptions
            );
        }
    }

    $x += ( 3 * $size_sm_rect + 8 );
    $p->set_graphics_option("linejoin=0");
    $p->rect( $x - 3.7, $ypos - 0.5, 3, 3 );
    $p->fill();
    $p->set_graphics_option("linejoin=1");
    foreach my $i ( 0 .. 1 ) {
        $p->rect( $x + $i * $size_sm_rect, $ypos, $size_sm_rect,
            $size_sm_rect );
        $p->stroke();
        $char = substr( $axis1tertiary2, $i, 1 );
        if ( $char ne '' ) {
            $p->fit_textline(
                $char,     $x + 3 + $i * $size_sm_rect,
                $ypos + 3, $basesmallfontoptions
            );
        }
    }

    $ypos -= 20;

    $x = $xpos + 32;
    foreach my $i ( 0 .. 2 ) {
        $p->rect( $x + $i * $size_sm_rect, $ypos, $size_sm_rect,
            $size_sm_rect );
        $p->stroke();
        $char = substr( $axis2primary1, $i, 1 );
        if ( $char ne '' ) {
            $p->fit_textline(
                $char,     $x + 3 + $i * $size_sm_rect,
                $ypos + 3, $basesmallfontoptions
            );
        }
    }

    $x += ( 3 * $size_sm_rect + 8 );
    $p->set_graphics_option("linejoin=0");
    $p->rect( $x - 3.7, $ypos - 0.5, 3, 3 );
    $p->fill();
    $p->set_graphics_option("linejoin=1");
    foreach my $i ( 0 .. 1 ) {
        $p->rect( $x + $i * $size_sm_rect, $ypos, $size_sm_rect,
            $size_sm_rect );
        $p->stroke();
        $char = substr( $axis2primary2, $i, 1 );
        if ( $char ne '' ) {
            $p->fit_textline(
                $char,     $x + 3 + $i * $size_sm_rect,
                $ypos + 3, $basesmallfontoptions
            );
        }
    }

    $x += ( 2 * $size_sm_rect + 8 );
    foreach my $i ( 0 .. 2 ) {
        $p->rect( $x + $i * $size_sm_rect, $ypos, $size_sm_rect,
            $size_sm_rect );
        $p->stroke();
        $char = substr( $axis2secondary1, $i, 1 );
        if ( $char ne '' ) {
            $p->fit_textline(
                $char,     $x + 3 + $i * $size_sm_rect,
                $ypos + 3, $basesmallfontoptions
            );
        }
    }

    $x += ( 3 * $size_sm_rect + 8 );
    $p->set_graphics_option("linejoin=0");
    $p->rect( $x - 3.7, $ypos - 0.5, 3, 3 );
    $p->fill();
    $p->set_graphics_option("linejoin=1");
    foreach my $i ( 0 .. 1 ) {
        $p->rect( $x + $i * $size_sm_rect, $ypos, $size_sm_rect,
            $size_sm_rect );
        $p->stroke();
        $char = substr( $axis2secondary2, $i, 1 );
        if ( $char ne '' ) {
            $p->fit_textline(
                $char,     $x + 3 + $i * $size_sm_rect,
                $ypos + 3, $basesmallfontoptions
            );
        }
    }

    $ypos -= 14.5;
    $p->fit_textline( "Medical", $xpos + 5, $ypos, $baseboldsmallfontoptions );

    $p->rect( $xpos + 5.5, $ypos - 65, 245, 61 );
    $p->stroke();
    $tf =
      $p->create_textflow( $axis3, $basexxsmallfontoptions . " leading=130%" );
    $p->fit_textflow( $tf, $xpos + 8, $ypos - 63, $xpos + 248,
        $ypos - 5, "verticalalign=top" );

    ##

    ##
    # LEGAL NAME AND ADDRESS SECTION
    ##
    $xpos      = $marginleft;
    $ypos_base = $marginbottom + $h_legal + $h_addr;
    $ypos      = $ypos_base;
    $p->setlinewidth(2.0);
    $p->moveto( $marginleft, $ypos );
    $p->lineto( $marginleft + $contentwidth, $ypos );
    $p->stroke();

    $ypos -= 12;
    $p->fit_textline( "LEGAL NAME:", $xpos + 3, $ypos, $baseboldfontoptions );
    $p->fit_textline( "Last:",   $xpos + 72,    $ypos, $basexsmallfontoptions );
    $p->fit_textline( $lastname, $xpos + 90,    $ypos, $basexsmallfontoptions );

    $xpos += $w_section2_part1;
    $p->fit_textline( "Maiden:", $xpos + 21.5,  $ypos, $basexsmallfontoptions );
    $p->fit_textline( $maidenname, $xpos + 50,  $ypos, $basexsmallfontoptions );
    $p->fit_textline( "First:",    $xpos + 166, $ypos, $basexsmallfontoptions );
    $p->fit_textline( $firstname,  $xpos + 184, $ypos, $basexsmallfontoptions );

    $xpos += $w_section2_part2;
    $p->fit_textline( "Middle:",   $xpos + 98,  $ypos, $basexsmallfontoptions );
    $p->fit_textline( $middlename, $xpos + 124, $ypos, $basexsmallfontoptions );
    $p->fit_textline( "Suffix:",   $xpos + 206, $ypos, $basexsmallfontoptions );
    $p->fit_textline( $suffixname, $xpos + 228, $ypos, $basexsmallfontoptions );

    $xpos = $marginleft;
    $ypos_base -= $h_legal;
    $ypos = $ypos_base;
    $p->setlinewidth(1.2);
    $p->moveto( $marginleft, $ypos );
    $p->lineto( $marginleft + $contentwidth, $ypos );
    $p->stroke();

    $ypos -= 10.5;
    $p->fit_textline( "ADDRESS:", $xpos + 3,  $ypos, $baseboldfontoptions );
    $p->fit_textline( "(1)",      $xpos + 50, $ypos, $basesmallfontoptions );
    $p->fit_textline( $address1,  $xpos + 63, $ypos, $basesmallfontoptions );

    $xpos += $w_section2_part1;
    $p->fit_textline( "(2)",     $xpos + 93,  $ypos, $basesmallfontoptions );
    $p->fit_textline( $address2, $xpos + 106, $ypos, $basesmallfontoptions );

    $xpos += $w_section2_part2;
    $p->fit_textline( "CITY:",  $xpos + 6,   $ypos, $baseboldsmallfontoptions );
    $p->fit_textline( $city,    $xpos + 30,  $ypos, $basesmallfontoptions );
    $p->fit_textline( "STATE:", $xpos + 170, $ypos, $baseboldsmallfontoptions );
    $p->fit_textline( $state,   $xpos + 200, $ypos, $basesmallfontoptions );
    ##

    $p->end_page_ext("");
}

sub create_help_page {
    my ($p) = @_;

    my $tf;
    my $x;

    my $TransactionType =
"<fakebold=true fontsize=$fontsizemid underline=true underlineposition=-15% underlinewidth=1.0>"
      . "TRANSACTION TYPE:"
      . "<fakebold=false underline=false>"
      . " (Enter Appropriate Code)\n"
      . "<fontsize=$fontsizexsmall leftindent=10>"
      . "21 Pre-admission - Only Section I is to be completed with Name, & Address\n"
      . "23 Admission - All sections required; CAR/ASI/TASI depends on age/service focus\n"
      . "27 First Contact - Only Section I is to be completed with Name, & Address\n"
      . "40 Level of Care Change\n"
      . "41 Information Update - Only fields to be updated are required\n"
      . "42 Treatment Extension/Outcome Update\n"
      . "60 Discharge/Completed Treatment\n"
      . "61 Discharge/Completed Court Treatment\n"
      . "62 Discharge/Left Against Counselor's Advice (ACA)\n"
      . "63 Discharge/Moved\n"
      . "64 Discharge/Transferred to another treatment facility\n"
      . "65 Discharge/Incarcerated\n"
      . "66 Discharge/Broke Rules\n"
      . "67 Discharge/AWOL\n"
      . "68 Discharge/Death - Primary Referral 36\n"
      . "69 Discharge/Failed to begin Treatment\n"
      . "70 Discharge/ Due to Treatment Incompatibility\n"
      . "71 Discharge/Medical\n"
      . "72 Discharge/Children Related To Parent's Discharge";
    my $note =
"Note: All fields will be assumed to be updated on all transaction types. Prior to 7/1/2010, only certain fields were required to be updated for different transactions. To allow agencies to receive credit for all the changes which occurred during treatment, all fields are allowed to be updated, regardless of transaction type.";
    my $ServiceFocus =
"<fakebold=true fontsize=$fontsizemid underline=true underlineposition=-15% underlinewidth=1.0>"
      . "SERVICE FOCUS:\n"
      . "<fakebold=false fontsize=$fontsizexsmall underline=false>"
      . "01 - Mental Health\n"
      . "02 - Substance Abuse\n"
      . "03 - Drug Court\n"
      . "06 - Mental Health and Substance Abuse\n"
      . "09 - Special Populations Treatment Units\n"
      . "11 - Other (R.C., Homeless/Housing Srvcs\n"
      . "12 - PACT\n"
      . "13 - Co-Occurring\n"
      . "14 - SOC (Systems of Care)\n"
      . "15 - MH Court\n"
      . "16 - ICC\n"
      . "17 - MH Court/PACT\n"
      . "18 - ICC/MHC\n"
      . "19 - Gambling\n"
      . "20 - Gambling/Mental Health\n"
      . "21 - Gambling/Substance Abuse\n"
      . "22 - RICCT Team Mental Health\n"
      . "23 - Day School\n"
      . "24 - Medication Clinic Only\n"
      . "25 - To be determined\n"
      . "26 - Mobile Crisis\n"
      . "27 - Long Term MH Inpatient\n"
      . "30 - Non-DMHSAS/OHCA funded";
    my $Referral =
        "01 Self\n"
      . "02 Significant Other\n"
      . "03 School\n"
      . "04 Church/Clergy\n"
      . "05 Group Home\n"
      . "06 Employer, Union\n"
      . "08 Non-Psychiatric Hospital\n"
      . "09 VA System\n"
      . "10 Indian Health Service\n"
      . "11 Department of Health\n"
      . "12 Department of Corrections\n"
      . "14 Department of Human Services\n"
      . "18 Nursing Home\n"
      . "21 Private Psychiatrist/MH Prof\n"
      . "22 Social Security\n"
      . "23 Attorney/Legal Aid\n"
      . "25 Law Enforcement\n"
      . "26 Reachout Hot-Line/Advertising Media\n"
      . "28 Referral Due to Unscheduled Discharge <fakebold=true>for 62 and 67\n"
      . "<fakebold=false>30 Shelter for Homeless\n"
      . "31 Additional Services Recommended, Referral not Attainable\n"
      . "32 Court\n"
      . "33 Probation\n"
      . "34 Parole\n"
      . "35 Department of Public Safety\n"
      . "36 Active Client-Died <fakebold=true>(Used with 68-Discharge only)\n"
      . "<fakebold=false>37 Private Physician\n"
      . "38 HMO/MCO\n"
      . "39 Change in Pay Source (to/from public funding)\n"
      . "40 <italicangle=-10>ODMHSAS/OHCA Funded Facility <italicangle=0 fakebold=true>(With Agency Number)\n"
      . "<fakebold=false>41None-ODMHSAS/OHCA funded Psychiatric Hospital\n"
      . "42 None-ODMHSAS/OHCA funded Mental Health Center\n"
      . "43 None-ODMHSAS/OHCA funded \n"
      . "44 None-ODMHSAS/OHCA funded Residential Care Home\n"
      . "45 None-ODMHSAS/OHCA funded Alcohol/Drug Program\n"
      . "46 None-ODMHSAS/OHCA funded Domestic Violence Facility\n"
      . "47 None-ODMHSAS/OHCA funded Crisis/Stabilization Facility\n"
      . "48 Office of Juvenile Affairs\n"
      . "49 TANF/Child Welfare\n"
      . "50 Change in Eligibility Standards\n"
      . "51 Self Help Group (AA/NA/CA)\n"
      . "52 Parent/Guardian";

    my $LegalStatus =
"<fakebold=true fontsize=$fontsizemid underline=true underlineposition=-15% underlinewidth=1.0>LEGAL STATUS:\n"
      . "<fakebold=false fontsize=$fontsizexsmall underline=false italicangle=-10>     01 - Voluntary Admission*\n"
      . "<italicangle=0>     03 - Civil Commitment\n"
      . "05 - Not Guilty by Reason of Insanity (NGRI)\n"
      . "07 - Juvenile Court Order\n"
      . "09 - Court Order for Observation/Evaluation\n"
      . "12 - Emergency Detention\n"
      . "13 - Continued Emergency Detention\n"
      . "15 - Court Referred\n"
      . "<italicangle=-10>17 - Protective Custody* <italicangle=0 fakebold=true>(Co. Not Required)*\n"
      . "<fakebold=false>20 - Criminal Hold (CR-H) - OFC Only\n"
      . "21 - Court Commit with Hold (CC-H) - OFC Only\n";

    my $PresentingProblem =
"<fakebold=true fontsize=$fontsizemid underline=true underlineposition=-15% underlinewidth=1.0>"
      . "PRESENTING PROBLEM:\n"
      . "<fakebold=false fontsize=$fontsizexsmall underline=false leftindent=6>"
      . "100 Other-Non-Behavioral Health Problem\n"
      . "<fakebold=true underline=true underlineposition=-20% underlinewidth=0.6 leftindent=0>"
      . "Physical\n"
      . "<fakebold=false underline=false leftindent=4>110 Speech/Hearing\n"
      . "120 Physical\n"
      . "130 Medical/Somatic\n"
      . "<nextline leading=20%>"
      . "<fakebold=true underline=true underlineposition=-20% underlinewidth=0.6 leftindent=0>"
      . "Development Inadequacies\n"
      . "<leading=120% fakebold=false underline=false leftindent=4>"
      . "210 Intellectual\n"
      . "220 Emotional\n"
      . "230 Social\n"
      . "240 Physical\n"
      . "<nextline leading=20%>"
      . "<fakebold=true underline=true underlineposition=-20% underlinewidth=0.6 leftindent=0>"
      . "Abuse Victim\n"
      . "<leading=120% fakebold=false underline=false leftindent=4>"
      . "311 Sexual Incest-Received Medical Treatment\n"
      . "312 Sexual incest-No Medical Treatment\n"
      . "314 History of Sexual Incest\n"
      . "321 Exploitation/Neglect-Received Medical Treatment\n"
      . "322 Exploitation/Neglect-No Medical Treatment\n"
      . "331 Psychological-Received Medical Treatment\n"
      . "332 Psychological-No Medical Treatment\n"
      . "341 Physical-Received Medical Treatment\n"
      . "342 Physical-No Medical Treatment\n"
      . "344 History of Physical Abuse\n"
      . "351 Family/Dependent of Abuse Victim-Received Medical Treatment\n"
      . "352 Family/Dependent of Abuse Victim-No Medical Treatment\n"
      . "361 Sexual Assault by Stranger-Received Medical Treatment\n"
      . "362 Sexual Assault by Stranger-No Medical Treatment\n"
      . "364 History of Sexual Abuse\n"
      . "371 Sexual Assault by Acquaintance/Intimate Partner with Medical Treatment\n"
      . "372 Sexual Assault by Acquaintance/Intimate Partner without Medical Treatment\n"
      . "<nextline leading=20%>"
      . "<fakebold=true underline=true underlineposition=-20% underlinewidth=0.6 leftindent=0>"
      . "Social Relations Disturbance\n"
      . "<leading=120% fakebold=false underline=false leftindent=4>"
      . "410 With Family Members\n"
      . "420 Outside Immediate Family\n"
      . "<nextline leading=20%>"
      . "<fakebold=true underline=true underlineposition=-20% underlinewidth=0.6 leftindent=0>"
      . "Social Performance Deficit\n"
      . "<leading=120% fakebold=false underline=false leftindent=4>"
      . "450 Social Performance Deficit\n"
      . "<nextline leading=20%>"
      . "<fakebold=true underline=true underlineposition=-20% underlinewidth=0.6 leftindent=0>"
      . "Emotional Maladjustment/Disturbance\n"
      . "<leading=120% fakebold=false underline=false leftindent=4>"
      . "500 Emotional Maladjustment/Disturbance\n"
      . "501 Depression\n"
      . "502 Anxiety/Panic\n"
      . "503 Eating Disorder\n"
      . "<nextline leading=20%>"
      . "<fakebold=true underline=true underlineposition=-20% underlinewidth=0.6 leftindent=0>"
      . "Thought Disorder/Disturbance\n"
      . "<leading=120% fakebold=false underline=false leftindent=4>"
      . "510 Perceptual Problems\n"
      . "520 Disorientation\n"
      . "530 Other Psychotic Symptoms\n"
      . "<nextline leading=20%>"
      . "<fakebold=true underline=true underlineposition=-20% underlinewidth=0.6 leftindent=0>"
      . "Behavioral Disturbance\n"
      . "<leading=120% fakebold=false underline=false leftindent=4>"
      . "610 Homicidal\n"
      . "620 Assaultive\n"
      . "621 Domestic Abuse Perpetrator\n"
      . "630 Other\n"
      . "631 Involvement with Criminal Justice System\n"
      . "632 Runaway Behavior\n"
      . "633 Attention Deficit/Hyperactivity Disorder\n"
      . "634 Oppositional Defiant Disorder\n"
      . "635 Posttraumatic Stress Disorder\n"
      . "<nextline leading=20%>"
      . "<fakebold=true underline=true underlineposition=-20% underlinewidth=0.6 leftindent=0>"
      . "Suicidal/Self-Abusive\n"
      . "<leading=120% fakebold=false underline=false leftindent=4>"
      . "650 Suicidal/Self-Abusive\n"
      . "<nextline leading=20%>"
      . "<fakebold=true underline=true underlineposition=-20% underlinewidth=0.6 leftindent=0>"
      . "Substance Abuse Related Problems\n"
      . "<leading=120% fakebold=false underline=false leftindent=4>"
      . "710 Alcohol Abuse\n"
      . "711 Alcohol Dependency\n"
      . "720 Drug/Other Abuse\n"
      . "721 Drug/Other Dependency\n"
      . "730 Abuse of <underline=true>Both<underline=false> Alcohol & Drug(s)\n"
      . "731 Dependency on <underline=true>Both<underline=false> Alcohol & Drug(s)\n"
      . "741 At Risk for Relapse (Alcohol)\n"
      . "742 At Risk for Relapse (Drugs)\n"
      . "743 At Risk for Relapse (Both)\n"
      . "745 Dependent Child of an Alcohol Abuse Client\n"
      . "746 Dependent Child of a Drug Abuse Client\n"
      . "747 Dependent Child of <underline=true>Both<underline=false> Alcohol/Drug Abuse Client\n"
      . "748 Co-Dependent of an Alcohol Abuse Client\n"
      . "749 Co-Dependent of a Drug Abuse Client\n"
      . "750 Co-Dependent of <underline=true>Both<underline=false> Alcohol/Drug Abuse Client\n"
      . "751 Family Member or Significant Other of a SA Client\n"
      . "<nextline leading=20%>"
      . "<fakebold=true underline=true underlineposition=-20% underlinewidth=0.6 leftindent=0>"
      . "Gambling\n"
      . "<leading=120% fakebold=false underline=false leftindent=4>"
      . "760 Pathological Gambling\n"
      . "761 Problem Gambling\n"
      . "762 Relative of person with Problem Gambling";

    my $DisabilityIndicators =
"<fakebold=true fontsize=$fontsizemid underline=true underlineposition=-15% underlinewidth=1.0>"
      . "DISABILITY INDICATORS:\n"
      . "<fakebold=false fontsize=$fontsizexsmall underline=false leftindent=6>"
      . "01 None\n"
      . "02 Semi-Ambulatory\n"
      . "03 Non-Ambulatory\n"
      . "04 Severe Sight Disability\n"
      . "05 Blind\n"
      . "06 Organic Based Communication Disability\n"
      . "07 Chronic Health Problem\n"
      . "08 Mental Retardation/Developmental Disability\n"
      . "09 Hard of Hearing\n"
      . "10 Deaf\n"
      . "11 Interpreter for the Deaf (Must 09 or 10)";

    my $DrugsOfChoice =
"<fakebold=true fontsize=$fontsizemid underline=true underlineposition=-15% underlinewidth=1.0>"
      . "DRUGS OF CHOICE:\n"
      . "<fakebold=false fontsize=$fontsizexsmall underline=false leftindent=6>"
      . "01 None\n"
      . "02 Alcohol\n"
      . "03 Heroin\n"
      . "04 Non-RX Methadone\n"
      . "05 Other Opiates & Synthetics\n"
      . "06 Barbiturates\n"
      . "07 Other Sedatives/Hypnotics\n"
      . "08 Amphetamines\n"
      . "09 Cocaine\n"
      . "10 Marijuana/Hashish\n"
      . "11 Other Hallucinogens\n"
      . "12 Inhalants\n"
      . "13 Over-the-Counter\n"
      . "14 Tranquilizers\n"
      . "15 PCP\n"
      . "16 Other\n"
      . "17 Unknown\n"
      . "18 Methamphetamine\n"
      . "19 Benzodiazepine\n"
      . "20 Other Stimulants\n"
      . "21 Club Drug";

    my $ypos = $pagewidth - $margintop_help;

    $p->begin_page_ext( $pageheight, $pagewidth, "" );

##
    # Header line
    $p->setlinewidth(1.0);
    $p->moveto( $marginleft_help, $ypos );
    $p->lineto( $marginleft_help + $contentwidth_help, $ypos );
    $p->stroke();
##

    $p->fit_textline(
"Questions? Call the ODMHSAS PICIS Provider Assistance line at 855-521-6444 or send an email to gethelp\@odmhsas.org",
        $pageheight / 2,
        $ypos + $fontsize,
        $basemidfontoptions . " position={center bottom}"
    );

##

##
    # Page Content
    my $h_transactiontype = 90;
    $ypos -= $h_transactiontype;
    $tf = $p->create_textflow( $TransactionType,
        $basexsmallfontoptions . " leading=120%" );
    my $result = $p->fit_textflow(
        $tf, $marginleft_help, $ypos,
        $marginleft_help + $contentwidth_help / 2,
        $ypos + $h_transactiontype,
        "verticalalign=top"
    );
    if ( $result ne "_stop" ) {
        $result = $p->fit_textflow(
            $tf,
            $marginleft_help + $contentwidth_help / 2,
            $ypos,
            $marginbottom_help + $contentwidth_help,
            $ypos + $h_transactiontype,
            "verticalalign=bottom"
        );
    }

    $ypos -= $fontsizexxsmall;
    my $h_note = 38;
    $ypos -= $h_note;
    $p->setlinewidth(1.0);
    $p->rect( $marginleft_help, $ypos, $contentwidth_help, $h_note );
    $p->stroke();
    $tf = $p->create_textflow( $note,
        $baseboldmidfontoptions . " leading=120% alignment=justify" );
    $p->fit_textflow(
        $tf, $marginleft_help + 2,
        $ypos,
        $marginleft_help + $contentwidth_help - 2,
        $ypos + $h_note + 2,
        "verticalalign=top"
    );

    $ypos -= $fontsizexxsmall;

    my $h_servicefocus = 54;
    $ypos -= $h_servicefocus;
    $x = $marginleft_help;
    my $w_servicefocus_column_1 = 140;
    my $w_servicefocus_column_2 = 148;
    my $w_servicefocus_column_3 = 120;
    $tf = $p->create_textflow( $ServiceFocus,
        $basexsmallfontoptions . " leading=120%" );
    my $result = $p->fit_textflow(
        $tf, $x + 2, $ypos,
        $x + $w_servicefocus_column_1,
        $ypos + $h_servicefocus,
        "verticalalign=top"
    );

    if ( $result ne "_stop" ) {
        $x += $w_servicefocus_column_1;
        $result = $p->fit_textflow(
            $tf, $x + 2, $ypos,
            $x + $w_servicefocus_column_2,
            $ypos + $h_servicefocus,
            "verticalalign=top"
        );
    }
    if ( $result ne "_stop" ) {
        $x += $w_servicefocus_column_2;
        $result = $p->fit_textflow(
            $tf, $x + 2, $ypos,
            $x + $w_servicefocus_column_3,
            $ypos + $h_servicefocus,
            "verticalalign=top"
        );
    }
    if ( $result ne "_stop" ) {
        $x += $w_servicefocus_column_3;
        $result = $p->fit_textflow(
            $tf, $x + 2, $ypos,
            $marginleft + $contentwidth_help,
            $ypos + $h_servicefocus,
            "verticalalign=top"
        );
    }

    $ypos -= $fontsizexxsmall;

    $ypos -= $fontsizemid;
    $p->fit_textline( "REFERRAL:", $marginleft_help, $ypos,
        $baseboldmidfontoptions_u );
    $p->fit_textline(
        "(Primary and Secondary)",
        $marginleft_help + 56,
        $ypos, $basemidfontoptions
    );
    my $h_referral = 130;
    $ypos -= $h_referral;
    $x = $marginleft_help;
    my $w_referral_column_1 = 140;
    my $w_referral_column_2 = 200;
    $tf = $p->create_textflow( $Referral,
        $basexsmallfontoptions . " leading=120%" );
    my $result = $p->fit_textflow(
        $tf, $x + 8, $ypos,
        $x + $w_referral_column_1,
        $ypos + $h_referral,
        "verticalalign=top"
    );

    if ( $result ne "_stop" ) {
        $x += $w_referral_column_1;
        $result = $p->fit_textflow(
            $tf, $x, $ypos,
            $x + $w_referral_column_2,
            $ypos + $h_referral,
            "verticalalign=top"
        );
    }
    if ( $result ne "_stop" ) {
        $x += $w_referral_column_2;
        $result = $p->fit_textflow(
            $tf, $x, $ypos,
            $marginleft_help + $contentwidth_help,
            $ypos + $h_referral,
            "verticalalign=top"
        );
    }

    $p->moveto( $marginleft_help, $ypos );
    $p->lineto( $marginleft_help + $contentwidth_help, $ypos );
    $p->stroke();

    $ypos -= ( $fontsizelarge + 1 );
    $p->fit_textline( "LANGUAGE", $marginleft_help, $ypos,
        $baseboldmidfontoptions_u );
    $p->fit_textline( "1 - Spanish", $marginleft_help + 70,
        $ypos + 1, $basexsmallfontoptions );
    $p->fit_textline( "3 - German", $marginleft_help + 185,
        $ypos + 1, $basexsmallfontoptions );
    $p->fit_textline(
        "5 - Vietnamese",
        $marginleft_help + 235,
        $ypos + 1, $basexsmallfontoptions
    );
    $p->fit_textline(
        "7 - Slavic (Russian, Polish, etc.)",
        $marginleft_help + 320,
        $ypos + 1, $basexsmallfontoptions
    );
    $p->fit_textline(
        "9 - Other (specify)",
        $marginleft_help + 430,
        $ypos + 1,
        $basexsmallfontoptions
    );

    $ypos -= ( $fontsizelarge + 1 );
    $p->fit_textline( "PROFICIENCY:", $marginleft_help, $ypos,
        $baseboldmidfontoptions_u );
    $p->fit_textline(
        "2 - Native North American (specify)",
        $marginleft_help + 70,
        $ypos + 1, $basexsmallfontoptions
    );
    $p->fit_textline( "4 - French", $marginleft_help + 185,
        $ypos + 1, $basexsmallfontoptions );
    $p->fit_textline( "6 - Chinese", $marginleft_help + 235,
        $ypos + 1, $basexsmallfontoptions );
    $p->fit_textline(
        "8 - Sign Language",
        $marginleft_help + 320,
        $ypos + 1, $basexsmallfontoptions
    );

    $ypos -= $fontsizexxsmall;

    my $h_legalstatus = 30;
    $ypos -= $h_legalstatus;
    $x = $marginleft_help;
    my $w_legalstaus_column_1 = 110;
    my $w_legalstaus_column_2 = 170;
    my $w_legalstaus_column_3 = 120;
    $tf = $p->create_textflow( $LegalStatus,
        $basexsmallfontoptions . " leading=120%" );
    my $result = $p->fit_textflow(
        $tf, $x, $ypos,
        $x + $w_referral_column_1,
        $ypos + $h_legalstatus,
        "verticalalign=top"
    );

    if ( $result ne "_stop" ) {
        $x += $w_legalstaus_column_1;
        $result = $p->fit_textflow(
            $tf, $x, $ypos,
            $x + $w_legalstaus_column_2,
            $ypos + $h_legalstatus,
            "verticalalign=center"
        );
    }
    if ( $result ne "_stop" ) {
        $x += $w_legalstaus_column_2;
        $result = $p->fit_textflow(
            $tf, $x, $ypos,
            $x + $w_legalstaus_column_3,
            $ypos + $h_legalstatus,
            "verticalalign=center"
        );
    }
    if ( $result ne "_stop" ) {
        $x += $w_legalstaus_column_3;
        $result = $p->fit_textflow(
            $tf, $x, $ypos,
            $marginleft_help + $contentwidth_help,
            $ypos + $h_legalstatus,
            "verticalalign=center"
        );
    }

    $ypos -= 3;

    my $h_presentprob = 245;
    $ypos -= $h_presentprob;
    $x = $marginleft_help;
    my $w_presentprob_column_1 = 198;
    my $w_presentprob_column_2 = 173;
    $tf = $p->create_textflow( $PresentingProblem,
        $basexsmallfontoptions . " leading=120%" );
    my $result = $p->fit_textflow(
        $tf, $x, $ypos,
        $x + $w_presentprob_column_1,
        $ypos + $h_presentprob,
        "verticalalign=top"
    );

    if ( $result ne "_stop" ) {
        $x += $w_presentprob_column_1;
        $result = $p->fit_textflow(
            $tf, $x, $ypos,
            $x + $w_presentprob_column_2,
            $ypos + $h_presentprob,
            "verticalalign=top"
        );
    }
    if ( $result ne "_stop" ) {
        $x += $w_presentprob_column_2;
        $result = $p->fit_textflow(
            $tf, $x, $ypos,
            $marginleft_help + $contentwidth_help,
            $ypos + $h_presentprob,
            "verticalalign=top"
        );
    }

    my $h_disability        = 150;
    my $y_offset_disability = 120;
    $tf = $p->create_textflow( $DisabilityIndicators,
        $basexsmallfontoptions . " leading=120%" );
    my $result = $p->fit_textflow(
        $tf,
        $x,
        $ypos - $y_offset_disability,
        $marginleft_help + $contentwidth_help,
        $ypos - $y_offset_disability + $h_disability,
        "verticalalign=top"
    );

    $ypos -= $fontsizexxsmall;

    my $h_drugsofchoice = 58;
    my $w_drugsofchoice = 325;
    $ypos -= $h_drugsofchoice;
    $p->setlinewidth(1.0);
    $p->rect( $marginleft_help, $ypos, $marginleft_help + $w_drugsofchoice,
        $h_drugsofchoice );
    $p->stroke();
    $x = $marginleft_help;
    my $w_drugsofchoice_column_1 = 100;
    my $w_drugsofchoice_column_2 = 100;
    my $w_drugsofchoice_column_3 = 75;
    $tf = $p->create_textflow( $DrugsOfChoice,
        $basexsmallfontoptions . " leading=120%" );
    my $result = $p->fit_textflow(
        $tf, $x + 2, $ypos,
        $x + $w_drugsofchoice_column_1,
        $ypos + $h_drugsofchoice,
        "verticalalign=top"
    );

    if ( $result ne "_stop" ) {
        $x += $w_drugsofchoice_column_1;
        $result = $p->fit_textflow(
            $tf, $x, $ypos,
            $x + $w_drugsofchoice_column_2,
            $ypos + $h_drugsofchoice,
            "verticalalign=center"
        );
    }
    if ( $result ne "_stop" ) {
        $x += $w_drugsofchoice_column_2;
        $result = $p->fit_textflow(
            $tf, $x, $ypos,
            $x + $w_drugsofchoice_column_3,
            $ypos + $h_drugsofchoice,
            "verticalalign=center"
        );
    }
    if ( $result ne "_stop" ) {
        $x += $w_drugsofchoice_column_3;
        $result = $p->fit_textflow(
            $tf, $x, $ypos,
            $marginleft + 355,
            $ypos + $h_drugsofchoice,
            "verticalalign=center"
        );
    }

    $ypos -= ( $fontsizelarge + 1 );
    $p->fit_textline( "USUAL ROUTE OF ADMINISTRATION:",
        $marginleft_help, $ypos, $baseboldmidfontoptions_u );
    $p->fit_textline( "1 - Oral", $marginleft_help + 175,
        $ypos + 1, $basexsmallfontoptions );
    $p->fit_textline( "2 - Smoking", $marginleft_help + 205,
        $ypos + 1, $basexsmallfontoptions );
    $p->fit_textline(
        "3 - Inhalation",
        $marginleft_help + 245,
        $ypos + 1, $basexsmallfontoptions
    );
    $p->fit_textline(
        "4 - Injection",
        $marginleft_help + 295,
        $ypos + 1, $basexsmallfontoptions
    );
    $p->fit_textline( "5 - Other", $marginleft_help + 335,
        $ypos + 1, $basexsmallfontoptions );

    $ypos -= ( $fontsizelarge + 1 );
    $p->fit_textline( "FREQUENCY OF USE:",
        $marginleft_help, $ypos, $baseboldmidfontoptions_u );
    $p->fit_textline(
        "1 - No Past Month Use",
        $marginleft_help + 102,
        $ypos + 1,
        $basexsmallfontoptions
    );
    $p->fit_textline(
        "2 - 1-3 Times/Month",
        $marginleft_help + 182,
        $ypos + 1,
        $basexsmallfontoptions
    );
    $p->fit_textline(
        "3 - 1-2 Times/Week",
        $marginleft_help + 250,
        $ypos + 1,
        $basexsmallfontoptions
    );
    $p->fit_textline(
        "4 - 3-6 Times/Week",
        $marginleft_help + 315,
        $ypos + 1,
        $basexsmallfontoptions
    );
    $p->fit_textline( "5 - Daily", $marginleft_help + 390,
        $ypos + 1, $basexsmallfontoptions );

    $ypos -= ( $fontsizelarge + 1 );
    $p->fit_textline( "LEVEL OF CARE:",
        $marginleft_help, $ypos, $baseboldmidfontoptions_u );
    $p->fit_textline(
        "CI - Residential Treatment",
        $marginleft_help + 80,
        $ypos + 1, $basexsmallfontoptions
    );
    $p->fit_textline(
        "CL - Community Living/Halfway House/ResCare",
        $marginleft_help + 175,
        $ypos + 1, $basexsmallfontoptions
    );
    $p->fit_textline(
        "HA - Inpatient",
        $marginleft_help + 335,
        $ypos + 1, $basexsmallfontoptions
    );

    $ypos -= $fontsizemid;
    $p->fit_textline(
        "OO - Outpatient",
        $marginleft_help + 80,
        $ypos + 1, $basexsmallfontoptions
    );
    $p->fit_textline(
        "SC - Community-Based Structured Crisis",
        $marginleft_help + 175,
        $ypos + 1, $basexsmallfontoptions
    );
    $p->fit_textline( "SN - Detox", $marginleft_help + 335,
        $ypos + 1, $basexsmallfontoptions );
##

    # Footer line
    $p->setlinewidth(1.0);
    $p->moveto( $marginleft_help, $marginbottom_help );
    $p->lineto( $marginleft_help + $contentwidth_help, $marginbottom_help );
    $p->stroke();
##
    $p->fit_textline(
        "ODMHSAS CDC (back) Revised August 25, 2011 by MAR",
        $marginleft_help, $marginbottom_help - $fontsizexlarge,
        $basemidfontoptions
    );

    $p->end_page_ext("");
}

sub convertDateTime {
    my ( $self, $str ) = @_;

    my @arr = split( ':', $str );

    if ( $#arr ne 1 ) {
        return "";
    }

    my $hrs  = length( $arr[0] ) eq 2 ? $arr[0] : "0" . $arr[0];
    my $mins = length( $arr[1] ) eq 2 ? $arr[1] : "0" . $arr[1];

    return $hrs . $mins;
}
