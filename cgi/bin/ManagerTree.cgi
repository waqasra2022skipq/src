#!/usr/bin/perl
use lib '/home/okmis/mis/src/lib';
use DBI;
use myForm;
use myDBI;
use DBA;
use SysAccess;
use myConfig;
use DBUtil;
use myHTML;
use gHTML;
use Time::HiRes qw(time);
#$t_start=Time::HiRes::time;
#warn "ManagerTree   curtime: $t_start\n";

#warn qq|\n\nSTART: ManagerTree:\n|;
############################################################################
my $form = myForm->new();
my $dbh = myDBI->dbconnect($form->{'DBNAME'});

#warn qq|CHECK: form:\n|;
#foreach my $f ( sort keys %{$form} ) { warn "ManagerTree: form-$f=$form->{$f}\n"; }

my $sProviderPrefs = $dbh->prepare("select * from ProviderPrefs where ProvID=?");
$sProviderPrefs->execute($form->{'LOGINUSERID'});
my $rProviderPrefs = $sProviderPrefs->fetchrow_hashref;
$sProviderPrefs->finish();
#warn qq|ManagerTree: dbh=${dbh}=\n|;
#warn qq|ManagerTree: TreeTabs=$rProviderPrefs->{'TreeTabs'}=\n|;
#warn qq|ManagerTree: ListClients=$rProviderPrefs->{'ListClients'}=\n|;

my $addURL = "mlt=$form->{mlt}&misLINKS=$form->{misLINKS}";
my $ChartList = '/cgi/bin/ChartList.cgi';
my $ClientList = '/cgi/bin/ClientList.cgi';
myForm->pushLINK();       # save this link/page to return to.
my $tabclients = $rProviderPrefs->{'ListClients'} ? qq|
<script language="JavaScript" type="text/javascript" src="/cgi/js/tabs.js"></script>
<link rel="STYLESHEET" type="text/css" href="/cgi/css/tabs.css" />
| : '';

# Start out the display.
my $html = myHTML->new($form) . qq|
<LINK HREF="|.myConfig->cfgfile('tabcontent/template6/tabcontent.css',1).qq|" REL="stylesheet" TYPE="text/css" >
<SCRIPT SRC="|.myConfig->cfgfile('tabcontent/tabcontent.js',1).qq|" TYPE="text/javascript" ></SCRIPT>
${tabclients}
<TABLE CLASS="main" >
  <TR ALIGN="center" >
| . myHTML->leftpane($form,'clock mail managertree collapseipad') . qq|
    <TD WIDTH="84%" ALIGN="center" >
| . myHTML->hdr($form) . myHTML->menu($form) . qq|
    <FORM NAME="MgrTree" ACTION="/cgi/bin/mis.cgi" METHOD="POST" >
<TABLE CLASS="main fullsize" >
  <TR ALIGN="left" >
    <TD >
|;

my $tabid = DBUtil->genToken();
if ( $rProviderPrefs->{'TreeTabs'} )
{
  my @Tabs = ();
  my $tab = main->genTreeTabs($form,$form->{LOGINUSERID});
#$t_diff=Time::HiRes::time-$t_start;
#warn "1.ManagerTree elapsed time: $t_diff seconds!\n";
  my $tabcontent = 'Managerial Tree'.chr(253).$tab;
  push(@Tabs,$tabcontent);
#$t_diff=Time::HiRes::time-$t_start;
#warn "2.ManagerTree elapsed time: $t_diff seconds!\n";
  $tab = gHTML->misGuide($form);
#$t_diff=Time::HiRes::time-$t_start;
#warn "3.ManagerTree elapsed time: $t_diff seconds!\n";
  my $tabcontent = 'Guide'.chr(253).$tab;
  push(@Tabs,$tabcontent);
#$t_diff=Time::HiRes::time-$t_start;
#warn "4.ManagerTree elapsed time: $t_diff seconds!\n";
  $tab = gHTML->misSiteMsg($form);
#$t_diff=Time::HiRes::time-$t_start;
#warn "5.ManagerTree elapsed time: $t_diff seconds!\n";
  my $tabcontent = 'Site Messages'.chr(253).$tab;
  push(@Tabs,$tabcontent);
#$t_diff=Time::HiRes::time-$t_start;
#warn "6.ManagerTree elapsed time: $t_diff seconds!\n";
#  $tab = gHTML->misLinks($form);
#$t_diff=Time::HiRes::time-$t_start;
#warn "7.ManagerTree elapsed time: $t_diff seconds!\n";
#  my $tabcontent = 'Links'.chr(253).$tab;
#  push(@Tabs,$tabcontent);
#$t_diff=Time::HiRes::time-$t_start;
#warn "8.ManagerTree elapsed time: $t_diff seconds!\n";
  $tab = gHTML->misFeatures($form);
  my $tabcontent = 'Feature of the Month'.chr(253).$tab;
  push(@Tabs,$tabcontent);
  $html .= gHTML->setTab('','',@Tabs);
}
else
{ $html .= main->genTreeFlat($form,$form->{LOGINUSERID}); }
$html .= qq|
    </TD>
  </TR>
</TABLE>
<INPUT TYPE="hidden" NAME="mlt" VALUE="$form->{mlt}" >
</FORM>
|;
$html .= myHTML->rightpane($form,'search');
myDBI->cleanup();

print $html;

exit;
############################################################################
# Print out the Tree for this Provider.
sub genTreeFlat
{
  my ($self,$form,$ProvID) = @_;
#warn qq|genTreeFlat:\n|;
  my $out = qq|
<TABLE CLASS="home fullsize" >
      <TR CLASS="port" ><TD CLASS="hdrcol heading" COLSPAN="2" >Managerial Tree</TD></TR>
|;
  my $mtree = '';
  my $sManagerTree = $dbh->prepare("select * from ManagerTree where TreeProvID=? order by Cnt");
  $sManagerTree->execute($ProvID);
  while ( my $r = $sManagerTree->fetchrow_hashref )
  { $mtree .= main->genHTML($form,$r); }
  $out .= $mtree;
  $out .= qq|  </TABLE>\n|;
  $out .= gHTML->misSiteMsg($form) .
  qq|
    </TD>
    <TD CLASS="home subtitle" >
|
  . gHTML->misGuide($form) 
  . gHTML->misFeatures($form)
  . qq|
|;
  $sManagerTree->finish();
  return($out);
}
#  . gHTML->misLinks($form)
##
sub genTreeTabs
{
  my ($self,$form,$ProvID) = @_;
#$t_diff=Time::HiRes::time-$t_start;
#warn "a.ManagerTree elapsed time: $t_diff seconds!\n";
#warn qq|genTreeTabs:\n|;
  my $out = qq|
<TABLE CLASS="home fullsize" >
|;
  my ($AgencyCnt,$ClinicCnt,$Ghtml) = (0,0,'');
  my @Agencies = (); my @AgencyHtml = (); my $Ahtml = '';
  my @Clinics = (); my @ClinicHtml = (); my $Chtml = '';
  my $sManagerTree = $dbh->prepare("select * from ManagerTree where TreeProvID=? order by Cnt");
  $sManagerTree->execute($ProvID);
  while ( my $r = $sManagerTree->fetchrow_hashref )
  { 
    my $html = main->genHTML($form,$r); 
    if ( $r->{Cnt} == 1 )       # first record has counts.
    {
      $AgencyCnt = $r->{AgencyCnt};
      $ClinicCnt = $r->{ClinicCnt};
    }
    if ( $AgencyCnt > 1 )       # roll up Agencys.
    { 
      if ( $r->{Type} == 2 )    # new Agency.
      {
        push(@AgencyHtml,$Ahtml) if ( $Ahtml ne '' );
#       first get rid of preps...and save the initals...
        (my $Name = $r->{Name}) =~ s/ and | for | of / /gi;
        my $Initials=''; $Initials.=uc($1) while $Name=~/(\w)\w+\s?/g;
        push(@Agencies,$Initials);
        $Ahtml = $html;
      }
      elsif ( $Ahtml eq '' )    # no Agency yet.
      { $Ghtml .= $html; }
      else { $Ahtml .= $html; }
    }
    elsif ( $ClinicCnt > 1 )    # roll up Clinics.
    { 
      if ( $r->{Type} == 3 )    # new Clinic.
      {
        push(@ClinicHtml,$Chtml) if ( $Chtml ne '' );
#       first get rid of preps...and save the initals...
        (my $Name = $r->{Name}) =~ s/ and | for | of / /gi;
        my $Initials=''; $Initials.=uc($1) while $Name=~/(\w)\w+\s?/g;
        push(@Clinics,$Initials);
        $Chtml = $html;
      }
      elsif ( $Chtml eq '' )    # no Clinic yet.
      { $Ghtml .= $html; }
      else { $Chtml .= $html; }
    }
    else { $Ghtml .= $html; }
  }
  $out .= $Ghtml;
  push(@AgencyHtml,$Ahtml) if ( $Ahtml ne '' );
  push(@ClinicHtml,$Chtml) if ( $Chtml ne '' );

  if ( scalar(@Agencies) > 1 )
  {
    my @Tabs = ();
    for ($a=0; $a<=$#Agencies; $a++)
    {
      my $tabcontent = $Agencies[$a].chr(253).qq|<TABLE CLASS="fullsize" >|.$AgencyHtml[$a].qq|</TABLE>|;
      push(@Tabs,$tabcontent);
    }
    $out .= qq|
  <TR>
    <TD CLASS="home" >
|.gHTML->setTab('','',@Tabs).qq|
    </TD>
  </TR>
|;
  }
  if ( scalar(@Clinics) > 1 )
  {
    my @Tabs = ();
    for ($c=0; $c<=$#Clinics; $c++)
    {
      my $tabcontent = $Clinics[$c].chr(253).qq|<TABLE CLASS="fullsize" >|.$ClinicHtml[$c].qq|</TABLE>|;
      push(@Tabs,$tabcontent);
    }
    $out .= qq|
  <TR>
    <TD CLASS="home" >
|.gHTML->setTab('','',@Tabs).qq|
    </TD>
  </TR>
|;
  }
  $out .= qq|
</TABLE>
|;
  $sManagerTree->finish();
  return($out);
}
############################################################################
# Print out this Provider.
sub genHTML
{
  my ($self,$form,$r) = @_;
# set the Unreviewed Treatments by Provider
  my ($UnRevCnt,$UnBillCnt) = (0,0);
  my $sUnreviewed = $dbh->prepare("select * from Unreviewed where ProvID=?");
  $sUnreviewed->execute($r->{ListProvID}) || myDBI->dberror("select Unreviewed where ProvID=$r->{ListProvID}");
  if ($rUnreviewed = $sUnreviewed->fetchrow_hashref  ) { $UnRevCnt = $rUnreviewed->{Count}; $UnBillCnt = $rUnreviewed->{Unbilled}; }
  my $UnRev = $UnRevCnt ? "<FONT COLOR=red >${UnRevCnt}</FONT>" : "<FONT COLOR=black >${UnRevCnt}</FONT>";
  my $UnBill = $UnBillCnt ? "<FONT COLOR=black >${UnBillCnt}</FONT>" : "<FONT COLOR=red >${UnBillCnt}</FONT>";
  $sUnreviewed->finish();

  my $ClientListURL = $ClientList.qq|?Provider_ProvID=$r->{ListProvID}&|.$addURL;
  my $ClientListIMG = qq|<IMG BORDER=0 ALT="Client-List by Provider" SRC="/images/icon_folder.gif">|;
  my $ChartListURL = $ChartList.qq|?Provider_ProvID=$r->{ListProvID}&SortType=NotBilled&|.$addURL;
  my $ChartListIMG = qq|<IMG BORDER=0 ALT="Chart-List by Provider" SRC="/images/clipboard.gif">|;

  my $Email =qq|<A HREF="mailto:$r->{Email}">$r->{Email}</A>|;
  my $Spacer = qq|  <IMG HEIGHT=1 WIDTH="$r->{Indent}" SRC="/images/blank.gif">|;
  my $ProvInfo = '';
  my $Info = '';
  if ( $r->{Clinician} )
  { 
    my $ws1 = $dbh->quote("$r->{Name} Client List ID=$r->{ListProvID}");
    my $ws2 = $dbh->quote("$r->{Name} Chart List ID=$r->{ListProvID}");
    $ProvInfo = qq|
      <A HREF="${ClientListURL}" ONMOUSEOVER="window.status=${ws1}; return true;" ONMOUSEOUT="window.status=''" >${ClientListIMG}</A>
      <A HREF="${ChartListURL}" ONMOUSEOVER="window.status=${ws2}; return true;" ONMOUSEOUT="window.status=''" >${ChartListIMG}</A>
      &nbsp;
|;
    $Info = qq|(${UnRev}<FONT COLOR=black >/</FONT>${UnBill})|;
  }
  my $out .= qq|
    <TR>
      |;
  my $ws = $dbh->quote("$r->{Name} Information ID=$r->{ListProvID}");
  $ProvInfo .= qq| <A HREF="/cgi/bin/ProviderPage.cgi?Provider_ProvID=$r->{ListProvID}&${addURL}" ONMOUSEOVER="window.status=${ws}; return true;" ONMOUSEOUT="window.status=''" >$r->{Name}</A> |; 
  $out .= qq|
      <TD CLASS="title" > ${Spacer} ${ProvInfo} ${Info} ${Email} </TD>
|;
  my ($CLout,$ClientTxt,$ClientCnt,$BR) = ('','',0,'');
#$t_diff=Time::HiRes::time-$t_start;
#warn "b.ManagerTree elapsed time: $t_diff seconds!\n";
  if ( $rProviderPrefs->{'ListClients'} )
  {
    my $sClientAccess = $dbh->prepare("select distinct ClientAccess.ClientID,Client.LName,FName from ClientAccess left join Client on Client.ClientID=ClientAccess.ClientID where (ClientAccess.ProvID=? or Client.ProvID=?) and Client.Active=1 order by Client.LName, Client.FName");
    $sClientAccess->execute($r->{ListProvID},$r->{ListProvID});
    while ( my $r = $sClientAccess->fetchrow_hashref )
    {
      $ClientCnt++;
      my $ClientID = $r->{'ClientID'};
      (my $ClientName = "$r->{'LName'}, $r->{'FName'}") =~ s/'/&#39;/g;
      my $ClientPage = qq|/cgi/bin/ClientPage.cgi?Client_ClientID=${ClientID}&${addURL}|;
      $ClientTxt .= qq|
      ${BR}
      <A HREF="/cgi/bin/mis.cgi?MIS_Action=Note&Client_ClientID=${ClientID}&Treatment_TrID=new&${addURL}" >
        <IMG BORDER=0 ALT="General Chart Entry" SRC="/images/facesicon.gif">
      </A>
      <A HREF="${ChartList}?Client_ClientID=${ClientID}&SortType=NotReconciled&${addURL}" >
        <IMG BORDER=0 HEIGHT=15 WIDTH=15 ALT="Chart List by Client" SRC="/images/clipboard.gif" >
      </A>
      <A HREF="${ClientPage}" ONMOUSEOVER="window.status='Click for Client Page'" ONMOUSEOUT="window.status=''" >${ClientName}</A>
|;
      $BR = "<BR>";
    }
    $sClientAccess->finish();
  }
#$t_diff=Time::HiRes::time-$t_start;
#warn "c.ManagerTree elapsed time: $t_diff seconds!\n";
  if ( $ClientTxt eq '' ) { $CLout = "&nbsp;"; } else
  {
    my $CLURL = $ClientList.qq|?Provider_ProvID=$r->{ListProvID}&SearchType=ByAccess&|.$addURL;
    my $CLIMG = qq|<IMG BORDER=0 ALT="Client-List by Provider Access" SRC="/images/icon_folder.gif">|;
    my $ws1 = $dbh->quote("$r->{Name} Client List ID=$r->{ListProvID}");
    my $tabid = DBUtil->genToken();
    $CLout = qq|
        <A HREF="${CLURL}" ONMOUSEOVER="window.status=${ws1}; return true;" ONMOUSEOUT="window.status=''" >${CLIMG} Clients by Access</A>
        <DIV STYLE="display:none" ID="${tabid}1">
          <UL CLASS="tab">
            <LI ONCLICK="showTab('${tabid}',2,1,2);" >
              <IMG BORDER=0 ALT="Hide Client-List" SRC="/images/hideshow_infohidden.gif" > ${ClientCnt}
            </LI>
          </UL>
          ${ClientTxt}
        </DIV>
        <DIV STYLE="display:block" ID="${tabid}2">
          <UL CLASS="tab">
            <LI ONCLICK="showTab('${tabid}',1,1,2);" >
              <IMG BORDER=0 ALT="Show Client-List" SRC="/images/hideshow_infoshown.gif" > ${ClientCnt}
            </LI>
          </UL>
        </DIV>
|;
  }
  $out .= qq|      <TD CLASS="title" > ${CLout} </TD>
    </TR>
|;
  return($out);
}
############################################################################
