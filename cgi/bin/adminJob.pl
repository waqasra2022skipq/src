#!/usr/bin/perl
############################################################################
use lib '/var/www/okmis/src/lib';
use DBI;
use myForm;
use myDBI;
use myHTML;
use DBUtil;
use Cwd;
use Time::Local;

############################################################################
my $form = myForm->new();
my $dbh  = myDBI->dbconnect( $form->{'DBNAME'} );
unless ( SysAccess->chkPriv( $form, 'Agent' ) ) {
    myDBI->error("Access Denied / Not Found!");
}

#foreach my $f ( sort keys %{$form} ) { warn ": form-$f=$form->{$f}\n"; }

my $type = $form->{'type'};
if ( $type eq '' ) { myDBI->error("type ERROR / NULL!"); }
my $job = $form->{'job'};
if ( $job eq '' ) { myDBI->error("job ERROR / NULL!"); }

my $ADMINDIR = myConfig->cfg('ADMINDIR');
my $dirpath  = qq|${ADMINDIR}/${type}|;
chdir($dirpath);
my $pwd = cwd();

my $typename =
    $type eq '837' ? 'Billing'
  : $type eq '835' ? 'Remittances'
  : $type eq '271' ? 'Eligibility'
  :                  'Unknown';
my $SRCBIN = myConfig->cfg('SRCBIN');
my $cmd =
    $type eq '837' && $job =~ /process/i ? qq|${SRCBIN}/Pro837|
  : $type eq '835' && $job =~ /process/i ? qq|${SRCBIN}/Pro835|
  : $type eq '271' && $job =~ /process/i ? qq|${SRCBIN}/Pro271|
  :                                        'Unknown';
my $stamp   = DBUtil->Date( 'today', 'fmt', 'YYYYMMDD' );
my $outfile = $job . $type . '_' . $stamp . '.log';

my $html = myHTML->close( 1, $form->{'mlt'} );
if    ( $form->{submit} ) { $html = main->submit(); }
elsif ( $form->{status} ) { $html = main->status(); }
else                      { $html = main->verify(); }

myDBI->cleanup();
print $html;
exit;
############################################################################
sub submit {
    my ($self) = @_;
    system(
"${cmd} DBNAME=$form->{'DBNAME'}\\&mlt=$form->{'mlt'} > ${outfile} 2>${outfile} &"
    );
    sleep 4;
    my $outtext = DBUtil->ReadFile($outfile);
    my $results = $outtext eq '' ? 'Job still running; check log file' : '';
    my $html    = myHTML->newHTML(
        $form,
        "${type}: ${job}",
        'CheckPopupWindow noclock countdown_10'
      )
      . qq|
<P>
<P>
<SCRIPT LANGUAGE="JavaScript" SRC="/cgi/js/novalidate.js"> </SCRIPT>
<FORM NAME="submit" ACTION="/cgi/bin/adminJob.pl" METHOD="POST">
<DIV CLASS="strcol" >
JOB executed ${typename}: ${job}
Results:
<PRE>
${results}
${outtext}
</PRE>
</DIV>
<P>
<DIV CLASS="strcol" >
  <INPUT TYPE="submit" ONCLICK="return validate(this.form);" NAME="status" VALUE="status" >
  <INPUT TYPE="button" NAME="close" VALUE="close" ONCLICK="javascript: window.close()" >
</DIV>
  <INPUT TYPE="hidden" NAME="type" VALUE="${type}" >
  <INPUT TYPE="hidden" NAME="job" VALUE="${job}" >
  <INPUT TYPE="hidden" NAME="mlt" VALUE="$form->{mlt}" >
  <INPUT TYPE="hidden" NAME="misLINKS" VALUE="$form->{misLINKS}" >
  <INPUT TYPE="hidden" NAME="FORMID" VALUE="$form->{FORMID}" >
</FORM>
</BODY>
</HTML>
|;
    return ($html);
}

sub status {
    my ($self)  = @_;
    my $outtext = DBUtil->ReadFile($outfile);
    my $results = $outtext eq '' ? 'Job still running; check log file' : '';
    my $html    = myHTML->newHTML(
        $form,
        "${type}: ${job}",
        'CheckPopupWindow noclock countdown_10'
      )
      . qq|
<P>
<P>
<SCRIPT LANGUAGE="JavaScript" SRC="/cgi/js/novalidate.js"> </SCRIPT>
<FORM NAME="submit" ACTION="/cgi/bin/adminJob.pl" METHOD="POST">
<DIV CLASS="strcol" >
JOB status ${typename}: ${job}
Results:
<PRE>
${results}
${outtext}
</PRE>
</DIV>
<P>
<DIV CLASS="strcol" >
  <INPUT TYPE="submit" ONCLICK="return validate(this.form);" NAME="status" VALUE="status" >
  <INPUT TYPE="button" NAME="close" VALUE="close" ONCLICK="javascript: window.close()" >
</DIV>
  <INPUT TYPE="hidden" NAME="type" VALUE="${type}" >
  <INPUT TYPE="hidden" NAME="job" VALUE="${job}" >
  <INPUT TYPE="hidden" NAME="mlt" VALUE="$form->{mlt}" >
  <INPUT TYPE="hidden" NAME="misLINKS" VALUE="$form->{misLINKS}" >
  <INPUT TYPE="hidden" NAME="FORMID" VALUE="$form->{FORMID}" >
</FORM>
</BODY>
</HTML>
|;
    return ($html);
}

sub verify {
    my ($self) = @_;
    my $html = myHTML->newHTML(
        $form,
        "${type}: ${job}",
        'CheckPopupWindow noclock countdown_10'
      )
      . qq|
<P>
<P>
<SCRIPT LANGUAGE="JavaScript" SRC="/cgi/js/novalidate.js"> </SCRIPT>
<FORM NAME="submit" ACTION="/cgi/bin/adminJob.pl" METHOD="POST">
<DIV CLASS="strcol" >
  Do you want to execute JOB ${typename}: ${job}
</DIV>
<P>
<DIV CLASS="strcol" >
  <INPUT TYPE="submit" ONCLICK="return validate(this.form);" NAME="submit" VALUE="submit" >
  <INPUT TYPE="button" NAME="cancel" VALUE="cancel" ONCLICK="javascript: window.close()" >
</DIV>
  <INPUT TYPE="hidden" NAME="type" VALUE="${type}" >
  <INPUT TYPE="hidden" NAME="job" VALUE="${job}" >
  <INPUT TYPE="hidden" NAME="mlt" VALUE="$form->{mlt}" >
  <INPUT TYPE="hidden" NAME="misLINKS" VALUE="$form->{misLINKS}" >
  <INPUT TYPE="hidden" NAME="FORMID" VALUE="$form->{FORMID}" >
</FORM>
</BODY>
</HTML>
|;
    return ($html);
}
############################################################################
