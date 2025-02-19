#!/usr/bin/perl
use lib '/var/www/okmis/src/lib';
use DBI;
use myForm;
use myDBI;
use MgrTree;
use SysAccess;
use DBA;
use DBUtil;
use myHTML;
use gHTML;

############################################################################
my $form   = myForm->new();
my $dbh    = myDBI->dbconnect( $form->{'DBNAME'} );
my $addURL = "mlt=$form->{mlt}&misLINKS=$form->{misLINKS}";
myForm->pushLINK();    # save this link/page to return to.

#warn "ENTER->ManagerTreeIA::new-> LOGINPROVID=$form->{LOGINPROVID}\n";
$MyURL  = qq|/cgi/bin/mis.cgi?MIS_Action=MgrTreeIA&mlt=$form->{mlt}|;
$addURL = qq|mlt=$form->{mlt}&misLINKS=$form->{misLINKS}|;

# set the Unreviewed Treatments by Provider
$Counts      = {};
$qUnreviewed = qq|select * from Unreviewed order by ProvID|;
$sUnreviewed = $dbh->prepare($qUnreviewed);
$sUnreviewed->execute() || myDBI->dberror($qUnreviewed);
while ( $r = $sUnreviewed->fetchrow_hashref ) { $Counts{ $r->{ProvID} } = $r; }
$sUnreviewed->finish();

# Start out the display.
my $html = myHTML->new($form) . qq|
<LINK HREF="|
  . myConfig->cfgfile( 'tabcontent/template6/tabcontent.css', 1 )
  . qq|" REL="stylesheet" TYPE="text/css" >
<SCRIPT SRC="|
  . myConfig->cfgfile( 'tabcontent/tabcontent.js', 1 )
  . qq|" TYPE="text/javascript" ></SCRIPT>
<TABLE CLASS="main" >
  <TR ALIGN="center" >
| . myHTML->leftpane( $form, 'clock mail managertree collapseipad' ) . qq|
    <TD WIDTH="84%" ALIGN="center" >
| . myHTML->hdr($form) . myHTML->menu($form) . qq|
    <FORM NAME="MgrTree" ACTION="/cgi/bin/mis.cgi" METHOD="POST" >
<TABLE CLASS="main fullsize" >
  <TR ALIGN="left" >
    <TD >
|;

##
# set for this Provider so as not to output twice.
#   first order by Name instead of ProvID...
##
my $NoMe = 1;
if ( $form->{LOGINACLID} ) {
    my $qACL = qq|select ProvID from Provider |;
    my $conj = qq|where|;
    foreach my $id ( split( chr(253), $form->{LOGINACLID} ) ) {
        $qACL .= qq| ${conj} ProvID='${id}' |;
        $conj = qq|or|;
    }
    $qACL .= qq| order by Provider.Name, Provider.LName, Provider.FName|;

    #warn qq|ACLID=$form->{ACLID}, q=$qACL\n|;
    my $sACL = $dbh->prepare($qACL);
    $sACL->execute() || myDBI->dberror($qACL);
    while ( my ($id) = $sACL->fetchrow_array ) {
        $html .= main->getBranch( $form, $id, $Index );
        $NoMe = 0
          if ( index( $html, "Provider_ProvID=$form->{LOGINPROVID}" ) > 0 );

        #warn qq|NoMe=$NoMe: $id=$id\n|;
    }
}

#warn qq|NoMe=$NoMe, LOGINPROVID=$form->{LOGINPROVID}\n|;
if ($NoMe) { $html .= main->getBranch( $form, $form->{LOGINPROVID}, $Index ); }

$html .= gHTML->misSiteMsg($form) . qq|
    </TD>
  </TR>
</TABLE>
<INPUT TYPE="hidden" NAME="mlt" VALUE="$form->{mlt}" >
</FORM>
|;
$html .= myHTML->rightpane( $form, 'search' );
myDBI->cleanup();

print $html;

exit;
############################################################################
# Output all Sub-Providers for Provider
sub getBranch {

    my ( $self, $form, $ProvID, $Index ) = @_;

    #warn qq|getBranch: $ProvID, $Index\n|;
    # First print out this Provider.
    my $sProvider = $dbh->prepare("select * from Provider where ProvID=?");
    $sProvider->execute($ProvID);
    my $rProvider = $sProvider->fetchrow_hashref;

    #warn "getBranch 0: result=$rProvider->{ProvID}, $rProvider->{Type}\n";
    my $out = qq|  <TABLE CLASS="home fullsize" >\n|;
    $out .= main->genHTML( $form, $rProvider );
    $sProvider->finish();

    # Print out the Tree for this Provider.
    for my $branch ( MgrTree->getProviders( $form, $ProvID, $Index ) ) {

#    next if ( $branch->{Active} );
#warn qq|getBranch: ProvName=$branch->{Name}, $branch->{LName}, $branch->{FName}, $branch->{Index}\n|;
        $out .= main->genHTML( $form, $branch );
    }
    $out .= qq|  </TABLE>\n|;
    return ($out);
}
############################################################################
# Print out this Manager and all their sub-Managers.
sub genHTML {
    my ( $self, $form, $r ) = @_;

    my $Width     = 10 + ( 20 * $r->{Index} );
    my $UnRevCnt  = $Counts{ $r->{ProvID} }{'Count'};
    my $UnBillCnt = $Counts{ $r->{ProvID} }{'Unbilled'};
    my $UnRev =
      $UnRevCnt
      ? "<FONT COLOR=red >${UnRevCnt}</FONT>"
      : "<FONT COLOR=black >${UnRevCnt}</FONT>";
    my $UnBill =
      $UnBillCnt
      ? "<FONT COLOR=black >${UnBillCnt}</FONT>"
      : "<FONT COLOR=red >${UnBillCnt}</FONT>";
    my $ClientListURL =
      qq|/cgi/bin/ClientList.cgi?Provider_ProvID=$r->{ProvID}|;
    my $ClientListIMG =
qq|<IMG BORDER=0 ALT="Client-List by Provider" SRC="/images/icon_folder.gif">|;
    my $ChartListURL =
qq|/cgi/bin/ChartList.cgi?Provider_ProvID=$r->{ProvID}&SortType=NotBilled|;
    my $ChartListIMG =
qq|<IMG BORDER=0 ALT="Chart-List by Provider" SRC="/images/clipboard.gif">|;

    my $Email    = qq|<A HREF="mailto:$r->{Email}">$r->{Email}</A>|;
    my $Spacer   = qq|  <IMG HEIGHT=1 WIDTH="$Width" SRC="/images/blank.gif">|;
    my $ProvName = qq|$r->{'Name'}|;
    if ( $r->{Type} == 4 ) {
        $ProvName = qq|$r->{'LName'}, $r->{'FName'} $r->{'Suffix'}|;
    }
    my $ProvInfo = '';
    my $JobTitle = '';
    my $Info     = '';
    my $qClinicProvider =
qq|select Type from ProviderPrivs where ProvID=? and Type='ClinicProvider'|;
    my $sClinicProvider = $dbh->prepare($qClinicProvider);
    $sClinicProvider->execute( $r->{ProvID} )
      || myDBI->dberror($qClinicProvider);
    if ( my ($ClinicProvider) = $sClinicProvider->fetchrow_array ) {
        my $ws1 = $dbh->quote("${ProvName} Client List ID=$r->{ProvID}");
        my $ws2 = $dbh->quote("${ProvName} Chart List ID=$r->{ProvID}");
        $ProvInfo = qq|
      <A HREF="${ClientListURL}&${addURL}" ONMOUSEOVER="window.status=${ws1}; return true;" ONMOUSEOUT="window.status=''" >$ClientListIMG</A>
      <A HREF="${ChartListURL}&${addURL}" ONMOUSEOVER="window.status=${ws2}; return true;" ONMOUSEOUT="window.status=''" >$ChartListIMG</A>
      &nbsp; &nbsp; &nbsp; &nbsp;
|;
        $Info = qq|(${UnRev}<FONT COLOR=black >/</FONT>${UnBill})|;
    }
    elsif ( $r->{Type} == 4 ) { $ProvName .= qq| ($r->{JobTitle})|; }
    $sClinicProvider->finish();

#warn "genHTML: Name=$ProvName, ProvID=$r->{ProvID}, Index=$r->{Index}, W=$Width\n";
    my $out .= qq|
    <TR>
      |;
    if ( $r->{Active} ) {
        $ProvInfo .=
qq|${ClientListIMG} ${ChartListIMG}  <FONT COLOR=black >${ProvName}</FONT> |;
    }
    else {
        my $ws = $dbh->quote("${ProvName} Information ID=$r->{ProvID}");
        $ProvInfo .=
qq| <A HREF="/cgi/bin/ProviderPage.cgi?Provider_ProvID=$r->{ProvID}&${addURL}" ONMOUSEOVER="window.status=${ws}; return true;" ONMOUSEOUT="window.status=''" >${ProvName}</A> |;
    }
    $out .= qq|
      <TD CLASS="title" > ${Spacer} ${ProvInfo} ${Info} ${Email} </TD>
|;
    $out .= qq|
    </TR>
|;
    return ($out);
}
############################################################################
