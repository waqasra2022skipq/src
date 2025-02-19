#!/usr/bin/perl
use lib '/var/www/okmis/src/lib';
use DBI;
use DBForm;
use DBA;
use DBUtil;
use SOAP::Lite ( maptype => {} );

#use SOAP::Lite ( +trace => all, maptype => {} );
###################################################################################
# EXAMPLE
# POST /ErrorListWebService/service.asmx HTTP/1.1
# Host: ww1.odmhsas.org
# Content-Type: text/xml; charset=utf-8
# Content-Length: length
# SOAPAction: "http://tempuri.org/Notifications"
#
# <?xml version="1.0" encoding="utf-8"?>
# <soap:Envelope xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns:xsd="http://www.w3.org/2001/XMLSchema" xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/">
#   <soap:Body>
#     <Notifications xmlns="http://tempuri.org/">
#       <i>
#         <_userid>string</_userid>
#         <_password>string</_password>
#         <_userid2>string</_userid2>
#         <_password2>string</_password2>
#         <_provideridloc>string</_provideridloc>
#         <_requestKey>string</_requestKey>
#         <_errors>string</_errors>
#         <_errcnt>int</_errcnt>
#       </i>
#     </Notifications>
#   </soap:Body>
# </soap:Envelope>
###################################################################################
my $form = DBForm->new();

#foreach my $f ( sort keys %{$form} ) { print "DMHloc: form-$f=$form->{$f}\n"; }
my $dbh        = $form->dbconnect();
my $AgencySite = $form->{'AgencySite'};    # PIN
my $AgencyNum  = $form->{'AgencyNum'};     # 0=Individual, 1=Agency
my $WebSupport =
  qq|\nContact DMH support\nDavid Melton: 405-522-3819 or DMelton\@odmhsas.org|;
my $test =
     $form->{'DBNAME'} eq 'okmisorg_devmms'
  || $form->{'DBNAME'} eq 'okmisorg_devoays'
  || $form->{'DBNAME'} eq 'okmis_demo'
  || $form->{'DBNAME'} eq 'okmms_dev' ? 1 : 0;
my @notes = (
    '',
'this is when your provider has an open level PA, and someone else enters a 21',
    'your provider entered a 21, but they have an open level somewhere else',
'this is when your provider has an open level PA, and someone enters a level PA on them',
'other provider ended their level PA, and your PA was on pended status. PA is now active.',
'you terminated another provider, now that provider is contesting the termination',
    'other agency proposed a collaboration',
    'other agency accepted your collaboration proposal',
    'other agency ended your PA, as of today that PA is ended',
'you had an active collaboration, but the other provider cancelled it, now you get the full amount of your PA on what is remaining',
'other agency voluntarily ended their own PA, you entered a PG038 which is why you are notified',
    'when collaboration is active, but other provider requested a change',
'you entered a 21 on a person that is already being seen at two other agencies. Level PA will not be allowed.',
'you entered an update PA that could not be updated by the current collaboration agreement.  You will need to renegotiate the collaboration.',
'Customer has a level PA at another agency, collaboration needed. You got this because you submitted a level PA for the customer and that PA is now on pended status.',
    'other agency deleted their pended PA',
'you accepted a collaboration. This comes back in the initial response. This is still sent in the notifications in case someone updates PICIS outside of your system.',
'you sent us a termination, and we activated your PA. This is also a duplicate response.',
'your provider entered a PA adjustment to change the PA, this will send you the details.'
);
my ( $hdrcnt, $errmsg, $saveLog ) = ( 0, '', 0 );
print qq|DBNAME=$form->{DBNAME}\n|;
print qq|AgencySite=${AgencySite}\n|;
print qq|AgencyNum=${AgencyNum}\n|;
print qq|test=${test}\n|;

my $url =
  $test
  ? 'https://dmhwebservices.odmhsas.org/ErrorListWebServiceTest/Service.asmx'
  : 'https://dmhwebservices.odmhsas.org/ErrorListWebService/Service.asmx';
my $soap =
  SOAP::Lite->uri('http://tempuri.org')
  ->on_action( sub { join '/', 'http://tempuri.org', $_[1] } )
  ->readable(1)
  ->proxy($url);

# modify the cipher list because of handshake issues with ASP.net
$soap->{_transport}->{_proxy}->{ssl_opts}->{SSL_cipher_list} =
  'SHA:!NULL:!3DES:!DES:!ADH:!SRP';

my $method =
  SOAP::Data->name('Notifications')->attr( { xmlns => 'http://tempuri.org/' } );

#print qq|method=$method\n|;
my $token = $form->{'TODAY'} . '_' . DBUtil->genToken();

#$token = $test ? 'dmhtest1' : 'prodtest1';
print qq|token=${token}\n|;
my @params = main->setParameters( $form, $AgencySite, $AgencyNum, $token );
my $result;
my @Header;
my @Detail;

#print qq|KLS: setParameters is done...\n|;
eval { $result = $soap->call( $method => @params ); };
if ($@) {
    $form->complete();
    ( $errmsg, $rest ) = split( "at /home", $@, 2 );
    print qq|Connection FAILED:\n${errmsg}\n${WebSupport}\n|;
    exit;
}

#print qq|KLS: back from soap-call...\n|;
if ( $result->fault ) {
    print qq|faultstring=| . $result->faultstring . "\n";
    my ( $msg, $rest ) = split( "\r", $result->faultstring, 2 );
    $errmsg = qq|faultstring=${msg}\n|;
}
else {
    my $sClientPrAuthCDC =
      $dbh->prepare("select * from ClientPrAuthCDC where CDCKey=?");

    #foreach $xml (@xml) { main->prtHASH($xml); }
    @Header = $result->valueof('//Header');
    @Detail = $result->valueof('//Detail');
    foreach $Header (@Header) {
        $hdrcnt++;
        my $CDCKey = $Header->{'CDCkey'};
        if ( $CDCKey eq '' ) {
            $errmsg .=
              $hdrcnt == 1
              ? qq|hdrcnt=${hdrcnt}|
              : qq|ERROR: NOCDCKey: hdrcnt=${hdrcnt}|;
        }
        else {
            print qq|FIND: CDCKey=${CDCKey}=\n|;
            $sClientPrAuthCDC->execute($CDCKey);
            if ( my $rClientPrAuthCDC = $sClientPrAuthCDC->fetchrow_hashref ) {
                main->updCDCPA( $form, $Header, $rClientPrAuthCDC );
            }
            else {
                print qq|
ClientPrAuthCDC MISSING:
  CDCKey=${CDCKey}
  PA_Number=$Header->{'PA_Number'}
  Provideridloc=$Header->{'Provideridloc'}
  Recipient_id=$Header->{'Recipient_id'}
|;
            }
            $saveLog = 1;
        }
    }
    $sClientPrAuthCDC->finish();
}

# save to the DMHLog to show we got an update...
if ($saveLog) {
    my $rDMHLog = ();
    $rDMHLog->{'CreateDate'}   = $form->{'TODAY'};
    $rDMHLog->{'CreateProvID'} = $form->{'LOGINPROVID'};
    $rDMHLog->{'ChangeProvID'} = $form->{'LOGINPROVID'};
    $rDMHLog->{'AgencySite'}   = $AgencySite;
    $rDMHLog->{'AgencyNum'}    = $AgencyNum;
    $rDMHLog->{'requestKey'}   = $token;
    $rDMHLog->{'xmlstring'}    = $soap->transport->http_response->as_string;

#print qq|xmlstring: $rDMHLog->{'xmlstring'}\nxmlstring:\n|;
#foreach my $f ( sort keys %{$rDMHLog} ) { print "  saveLog: rDMHLog: $f=$rDMHLog->{$f}\n"; }
    my $LogID = DBA->doUpdate( $form, "DMHLog", $rDMHLog );
}
$form->complete();
print qq|DONE: ${errmsg}\n|;
exit;

###################################################################################
sub setParameters {
    my ( $self, $form, $loc, $isAgency, $key ) = @_;
    my ( $userid2, $password2 ) = DBA->idDMH( $form, $loc, $isAgency );
    if ($test) { ( $userid2, $password2 ) = ( 'Millennium', 'M1ll3N1uM123' ); }

    #print qq|setParameters: loc=$loc\n|;
    #print qq|setParameters: key=$key\n|;
    my @params = (
        SOAP::Data->name('i')->value(
            \SOAP::Data->value(
                SOAP::Data->name('_userid')->value('dmhwebsrv'),
                SOAP::Data->name('_password')->value('B90wR2k'),
                SOAP::Data->name('_userid2')->value($userid2),
                SOAP::Data->name('_password2')->value($password2),
                SOAP::Data->name('_provideridloc')->value($loc),
                SOAP::Data->name('_requestKey')->value($key),

                #         <_errors>string</_errors>
                #         <_errcnt>int</_errcnt>
            )
        ),
    );
    return (@params);
}

sub updCDCPA {
    my ( $self, $form, $rHeader, $rCDC ) = @_;

    #print qq|BEGIN: updCDCPA ======\n|;
    #print qq|updCDCPA: PrAuthID=$rCDC->{'ClientPrAuthID'}\n|;
    foreach my $f ( sort keys %{$rHeader} ) {
        print "updCDCPA: rHeader-$f=$rHeader->{$f}\n";
    }
    my $PrAuthID         = $rCDC->{'ClientPrAuthID'};
    my $PAnumber         = $rHeader->{'PA_Number'};
    my $NotificationKey  = $rHeader->{'NotificationKey'};
    my $NotificationType = $rHeader->{'NotificationType'};
    my $EmailHeader      = $rHeader->{'EmailHeader'};
    main->updCDC( $form, $PAnumber, $NotificationType, $EmailHeader, $rCDC );
    my $rPA = main->updLines( $form, $NotificationKey, $rCDC );
    $rPA->{'ChangeProvID'}     = 91;
    $rPA->{'PAnumber'}         = $PAnumber if ( $PAnumber ne '' );
    $rPA->{'NotificationType'} = $NotificationType
      if ( $NotificationType ne '' );
    foreach my $f ( sort keys %{$rPA} ) { print "  updPA: $f=$rPA->{$f}\n"; }
    my $UID = DBA->doUpdate( $form, 'ClientPrAuth', $rPA, "ID=$PrAuthID" );

    #print qq|END updCDCPA UID=${UID}======\n|;
    return ();
}

# we can add proposed1=our Agency
#            proposed2=other Agency
# Notification 22 – this is when the HH high intensity customer is lowered to moderate intensity and locked
# Notification 23 – this is when the locked customer is meeting high criteria and it is less than six months
# Notification 24 – this is when the locked customer is meeting high criteria and it is more than six months
#      || $NotificationType == 24 )    # Health Home, Customer no change.
# to the CDC table
sub updCDC {
    my ( $self, $form, $PAnumber, $NotificationType, $EmailHeader, $rCDC ) = @_;

#print qq|  ENTER updCDC: PAnumber=${PAnumber}, NotificationType=${NotificationType}, EmailHeader=${EmailHeader}\n|;
    my $dbh      = $form->dbconnect();
    my $PrAuthID = $rCDC->{'ClientPrAuthID'};
    my $Status   = $rCDC->{'Status'};

    #print qq|  updCDC: PrAuthID=${PrAuthID}, Status=${Status}\n|;
    my $rUpdateCDC = ();
    $rUpdateCDC->{'Status'}       = $rCDC->{'Status'};
    $rUpdateCDC->{'StatusDate'}   = $rCDC->{'StatusDate'};
    $rUpdateCDC->{'ChangeProvID'} = 91;
    $rUpdateCDC->{'Reason'} = $EmailHeader . ' ' . $notes[$NotificationType];
    if (
        (
            $NotificationType ==
            4     # Collab not needed, other provider terminated
            || $NotificationType == 7     # Collab proposal has been accepted
            || $NotificationType == 15    # Collab will not be needed
            || $NotificationType == 16    # Collab proposal has been accepted
            || $NotificationType ==
            17    # Termination accepted, your PA is now active
            || $NotificationType ==
            22    # Health Home, Customer does not meet the high intensity
            || $NotificationType == 23
        )         # Health Home, Customer has met high intensity and is unlocked
        && $Status ne 'Approved'
        && $PAnumber ne ''
      )
    {
        $rUpdateCDC->{'Status'}     = 'Approved';
        $rUpdateCDC->{'StatusDate'} = $form->{'TODAY'};
        $rUpdateCDC->{'Fail'}       = '';
    }
    if (
        $NotificationType == 8    # Termination ended your PA
        && $Status ne 'Closed'
        && $PAnumber ne ''
      )
    {
        $rUpdateCDC->{'Status'}     = 'Closed';
        $rUpdateCDC->{'StatusDate'} = $form->{'TODAY'};
    }

#foreach my $f ( sort keys %{$rUpdateCDC} ) { print "  updCDC: rUpdateCDC: $f=$rUpdateCDC->{$f}\n"; }
    my $CDCID = DBA->doUpdate( $form, 'ClientPrAuthCDC', $rUpdateCDC,
        "ClientPrAuthID=${PrAuthID}" );

    # DON'T UNLOCK say a Pending PA!
    #  my $lock = $rUpdateCDC->{'Status'} eq 'Approved' ? 1 : 0;
    #  CDC->Lock($form,'ClientPrAuth',$PrAuthID,$lock);
    #print qq|  updCDC: CDCID=${CDCID}, PrAuthID=${PrAuthID}, lock=${lock}\n|;
    # INSTEAD, MAKE SURE THE Approved PAs ARE LOCKED.
    if ( $rUpdateCDC->{'Status'} =~ /Approved|Pending/ ) {
        CDC->Lock( $form, 'ClientPrAuth', $PrAuthID, 1 );
    }

    # save to the CDCLog to show we got an update...
    my $rUpdateLog = ();

 # copy below each value because if not $rUpdateLog=$rCDC is the same reference.
 #   and delete $rUpdateLog deletes from $rCDC
    foreach my $f ( sort keys %{$rCDC} ) { $rUpdateLog->{$f} = $rCDC->{$f}; }
    delete $rUpdateLog->{'ClientPrAuthID'};         # remove ID to the HDR.
    $rUpdateLog->{'ClientPrAuthCDCID'} = $CDCID;    # attach to the CDC.
    $rUpdateLog->{'Status'}            = $rUpdateCDC->{'Status'};
    $rUpdateLog->{'StatusDate'}        = $rUpdateCDC->{'StatusDate'};
    $rUpdateLog->{'Reason'}            = $rUpdateCDC->{'Reason'};
    $rUpdateLog->{'ChangeProvID'}      = $rUpdateCDC->{'ChangeProvID'};

    foreach my $f ( sort keys %{$rUpdateLog} ) {
        print "  updCDC: rUpdateLog: $f=$rUpdateLog->{$f}\n";
    }
    my $LogID = DBA->doUpdate( $form, "ClientPrAuthCDCSent", $rUpdateLog );

#print qq|  END updCDC: PrAuthID=${PrAuthID}, PAnumber=${PAnumber}, LogID=${LogID}\n|;
    return ();
}

sub updLines {
    my ( $self, $form, $key, $rCDC ) = @_;
    my $dbh       = $form->dbconnect();
    my $ClientID  = $rCDC->{'ClientID'};
    my $PrAuthID  = $rCDC->{'ClientPrAuthID'};
    my $rUpdatePA = ();

    #print qq|  BEGIN: updLines ======\n|;
    #print qq|  updLines: Detail=@Detail\n|;
    print
qq|  updLines: key=${key}, ClientID=${ClientID}, PrAuthID=${PrAuthID}/$rCDC->{'ClientPrAuthID'}\n|;
    my $cnt = 0;
    foreach $Detail (@Detail) {
        if ( $Detail->{'notificationkey'} == $key ) {
            $cnt++;

            #print qq|  updLines: cnt=${cnt}\n|;
            if ( $Detail->{'PGgroup'} eq 'PG030' ) {
                print qq|  updLines: CHECK UNITS PG030\n|;
                foreach my $f ( sort keys %{$Detail} ) {
                    print "  updLines: Detail-$f=$Detail->{$f}\n";
                }
            }

            if ( $cnt == 1 ) {

                #print qq|  updLines: DELETE!\n|;
                my $sDelete =
                  $dbh->prepare("delete from PALines where PrAuthID=?");
                $sDelete->execute($PrAuthID)
                  || $form->dberror("setPALines: delete PALines $PrAuthID");
                $sDelete->finish();
            }
            my $rUpdate = ();
            $rUpdate->{'ClientID'}     = $ClientID;
            $rUpdate->{'PrAuthID'}     = $PrAuthID;
            $rUpdate->{'CreateProvID'} = $form->{'LOGINPROVID'};
            $rUpdate->{'CreateDate'}   = $form->{'TODAY'};
            $rUpdate->{'ChangeProvID'} = $form->{'LOGINPROVID'};
            $rUpdate->{'LineNumber'}   = $Detail->{'PAline'};
            ( $rUpdate->{'BegDate'}, $time ) =
              split( 'T', $Detail->{'LineBegdate'} );
            ( $rUpdate->{'EndDate'}, $time ) =
              split( 'T', $Detail->{'LineEnddate'} );
            $rUpdate->{'PAgroup'} = $Detail->{'PGgroup'};
            $rUpdate->{'Status'}  = $Detail->{'LineStatus'};
            $rUpdate->{'Cost'} =
              $Detail->{'LineStatus'} eq 'K' ? 0 : $Detail->{'LineCost'};
            $rUpdate->{'Units'} = 0;

#foreach my $f ( sort keys %{$rUpdate} ) { print "  updLines: rUpdate-$f=$rUpdate->{$f}\n"; }
            $UID = DBA->doUpdate( $form, 'PALines', $rUpdate );

            # update ClientPrAuth when these change based on the PAlines...
            $rUpdatePA->{'EffDate'} = $rUpdate->{'BegDate'}
              if ( $rUpdatePA->{'EffDate'} eq '' );
            $rUpdatePA->{'ExpDate'} = $rUpdate->{'EndDate'};

 #print qq|  updLines: AuthAmt=$Detail->{'LineCost'}/$rUpdatePA->{'AuthAmt'}\n|;
            $rUpdatePA->{'AuthAmt'} += $rUpdate->{'Cost'};

 #print qq|  updLines: AuthAmt=$Detail->{'LineCost'}/$rUpdatePA->{'AuthAmt'}\n|;
            $rUpdatePA->{'PAgroup'} = $rUpdate->{'PAgroup'};
        }
    }
    print qq|  updLines: total cnt=${cnt}\n|;

#foreach my $f ( sort keys %{$rUpdatePA} ) { print "  updLines: rUpdatePA-$f=$rUpdatePA->{$f}\n"; }
#print qq|  END updLines======\n|;
    return ($rUpdatePA);
}
