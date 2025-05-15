#!/usr/bin/perl
use strict;
use lib 'C:/xampp/htdocs/src/lib';
use Cwd;
use DBI;
use myForm;
use myDBI;
use NewCrop;

###################################################################################
# arguments: DBNAME, ClientID, requestedPage=Meds|xxx
# UserRole: set to LOGINPROVID
###################################################################################
my $form = myForm->new();
my $dbh  = myDBI->dbconnect( $form->{'DBNAME'} );

# Specify the URL...
my $UseProduction =
     $form->{'DBNAME'} eq 'okmis_demo'
  || $form->{'DBNAME'} eq 'okmis_dev'
  || $form->{'LOGINPROVID'} == 2501
  || $form->{'LOGINPROVID'} == 2502
  || $form->{'LOGINPROVID'} == 2503 ? 0 : 1;
my $demo = $UseProduction ? '' : 'demo';
my $webpage =
  $UseProduction
  ? 'https://secure.newcropaccounts.com/InterfaceV7/RxEntry.aspx'
  : 'https://preproduction.newcropaccounts.com/InterfaceV7/RxEntry.aspx';

#warn qq|NewCrop: UseProduction=${UseProduction}\ndemo=${demo}\nwebpage=${webpage}\n|;
#my $webpage="https://preproduction.newcropaccounts.com/InterfaceV7/RxEntry.aspx";
# Set the xml Form Field RxInput...
my ( $err, $xml ) = main->setRxInput( $form->{'requestedPage'} );
my $pwd = cwd();

#my $text = qq|\nDBNAME:$form->{DBNAME}\nPROVID:$form->{LOGINPROVID}\nClientID:$form->{ClientID}\nwebpage:${webpage}\n|;
#DBUtil->email($form,"support\@okmis.com","NewCrop: $form->{'LOGINUSERNAME'}",$text);
#warn qq|NewCrop: pwd=$pwd\nrequestedPage=$form->{'requestedPage'}\n|;
#warn qq|NewCrop: write to nc.xml\n|;
open( OUT, ">nc.xml" );
print OUT $pwd . "\n";
print OUT $xml;
close OUT;

myDBI->cleanup();

if ( $err ne '' || $form->{test} ) {
    my $str = '';
    while ( $xml =~ /([^\n]+)\n?/g ) {
        $str .= DBA->subxml($1) . "\n" unless ( $1 =~ /password/ );
    }
    my $errors = $err ne '' ? qq|ERRORS:\n${err}| : qq|Errors: NONE|;
    print qq|Content-Type: text/html; charset=ISO-8859-1

<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.0 Transitional//EN" >
<html>
 <head> <title>Driver</title> </head>
 <body>
<pre>
${errors}

${str}
</pre>
 </body>
</html>
|;
}
else {
    $xml = DBA->subxml($xml);    # strip bad stuff...
    print qq|Content-Type: text/html; charset=ISO-8859-1

<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.0 Transitional//EN" >
<html>
 <head> <title>Driver</title> </head>
 <body>
  <form id="info" name="info" method="post" action="${webpage}">
   <textarea id="RxInput" name="RxInput" rows="33" cols="79" style="display:none" >${xml}</textarea>
  </form>
 </body>
 <script>window.onLoad = document.info.submit();</script> 
</html>
|;
}
exit;
###################################################################################
sub setRxInput {
    my ( $self, $requestedPage ) = @_;

#warn qq|setRxInput: requestedPage=${requestedPage}, select Client $form->{ClientID}\n|;
    my $sClient = $dbh->prepare("select * from Client where Client.ClientID=?");
    $sClient->execute( $form->{'ClientID'} )
      || myDBI->dberror("setRxInput: select Client $form->{ClientID}");
    my $rClient   = $sClient->fetchrow_hashref;
    my $ClientID  = $rClient->{'ClientID'};
    my $PatientID = $form->{'DBNAME'} . '-' . $ClientID;

    #warn qq|setRxInput: PatientID=${PatientID}, ClientID=${ClientID}\n|;
    my $Zip = substr( $rClient->{Zip}, 0, 5 );
    ( my $HomePhone   = $rClient->{HmPh} ) =~ s/[- ]//g;
    ( my $DateOfBirth = $rClient->{DOB} )  =~ s/[- ]//g;
    my $sClientVitalSigns = $dbh->prepare(
        "select * from ClientVitalSigns where ClientID=? order by VDate desc");
    $sClientVitalSigns->execute($ClientID)
      || myDBI->dberror("setRxInput: select ClientVitalSigns ${ClientID}");
    my $rClientVitalSigns = $sClientVitalSigns->fetchrow_hashref;
    my $height            = ( $rClientVitalSigns->{'HeightFeet'} * 12 ) +
      $rClientVitalSigns->{'HeightInches'};
    my $weight    = $rClientVitalSigns->{'Weight'};
    my $ProvID    = $rClient->{ProvID};
    my $sProvider = $dbh->prepare("select * from Provider where ProvID=?");
    $sProvider->execute($ProvID) || myDBI->dberror("select Provider $ProvID");
    my $rPrimaryProvider = $sProvider->fetchrow_hashref;
    NewCrop->new( $form, '', $form->{'LOGINPROVID'}, $ClientID );
    my $Prescriber =
        NewCrop->isPrescriber($form)
      ? NewCrop->Prescriber($form)
      : NewCrop->Staff($form);
    my $SupervisingPhysician =
        NewCrop->provider('code') eq 'M'
      ? NewCrop->SupervisingPhysician($form)
      : '';

    #warn qq|setRxInput: Prescriber=${Prescriber}\n|;

    my $xml = qq|
<?xml version="1.0" encoding="utf-8"?>

<NCScript xmlns="http://secure.newcropaccounts.com/interfaceV7"
          xmlns:NCStandard="http://secure.newcropaccounts.com/interfaceV7:NCStandard"
          xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance">
| . NewCrop->Credentials($demo) . NewCrop->UserRole($form) . qq|
  <Destination>
    <!-- See XML Schema: RequestedPageType for valid values -->
    <requestedPage>${requestedPage}</requestedPage>
  </Destination>
  <Account ID="| . NewCrop->agency('AccountID') . qq|">
    <accountName>| . NewCrop->agency('accountName') . qq|</accountName>
    <siteID>| . NewCrop->agency('siteID') . qq|</siteID>
    <AccountAddress>
      <address1>| . NewCrop->agency('Addr1') . qq|</address1>
      <address2>| . NewCrop->agency('Addr2') . qq|</address2>
      <city>| . NewCrop->agency('City') . qq|</city>
      <state>| . NewCrop->agency('ST') . qq|</state>
      <zip>| . NewCrop->agency('ZipCode') . qq|</zip>
      <zip4>| . NewCrop->agency('ZipPlus') . qq|</zip4>
      <country>US</country>
    </AccountAddress>
    <accountPrimaryPhoneNumber>|
      . NewCrop->agency('accountPrimaryPhoneNumber')
      . qq|</accountPrimaryPhoneNumber>
    <accountPrimaryFaxNumber>|
      . NewCrop->agency('accountPrimaryFaxNumber')
      . qq|</accountPrimaryFaxNumber>
  </Account>
  <Location ID="| . NewCrop->clinic('LocationID') . qq|">
    <locationName>| . NewCrop->clinic('locationName') . qq|</locationName>
    <LocationAddress>
      <address1>| . NewCrop->clinic('Addr1') . qq|</address1>
      <address2>| . NewCrop->clinic('Addr2') . qq|</address2>
      <city>| . NewCrop->clinic('City') . qq|</city>
      <state>| . NewCrop->clinic('ST') . qq|</state>
      <zip>| . NewCrop->clinic('ZipCode') . qq|</zip>
      <zip4>| . NewCrop->clinic('ZipPlus') . qq|</zip4>
      <country>US</country>
    </LocationAddress>
    <primaryPhoneNumber>|
      . NewCrop->clinic('primaryPhoneNumber')
      . qq|</primaryPhoneNumber>
    <primaryFaxNumber>|
      . NewCrop->clinic('primaryFaxNumber')
      . qq|</primaryFaxNumber>
    <pharmacyContactNumber>|
      . NewCrop->clinic('pharmacyContactNumber')
      . qq|</pharmacyContactNumber>
  </Location>| . $SupervisingPhysician . $Prescriber . qq|
  <Patient ID="${PatientID}">
    <PatientName>
      <last>$rClient->{'LName'}</last>
      <first>$rClient->{'FName'}</first>
      <middle>$rClient->{'MName'}</middle>
    </PatientName>
    <medicalRecordNumber>${PatientID}</medicalRecordNumber>
    <memo>$rClient->{'WHAT'}</memo>
    <PatientAddress>
      <address1>$rClient->{'Addr1'}</address1>
      <address2>$rClient->{'Addr2'}</address2>
      <city>$rClient->{'City'}</city>
      <state>$rClient->{'ST'}</state>
      <zip>${Zip}</zip>
      <country>US</country>
    </PatientAddress>
    <PatientContact>
      <homeTelephone>${HomePhone}</homeTelephone>
    </PatientContact>
    <PatientCharacteristics>
      <dob>${DateOfBirth}</dob>
      <gender>$rClient->{'Gend'}</gender>
      <height>${height}</height>
      <heightUnits>inches</heightUnits>
      <weight>${weight}</weight>
      <weightUnits>lbs.</weightUnits>
    </PatientCharacteristics>
| . main->ptGuarantor( $requestedPage, $rClient ) . qq|
| . main->ptInsurance( $requestedPage, $rClient, 1 ) . qq|
| . main->ptAllergies( $requestedPage, $rClient ) . qq|
| . main->EncounterId($requestedPage) . qq|
  </Patient>
| . main->ptMedications( $requestedPage, $rClient ) . qq|
</NCScript>
|;
    $sClient->finish();
    $sClientVitalSigns->finish();
    $sProvider->finish();

    # eliminate null values ...
    my $str = '';
    foreach my $line ( split( /\n/, $xml ) ) {
        $str .= $line . "\n" unless ( $line =~ m/></ );
    }
    my $err = main->checkForErrors( $rClient, $height, $weight );
    return ( $err, $str );
}

sub checkForErrors {
    my ( $self, $rClient, $height, $weight ) = @_;
    my $err = '';
    my $Zip = substr( $rClient->{'Zip'}, 0, 5 );
    ( my $HomePhone   = $rClient->{'HmPh'} ) =~ s/[- ]//g;
    ( my $DateOfBirth = $rClient->{'DOB'} )  =~ s/[- ]//g;
    if ( NewCrop->provider('user') eq '' ) {
        $err .= qq|>>>Login Provider MISSING user for UserRole!\n|;
    }
    if ( NewCrop->provider('role') eq '' ) {
        $err .= qq|>>>Login Provider MISSING role for UserRole!\n|;
    }
    if ( $form->{'requestedPage'} eq '' ) {
        $err .= qq|>>>requestedPage MISSING!\n|;
    }
    if ( NewCrop->agency('AccountID') eq '' ) {
        $err .= qq|>>>Agency AccountID MISSING!\n|;
    }
    if ( NewCrop->agency('accountName') eq '' ) {
        $err .= qq|>>>Agency accountName MISSING!\n|;
    }
    if ( NewCrop->agency('siteID') eq '' ) {
        $err .= qq|>>>Agency siteID MISSING!\n|;
    }
    if ( NewCrop->agency('Addr1') eq '' ) {
        $err .= qq|>>>Agency Addr1 MISSING!\n|;
    }
    if ( NewCrop->agency('City') eq '' ) {
        $err .= qq|>>>Agency City MISSING!\n|;
    }
    if ( NewCrop->agency('ST') eq '' ) { $err .= qq|>>>Agency ST MISSING!\n|; }
    if ( NewCrop->agency('ZipCode') eq '' ) {
        $err .= qq|>>>Agency ZipCode MISSING!\n|;
    }
    if ( NewCrop->agency('accountPrimaryPhoneNumber') eq '' ) {
        $err .= qq|>>>Agency Primary Phone Number MISSING!\n|;
    }
    if ( NewCrop->agency('accountPrimaryFaxNumber') eq '' ) {
        $err .= qq|>>>Agency Primary Fax Number MISSING!\n|;
    }
    if ( NewCrop->clinic('LocationID') eq '' ) {
        $err .= qq|>>>Clinic LocationID MISSING!\n|;
    }
    if ( NewCrop->clinic('locationName') eq '' ) {
        $err .= qq|>>>Clinic LocationName MISSING!\n|;
    }
    if ( NewCrop->clinic('Addr1') eq '' ) {
        $err .= qq|>>>Clinic Addr1 MISSING!\n|;
    }
    if ( NewCrop->clinic('City') eq '' ) {
        $err .= qq|>>>Clinic City MISSING!\n|;
    }
    if ( NewCrop->clinic('ST') eq '' ) { $err .= qq|>>>Clinic ST MISSING!\n|; }
    if ( NewCrop->clinic('ZipCode') eq '' ) {
        $err .= qq|>>>Clinic ZipCode MISSING!\n|;
    }
    if ( NewCrop->clinic('primaryPhoneNumber') eq '' ) {
        $err .= qq|>>>Clinic primary Phone Number MISSING!\n|;
    }
    if ( NewCrop->clinic('primaryFaxNumber') eq '' ) {
        $err .= qq|>>>Clinic primary Fax Number MISSING!\n|;
    }
    if ( NewCrop->clinic('pharmacyContactNumber') eq '' ) {
        $err .= qq|>>>Clinic pharmacy Contact Number MISSING!\n|;
    }
    if ( NewCrop->provider('code') eq 'M' ) {
        if ( NewCrop->supervisor('LName') eq '' ) {
            $err .= qq|>>>Supervising Physician Last Name MISSING!\n|;
        }
        if ( NewCrop->supervisor('FName') eq '' ) {
            $err .= qq|>>>Supervising Physician First Name MISSING!\n|;
        }
        if ( NewCrop->supervisor('dea') eq '' ) {
            $err .= qq|>>>Supervising Physician dea Number MISSING!\n|;
        }
        if ( NewCrop->supervisor('licenseState') eq '' ) {
            $err .= qq|>>>Supervising Physician license State MISSING!\n|;
        }
        if ( NewCrop->supervisor('licenseNumber') eq '' ) {
            $err .= qq|>>>Supervising Physician license Number MISSING!\n|;
        }
        if ( NewCrop->supervisor('npi') eq '' ) {
            $err .= qq|>>>Supervising Physician NPI Number MISSING!\n|;
        }
    }
    if ( NewCrop->prescriber('LName') eq '' ) {
        $err .= qq|>>>Prescriber Last Name MISSING!\n|;
    }
    if ( NewCrop->prescriber('FName') eq '' ) {
        $err .= qq|>>>Prescriber First Name MISSING!\n|;
    }
    if ( NewCrop->isPrescriber($form) ) {
        if ( NewCrop->prescriber('dea') eq '' ) {
            $err .= qq|>>>Prescriber dea Number MISSING!\n|;
        }
        if ( NewCrop->prescriber('licenseState') eq '' ) {
            $err .= qq|>>>Prescriber license State MISSING!\n|;
        }
        if ( NewCrop->prescriber('licenseNumber') eq '' ) {
            $err .= qq|>>>Prescriber license Number MISSING!\n|;
        }
        if ( NewCrop->prescriber('npi') eq '' ) {
            $err .= qq|>>>Prescriber NPI Number MISSING!\n|;
        }
    }
    if ( $rClient->{'ClientID'} eq '' ) {
        $err .= qq|>>>Patient ID MISSING (ClientID)!\n|;
    }
    if ( $rClient->{'LName'} eq '' ) {
        $err .= qq|>>>Patient Last Name MISSING!\n|;
    }
    if ( $rClient->{'FName'} eq '' ) {
        $err .= qq|>>>Patient First Name MISSING!\n|;
    }
    if ( $rClient->{'Addr1'} eq '' ) {
        $err .= qq|>>>Patient Addr1 MISSING!\n|;
    }
    if ( $rClient->{'City'} eq '' ) { $err .= qq|>>>Patient City MISSING!\n|; }
    if ( $rClient->{'ST'} eq '' )   { $err .= qq|>>>Patient ST MISSING!\n|; }
    if ( ${Zip} eq '' )             { $err .= qq|>>>Patient Zip MISSING!\n|; }
    if ( ${HomePhone} eq '' ) { $err .= qq|>>>Patient HomePhone MISSING!\n|; }
    if ( ${DateOfBirth} eq '' ) {
        $err .= qq|>>>Patient DateOfBirth MISSING!\n|;
    }
    if ( $rClient->{'Gend'} eq '' ) {
        $err .= qq|>>>Patient Gender MISSING!\n|;
    }
    if ( $weight eq '' ) { $err .= qq|>>>Patient Weight MISSING!\n|; }
    if ( $height eq '' || $height == 0 ) {
        $err .= qq|>>>Patient Height MISSING!\n|;
    }
    return ($err);
}

sub ptGuarantor {
    my ( $self, $reqPage, $rClient ) = @_;
    return () unless ( $reqPage eq 'lab-orders' );
    my $ClientID   = $rClient->{'ClientID'};
    my $xml        = '';
    my $sGuarantor = $dbh->prepare("select * from Guarantor where ClientID=?");
    $sGuarantor->execute($ClientID)
      || myDBI->dberror("select Guarantor ${ClientID}");
    my $rGuarantor = $sGuarantor->fetchrow_hashref;
    my $Rel        = main->getRelationship( $rGuarantor->{'ClientRel'} );

    #warn qq|Guarantor: Rel=$Rel\n|;
    $rGuarantor = $rClient if ( $Rel =~ /self/i );
    my $GuarantorID = $form->{'DBNAME'} . '-G' . $ClientID;
    my ( $zip, $zip4 ) = split( '-', $rGuarantor->{'Zip'} );
    ( my $HomePhone   = $rGuarantor->{HmPh} ) =~ s/[- ]//g;
    ( my $WorkPhone   = $rGuarantor->{WkPh} ) =~ s/[- ]//g;
    ( my $DateOfBirth = $rGuarantor->{DOB} )  =~ s/[- ]//g;
    $xml .= qq|
    <PatientGuarantor ID="${GuarantorID}"> <!--Assign a unique ID for each PatientGuarantor-->
      <GuarantorName>
        <last>$rGuarantor->{'LName'}</last>
        <first>$rGuarantor->{'FName'}</first>
        <middle>$rGuarantor->{'MName'}</middle>
      </GuarantorName>
      <guarantorDob>${DateOfBirth}</guarantorDob>
      <guarantorGender>$rGuarantor->{'Gend'}</guarantorGender>
      <GuarantorAddress>
        <address1>$rGuarantor->{'Addr1'} Somestreet</address1>
        <address2>$rGuarantor->{'Addr2'} 123</address2>
        <city>$rGuarantor->{'City'}</city>
        <state>$rGuarantor->{'ST'}</state>
        <zip>${zip}</zip>
        <zip4>${zip4}</zip4>
        <country>US</country>
      </GuarantorAddress>
      <GuarantorContact>
        <homeTelephone>${HomePhone}</homeTelephone>
        <workTelephone>${WorkPhone}</workTelephone>
      </GuarantorContact>
      <guarantorRelationship>${Rel}</guarantorRelationship> <!--Self, Spouse, Child, Employer, Unknown-->
    </PatientGuarantor>
|;
    $sGuarantor->finish();
    return ($xml);
}

sub ptInsurance {
    my ( $self, $reqPage, $rClient, $Priority ) = @_;
    return () unless ( $reqPage eq 'lab-orders' );
    my $ClientID      = $rClient->{'ClientID'};
    my @PriorityNames = ( '', 'Primary', 'Secondary', 'Tertirary' );
    my $xml           = '';
    my $sInsurance    = $dbh->prepare(
"select * from Insurance where ClientID=? and Priority=? and InsNumEffDate<=curdate() and (curdate()<=InsNumExpDate or InsNumExpDate is NULL)"
    );
    $sInsurance->execute( $ClientID, $Priority )
      || myDBI->dberror("select Insurance ${ClientID}");
    if ( my $rInsurance = $sInsurance->fetchrow_hashref ) {
        my $sxInsurance = $dbh->prepare("select * from xInsurance where ID=?");
        $sxInsurance->execute( $rInsurance->{InsID} )
          || myDBI->dberror("select xInsurance $rInsurance->{InsID}");
        my $rxInsurance = $sxInsurance->fetchrow_hashref;
        my ( $pzip, $pzip4 ) = split( '-', $rxInsurance->{'Zip'} );
        my $InsProv =
          main->getinsuranceServiceProvider( $rxInsurance->{'Name'} );

        my $Rel = main->getRelationship( $rInsurance->{'ClientRel'} );
        my ( $izip, $izip4 ) = split( '-', $rClient->{'Zip'} );
        ( my $DateOfBirth = $rClient->{DOB} )  =~ s/[- ]//g;
        ( my $HomePhone   = $rClient->{HmPh} ) =~ s/[- ]//g;

        $xml .= qq|
    <PatientPayorAndInsured ID="$rxInsurance->{PayID}"> <!--ID is the HSI number-->
      <payor>
        <payorName>$rxInsurance->{'Name'}</payorName>
        <PayorAddress>
          <address1>$rxInsurance->{'Addr1'}</address1>
          <address2>$rxInsurance->{'Addr2'}</address2>
          <city>$rxInsurance->{'City'}</city>
          <state>$rxInsurance->{'ST'}</state>
          <zip>${pzip}</zip>
          <zip4>${pzip4}</zip4>
          <country>US</country>
        </PayorAddress>
        <insuranceServiceProvider>${InsProv}</insuranceServiceProvider> <!--Medicare, Medicaid, BCBS, Other-->
        <payorGroupNumber>$rInsurance->{'GrpNum'}</payorGroupNumber>
      </payor>
      <insured>
        <patientRelationship>${Rel}</patientRelationship>
        <priorityCode>$PriorityNames[$Priority]</priorityCode> <!--Primary, Secondary, Tertirary-->
        <policyNumber>$rInsurance->{'InsIDNum'}</policyNumber>
        <groupNumber>$rInsurance->{'GrpNum'}</groupNumber>
        <InsuredName>
          <last>$rClient->{'LName'}</last>
          <first>$rClient->{'FName'}</first>
          <middle>$rClient->{'MName'}</middle>
        </InsuredName>
        <InsuredAddress>
          <address1>$rClient->{'Addr1'}</address1>
          <address2>$rClient->{'Addr2'}</address2>
          <city>$rClient->{'City'}</city>
          <state>$rClient->{'ST'}</state>
          <zip>${izip}</zip>
          <zip4>${izip4}</zip4>
          <country>US</country>
        </InsuredAddress>
        <insuredDob>${DateOfBirth}</insuredDob>
        <insuredGender>$rClient->{'Gend'}</insuredGender>
        <InsuredContact>
          <homeTelephone>${HomePhone}</homeTelephone>
        </InsuredContact>
      </insured>
    </PatientPayorAndInsured>
|;
        $sxInsurance->finish();
    }
    $sInsurance->finish();
    return ($xml);
}

# ClientAllergies -> okmis_config-xAllergies
#   xAllergies is built from the: tblcompositeallergy.txt received from NewCrop
#   The AID=ID in xAllergies, the ID from tblcompositeallergy.txt
sub ptAllergies {
    my ( $self, $reqPage, $rClient ) = @_;
    return () unless ( $reqPage eq 'compose' );
    my $ClientID         = $rClient->{'ClientID'};
    my $xml              = '';
    my $sClientAllergies = $dbh->prepare(
        "select * from ClientAllergies where ClientID=? and AID is not null");
    $sClientAllergies->execute($ClientID)
      || myDBI->dberror("select ClientAllergies ${ClientID}");
    while ( my $rClientAllergies = $sClientAllergies->fetchrow_hashref ) {
        my $Reaction =
          DBA->getxref( $form, 'xAdverseReaction', $rClientAllergies->{RID},
            'ConceptName' );
        ( my $Comments = $rClientAllergies->{'Comments'} ) =~ s/"//g;

        #warn qq|NewCrop: Reaction=${Reaction}, Comments=${Comments}\n|;
        $Reaction .= ' ' . $Comments unless ( $Comments eq '' );

        #warn qq|NewCrop: Reaction=${Reaction}\n|;
        $xml .= qq|
    <PatientAllergies>
      <allergyID>$rClientAllergies->{'AID'}</allergyID>
      <allergyTypeID>FDB</allergyTypeID>
      <allergySeverityTypeID>$rClientAllergies->{'Severity'}</allergySeverityTypeID>
      <allergyComment>| . DBA->subxml($Reaction) . qq|</allergyComment>
   </PatientAllergies>
|;
    }
    $sClientAllergies->finish();
    return ($xml);
}

sub EncounterId {
    my ( $self, $reqPage ) = @_;
    my $xml = '';
    if ( $reqPage eq 'compose' ) {
        $xml = qq|        <EncounterIdentifier>102</EncounterIdentifier>|;
    }
    return ($xml);
}

sub ptMedications {
    my ( $self, $reqPage, $rClient ) = @_;
    return () unless ( $reqPage eq 'compose' );
    my $ClientID = $rClient->{'ClientID'};
    my $xml      = '';
    my $sClientMeds =
      $dbh->prepare("select * from ClientMeds where ClientID=?");
    $sClientMeds->execute($ClientID)
      || myDBI->dberror("select ClientMeds ${ClientID}");
    my $rClientMeds = $sClientMeds->fetchrow_hashref;
    my $cnt         = $sClientMeds->rows();
    $sClientMeds->finish();

    #warn qq|Meds: ClientID=${ClientID}, cnt=$cnt\n|;
    return () if ($cnt);

    #  return();

    my $sPDMed = $dbh->prepare(
        "select * from PDMed where ClientID=? and MedActive=1 and Locked=0");
    $sPDMed->execute($ClientID) || myDBI->dberror("select PDMed ${ClientID}");
    while ( my $rPDMed = $sPDMed->fetchrow_hashref ) {
        ( my $startDate = $rPDMed->{StartDate} ) =~ s/[- ]//g;
        my $MedName =
          DBA->getxref( $form, 'xMedNames', $rPDMed->{MedID}, 'TradeName' );
        my $Freq =
          DBA->getxref( $form, 'xMedFreq', $rPDMed->{MedFreq}, 'Text' );
        my $rPhys = DBA->selxref( $form, 'xNPI', 'NPI', $rPDMed->{PhysNPI} );
        my $doctorName =
            $rPhys->{'ProvPrefix'} . ' '
          . $rPhys->{'ProvLastName'} . ' '
          . $rPhys->{'ProvMiddleName'} . ' '
          . $rPhys->{'ProvFirstName'} . ' '
          . $rPhys->{'ProvSuffix'};
        $doctorName =~ s/^\s+|\s+$//g;
        $xml .= qq|
  <OutsidePrescription>
    <externalId>$rPDMed->{'MedID'}</externalId>
    <date>${startDate}</date>
    <doctorName>${doctorName}</doctorName>
    <drug>${MedName} $rPDMed->{'MedDos'}</drug>
    <dispenseNumber>$rPDMed->{'Count'}</dispenseNumber>
    <sig>$Freq</sig>
    <refillCount>$rPDMed->{'Refills'}</refillCount>
    <prescriptionType>reconcile</prescriptionType>
  </OutsidePrescription>
|;
        my $sLock = $dbh->prepare("update PDMed set Locked=1 where PDMedID=?");
        $sLock->execute( $rPDMed->{PDMedID} )
          || myDBI->dberror("NewCrop: Lock PDMed:$rPDMed->{PDMedID}");
        $sLock->finish();

        #warn qq|Meds: set Locked to 1: PDMedID=$rPDMed->{PDMedID}\n|;
    }
    $sPDMed->finish();
    return ($xml);
}
###################################################################################
sub getRelationship {
    my ( $self, $relation ) = @_;
    my $rel =
        $relation =~ /|I/      ? 'Self'
      : $relation =~ /W|H/     ? 'Spouse'
      : $relation =~ /SON|DAU/ ? 'Child'
      : $relation =~ /EMP/     ? 'Employer'
      :                          'Unknown';
    return ($rel);
}

sub getinsuranceServiceProvider {
    my ( $self, $insurancename ) = @_;
    my $ins =
        $insurancename =~ /medicaid/ ? 'Medicaid'
      : $insurancename =~ /medicare/ ? 'Medicare'
      : $insurancename =~ /bcbs/     ? 'BCBS'
      :                                'Other';
    return ($ins);
}
###################################################################################
