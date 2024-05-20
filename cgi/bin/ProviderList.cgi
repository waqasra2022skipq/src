#!/usr/bin/perl
############################################################################
use lib '/home/okmis/mis/src/lib';
use CGI qw(:standard escape);
use DBI;
use DBForm;
use DBA;
use DBUtil;
use SysAccess;
use myHTML;

############################################################################
$form = DBForm->new;
$dbh = $form->dbconnect;
my $addURL = qq|mlt=$form->{mlt}&mislINKS=$form->{misLINKS}|;
my $backURL = "/cgi/bin/mis.cgi?misPOP=1&${addURL}";

$s=$dbh->prepare("select * from Provider where Type=2 or Type=3");
  $s->execute();
  while (my $r = $s->fetchrow_hashref) { $ClinicList->{$r->{ProvID}} = $r; }
$s->finish();
my $qClinicProvider=qq|select Type from ProviderPrivs where ProvID=? and Type='ClinicProvider'|;
my $sClinicProvider=$dbh->prepare($qClinicProvider);
############################################################################
# Output the Provider List part of the HTML.
##
my $SearchName = '';
my $qProvider = searchFor();
#warn qq|qProvider=$qProvider\n|;
my $sProvider = $dbh->prepare($qProvider);
$sProvider->execute();
my $html = myHTML->newPage($form,"Provider Listing") . qq|
<TABLE CLASS="main fullsize" >
  <TR >
    <TD CLASS="strcol" WIDTH=70% ALIGN=left >
      <FONT CLASS="strcol" >Provider List</FONT> 
      <BR>
      <FONT CLASS="strcol" >${SearchName}</FONT>
    </TD>
    <TD CLASS="numcol" >
      <A HREF="${backURL}" ><IMG BORDER="0" ALT="back" SRC="/images/chartback.gif" WIDTH="40" HEIGHT="40" ></A>
    </TD>
  </TR>
</TABLE>

<TABLE CLASS="home fullsize" >
  <TR >
    <TD CLASS="port strcol" >Provider</TD>
    <TD CLASS="port hdrcol" >Active</TD>
    <TD CLASS="port strcol" >Email</TD>
    <TD CLASS="port strcol" >Work Phone</TD>
    <TD CLASS="port strcol" >Cell</TD>
    <TD CLASS="port strcol" >Clinic/Agency</TD>
  </TR>
|;
while ( $rProvider = $sProvider->fetchrow_hashref )
{
  if ( SysAccess->verify($form,'hasProviderAccess',$rProvider->{ProvID}) )
  { $html .= main->ProviderList($form,$rProvider); }
}
$html .= qq|</TABLE>\n|;
$html .= myHTML->rightpane($form,'search');
##
# Close the SQL statments.
##
$sProvider->finish();
$sClinicProvider->finish();
$form->complete();

print $html;
exit;

############################################################################
sub searchFor
{
  my ($self) = @_;
  my $str = '';
  if ( $form->{'SearchType'} eq 'ProviderID' )
  {
    $SearchName = qq|Provider ID: $form->{SearchString}|;
#warn "ProviderList.cgi: SearchName=$SearchName\n";
    $str = qq|select distinct Provider.* from Provider where Provider.ProvID = '$form->{SearchString}' order by Provider.LName, Provider.FName|;
  }
  elsif ( $form->{'SearchType'} eq 'ProviderFirstName' )
  {
    $SearchName = qq|First Name: $form->{SearchString}|;
    ($SearchStr = $form->{SearchString}) =~ s/\.{3}/\%/g;
#warn "ProviderList.cgi: SearchName=$SearchName\n";
    $str = qq|select distinct Provider.* from Provider where Provider.FName like '$SearchStr' order by Provider.LName, Provider.FName|;
  }
  elsif ( $form->{'SearchType'} eq 'ProviderLastName' )
  {
    $SearchName = qq|Last Name: $form->{SearchString}|;
    ($SearchStr = $form->{SearchString}) =~ s/\.{3}/\%/g;
#warn "ProviderList.cgi: SearchStr=$SearchStr\n";
    $str = qq|select distinct Provider.* from Provider where Provider.LName like '$SearchStr' order by Provider.LName, Provider.FName|;
  }
  else
  { $form->error("Provider List / Access Denied"); }
  return($str);
}
############################################################################
# This subroutine outputs the HTML for each Provider Line.
sub ProviderList()
{
  my ($self,$form,$r) = @_;

  my $page = qq|/cgi/bin/ProviderPage.cgi?Provider_ProvID=$r->{ProvID}&${addURL}|;
  my $ProviderName = qq|$r->{LName}, $r->{FName} $r->{MName}|;
  my $ws1 = $dbh->quote("${ProvName} Chart List ID=$r->{ProvID}");
  my $ws2 = $dbh->quote("${ProvName} Client List ID=$r->{ProvID}");
  my $ws3= $dbh->quote("${ProviderName} Information ID=$r->{ProvID}");

  my $links = '';
  $sClinicProvider->execute($r->{ProvID}) || $form->dberror($qClinicProvider);
  if ( my ($ClinicProvider) = $sClinicProvider->fetchrow_array )
  {
    $links = qq| 
      <A HREF="/cgi/bin/ClientList.cgi?Provider_ProvID=$r->{ProvID}&${addURL}" ONMOUSEOVER="window.status=${ws2}; return true;" ONMOUSEOUT="window.status=''" ><IMG BORDER=0 ALT="Client-List by Provider" SRC="/images/icon_folder.gif"></A>
      <A HREF="/cgi/bin/ChartList.cgi?Provider_ProvID=$r->{ProvID}&SortType=NotBilled&${addURL}" ONMOUSEOVER="window.status=${ws1}; return true;" ONMOUSEOUT="window.status=''" ><IMG BORDER=0 ALT="Chart-List by Provider" SRC="/images/clipboard.gif"></A>
      <A HREF="${page}" ONMOUSEOVER="window.status=${ws3}; return true;" ONMOUSEOUT="window.status=''" >${ProviderName}</A>
|;
  }
  else
  {
    $links = qq| 
      <A HREF="${page}" ONMOUSEOVER="window.status=${ws3}; return true;" ONMOUSEOUT="window.status=''" >${ProviderName}</A>
|;
  }

  my $Active = $r->{Active} ? 'yes' : 'no';
  my $ClinicID = MgrTree->getClinic($form,$r->{ProvID});
  $ClinicID = MgrTree->getAgency($form,$r->{ProvID}) unless ( $ClinicID );
  my $ClinicName = $ClinicList->{$ClinicID}{Name};

  my $html = qq|
  <TR >
    <TD CLASS="strcol" >${links}</TD>
    <TD CLASS="hdrcol" >${Active}</TD>
    <TD CLASS="strcol" ><A HREF="mailto:$r->{Email}">$r->{Email}</A></TD>
    <TD CLASS="strcol" >$r->{WkPh}</TD>
    <TD CLASS="strcol" >$r->{MobPh}</TD>
    <TD CLASS="strcol" >${ClinicName}</TD>
  </TR>
|;
  return($html);
}
############################################################################
