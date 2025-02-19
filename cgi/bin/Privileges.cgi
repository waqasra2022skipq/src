#!/usr/bin/perl
############################################################################
use lib '/var/www/okmis/src/lib';
use DBI;
use DBForm;
use SysAccess;
use DBA;
use DBUtil;
use myHTML;
use gHTML;

############################################################################
$form = DBForm->new();
my $dbh = $form->dbconnect();
##
# Access required
if ( !$form->{Provider_ProvID} ) {
    $form->error("Provider Page / denied ProvID NULL");
}
if ( !SysAccess->verify( $form, 'hasProviderAccess' ) ) {
    $form->error("Provider Page / denied Provider Access)");
}
if ( !SysAccess->verify( $form, 'Privilege=ProviderPrivs' ) ) {
    $form->error("Provider Page / denied Access to Privileges");
}

############################################################################
my $Agent = SysAccess->verify( $form, 'Privilege=Agent' );
if ( $form->{UpdateTables} =~ /all/i ) {
    my $sDelete = $dbh->prepare(
        "delete from ProviderPrivs where ProvID=$form->{Provider_ProvID}");
    $sDelete->execute() || $form->dberror("delete ProviderPrivs");
    $sDelete->finish();

    #warn qq|DELETE ProviderPrivs: ProvID=$form->{Provider_ProvID}\n|;
    my $sInsert = $dbh->prepare(
"INSERT INTO ProviderPrivs (ProvID,Type,Rank,CreateProvID,CreateDate,ChangeProvID) VALUES (?,?,?,?,?,?)"
    );
    my $qxPrivileges =
qq|select * from okmis_config.xPrivileges where ExpDate is null order by Descr |;
    my $sxPrivileges = $dbh->prepare($qxPrivileges);
    $sxPrivileges->execute() || $form->dberror($qxPrivileges);
    while ( my $rxPrivileges = $sxPrivileges->fetchrow_hashref ) {

#warn qq|ProviderPrivs: $rxPrivileges->{Priv}-value=$form->{$rxPrivileges->{Priv}}\n|;
        if ( $form->{ $rxPrivileges->{Priv} } == 1 )    # Privilege CHECKED
        {
            $sInsert->execute( $form->{Provider_ProvID},
                $rxPrivileges->{Priv}, '1', $form->{LOGINPROVID},
                $form->{TODAY},        $form->{LOGINPROVID} )
              || $form->dberror("insert ProviderPrivs");

#warn qq|INSERT ProviderPrivs: $form->{Provider_ProvID}, $rxPrivileges->{Priv}\n|;
        }
    }
    $sxPrivileges->finish();
    $sInsert->finish();

    foreach my $ClinicID (
        SysAccess->getACL( $form, $form->{LOGINPROVID}, 'Clinic' ) )
    {
        if ( $form->{$ClinicID} == 1 )    # Clinic access
        {
            $sInsert->execute( $form->{Provider_ProvID},
                $ClinicID, '9', $form->{LOGINPROVID}, $form->{TODAY},
                $form->{LOGINPROVID} )
              || $form->dberror("insert ProviderPrivs");

          #warn qq|INSERT ProviderPrivs: $form->{Provider_ProvID}, $ClinicID\n|;
        }
    }

    main->setGraphUser( $form, $form->{'Provider_ProvID'} );
##
    # EXIT on update.
    $form->complete();
    print
qq|Location: /cgi/bin/ProviderPage.cgi?Provider_ProvID=$form->{Provider_ProvID}&mlt=$form->{mlt}\n\n|;
    exit;
}
##
# CONTINUE if not update
############################################################################
# get Provider record for summary output.
my $qProvider = qq|select * from Provider where ProvID=?|;
my $sProvider = $dbh->prepare($qProvider);
$sProvider->execute( $form->{Provider_ProvID} )
  || $form->dberror("select Provider table in ProviderPrivs");
my $rProvider = $sProvider->fetchrow_hashref;

my $qProviderPrivs = qq|select * from ProviderPrivs where ProvID=? and Type=?|;
my $sProviderPrivs = $dbh->prepare($qProviderPrivs);
my $Defns;
my $qxPrivileges =
qq|select * from okmis_config.xPrivileges where ExpDate is null order by Category|;

#warn "\nqxPrivileges=\n$qxPrivileges\n";
my $sxPrivileges = $dbh->prepare($qxPrivileges);
$sxPrivileges->execute || $form->dberror($qxPrivileges);
while ( my $rxPrivileges = $sxPrivileges->fetchrow_hashref ) {
    my $text =
      $rxPrivileges->{Defn} ? $dbh->quote( $rxPrivileges->{Defn} ) : "''";
    $Defns .=
qq|<SCRIPT LANGUAGE="JavaScript">newtextMsg('help$rxPrivileges->{Priv}',${text});</SCRIPT>\n|;
}
my @Categories = ();
my $qxPrivileges =
qq|select Category from okmis_config.xPrivileges where ExpDate is null group by Category|;

#warn "\nqxPrivileges=\n$qxPrivileges\n";
my $sxPrivileges = $dbh->prepare($qxPrivileges);
$sxPrivileges->execute || $form->dberror($qxPrivileges);
while ( my $rxPrivileges = $sxPrivileges->fetchrow_hashref ) {
    if ( $rxPrivileges->{Category} =~ /agent/i ) {
        push( @Categories, $rxPrivileges->{Category} ) if ( ${Agent} );
    }
    else { push( @Categories, $rxPrivileges->{Category} ); }
}
############################################################################
# Start out the display.
my $html = myHTML->new($form) . qq|
${Defns}
<TABLE CLASS="main" >
  <TR ALIGN="center" >
| . myHTML->leftpane( $form, 'clock mail managertree collapseipad' ) . qq|
    <TD WIDTH="84%" ALIGN="center" >
| . myHTML->hdr($form) . myHTML->menu($form) . qq|
<FORM NAME="ProviderPrivs" ACTION="/cgi/bin/Privileges.cgi" METHOD="POST" >
|;
############################################################################
my $BackLinks = gHTML->setLINKS( $form, 'back' );
my $qxPrivileges =
qq|select * from okmis_config.xPrivileges where Category=? and ExpDate is null order by Descr |;
$html .= qq|
<TABLE CLASS="main fullsize" >
  <TR >
    <TD CLASS="strcol" >
      $rProvider->{FName} $rProvider->{MName} $rProvider->{LName} 
      <BR>Provider Privileges
    </TD>
    <TD CLASS="numcol" >${BackLinks}</TD>
  </TR>
</TABLE>
<HR WIDTH="90%" >
<TABLE CLASS="home fullsize" >
    <TR ><TD ><TABLE CLASS="home fullsize" >
|;
my $sxPrivileges = $dbh->prepare($qxPrivileges);

foreach my $Category (@Categories) {
    $html .= qq|
 <TR> <TD CLASS="port hdrtxt" >${Category}</TD></TR>
 <TR>
 <TD CLASS="strcol" >
 <UL> 
|;
    $sxPrivileges->execute($Category) || $form->dberror($qxPrivileges);
    while ( my $rxPrivileges = $sxPrivileges->fetchrow_hashref ) {
        $sProviderPrivs->execute( $form->{Provider_ProvID},
            $rxPrivileges->{Priv} );
        if ( $rProviderPrivs = $sProviderPrivs->fetchrow_hashref ) {
            $Checked = 'CHECKED';
        }
        else { $Checked = ''; }
        $Help =
qq|<A HREF="javascript:void(0)" ONMOUSEOVER="textMsg.show('help$rxPrivileges->{Priv}')" ONMOUSEOUT="textMsg.hide()" ><IMG WIDTH=15 HEIGHT=15 BORDER=0 SRC="/images/qm1.gif"></A>|;
        $Descr =
          $Agent
          ? qq|$rxPrivileges->{Descr} ($rxPrivileges->{Priv})|
          : $rxPrivileges->{Descr};
        $html .=
qq|  <LI><INPUT TYPE="checkbox" NAME="$rxPrivileges->{Priv}" VALUE="1" ${Checked} >${Descr} ${Help}</LI>|;
    }
    $html .= qq|</UL>
 </TD>
 </TR>
|;
}
$html .= qq|
 <TR><TD CLASS="port hdrtxt" >Access Billing Error Reports for Clinic</TD></TR>
 <TR>
 <TD CLASS="strcol" >
 <UL> 
|;
foreach
  my $ClinicID ( SysAccess->getACL( $form, $form->{LOGINPROVID}, 'Clinic' ) )
{
    $sProvider->execute($ClinicID);
    my $rClinic = $sProvider->fetchrow_hashref;
    $sProviderPrivs->execute( $form->{Provider_ProvID}, $ClinicID );
    if ( $rProviderPrivs = $sProviderPrivs->fetchrow_hashref ) {
        $Checked = 'CHECKED';
    }
    else { $Checked = ''; }
    $html .=
qq|  <LI><INPUT TYPE="checkbox" NAME="${ClinicID}" VALUE="1" ${Checked} >$rClinic->{Name}</LI>|;
}
$html .= qq|</UL>
 </TD>
 </TR>
|;
$html .= qq|
    </TABLE></TD></TR>
</TABLE>
<TABLE CLASS="main fullsize" >
  <TR >
    <TD CLASS="numcol" >
      <INPUT TYPE="submit" NAME="Provider_ProvID=$form->{Provider_ProvID}&UpdateTables=all" VALUE="Add/Update">
    </TD>
  </TR>
</TABLE>
<INPUT TYPE="hidden" NAME="mlt" VALUE="$form->{mlt}" >
<INPUT TYPE="hidden" NAME="LINKID" VALUE="$form->{LINKID}" >
<INPUT TYPE="hidden" NAME="misLINKS" VALUE="$form->{misLINKS}" >
</FORM>
|;
$html .= myHTML->rightpane( $form, 'search' );

$sProvider->finish();
$sxPrivileges->finish();
$sProviderPrivs->finish();
$form->complete();
print $html;
exit;
############################################################################
sub setGraphUser {
    my ( $self, $form, $ProvID ) = @_;

    #warn qq|setGraphUser: $ProvID\n|;
    return () if ( $ProvID <= 91 );
    my $qProviders =
qq|select Provider.ProvID,Provider.FName,Provider.LName,UserLogin.Password,UserLogin.loginid from Provider left join UserLogin on UserLogin.UserID=Provider.ProvID where Provider.ProvID=?|;
    my $dbh  = $form->dbconnect();
    my $gdbh = $form->connectdb('graphsok_d3');

    # update in the graph users records...
    my $sProvider = $dbh->prepare($qProviders);
    $sProvider->execute($ProvID);
    if ( my $rProvider = $sProvider->fetchrow_hashref ) {
        if ( SysAccess->chkPriv( $form, 'Graphs', $ProvID ) ) {
            my $r = ();
            my ( $pfx, $hospital ) = split( '_', $form->{'DBNAME'} );
            $r->{'hospital'} = $hospital;
            $r->{'username'} = $rProvider->{'loginid'};
            $r->{'password'} = main->getPswd( $form, $rProvider->{'Password'} );
            $r->{'role'} =
              SysAccess->chkPriv( $form, 'ClinicManager', $ProvID )
              ? 'manager'
              : 'provider';
            $r->{'provider'} = qq|$rProvider->{'LName'}, $rProvider->{'FName'}|;
            $r->{'provid'}   = $ProvID;
            $r->{'mlt'}      = DBUtil->genToken(12);
            my $u;
            my $q =
qq|select * from users where hospital='$r->{'hospital'}' and provid='$r->{provid}'|;
            my $s = $gdbh->prepare($q);
            $s->execute() || $form->dberror($q);

            if ( my $t = $s->fetchrow_hashref ) {
                $r->{'id'} = $t->{'id'};
                $u = DBA->genUpdate( $form, 'users', $r, 'id' );
            }
            else { $u = DBA->genInsert( $form, 'users', $r ); }

            #warn qq|Privileges: u=$u\n|;
            my $susers = $gdbh->prepare($u);
            $susers->execute() || $form->dberror($qusers);
            $susers->finish();
            $s->finish();
        }
        else {
            my ( $pfx, $hospital ) = split( '_', $form->{'DBNAME'} );
            my $q =
qq|delete from users where hospital='${hospital}' and provid='${ProvID}'|;

            #warn qq|Privileges: q=$q\n|;
            my $s = $gdbh->prepare($q);
            $s->execute() || $form->dberror($q);
            $s->finish();
        }
    }
    $sProvider->finish();
    $form->complete();
    $gdbh->disconnect();
    return ();
}

sub getPswd {
    my ( $self, $form, $pswd ) = @_;
    my $dbh  = $form->dbconnect();
    my $qmd5 = qq|select MD5(?)|;
    my $smd5 = $dbh->prepare($qmd5);
    $smd5->execute($pswd);
    my $md5 = $smd5->fetchrow_array;
    $smd5->finish();
    return ($md5);
}
############################################################################
