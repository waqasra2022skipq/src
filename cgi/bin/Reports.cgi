#!/usr/bin/perl
use lib 'C:/xampp/htdocs/src/lib';
use DBI;
use DBForm;
use SysAccess;
use DBA;
use myHTML;
use gHTML;
use Time::Local;
my $DT = localtime();

############################################################################
my $form = DBForm->new();
my $dbh  = $form->dbconnect();
my $cdbh = $form->connectdb('okmis_config');

#foreach my $f ( sort keys %{$form} ) { warn "ProviderRpts: form-$f=$form->{$f}\n"; }
############################################################################
# Access required
warn qq|ENTER->Reports.cgi: ProvID=$form->{Provider_ProvID}\n|;
if ( !$form->{Provider_ProvID} ) {
    $form->error("Provider Page / denied ProvID NULL");
}
if ( !SysAccess->verify( $form, 'hasProviderAccess' ) ) {
    $form->error("Provider Page / denied Provider Access)");
}
if ( !SysAccess->verify( $form, 'Privilege=ProviderRpts' ) ) {
    $form->error("Provider Page / denied Access to Reports");
}

############################################################################
my $Agent = SysAccess->verify( $form, 'Privilege=Agent' );
if ( $form->{UpdateTables} =~ /all/i ) {
    my $sDelete = $dbh->prepare(
        "delete from ProviderRpts where ProvID=$form->{Provider_ProvID}");
    $sDelete->execute() || $form->dberror("delete ProviderRpts");
    $sDelete->finish();

    #warn qq|DELETE ProviderRpts: ProvID=$form->{Provider_ProvID}\n|;
    my $sInsert = $dbh->prepare(
"INSERT INTO ProviderRpts (ProvID,Name,CreateProvID,CreateDate,ChangeProvID) VALUES (?,?,?,?,?)"
    );

    my $ReportNames;
    my $qxReports =
qq|select * from xReports where Cron=1 and ExpDate is null order by Descr |;
    my $sxReports = $cdbh->prepare($qxReports);
    $sxReports->execute() || $form->dberror($qxReports);
    while ( my $rxReports = $sxReports->fetchrow_hashref ) {
        if ( $form->{ $rxReports->{Name} } == 1 ) {
            $sInsert->execute(
                $form->{Provider_ProvID}, $rxReports->{Name},
                $form->{LOGINPROVID},     $form->{TODAY},
                $form->{LOGINPROVID}
            ) || $form->dberror("insert ProviderRpts");

  #warn qq|INSERT ProviderRpts: $form->{Provider_ProvID}, $rxReports->{Name}\n|;
            $ReportNames .= qq|$rxReports->{Name}\n|;
        }
    }
    $sxReports->finish();
    $sInsert->finish();

##
    # send notice to support to add reports to cron.
    my $Subject =
      qq|Provider Reports: $form->{Provider_FName_1} $form->{Provider_LName_1}|;
    my $Message = qq|Scheduled Reports for Provider ${DT}\n\n${ReportNames}|;
    DBUtil->email( $form, 'support@okmis.com', $Subject, $Message );
##
    # exit on update.
    $cdbh->disconnect();
    $form->complete();
    print
qq|Location: /cgi/bin/ProviderPage.cgi?Provider_ProvID=$form->{Provider_ProvID}&mlt=$form->{mlt}\n\n|;
}
##
# CONTINUE if not update
############################################################################
# get Provider record for summary output.
my $qProvider = qq|select * from Provider where ProvID=?|;
my $sProvider = $dbh->prepare($qProvider);
$sProvider->execute( $form->{Provider_ProvID} )
  || $form->dberror("Provider in ProviderRpts");
my $rProvider = $sProvider->fetchrow_hashref;

my $qProviderRpts = qq|select * from ProviderRpts where ProvID=? and Name=?|;
my $sProviderRpts = $dbh->prepare($qProviderRpts);
my $Defns;
my $qxReports =
qq|select * from xReports where Cron=1 and Script is not null and ExpDate is null order by Category|;

#warn "\nqxReports=\n$qxReports\n";
my $sxReports = $cdbh->prepare($qxReports);
$sxReports->execute || $form->dberror($qxReports);
while ( my $rxReports = $sxReports->fetchrow_hashref ) {
    my $text = $rxReports->{Defn} ? $dbh->quote( $rxReports->{Defn} ) : "''";
    $Defns .=
qq|<SCRIPT LANGUAGE="JavaScript">newtextMsg('help$rxReports->{Name}',${text});</SCRIPT>\n|;
}
my @Categories = ();
my $qxReports =
qq|select Category from xReports where Cron=1 and ExpDate is null group by Category|;

#warn "\nqxReports=\n$qxReports\n";
my $sxReports = $cdbh->prepare($qxReports);
$sxReports->execute() || $form->dberror($qxReports);
while ( my $rxReports = $sxReports->fetchrow_hashref ) {

    #  if ( $rxReports->{Category} =~ /agent/i )
    #  { push(@Categories,$rxReports->{Category}) if ( ${Agent} ); }
    #  else
    #  { push(@Categories,$rxReports->{Category}); }
    push( @Categories, $rxReports->{Category} );
}
############################################################################
my $BackLinks = gHTML->setLINKS( $form, 'back' );
my $qxReports =
qq|select * from xReports where Cron=1 and Category=? and ExpDate is null order by Descr |;
my $html = myHTML->newPage( $form, "Schedule Reports for Provider" ) . qq|
${Defns}
<FORM NAME="ProviderRpts" ACTION="/src/cgi/bin/mis.cgi" METHOD="POST" >
<TABLE CLASS="main fullsize" >
  <TR >
    <TD CLASS="strcol" >
      $rProvider->{FName} $rProvider->{MName} $rProvider->{LName} 
    </TD>
    <TD CLASS="numcol" >${BackLinks}</TD>
  </TR>
</TABLE>
</FORM>
<TABLE CLASS="home fullsize" >
<FORM NAME="Reports" ACTION="/src/cgi/bin/Reports.cgi" METHOD="POST" >
<TABLE CLASS="home fullsize">
  <TR>
    <TD CLASS="port" COLSPAN="2" >
      Any reports selected will be setup to run automatically and available under Reports->Your Report List.
    </TD>
  </TR>
|;
my $sxReports = $cdbh->prepare($qxReports);
foreach my $Category (@Categories) {
    $html .= qq|
  <TR>
    <TD CLASS="port hdrstr" >${Category}</TD>
    <TD CLASS="home strcol" >
     <UL> 
|;
    $sxReports->execute($Category) || $form->dberror($qxReports);
    while ( my $rxReports = $sxReports->fetchrow_hashref ) {

        #warn qq|CHECK: $rxReports->{Name}, $rxReports->{Priv}\n|;
        $sProviderRpts->execute( $form->{Provider_ProvID}, $rxReports->{Name} );
        if ( $rProviderRpts = $sProviderRpts->fetchrow_hashref ) {
            $Checked = 'CHECKED';
            $Value   = 1;
            $Text    = 'Yes';
        }
        else { $Checked = ''; $Value = 0; $Text = 'No'; }
        $Help =
qq|<A HREF="javascript:void(0)" ONMOUSEOVER="textMsg.show('help$rxReports->{Name}')" ONMOUSEOUT="textMsg.hide()" ><IMG WIDTH=15 HEIGHT=15 BORDER=0 SRC="/images/qm1.gif"></A>|;
        if ( SysAccess->verify( $form, "Privilege=$rxReports->{Priv}" ) ) {
            $html .=
qq|  <LI><INPUT TYPE="checkbox" NAME="$rxReports->{Name}" VALUE="1" ${Checked} >$rxReports->{Descr} ${Help}</LI>|;
        }
        else {
            $html .=
qq|  <LI><INPUT TYPE="hidden" NAME="$rxReports->{Name}" VALUE="${Value}" >[${Text}] $rxReports->{Descr} ${Help}</LI>|;
        }
    }
    $html .= qq|</UL>
    </TD>
  </TR>
|;
}
$html .= qq|
</TABLE>
<TABLE CLASS="main fullsize" >
  <TR >
    <TD CLASS="numcol" >
      <INPUT TYPE="submit" NAME="Provider_ProvID=$form->{Provider_ProvID}&UpdateTables=all" VALUE="Add/Update">
    </TD>
  </TR>
</TABLE>
<TABLE CLASS="main fullsize" >
</TABLE>
<INPUT TYPE=hidden NAME="Provider_FName_1" VALUE="$rProvider->{FName}" >
<INPUT TYPE=hidden NAME="Provider_LName_1" VALUE="$rProvider->{LName}" >
<INPUT TYPE=hidden NAME="mlt" VALUE="$form->{mlt}" >
<INPUT TYPE=hidden NAME="LINKID" VALUE="$form->{LINKID}" >
<INPUT TYPE=hidden NAME="misLINKS" VALUE="$form->{misLINKS}" >
</FORM>
|;
$html .= myHTML->rightpane( $form, 'search' );

$sProvider->finish();
$sxReports->finish();
$sProviderRpts->finish();
$cdbh->disconnect();
$form->complete();

print $html;
exit;
############################################################################
