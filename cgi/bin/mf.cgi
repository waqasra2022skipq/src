#!C:/Strawberry/perl/bin/perl.exe
############################################################################
use lib 'C:/xampp/htdocs/src/lib';
use DBI;
use myForm;
use myDBI;
use DBA;
use DBUtil;
use myHTML;

############################################################################


my $form    = myForm->new();
my $dbh     = myDBI->dbconnect( $form->{'DBNAME'} );
my $ProvID  = $form->{'ProvID'};
my @ProvIDs = ();
my $TITLE   = 'DEFAULT';
my $LISTS   = ();


if ( $ProvID == 90 )    # Help Desk Global Forms
{ 
    push( @ProvIDs, '90' );
    $TITLE = qq|Millennium Forms / Links|;
    $LISTS->{'90'}->{'Section 1'} =
'Medicaid:OHCA:DMH:Clinical_Pathways:Medicare:BCBS:Tricare:SAMHSA:MCO Humana:MCO Complete Health:MCO Atena';
    $LISTS->{'90'}->{'Section 2'} =
      'MyHealth:CARF:Testing:Charting:Library:Federal:State:Curricula:Legal';
}
else {
    $TITLE = qq|Corporate Forms|;
    my ( $addprov, $sel, $conj ) = ( 1, '', '' );
    $addprov = 0 if ( $form->{LOGINPROVID} == 91 );
    foreach my $p (
        SysAccess->getACL( $form, $form->{LOGINPROVID}, 'Agency:Clinic' ) )
    {
        $sel .= qq|${conj} ProvID=${p} |;
        $conj    = ' or ';
        $addprov = 0 if ( $form->{LOGINPROVID} == $p );
    }
    $sel .= qq|${conj} ProvID=$form->{LOGINPROVID}| if ($addprov);

    #warn qq|sel=${sel}\n|;
    my $sProvider = $dbh->prepare(
"select ProvID,Name,FName,LName from Provider where Active=1 and (${sel}) order by Type,Name,LName,FName"
    );
    my $sProviderEDocs = $dbh->prepare(
"select ProviderEDocs.ID,xEDocTags.Tag,Provider.ProvID,Provider.Name,Provider.FName,Provider.LName from ProviderEDocs left join Provider on Provider.ProvID=ProviderEDocs.ProvID left join okmis_config.xEDocTags on xEDocTags.ID=ProviderEDocs.Type where ProviderEDocs.ProvID=? and ProviderEDocs.Public=1 group by xEDocTags.Tag"
    );
    $sProvider->execute() || myDBI->dberror("select Provider ${sel}");
    while ( my $rProvider = $sProvider->fetchrow_hashref ) {

        #warn qq|LOOP: ProvID=$rProvider->{ProvID}\n|;
        my $p = $rProvider->{'ProvID'};
        next if ( $p == 90 );
        push( @ProvIDs, $p );
        my ( $name, $list, $dlm, $cnt, $cont ) = ( '', '', '', 0, '' );
        $sProviderEDocs->execute($p)
          || myDBI->dberror("select ProviderEDocs ${p}");
        while ( my $rProviderEDocs = $sProviderEDocs->fetchrow_hashref ) {
            $cnt++;
            $name =
              $rProviderEDocs->{'Name'} eq ''
              ? qq|$rProviderEDocs->{'FName'} $rProviderEDocs->{'LName'}|
              : $rProviderEDocs->{'Name'};
            $name .= ' (continued)' . $cont if ( $cnt > 10 );

            #warn qq|LOOP: name=${name}\n|;
            if ( $cnt % 10 == 0 ) {
                $LISTS->{$p}->{$name} = $list;
                $list                 = '';
                $dlm                  = '';
                $cont .= ' ';
            }
            $list .= $dlm . $rProviderEDocs->{'Tag'};
            $dlm = ':';
        }
        $LISTS->{$p}->{$name} = $list;
    }
    $sProvider->finish();
    $sProviderEDocs->finish();
}

############################################################################
my $CloseButton =
qq|<INPUT TYPE="button" NAME="close" VALUE="close" ONCLICK="javascript: window.close()" >|;

#my $BodyArg = qq|STYLE="background-color:#ccffff"|;
#my $BodyArg = qq|STYLE="background-color:#e6e6fa"|;
#my $BodyArg = qq|STYLE="background-color:#00b1b3"|;
#my $BodyArg = qq|STYLE="background-color:#00cccc"|;
#my $BodyArg = qq|STYLE="background-color:#cccc00"|;
#my $BodyArg = qq|STYLE="background-color:#0099ff"|;
#my $BodyArg = qq|STYLE="background-color:#993333"|;

my $BodyArg = qq|STYLE="background-color: #007acc"|;
my $html    = myHTML->new( $form, $TITLE, 'CheckPopupWindow', $BodyArg ) . qq|
<LINK HREF="|
  . myConfig->cfgfile( 'tabcontent/template6/tabcontent.css', 1 )
  . qq|" REL="stylesheet" TYPE="text/css" >
<SCRIPT SRC="|
  . myConfig->cfgfile( 'tabcontent/tabcontent.js', 1 )
  . qq|" TYPE="text/javascript" ></SCRIPT>
<SCRIPT LANGUAGE="JavaScript" TYPE="text/javascript" SRC="/src/cgi/js/tabs.js"></SCRIPT>
<LINK REL="STYLESHEET" TYPE="text/css" HREF="/src/cgi/css/tabs.css" />
<P>
<P>
<TABLE STYLE="background-color:steelblue" CLASS="list fullsize" >
  <TR ><TD CLASS="hdrtxt header" COLSPAN="2" >${TITLE}</TD></TR>
  <TR >
    <TD CLASS="strcol" >Click on Tabs/Links to open.</TD>
    <TD CLASS="numcol" >${CloseButton}</TD>
  </TR>
</TABLE>
|;
foreach my $ProvID (@ProvIDs) {
    foreach my $section ( sort keys %{ $LISTS->{$ProvID} } ) {

#warn qq|CALL: ProvID=${ProvID}, section=$section, list=$LISTS->{$ProvID}->{$section}\n|;
        $html .= qq|
<TABLE CLASS="list fullsize" >
  <TR ><TD CLASS="hdrtxt title" COLSPAN="2" >${section}</TD></TR>
  <TR >
    <TD >
|
          . DBA->setEDocTags( $form, $ProvID, $LISTS->{$ProvID}->{$section} )
          . qq|
    </TD>
  </TR>
</TABLE>
|;
    }
}
$html .= qq|
</BODY>
</HTML>
|;
print $html;
myDBI->cleanup();
exit;
#############################################################################
