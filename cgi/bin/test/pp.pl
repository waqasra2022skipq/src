#!/usr/bin/perl
############################################################################
use lib 'C:/xampp/htdocs/src/lib';
#
# Block starter:
# Import a PDF page containing blocks and fill text and image
# blocks with some data. For each addressee of the simulated
# mailing a separate page with personalized information is
# generated.
# A real-world application would fill the Blocks with data from
# some external data source. We simulate this with static data.
#
# Required software: PPS 9
# Required data: input PDF, image

use myForm;
use myDBI;
use Config;
use MgrTree;
use DBA;
use cBill;

use PDFlib::PDFlib 9.1;
use strict;
############################################################################

my $form         = myForm->new();
my $dbh          = myDBI->dbconnect( $form->{'DBNAME'} );
my $sTreatment   = $dbh->prepare("select * from Treatment where TrID=?");
my $sProgNotes   = $dbh->prepare("select * from ProgNotes where NoteID=?");
my $sPhysNotes   = $dbh->prepare("select * from PhysNotes where NoteID=?");
my $sClient      = $dbh->prepare("select * from Client where ClientID=?");
my $sClientLegal = $dbh->prepare("select * from ClientLegal where ClientID=?");
my $sProvider    = $dbh->prepare("select * from Provider where ProvID=?");
my $sInsurance   = $dbh->prepare(
"select Insurance.ClientID,Insurance.InsIDNum,Insurance.InsID,xInsurance.Name from Insurance left join xInsurance on xInsurance.ID=Insurance.InsID where Insurance.ClientID=? and Insurance.InsID=? and Insurance.InsNumEffDate<=? and (?<=Insurance.InsNumExpDate or Insurance.InsNumExpDate is NULL) order by Insurance.InsNumEffDate desc"
);
my $sClientNoteProblems = $dbh->prepare(
"select ClientNoteProblems.ID,ClientNoteProblems.Locked,misICD10.ICD10, misICD10.icdName, misICD10.sctName, DATE_FORMAT(ClientNoteProblems.InitiatedDate,'%m/%d/%Y') as InitiatedDate, DATE_FORMAT(ClientNoteProblems.ResolvedDate,'%m/%d/%Y') as ResolvedDate, ClientNoteProblems.Priority from ClientNoteProblems left join okmis_config.misICD10 on misICD10.ID = ClientNoteProblems.UUID where ClientNoteProblems.TrID=? order by ClientNoteProblems.Priority"
);
my $sClientNoteTrPlanPG = $dbh->prepare(
    "select * from ClientNoteTrPlanPG where TrID=? order by Priority");
my $sClientTrPlanPG =
  $dbh->prepare("select * from ClientTrPlanPG where ID=? order by Priority");
my $sClientTrPlanOBJ = $dbh->prepare(
    "select * from ClientTrPlanOBJ where TrPlanPGID=? order by Priority");
my $sClientVitalSigns = $dbh->prepare(
"select * from ClientVitalSigns where ClientID=? and VDate<=? order by VDate desc"
);
my $sClientNoteMeds = $dbh->prepare(
"select * from ClientNoteMeds left join ClientMeds on ClientMeds.ID=ClientNoteMeds.ClientMedsID where TrID=? order by ClientMeds.DrugInfo, ClientMeds.PrescriptionDate"
);
my $sClientNoteFamilyI =
  $dbh->prepare("select * from ClientNoteFamilyI where TrID=?");
my $sClientNoteFamilyP =
  $dbh->prepare("select * from ClientNoteFamilyP where TrID=?");

my @alpha = (
    '',  'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm',
    'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z'
);
my $pdfpath = myConfig->cfg('FORMDIR') . "/printing/printNote_Rev1.pdf";
my $labelfont =
  qq|<nounderline fontname={Times New Roman} alignment=left encoding=unicode>|;
my $responsefont =
  qq|<nounderline fontname={Arial} alignment=left encoding=unicode>|;
my $hdrfont =
  qq|<underline fontname={Times New Roman} alignment=center encoding=unicode>|;

# This is where the data files are. Adjust as necessary.
##use constant searchpath => "/tmp/test/data";
##use constant fontpath => "/usr/share/fonts/msttcore";
use constant outfile   => "printNotes2.pdf";
use constant imagefile => "new.jpg";

# Names of the encounter-specific Blocks contained on the imported page
my @formblocks = ( "b1", "b2", "b4" );

# number of address blocks
my $nblocks = @formblocks;

# Static text simulates database-driven main contents
my @blockdata = (
    [ "b1", "Dear Paper Planes Fan," ],
    [
        "b2",
        "Our <fillcolor=red>BEST PRICE OFFER<fillcolor=black> includes today:"
          . "\n\n"
          . "Long Distance Glider\nWith this paper rocket you can send all your "
          . "messages even when sitting in a hall or in the cinema pretty near "
          . "the back.\n\n"
          . "Giant Wing\nAn unbelievable sailplane! It is amazingly robust and "
          . "can even do aerobatics. But it is best suited to gliding.\n\n"
          . "Cone Head Rocket\nThis paper arrow can be thrown with big swing. "
          . "We launched it from the roof of a hotel. It stayed in the air a "
          . "long time and covered a considerable distance.\n\n"
          . "Super Dart\nThe super dart can fly giant loops with a radius of 4 "
          . "or 5 meters and cover very long distances. Its heavy cone point is "
          . "slightly bowed upwards to get the lift required for loops.\n\n"
          . "Visit us on our Web site at www.kraxi.com!"
    ],
    [ "b3", "Yours sincerely,\nVictor Kraxi" ]
);

my $nblockdata = @blockdata;

# ClientID: 60309
#my @TrIDs = (1059724, 1059727, 1062395);
#my @TrIDs = (1064068,1054278,1057757,1064069,1068111,1037222,1037223,1037225);
#my @TrIDs = (1077815, 1077816, 1077817, 1077818, 1077819, 1077820, 1077821, 1077822);

my @pagehandles = ();
my $pageno      = 0;
my $objtype;

eval {
    my $p = new PDFlib::PDFlib;

##    $p->set_option("SearchPath={{" . searchpath . "}}");
##    $p->set_option("SearchPath={{" . fontpath . "}}");

    # This means we must check return values of load_font() etc.
    $p->set_option("errorpolicy=return");

    # all strings are expected as utf8
    $p->set_option("stringformat=utf8");

    print qq|create outfile: | . outfile . "\n";
    if (
        $p->begin_document( outfile,
            "destination={type=fitwindow} pagelayout=singlepage" ) == -1
      )
    {
        throw new Exception( "Error: " . $p->get_errmsg() );
    }

    $p->set_info( "Creator", "PDFlib starter sample" );
    $p->set_info( "Title",   "starter_block" );

##    $p->set_option("enumeratefonts saveresources={filename=pdflib.upr}");

    # Open the Block template which contains PDFlib Blocks
    my $indoc = $p->open_pdi_document( $pdfpath, "" );
    if ( $indoc == -1 ) { die( "Error: " . $p->get_errmsg() ); }

    my $no_of_input_pages = $p->pcos_get_number( $indoc, "length:pages" );
    print qq|no_of_input_pages: ${no_of_input_pages}\n|;

    # Prepare all pages of the input document. We assume a small
    # number of input pages and a large number of generated output
    # pages. Therefore it makes sense to keep the input pages
    # open instead of opening the pages again for each encounter.

    for ( $pageno = 1 ; $pageno <= $no_of_input_pages ; $pageno++ ) {

        # Open the first page and clone the page size
        $pagehandles[$pageno] =
          $p->open_pdi_page( $indoc, $pageno, "cloneboxes" );
        if ( $pagehandles[$pageno] == -1 ) {
            die( "Error: " . $p->get_errmsg() );
        }
    }

    my $image = $p->load_image( "auto", imagefile, "" );

    if ( $image == -1 ) { die( "Error: " . $p->get_errmsg() ); }

    # Duplicate input pages for each encounter and fill Blocks

    #KLS
    my $cnt = 0;
    foreach my $TrID ( split( ' ', $form->{'TrIDs'} ) ) {
        $cnt++;
        print qq|start: ${TrID}\n|;
        main->printNote( $p, $TrID, $no_of_input_pages, $indoc );
    }
    print qq|finished: cnt=${cnt}\n|;

    # Close all input pages
    for ( $pageno = 1 ; $pageno <= $no_of_input_pages ; $pageno++ ) {
        $p->close_pdi_page( $pagehandles[$pageno] );
    }
    $p->close_pdi_document($indoc);
    $p->close_image($image);

    $p->end_document("");

};
if ($@) { die("$0: PDFlib Exception occurred:\n$@"); }
$sTreatment->finish();
$sProgNotes->finish();
$sPhysNotes->finish();
$sClient->finish();
$sClientLegal->finish();
$sInsurance->finish();
$sProvider->finish();
$sClientNoteProblems->finish();
$sClientNoteTrPlanPG->finish();
$sClientTrPlanPG->finish();
$sClientTrPlanOBJ->finish();
$sClientVitalSigns->finish();
$sClientNoteMeds->finish();
$sClientNoteFamilyI->finish();
$sClientNoteFamilyP->finish();
myDBI->cleanup();
exit;
############################################################################
sub printNote {
    my ( $self, $p, $TrID, $no_of_input_pages, $indoc ) = @_;

    # Option list for text blocks
    my $optlist = "encoding=winansi embedding";
    my $str;
    print qq|test ID: | . $TrID . "\n";
    $sTreatment->execute($TrID)
      || myDBI->dberror("printNotes: select Treatment ${TrID}");
    if ( my $rTreatment = $sTreatment->fetchrow_hashref ) {
        print qq|add ID: | . $TrID . "\n";
        my $rNote;
        my $NoteType = $rTreatment->{'Type'};
        my ( $num, $NoteDescr ) = DBA->noteType($NoteType);
        if ( $NoteType =~ /1|4/ )    # progress or medicare
        {
            $sProgNotes->execute($TrID)
              || myDBI->dberror("PrintNotes: select ProgNotes ${TrID}");
            $rNote = $sProgNotes->fetchrow_hashref;
        }
        elsif ( $NoteType == 2 )     # physician
        {
            $sPhysNotes->execute($TrID)
              || myDBI->dberror("PrintNotes: select PhysNotes ${TrID}");
            $rNote = $sPhysNotes->fetchrow_hashref;
        }
        my $dbilled =
          DBUtil->Date( $rTreatment->{'BillDate'}, 'fmt', 'MM/DD/YYYY' );
        my $ClientID = $rTreatment->{'ClientID'};
        $sClient->execute($ClientID)
          || myDBI->dberror("printNotes: select Client $ClientID");
        my $rClient = $sClient->fetchrow_hashref;
        my $rxSC    = cBill->getServiceCode(
            $form,                           $rTreatment->{'SCID'},
            $rTreatment->{'ContLogDate'},    $rTreatment->{'ContLogBegTime'},
            $rTreatment->{'ContLogEndTime'}, $TrID,
            $rTreatment->{'BillDate'}
        );
        $sProvider->execute( $rTreatment->{'ClinicID'} )
          || myDBI->dberror("select Clinic $rTreatment->{'ClinicID'}");
        my $rClinic = $sProvider->fetchrow_hashref;
        $sClientLegal->execute($ClientID)
          || myDBI->dberror("printNotes: select ClientLegal $ClientID");
        my $rClientLegal = $sClientLegal->fetchrow_hashref;
        $sInsurance->execute(
            $rTreatment->{ClientID},    $rxSC->{InsID},
            $rTreatment->{ContLogDate}, $rTreatment->{ContLogDate}
        ) || myDBI->dberror("select Insurance ${TrID} ${ClientID}");
        my $rInsurance = $sInsurance->fetchrow_hashref;

        my $groupno =
            $rInsurance->{InsIDNum} !~ /^(\d{3})-(\d{2})-(\d{4})/
          ? $rInsurance->{InsIDNum}
          : '';
        my $dos =
          DBUtil->Date( $rTreatment->{ContLogDate}, 'fmt', 'MM/DD/YYYY' );
        my $stime             = DBUtil->AMPM( $rTreatment->{ContLogBegTime} );
        my $etime             = DBUtil->AMPM( $rTreatment->{ContLogEndTime} );
        my $DurationInMinutes = $rxSC->{Duration} / 60;

        # Header info...
        my $AgencyID = MgrTree->getAgency( $form, $rClient->{clinicClinicID} );
        $sProvider->execute($AgencyID) || myDBI->dberror("execute: sProvider");
        my $rAgency    = $sProvider->fetchrow_hashref;
        my $AgencyName = $rAgency->{Name};
        my $AgencyAddr = $rAgency->{Addr1} . ', ';
        $AgencyAddr .= $rAgency->{Addr2} . ', ' if ( $rAgency->{Addr2} );
        my $AgencyCSZ .=
          $rAgency->{City} . ', ' . $rAgency->{ST} . '  ' . $rAgency->{Zip};
        my $AgencyPh =
          'Office: ' . $rAgency->{WkPh} . '  Fax: ' . $rAgency->{Fax};

        # Loop over all pages of the input document
        for ( $pageno = 1 ; $pageno <= $no_of_input_pages ; $pageno++ ) {

            # Start the next output page. The dummy size will be
            # replaced with the cloned size of the input page.

            $p->begin_page_ext( 10, 10, "" );

            # Place the imported page on the output page, and clone all
            # page boxes which are present in the input page; this will
            # override the dummy size used in begin_page_ext().

            $p->fit_pdi_page( $pagehandles[$pageno], 0, 0, "cloneboxes" );

            $str = qq|${AgencyName}\n${AgencyAddr}\n${AgencyCSZ}\n${AgencyPh}|;
            if (
                $p->fill_textblock( $pagehandles[$pageno], 'agencyinfo', $str,
                    $optlist ) == -1
              )
            {
                printf( "Warning: %s\n", $p->get_errmsg() );
            }
            if (
                $p->fill_textblock(
                    $pagehandles[$pageno],
                    'myTitle',
"$rInsurance->{'Name'} Note # ${TrID} <fontsize=8>(${NoteDescr})",
                    $optlist
                ) == -1
              )
            {
                printf( "Warning: %s\n", $p->get_errmsg() );
            }
            my $grpsize =
              $rNote->{'GrpSize'} >= 1
              ? qq|               ${labelfont}Group Size: ${responsefont}$rNote->{'GrpSize'}\n|
              : qq|\n|;
            my $str =
qq|Name: ${responsefont}$rClient->{'LName'}, $rClient->{'FName'} (${ClientID})|;
            $str .=
qq|               ${labelfont}Group #: ${responsefont}${groupno}\n|;
            $str .=
qq|${labelfont}Type Of Service: ${responsefont}$rxSC->{SCName} ${grpsize}|;
            $str .= qq|${labelfont}Date Of Service: ${responsefont}${dos}|;
            $str .=
qq|               ${labelfont}Start Time: ${responsefont}${stime}|;
            $str .=
              qq|               ${labelfont}End Time: ${responsefont}${etime}|;
            $str .=
qq|               ${labelfont}Total Minutes: ${responsefont}${DurationInMinutes}|;

            if (
                $p->fill_textblock( $pagehandles[$pageno],
                    'noteinfo', $str, $optlist ) == -1
              )
            {
                printf( "Warning: %s\n", $p->get_errmsg() );
            }

            main->getProblems( $p, $TrID );

            # specific note type details...
            my $notetext = main->getPG( $p, $rTreatment, $rxSC->{'Type'} );
            my $llx      = $p->pcos_get_number( $indoc,
                "pages[" . ( $pageno - 1 ) . "]/blocks/problems/rect[0]" );
            my $lly = $p->pcos_get_number( $indoc,
                "pages[" . ( $pageno - 1 ) . "]/blocks/problems/rect[1]" );
            my $urx = $p->pcos_get_number( $indoc,
                "pages[" . ( $pageno - 1 ) . "]/blocks/problems/rect[2]" );
            my $ury = $p->pcos_get_number( $indoc,
                "pages[" . ( $pageno - 1 ) . "]/blocks/problems/rect[3]" );
            print qq|COORDINATES: ${llx} ${lly} ${urx} ${ury} \n|;

            #$notetext .= qq|COORDINATES: ${llx} ${lly} ${urx} ${ury} \n|;
            if ( $NoteType == 1 )    # append Methods to problems addressed
            {
                $notetext .=
qq|\n${labelfont}METHODS USED TO ADDRESS PROBLEMS (What Techniques or Activities Were Used To Work On Problems): 
${responsefont}| . $rNote->{'Methods'};
            }
            elsif ( $NoteType =~ /2|3/ )    # physician or electronic
            {
                my $dlm = '';
                $notetext .= qq|\n\n${hdrfont}Interactive Complexity:\n|;
                if ( $rNote->{'Maladaptive'} ) {
                    $notetext .=
qq|${dlm}1. The need to manage maladaptive communication (related to, e.g., high anxiety, high reactivity, repeated questions, or disagreement) among participants that complicates delivery of care.|;
                    $dlm = "\n";
                }
                if ( $rNote->{'Interfere'} ) {
                    $notetext .=
qq|${dlm}2. Caregiver emotions or behaviors that interfere with implementation of the treatment plan.|;
                    $dlm = "\n";
                }
                if ( $rNote->{'Sentinel'} ) {
                    $notetext .=
qq|${dlm}3. Evidence or disclosure of a sentinel event and mandated report to a third party (e.g., abuse or neglect with report to state agency) with initiation of discussion of the sentinel event and/or report with patient and other visit participants.|;
                    $dlm = "\n";
                }
                if ( $rNote->{'PlayOvercome'} ) {
                    $notetext .=
qq|${dlm}4. Use of play equipment, physical devices, interpreter or translator to overcome barriers to diagnostic or therapeutic interaction with a patient who is not fluent in the same language or who has not developed or lost expressive or receptive language skills to use or understand typical language|;
                    $dlm = "\n";
                }
                $notetext .= main->getParticipants( $p, $rTreatment );
                if ( $NoteType == 2 ) {
                    $notetext .=
qq|\n${labelfont}Referral Reason: \n${responsefont}$rNote->{RefReason}\n|;
                    $notetext .=
qq|\n${labelfont}Referral Detail: \n${responsefont}$rNote->{RefDetail}\n|;
                    $notetext .=
qq|\n${labelfont}Chief Complaint: \n${responsefont}$rNote->{Complaint}\n|;
                    $notetext .=
qq|\n${labelfont}Health Concerns: \n${responsefont}$rNote->{Concerns}\n|;
                    $notetext .=
qq|\n${labelfont}History of Present Illness: \n${responsefont}$rNote->{PresentHistory}\n|;
                    $notetext .=
qq|\n${labelfont}Past, Family and Social History: \n${responsefont}$rNote->{SocialHistory}\n|;
                    $notetext .=
qq|\n${labelfont}Review of Systems: \n${responsefont}$rNote->{Review}\n|;
                    $notetext .=
qq|\n${labelfont}Objective Findings: \n${responsefont}$rNote->{Findings}\n|;
                    $notetext .= main->getVitals( $p, $rTreatment );
                    $notetext .= main->getMeds( $p, $rTreatment );
                }
            }
            elsif ( $NoteType == 4 )    # append Meghods and Interventions
            {
                $notetext .= qq|\n${labelfont}CONTENTS TOPICS DISCUSSED: 
${responsefont}| . $rNote->{'Methods'};
                my $int    = $rNote->{'Intervention'};
                my $xtable = 'xNoteInt' . $int;
                $notetext .= qq|\n\n${labelfont}INTERVENTION: ${responsefont}|
                  . DBA->getxref( $form, 'xNoteInt', $int, 'Descr' ) . qq|
${labelfont}SPECFIC TECHNIQUES:|;
                foreach my $tech ( split( chr(253), $rNote->{'Techniques'} ) ) {
                    $notetext .=
                      "\n" . DBA->getxref( $form, $xtable, $tech, 'Descr' );
                }
            }
            if ( $NoteType =~ /1|2|4/ )    # progress | physician | medicare
            {
                $notetext .=
qq|\n\n${labelfont}PROGRESS MADE TOWARDS GOALS: ${responsefont}|
                  . DBA->getxref( $form, 'xProgress', $rNote->{Progress},
                    'Descr' )
                  . qq|
${labelfont}As Evidenced By:
${responsefont}| . $rNote->{'ProgEvidence'};
            }
            if ( $NoteType =~ /1|4/ )      # progress or medicare
            {
                if ( $rNote->{'NewProblems'} ne '' ) {
                    $notetext .=
qq|\n\n${labelfont}NEW NEED(S), GOALS AND/OR OBJECTIVES IDENTIFIED DURING SESSION:
${labelfont}Describe Below:\n${responsefont}| . $rNote->{'NewProblems'};
                }
                if ( $rxSC->{'Type'} eq 'CI' ) {
                    my $cGAF =
                      $rNote->{'GAFCurrent'} eq ''
                      ? "${responsefont}None"
                      : "${responsefont}$rNote->{'GAFCurrent'}";
                    my $pGAF =
                      $rNote->{'GAFRecent'} eq ''
                      ? "${responsefont}None"
                      : "${responsefont}$rNote->{'GAFRecent'}";
                    $notetext .=
qq|LEVEL OF FUNCTIONING ASSESSMENT GAF: CURRENT: ${cGAF} ${labelfont}RECENT PAST (30 DAYS): ${pGAF}
| . $rNote->{'CrisisText'};
                }
            }
            $notetext .=
qq|\n\n${labelfont}Patient Education Performed: ${responsefont}Yes|
              if ( $rTreatment->{'EdPerformed'} );
            if (
                $p->fill_textblock( $pagehandles[$pageno],
                    'notetext', $notetext, $optlist ) == -1
              )
            {
                printf( "Warning: %s\n", $p->get_errmsg() );
            }
            my $completedby = "Electronically Signed By: "
              . DBA->setProvCreds(
                $form, $rTreatment->{'ProvID'},
                $rxSC->{InsID},
                $rTreatment->{'ProvOKDate'},
                $rTreatment->{'ProvOKTime'}
              );

#my $approvedby = $rTreatment->{'MgrProvID'} == $rTreatment->{'ProvID'} ? '' : "                   Approved By: ".DBA->setProvCreds($form,$rTreatment->{'MgrProvID'},$rxSC->{InsID},$rTreatment->{'MgrRevDate'},$rTreatment->{'MgrRevTime'});
#my $enteredby = $rTreatment->{'EnteredBy'} == $rTreatment->{'ProvID'} ? '' : "                      Entered By: ".DBA->setProvCreds($form,$rTreatment->{'EnteredBy'},$rxSC->{InsID},$rTreatment->{'ChartEntryDate'});
            my $approvedby = "                   Approved By: "
              . DBA->setProvCreds(
                $form, $rTreatment->{'MgrProvID'},
                $rxSC->{InsID},
                $rTreatment->{'MgrRevDate'},
                $rTreatment->{'MgrRevTime'}
              );
            my $enteredby = "                      Entered By: "
              . DBA->setProvCreds(
                $form,          $rTreatment->{'EnteredBy'},
                $rxSC->{InsID}, $rTreatment->{'ChartEntryDate'}
              );
            $str = $completedby . "\n" . $approvedby . "\n" . $enteredby . "\n";
            if (
                $p->fill_textblock( $pagehandles[$pageno], 'completedby', $str,
                    $optlist ) == -1
              )
            {
                printf( "Warning: %s\n", $p->get_errmsg() );
            }

            # Loop over all encounter-specific Blocks. Fill each
            # Block with the corresponding person's address data.
            for ( my $j = 0 ; $j < $nblocks ; $j++ ) {

                # Check whether the Block is present on the imported page;
                # type "dictionary" means that the Block is present.

                $objtype = $p->pcos_get_string( $indoc,
                        "type:pages["
                      . ( $pageno - 1 )
                      . "]/blocks/"
                      . $formblocks[$j] );
                if ( $objtype eq "dict" ) {
                    my $str =
                        $j
                      . ' <fontname={NotoSerif-Regular} encoding=unicode fontsize=20> this is block: '
                      . $formblocks[$j];
                    if (
                        $p->fill_textblock(
                            $pagehandles[$pageno], $formblocks[$j],
                            $str,                  $optlist
                        ) == -1
                      )
                    {
                        printf( "Warning: %s\n", $p->get_errmsg() );
                    }
                }
            }
            my $CustAgency = DBA->getxref( $form, 'xCustAgency',
                $rClientLegal->{'CustAgency'}, 'Descr' );
            $CustAgency = 'None' if ( $CustAgency eq '' );
            my $jolts =
              $rClientLegal->{'JOLTS'} eq ''
              ? ''
              : qq|JOLTS: $rClientLegal->{'JOLTS'}|;
            my $caseid =
              $rClientLegal->{'CASEID'} eq ''
              ? ''
              : qq|CASEID: $rClientLegal->{'CASEID'}|;
            my $cagency =
              qq|${CustAgency} ${jolts} ${caseid}|;    # Append to CustAgency.

            #$rClinic->{'Name'} .= qq|REDUCE LINE TEST|;
            #$cagency .= qq|TEST TO REDUCE LINE|;
            $str = qq|Service Code: ${responsefont}$rxSC->{'SCNum'}|;
            $str .=
qq|     ${labelfont}Total Units: ${responsefont}$rTreatment->{'Units'}|;
            $str .= qq|     ${labelfont}Date Billed: ${responsefont}${dbilled}|;
            $str .= qq|     ${labelfont}By: ${responsefont}$rClinic->{Name}|;
            $str .=
              qq|     ${labelfont}Custody Agency: ${responsefont}${cagency}|;
            if (
                $p->fill_textblock( $pagehandles[$pageno], 'noteinfo2', $str,
                    $optlist ) == -1
              )
            {
                printf( "Warning: %s\n", $p->get_errmsg() );
            }
            if (
                $p->fill_textblock(
                    $pagehandles[$pageno],
                    'myFooter',
"Confidentiality of drug/alcohol abuse records is protected by Federal Law. Federal regulations (42 CFR, Part 2 prohibits making any further disclosure of this information unless further disclosure is expressively permitted by written consent of the person to whom it pertains or as otherwise permitted by 42 CFR, Part 2. A GENERAL AUTHORIZATION FOR RELEASE OF MEDICAL OR OTHER INFORMATION IS NOT SUFFICIENT FOR THIS PURPOSE. The Federal rules restrict any use of the information to criminally investigate or prosecute any alcohol/drug abuse client.",
                    $optlist
                ) == -1
              )
            {
                printf( "Warning: %s\n", $p->get_errmsg() );
            }

            $p->end_page_ext("");
        }
    }
    else {
        print qq|skip ID: | . $TrID . "\n";

        # Loop over all pages of the input document
        for ( $pageno = 1 ; $pageno <= $no_of_input_pages ; $pageno++ ) {
            $p->begin_page_ext( 10, 10, "" );
            $p->fit_pdi_page( $pagehandles[$pageno], 0, 0, "cloneboxes" );
            $str = qq|TrID: ${TrID} NOT FOUND!.\n|;
            if (
                $p->fill_textblock( $pagehandles[$pageno], 'agencyinfo', $str,
                    $optlist ) == -1
              )
            {
                printf( "Warning: %s\n", $p->get_errmsg() );
            }
            $p->end_page_ext("");
        }
    }
    return ();
}

# -----------------------------------------------
# Create and place table with ICD10/Problems list
# -----------------------------------------------
sub getProblems {
    my ( $self, $p, $TrID ) = @_;
    $sClientNoteProblems->execute($TrID);
    my $cnt     = $sClientNoteProblems->rows;
    my $optlist = "encoding=winansi embedding";
    if ( $cnt == 0 ) {
        my $str = qq|CLIENT PROBLEMS:\n${responsefont}None|;
        if (
            $p->fill_textblock( $pagehandles[$pageno],
                'problems', $str, $optlist ) == -1
          )
        {
            printf( "Warning: %s\n", $p->get_errmsg() );
        }
        return ();
    }
    {
        my $str = qq|CLIENT PROBLEMS:|;
        if (
            $p->fill_textblock( $pagehandles[$pageno],
                'problems', $str, $optlist ) == -1
          )
        {
            printf( "Warning: %s\n", $p->get_errmsg() );
        }
    }

    # make 0 null, to set starting at 1...
    my @headers    = ( "", "ICD10", "NAME", "INITIATED", "RESOLVED" );
    my @alignments = ( "", "left",  "left", "center",    "center" );

    my $fontsize = 10;
    my $basefontoptions =
        "fontname=TimesNewRomanPSMT fontsize="
      . $fontsize
      . " embedding encoding=unicode";
    my $optlist;
    my $x_table    = 32;
    my $tablewidth = 545;

    # ---------- Header row
    my $row = 1;
    my $col = 1;
    my $tbl = -1;
    my $buf;

    for ( $col = 1 ; $col <= $#headers ; $col++ ) {
        $optlist =
            "fittextline={position={"
          . $alignments[$col]
          . " center} "
          . $basefontoptions
          . "} margin=2";
        $tbl = $p->add_table_cell( $tbl, $col, $row, $headers[$col], $optlist );
    }
    $row++;

    # ---------- Data rows: one for each ICD10
    $basefontoptions =
      "fontname={Arial} fontsize=" . $fontsize . " embedding encoding=unicode";
    while ( my $rClientNoteProblems = $sClientNoteProblems->fetchrow_hashref ) {
        $col = 1;                                 # column 1: ICD10
                                                  #$buf = sprintf("%d", $i + 1);
        $buf = $rClientNoteProblems->{'ICD10'};

        #print qq|buf=${buf}, row=${row}, col=${col}\n|;
        $optlist =
            "fittextline={position={"
          . $alignments[$col]
          . " center} "
          . $basefontoptions
          . "} colwidth=10% margin=2";
        $tbl = $p->add_table_cell( $tbl, $col, $row, $buf, $optlist );

        $col = 2;                                   # column 2: NAME
        $buf = $rClientNoteProblems->{'icdName'};

        #print qq|buf=${buf}, row=${row}, col=${col}\n|;
        $optlist =
            "fittextline={position={"
          . $alignments[$col]
          . " center} "
          . $basefontoptions
          . "} colwidth=60% margin=2";
        $tbl = $p->add_table_cell( $tbl, $col, $row, $buf, $optlist );

        $col = 3;                                      # column 3: INITIATE DATE
        $buf = $rClientNoteProblems->{'InitiatedDate'};

        #print qq|buf=${buf}, row=${row}, col=${col}\n|;
        $optlist =
            "fittextline={position={"
          . $alignments[$col]
          . " center} "
          . $basefontoptions
          . "} colwidth=15% margin=2";
        $tbl = $p->add_table_cell( $tbl, $col, $row, $buf, $optlist );

        $col = 4;                                      # column 4: INITIATE DATE
        $buf = $rClientNoteProblems->{'ResolvedDate'};

        #print qq|buf=${buf}, row=${row}, col=${col}\n|;
        $optlist =
            "fittextline={position={"
          . $alignments[$col]
          . " center} "
          . $basefontoptions
          . "} colwidth=15% margin=2";
        $tbl = $p->add_table_cell( $tbl, $col, $row, $buf, $optlist );

        $row++;
    }

    my $top = 635;

    # Place the table on the page; Shade every other row.
    $optlist = "header=1 fill={{area=rowodd fillcolor={gray 0.9}}} ";
    my $result = $p->fit_table( $tbl, $x_table, $top, $x_table + $tablewidth,
        20, $optlist );
    if ( $result eq "_error" ) {
        throw new Exception( "Couldn't place table: " . $p->get_errmsg() );
    }
    $p->delete_table( $tbl, "" );
    return ();
}

sub getPG {
    my ( $self, $p, $rTreatment, $SCType ) = @_;
    my $TrID     = $rTreatment->{'TrID'};
    my $NoteType = $rTreatment->{'Type'};
    my $out =
qq|SPECIFIC PROBLEM(S) ADDRESSED (As Identified On Comprehensive Treatment Plan):
${responsefont}|;
    $out .= qq|Develop / Review Treatment Plan\n| if ( $SCType eq 'TP' );
    $out .= qq|Crisis Response\n|                 if ( $SCType eq 'CI' );
    $sClientNoteTrPlanPG->execute($TrID)
      || myDBI->dberror("printNotes: select ClientNoteTrPlanPG ${TrID}");

    while ( my $rClientNoteTrPlanPG = $sClientNoteTrPlanPG->fetchrow_hashref ) {
        $sClientTrPlanPG->execute( $rClientNoteTrPlanPG->{'TrPlanPGID'} )
          || myDBI->dberror(
"printNotes: select ClientTrPlanPG $rClientNoteTrPlanPG->{'TrPlanPGID'}"
          );
        while ( my $rClientTrPlanPG = $sClientTrPlanPG->fetchrow_hashref ) {
            my $Priority = int( $rClientTrPlanPG->{'Priority'} / 10 );
            my $PROB     = DBA->subchr( $rClientTrPlanPG->{'Prob'} );
            my $GOAL     = DBA->subchr( $rClientTrPlanPG->{'Goal'} );
            $out .= "#" . $Priority . ": Problem: " . ${PROB} . "\n";
            $out .= "\tGoal: " . ${GOAL} . "\n";
            my $cnt = 0;
            $sClientTrPlanOBJ->execute( $rClientTrPlanPG->{'ID'} )
              || myDBI->dberror(
                "printNotes: select ClientTrPlanOBJ $rClientTrPlanPG->{'ID'}");
            while ( my $rClientTrPlanOBJ = $sClientTrPlanOBJ->fetchrow_hashref )
            {
                $cnt++;
                my $ltr = @alpha[$cnt];
                my $OBJ = DBA->subchr( $rClientTrPlanOBJ->{'Obj'} );

       #print qq|printNotes: ClientNoteTrPlanOBJ: ID=$rClientTrPlanOBJ->{ID}\n|;
                $out .= "\t\tObjective ${Priority}${ltr}: " . ${OBJ} . "\n";
            }
        }
    }
    return ($out);
}
############################################################################
sub getParticipants {
    my ( $self, $TrID ) = @_;
    my ( $self, $p, $rTreatment ) = @_;
    my $TrID         = $rTreatment->{'TrID'};
    my $out          = '';
    my $Informants   = '';
    my $Participants = '';
    my $row          = 0;
    $sClientNoteFamilyI->execute($TrID)
      || $form->dberror("ClientMU: select ClientNoteFamilyI ${TrID}");

    while ( my $rClientNoteFamilyI = $sClientNoteFamilyI->fetchrow_hashref ) {
        $row++;
        $Informants .=
            $rClientNoteFamilyI->{'FName'} . ' '
          . $rClientNoteFamilyI->{'LName'} . ' ('
          . DBA->getxref( $form, 'xRelationship', $rClientNoteFamilyI->{Rel},
            'Descr' ) . ') ';
    }
    $out .=
      $Informants eq '' ? '' : qq|\n${labelfont}Informants: ${Informants}|;
    $sClientNoteFamilyP->execute($TrID)
      || $form->dberror("ClientMU: select ClientNoteFamilyP ${TrID}");
    while ( my $rClientNoteFamilyP = $sClientNoteFamilyP->fetchrow_hashref ) {
        $row++;
        my $Participants .=
            $rClientNoteFamilyP->{'FName'} . ' '
          . $rClientNoteFamilyP->{'LName'} . ' ('
          . DBA->getxref( $form, 'xRelationship', $rClientNoteFamilyP->{Rel},
            'Descr' ) . ') ';
    }
    $out .=
      $Participants eq ''
      ? ''
      : qq|\n${labelfont}Participants: ${Participants}|;

    #$out .= qq|\n${labelfont}Informants: FName LName relation|;
    #$out .= qq|\n${labelfont}Participants: FName LName relation|;
    return ($out);
}

sub getVitals {
    my ( $self, $p, $rTreatment ) = @_;
    my $ClientID = $rTreatment->{'ClientID'};
    $sClientVitalSigns->execute( $ClientID, $rTreatment->{ContLogDate} )
      || myDBI->dberror("getVitals: select ClientVitalSigns ${ClientID}");
    my $cnt = $sClientVitalSigns->rows;

    #$cnt = 1 unless($cnt);
    my $out =
qq|${labelfont}Date\tHeight\tWeight\tWaist\tTemp\tBP\tPulse\tOximetry\tBloodSugar\tRespiration\n|
      if ( $cnt > 0 );
    my $row = 0;
    while ( my $r = $sClientVitalSigns->fetchrow_hashref ) {
        $row++;
        my $Height = $r->{'HeightFeet'} eq '' ? '' : qq|$r->{'HeightFeet'} ft.|;
        $Height .=
          $r->{'HeightInches'} eq '' ? '' : qq| $r->{'HeightInches'} in.|;
        my $Weight = $r->{'Weight'} eq ''      ? '' : qq|$r->{'Weight'} lbs.|;
        my $Waist  = $r->{'Waist'} eq ''       ? '' : qq|$r->{'Waist'} in.|;
        my $Temp   = $r->{'Temperature'} eq '' ? '' : qq|$r->{'Temperature'} F|;
        my $BP =
            $r->{'BPSystolic'} eq '' && $r->{'BPDiastolic'} eq '' ? ''
          : $r->{'BPSystolic'} eq '' ? qq|missing / $r->{'BPDiastolic'}|
          :   qq|$r->{'BPSystolic'} / $r->{'BPDiastolic'}|;
        $out .=
qq|${responsefont}$r->{VDate}\t${Height}\t${Weight}\t$r->{Waist}\t${Temp}\t${BP}\t$r->{Pulse}\t$r->{Oximetry}\t$r->{BloodSugar}\t$r->{Respiration}\n|;
        print qq|printNotes: getVitals: ID=$r->{ID}\n|;
    }

#$out .= qq|${responsefont}Date\tHeight\tWeight\tWaist\tTemp\tBP\tPulse\tOximetry\tBloodSugar\tRespiration\n|;
    return ($out);
}

sub getMeds {
    my ( $self, $p, $rTreatment ) = @_;
    my $TrID = $rTreatment->{'TrID'};
    $sClientNoteMeds->execute($TrID)
      || $form->dberror("PrintNotes: select ClientNoteMeds");
    my $cnt = $sClientNoteMeds->rows;

    #$cnt = 1 unless($cnt);
    my $out =
qq|${labelfont}DrugID\tDrugInfo\tFrequency\tRoute\tSchedule\tPrescriptionDate\tRefills\n|
      if ( $cnt > 0 );
    my $row = 0;
    while ( my $rClientNoteMeds = $sClientNoteMeds->fetchrow_hashref ) {
        $row++;
        $out .=
qq|${responsefont}$rClientNoteMeds->{DrugID}\t$rClientNoteMeds->{DrugInfo}\t$rClientNoteMeds->{DosageFrequencyDescription}\t$rClientNoteMeds->{Route}\t$rClientNoteMeds->{ExternalDrugSchedule}\t$rClientNoteMeds->{PrescriptionDate}\t$rClientNoteMeds->{Refills}\n|;

        #    $rNote->{Text}
    }

#$out .= qq|${responsefont}DrugID\tDrugInfo\tDosageFrequencyDescription\tRoute\tExternalDrugSchedule\tPrescriptionDate\tRefills\n|;
    return ($out);
}
############################################################################
