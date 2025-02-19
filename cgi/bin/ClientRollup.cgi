#!/usr/bin/perl 
use lib '/var/www/okmis/src/lib';
use DBI;
use myForm;
use myDBI;
use Rollup;
############################################################################
my $form = myForm->new();
my $dbh  = myDBI->dbconnect( $form->{'DBNAME'} );

#warn "ENTER ClientRollup: MIS_Action=$form->{'MIS_Action'}, fwdLINK=$form->{fwdLINK}\n";

if ( !$form->{Client_ClientID} ) {
    myDBI->error("Client Page / denied ClientID NULL");
}
if ( !SysAccess->verify( $form, 'hasClientAccess' ) ) {
    myDBI->error("Client Access Page / Not Client");
}
my $ClientID = $form->{Client_ClientID};
my $mlt      = $form->{mlt};
my $misLINKS = $form->{misLINKS};
my $Location =
qq|/cgi/bin/mis.cgi?view=ListClientEDocs.cgi&Client_ClientID=${ClientID}&mlt=${mlt}&misLINKS=$misLINKS\n\n|;

############################################################################

############################################################################
# Get the Provider for this client
my $sProvider = $dbh->prepare("select ProvID from Client where ClientID =?");
$sProvider->execute($ClientID);
$rProvider = $sProvider->fetchrow_hashref;
$sProvider->finish();
$ProvID = $rProvider->{ProvID};

# Get the Clinic for the Provider
$ClinicID = MgrTree->getClinic( $form, $ProvID );

# Now Get the Manager/Agency for this Clinic
$managerAgencyID = MgrTree->getAgency( $form, $ClinicID );

# Create the Directory for the Agency/Manager of the Clinic if not created
Rollup->createDirectory( $form, '/Agency/EDocs/', $managerAgencyID, 2 );

# Create the Directory for the Clinic of the provider if not created
Rollup->createDirectory( $form, "/Agency/EDocs/${managerAgencyID}/Clinics/",
    $ClinicID, 3 );

# Create the Directory for the Provider if not created
Rollup->createDirectory( $form,
    "/Agency/EDocs/${managerAgencyID}/Clinics/${ClinicID}/Providers/",
    $ProvID, 4 );

# Create the Directory for the Client if not created
Rollup->createDirectory(
    $form,
"/Agency/EDocs/${managerAgencyID}/Clinics/${ClinicID}/Providers/$ProvID/Clients/",
    $ClientID
);

# ProgNotes all already getting rolled up at Notes so no need to do it separately
my $SingleClientFolder =
"/Agency/EDocs/${managerAgencyID}/Clinics/${ClinicID}/Providers/$ProvID/Clients/${ClientID}";

# ProgNotes all already getting rolled up at Notes so no need to do it separately

Rollup->edocs( $form, $ClientID, 'ClientAdmit',  '2017-01-01' );
Rollup->edocs( $form, $ClientID, 'ClientAdmit',  '', $SingleClientFolder );
Rollup->edocs( $form, $ClientID, 'ClientTrPlan', '', $SingleClientFolder );
Rollup->edocs( $form, $ClientID, 'ClientPrAuth', '', $SingleClientFolder );

# CHANGE:START adding more notes

Rollup->edocs( $form, $ClientID, 'ClientPrAuthCDC',  '', $SingleClientFolder );
Rollup->edocs( $form, $ClientID, 'ClientLabs',       '', $SingleClientFolder );
Rollup->edocs( $form, $ClientID, 'ClientCARSReview', '', $SingleClientFolder );
Rollup->edocs( $form, $ClientID, 'PDMed',            '', $SingleClientFolder );
Rollup->edocs( $form, $ClientID, 'ClientRiskAssessment', '',
    $SingleClientFolder );

Rollup->edocs( $form, $ClientID, 'ClientPHQ',      '', $SingleClientFolder );
Rollup->edocs( $form, $ClientID, 'ClientPHQ15',    '', $SingleClientFolder );
Rollup->edocs( $form, $ClientID, 'ClientPHQ2',     '', $SingleClientFolder );
Rollup->edocs( $form, $ClientID, 'ClientPHQ4',     '', $SingleClientFolder );
Rollup->edocs( $form, $ClientID, 'ClientPHQ9',     '', $SingleClientFolder );
Rollup->edocs( $form, $ClientID, 'ClientTPHQ9',    '', $SingleClientFolder );
Rollup->edocs( $form, $ClientID, 'ClientPHQBrief', '', $SingleClientFolder );
Rollup->edocs( $form, $ClientID, 'ClientPHQSADS',  '', $SingleClientFolder );

Rollup->edocs( $form, $ClientID, 'ClientASI',  '', $SingleClientFolder );
Rollup->edocs( $form, $ClientID, 'ClientTASI', '', $SingleClientFolder );
Rollup->edocs( $form, $ClientID, 'ClientASAM', '', $SingleClientFolder );
Rollup->edocs( $form, $ClientID, 'SOGS',       '', $SingleClientFolder );
Rollup->edocs( $form, $ClientID, 'SOGSGSI',    '', $SingleClientFolder );
Rollup->edocs( $form, $ClientID, 'ClientMeds', '', $SingleClientFolder );

my $cnt = Rollup->Notes( $form, $ClientID, '', $SingleClientFolder );

Rollup->edocs( $form, $ClientID, 'ClientDischarge', '', $SingleClientFolder );
Rollup->edocs( $form, $ClientID, 'ClientEDocs',     '', $SingleClientFolder );

#warn qq|Rollup complete: ${Location}\n\n|;
Rollup->add_to_zip( $form, $SingleClientFolder, $ClientID );

myDBI->cleanup();

print qq|Location: ${Location}\n\n|;
exit;
############################################################################
