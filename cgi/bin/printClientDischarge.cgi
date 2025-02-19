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

use PDFlib::PDFlib;
use strict;
############################################################################

my $form = myForm->new();
my $IDs  = $form->{'IDs'};
my $dbh  = myDBI->dbconnect( $form->{'DBNAME'} );

# $IDs = '19519';
#warn "PrintDischarge: IDs=${IDs}\n";
##
# prepare selects...
##
my $qDischarge = qq|select * from ClientDischarge where ID=?|;
my $sDischarge = $dbh->prepare($qDischarge);
my $sClientDischargeCDC =
  $dbh->prepare("select * from ClientDischargeCDC where ClientDischargeID=?");
my $qClient =
qq|select Client.*,ClientLegal.JOLTS from Client left join ClientLegal on ClientLegal.ClientID=Client.ClientID where Client.ClientID=?|;
my $sClient   = $dbh->prepare($qClient);
my $sProvider = $dbh->prepare(
"select Provider.*, ProviderControl.LOGO from Provider left join ProviderControl on ProviderControl.ProvID=Provider.ProvID where Provider.ProvID=?"
);
my $qTreatment =
qq|select xSCType.Descr,count(Treatment.TrID) as Count,sum(Treatment.Units) as Units from Treatment left join xSC on xSC.SCID=Treatment.SCID left join okmis_config.xSCType on xSCType.ID=xSC.Type where ClientID=? and Treatment.ContLogDate between ? and ? group by xSCType.Descr|;
my $sTreatment = $dbh->prepare($qTreatment);
my $sPDMed     = $dbh->prepare(
"select * from PDMed where PDMed.ClientID=? and PDMed.StartDate >= ?  and PDMed.MedActive=1 order by PDMed.StartDate desc"
);
my $sInsurance = $dbh->prepare(
"select Insurance.*,xInsurance.Name,xInsurance.Ph1 from Insurance left join xInsurance on xInsurance.ID=Insurance.InsID where Insurance.ClientID=? and Insurance.Priority=? order by Insurance.InsNumEffDate desc, Insurance.InsNumExpDate"
);

my $searchpath = "../data";

my $pagewidth  = 595;
my $pageheight = 842;

my $fontname       = "Roboto-Light";
my $fontsizesmall  = 8;
my $fontsize       = 10;
my $fontsizelarge  = 12;
my $fontsizexlarge = 14;

my $marginleft   = 35;
my $margintop    = 30;
my $marginbottom = 40;
my $contentwidth = $pagewidth - 2 * $marginleft;
my $y_footer     = $marginbottom + 4 * $fontsizelarge + $fontsizesmall;

my $basefontoptions =
    "fontname="
  . $fontname
  . " fontsize="
  . $fontsize
  . " embedding encoding=unicode";
my $baseboldfontoptions  = $basefontoptions . " fakebold=true";
my $basesmallfontoptions = $basefontoptions . " fontsize=" . $fontsizesmall;
my $basesmallboldfontoptions =
  $baseboldfontoptions . " fontsize=" . $fontsizesmall;
my $baseboldlargefontoptions =
  $baseboldfontoptions . " fontsize=" . $fontsizelarge;

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
my $AgencyName;

# my $outfile = "kls.pdf";
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

    $p->set_info( "Creator", "Discharge" );
    $p->set_info( "Author",  "Keith Stephenson" );
    $p->set_info( "Title",   "Discharge Summary 2019-09-01" );

    printDischarge($p);

    $p->end_document("");

};

if ($@) {
    die("$0: PDFlib Exception occurred:\n$@");
}

$sDischarge->finish();
$sClientDischargeCDC->finish();
$sClient->finish();
$sProvider->finish();
$sTreatment->finish();
$sPDMed->finish();
$sInsurance->finish();
myDBI->cleanup();

if ( $form->{'file'} eq '' )    # create and print pdf.
{ print qq|Location: ${filename}\n\n|; }
exit;
############################################################################
sub printDischarge {
    my ($p) = @_;

    foreach my $ID ( split( ' ', $IDs ) ) {

        #warn "PrintDischarge: ID=${ID}\n";
        $sDischarge->execute($ID) || myDBI->dberror($qDischarge);
        while ( my $rDischarge = $sDischarge->fetchrow_hashref ) {
            $sClient->execute( $rDischarge->{ClientID} )
              || myDBI->dberror($qClient);
            my $rClient = $sClient->fetchrow_hashref;
            my $ProvID  = $rClient->{ProvID};
            $sProvider->execute($ProvID)
              || myDBI->dberror(
                "printClientDischarge: select Provider ${ProvID}");
            my $rPrimaryProvider = $sProvider->fetchrow_hashref;

            create_pages( $p, $rDischarge, $rClient, $rPrimaryProvider );
            $totalcount++;
        }
    }
    if   ($totalcount) { create_pagecount($p); }
    else               { create_empty_page($p); }

    #warn "printClientDischarge: pagecount=${pagecount}\n";
    return ($totalcount);
}

sub create_empty_page {
    my ($p) = @_;

    $p->begin_page_ext( $pagewidth, $pageheight, "" );
    $p->fit_textline(
        "NOT FOUND $form->{'IDs'}",
        $marginleft, $pageheight - 50,
        $basefontoptions
    );
    $p->end_page_ext("");
}

sub create_header {
    my ( $p, $rDischarge, $rClientDischargeCDC, $rClient ) = @_;

    # Header info...
    my $AgencyID = MgrTree->getAgency( $form, $rClient->{clinicClinicID} );
    $sProvider->execute($AgencyID)
      || myDBI->dberror("printClientDischarge: select Provider ${AgencyID}");
    my $rAgency = $sProvider->fetchrow_hashref;
    $AgencyName = $rAgency->{Name};
    my $AgencyAddr = $rAgency->{Addr1} . ' ';
    $AgencyAddr .= $rAgency->{Addr2} . ', ' if ( $rAgency->{Addr2} );
    $AgencyAddr .=
      "\n" . $rAgency->{City} . ', ' . $rAgency->{ST} . '  ' . $rAgency->{Zip};
    my $AgencyPh = 'Office: ' . $rAgency->{WkPh} . '  Fax: ' . $rAgency->{Fax};
    my $ServiceFocus =
      DBA->getxref( $form, 'xServiceFocus', $rDischarge->{ServiceFocus},
        'Descr' );
    my $TransType =
      DBA->getxref( $form, 'xCDCTransTypes', $rClientDischargeCDC->{TransType},
        'Text' );
    ##

    my $company          = $AgencyName;
    my $Address          = $AgencyAddr;
    my $OffceFax         = $AgencyPh;
    my $dischargesummary = $ServiceFocus;
    my $dischargetype    = $TransType;

    $p->begin_page_ext( $pagewidth, $pageheight, "" );

    $ypos = $pageheight - $margintop;

    $ypos -= $fontsizexlarge;
    $p->fit_textline( $company, $pagewidth / 2,
        $ypos, $baseboldlargefontoptions . " position={center bottom}" );

    my $h_address = 2 * $fontsizexlarge;
    $ypos -= $h_address;
    my $w_address = 150;
    my $x_address = $pagewidth / 2 - $w_address / 2;
    my $tf        = $p->create_textflow( $Address,
        $baseboldlargefontoptions
          . " leading=110% alignment=justify lastalignment=center" );
    $p->fit_textflow(
        $tf, $x_address, $ypos,
        $x_address + $w_address,
        $ypos + $h_address,
        "verticalalign=center"
    );

    $ypos -= $fontsizexlarge;
    $p->fit_textline( $OffceFax, $pagewidth / 2,
        $ypos, $baseboldlargefontoptions . " position={center bottom}" );

    # -----------------------------------
    # Place image of logo
    # -----------------------------------
    $ypos -= 2;
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
    $p->fit_textline( $dischargesummary, $pagewidth / 2,
        $ypos, $baseboldlargefontoptions . " position={center bottom}" );

    $ypos -= $fontsizexlarge;
    $p->fit_textline( $dischargetype, $pagewidth / 2,
        $ypos, $baseboldlargefontoptions . " position={center bottom}" );

    $ypos -= $fontsize;

}

sub create_footer {
    my ( $p, $ClientName, $ClientID ) = @_;

    my $footertext =
"<fakebold=true>Confidentiality of drug/alcohol abuse records is protected by Federal Law."
      . "<fakebold=false> Federal regulations (42 CFR, Part 2 prohibits making any further disclosure of this information unless further disclosure is expressively permitted by written consent of the person to whom it pertains or as otherwise permitted by 42 CFR, Part 2. A GENERAL AUTHORIZATION FOR RELEASE OF MEDICAL OR OTHER INFORMATION IS NOT SUFFICIENT FOR THIS PURPOSE. The Federal rules restrict any use of the information to criminally investigate or prosecute any alcohol/drug abuse client.";
    my $tf;

    $tf = $p->create_textflow( $footertext,
        $basesmallfontoptions . " leading=120% alignment=justify" );
    my $result =
      $p->fit_textflow( $tf, $marginleft, $marginbottom,
        $marginleft + $contentwidth,
        $y_footer, "verticalalign=center" );

    my $font = $p->load_font( $fontname, "unicode", "" );
    $p->setfont( $font, $fontsize );
    $p->show_xy( "$ClientName ($ClientID) ",
        $marginleft, $marginbottom - $fontsize );
    $p->show_xy(
        "Page " . ( ++$pagecount ),
        $pagewidth - $marginleft - 48.8,
        $marginbottom - $fontsize
    );
    $p->suspend_page("");
}

sub render_textline {
    my ( $p, $text, $h_tl, $optlist, $rDischarge, $rClientDischargeCDC,
        $rClient )
      = @_;
    my $ClientID   = $rClient->{ClientID};
    my $ClientName = qq|$rClient->{FName} $rClient->{LName}|;

    if ( $ypos < $y_footer + $h_tl ) {
        create_footer( $p, $ClientName, $ClientID );
        create_header( $p, $rDischarge, $rClientDischargeCDC, $rClient );
    }
    $ypos -= $h_tl;
    $p->fit_textline( $text, $marginleft, $ypos, $optlist );
}

sub render_textflow {
    my ( $p, $tf, $rDischarge, $rClientDischargeCDC, $rClient ) = @_;
    my $ClientID   = $rClient->{ClientID};
    my $ClientName = qq|$rClient->{FName} $rClient->{LName}|;
    my $result;
    my $h_tf;

    do {
        $result =
          $p->fit_textflow( $tf, $marginleft, $y_footer,
            $marginleft + $contentwidth,
            $ypos, "" );
        if ( $result eq "_boxfull" || $result eq "_boxempty" ) {
            create_footer( $p, $ClientName, $ClientID );
            create_header( $p, $rDischarge, $rClientDischargeCDC, $rClient );
        }
    } while ( $result ne "_stop" );
    $h_tf = $p->info_textflow( $tf, "textheight" );

    return $h_tf;
}

sub render_table {
    my ( $p, $tbl, $rDischarge, $rClientDischargeCDC, $rClient ) = @_;
    my $ClientID   = $rClient->{ClientID};
    my $ClientName = qq|$rClient->{FName} $rClient->{LName}|;
    my $result;
    my $h_tbl;
    my $RowHeightLimit = 15;
    my $diff;

    $diff = $ypos - $y_footer;
    if ( $diff <= $RowHeightLimit ) {
        create_footer( $p, $ClientName, $ClientID );
        create_header( $p, $rDischarge, $rClientDischargeCDC, $rClient );
    }

    do {
        $result =
          $p->fit_table( $tbl, $marginleft, $y_footer,
            $marginleft + $contentwidth,
            $ypos, "" );
        if ( $result eq "_boxfull" ) {
            create_footer( $p, $ClientName, $ClientID );
            create_header( $p, $rDischarge, $rClientDischargeCDC, $rClient );
        }
    } while ( $result eq "_boxfull" );
    $h_tbl = $p->info_table( $tbl, "height" );

    return $h_tbl;
}

sub create_pages {
    my ( $p, $rDischarge, $rClient, $rPrimaryProvider ) = @_;

    ##
    $sClientDischargeCDC->execute( $rDischarge->{ID} )
      || myDBI->dberror(
        "PrintDischarge: select ClientDischargeCDC $rDischarge->{ID}");
    my $rClientDischargeCDC = $sClientDischargeCDC->fetchrow_hashref;
    my $EffDate             = $rDischarge->{IntDate};
    my $ExpDate             = $rClientDischargeCDC->{TransDate};
    ##

    # Client info...
    my $ClientName = qq|$rClient->{FName} $rClient->{LName}|;
    my $ClientID   = $rClient->{ClientID};
    my $IntDatefmt =
      DBUtil->Date( $rDischarge->{IntDate}, 'fmt', 'MM/DD/YYYY' );
    my $TransDatefmt =
      DBUtil->Date( $rClientDischargeCDC->{TransDate}, 'fmt', 'MM/DD/YYYY' );
    my $DateCompleted =
      DBUtil->Date( $rDischarge->{CreateDate}, 'fmt', 'MM/DD/YYYY' );
    $rDischarge->{DevelopBy} = $rDischarge->{DevelopBy};

    my $InitCond = '';
    $rDischarge->{InitCond} = $rDischarge->{InitCond};
    foreach my $line ( DBUtil->parse_lines( $rDischarge->{InitCond}, 120 ) ) {
        $InitCond .= qq|  ${line}\n|;
    }
    my $IDNeeds = '';
    $rDischarge->{IDNeeds} = $rDischarge->{IDNeeds};
    foreach my $line ( DBUtil->parse_lines( $rDischarge->{IDNeeds}, 120 ) ) {
        $IDNeeds .= qq|  ${line}\n|;
    }
    my $Assessment = '';
    $rDischarge->{Assessment} = $rDischarge->{Assessment};
    foreach my $line ( DBUtil->parse_lines( $rDischarge->{Assessment}, 120 ) ) {
        $Assessment .= qq|  ${line}\n|;
    }

    my $Services =
      main->getServices( $rDischarge->{ClientID}, $EffDate, $ExpDate );

    my $Gains = '';
    $rDischarge->{Gains} = $rDischarge->{Gains};
    foreach my $line ( DBUtil->parse_lines( $rDischarge->{Gains}, 120 ) ) {
        $Gains .= qq|  ${line}\n|;
    }
    my $Needs = '';
    $rDischarge->{Needs} = $rDischarge->{Needs};
    foreach my $line ( DBUtil->parse_lines( $rDischarge->{Needs}, 120 ) ) {
        $Needs .= qq|  ${line}\n|;
    }
    my $DischargePlan = '';
    $rDischarge->{DischargePlan} = $rDischarge->{DischargePlan};
    foreach
      my $line ( DBUtil->parse_lines( $rDischarge->{DischargePlan}, 120 ) )
    {
        $DischargePlan .= qq|  ${line}\n|;
    }

    my $MedSummary = '';
    $rDischarge->{MedSum} = $rDischarge->{MedSum};
    foreach my $line ( DBUtil->parse_lines( $rDischarge->{MedSum}, 120 ) ) {
        $MedSummary .= qq|  ${line}|;
    }

    my @Medications =
      main->getMeds( $rDischarge->{ClientID}, $EffDate, $ExpDate );
    my @MedicationFollowUp =
      main->getNPIs( $rDischarge->{PhysNPI}, 'medfollowup', );
    my @Referrals =
      main->getNPIs( $rDischarge->{ReferralsNPI}, 'referralsmade' );

    $sProvider->execute( $rDischarge->{StaffID} )
      || myDBI->dberror(
        "printClientDischarge: select Provider $rDischarge->{'StaffID'}");
    my $rProvider = $sProvider->fetchrow_hashref;
    my $Staff     = qq|  $rProvider->{'FName'} $rProvider->{'LName'}|;
    my $FollowUpDate =
      DBUtil->Date( $rDischarge->{FollowUpDate}, 'fmt', 'MM/DD/YYYY' );
    $sProvider->execute( $rDischarge->{'CreateProvID'} )
      || myDBI->dberror(
        "printClientDischarge: select Provider $rDischarge->{'CreateProvID'}");
    my $rEnteredBy = $sProvider->fetchrow_hashref;
    my $EnteredBy  = qq|$rEnteredBy->{FName} $rEnteredBy->{LName}|;
    my $EnteredDate =
      DBUtil->Date( $rDischarge->{CreateDate}, 'fmt', 'MM/DD/YYYY' );

    my $ClientCopy = $rDischarge->{'ClientCopy'} ? '  Yes' : '  No';
    my $ReceivedBy = $rDischarge->{'ReceivedBy'};
    my $Response   = $rDischarge->{'Response'};
    my $OthersCopy = '';
    my $dlm        = '';
    foreach my $s ( split( chr(253), $rDischarge->{OthersCopy} ) ) {
        $OthersCopy .=
          $dlm . DBA->getxref( $form, 'xRelationship', $s, 'Descr' );
        $dlm = '; ';
    }
    ##

    # JOLTS section
    my $Effective = '';
    my $dlm       = '';
    foreach my $s ( split( chr(253), $rDischarge->{Effective} ) ) {
        $Effective .=
          $dlm . DBA->getxref( $form, 'xDisEffective', $s, 'Descr' );
        $dlm = '; ';
    }
    my $Reason = '';
    my $dlm    = '';
    foreach my $s ( split( chr(253), $rDischarge->{Reason} ) ) {
        $Reason .= $dlm . DBA->getxref( $form, 'xDisReason', $s, 'Descr' );
        $dlm = '; ';
    }
    my $Destination = '';
    my $dlm         = '';
    foreach my $s ( split( chr(253), $rDischarge->{Destination} ) ) {
        $Destination .=
          $dlm . DBA->getxref( $form, 'xDisDestination', $s, 'Descr' );
        $dlm = '; ';
    }
    my $EndReason =
        $rClient->{JOLTS} eq ''                   ? ''
      : $rClientDischargeCDC->{'TransType'} == 60 ? 'Successful'
      :                                             'Unsuccessful';
    ##

    my $dateofbirth   = DBUtil->Date( $rClient->{'DOB'}, 'fmt', 'MM/DD/YYYY' );
    my $intakedate    = $IntDatefmt;
    my $dischargedate = $TransDatefmt;
    my $dischargetime = $rClientDischargeCDC->{TransTime};
    my $persons       = $rDischarge->{DevelopBy};
    my $conditionsofintake    = $InitCond;
    my $needs                 = $IDNeeds;
    my $conditionsofdischarge = $Assessment;
    my $gainsorskills         = $Gains;
    my $preferences           = $Needs;
    my $transitionplan        = $DischargePlan;
    my $medicationsummary     = $MedSummary;
    my $companystuff          = $Staff;
    my $followupdate          = $FollowUpDate;
    my $wasgivencopy          = $ClientCopy;
    my $othersgivencopy       = $OthersCopy;
    my $ratings               = $Effective;
    my $dischargereason       = $Reason;
    my $dischargedestination  = $Destination;

    my $optlist;
    my $tf;
    my $h_tf;
    my $row = 1;
    my $col = 1;
    my $tbl = -1;
    my $h_tbl;

    create_header( $p, $rDischarge, $rClientDischargeCDC, $rClient );

    $ypos -= $fontsizelarge;
    $p->fit_textline( "Patient Name:",
        $marginleft, $ypos, $baseboldfontoptions );
    $p->fit_textline( $ClientName, $marginleft + 68, $ypos, $basefontoptions );
    $p->fit_textline( "Chart #:", $pagewidth / 2 - 55,
        $ypos, $baseboldfontoptions );
    $p->fit_textline( $ClientID, $pagewidth / 2 - 15, $ypos, $basefontoptions );
    $p->fit_textline(
        "Date of Birth:",
        $pagewidth / 2 + 90,
        $ypos, $baseboldfontoptions
    );
    $p->fit_textline( $dateofbirth, $pagewidth / 2 + 155,
        $ypos, $basefontoptions );

    $ypos -= ( 2 * $fontsize + 2 );
    $p->fit_textline( "Intake Date:", $marginleft, $ypos,
        $baseboldfontoptions );
    $p->fit_textline( $intakedate, $marginleft + 68, $ypos, $basefontoptions );
    $p->fit_textline(
        "Discharge Date:",
        $pagewidth / 2 - 55,
        $ypos, $baseboldfontoptions
    );
    $p->fit_textline( $dischargedate, $pagewidth / 2 + 20,
        $ypos, $basefontoptions );
    $p->fit_textline(
        "Discharge Time:",
        $pagewidth / 2 + 90,
        $ypos, $baseboldfontoptions
    );
    $p->fit_textline( $dischargetime, $pagewidth / 2 + 167,
        $ypos, $basefontoptions );

    render_textline(
        $p,
        "Person(s) involved in transition/discharge planning:",
        2 * $fontsize + 2,
        $baseboldfontoptions,
        $rDischarge,
        $rClientDischargeCDC,
        $rClient
    );
    render_textline( $p, $persons, 2 * $fontsizesmall,
        $basefontoptions, $rDischarge, $rClientDischargeCDC, $rClient );

    render_textline(
        $p,
        "Condition(s) at time of intake:",
        2 * $fontsizelarge,
        $baseboldfontoptions, $rDischarge, $rClientDischargeCDC, $rClient
    );
    $tf = $p->create_textflow( $conditionsofintake,
        $basefontoptions . " leading=120% alignment=justify" );
    $h_tf =
      render_textflow( $p, $tf, $rDischarge, $rClientDischargeCDC, $rClient );

    $ypos -= $h_tf;
    render_textline( $p, "Needs identified at intake:",
        $fontsizelarge, $baseboldfontoptions,
        $rDischarge,    $rClientDischargeCDC, $rClient );
    $tf = $p->create_textflow( $needs,
        $basefontoptions . " leading=120% alignment=justify" );
    $h_tf =
      render_textflow( $p, $tf, $rDischarge, $rClientDischargeCDC, $rClient );

    $ypos -= $h_tf;
    render_textline( $p, "Condition(s) at time of discharge:",
        $fontsizelarge, $baseboldfontoptions,
        $rDischarge,    $rClientDischargeCDC, $rClient );
    $tf = $p->create_textflow( $conditionsofdischarge,
        $basefontoptions . " leading=120% alignment=justify" );
    $h_tf =
      render_textflow( $p, $tf, $rDischarge, $rClientDischargeCDC, $rClient );

    $ypos -= $h_tf;
    render_textline( $p, "Gains or skills developed during treatment:",
        $fontsizelarge, $baseboldfontoptions,
        $rDischarge,    $rClientDischargeCDC, $rClient );
    $tf = $p->create_textflow( $gainsorskills,
        $basefontoptions . " leading=120% alignment=justify" );
    $h_tf =
      render_textflow( $p, $tf, $rDischarge, $rClientDischargeCDC, $rClient );

    $ypos -= $h_tf;
    render_textline(
        $p,
        "Specific client strengths/needs/abilities/preferences:",
        $fontsizelarge,
        $baseboldfontoptions,
        $rDischarge,
        $rClientDischargeCDC,
        $rClient
    );
    $tf = $p->create_textflow( $preferences,
        $basefontoptions . " leading=120% alignment=justify" );
    $h_tf =
      render_textflow( $p, $tf, $rDischarge, $rClientDischargeCDC, $rClient );

    $ypos -= $h_tf;
    render_textline( $p, "Transition plan:",
        $fontsizelarge, $baseboldfontoptions,
        $rDischarge,    $rClientDischargeCDC, $rClient );
    $tf = $p->create_textflow( $transitionplan,
        $basefontoptions . " leading=120% alignment=justify" );
    $h_tf =
      render_textflow( $p, $tf, $rDischarge, $rClientDischargeCDC, $rClient );

    $ypos -= $h_tf;
    render_textline(
        $p,
"Medication summary (including all medications prescribed at time of intake):",
        $fontsizexlarge,
        $baseboldfontoptions,
        $rDischarge,
        $rClientDischargeCDC,
        $rClient
    );
    $tf = $p->create_textflow( $medicationsummary,
        $basefontoptions . " leading=120% alignment=justify" );
    $h_tf =
      render_textflow( $p, $tf, $rDischarge, $rClientDischargeCDC, $rClient );

    $ypos -= ( $h_tf + $fontsizexlarge );
    my @table_headers =
      ( "Medication", "Instructions Sig", "Prescriber", "Current" );
    for ( $col = 1 ; $col <= $#table_headers + 1 ; $col++ ) {
        $optlist =
            "fittextline={position={left center} "
          . $baseboldfontoptions
          . " underline=true underlineposition=-20%}";
        $tbl = $p->add_table_cell(
            $tbl, $col, $row,
            $table_headers[ $col - 1 ],
            $optlist . ( ( $col eq 2 || $col eq 3 ) ? " colwidth=30%" : "" )
        );
    }
    $row++;

    # ---------- Data rows: one for each item
    $optlist =
        "fittextline={position={left center} "
      . $basefontoptions
      . "} marginright=2";
    if ( $#Medications ne -1 ) {
        for ( my $i = 0 ; $i < $#Medications + 1 ; $i++ ) {
            $col = 1;

            # column 1: Medication
            $tbl = $p->add_table_cell( $tbl, $col++, $row,
                $Medications[$i]{medication}, $optlist );

            # column 2: Instructions Sig
            $tbl = $p->add_table_cell(
                $tbl,
                $col++,
                $row,
                join( ' ',
                    $Medications[$i]{dose}, $Medications[$i]{frequency},
                    $Medications[$i]{route} ),
                $optlist . " colwidth=50%"
            );

            # column 5: Prescriber
            $tf = $p->add_textflow( -1, $Medications[$i]{prescriber},
                $basefontoptions );
            $tbl = $p->add_table_cell( $tbl, $col++, $row, "",
                $optlist . " textflow=" . $tf . " colwidth=50%" );

            # column 6: Current
            $tbl = $p->add_table_cell( $tbl, $col++, $row,
                $Medications[$i]{current}, $optlist );
            $row++;
        }
    }
    else {
        $col = 1;
        $tbl = $p->add_table_cell( $tbl, $col, $row, qq|  None|,
            $optlist . " colwidth=30%" );
    }
    $h_tbl =
      render_table( $p, $tbl, $rDischarge, $rClientDischargeCDC, $rClient );

    $ypos -= $h_tbl;
    render_textline(
        $p,
        "Medication follow-up:",
        2 * $fontsizelarge,
        $baseboldfontoptions, $rDischarge, $rClientDischargeCDC, $rClient
    );
    $row           = 1;
    $col           = 1;
    $tbl           = -1;
    @table_headers = ( "Name", "Address", "Phone", "NPI" );

    for ( $col = 1 ; $col <= $#table_headers + 1 ; $col++ ) {
        $optlist =
            "fittextline={position={left center} "
          . $baseboldfontoptions
          . " underline=true underlineposition=-20%}";
        $tbl = $p->add_table_cell(
            $tbl, $col, $row,
            $table_headers[ $col - 1 ],
            $optlist . ( $col eq 2 ? " colwidth=50%" : "" )
        );
    }
    $row++;
    $optlist = "fittextline={position={left center} " . $basefontoptions . "}";
    if ( $#MedicationFollowUp ne -1 ) {
        for ( my $i = 0 ; $i < $#MedicationFollowUp + 1 ; $i++ ) {
            $col = 1;

            # column: Name
            $tbl = $p->add_table_cell( $tbl, $col++, $row,
                $MedicationFollowUp[$i]{name}, $optlist );

            # column: Address
            $tf = $p->add_textflow( -1, $MedicationFollowUp[$i]{address},
                $basefontoptions );
            $tbl = $p->add_table_cell( $tbl, $col++, $row, "",
                $optlist . " textflow=" . $tf . " colwidth=50%" );

            # column: Phone
            $tbl = $p->add_table_cell( $tbl, $col++, $row,
                $MedicationFollowUp[$i]{phone}, $optlist );

            # column: NPI
            $tbl = $p->add_table_cell( $tbl, $col++, $row,
                $MedicationFollowUp[$i]{npi}, $optlist );
            $row++;
        }
    }
    else {
        $col = 1;
        $tbl = $p->add_table_cell( $tbl, $col, $row, qq|None|, $optlist );
    }
    $h_tbl =
      render_table( $p, $tbl, $rDischarge, $rClientDischargeCDC, $rClient );

    $ypos -= $h_tbl;
    render_textline(
        $p,
        "Referral(s) made:",
        2 * $fontsizelarge,
        $baseboldfontoptions, $rDischarge, $rClientDischargeCDC, $rClient
    );
    $row           = 1;
    $col           = 1;
    $tbl           = -1;
    @table_headers = ( "Type", "Name", "Address", "Phone" );

    for ( $col = 1 ; $col <= $#table_headers + 1 ; $col++ ) {
        $optlist =
            "fittextline={position={left center} "
          . $baseboldfontoptions
          . " underline=true underlineposition=-20%}";
        $tbl = $p->add_table_cell(
            $tbl, $col, $row,
            $table_headers[ $col - 1 ],
            $optlist . ( ( $col eq 2 || $col eq 3 ) ? " colwidth=50%" : "" )
        );
    }
    $row++;
    $optlist = "fittextline={position={left center} " . $basefontoptions . "}";
    if ( $#Referrals ne -1 ) {
        for ( my $i = 0 ; $i < $#Referrals + 1 ; $i++ ) {
            $col = 1;

            # column: Type
            $tbl = $p->add_table_cell( $tbl, $col++, $row, $Referrals[$i]{type},
                $optlist );

            # column: Name
            $tf =
              $p->add_textflow( -1, $Referrals[$i]{name}, $basefontoptions );
            $tbl = $p->add_table_cell( $tbl, $col++, $row, "",
                $optlist . " textflow=" . $tf . " colwidth=50%" );

            # column: Address
            $tf =
              $p->add_textflow( -1, $Referrals[$i]{address}, $basefontoptions );
            $tbl = $p->add_table_cell( $tbl, $col++, $row, "",
                $optlist . " textflow=" . $tf . " colwidth=50%" );

            # column: Phone
            $tbl =
              $p->add_table_cell( $tbl, $col++, $row, $Referrals[$i]{phone},
                $optlist );
            $row++;
        }
    }
    else {
        $col = 1;
        $tbl = $p->add_table_cell( $tbl, $col, $row, qq|None|,
            $optlist . " colspan=2" );
        $row++;
    }
    if (   $rDischarge->{'OthRefType'} eq ''
        && $rDischarge->{'OthRefName'} eq ''
        && $rDischarge->{'OthRefAddr'} eq '' )
    {
        $col = 1;
        $tbl =
          $p->add_table_cell( $tbl, $col, $row, qq|Other: none|, $optlist );
    }
    else {
        $col = 1;
        $tbl = $p->add_table_cell(
            $tbl,
            $col,
            $row,
qq|Other: $rDischarge->{'OthRefType'} / $rDischarge->{'OthRefName'} / $rDischarge->{'OthRefAddr'} / $rDischarge->{'OthRefWkPh'}|,
            $optlist
        );
    }
    $h_tbl =
      render_table( $p, $tbl, $rDischarge, $rClientDischargeCDC, $rClient );

    $ypos -= $h_tbl;
    render_textline( $p, "Response of the Client:",
        $fontsize,   $basesmallboldfontoptions,
        $rDischarge, $rClientDischargeCDC, $rClient );
    $tf = $p->create_textflow( $Response,
        $basefontoptions . " leading=120% alignment=justify" );
    $h_tf =
      render_textflow( $p, $tf, $rDischarge, $rClientDischargeCDC, $rClient );

    $ypos -= $h_tf;
    render_textline(
        $p,
        "$AgencyName Staff responsible for follow-up of referral(s):",
        2 * $fontsizelarge,
        $baseboldfontoptions,
        $rDischarge,
        $rClientDischargeCDC,
        $rClient
    );

  # $p->fit_textline($companystuff, $marginleft + 260, $ypos, $basefontoptions);
    $tf = $p->create_textflow( $companystuff . "\n",
        $basefontoptions . " leading=120% alignment=justify" );
    $h_tf =
      render_textflow( $p, $tf, $rDischarge, $rClientDischargeCDC, $rClient );

    $ypos -= $h_tf;
    render_textline( $p, "Follow-up date:",
        $fontsizexlarge, $baseboldfontoptions,
        $rDischarge,     $rClientDischargeCDC, $rClient );
    $p->fit_textline( $followupdate, $marginleft + 75, $ypos,
        $basefontoptions );

    $ypos -= 6 * $fontsizexlarge;
    render_textline( $p, "ELECTRONIC SIGNATURES/DATE STAMPS",
        $fontsize,   $basesmallboldfontoptions,
        $rDischarge, $rClientDischargeCDC, $rClient );

    my $signedBy = main->getSigns(
        $rDischarge->{ClientID},           $rDischarge->{CreateProvID},
        $rClientDischargeCDC->{TransDate}, $rClientDischargeCDC->{TransTime}
    );
    $tf = $p->create_textflow( $signedBy,
        $basefontoptions . " leading=120% alignment=justify" );
    $h_tf =
      render_textflow( $p, $tf, $rDischarge, $rClientDischargeCDC, $rClient );

    $ypos -= $h_tf;
    $ypos -= 5 * $fontsizexlarge;
    render_textline( $p, "Client was given copy of this plan:",
        $fontsize,   $basesmallboldfontoptions,
        $rDischarge, $rClientDischargeCDC, $rClient );
    $p->fit_textline( $wasgivencopy, $marginleft + 128,
        $ypos, $basesmallfontoptions );

    render_textline(
        $p,
"Client received resource list information regarding treatment options if symptoms recur or additional services are needed:",
        $fontsizelarge,
        $basesmallboldfontoptions,
        $rDischarge,
        $rClientDischargeCDC,
        $rClient
    );

    my $font = $p->load_font( "DejaVuSans", "unicode", "" );
    $p->setfont( $font, $fontsize );
    my ( $byMail, $inPerson ) = ( '', '' );
    if ( $ReceivedBy eq 'M' ) {
        $byMail   = "&#x2611;";
        $inPerson = "&#x2610;";
    }
    elsif ( $ReceivedBy eq 'P' ) {
        $byMail   = "&#x2610;";
        $inPerson = "&#x2611;";
    }
    else {
        $byMail   = "&#x2610;";
        $inPerson = "&#x2610;";
    }
    $p->fit_textline( $byMail, 485, $ypos - 2,
        "fontname={DejaVuSans} encoding=unicode fontsize=10 charref" );
    $p->fit_textline( "By mail", 495, $ypos, $basesmallfontoptions );
    $p->fit_textline( $inPerson, 526, $ypos - 2,
        "fontname={DejaVuSans} encoding=unicode fontsize=10 charref" );
    $p->fit_textline( "In person", 536, $ypos, $basesmallfontoptions );

    render_textline( $p, "Others given copy of this plan:",
        $fontsizelarge, $basesmallboldfontoptions,
        $rDischarge,    $rClientDischargeCDC, $rClient );
    $p->fit_textline( $othersgivencopy, $marginleft + 117,
        $ypos, $basesmallfontoptions );

    $ypos -= 2 * $fontsizexlarge;
    render_textline(
        $p,
        "JOLTS Information",
        $fontsizelarge,
        $baseboldfontoptions . " underline=true underlineposition=-20%",
        $rDischarge,
        $rClientDischargeCDC,
        $rClient
    );

    render_textline( $p, "Program/Service effectiveness rating(s):",
        $fontsizexlarge, $baseboldfontoptions,
        $rDischarge,     $rClientDischargeCDC, $rClient );
    $p->fit_textline( $ratings, $marginleft + 190, $ypos, $basefontoptions );

    render_textline( $p, "Discharge reason:",
        $fontsizexlarge, $baseboldfontoptions,
        $rDischarge,     $rClientDischargeCDC, $rClient );
    $p->fit_textline( $dischargereason, $marginleft + 90,
        $ypos, $basefontoptions );

    render_textline( $p, "Discharge destination:",
        $fontsizexlarge, $baseboldfontoptions,
        $rDischarge,     $rClientDischargeCDC, $rClient );
    $p->fit_textline( $dischargedestination, $marginleft + 110,
        $ypos, $basefontoptions );

    create_footer( $p, $ClientName, $ClientID );
}

############################################################################
sub getServices {
    my ( $self, $ClientID, $EffDate, $ExpDate ) = @_;
    my $fEffDate = DBUtil->Date( $EffDate, 'fmt', 'MM/DD/YYYY' );
    my $fExpDate = DBUtil->Date( $ExpDate, 'fmt', 'MM/DD/YYYY' );
    my ( $out, $cnt ) = ( "  from: ${fEffDate} through ${fExpDate}\n", 0 );
    $sTreatment->execute( $ClientID, $EffDate, $ExpDate );
    while ( my $rTreatment = $sTreatment->fetchrow_hashref ) {
        my $count = $rTreatment->{Count};
        my $units = sprintf( "%.2f", $rTreatment->{Units} );
        my $descr =
          $rTreatment->{Descr} eq '' ? 'Non-Billable' : $rTreatment->{Descr};
        $out .= qq|  ${descr} ${count} notes, ${units} units\n|;
        $cnt++;
    }
    $out .= qq|  None\n| unless ($cnt);
    return ($out);
}

sub getSigns {
    my ( $self, $ClientID, $ProvID, $D, $T ) = @_;
    my $out = '';
    $sInsurance->execute( $ClientID, 1 )
      ;    # select the Primary Insurance for this client.
    my $rInsurance = $sInsurance->fetchrow_hashref;
    my $signedBy =
      DBA->setProvCreds( $form, $ProvID, $rInsurance->{'InsID'}, $D, $T );
    $out .= qq|$signedBy\n|;
    return ($out);
}

sub getMeds {
    my ( $self, $ClientID, $EffDate, $ExpDate ) = @_;
    my ( $out, $cnt ) = ( '', 0 );
    my @dataset = ();

    # $out = qq|  Medication / Dosage / Prescriber / Date  \n|;
    my $rMeds = DBA->getMeds( $form, $ClientID );
    foreach my $f ( sort keys %{$rMeds} ) {
        my ( $date, $time ) = split( ' ', $rMeds->{$f}->{'DrugDate'} );

  #warn qq|rMeds: ${EffDate}: drugdate = $rMeds->{$f}->{'DrugDate'}, ${date}\n|;
        next if ( $date lt $EffDate );

        #warn qq|rMeds: passed: ${date}, ${EffDate}\n|;
        my $drugdate = DBUtil->Date( $date, 'fmt', 'MM/DD/YYYY' );

# $out .= qq|  $rMeds->{$f}->{'DrugInfo'} / $rMeds->{$f}->{'DrugType'} / $rMeds->{$f}->{'PhysicianName'} / ${drugdate}  \n|;
        push(
            @dataset,
            {
                "medication" => $rMeds->{$f}->{'DrugInfo'},
                "dose"       => $rMeds->{$f}->{'DrugType'},
                "frequency"  => "",
                "route"      => "",
                "prescriber" => $rMeds->{$f}->{'PhysicianName'},
                "current"    => ${drugdate}
            }
        );
        $cnt++;
    }

    # $out = qq|  None\n| unless ( $cnt );
    return @dataset;
}

sub fc {    # convert text to formal case
    my ($text) = @_;
    return join " ", map { ucfirst } split " ", lc $text;
}

sub getNPIs {
    my ( $self, $NPIs, $Fld ) = @_;
    my @out = ();

    #warn qq|NPIs=$NPIs\n|;
    foreach my $NPI ( split( chr(253), $NPIs ) ) {

        #warn qq|NPI=$NPI\n|;
        my $rxNPI = DBA->selxref( $form, 'xNPI', 'NPI', $NPI );
        if ( $Fld eq 'medfollowup' ) {
            my $name = fc "$rxNPI->{'ProvLastName'}, $rxNPI->{'ProvFirstName'}";
            my $address =
                fc "$rxNPI->{'Addr1'}, "
              . ( $rxNPI->{'Addr2'} ? $rxNPI->{'Addr2'} . ", " : "" )
              . " $rxNPI->{'City'}, $rxNPI->{'ST'}, $rxNPI->{'Zip'}";
            my $phone = $rxNPI->{'WkPh'};
            my $npi   = $rxNPI->{'NPI'};
            push(
                @out,
                {
                    "name"    => $name,
                    "address" => $address,
                    "phone"   => $phone,
                    "npi"     => $npi
                }
            );
        }
        else    # elsif ( $Fld eq 'referralsmade' )
        {
            my $type = fc $rxNPI->{'Type'};
            my $name = fc $rxNPI->{'ProvOrgName'};
            my $addr =
                fc "$rxNPI->{'Addr1'}, "
              . ( $rxNPI->{'Addr2'} ? $rxNPI->{'Addr2'} . ", " : "" )
              . " $rxNPI->{'City'}, $rxNPI->{'ST'}, $rxNPI->{'Zip'}";
            my $phone = $rxNPI->{'WkPh'};
            push(
                @out,
                {
                    "type"    => $type,
                    "name"    => $name,
                    "address" => $addr,
                    "phone"   => $phone
                }
            );
        }
    }
    return @out;
}
############################################################################

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

