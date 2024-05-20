#!/usr/bin/perl
use lib '/home/okmis/mis/src/lib';
use DBI;
use myForm;
use myDBI;
use DBA;
use myConfig;
use SysAccess;
use myHTML;

############################################################################
my $form = myForm->new();
my $dbh = myDBI->dbconnect($form->{'DBNAME'});
my $cdbh = myDBI->dbconnect('okmis_config');
my $AccessHR=SysAccess->ChkPriv($form,'HRReports');
my $ALLACCESS=$form->{LOGINPROVID} == 91 ? 1 : 0;

############################################################################
# get Provider record for summary output.
$qProvider = qq|select * from Provider where ProvID=?|;
$sProvider = $dbh->prepare($qProvider);
$sProvider->execute($form->{Provider_ProvID}) || myDBI->dberror("Provider in UserReports");
$rProvider = $sProvider->fetchrow_hashref;

my $Defns;
my $xtable = $form->{'xtable'} eq '' ? 'xReports' : $form->{'xtable'};
my $qxTable = qq|select * from ${xtable} where Script is not null and ExpDate is null order by Category|;
#warn "\nqxTable=\n$qxTable\n";
my $sxTable = $cdbh->prepare($qxTable);
$sxTable->execute || myDBI->dberror($qxTable);
while ( my $rxTable = $sxTable->fetchrow_hashref ) 
{ 
  my $text = $rxTable->{Defn} ? $dbh->quote($rxTable->{Defn}) : "''";
  $Defns .= qq|<SCRIPT LANGUAGE="JavaScript">newtextMsg('help$rxTable->{Name}',${text});</SCRIPT>\n|;
}
my @Categories = (); my $CatCount = 0;
my $qxTable = qq|select Category from ${xtable} where ExpDate is null group by Category|;
#warn "\nqxTable=\n$qxTable\n";
my $sxTable = $cdbh->prepare($qxTable);
$sxTable->execute || myDBI->dberror($qxTable);
while ( my $rxTable = $sxTable->fetchrow_hashref ) 
{ push(@Categories,$rxTable->{Category}); $CatCount++; }

############################################################################
# UNUSED???
#<link rel="STYLESHEET" type="text/css" href="/cgi/css/tabs.css" />
#<LINK REL="stylesheet" TYPE="text/css" HREF="/cgi/jcal/calendar-forest.css" >
#<script language="JavaScript" type="text/javascript" src="/cgi/js/tabs.js"></script>
#<SCRIPT TYPE="text/javascript" SRC="/cgi/jcal/calendar.js"></SCRIPT>
#<SCRIPT TYPE="text/javascript" SRC="/cgi/jcal/calendar-en.js"></SCRIPT>
#<SCRIPT TYPE="text/javascript" SRC="/cgi/jcal/calendar-setup.js"></SCRIPT>
############################################################################
# Start out the display.
my $html = myHTML->newHTML($form,'Provider Reports','CheckPopupWindow noclock countdown_60') . qq|
<DIV CLASS="title" >Reports Window</DIV>
${Defns}
<DIV ALIGN="center" > 
  <FORM NAME="Reports" ACTION="/cgi/bin/GenReports.cgi" METHOD="POST" >

|;
my $AutoRun = $xtable eq 'xReports' ? qq|
<U>Automatically run reports*:</U><BR>
These reports run at a set date/time. They have an (add/remove) link next to them (you can add them only if you have the Human Resources Access). This link (if you have access to the report) can be used to have the report run for you at the set date/time and placed in <A HREF="javascript:LoadInParent('/cgi/bin/ListFiles.cgi?Type=RPT&mlt=$form->{mlt}&misLINKS=$form->{misLINKS}',true)" ONMOUSEOVER="window.status='Your Reports List'; return true;" ONMOUSEOUT="window.status=''" ><U>'your reports list'</U></A>. When they do run, an email is sent to your email address.<BR>
| : '';

my $cnt=0;
my $BreakPt = 4;
my $colspan=int($CatCount/$BreakPt);
my $w="33%";
my $qxTable = qq|select * from ${xtable} where Category=? and ExpDate is null order by Descr |;
$html .= qq|
<TABLE CLASS="home fullsize" >
  <TR>
    <TD COLSPAN="${CatCount}" >
      <DIV CLASS="subtitle tophdr" >Guide</DIV>
      <DIV CLASS="subtitle" >
Use Report Name link to access report. Those without a link cannot be run (check your privileges).<BR>
${AutoRun}
      </DIV>
    </TD>
  </TR>
</TABLE>
<TABLE CLASS="home fullsize" >
  <TR>
    <TD WIDTH="${w}" >
|;
my $sxTable = $cdbh->prepare($qxTable);
foreach my $Category ( @Categories ) 
{ 
  if ( $cnt>0 && $cnt%$BreakPt == 0 )
  { $html .= qq|      </TD><TD WIDTH="${w}" >\n|; }
  $html .= qq|
      <DIV CLASS="subtitle tophdr" >${Category}</DIV>
      <DIV CLASS="subtitle strcol" >
|;
  $sxTable->execute($Category) || myDBI->dberror($qxTable);
  while ( my $rxTable = $sxTable->fetchrow_hashref )
  {
#warn qq|CHECK: $rxTable->{Name}, $rxTable->{Priv}\n|;
    $Help = qq|<A HREF="javascript:void(0)" ONMOUSEOVER="textMsg.show('help$rxTable->{Name}')" ONMOUSEOUT="textMsg.hide()" ><IMG WIDTH="15" HEIGHT="15" BORDER="0" SRC="/images/qm1.gif"></A>|;
    if ( $ALLACCESS || SysAccess->ChkPriv($form,"$rxTable->{Priv}") )
    {
      my $upd = $rxTable->{Cron} && $AccessHR ? main->setUpdate($form,$form->{LOGINPROVID},$rxTable->{Name}) : '';
      my $flg = $rxTable->{Cron} ? '*' : '';
      $html .= qq|<A HREF="javascript:ReportWindow('/cgi/bin/GenReport.cgi?Name=$rxTable->{Name}&mlt=$form->{mlt}&$rxTable->{Args}&xtable=$form->{xtable}','$rxTable->{Name}',900,1000)" >$rxTable->{Descr}</A>${flg} ${Help} ${upd} <BR>\n|;
    }
    elsif ( $rxTable->{Priv} eq 'Agent' || $rxTable->{Priv} eq '91' ) { null; }  # don't let normal users see these.
    else { $html .= qq|$rxTable->{Descr} ${Help}<BR>\n|; }
  }
  $html .= qq|<BR>      </DIV>|;
  $cnt++;
}
$html .= qq|
    </TD>
  </TR>
</TABLE>
<INPUT TYPE="hidden" NAME="mlt" VALUE="$form->{mlt}" >
<INPUT TYPE="hidden" NAME="LINKID" VALUE="$form->{LINKID}" >
<INPUT TYPE="hidden" NAME="misLINKS" VALUE="$form->{misLINKS}" >
<INPUT TYPE="hidden" NAME="xtable" VALUE="$form->{xtable}" >
</FORM>
| . myHTML->rightpane($form);
#<BR><BR><BR><BR><BR><BR><BR><BR><BR><BR><BR><BR>

$sProvider->finish();
$sxTable->finish();

myDBI->cleanup();

print $html;
exit;
############################################################################
sub setUpdate
{
  my ($self,$form,$ProvID,$Name) = @_;
  my $url; my $type;
  my $qProviderRpts = qq|select * from ProviderRpts where ProvID=? and Name=?|;
  my $sProviderRpts = $dbh->prepare($qProviderRpts);
  $sProviderRpts->execute($ProvID,$Name) || myDBI->dberror("execute error: UserReports/setUpdate");
  if ( $rProviderRpts = $sProviderRpts->fetchrow_hashref )
  { $type='remove'; } else { $type='add'; }
  $url = qq|<A HREF="javascript:InputWindow('/cgi/bin/addProviderRpt.cgi?mlt=$form->{mlt}&Name=$Name','${Name}',300,300)" >(${type})</A>|;
  return($url);
}
############################################################################
