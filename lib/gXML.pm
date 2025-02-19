package gXML;
use DBI;
use DBForm;
use myDBI;
use DBA;
use DBUtil;
use XML::LibXSLT;
use XML::LibXML;
binmode STDOUT, ":utf8";
my $debug = 1;
#############################################################################
# local gXML variable: access with $gXML::varname
#############################################################################
# input xml, output ccda.xml (text)
sub styleCCDA
{
  my ($self,$form,$xmlfile,$type) = @_;
##
# first read and parse the file
  my $xmlpath = $form->{'DOCROOT'}.$xmlfile;
  my $docfile = '';
# load_xml: initializes the parser and parse_file()
  eval { $docfile = XML::LibXML->load_xml(location => $xmlpath); };
  return('parse_error') if ( $@ );

# initialize XSLT processor and read [type] stylesheet
  my $xslt = XML::LibXSLT->new( );
  my $CCDAxsl = $form->{'DOCROOT'}.myConfig->cfgfile("CCDA_${type}.xsl",1);
  my $stylesheet_ccda = $xslt->parse_stylesheet_file( $CCDAxsl );
# next the generate/transform the CCDA file...
  my $ccdatrans = $stylesheet_ccda->transform( $docfile );
  my $ccdaout = $stylesheet_ccda->output_string( $ccdatrans );
  return($ccdaout);
}
# input xml, output qrda (text)
sub styleQRDA
{
  my ($self,$form,$xmlfile) = @_;
##
# first read and parse the file
  my $xmlpath = $form->{'DOCROOT'}.$xmlfile;
  my $docfile = '';
# load_xml: initializes the parser and parse_file()
  eval { $docfile = XML::LibXML->load_xml(location => $xmlpath); };
  return('parse_error') if ( $@ );

# initialize XSLT processor and read stylesheet
  my $xslt = XML::LibXSLT->new( );
  my $QRDAxsl = $form->{'DOCROOT'}.myConfig->cfgfile("QRDA1.xsl",1);
  my $stylesheet_qrda = $xslt->parse_stylesheet_file( $QRDAxsl );
# next the generate/transform the QRDA file...
  my $qrdatrans = $stylesheet_qrda->transform( $docfile );
  my $qrdaout = $stylesheet_qrda->output_string( $qrdatrans );
  return($qrdaout);
}
# input ccda, output cda.htm (text)
sub styleCDA
{
  my ($self,$form,$ccdafile) = @_;
# first read and parse the file
  my $ccdapath = $form->{'DOCROOT'}.$ccdafile;
  my $docfile = '';
# load_xml: initializes the parser and parse_file()
  eval { $docfile = XML::LibXML->load_xml(location => $ccdapath); };
  return('parse_error') if ( $@ );

# initialize XSLT processor and read stylesheet
  my $xslt = XML::LibXSLT->new( );
  my $CDAxsl = $form->{'DOCROOT'}.myConfig->cfgfile('CDA.xsl',1);
  my $stylesheet_cda = $xslt->parse_stylesheet_file( $CDAxsl );
# next generate the cda : transform and save result
  my %xslargs = $self->setCDAparms($form,$form->{'LOGINPROVID'});
  my $cdatrans = $stylesheet_cda->transform( $docfile , XML::LibXSLT::xpath_to_string(%xslargs));
  my $cdaout = $stylesheet_cda->output_string( $cdatrans );
  return($cdaout);
}
# reads a CDA and convert the CDA.xsl to /cfg directory.
#  NOT USED because the phimail converts it on download
sub readCDA
{
  my ($self,$form,$filename) = @_;
  my $out = '';
  my $filepath = $form->{'DOCROOT'}.$filename;
  local $/ = undef;
  if ( open(FILE,$filepath) )
  {
    binmode FILE;
    $out = <FILE>;
    $out =~ s|href="CDA.xsl"|href="/cfg/CDA.xsl"|;
    close(FILE);
  } else { return('open_error'); }
  return($out);
}
sub addXML
{
  my ($self,$form,$filepath) = @_;
warn qq|addXML: filepath=${filepath}=\n| if ( $debug );
warn qq|set ccda_ss=${filepath}=\n| if ( $debug );
warn qq|xmlfile=${xmlfile}=\n| if ( $debug );
  my $xmlfile = '/tmp/XML_'.DBUtil->genToken().'.xml';
  my $xmlpath = $form->{'DOCROOT'}.$xmlfile;
warn qq|write: xmlpath=${xmlpath}=\n| if ( $debug );
  my $result = `php /var/www/okmis/src/MU/parseCCDA.php ${filepath} > ${xmlpath} 2>${xmlpath}.err`;
warn qq|addXML: xmlfile=${xmlfile}=\n| if ( $debug );
  return($xmlfile);
}
sub setCDAparms
{ 
  my ($self,$form,$ProvID) = @_;
  my $dbh = myDBI->dbconnect($form->{'DBNAME'});
  my %in = (
    a1  => 'referrals-1',
    a2  => 'medications-1',
    a3  => 'care plan-0',
    a4  => 'chief complaint-1',
    a5  => 'functional status-1',
    a6  => 'family history-1',
    a7  => 'social history-1',
    a8  => 'immunizations-1',
    a9  => 'encounter diagnosis-1',
   a10  => 'medical equipment-1',
   a11  => 'results-1',
   a12  => 'meds administered-1',
   a13  => 'vital signs-1',
   a14  => 'discharge instructions-1',
   a15  => 'problems-1',
   a16  => 'health concerns-1',
   a17  => 'allergies-1',
   a18  => 'goals-1',
   a19  => 'procedures-1',
   a20  => 'assesments-1',
  );
  my %xslargs = ();
  my $sProviderCDAparms = $dbh->prepare("select * from ProviderCDAparms where ProvID=? order by Priority");
  $sProviderCDAparms->execute($ProvID) || $form->dberror("setCDAparms: select ProviderCDAparms");
  while ( my $rProviderCDAparms = $sProviderCDAparms->fetchrow_hashref )
  {
    my $arg = 'a'.$rProviderCDAparms->{'Priority'}/10;
    my $val = $rProviderCDAparms->{'Descr'}.'-'.$rProviderCDAparms->{'Visible'};
    $xslargs{$arg} = $val;
  }
  $sProviderCDAparms->finish();
  my $cnt = keys %xslargs;
warn qq|setCDAparms: count=$cnt\n| if ( $debug );
  %xslargs = %in unless ( $cnt );
  return(%xslargs);
}
#############################################################################
# these used without namespace...
sub getVALUE
{
  my ($self,$xmltree,$nodepath) = @_;
#warn qq|\ngetVALUE nodepath=${nodepath}\n|;
  my ($node) = $xmltree->findnodes($nodepath);
  if ( defined($node) )
  {
my $name = $node->nodeName;
warn qq|name=${name}\n| if ( $debug );
  (my $city = $node->textContent) =~ s/^\s*(.*?)\s*$/$1/g;   # trim both leading/trailing
  }
  return($city);
}
sub getNODES
{
  my ($self,$xmltree,$nodepath) = @_;
#warn qq|\ngetNODES nodepath=${nodepath}\n|;
  my @list = ();
  my ($nodes) = $xmltree->findnodes($nodepath);
  if ( defined($nodes) )
  {
    for my $node ($nodes->getChildrenByTagName('*'))
    {
my $name = $node->nodeName;
#warn qq|name=${name}\n|;
      (my $text = $node->textContent) =~ s/^\s*(.*?)\s*$/$1/g;   # trim both leading/trailing
      push(@list,$text); 
    }
  }
  return(@list);
}
sub getATTR
{
  my ($self,$xmltree,$nodepath) = @_;
#warn qq|\nwithattr nodepath=${nodepath}\n|;
  my @list = ();
  my ($nodes) = $xmltree->findnodes($nodepath);
  for my $node ($nodes->getChildrenByTagName('*'))
  {
my $name = $node->nodeName;
#warn qq|name=${name}\n|;
    (my $text = $node->textContent) =~ s/^\s*(.*?)\s*$/$1/g;   # trim both leading/trailing
    for my $attr ($node->attributes)
    { push(@list,$attr->getValue); }
    if( !$node->getChildrenByTagName('*') && $text ) { push(@list,$text); }
for my $attr ($node->attributes)
{ warn "value of ", $node->nodeName, ": attr=value: ", $attr->getName, "=", $attr->getValue, "\n"; }
if( !$node->getChildrenByTagName('*') && $text ) { warn "node=text: ${name}=${text}\n"; }
  }
  return(@list);
}
#############################################################################
#doc: <patientRoleObj> Client,ClientSocial; ClientIntake,ClientSocial Page
sub genPatient
{
  my ($self,$form,$rClient) = @_;
warn qq|genPatient: ClientID=$rClient->{'ClientID'}\n| if ( $debug );
  my $dbh = myDBI->dbconnect($form->{'DBNAME'});
  my $ClientID = $rClient->{'ClientID'};
  my $ClientAddr = $rClient->{'Addr1'};
  $ClientAddr .= ', ' . $rClient->{'Addr2'} if ( $rClient->{'Addr2'} ne '' );
  my $Gend = DBA->getxref($form,'xGend',$rClient->{Gend},'Descr');
  my ($Race,$Racedummy) = split(chr(253),$rClient->{'Race'});
warn qq|Race=$rClient->{'Race'}=\n| if ( $debug );
warn qq|Race=${Race}=, Racedummy=${Racedummy}=\n| if ( $debug );
  my $RaceGranularID = $Race eq '0000-0' ? 'UNK' : $Race;
warn qq|RaceGranularID=${RaceGranularID}=\n| if ( $debug );
  my $RaceGranularConcept = DBA->getxref($form,'xRaces',$Race,'Concept');
warn qq|RaceGranularConcept=${RaceGranularConcept}=\n| if ( $debug );
  $RaceGranularConcept =~ s/-//;
  my $RaceGranularCode = DBA->getxref($form,'xRaces',$Race,'Code');
warn qq|RaceGranularCode=${RaceGranularCode}=\n| if ( $debug );
  my ($RaceParent,$Codedummy) = split('\.',$RaceGranularCode);
warn qq|RaceParent=${RaceParent}=, Codedummy=${Codedummy}=\n| if ( $debug );
# we don't gather granular, so no reason to work up the Race tree.
  my $cdbh = myDBI->dbconnect('okmis_config');      # connect to the config database.
  my $sxRaces = $cdbh->prepare("select * from xRaces where Code=?");
  $sxRaces->execute($RaceParent) || $form->dberror("genPatient: select xRaces: ${RaceParent}");
  my $rxRaces = $sxRaces->fetchrow_hashref;
  my $RaceID = $rxRaces->{'ID'};
  my $RaceConcept = $rxRaces->{'Concept'};
  $RaceConcept =~ s/-//;
  my ($Ethnicity,$dummy) = split(chr(253),$rClient->{'Ethnicity'});
  my $EthnicityID = $Ethnicity eq '0000-0' ? 'UNK' : $Ethnicity;
  my $EthnicityConcept = DBA->getxref($form,'xEthnicity',$Ethnicity,'Concept');
  $EthnicityConcept =~ s/-//;
  (my $DOB = $rClient->{'DOB'}) =~ s/-//g;
  my $sClientSocial = $dbh->prepare("select * from ClientSocial where ClientID=?");
  $sClientSocial->execute($ClientID) || $form->dberror("genPatient: select ClientSocial: ${ClientID}");
  my $rClientSocial = $sClientSocial->fetchrow_hashref;
  my $PreLang = DBA->getxref($form,'xLanguages',$rClientSocial->{PreLang},'AltID');
# KLS ??? FIX our xInsurance table?
  my $sInsurance = $dbh->prepare("select Insurance.*,xInsurance.CQMID from Insurance left join xInsurance on xInsurance.ID=Insurance.InsID where Insurance.ClientID=? and Insurance.Priority=? order by Insurance.InsNumExpDate desc");
  #### and InsNumEffDate<=curdate() and (curdate()<=InsNumExpDate or InsNumExpDate is NULL)
warn qq|genPatient: call sInsurance=${ClientID}\n| if ( $debug );
  $sInsurance->execute($ClientID,1) || $form->dberror("genPatient: select Insurance ${ClientID}");
  my $rInsurance = $sInsurance->fetchrow_hashref;
  my $CQMID = $rInsurance->{'CQMID'};

  my $out = qq|
  <patientRoleObj>
    <patientAddress>
      <streetAddressLine>${ClientAddr}</streetAddressLine>
      <city>$rClient->{'City'}</city>
      <state>$rClient->{'ST'}</state>
      <postalCode>$rClient->{'Zip'}</postalCode>
      <country>US</country>
      <phone>$rClient->{'HmPh'}</phone>
      <mobile>$rClient->{'MobPh'}</mobile>
    </patientAddress>
    <raceCode>${RaceID}</raceCode>
    <race>${RaceConcept}</race>
    <granularRacecode>${RaceGranularID}</granularRacecode>
    <granularRace>${RaceGranularConcept}</granularRace>
    <patientSuffix>$rClient->{'Suffix'}</patientSuffix>
    <patientMiddleName>$rClient->{'MName'}</patientMiddleName>
    <patientFirstName>$rClient->{'FName'}</patientFirstName>
    <patientPreviousName>$rClient->{'MaidenName'}</patientPreviousName>
    <patientFamilyName>$rClient->{'LName'}</patientFamilyName>
    <administrativeGenderCode>$rClient->{'Gend'}</administrativeGenderCode>
    <administrativeGenderDisplayName>${Gend}</administrativeGenderDisplayName>
    <birthTime>${DOB}</birthTime>
    <ethnicGroupCode>${EthnicityID}</ethnicGroupCode>
    <ethnicGroupCodeDisplayName>${EthnicityConcept}</ethnicGroupCodeDisplayName>
    <languageCommunication>${PreLang}</languageCommunication>
    <insuranceProvider>${CQMID}</insuranceProvider>
    <mrn>${ClientID}</mrn>
  </patientRoleObj>|;
# xxx PrimaryProviderObj ??? FIX our Primary Provider
#doc: <PrimaryProviderObj...> NULL
  $out .= qq|
  <PrimaryProviderObj />|;
  $sxRaces->finish();
  $sClientSocial->finish();
  $sInsurance->finish();
  return($out);
}
sub genAllergies
{
  my ($self,$form,$rTreatment,$spc) = @_;
  my $dbh = myDBI->dbconnect($form->{'DBNAME'});
  my $ClientID = $rTreatment->{'ClientID'};
  my $idx = 0;
  my $out = qq|
${spc}<allergyListObj>|;
  my $s = $dbh->prepare("select ClientAllergies.*,xAllergies.MappedID as ACode,xAllergies.Descr as AName,xAdverseReaction.ConceptCode as RCode,xAdverseReaction.ConceptName as RName,xSeverity.Code as SCode from ClientAllergies left join okmis_config.xAllergies on xAllergies.ID=ClientAllergies.AID left join okmis_config.xAdverseReaction on xAdverseReaction.ID=ClientAllergies.RID left join okmis_config.xSeverity on xSeverity.Descr=ClientAllergies.Severity where ClientID=? and ClientAllergies.Severity is not null");
  $s->execute($ClientID) || $form->dberror("select ClientAllergies: ${ClientID}");
  while ( my $r = $s->fetchrow_hashref )
  {
    $idx++;
    (my $sdate = $r->{'StartDate'}) =~ s/-//g;
    (my $edate = $r->{'EndDate'}) =~ s/-//g;
    my $status = $r->{'EndDate'} eq '' ? 'Active' : 'Completed';
    $out .= qq|
${spc}  <Allergy>
${spc}    <id>ClientAllergies_$r->{'ID'}</id>
${spc}    <effectiveTimeLow>${sdate}</effectiveTimeLow>
${spc}    <participantCode>$r->{'ACode'}</participantCode>
${spc}    <codeSystem>2.16.840.1.113883.6.88</codeSystem>
${spc}    <participantDisplayName>$r->{'AName'}</participantDisplayName>
${spc}    <status>${status}</status>
${spc}    <reactionValueCode>$r->{'RCode'}</reactionValueCode>
${spc}    <reactionValueDisplayName>$r->{'RName'}</reactionValueDisplayName>
${spc}    <severityCode>$r->{'SCode'}</severityCode>
${spc}    <severityDisplayName>$r->{'Severity'}</severityDisplayName>
${spc}  </Allergy>|;
  }
  $out .= qq|
${spc}</allergyListObj>|;
  $s->finish();
#print qq|genAllergies: out=\n$out\n|;
# NewCrop Allergy values - if we ever get Allergies from NewCrop
#      <effectiveTimeLow>20070501</effectiveTimeLow>
#      <!-- NewCrop <OnsetDate>20150108</OnsetDate>-->
#      <participantCode>7980</participantCode>
#      <!-- NewCrop <Rxcui>2670</Rxcui>-->
#      <codeSystem>2.16.840.1.113883.6.88</codeSystem>
#      <!-- NewCrop Hard Coded-->
#      <participantDisplayName>Penicillin G benzathine</participantDisplayName>
#      <!-- NewCrop <AllergyName>Aspirin</AllergyName>-->
#      <status>Active</status>
#      <!-- NewCrop <Status>A</Status>-->
#      <reactionValueCode>247472004</reactionValueCode>
#      <!-- Optional  -->
#      <reactionValueDisplayName>Hives</reactionValueDisplayName>
#      <severityCode>6736007</severityCode>
#      <severityDisplayName>Moderate</severityDisplayName>
#      <!-- NewCrop <AllergySeverityName>Moderate</AllergySeverityName>-->
  return($out);
}
sub genParticipants
{
  my ($self,$form,$rTreatment,$table,$spc) = @_;
  my $dbh = myDBI->dbconnect($form->{'DBNAME'});
  my $TrID = $rTreatment->{'TrID'};
warn qq|genParticipants: ClientID=$rTreatment->{ClientID}, TrID=$rTreatment->{TrID}, table=${table}, spc=${spc}=\n| if ( $debug );
  my $idx = 0;
  my $tag = $table eq 'ClientNoteFamilyI' ? 'informant' : 'Participant';
  my $Participants = $table eq 'ClientNoteFamilyI' ? '' : qq|${spc}<participantListObj>|;
  my $s = $dbh->prepare("select * from ${table} where TrID=?");
  $s->execute($TrID) || $form->dberror("genParticipants: select ${table} ${TrID}");
  while ( my $r = $s->fetchrow_hashref )
  {
    $idx++;
    my $Relation = DBA->getxref($form,'xRelationship',$r->{Rel},'Descr');
    my $RelationCode = DBA->getxref($form,'xRelationship',$r->{Rel},'HL7code');
    $Participants .= qq|
${spc}  <${tag}>
${spc}    <id>${table}_$r->{'ID'}</id>
${spc}    <Relation>${Relation}</Relation>
${spc}    <RelationCode>${RelationCode}</RelationCode>
${spc}    <givenName>$r->{'FName'}</givenName>
${spc}    <familyName>$r->{'LName'}</familyName>
${spc}  </${tag}>|;
  }
  $Participants .= $table eq 'ClientNoteFamilyI' ? '' : qq|
${spc}</participantListObj>|;
  $s->finish();
  return($Participants);
}
sub genCareTeam
{
  my ($self,$form,$TrPlanID,$spc) = @_;
warn qq|genCareTeam: TrPlanID=${TrPlanID}, spc=${spc}=\n| if ( $debug );
  my $dbh = myDBI->dbconnect($form->{'DBNAME'});
  my $idx = 0;
  my $CareTeam = qq|${spc}<careTeamObj>|;
  my $s = $dbh->prepare("select * from ClientTrPlanS left join Provider on Provider.ProvID=ClientTrPlanS.ProvID where ClientTrPlanS.TrPlanID=?");
  $s->execute($TrPlanID) || $form->dberror("genCareTeam: select ClientTrPlanS ${TrPlanID}");
  while ( my $r = $s->fetchrow_hashref )
  {
    $idx++;
warn qq|CareTeam: ProvID=$r->{'ProvID'}\n| if ( $debug );
    my $ProvIDAddr = $r->{'Addr1'};
    $ProvIDAddr .= ', ' . $r->{'Addr2'} if ( $r->{'Addr2'} ne '' );
    my $Phone = $r->{'WkPh'} eq '' ? $r->{'HmPh'} : $r->{'WkPh'};
    $CareTeam .= qq|
${spc}  <AssignedPerson>
${spc}    <prefix>$r->{'Prefix'}</prefix>
${spc}    <suffix>$r->{'Suffix'}</suffix>
${spc}    <givenName>$r->{'FName'}</givenName>
${spc}    <familyName>$r->{'LName'}</familyName>
${spc}    <streetAddressLine>${ProvIDAddr}</streetAddressLine>
${spc}    <city>$r->{'City'}</city>
${spc}    <state>$r->{'ST'}</state>
${spc}    <postalCode>$r->{'Zip'}</postalCode>
${spc}    <phone>${Phone}</phone>
${spc}    <providerid>$r->{'ProvID'}</providerid>
${spc}    <country>US</country>
${spc}  </AssignedPerson>|;
  }
  $CareTeam .= qq|
${spc}</careTeamObj>|;
  $s->finish();
  return($CareTeam);
}
sub genTrPlan         # FIX xxx
{
  my ($self,$form,$rTreatment,$spc) = @_;
  my ($rNoteDetail,$Assessment,$rClientTrPlan) = $self->setVisit($form,$rTreatment);
  my $out = qq|
${spc}<carePlanListObj>|;
# xxx what value for CarePlan?? FIX
  my $status = $rClientTrPlan->{'EffDate'} eq '' ? 'active' : 'complete';
  (my $edate = $rClientTrPlan->{'EffDate'}) =~ s/-//g;
  my $TrPlanType = DBA->getxref($form,'xTrPlanType',$rClientTrPlan->{'Type'},'Descr');
  $TrPlanType = 'Future Visit';     # xxx
# xxx codeCode and codeSystem? REMOVED
# removed ${spc}    <codeCode>748747</codeCode>
# removed ${spc}    <codeSystem>2.16.840.1.113883.6.88</codeSystem>
  foreach my $line ( split(/\n/,$rClientTrPlan->{'TransitionPlan'}) )
  {
    $out .= qq|
${spc}  <CarePlan>
${spc}    <status>${status}</status>
${spc}    <text>|.DBA->subxml($line).qq|</text>
${spc}    <date>${edate}</date>
${spc}    <plantype>${TrPlanType}</plantype>
${spc}  </CarePlan>|;
  }
  $out .= qq|
${spc}</carePlanListObj>\n|;
  $out .= $self->genTrPlanPG($form,$rClientTrPlan,'  ')."\n";
  $out .= $self->genHealthConcern($form,$rTreatment,'  ');
  $out .= qq|
${spc}<assesmentListObj>
${spc}  <Assesment>
${spc}    <text>${Assessment}</text>
${spc}  </Assesment>
${spc}</assesmentListObj>|;
  return($out);
}
sub genTrPlanPG             # FIX xxx
{
  my ($self,$form,$rClientTrPlan,$spc) = @_;
  my $dbh = myDBI->dbconnect($form->{'DBNAME'});
  my $idx = 0;
  my $out = qq|
${spc}<goalListObj>|;
  (my $edate = $rClientTrPlan->{'EffDate'}) =~ s/-//g;
  my $TrPlanID = $rClientTrPlan->{'ID'};
  my $s = $dbh->prepare("select * from ClientTrPlanPG where TrPlanID=? order by Priority");
  $s->execute($TrPlanID) || $form->dberror("genTrPlanPG: select ClientTrPlanPG");
  while ( my $r = $s->fetchrow_hashref )
  {
    $idx++;
    $out .= qq|
${spc}  <Goal>
${spc}    <text>$r->{'Goal'}</text>
${spc}    <date>${edate}</date>
${spc}    <value>$r->{'xxx'}</value>
${spc}  </Goal>|;
  }
  $out .= qq|
${spc}</goalListObj>|;
  $s->finish();
  return($out);
}
sub genHealthConcern                          # Physician notes
{
  my ($self,$form,$rTreatment,$spc) = @_;
warn qq|genHealthConcern: ClientID=$rTreatment->{ClientID}, TrID=$rTreatment->{TrID}, spc=${spc}=\n| if ( $debug );
  my ($rNoteDetail,$Assessment,$rClientTrPlan) = $self->setVisit($form,$rTreatment);
  my $out = qq|
${spc}<healthConcernListObj>|;
  if ( $rNoteDetail->{'Concerns'} ne '' )
  {
    my $cnt = 0;
    (my $edate = $rTreatment->{'ContLogDate'}) =~ s/-//g;
    foreach my $line ( split(/\n/,$rNoteDetail->{'Concerns'}) )
    {
      $cnt++;
      $out .= qq|
${spc}  <HealthConcern>
${spc}    <id>NoteDetail_$rNoteDetail->{ID}-${cnt}</id>
${spc}    <value>|.DBA->subxml($line).qq|</value>
${spc}    <status>completed</status>
${spc}    <date>${edate}</date>
${spc}  </HealthConcern>|;
    }
  }
  $out .= qq|
${spc}</healthConcernListObj>|;
  return($out);
}
sub genFunctionalStatus
{
  my ($self,$form,$rTreatment,$spc) = @_;
  my $dbh = myDBI->dbconnect($form->{'DBNAME'});
  my $ClientID = $rTreatment->{'ClientID'};
warn qq|genFunctionalStatus: ClientID=$rTreatment->{ClientID}, TrID=$rTreatment->{TrID}, spc=${spc}=\n| if ( $debug );
  my $idx = 0;
  my $out = qq|
${spc}<FunctionalStatusListObj>|;
  my $s = $dbh->prepare("select * from ClientDevl where ClientID=?");
  $s->execute($ClientID) || $form->dberror("genFunctionalStatus: select ClientDevl ${ClientID}");
  while ( my $r = $s->fetchrow_hashref )
  {
    $idx++;
    my $F1 = DBA->getxref($form,'xFunctionalStatus',$r->{'FuncStatus1'},'ConceptName');
    my $status = 'completed';
    (my $edate = $r->{'CreateDate'}) =~ s/-//g;    # xxx
    my $Type = $r->{'Handicap1'} == 8 ? 'Cognitive' : 'Functional';
    $out .= qq|
${spc}  <FunctionalStatus>
${spc}    <id>ClientDevl_$r->{'ID'}-1</id>
${spc}    <Text>${F1}</Text>
${spc}    <code>$r->{'FuncStatus1'}</code>
${spc}    <Status>${status}</Status>
${spc}    <effectiveTime>${edate}</effectiveTime>
${spc}    <Type>${Type}</Type>
${spc}  </FunctionalStatus>| if ( $r->{'FuncStatus1'} ne '' );
    my $F2 = DBA->getxref($form,'xFunctionalStatus',$r->{'FuncStatus2'},'ConceptName');
    my $Type = $r->{'Handicap2'} == 8 ? 'Cognitive' : 'Functional';
    $out .= qq|
${spc}  <FunctionalStatus>
${spc}    <id>ClientDevl_$r->{'ID'}-2</id>
${spc}    <Text>${F2}</Text>
${spc}    <code>$r->{'FuncStatus2'}</code>
${spc}    <Status>${status}</Status>
${spc}    <effectiveTime>${edate}</effectiveTime>
${spc}    <Type>${Type}</Type>
${spc}  </FunctionalStatus>| if ( $r->{'FuncStatus2'} ne '' );
    my $F3 = DBA->getxref($form,'xFunctionalStatus',$r->{'FuncStatus3'},'ConceptName');
    my $Type = $r->{'Handicap3'} == 8 ? 'Cognitive' : 'Functional';
    $out .= qq|
${spc}  <FunctionalStatus>
${spc}    <id>ClientDevl_$r->{'ID'}-3</id>
${spc}    <Text>${F3}</Text>
${spc}    <code>$r->{'FuncStatus3'}</code>
${spc}    <Status>${status}</Status>
${spc}    <effectiveTime>${edate}</effectiveTime>
${spc}    <Type>${Type}</Type>
${spc}  </FunctionalStatus>| if ( $r->{'FuncStatus3'} ne '' );
    my $F4 = DBA->getxref($form,'xFunctionalStatus',$r->{'FuncStatus4'},'ConceptName');
    my $Type = $r->{'Handicap4'} == 8 ? 'Cognitive' : 'Functional';
    $out .= qq|
${spc}  <FunctionalStatus>
${spc}    <id>ClientDevl_$r->{'ID'}-4</id>
${spc}    <Text>${F4}</Text>
${spc}    <code>$r->{'FuncStatus4'}</code>
${spc}    <Status>${status}</Status>
${spc}    <effectiveTime>${edate}</effectiveTime>
${spc}    <Type>${Type}</Type>
${spc}  </FunctionalStatus>| if ( $r->{'FuncStatus4'} ne '' );
  }
  $out .= qq|
${spc}</FunctionalStatusListObj>|;
  $s->finish();
  return($out);
}
sub genReferrals                              # Physician notes
{
  my ($self,$form,$rTreatment,$spc) = @_;
warn qq|genReferrals: ClientID=$rTreatment->{ClientID}, TrID=$rTreatment->{TrID}, spc=${spc}=\n| if ( $debug );
  my ($rNoteDetail,$Assessment,$rClientTrPlan) = $self->setVisit($form,$rTreatment);
  my $out = qq|
${spc}<ReferralListObj>|;
  if ( $rNoteDetail->{'RefReason'} ne '' )
  {
    (my $edate = $rTreatment->{'ContLogDate'}) =~ s/-//g;
    $out .= qq|
${spc}  <Referral>
${spc}    <Reason>|.DBA->subxml($rNoteDetail->{'RefReason'}).qq|</Reason>
${spc}    <Details>|.DBA->subxml($rNoteDetail->{'RefDetail'}).qq|</Details>
${spc}    <Status>completed</Status>
${spc}    <effectiveTime>${edate}</effectiveTime>
${spc}  </Referral>|;
  }
  $out .= qq|
${spc}</ReferralListObj>|;
  return($out);
}
sub genChiefComplaint
{
  my ($self,$form,$rTreatment,$spc) = @_;
  my ($rNoteDetail,$Assessment,$rClientTrPlan) = $self->setVisit($form,$rTreatment);
  my $dbh = myDBI->dbconnect($form->{'DBNAME'});
  my $idx = 0;
  my $out = qq|
${spc}<Chiefcomplaint>|;
  if ( $rTreatment->{'Type'} == 2 )           # use the PhysNote Complaint
  {
    $out .= qq|
${spc}  |.DBA->subxml($rNoteDetail->{'Complaint'});
  }
  else                                        # use the TrPlanPG as Complaint
  {
    my $TrPlanID = $rClientTrPlan->{'ID'};
    my $s = $dbh->prepare("select * from ClientTrPlanPG where TrPlanID=? order by Priority");
    $s->execute($TrPlanID) || $form->dberror("genChiefComplaint: select ClientTrPlanPG");
    while ( my $r = $s->fetchrow_hashref )
    {
      $idx++;
      $out .= qq|
${spc}  |.DBA->subxml($r->{'Prob'});
    }
    $s->finish();
  }
  $out .= qq|
${spc}</Chiefcomplaint>\n|;
  return($out);
}
sub genHealthStatus
{
  my ($self,$form,$rTreatment,$spc) = @_;
warn qq|genHealthStatus: ClientID=$rTreatment->{ClientID}, TrID=$rTreatment->{TrID}, spc=${spc}=\n| if ( $debug );
  my $dbh = myDBI->dbconnect($form->{'DBNAME'});
  my $out = '';
  my $ClientID = $rTreatment->{'ClientID'};
  my $sClientHealth = $dbh->prepare("select * from ClientHealth where ClientID=?");
  $sClientHealth->execute($ClientID) || $form->dberror("select ClientHealth: ${ClientID}");
  my $rClientHealth = $sClientHealth->fetchrow_hashref;
  if ( $rClientHealth->{'OverallHealth'} ne '' )
  {
    my $value = DBA->getxref($form,'xHealthStatus',$rClientHealth->{OverallHealth},'ConceptName');
    my $code = DBA->getxref($form,'xHealthStatus',$rClientHealth->{OverallHealth},'ConceptCode');
    (my $edate = $rTreatment->{'ContLogDate'}) =~ s/-//g;
    $out .= qq|
${spc}<healthStatusObj>
${spc}  <value>${value}</value>
${spc}  <code>${code}</code>
${spc}  <date>${edate}</date>
${spc}</healthStatusObj>|;
  }
  $sClientHealth->finish();
  return($out);
}
sub setXML
{ 
  my ($self,$form,$ProvID,$ClientID,$TrID,$BDate,$EDate,$flags) = @_;
warn qq|ProvID=${ProvID}\n| if ( $debug );
warn qq|ClientID=${ClientID}\n| if ( $debug );
warn qq|TrID=${TrID}\n| if ( $debug );
warn qq|BDate=${BDate}\n| if ( $debug );
warn qq|EDate=${EDate}\n| if ( $debug );
warn qq|flags=${flags}\n| if ( $debug );
  my $dbh = myDBI->dbconnect($form->{'DBNAME'});
  my $sProvider = $dbh->prepare("select * from Provider where ProvID=?");
  $sProvider->execute($ProvID) || $form->dberror("setXML: select Provider ${ProvID}");
  my $rNoteProvider = $sProvider->fetchrow_hashref;
  my $sClient = $dbh->prepare("select * from Client where ClientID=?");
  $sClient->execute($ClientID) || $form->dberror("setXML: select Client ${ClientID}");
  my $rClient = $sClient->fetchrow_hashref;

  (my $today = $form->{'TODAY'}) =~ s/-//g;
  (my $now = substr($form->{'NOW'},0,5)) =~ s/://g;
  my $DOCID = $today.$now.'_'.DBUtil->genToken();
  my $DOCTYPE = $flags =~ /QRDA/ ? 'QRDA' : 'CCDA';
  my $HEADER = $DOCTYPE eq 'CCDA'
               ? qq|<CCDA xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns:xsd="http://www.w3.org/2001/XMLSchema">
  <CCDACode>34133-9</CCDACode>
  <CCDADisplayName>Summarization of episode note</CCDADisplayName>
  <CCDAEffectiveTimeValue>${today}${now}</CCDAEffectiveTimeValue>|
               : qq|<QRDA xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns:xsd="http://www.w3.org/2001/XMLSchema">
  <documentGeneratedDatetime>${today}${now}</documentGeneratedDatetime>
  <CQMNumber>$form->{MEASUREID}</CQMNumber>|;
  my $DOCCLOSE = $DOCTYPE eq 'CCDA'
                 ? qq|\n  <${DOCTYPE}TypeObj>${DOCTYPE}</${DOCTYPE}TypeObj>\n</${DOCTYPE}>\n|
                 : qq|\n</${DOCTYPE}>|;

# KLS documentGeneratedDatetime OK?

  my $ehrid = '78A150ED-B890-49dc-B716-5EC0027B3982';    # KLS ??
  my $xml = qq|${HEADER}
  <DocumentID>${DOCID}</DocumentID>
  <EHRName>Millennium Information Services</EHRName>
  <EHRID>${ehrid}</EHRID>|;
  $xml .= $self->genPatient($form,$rClient);
  if ( $DOCTYPE eq 'CCDA' )
  {
    $xml .= $self->setCCDA($form,$rClient,$TrID,$BDate,$EDate);
#warn qq|AFTER setCCDA: xml=${xml}\n| if ( $debug );
  }
  else
  {
    $xml .= $self->setQRDA($form,$rNoteProvider,$rClient,$BDate,$EDate);
  }
  $xml .= $DOCCLOSE;
  $xml =~ s{$/$/}{$/}gs;            # remove blanks lines.
  if ( $flags =~ /nonulls/i )       # eliminate null values? ...
  {
    my $str = '';
    foreach my $line ( split(/\n/,$xml) ) { $str .= $line . "\n" unless ( $line =~ m/></ ); }
    $xml = $str;
  }
  $sProvider->finish();
  $sClient->finish();
  return($xml);
}
##
# CCDA files contain information by Patient/Encounter
##
sub setCCDA
{
  my ($self,$form,$rClient,$TrID,$BDate,$EDate) = @_;

  my $dbh = myDBI->dbconnect($form->{'DBNAME'});
  my $ClientID = $rClient->{'ClientID'};
  my @Encounters = ();
  my $sTreatment = $dbh->prepare("select * from Treatment where ClientID=? and TrID=?");
  $sTreatment->execute($ClientID,$TrID) || $form->dberror("select Treatment: ${ClientID}/${TrID}");
  my $rTreatment = $sTreatment->fetchrow_hashref;
  push(@Encounters,$rTreatment);
  my $out = '';

  $out .= $self->genClinical($form,$rClient,$rTreatment);

#doc: <allergyListObj> ClientAllergies; Health History Page
  $out .= $self->genAllergies($form,$rTreatment,'  ')."\n";

#doc: <Encounter> Treatment; values on Note
#doc:   <diagnosis...> ClientNoteProblems; Priority 1 Problem checked on Note
#doc:   <encounteraddress> Treatment; BillToClinic
#doc: <careTeamObj> ClientTrPlanS; Providers Signed on TrPlan
  $out .= $self->genEncounters($form,'  ',\@Encounters,$BDate,$EDate);
#doc: <problemListObj...> ClientNoteProblems; Problems checked on Note
  $out .= $self->genProblems($form,'  ',$rTreatment->{'ClientID'});
#doc: <resultListObj...> ClientLabs; dummy entries for test
  $out .= $self->genLabResults($form,'  ',$rTreatment->{'ClientID'});
#doc: <encounterDiagnosisListObj...> NULL
  $out .= qq|  <encounterDiagnosisListObj />\n|;
#doc: <vitalSignListObj...> ClientVitalSigns; Vital Signs Entry Page and Note Page
  $out .= $self->genVitalSigns($form,'  ',$rTreatment->{'ClientID'});
#doc: <socialHistoryListObj> ClientSATobacco; Substance Abuse Tobacco Page
  $out .= $self->genSocialHistory($form,'  ',$rTreatment->{'ClientID'});
#doc: <procedureListObj> ClientProcedures; Client MU Page
  $out .= $self->genProcedures($form,'  ',$rTreatment->{'ClientID'});
#doc: <carePlanListObj> ClientTrPlan; TrPlan within Note Contact Date
#doc:   <CarePlan> split by newline
#doc:     <text> ClientTrPlan-TransitionPlan;
#doc:     <plantype> HARDCODED; 'Future Visit'
#doc: <goalListObj> ClientTrPlanPG; TrPlan within Note Contact Date
#doc: <healthConcernListObj> PhysNotes; Concern from Note
#doc:   <HealthConcern> PhysNotes-Concern; split by newline
#doc: <assesmentListObj> Treatment; Methods(ProgressNote) or ProgEvidence(PhysicianNote)
  $out .= $self->genTrPlan($form,$rTreatment,'  ')."\n";
#doc: <medicationListObj> ClientMeds; from NewCrop
  $out .= $self->genMedications($form,'  ',$rTreatment->{'ClientID'},'active');
#doc: <medicationAdministeredListObj> ClientMeds and PrescriptionDate = CreateDate ??dumb
  $out .= $self->genMedications($form,'  ',$rTreatment->{'ClientID'},'admin',$rTreatment->{'ContLogDate'});
#doc: <immunizationListObj> ClientVaccines; Client MU Page
  $out .= $self->genImmunization($form,'  ',$rTreatment->{ClientID});
#doc: <FunctionalStatusListObj> ClientDevl; Developmental History Page (4 Handicaps)
  $out .= $self->genFunctionalStatus($form,$rTreatment,'  ')."\n";
#doc: <ReferralListObj> Treatment; RefReason/RefDetail from Note
  $out .= $self->genReferrals($form,$rTreatment,'  ')."\n";
#doc: <Chiefcomplaint> Treatment/ClientTrPlanPG; Complaint(PhysicianNote) or Prob(otherNote)
  $out .= $self->genChiefComplaint($form,$rTreatment,'  ');
  $out .= $self->genHealthStatus($form,$rTreatment,'  ');
  $sTreatment->finish();
  return($out);
}
##
# QRDA files contain information by Author/Patient/daterange
##
sub setQRDA
{
  my ($self,$form,$rNoteProvider,$rClient,$BDate,$EDate) = @_;

  my $dbh = myDBI->dbconnect($form->{'DBNAME'});
  my $NoteProvID = $rNoteProvider->{'ProvID'};
warn qq|setQRDA: ProvID=${NoteProvID}\n| if ( $debug);
  my $ClientID = $rClient->{'ClientID'};
warn qq|setQRDA: ClientID=${ClientID}\n| if ( $debug);
  my ($BTime,$ETime) = ('','');
  my $out = '';
  my @Encounters = ();

  my $with = qq|(ContLogDate between '${BDate}' and '${EDate}')|;
warn qq|setQRDA: select * from Treatment where ProvID=? and ClientID=? and ${with} order by ContLogDate,ContLogBegTime,ContLogEndTime\n| if ( $debug );
  my $sTreatment = $dbh->prepare("select * from Treatment where ProvID=? and ClientID=? and ${with} order by ContLogDate,ContLogBegTime,ContLogEndTime");
  $sTreatment->execute($NoteProvID,$ClientID) || $form->dberror("select Treatment: ${NoteProvID}/${ClientID}/${with}");
  while ( my $rTreatment = $sTreatment->fetchrow_hashref )
  {
warn qq|setQRDA: ClientID=$rTreatment->{ClientID}, TrID=$rTreatment->{TrID}\n| if ( $debug);
    push(@Encounters,$rTreatment);
# Times are from the notes - where dates are from the reporting dates selection (not ContactDates)
#  we don't ask for times on reporting.
    $BTime = substr($rTreatment->{'ContLogBegTime'},0,5) if ( $BTime eq '' );
    $ETime = substr($rTreatment->{'ContLogEndTime'},0,5);
  }
  $out .= $self->genProvider($form,$rNoteProvider,$rClient);
  $out .= $self->genLegal($form,'  ');
  $out .= $self->genReporting($form,'  ',$BDate,$BTime,$EDate,$ETime);
  $out .= $self->genEncounters($form,'  ',\@Encounters,$BDate,$EDate);
  $out .= $self->genImmunization($form,'  ',$ClientID);
  $out .= $self->genInterventions($form,'  ',$ClientID,'Ordered');
  $out .= $self->genInterventions($form,'  ',$ClientID,'Performed');
  $out .= $self->genLabResults($form,'  ',$ClientID);
  $out .= $self->genMedications($form,'  ',$ClientID,'dispensed');
  $out .= $self->genMedications($form,'  ',$ClientID,'order');
  $out .= $self->genMedications($form,'  ',$ClientID,'active');
  $out .= $self->genPhysicalExam($form,'  ',$ClientID);
  $out .= $self->genProcedures($form,'  ',$ClientID);
  $out .= $self->genRiskAssessment($form,'  ',$ClientID);
  $out .= $self->genProblems($form,'  ',$ClientID);
  $out .= $self->genSocialHistory($form,'  ',$ClientID);
  $sTreatment->finish();
  return($out);
}
sub setVisit
{
  my ($self,$form,$rTreatment) = @_;

  my $dbh = myDBI->dbconnect($form->{'DBNAME'});
  my $ClientID = $rTreatment->{'ClientID'};
  my $ContDate = $rTreatment->{'ContLogDate'};

  # global sql statements
  my $sProgNotes = $dbh->prepare("select * from ProgNotes where NoteID=?");
  my $sPhysNotes = $dbh->prepare("select * from PhysNotes where NoteID=?");
  my $sClientTrPlan = $dbh->prepare("select * from ClientTrPlan where ClientID=? and ? between ClientTrPlan.EffDate and ExpDate order by ExpDate desc");

  # set note/treatment/client/first trplan
  my ($rNoteDetail,$Assessment) = ('','');
  if ( $rTreatment->{'Type'} == 1 || $rTreatment->{'Type'} == 4 )         # progress or medicare
  {
    $sProgNotes->execute($rTreatment->{TrID}) || $form->dberror("setVisit: select ProgNotes $rTreatment->{TrID}");
    $rNoteDetail = $sProgNotes->fetchrow_hashref;
    $Assessment = DBA->subxml($rNoteDetail->{'Methods'});
  }
  elsif ( $rTreatment->{'Type'} == 2 )                                    # physician
  {
    $sPhysNotes->execute($rTreatment->{TrID}) || $form->dberror("setVisit: select PhysNotes $rTreatment->{TrID}");
    $rNoteDetail = $sPhysNotes->fetchrow_hashref;
    $Assessment = DBA->subxml($rNoteDetail->{'ProgEvidence'});
  }
  $sClientTrPlan->execute($ClientID,$ContDate) || $form->dberror("select ClientTrPlan: ${ClientID}");
  my $rClientTrPlan = $sClientTrPlan->fetchrow_hashref;
#foreach my $f ( sort keys %{$rClientTrPlan} ) { warn ": rClientTrPlan-$f=$rClientTrPlan->{$f}\n"; }
  $sProgNotes->finish();
  $sPhysNotes->finish();
  $sClientTrPlan->finish();
  return($rNoteDetail,$Assessment,$rClientTrPlan);
}
sub genProvider
{
  my ($self,$form,$rProvider,$rClient) = @_;

  my $dbh = myDBI->dbconnect($form->{'DBNAME'});
  my $ProvID = $rProvider->{'ProvID'};
  my $sProvider = $dbh->prepare("select * from Provider where ProvID=?");
  my $sProviderControl = $dbh->prepare("select * from ProviderControl where ProvID=?");
  my $sProviderLicenses = $dbh->prepare("select * from ProviderLicenses where ProvID=?");

  $sProviderControl->execute($ProvID) || $form->dberror("genProvider: select ProviderControl ${ProvID}");
  my $rProviderControl = $sProviderControl->fetchrow_hashref;
  $sProviderLicenses->execute($ProvID) || $form->dberror("genProvider: select ProviderLicenses ${ProvID}");
  my $rProviderLicenses = $sProviderLicenses->fetchrow_hashref;
  $sProvider->execute($rClient->{'clinicClinicID'}) || $form->dberror("genProvider: select Clinic $rClient->{'clinicClinicID'}");
  my $rClinic = $sProvider->fetchrow_hashref;

  my $ClinicAddr = $rClinic->{'Addr1'};
  $ClinicAddr .= ', ' . $rClinic->{'Addr2'} if ( $rClinic->{'Addr2'} ne '' );
  my $ClinicPh = $rClinic->{'WkPh'} eq '' ? '' : 'tel: '.$rClinic->{'WkPh'};

#doc: <author> Provider; Provider on Note
#doc: <FacilityAddressObj> Provider; Assigned Clinic
  my $out = qq|
  <authorObj>
    <prefix>$rProvider->{'Prefix'}</prefix>
    <givenName>$rProvider->{'FName'}</givenName>
    <familyName>$rProvider->{'LName'}</familyName>
    <providerid>$rProvider->{'ProvID'}</providerid>
    <NPI>$rProviderControl->{NPI}</NPI>
    <TIN>$rProviderLicenses->{TIN}</TIN>
    <CCN>$rProviderLicenses->{CCN}</CCN>
  </authorObj>
  <custodianObj>
    <name>$rClinic->{'Name'}</name>
    <streetAddressLine>${ClinicAddr}</streetAddressLine>
    <city>$rClinic->{'City'}</city>
    <state>$rClinic->{'ST'}</state>
    <postalCode>$rClinic->{'Zip'}</postalCode>
    <country>US</country>
    <phone>${ClinicPh}</phone>
  </custodianObj>
|;
  $sProvider->finish();
  $sProviderControl->finish();
  $sProviderLicenses->finish();
  return($out);
}
sub genClinical
{
  my ($self,$form,$rClient,$rTreatment) = @_;

  my $dbh = myDBI->dbconnect($form->{'DBNAME'});
warn qq|genClinical: ClientID=$rClient->{ClientID}/$rTreatment->{ClientID}\n| if ( $debug );
  my $ClientID = $rTreatment->{'ClientID'};
warn qq|genClinical: ClientID=${ClientID}\n| if ( $debug );

  my $sProvider = $dbh->prepare("select * from Provider where ProvID=?");
warn qq|genClinical: ProvID=$rClient->{ProvID}\n| if ( $debug );
  $sProvider->execute($rClient->{'ProvID'})
              || $form->dberror("genClinic: select PrimaryProvider $rClient->{'ProvID'}");
  my $rPrimaryProvider = $sProvider->fetchrow_hashref;
warn qq|genClinical: NoteProvID=$rTreatment->{ProvID}\n| if ( $debug );
  $sProvider->execute($rTreatment->{'ProvID'})
              || $form->dberror("genClinic: select NoteProvider $rTreatment->{'ProvID'}");
  my $rNoteProvider = $sProvider->fetchrow_hashref;
warn qq|genClinical: EnteredBy=$rTreatment->{EnteredBy}\n| if ( $debug );
  $sProvider->execute($rTreatment->{'EnteredBy'})
              || $form->dberror("genClinic: select EnteredBy $rTreatment->{'EnteredBy'}");
  my $rEnteredBy = $sProvider->fetchrow_hashref;
warn qq|genClinical: ClinicID=$rTreatment->{ClinicID}\n| if ( $debug );
  $sProvider->execute($rTreatment->{'ClinicID'})
              || $form->dberror("genClinic: select Clinic $rTreatment->{'ClinicID'}");
  my $rClinic = $sProvider->fetchrow_hashref;
  my $ClinicAddr = $rClinic->{'Addr1'};
  $ClinicAddr .= ', ' . $rClinic->{'Addr2'} if ( $rClinic->{'Addr2'} ne '' );

  my $ContDate = $rTreatment->{'ContLogDate'};
  (my $contdate = $ContDate) =~ s/-//g;
  (my $begtime = substr($rTreatment->{'ContLogBegTime'},0,5)) =~ s/://g;
  my $visitDate = $contdate.$begtime;

  my $sClientTrPlan = $dbh->prepare("select * from ClientTrPlan where ClientID=? and ? between ClientTrPlan.EffDate and ExpDate order by ExpDate desc");
  $sClientTrPlan->execute($ClientID,$ContDate) || $form->dberror("genClinical: select ClientTrPlan ${ClientID}/${ContDate}");
  my $rClientTrPlan = $sClientTrPlan->fetchrow_hashref;

#doc: <author> Provider; Provider on Note
#doc: <dateEnterer> Provider; EnteredBy on Note
#doc: <informant> ClientNoteFamilyI; Checked on Note
#doc: <informationRecepient> Provider; Primary Provider Assigned
#doc: <participantListObj> ClientNoteFamilyP; Checked on Note
#doc: <careTeamObj> ClientTrPlanS; Providers Signed on TrPlan
#doc: <FacilityAddressObj> Provider; BillToClinic on Note
  my $out = qq|
  <author>
    <prefix>$rNoteProvider->{'Prefix'}</prefix>
    <givenName>$rNoteProvider->{'FName'}</givenName>
    <familyName>$rNoteProvider->{'LName'}</familyName>
    <providerid>$rNoteProvider->{'ProvID'}</providerid>
    <visitDate>${visitDate}</visitDate>
  </author>
  <dataEnterer>
    <givenName>$rEnteredBy->{'FName'}</givenName>
    <familyName>$rEnteredBy->{'LName'}</familyName>
    <providerid>$rEnteredBy->{'ProvID'}</providerid>
  </dataEnterer>
| . $self->genParticipants($form,$rTreatment,'ClientNoteFamilyI','') . qq|
  <informationRecepient>
    <givenName>$rPrimaryProvider->{'FName'}</givenName>
    <familyName>$rPrimaryProvider->{'LName'}</familyName>
  </informationRecepient>
| . $self->genParticipants($form,$rTreatment,'ClientNoteFamilyP','  ') . qq|
| . $self->genCareTeam($form,$rClientTrPlan->{'ID'},'  ') . qq|
  <FacilityAddressObj>
    <name>$rClinic->{'Name'}</name>
    <streetAddressLine>${ClinicAddr}</streetAddressLine>
    <city>$rClinic->{'City'}</city>
    <state>$rClinic->{'ST'}</state>
    <postalCode>$rClinic->{'Zip'}</postalCode>
    <country>US</country>
    <phone>$rClinic->{'WkPh'}</phone>
  </FacilityAddressObj>
|;
  $sProvider->finish();
  $sClientTrPlan->finish();
  return($out);
}
sub genReporting
{
  my ($self,$form,$spc,$BDate,$BTime,$EDate,$ETime) = @_;
warn qq|genReporting: BDate=${BDate}=\n| if ( $debug );
warn qq|genReporting: BTime=${BTime}=\n| if ( $debug );
warn qq|genReporting: EDate=${EDate}=\n| if ( $debug );
warn qq|genReporting: ETime=${ETime}=\n| if ( $debug );
  my $id = '78A150ED-B890-49dc-B716-5EC0027B3982';    # ehrid?? KLS ??

  my $bperiod = DBUtil->Date($BDate,'fmt','MONTH D1SUF, YYYY');
  my $eperiod = DBUtil->Date($EDate,'fmt','MONTH D1SUF, YYYY');
  my $Btime = substr($BTime,0,5);
warn qq|genReporting: Btime=${Btime}=\n| if ( $debug );
  my $Etime = substr($ETime,0,5);
warn qq|genReporting: Etime=${Etime}=\n| if ( $debug );

  (my $bdate = $BDate) =~ s/-//g;
  (my $btime = $Btime) =~ s/://g;
warn qq|genReporting: btime=${btime}=\n| if ( $debug );
  my $TimeLow = $bdate.$btime;

  (my $edate = $EDate) =~ s/-//g;
  (my $etime = $Etime) =~ s/://g;
warn qq|genReporting: etime=${etime}=\n| if ( $debug );
  my $TimeHigh = $edate.$etime;

  my $out = qq|
${spc}<reportingParametersObj>
${spc}  <id>${id}</id>
${spc}  <title>
${spc}          
${spc}            Reporting period: ${bperiod} ${Btime} - ${eperiod} ${Etime}
${spc}          
${spc}        </title>
${spc}  <effectiveTimeLow>${TimeLow}</effectiveTimeLow>
${spc}  <effectiveTimeHigh>${TimeHigh}</effectiveTimeHigh>
${spc}</reportingParametersObj>
|;
  return($out);
}
sub genLegal
{
  my ($self,$form,$spc) = @_;
  (my $today = $form->{'TODAY'}) =~ s/-//g;
  (my $now = substr($form->{'NOW'},0,5)) =~ s/://g;
  my $out = qq|
${spc}<legalObj>
${spc}  <time>${today}${now}</time>
${spc}  <streetAddressLine></streetAddressLine>
${spc}  <city></city>
${spc}  <state></state>
${spc}  <postalCode></postalCode>
${spc}  <country></country>
${spc}  <telecom></telecom>
${spc}  <assignedPerson_givenName></assignedPerson_givenName>
${spc}  <assignedPerson_familyName></assignedPerson_familyName>
${spc}  <representedOrganization_name></representedOrganization_name>
${spc}</legalObj>
|;
  return($out);
}
sub genEncounters
{
  my ($self,$form,$spc,$Encounters,$BDate,$EDate) = @_;
#warn qq|genEncounter: @$Encounters: BDate=${BDate}, EDate=${EDate}\n| if ( $debug );
  my $idx = 0;
  my $out = qq|
${spc}<encounterListObj>|;
  my $dbh = myDBI->dbconnect($form->{'DBNAME'});
  my $sProvider = $dbh->prepare("select * from Provider where ProvID=?");
  my $sClientTrPlan = $dbh->prepare("select * from ClientTrPlan where ClientID=? and ? between ClientTrPlan.EffDate and ExpDate order by ExpDate desc");
  my $sDiagnosis = $dbh->prepare("select misICD10.ICD10,misICD10.icdName,misICD10.sctName,misICD10.SNOMEDID,ClientNoteProblems.UUID,ClientNoteProblems.Priority,ClientNoteProblems.InitiatedDate,ClientNoteProblems.ResolvedDate from ClientNoteProblems inner join okmis_config.misICD10 on misICD10.ID=ClientNoteProblems.UUID where ClientNoteProblems.ClientID=? and ClientNoteProblems.TrID=? order by ClientNoteProblems.Priority");
  foreach my $rTreatment ( @{ $Encounters } )
  {
    my $ClientID = $rTreatment->{'ClientID'};
    my $TrID = $rTreatment->{'TrID'};
warn qq|genEncounter: ClientID=${ClientID}, TrID=${TrID}\n| if ( $debug );
    my $ContDate = $rTreatment->{'ContLogDate'};
    my $ClinicID = $rTreatment->{'ClinicID'};
    (my $contdate = $ContDate) =~ s/-//g;
    (my $begtime = substr($rTreatment->{'ContLogBegTime'},0,5)) =~ s/://g;
    my $TimeLow = $contdate.$begtime;
    (my $endtime = substr($rTreatment->{'ContLogEndTime'},0,5)) =~ s/://g;
    my $TimeHigh = $contdate.$endtime;

    $sClientTrPlan->execute($ClientID,$ContDate) || $form->dberror("genEncounters: select ClientTrPlan ${ClientID}/${ContDate}");
    my $rClientTrPlan = $sClientTrPlan->fetchrow_hashref;
    $sDiagnosis->execute($ClientID,$TrID) || $form->dberror("genEncounters: select ClientNoteProblems ${ClientID}/${TrID}");
    my $rDiagnosis = $sDiagnosis->fetchrow_hashref;
    my $rPD = DBA->getVALUESET($form,$form->{'MEASUREID'},'Encounter Principal Diagnosis',$rDiagnosis->{'SNOMEDID'});
#   default Code System if no CQM/MEASUREID for general QRDA run...
    $rPD->{'CodeSystemOID'} = '2.16.840.1.113883.6.96' if ( $form->{'MEASUREID'} eq '' );
warn qq|genEncounter: MEASUREID=$form->{'MEASUREID'}, SNOMEDID=$rDiagnosis->{'SNOMEDID'}, rPD=$rPD->{'CodeSystemOID'}\n| if ( $debug );
    my $DischargeCode = DBA->getxref($form,'xDischargeStatus',$rTreatment->{'InPatientDisStatus'},'ConceptCode');
    my $DischargeValueSet = DBA->getxref($form,'xDischargeStatus',$rTreatment->{'InPatientDisStatus'},'ValueSetOID');
    my $DischargeCodeSystem = DBA->getxref($form,'xDischargeStatus',$rTreatment->{'InPatientDisStatus'},'CodeSystemOID');
    $sProvider->execute($ClinicID) || $form->dberror("genEncounters: select Provider ${ClinicID}");
    my $rClinic = $sProvider->fetchrow_hashref;
    my $ServiceCode = DBA->getxref($form,'xSC',$rTreatment->{SCID},'SCNum');
#   default Medicaid HealthHome billing codes to pophealth G0444 Depression screening
#   else if valid cptcode then use it
#   else default to 99201 (Outpatient visit for evaluation) for non-cptcode (i.e. Medicaid)
    my $CPTCODE = $ServiceCode =~ /^G8431/ ? 'G0444'
                : $ServiceCode =~ /^9/ ? $ServiceCode
                : '99201';   
    my $ClinicAddr = $rClinic->{'Addr1'};
    $ClinicAddr .= ', ' . $rClinic->{'Addr2'} if ( $rClinic->{'Addr2'} ne '' );
    foreach my $rVALUESET ( DBA->getVALUESET($form,$form->{'MEASUREID'},'Encounter',$CPTCODE) )
    {
      $out .= qq|
${spc}  <Encounter>
${spc}    <text>Routine Follow-up Visit</text>
${spc}    <visitID>${TrID}</visitID>
${spc}    <effectiveTimeLow>${TimeLow}</effectiveTimeLow>
${spc}    <effectiveTimeHigh>${TimeHigh}</effectiveTimeHigh>
${spc}    <cptCodes>${CPTCODE}</cptCodes>
${spc}    <principaldiagnosiscode>$rDiagnosis->{'SNOMEDID'}</principaldiagnosiscode>
${spc}    <principaldiagnosisname>$rDiagnosis->{'sctName'}</principaldiagnosisname>
${spc}    <principaldiagnosiscodeSystem>$rPD->{'CodeSystemOID'}</principaldiagnosiscodeSystem>
${spc}    <principaldiagnosisvalueSet>$rPD->{'ValueSetOID'}</principaldiagnosisvalueSet>
${spc}    <conceptValue>$rVALUESET->{'Concept'}</conceptValue>
${spc}    <conceptValueOID>$rVALUESET->{'ValueSetOID'}</conceptValueOID>
${spc}    <conceptCodeOID>$rVALUESET->{'CodeSystemOID'}</conceptCodeOID>
${spc}    <encounterlocation>$rClinic->{'Name'}</encounterlocation>
${spc}    <encounteraddress>
${spc}      <streetAddressLine>${ClinicAddr}</streetAddressLine>
${spc}      <city>$rClinic->{'City'}</city>
${spc}      <state>$rClinic->{'ST'}</state>
${spc}      <postalCode>$rClinic->{'Zip'}</postalCode>
${spc}      <country>US</country>
${spc}      <phone>$rClinic->{'WkPh'}</phone>
${spc}    </encounteraddress>
| . $self->genCareTeam($form,$rClientTrPlan->{'ID'},"${spc}    ") . qq|
${spc}    <dischargecode>${DischargeCode}</dischargecode>
${spc}    <dischargevalueSet>${DischargeValueSet}</dischargevalueSet>
${spc}    <dischargecodeSystem>${DischargeCodeSystem}</dischargecodeSystem>
${spc}  </Encounter>|;
    }
  }
  $out .= qq|
  </encounterListObj>
|;
  $sProvider->finish();
  $sDiagnosis->finish();
  $sClientTrPlan->finish();
  return($out);
}
sub genImmunization
{
  my ($self,$form,$spc,$ClientID) = @_;
  my $dbh = myDBI->dbconnect($form->{'DBNAME'});
warn qq|genImmunization: ClientID=${ClientID}, spc=${spc}=\n| if ( $debug );
  my $idx = 0;
  my $out = qq|
${spc}<immunizationListObj>|;
  my $s = $dbh->prepare("select ClientVaccines.*,xVaccines.Descr as VName,xDrugRouteOfAdmin.ID as RCode,xDrugRouteOfAdmin.Descr as RName,xVaccineReject.Descr as Rejected from ClientVaccines left join okmis_config.xVaccines on xVaccines.ID=ClientVaccines.CVX left join okmis_config.xDrugRouteOfAdmin on xDrugRouteOfAdmin.ID=ClientVaccines.RouteCode left join okmis_config.xVaccineReject on xVaccineReject.ID=ClientVaccines.RejectCode where ClientID=?");
  $s->execute($ClientID) || $form->dberror("genImmunization: select ClientVaccines ${ClientID}");
  while ( my $r = $s->fetchrow_hashref )
  {
    $idx++;
    my $status = $r->{'Rejected'} eq '' ? 'completed' : 'Cancelled';
    my $negInd = $r->{'Rejected'} eq '' ? 'false' : 'true';
    (my $date = $r->{'AdminDate'}) =~ s/-//g;
    (my $time = '') =~ s/://g;
    my $TimeLow = $date.$time;
    my $TimeHigh = $TimeLow;        # WHY??
warn qq|genImmunization: TimeLow=${TimeLow}, TimeHigh=${TimeHigh}, AdminDate=$r->{AdminDate}\n| if ( $debug );
warn qq|genImmunization: CVX=$r->{CVX}\n| if ( $debug );
    foreach my $rVALUESET ( DBA->getVALUESET($form,$form->{'MEASUREID'},'Immunization',$r->{'CVX'}) )
    {
    $out .= qq|
${spc}  <Immunization>
${spc}    <id>ClientVaccines_$r->{'ID'}</id>
${spc}    <status>${status}</status>
${spc}    <effectiveTimeLow>${TimeLow}</effectiveTimeLow>
${spc}    <effectiveTimeHigh>${TimeHigh}</effectiveTimeHigh>
${spc}    <routeCodeCode>$r->{'RCode'}</routeCodeCode>
${spc}    <routeCodeDisplayName>$r->{'RName'}</routeCodeDisplayName>
${spc}    <manufacturedMaterialObj>
${spc}      <manufacturedMaterialTranslationCode>$r->{'CVX'}</manufacturedMaterialTranslationCode>
${spc}      <manufacturedMaterialTranslationDisplayName>$r->{'VName'}</manufacturedMaterialTranslationDisplayName>
${spc}      <conceptValue>$rVALUESET->{'Concept'}</conceptValue>
${spc}      <conceptValueOID>$rVALUESET->{'ValueSetOID'}</conceptValueOID>
${spc}      <conceptCodeOID>$rVALUESET->{'CodeSystemOID'}</conceptCodeOID>
${spc}    </manufacturedMaterialObj>
${spc}    <manufacturerOrganization>$r->{'xxx'}Immuno Inc. FIX</manufacturerOrganization>
${spc}    <lotnumber>$r->{'LotNum'}</lotnumber>
${spc}    <rejectionReason>$r->{'Rejected'}</rejectionReason>
${spc}    <rejectionReasonCode>$r->{'RejectCode'}</rejectionReasonCode>
${spc}    <negationInd>${negInd}</negationInd>
${spc}  </Immunization>|;
    }
  }
  $out .= qq|
${spc}</immunizationListObj>
|;
  $s->finish();
  return($out);
}
sub genLabResults
{
  my ($self,$form,$spc,$ClientID) = @_;
  my $dbh = myDBI->dbconnect($form->{'DBNAME'});
warn qq|genLabResults: spc=${spc}, ClientID=${ClientID}\n| if ( $debug );
  my $idx = 0;
  my $out = qq|
${spc}<resultListObj>|;
  my $s = $dbh->prepare("select * from ClientLabs where ClientID=?");
  $s->execute($ClientID) || $form->dberror("genLabResults: select ClientLabs ${ClientID}");
  while ( my $r = $s->fetchrow_hashref )
  {
    $idx++;
    my $negInd = $r->{'Rejected'} eq '' ? 'false' : 'true';
warn qq|genLabResults: MEASUREID=$form->{MEASUREID}, SNOMEDID=$r->{SNOMEDID}\n| if ( $debug );
    foreach my $rVALUESET ( DBA->getVALUESET($form,$form->{'MEASUREID'},'Laboratory Test Performed',$r->{'SNOMEDID'}) )
    {
warn qq|genLabResults: VALUESET: Concept=$rVALUESET->{Concept}\n| if ( $debug );
warn qq|genLabResults: VALUESET: SNOMEDNAME=$r->{SNOMEDNAME}\n| if ( $debug );
warn qq|genLabResults: VALUESET: SNOMEDNAME=$rVALUESET->{SNOMEDNAME}\n| if ( $debug );
    $out .= qq|
${spc}  <Result>
${spc}    <status>$r->{'status'}</status>
${spc}    <codeCode>$r->{'SNOMEDID'}</codeCode>
${spc}    <codeDisplayName>$r->{'SNOMEDNAME'}</codeDisplayName>
${spc}    <conceptValue>$rVALUESET->{'Concept'}</conceptValue>
${spc}    <conceptValueOID>$rVALUESET->{'ValueSetOID'}</conceptValueOID>
${spc}    <conceptCodeOID>$rVALUESET->{'CodeSystemOID'}</conceptCodeOID>
${spc}    <negationInd>${negInd}</negationInd>
| . $self->genLabResultsObs($form,"${spc}    ",$ClientID,$r->{'ID'}) . qq|
${spc}  </Result>|;
    }
  }
  $out .= qq|
${spc}</resultListObj>
|;
  $s->finish();
  return($out);
}
# valuetype for results are (ResultObs)
#  "ST" for text where you have to mention valueValue
#  "PQ" for numeric where you have to mention valueUnit and valueValue
# valueValue will be blank for pending results
sub genLabResultsObs
{
  my ($self,$form,$spc,$ClientID,$ClientLabsID) = @_;
warn qq|genLabResultsObs: spc=${spc}, ClientID=${ClientID}, ClientLabsID=${ClientLabsID}=\n| if ( $debug );
  my $dbh = myDBI->dbconnect($form->{'DBNAME'});
  my $idx = 0;
  my $out = qq|
${spc}<resultObs>|;
  ##my $s = $dbh->prepare("select ClientLabResults.*, xLabResults.ConceptCode, xLabResults.ConceptName from ClientLabResults left join okmis_config.xLabResults on xLabResults.ConceptCode=ClientLabResults.Code where ClientLabsID=?");
  my $s = $dbh->prepare("select ClientLabResults.* from ClientLabResults where ClientLabsID=?");
  $s->execute($ClientLabsID) || $form->dberror("genLabResults: select ClientLabResults");
  while ( my $r = $s->fetchrow_hashref )
  {
    $idx++;
    (my $edate = $r->{'AdminDate'}) =~ s/-//g;
    ##my $valuetype = $r->{'Code'} eq '' ? 'CD' : 'PQ';   # PQ is numeric result, CD is coded result.
##    foreach my $rVALUESET ( DBA->getVALUESET($form,$form->{'MEASUREID'},'Laboratory Test Performed',$r->{'Code'}) )
##    {
      $out .= qq|
${spc}  <ResultObs>
${spc}    <code>$r->{'Code'}</code>
${spc}    <displayName>$r->{'Name'}</displayName>
${spc}    <status>$r->{'Status'}</status>
${spc}    <effectiveTime>${edate}</effectiveTime>
${spc}    <valueValue>$r->{'Value'}</valueValue>
${spc}    <valueUnit>$r->{'Unit'}</valueUnit>
${spc}    <leftrange>$r->{'Min'}</leftrange>
${spc}    <rightrange>$r->{'Max'}</rightrange>
${spc}    <valuetype>$r->{Type}</valuetype>
${spc}  </ResultObs>|;
##${spc}    <conceptValue>$rVALUESET->{'Concept'}</conceptValue>
##${spc}    <conceptValueOID>$rVALUESET->{'ValueSetOID'}</conceptValueOID>
##${spc}    <conceptCodeOID>$rVALUESET->{'CodeSystemOID'}</conceptCodeOID>
##    }
  }
  $s->finish();
  $out .= qq|
${spc}</resultObs>
|;
  return($out);
}
sub genMedications
{
  my ($self,$form,$spc,$ClientID,$type,$ForDate) = @_;
  my $dbh = myDBI->dbconnect($form->{'DBNAME'});
warn qq|genMedications: ClientID=${ClientID}, type=${type}, spc=${spc}=\n| if ( $debug );
  my $idx = 0;
  my $tag  = $type =~ /active/i ? qq|medicationListObj|
             : $type =~ /admin/i ? qq|medicationAdministeredListObj|
             : $type =~ /order/i ? qq|medicationOrderListObj|
             : $type =~ /dispensed/i ? qq|medicationDispensedListObj| : '';
  my $Category = $type =~ /active/i ? qq|Medication Active|
             : $type =~ /admin/i ? qq|Medication Administered|                        # Immunizations/Vaccines 
             : $type =~ /order/i ? qq|Medication Order|
             : $type =~ /dispensed/i ? qq|Medication Dispensed| : '';
  my $with = $type =~ /active/i ? qq|and Active=1|
             : $type =~ /admin/i ? qq|and DATE(PrescriptionDate)='${ForDate}'|        # this is dumb.
             : $type =~ /order/i ? qq|and Active=1|
             : $type =~ /dispensed/i ? qq|and Active=1| : '';
  my $out = qq|
${spc}<${tag}>|;

  my $sClientMeds = $dbh->prepare("select * from ClientMeds where ClientID=? ${with} order by PrescriptionDate");
  $sClientMeds->execute($ClientID) || $form->dberror("genMedications: select ClientMeds ${ClientID}");
  while ( my $r = $sClientMeds->fetchrow_hashref )
  {
    $idx++;
#NewCrop Optional ${spc}   <effectiveTimePeriodValue>$r->{'xxx'}</effectiveTimePeriodValue>
#NewCrop Optional ${spc}   <effectiveTimePeriodUnit>$r->{'xxx'}</effectiveTimePeriodUnit>
    (my $date = substr($r->{'PrescriptionDate'},0,10)) =~ s/-//g;
    (my $time = substr($r->{'PrescriptionDate'},11,5)) =~ s/://g;
    my $TimeLow = $date.$time;
    my $TimeHigh = $TimeLow;        # WHY??
    my $rRejected = DBA->selxref($form,'xMedicationRejected','ID',$r->{'Rejected'});
warn qq|genMedications: ClientID=${ClientID}, Rejected=$r->{'Rejected'}, ConceptCode=$rRejected->{'ConceptCode'}=\n| if ( $debug );
    my $negInd = $r->{'Rejected'} eq '' ? 'false' : 'true';
warn qq|genMedications: ClientID=${ClientID}, Category=${Category}, rxcui=$r->{'rxcui'}=\n| if ( $debug );
    foreach my $rVALUESET ( DBA->getVALUESET($form,$form->{'MEASUREID'},$Category,$r->{'rxcui'}) )
    {
    $out .= qq|
${spc}  <Medication>
${spc}    <id>ClientMeds_$r->{'ID'}</id>
${spc}    <effectiveTimeLow>${TimeLow}</effectiveTimeLow>
${spc}    <effectiveTimeHigh>${TimeHigh}</effectiveTimeHigh>
${spc}    <routeCodeCode>$r->{'ExternalDrugRoute'}</routeCodeCode>
${spc}    <routeCodeDisplayName>$r->{'Route'}</routeCodeDisplayName>
${spc}    <doseQuantityValue>$r->{'Strength'}</doseQuantityValue>
${spc}    <doseQuantityUnit>$r->{'StrengthUOM'}</doseQuantityUnit>
${spc}    <instructions>$r->{'DosageFrequencyDescription'}</instructions>
${spc}    <manufacturedMaterialObj>
${spc}      <manufacturedMaterialCode>$r->{'rxcui'}</manufacturedMaterialCode>
${spc}      <manufacturedMaterialDisplayName>$r->{'DrugInfo'}</manufacturedMaterialDisplayName>
${spc}      <conceptValue>$rVALUESET->{'Concept'}</conceptValue>
${spc}      <conceptValueOID>$rVALUESET->{'ValueSetOID'}</conceptValueOID>
${spc}      <conceptCodeOID>$rVALUESET->{'CodeSystemOID'}</conceptCodeOID>
${spc}    </manufacturedMaterialObj>
${spc}    <medicationSupplyObjLst />
${spc}    <negationInd>${negInd}</negationInd>
${spc}    <rejectionReasonCode>$rRejected->{'ConceptCode'}</rejectionReasonCode>
${spc}    <rejectionReason>$rRejected->{'ConceptName'}</rejectionReason>
${spc}    <rejectionReasonCodeSystem>$rRejected->{'CodeSystemOID'}</rejectionReasonCodeSystem>
${spc}    <rejectionReasonValueset>$rRejected->{'ValueSetOID'}</rejectionReasonValueset>
${spc}  </Medication>|;
    }
  }
  $out .= qq|
${spc}</${tag}>
|;
  $sClientMeds->finish();
  return($out);
}
sub genProblems
{
  my ($self,$form,$spc,$ClientID) = @_;
  my $dbh = myDBI->dbconnect($form->{'DBNAME'});
  my $idx = 0;
  my $out = qq|
${spc}<problemListObj>|;
  #my $s = $dbh->prepare("select misICD10.ICD10,misICD10.icdName,misICD10.sctName,misICD10.SNOMEDID,ClientNoteProblems.UUID,ClientNoteProblems.Priority,ClientNoteProblems.InitiatedDate,ClientNoteProblems.ResolvedDate from ClientNoteProblems inner join okmis_config.misICD10 on misICD10.ID=ClientNoteProblems.UUID where ClientNoteProblems.ClientID=? and ClientNoteProblems.TrID=? order by ClientNoteProblems.Priority");
  my $s = $dbh->prepare("select ClientProblems.*,misICD10.SNOMEDID,misICD10.sctName from ClientProblems inner join okmis_config.misICD10 on misICD10.ID=ClientProblems.UUID where ClientProblems.ClientID=? order by ClientProblems.Priority");
  $s->execute($ClientID) || $form->dberror("Physician Note: select ClientNoteProblems");
  while ( my $r = $s->fetchrow_hashref )
  {
    $idx++;
    my $cnt = 0;
    my $Priority = int($r->{'Priority'}/10);
    (my $idate = $r->{'InitiatedDate'}) =~ s/-//g;
    (my $rdate = $r->{'ResolvedDate'}) =~ s/-//g;
    my $status = $r->{'ResolvedDate'} eq '' ? 'active' : 'completed';
    my $negInd = $r->{'negationInd'} == 1 ? 'true' : 'false';
warn qq|genProblems: ClientID=${ClientID}, Category=Diagnosis, SNOMEDID=$r->{'SNOMEDID'}=\n| if ( $debug );
    foreach my $rVALUESET ( DBA->getVALUESET($form,$form->{'MEASUREID'},'Diagnosis',$r->{'SNOMEDID'}) )
    {
      $cnt++;
    $out .= qq|
${spc}  <Problem>
${spc}    <id>ClientProblems_$r->{'ID'}-priority${Priority}-${cnt}</id>
${spc}    <status>${status}</status>
${spc}    <topLevelEffectiveTimeLow>${idate}</topLevelEffectiveTimeLow>
${spc}    <topLevelEffectiveTimeHigh>${rdate}</topLevelEffectiveTimeHigh>
${spc}    <problemNameCode>$r->{'SNOMEDID'}</problemNameCode>
${spc}    <problemNameDisplayName>$r->{'sctName'}</problemNameDisplayName>
${spc}    <conceptValue>$rVALUESET->{'Concept'}</conceptValue>
${spc}    <conceptValueOID>$rVALUESET->{'ValueSetOID'}</conceptValueOID>
${spc}    <conceptCodeOID>$rVALUESET->{'CodeSystemOID'}</conceptCodeOID>
${spc}    <negationInd>${negInd}</negationInd>
${spc}  </Problem>|;
    }
  }
  $out .= qq|
${spc}</problemListObj>
|;
  $s->finish();
  return($out);
}
# BMI LOINC Value LOINC Value Set		39156-5
# BMI percentile Grouping Value Set		59574-4
# Height Grouping Value Set			3137-7
# Weight Grouping Value Set			18833-4
# Diastolic Blood Pressure Grouping Value Set	8462-4
# Systolic Blood Pressure Grouping Value Set	8480-6
sub genPhysicalExam
{
  my ($self,$form,$spc,$ClientID) = @_;
  my $dbh = myDBI->dbconnect($form->{'DBNAME'});
  my $idx = 0;
  my @Observations = ('165_BPSystolic_8480-6_mm[Hg]','165_BPDiastolic_8462-4_mm[Hg]','69_BMI_39156-5_kg/m2','155_BMI_59574-4_kg/m2','_BPSystolic_8480-6_mm[Hg]','_BPDiastolic_8462-4_mm[Hg]','_BMI_39156-5_kg/m2');
  my $out = qq|
${spc}<physicalExamListObj>|;
  my $s = $dbh->prepare("select * from ClientVitalSigns where ClientID=? order by VDate");
  $s->execute($ClientID) || $form->dberror("genPhysicalExam: select ClientVitalSigns");
  while ( my $r = $s->fetchrow_hashref )
  {
    $idx++;
    my $cnt = 0;
    my $height = ($r->{'HeightFeet'} * 12) + $r->{'HeightInches'};
    my $weightkg = ($r->{'Weight'} * 0.45359237);
    my $tempcel = (($r->{'Temperature'} -32) * 1.8);
    my $bmi = 0;
    if ( $height > 0 ) { $bmi = ( $r->{'Weight'} / ( $height * $height ) ) * 703; }
    $bmi = sprintf("%.2f",$bmi);
    $r->{'BMI'} = $bmi;
    my $status = $r->{'VDate'} eq '' ? 'active' : 'completed';
    (my $date = $r->{'VDate'}) =~ s/-//g;
    (my $time = '00:00') =~ s/://g;
    my $TimeLow = $date.$time;
    my $TimeHigh = $TimeLow;        # WHY??
    my $rRejected = DBA->selxref($form,'xProcedureRejected','ID',$r->{'Rejected'});
    my $negInd = $r->{'Rejected'} eq '' ? 'false' : 'true';
    foreach my $Obs ( @Observations )
    {
      $cnt++;
      my ($measure,$fld,$code,$unit) = split('_',$Obs);
warn qq|Obs=${Obs}, measure=$form->{'MEASUREID'}/${measure}, fld=${fld}, code=${code}, unit=${unit}\n| if ( $debug );
      next unless ( $form->{'MEASUREID'} eq $measure );
      foreach my $rVALUESET ( DBA->getVALUESET($form,$form->{'MEASUREID'},'Physical Exam',$code) )
      {
        $out .= qq|
${spc}  <Observation>
${spc}    <id>ClientVitalSigns_$r->{'ID'}-${cnt}</id>
${spc}    <status>${Status}</status>
${spc}    <effectiveTimeLow>${TimeLow}</effectiveTimeLow>
${spc}    <effectiveTimeHigh>${TimeHigh}</effectiveTimeHigh>
${spc}    <codeCode>${code}</codeCode>
${spc}    <codeDisplayName>$rVALUESET->{'ConceptDescription'}</codeDisplayName>
${spc}    <valueValue>$r->{$fld}</valueValue>
${spc}    <valueUnit>${unit}</valueUnit>
${spc}    <conceptValue>$rVALUESET->{'Concept'}</conceptValue>
${spc}    <conceptValueOID>$rVALUESET->{'ValueSetOID'}</conceptValueOID>
${spc}    <conceptCodeOID>$rVALUESET->{'CodeSystemOID'}</conceptCodeOID>
${spc}    <reasoncode>$rRejected->{'ConceptCode'}</reasoncode>
${spc}    <rejectDisplayName>$rRejected->{'ConceptName'}</rejectDisplayName>
${spc}    <rejectcodeSystem>$rRejected->{'CodeSystemOID'}</rejectcodeSystem>
${spc}    <rejectcodevalueset>$rRejected->{'ValueSetOID'}</rejectcodevalueset>
${spc}    <negationInd>${negInd}</negationInd>
${spc}  </Observation>| if ( $r->{$fld} ne '' );
      }
    }
  }
  $out .= qq|
${spc}</physicalExamListObj>
|;
  $s->finish();
  return($out);
}
sub genVitalSigns
{
  my ($self,$form,$spc,$ClientID) = @_;
  my $dbh = myDBI->dbconnect($form->{'DBNAME'});
  my $idx = 0;
  my $out = qq|
${spc}<vitalSignListObj>|;
  my $s = $dbh->prepare("select * from ClientVitalSigns where ClientID=? order by VDate");
  $s->execute($ClientID) || $form->dberror("genVitalSigns: select ClientVitalSigns");
  while ( my $r = $s->fetchrow_hashref )
  {
    $idx++;
    (my $vdate = $r->{'VDate'}) =~ s/-//g;
    my $status = $r->{'VDate'} eq '' ? 'active' : 'completed';
    my $height = ($r->{'HeightFeet'} * 12) + $r->{'HeightInches'};
    my $weightkg = ($r->{'Weight'} * 0.45359237);
    my $tempcel = (($r->{'Temperature'} -32) * 1.8);
    my $bmi = 0;
    if ( $height > 0 ) { $bmi = ( $r->{'Weight'} / ( $height * $height ) ) * 703; }
    $bmi = sprintf("%.2f",$bmi);
    $out .= qq|
${spc}  <VitalSign>
${spc}    <effectiveTimeLow>${vdate}</effectiveTimeLow>
${spc}    <effectiveTimeHigh>${vdate}</effectiveTimeHigh>
${spc}    <Observation>|;
    $out .= qq|
${spc}      <VitalSignObs>
${spc}        <codeCode>8302-2</codeCode>
${spc}        <codeDisplayName>Height</codeDisplayName>
${spc}        <status>${status}</status>
${spc}        <effectiveTime>${vdate}</effectiveTime>
${spc}        <valueValue>${height}</valueValue>
${spc}        <valueUnit>[in_i]</valueUnit>
${spc}      </VitalSignObs>| if ( $height ne '' );
    $out .= qq|
${spc}      <VitalSignObs>
${spc}        <codeCode>29463-7</codeCode>
${spc}        <codeDisplayName>Patient Body Weight - Measured</codeDisplayName>
${spc}        <status>${status}</status>
${spc}        <effectiveTime>${vdate}</effectiveTime>
${spc}        <valueValue>$r->{'Weight'}</valueValue>
${spc}        <valueUnit>[lb_av]</valueUnit>
${spc}      </VitalSignObs>| if ( $r->{'Weight'} ne '' );
    $out .= qq|
${spc}      <VitalSignObs>
${spc}        <codeCode>8480-6</codeCode>
${spc}        <codeDisplayName>BP Systolic</codeDisplayName>
${spc}        <status>${status}</status>
${spc}        <effectiveTime>${vdate}</effectiveTime>
${spc}        <valueValue>$r->{'BPSystolic'}</valueValue>
${spc}        <valueUnit>mm[Hg]</valueUnit>
${spc}      </VitalSignObs>| if ( $r->{'BPSystolic'} ne '' );
    $out .= qq|
${spc}      <VitalSignObs>
${spc}        <codeCode>8462-4</codeCode>
${spc}        <codeDisplayName>BP Diastolic</codeDisplayName>
${spc}        <status>${status}</status>
${spc}        <effectiveTime>${vdate}</effectiveTime>
${spc}        <valueValue>$r->{'BPDiastolic'}</valueValue>
${spc}        <valueUnit>mm[Hg]</valueUnit>
${spc}      </VitalSignObs>| if ( $r->{'BPDiastolic'} ne '' );
    $out .= qq|
${spc}      <VitalSignObs>
${spc}        <codeCode>39156-5</codeCode>
${spc}        <codeDisplayName>BMI (Body Mass Index)</codeDisplayName>
${spc}        <status>${status}</status>
${spc}        <effectiveTime>${vdate}</effectiveTime>
${spc}        <valueValue>${bmi}</valueValue>
${spc}        <valueUnit>kg/m2</valueUnit>
${spc}      </VitalSignObs>| if ( $bmi ne '' );
    $out .= qq|
${spc}      <VitalSignObs>
${spc}        <codeCode>59408-5</codeCode>
${spc}        <codeDisplayName>O2 % BldC Oximetry</codeDisplayName>
${spc}        <status>${status}</status>
${spc}        <effectiveTime>${vdate}</effectiveTime>
${spc}        <valueValue>$r->{'Oximetry'}</valueValue>
${spc}        <valueUnit>%</valueUnit>
${spc}      </VitalSignObs>| if ( $r->{'Oximetry'} ne '' );
    $out .= qq|
${spc}      <VitalSignObs>
${spc}        <codeCode>9279-1</codeCode>
${spc}        <codeDisplayName>Respiratory Rate</codeDisplayName>
${spc}        <status>${status}</status>
${spc}        <effectiveTime>${vdate}</effectiveTime>
${spc}        <valueValue>$r->{'Respiration'}</valueValue>
${spc}        <valueUnit>/min</valueUnit>
${spc}      </VitalSignObs>| if ( $r->{'Respiration'} ne '' );
    $out .= qq|
${spc}      <VitalSignObs>
${spc}        <codeCode>8867-4</codeCode>
${spc}        <codeDisplayName>Heart Rate</codeDisplayName>
${spc}        <status>${status}</status>
${spc}        <effectiveTime>${vdate}</effectiveTime>
${spc}        <valueValue>$r->{'Pulse'}</valueValue>
${spc}        <valueUnit>/min</valueUnit>
${spc}      </VitalSignObs>| if ( $r->{'Pulse'} ne '' );
    $out .= qq|
${spc}      <VitalSignObs>
${spc}        <codeCode>8310-5</codeCode>
${spc}        <codeDisplayName>Body Temperature</codeDisplayName>
${spc}        <status>${status}</status>
${spc}        <effectiveTime>${vdate}</effectiveTime>
${spc}        <valueValue>$r->{'Temperature'}</valueValue>
${spc}        <valueUnit>[degF]</valueUnit>
${spc}      </VitalSignObs>| if ( $r->{'Temperature'} ne '' );
    $out .= qq|
${spc}    </Observation>
${spc}  </VitalSign>|;
  }
  $out .= qq|
${spc}</vitalSignListObj>
|;
  $s->finish();
  return($out);
}
sub genProcedures
{
  my ($self,$form,$spc,$ClientID) = @_;
  my $dbh = myDBI->dbconnect($form->{'DBNAME'});
warn qq|genProcedures: ClientID=${ClientID}, type=${type}\n| if ( $debug );
  my $idx = 0;
  my $out = qq|
${spc}<procedureListObj>|;
  my $s = $dbh->prepare("select ClientProcedures.*, xProcedures.ConceptCode as ProcedureCode, xProcedures.ConceptName as ProcedureName, xProcedureTarget.ConceptCode as TargetCode, xProcedureTarget.ConceptName as TargetName from ClientProcedures left join okmis_config.xProcedures on xProcedures.ConceptCode=ClientProcedures.ProcedureID left join okmis_config.xProcedureTarget on xProcedureTarget.ID=ClientProcedures.TargetID where ClientProcedures.ClientID=? order by ClientProcedures.StartDate");
  $s->execute($ClientID) || $form->dberror("genProcedures: select Client ${ClientID}");
  while ( my $r = $s->fetchrow_hashref )
  {
foreach my $f ( sort keys %{$r} ) { warn "genProcedures: r-$f=$r->{$f}\n"; }
    $idx++;
    my $Status = 'completed';
    (my $sdate = $r->{'StartDate'}) =~ s/-//g;
    (my $edate = $r->{'EndDate'}) =~ s/-//g;
warn qq|genProcedures: PerformerNPI=$r->{PerformerNPI}\n| if ( $debug );
    my $rPerformer = DBA->selxref($form,'xNPI','NPI',$r->{'PerformerNPI'});
    my $PerformerAddr = $rPerformer->{'Addr2'} eq '' 
                      ? "$rPerformer->{'Addr1'}"
                      : "$rPerformer->{'Addr1'}, $rPerformer->{'Addr2'}";
warn qq|genProcedures: PerformerAddr=${PerformerAddr}\n| if ( $debug );
    my $rRejected = DBA->selxref($form,'xProcedureRejected','ID',$r->{'Rejected'});
foreach my $f ( sort keys %{$rRejected} ) { warn "genProcedures: rRejected-$f=$rRejected->{$f}\n"; }
    my $negInd = $r->{'Rejected'} eq '' ? 'false' : 'true';
warn qq|genProcedures: negInd=${negInd}\n| if ( $debug );
    foreach my $rVALUESET ( DBA->getVALUESET($form,$form->{'MEASUREID'},'Procedure',$r->{'ProcedureCode'}) )
    {
foreach my $f ( sort keys %{$rVALUESET} ) { warn "genProcedures: rVALUESET-$f=$rVALUESET->{$f}\n"; }
    $out .= qq|
${spc}  <Procedure>
${spc}    <id>ClientProcedures_$r->{ID}</id>
${spc}    <status>${Status}</status>
${spc}    <effectiveTimeLow>${sdate}</effectiveTimeLow>
${spc}    <effectiveTimeHigh>${edate}</effectiveTimeHigh>
${spc}    <codeCode>$r->{'ProcedureCode'}</codeCode>
${spc}    <codeDisplayName>$r->{'ProcedureName'}</codeDisplayName>
${spc}    <conceptValue>$rVALUESET->{'Concept'}</conceptValue>
${spc}    <conceptValueOID>$rVALUESET->{'ValueSetOID'}</conceptValueOID>
${spc}    <conceptCodeOID>$rVALUESET->{'CodeSystemOID'}</conceptCodeOID>
${spc}    <targetSiteCodeCode>$r->{'TargetCode'}</targetSiteCodeCode>
${spc}    <targetSiteCodeDisplayName>$r->{'TargetName'}, CodeSystem - SNOMED-CT</targetSiteCodeDisplayName>
${spc}    <performer>|.DBA->subxml($rPerformer->{'ProvOrgName'}).qq|</performer>
${spc}    <performerAddress>
${spc}      <streetAddressLine>${PerformerAddr}</streetAddressLine>
${spc}      <city>$rPerformer->{'City'}</city>
${spc}      <state>$rPerformer->{'ST'}</state>
${spc}      <postalCode>$rPerformer->{'Zip'}</postalCode>
${spc}      <country>US</country>
${spc}      <phone>$rPerformer->{'WkPh'}</phone>
${spc}    </performerAddress>
${spc}    <deviceCode>$r->{'DeviceCode'}</deviceCode>
${spc}    <deviceName>$r->{'gmdnPTName'}, CodeSystem – SNOMED-CT</deviceName>
${spc}    <deviceId>$r->{'di'}</deviceId>
${spc}    <reasoncode>$rRejected->{'ConceptCode'}</reasoncode>
${spc}    <rejectDisplayName>$rRejected->{'ConceptName'}</rejectDisplayName>
${spc}    <rejectcodeSystem>$rRejected->{'CodeSystemOID'}</rejectcodeSystem>
${spc}    <rejectcodevalueset>$rRejected->{'ValueSetOID'}</rejectcodevalueset>
${spc}    <negationInd>${negInd}</negationInd>
${spc}  </Procedure>|;
    }
  }
  $out .= qq|
${spc}</procedureListObj>
|;
warn qq|genProcedures: out=${out}\n| if ( $debug );
  $s->finish();
  return($out);
}
sub genInterventions
{
  my ($self,$form,$spc,$ClientID,$type) = @_;
warn qq|genInterventions: ClientID=${ClientID}, type=${type}\n| if ( $debug );
  my $dbh = myDBI->dbconnect($form->{'DBNAME'});
  my $idx = 0;
  my $xtable = $type eq 'Ordered' ? 'xInterventionOrder' : 'xInterventionPerformed';
  my $out = qq|
${spc}<intervention${type}ListObj>|;
  my $s = $dbh->prepare("select ClientInterventions${type}.*, ${xtable}.ConceptCode, ${xtable}.ConceptName from ClientInterventions${type} left join okmis_config.${xtable} on ${xtable}.ID=ClientInterventions${type}.Intervention where ClientInterventions${type}.ClientID=? order by ClientInterventions${type}.VisitDate");
  $s->execute($ClientID) || $form->dberror("genInterventions${type}: select Client ${ClientID}");
  while ( my $r = $s->fetchrow_hashref )
  {
    $idx++;
    my $Status = 'completed';
    (my $date = $r->{'VisitDate'}) =~ s/-//g;
    (my $time = '00:00') =~ s/://g;
    my $TimeLow = $date.$time;
    my $TimeHigh = $TimeLow;        # WHY??
#foreach my $f ( sort keys %{$r} ) { warn "genInterventions: r-$f=$r->{$f}\n"; }
warn qq|genInterventions: ClientID=${ClientID}, Reason=$r->{Reason}=\n| if ( $debug );
    my $rReason = $type eq 'Order' ? DBA->selxref($form,"${xtable}Reason",'ID',$r->{'Reason'}) : '';
#foreach my $f ( sort keys %{$rReason} ) { warn "genInterventions: rReason-$f=$rReason->{$f}\n"; }
warn qq|genInterventions: ClientID=${ClientID}, Rejected=$r->{Rejected}=\n| if ( $debug );
    my $rRejected = DBA->selxref($form,"${xtable}Rejected",'ID',$r->{'Rejected'});
#foreach my $f ( sort keys %{$rRejected} ) { warn "genInterventions: rRejected-$f=$rRejected->{$f}\n"; }
    my $negInd = $r->{'Rejected'} eq '' ? 'false' : 'true';
warn qq|genInterventions: ClientID=${ClientID}, ConceptCode=$r->{ConceptCode}=\n| if ( $debug );
    foreach my $rVALUESET ( DBA->getVALUESET($form,$form->{'MEASUREID'},"Intervention ${type}",$r->{'ConceptCode'}) )
    {
#foreach my $f ( sort keys %{$rVALUESET} ) { warn "genInterventions: rVALUESET-$f=$rVALUESET->{$f}\n"; }
    $out .= qq|
${spc}  <Intervention>
${spc}    <id>ClientInterventions${type}_$r->{'ID'}</id>
${spc}    <status>${Status}</status>
${spc}    <effectiveTimeLow>${TimeLow}</effectiveTimeLow>
${spc}    <effectiveTimeHigh>${TimeHigh}</effectiveTimeHigh>
${spc}    <codeCode>$r->{'ConceptCode'}</codeCode>
${spc}    <codeDisplayName>$r->{'ConceptName'}</codeDisplayName>
${spc}    <reasonCode>$rReason->{'ConceptCode'}</reasonCode>
${spc}    <reasonDisplayName>$rReason->{'ConceptName'}</reasonDisplayName>
${spc}    <reasoncodeSystem>$rReason->{'CodeSystemOID'}</reasoncodeSystem>
${spc}    <reasoncodevalueset>$rReason->{'ValueSetOID'}</reasoncodevalueset>
${spc}    <rejectReasonCode>$rRejected->{'ConceptCode'}</rejectReasonCode>
${spc}    <rejectDisplayName>$rRejected->{'ConceptName'}</rejectDisplayName>
${spc}    <rejectcodeSystem>$rRejected->{'CodeSystemOID'}</rejectcodeSystem>
${spc}    <rejectcodevalueset>$rRejected->{'ValueSetOID'}</rejectcodevalueset>
${spc}    <conceptValue>$rVALUESET->{'Concept'}</conceptValue>
${spc}    <conceptValueOID>$rVALUESET->{'ValueSetOID'}</conceptValueOID>
${spc}    <conceptCodeOID>$rVALUESET->{'CodeSystemOID'}</conceptCodeOID>
${spc}    <negationInd>${negInd}</negationInd>
${spc}  </Intervention>|;
    }
  }
  $out .= qq|
${spc}</intervention${type}ListObj>
|;
  $s->finish();
  return($out);
}
sub genRiskAssessment
{
  my ($self,$form,$spc,$ClientID) = @_;
  my $dbh = myDBI->dbconnect($form->{'DBNAME'});
  my $idx = 0;
  my $out = qq|
${spc}<riskAssessmentListObj>|;
  my $s = $dbh->prepare("select ClientRiskAssessment.*, xRiskAssessment.ConceptCode, xRiskAssessment.ConceptName from ClientRiskAssessment left join okmis_config.xRiskAssessment on xRiskAssessment.ID=ClientRiskAssessment.Assessment where ClientRiskAssessment.ClientID=? order by ClientRiskAssessment.VisitDate");
  $s->execute($ClientID) || $form->dberror("genRiskAssessment: select Client ${ClientID}");
  while ( my $r = $s->fetchrow_hashref )
  {
    $idx++;
    my $Status = 'completed';
    (my $date = $r->{'VisitDate'}) =~ s/-//g;
    (my $time = '00:00') =~ s/://g;
    my $TimeLow = $date.$time;
    my $TimeHigh = $TimeLow;        # WHY??
    my $rResult = DBA->selxref($form,'xRiskAssessmentResult','ID',$r->{'Result'});
    my $rRejected = DBA->selxref($form,'xRiskAssessmentRejected','ID',$r->{'Rejected'});
    my $negInd = $r->{'Rejected'} eq '' ? 'false' : 'true';
# keep for a couple of days the following logic???
    my ($valuetype,$valueCode,$valueCodeSystem,$valueCodeValueSet) = ('CD','','','');
    if ( $valuetype eq 'CD' && $r->{'Result'} != '' )
    {
      $valueCode         = qq|${spc}    <valueCode>428171000124102</valueCode>|;
      $valueCodeSystem   = qq|${spc}    <valueCodeSystem/>|;
      $valueCodeValueSet = qq|${spc}    <valueCodeValueSet>2.16.840.1.113883.3.600.2451</valueCodeValueSet>|;
    }
    elsif ( $valuetype eq 'PQ' && $r->{'Result'} != '' )
    {
      $valueCode         = qq|${spc}    <valueValue/>|;
      $valueCodeSystem   = qq|${spc}    <valueUnit/>|;
      $valueCodeValueSet = qq|${spc}    <valueDisplayName>Negative Depression Screening</valueDisplayName>|;
    }
    elsif ( $valuetype eq 'ST' && $r->{'Result'} != '' )
    {
      $valueCode         = qq|${spc}    <valueInnerText/>|;
      $valueCodeSystem   = '';
      $valueCodeValueSet = '';
    }
    foreach my $rVALUESET ( DBA->getVALUESET($form,$form->{'MEASUREID'},'Risk Category Assessment',$r->{'ConceptCode'}) )
    {
    $out .= qq|
${spc}  <riskAssessment>
${spc}    <id>ClientRiskAssessment_$r->{'ID'}</id>
${spc}    <status>${Status}</status>
${spc}    <effectiveTimeLow>${TimeLow}</effectiveTimeLow>
${spc}    <effectiveTimeHigh>${edate}</effectiveTimeHigh>
${spc}    <codeCode>$r->{'ConceptCode'}</codeCode>
${spc}    <codeDisplayName>$r->{'ConceptName'}</codeDisplayName>
${spc}    <conceptValue>$rVALUESET->{'Concept'}</conceptValue>
${spc}    <conceptValueOID>$rVALUESET->{'ValueSetOID'}</conceptValueOID>
${spc}    <conceptCodeOID>$rVALUESET->{'CodeSystemOID'}</conceptCodeOID>
${spc}    <valueCode>$rResult->{'ConceptCode'}</valueCode>
${spc}    <valueCodeSystem>$rResult->{'CodeSystemOID'}</valueCodeSystem>
${spc}    <valueCodeValueSet>$rResult->{'ValueSetOID'}</valueCodeValueSet>
${spc}    <rejectcode>$rRejected->{'ConceptCode'}</rejectcode>
${spc}    <rejectDisplayName>$rRejected->{'ConceptName'}</rejectDisplayName>
${spc}    <rejectcodeSystem>$rRejected->{'CodeSystemOID'}</rejectcodeSystem>
${spc}    <rejectcodevalueset>$rRejected->{'ValueSetOID'}</rejectcodevalueset>
${spc}    <negationInd>${negInd}</negationInd>
${spc}  </riskAssessment>|;
    }
  }
  $out .= qq|
${spc}</riskAssessmentListObj>
|;
  $s->finish();
  return($out);
}
sub genSocialHistory
{
  my ($self,$form,$spc,$ClientID) = @_;
  my $dbh = myDBI->dbconnect($form->{'DBNAME'});
  my $idx = 0;
  my $out = qq|
${spc}<socialHistoryListObj>|;
  my $s = $dbh->prepare("select ClientSATobacco.*,xSmokingStatus.Descr,xSmokingStatus.SNOMEDID from ClientSATobacco left join okmis_config.xSmokingStatus on xSmokingStatus.ID=ClientSATobacco.SmokingStatus where ClientID=? order by StartDate,EndDate");
  $s->execute($ClientID) || $form->dberror("genSocialHistory: select ClientSATobacco");
  while ( my $r = $s->fetchrow_hashref )
  {
#foreach my $f ( sort keys %{$r} ) { warn "genSocialHistory: r-$f=$r->{$f}\n"; }
    $idx++;
    (my $sdate = $r->{'StartDate'}) =~ s/-//g;
    (my $edate = $r->{'EndDate'}) =~ s/-//g;
    foreach my $rVALUESET ( DBA->getVALUESET($form,$form->{'MEASUREID'},'Smoking Status',$r->{'SNOMEDID'}) )
    {
    $out .= qq|
${spc}  <SocialHistory>
${spc}    <id>ClientSATobacco_$r->{'ID'}</id>
${spc}    <effectiveTimeLow>${sdate}</effectiveTimeLow>
${spc}    <effectiveTimeHigh>${edate}</effectiveTimeHigh>
${spc}    <valueCode>$r->{'SNOMEDID'}</valueCode>
${spc}    <valueDisplayName>Smoking Status: $r->{'Descr'}</valueDisplayName>
${spc}    <conceptValue>$rVALUESET->{'Concept'}</conceptValue>
${spc}    <conceptValueOID>$rVALUESET->{'ValueSetOID'}</conceptValueOID>
${spc}    <conceptCodeOID>$rVALUESET->{'CodeSystemOID'}</conceptCodeOID>
${spc}  </SocialHistory>|;
    }
  }
  $out .= qq|
${spc}</socialHistoryListObj>
|;
  $s->finish();
  return($out);
}
#############################################################################
1;
