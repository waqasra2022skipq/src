#!/usr/bin/perl
############################################################################
use lib '/var/www/okmis/src/lib';
use DBI;
use myForm;
use myDBI;
use DBA;
use MgrTree;
use DBUtil;
use utf8;
use Time::Local;
my $DT = localtime();

use PDFlib::PDFlib;
use strict;
############################################################################

my $form = myForm->new();
my $IDs  = $form->{'IDs'};
my $dbh  = myDBI->dbconnect( $form->{'DBNAME'} );

#warn "printClientTrPlan: IDs=${IDs}\n";
##
# prepare selects...
##
my $sClientProblems = $dbh->prepare(
"select ClientProblems.ID,ClientProblems.Locked,misICD10.ICD10, misICD10.icdName, misICD10.sctName, DATE_FORMAT(ClientProblems.InitiatedDate,'%m/%d/%Y') as InitiatedDate, DATE_FORMAT(ClientProblems.ResolvedDate,'%m/%d/%Y') as ResolvedDate, ClientProblems.Priority from ClientProblems left join okmis_config.misICD10 on misICD10.ID = ClientProblems.UUID where ClientProblems.ClientID=? order by ClientProblems.Priority"
);
my $sClientTrPlan = $dbh->prepare("select * from ClientTrPlan where ID=?");
my $sClient       = $dbh->prepare(
"select Client.*,ClientIntake.Services,ClientIntake.ServiceFocus,ClientSummary.Overall from Client left join ClientIntake on ClientIntake.ClientID=Client.ClientID left join ClientSummary on ClientSummary.ClientID=Client.ClientID where Client.ClientID=?"
);
my $sProvider = $dbh->prepare(
"select Provider.*, ProviderControl.LOGO from Provider left join ProviderControl on ProviderControl.ProvID=Provider.ProvID where Provider.ProvID=?"
);
my $qClientTrPlanPG =
  qq|select * from ClientTrPlanPG where TrPlanID=? order by Priority|;
my $sClientTrPlanPG = $dbh->prepare($qClientTrPlanPG);
my $qClientTrPlanOBJ =
  qq|select * from ClientTrPlanOBJ where TrPlanPGID=? order by Priority|;
my $sClientTrPlanOBJ = $dbh->prepare($qClientTrPlanOBJ);
my $sClientTrPlanS   = $dbh->prepare(
    "select * from ClientTrPlanS where TrPlanID=? order by SignDate");
my $sClientTrPlanSProv = $dbh->prepare(
"select ClientTrPlanS.*,Provider.FName,Provider.LName from ClientTrPlanS left join ClientTrPlan on ClientTrPlan.ID=ClientTrPlanS.TrPlanID left join Provider on Provider.ProvID=ClientTrPlanS.ProvID where ClientTrPlanS.TrPlanID=? and ClientTrPlanS.ProvID=? order by ClientTrPlanS.SignDate"
);
my $qCredentials =
qq|select PIN,Abbr from Credentials left join okmis_config.xCredentials on xCredentials.ID=Credentials.CredID where ProvID=? and InsID=? order by Credentials.Rank|;
my $sCredentials = $dbh->prepare($qCredentials);
my $sInsurance   = $dbh->prepare(
"select * from Insurance where ClientID=? and Priority=1 order by InsNumEffDate desc"
);

my $searchpath = "../data";

my $pagewidth  = 595;
my $pageheight = 842;

my $fontname        = "Roboto-Light";
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
my $basemidfontoptions     = $basefontoptions . " fontsize=" . $fontsizemid;
my $baseboldmidfontoptions = $baseboldfontoptions . " fontsize=" . $fontsizemid;
my $baselargefontoptions   = $basefontoptions . " fontsize=" . $fontsizelarge;
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

my $marginleft   = 40;
my $margintop    = 35;
my $marginbottom = 35;
my $contentwidth = $pagewidth - 2 * $marginleft;
my $h_footer     = 5 * $fontsizemid;

my $footertext =
"<fakebold=true>Confidentiality of drug/alcohol abuse records is protected by Federal Law."
  . "<fakebold=false> Federal regulations (42 CFR, Part 2 prohibits making any further disclosure of this information unless further disclosure is expressively permitted by written consent of the person to whom it pertains or as otherwise permitted by 42 CFR, Part 2. A GENERAL AUTHORIZATION FOR RELEASE OF MEDICAL OR OTHER INFORMATION IS NOT SUFFICIENT FOR THIS PURPOSE. The Federal rules restrict any use of the information to criminally investigate or prosecute any alcohol/drug abuse client.";

my $ypos       = $pageheight - $margintop;
my $pagecount  = 0;
my $totalcount = 0;

my $filename = '/tmp/'
  . $form->{'LOGINID'} . '_'
  . DBUtil->genToken() . '_'
  . DBUtil->Date( '', 'stamp' ) . '.pdf';
my $outfile = $form->{'file'} eq ''    # create and print pdf else just create.
  ? $form->{'DOCROOT'} . $filename
  : $form->{'file'};
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

    $p->set_info( "Creator", "Treatment Plan" );
    $p->set_info( "Author",  "Keith Stephenson" );
    $p->set_info( "Title",   "Treatment Plan 2019-09-01" );

    printTrPlan($p);

    $p->end_document("");

};

if ($@) {
    die("$0: PDFlib Exception occurred:\n$@");
}
$sClientTrPlan->finish();
$sClientTrPlanPG->finish();
$sClientTrPlanS->finish();
$sClientTrPlanSProv->finish();
$sClientProblems->finish();
$sProvider->finish();
$sCredentials->finish();
$sInsurance->finish();
$sClient->finish();
myDBI->cleanup();

if ( $form->{'file'} eq '' )    # create and print pdf.
{ print qq|Location: ${filename}\n\n|; }
exit;
############################################################################

sub printTrPlan {
    my ($p) = @_;

    foreach my $ID ( split( ' ', $IDs ) ) {

        #warn qq|ID=$ID\n|;
        $sClientTrPlan->execute($ID)
          || myDBI->dberror("printClientTrPlan: select ClientTrPlan $ID");
        while ( my $rClientTrPlan = $sClientTrPlan->fetchrow_hashref ) {
            $sClient->execute( $rClientTrPlan->{ClientID} )
              || myDBI->dberror(
                "printClientTrPlan: select Client $rClientTrPlan->{'ClientID'}"
              );
            my $rClient = $sClient->fetchrow_hashref;
            my $ProvID  = $rClient->{ProvID};
            $sProvider->execute($ProvID)
              || myDBI->dberror("printClientTrPlan: select Provider $ProvID");
            my $rPrimaryProvider = $sProvider->fetchrow_hashref;

            create_pages( $p, $rClientTrPlan, $rClient, $rPrimaryProvider );
            $totalcount++;
        }
    }
    if   ($totalcount) { create_pagecount($p); }
    else               { create_empty_page($p); }

    #warn "printClientTrPlan: pagecount=${pagecount}\n";
    return ($totalcount);
}

sub create_empty_page {
    my ($p) = @_;

    $p->begin_page_ext( $pagewidth, $pageheight, "" );
    $p->fit_textline(
        "NOT FOUND $IDs",
        $marginleft, $pageheight - 50,
        $basefontoptions
    );
    $p->end_page_ext("");
}

sub create_header {
    my ( $p, $Title, $rClient ) = @_;

##
    # Header info...
    my $AgencyID = MgrTree->getAgency( $form, $rClient->{clinicClinicID} );

    #warn qq|AgencyID=${AgencyID}\n|;
    $sProvider->execute($AgencyID)
      || myDBI->dberror(
        "printClientTrPlan: select Provider AgencyID=${AgencyID}");
    my $rAgency    = $sProvider->fetchrow_hashref;
    my $AgencyName = $rAgency->{Name};
    my $AgencyAddr = $rAgency->{'Addr1'};
    $AgencyAddr .= ', ' . $rAgency->{'Addr2'} if ( $rAgency->{'Addr2'} );
    my $AgencyCSZ =
      $rAgency->{'City'} . ', ' . $rAgency->{'ST'} . '  ' . $rAgency->{'Zip'};
    my $AgencyPh =
      'Office: ' . $rAgency->{'WkPh'} . '  Fax: ' . $rAgency->{'Fax'};
    my $reportInfo = '';    # right side of heading
##
    my $Company  = $AgencyName;
    my $Address  = "$AgencyAddr\n$AgencyCSZ";
    my $OffceFax = $AgencyPh;

    my $tf;

    $p->begin_page_ext( $pagewidth, $pageheight, "" );
    $ypos = $pageheight - $margintop;

    $ypos -= $fontsizelarge;
    $p->fit_textline( $Company, $pagewidth / 2,
        $ypos, $baseboldlargefontoptions . " position={center bottom}" );

    my $h_address = 2 * $fontsizexxlarge;
    $ypos -= $h_address;
    my $w_address = 150;
    my $x_address = $pagewidth / 2 - $w_address / 2;
    $tf = $p->create_textflow( $Address,
        $baseboldlargefontoptions
          . " leading=110% alignment=justify lastalignment=center" );
    $p->fit_textflow(
        $tf, $x_address, $ypos,
        $x_address + $w_address,
        $ypos + $h_address,
        "verticalalign=center"
    );

    $ypos -= $fontsizelarge;
    $p->fit_textline( $OffceFax, $pagewidth / 2,
        $ypos, $baseboldlargefontoptions . " position={center bottom}" );

    # -----------------------------------
    # Place image of logo
    # -----------------------------------
    my $y_offsetlogo = 2;
    $ypos -= $y_offsetlogo;
    my $h_logo = $pageheight - $margintop - $ypos;
    my $w_logo = 150;

    my ( $logodirectory, $logofilename ) = $rAgency->{'LOGO'} =~ m/(.*\/)(.*)$/;
    if    ( $logofilename eq '' ) { $logofilename = 'logo.png'; }
    elsif ( not -e "/usr/local/PDFlib/${logofilename}" ) {
        $logofilename = 'logo.png';
    }
    my $logoimage = $p->load_image( "auto", $logofilename, "" );
    $p->fit_image( $logoimage, $marginleft, $ypos,
        "boxsize={" . $w_logo . " " . $h_logo . "} fitmethod=meet" );
    $p->close_image($logoimage);
    ##

    $ypos -= $fontsizexlarge;
    $p->fit_textline( $Title, $pagewidth / 2,
        $ypos, $baseboldlargefontoptions . " position={center bottom}" );

    $ypos -= $fontsizexxlarge;

}

sub create_footer {
    my ( $p, $ClientName, $ClientID, $DT ) = @_;

    my $tf;
    my $optlist;

    $optlist = $basesmallfontoptions . " leading=120% alignment=justify";
    $tf      = $p->create_textflow( $footertext, $optlist );
    $p->fit_textflow(
        $tf, $marginleft, $marginbottom,
        $marginleft + $contentwidth,
        $marginbottom + $h_footer,
        "verticalalign=top"
    );

    my $font = $p->load_font( $fontname, "unicode", "" );
    $p->setfont( $font, $fontsizelarge );
    $p->show_xy( "$ClientName ($ClientID) ", $marginleft, $marginbottom );
    $p->show_xy( $DT, $pagewidth - $marginleft - 120,     $marginbottom );
    $p->show_xy(
        "Page " . ( ++$pagecount ),
        $pagewidth / 2 - 20,
        $marginbottom
    );
    $p->suspend_page("");
}

sub create_pagecount {
    my ($p) = @_;

    for ( my $i = 1 ; $i < $pagecount + 1 ; $i++ ) {

        # Revisit page $i
        $p->resume_page("pagenumber $i");

        # Add the total number of pages
        $p->show( " of " . $pagecount );
        $p->end_page_ext("");
    }
}

sub create_pages {
    my ( $p, $rClientTrPlan, $rClient, $rPrimaryProvider ) = @_;

#foreach my $f ( sort keys %{$rClientTrPlan} ) { warn ": rClientTrPlan-$f=$rClientTrPlan->{$f}\n"; }
# Client info...
    my $ClientID   = $rClient->{ClientID};
    my $ClientName = qq|$rClient->{FName} $rClient->{LName}|;
    my $TrPlanID   = $rClientTrPlan->{ID};
    my $IntDatefmt =
      DBUtil->Date( $rClientTrPlan->{IntDate}, 'fmt', 'MM/DD/YYYY' );
    my $CompleteDate =
        $rClientTrPlan->{'PGSigDate'} eq ''
      ? $rClientTrPlan->{'ClSigDate'}
      : $rClientTrPlan->{'PGSigDate'};
    $sClientTrPlanS->execute($TrPlanID)
      || myDBI->dberror("printClientTrPlan: select ClientTrPlanS ");
    if ( my $rClientTrPlanS = $sClientTrPlanS->fetchrow_hashref ) {
        $CompleteDate = $rClientTrPlanS->{'SignDate'};
    }
    my $DCompleted      = DBUtil->Date( $CompleteDate, 'fmt', 'MM/DD/YYYY' );
    my $PersonsInvolved = $rClientTrPlan->{'PersonsInvolved'};
##
    my $ServiceFocus =
      DBA->getxref( $form, 'xServiceFocus', $rClient->{'ServiceFocus'},
        'Descr' );
    my $TrPlanType =
      DBA->getxref( $form, 'xTrPlanType', $rClientTrPlan->{'Type'}, 'Descr' );
    my $Title = uc qq|${ServiceFocus} ${TrPlanType}|;    # bottom of heading
    my $Strengths              = main->getStrengths( $rClientTrPlan, 'none' );
    my $Needs                  = main->getNeeds( $rClientTrPlan, 'none' );
    my $ClientPreference       = $rClientTrPlan->{'Preferences'};
    my $ClientExpectation      = $rClient->{'Overall'};
    my $DischargeCriteria      = $rClientTrPlan->{'DischargeCriteria'};
    my $TransitionPlan         = $rClientTrPlan->{'TransitionPlan'};
    my $CollaborativeReferrals = main->getNPIs( $rClientTrPlan->{ReferralsNPI},
        'CollaborativeReferrals', 'None' );
    my $Theoretical = '';

    foreach
      my $t ( split( chr(253), $rClientTrPlan->{Theoretical} ) )   # multivalues
    {
        $Theoretical .= qq|  |
          . DBA->getxref( $form, 'xTrPlanTheoretical', $t, 'Descr' ) . qq|\n|;
    }
    my $Services = '';
    foreach
      my $s ( split( chr(253), $rClientTrPlan->{Services} ) )      # multivalues
    {
        $Services .=
          qq|  | . DBA->getxref( $form, 'xServices', $s, 'Descr' ) . qq|\n|;
    }

    $sProvider->execute( $rClientTrPlan->{CreateProvID} )
      || myDBI->dberror(
"printClientTrPlan: select Provider CreateProvID=$rClientTrPlan->{'CreateProvID'}"
      );
    my $rEnteredBy = $sProvider->fetchrow_hashref;
    my $EnteredBy  = qq|$rEnteredBy->{FName} $rEnteredBy->{LName}|;
    my $EnteredDate =
      DBUtil->Date( $rClientTrPlan->{CreateDate}, 'fmt', 'MM/DD/YYYY' );

    $sInsurance->execute( $rClientTrPlan->{ClientID} )
      || myDBI->dberror("printClientTrPlan: select Insurance $ClientID");
    my $rInsurance = $sInsurance->fetchrow_hashref;

    my $ClientCopy = $rClientTrPlan->{'ClientCopy'} ? '  Yes' : '  No';
    my $ReceivedBy =
        $rClientTrPlan->{'ReceivedBy'} eq 'M' ? '  Mail'
      : $rClientTrPlan->{'ReceivedBy'} eq 'P' ? '  In Person'
      :                                         '  Unknown';
    my $OthersCopy = '';
    my $dlm        = '';
    foreach my $s ( split( chr(253), $rClientTrPlan->{OthersCopy} ) ) {
        $OthersCopy .=
          $dlm . DBA->getxref( $form, 'xRelationship', $s, 'Descr' );
        $dlm = '; ';
    }
    $OthersCopy = 'None' if ( $OthersCopy eq '' );

    # page
    $sProvider->execute( $rClientTrPlan->{'StaffID'} )
      || myDBI->dberror(
        "printClientTrPlan: select Staff $rClientTrPlan->{StaffID}");
    my $rStaff = $sProvider->fetchrow_hashref;
    my $staff  = qq|$rStaff->{FName} $rStaff->{LName}|;

    my $DateCompleted         = $DCompleted;
    my $PersonsInvolved       = $PersonsInvolved;
    my @ClientProblemsHeaders = (
        "ICD10",
        "ICD Name",
        "SNOMED Name",
        "Initiated Date",
        "Resolved Date"
    );
    my @ClientProblems    = main->getProblems( $rClientTrPlan->{ClientID} );
    my $preferences       = $ClientPreference;
    my $expectation       = $ClientExpectation;
    my $DischargeCriteria = $DischargeCriteria;
    my $EstDischargeDate =
      DBUtil->Date( $rClientTrPlan->{EstDischargeDate}, 'fmt', 'MM/DD/YYYY' );
    my $TransitionPlan      = $TransitionPlan;
    my $CollReferrals       = $CollaborativeReferrals;
    my $approaches          = $Theoretical;
    my $HistoricalInfo      = $rClientTrPlan->{'Comments'};
    my $InterpretiveSummary = $rClientTrPlan->{'Summary'};
    my $WasGivenCopy        = $ClientCopy;
    my $ReceivedResource    = $ReceivedBy;
    my $OthersGivenCopy     = $OthersCopy;
    my $StaffRes            = $staff;

    my $tf;
    my $result;
    my $h_tf;
    my $row = 1;
    my $col = 1;
    my $tbl = -1;
    my $optlist;
    my $text;

    create_header( $p, $Title, $rClient );

    $ypos -= $fontsizelarge;
    $p->fit_textline( "Client Name:", $marginleft, $ypos,
        $baseboldlargefontoptions_u );
    $p->fit_textline( $ClientName, $marginleft + 70, $ypos, $basefontoptions );
    $p->fit_textline(
        "Client ID#:", $marginleft + $contentwidth / 3,
        $ypos,         $baseboldlargefontoptions_u
    );
    $p->fit_textline( $ClientID, $marginleft + $contentwidth / 3 + 57,
        $ypos, $basefontoptions );
    $p->fit_textline(
        "Date Completed:",
        $marginleft + $contentwidth * 2 / 3,
        $ypos, $baseboldlargefontoptions_u
    );
    $p->fit_textline( $DateCompleted, $marginleft + $contentwidth * 2 / 3 + 89,
        $ypos, $basefontoptions );

    $ypos -= ( $fontsizexxlarge + $fontsizelarge );
    $p->fit_textline( "Persons Involved with Treatment/Transition Planning:",
        $marginleft, $ypos, $baseboldlargefontoptions_u );
    $ypos -= 2;
    $tf = $p->create_textflow( $PersonsInvolved,
        $basefontoptions . " leading=120%" . " alignment=justify" );
    $h_tf = render_textflow( $p, $tf, $Title, $rClient );

    $ypos -= ( $h_tf + $fontsizexxlarge );
    $p->fit_textline( "Client Problems:",
        $marginleft, $ypos, $baseboldlargefontoptions_u );

    for ( $col = 1 ; $col <= $#ClientProblemsHeaders + 1 ; $col++ ) {
        $optlist =
            "fittextline={position={left center} "
          . $baseboldlargefontoptions_u
          . "} margin=2"
          . ( $col eq 1 ? " marginleft=0" : "" );
        $tbl = $p->add_table_cell( $tbl, $col, $row,
            $ClientProblemsHeaders[ $col - 1 ], $optlist );
    }
    $row++;
    for ( my $i = 0 ; $i < $#ClientProblems + 1 ; $i++ ) {
        $col = 1;
        $optlist =
            "fittextline={position={left center} "
          . $basefontoptions
          . "} margin=2"
          . ( $col ne 4 ? " marginright=$fontsize" : "" );
        $tbl =
          $p->add_table_cell( $tbl, $col++, $row, $ClientProblems[$i]{icd10},
            $optlist );

        $tf = $p->add_textflow( -1, $ClientProblems[$i]{icdName},
            $basefontoptions );
        $tbl = $p->add_table_cell( $tbl, $col++, $row, "",
            $optlist . " textflow=" . $tf . " colwidth=35%" );

        $tf = $p->add_textflow( -1, $ClientProblems[$i]{snomedName},
            $basefontoptions );
        $tbl = $p->add_table_cell( $tbl, $col++, $row, "",
            $optlist . " textflow=" . $tf . " colwidth=35%" );

        $tbl = $p->add_table_cell( $tbl, $col++, $row,
            $ClientProblems[$i]{initiatedDate}, $optlist );
        $tbl = $p->add_table_cell( $tbl, $col++, $row,
            $ClientProblems[$i]{resolvedDate}, $optlist );
        $row++;
    }
    my $h_tbl = render_table( $p, $tbl, $Title, $rClient );

    $ypos -= ( $h_tbl + $fontsizelarge );
    $p->fit_textline( "Strengths / Abilities ",
        $marginleft, $ypos, $baseboldlargefontoptions_u );
    $p->fit_textline(
        "(In Client's Words)",
        $marginleft + 102,
        $ypos, $baseboldlargefontoptions_ui
    );
    $ypos -= 2;
    $tf = $p->create_textflow( $Strengths,
        $basefontoptions . " leading=120%" . " alignment=justify" );
    $h_tf = render_textflow( $p, $tf, $Title, $rClient );

    $ypos -= ( $h_tf + $fontsizexxlarge );
    $p->fit_textline( "Needs, Liabilities, and Barriers ",
        $marginleft, $ypos, $baseboldlargefontoptions_u );
    $p->fit_textline(
        "(In Client's Words)",
        $marginleft + 154,
        $ypos, $baseboldlargefontoptions_ui
    );
    $ypos -= 2;
    $tf = $p->create_textflow( $Needs,
        $basefontoptions . " leading=120%" . " alignment=justify" );
    $h_tf = render_textflow( $p, $tf, $Title, $rClient );

    $ypos -= ( $h_tf + $fontsizexxlarge );
    $p->fit_textline( "Client's Preferences:",
        $marginleft, $ypos, $baseboldlargefontoptions_u );
    $ypos -= 2;
    $tf = $p->create_textflow( $preferences,
        $basefontoptions . " leading=120%" . " alignment=justify" );
    $h_tf = render_textflow( $p, $tf, $Title, $rClient );

    $ypos -= ( $h_tf + $fontsizexxlarge );
    $p->fit_textline( "Client's Overall Expectation from Treatment:",
        $marginleft, $ypos, $baseboldlargefontoptions_u );
    $ypos -= 2;
    $tf = $p->create_textflow( $expectation,
        $basefontoptions . " leading=120%" . " alignment=justify" );
    $h_tf = render_textflow( $p, $tf, $Title, $rClient );

    $ypos -= ( $h_tf + $fontsizexxlarge );
    $p->fit_textline( "Discharge Criteria:",
        $marginleft, $ypos, $baseboldlargefontoptions_u );
    $p->fit_textline(
        "Estimated Discharge Date:",
        $pagewidth / 2,
        $ypos, $baseboldlargefontoptions_u
    );
    $p->fit_textline( $EstDischargeDate, $pagewidth - $marginleft - 45,
        $ypos, $basefontoptions );
    $ypos -= 2;
    $tf = $p->create_textflow( $DischargeCriteria,
        $basefontoptions . " leading=120%" . " alignment=justify" );
    $h_tf = render_textflow( $p, $tf, $Title, $rClient );

    $ypos -= ( $h_tf + $fontsizexxlarge );
    $p->fit_textline( "Transition / Aftercare Plan:",
        $marginleft, $ypos, $baseboldlargefontoptions_u );
    $ypos -= 2;
    $tf = $p->create_textflow( $TransitionPlan,
        $basefontoptions . " leading=120%" . " alignment=justify" );
    $h_tf = render_textflow( $p, $tf, $Title, $rClient );

    $ypos -= ( $h_tf + $fontsizexxlarge );
    $p->fit_textline( "Collaborative Referrals:",
        $marginleft, $ypos, $baseboldlargefontoptions_u );
    $ypos -= 2;
    $tf = $p->create_textflow( $CollReferrals,
        $basefontoptions . " leading=120%" . " alignment=justify" );
    $h_tf = render_textflow( $p, $tf, $Title, $rClient );

    $ypos -= ( $h_tf + $fontsizexxlarge );
    $p->fit_textline( "Services to be provided:",
        $marginleft, $ypos, $baseboldlargefontoptions_u );
    $ypos -= 2;
    $tf = $p->create_textflow( $Services,
        $basefontoptions . " leading=120%" . " alignment=justify" );
    $h_tf = render_textflow( $p, $tf, $Title, $rClient );

    $ypos -= ( $h_tf + $fontsizexxlarge );
    $p->fit_textline( "Theoretical approach(es) of individual psychotherapy:",
        $marginleft, $ypos, $baseboldlargefontoptions_u );
    $ypos -= 2;
    $tf = $p->create_textflow( $approaches,
        $basefontoptions . " leading=120%" . " alignment=justify" );
    $h_tf = render_textflow( $p, $tf, $Title, $rClient );

    $ypos -= ( $h_tf + $fontsizexxlarge );

    $HistoricalInfo = utf8::encode($HistoricalInfo);

    $tf = $p->create_textflow( "Historical Information",
        $baseboldlargefontoptions_u . " leading=120%" . " alignment=justify" );
    $h_tf = render_textflow( $p, $tf, $Title, $rClient );

    $ypos -= ( $h_tf + $fontsizexxlarge );

    $tf = $p->create_textflow( $HistoricalInfo,
        $basefontoptions . " leading=120%" . " alignment=justify" );
    $h_tf = render_textflow( $p, $tf, $Title, $rClient );

    $ypos -= ( $h_tf + $fontsizexxlarge );

    $tf = $p->create_textflow(
"<fontsize=11 fontstyle=italic fakebold=true underline>Interpretive Summary\n<fakebold=false underline=false fontsize=$fontsize>$InterpretiveSummary",
        $basefontoptions . " leading=120%" . " alignment=justify"
    );
    $h_tf = render_textflow( $p, $tf, $Title, $rClient );

    $ypos -= ( $h_tf + 30 );
    $text =
      "Client was given copy of this plan: <fontsize=$fontsize>$WasGivenCopy\n"
      . "<fontsize=$fontsizemid>Client received resource list regarding treatment options if symptoms recur or additional services needed: <fontsize=$fontsize>$ReceivedResource\n"
      . "<fontsize=$fontsizemid>Others given copy of this plan: <fontsize=$fontsize>$OthersGivenCopy\n"
      . "\n"
      . "<fakebold=true fontsize=$fontsizemid>Staff Responsible for Follow-Up of Referrals: <fakebold=false fontsize=$fontsize>$StaffRes";
    $tf = $p->create_textflow( $text,
        $basemidfontoptions . " leading=120%" . " alignment=justify" );
    $h_tf = render_textflow( $p, $tf, $Title, $rClient );

    create_footer( $p, $ClientName, $ClientID, $DT );

    # multiple pages of Problems/Goals...

    my $rFOS = ();    # this gets rolled up by service/provider
    my ( $out1, $cnt, $txt ) = ( '', 0, '' );
    $sClientTrPlanPG->execute($TrPlanID);
    while ( my $rClientTrPlanPG = $sClientTrPlanPG->fetchrow_hashref ) {
        $cnt++;
        my $NeedSkill =
          DBA->getxref( $form, 'xNS', $rClientTrPlanPG->{NeedSkill}, 'Descr' );
        my $Problem =
            $NeedSkill eq 'Other'
          ? $rClientTrPlanPG->{Prob}
          : "${NeedSkill} $rClientTrPlanPG->{Prob}";

        create_header( $p, $Title, $rClient );

        $ypos -= $fontsizexxlarge;
        $p->fit_textline(
            "PROBLEM #" . int( $rClientTrPlanPG->{Priority} / 10 ),
            $pagewidth / 2 - 23,
            $ypos, $basemidfontoptions
        );

        $ypos -= 3 * $fontsizelarge;
        $p->fit_textline( "PROBLEM :", $marginleft + 3,
            $ypos, $baseboldmidfontoptions );
        $p->fit_textline( $Problem, $marginleft + 75,
            $ypos, $basemidfontoptions );

        $ypos -= $fontsizexxlarge;
        $p->fit_textline( "GOAL :", $marginleft + 3,
            $ypos, $baseboldlargefontoptions );
        $p->fit_textline(
            $rClientTrPlanPG->{Goal},
            $marginleft + 75,
            $ypos, $basemidfontoptions
        );

        $ypos -= 2 * $fontsizexxlarge;
        $p->fit_textline( "CURRENT OBJECTIVES: ",
            $marginleft, $ypos, $baseboldmidfontoptions );
        $p->fit_textline(
            "(Must be behaviorally measurable)",
            $marginleft + 115,
            $ypos, $basemidfontoptions
        );

        my $r = $rClientTrPlanPG;

        #warn qq|getOBJs: ID=$r->{ID}\n|;
        my @alpha =
          ( '', 'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'l', 'm' );
        my $Priority = int( $r->{'Priority'} / 10 );
        my ( $out, $i, $txt, $prog ) = ( '', 0, '', '' );
        $sClientTrPlanOBJ->execute( $r->{'ID'} );
        while ( my $rClientTrPlanOBJ = $sClientTrPlanOBJ->fetchrow_hashref ) {

            #warn qq|getOBJs: ID=$r->{ID}, OBJID=$rClientTrPlanOBJ->{'ID'}\n|;
            #warn qq|getOBJs: Progress=$rClientTrPlanOBJ->{Progress}\n|;
            $i++;
            my $ltr = @alpha[$i];
            $prog .=
              $Priority . $ltr . ': ' . $rClientTrPlanOBJ->{Progress} . "\n";
            my $obj = $rClientTrPlanOBJ->{'Obj'};

            #warn qq|getOBJs: i=$i, ltr=$ltr, obj=$obj\n|;
            unless ( $obj eq '' ) {

# my (@Services, $rFOS) = getObjServ($r->{'TrPlanID'},$rClientTrPlanOBJ,$Priority.$ltr,$rFOS);

                my ( $TrPlanID, $r, $objnum ) =
                  ( $r->{'TrPlanID'}, $rClientTrPlanOBJ, $Priority . $ltr );
                my @Services = ();
                for ( my $i = 1 ; $i <= 3 ; $i++ ) {
                    my $serv = $r->{ 'Service' . $i };
                    my $prov = $r->{ 'ProvID' . $i };
                    unless ( $serv eq '' ) {
                        my $idate = $r->{'InitiatedDate'};
                        my $tdate = $r->{'TargetDate'};
                        push(
                            @Services,
                            {
                                "tos" => qq|${objnum}${i}: |
                                  . DBA->getxref(
                                    $form, 'xServices', $serv, 'Descr'
                                  ),
                                "tosdi" =>
                                  DBUtil->Date( $idate, 'fmt', 'MM/DD/YYYY' ),
                                "tostd" =>
                                  DBUtil->Date( $tdate, 'fmt', 'MM/DD/YYYY' )
                            }
                        );
                        my $tos =
                          DBA->getxref( $form, 'xServices', $serv, 'Descr' );
                        $sProvider->execute($prov)
                          || myDBI->dberror(
                            "printClientTrPlan: select Provider $prov");
                        my $rProvider = $sProvider->fetchrow_hashref;
                        my $ProvName =
                          qq|$rProvider->{'FName'} $rProvider->{'LName'}|;
                        my $key =
                            $tos . '_'
                          . $ProvName . '_'
                          . $TrPlanID . '_'
                          . ${serv} . '_'
                          . ${prov};

                        #warn qq|saveFOS: key=$key\n|;
                        $rFOS->{$key} = $r->{'Frequency'}
                          if ( $serv && $rProvider->{'LName'} );
                    }
                }

                $ypos -= 3;
                $tf = $p->create_textflow( qq|${Priority}${ltr}: | . $obj,
                    $basefontoptions . " leading=120%" . " alignment=justify" );
                $h_tf = render_textflow( $p, $tf, $Title, $rClient );

                my $row = 1;
                my $col = 1;
                my $tbl = -1;

                $ypos -= ( $h_tf + 3 );
                my @ServicesHeaders =
                  ( "TYPES OF SERVICE", "DATE INITIATED", "TARGET DATE" );
                for ( $col = 1 ; $col <= $#ServicesHeaders + 1 ; $col++ ) {
                    $optlist =
                        "fittextline={position={"
                      . ( $col ne 1 ? "center" : "left" )
                      . " center} "
                      . $baseboldmidfontoptions
                      . "} margin=2"
                      . ( $col eq 1 ? " marginleft=0 colwidth=70%" : "" );
                    $tbl = $p->add_table_cell( $tbl, $col, $row,
                        $ServicesHeaders[ $col - 1 ], $optlist );
                }
                $row++;
                for ( my $index = 0 ; $index <= $#Services ; $index++ ) {
                    $col = 1;
                    $optlist =
                        "fittextline={position={left center} "
                      . $basefontoptions
                      . "} margin=2 marginleft=0 colwidth=70%";
                    $tbl = $p->add_table_cell(
                        $tbl, $col++, $row,
                        $Services[$index]{tos},
                        $optlist . ""
                    );
                    $optlist =
                        "fittextline={position={center center} "
                      . $basefontoptions
                      . "} margin=2";
                    $tbl = $p->add_table_cell( $tbl, $col++, $row,
                        $Services[$index]{tosdi}, $optlist );
                    $tbl = $p->add_table_cell( $tbl, $col++, $row,
                        $Services[$index]{tostd}, $optlist );
                    $row++;
                }
                my $h_tbl = render_table( $p, $tbl, $Title, $rClient );

                $ypos -= ( $h_tbl + $fontsizesmall );
            }
        }

        $ypos -= $fontsizesmall;
        $tf = $p->create_textflow(
"<fakebold=true>PROGRESS ON CURRENT/PREVIOUS GOAL SINCE LAST AUTHORIZATION:\n"
              . "<fakebold=false>(Extension Requests Only)",
            $basemidfontoptions
              . " leading=120%"
              . " alignment=justify lastalignment=center"
        );
        $h_tf = render_textflow( $p, $tf, $Title, $rClient );

        $ypos -= ( $h_tf + 4 );
        $tf = $p->create_textflow( $prog,
            $basefontoptions . " leading=120%" . " alignment=justify" );
        $h_tf = render_textflow( $p, $tf, $Title, $rClient );

        create_footer( $p, $ClientName, $ClientID, $DT );
    }

    # page3
    my $iwehave       = '';
    my $agree         = $rClientTrPlan->{'Agrees'} ? "&#x2713;" : ' ';
    my $disagree      = $rClientTrPlan->{'Agrees'} ? ' '        : "&#x2713;";
    my @FreqOfService = main->setFOS( $rFOS, $rInsurance );

    create_header( $p, $Title, $rClient );

    $optlist = $baseboldmidfontoptions . " leading=120% alignment=justify";
    my $h_iwehave = 4 * $fontsizelarge;
    $ypos -= $h_iwehave;
    my $Iwehave =
"I/We (client/guardian) have actively participated in the development of this service plan and understand the treatment goals and objectives listed. I have the following comments/response :\n"
      . "<nextline leading=50%>I/We (     agree)(     disagree) with this service plan.";
    $tf = $p->create_textflow( $Iwehave, $optlist );
    $p->fit_textflow(
        $tf, $marginleft, $ypos,
        $marginleft + $contentwidth,
        $ypos + $h_iwehave,
        "verticalalign=top"
    );
    $p->fit_textline( $agree, $marginleft + 31,
        $ypos + 3,
        "fontname={DejaVuSans} encoding=unicode fontsize=10 charref" );
    $p->fit_textline( $disagree, $marginleft + 78,
        $ypos + 3,
        "fontname={DejaVuSans} encoding=unicode fontsize=10 charref" );

    $ypos -= ( $fontsizexxlarge + 5 );
    $p->setlinewidth(1.2);
    $p->moveto( $marginleft, $ypos );
    $p->lineto( $marginleft + ( $contentwidth - 30 ) / 2, $ypos );
    $p->moveto( $marginleft + ( $contentwidth - 30 ) / 2 + 30, $ypos );
    $p->lineto( $marginleft + $contentwidth, $ypos );
    $p->closepath_stroke();

    $ypos -= $fontsizexlarge;
    $p->fit_textline( "Client Signature, 14 or older",
        $marginleft, $ypos, $baseboldmidfontoptions );
    $p->fit_textline( "Date", $marginleft + ( $contentwidth - 30 ) / 2 - 70,
        $ypos, $baseboldmidfontoptions );
    $p->fit_textline(
        "Parent/ Guardian Signature",
        $marginleft + ( $contentwidth - 30 ) / 2 + 30,
        $ypos, $baseboldmidfontoptions
    );
    $p->fit_textline(
        "Date", $marginleft + $contentwidth - 70,
        $ypos,  $baseboldmidfontoptions
    );

    $ypos -= ( $fontsizexxlarge + 2 );
    $p->fit_textline(
        "Relationship to client",
        $marginleft + ( $contentwidth - 30 ) / 2 + 30,
        $ypos, $baseboldmidfontoptions
    );

    $ypos -= 5;
    $p->setlinewidth(1.2);
    $p->moveto( $marginleft, $ypos );
    $p->lineto( $marginleft + ( $contentwidth - 30 ) / 2, $ypos );
    $p->closepath_stroke();

    $ypos -= $fontsizexlarge;
    $p->fit_textline( "Witness", $marginleft, $ypos, $baseboldmidfontoptions );

    $ypos -= ( 2 * $fontsizemid );
    $p->fit_textline( "If client is unable to sign, document the reason :",
        $marginleft, $ypos, $baseboldmidfontoptions );

    $ypos -= ( 2 * $fontsizemid );
    $p->fit_textline( "TREATMENT TEAM :",
        $marginleft, $ypos, $baseboldlargefontoptions );

    my $row = 1;
    my $col = 1;
    my $tbl = -1;
    $ypos -= $fontsize;
    my @FreqOfServiceHeaders = (
        "Type of Service",
        "Frequency of Service",
        "Electronically Signed By:"
    );

    for ( $col = 1 ; $col <= $#FreqOfServiceHeaders + 1 ; $col++ ) {
        $optlist =
            "fittextline={position={"
          . ( $col eq 2 ? "center" : "left" )
          . " center} "
          . $baseboldmidfontoptions
          . "} margin=2 marginleft=0"
          . ( $col eq 3 ? " marginleft=0 colwidth=60%" : "" );
        $tbl = $p->add_table_cell( $tbl, $col, $row,
            $FreqOfServiceHeaders[ $col - 1 ], $optlist );
    }
    $row++;
    for ( my $index = 0 ; $index <= $#FreqOfService ; $index++ ) {
        $col = 1;
        $optlist =
            "fittextline={position={left center} "
          . $basefontoptions
          . "} margin=2 marginleft=0";
        $tbl =
          $p->add_table_cell( $tbl, $col++, $row, $FreqOfService[$index]{tos},
            $optlist );
        $optlist =
            "fittextline={position={center center} "
          . $basefontoptions
          . "} margin=2 marginleft=0";
        $tbl =
          $p->add_table_cell( $tbl, $col++, $row, $FreqOfService[$index]{fos},
            $optlist );
        $optlist =
            "fittextline={position={left center} "
          . $basefontoptions
          . "} margin=2 marginleft=0 colwidth=60%";
        $tbl = $p->add_table_cell( $tbl, $col++, $row,
            $FreqOfService[$index]{esign}, $optlist );
        $row++;
    }
    my $h_tbl = render_table( $p, $tbl, $Title, $rClient );

    create_footer( $p, $ClientName, $ClientID, $DT );
}

sub render_textflow {
    my ( $p, $tf, $Title, $rClient ) = @_;
    my $ClientID   = $rClient->{ClientID};
    my $ClientName = qq|$rClient->{FName} $rClient->{LName}|;
    my $result;
    my $h_tf;

    do {
        $result = $p->fit_textflow(
            $tf, $marginleft,
            $marginbottom + $h_footer + $fontsizesmall,
            $marginleft + $contentwidth,
            $ypos, ""
        );
        if ( $result eq "_boxfull" || $result eq "_boxempty" ) {
            create_footer( $p, $ClientName, $ClientID, $DT );
            create_header( $p, $Title, $rClient );
        }
    } while ( $result ne "_stop" );
    $h_tf = $p->info_textflow( $tf, "textheight" );

    return $h_tf;
}

sub render_table {
    my ( $p, $tbl, $Title, $rClient ) = @_;

    #warn qq|printClientTrPlan: tbl=${tbl}, Title=${Title}\n|;
    my $ClientID   = $rClient->{ClientID};
    my $ClientName = qq|$rClient->{FName} $rClient->{LName}|;

  #warn qq|printClientTrPlan: ClientID=${ClientID}, ClientName=${ClientName}\n|;
    my $result;
    my $h_tbl;
    my $RowHeightLimit = 20;
    my $diff;
    $diff = $ypos - ( $marginbottom + $h_footer );
    if ( $diff <= $RowHeightLimit ) {
        create_footer( $p, $ClientName, $ClientID, $DT );
        create_header( $p, $Title, $rClient );
    }
    do {
        $result = $p->fit_table(
            $tbl, $marginleft,
            $marginbottom + $h_footer,
            $marginleft + $contentwidth,
            $ypos, ""
        );
        if ( $result eq "_boxfull" ) {
            create_footer( $p, $ClientName, $ClientID, $DT );
            create_header( $p, $Title, $rClient );
        }
    } while ( $result eq "_boxfull" );
    $h_tbl = $p->info_table( $tbl, "height" );
    return $h_tbl;
}

############################################################################
sub getStrengths {
    my ( $self, $r, $None ) = @_;
    my ( $out, $cnt ) = ( '', 0 );
    unless ( $r->{SA1} eq '' ) { $out .= qq|  | . $r->{SA1} . qq|\n|; $cnt++; }
    unless ( $r->{SA2} eq '' ) { $out .= qq|  | . $r->{SA2} . qq|\n|; $cnt++; }
    unless ( $r->{SA3} eq '' ) { $out .= qq|  | . $r->{SA3} . qq|\n|; $cnt++; }
    unless ( $r->{SA4} eq '' ) { $out .= qq|  | . $r->{SA4} . qq|\n|; $cnt++; }
    $out = qq|  ${None}\n| unless ($cnt);
    return ($out);
}

sub getNeeds {
    my ( $self, $r, $None ) = @_;
    my ( $out, $cnt ) = ( '', 0 );
    unless ( $r->{L1} eq '' ) { $out .= qq|  | . $r->{L1} . qq|\n|; $cnt++; }
    unless ( $r->{L2} eq '' ) { $out .= qq|  | . $r->{L2} . qq|\n|; $cnt++; }
    unless ( $r->{L3} eq '' ) { $out .= qq|  | . $r->{L3} . qq|\n|; $cnt++; }
    unless ( $r->{L4} eq '' ) { $out .= qq|  | . $r->{L4} . qq|\n|; $cnt++; }
    $out = qq|  ${None}\n| unless ($cnt);
    return ($out);
}

sub getProblems {
    my ( $self, $ClientID ) = @_;
    my $cnt = 0;
    my @out = ();
    $sClientProblems->execute($ClientID);
    while ( my $rClientProblems = $sClientProblems->fetchrow_hashref ) {
        $cnt++;
        push(
            @out,
            {
                "icd10"         => $rClientProblems->{'ICD10'},
                "icdName"       => $rClientProblems->{'icdName'},
                "snomedName"    => $rClientProblems->{'sctName'},
                "initiatedDate" => $rClientProblems->{'InitiatedDate'},
                "resolvedDate"  => $rClientProblems->{'ResolvedDate'}
            }
        );
    }
    return @out;
}

sub getObjServ {
    my ( $TrPlanID, $r, $objnum, $rFOS ) = @_;
    my @Services = ();
    my $out      = qq|      <typeofservice>\n|;
    for ( my $i = 1 ; $i <= 3 ; $i++ ) {
        my $serv = $r->{ 'Service' . $i };
        my $prov = $r->{ 'ProvID' . $i };
        unless ( $serv eq '' ) {
            my $idate = $r->{'InitiatedDate'};
            my $tdate = $r->{'TargetDate'};
            push(
                @Services,
                {
                    "tos" => qq|${objnum}${i}: |
                      . DBA->getxref( $form, 'xServices', $serv, 'Descr' ),
                    "tosdi" => DBUtil->Date( $idate, 'fmt', 'MM/DD/YYYY' ),
                    "tostd" => DBUtil->Date( $tdate, 'fmt', 'MM/DD/YYYY' )
                }
            );
            my $tos = DBA->getxref( $form, 'xServices', $serv, 'Descr' );
            $sProvider->execute($prov)
              || myDBI->dberror("printClientTrPlan: select Provider $prov");
            my $rProvider = $sProvider->fetchrow_hashref;
            my $ProvName  = qq|$rProvider->{'FName'} $rProvider->{'LName'}|;
            my $key =
                $tos . '_'
              . $ProvName . '_'
              . $TrPlanID . '_'
              . ${serv} . '_'
              . ${prov};

            #warn qq|saveFOS: key=$key\n|;
            $rFOS->{$key} = $r->{'Frequency'}
              if ( $serv && $rProvider->{'LName'} );
        }
    }
    return ( @Services, $rFOS );
}

sub setFOS {
    my ( $self, $r, $rInsurance ) = @_;
    my @out = ();
    my $cnt = 0;
    foreach my $key ( sort keys %{$r} ) {

        #warn qq|setFOS: key=$key\n|;
        my ( $tos, $ProvName, $TrPlanID, $ServID, $ProvID ) =
          split( '_', $key );
        my $fos = $r->{$key};

        # Electronically Signed By: John Doe, M.D. 08/01/2008 @ 06:26 A
        my $esign = $ProvName;
        $sClientTrPlanSProv->execute( $TrPlanID, $ProvID )
          || myDBI->dberror("printClientTrPlan: select ClientTrPlanSProv ");
        if ( my $rClientTrPlanSProv = $sClientTrPlanSProv->fetchrow_hashref ) {
            my $SignDate = DBUtil->Date( $rClientTrPlanSProv->{'SignDate'},
                'fmt', 'MM/DD/YYYY' );
            my $SignTime = DBUtil->AMPM( $rClientTrPlanSProv->{'SignTime'} );
            my $when =
              $SignTime eq '' ? $SignDate : qq|${SignDate} @ ${SignTime}|;
            $sCredentials->execute( $rClientTrPlanSProv->{ProvID},
                $rInsurance->{InsID} );
            my ( $ProvPIN, $ProvCred ) = $sCredentials->fetchrow_array;

#warn qq|esign: ProvID=$rClientTrPlanSProv->{ProvID}, InsID=$rClientTrPlanSProv->{InsID}: $ProvPIN, $ProvCred\n|;
            $esign .= qq| ${when} ${ProvCred}|;

            #warn qq|esign: $esign\n|;
        }
        push(
            @out,
            {
                "tos"   => ${tos},
                "fos"   => ${fos},
                "esign" => ${esign}
            }
        );
    }
    return @out;
}

sub getNPIs {
    my ( $self, $NPIs, $Fld, $None ) = @_;
    my ( $out, $cnt ) = ( '', 0 );
    $out = qq|  Name / Address / Phone / NPI\n|;
    foreach my $NPI ( split( chr(253), $NPIs ) ) {
        my $rxNPI = DBA->selxref( $form, 'xNPI', 'NPI', $NPI );
        my $name =
          $rxNPI->{'EntityTypeCode'} == 1
          ? "$rxNPI->{'ProvLastName'}, $rxNPI->{'ProvFirstName'}"
          : $rxNPI->{'ProvOrgName'};
        my $addr =
"$rxNPI->{'Addr1'}, $rxNPI->{'Addr2'}, $rxNPI->{'City'}, $rxNPI->{'ST'}, $rxNPI->{'Zip'}";
        my $phone = $rxNPI->{'WkPh'};
        my $npi   = $rxNPI->{'NPI'};
        $out .= qq|  ${name} / ${addr} / ${phone} / ${npi}\n|;
        $cnt++;
    }
    $out = qq|  ${None}\n| unless ($cnt);
    return ($out);
}
############################################################################
