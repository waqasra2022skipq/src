#!/usr/bin/perl
use lib '/var/www/okmis/src/lib';
use DBI;
use DBA;
use myForm;
use myDBI;
use DBUtil;
use SOAP::Lite ( maptype => {} );
use CGI::Carp qw(fatalsToBrowser);

#use SOAP::Lite ( +trace => all, maptype => {} );
#use SOAP::Lite ( +trace => [ transport => sub { print $_[0]->as_string } ] );

my $debug = 0;

###################################################################################
#$SOAP::Constants::DO_NOT_USE_CHARSET = 1;
my $form = myForm->new();
my $dbh  = myDBI->dbconnect( $form->{'DBNAME'} );

#foreach my $f ( sort keys %{$form} ) { warn "DMHws: form-$f=$form->{$f}\n"; }

##my $url = 'https://ww4.odmhsas.org/ErrorListWebService/service.asmx';
my $url = 'https://dmhwebservices.odmhsas.org/ErrorListWebService/Service.asmx';
my $myID        = $form->{'myID'};
my $table       = $form->{'action'};
my $ClientID    = $form->{'Client_ClientID'};
my $CDCID       = '';
my $error_nodes = '';
my $WebSupport =
  qq|\nContact DMH support\nDavid Melton: 405-522-3819 or DMelton\@odmhsas.org|;

#warn qq|DMHws: myID: ${myID}\n|;
#warn qq|DMHws: table: ${table}\n|;
#warn qq|DMHws: ClientID: ${ClientID}\n|;

my $sProvider = $dbh->prepare("select * from Provider where ProvID=?");
$sProvider->execute( $form->{'LOGINPROVID'} )
  || myDBI->dberror("DMHws: select Provider: $form->{'LOGINPROVID'}");
$rProvider = $sProvider->fetchrow_hashref;
$sProvider->finish();

my $reqtype = $table eq 'ClientDischarge' ? 'Discharge' : 'Prior Authorization';
my $location =
  $table eq 'ClientDischarge'
  ? qq|Location: /cgi/bin/mis.cgi?view=ListDischarges.cgi&Client_ClientID=${ClientID}&mlt=$form->{mlt}&misLINKS=$form->{misLINKS}\n\n|
  : qq|Location: /cgi/bin/mis.cgi?MIS_Action=ClientPage&Client_ClientID=${ClientID}&mlt=$form->{mlt}&misLINKS=$form->{misLINKS}\n\n|;

# first CHECK the Discharge or Prior Auth...
my $errmsg =
  $table eq 'ClientDischarge'
  ? CDC->setDIS( $form, $myID )
  : CDC->setPA( $form, $myID );
if ($debug) {
    DBA->setAlert( $form,
"DEBUG:\nTEST JQUERY.\nTest if the setAlert works OK\nWith the newlines and other stuff.\nLike multiple lines in a box\nHow big is the box and what size will it expand to if we write a long sentence that has many many words in it. \nDoes the box work OK?"
    );
    myDBI->cleanup();
    print $location;
    exit;
}

#warn qq|errmsg: ${errmsg}\n|;
if ( $errmsg ne '' ) {
    my $rUpdateCDC = ();
    $rUpdateCDC->{'StatusDate'} = $form->{'TODAY'};
    $rUpdateCDC->{'Fail'}       = qq|check FAILED: ${errmsg}|;
    $CDCID =
      DBA->doUpdate( $form, "${table}CDC", $rUpdateCDC, "${table}ID=${myID}",
        '', 1 );
    DBA->setAlert( $form, "check FAILED: ${errmsg}" );
    myDBI->cleanup();
    print $location;
    exit;
}
my $alertmsg = '';
my $rHDR     = ();
my $rHDRCDC  = ();
my $sHDR     = $dbh->prepare("select * from ${table} where ID=?");
$sHDR->execute($myID) || myDBI->dberror("DMHws: select ${table}: ${myID}");
if ( $rHDR = $sHDR->fetchrow_hashref ) {
    my $sHDRCDC = $dbh->prepare("select * from ${table}CDC where ${table}ID=?");
    $sHDRCDC->execute($myID)
      || myDBI->dberror("DMHws: select ClientPrAuthCDC: ${myID}");
    if ( $rHDRCDC = $sHDRCDC->fetchrow_hashref ) { null; }
    else { $errmsg = qq|Failed to read ClientPrAuthCDC-${myID}|; }
    $sHDRCDC->finish();
}
else { $errmsg = qq|Failed to read ${table}-${myID}|; }
$sHDR->finish();
$CDCID = $rHDRCDC->{'ID'};
my ( $userid2, $password2 ) =
  DBA->idDMH( $form, $rHDRCDC->{'AgencySite'}, $rHDRCDC->{'AgencyNum'} );
if (   $form->{'DBNAME'} eq 'okmis_dev'
    || $form->{'DBNAME'} eq 'okmms_dev'
    || $form->{'DBNAME'} eq 'okmis_demo' )
{
    $rHDRCDC->{'FirstName'}   = 'Mother';
    $rHDRCDC->{'InsIDNum'}    = '777777771';
    $rHDRCDC->{'DateOfBirth'} = '1980-01-01';
    if ( $ClientID == 52299 ) {
        $rHDRCDC->{'FirstName'}   = 'Mother';
        $rHDRCDC->{'InsIDNum'}    = '777777771';
        $rHDRCDC->{'DateOfBirth'} = '1980-01-01';
    }
    elsif ( $ClientID == 50396 ) {
        $rHDRCDC->{'FirstName'}   = 'Father';
        $rHDRCDC->{'InsIDNum'}    = '777777772';
        $rHDRCDC->{'DateOfBirth'} = '1980-01-01';
    }
    elsif ( $ClientID == 52045 ) {
        $rHDRCDC->{'FirstName'}   = 'Daughter';
        $rHDRCDC->{'InsIDNum'}    = '777777773';
        $rHDRCDC->{'DateOfBirth'} = '2000-01-01';
    }
    elsif ( $ClientID == 52438 ) {
        $rHDRCDC->{'FirstName'}   = 'Son';
        $rHDRCDC->{'InsIDNum'}    = '777777774';
        $rHDRCDC->{'DateOfBirth'} = '2000-01-01';
    }
    $rHDRCDC->{'LastName'} = 'TestClient';
    ##$url = 'https://ww1.odmhsas.org/ErrorListWebService/service.asmx';
    $url =
      'https://dmhwebservices.odmhsas.org/ErrorListWebServiceTest/Service.asmx';
    ( $userid2, $password2 ) = ( 'Millennium', 'M1ll3N1uM123' );
}
if ( $form->{'DBNAME'} eq 'okmis_dev' ) {
    warn qq|DMHws: $errmsg\n|;
    warn qq|DMHws: url=${url}\n|;
    warn qq|DMHws: ClientID=${ClientID}\n|;
    foreach my $f ( sort keys %{$rHDR} ) { warn ": rHDR-$f=$rHDR->{$f}\n"; }
    foreach my $f ( sort keys %{$rHDRCDC} ) {
        warn ": rHDRCDC-$f=$rHDRCDC->{$f}\n";
    }
}
if ( $errmsg eq '' ) {
    my $soap =
      SOAP::Lite->uri('http://tempuri.org')
      ->on_action( sub { join '/', 'http://tempuri.org', $_[1] } )
      ->readable(1)
      ->proxy($url);

    # modify the cipher list because of handshake issues with ASP.net
    $soap->{_transport}->{_proxy}->{ssl_opts}->{SSL_cipher_list} =
      'SHA:!NULL:!3DES:!DES:!ADH:!SRP';

    my $method = SOAP::Data->name('CDCPAErrors')
      ->attr( { xmlns => 'http://tempuri.org/' } );

    #warn qq|method=$method\n|;
    #warn qq|KLS: LastName=$rHDRCDC->{'LastName'}\n|;
    #warn qq|KLS: TransDate=$rHDRCDC->{'TransDate'}\n|;
    my @params = main->setParameters( $form, $rHDR, $rHDRCDC );
    my $result;

    #warn qq|KLS: setParameters is done...\n|;
    eval { $result = $soap->call( $method => @params ); };
    if ($@) {
        ( $errmsg, $rest ) = split( "at /home", $@, 2 );
        DBA->setAlert( $form, "Connection FAILED:\n${errmsg}\n${WebSupport}" );
        myDBI->cleanup();
        print $location;
        exit;
    }

    #warn qq|KLS: back from soap-call...\n|;
    if ( $result->fault ) {
        warn qq|faultstring=| . $result->faultstring . "\n";
        my ( $msg, $rest ) = split( "\r", $result->faultstring, 2 );
        $errmsg = qq|faultstring=${msg}\n|;
        my $rUpdateCDC = ();
        $rUpdateCDC->{'StatusDate'} = $form->{'TODAY'};
        $rUpdateCDC->{'Fail'}       = $errmsg;
        $CDCID = DBA->doUpdate( $form, "${table}CDC", $rUpdateCDC,
            "${table}ID=${myID}", '', 1 );
        delete $rHDRCDC->{"${table}ID"};    # remove ID to the HDR.
        $rHDRCDC->{"${table}CDCID"} = $CDCID;             # attach to the CDC.
        $rHDRCDC->{'StatusDate'}    = $form->{'TODAY'};
        $rHDRCDC->{'Fail'}          = $errmsg;
        my $LogID = DBA->doUpdate( $form, "${table}CDCSent", $rHDRCDC );
        $alertmsg = $errmsg;
    }
    else {
        # start test...,
        # errmsg / errfld= / ,
        # : node-BegDate=2016-09-14T00:00:00-05:00,
        # : node-CDCkey=3000863,
        # : node-Cost=483.0000,
        # : node-EndDate=2016-12-13T00:00:00-06:00,
        # : node-Length1=month,
        # : node-Length2=3,
        # : node-PAlines=1,
        # : node-PAnumber=4513102122,
        # : node-PAstatus=Instant,
        # : node-PGgroup=PG038,
        # : node-Units=0,
        # : node-errcode=,
        # : node-errmsg=,
        #warn qq|result=|.$result->result."\n";
        my @nodes = $result->valueof('//test');

        #warn qq|nodes=@nodes\n|;
        #warn qq|start test...\n|;
        my $rUpdate    = ();
        my $rUpdateCDC = ();
        foreach $node (@nodes) {

          #warn qq|errmsg/errfld=|.$node->{'errmsg'}."/".$node->{'errfld'}."\n";
          #warn qq|DMHws: PAstatus=|.$node->{'PAstatus'}."\n";
          #warn qq|DMHws: PGgroup=|.$node->{'PGgroup'}."\n";
            $errmsg .= qq|$node->{'errmsg'}\n| if ( $node->{'errmsg'} ne '' );

     #foreach my $f ( sort keys %{ $node } ) { warn ": node-$f=$node->{$f}\n"; }
            foreach my $f ( sort keys %{$node} ) {
                next
                  if ( $node->{$f} eq '' )
                  ;    # skip when they send us nulls, don't update
                if ( $f eq 'BegDate' )    #=2016-09-14T00:00:00-05:00,
                {
                    ( $rUpdate->{'EffDate'}, $time ) =
                      split( 'T', $node->{$f} );
                }
                elsif ( $f eq 'CDCkey' )     #=3000863,
                { $rUpdateCDC->{'CDCKey'} = $node->{$f}; }
                elsif ( $f eq 'Cost' )       #=483.0000,
                { $rUpdate->{'AuthAmt'} = $node->{$f}; }
                elsif ( $f eq 'EndDate' )    #=2016-12-13T00:00:00-06:00,
                {
                    ( $rUpdate->{'ExpDate'}, $time ) =
                      split( 'T', $node->{$f} );
                }
                elsif ( $f eq 'Length1' )     #=month,
                { $Length1 = $node->{$f}; }
                elsif ( $f eq 'Length2' )     #=3,
                { $rUpdate->{'LOS'} = $node->{$f}; }
                elsif ( $f eq 'PAlines' )     #=1,
                { $rUpdate->{'LinesAuth'} = $node->{$f}; }
                elsif ( $f eq 'PAnumber' )    #=4513102122,
                { $rUpdate->{'PAnumber'} = $node->{$f}; }
                elsif ( $f eq 'PAstatus' )    #=Instant,
                { $rUpdateCDC->{'Status'} = $node->{$f}; }
                elsif ( $f eq 'PGgroup' )     #=PG038,
                { $rUpdate->{'PAgroup'} = $node->{$f}; }
                elsif ( $f eq 'Units' )       #=0,
                { $rUpdate->{'UnitsAuth'} = $node->{$f}; }
                elsif ( $f eq 'Column1' )     #=Instant,
                {
                    if ( $node->{$f} eq 'Information Verified OK' ) {
                        $rUpdateCDC->{'Status'} = 'Verified';
                    }
                    else { $errmsg .= qq|$node->{$f}\n|; }
                }
                elsif ( $f eq 'HHresponse' ) {
                    $rUpdate->{'HHresponse'} = $node->{$f};
                }
                else { $error_nodes .= "node: ${f}=$node->{$f}"; }
            }
        }

        # fix certain Status coming in...
        # Status is always instant or saved.
        if ( $rUpdate->{'PAgroup'} =~ /ZZ/ ) {
            $rUpdateCDC->{'Status'} = 'Pending';
            $rUpdate->{'PAgroup'} =~ s/ZZ/PG/;
            $rUpdateCDC->{'Reason'} = 'Pending ZZ';
        }
        if ( $rUpdateCDC->{'Status'} =~ m/approved/i ) {
            $rUpdateCDC->{'Status'} = 'Approved';
        }
        if ( $rUpdateCDC->{'Status'} =~ m/instant/i ) {
            $rUpdateCDC->{'Status'} = 'Approved';
            $rUpdateCDC->{'Reason'} .= "Instant PA\n";
        }
        if ( $rUpdateCDC->{'Status'} =~ m/saved/i ) {
            $rUpdateCDC->{'Status'} =
              $rHDRCDC->{'TransType'} < 60 ? 'CDCONLY' : 'Approved';
            $rUpdateCDC->{'Reason'} .= "CDCONLY\n";
        }
        if ( $errmsg ne '' ) { $rUpdateCDC->{'Status'} = 'Rejected'; }

        #warn qq|DMHws: CDCID=${CDCID}\n|;
        # update Authorized? PA...
        my $writePA = $errmsg eq '' ? 1 : 0;
        if ($writePA) {
            if ( $rHDRCDC->{'TransType'} eq '27' ) {
                $rUpdate->{'PAgroup'} = 'CDCONLY'
                  if ( $rUpdate->{'PAgroup'} eq '' );
                $rUpdate->{'PAnumber'} = 'CDCONLY'
                  if ( $rUpdate->{'PAnumber'} eq '' );
                my $date =
                    $rUpdate->{'EffDate'} eq ''
                  ? $rHDR->{'EffDate'}
                  : $rUpdate->{'EffDate'};
                $rUpdate->{'ExpDate'} = DBUtil->Date( $date, 1, -1 )
                  if ( $rUpdate->{'ExpDate'} eq '' );
            }

            #warn qq|DMHws: myID=${myID}, errmsg=$errmsg\n|;
            $rUpdate->{'ChangeProvID'} = $form->{'LOGINPROVID'};

#foreach my $f ( sort keys %{$rUpdate} ) { warn "  ${table}: $f=$rUpdate->{$f}\n"; }
            my $ID1 = DBA->doUpdate( $form, $table, $rUpdate, "ID=${myID}" );
        }

#my @nodes = $result->valueof('//i');
#warn qq|nodes=@nodes\n|;
#warn qq|start i...\n|;
#foreach $node (@nodes) { foreach my $f ( sort keys %{ $node } ) { warn ": node-$f=$node->{$f}\n"; } }

        # FIX with list of errors code not to update CDC Status
        #   just update the Sent log.
        # : node-errcode=CDC90160,
        # : node-errfld=TransmissionType,
        # : node-errmsg=Customer already has a CDC for this exact date and time
        if (   $errmsg =~ /already has an open CDC/
            && $rHDRCDC->{'TransType'} < 60 )
        {
            $errmsg .= qq| (change TransType to 42)|;
        }
        elsif ($errmsg =~ /does not have an open CDC/
            && $rHDRCDC->{'TransType'} < 60 )
        {
            $errmsg .= qq| (change TransType to 23)|;
        }
        elsif ( $errmsg =~ /duplicate record already on file/ ) {
            $errmsg .= qq| (change TransDate/Time)|;
        }
        my $writeCDC = $rHDRCDC->{'Status'} eq 'Approved' ? 0 : 1;
        if ($writeCDC) {
            if ( $rUpdateCDC->{'Status'} eq '' ) {
                $rUpdateCDC->{'Status'} = $rHDRCDC->{'Status'};
            }
            $rUpdateCDC->{StatusDate}     = $form->{'TODAY'};
            $rUpdateCDC->{'Fail'}         = $errmsg;
            $rUpdateCDC->{'ChangeProvID'} = $form->{'LOGINPROVID'};

#foreach my $f ( sort keys %{$rUpdateCDC} ) { warn "  CDC: $f=$rUpdateCDC->{$f}\n"; }
            $CDCID = DBA->doUpdate( $form, "${table}CDC", $rUpdateCDC,
                "${table}ID=${myID}", '', 1 );
            my $lock = $errmsg eq '' ? 1 : 0;
            CDC->Lock( $form, $table, $myID, $lock );

            # set the PALines only for Approved PAs...
            Inv->setPALines( $form, $myID ) if ( rHDRCDC->{'TransType'} < 60 );

            #warn qq|NEAR END: errmsg=${errmsg}=\n|;
        }
        $alertmsg =
          $errmsg eq ''
          ? qq|Client ${reqtype}: $rUpdateCDC->{'Status'}|
          : $errmsg;

        #warn qq|NEAR END: alertmsg=${alertmsg}=\n|;
        my $rUpdateLog = ();

# copy below each value because if not $rUpdateLog=$rHDRCDC is the same reference.
#   and delete $rUpdateLog deletes from $rHDRCDC
        foreach my $f ( sort keys %{$rHDRCDC} ) {
            $rUpdateLog->{$f} = $rHDRCDC->{$f};
        }
        delete $rUpdateLog->{"${table}ID"};         # remove ID to the HDR.
        $rUpdateLog->{"${table}CDCID"} = $CDCID;    # attach to the CDC.
        $rUpdateLog->{'CDCKey'}        = $rUpdateCDC->{'CDCKey'};
        $rUpdateLog->{'Status'}        = $rUpdateCDC->{'Status'};
        $rUpdateLog->{'StatusDate'}    = $rUpdateCDC->{'StatusDate'};
        $rUpdateLog->{'Fail'}          = $rUpdateCDC->{'Fail'};
        $rUpdateLog->{'Reason'}        = $rUpdateCDC->{'Reason'};
        $rUpdateLog->{'ChangeProvID'}  = $rUpdateCDC->{'ChangeProvID'};
        $rUpdateLog->{'xmlstring'} = $soap->transport->http_response->as_string;
        my $LogID = DBA->doUpdate( $form, "${table}CDCSent", $rUpdateLog );
    }
}
else { $alertmsg = $errmsg; }

#warn qq|END: alertmsg=${alertmsg}\n|;
DBA->setAlert( $form, $alertmsg );

#if ( $error_nodes ne '' ) { DBUtil->email($form,'support@okmis.com',"ERROR DMHws: $form->{'DBNAME'}: $rHDRCDC->{'ClientID'}",$error_nodes); }

myDBI->cleanup();

print $location;
exit;

###################################################################################
sub setParameters {
    my ( $self, $form, $rHDR, $rHDRCDC ) = @_;

    #warn qq|setParameters: ClientID=$rHDRCDC->{'ClientID'}\n|;
    #warn qq|setParameters: LastName=$rHDRCDC->{'LastName'}\n|;
    #warn qq|setParameters: TransDate=$rHDRCDC->{'TransDate'}\n|;
    my @client = main->setCDC($rHDRCDC);
    my @pa     = main->setPA($rHDR);
    my @params = (
        SOAP::Data->name('i')->value(
            \SOAP::Data->value(
                SOAP::Data->name('_userid')->value('dmhwebsrv'),
                SOAP::Data->name('_password')->value('B90wR2k'),
                SOAP::Data->name('_userid2')->value($userid2),
                SOAP::Data->name('_password2')->value($password2),
                SOAP::Data->name('_mode')->value('Add'),
                SOAP::Data->name('_provideridloc')
                  ->value( $rHDRCDC->{'AgencySite'} ),
                @client,
                @pa,
            )
        ),
    );
    return (@params);
}

sub setCDC {
    my ( $self, $rSend ) = @_;
    my @CDC = ();
    push( @CDC,
        SOAP::Data->name('_Harm_Int')->value( $rSend->{'Harmfulintent'} ) );
    push( @CDC,
        SOAP::Data->name('_recipient_id')->value( $rSend->{'InsIDNum'} ) )
      if ( $rSend->{'InsIDNum'} ne '' );
    push( @CDC,
        SOAP::Data->name('_birthdate')->value( $rSend->{'DateOfBirth'} ) )
      if ( $rSend->{'DateOfBirth'} ne '' );
    push( @CDC, SOAP::Data->name('_gender')->value( $rSend->{'Gend'} ) )
      if ( $rSend->{'Gend'} ne '' );
    push( @CDC, SOAP::Data->name('_email')->value( $rSend->{'Email'} ) )
      if ( $rSend->{'Email'} ne '' );
    push( @CDC, SOAP::Data->name('_transdate')->value( $rSend->{'TransDate'} ) )
      if ( $rSend->{'TransDate'} ne '' );
    my $time = substr( $rSend->{'TransTime'}, 0, 2 )
      . substr( $rSend->{'TransTime'}, 3, 2 );
    push( @CDC, SOAP::Data->name('_transtime')->value($time) )
      if ( $time ne '' );
    push( @CDC, SOAP::Data->name('_transtype')->value( $rSend->{'TransType'} ) )
      if ( $rSend->{'TransType'} ne '' );
    push( @CDC,
        SOAP::Data->name('_servfocus')->value( $rSend->{'ServiceFocus'} ) )
      if ( $rSend->{'ServiceFocus'} ne '' );
    push( @CDC, SOAP::Data->name('_racewhite')->value( $rSend->{'RaceWhite'} ) )
      if ( $rSend->{'RaceWhite'} ne '' );
    push( @CDC, SOAP::Data->name('_raceblack')->value( $rSend->{'RaceBlack'} ) )
      if ( $rSend->{'RaceBlack'} ne '' );
    push( @CDC,
        SOAP::Data->name('_raceindian')->value( $rSend->{'RaceIndian'} ) )
      if ( $rSend->{'RaceIndian'} ne '' );
    push( @CDC,
        SOAP::Data->name('_racehawaiian')->value( $rSend->{'EthnicIslander'} ) )
      if ( $rSend->{'EthnicIslander'} ne '' );
    push( @CDC, SOAP::Data->name('_raceasian')->value( $rSend->{'RaceAsian'} ) )
      if ( $rSend->{'RaceAsian'} ne '' );
    push( @CDC,
        SOAP::Data->name('_hispanlatino')->value( $rSend->{'EthnicHispanic'} ) )
      if ( $rSend->{'EthnicHispanic'} ne '' );
    push( @CDC, SOAP::Data->name('_mhscreen')->value( $rSend->{'MHScreen'} ) )
      if ( $rSend->{'MHScreen'} ne '' );
    push( @CDC, SOAP::Data->name('_sascreen')->value( $rSend->{'SAScreen'} ) )
      if ( $rSend->{'SAScreen'} ne '' );
    push( @CDC,
        SOAP::Data->name('_traumascreen')->value( $rSend->{'TraumaScreen'} ) )
      if ( $rSend->{'TraumaScreen'} ne '' );
    push( @CDC,
        SOAP::Data->name('_traumascore')->value( $rSend->{'traumaScore'} ) )
      if ( $rSend->{'traumaScore'} ne '' );
    push( @CDC,
        SOAP::Data->name('_gamblingscreen')->value( $rSend->{'GamblingScreen'} )
    ) if ( $rSend->{'GamblingScreen'} ne '' );
    push( @CDC, SOAP::Data->name('_alert')->value( $rSend->{'Alert'} ) )
      if ( $rSend->{'Alert'} ne '' );
    push( @CDC,
        SOAP::Data->name('_primref')->value( $rSend->{'PriReferralType'} ) )
      if ( $rSend->{'PriReferralType'} ne '' );
    push( @CDC,
        SOAP::Data->name('_primrefag')->value( $rSend->{'PriReferralNPI'} ) )
      if ( $rSend->{'PriReferralNPI'} ne '' );
    push( @CDC,
        SOAP::Data->name('_secref')->value( $rSend->{'SecReferralType'} ) )
      if ( $rSend->{'SecReferralType'} ne '' );
    push( @CDC,
        SOAP::Data->name('_secrefag')->value( $rSend->{'SecReferralNPI'} ) )
      if ( $rSend->{'SecReferralNPI'} ne '' );
    push( @CDC,
        SOAP::Data->name('_countyres')->value( $rSend->{'CountyofRes'} ) )
      if ( $rSend->{'CountyofRes'} ne '' );
    push( @CDC, SOAP::Data->name('_zipcode')->value( $rSend->{'Zip'} ) )
      if ( $rSend->{'Zip'} ne '' );
    push( @CDC, SOAP::Data->name('_famident')->value( $rSend->{'FamilyID'} ) )
      if ( $rSend->{'FamilyID'} ne '' );
    push( @CDC, SOAP::Data->name('_probprim')->value( $rSend->{'Problem1'} ) )
      if ( $rSend->{'Problem1'} ne '' );
    push( @CDC, SOAP::Data->name('_probsec')->value( $rSend->{'Problem2'} ) )
      if ( $rSend->{'Problem2'} ne '' );
    push( @CDC, SOAP::Data->name('_probtert')->value( $rSend->{'Problem3'} ) )
      if ( $rSend->{'Problem3'} ne '' );
    push( @CDC, SOAP::Data->name('_lname')->value( $rSend->{'LastName'} ) )
      if ( $rSend->{'LastName'} ne '' );
    push( @CDC, SOAP::Data->name('_maiden')->value( $rSend->{'MaidenName'} ) )
      if ( $rSend->{'MaidenName'} ne '' );
    push( @CDC, SOAP::Data->name('_fname')->value( $rSend->{'FirstName'} ) )
      if ( $rSend->{'FirstName'} ne '' );
    push( @CDC, SOAP::Data->name('_mi')->value( $rSend->{'MiddleName'} ) )
      if ( $rSend->{'MiddleName'} ne '' );
    push( @CDC, SOAP::Data->name('_suffix')->value( $rSend->{'Suffix'} ) )
      if ( $rSend->{'Suffix'} ne '' );
    push( @CDC, SOAP::Data->name('_address1')->value( $rSend->{'Addr1'} ) )
      if ( $rSend->{'Addr1'} ne '' );
    push( @CDC, SOAP::Data->name('_address2')->value( $rSend->{'Addr2'} ) )
      if ( $rSend->{'Addr2'} ne '' );
    push( @CDC, SOAP::Data->name('_city')->value( $rSend->{'City'} ) )
      if ( $rSend->{'City'} ne '' );
    push( @CDC, SOAP::Data->name('_state')->value( $rSend->{'State'} ) )
      if ( $rSend->{'State'} ne '' );
    push( @CDC,
        SOAP::Data->name('_residcur')->value( $rSend->{'CurrentResidence'} ) )
      if ( $rSend->{'CurrentResidence'} ne '' );
    push( @CDC,
        SOAP::Data->name('_custodydoc')
          ->value( $rSend->{'IncarcerationStatus'} ) )
      if ( $rSend->{'IncarcerationStatus'} ne '' );
    push( @CDC,
        SOAP::Data->name('_livsitcur')->value( $rSend->{'LivingSituation'} ) )
      if ( $rSend->{'LivingSituation'} ne '' );
    push( @CDC,
        SOAP::Data->name('_chronichomeless')
          ->value( $rSend->{'AlertCHomeless'} ) )
      if ( $rSend->{'AlertCHomeless'} ne '' );
    push( @CDC, SOAP::Data->name('_employcur')->value( $rSend->{'EmplStat'} ) )
      if ( $rSend->{'EmplStat'} ne '' );
    push( @CDC, SOAP::Data->name('_emptypecur')->value( $rSend->{'EmplType'} ) )
      if ( $rSend->{'EmplType'} ne '' );
    push( @CDC, SOAP::Data->name('_education')->value( $rSend->{'Education'} ) )
      if ( $rSend->{'Education'} ne '' );
    push( @CDC, SOAP::Data->name('_inschool')->value( $rSend->{'InSchool'} ) )
      if ( $rSend->{'InSchool'} ne '' );
    push( @CDC, SOAP::Data->name('_marital')->value( $rSend->{'MarStat'} ) )
      if ( $rSend->{'MarStat'} ne '' );
    push( @CDC, SOAP::Data->name('_alertpreg')->value( $rSend->{'Pregnant'} ) )
      if ( $rSend->{'Pregnant'} ne '' );
    push( @CDC,
        SOAP::Data->name('_duedate')->value( $rSend->{'PregnantDate'} ) )
      if ( $rSend->{'PregnantDate'} ne '' );
    push( @CDC, SOAP::Data->name('_income')->value( $rSend->{'AnnualIncome'} ) )
      if ( $rSend->{'AnnualIncome'} ne '' );
    push( @CDC, SOAP::Data->name('_numlivho')->value( $rSend->{'IncomeDeps'} ) )
      if ( $rSend->{'IncomeDeps'} ne '' );
    push( @CDC, SOAP::Data->name('_benssi')->value( $rSend->{'SSI'} ) )
      if ( $rSend->{'SSI'} ne '' );
    push( @CDC, SOAP::Data->name('_benssdi')->value( $rSend->{'SSDI'} ) )
      if ( $rSend->{'SSDI'} ne '' );
    push( @CDC,
        SOAP::Data->name('_speakengl')->value( $rSend->{'LangEnglish'} ) )
      if ( $rSend->{'LangEnglish'} ne '' );
    push( @CDC, SOAP::Data->name('_langpref')->value( $rSend->{'LangOther'} ) )
      if ( $rSend->{'LangOther'} ne '' );
    push( @CDC,
        SOAP::Data->name('_disability1')->value( $rSend->{'Handicap1'} ) )
      if ( $rSend->{'Handicap1'} ne '' );
    push( @CDC,
        SOAP::Data->name('_disability2')->value( $rSend->{'Handicap2'} ) )
      if ( $rSend->{'Handicap2'} ne '' );
    push( @CDC,
        SOAP::Data->name('_disability3')->value( $rSend->{'Handicap3'} ) )
      if ( $rSend->{'Handicap3'} ne '' );
    push( @CDC,
        SOAP::Data->name('_disability4')->value( $rSend->{'Handicap4'} ) )
      if ( $rSend->{'Handicap4'} ne '' );
    push( @CDC,
        SOAP::Data->name('_veteran')->value( $rSend->{'MilitaryStatus'} ) )
      if ( $rSend->{'MilitaryStatus'} ne '' );
    push( @CDC,
        SOAP::Data->name('_legalstat')->value( $rSend->{'LegalStatus'} ) )
      if ( $rSend->{'LegalStatus'} ne '' );
    push( @CDC,
        SOAP::Data->name('_countycom')->value( $rSend->{'CommitmentCounty'} ) )
      if ( $rSend->{'CommitmentCounty'} ne '' );
    push( @CDC,
        SOAP::Data->name('_cde_tobacco')->value( $rSend->{'TobaccoUse'} ) )
      if ( $rSend->{'TobaccoUse'} ne '' );
    push( @CDC, SOAP::Data->name('_drugch1')->value( $rSend->{'Drug1'} ) )
      if ( $rSend->{'Drug1'} ne '' );
    push( @CDC, SOAP::Data->name('_drugch2')->value( $rSend->{'Drug2'} ) )
      if ( $rSend->{'Drug2'} ne '' );
    push( @CDC, SOAP::Data->name('_drugch3')->value( $rSend->{'Drug3'} ) )
      if ( $rSend->{'Drug3'} ne '' );
    push( @CDC, SOAP::Data->name('_drugrte1')->value( $rSend->{'Route1'} ) )
      if ( $rSend->{'Route1'} ne '' );
    push( @CDC, SOAP::Data->name('_drugrte2')->value( $rSend->{'Route2'} ) )
      if ( $rSend->{'Route2'} ne '' );
    push( @CDC, SOAP::Data->name('_drugrte3')->value( $rSend->{'Route3'} ) )
      if ( $rSend->{'Route3'} ne '' );
    push( @CDC, SOAP::Data->name('_drugfreq1')->value( $rSend->{'Freq1'} ) )
      if ( $rSend->{'Freq1'} ne '' );
    push( @CDC, SOAP::Data->name('_drugfreq2')->value( $rSend->{'Freq2'} ) )
      if ( $rSend->{'Freq2'} ne '' );
    push( @CDC, SOAP::Data->name('_drugfreq3')->value( $rSend->{'Freq3'} ) )
      if ( $rSend->{'Freq3'} ne '' );
    push( @CDC, SOAP::Data->name('_drugage1')->value( $rSend->{'Age1'} ) )
      if ( $rSend->{'Age1'} ne '' );
    push( @CDC, SOAP::Data->name('_drugage2')->value( $rSend->{'Age2'} ) )
      if ( $rSend->{'Age2'} ne '' );
    push( @CDC, SOAP::Data->name('_drugage3')->value( $rSend->{'Age3'} ) )
      if ( $rSend->{'Age3'} ne '' );
    push( @CDC,
        SOAP::Data->name('_sublevcare')->value( $rSend->{'LevelOfCare'} ) )
      if ( $rSend->{'LevelOfCare'} ne '' );
    push( @CDC, SOAP::Data->name('_carmood')->value( $rSend->{'CAR1'} ) )
      if ( $rSend->{'CAR1'} ne '' );
    push( @CDC, SOAP::Data->name('_carthink')->value( $rSend->{'CAR2'} ) )
      if ( $rSend->{'CAR2'} ne '' );
    push( @CDC, SOAP::Data->name('_carsubuse')->value( $rSend->{'CAR3'} ) )
      if ( $rSend->{'CAR3'} ne '' );
    push( @CDC, SOAP::Data->name('_carmed')->value( $rSend->{'CAR4'} ) )
      if ( $rSend->{'CAR4'} ne '' );
    push( @CDC, SOAP::Data->name('_carfam')->value( $rSend->{'CAR5'} ) )
      if ( $rSend->{'CAR5'} ne '' );
    push( @CDC, SOAP::Data->name('_carintper')->value( $rSend->{'CAR6'} ) )
      if ( $rSend->{'CAR6'} ne '' );
    push( @CDC, SOAP::Data->name('_carrole')->value( $rSend->{'CAR7'} ) )
      if ( $rSend->{'CAR7'} ne '' );
    push( @CDC, SOAP::Data->name('_carsocleg')->value( $rSend->{'CAR8'} ) )
      if ( $rSend->{'CAR8'} ne '' );
    push( @CDC, SOAP::Data->name('_carself')->value( $rSend->{'CAR9'} ) )
      if ( $rSend->{'CAR9'} ne '' );
    push( @CDC,
        SOAP::Data->name('_asimednew')->value( $rSend->{'ASIMedical'} ) )
      if ( $rSend->{'ASIMedical'} ne '' );
    push( @CDC, SOAP::Data->name('_asiempnew')->value( $rSend->{'ASIEmploy'} ) )
      if ( $rSend->{'ASIEmploy'} ne '' );
    push( @CDC,
        SOAP::Data->name('_asialcnew')->value( $rSend->{'ASIAlcohol'} ) )
      if ( $rSend->{'ASIAlcohol'} ne '' );
    push( @CDC, SOAP::Data->name('_asidrugnew')->value( $rSend->{'ASIDrug'} ) )
      if ( $rSend->{'ASIDrug'} ne '' );
    push( @CDC,
        SOAP::Data->name('_asilegalnew')->value( $rSend->{'ASILegal'} ) )
      if ( $rSend->{'ASILegal'} ne '' );
    push( @CDC,
        SOAP::Data->name('_asifamilynew')->value( $rSend->{'ASIFamily'} ) )
      if ( $rSend->{'ASIFamily'} ne '' );
    push( @CDC,
        SOAP::Data->name('_asipsychnew')->value( $rSend->{'ASIPsych'} ) )
      if ( $rSend->{'ASIPsych'} ne '' );
    push( @CDC, SOAP::Data->name('_tasia')->value( $rSend->{'TASIChemical'} ) )
      if ( $rSend->{'TASIChemical'} ne '' );
    push( @CDC, SOAP::Data->name('_tasib')->value( $rSend->{'TASISchool'} ) )
      if ( $rSend->{'TASISchool'} ne '' );
    push( @CDC, SOAP::Data->name('_tasic')->value( $rSend->{'TASIEmploy'} ) )
      if ( $rSend->{'TASIEmploy'} ne '' );
    push( @CDC, SOAP::Data->name('_tasid')->value( $rSend->{'TASIFamily'} ) )
      if ( $rSend->{'TASIFamily'} ne '' );
    push( @CDC, SOAP::Data->name('_tasie')->value( $rSend->{'TASIPeer'} ) )
      if ( $rSend->{'TASIPeer'} ne '' );
    push( @CDC, SOAP::Data->name('_tasif')->value( $rSend->{'TASILegal'} ) )
      if ( $rSend->{'TASILegal'} ne '' );
    push( @CDC, SOAP::Data->name('_tasig')->value( $rSend->{'TASIPsych'} ) )
      if ( $rSend->{'TASIPsych'} ne '' );
    push( @CDC, SOAP::Data->name('_ace')->value( $rSend->{'ACEScore'} ) )
      if ( $rSend->{'ACEScore'} ne '' );
    push( @CDC, SOAP::Data->name('_smi')->value( $rSend->{'SMI'} ) )
      if ( $rSend->{'SMI'} ne '' );
    push( @CDC, SOAP::Data->name('_sed')->value( $rSend->{'SED'} ) )
      if ( $rSend->{'SED'} ne '' );
    push( @CDC,
        SOAP::Data->name('_arrested30days')->value( $rSend->{'Arrested30'} ) )
      if ( $rSend->{'Arrested30'} ne '' );
    push( @CDC,
        SOAP::Data->name('_arrested12months')->value( $rSend->{'Arrested12'} ) )
      if ( $rSend->{'Arrested12'} ne '' );
    push( @CDC,
        SOAP::Data->name('_SHG_30Days')->value( $rSend->{'SelfHelp30'} ) )
      if ( $rSend->{'SelfHelp30'} ne '' );
    push( @CDC,
        SOAP::Data->name('_clinician')->value( $rSend->{'ClinicianOfRecord'} ) )
      if ( $rSend->{'ClinicianOfRecord'} ne '' );
    push( @CDC, SOAP::Data->name('_outofhome')->value( $rSend->{'Placement'} ) )
      if ( $rSend->{'Placement'} ne '' );
    push( @CDC,
        SOAP::Data->name('_NUM_RST_PLCMNT')
          ->value( $rSend->{'RestrictivePlacement'} ) )
      if ( $rSend->{'RestrictivePlacement'} ne '' );
    push( @CDC,
        SOAP::Data->name('_NUM_SELF_HARM')->value( $rSend->{'SelfHarm'} ) )
      if ( $rSend->{'SelfHarm'} ne '' );
    push( @CDC,
        SOAP::Data->name('_NUM_ABSENT_SCH')->value( $rSend->{'AbsentSchool'} ) )
      if ( $rSend->{'AbsentSchool'} ne '' );
    push( @CDC,
        SOAP::Data->name('_NUM_SUSP_SCH')->value( $rSend->{'SuspendedSchool'} )
    ) if ( $rSend->{'SuspendedSchool'} ne '' );
    push( @CDC,
        SOAP::Data->name('_NUM_ABSENT_DC')->value( $rSend->{'AbsentDayCare'} ) )
      if ( $rSend->{'AbsentDayCare'} ne '' );
    my $updatedby = qq|$rProvider->{'FName'} $rProvider->{'LName'}|;
    push( @CDC, SOAP::Data->name('_updatedby')->value($updatedby) )
      if ( $updatedby ne '' );
    push( @CDC, SOAP::Data->name('_CDCRecordId')->value( $rSend->{'CDCKey'} ) )
      if ( $rSend->{'CDCKey'} ne '' );
    return (@CDC);
}
##################################################################################
sub setPA {
    my ( $self, $rSend ) = @_;

    # transmissiontype: 1=CDCONLY, 3=CDCPA
    my $NeedPA =
        $rSend->{'TransType'} =~ /21|27/ ? 1
      : $rSend->{'TransType'} >= 60      ? 1
      :                                    3;
    my @PA = ();
    return (@PA) unless ($NeedPA);

    push( @PA, SOAP::Data->name('_PG_group')->value( $rSend->{'PAgroup'} ) )
      if ( $rSend->{'PAgroup'} ne '' );
    push( @PA, SOAP::Data->name('_PA_begdate')->value( $rSend->{'EffDate'} ) )
      if ( $rSend->{'EffDate'} ne '' );
    push( @PA, SOAP::Data->name('_PA_SOGSGSI')->value( $rSend->{'SOGSGSI'} ) )
      if ( $rSend->{'SOGSGSI'} ne '' );
    push( @PA,
        SOAP::Data->name('_PA_Diag1Prim')->value( $rSend->{'Diag1Prim'} ) )
      if ( $rSend->{'Diag1Prim'} ne '' );
    push( @PA, SOAP::Data->name('_PA_Diag1Sec')->value( $rSend->{'Diag1Sec'} ) )
      if ( $rSend->{'Diag1Sec'} ne '' );
    push( @PA,
        SOAP::Data->name('_PA_Diag1Tert')->value( $rSend->{'Diag1Tert'} ) )
      if ( $rSend->{'Diag1Tert'} ne '' );
    push( @PA,
        SOAP::Data->name('_PA_Diag2Prim')->value( $rSend->{'Diag2Prim'} ) )
      if ( $rSend->{'Diag2Prim'} ne '' );
    push( @PA, SOAP::Data->name('_PA_Diag2Sec')->value( $rSend->{'Diag2Sec'} ) )
      if ( $rSend->{'Diag2Sec'} ne '' );
    push( @PA, SOAP::Data->name('_PA_Diag3')->value( $rSend->{'Diag3'} ) )
      if ( $rSend->{'Diag3'} ne '' );
    push( @PA, SOAP::Data->name('_PA_number')->value( $rSend->{'PAnumber'} ) )
      if ( $rSend->{'PAnumber'} ne '' );
    push( @PA, SOAP::Data->name('_PA_transmissiontype')->value($NeedPA) )
      if ( $NeedPA ne '' );
    return (@PA);
}
