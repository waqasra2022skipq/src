#!/usr/bin/perl
use lib 'C:/xampp/htdocs/src/lib';
use DBI;
use DBA;
use myForm;
use myDBI;
use DBUtil;
use SOAP::Lite ( maptype => {} );
my $debug = 0;
###################################################################################
my $form = myForm->new();
my $dbh  = myDBI->dbconnect( $form->{'DBNAME'} );

#foreach my $f ( sort keys %{$form} ) { warn "DMHcm: form-$f=$form->{$f}\n"; }
my $InsNumIDs = $form->{'InsNumIDs'};
my $ProvID    = $form->{'Provider_ProvID'};
my $ClientID  = $form->{'Client_ClientID'};
my $table     = $form->{'action'};

#warn qq|DMHcm: InsNumIDs: ${InsNumIDs}\n|;
#warn qq|DMHcm: ProvID: ${ProvID}\n|;
#warn qq|DMHcm: table: ${table}\n|;

my $url = 'https://dmhwebservices.odmhsas.org/ErrorListWebService/Service.asmx';
my $WebSupport =
  qq|\nContact DMH support\nDavid Melton: 405-522-3819 or DMelton\@odmhsas.org|;
my $location =
qq|Location: /cgi/bin/ClientList.cgi?Provider_ProvID=${ProvID}&Client_ClientID=${ClientID}&mlt=$form->{mlt}&misLINKS=$form->{misLINKS}\n\n|;
my $sInsurance = $dbh->prepare("select * from Insurance where InsIDNum=?");

if ($debug) {
    DBA->setAlert( $form,
"DEBUG:\nTEST JQUERY.\nTest if the setAlert works OK\nWith the newlines and other stuff.\nLike multiple lines in a box\nHow big is the box and what size will it expand to if we write a long sentence that has many many words in it. \nDoes the box work OK?"
    );
    $sInsurance->finish();
    myDBI->cleanup();
    print $location;
    exit;
}

my ( $errmsg, $error_nodes, $alertmsg ) = ( '', '', '' );
my ( $userid2, $password2 ) = ( 'MIS', '!MsV3nD0rL3v3l_45' );
if ( $form->{'DBNAME'} eq 'okmms_dev' || $form->{'DBNAME'} eq 'okmis_demo' ) {
    $url =
      'https://dmhwebservices.odmhsas.org/ErrorListWebService/Service.asmx';
}

#warn qq|DMHcm: url=${url}\n|;
if ( $errmsg eq '' ) {
    my $soap =
      SOAP::Lite->uri('http://tempuri.org')
      ->on_action( sub { join '/', 'http://tempuri.org', $_[1] } )
      ->readable(1)
      ->proxy($url);

    # modify the cipher list because of handshake issues with ASP.net
    $soap->{_transport}->{_proxy}->{ssl_opts}->{SSL_cipher_list} =
      'SHA:!NULL:!3DES:!DES:!ADH:!SRP';

    my $method = SOAP::Data->name('ProgramEligibilityStringList')
      ->attr( { xmlns => 'http://tempuri.org/' } );

    #warn qq|method=$method\n|;
    my @params = main->setParameters($InsNumIDs);
    my $result;

    #warn qq|KLS: setParameters is done...\n|;
    eval { $result = $soap->call( $method => @params ); };
    if ($@) {
        ( $errmsg, $rest ) = split( "at /home", $@, 2 );
        DBA->setAlert( $form, "Connection FAILED:\n${errmsg}\n${WebSupport}" );
        $sInsurance->finish();
        myDBI->cleanup();
        print $location;
        exit;
    }

    #warn qq|KLS: back from soap-call...\n|;
    if ( $result->fault ) {
        warn qq|faultstring=| . $result->faultstring . "\n";
        my ( $msg, $rest ) = split( "\r", $result->faultstring, 2 );
        $errmsg = qq|faultstring=${msg}\n|;
        my $rUpdate = ();
        $rUpdate->{'StatusDate'} = $form->{'TODAY'};
        $rUpdate->{'Fail'}       = $errmsg . ' ' . $InsNumIDs;
        $LogID    = DBA->doUpdate( $form, "EligibleDMH", $rUpdate );
        $alertmsg = $errmsg;
    }
    else {
        # start ProgramEligibility...,
        #warn qq|result=|.$result->result."\n";
        my @nodes = $result->valueof('//ProgramEligibility');

        #warn qq|nodes=@nodes\n|;
        #warn qq|start ProgramEligibility...\n|;
        foreach $node (@nodes) {

          #warn qq|errmsg/errfld=|.$node->{'errmsg'}."/".$node->{'errfld'}."\n";
            $errmsg .= qq|$node->{'errmsg'}\n| if ( $node->{'errmsg'} ne '' );
            my $rUpdate = ();

     #foreach my $f ( sort keys %{ $node } ) { warn ": node-$f=$node->{$f}\n"; }
            foreach my $f ( sort keys %{$node} ) {
                next
                  if ( $node->{$f} eq '' )
                  ;    # skip when they send us nulls, don't update
                if ( $f eq 'RECIPIENT_ID' ) {
                    $rUpdate->{'RECIPIENTID'} = $node->{$f};
                }
                elsif ( $f eq 'TXIX' )  { $rUpdate->{'TXIX'}  = $node->{$f}; }
                elsif ( $f eq 'DMH' )   { $rUpdate->{'DMH'}   = $node->{$f}; }
                elsif ( $f eq 'REHAB' ) { $rUpdate->{'REHAB'} = $node->{$f}; }
                elsif ( $f eq 'CASEMGMT' ) {
                    $rUpdate->{'CASEMGMT'} = $node->{$f};
                }
                elsif ( $f eq 'CASEMGMTUNITS' ) {
                    $rUpdate->{'CASEMGMTUNITS'} = $node->{$f};
                }
                elsif ( $f eq 'CCBHC' ) { $rUpdate->{'CCBHC'} = $node->{$f}; }
                elsif ( $f eq 'BAD_ADDRESS' ) {
                    $rUpdate->{'BADADDRESS'} = $node->{$f};
                }
                elsif ( $f eq 'VALID_ID' ) {
                    $rUpdate->{'Status'} = $node->{$f};
                }
                elsif ( $f eq 'OCH' ) { $rUpdate->{'OCH'} = $node->{$f}; }
                elsif ( $f eq 'HUM' ) { $rUpdate->{'HUM'} = $node->{$f}; }
                elsif ( $f eq 'AET' ) { $rUpdate->{'AET'} = $node->{$f}; }
                else { $error_nodes .= "node: ${f}=$node->{$f}"; }
            }
            $sInsurance->execute( $rUpdate->{'RECIPIENTID'} )
              || myDBI->dberror(
                "DMHcm: select Insurance: $rUpdate->{'RECIPIENTID'}");
            $rInsurance              = $sInsurance->fetchrow_hashref;
            $rUpdate->{'ClientID'}   = $rInsurance->{'ClientID'};
            $rUpdate->{'StatusDate'} = $form->{'TODAY'};
            $alertmsg                = qq|Response is:<BR>|;
            foreach my $f ( sort keys %{$rUpdate} ) {
                $alertmsg .= qq|$f=$rUpdate->{$f}<BR>|;
            }
            if ( $rUpdate->{'Status'} == 0 ) {
                $alertmsg =
                  qq|Not a valid Member ID!<BR>$rUpdate->{'RECIPIENTID'}|;
                $rUpdate->{'Fail'} = qq|Not a valid Member ID!|;
            }

#foreach my $f ( sort keys %{ $rUpdate } ) { warn ": rUpdate-$f=$rUpdate->{$f}\n"; }
            my $ID = DBA->doUpdate( $form, "EligibleDMH", $rUpdate,
                "RECIPIENTID='$rUpdate->{'RECIPIENTID'}'" );
        }
    }
}
else { $alertmsg = $errmsg; }
$sInsurance->finish();

myDBI->cleanup();

DBA->setAlert( $form, $alertmsg );

#warn qq|END: alertmsg=${alertmsg}\n|;
if ( $error_nodes ne '' ) {
    DBUtil->email( $form, 'support@okmis.com',
        "ERROR DMHcm: $form->{'DBNAME'}: ${ClientID}", $error_nodes );
}
print $location;
exit;

###################################################################################
sub setParameters {
    my ( $self, $ids ) = @_;

    #warn qq|setParameters: ids=${ids}\n|;
    my @clients = main->setInsIDs($ids);
    my @params  = (
        SOAP::Data->name('i')->value(
            \SOAP::Data->value(
                SOAP::Data->name('_userid')->value('dmhwebsrv'),
                SOAP::Data->name('_password')->value('B90wR2k'),
                SOAP::Data->name('_userid2')->value($userid2),
                SOAP::Data->name('_password2')->value($password2),
                SOAP::Data->name('_recipientlist')
                  ->value( \SOAP::Data->value(@clients) )
            )
        ),
    );
    return (@params);
}
##################################################################################
sub setInsIDs {
    my ( $self, $ids ) = @_;
    my @params;
    foreach my $InsID ( split( ' ', $ids ) ) {
        push( @params, SOAP::Data->name('string')->value($InsID) );
    }
    return (@params);
}
