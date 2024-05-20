#!/usr/bin/perl
use lib '/home/okmis/mis/src/lib';
use CGI qw(:standard escape);
use DBI;
use DBForm;
use DBA;
use myHTML;
############################################################################
# ClientMail is just a routine to save MAIL given away to Providers
############################################################################
my $form = DBForm->new();
foreach my $f ( sort keys %{$form} ) { warn "ClientMail: form-$f=$form->{$f}\n"; }
warn "ClientMail: ClientID=${'Client_ClientID'}, USERLOGINID=$form->{USERLOGINID}\n";
my ($DBNAME,$USERID) = split(':',$form->{'USERLOGINID'});
warn "ClientMail: DBNAME=${DBNAME}, USERID=${USERID}\n";
my $ClientID = $form->{'Client_ClientID'} ? $form->{'Client_ClientID'} : $USERID;

############################################################################
# Access required
##
if ( !$ClientID ) { $form->error("Client ACL / denied ClientID NULL"); }
if ( ! SysAccess->hasClientAccess($form,$ClientID) )
{ $form->error("Client Access List / Not Client"); }

############################################################################
# get the database they are attached to.
my $dbh = $form->dbconnect();
my $mdbh = $form->connectdb($DBNAME);
# get Client.
my $sClient = $mdbh->prepare("select * from Client where ClientID=?");
$sClient->execute($USERID);
my $rClient = $sClient->fetchrow_hashref;
my $PrimaryProvID = $rClient->{'ProvID'};
# get Primary Provider.
my $sProvider = $mdbh->prepare("select * from Provider where ProvID=?");
$sProvider->execute($PrimaryProvID);
my $rProvider = $sProvider->fetchrow_hashref;
my $PrimaryProvider = qq|$rProvider->{'FName'} $rProvider->{'LName'} $rProvider->{'Suffix'}|;

warn qq|ClientMail: UpdateTables=$form->{UpdateTable}\n|;
my $html = '';
# Are we updating? or printing HTML?
if ( $form->{UpdateTables} )
{ $html .= main->doUpdate(); }
elsif ( $form->{'IDs'} )
{ $html .= main->doPRINT(); }
else
{ $html .= main->doHTML(); }

$sClient->finish();
$sProvider->finish();
$form->complete();
$mdbh->disconnect();

print $html;
exit;

############################################################################
sub doUpdate()
{
  my ($self) = @_;
warn "ClientMail: doUpdate: ClientID=${ClientID}\n";
  my $FromName = $form->{LOGINNAME} eq '' ? $form->{LOGINUSERNAME} : $form->{LOGINNAME};
  my $DateSent = DBUtil->Date('','stamp','long');
  my $ToName = $PrimaryProvider;
  my $Subject = $form->{ClientMail_Subject_1};
  my $Message = $form->{ClientMail_Message_1};
  my $rMail = ();
  $rMail->{'CreateUserID'} = $form->{'LOGINUSERID'};
  $rMail->{'CreateDate'} = $form->{'TODAY'};
  $rMail->{'ChangeUserID'} = $form->{'LOGINUSERID'};
  $rMail->{'CreateUserID'} = $form->{'LOGINUSERID'};
  $rMail->{'ClientID'} = $ClientID;
  $rMail->{'FromLOGINID'} = $form->{'USERLOGINID'};
  $rMail->{'ToProvID'} = $PrimaryProvID;
  $rMail->{'ToProvName'} = $PrimaryProvider;
  $rMail->{'Subject'} = $Subject;
  $rMail->{'Message'} = $Message;
  $rMail->{'DateSent'} = $DateSent;
  $rMail->{'Status'} = 'send';
  my $qMail = DBA->genInsert($form,'ClientMail',$rMail);
warn qq|ClientMail: qMail=${qMail}\n|;
  $sMail = $dbh->prepare($qMail);
  $sMail->execute() || $form->dberror($qMail);
  $sMail->finish();
  my $Location = $form->{'HTTPSERVER'};
warn qq|ClientMail: Location=$Location\n|;
  my $html = qq|Location: ${Location}\n\n|;
  return($html);
}
sub doPRINT()
{
  my ($self) = @_;
warn "ClientMail: doHTML: ClientID=${ClientID}\n";
  my $sMail = $dbh->prepare("select * from ClientMail where ID=?");
  $sMail->execute($form->{'IDs'});
  my $rMail = $sMail->fetchrow_hashref;
  $sMail->finish();
  my $FromName = $form->{LOGINNAME} eq '' ? $form->{LOGINUSERNAME} : $form->{LOGINNAME};
  my $ToProvName = $rMail->{'ToProvName'};
  my $DateSent = $rMail->{'DateSent'};
  my $Status = $rMail->{'Status'};
  my $Subject = $rMail->{'Subject'};
  my $Message = $rMail->{'Message'};
  my $html = myHTML->new($form,"Client Mail");
#      <INPUT TYPE="button" NAME="close" VALUE="close" ONCLICK="javascript: window.close()" >
  $html .= qq|
<TABLE CLASS="main halfsize" >
  <TR >
    <TD CLASS="strcol" >
      ${FromName}
    </TD>
  </TR>
</TABLE>

<TABLE CLASS="home halfsize" >
  <TR ><TD CLASS="port hdrtxt" COLSPAN="2" >Client secure mail to your Provider</TD></TR>
|;
  $html .= qq|
</TABLE>
<TABLE CLASS="home halfsize" >
  <TR>
    <TD CLASS="strcol subtitle" >From:</TD>
    <TD CLASS="strcol subtitle" >${FromName}</TD>
  </TR>
  <TR>
    <TD CLASS="strcol subtitle" >To:</TD>
    <TD CLASS="strcol subtitle" >${ToProvName}</TD>
  </TR>
  <TR>
    <TD CLASS="strcol subtitle" >Date:</TD>
    <TD CLASS="strcol subtitle" >${DateSent}</TD>
  </TR>
  <TR>
    <TD CLASS="strcol subtitle" >Status:</TD>
    <TD CLASS="strcol subtitle" >${Status}</TD>
  </TR>
  <TR>
    <TD CLASS="strcol subtitle" >Subject:</TD>
    <TD CLASS="strcol subtitle" >${Subject}</TD>
  </TR>
  <TR>
    <TD CLASS="strcol subtitle" >Message:</TD>
    <TD CLASS="strcol subtitle" >${Message}</TD>
  </TR>
</TABLE>
|;
  return($html);
}
sub doHTML()
{
  my ($self) = @_;
warn "ClientMail: doHTML: ClientID=${ClientID}\n";
  my $FromName = $form->{LOGINNAME} eq '' ? $form->{LOGINUSERNAME} : $form->{LOGINNAME};
  my $DateSent = DBUtil->Date('','stamp','long');
  my $ToName = $PrimaryProvider;
  my $Subject = qq|  <INPUT TYPE="text" NAME="ClientMail_Subject_1" VALUE="" ONFOCUS="select()" SIZE=60>|;
  my $Message = qq|  <TEXTAREA NAME="ClientMail_Message_1" COLS="80" ROWS="18" WRAP="virtual" onFocus="select()" ></TEXTAREA>|;
  my $html = myHTML->new($form,"Client Mail");
  $html .= qq|
<FORM NAME="ClientMail" ACTION="/cgi/bin/ClientMail.cgi" METHOD="POST" >
<TABLE CLASS="main halfsize" >
  <TR >
    <TD CLASS="strcol" >
      ${FromName}
    </TD>
  </TR>
</TABLE>

<TABLE CLASS="home halfsize" >
  <TR ><TD CLASS="port hdrtxt" COLSPAN="2" >Send Client secure mail to your Provider</TD></TR>
  <TR ><TD CLASS="strcol" COLSPAN="2" >Enter subject/message to sent to your provider.</TD></TR>
|;
  $html .= qq|
</TABLE>
<TABLE CLASS="home halfsize" >
  <TR>
    <TD CLASS="strcol subtitle" >From:</TD>
    <TD CLASS="strcol subtitle" >${FromName}</TD>
  </TR>
  <TR>
    <TD CLASS="strcol subtitle" >Date:</TD>
    <TD CLASS="strcol subtitle" >${DateSent}</TD>
  </TR>
  <TR>
    <TD CLASS="strcol subtitle" >To:</TD>
    <TD CLASS="strcol subtitle" >${ToName}</TD>
  </TR>
  <TR>
    <TD CLASS="strcol subtitle" >Subject:</TD>
    <TD CLASS="strcol subtitle" >${Subject}</TD>
  </TR>
  <TR>
    <TD CLASS="strcol subtitle" >Message:</TD>
    <TD CLASS="strcol subtitle" >${Message}</TD>
  </TR>
</TABLE>
<TABLE CLASS="main halfsize" >
  <TR>
    <TD CLASS="numcol" >
      <INPUT TYPE="button" ONCLICK="window.location='$form->{'HTTPSERVER'}'" VALUE="Cancel">
      <INPUT TYPE="submit" NAME="UpdateTables=all" VALUE="Send">
    </TD>
  </TR>
</TABLE>
<INPUT TYPE="hidden" NAME="Client_ClientID" VALUE="${ClientID}" >
<INPUT TYPE="hidden" NAME="mlt" VALUE="$form->{mlt}" >
<INPUT TYPE="hidden" NAME="LINKID" VALUE="$form->{LINKID}" >
<INPUT TYPE="hidden" NAME="misLINKS" VALUE="$form->{misLINKS}" >

</FORM>
|;
  return($html);
}
############################################################################
