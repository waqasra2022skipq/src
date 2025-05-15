#!/usr/bin/perl
use lib 'C:/xampp/htdocs/src/lib';
use DBI;
use DBA;
use myForm;
use myDBI;
use DBUtil;

my $debug = 0;

###################################################################################
my $form = myForm->new();
my $dbh  = myDBI->dbconnect( $form->{'DBNAME'} );

#foreach my $f ( sort keys %{$form} ) { warn "PMPws: form-$f=$form->{$f}\n"; }
my $ClientID = $form->{'Client_ClientID'};

my $sProvider = $dbh->prepare("select * from Provider where ProvID=?");
my $sProviderLicenses =
  $dbh->prepare("select * from ProviderLicenses where ProvID=?");
my $sClient = $dbh->prepare("select * from Client where ClientID=?");
$sClient->execute($ClientID)
  || myDBI->dberror("DMHws: select Client: ${ClientID}");
if ( $rClient = $sClient->fetchrow_hashref ) {
    foreach my $f ( sort keys %{$rClient} ) {
        warn "PMPws: rClient-$f=$rClient->{$f}\n";
    }

    # reformat these...
    my $DOB = DBUtil->Date( $rClient->{DOB}, 'fmt', 'MM/DD/YYYY' );

    my $ClinicID = $rClient->{'clinicClinicID'};
    $sProvider->execute($ClinicID)
      || myDBI->dberror("PMPws: select Provider: ${ClinicID}");
    $rClinic = $sProvider->fetchrow_hashref;
    $sProviderLicenses->execute($ClinicID)
      || myDBI->dberror("PMPws: select ProviderLicenses: ${ClinicID}");
    $rProviderLicenses = $sProvider->fetchrow_hashref;
    foreach my $f ( sort keys %{$rClinic} ) {
        warn "PMPws: rClinic-$f=$rClinic->{$f}\n";
    }
    my $xml = qq|
<PatientRequest xmlns="http://xml.appriss.com/gateway/v5_1" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance">
  <Requester>
    <Provider>
      <Role>Physician</Role>
    </Provider>
    <Location>
      <Name>$rClinic->{'Name'}</Name>
      <DEANumber>$rProviderLicenses->{'DEA'}</DEANumber>
      <Address>
        <StateCode>$rClinic->{'ST'}</StateCode>
      </Address>
    </Location>
  </Requester>
  <PrescriptionRequest>
    <Patient>
      <Name>
        <First>$rClient->{'FName'}</First>
        <Last>$rClient->{'LName'}</Last>
      </Name>
      <Birthdate>${DOB}</Birthdate>
      <!--  address Zipcode OR Phone  -->
      <Address>
        <ZipCode>$rClient->{'Zip'}</ZipCode>
      </Address>
    </Patient>
  </PrescriptionRequest>
</PatientRequest>
|;
    print $xml;
}
else {
    print qq|\n>>>ERROR: Not a valid ClientID!\n\n|;
}
$sClient->finish();
$sProvider->finish();
$sProviderLicenses->finish();
myDBI->cleanup();
exit;
###################################################################################
