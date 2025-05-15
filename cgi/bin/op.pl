#!/usr/bin/perl
#############################################################################
use lib 'C:/xampp/htdocs/src/lib';
use DBI;
use myForm;
use DBA;
use SysAccess;
use DBUtil;
use utils;
use graphs;
use Time::Local;
my $DT = localtime();

#############################################################################
my $form   = myForm->parse();
my $method = $form->{'method'};
my $value  = $form->{'value'};
my $target = $form->{'target'};
##$form->{'sesid'} = $form->{'s'};
$form = utils->readsid($form);
my $graphtype = $form->{'method'};    # graphtype comes from sesid file.

#foreach my $f ( sort keys %{$form} ) { warn "options: form-$f=$form->{$f}\n"; }
#warn qq|op.pl: graphtype=${graphtype}\n|;
if ( $method eq 'test' ) {

    #warn qq|op.pl: test: target=${target}, value=${value}\n|;
    my $html = qq|
<SCRIPT TYPE="text/javascript" >
alert("this is the NEW test");
</SCRIPT>
|;
    my $ex = qq|javascript:execute_script('grapharea');|;

    #warn qq|op.pl: html=\n${html}\n|;
    $out = $err eq ''
      ? qq|
  <command method="setcontent">
    <target>${target}</target>
    <content><![CDATA[${html}]]></content>
  </command>
  <command method="setscript">
    <target>execute_script</target>
    <content><![CDATA[${ex}]]></content>
  </command>
|
      : main->ierr( $target, $err, $msg, $id );
    $out .= main->iwarn( $warn, $msg, $id );
}
elsif ( $method eq 'ClinicProvider' ) {

    #warn qq|op.pl: ClinicProvider: target=${target}, value=${value}\n|;
    my $html = main->selections('ClinicIDs:ProvIDs');

    #warn qq|op.pl: html=\n${html}\n|;
    #my $ex = qq|javascript:execute_script('optionsarea');|;
    #<command method="setscript">
    #  <target>execute_script</target>
    #  <content><![CDATA[${ex}]]></content>
    #</command>
    $out = $err eq ''
      ? qq|
  <command method="setcontent">
    <target>${target}</target>
    <content><![CDATA[${html}]]></content>
  </command>
|
      : main->ierr( $target, $err, $msg, $id );
    $out .= main->iwarn( $warn, $msg, $id );
}
else {
    #warn qq|op.pl: else: target=${target}, value=${value}\n|;
    #warn qq|op.pl: else: method=${method}\n|;
    my $html = main->selections($method);

    #warn qq|op.pl: html=\n${html}\n|;
    $out = $err eq ''
      ? qq|
  <command method="setcontent">
    <target>${target}</target>
    <content><![CDATA[${html}]]></content>
  </command>
|
      : main->ierr( $target, $err, $msg, $id );
    $out .= main->iwarn( $warn, $msg, $id );
}
$xml = qq|<response>\n${out}</response>|;
myDBI->cleanup();

#warn qq|graphs: xml=${xml}\n|;
print qq|Content-type: text/xml

<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
${xml}
|;
exit;
############################################################################
sub selections {
    my ( $self, $requested_options ) = @_;

    #warn qq|options: check: $form->{Name}\n|;
    my ( $html, $my_options, $section ) = ( '', '', '' );
    my $args = qq|'&mlt=$form->{mlt}&sesid=$form->{sesid}'|;
    foreach my $option ( split( ':', $requested_options ) ) {
        $args .= qq|+'|;
        if    ( $option eq 'Active' )     { $section = main->setActive(); }
        elsif ( $option eq 'Days' )       { $section = main->setDays(); }
        elsif ( $option eq 'CustAgency' ) { $section = main->setCustAgency(); }
        elsif ( $option eq 'ClinicIDs' )  { $section = main->setClinicIDs(); }
        elsif ( $option eq 'daterange' )  { $section = main->setDates(); }
        elsif ( $option eq 'Format' )     { $section = main->setFormat(); }
        elsif ( $option eq 'InsIDs' )     { $section = main->setInsIDs(); }
        elsif ( $option eq 'ProvIDs' )    { $section = main->setProvIDs(); }
        elsif ( $option eq 'sYearMonth' ) { $section = main->setsYearMonth(); }
        $my_options .= qq|
<TABLE CLASS="home hdrcol" >
  <TR CLASS="subtitle tophdr" ><TD >${opt}</TD</TR>
  <TR>
${section}
  </TR>
</TABLE >
|;
        $args .= qq|&${option}='+document.theoptions.${option}.value|;
    }
    $html = qq|
<FORM ID="theoptions" NAME="theoptions" METHOD="POST" >
${my_options}
<DIV ><INPUT TYPE="button" ONCLICK="return validate(this.form);" VALUE="reset" /> </DIV>
<INPUT TYPE="hidden" NAME="sesid" VALUE="$form->{'sesid'}" >
</FORM>
|;
    return ($html);
}

sub setActive {
    my ($self)  = @_;
    my $checked = $form->{Active} ? 'CHECKED' : '';
    my $html    = qq|
    <TD >Active only: <INPUT TYPE="checkbox" NAME="Active" VALUE="1" ${checked}></TD >
|;
    return ($html);
}

sub setDays {
    my ($self) = @_;
    my $html = qq|
    <TD >Days: <INPUT TYPE="text" NAME="Days" VALUE="$form->{Days}" ONFOCUS="select()" ONCHANGE="return vNum(this,1,1000)" SIZE=12 ></TD >
|;
    return ($html);
}

sub setClinicIDs {
    my ($self) = @_;
    my $ListClinics =
      gHTML->selClinics( $form, $form->{LOGINPROVID}, $form->{ClinicIDs} );
    my $html = qq|
    <TD CLASS="numcol" >Clinics:</TD><TD><SELECT NAME="ClinicIDs" MULTIPLE SIZE="5" >${ListClinics}</SELECT></TD >
|;
    return ($html);
}

sub setProvIDs {
    my ($self) = @_;
    my $ListProviders =
      gHTML->selProviders( $form, $form->{LOGINPROVID}, $form->{ProvIDs} );
    my $html = qq|
    <TD CLASS="numcol" >Providers:</TD><TD><SELECT NAME="ProvIDs" MULTIPLE SIZE="5" >${ListProviders}</SELECT></TD >
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
|;
    return ($html);
}

sub setInsIDs {
    my ($self) = @_;
    my $html = qq|
  <TR>
    <TD >Insurance:</TD>
    <TD>
      <SELECT NAME="InsIDs" >
| . DBA->selInsurance( $form, $form->{InsIDs} ) . qq|
      </SELECT>
    </TD>
  </TR>
|;
    return ($html);
}

sub setCustAgency {
    my ($self)   = @_;
    my $CustList = DBA->selxTable( $form, 'xCustAgency', $form->{CustAgency} );
    my $html     = qq|
    <TD >Custody Agency: <SELECT NAME="CustAgency" >${CustList}</SELECT></TD >
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
        <LI><INPUT TYPE="radio" NAME="daterange" VALUE="last3m" ${last3m} >Last 3 Months</LI>
        <LI><INPUT TYPE="radio" NAME="daterange" VALUE="last6m" ${last6m} >Last 6 Months</LI>
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

sub setOutput {
    my ($self) = @_;
    my $html, $OutputTypes, $cnt = 0;
    if    ( $form->{output} =~ /html/i )  { $out1 = 'CHECKED'; }
    elsif ( $form->{output} =~ /ss/i )    { $out2 = 'CHECKED'; }
    elsif ( $form->{output} =~ /pdf/i )   { $out3 = 'CHECKED'; }
    elsif ( $form->{output} =~ /graph/i ) { $out4 = 'CHECKED'; }
    else                                  { $out1 = 'CHECKED'; }
    if ( $rxTable->{Outputs} =~ /html/ ) {
        $cnt++;
        $OutputTypes .=
qq|        <LI><INPUT TYPE="radio" NAME="output" VALUE="html" ${out1} > html</LI>|;
    }
    if ( $rxTable->{Outputs} =~ /ss/ ) {
        $cnt++;
        $OutputTypes .=
qq|        <LI><INPUT TYPE="radio" NAME="output" VALUE="ss" ${out2} > SpreadSheet</LI>|;
    }
    if ( $rxTable->{Outputs} =~ /pdf/ ) {
        $cnt++;
        $OutputTypes .=
qq|        <LI><INPUT TYPE="radio" NAME="output" VALUE="pdf" ${out3} > pdf</LI>|;
    }
    if ( $rxTable->{Outputs} =~ /graph/ ) {
        $cnt++;
        $OutputTypes .=
qq|        <LI><INPUT TYPE="radio" NAME="output" VALUE="graph" ${out4} > graph</LI>|;
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
############################################################################
sub imsg {
    my ( $self, $msg, $id ) = @_;
    return ('') if ( $msg eq '' );
    my $out = qq|
  <command method="setcontent">
    <target>${id}</target>
    <content>${msg}</content>
  </command>
|;
    return ($out);
}

sub iwarn {
    my ( $self, $warn, $msg, $id ) = @_;
    return ('') if ( $warn eq '' );
    my $out = qq|
  <command method="alert">
    <message>${warn}</message>
  </command>
|;
    $out .= main->imsg( $msg, $id ) if ( $id ne '' );
    return ($out);
}

sub ierr {
    my ( $self, $target, $err, $msg, $id ) = @_;
    my $out = qq|
  <command method="setdefault">
    <target>${target}</target>
  </command>
  <command method="alert">
    <message>${err}</message>
  </command>
  <command method="focus">
    <target>${target}</target>
  </command>
|;
    $out .= main->imsg( $msg, $id ) if ( $id ne '' );
    return ($out);
}
############################################################################
############################################################################
############################################################################
############################################################################
############################################################################
############################################################################
#if ( $form->{submit} )
#{
#  # save to incoming sesid...
#  $form = utils->writesid($form,$form->{'sesid'});
#  $html = main->done();
#}
#else
#{
#  $form->{'sesid'} = $form->{'s'};
#  $form = utils->readsid($form);
#  $html = main->selections();
#}
############################################################################
