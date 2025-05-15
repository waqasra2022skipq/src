#!/usr/bin/perl 
use lib 'C:/xampp/htdocs/src/lib';
use DBI;
use myForm;
use myDBI;
use Rollup;
use MgrTree;

############################################################################
my $form = myForm->new();

#warn "ENTER ClientRollup: MIS_Action=$form->{'MIS_Action'}, fwdLINK=$form->{fwdLINK}\n";

if ( !$form->{Provider_ProvID} ) {
    myDBI->error("Provider Page / denied ProvID NULL");
}
if ( !SysAccess->verify( $form, 'hasProviderAccess' ) ) {
    myDBI->error("Provider Access Page / Not Provider");
}
my $ProvID   = $form->{Provider_ProvID};
my $mlt      = $form->{mlt};
my $misLINKS = $form->{misLINKS};
my $Location =
qq|/cgi/bin/mis.cgi?view=ListProviderEDocs.cgi&Provider_ProvID=${ProvID}&mlt=${mlt}&misLINKS=$misLINKS\n\n|;

my $dbh = myDBI->dbconnect( $form->{'DBNAME'} );

# get Provider record for summary output.
my $sProvider = $dbh->prepare("select Type from Provider where ProvID=?");

# Updating the Code 17/11/2023

$sProvider->execute($ProvID);
my $rProvider = $sProvider->fetchrow_hashref;
my $agencyID;

if ( $rProvider->{Type} == 2 ) {

    # If Agency

    $agencyID = $ProvID;

  # Create Directory if not created at DOCROOT/Agency/EDocs/{Agency/Provider ID}
    Rollup->createDirectory( $form, '/Agency/EDocs/', $agencyID, 2 );
    main->doRollup( $form, $ProvID, "/Agency/EDocs/$ProvID" );

    foreach my $rProvInner ( MgrTree->getProviders( $form, $agencyID, 0 ) ) {
        next if ( $rProvInner->{Type} ne 3 );
        my $ClinicID = $rProvInner->{ProvID};
        main->doClinicRollup( $form, $ClinicID, $agencyID );
    }

    # Rollup->ProviderEDocs($form, $ProvID, "Billing837");
    # Rollup->ProviderEDocs($form, $ProvID, "ProviderPay");
    # Rollup->ProviderEDocs($form, $ProvID, "Treatment");
}

if ( $rProvider->{Type} == 3 ) {

    # If Provider is Clinic
    $ClinicID = $ProvID;

    # First find the Agency/Manager this Clinic Belongs to.

    $managerAgencyID = MgrTree->getAgency( $form, $ClinicID );

    # Create the Directory for this Agency if not created
    Rollup->createDirectory( $form, '/Agency/EDocs/', $managerAgencyID, 2 );

    # Now call the doClinicRollup
    main->doClinicRollup( $form, $ClinicID, $managerAgencyID );
}

if ( $rProvider->{Type} == 4 ) {

    # If Provider is Simple Provider
    my $Provider_ID = $ProvID;

    # Get the Manager/Clinic for this Provider

    $ClinicID = MgrTree->getClinic( $form, $Provider_ID );

    # Now Get the Manager/Agency for this Clinic
    $managerAgencyID = MgrTree->getAgency( $form, $ClinicID );

    # Create the Directory for the Agency/Manager of the Clinic if not created
    $newDir =
      Rollup->createDirectory( $form, '/Agency/EDocs/', $managerAgencyID, 2 );

    # Create the Directory for the Clinic of the provider if not created
    Rollup->createDirectory( $form, "/Agency/EDocs/${managerAgencyID}/Clinics/",
        $ClinicID, 3 );

    main->doProvidersRollup( $form, $Provider_ID, $ClinicID, $managerAgencyID );

}

sub doClinicRollup {
    my ( $self, $form, $ClinicID, $agencyID ) = @_;

    Rollup->createDirectory( $form, "/Agency/EDocs/${agencyID}/Clinics/",
        $ClinicID, 3 );
    main->doRollup( $form, $ClinicID,
        "/Agency/EDocs/${agencyID}/Clinics/$ClinicID" );

    foreach my $rProvInner ( MgrTree->getProviders( $form, $ClinicID, 1 ) ) {
        my $Provider_ID = $rProvInner->{ProvID};
        main->doProvidersRollup( $form, $Provider_ID, $ClinicID, $agencyID );
    }
}

sub doProvidersRollup {
    my ( $self, $form, $Provider_ID, $ClinicID, $agencyID ) = @_;

    Rollup->createDirectory( $form,
        "/Agency/EDocs/${agencyID}/Clinics/${ClinicID}/Providers/",
        $Provider_ID, 4 );
    main->doRollup( $form, $Provider_ID,
        "/Agency/EDocs/${agencyID}/Clinics/$ClinicID/Providers/$Provider_ID" );

    main->setUpClientRollUP( $form, $Provider_ID,
"/Agency/EDocs/${agencyID}/Clinics/$ClinicID/Providers/$Provider_ID/Clients/"
    );
}

sub setUpClientRollUP {
    my ( $self, $form, $Provider_ID, $ClientsFolder ) = @_;
    my $qClients =
qq|select distinct ClientID from Client where ProvID='$Provider_ID' and Active=1|;

    # Get the Clients of the Provider
    $sClient = $dbh->prepare($qClients);
    $sClient->execute();

    while ( $rClient = $sClient->fetchrow_hashref ) {
        $ClientID = $rClient->{'ClientID'};
        Rollup->createDirectory( $form, $ClientsFolder, $ClientID );

        $SingleClientFolder = "${ClientsFolder}${ClientID}";
        Rollup->edocs( $form, $ClientID, 'ClientAdmit', '2017-01-01',
            $SingleClientFolder );
        Rollup->edocs( $form, $ClientID, 'ClientAdmit', '',
            $SingleClientFolder );
        Rollup->edocs( $form, $ClientID, 'ClientTrPlan', '',
            $SingleClientFolder );
        Rollup->edocs( $form, $ClientID, 'ClientPrAuth', '',
            $SingleClientFolder );

        # CHANGE:START adding more notes

        Rollup->edocs( $form, $ClientID, 'ClientPrAuthCDC', '',
            $SingleClientFolder );
        Rollup->edocs( $form, $ClientID, 'ClientLabs', '',
            $SingleClientFolder );
        Rollup->edocs( $form, $ClientID, 'ClientCARSReview', '',
            $SingleClientFolder );
        Rollup->edocs( $form, $ClientID, 'PDMed', '', $SingleClientFolder );
        Rollup->edocs( $form, $ClientID, 'ClientRiskAssessment', '',
            $SingleClientFolder );

        Rollup->edocs( $form, $ClientID, 'ClientPHQ', '', $SingleClientFolder );
        Rollup->edocs( $form, $ClientID, 'ClientPHQ15', '',
            $SingleClientFolder );
        Rollup->edocs( $form, $ClientID, 'ClientPHQ2', '',
            $SingleClientFolder );
        Rollup->edocs( $form, $ClientID, 'ClientPHQ4', '',
            $SingleClientFolder );
        Rollup->edocs( $form, $ClientID, 'ClientPHQ9', '',
            $SingleClientFolder );
        Rollup->edocs( $form, $ClientID, 'ClientTPHQ9', '',
            $SingleClientFolder );
        Rollup->edocs( $form, $ClientID, 'ClientPHQBrief', '',
            $SingleClientFolder );
        Rollup->edocs( $form, $ClientID, 'ClientPHQSADS', '',
            $SingleClientFolder );

        Rollup->edocs( $form, $ClientID, 'ClientTASI', '',
            $SingleClientFolder );
        Rollup->edocs( $form, $ClientID, 'ClientASAM', '',
            $SingleClientFolder );

        Rollup->edocs( $form, $ClientID, 'ClientACE', '', $SingleClientFolder );
        Rollup->edocs( $form, $ClientID, 'ClientGAD7', '',
            $SingleClientFolder );
        Rollup->edocs( $form, $ClientID, 'ClientBasis32', '',
            $SingleClientFolder );
        Rollup->edocs( $form, $ClientID, 'ClientASI', '', $SingleClientFolder );
        Rollup->edocs( $form, $ClientID, 'SOGS',      '', $SingleClientFolder );
        Rollup->edocs( $form, $ClientID, 'SOGSGSI',   '', $SingleClientFolder );
        Rollup->edocs( $form, $ClientID, 'ClientMeds', '',
            $SingleClientFolder );
        Rollup->edocs( $form, $ClientID, 'ClientDischarge', '',
            $SingleClientFolder );
        Rollup->edocs( $form, $ClientID, 'ClientEDocs', '',
            $SingleClientFolder );

        Rollup->Notes( $form, $ClientID, '', $SingleClientFolder )
          ;    # now Type does not matter
        Rollup->add_to_zip( $form, $SingleClientFolder, $ClientID );

    }

    $sClient->finish();

}

sub doRollup {
    my ( $self, $form, $ProvID, $path ) = @_;

    Rollup->ProviderEDocs( $form, $ProvID, "Credentials",   $path );
    Rollup->ProviderEDocs( $form, $ProvID, "ProviderCreds", $path );

    Rollup->RollupFiles( $form, $ProvID, $path );

    Rollup->Notes( $form, '', $ProvID, $path );
    Rollup->ProviderEDocs( $form, $ProvID, "ProviderEDocs", $path );

    Rollup->add_to_zip( $form, $path, $ProvID );
}

# Rollup->ProviderEDocs($form, $ProvID, "ProviderEDocs");
# Rollup->ProviderEDocs($form, $ProvID, "ProviderCreds");

# if ( $rProvider->{Type} == 3 ) {
# 	# To Print Provider Billing for Clininc
# 	Rollup->ProviderEDocs($form, $ProvID, "Billing");
# }

# if ( $rProvider->{Type} == 2 ) {
# 	# If Agency
# 	# Rollup->ProviderEDocs($form, $ProvID, "Billing837");
# 	Rollup->ProviderEDocs($form, $ProvID, "ProviderPay");
# 	Rollup->ProviderEDocs($form, $ProvID, "Treatment");
# }

# my $cnt = Rollup->Notes($form,'',$ProvID); # Progress
$sProvider->finish();
warn qq|Rollup complete: ${Location}\n\n|;
myDBI->cleanup();
print qq|Location: ${Location}\n\n|;
exit;
############################################################################
