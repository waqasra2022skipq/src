#!/usr/bin/perl
use lib 'C:/xampp/htdocs/src/lib';
use CGI qw(:standard escape);
use DBI;
use myForm;
use myDBI;
use DBA;
use SysAccess;
use MgrTree;
use myHTML;
use gHTML;
############################################################################
# ClientAccess is just a routine to save MANUAL access given away to Providers
#  for Clients. The real table is ClientACL which builds Providers access
#  to Clients by combining both ClientAccess and Providers SiteACL.
############################################################################
my $form = myForm->new();
my $dbh  = myDBI->dbconnect( $form->{'DBNAME'} );

#warn qq|ClientAccess: ClientID=$form->{Client_ClientID}, UpdateTables=$form->{UpdateTable}\n|;

############################################################################
# Access required
##
if ( !$form->{Client_ClientID} ) {
    myDBI->error("Client ACL / denied ClientID NULL");
}
if ( !SysAccess->verify( $form, 'Privilege=ClientAccess' ) ) {
    myDBI->error("Access Denied! / Client Access Control");
}
if ( !SysAccess->verify( $form, 'hasClientAccess' ) ) {
    myDBI->error("Client Access List / Not Client");
}

############################################################################
# get Client record for summary output.
my $sClient = $dbh->prepare(
"select Client.*,ClientLegal.JOLTS from Client left join ClientLegal on ClientLegal.ClientID=Client.ClientID where Client.ClientID=?"
);
$sClient->execute( $form->{Client_ClientID} );
my $rClient    = $sClient->fetchrow_hashref;
my $ClientName = $rClient->{Pref};
$ClientName .= " $rClient->{FName}"  if ( $rClient->{FName} );
$ClientName .= " $rClient->{MName}"  if ( $rClient->{MName} );
$ClientName .= " $rClient->{LName}"  if ( $rClient->{LName} );
$ClientName .= " $rClient->{Suffix}" if ( $rClient->{Suffix} );
$sClient->finish();

############################################################################
# Are we updating? or printing HTML?
if   ( $form->{UpdateTables} ) { &doUpdate; }
else                           { &doHTML; }

myDBI->cleanup();
exit;

############################################################################
# print HTML
##
sub doHTML() {

    #warn "ClientAccess->BEGIN:\n";
    ############################################################################
    # get the Primary Provider
    my $sProvider = $dbh->prepare("select * from Provider where ProvID=?");
    $sProvider->execute( $rClient->{ProvID} );
    $rProvider   = $sProvider->fetchrow_hashref;
    $ProvID      = $rProvider->{ProvID};
    $PrimaryProv = "$rProvider->{FName} $rProvider->{LName}";
    $sProvider->finish();

#warn "ClientAccess: ClientID=$form->{Client_ClientID}, PPProvID=$rClient->{ProvID}, ProvID=$ProvID\n";
    $PPSelect = DBA->selProviders( $form, $rClient->{ProvID} );

    #warn "ClientAccess: PPSelect=$PPSelect\n";

    ############################################################################
    # get the Assigned Clinics.
    $clinicClinicSelVal =
      DBA->selClinics( $form, '', $rClient->{clinicClinicID}, '', 1 );

    #warn "ClientAccess:  clinic= clinicClinicSelVal=$clinicClinicSelVal\n";

    ############################################################################
    # get the Client Access List of Providers.
    #   if Login is Primary Provider or immediate Manager of Primary Provider.
## 2 lists are for HIPAA requirements to know who gave away access.
    my $HeaderACL  = '';
    my $DisplayACL = '';
    my $ACLSelect  = '';

    #warn qq|PID=$form->{LOGINPROVID}, CID=$rClient->{ProvID}\n|;
    if (   $form->{LOGINPROVID} == $rClient->{ProvID}
        || $form->{LOGINPROVID} ==
        MgrTree->getManager( $form, $rClient->{ProvID} ) )
    {
        if ( $form->{LOGINPROVID} == $rClient->{ProvID} ) {
            $HeaderACL  = 'Access List for Primary Provider';
            $DisplayACL = 'Providers';
        }
        else {
            $HeaderACL  = 'Access List for Immediate Managers';
            $DisplayACL = 'Managers / HR';
        }
        ( $ACL_ProviderIDs, $delm ) = ( '', '' );
        my $sACL = $dbh->prepare("select * from ClientAccess where ClientID=?");
        $sACL->execute( $form->{Client_ClientID} );
        while ( $rACL = $sACL->fetchrow_hashref ) {
            $ACL_ProviderID = $rACL->{ProvID};
            $ACL_ProviderIDs .= "${delm}${ACL_ProviderID}";
            $delm = chr(253);
        }
        $sACL->finish();
        if ( $form->{LOGINPROVID} == $rClient->{ProvID} ) {
            $ACLSelect = DBA->selClinicProvider( $form, $ACL_ProviderIDs );
        }
        else { $ACLSelect = DBA->selClinicManager( $form, $ACL_ProviderIDs ); }

 #warn "ClientAccess: ACL_ProviderIDs=$ACL_ProviderIDs\nACLSelect=$ACLSelect\n";
    }
    elsif ( SysAccess->verify( $form, 'Privilege=Agent' ) ) {
        $HeaderACL  = 'Access List for Agent';
        $DisplayACL = 'All Providers';
        ( $ACL_ProviderIDs, $delm ) = ( '', '' );
        my $sACL = $dbh->prepare("select * from ClientAccess where ClientID=?");
        $sACL->execute( $form->{Client_ClientID} );
        while ( $rACL = $sACL->fetchrow_hashref ) {
            $ACL_ProviderID = $rACL->{ProvID};
            $ACL_ProviderIDs .= "${delm}${ACL_ProviderID}";
            $delm = chr(253);
        }
        $sACL->finish();
        $ACLSelect = DBA->selProviders( $form, $ACL_ProviderIDs );
    }

    ############################################################################
    # output the HTML

    my $BackLinks = gHTML->setLINKS( $form, 'back' );
    print myHTML->newPage( $form, "Client Access" );
    print qq|
<FORM NAME="ClientAccess" ACTION="/src/cgi/bin/ClientAccess.cgi" METHOD="POST" >
<TABLE CLASS="main fullsize" >
  <TR >
    <TD CLASS="strcol" >
      ${ClientName} ($form->{Client_ClientID}) $rClient->{SSN} $rClient->{'JOLTS'}
      <BR>
      Client Access
    </TD>
    <TD CLASS="numcol" > ${BackLinks} </TD>
  </TR>
</TABLE>

<TABLE CLASS="home fullsize" >
  <TR ><TD CLASS="port heading" COLSPAN="3" >Client Access Control Lists</TD></TR>
  <TR ><TD CLASS="port hdrtxt" COLSPAN="3" >Providers for Client</TD></TR>
  <TR >
    <TD CLASS="strcol" WIDTH="30%" >Primary Provider</TD>
    <TD CLASS="strcol" >
      <SELECT NAME="Client_ProvID" >
        ${PPSelect}
      </SELECT>
    </TD>
    <TD CLASS="strcol" >&nbsp;</TD>
  </TR>
  <TR ><TD CLASS="strcol" COLSPAN="3" >&nbsp;</TD></TR>
|;
    if ( ${DisplayACL} eq '' ) {
        print qq|
  <TR ><TD CLASS="port hdrtxt" COLSPAN="3" >No Access List</TD></TR>
  <TR >
    <TD CLASS="strcol" WIDTH="30%" >&nbsp;</TD>
    <TD CLASS="strcol" COLSPAN="2" ALIGN=left >
      You are neither Primary Provider or Immediate Manager.<BR>
      Providers assigned access to this client can be accessed only by the Primary Privider or the Immediate Manager to the Primary Provider.
    </TD>
  </TR>
  <TR ><TD CLASS="strcol" COLSPAN="3" >&nbsp;</TD></TR>
|;
    }
    else {
        print qq|
  <TR ><TD CLASS="port hdrtxt" COLSPAN="3" >${HeaderACL}</TD></TR>
  <TR >
    <TD CLASS="strcol" WIDTH="30%" >Assigned ${DisplayACL}</TD>
    <TD CLASS="strcol" >
      <SELECT NAME="ACL_ProviderIDs" MULTIPLE SIZE=10 >
        ${ACLSelect}
      </SELECT>
    </TD>
    <TD CLASS="strcol" ALIGN=left >
      Providers assigned access to this client.
      You can select multiple Providers by using your ctrl key with your mouse.
    </TD>
  </TR>
  <TR ><TD CLASS="strcol" COLSPAN="3" >&nbsp;</TD></TR>
|;
    }
    print qq|
  <TR ><TD CLASS="port hdrtxt" COLSPAN="3" >Clinic</TD></TR>
  <TR >
    <TD CLASS="strcol" WIDTH="30%" >Assigned Clinic</TD>
    <TD CLASS="strcol" >
      <SELECT NAME="Client_clinicClinicID" >
        ${clinicClinicSelVal}
      </SELECT>
    </TD>
    <TD CLASS="strcol" ALIGN=left >(where Chart is kept)</TD>
  </TR>
  <TR ><TD CLASS="strcol" COLSPAN="3" >&nbsp;</TD></TR>
</TABLE>
<INPUT TYPE="hidden" NAME="mlt" VALUE="$form->{mlt}" >
<INPUT TYPE="hidden" NAME="LINKID" VALUE="$form->{LINKID}" >
<INPUT TYPE="hidden" NAME="misLINKS" VALUE="$form->{misLINKS}" >

<TABLE CLASS="main fullsize" >
  <TR>
    <TD CLASS="numcol" >
      <INPUT TYPE="submit" NAME="UpdateTables=all&Client_ClientID=$form->{Client_ClientID}" VALUE="UPDATE Access">
    </TD>
  </TR>
</TABLE>
</FORM>
|;
    print myHTML->rightpane( $form, 'search' );
    return (1);
}
############################################################################
# UPDATE
##
sub doUpdate() {

#warn "ClientAccess,update: Client=$form->{Client_ClientID}, ACL_ProviderIDs=$form->{ACL_ProviderIDs}\n";

    # 1st delete any Access for client using the same list they had in the HTML.
    # selection is just like on FORM
    my $sDelete =
      $dbh->prepare("delete from ClientAccess where ProvID=? and ClientID=?");
    my $ACList;
    if ( $form->{LOGINPROVID} == $rClient->{ProvID} ) {
        $ACList = DBA->selClinicProvider( $form, $form->{ACL_ProviderIDs}, 1 );
    }
    elsif ( $form->{LOGINPROVID} ==
        MgrTree->getManager( $form, $rClient->{ProvID} ) )
    {
        $ACList = DBA->selClinicManager( $form, $form->{ACL_ProviderIDs}, 1 );
    }
    elsif ( SysAccess->verify( $form, 'Privilege=Agent' ) ) {
        $ACList = DBA->selProviders( $form, $form->{ACL_ProviderIDs}, 1 );
    }

    #warn "ClientAccess,update: ACList=$ACList\n";
    foreach my $desc ( sort keys %{$ACList} ) {

        #warn "ClientAccess,delete $ACList->{$desc},$form->{Client_ClientID}\n";
        $sDelete->execute( $ACList->{$desc}, $form->{Client_ClientID} );
    }
    $sDelete->finish();

    my ( $Results, $Cnt ) = ( '', 0 );

    # next add any Access for client.
    #warn "ClientAccess: ACL_ProviderIDs=$form->{ACL_ProviderIDs}\n";
    my $sInsert =
      $dbh->prepare("insert into ClientAccess (ProvID,ClientID) values (?,?)");
    foreach my $ProvID ( split( chr(253), $form->{ACL_ProviderIDs} ) ) {

#warn "ClientAccess,insert into ClientAccess (ProvID,ClientID) VALUES (${ProvID},$form->{Client_ClientID})\n";
        $sDelete->execute( $ProvID, $form->{Client_ClientID} )
          ;    # needed to delete because of inactive Providers not in list.
        $sInsert->execute( $ProvID, $form->{Client_ClientID} );
        $Cnt++;
    }
    $sInsert->finish();
    $Results .= "<BR>Access added for $Cnt Providers." if ($Cnt);

    # set the real ClientACL table for this client
    #   all Client Access based on ClientACL, so we need to update it...
    #   it uses the Providers SiteACL + the ClientAccess to update ClientACL...
    #   and we just changed the CLientAccess table...
    SysAccess->rebldClientACL(
        $form,
        $form->{Client_ClientID},
        $form->{Client_ProvID}, 1
    );
    foreach my $ProvID ( split( chr(253), $form->{ACL_ProviderIDs} ) ) {

        #warn "ClientAccess: rebld: ${ProvID}, $form->{Client_ClientID})\n";
        SysAccess->rebldClientACL(
            $form,
            $form->{Client_ClientID},
            $form->{Client_ProvID},
            1, $ProvID
        );
    }

    # Change Primary Provider for this Client?
    if (   $form->{Client_ProvID}
        && $form->{Client_ProvID} ne $rClient->{ProvID} )
    {
      #warn "ClientAccess,update: Client set ProvID='$form->{Client_ProvID}'\n";
        my $sUpdate =
          $dbh->prepare("update Client set ProvID=? where ClientID=?");
        $sUpdate->execute( $form->{Client_ProvID}, $form->{Client_ClientID} );
        $sUpdate->finish();
        $Results .= "<BR>Primary Provider changed for this Client";
    }

    # Change Clinic for this Client?
    if (   $form->{Client_clinicClinicID}
        && $form->{Client_clinicClinicID} ne $rClient->{clinicClinicID} )
    {
#warn "ClientAccess,update: Client set clinicClinicID='$form->{Client_clinicClinicID}'\n";
        my $sUpdate =
          $dbh->prepare("update Client set clinicClinicID=? where ClientID=?");
        $sUpdate->execute( $form->{Client_clinicClinicID},
            $form->{Client_ClientID} );
        $sUpdate->finish();
        $Results .= "<BR>Assigned Clinic changed for this Client";
    }

  # set any UnApproved PAs for new Primary Provider (ie: PG030 or IndLBHP/Psych)
    PostUpd->updPA( $form, $form->{Client_ClientID} );

    $Results = 'No changes found.' if ( $Results eq '' );

    my $Location = myForm->popLINK();

    #warn qq|ClientAccess: Location=$Location\n|;
    print qq|Location: $Location\n\n|;
    return (1);
}
