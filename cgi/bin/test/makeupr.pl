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
use MgrTree;

use PDFlib::PDFlib 9.1;
use strict;
############################################################################

my $form       = myForm->new();
my $dbh        = myDBI->dbconnect( $form->{'DBNAME'} );
my $sTreatment = $dbh->prepare("select * from Treatment where TrID=?");
my $sClient    = $dbh->prepare("select * from Client where ClientID=?");
my $sProvider  = $dbh->prepare("select * from Provider where ProvID=?");

# This is where the data files are. Adjust as necessary.
use constant searchpath => "/tmp/test/data";
use constant fontpath   => "/usr/share/fonts/msttcore";
use constant outfile    => "printNotes2.pdf";
use constant infile     => "printNotes_Rev2.pdf";
use constant imagefile  => "new.jpg";

# Names of the encounter-specific Blocks contained on the imported page
my @formblocks = ( "agencyname", "noteinfo", "clientname" );

# number of address blocks
my $nblocks = @formblocks;

# Personalization data for the encounter
my @encounters = (
    [ "Mr Maurizio Moroni",   "Strada Provinciale 124", "Reggio Emilia" ],
    [ "Ms Dominique Perrier", "25, rue Lauriston",      "Paris" ],
    [ "Mr Liu Wong",          "55 Grizzly Peak Rd.",    "Butte" ]
);

my $nencounters = @encounters;

# Static text simulates database-driven main contents
my @blockdata = (
    [ "intro", "Dear Paper Planes Fan," ],
    [
        "announcement",
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
    [ "goodbye", "Yours sincerely,\nVictor Kraxi" ]
);

my $nblockdata = @blockdata;

# ClientID: 60309
my @TrIDs  = ( 1059724, 1059727, 1062395 );
my $nTrIDs = @TrIDs;

my @pagehandles = ();
my $pageno      = 0;
my $objtype;

eval {
    my $p = new PDFlib::PDFlib;

    $p->set_option( "SearchPath={{" . searchpath . "}}" );
    $p->set_option( "SearchPath={{" . fontpath . "}}" );

    # This means we must check return values of load_font() etc.
    $p->set_option("errorpolicy=return");

    # all strings are expected as utf8
    $p->set_option("stringformat=utf8");

    if (
        $p->begin_document( outfile,
            "destination={type=fitwindow} pagelayout=singlepage" ) == -1
      )
    {
        throw new Exception( "Error: " . $p->get_errmsg() );
    }

    $p->set_info( "Creator", "PDFlib starter sample" );
    $p->set_info( "Title",   "starter_block" );

    $p->set_option("enumeratefonts saveresources={filename=pdflib.upr}");

    # Open the Block template which contains PDFlib Blocks
    my $indoc = $p->open_pdi_document( infile, "" );
    if ( $indoc == -1 ) { die( "Error: " . $p->get_errmsg() ); }

    my $no_of_input_pages = $p->pcos_get_number( $indoc, "length:pages" );

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

    for ( my $i = 0 ; $i < $nTrIDs ; $i++ ) {
        my $TrID = $TrIDs[$i];
        $sTreatment->execute($TrID)
          || myDBI->dberror("PrintNotes: select Treatment $TrID");
        my $rTreatment = $sTreatment->fetchrow_hashref;
        my $NoteType   = $rTreatment->{Type};
        my $ClientID   = $rTreatment->{'ClientID'};
        $sClient->execute($ClientID)
          || myDBI->dberror("PrintNotes: select Client $ClientID");
        my $rClient = $sClient->fetchrow_hashref;

        # Header info...
        my $AgencyID = MgrTree->getAgency( $form, $rClient->{clinicClinicID} );
        $sProvider->execute($AgencyID) || myDBI->dberror("execute: sProvider");
        my $rAgency    = $sProvider->fetchrow_hashref;
        my $AgencyName = DBA->subxml( $rAgency->{Name} );
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

            # Option list for text blocks
            my $optlist = "encoding=winansi embedding";

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

#my $str = $TrIDs[$i].' '.$i.' <fontname={NotoSerif-Regular} encoding=unicode fontsize=20> this is block: '.$formblocks[$j];
                    my $str =
qq|${AgencyName}\n${AgencyAddr}\n${AgencyCSZ}\n${AgencyPh}|;
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

            $p->end_page_ext("");
        }
    }

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
$sClient->finish();
$sProvider->finish();
myDBI->cleanup();
exit;
