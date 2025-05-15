#!/usr/bin/perl
use lib 'C:/xampp/htdocs/src/lib';
use DBI;
use myForm;
use myDBI;
use SysAccess;
use myConfig;
use myHTML;
use File::stat;

############################################################################
my $form = myForm->new();
my $dbh  = myDBI->dbconnect( $form->{'DBNAME'} );
my $type = $form->{'type'};

unless ( SysAccess->chkPriv( $form, 'Agent' ) ) {
    myDBI->error("Access Denied! (List ${type} Electronic Files)");
}

my $typename =
    $type eq '837' ? 'Billing'
  : $type eq '835' ? 'Remittances'
  : $type eq '271' ? 'Eligibility'
  :                  'Unknown';
my $desc = $type eq '837'
  ? qq|
<P CLASS="indent1" >
Billing Files (837) are generated automatically at 5pm each Monday.
 They complete about 8pm.
</P>

<P CLASS="indent1" >
The 837 file for Medicaid is to be UPLOADED to OHCA each Tuesday morning.
 It will will be listed under the <U>Transfer Files</U> for <U>Billing</U>.
 Download the medicaid*.837 file to your computer.
</P>

<P CLASS="indent1" >
<DIV CLASS="indent" >Using IE, log into OHCA User ID: <U>ohcamis</U></DIV>
<DIV CLASS="indent" >and under the Files Exchange->Upload Files and upload our 837 as </DIV>
<DIV CLASS="indent" >Transaction Type: <U>Claim Submission - Prof</U></DIV>
</P>

<P CLASS="indent1" >
After a few hours OHCA will process the file and return a '999' file which will show the errors, if any.
<P CLASS="indent1" >
Download the '999' file from Files Exchanges->Download Files.
  Unzip the file and upload it here.
  Examine the file using the 'Response & Log files' Billing option.
  Anything other than an AK1,AK2 or AK9 will be an error, such as IK3, CLX or IK4.
  The Transaction ID and the Rejected Segments will be listed in the report.
</P>

<P CLASS="indent1" >
IF ANY Rejects call OHCA EDI (405-522-6205,#,1,200129170*21,,2,2) with the Transaction ID of the uploaded file 
<BR>from the -report-
<BR>OR from the -second part of the file name (i.e.: 1234567 of filename: w.<U>1234567</U>.50000008.999.rsp)-
<BR>OR from the -Upload Files->Search on the OHCA website where you downloaded the file-.
</P>

<P CLASS="indent1" >
All other Insurance 837 files generated are automatically uploaded to availity or officeally Monday night. You can check them from those sites. ANY uploaded file to OHCA will have a returned '999' file.
</P>

<P CLASS="indent1" >
|
  : $type eq '835' ? qq|
<P CLASS="indent1" >
Remittance files are automatically downloaded from Availity and OfficeAlly on Sun 10am, Mon 11pm and Wed 10am. 
</P>

<P CLASS="indent1" >
All insurances except for the OHCA Medicaid insurance. It will have to be downloaded by logging into OHCA (ohcamis)
</P>

<P CLASS="indent1" > Once downloaded then upload the file to MIS via the Remittances Transfer Files option.
</P>

<P CLASS="indent1" >
Once the 835 files are downloaded from OHCA and via Availity and OfficeAlly you can use the Process 835 Remittance Files option.
</P>

<P></P>
|
  : $type eq '271' ? qq|
<P CLASS="indent1" >
Eligibility Files (270) are generated automatically at 8am each 14th and 28th of the month.
 The 14th run generates for the current month, the 28th run generates for the next month.
 The <U>Process 271 Eligibility Files</U> will process for the 'last' run (see 'daterange.out' file).

<P CLASS="indent1" >
The 270 file for Medicaid Eligibility is to be UPLOADED to OHCA when generated. 
 It will will be listed under the <U>Transfer Files</U> for <U>Eligibility</U>.
 Download the medicaid*.270 file to your computer. 

<P CLASS="indent1" >
Using IE, log into OHCA and under the Files Exchange->Upload Files upload our 270 as 'Transaction Type: Eligibility Inquiry'.

<P CLASS="indent1" >
After a few hours OHCA will process the file and return a '271' file.
 Download and unzip  the '271' file from Files Exchanges->Download Files.
 Upload the '271' file to MIS using the Eligibility->Transfer Files.
 Then run the Process 271 Eligibility Files.

<P CLASS="indent1" >
 You can download and look at the '999' file from Files Exchanges->Download Files which will show any errors, if any, if you'd like but the '271' is what you need.
 Unzip the file and open it to see the errors.
 Anything other than an AK1,AK2 or AK9 will be an error, such as IK3 or IK4.

<P CLASS="indent1" >
Call OHCA EDI (405-522-6205,#,1,200129170*21,,2,2) with the transaction ID if the '270' file has errors. It will be the 6 digit listed in the Upload Files->Search OR the 6 digits of the first part of the '999' you looked at for the errors.
|
  : 'Unknown';

############################################################################
my $CloseButton =
qq|<INPUT TYPE="button" NAME="close" VALUE="close" ONCLICK="javascript: window.close()" >|;

my $html = myHTML->newHTML(
    $form,
    'Generate Job/File Panel',
    'CheckPopupWindow noclock countdown_10'
  )
  . qq|
<P>
<P>
<SCRIPT LANGUAGE="JavaScript" SRC="/src/cgi/js/novalidate.js"> </SCRIPT>
<DIV CLASS="home title strcol" >
${desc}
</DIV>
<FORM NAME="adminFiles" ACTION="/cgi/bin/mis.cgi" METHOD="POST" >
| . main->listJobs($type) . qq|
<INPUT TYPE="hidden" NAME="mlt" VALUE="$form->{mlt}" >
<INPUT TYPE="hidden" NAME="misLINKS" VALUE="$form->{misLINKS}" >
<INPUT TYPE="hidden" NAME="LINKID" VALUE="$form->{LINKID}" >
</FORM>

</BODY>
</HTML>
|;

myDBI->cleanup();
print $html;
exit;
############################################################################
sub listJobs {
    my ( $self, $type ) = @_;
    my $html =
        $type eq '837' ? main->gen837()
      : $type eq '835' ? main->gen835()
      : $type eq '271' ? main->gen271()
      :                  'Unknown';
    return ($html);
}
#####################################################################
sub gen837 {
    my ($self) = @_;
    my $html = '';
    $html .= qq|
<P>
<P>
|;
    return ($html);
}
#####################################################################
sub gen835 {
    my ($self) = @_;
    my $html = '';
    $html .= qq|
<P>
<P>
|;
    return ($html);
}
#####################################################################
sub gen271 {
    my ($self) = @_;
    my $html = '';
    $html .= qq|
<P>
<P>
|;
    return ($html);
}
#####################################################################
