#!/usr/bin/perl
use lib '/home/okmis/mis/src/lib';
use CGI::Carp qw(warningsToBrowser fatalsToBrowser);

use strict;
use warnings;
use LWP::UserAgent;
use JSON;
use HTTP::Request;
use CGI qw(:standard escape);
use DBForm;
use Try::Tiny;


my $form = DBForm->parse();

# my $USPS_TOKEN = $ENV{'USPS_TOKEN'} ? $ENV{'USPS_TOKEN'} : 'eyJraWQiOiJIdWpzX2F6UnFJUzBpSE5YNEZIRk96eUwwdjE4RXJMdjNyZDBoalpNUnJFIiwidHlwIjoiSldUIiwiYWxnIjoiUlMyNTYifQ.eyJlbnRpdGxlbWVudHMiOltdLCJzdWIiOiIiLCJjcmlkIjoiIiwic3ViX2lkIjoiIiwicm9sZXMiOltdLCJwYXltZW50X2FjY291bnRzIjp7fSwiaXNzIjoiaHR0cHM6Ly9rZXljLnVzcHMuY29tL3JlYWxtcy9VU1BTIiwiY29udHJhY3RzIjp7fSwiZmFzdCI6IiIsImF6cCI6ImhUeG1HZzJ5WHJBUlh5VEFzcUtsaVVYVUFnbnRSeVcxRzNQREFXVHRZekJqWUFDaSIsIm1haWxfb3duZXJzIjpbXSwic2NvcGUiOiJkb21lc3RpYy1wcmljZXMgYWRkcmVzc2VzIGludGVybmF0aW9uYWwtcHJpY2VzIHNlcnZpY2Utc3RhbmRhcmRzIGxvY2F0aW9ucyBzaGlwbWVudHMiLCJjb21wYW55X25hbWUiOiIiLCJleHAiOjE3MzczODE1OTMsImlhdCI6MTczNzM1Mjc5MywianRpIjoiN2YyMGI0YzctMjA1Yy00MGYxLWExY2YtNjMxZmQwZDhkOGE2In0.F5TvXpsCopM7UfnU1AKUEinsVY6QMn22aOKo3t8VYKgdv_eMeWfmVX-iNRop9BgsKN-IHsPT7yHzzchD0VcXFFw2gC1UBnmi6UrAEz3ELBkzTgXH4e8HV96Cv5MzCgF40QjzlK9GnhW67t7zSV8WNkagRkNY9gNQEUwc2loI3fJ36GSrkjDLBMW1Q0vO6cGPFZBfmQVH8Mpt5ptGhiN-tNAGvL6VAgjnm92Uvp2ochnUmgT4Wn4ALP8SWjvjD4mUCHVd1nDP4z4nIpZn5CvTOwKtRlXZLdqO9NISbpUO_tZn5FGpnBnQMHhAttidIivJuHpZYoE_k8-hAqeHOzi_kA';
my $dbh = myDBI->dbconnect('okmis_config');
my $s=$dbh->prepare("select access_token from USPSTokens");
$s->execute();
my $r = $s->fetchrow_hashref;
my $USPS_TOKEN = $r->{'access_token'};


my $update_token_q=$dbh->prepare("Update USPSTokens set access_token=? WHERE access_token = ?");

# print qq|Content-type: text/xml\n\n<?xml version="1.0" encoding="UTF-8" standalone="yes"?>\n<response>${USPS_TOKEN}</response>\n|;

#     $form->complete();
#     exit;

my $api_url = "https://apis.usps.com/addresses/v3/address"; # New endpoint
my $api_key = "OsIAIMJ9I76boItsLnBOeRBIrpQnNOuw42AL9tuuhUEnXmKv"; # Replace with your API key


# OAuth 2.0 Credentials
my $client_id = "hTxmGg2yXrARXyTAsqKliUXUAgntRyW1G3PDAWTtYzBjYACi";
my $client_secret = "raM669vwDsm6wpoAVq3x3wX2NBPq4ikcqiq1KtWr2zlG4GANcasGR24tmNuzymrl";
my $custreg_uid = '360287389';
my $token_url = "https://apis.usps.com/oauth2/v3/token";

# Function to get access token
sub get_access_token {
    my $ua = LWP::UserAgent->new;
    my $req = HTTP::Request->new('POST', $token_url);
    $req->header('Content-Type' => 'application/x-www-form-urlencoded');

    my $body = "grant_type=client_credentials&client_id=$client_id&client_secret=$client_secret&scope=addresses";
    $req->content($body);

    my $response = $ua->request($req);

    if ($response->is_success) {
        my $token_data = decode_json($response->decoded_content);
        $update_token_q->execute($token_data->{access_token}, $USPS_TOKEN);
        return $token_data->{access_token};
    } else {
        die "Failed to get access token: " . $response->status_line . " " . $client_id . " " . $client_secret;
    }
}

my $access_token = "";
if($USPS_TOKEN) {
    $access_token = $USPS_TOKEN;
} else {
    $access_token = get_access_token();
}


sub uspsValidateAddress {
    my ($form) = @_;

    try {
        my $Addr1 = $form->{'Addr1'};
        my $City = $form->{'City'};
        my $State = $form->{'State'} eq '' ? 'OK' : $form->{'State'};

        my ($Zip5,$Zip4) = split('-',$form->{Zip});
        $Zip5 = '00000' if ( $Zip5 eq '' );
        $Zip4 = '0000' if ( $Zip4 eq '' );

        my $query = "?streetAddress=${Addr1}&city=${City}&state=${State}&ZIPCode=${Zip5}";

        # Create a user agent
        my $ua = LWP::UserAgent->new;

        # Create a GET request
        my $req = HTTP::Request->new(GET => $api_url . $query);

        # Add headers
        $req->header('accept' => 'application/json');
        $req->header('x-user-id' => 'XXXXXXXXXXXX');
        $req->header('authorization' => 'Bearer ' . $access_token); # Ensure $TOKEN is set in the environment

        # Send the request
        my $response = $ua->request($req);

        # Check the response
        if ($response->is_success) {
            $response->decoded_content;
        } else {
            if($response->{'error'}->{'errors'}->{'title'} eq "token_expired") {
                $access_token = get_access_token();
            } else {
                return $response->decoded_content;
            }
        }
    } catch {
            return "caught error: $_";
    };


}

eval {

    my $validated_address = uspsValidateAddress($form);
    my $target = "$form->{'Prefix'}Check_Address_1";

    $validated_address = decode_json($validated_address);

    if($validated_address->{'error'}->{'message'} eq "The access token presented with the request has expired.") {
        $access_token = get_access_token();
        $validated_address = "";    
        $validated_address = uspsValidateAddress($form);
        $validated_address = decode_json($validated_address);
    } 

    my $err = 0;
    my $err_message = ""; 
    my $script = "";
    my $content = "";


    if($validated_address->{'error'}->{'code'} ne "") {
        $err = 1;
        $err_message = "Ivalid Address";
    } else {
        my $City = $validated_address->{'address'}->{'city'};
        my $State = $validated_address->{'address'}->{'state'};
        my $Zip = $validated_address->{'address'}->{'ZIPCode'};
        my $Addr2 = $validated_address->{'address'}->{'streetAddress'};

        $script = qq|
          document.getElementsByName('$form->{'Prefix'}City_1')[0].value = "${City}";
          document.getElementsByName('$form->{'Prefix'}ST_1')[0].value = "${State}";
          document.getElementsByName('$form->{'Prefix'}Zip_1')[0].value = "${Zip}";
          document.getElementsByName('$form->{'Prefix'}Addr_1')[0].value = "${Addr2}";
        |;
        $content = qq|
            <img src="/images/check.jpg" width="20" height="20" style="vertical-align: middle;margin-right: 8px;">
            <span>Verified</span>
            |;
    }

    my $out;

    if($err) {
        $out = main->ierr($target,$err_message);
    } else {
        $out = qq|
          <command method="setscript">
            <target>executeit</target>
            <content><![CDATA[${script}]]></content>
          </command>
          <command method="setcontent">
            <target>${target}</target>
            <content><![CDATA[${content}]]></content>
          </command>
        |;
    }

    my $xml = qq|<response>\n${out}</response>|;

    print qq|Content-type: text/xml\n\n<?xml version="1.0" encoding="UTF-8" standalone="yes"?>\n${xml}\n|;

    $form->complete();
    exit;
};
if ($@) {
    print "Error: $@\n";
}

###################################################################################
sub ierr
{
  my ($self,$target,$err) = @_;
#warn qq|ierr: target=$target\n|;
  my $out = qq|
  <command method="setdefault">
    <target>${target}</target>
  </command>
  <command method="alert">
    <message>${err}</message>
  </command>
  <command method="focus">
    <target>${target}</target>
  </command>
|;
  return($out);
}

$s->finish();
