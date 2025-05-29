#!C:/Strawberry/perl/bin/perl.exe
use lib 'C:/xampp/htdocs/src/lib';
use myConfig;
use Cwd;
use DBI;
use myForm;
use myDBI;
use DBUtil;
use myHTML;
use Try::Tiny;
use Excel::Writer::XLSX;

############################################################################
my $form = myForm->new();

my $debug = $form->{'LOGINPROVID'} == 91 ? 0 : 0;

#$debug = 1;
if ($debug) {
    warn qq|\n\n| . localtime() . qq|\n\nGenReport: enter: $form->{Name}\n|;
    foreach my $f ( sort keys %{$form} ) {
        warn "GenReport: form-$f=$form->{$f}\n";
    }
}
my %Args = (
    'Active' =>
      qq|<INPUT TYPE="hidden" NAME="Active" VALUE="$form->{Active}" >|,
    'Days'   => qq|<INPUT TYPE="hidden" NAME="Days" VALUE="$form->{Days}" >|,
    'Folder' =>
      qq|<INPUT TYPE="hidden" NAME="Folder" VALUE="$form->{Folder}" >|,
    'InsCode' =>
      qq|<INPUT TYPE="hidden" NAME="InsCode" VALUE="$form->{InsCode}" >|,
    'CustAgency' =>
      qq|<INPUT TYPE="hidden" NAME="CustAgency" VALUE="$form->{CustAgency}" >|,
    'ClinicIDs' =>
      qq|<INPUT TYPE="hidden" NAME="ClinicIDs" VALUE="$form->{ClinicIDs}" >|,
    'daterange' =>
      qq|<INPUT TYPE="hidden" NAME="daterange" VALUE="$form->{daterange}" >|,
    'FromDate' =>
      qq|<INPUT TYPE="hidden" NAME="FromDate" VALUE="$form->{FromDate}" >|,
    'ToDate' =>
      qq|<INPUT TYPE="hidden" NAME="ToDate" VALUE="$form->{ToDate}" >|,
    'Format' =>
      qq|<INPUT TYPE="hidden" NAME="Format" VALUE="$form->{Format}" >|,
    'InsID'   => qq|<INPUT TYPE="hidden" NAME="InsID" VALUE="$form->{InsID}" >|,
    'ProvIDs' =>
      qq|<INPUT TYPE="hidden" NAME="ProvIDs" VALUE="$form->{ProvIDs}" >|,
    'ClientIDs' =>
      qq|<INPUT TYPE="hidden" NAME="ClientIDs" VALUE="$form->{ClientIDs}" >|,
    'CQM'     => qq|<INPUT TYPE="hidden" NAME="CQM" VALUE="$form->{CQM}" >|,
    'AMSType' =>
      qq|<INPUT TYPE="hidden" NAME="AMSType" VALUE="$form->{AMSType}" >|,
    'ActivityName' =>
qq|<INPUT TYPE="hidden" NAME="ActivityName" VALUE="$form->{ActivityName}" >|,
    'sYearMonth' =>
      qq|<INPUT TYPE="hidden" NAME="sYearMonth" VALUE="$form->{sYearMonth}" >|,
    'CronTime' =>
      qq|<INPUT TYPE="hidden" NAME="CronTime" VALUE="$form->{CronTime}" >|,
    'CronDay' =>
      qq|<INPUT TYPE="hidden" NAME="CronDay" VALUE="$form->{CronDay}" >|,
    'CronMonth' =>
      qq|<INPUT TYPE="hidden" NAME="CronMonth" VALUE="$form->{CronMonth}" >|,
    'CronWeek' =>
      qq|<INPUT TYPE="hidden" NAME="CronWeek" VALUE="$form->{CronWeek}" >|,
);

my $dbh  = myDBI->dbconnect( $form->{'DBNAME'} );
my $cdbh = myDBI->dbconnect('okmis_config');

chdir("$form->{DOCROOT}/tmp");
my $result  = '';
my $xtable  = $form->{'xtable'} eq '' ? 'xReports' : $form->{'xtable'};
my $sxTable = $cdbh->prepare("select * from ${xtable} where Name=?");
$sxTable->execute( $form->{Name} )
  || myDBI->dberror("execute error: $form->{Name}/check");
my $rxTable = $sxTable->fetchrow_hashref;
##foreach my $f ( sort keys %{$rxTable} ) { warn "GenReport: rxTable-$f=$rxTable->{$f}\n"; }

if ( $rxTable->{Inputs} eq 'none' ) {
    my $cmd =
qq| /src/reports/$rxTable->{Script} DBNAME=$form->{DBNAME}\\&mlt=$form->{mlt}\\&hdrline=$form->{hdrline}\\&output=$form->{output}|;

    $result = main->runReport("${cmd}");
}
elsif ( $rxTable->{Inputs} eq 'shell' ) {
    my $cmd =
qq|C:/src/reports/$rxTable->{Script} $form->{$rxTable->{Args}} $form->{mlt}|;
    $result = main->runReport("${cmd}");
}
elsif ( $form->{report} || $form->{save} ) { $result = main->submit(); }
else                                       { $result = main->check(); }
$sxTable->finish();
myDBI->cleanup();
print $result;
exit;

############################################################################
sub check {
    warn qq|GenReport: check: $form->{Name}\n| if ($debug);
    my ( $askSection, $addHIDDEN ) = ( '', '' );
    my $savebutton = $rxTable->{'Outputs'} =~
      /save/i    ## don't give them this as output, but save button option
      ? qq|<INPUT TYPE="submit" NAME="save" VALUE="save" ONCLICK="return validate(this.form);" >|
      : '';

 #foreach my $f ( sort keys %{Args} ) { warn "GenReport: Args-$f=$Args{$f}\n"; }
    my $askIns;
    foreach my $inp ( split( ':', $rxTable->{Inputs} ) ) {
        warn qq|GenReport: process: ${inp}\n| if ($debug);
        if ( $inp eq 'Active' ) {
            delete $Args{Active};
            $askSection .= main->setActive();
        }
        elsif ( $inp eq 'Days' ) {
            delete $Args{Days};
            $askSection .= main->setDays();
        }
        elsif ( $inp eq 'Folder' ) {
            delete $Args{Folder};
            $askSection .= main->setFolder();
        }
        elsif ( $inp eq 'CustAgency' ) {
            delete $Args{CustAgency};
            $askSection .= main->setCustAgency();
        }
        elsif ( $inp eq 'ClinicIDs' ) {
            delete $Args{ClinicIDs};
            if ( SysAccess->getClinics($form) > 1 ) {
                $askSection .= main->setClinicIDs();
            }
        }
        elsif ( $inp eq 'daterange' ) {
            delete $Args{daterange};
            delete $Args{FromDate};
            delete $Args{ToDate};
            $askSection .= main->setDates();
        }
        elsif ( $inp eq 'Format' ) {
            delete $Args{Format};
            $askSection .= main->setFormat();
        }
        elsif ( $inp eq 'InsID' ) {
            delete $Args{InsID};
            $askSection .= main->setInsID();
            $askIns = 1;
        }
        elsif ( $inp eq 'ProvIDs' ) {
            delete $Args{ProvIDs};
            if ( SysAccess->getProviders($form) > 1 ) {
                $askSection .= main->setProvIDs();
            }
        }
        elsif ( $inp eq 'ClientIDs' ) {
            delete $Args{ClientIDs};
            $askSection .= main->setClientIDs();
        }
        elsif ( $inp eq 'sYearMonth' ) {
            delete $Args{sYearMonth};
            $askSection .= main->setYM();
        }
        elsif ( $inp eq 'ProvClients' ) {
            delete $Args{ProvIDs};
            delete $Args{ClientIDs};
            delete $Args{CQM};
            $askSection .= main->setProvClients();
        }
        elsif ( $inp eq 'QRDAIII' ) {
            delete $Args{ProvIDs};
            delete $Args{ClientIDs};
            delete $Args{CQM};
            $askSection .= main->setQRDAIII();
        }
        elsif ( $inp eq 'AMSType' ) {
            delete $Args{AMSType};
            $askSection .= main->setAMSType();
        }
        elsif ( $inp eq 'CronTime' ) {
            delete $Args{CronTime};
            delete $Args{CronDay};
            delete $Args{CronMonth};
            delete $Args{CronWeek};
            $askSection .= main->setCronTime();
        }
    }
    warn qq|\n\n| if ($debug);

 # set the hidden VARS from what was NOT input from screen...
 #foreach my $f ( sort keys %{Args} ) { warn "GenReport: Args-$f=$Args{$f}\n"; }
    foreach my $f ( sort keys %{Args} ) { $addHIDDEN .= "$Args{$f}\n"; }

    # ALWAYS set the type of output...
    $askSection .= main->setOutput();

# to limit reports hanging the system we tried this...ALWAYS narrow to selecting an Insurance
# but users did not like...
    my $validation = $askIns && $form->{'DBNAME'} eq 'okmis_dev'
      ? qq|
  if ( isEmpty(form.InsID) )
  { return vEntry("notnull",form.InsID); }
  else if (typeof form.daterange != "undefined")
  { return vDates(form); }
|
      : qq|
  if (typeof form.daterange != "undefined")
  { return vDates(form); }
|;

    my $html =
      myHTML->newHTML( $form, $form->{'Name'},
        "checkinputwindow noclock countdown_10" )
      . qq|
  <link rel="stylesheet" type="text/css" href="/src/cgi/jcal/calendar-forest.css" >
  <link rel="stylesheet" type="text/css" href="/src/cgi/css/StyleYearMonth.css"> 
  <SCRIPT type="text/javascript" src="/src/cgi/js/ajaxrequest.js"></SCRIPT>
  <script type="text/javascript" src="/src/cgi/jcal/calendar.js"></script>
  <script type="text/javascript" src="/src/cgi/jcal/calendar-en.js"></script>
  <script type="text/javascript" src="/src/cgi/jcal/calendar-setup.js"></script>
  <script type="text/javascript" src="/src/cgi/js/vDate.js"></script>
  <script type="text/javascript" src="/src/cgi/js/vTime.js"></script>
  <script type="text/javascript" src="/src/cgi/js/vNum.js"></script>
  <script type="text/javascript" src="/src/cgi/js/YearMonth.js"></script>
  <SCRIPT TYPE="text/javascript" >
function validate(form)
{
${validation}
}
  </SCRIPT>
</HEAD>
<BODY >
<P >$rxTable->{Descr}</P>
<FORM NAME="$form->{Name}" ACTION="/src/cgi/bin/GenReport.cgi" METHOD="POST">
${askSection}
<TABLE CLASS="home hdrcol" >
  <TR >
    <TD CLASS="hdrcol" >
      <INPUT TYPE="submit" NAME="report" VALUE="report" ONCLICK="return validate(this.form);" >
      ${savebutton}
      <INPUT TYPE="button" NAME="cancel" VALUE="cancel" ONCLICK="javascript: window.close()" >
    </TD >
  </TR>
</TABLE >
<P >$rxTable->{Defn}</P>
<INPUT TYPE="hidden" NAME="Name" VALUE="$form->{Name}" >
<INPUT TYPE="hidden" NAME="hdrline" VALUE="$form->{hdrline}" >
<INPUT TYPE="hidden" NAME="Type" VALUE="$form->{Type}" >
<INPUT TYPE="hidden" NAME="Flag" VALUE="$form->{Flag}" >
<INPUT TYPE="hidden" NAME="Log" VALUE="$form->{Log}" >
<INPUT TYPE="hidden" NAME="NoNonBill" VALUE="$form->{NoNonBill}" >
<INPUT TYPE="hidden" NAME="ForProvID" VALUE="$form->{ForProvID}" >
<INPUT TYPE="hidden" NAME="Client_ClientID" VALUE="$form->{Client_ClientID}" >
<INPUT TYPE="hidden" NAME="ClientCARSReview_ID" VALUE="$form->{ClientCARSReview_ID}" >
<INPUT TYPE="hidden" NAME="mlt" VALUE="$form->{mlt}" >
<INPUT TYPE="hidden" NAME="xtable" VALUE="$form->{xtable}" >
${addHIDDEN}
</FORM>
<SCRIPT LANGUAGE="JavaScript">
document.$form->{Name}.elements[0].focus();
</SCRIPT>
</BODY>
</HTML>
|;
    return ($html);
}

sub submit {
      warn "START DEBUGGUNG!!!!!";
   warn qq|GenReport: submit: $form->{Name}, Inputs=$rxTable->{Inputs}\n| if ($debug);

my $hdrline = $form->{hdrline} ? $form->{hdrline} : 3;

# Start with the Perl interpreter and script path
my $script_path = "C:/xampp/htdocs/src/reports/$rxTable->{Script}";

# Start building the parameter string
my %all_params = %{$form};

# Include extra dynamic Args
foreach my $inp (sort keys %{Args}) {
    $all_params{$inp} = $form->{$inp};
}

# Add optional extras
$all_params{ForProvID}         = $form->{ForProvID}         if $form->{ForProvID};
$all_params{Client_ClientID}   = $form->{Client_ClientID}   if $form->{Client_ClientID};
$all_params{ClientCARSReview_ID} = $form->{ClientCARSReview_ID} if $form->{ClientCARSReview_ID};

# Clean ReportDescr
(my $ReportDescr = $rxTable->{Descr}) =~ s/'//g;
$all_params{ReportDescr} = $ReportDescr;
$all_params{xtable}       = $form->{xtable};
$all_params{submit}       = 1;

    # Build the command parts array
    my @cmd_parts = ("perl", qq|"$script_path"|);

    foreach my $key (sort keys %all_params) {
        my $val = $all_params{$key} // '';
        $val =~ s/"/\\"/g;     # Escape any double quotes inside the value
        push @cmd_parts, qq|"$key=$val"|;  # Add each key=value pair as its own argument
    }

    # Join the command parts into a single command string
    my $cmd = join(' ', @cmd_parts);

    # warn "FINAL CMD: $cmd";  # For debugging

    my $out = main->runReport($cmd);

    my $html = '';
    my ( $header, $body ) = ( '', '' );
    my $sfx = '.txt';
    if ( $form->{output} eq 'ss' ) {
        ( my $Descr = $rxTable->{Descr} ) =~ s;\/;\:;g;
        my $newfile = 'RPT_'
          . $form->{PROVLOGINID} . '_'
          . ${Descr} . '_'
          . $form->{TODAY} . '.xlsx';

        # Your data generation logic here
        my @data = [];
        my @cmd_resp =
          split( '\n', $out );    #Split the Responce from CMD file into lines

        foreach my $line (@cmd_resp) {
            my @tabs = split( '\t', $line );    #Split the Line by Tabs
            @line_here = [];
            foreach my $fld (@tabs) {
                push( @line_here, [$fld] );
            }
            shift @line_here;
            push( @data, [@line_here] );
        }

        my $workbook  = Excel::Writer::XLSX->new($newfile);
        my $worksheet = $workbook->add_worksheet();

        # Write data to the worksheet
        my $row = 0;
        foreach my $row_data (@data) {
            my $col = 0;
            foreach my $cell_data (@$row_data) {
                $worksheet->write( $row, $col, $cell_data );
                $col++;
            }
            $row++;
        }

        # Close the workbook
        $workbook->close();
  
        my $q = new CGI;
        print $q->header(
            -type =>
'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
            -attachment => $newfile
        );

        # Read and print the XLSX file
        open my $xlsx_file, '<', $newfile or die "Unable to open XLSX file: $!";
        binmode $xlsx_file;
        while ( my $chunk = <$xlsx_file> ) {
            print $chunk;
        }
        close $xlsx_file;
    }
    elsif ( $form->{output} eq 'html' ) {
        $header = qq|Content-type: text/html\n\n|;
        $body =
qq|<HTML lang="en" >\n<HEAD><TITLE>$form->{Name}</TITLE></HEAD>\n<BODY >|
          . gHTML->htmlReport( $out, $hdrline )
          . qq|\n</BODY>\n</HTML>\n|;
        $sfx = '.html';
    }
    elsif ( $form->{output} eq 'plain' ) { $body = $out; }
    elsif ( $form->{output} eq 'graph' ) {
        $header = qq|Content-type: text/html\n\n|;
        $body   = qq|<HTML lang="en" >
<HEAD>
  <meta charset="utf-8">
  <TITLE>$form->{Name}</TITLE>
  <script type="text/javascript" src="/src/cgi/d3lib/d3.js"></script>
  <link href="/src/cgi/d3lib/nv.d3.css" rel="stylesheet">
  <script type="text/javascript" src="/src/cgi/d3lib/nv.d3.js"></script>
  <link href="/src/cgi/d3lib/my.d3.css" rel="stylesheet">
</HEAD>
<BODY > 
${out}
</BODY>
</HTML>
|;
        $sfx = '.html';
    }
    elsif ( $form->{output} eq 'pdf' ) {
        $header = qq|Content-Type: application/pdf\n\n|;
        $body   = $out;
        $sfx    = '.pdf';
    }
    elsif ( $form->{output} eq 'fdf' ) {
        $header = qq|Content-Type: application/vnd.fdf\n\n|;
        $body   = $out;
        $sfx    = '.fdf';
    }
    elsif ( $form->{output} eq 'text' ) {
        $header = qq|Content-type: text/html\n\n|;
        $body =
qq|<HTML lang="en" >\n<HEAD><TITLE>$form->{Name}</TITLE></HEAD>\n<BODY>\n<PRE>\n|
          . $out
          . qq|\n</PRE>\n</BODY>\n</HTML>\n|;
    }
    else {
        $header = qq|Content-type: text/html\n\n|;
        $body   = qq|<HTML lang="en" >
<HEAD>
  <TITLE>$form->{Name}</TITLE>
</HEAD>
<BODY>
  <P CLASS="heading">ERROR! output=$form->{output}</P>
</BODY>
</HTML>
|;
        $sfx = '.html';
    }
## KLS
    if ( $form->{save} ) {
        my $linecnt = 0;
        if ( $sfx eq '.pdf' ) { $linecnt = 'x'; }
        else {
            $linecnt = DBUtil->CountFile($diskfile) - 4;
            $linecnt = 0 if ( $linecnt < 0 );
        }
        ( my $Descr = $rxTable->{Descr} ) =~ s;\/;\:;g;
        my $rptDir = $rxReports->{Dir} eq '' ? 'reports2' : $rxReports->{Dir};
        chdir("$form->{DOCROOT}/${rptDir}");
        my $pwd = cwd();
        my $newfile =
            'RPT_scheduled_'
          . $form->{PROVLOGINID} . '_'
          . ${Descr} . '_'
          . $form->{TODAY} . '_'
          . $linecnt . '_'
          . DBUtil->Date( '', 'stamp' ) . '_'
          . DBUtil->genToken() . '.'
          . $sfx;
        open FILE, ">${newfile}" or die "Couldn't open file: $!";
        print FILE $body;
        close(FILE);
        $html =
          myHTML->newHTML( $form, $form->{Name},
            'CheckPopupWindow noclock countdown_1' )
          . qq|
  <P CLASS="heading" >Your report has been saved to your Report List.</P>
  <P CLASS="title" >Report List can be accessed from the main menu Report->My Reports List.</P>
</BODY>
<INPUT TYPE="hidden" NAME="CLOSEWINDOW" VALUE="CLOSE">
</HTML>
|;
        ##DBA->setAlert($form,"You report has been saved.\n");
        warn qq|GenReport: save: COMPLETE\n${html}| if ($debug);
    }
    else { $html = $header . $body; }
    warn qq|GenReport: submit: COMPLETE\n| if ($debug);
    return ($html);
}

sub setProvClients {
    my ($self) = @_;
    my $html;
    my $ListProviders =
      gHTML->selProviders( $form, $form->{LOGINPROVID}, $form->{ProvIDs} );
    my $ListCQMs = DBA->selxTable( $form, xCQM, '', 'MeasureTitle ID' );
    my $html     = qq|
<TABLE CLASS="home fullsize" >
  <TR >
    <TD >
      Select Measure:
      <SELECT NAME="CQM" >${ListCQMs}</SELECT> 
    </TD>
  </TR>
</TABLE >
<TABLE CLASS="home fullsize" >
  <TR >
    <TD > Select Providers:<BR><SELECT NAME="ProvIDs" ONCHANGE="callAjax('ListProviderClients','','ListProviderClients','&id='+this.value,'popup.pl');" SIZE="15" >${ListProviders}</SELECT> </TD >
    <TD WIDTH="66%" >
<SPAN ID="ListProviderClients" >
|
      . myHTML->set1CheckBoxColumn(
        $form, "", 'ClientIDs', 'ClientID',
        'LName~Last Name~strcol:FName~First Name~strcol:DOB~~hdrcol',
        'Select Clients'
      )
      . qq|
</SPAN>
    </TD >
  </TR>
</TABLE >
|;
    warn qq|GenReport: setProvClients: ${html}\n| if ( $debug == 2 );
    return ($html);
}

sub setQRDAIII {
    my ($self) = @_;
    my $html;
    my $ListProviders =
      gHTML->selProviders( $form, $form->{LOGINPROVID}, $form->{ProvIDs} );
    my $ListCQMs = DBA->selxTable( $form, xCQM, '', 'MeasureTitle ID' );
    my $html     = qq|
  <TABLE CLASS="home fullsize" >
    <TR >
      <TD >
        Select Measure:
        <SELECT NAME="CQM" >${ListCQMs}</SELECT> 
      </TD>
    </TR>
  </TABLE >
  <TABLE CLASS="home fullsize" >
    <TR >
      <TD >
        Select Providers:
        <SELECT NAME="ProvIDs" >${ListProviders}</SELECT>
      </TD >
    </TR>
  </TABLE >
  |;
    return ($html);
}

sub setActive {
    my ($self)  = @_;
    my $checked = $form->{Active} ? 'CHECKED' : '';
    my $html    = qq|
<TABLE CLASS="home strcol" >
  <TR>
    <TD >Active only: <INPUT TYPE="checkbox" NAME="Active" VALUE="1" ${checked}></TD >
  </TR>
</TABLE >
|;
    return ($html);
}

sub setDays {
    my ($self) = @_;
    my $html = qq|
<TABLE CLASS="home strcol" >
  <TR>
    <TD >Days: <INPUT TYPE="text" NAME="Days" VALUE="$form->{Days}" ONFOCUS="select()" ONCHANGE="return vNum(this,1,1000)" SIZE="12" ></TD >
  </TR>
</TABLE >
|;
    return ($html);
}

sub setClinicIDs {
    my ($self) = @_;
    my $ListClinics =
      gHTML->selClinics( $form, $form->{LOGINPROVID}, $form->{ClinicIDs} );
    my $html = qq|
<TABLE CLASS="home hdrcol" >
  <TR>
    <TD CLASS="numcol" >Clinics:</TD><TD><SELECT NAME="ClinicIDs" MULTIPLE SIZE="5" >${ListClinics}</SELECT></TD >
  </TR>
</TABLE >
|;
    return ($html);
}

sub setProvIDs {
    my ($self) = @_;
    my $ListProviders =
      gHTML->selProviders( $form, $form->{LOGINPROVID}, $form->{ProvIDs} );
    my $html = qq|
<TABLE CLASS="home hdrcol" >
  <TR>
    <TD CLASS="numcol" >Providers:</TD><TD><SELECT NAME="ProvIDs" MULTIPLE SIZE="5" >${ListProviders}</SELECT></TD >
  </TR>
</TABLE >
|;
    return ($html);
}

sub setClientIDs {
    my ($self)      = @_;
    my $ListClients = DBA->selClients( $form, $form->{ClientIDs} );
    my $html        = qq|
<TABLE CLASS="home hdrcol" >
  <TR>
    <TD CLASS="numcol" >Clients:</TD><TD><SELECT NAME="ClientIDs" MULTIPLE SIZE="5" >${ListClients}</SELECT></TD >
  </TR>
</TABLE >
|;
    return ($html);
}

sub setFormat {
    my ($self) = @_;
    if    ( $form->{Format} =~ /quick/i )        { $quick        = 'CHECKED'; }
    elsif ( $form->{Format} =~ /extended/i )     { $extended     = 'CHECKED'; }
    elsif ( $form->{Format} =~ /jolts/i )        { $jolts        = 'CHECKED'; }
    elsif ( $form->{Format} =~ /byprovidersc/i ) { $byprovidersc = 'CHECKED'; }
    elsif ( $form->{Format} =~ /byproviderdate/i ) {
        $byproviderdate = 'CHECKED';
    }
    elsif ( $form->{Format} =~ /byprovideronly/i ) {
        $byprovideronly = 'CHECKED';
    }
    elsif ( $form->{Format} =~ /byclientsc/i )   { $byclientsc   = 'CHECKED'; }
    elsif ( $form->{Format} =~ /byclientdate/i ) { $byclientdate = 'CHECKED'; }
    else                                         { $quick        = 'CHECKED'; }
    my $html = qq|
<TABLE CLASS="home hdrcol" >
  <TR>
    <TD CLASS="numcol" >Format:</TD>
    <TD CLASS="numcol" >
      <UL>
        <LI><INPUT TYPE="radio" NAME="Format" VALUE="Quick" ${quick} > Quick</LI>
        <LI><INPUT TYPE="radio" NAME="Format" VALUE="Extended" ${extended} > Extended</LI>
        <LI><INPUT TYPE="radio" NAME="Format" VALUE="Jolts" ${jolts} > Jolts</LI>
        <LI><INPUT TYPE="radio" NAME="Format" VALUE="ByProviderCode" ${byprovidersc} > by Provider / Service Code</LI>
        <LI><INPUT TYPE="radio" NAME="Format" VALUE="ByProviderDate" ${byproviderdate} > by Provider / Service Date</LI>
        <LI><INPUT TYPE="radio" NAME="Format" VALUE="ByProviderOnly" ${byprovideronly} > by Provider Only</LI>
        <LI><INPUT TYPE="radio" NAME="Format" VALUE="ByClientCode" ${byclientsc} > by Client / Service Code</LI>
        <LI><INPUT TYPE="radio" NAME="Format" VALUE="ByClientDate" ${byclientdate} > by Client / Service Date</LI>
      </UL>
    </TD >
  </TR>
</TABLE >
|;
    return ($html);
}

sub setInsID {
    my ($self) = @_;
    my $html = qq|
<TABLE CLASS="home hdrcol" >
  <TR>
    <TD >Insurance:</TD>
    <TD>
      <SELECT NAME="InsID" >
| . DBA->selInsurance( $form, $form->{InsID} ) . qq|
      </SELECT>
    </TD>
  </TR>
</TABLE >
|;
    return ($html);
}

sub setCustAgency {
    my ($self) = @_;
    my $CustList =
      DBA->selxTable( $form, 'xCustAgency', $form->{'CustAgency'} );
    my $html = qq|
<TABLE CLASS="home hdrcol" >
  <TR>
    <TD >Custody Agency: <SELECT NAME="CustAgency" >${CustList}</SELECT></TD >
  </TR>
</TABLE >
|;
    return ($html);
}

sub setDates {
    my ($self) = @_;
    if    ( $form->{daterange} eq "thisweek" )    { $thisweek    = 'CHECKED'; }
    elsif ( $form->{daterange} eq "lastweek" )    { $lastweek    = 'CHECKED'; }
    elsif ( $form->{daterange} eq "thismonth" )   { $thismonth   = 'CHECKED'; }
    elsif ( $form->{daterange} eq "lastmonth" )   { $lastmonth   = 'CHECKED'; }
    elsif ( $form->{daterange} eq "last3m" )      { $last3m      = 'CHECKED'; }
    elsif ( $form->{daterange} eq "last6m" )      { $last6m      = 'CHECKED'; }
    elsif ( $form->{daterange} eq "back1m" )      { $back1m      = 'CHECKED'; }
    elsif ( $form->{daterange} eq "back6m" )      { $back6m      = 'CHECKED'; }
    elsif ( $form->{daterange} eq "back12m" )     { $back12m     = 'CHECKED'; }
    elsif ( $form->{daterange} eq "thisquarter" ) { $thisquarter = 'CHECKED'; }
    elsif ( $form->{daterange} eq "lastquarter" ) { $lastquarter = 'CHECKED'; }
    elsif ( $form->{daterange} eq "thisyear" )    { $thisyear    = 'CHECKED'; }
    elsif ( $form->{daterange} eq "lastyear" )    { $lastyear    = 'CHECKED'; }
    elsif ( $form->{daterange} eq "2yago" )       { $twoyago     = 'CHECKED'; }
    elsif ( $form->{daterange} eq "all" )         { $all         = 'CHECKED'; }
    elsif ( $form->{daterange} eq "today" )       { $today       = 'CHECKED'; }
    my $html = qq|
<SCRIPT TYPE="text/javascript" >
function vDates(form)
{
  if ( isEmpty(form.daterange) )
  {
    if ( isEmpty(form.FromDate) )
    {
      if ( isEmpty(form.ToDate) )
      { return vOK(form.FromDate,"Please select a radio date button!\\nor From/To Dates!"); }
      else
      { return vOK(form.FromDate,"Please enter From Date with To Date!"); }
    }
    else
    {
      if ( isEmpty(form.ToDate) )
      { return vOK(form.ToDate,"Please enter To Date with From Date!"); }
    }
  }
  return true;
}
function clrObj(Date,form,name)
{
  var Obj = form[name];
  for(var i = 0; i < Obj.length; i++) 
  { Obj[i].checked = false; }
  return vDate(Date); 
}
</SCRIPT >
<TABLE CLASS="home hdrcol" >
  <TR CLASS="subtitle tophdr" ><TD COLSPAN="3" >week = Mon-Sun (Billing Week)</TD></TR>
  <TR>
    <TD >
      <UL>
        <LI><INPUT TYPE="radio" NAME="daterange" VALUE="today" ${today} >Today</LI>
        <LI><INPUT TYPE="radio" NAME="daterange" VALUE="thisweek" ${thisweek} >This Week</LI>
        <LI><INPUT TYPE="radio" NAME="daterange" VALUE="lastweek" ${lastweek} >Last Week</LI>
        <LI><INPUT TYPE="radio" NAME="daterange" VALUE="thismonth" ${thismonth} >This Month</LI>
        <LI><INPUT TYPE="radio" NAME="daterange" VALUE="lastmonth" ${lastmonth} >Last Month</LI>
      </UL>
    </TD >
    <TD >
      <UL>
        <LI><INPUT TYPE="radio" NAME="daterange" VALUE="last3m" ${last3m} >Last 3 Months (before current)</LI>
        <LI><INPUT TYPE="radio" NAME="daterange" VALUE="last6m" ${last6m} >Last 6 Months (before current)</LI>
        <LI><INPUT TYPE="radio" NAME="daterange" VALUE="back1m" ${back1m} >Back 1 Month from today</LI>
        <LI><INPUT TYPE="radio" NAME="daterange" VALUE="back6m" ${back6m} >Back 6 Months from today</LI>
        <LI><INPUT TYPE="radio" NAME="daterange" VALUE="back12m" ${back12m} >Back 12 Months from today</LI>
      </UL>
    </TD >
    <TD >
      <UL>
        <LI><INPUT TYPE="radio" NAME="daterange" VALUE="thisquarter" ${thisquarter} >This Quarter</LI>
        <LI><INPUT TYPE="radio" NAME="daterange" VALUE="lastquarter" ${lastquarter} >Last Quarter</LI>
        <LI><INPUT TYPE="radio" NAME="daterange" VALUE="thisyear" ${thisyear} >This Year</LI>
        <LI><INPUT TYPE="radio" NAME="daterange" VALUE="lastyear" ${lastyear} >Last Year</LI>
        <LI><INPUT TYPE="radio" NAME="daterange" VALUE="2yago" ${twoyago} >2 Years Ago</LI>
        <LI><INPUT TYPE="radio" NAME="daterange" VALUE="all" ${all} >Everything</LI>
      </UL>
    </TD >
  </TR>
</TABLE >
<TABLE CLASS="home hdrcol" >
  <TR CLASS="subtitle tophdr" ><TD >or select date range</TD</TR>
  <TR>
    <TD >
      <UL>
        <LI>FromDate:
          <INPUT TYPE="text" NAME="FromDate" ID="FromDate" ONCHANGE="return clrObj(this,this.form,'daterange');" ><BUTTON TYPE="reset" ID="FromDateB">calendar</BUTTON>
        </LI>
          <script type="text/javascript">Calendar.setup({inputField:"FromDate",button:"FromDateB"});</script>
        <LI>ToDate:&nbsp;&nbsp;&nbsp;
          <INPUT TYPE="text" NAME="ToDate" ID="ToDate" ONCHANGE="return clrObj(this,this.form,'daterange');" ><BUTTON TYPE="reset" ID="ToDateB">calendar</BUTTON></LI>
          <script type="text/javascript">Calendar.setup({inputField:"ToDate",button:"ToDateB"});</script>
        </LI>
      </UL>
    </TD >
  </TR>
</TABLE >
|;
    return ($html);
}

sub setYM {
    my ($self) = @_;
    my $YM =
        $form->{sYearMonth}
      ? $form->{sYearMonth}
      : substr( $form->{TODAY}, 0, 7 );
    my $html = qq|
<TABLE CLASS="home hdrcol" >
  <TR CLASS="subtitle tophdr" ><TD >select YearMonth from calendar</TD</TR>
  <TR>
    <TD><IMG ALT="Year/Month Picker" ONCLICK="showYearMonth('sYearMonth');" SRC="/images/calendar.jpg" ></TD>
    <TD ><INPUT TYPE="text" NAME="sYearMonth" ID="sYearMonth" VALUE="${YM}" ONFOCUS="this.blur();" ></TD>
  </TR>
</TABLE >
|;
    return ($html);
}

sub setFolder {
    my ($self) = @_;
    my $html = qq|
<TABLE CLASS="home strcol" >
  <TR>
    <TD >Folder: <INPUT TYPE="text" NAME="Folder" VALUE="$form->{Folder}" ONFOCUS="select()" SIZE="60" ></TD >
  </TR>
</TABLE >
|;
    return ($html);
}

sub setAMSType {
    my ($self)  = @_;
    my $AMSType = DBA->selxTable( $form, 'xAMSType', $form->{'AMSType'} );
    my $html    = qq|
<TABLE CLASS="home hdrcol" >
  <TR>
    <TD >AMS Report Type: <SELECT NAME="AMSType" >${AMSType}</SELECT></TD >
  </TR>
</TABLE >
|;
    return ($html);
}

sub setCronTime {
    my ($self) = @_;
    my $html = qq|
<TABLE CLASS="home hdrcol" >
  <TR><TD CLASS="port" COLSPAN="4" >Select Times to run job:</TD></TR>
  <TR>
    <TD >StartTime:
      <INPUT TYPE=text NAME="CronTime" VALUE="$form->{'CronTime'}" ONFOCUS="select()" ONCHANGE="return vTime(this,1,this)" MAXLENGTH="10" SIZE="10" >
    </TD>
    <TD >DayOfMonth:
      <INPUT TYPE="text" NAME="CronDay" VALUE="$form->{CronDay}" ONFOCUS="select()" ONCHANGE="return vNum(this,1,31)" SIZE="12" >
    </TD>
    <TD >Month:
      <SELECT NAME="CronMonth" >
|
      . DBA->selxTable( $form, 'xMonths', $form->{'CronMonth'}, 'ID Descr', 1 )
      . qq|
      </SELECT>
    </TD>
    <TD >DayOfWeek:
      <SELECT NAME="CronWeek" >
|
      . DBA->selxTable( $form, 'xDaysOfWeek', $form->{'CronWeek'}, 'ID Descr',
        1 )
      . qq|
      </SELECT>
    </TD>
  </TR>
</TABLE >
|;
    return ($html);
}

sub setOutput {
    my ($self) = @_;
    my ($html, $OutputTypes, $cnt) = (undef, undef, 0);
    my ($outhtml, $outss, $outpdf, $outfdf, $outgraph, $outtext);
    if    ( $form->{output} =~ /html/i )  { $outhtml  = 'CHECKED'; }
    elsif ( $form->{output} =~ /ss/i )    { $outss    = 'CHECKED'; }
    elsif ( $form->{output} =~ /pdf/i )   { $outpdf   = 'CHECKED'; }
    elsif ( $form->{output} =~ /fdf/i )   { $outfdf   = 'CHECKED'; }
    elsif ( $form->{output} =~ /graph/i ) { $outgraph = 'CHECKED'; }
    elsif ( $form->{output} =~ /text/i )  { $outtext  = 'CHECKED'; }
    else                                  { $outhtml  = 'CHECKED'; }

    if ( $rxTable->{Outputs} =~ /text/ ) {
        $cnt++;
        $OutputTypes .=
qq|        <LI><INPUT TYPE="radio" NAME="output" VALUE="text" ${outtext} > text</LI>|;
    }
    if ( $rxTable->{Outputs} =~ /html/ ) {
        $cnt++;
        $OutputTypes .=
qq|        <LI><INPUT TYPE="radio" NAME="output" VALUE="html" ${outhtml} > html</LI>|;
    }
    if ( $rxTable->{Outputs} =~ /ss/ ) {
        $cnt++;
        $OutputTypes .=
qq|        <LI><INPUT TYPE="radio" NAME="output" VALUE="ss" ${outss} > SpreadSheet</LI>|;
    }
    if ( $rxTable->{Outputs} =~ /pdf/ ) {
        $cnt++;
        $OutputTypes .=
qq|        <LI><INPUT TYPE="radio" NAME="output" VALUE="pdf" ${outpdf} > pdf</LI>|;
    }
    if ( $rxTable->{Outputs} =~ /fdf/ ) {
        $cnt++;
        $OutputTypes .=
qq|        <LI><INPUT TYPE="radio" NAME="output" VALUE="fdf" ${outfdf} > fdf</LI>|;
    }
    if ( $rxTable->{Outputs} =~ /graph/ ) {
        $cnt++;
        $OutputTypes .=
qq|        <LI><INPUT TYPE="radio" NAME="output" VALUE="graph" ${outgraph} > graph</LI>|;
    }
    if ( $cnt > 1 ) {
        $html = qq|
<TABLE CLASS="home hdrcol" >
  <TR CLASS="subtitle tophdr" ><TD >Type of output</TD</TR>
  <TR CLASS="subtitle" >
    <TD >
      <UL>
${OutputTypes}
      </UL>
    </TD >
  </TR>
</TABLE >
|;
    }
    else {
        $html =
          qq|<INPUT TYPE="hidden" NAME="output" VALUE="$rxTable->{Outputs}" >|;
    }
    return ($html);
}

sub runReport {
    my ( $self, $cmd ) = @_;
    my $ProvID  = $form->{'LOGINPROVID'};
    my $RptID   = $rxTable->{'ID'};
    my $RptName = $rxTable->{'Name'};
    warn
qq|GenReport: runReport: $form->{Name}: output=$form->{output}, cmd:${cmd}\n|
      if '1';
    warn
qq|GenReport: runReport: ProvID=$ProvID, RptID=$RptID, xtable=$xtable, RptName=$RptName\n|
      if ($debug);
      
    # first log the Report...
    my $DT = main->getDATETIME();
    my $s  = $dbh->prepare(
"insert into wReports (ProvID,RptID,xtable,RptName,BeginTime) values ($ProvID,$RptID,'$xtable','$RptName','$DT')"
    );
    $s->execute()
      || myDBI->dberror("insert error wReports: ${ProvID}/${RptID}");
    my $NEWID = $s->{'mysql_insertid'};

    # run the Report...
    my $diskfile = DBUtil->ExecCmd( $cmd, '.warn' );
    my $out      = DBUtil->ReadFile($diskfile);

    # end time the Report...
    $DT = main->getDATETIME();
    $s =
      $dbh->prepare("update wReports set EndTime='${DT}' where ID='${NEWID}'");
    $s->execute() || myDBI->dberror("update error wReports: ${NEWID}/${DT}");
    $s->finish();
    warn
qq|GenReport: runReport: $form->{Name}: diskfile=$diskfile\nout=\n${out}\n|
      if ( $debug == 2 );
    return ($out);
}

sub getDATETIME {
    my ($self) = @_;
    my ( $sec, $min, $hrs, $day, $month, $year, $wday, $julian ) = localtime();
    $month++;
    $year += 1900;
    $month = length($month) == 2 ? $month : '0' . $month;
    $day   = length($day) == 2   ? $day   : '0' . $day;
    $hrs   = length($hrs) == 2   ? $hrs   : '0' . $hrs;
    $min   = length($min) == 2   ? $min   : '0' . $min;
    $sec   = length($sec) == 2   ? $sec   : '0' . $sec;
    my $CURTIME = qq|${year}-${month}-${day} ${hrs}:${min}:${sec}|;
    return ($CURTIME);
}
############################################################################
