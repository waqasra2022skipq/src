package prt;

############################################################################
sub getMeds
{
  my ($self,$ClientID) = @_;
  my ($out,$cnt) = ('',0);
  my $qPDMed = qq|select * from PDMed where ClientID=? order by MedEffDate|;
  my $sPDMed = $dbh->prepare($qPDMed);
  $sPDMed->execute($ClientID);
  while ( $rPDMed = $sPDMed->fetchrow_hashref )
  {
    my $rxNPI = DBA->selxref($form,'xNPI','NPI',$rPDMed->{'PhysNPI'});
    my $ProvName = $rxNPI->{'ProvLastName'};
    $ProvName .= ', ' . substr($rxNPI->{'ProvFirstName'},0,1) if ( $rxNPI->{'ProvFirstName'} ne '' );
    $out .= qq|      <medications>\n|;
PhysicianName
    $out .= qq|       <physician>${ProvName}</physician>\n|;
PhysicianName

DrugInfo
    $out .= qq|       <medication>| . DBA->getxref($form,'xMedNames',$rPDMed->{MedID},'TradeName') . qq|</medication>\n|;
DrugInfo

    $out .= qq|       <type>| . DBA->getxref($form,'xMedType',$rPDMed->{MedType},'Abbr') . qq|</type>\n|;

PatientFriendlySIG
    $out .= qq|       <dosage>| . DBA->subxml($rPDMed->{'MedDos'}) . qq|</dosage>\n|;
    $out .= qq|       <frequency>| . DBA->subxml($rPDMed->{'MedFreq'}) . qq|</frequency>\n|;
    $out .= qq|       <route>| . DBA->getxref($form,'xMedRoute',$rPDMed->{Route},'Descr') . qq|</route>\n|;
PatientFriendlySIG

PrescriptionDate
    $out .= qq|       <startdate>| . DBUtil->Date($rPDMed->{StartDate},'fmt','MM/DD/YYYY') . qq|</startdate>|;
PrescriptionDate

    $out .= qq|       <reason>| . DBA->subxml($rPDMed->{Benefits}) . qq|</reason>\n|;
    $out .= qq|       <sideeffects>| . DBA->getxref($form,'xSideEff',$rPDMed->{MedSEff},'Descr') . qq|</sideeffects>\n|;
    $out .= qq|      </medications>\n|;
    $cnt++;
  }
  $sPDMed->finish();
  $out = qq|      <medications><physician>None</physician></medications>\n| unless ( $cnt );
  return($out);
}


CREATE TABLE `ClientMeds` (
  `ID` int(11) NOT NULL AUTO_INCREMENT,
  `ClientID` int(11) DEFAULT NULL,
  `CreateProvID` int(11) DEFAULT NULL,
  `CreateDate` date DEFAULT NULL,
  `ChangeProvID` int(11) DEFAULT NULL,
  `ChangeDate` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  `FormID` varchar(12) DEFAULT NULL,
  `Active` char(1) NOT NULL,
  `PrescriptionDate` datetime NOT NULL,
  `DrugID` varchar(20) NOT NULL,
  `DrugTypeID` char(1) NOT NULL,
  `DrugName` varchar(30) NOT NULL,
  `DrugInfo` varchar(200) DEFAULT NULL,
  `Strength` varchar(15) DEFAULT NULL,
  `StrengthUOM` varchar(15) DEFAULT NULL,
  `DosageNumberDescription` varchar(50) DEFAULT NULL,
  `DosageForm` varchar(50) DEFAULT NULL,
  `Route` varchar(50) DEFAULT NULL,
  `DosageFrequencyDescription` varchar(50) DEFAULT NULL,
  `Dispense` varchar(100) DEFAULT NULL,
  `TakeAsNeeded` char(1) NOT NULL,
  `DispenseAsWritten` char(1) NOT NULL,
  `Refills` tinyint(4) NOT NULL,
  `Status` char(1) NOT NULL,
  `SubStatus` char(1) NOT NULL,
  `Archive` char(1) NOT NULL,
  `PrescriptionGuid` varchar(64) NOT NULL,
  `OrderGUID` varchar(64) DEFAULT NULL,
  `PrescriptionNotes` varchar(255) DEFAULT NULL,
  `PharmacistNotes` varchar(255) DEFAULT NULL,
  `ExternalPhysicianID` varchar(50) DEFAULT NULL,
  `PhysicianName` varchar(176) DEFAULT NULL,
  `DateMovedToPreviousMedications` varchar(1) NOT NULL,
  `FormularyType` varchar(20) DEFAULT NULL,
  `FormularyTypeID` varchar(1) NOT NULL,
  `FormularyMember` varchar(50) DEFAULT NULL,
  `FormularyId` varchar(50) DEFAULT NULL,
  `FormularyStatus` varchar(2) DEFAULT NULL,
  `ModifiedSig` bit(1) DEFAULT NULL,
  `ModifiedSigStatus` varchar(1) DEFAULT NULL,
  `ExternalPrescriptionID` varchar(50) NOT NULL,
  `EpisodeIdentifier` varchar(40) NOT NULL,
  `EncounterIdentifier` varchar(40) NOT NULL,
  `ExternalSource` varchar(1) DEFAULT NULL,
  `ExternalDrugConcept` varchar(105) DEFAULT NULL,
  `ExternalDrugName` varchar(35) DEFAULT NULL,
  `ExternalDrugStrength` varchar(35) DEFAULT NULL,
  `ExternalDrugStrengthUOM` varchar(35) DEFAULT NULL,
  `ExternalDrugStrengthWithUOM` varchar(35) DEFAULT NULL,
  `ExternalDrugDosageForm` varchar(35) DEFAULT NULL,
  `ExternalDrugRoute` varchar(35) DEFAULT NULL,
  `ExternalDrugIdentifier` varchar(35) DEFAULT NULL,
  `ExternalDrugIdentifierType` varchar(35) DEFAULT NULL,
  `ExternalDrugSchedule` varchar(1) DEFAULT NULL,
  `ExternalDrugOTC` varchar(1) DEFAULT NULL,
  `DosageNumberTypeID` smallint(6) NOT NULL,
  `DosageFormTypeId` tinyint(4) NOT NULL,
  `DosageRouteTypeId` tinyint(4) NOT NULL,
  `DosageFrequencyTypeID` smallint(6) NOT NULL,
  `DaysSupply` int(11) NOT NULL,
  `PrescriptionTimestamp` datetime NOT NULL,
  `OriginalPrescriptionGuid` varchar(64) NOT NULL,
  `ExternalUserID` varchar(50) NOT NULL,
  `ExternalUserType` varchar(1) NOT NULL,
  `DeaGenericNamedCode` varchar(1) NOT NULL,
  `Diagnosis` varchar(20) NOT NULL,
  `DiagnosisSource` varchar(6) NOT NULL,
  `DiagnosisName` varchar(200) NOT NULL,
  `DispenseNumberQualifier` varchar(50) NOT NULL,
  `DispenseNumberQualifierDescription` varchar(50) NOT NULL,
  `LocationName` varchar(100) NOT NULL,
  `GenericName` varchar(30) NOT NULL,
  `PatientFriendlySIG` varchar(140) NOT NULL,
  `PrintLeaflet` varchar(1) NOT NULL,
  `DeaClassCode` varchar(1) NOT NULL,
  `PharmacyType` int(11) NOT NULL,
  `PharmacyDetailType` tinyint(4) NOT NULL,
  `FinalDestinationType` tinyint(4) NOT NULL,
  `FinalStatusType` tinyint(4) NOT NULL,
  `PatientID` varchar(50) DEFAULT NULL,
  `PatientIDType` varchar(1) NOT NULL,
  `rxcui` decimal(11,0) DEFAULT NULL,
  `DeaLegendDescription` varchar(2) NOT NULL,
  `DrugSubID1` varchar(20) DEFAULT NULL,
  `FormularyChecked` varchar(5) DEFAULT NULL,
  `SourcePrescriptionGuid` text,
  `StrengthUnknown` varchar(1) NOT NULL,
  PRIMARY KEY (`ID`),

############################################################################
1;
