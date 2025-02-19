#!/usr/bin/perl
use lib '/var/www/okmis/src/lib';
use CGI qw(:standard escape);
use Cwd;
use DBI;
use DBA;
use DBForm;
use PDF;
use Time::Local;

############################################################################
# DUPLICATE ROUTINE genTrPlan
# THIS ROUTINE IS USED IN tables.cfg AND IS THE SAME AS reports/genTrPlan
# DUPLICATE ROUTINE genTrPlan
############################################################################
my $form = DBForm->new();
$form = DBUtil->setDates($form);
my $DateRange = qq|from $form->{FromDateD} thru $form->{ToDateD}|;
open DBG, ">/var/www/okmis/src/debug/genTrPlan.out"
  or die "Couldn't open file: $!";
foreach my $f ( sort keys %{$form} ) { print DBG ": form-$f=$form->{$f}\n"; }
############################################################################
my $dbh = $form->dbconnect();
chdir("$form->{DOCROOT}/tmp");
my $sTrPlan = $dbh->prepare("select * from TrPlan where TrPlan.PrAuthID=?");
my $sTrPlanS =
  $dbh->prepare("select * from TrPlanS where TrPlanID=? order by SignDate");
my $sPrAuth =
  $dbh->prepare("select * from ClientPrAuth where ClientPrAuth.ID=?");
my $sClient = $dbh->prepare(
"select * from Client left join ClientIntake on ClientIntake.ClientID=Client.ClientID where Client.ClientID=?"
);
my $sClientPrAuthCDC = $dbh->prepare(
    "select * from ClientPrAuthCDC where ClientPrAuthCDC.ClientPrAuthID=?");
my $sPrAuthRVU = $dbh->prepare(
"select * from PrAuthRVU left join xSC on xSC.SCID=PrAuthRVU.SCID where PrAuthRVU.PrAuthID=? order by xSC.SCNum"
);
my $sInsurance = $dbh->prepare(
"select * from Insurance left join xInsurance on xInsurance.ID=Insurance.InsID where Insurance.InsNumID=?"
);
my $sProvider = $dbh->prepare('select * from Provider where ProvID=?');
my $sClinic   = $dbh->prepare('select * from Provider where ProvID=?');

############################################################################
# this is the pdf template we need
#   it is the first 3 objects with 2 font objects and the content object
$pdtpath = '/var/www/okmis/src/pdf/TrPlan.pdt';
if ( $form->{IDs} ) {
    $pdf = PDF->start($pdtpath);
    &printPDF( $form->{'IDs'} );
    $pdf->finish();
    my $file =
        'genTrPlan_'
      . DBUtil->genToken() . '_'
      . DBUtil->Date( '', 'stamp' ) . '.pdf';
    open PDFFILE, ">${file}" or die "Couldn't open file: $!";
    print PDFFILE $pdf->{outText};
    close(PDFFILE);

    # html file is /tmp -> https:://DOCROOT/tmp
    print qq|Content-Type: application/pdf\n\n$pdf->{outText}|;
}
else {
    $pdf = PDF->start($pdtpath);
    my $cnt = 0;
    my $ForProvID =
      $form->{Provider} ? $form->{Provider} : $form->{LOGINPROVID};
    my $ClinicSelection =
      DBA->getClinicSelection( $form, $ForProvID, 'Client.clinicClinicID' );
##
    # select by TrPlan so we ONLY GET those PAs with a Treatment Plan...
    #  not PG038, 21s or so...
    my $qBySelect = qq|
select TrPlan.PrAuthID
  from TrPlan
    left join ClientPrAuth on ClientPrAuth.ID=TrPlan.PrAuthID
    left join ClientPrAuthCDC on ClientPrAuthCDC.ClientPrAuthID=ClientPrAuth.ID
    left join Client on Client.ClientID=TrPlan.ClientID
  where ClientPrAuthCDC.Status='Approved'
    and (ClientPrAuthCDC.StatusDate>='$form->{FromDate}' and ClientPrAuthCDC.StatusDate<='$form->{ToDate}')
    ${ClinicSelection}
  group by Client.LName, Client.FName 
|;
    print DBG "q=$qBySelect\n";
    my $sBySelect = $dbh->prepare($qBySelect);
    $sBySelect->execute() || $form->dberror($qBySelect);
    while ( my ($PAID) = $sBySelect->fetchrow_array ) {
        print DBG "ClientPrAuth ID is = $PAID\n";
        $cnt++;
        &printPDF($PAID);
    }
    $sBySelect->finish();
    if ( $cnt == 0 ) {
        $pdf->add( '', "/R5 14 Tf\n1 0 0 1 40 740 Tm (None selected.) Tj\n" );
    }
    $pdf->finish();
    my $file =
        'genTrPlan_'
      . DBUtil->genToken() . '_'
      . DBUtil->Date( '', 'stamp' ) . '.pdf';
    open PDFFILE, ">${file}" or die "Couldn't open file: $!";
    print PDFFILE $pdf->{outText};
    close(PDFFILE);

    # html file is /tmp -> https:://DOCROOT/tmp
    print qq|Content-Type: application/pdf\n\n$pdf->{outText}|;
}
$sClinic->finish();
$sProvider->finish();
$sInsurance->finish();
$sClient->finish();
$sPrAuth->finish();
$sClientPrAuthCDC->finish();
$sTrPlan->finish();
$sTrPlanS->finish();
$sPrAuthRVU->finish();
$form->complete();
close(DBG);
exit;

############################################################################
sub printPDF(\%) {
    my ($PrAuthID) = @_;

    $sTrPlan->execute($PrAuthID);
    my $rTrPlan = $sTrPlan->fetchrow_hashref;
    $sPrAuth->execute($PrAuthID);
    my $rPrAuth = $sPrAuth->fetchrow_hashref;
    $sClient->execute( $rPrAuth->{ClientID} );
    my $rClient      = $sClient->fetchrow_hashref;
    my $ClinicID     = $rClient->{clinicClinicID};
    my $ClientProvID = $rClient->{ProvID};
    print DBG
      "ClientID=$rPrAuth->{ClientID}, ClinicID=$rClient->{clinicClinicID}\n";
    $sClinic->execute($ClinicID);
    my $rClinic = $sClinic->fetchrow_hashref;
    print DBG
      "$ClinicID: $rClinic->{Name} ($rClient->{FName} $rClient->{LName})\n";
    $AgencyName = $rClinic->{Name};
    $AgencyAddr = $rClinic->{Addr1} . ', ';
    $AgencyAddr .= $rClinic->{Addr2} . ', ' if ( $rClinic->{Addr2} );
    $AgencyAddr .=
      $rClinic->{City} . ', ' . $rClinic->{ST} . '  ' . $rClinic->{Zip};
    $AgencyPh = 'Office: ' . $rClinic->{WkPh} . '  Fax: ' . $rClinic->{Fax};
    $sProvider->execute($ClientProvID);
    my $rProvider = $sProvider->fetchrow_hashref;
    my $ProvName  = qq|$rProvider->{FName} $rProvider->{LName}|;
    print DBG "$rClient->{ClientID}\t$rClient->{LName}\t$rClient->{FName}\n";

    $sInsurance->execute( $rPrAuth->{InsuranceID} );
    my $rInsurance = $sInsurance->fetchrow_hashref;
    my $DateRange  = 'for '
      . DBUtil->Date( $rPrAuth->{EffDate}, 'fmt', 'MM/DD/YYYY' )
      . ' thru '
      . DBUtil->Date( $rPrAuth->{ExpDate}, 'fmt', 'MM/DD/YYYY' );
    my $DOB     = DBUtil->Date( $rClient->{DOB},        'fmt', 'MM/DD/YYYY' );
    my $ReqDate = DBUtil->Date( $rPrAuth->{StatusDate}, 'fmt', 'MM/DD/YYYY' );

    my $out = '';
##
    # 290 (width of page) / 2 (in half) * 5 (boldness&size of font)
    my $x = ( 290 - ( ( length($AgencyName) / 2 ) * 5 ) );
    $pdf->addElement( $x, 740, $AgencyName, '/R10', 14 );
    $x = ( 290 - ( ( length($AgencyAddr) / 2 ) * 4 ) );
    $pdf->addElement( $x, 730, $AgencyAddr, '/R10', 11 );
    $x = ( 290 - ( ( length($AgencyPh) / 2 ) * 4 ) );
    $pdf->addElement( $x, 720, $AgencyPh, '/R10', 11 );
    $Title = qq|PRIOR AUTHORIZATION ${DateRange}|;
    $x     = ( 290 - ( ( length($Title) / 2 ) * 6 ) );
    $pdf->addElement( $x, 700, $Title, '/R5', 12 );
    my $Type = DBA->getxref( $form, 'xPrAuthType', $rPrAuth->{Type}, 'Descr' );
    $x = ( 290 - ( ( length($Type) / 2 ) * 4 ) );
    $pdf->addElement( $x, 683, $Type, '/R5', 12 );
    $pdf->addElement( 120, 666,
        "$rClient->{LName}, $rClient->{FName} $rClient->{MName}",
        '/R10', 11 );
    $pdf->addElement( 330, 666, $rClient->{ClientID}, '/R10', 11 );
    $pdf->addElement( 120, 655, $DOB,                 '/R10', 11 );
    $pdf->addElement( 330, 655, $rClient->{SSN},      '/R10', 11 );
    $pdf->addElement( 120, 644, $ReqDate,             '/R10', 11 );
    $pdf->addElement( 330, 644, $rPrAuth->{PAnumber}, '/R10', 11 );
    my $ReqType =
      DBA->getxref( $form, 'xPrAuthReqType', $rPrAuth->{ReqType}, 'Descr' );
    $pdf->addElement( 430, 644, $ReqType,                '/R10', 11 );
    $pdf->addElement( 120, 633, $rInsurance->{Name},     '/R10', 11 );
    $pdf->addElement( 330, 633, $rInsurance->{InsIDNum}, '/R10', 11 );
    $sClientPrAuthCDC->execute($PrAuthID)
      || $form->dberror("select ClientPrAuthCDC ${PrAuthID}");

    if ( my $rClientPrAuthCDC = $sClientPrAuthCDC->fetchrow_hashref ) {
        $pdf->addElement( 430, 633, "CDCKey: $rClientPrAuthCDC->{CDCKey}",
            '/R10', 10 );
        my $StatusDate =
          DBUtil->Date( $rClientPrAuthCDC->{StatusDate}, 'fmt', 'MM/DD/YY' );
        $pdf->addElement( 30, 613, "$rClientPrAuthCDC->{Status}: ${StatusDate}",
            '/R10', 10 );
    }

    my $y   = 588;
    my $Cnt = 0;
    if ( $rPrAuth->{PAgroup} eq '' ) {
        $sPrAuthRVU->execute( $rPrAuth->{ID} ) || $form->dberror($qPrAuthRVU);
        while ( my $r = $sPrAuthRVU->fetchrow_hashref ) {
            $Cnt++;
            $pdf->addElement( 30, $y, '*',         '/R10', 10 ) if ( $r->{IC} );
            $pdf->addElement( 35, $y, $r->{SCNum}, '/R10', 10 );
            my $SCName = substr( $r->{SCName}, 0, 56 );
            $pdf->addElement( 100, $y, $SCName,       '/R10', 10 );
            $pdf->addElement( 345, $y, $r->{ReqRVU},  '/R10', 10 );
            $pdf->addElement( 380, $y, $r->{AuthRVU}, '/R10', 10 );
            $pdf->addElement( 410, $y, $r->{PANum},   '/R10', 10 );
            my $EffDate = DBUtil->Date( $r->{EffDate}, 'fmt', 'MM/DD/YY' );
            my $ExpDate = DBUtil->Date( $r->{ExpDate}, 'fmt', 'MM/DD/YY' );
            $pdf->addElement( 475, $y, "${EffDate} thru ${ExpDate}",
                '/R10', 10 );
            $y = $Cnt % 4 == 0 ? $y -= 12 : $y - 13;

            #my $m=$Cnt%5;
            print DBG "$SCName, Cnt=$Cnt, m=$m, y=$y\n";
        }
        $pdf->addText( 30, 495, 430, 50,
            '* means Service is approved for InterChangeable', 8 );
    }
    else {
        my $PAgroup = $rPrAuth->{'PAgroup'};
        my $Descr   = DBA->getxref( $form, 'xPAgroups', $PAgroup, 'Descr' );
        $pdf->addElement( 35, $y, "$PAgroup $Descr", '/R10', 10 );
        my $EffDate = DBUtil->Date( $rPrAuth->{EffDate}, 'fmt', 'MM/DD/YY' );
        my $ExpDate = DBUtil->Date( $rPrAuth->{ExpDate}, 'fmt', 'MM/DD/YY' );
        $pdf->addElement( 380, $y, "\$ $rPrAuth->{AuthAmt}/month", '/R10', 10 );
        $pdf->addElement( 475, $y, "${EffDate} thru ${ExpDate}",   '/R10', 10 );
    }
    my $y   = 538;
    my $x   = 35;
    my $Cnt = 0;
    $sTrPlanS->execute( $rTrPlan->{'TrPlanID'} )
      || $form->dberror("genTrPlan: select TrPlanS ");
    while ( my $rTrPlanS = $sTrPlanS->fetchrow_hashref ) {
        $Cnt++;
        my $signby = DBA->setProvCreds(
            $form, $rTrPlanS->{'ProvID'}, $rInsurance->{InsID},
            $rTrPlanS->{'SignDate'},
            $rTrPlanS->{'SignTime'}
        );
        $pdf->addElement( $x, $y, "${signby}", '/R10', 10 );
        $y = $Cnt % 4 == 0 ? $y -= 12 : $y - 13;
        last if ( $Cnt == 4 );
    }
    $pdf->addText( 35, 467, 430, 50, $rTrPlan->{OthComments},    8 );
    $pdf->addText( 35, 402, 430, 50, $rTrPlan->{TrPlanClResCom}, 8 );
    $pdf->addText( 35, 337, 430, 50, $rTrPlan->{DCCrit1},        8 );
    $pdf->addText( 35, 272, 430, 50, $rTrPlan->{Aftercare},      8 );
    $pdf->addText( 35, 207, 430, 70, $rTrPlan->{Summary},        8 );
    $pdf->addText( 35, 122, 430, 70, $rTrPlan->{TrPlanComments}, 8 );

    # add a page 'deflate' or not ''.
    $pdf->add( 'deflate', $out );
    return (1);
}
############################################################################
