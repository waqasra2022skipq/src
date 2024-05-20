package TLevel;
use DBForm;
use myDBI;
use DBUtil;
use DBA;
my $debug = 0;
############################################################################
# Calculate a Treatment Level
############################################################################
sub getTL
{
  my ($self,$form,$ClientID,$AdultAge,$PrAuthID) = @_;
warn qq|getTL: ClientID=$ClientID, AdultAge=$AdultAge, PrAuthID=$PrAuthID\n| if ( $debug );
  my $TLevel = '';
  my $dbh = myDBI->dbconnect($form->{'DBNAME'});
  return($TLevel) unless ( $ClientID );

# get Client information
  my $sClient = $dbh->prepare("select Client.DOB,ClientLegal.CustAgency,ClientRelations.Residence,ClientRelations.GHLevel from Client left join ClientLegal on ClientLegal.ClientID=Client.ClientID left join ClientRelations on ClientRelations.ClientID=Client.ClientID where Client.ClientID=?");
  $sClient->execute($ClientID);
  my ($DOB,$CustAgency,$Residence,$GHLevel) = $sClient->fetchrow_array;
  $sClient->finish();
  # if GH Level C,D,D+,E  & 'Group Home' or 'Therapeutic Foster Care'
# No longer change the TL, just set TLevel (TLevel on printouts)...
  my $ResDescr = DBA->getxref($form,'xResidence',$Residence,'Descr');
warn qq|getTL: DOB=${DOB}, GHLevel=$GHLevel, ResDescr=$ResDescr, CustAgency=$CustAgency\n| if ( $debug );
# Check if 'C' is RBMS???<<<
  if ( $GHLevel =~ /[D|E]/i && ( $ResDescr =~ /group home/i || $ResDescr =~ /therapeutic foster care/i ) ) { $TLevel = 'R'; }  # RBMS
  elsif ( $ResDescr =~ /icf\/mr/i  ) { $TLevel = 'I'; }                                     # ICF/MR
  elsif ( $ResDescr =~ /nursing home/i ) { $TLevel = 'N'; }                                 # Nursing Home
  elsif ( $CustAgency eq 'MSTO' || $CustAgency eq 'MSTJ' ) { $TLevel = 'M'; }  # MST
  else { my ($isAdult,$TL) = $self->getTreatmentLevel($form,$ClientID,$AdultAge,$PrAuthID); $TLevel = $TL; }
warn qq|getTL: TLevel=$TLevel\n| if ( $debug );
  return($TLevel);
}
sub getTreatmentLevel
{
  my ($self,$form,$ClientID,$AdultAge,$PrAuthID) = @_;
  my $dbh = myDBI->dbconnect($form->{'DBNAME'});
  return(0,'') unless ( $ClientID );
warn qq|getTreatmentLevel: ClientID=$ClientID, AdultAge=$AdultAge, PrAuthID=$PrAuthID\n| if ( $debug );

# need to know what StatusDate/ReqType this is?
  my $sPrAuth = $dbh->prepare("select * from ClientPrAuth where ClientID=? and ID=?");
  $sPrAuth->execute($ClientID,$PrAuthID);
  my $rPrAuth = $sPrAuth->fetchrow_hashref;
  my $ReqType = $rPrAuth->{'ReqType'} eq '' ? DBA->setPrAuthReqType($form,$ClientID)
              : $rPrAuth->{'ReqType'};
  my $ReqDate = $rPrAuth->{'StatusDate'} eq '' ? $form->{'TODAY'}
              : $rPrAuth->{'StatusDate'};
warn qq|getTreatmentLevel: ReqType=$ReqType, ReqDate=$ReqDate, Type=$rPrAuth->{Type}\n| if ( $debug );
  $sPrAuth->finish();

# get Client information
  my $sClient = $dbh->prepare("select DOB from Client where ClientID=?");
  $sClient->execute( $ClientID );
  my ($DOB) = $sClient->fetchrow_array;
  my $Age = DBUtil->Date($DOB,'age',$ReqDate);
  my $isAdult = $Age >= $AdultAge ? 1 : 0;
  $sClient->finish();
warn qq|DOB=$DOB, Age=$Age, isAdult=$isAdult\n| if ( $debug );

  my $TL = '00';
warn qq|getTreatmentLevel: TL=$TL, ReqType=$ReqType\n| if ( $debug );
#  Service Focus must be...
#  SA = Substance Abuse or Drug Court
#  IN = Mental Health and Substance Abuse or Special Populations Treatment Units or Co-Occuring (integrated)
#  GA = Gambling or Gambling Substance Abuse or Gambling Mental Health
  if ( $ReqType =~ /SA|GA|IN/ )
  {
    if ( $isAdult ) { $TL = $self->CalcASI($form,$ClientID); }
    else            { $TL = $self->CalcTASI($form,$ClientID); }
  }
  $TL = $self->CalcCARS($form,$ClientID,$PrAuthID,$isAdult) if ( $TL eq '00' );
warn qq|getTreatmentLevel: TL=$TL\n| if ( $debug );
  return($isAdult,$TL);
}
############################################################################
sub CalcASI
{
  my ($self,$form,$ClientID) = @_;
  my ($M,$E,$A,$D,$L,$F,$P) = $self->getASI($form,$ClientID);
  my ($T7,$T6,$T5,$T4) = (0,0,0,0);
  $T7++ if ( $M >= 7 );
  $T7++ if ( $E >= 7 );
  $T7++ if ( $A >= 7 );
  $T7++ if ( $D >= 7 );
  $T7++ if ( $L >= 7 );
  $T7++ if ( $F >= 7 );
  $T7++ if ( $P >= 7 );
  $T6++ if ( $M >= 6 );
  $T6++ if ( $E >= 6 );
  $T6++ if ( $A >= 6 );
  $T6++ if ( $D >= 6 );
  $T6++ if ( $L >= 6 );
  $T6++ if ( $F >= 6 );
  $T6++ if ( $P >= 6 );
  $T5++ if ( $M >= 5 );
  $T5++ if ( $E >= 5 );
  $T5++ if ( $A >= 5 );
  $T5++ if ( $D >= 5 );
  $T5++ if ( $L >= 5 );
  $T5++ if ( $F >= 5 );
  $T5++ if ( $P >= 5 );
  $T4++ if ( $M >= 4 );
  $T4++ if ( $E >= 4 );
  $T4++ if ( $A >= 4 );
  $T4++ if ( $D >= 4 );
  $T4++ if ( $L >= 4 );
  $T4++ if ( $F >= 4 );
  $T4++ if ( $P >= 4 );
warn qq|CalcASI: T7=$T7, T6=$T6, T5=$T5, T4=$T4\n| if ( $debug );
  my $TL = '00';
  if    ( $T7 >= 3 && ( $A >= 4 || $D >= 4 ) ) { $TL = '04'; }
  elsif ( $T6 >= 3 && ( $A >= 4 || $D >= 4 ) ) { $TL = '03'; }
  elsif ( $T5 >= 3 && ( $A >= 4 || $D >= 4 ) ) { $TL = '02'; }
  elsif ( $T4 >= 2 && ( $A >= 4 || $D >= 4 ) ) { $TL = '01'; }
  elsif ( $A >= 4 || $D >= 4 ) { $TL = 'P'; }
  return($TL);
}
sub getASI
{
  my ($self,$form,$ClientID) = @_;
warn qq|ENTER: getASI: $ClientID\n| if ( $debug );
  my $dbh = myDBI->dbconnect($form->{'DBNAME'});
  my ($M,$E,$A,$D,$L,$F,$P) = (0,0,0,0,0,0,0);
  my $qClientASI = qq|select * from ClientASI where G1=? order by G5 desc,CreateDate desc|;
  my $id = $ClientID;
warn qq|$qClientASI,$id\n| if ( $debug );
  my $sClientASI = $dbh->prepare($qClientASI);
  $sClientASI->execute($id);
  if (  $rClientASI = $sClientASI->fetchrow_hashref )
  {
warn qq|FOUND ASI: $rClientASI->{ID}\n| if ( $debug );
    $M = $rClientASI->{SPMedical};
    $E = $rClientASI->{SPEmpSup};
    $A = $rClientASI->{SPAlcohol};
    $D = $rClientASI->{SPDrugs};
    $L = $rClientASI->{SPLegal};
    $F = $rClientASI->{SPFamily};
    $P = $rClientASI->{SPPsych};
  }
  $sClientASI->finish();
warn qq|LEAVE: ASI: M=$M, E=$E, A=$A, D=$D, L=$L, F=$F, P=$P\n| if ( $debug );
  return($M,$E,$A,$D,$L,$F,$P);
}
sub CalcTASI
{
  my ($self,$form,$ClientID) = @_;
  my ($C,$S,$E,$F,$P,$L,$Y) = $self->getTASI($form,$ClientID);
  my ($T4,$T3,$T2) = (0,0,0);
  $T4++ if ( $C >= 4 );
  $T4++ if ( $S >= 4 );
  $T4++ if ( $E >= 4 );
  $T4++ if ( $F >= 4 );
  $T4++ if ( $P >= 4 );
  $T4++ if ( $L >= 4 );
  $T4++ if ( $Y >= 4 );
  $T3++ if ( $C >= 3 );
  $T3++ if ( $S >= 3 );
  $T3++ if ( $E >= 3 );
  $T3++ if ( $F >= 3 );
  $T3++ if ( $P >= 3 );
  $T3++ if ( $L >= 3 );
  $T3++ if ( $Y >= 3 );
  $T2++ if ( $C >= 2 );
  $T2++ if ( $S >= 2 );
  $T2++ if ( $E >= 2 );
  $T2++ if ( $F >= 2 );
  $T2++ if ( $P >= 2 );
  $T2++ if ( $L >= 2 );
  $T2++ if ( $Y >= 2 );
warn qq|CalcTASI: T4=$T4, T3=$T3, T2=$T2\n| if ( $debug );
  my $TL = '00';
  if    ( $T4 >= 3 && $C >= 2 ) { $TL = '04'; }
  elsif ( ($T3 >= 3 || $T4 >= 2) && $C >= 2 ) { $TL = '03'; }
  elsif ( ($T3 >= 2 || $T4 >= 1) && $C >= 2 ) { $TL = '02'; }
  elsif ( $T2 >= 3 && $C >= 2 ) { $TL = '01'; }
  elsif ( $C >= 2 ) { $TL = 'P'; }
  return($TL);
}
sub getTASI
{
  my ($self,$form,$ClientID) = @_;
warn qq|ENTER: getTASI: $ClientID\n| if ( $debug );
  my $dbh = myDBI->dbconnect($form->{'DBNAME'});
  my ($C,$S,$E,$F,$P,$L,$Y) = (0,0,0,0,0,0,0);
  my $qClientTASI = qq|select * from ClientTASI where ClientID=? order by IntDate desc,CreateDate desc|;
  my $id = $ClientID;
warn qq|$qClientTASI,$id\n| if ( $debug );
  my $sClientTASI = $dbh->prepare($qClientTASI);
  $sClientTASI->execute($id);
  if (  $rClientTASI = $sClientTASI->fetchrow_hashref )
  {
warn qq|FOUND TASI: $rClientTASI->{ID}\n| if ( $debug );
    $C = $rClientTASI->{SPChemical};
    $S = $rClientTASI->{SPSchool};
    $E = $rClientTASI->{SPEmpSup};
    $F = $rClientTASI->{SPFamily};
    $P = $rClientTASI->{SPPeerSoc};
    $L = $rClientTASI->{SPLegal};
    $Y = $rClientTASI->{SPPsych};
  }
  $sClientTASI->finish();
warn qq|LEAVE: TASI: C=$C, S=$S, E=$E, F=$F, P=$P, L=$L, Y=$Y\n| if ( $debug );
  return($C,$S,$E,$F,$P,$L,$Y);
}
sub CalcCARS
{
  my ($self,$form,$ClientID,$PrAuthID,$isAdult) = @_;
warn qq|CalcCARS: ClientID=$ClientID,PrAuthID=$PrAuthID,isAdult=$isAdult\n| if ( $debug );
  my $dbh = myDBI->dbconnect($form->{'DBNAME'});
# get CAR Scores (just the first 9)
  my $sPDDom = $dbh->prepare("select Dom1Score, Dom2Score, Dom3Score, Dom4Score, Dom5Score, Dom6Score, Dom7Score, Dom8Score, Dom9Score from PDDom where ClientID=? and PrAuthID=?");
  $sPDDom->execute($ClientID,$PrAuthID);
  # we skip 0 and get 1-9.
  my @Scores = (undef, $sPDDom->fetchrow_array);
  $sPDDom->finish();

  my $over40 = 0;
  my $in30 = 0;
  my $in20 = 0;
  foreach my $s ( @Scores[1,2,3,4,5,6,7,8,9] )
  { #next if !defined $s;
    $s >= 40             && $over40++;
    $s >= 30 && $s <= 39 && $in30++;
    $s >= 20 && $s <= 29 && $in20++;
warn qq|CalcCARS: s=$s\n| if ( $debug );
  }
warn qq|CalcCARS: in20=$in20, in30=$in30, over40=$over40\n| if ( $debug );

### Level 4 Adult / Child
warn qq|CalcCARS: check Level 4: over40=$over40\n| if ( $debug );
  # >= 40 in 4 domains (Adult) 3 domains (Child) WITH 1 domain being in 1,6,7 or 9
  $domaincount = $isAdult ? 4 : 3;
warn qq|CalcCARS: domaincount=$domaincount\n| if ( $debug );
  if( $over40 >= $domaincount )
  { foreach my $s ( @Scores[1,6,7,9] ) { return('04') if ( $s >= 40 ); } }

### Level 3 Adult / Child
warn qq|CalcCARS: check Level 3: in30=$in30\n| if ( $debug );
  # >= 30-39 in 4 domains WITH 2 domains being in 1,6,7 or 9
  if( $in30 >= 4 )
  { 
    my $count = 0;
    foreach my $s ( @Scores[1,6,7,9] ) { $count++ if ( 30 <= $s && $s <= 39 ); }
    return('03') if ( $count >= 2 );
  }
  # >= 40 in 2 domains WITH 1 domain being in 1,6,7 or 9
warn qq|CalcCARS: check Level 3: over40=$over40\n| if ( $debug );
  if( $over40 >=2 )
  { foreach my $s ( @Scores[1,6,7,9] ) { return('03') if ( $s >= 40 ); } }
  # >= 30-39 in 2 domains AND >= 40 in 1 domain WITH 
  #   either the 40 or 2 of the 30's being in domains 1,6,7 or 9
warn qq|CalcCARS: check Level 3: in30=$in30,over40=$over40\n| if ( $debug );
  if( $in30 >=2 && $over40 )
  { 
    my $count = 0;
    foreach my $s ( @Scores[1,6,7,9] )
    {
      return('03') if ( $s >= 40 );
      $count++ if ( $s >= 30 );
    }
    return('03') if ( $count >= 2 );
  }

### Level 2 Adult (2) and Level 2 Child (6)
warn qq|CalcCARS: check Level 2: in30=$in30,over40=$over40\n| if ( $debug );
  # (a) >= 30-39 in 3 domains,
  # (b) >= 40-49 in 1 domain
  return('02') if ( $in30 >=3 );
  return('02') if ( $over40 );

### Level 1 Adult (1) and Level 1 Child (5)
warn qq|CalcCARS: check Level 1: in20=$in20,in30=$in30\n| if ( $debug );
  # (a) >= 20-29 in 4 domains,
  # (b) >= 30-39 in 2 domains,
  # (c) >= 20-29 in 3 domains AND >= 30-39 in 1 domain
  return('01') if ( $in20 >= 4 );
  return('01') if ( $in30 >= 2 );
  return('01') if ( $in20 >= 3 && $in30 >= 1 );

### Prevention and Recovery Adult / Child
warn qq|CalcCARS: check Level P: in20=$in20,in30=$in30\n| if ( $debug );
  # (a) >= 20-29 in 3 domains,
  # (b) >= 30-39 in 1 domains,
  # (c) >= 20-29 in 2 domains AND >= 30-39 in 1 domain
  return('P') if ( $in20 >= 3 );
  return('P') if ( $in30 >= 1 );
  return('P') if ( $in20 >= 2 && $in30 >= 1 );

warn qq|fall-thru\n| if ( $debug );
  # Fall-Through to unknown value
  return('00');
}
############################################################################
1;
