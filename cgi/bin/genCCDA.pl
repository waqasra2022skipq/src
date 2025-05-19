#!/usr/bin/perl
use lib 'C:/xampp/htdocs/src/lib';
use Cwd;
use DBI;
use DBForm;
use DBA;
use myHTML;
use gXML;
use XML::LibXSLT;
use XML::LibXML;
binmode STDOUT, ":utf8";

############################################################################
# usage:
#        to create files: Visit_[trid].xml, CCDA_Visit_[trid].xml
#        to create files: Referral_[trid].xml, CCDA_Referral_[trid].xml
#        for sending (sendCCDA.cgi) to phimail
############################################################################
my $form = DBForm->new();
my $dbh  = $form->dbconnect();
foreach my $f ( sort keys %{$form} ) { warn ": form-$f=$form->{$f}\n"; }
my $ProvID   = $form->{'ProvID'};
my $ClientID = $form->{'ClientID'};
my $TrID     = $form->{'TrIDs'};
my $Agent    = SysAccess->verify( $form, 'Privilege=Agent' );
unless ($Agent) { $form->error("Page DENIED!"); }
##
# first generate the XML file...
my $xml = qq|<?xml version="1.0" encoding="utf-8"?>\n|
  . gXML->setXML( $form, $ProvID, $ClientID, $TrID, '', '', 'CCDA nonulls' );

#$form->{'MEASUREID'} = 2; my $xml = qq|<?xml version="1.0" encoding="utf-8"?>\n|.gXML->setXML($form,$ProvID,$ClientID,'','2017-07-01','2017-09-31','QRDA nonulls');
my $xmlfile = qq|/tmp/XML_${TrID}.xml|;
my $xmlpath = qq|$form->{DOCROOT}${xmlfile}|;
open( XML, ">", $xmlpath ) || die "Couldn't open '${xmlpath}' file: $!";
print XML $xml;
close(XML);

# next the generate Visit CCDA file...
my $visitout  = gXML->styleCCDA( $form, $xmlfile, 'Visit' );
my $visitfile = qq|/tmp/CCDA_${TrID}_Visit.xml|;
warn qq|genCCDA: visitfile=${visitfile}\n|;
my $visitpath = qq|$form->{DOCROOT}${visitfile}|;
warn qq|genCCDA: visitpath=${visitpath}\n|;
open( OUT, ">:encoding(UTF-8)", $visitpath )
  || die "Couldn't open '${visitpath}' file: $!";
print OUT $visitout;
close(OUT);

# next the generate Referral CCDA file...
my $referralout  = gXML->styleCCDA( $form, $xmlfile, 'Referral' );
my $referralfile = qq|/tmp/CCDA_${TrID}_Referral.xml|;
warn qq|genCCDA: referralfile=${referralfile}\n|;
my $referralpath = qq|$form->{DOCROOT}${referralfile}|;
warn qq|genCCDA: referralpath=${referralpath}\n|;
open( OUT, ">:encoding(UTF-8)", $referralpath )
  || die "Couldn't open '${referralpath}' file: $!";
print OUT $referralout;
close(OUT);

### next the generate QRDA file...
##  my $qrdavisitout = gXML->styleQRDA($form,$xmlfile);
##  my $qrdavisitfile = qq|/tmp/QRDA_${TrID}.xml|;
##warn qq|genCCDA: qrdavisitfile=${qrdavisitfile}\n|;
##  my $qrdavisitpath = qq|$form->{DOCROOT}${qrdavisitfile}|;
##warn qq|genCCDA: qrdavisitpath=${qrdavisitpath}\n|;
##  open(OUT, ">:encoding(UTF-8)", $qrdavisitpath) || die "Couldn't open '${qrdavisitpath}' file: $!";
##  print OUT $qrdavisitout;
##  close(OUT);
##  my $qrdahtml = qq|
##<TABLE CLASS="home fullsize" >
##  <TR>
##    <TD CLASS="strcol" >
##      <A HREF="javascript:ReportWindow('${qrdavisitfile}','VisitFile')" >click to display QRDA</A>
##    </TD>
##  </TR>
##</TABLE>|;

# next the generate Visit CDA file...
my $cdavisit     = gXML->styleCDA( $form, $visitfile );
my $cdavisitfile = qq|/tmp/CDA_${TrID}_Visit.htm|;
warn qq|genCCDA: cdavisitfile=${cdavisitfile}\n|;
my $cdavisitpath = qq|$form->{DOCROOT}$cdavisitfile|;
warn qq|genCCDA: cdavisitpath=${cdavisitpath}\n|;
open( OUT, ">:encoding(UTF-8)", $cdavisitpath )
  || die "Couldn't open '${cdavisitpath}' file: $!";
print OUT $cdavisit;
close(OUT);

# next the generate Referral CDA file...
my $cdareferral     = gXML->styleCDA( $form, $referralfile );
my $cdareferralfile = qq|/tmp/CDA_${TrID}_Referral.htm|;
warn qq|genCCDA: cdareferralfile=${cdareferralfile}\n|;
my $cdareferralpath = qq|$form->{DOCROOT}$cdareferralfile|;
warn qq|genCCDA: cdareferralpath=${cdareferralpath}\n|;
open( OUT, ">:encoding(UTF-8)", $cdareferralpath )
  || die "Couldn't open '${cdareferralpath}' file: $!";
print OUT $cdareferral;
close(OUT);
##
# now output the html screen to select the created documents...
my $html =
  myHTML->newHTML( $form, 'Send CCDA', 'CheckPopupWindow noclock countdown_1' )
  . qq|
<SCRIPT LANGUAGE="JavaScript" >
function validate(form)
{
  return true;
}
</SCRIPT>

<TABLE CLASS="main" >
  <TR> <TD CLASS="hdrcol title" >Send CCDA</TD> </TR>
</TABLE>
<FORM NAME="EmailVisit" ACTION="/src/cgi/bin/sendCCDA.cgi" METHOD="POST" >
<TABLE CLASS="home fullsize" >
  <TR>
    <TD CLASS="strcol" >
      To:
      <SELECT NAME="To" >|
  . DBA->selxTable(
    $form, 'xPhiEmails',
    'wellformed1@ttpedge.sitenv.org',
    'Email Purpose',
    '', 'Email'
  )
  . qq|      </SELECT>
    </TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="submit" ONCLICK="return validate(this.form);" VALUE="Send Visit CCDA">
    </TD>
  </TR>
</TABLE>
<TABLE CLASS="home fullsize" >
  <TR>
    <TD CLASS="strcol" >
      <A HREF="javascript:ReportWindow('${cdavisitfile}','VisitFile')" >click to display Visit CDA</A>
    </TD>
  </TR>
</TABLE>
  
<INPUT TYPE="hidden" NAME="sendfile" VALUE="${visitpath}">
<INPUT TYPE="hidden" NAME="mlt" VALUE="$form->{mlt}">
</FORM>

<FORM NAME="EmailReferral" ACTION="/src/cgi/bin/sendCCDA.cgi" METHOD="POST" >
<TABLE CLASS="home fullsize" >
  <TR>
    <TD CLASS="strcol" >
      To:
      <SELECT NAME="To" >|
  . DBA->selxTable(
    $form, 'xPhiEmails',
    'wellformed1@ttpedge.sitenv.org',
    'Email Purpose',
    '', 'Email'
  )
  . qq|      </SELECT>
    </TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="submit" ONCLICK="return validate(this.form);" VALUE="Send Referral CCDA">
    </TD>
  </TR>
</TABLE>
<TABLE CLASS="home fullsize" >
  <TR>
    <TD CLASS="strcol" >
      <A HREF="javascript:ReportWindow('${cdareferralfile}','ReferralFile')" >click to display Referral CDA</A>
    </TD>
  </TR>
</TABLE>
  
<INPUT TYPE="hidden" NAME="sendfile" VALUE="${referralpath}">
<INPUT TYPE="hidden" NAME="mlt" VALUE="$form->{mlt}">
</FORM>
    </TD>
  </TR>
</TABLE>
<BR><BR><BR><BR><BR><BR><BR><BR><BR><BR><BR><BR>
</BODY>
</HTML>
|;
print $html;
$form->complete();
exit;
############################################################################
# html for other 2 files generate to be put on screen
#      <BR>
#      <A HREF="${visitfile}" >right click to save ccda file</A>
#      <BR>
#      <A HREF="${xmlfile}" >right click to save xml file</A>
