#!/usr/bin/perl
use lib '/home/okmis/mis/src/lib';
use myConfig;
use Cwd;
use DBI;
use DBForm;
use SysAccess;
use DBA;
use DBUtil;
use myHTML;
use gHTML;

############################################################################
my $form = DBForm->new();
chdir("$form->{DOCROOT}/tmp");
$pwd=cwd();
warn "ListMISEmails: update: pwd=$pwd\n";
my $dbh = $form->connectdb('okmis_config');
if ( ! SysAccess->verify($form,'Privilege=Agent') )
{ $form->error("Agent Access / Not Found!"); }

############################################################################
foreach my $f ( sort keys %{$form} ) { warn "ListMISEmails: form-$f=$form->{$f}\n"; }
if    ( $form->{update} )   { print main->update(); }
elsif ( $form->{viewedit} ) { print main->viewedit(); }
else                        { print main->list(); }
$form->complete();
exit;

############################################################################
sub viewedit()
{
warn qq|viewedit: ID=$form->{ID}\n|;
  my $rEmail = ();
  my $qEmail = qq|select * from MISEmails where ID=?|;
  $sEmail=$dbh->prepare($qEmail);
  $sEmail->execute($form->{'ID'});
  $rEmail = $sEmail->fetchrow_hashref;
  #$form->error("MISEmails->${ID} Not Found!") if ( $rEmail->{'ID'} eq '' );
  my $html = myHTML->new($form) . qq|
<SCRIPT LANGUAGE="JavaScript" SRC="/cgi/js/NoEnter.js"> </SCRIPT>
<SCRIPT LANGUAGE="JavaScript" SRC="/cgi/js/vEntry.js"> </SCRIPT>
<SCRIPT LANGUAGE="JavaScript">
function validate(form)
{
  return vEntry("notnull",form.SUBJ
                         ,form.MSG
               );
}
</SCRIPT>
<FORM NAME="MISEmail" ACTION="/cgi/bin/ListMISEmails.cgi" METHOD="POST" >
<TABLE CLASS="main fullsize" >
  <TR >
    <TD CLASS="strcol" >
      Global MIS Email Entry Screen
    </TD>
  </TR>
</TABLE>
<TABLE CLASS="home fullsize" >
  <TR >
    <TD CLASS="port hdrtxt" COLSPAN="2" >
      Enter your Subject and Message
    </TD>
  </TR>
  <TR >
    <TD CLASS="strcol" >Subject</TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="text" NAME="SUBJ" VALUE="$rEmail->{'SUBJ'}" ONFOCUS="select()" SIZE="80" >
    </TD>
  </TR>
  <TR >
    <TD CLASS="strcol" >Message</TD>
    <TD CLASS="strcol" >
      <TEXTAREA NAME="MSG" COLS="80" ROWS="22" WRAP="virtual" ONFOCUS="select()" >$rEmail->{'MSG'}</TEXTAREA>
    </TD>
  </TR>
</TABLE>

<TABLE CLASS="main fullsize" >
  <TR >
    <TD CLASS="numcol" >
      <INPUT TYPE="submit" ONCLICK="return vDELETE('Are you sure you want to delete this email?');" NAME="update=1&delete=1" VALUE="Delete" >
      <INPUT TYPE="submit" ONCLICK="return validate(this.form);" NAME="update=1&email=1" VALUE="Add/Update/Email">
      <INPUT TYPE="submit" ONCLICK="return validate(this.form);" NAME="update=1" VALUE="Add/Update">
    </TD>
  </TR>
</TABLE>

<INPUT TYPE="hidden" NAME="ID" VALUE="$rEmail->{'ID'}" >
<INPUT TYPE="hidden" NAME="mlt" VALUE="$form->{'mlt'}" >
<INPUT TYPE="hidden" NAME="FORMID" VALUE="$form->{'FORMID'}" >
<INPUT TYPE="hidden" NAME="LINKID" VALUE="$form->{'LINKID'}" >
<INPUT TYPE="hidden" NAME="misLINKS" VALUE="$form->{'misLINKS'}" >
</FORM>
<SCRIPT LANGUAGE="JavaScript">
document.MISEmail.elements[0].focus();
</SCRIPT>
</BODY>
</HTML>
|;
  return($html);
}
sub update()
{
  my $ID = $form->{'ID'};
  my ($q,$out) = ('','');
  my $r = ();
  $r->{'ChangeProvID'} = $form->{'LOGINPROVID'};
  $r->{SUBJ} = $form->{'SUBJ'};
  $r->{MSG} = $form->{'MSG'};
  $r->{'SentDate'} = $form->{'TODAY'} if ( $form->{'email'} );
  if ( $ID )
  {
    if ( $form->{'delete'} )
    { $q = qq|delete from MISEmails where ID='${ID}'|; }
    else
    {
      $r->{ID} = $ID;
      $q = DBA->genUpdate($form,'MISEmails',$r,'ID');
    }
  }
  else
  {
    $r->{'CreateDate'} = $form->{'TODAY'};
    $r->{'CreateProvID'} = $form->{'LOGINPROVID'};
    $q = DBA->genInsert($form,'MISEmails',$r);
  }
warn qq|q=$q\n|;
  $s=$dbh->prepare($q);
  $s->execute();
  if ( $form->{'email'} )
  {
    my $outfile = DBUtil->ExecCmd("/home/okmis/mis/src/reports/MISEmail ${ID}");
    $out = DBUtil->ReadFile($outfile);
  }
  return(main->list($out));
}
sub list()
{
  my ($self,$text) = @_;
  my $Title = qq|MIS Emails Listing|;
  my $Hdr = qq|Emails listed with a SentDate were sent Globally on that date. Those without a SentDate have been entered but not yet sent. To send those or to resend a message to all MIS providers across all data sites, View/Edit the message and click on the Add/Update/Email button.|;
  my $html = myHTML->new($form) . qq|
<SCRIPT LANGUAGE="JavaScript" SRC="/cgi/js/NoEnter.js"> </SCRIPT>
<SCRIPT LANGUAGE="JavaScript" SRC="/cgi/js/vEntry.js"> </SCRIPT>
<SCRIPT LANGUAGE="JavaScript" >function validate(form) { return(1); }</SCRIPT>

<FORM NAME="MISEmails" ACTION="/cgi/bin/ListMISEmails.cgi" METHOD="POST" >
<DIV CLASS="main header" >Millennium Information Services Global Emails</DIV>
<HR WIDTH="90%" >
<TABLE CLASS="port fullsize" >
  <TR ><TD CLASS="header" >${Title}</TD></TR>
  <TR ><TD CLASS="title" >${Hdr}</TD></TR>
</TABLE>
<TABLE CLASS="home fullsize" >
  <TR CLASS="port" >
    <TH ALIGN="left" >SentDate</TH>
    <TH ALIGN="left" >Subject</TH>
    <TH ALIGN="left" >Created</TH>
    <TH ALIGN="left" >By</TH>
    <TH ALIGN="center" >&nbsp;
      <INPUT TYPE="submit" ONCLICK="return validate(this.form);" NAME="viewedit=1&ID=" VALUE="Add New Message">
    </TH>
  </TR >
|; 

#============================================================================
  my $qEmails = qq|select * from MISEmails order by SentDate desc|;
  my $cnt = 0;
  $sEmails=$dbh->prepare($qEmails);
  $sEmails->execute();
  while (my $rEmails = $sEmails->fetchrow_hashref)
  {
    $cnt+=1;
    $even = int($cnt/2) == $cnt/2 ? '1' : '0';
    my $class = qq|rptodd|;
    if ( $even ) { $class = qq|rpteven|; }
    my $SentDate = DBUtil->Date($rEmails->{SentDate},'fmt','MM/DD/YYYY');
    my $CreateDate = DBUtil->Date($rEmails->{CreateDate},'fmt','MM/DD/YYYY');
    my $ProvName = DBA->getxref($form,'Provider',$rEmails->{CreateProvID},'LName');
    $html .= qq|  <TR CLASS="${class}" >\n|;
    $html .= qq|    <TD ALIGN="left" >${SentDate} &nbsp;</TD>\n|;
    $html .= qq|    <TD ALIGN="left" >$rEmails->{SUBJ} &nbsp;</TD>\n|;
    $html .= qq|    <TD ALIGN="left" >${CreateDate} &nbsp;</TD>\n|;
    $html .= qq|    <TD ALIGN="left" >${ProvName} &nbsp;</TD>\n|;
    $html .= qq|    <TD ALIGN="center" ><INPUT TYPE="submit" ONCLICK="return validate(this.form);" NAME="viewedit=1&ID=$rEmails->{'ID'}" VALUE="View/Edit"> </TD>\n|;
    $html .= qq|  </TR>\n|; 
  }
#============================================================================

  $html .= qq|</TABLE>\n|;
  $html .= qq|
<HR WIDTH="90%" >
<INPUT TYPE="hidden" NAME="mlt" VALUE="$form->{mlt}" >
<INPUT TYPE="hidden" NAME="misLINKS" VALUE="$form->{misLINKS}" >
<INPUT TYPE="hidden" NAME="LINKID" VALUE="$form->{LINKID}" >
</FORM>
<PRE>${text}</PRE>

<SCRIPT LANGUAGE="JavaScript">
document.MISEmails.elements[0].focus();
</SCRIPT>
</BODY>
</HTML>
|;
  $sEmails->finish();
  return($html);
}
############################################################################
