#!/usr/bin/perl
############################################################################
use lib 'C:/xampp/htdocs/src/lib';
use DBI;
use myForm;
use myDBI;
use MgrTree;
use DBA;
use DBUtil;

#use DBD::mysql;

use PDFlib::PDFlib;
use strict;
############################################################################

my $form      = myForm->new();
my $IDs       = $form->{'IDs'};
my $dbh       = myDBI->dbconnect( $form->{'DBNAME'} );
my $sClient   = $dbh->prepare("select * from Client where ClientID=?");
my $sProvider = $dbh->prepare(
"select Provider.*, ProviderControl.FinMgrID, ProviderControl.LOGO from Provider left join ProviderControl on ProviderControl.ProvID=Provider.ProvID where Provider.ProvID=?"
);

# get the clinic from the first InvID...
my $sFindClinic = $dbh->prepare(
"select * from Client left join Invoices on Invoices.ClientID=Client.ClientID where Invoices.ID=?"
);

my $pagesetting = "width=a4.width height=a4.height";

my $fontname       = "Roboto-Light";
my $fontsizexsmall = 9;
my $fontsizesmall  = 10;
my $fontsize       = 11;
my $fontsizelarge  = 13;

my $marginleft   = 30;
my $margintop    = 40;
my $contentwidth = 535;

my $h_header     = 73;
my $y_headerline = 740;
my $y_start      = $y_headerline + $h_header;

# get the clinic from the first InvID...
my ( $FirstInvID, $dummy ) = split( ' ', $IDs );
$sFindClinic->execute($FirstInvID)
  || myDBI->dberror("printInvoice: select Clinic $FirstInvID");
my $rFindClinic = $sFindClinic->fetchrow_hashref;
my $AgencyID    = MgrTree->getAgency( $form, $rFindClinic->{'clinicClinicID'} );
$sProvider->execute($AgencyID) || myDBI->dberror("execute: sProvider");
my $rAgency    = $sProvider->fetchrow_hashref;
my $AgencyName = $rAgency->{Name};
my $AgencyAddr = $rAgency->{'Addr1'};
$AgencyAddr .= ", " . $rAgency->{'Addr2'} if ( $rAgency->{'Addr2'} );
$AgencyAddr .= "\n"
  . $rAgency->{'City'} . ", "
  . $rAgency->{'ST'} . "  "
  . $rAgency->{'Zip'} . "\n";
my $AgencyPh =
  "Office: " . $rAgency->{'WkPh'} . "\nFax: " . $rAgency->{'Fax'} . "\n";

my ( $logodirectory, $logofilename ) = $rAgency->{'LOGO'} =~ m/(.*\/)(.*)$/;
if    ( $logofilename eq '' ) { $logofilename = 'logo.png'; }
elsif ( not -e "/usr/local/PDFlib/${logofilename}" ) {
    $logofilename = 'logo.png';
}
my $imagesize = 100;
my $x_logo    = $marginleft;
my $y_logo    = $y_headerline + $fontsize;

my $sender         = $AgencyName;
my $senderfull     = $AgencyAddr . $AgencyPh;
my $x_sender       = 190;
my $y_sender       = $y_start - $fontsizelarge * 1.4;
my $x_senderdetail = 190;
my $y_senderdetail = $y_headerline - $fontsizexsmall / 2;
my $w_senderdetail = 220;
my $h_senderdetail = $fontsize * 6;

my $x_invoice = 444;
my $y_invoice = $y_headerline + 40;
my $w_invoice = 130;
my $h_invoice = $fontsize * 3;

my $x_client = $marginleft;
my $h_client = $fontsize * 5;
my $y_client = $y_headerline - $h_client;
my $w_client = $contentwidth - 20;

my @table_headers = (
    "Date",   "Code", "Description / TrID", "Units",
    "Charge", "Type", "Payment",            "PayDate",
    "AmtDue"
);
my @table_alignments = (
    "left",  "left", "left", "right", "right", "left",
    "right", "left", "right"
);

my $x_table  = $marginleft;
my $y_table  = 50;
my $w_table  = $contentwidth;
my $mt_table = 25;

my $footertext =
    "<fontsize="
  . $fontsizesmall
  . ">Please Send Payment to:\n"
  . "<fontsize="
  . $fontsize
  . ">${AgencyName}\n${AgencyAddr}\n\n"
  . "<fontsize="
  . $fontsizesmall
  . ">For questions regarding your invoice contact:\n"
  . "<fontsize="
  . $fontsize . ">";
$sProvider->execute( $rAgency->{FinMgrID} )
  || myDBI->dberror("printInvoice: select FinMgrID");

if ( my $rFinMgr = $sProvider->fetchrow_hashref ) {
    $footertext .=
qq|$rFinMgr->{'FName'} $rFinMgr->{'LName'}\n$rFinMgr->{'JobTitle'}\n${AgencyName}\n$rFinMgr->{'WkPh'}|;
}
else {
    $footertext .= qq|${AgencyName}\n${AgencyPh}|;
}
my $mt_footer = 50;

my $basefontoptions = "";
my $filename        = '/tmp/'
  . $form->{'LOGINID'} . '_'
  . DBUtil->genToken() . '_'
  . DBUtil->Date( '', 'stamp' ) . '.pdf';
my $outfile = $form->{'file'} eq ''    # create and print pdf else just create.
  ? $form->{'DOCROOT'} . $filename
  : $form->{'file'};

#$outfile = 'kls.pdf';

eval {

    # create a new PDFlib object
    my $p = new PDFlib::PDFlib;

    # This mean we don't have to check error return values, but will
    # get an exception in case of runtime problems.

    $p->set_option("errorpolicy=exception");

    # all strings are expected as utf8
    $p->set_option("stringformat=utf8");

    $p->begin_document( $outfile, "" );

    $p->set_info( "Creator", "Keith Stephenson" );
    $p->set_info( "Author",  "Keith Stephenson" );
    $p->set_info( "Title",   "Invoice Print" );

    my @invoices = fetch_invoice($IDs);
    for ( my $i = 0 ; $i < $#invoices + 1 ; $i++ ) {
        my $clientID = $invoices[$i]{clientID};
        my $invID    = $invoices[$i]{invID};
        my $invDate  = $invoices[$i]{invDate};

        my @invItems = fetch_invoice_items($invID);
        create_header( $p, $invID, $invDate );
        create_client( $p, $clientID );
        create_table( $p, @invItems );
    }

    $p->end_document("");

};

if ($@) {
    die("$0: PDFlib Exception occurred:\n$@");
}
$sClient->finish();
$sProvider->finish();
$sFindClinic->finish();
myDBI->cleanup();
if ( $form->{'file'} eq '' )    # create and print pdf.
{ print qq|Location: ${filename}\n\n|; }
exit;

############################################################################
sub fetch_invoice {
    my ($InvIDs) = @_;
    my $query;
    my $query_handle;

    # PREPARE THE QUERY
    my $query =
"SELECT ClientID, ID, DATE_FORMAT(InvDate, '%m/%d/%y') FROM Invoices WHERE ID=?";
    my $query_handle = $dbh->prepare($query);

    my $ClientID;
    my $InvID;
    my $InvDate;

    my @dataset = ();
    foreach my $id ( split( ' ', $InvIDs ) ) {

        # EXECUTE THE QUERY
        $query_handle->execute($id);

        # BIND TABLE COLUMNS TO VARIABLES
        $query_handle->bind_columns( undef, \$ClientID, \$InvID, \$InvDate );

        # LOOP THROUGH RESULTS
        if ( $query_handle->fetch() ) {
            push(
                @dataset,
                {
                    clientID => $ClientID,
                    invID    => $InvID,
                    invDate  => $InvDate
                }
            );
        }
    }
    $query_handle->finish();
    return @dataset;
}

sub fetch_invoice_items {

    my ($invoiceID) = @_;
    my $query;
    my $query_handle;

    my $TrID;
    my $ContDate;
    my $ScNum;
    my $Descr;
    my $Units;
    my $BillAmt;
    my $InsCode;
    my $PaidAmt;
    my $PaidDate;
    my $AmtDue;

    my @dataset = ();

    # PREPARE THE QUERY
    $query =
"SELECT TrID, DATE_FORMAT(ContDate, '%m/%d/%y'), ScNum, Descr, Units, BillAmt, InsCode, PaidAmt, DATE_FORMAT(PaidDate, '%m/%d/%y'), AmtDue FROM InvItems WHERE InvID=$invoiceID";
    $query_handle = $dbh->prepare($query);

    # EXECUTE THE QUERY
    $query_handle->execute();

    # BIND TABLE COLUMNS TO VARIABLES
    $query_handle->bind_columns(
        undef,     \$TrID,     \$ContDate, \$ScNum,
        \$Descr,   \$Units,    \$BillAmt,  \$InsCode,
        \$PaidAmt, \$PaidDate, \$AmtDue
    );

    my $cnt = 0;

    # LOOP THROUGH RESULTS
    while ( $query_handle->fetch() ) {
        $cnt++;

        #warn qq|cnt=$cnt\n|;
        push(
            @dataset,
            {
                date       => $ContDate,
                code       => $ScNum,
                descr_trid => "$Descr / #$TrID",
                units      => $Units,
                charge     => $BillAmt,
                type       => $InsCode,
                payment    => $PaidAmt,
                paydate    => $PaidDate,
                amtdue     => $AmtDue
            }
        );
    }
    $query_handle->finish();
    return @dataset;
}

sub create_header {
    my ( $p, $invoiceID, $invoiceDate ) = @_;

    my $invoicetext =
        "INVOICE DATE: <fakebold=true>$invoiceDate\n"
      . "<fakebold=false>INVOICE #: <fakebold=true>$invoiceID";

    $p->begin_page_ext( 0, 0, $pagesetting );

    # -----------------------------------
    # Place image of logo
    # -----------------------------------
    $basefontoptions =
        "fontname="
      . $fontname
      . " fontsize="
      . $fontsize
      . " embedding encoding=unicode";

    my $logoimage = $p->load_image( "auto", $logofilename, "" );
    my $optlist =
      "boxsize={" . $imagesize . " " . $imagesize . "} fitmethod=meet";
    $p->fit_image( $logoimage, $x_logo, $y_logo, $optlist );
    $p->close_image($logoimage);

    # -----------------------------------
    # Place sender and sender detail
    # -----------------------------------

    $p->setlinewidth(1.2);
    $p->moveto( $marginleft, $y_headerline );
    $p->lineto( $marginleft + $contentwidth, $y_headerline );
    $p->closepath_stroke();

    # -----------------------------------
    # Place sender and sender detail
    # -----------------------------------

    $optlist = $basefontoptions . " fontsize=" . $fontsizelarge;
    $p->fit_textline( $sender, $x_sender, $y_sender, $optlist );
    $optlist =
        $basefontoptions
      . " fontname="
      . $fontname
      . " fontsize="
      . $fontsize
      . " leading=105% alignment=justify lastalignment=center";
    my $tf = $p->create_textflow( $senderfull, $optlist );
    $p->fit_textflow(
        $tf, $x_senderdetail, $y_senderdetail,
        $x_senderdetail + $w_senderdetail,
        $y_senderdetail + $h_senderdetail,
        "verticalalign=bottom"
    );
    $p->delete_textflow($tf);

    # -----------------------------------
    # Place invoice date and invoice
    # -----------------------------------

    $optlist =
        $basefontoptions
      . " alignment=justify leading=120% fontsize="
      . $fontsize;
    $tf = $p->create_textflow( $invoicetext, $optlist );
    $p->fit_textflow(
        $tf, $x_invoice, $y_invoice,
        $x_invoice + $w_invoice,
        $y_invoice + $h_invoice,
        "verticalalign=center"
    );
    $p->delete_textflow($tf);

}

sub create_client {
    my ( $p, $clientID ) = @_;

    # -----------------------------------
    # Place client, address, phone
    # -----------------------------------

    $sClient->execute($clientID)
      || myDBI->dberror("printInvoice: select Client $clientID");
    my $rClient = $sClient->fetchrow_hashref;
    my $ClientAddr =
      $rClient->{'Addr2'} eq ''
      ? qq|$rClient->{'Addr1'}|
      : qq|$rClient->{'Addr1'}, $rClient->{'Addr2'}|;
    $ClientAddr .=
      qq|, $rClient->{'City'}, $rClient->{'ST'}  $rClient->{'Zip'}|;
    my $clienttext =
"Client: <fakebold=true>$rClient->{'FName'} $rClient->{'LName'} ($rClient->{'ClientID'})\n"
      . "<fakebold=false>Address: <fakebold=true>${ClientAddr}\n"
      . "<fakebold=false>Phone#: <fakebold=true>$rClient->{'HmPh'}";
    my $optlist =
        $basefontoptions
      . " fontname="
      . $fontname
      . " fontsize="
      . $fontsize
      . " leading=110%";
    my $tf = $p->create_textflow( $clienttext, $optlist );
    $p->fit_textflow(
        $tf, $x_client, $y_client,
        $x_client + $w_client,
        $y_client + $h_client,
        "verticalalign=center"
    );
    $p->delete_textflow($tf);
}

sub create_table {
    my ( $p, @dataset ) = @_;

    my $total     = 0;
    my $pagecount = 0;

    $basefontoptions =
        "fontname="
      . $fontname
      . " fontsize="
      . $fontsize
      . " embedding encoding=unicode";

    my $smallfontoption =
        "fontname="
      . $fontname
      . " fontsize="
      . $fontsizesmall
      . " embedding encoding=unicode";

    my $smallboldfontoption = $smallfontoption . " fakebold=true";

    # -----------------------------------
    # Create and place table with item list
    # -----------------------------------

    # ---------- Header row
    my $row = 1;
    my $col = 1;
    my $tbl = -1;
    my $buf;
    my $optlist;
    my $font;
    my $tf;

    for ( $col = 1 ; $col <= $#table_headers + 1 ; $col++ ) {
        $optlist =
            "fittextline={position={"
          . $table_alignments[ $col - 1 ]
          . " center} "
          . $basefontoptions
          . "} margin=2";
        $tbl = $p->add_table_cell( $tbl, $col, $row, $table_headers[ $col - 1 ],
            $optlist );
    }
    $row++;

    # ---------- Data rows: one for each item

    for ( my $i = 0 ; $i < $#dataset + 1 ; $i++ ) {
        my $sum = $dataset[$i]{amtdue};
        $col = 1;

        # column 1: Date
        $optlist =
            "fittextline={position={"
          . $table_alignments[ $col - 1 ]
          . " center} "
          . $smallboldfontoption
          . "} margin=2";
        $tbl = $p->add_table_cell( $tbl, $col++, $row, $dataset[$i]{date},
            $optlist );

        # column 2: Code
        $optlist =
            "fittextline={position={"
          . $table_alignments[ $col - 1 ]
          . " center} "
          . $smallboldfontoption
          . "} margin=2";
        $tbl = $p->add_table_cell( $tbl, $col++, $row, $dataset[$i]{code},
            $optlist );

        # column 3: Description / TrID
        $optlist = "charref " . $smallboldfontoption;
        $tf      = $p->add_textflow( -1, $dataset[$i]{descr_trid}, $optlist );

        $optlist =
            "fittextline={position={"
          . $table_alignments[ $col - 1 ]
          . " center}} textflow="
          . $tf
          . " colwidth=60% margin=2";
        $tbl = $p->add_table_cell( $tbl, $col++, $row, "", $optlist );

        # column 4: Units
        $buf = sprintf( "%.2f", $dataset[$i]{units} );
        $optlist =
            "fittextline={position={"
          . $table_alignments[ $col - 1 ]
          . " center} "
          . $smallboldfontoption
          . "} margin=2";
        $tbl = $p->add_table_cell( $tbl, $col++, $row, $buf, $optlist );

        # column 5: Charge
        $buf = sprintf( "%.2f", $dataset[$i]{charge} );
        $optlist =
            "fittextline={position={"
          . $table_alignments[ $col - 1 ]
          . " center} "
          . $smallboldfontoption . " "
          . "} margin=2";
        $tbl = $p->add_table_cell( $tbl, $col++, $row, $buf, $optlist );

        # column 6: Type
        $optlist =
            "fittextline={position={"
          . $table_alignments[ $col - 1 ]
          . " center} "
          . $smallboldfontoption
          . "} margin=2";
        $tbl = $p->add_table_cell( $tbl, $col++, $row, $dataset[$i]{type},
            $optlist );

        # column 7: Payment
        $buf = sprintf( "%.2f", $dataset[$i]{payment} );
        $optlist =
            "fittextline={position={"
          . $table_alignments[ $col - 1 ]
          . " center} "
          . $smallboldfontoption
          . "} margin=2";
        $tbl = $p->add_table_cell( $tbl, $col++, $row, $buf, $optlist );

        # column 8: PayDate
        $optlist =
            "fittextline={position={"
          . $table_alignments[ $col - 1 ]
          . " center} "
          . $smallboldfontoption
          . "} margin=2";
        $tbl = $p->add_table_cell( $tbl, $col++, $row, $dataset[$i]{paydate},
            $optlist );

        # column 9: AmtDue
        $buf = sprintf( "%.2f", $dataset[$i]{amtdue} );
        $optlist =
            "fittextline={position={"
          . $table_alignments[ $col - 1 ]
          . " center} "
          . $smallboldfontoption
          . "} margin=2";
        $tbl = $p->add_table_cell( $tbl, $col++, $row, $buf, $optlist );

        $total += $sum;
        $row++;
    }

    $optlist =
        "fittextline={position={right center} "
      . $basefontoptions
      . "} margin=2 colspan=2 matchbox={name=subtotaltitle} rowheight=16";
    $tbl = $p->add_table_cell( $tbl, 7, $row, "", $optlist );

    $optlist =
        "fittextline={position={right center} "
      . $smallboldfontoption
      . "} margin=2 matchbox={name=subtotal} rowheight=16";
    $tbl = $p->add_table_cell( $tbl, 9, $row++, "", $optlist );

    # ---------- Place the table instance(s), creating pages as required
    my $result;
    my $roundedValue;
    my $x3;
    my $y3;
    my $y;

    do {

        if ( ++$pagecount == 1 ) {

            $y = $y_headerline - $h_client - $mt_table;
        }
        else {
            $y = $y_start - $mt_table;
        }

        # Place the table on the page; Shade every other row.
        $optlist =
            "header=1 footer=1"
          . " fill={{area=rowodd fillcolor={gray 0.9}} "
          . "{area=header fillcolor={rgb 0.90 0.90 0.98}} "
          . "{area=footer fillcolor={rgb 0.98 0.92 0.84}}}";

        $result = $p->fit_table( $tbl, $x_table, $y_table, $x_table + $w_table,
            $y, $optlist );

        if ( $result ne "_boxfull" ) {
            $roundedValue = sprintf( "%.2f", $total );
            $x3           = 0;
            $y3           = 0;

            if ( $p->info_matchbox( "subtotaltitle", 1, "exists" ) eq 1 ) {
                $x3 = $p->info_matchbox( "subtotaltitle", 1, "x3" );
                $y3 = $p->info_matchbox( "subtotaltitle", 1, "y3" );
            }
            $p->fit_textline( "GRAND TOTAL:", $x3 - 2, $y3 - 2,
                $basefontoptions . " position={right top}" );

            if ( $p->info_matchbox( "subtotal", 1, "exists" ) eq 1 ) {
                $x3 = $p->info_matchbox( "subtotal", 1, "x3" );
                $y3 = $p->info_matchbox( "subtotal", 1, "y3" );
            }
            $p->fit_textline( $roundedValue, $x3 - 2, $y3 - 2,
                $smallboldfontoption . " position={right top}" );

        }
        if ( $result eq "_boxfull" ) {

            # Get the last body row output in the table instance
            my $lastrow = $p->info_table( $tbl, "lastbodyrow" );

            # Calculate the subtotal
            my $subtotal = 0;
            for ( my $i = 0 ; $i < $lastrow - 1 ; $i++ ) {
                $subtotal += $dataset[$i]{amtdue};
            }

            # Format the subtotal to a maximum of two fraction digits
            $roundedValue = sprintf( "%.2f", $subtotal );

            # Retrieve the coordinates of the third (upper right) corner of
            # the "subtotal" matchbox. The parameter "1" indicates the
            # first instance of the matchbox.

            $x3 = 0;
            $y3 = 0;

            if ( $p->info_matchbox( "subtotaltitle", 1, "exists" ) eq 1 ) {
                $x3 = $p->info_matchbox( "subtotaltitle", 1, "x3" );
                $y3 = $p->info_matchbox( "subtotaltitle", 1, "y3" );
            }
            $p->fit_textline( "SUB TOTAL:", $x3 - 2, $y3 - 2,
                $basefontoptions . " position={right top}" );

            if ( $p->info_matchbox( "subtotal", 1, "exists" ) eq 1 ) {
                $x3 = $p->info_matchbox( "subtotal", 1, "x3" );
                $y3 = $p->info_matchbox( "subtotal", 1, "y3" );
            }
            $p->fit_textline( $roundedValue, $x3 - 2, $y3 - 2,
                $smallboldfontoption . " position={right top}" );
            $p->end_page_ext("");
            $p->begin_page_ext( 0, 0, $pagesetting );
        }

    } while ( $result eq "_boxfull" );

    # -----------------------------------------------
    # Place the closing text directly after the table
    # -----------------------------------------------

    # Get the table height of the current table instance
    my $tabheight = $p->info_table( $tbl, "height" );

    my $y = $y - $tabheight - $mt_footer;

    # Add the closing Textflow to be placed after the table
    my $tf_opts = $basefontoptions . " leading=120%" . " alignment=justify";
    my $tf      = $p->create_textflow( $footertext, $tf_opts );

    # Loop until all text has been fit which is indicated by the "_stop"
    # return value of fit_textflow()

    do {
        $result = $p->fit_textflow( $tf, 50, 50, $contentwidth, $y, "" );

        if ( $result eq "_boxfull" || $result eq "_boxempty" ) {
            $p->end_page_ext("");
            $p->begin_page_ext( 0, 0, $pagesetting );
            $y = $y_start - $mt_table;
        }
    } while ( $result ne "_stop" );

    $p->delete_table( $tbl, "" );

    $p->end_page_ext("");
}
