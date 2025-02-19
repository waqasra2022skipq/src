#!/usr/bin/perl
############################################################################
use lib '/var/www/okmis/src/lib';

use strict;

use warnings;
use PDF::API2;
use myConfig;
use DBForm;

############################################################################
my $form = DBForm->new();
my $dbh  = $form->dbconnect();

##
# prepare selects...
##
my $sSOGS     = $dbh->prepare("select * from SOGS where ID=?");
my $sClient   = $dbh->prepare("select * from Client where ClientID=?");
my $qProvider = qq|select * from Provider where ProvID=?|;
my $sProvider = $dbh->prepare($qProvider);
my $ClientID;

# Input PDF file with questions
my $input_pdf = myConfig->cfg('FORMDIR') . "/PrintSOGS_Rev2.pdf";

# Open an new PDF file
my $base_pdf = PDF::API2->new();

foreach my $ID ( split / /, $form->{IDs} ) {

    # Open an existing PDF file
    my $pdf = PDF::API2->open($input_pdf);
    $base_pdf->import_page( $pdf, 1, 1 );
    $base_pdf->import_page( $pdf, 2, 2 );
}

my $page_count = 0;

my $total_pages = $base_pdf->page_count();
foreach my $ID ( split / /, $form->{IDs} ) {
    $sSOGS->execute($ID) || $form->dberror("PrintSOGS: select SOGS $ID");
    my $r = $sSOGS->fetchrow_hashref;

    # Client info...
    $ClientID = $r->{'ClientID'};
    $sClient->execute($ClientID)
      || $form->dberror("PrintSOGS: select Client $ClientID");
    my $rClient = $sClient->fetchrow_hashref;
    my $ClientName =
      qq|$rClient->{FName} $rClient->{LName} ($rClient->{ClientID})|;

    my $AgencyID = MgrTree->getAgency( $form, $rClient->{clinicClinicID} );
    $sProvider->execute($AgencyID) || $form->dberror($qProvider);

    my $rProvider = $sProvider->fetchrow_hashref;

    my $Staff =
      qq|$rProvider->{'FName'} $rProvider->{'LName'} ($rProvider->{'ProvID'})|;
    $r->{'TransDate'} = DBUtil->Date( $r->{'TransDate'}, 'fmt', 'MM/DD/YYYY' );

    # Retrieve an existing page
    my $page1 = $base_pdf->open_page( ++$page_count );

    # Add a built-in font to the PDF
    my $font = $base_pdf->font('Helvetica');

    my $page_number = $page1->text();
    $page_number->font( $font, 8 );
    $page_number->position( 315, 30 );
    $page_number->text($page_count);

    my $page_number_1_all = $page1->text();
    $page_number_1_all->font( $font, 8 );
    $page_number_1_all->position( 328, 30 );
    $page_number_1_all->text($total_pages);

    # Add some text to the page
    my $text = $page1->text();
    $text->font( $font, 10 );
    $text->position( 70, 720 );
    $text->text($ClientName);

    my $date_top = $page1->text();
    $date_top->font( $font, 10 );
    $date_top->position( 250, 720 );
    $date_top->text( $r->{'TransDate'} );

    my $Staff_text = $page1->text();
    $Staff_text->font( $font, 10 );
    $Staff_text->position( 450, 720 );
    $Staff_text->text($Staff);

    # Line 1
    my $A1a1 = $page1->text();
    $A1a1->font( $font, 8 );
    $A1a1->position( 350, 630 );
    $A1a1->text( $r->{'A1a1'} );

    my $A1a2 = $page1->text();
    $A1a2->font( $font, 8 );
    $A1a2->position( 470, 630 );
    $A1a2->text( $r->{'A1a2'} );

    # Line 2
    my $A1b1 = $page1->text();
    $A1b1->font( $font, 8 );
    $A1b1->position( 350, 600 );
    $A1b1->text( $r->{'A1b1'} );

    my $A1b2 = $page1->text();
    $A1b2->font( $font, 8 );
    $A1b2->position( 470, 600 );
    $A1b2->text( $r->{'A1b2'} );

    # Line 3
    my $A1c1 = $page1->text();
    $A1c1->font( $font, 8 );
    $A1c1->position( 350, 570 );
    $A1c1->text( $r->{'A1c1'} );

    my $A1c2 = $page1->text();
    $A1c2->font( $font, 8 );
    $A1c2->position( 470, 570 );
    $A1c2->text( $r->{'A1c2'} );

    # Line 4
    my $A1d1 = $page1->text();
    $A1d1->font( $font, 8 );
    $A1d1->position( 350, 540 );
    $A1d1->text( $r->{'A1d1'} );

    my $A1d2 = $page1->text();
    $A1d2->font( $font, 8 );
    $A1d2->position( 470, 540 );
    $A1d2->text( $r->{'A1d2'} );

    # Line 5
    my $A1e1 = $page1->text();
    $A1e1->font( $font, 8 );
    $A1e1->position( 350, 500 );
    $A1e1->text( $r->{'A1e1'} );

    my $A1e2 = $page1->text();
    $A1e2->font( $font, 8 );
    $A1e2->position( 470, 500 );
    $A1e2->text( $r->{'A1e2'} );

    # Line 6 Q:f
    my $A1f1 = $page1->text();
    $A1f1->font( $font, 8 );
    $A1f1->position( 350, 470 );
    $A1f1->text( $r->{'A1f1'} );

    my $A1f2 = $page1->text();
    $A1f2->font( $font, 8 );
    $A1f2->position( 470, 470 );
    $A1f2->text( $r->{'A1f2'} );

    # Line 7 Q:g
    my $A1g1 = $page1->text();
    $A1g1->font( $font, 8 );
    $A1g1->position( 350, 440 );
    $A1g1->text( $r->{'A1g1'} );

    my $A1g2 = $page1->text();
    $A1g2->font( $font, 8 );
    $A1g2->position( 470, 440 );
    $A1g2->text( $r->{'A1g2'} );

    # Line 8 Q:h
    my $A1h1 = $page1->text();
    $A1h1->font( $font, 8 );
    $A1h1->position( 350, 410 );
    $A1h1->text( $r->{'A1h1'} );

    my $A1h2 = $page1->text();
    $A1h2->font( $font, 8 );
    $A1h2->position( 470, 410 );
    $A1h2->text( $r->{'A1h2'} );

    # Line 9 Q:i
    my $A1i1 = $page1->text();
    $A1i1->font( $font, 8 );
    $A1i1->position( 350, 390 );
    $A1i1->text( $r->{'A1i1'} );

    my $A1i2 = $page1->text();
    $A1i2->font( $font, 8 );
    $A1i2->position( 470, 390 );
    $A1i2->text( $r->{'A1i2'} );

    # Line 10 Q:j
    my $A1j1 = $page1->text();
    $A1j1->font( $font, 8 );
    $A1j1->position( 350, 370 );
    $A1j1->text( $r->{'A1j1'} );

    my $A1j2 = $page1->text();
    $A1j2->font( $font, 8 );
    $A1j2->position( 470, 370 );
    $A1j2->text( $r->{'A1j2'} );

    # Line 11 Q:k
    my $A1k1 = $page1->text();
    $A1k1->font( $font, 8 );
    $A1k1->position( 350, 360 );
    $A1k1->text( $r->{'A1k1'} );

    my $A1k2 = $page1->text();
    $A1k2->font( $font, 8 );
    $A1k2->position( 470, 360 );
    $A1k2->text( $r->{'A1k2'} );

    # Line 13 Q:l
    my $A1l1 = $page1->text();
    $A1l1->font( $font, 8 );
    $A1l1->position( 350, 320 );
    $A1l1->text( $r->{'A1l1'} );

    my $A1l2 = $page1->text();
    $A1l2->font( $font, 8 );
    $A1l2->position( 470, 320 );
    $A1l2->text( $r->{'A1l2'} );

    # Line 14 Q:m
    my $A1m1 = $page1->text();
    $A1m1->font( $font, 8 );
    $A1m1->position( 350, 290 );
    $A1m1->text( $r->{'A1m1'} );

    my $A1m2 = $page1->text();
    $A1m2->font( $font, 8 );
    $A1m2->position( 470, 290 );
    $A1m2->text( $r->{'A1m2'} );

    # Line 15 Q:n
    my $A1n1 = $page1->text();
    $A1n1->font( $font, 8 );
    $A1n1->position( 350, 260 );
    $A1n1->text( $r->{'A1n1'} );

    my $A1n2 = $page1->text();
    $A1n2->font( $font, 8 );
    $A1n2->position( 470, 260 );
    $A1n2->text( $r->{'A1n2'} );

    # Line 16 Q:2
    my $A2 = $page1->text();
    $A2->font( $font, 8 );
    $A2->position( 500, 235 );
    $A2->text( $r->{'A2'} );

    # Line 17 Q:3
    my $A3 = $page1->text();
    $A3->font( $font, 8 );
    $A3->position( 400, 200 );
    $A3->text( $r->{'A3'} );

    # Line 18 Q:4
    my $A4 = $page1->text();
    $A4->font( $font, 8 );
    $A4->position( 450, 165 );
    $A4->text( $r->{'A4'} );

    # Line 19 Q:5a
    my $A5a = $page1->text();
    $A5a->font( $font, 8 );
    $A5a->position( 410, 130 );
    $A5a->text( $r->{'A5a'} );

    # Line 20 Q:5b
    my $A5b = $page1->text();
    $A5b->font( $font, 8 );
    $A5b->position( 500, 100 );
    $A5b->text( $r->{'A5b'} );

    # Retrieve an existing page
    my $page2 = $base_pdf->open_page( ++$page_count );

    my $page_number_2 = $page2->text();
    $page_number_2->font( $font, 8 );
    $page_number_2->position( 315, 30 );
    $page_number_2->text($page_count);

    my $page_number_2_all = $page2->text();
    $page_number_2_all->font( $font, 8 );
    $page_number_2_all->position( 328, 30 );
    $page_number_2_all->text($total_pages);

    # Line 1 Q:6
    my $A6 = $page2->text();
    $A6->font( $font, 8 );
    $A6->position( 100, 735 );
    $A6->text( $r->{'A6'} );

    # Line 2 Q:7
    my $A7 = $page2->text();
    $A7->font( $font, 8 );
    $A7->position( 500, 720 );
    $A7->text( $r->{'A7'} );

    # Line 3 Q:7a
    my $A7a = $page2->text();
    $A7a->font( $font, 8 );
    $A7a->position( 500, 695 );
    $A7a->text( $r->{'A7a'} );

    # Line 4 Q:8
    my $A8 = $page2->text();
    $A8->font( $font, 8 );
    $A8->position( 100, 645 );
    $A8->text( $r->{'A8'} );

    # Line 5 Q:9
    my $A9 = $page2->text();
    $A9->font( $font, 8 );
    $A9->position( 520, 605 );
    $A9->text( $r->{'A9'} );

    # Q:10
    my $A10 = $page2->text();
    $A10->font( $font, 8 );
    $A10->position( 520, 580 );
    $A10->text( $r->{'A10'} );

    # Q:11
    my $A11 = $page2->text();
    $A11->font( $font, 8 );
    $A11->position( 520, 555 );
    $A11->text( $r->{'A11'} );

    # Q:12
    my $A12 = $page2->text();
    $A12->font( $font, 8 );
    $A12->position( 520, 530 );
    $A12->text( $r->{'A12'} );

    # Q:13
    my $A13 = $page2->text();
    $A13->font( $font, 8 );
    $A13->position( 520, 500 );
    $A13->text( $r->{'A13'} );

    # Q:14
    my $A14 = $page2->text();
    $A14->font( $font, 8 );
    $A14->position( 520, 470 );
    $A14->text( $r->{'A14'} );

    # Q:15
    my $A15 = $page2->text();
    $A15->font( $font, 8 );
    $A15->position( 520, 450 );
    $A15->text( $r->{'A15'} );

    # Q:16
    my $A16 = $page2->text();
    $A16->font( $font, 8 );
    $A16->position( 520, 430 );
    $A16->text( $r->{'A16'} );

    # Q:17
    my $A17 = $page2->text();
    $A17->font( $font, 8 );
    $A17->position( 520, 410 );
    $A17->text( $r->{'A17'} );

    # Q:18a
    my $A18a = $page2->text();
    $A18a->font( $font, 8 );
    $A18a->position( 520, 355 );
    $A18a->text( $r->{'A18a'} );

    # Q:18b
    my $A18b = $page2->text();
    $A18b->font( $font, 8 );
    $A18b->position( 520, 335 );
    $A18b->text( $r->{'A18b'} );

    # Q:18c
    my $A18c = $page2->text();
    $A18c->font( $font, 8 );
    $A18c->position( 520, 315 );
    $A18c->text( $r->{'A18c'} );

    # Q:18d
    my $A18d = $page2->text();
    $A18d->font( $font, 8 );
    $A18d->position( 520, 295 );
    $A18d->text( $r->{'A18d'} );

    # Q:18e
    my $A18e = $page2->text();
    $A18e->font( $font, 8 );
    $A18e->position( 520, 275 );
    $A18e->text( $r->{'A18e'} );

    # Q:18f
    my $A18f = $page2->text();
    $A18f->font( $font, 8 );
    $A18f->position( 520, 255 );
    $A18f->text( $r->{'A18f'} );

    # Q:18g
    my $A18g = $page2->text();
    $A18g->font( $font, 8 );
    $A18g->position( 520, 235 );
    $A18g->text( $r->{'A18g'} );

    # Q:18h
    my $A18h = $page2->text();
    $A18h->font( $font, 8 );
    $A18h->position( 520, 215 );
    $A18h->text( $r->{'A18h'} );

    # Q:18i
    my $A18i = $page2->text();
    $A18i->font( $font, 8 );
    $A18i->position( 520, 195 );
    $A18i->text( $r->{'A18i'} );

    # Q:18j
    my $A18j = $page2->text();
    $A18j->font( $font, 8 );
    $A18j->position( 520, 175 );
    $A18j->text( $r->{'A18j'} );

    # Q:18k
    my $A18k = $page2->text();
    $A18k->font( $font, 8 );
    $A18k->position( 520, 155 );
    $A18k->text( $r->{'A18k'} );

    # Total
    $font = $base_pdf->font('Helvetica-Bold');

    my $Total = $page2->text();
    $Total->font( $font, 10 );
    $Total->position( 40, 130 );
    $Total->text('Total Score:');

    # Total
    my $TotalScore = $page2->text();
    $TotalScore->font( $font, 8 );
    $TotalScore->position( 100, 130 );
    $TotalScore->text( $r->{'TotalScore'} );

}

if ( $form->{"file"} ) {

    # If call is from CMD/Terminal
    $base_pdf->save( $form->{"file"} );
}
else {
    # If call is from Browser

    # Create CGI object
    my $cgi = CGI->new;

    my $out_file = "Client_${ClientID}_SOGS.pdf";

    # Set content type to PDF
    print $cgi->header( -type => 'application/pdf', -attachment => $out_file );

    # Save the PDF to a scalar
    my $string = $base_pdf->to_string();

    # Print the PDF content
    print $string;
}

exit 1;
