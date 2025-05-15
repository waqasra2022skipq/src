#!/usr/bin/perl
use lib 'C:/xampp/htdocs/src/lib';
use DBI;
use myForm;
use myDBI;
use gHTML;
use Time::Local;
my $DT = localtime();
############################################################################
my $form = myForm->new();
my $dbh  = myDBI->dbconnect( $form->{'DBNAME'} );

my $ClientID = $form->{ClientID} ? $form->{ClientID} : $form->{Client_ClientID};
my ( $delm, $InsSel ) = ( '', '' );
my $s = $dbh->prepare("select InsID from Insurance where ClientID=?");
$s->execute($ClientID)
  || myDBI->dberror("ClientSC: select Insurance ClientID=${ClientID}");
while ( my ($InsID) = $s->fetchrow_array ) {
    $InsSel .= qq|${delm} xInsurance.ID=${InsID} |;
    $delm = 'or';
}
$s->finish();
my $report = qq|No Insurances for Client (or no ClientID).|;
if ($InsSel)    # generate report?
{
    my $ForIns = $InsSel ? qq| and (${InsSel})| : '';
    my $select = qq|
select xInsurance.Name, xCredentials.Abbr as Credential
      ,xSC.SCNum, xSC.SCName
      ,xSCRestrictions.Descr as Restriction
      ,xSCRates.HrsPerUnit, xSCRates.UnitLbl, xSCRates.RVUPct
      ,xSCRates.EffDate, xSCRates.ExpDate
  from xSC
  left join xSCRates on xSCRates.SCID=xSC.SCID
  left join xInsurance on xInsurance.ID=xSC.InsID
  left join okmis_config.xCredentials on xCredentials.ID=xSC.CredID
  left join okmis_config.xSCRestrictions on xSCRestrictions.ID=xSC.Restriction
 where xSCRates.EffDate is not null
  and xSC.Active=1 and (xSCRates.ExpDate>curdate() or xSCRates.ExpDate is null)
  ${ForIns}
 order by xInsurance.Name, xCredentials.Abbr, xSC.SCNum, xSC.SCID, xSCRates.EffDate, xSCRestrictions.Descr
|;
    $report = gHTML->rptSQL( $form, $select, '', ':::::::numeric:date:date',
        '::::::::MM/DD/YY:MM/DD/YY' );
}
my $html = qq|Content-type: text/html


<HTML>
<HEAD>
<TITLE>Client Insurances Service Code Listing</TITLE>
<META HTTP-EQUIV="expires" CONTENT="Mon, 23 Mar 1998 20:00:00 GMT">
<LINK REL="stylesheet" HREF="/src/cgi/css/mis.css" TYPE="text/css" TITLE="Millennium style sheet">
</HEAD>
<BODY>
<DIV ALIGN="center" >
<TABLE CLASS="porttitle" >${report}</TABLE>
</DIV>
</BODY>
</HTML>
|;

myDBI->cleanup();

print $html;
exit;
############################################################################
