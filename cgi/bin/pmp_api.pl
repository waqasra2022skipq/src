#!/usr/bin/perl -w
use lib '/home/okmis/mis/src/lib';
use strict;
use DBI;
use login;
use DBForm;
use DBUtil;
use LWP::UserAgent;
use JSON;
use XML::Simple;
use Digest::SHA qw(sha256_hex);
use Digest::MD5 qw(md5 md5_hex md5_base64);
use Net::SSL;

###################################################################################
my $form = DBForm->parse();
$form    = login->chkLogin($form);
my $dbh  = $form->dbconnect($form->{'DBNAME'});

my $proxy    = "https://mutualauth.pmpgateway.net/v5_1";
my $PMP_USER = "in-house-build-millennium-medical-services-llc-prep";
my $PMP_PASS = "Cubs2016!";

##set server certificate and key without no password as well
$ENV{PERL_LWP_SSL_VERIFY_HOSTNAME} = 0;
$ENV{HTTPS_CERT_FILE} = "/etc/apache2/cert/certificate.pem";
$ENV{HTTPS_KEY_FILE}  = "/etc/apache2/cert/client-no-password.key";
##set server certificate and key as well end

my $sClient = $dbh->prepare("select * from Client where ClientID=?");
my $sProvider = $dbh->prepare("select * from Provider where ProvID=?");
my $sProviderLicenses = $dbh->prepare("select * from ProviderLicenses where ProvID=?");

my $ClientID = $form->{'Client_ClientID'};

$sClient->execute($ClientID) || $form->dberror("DMHws: select Client: ${ClientID}");
my $rClient = $sClient->fetchrow_hashref;
my $ProvID = $rClient->{'ProvID'};
$sProvider->execute($ProvID) || $form->dberror("PMP: select Provider: ${ProvID}");
my $rProvider = $sProvider->fetchrow_hashref;
$sProviderLicenses->execute($ProvID) || $form->dberror("PMP: select ProviderLicenses: ${ProvID}");
my $rProviderLicenses = $sProviderLicenses->fetchrow_hashref;

###################################################################################
my $json_str;

if ($form->{'method'} eq 'GetOpioidRegistry')
{
  my %json = ();
  my $patient_link = main->patient_request($rClient, $rProvider, $rProviderLicenses);
  my $report_link = main->report_request($rProvider, $rProviderLicenses, $patient_link);

  $json{'patient_link'} = $patient_link;
  $json{'report_link'} = $report_link;

  $json_str = encode_json \%json;
}

$sClient->finish();
$sProvider->finish();
$sProviderLicenses->finish();
$dbh->disconnect();
$form->complete();

print qq|Content-type: application/json\n\n$json_str|;
exit;

###################################################################################
sub patient_request
{
  my ($self, $rClient, $rProvider, $rProviderLicenses) = @_;

  my $patientLink = "";

  my $requestXML = qq|<?xml version="1.0" encoding="UTF-8"?>
<PatientRequest xmlns="http://xml.appriss.com/gateway/v5_1" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance">
  <Requester>
    <Provider>
      <Role>Physician</Role>
      <FirstName>Rob</FirstName>
      <LastName>Phillips</LastName>
      <DEANumber>MP2428577</DEANumber>
    </Provider>
    <Location>
      <Name>MILLENNIUM MEDICAL SERVICES, LLC</Name>
      <NPINumber>1194119016</NPINumber>
      <Address>
        <StateCode>OK</StateCode>
      </Address>
    </Location>
  </Requester>
  <PrescriptionRequest>
    <Patient>
      <Name>
        <First>Jordan</First>
        <Last>Dye</Last>
      </Name>
      <Birthdate>1990-04-02</Birthdate>
      <!-- ZipCode or Phone is required. -->
      <Address>
        <ZipCode>73072</ZipCode>
      </Address>
    </Patient>
  </PrescriptionRequest>
</PatientRequest>|;
  
  my $ua = new LWP::UserAgent;
  $ua->agent('Mozilla/5.0 [en] (Win98; U)');
  $ua->protocols_allowed( [ 'http', 'https']);

  my $api_url = $proxy . "/patient";

  my $nonce = main->generate_nonce(); 
  my $time  = time();

  my $pass_digest_string = "$PMP_PASS:$nonce:$time";
  my $pass_digest = sha256_hex($pass_digest_string);

  $ua->default_header('X-Auth-Username'       => $PMP_USER);
  $ua->default_header('X-Auth-Timestamp'      => $time);
  $ua->default_header('X-Auth-Nonce'          => $nonce);
  $ua->default_header('X-Auth-PasswordDigest' => $pass_digest);

  my $request = HTTP::Request->new( POST => $api_url );
        
  $request->content( $requestXML );

  $request->content_type("application/xml; charset=utf-8");

  my $response = $ua->request($request);

  if ($response->is_success)
  {
    my $data = XMLin($response->decoded_content);
    $patientLink = $data->{Report}->{ReportRequestURLs}->{ViewableReport}->{content};
  }

  return $patientLink;
}

sub report_request
{
  my ($self, $rProvider, $rProviderLicenses, $patientLink) = @_;

  my $reportLink = "";

  my $requestXML = qq|<?xml version="1.0" encoding="UTF-8"?>
<ReportRequest xmlns="http://xml.appriss.com/gateway/v5_1" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance">
  <Requester>
    <ReportLink /><!-- Include this element to get the report as a on-time-use URL. -->
    <Provider><!-- Person viewing the report. -->
      <Role>Physician</Role>
      <FirstName>Rob</FirstName>
      <LastName>Phillips</LastName>
      <DEANumber>MP2428577</DEANumber>
      <NPINumber>1194119016</NPINumber>
    </Provider>
    <Location>
      <Name>MILLENNIUM MEDICAL SERVICES, LLC</Name>
      <!-- At least one identifier is required: DEANumber, NPINumber, or NCPDPNumber. -->
      <NPINumber>1245286285</NPINumber>
      <Address>
        <StateCode>OK</StateCode>
      </Address>
    </Location>
  </Requester>
</ReportRequest>|;

  if ($patientLink ne '')
  {
    my $ua = new LWP::UserAgent;
    $ua->agent('Mozilla/5.0 [en] (Win98; U)');
    $ua->protocols_allowed( [ 'http', 'https']);

    my $nonce = main->generate_nonce(); 
    my $time  = time();

    my $pass_digest_string = "$PMP_PASS:$nonce:$time";
    my $pass_digest = sha256_hex($pass_digest_string);

    $ua->default_header('X-Auth-Username'       => $PMP_USER);
    $ua->default_header('X-Auth-Timestamp'      => $time);
    $ua->default_header('X-Auth-Nonce'          => $nonce);
    $ua->default_header('X-Auth-PasswordDigest' => $pass_digest);

    my $request = HTTP::Request->new( POST => $patientLink );
          
    $request->content( $requestXML );

    $request->content_type("application/xml; charset=utf-8");

    my $response = $ua->request($request);

    if ($response->is_success)
    {
      my $data = XMLin($response->decoded_content);
      $reportLink = $data->{ReportLink};
    }
  }

  return $reportLink;
}

sub generate_nonce
{
  my ($self) = @_;

  my $seed = localtime(time)."-".int(rand(100));
    
  my $md5 = lc md5_hex($seed);
  my @octets = $md5 =~ /(.{2})/g;

  substr $octets[6], 0, 1, '4';
  substr $octets[8], 0, 1, '8';
  my $nonce = "@octets[0..3]-@octets[4..5]-@octets[6..7]-@octets[8..+9]-@octets[10..15]";
  $nonce =~ s/ //g;

  return $nonce;
}
