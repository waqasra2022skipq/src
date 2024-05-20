package Inv;
use DBA;
use myDBI;
use DBUtil;
############################################################################
sub setNotePrAuthID
{
  my ($self,$form,$TrID) = @_;
#warn qq|\n\nsetNotePrAuthID: TrID=$TrID\n|;
  my $PrAuthID = '';                   # returned value
  my $dbh = myDBI->dbconnect($form->{'DBNAME'});
  my $sTreatment = $dbh->prepare("select Treatment.*, xSC.InsID, xSC.Interchange, xSC.ExInv, xSCRates.UnitLbl from Treatment left join xSC on xSC.SCID=Treatment.SCID left join xSCRates on xSCRates.SCID=xSC.SCID where TrID=?");
  $sTreatment->execute($TrID) || $form->dberror("setNotePrAuthID: select $TrID");
  if ( my $rTreatment = $sTreatment->fetchrow_hashref )
  {
    my $SCID = $rTreatment->{Interchange}?$rTreatment->{Interchange}:$rTreatment->{SCID};
#warn qq|setNotePrAuthID: ClientID=$rTreatment->{ClientID}, TrID=$TrID, SCID=$rTreatment->{SCID}/$SCID\n|;
#warn qq|setNotePrAuthID: ContLogDate=$rTreatment->{ContLogDate}, Units=$rTreatment->{Units}, BilledAmt=$rTreatment->{BilledAmt}\n|;
#warn qq|setNotePrAuthID: pass: UnitLbl=$rTreatment->{UnitLbl}, ExInv=$rTreatment->{ExInv}\n|;
    if ( $rTreatment->{UnitLbl} eq 'NonBill' ) { null; }    # we don't set these.
    elsif ( $rTreatment->{ExInv} ) { null; }                # we don't set these.
    else
    {
      my $qPrAuth = qq|select ClientPrAuth.*, Insurance.InsID from ClientPrAuth left join Insurance on Insurance.InsNumID=ClientPrAuth.InsuranceID where ClientPrAuth.ClientID='$rTreatment->{ClientID}' and Insurance.InsID='$rTreatment->{InsID}' and ClientPrAuth.PAnumber is not null and ('$rTreatment->{ContLogDate}' between ClientPrAuth.EffDate and ClientPrAuth.ExpDate) order by ClientPrAuth.EffDate|;
#warn qq|setNotePrAuthID: qPrAuth=$qPrAuth\n|;
      my $sPrAuth = $dbh->prepare($qPrAuth);
      $sPrAuth->execute() || $form->dberror($qPrAuth);
      while ( my $rPrAuth = $sPrAuth->fetchrow_hashref )
      {
#warn qq|setNotePrAuthID: InsID=$rPrAuth->{InsID}, PrAuthID=$rPrAuth->{ID}, EffDate=$rPrAuth->{EffDate}, ExpDate=$rPrAuth->{ExpDate}\n|;
        my $inv = Inv->InvPA($form,$rPrAuth,$rTreatment->{ContLogDate});
        $inv = $inv->InvNotes($form,$rPrAuth->{ClientID},$rPrAuth->{InsID});
        my $PAgroup = $rPrAuth->{PAgroup};
#warn qq|setNotePrAuthID: skip: $PAgroup? ...\n|;
        if ( $PAgroup ) { next unless ( Inv->chkSCIDinPA($form,$PAgroup,$SCID) ); }
#warn qq|setNotePrAuthID: CurEffDate=$inv->{CurEffDate}, CurExpDate=$inv->{CurExpDate}\n|;
#warn qq|setNotePrAuthID: 1: CurAmtAuth=$inv->{CurAmtAuth}, CurAmtLeft=$inv->{CurAmtLeft}\n|;
        if ( $inv->{$SCID}->{UnitsAuth} > 0 )  # Units allocated; subtract this TrID
        { $Used = $rTreatment->{Units}; $Left = $inv->{$SCID}->{UnitsLeft}+$Used; }
        else    
        { $Used = $rTreatment->{BilledAmt}; $Left = $inv->{CurAmtLeft}+$Used; }
#warn qq|setNotePrAuthID: 2: CurAmtAuth=$inv->{CurAmtAuth}, CurAmtLeft=$inv->{CurAmtLeft}, CurUsed=$inv->{CurAmtUsed}, CurLeft=$inv->{CurAmtLeft}\n|;
#warn qq|setNotePrAuthID: Used=$Used, Left=$Left, SCID=$SCID, PrAuthID=$PrAuthID\n|;
        $PrAuthID = $rPrAuth->{ID} if ( $Left > 0 && $Used <= $Left );
      }
      $sPrAuth->finish();
    }
    if ( $PrAuthID )
    {
#warn qq|setNotePrAuthID: update Treatment set PrAuthID=${PrAuthID} where TrID=${TrID}\n|;
      my $sUpdate = $dbh->prepare("update Treatment set PrAuthID=? where TrID=?");
      $sUpdate->execute($PrAuthID,$TrID) || $form->dberror("setNotePrAuthID: update $PrAuthID/$TrID");
      $sUpdate->finish();
    }
    else
    {
      my $sUpdate = $dbh->prepare("update Treatment set PrAuthID=NULL where TrID=?");
#warn qq|setNotePrAuthID: update Treatment set PrAuthID=NULL where TrID=${TrID}\n|;
      $sUpdate->execute($TrID) || $form->dberror("setNotePrAuthID: update NULL/$TrID");
      $sUpdate->finish();
    }
    $sTreatment->finish();
  }
#warn qq|setNotePrAuthID: END setNotePrAuthID: PrAuthID=$PrAuthID\n|;
  return($PrAuthID);
}
sub setInv
{
  my ($self,$form,$ClientID,$cDate) = @_;
  my $dbh = myDBI->dbconnect($form->{'DBNAME'});
  my $CurDate = $cDate ? $cDate : $form->{TODAY};
  my $qPrAuth = qq|
select ClientPrAuth.*,ClientPrAuthCDC.TransType,Client.DOB,Client.ProvID,Client.clinicClinicID,Client.DOB,Insurance.InsID
  from ClientPrAuth
    left join ClientPrAuthCDC on ClientPrAuthCDC.ClientPrAuthID=ClientPrAuth.ID
    left join Client on Client.ClientID=ClientPrAuth.ClientID
    left join Insurance on Insurance.InsNumID=ClientPrAuth.InsuranceID
  where ClientPrAuth.ClientID='${ClientID}'
  and ClientPrAuth.PAnumber is not null
  and (ClientPrAuthCDC.TransType > 21 and ClientPrAuthCDC.TransType < 60)
  and '${CurDate}' between ClientPrAuth.EffDate and ClientPrAuth.ExpDate
  order by ClientPrAuth.EffDate
|;
#warn qq|setInv: qPrAuth=\n$qPrAuth\n|;
  my $sPrAuth = $dbh->prepare($qPrAuth);
  $sPrAuth->execute();
  if ( $rPrAuth = $sPrAuth->fetchrow_hashref )
  {
#warn qq|setInv: PrAuth=$rPrAuth->{ID}\n|;
    $self = $self->InvPA($form,$rPrAuth,$CurDate);
    $self = $self->InvNotes($form,$rPrAuth->{ClientID},$rPrAuth->{InsID});
  }
  $sPrAuth->finish();
  return($self);
}
############################################################################
sub InvPA
{
  my ($class,$form,$rPrAuth,$cDate) = @_;
  my $self = {};
  bless $self, $class;
  my $PrAuthID = $rPrAuth->{ID};
  my $CurDate = $cDate ? $cDate : $form->{TODAY};
  my $PAnumber = $rPrAuth->{PAnumber} eq '' ? 'No Auth#' : $rPrAuth->{PAnumber};
#warn qq|\nInvPA: ClientID=$rPrAuth->{ClientID},ID=$rPrAuth->{ID},CurDate=$CurDate,PAnumber=$rPrAuth->{PAnumber}\n|;
  my $PAEffDate = $rPrAuth->{EffDate};
  my $PAExpDate = $rPrAuth->{ExpDate};
#warn qq|InvPA: PAnumber=$PAnumber, PAEffDate=${PAEffDate}, PAExpDate=$PAExpDate \n|;
  my $PACnt = 0;   # NOT USED???
#foreach my $f ( sort keys %{$rPrAuth} ) { warn "InvPA: rPrAuth-$f=$rPrAuth->{$f}\n"; }
  my $AmtAuth = $rPrAuth->{AuthAmt};
  my $UnitsAuth = $rPrAuth->{UnitsAuth};
  my $LinesAuth = $rPrAuth->{'LinesAuth'} ? $rPrAuth->{'LinesAuth'} : 1;  # always >0
  my $PerMonthAmt = $AmtAuth/$LinesAuth;
#warn qq|ClientID=$rPrAuth->{ClientID},${AmtAuth}/${LinesAuth}=${PerMonthAmt}\n|;

# General info
  $self->{'ClientID'} = $rPrAuth->{'ClientID'};
  $self->{'ProviderID'} = $rPrAuth->{'ProvID'};
  $self->{'ClinicID'} = $rPrAuth->{'clinicClinicID'};
  $self->{'InsID'} = $rPrAuth->{'InsID'};
  $self->{InsDescr} = DBA->getxref($form,'xInsurance',$rPrAuth->{InsID},'Descr');
  $self->{PACnt} = $PACnt;
  $self->{PACntText} = $PACnt > 1 ? 'Multiple PAs' : '';
  $self->{PPACnt} = $rPrAuth->{PAnumber} eq '' ? 0 : 1;
#warn qq|InvPA: InsDescr=$self->{InsDescr}, PACnt=$self->{PACnt}, PPACnt=$self->{PPACnt}\n|;
  $self->{PAnumber} = $PAnumber;
  $self->{PAEffDate} = $PAEffDate;
  $self->{PAExpDate} = $PAExpDate;
  $self->{fPAEffDate} = DBUtil->Date($PAEffDate,'fmt','MM/DD/YYYY');
  $self->{fPAExpDate} = DBUtil->Date($PAExpDate,'fmt','MM/DD/YYYY');
  $self->{AuthPeriod} = "$self->{fPAEffDate}-$self->{fPAExpDate}";
  $self->{LinesAuth} = $LinesAuth;          # number to divide TOTAL Units/Amt by.
  $self->{LOS} = $rPrAuth->{LOS};           # number of months for PA.
  $self->{PAgroup} = $rPrAuth->{PAgroup};   # set for medicaid, not for other insurances.
# Amt info
  $self->{AmtAuth} = $AmtAuth;
  $self->{AmtUsed} = '0';
  $self->{AmtLeft} = $self->{AmtAuth} - $self->{AmtUsed};
#warn qq|ClientID=$rPrAuth->{ClientID},$self->{AmtAuth}\n|;
# Units info
  $self->{UnitsAuth} = $UnitsAuth;
  $self->{UnitsUsed} = 0;
  $self->{UnitsLeft} = $self->{UnitsAuth} - $self->{UnitsUsed};

  $self->getPALines($form,$PrAuthID);
#foreach my $k ( @{$self->{PADates}} ) { warn qq|InvPA: k=$k\n|; }
# CurPeriod: MM/DD/YYYY-MM/DD/YYYY
  my ($CurEffDate,$CurExpDate,$CurPeriod) = $self->CurrentPeriod($form,$CurDate);
  $self->{CurEffDate} = $CurEffDate;
  $self->{CurExpDate} = $CurExpDate;
  $self->{CurPeriod} = $CurPeriod;
  ($self->{fCurEffDate},$self->{fCurExpDate}) = split('-',$self->{CurPeriod});
  $self->{PARemDays} = DBUtil->Date($PAExpDate,'diff',$CurDate);
  $self->{CurRemDays} = DBUtil->Date($self->{CurExpDate},'diff',$CurDate);
#warn qq|InvPA: CurEffDate=$self->{CurEffDate}, CurExpDate=$self->{CurExpDate}, CurPeriod=$self->{CurPeriod}\n|;
#warn qq|InvPA: fCurEffDate=$self->{fCurEffDate}, fCurExpDate=$self->{fCurExpDate}\n|;
#warn qq|InvPA: PARemDays=$self->{PARemDays}, CurRemDays=$self->{CurRemDays}\n|;
  $self->{CurAmtAuth} = $self->{$CurPeriod}->{AmtAuth};
  $self->{CurAmtUsed} = '0';
  $self->{CurAmtLeft} = $self->{CurAmtAuth}-$self->{CurAmtUsed};
  $self->{CurUnitsAuth} = $self->{$CurPeriod}->{UnitsAuth};
  $self->{CurUnitsUsed} = '0';
  $self->{CurUnitsLeft} = $self->{CurUnitsAuth}-$self->{CurUnitsUsed};
  return($self);
}
sub getPALines
{
  my ($self,$form,$PrAuthID) = @_;
  my $dbh = myDBI->dbconnect($form->{'DBNAME'});
  $sPALines = $dbh->prepare("select * from PALines where PrAuthID=? order by BegDate,EndDate");
  $sPALines->execute($PrAuthID);
  while ( $rPALines = $sPALines->fetchrow_hashref )
  {
    my $BegDate = $rPALines->{'BegDate'};
    my $EndDate = $rPALines->{'EndDate'};
#warn qq|getPALines: BegDate=${BegDate},EndDate=${EndDate}\n|;
    push(@{$self->{PADates}},"${BegDate}/${EndDate}");
    my $fBegDate = DBUtil->Date($BegDate,'fmt','MM/DD/YYYY');
    my $fEndDate = DBUtil->Date($EndDate,'fmt','MM/DD/YYYY');
    my $key = "${fBegDate}-${fEndDate}";
    $self->{$key}->{AmtAuth} = $rPALines->{'Cost'};
    $self->{$key}->{AmtUsed} = 0;
    $self->{$key}->{AmtLeft} = $self->{$key}->{AmtAuth}-$self->{$key}->{AmtUsed};
    $self->{$key}->{UnitsAuth} = $rPALines->{'Units'};
    $self->{$key}->{UnitsUsed} = 0;
    $self->{$key}->{UnitsLeft} = $self->{$key}->{UnitsAuth}-$self->{$key}->{UnitsUsed};
#warn qq|getPALines: ${key}: AmtAuth=$self->{$key}->{AmtAuth},AmtLeft=$self->{$key}->{AmtLeft}\n|;
    foreach my $scidunits ( split(chr(253),$rPALines->{'SCIDs'}) )
    {
      my ($SCID,$Units) = split('/',$scidunits);
#warn qq|getPALines: SCID=$SCID, Units=$Units\n|;
      my $SCNum = DBA->getxref($form,'xSC',$SCID,'SCNum');
      my $InsID = DBA->getxref($form,'xSC',$SCID,'InsID');
      my $InsDescr = DBA->getxref($form,'xInsurance',$InsID,'Descr');
      $self->{$SCID}->{UnitsAuth} += $Units;
      $self->{$SCID}->{UnitsUsed} = 0;
      $self->{$SCID}->{UnitsLeft} = $self->{$SCID}->{UnitsAuth}-$self->{$SCID}->{UnitsUsed};
      $self->{$SCID}->{EffDate} = $EffDate;
      $self->{$SCID}->{ExpDate} = $ExpDate;
      $self->{$SCID}->{PAText} .= qq|${EffDate} ${ExpDate} ${Units}}<BR>|;
      $self->{PASCID}->{$SCID} = qq|${InsDescr}-${SCNum}|;
    }
  }
  return(1);
}
sub InvNotes
{
  my ($self,$form,$ClientID,$InsID) = @_;
#warn qq|InvNotes: ClientID=$ClientID, InsID=$InsID, PAgroup=$self->{PAgroup}\n|;

  my $TrCnt = 0;
  my $InsDescr = DBA->getxref($form,'xInsurance',$InsID,'Descr');
  my $ShowAmounts = SysAccess->verify($form,'Privilege=ShowAmounts');
  my $dbh = myDBI->dbconnect($form->{'DBNAME'});
  $qTreatment = qq|
select Treatment.ClientID, Treatment.ProvID, Treatment.TrID, Treatment.SCID
     , Treatment.ContLogDate, Treatment.Units, Treatment.BilledAmt
     , xSC.InsID, xSC.Interchange, xSC.ExInv, xSC.SCNum, xSC.SCName, xSCRates.UnitLbl 
  from Treatment 
    left join xSC on xSC.SCID=Treatment.SCID
    left join xSCRates on xSCRates.SCID=xSC.SCID
  where ClientID=? and ContLogDate between ? and ?
    and xSCRates.EffDate <= Treatment.ContLogDate and (Treatment.ContLogDate <= xSCRates.ExpDate or xSCRates.ExpDate is null)
  order by ContLogDate|;
#warn qq|InvNotes: qTreatment=$qTreatment, ClientID=$ClientID, EffDate=$self->{PAEffDate}, $self->{PAExpDate}\n|;
  $sTreatment = $dbh->prepare($qTreatment);
  $sTreatment->execute($ClientID,$self->{PAEffDate},$self->{PAExpDate});
  while ( $rTreatment = $sTreatment->fetchrow_hashref )
  {
#warn qq|InvNotes: TrID=$rTreatment->{TrID}, ContLogDate=$rTreatment->{ContLogDate}\n|;
    my $TrID = $rTreatment->{TrID};
    my $SCID = $rTreatment->{Interchange} ? $rTreatment->{Interchange} : $rTreatment->{SCID};
    my $ContDate = $rTreatment->{ContLogDate};
    my $TrUnits = $rTreatment->{Units};
#warn qq|InvNotes: TrID=${TrID}, SCID=${SCID}, ContDate=${ContDate}, TrUnits=${TrUnits}\n|;
    next if ( $rTreatment->{UnitLbl} eq 'NonBill' );    # we don't want these.
    next if ( $rTreatment->{ExInv} );                   # we don't want these.
    $TrCnt+=1;
# these are for all notes within entire PA Period.
#   Units...
    $self->{$SCID}->{UnitsAuth} += 0;               # make sure it's numeric
    $self->{$SCID}->{UnitsUsed} += $TrUnits;
    $self->{$SCID}->{UnitsLeft} = $self->{$SCID}->{UnitsAuth}-$self->{$SCID}->{UnitsUsed};
    $self->{TRID}->{$TrID}->{UnitsUsed} += $TrUnits;
#   Amounts...
    $self->{$SCID}->{AmtAuth} += 0;                 # make sure it's numeric
    $self->{$SCID}->{AmtUsed} += $rTreatment->{BilledAmt};
    $self->{$SCID}->{AmtLeft} = $self->{$SCID}->{AmtAuth}-$self->{$SCID}->{AmtUsed};
    $self->{TRID}->{$TrID}->{AmtUsed} += $rTreatment->{BilledAmt};
#   Current totals...
    my ($CurEffDate,$CurExpDate,$CurPeriod) = $self->CurrentPeriod($form,$ContDate);
#warn qq|InvNotes: CurPeriod=$CurPeriod, AmtAuth=$self->{$CurPeriod}->{AmtAuth}, Amt=$rTreatment->{BilledAmt}, AmtUsed=$self->{$CurPeriod}->{AmtUsed}\n|;
#   only for Insurance/PA for these notes...
    if ( $rTreatment->{InsID} == $InsID 
         && $self->chkSCIDinPA($form,$self->{PAgroup},$SCID) )
    {
      $self->{UnitsUsed} += $TrUnits;
      $self->{UnitsLeft} = $self->{UnitsAuth} - $self->{UnitsUsed};
      $self->{AmtUsed} += $rTreatment->{BilledAmt};
      $self->{AmtLeft} = $self->{AmtAuth} - $self->{AmtUsed};
      if ( $self->{CurEffDate} le $ContDate && $ContDate le $self->{CurExpDate} )
      {
        $self->{CurAmtUsed} += $rTreatment->{BilledAmt};
        $self->{CurAmtLeft} = $self->{CurAmtAuth} - $self->{CurAmtUsed};
      }
#     add up by each period for PA, current in these.
      $self->{$CurPeriod}->{UnitsUsed} += $TrUnits;
      $self->{$CurPeriod}->{UnitsLeft} = 
              $self->{$CurPeriod}->{UnitsAuth} - $self->{$CurPeriod}->{UnitsUsed};
      $self->{$CurPeriod}->{AmtUsed} += $rTreatment->{BilledAmt};
      $self->{$CurPeriod}->{AmtLeft} = 
              $self->{$CurPeriod}->{AmtAuth} - $self->{$CurPeriod}->{AmtUsed};
      my $List = qq|${TrID} ${ContDate} ${TrUnits} |;
      $List .= $ShowAmounts ? $rTreatment->{BilledAmt} . ' <BR>' : ' <BR>';
      $self->{INPALIST} .= $List;
      $self->{$CurPeriod}->{INPALIST} .= $List;
      $self->{$CurPeriod}->{INPAUNITS} += $TrUnits;
      $self->{$CurPeriod}->{INPAAMT} += $rTreatment->{BilledAmt};
      $self->{$CurPeriod}->{INPA}->{$SCID} = qq|${InsDescr}-$rTreatment->{SCNum}|;
      $self->{$CurPeriod}->{$SCID}->{$TrID} = $TrID;
      $self->{$CurPeriod}->{$SCID}->{$TrID}->{ContDate} = $ContDate;
      $self->{$CurPeriod}->{$SCID}->{$TrID}->{Amt} = $rTreatment->{BilledAmt};
      $self->{$CurPeriod}->{$SCID}->{$TrID}->{Units} = $TrUnits;
      $self->{$CurPeriod}->{$SCID}->{LIST} .= $List;      # separate out by Service Code.
      $self->{$CurPeriod}->{$SCID}->{UNITS} += $TrUnits;
      $self->{$CurPeriod}->{$SCID}->{AMT} += $rTreatment->{BilledAmt};
      my $SCNum = $rTreatment->{'SCNum'};
      if ( $SCNum =~ /H2017/ )      # Rehab services...
      {
        my $List = qq|${TrID} ${SCNum} ${ContDate} ${TrUnits} |;
        $List .= $ShowAmounts ? $rTreatment->{BilledAmt} . ' <BR>' : ' <BR>';
        $self->{$CurPeriod}->{INPAH2017}->{H2017} = qq|${InsDescr}-H2017|;
        $self->{$CurPeriod}->{H2017}->{$TrID} = $rTreatment->{TrID};
        $self->{$CurPeriod}->{H2017}->{$TrID}->{ContDate} = $ContDate;
        $self->{$CurPeriod}->{H2017}->{$TrID}->{Amt} = $rTreatment->{BilledAmt};
        $self->{$CurPeriod}->{H2017}->{$TrID}->{Units} = $TrUnits;
        $self->{$CurPeriod}->{H2017}->{LIST} .= $List;      # separate out by Service Code.
        $self->{$CurPeriod}->{H2017}->{UNITS} += $TrUnits;
        $self->{$CurPeriod}->{H2017}->{AMT} += $rTreatment->{BilledAmt};
      }
      my $SCName = $rTreatment->{'SCName'};
      if ( $SCName =~ /(F2F)/ )      # Face To Face services...
      {
        my $List = qq|${TrID} ${SCNum} ${ContDate} ${TrUnits} |;
        $List .= $ShowAmounts ? $rTreatment->{BilledAmt} . ' <BR>' : ' <BR>';
        $self->{$CurPeriod}->{INPAF2F}->{F2F} = qq|${InsDescr}-F2F|;
        $self->{$CurPeriod}->{F2F}->{$TrID} = $rTreatment->{TrID};
        $self->{$CurPeriod}->{F2F}->{$TrID}->{ContDate} = $ContDate;
        $self->{$CurPeriod}->{F2F}->{$TrID}->{Amt} = $rTreatment->{BilledAmt};
        $self->{$CurPeriod}->{F2F}->{$TrID}->{Units} = $TrUnits;
        $self->{$CurPeriod}->{F2F}->{LIST} .= $List;      # separate out by Service Code.
        $self->{$CurPeriod}->{F2F}->{UNITS} += $TrUnits;
        $self->{$CurPeriod}->{F2F}->{AMT} += $rTreatment->{BilledAmt};
      }
    }
#   only for NON Insurance/PA for these notes...
    else
    {
      my $ins = DBA->getxref($form,'xInsurance',$rTreatment->{InsID},'Descr');
      my $List = qq|${TrID} ${ContDate} ${TrUnits} |;
      $List .= $ShowAmounts ? $rTreatment->{BilledAmt} . ' <BR>' : ' <BR>';
      $self->{NONPALIST} .= $List;
      $self->{$CurPeriod}->{NONPALIST} .= $List;
      $self->{$CurPeriod}->{NONPAUNITS} += $TrUnits;
      $self->{$CurPeriod}->{NONPAAMT} += $rTreatment->{BilledAmt};
      $self->{$CurPeriod}->{NONPA}->{$SCID} = qq|${ins}-$rTreatment->{SCNum}|;
      my $TrID = $rTreatment->{TrID};
      $self->{$CurPeriod}->{$SCID}->{$TrID} = $TrID;
      $self->{$CurPeriod}->{$SCID}->{$TrID}->{ContDate} = $ContDate;
      $self->{$CurPeriod}->{$SCID}->{$TrID}->{Amt} = $rTreatment->{BilledAmt};
      $self->{$CurPeriod}->{$SCID}->{$TrID}->{Units} = $TrUnits;
      $self->{$CurPeriod}->{$SCID}->{LIST} .= $List;      # separate out by Service Code.
      $self->{$CurPeriod}->{$SCID}->{UNITS} += $TrUnits;
      $self->{$CurPeriod}->{$SCID}->{AMT} += $rTreatment->{BilledAmt};
    }
#warn qq|$rTreatment->{ClientID}:CurPeriod=$CurPeriod:$rTreatment->{SCID},${SCID}:$rTreatment->{TrID},Units=$rTreatment->{Units},$self->{$SCID}->{UnitsUsed},$self->{$SCID}->{UnitsLeft}\n|;
#warn qq|ClientID=$rTreatment->{ClientID}:CurPeriod=$CurPeriod:SCID=$rTreatment->{SCID},${SCID}\n|;
#warn qq|TrID=$rTreatment->{TrID}:Amt=$rTreatment->{BilledAmt}:Units=${TrUnits}\n|;
#warn qq|CurAmt=$self->{CurAmtAuth},$self->{CurAmtUsed},$self->{CurAmtLeft}\n|;
  }
  $sTreatment->finish();
  $self->{TrCnt} = $TrCnt;
  $self->{AUTHLIST} = qq|<TABLE ALIGN="center" ><TR><TD CLASS="hdrcol">Code</TD><TD CLASS="hdrcol">Auth</TD><TD CLASS="hdrcol">Used</TD><TD CLASS="hdrcol">Left</TD></TR>|;
  foreach $SCID ( keys %{ $self->{PASCID} } )
  {
    my $UnitsAuth = sprintf("%.2f",$self->{$SCID}->{UnitsAuth});
    my $UnitsUsed = sprintf("%.2f",$self->{$SCID}->{UnitsUsed});
    my $UnitsLeft = sprintf("%.2f",$self->{$SCID}->{UnitsAuth} - $self->{$SCID}->{UnitsUsed});
    $self->{AUTHLIST} .= qq|<TR ><TD CLASS="hdrcol">$self->{PASCID}->{$SCID}</TD><TD CLASS="numcol">${UnitsAuth}</TD><TD CLASS="numcol">${UnitsUsed}</TD><TD CLASS="numcol">${UnitsLeft}</TD></TR>|;
  }
  $self->{AUTHLIST} .= qq|</TABLE>|;
#warn qq|InvNotes: TrCnt=$TrCnt\n|;
  return($self);
}
############################################################################
sub CurrentPeriod
{
  my ($self,$form,$TheDate) = @_;
  foreach my $Dates ( @{$self->{PADates}} )
  {
    my ($BDate,$EDate) = split('/',$Dates);
#warn qq|CurrentPeriod: BDate=$BDate, EDate=$EDate, TheDate=$TheDate\n|;
    if ( $BDate le $TheDate && $TheDate le $EDate )
    {
      my $fBDate = DBUtil->Date($BDate,'fmt','MM/DD/YYYY');
      my $fEDate = DBUtil->Date($EDate,'fmt','MM/DD/YYYY');
      my $key = "${fBDate}-${fEDate}";
      return($BDate,$EDate,$key);
    }
  }
  return();
# not used because displays on ClientList...
  my $fTheDate = DBUtil->Date($TheDate,'fmt','MM/DD/YYYY');
  my $key = "CURRENT-${fTheDate}";
#warn qq|CurrentPeriod: key=$key\n|;
  return($TheDate,$TheDate,$key);
}
############################################################################
sub CurPeriod
{
  my ($self,$form,$StartDate,$EndDate,$cDate) = @_;
  my $CurDate = $cDate ? $cDate : $form->{TODAY};
#warn qq|CurPeriod: StartDate=$StartDate, EndDate=$EndDate, CurDate=$CurDate\n|;
  return('','') if ( $CurDate lt $StartDate );
  return('','') if ( $CurDate gt $EndDate );
  my $BegCurDate = $StartDate;
  my $EndCurDate = DBUtil->Date($BegCurDate,1,-1);
  $EndCurDate = $EndDate if ( $EndCurDate gt $EndDate );
#warn qq|CurPeriod: CurDate=$CurDate, BegCurDate=$BegCurDate, EndCurDate=$EndCurDate\n|;
  until ( $BegCurDate le $CurDate && $CurDate le $EndCurDate )
  {
#warn qq| CurPeriod: 1. CurDate=$CurDate, BegCurDate=$BegCurDate, EndCurDate=$EndCurDate\n|;
    $BegCurDate = DBUtil->Date($EndCurDate,0,1);
    $EndCurDate = DBUtil->Date($BegCurDate,1,-1);
    $EndCurDate = $EndDate if ( $EndCurDate gt $EndDate );
#warn qq| CurPeriod: 2. CurDate=$CurDate, BegCurDate=$BegCurDate, EndCurDate=$EndCurDate\n|;
#warn qq| CurPeriod: check again...\n|;
  }
  return($BegCurDate,$EndCurDate);
}
sub chkSCIDinPA
{
  my ($self,$form,$PAgroup,$SCID) = @_;
#warn qq|chkSCIDinPA: PAgroup=${PAgroup}, SCID=${SCID}\n|;
  return(1) unless ( $PAgroup );
  return(1) unless ( $SCID );
  my $cdbh = myDBI->dbconnect('okmis_config');
  my $s = $cdbh->prepare("select SCIDs from xPAgroups where ID=?");
  $s->execute($PAgroup) || $form->dberror("chkSCIDinPA: select $PAgroup/$SCID");
  my ($SCIDs) = $s->fetchrow_array;
  my $ok=0;
  foreach my $scid ( split(chr(253),$SCIDs) )
  { $ok=1 if ( $scid == $SCID ); }
  $s->finish();
#warn qq|chkSCIDinPA: ok=$ok\n|;
  return($ok);
}
sub chkRVUSC
{
  my ($self,$form,$PrAuthID,$SCID) = @_;
  my $MatchSCID = 0;
  my $dbh = myDBI->dbconnect($form->{'DBNAME'});
  my $qPrAuthRVU = qq|select * from PrAuthRVU where PrAuthID=${PrAuthID} order by EffDate|;
#warn "qPrAuthRVU=\n$qPrAuthRVU\n";
  my $sPrAuthRVU = $dbh->prepare($qPrAuthRVU);
  $sPrAuthRVU->execute() || $form->dberror($qPrAuthRVU);
  while ( my $rPrAuthRVU = $sPrAuthRVU->fetchrow_hashref )
  {
#warn qq|$rNote->{TrID}: $rPrAuthRVU->{SCID}, $rNote->{SCID}, $rPrAuthRVU->{EffDate}, $rNote->{ContLogDate}, $rPrAuthRVU->{ExpDate}\n|;
    $MatchSCID = $rPrAuthRVU->{SCID} == $rNote->{SCID}
              && $rPrAuthRVU->{EffDate} le $rNote->{ContLogDate} 
              && $rNote->{ContLogDate} le $rPrAuthRVU->{ExpDate}
               ? 1 : 0;
#warn qq|MatchSCID=$MatchSCID\n|;
    last if ( $MatchSCID );
  }
  $sPrAuthRVU->finish();
  return($MatchSCID);
}
###########################################################################################
sub setPALines
{
  my ($self,$form,$PrAuthID) = @_;
#warn qq|\nsetPALines: PrAuthID=${PrAuthID}\n|;
  my $dbh = myDBI->dbconnect($form->{'DBNAME'});
  my $sPrAuth = $dbh->prepare("select ClientPrAuth.*,ClientPrAuthCDC.TransType from ClientPrAuth left join ClientPrAuthCDC on ClientPrAuthCDC.ClientPrAuthID=ClientPrAuth.ID where ClientPrAuth.ID=?");
  $sPrAuth->execute($PrAuthID) || $form->dberror("setPALines: select ClientPrAuth $PrAuthID");
  if ( my $rPrAuth = $sPrAuth->fetchrow_hashref )
  {
#warn qq|\nsetPALines: ClientID=$rPrAuth->{ClientID},ID=$rPrAuth->{ID},TransType=$rPrAuth->{TransType}\n|;
#foreach my $f ( sort keys %{$rPrAuth} ) { warn "  : rPrAuth-$f=$rPrAuth->{$f}\n"; }
    if ( $rPrAuth->{'NotificationType'} )        # these are specific to genClientPrAuthCDC.
    { $sPrAuth->finish(); return(); }

    my $sDelete = $dbh->prepare("delete from PALines where PrAuthID=?");
    $sDelete->execute($PrAuthID) || $form->dberror("setPALines: delete PALines $PrAuthID");
    $sDelete->finish();

    if ( $rPrAuth->{'PAnumber'} eq '' )          # ONLY Approved PAs.
    { $sPrAuth->finish(); return(); }

    my ($NumLines,$Units,$SCIDs) = (0,0,'');
    if ( $rPrAuth->{'PAgroup'} eq '' )
    {
#warn qq|setPALines: PrAuthID=$PrAuthID,EffDate=$rPrAuth->{EffDate},ExpDate=$rPrAuth->{ExpDate}\n|;
      ($Units,$NumLines,$SCIDs) = 
           $self->getRVUs($form,$PrAuthID,$rPrAuth->{'EffDate'},$rPrAuth->{'ExpDate'});
      my $sUpdate = $dbh->prepare("update ClientPrAuth set UnitsAuth=?,LinesAuth=?,LOS=? where ClientPrAuth.ID=?");
      $sUpdate->execute($Units,$NumLines,$NumLines,$PrAuthID)
                 || $form->dberror("setPALines: update ClientPrAuth $PrAuthID");
      $sUpdate->finish();
      $rPrAuth->{'UnitsAuth'} = $Units;
      $rPrAuth->{'LinesAuth'} = $NumLines;
      $rPrAuth->{'LOS'} = $NumLines;
#warn qq|setPALines: UnitsAuth=$rPrAuth->{UnitsAuth},LinesAuth=$rPrAuth->{LinesAuth},LOS=$rPrAuth->{LOS}\n|;
    }
    my $ClientID = $rPrAuth->{'ClientID'};
    my $PAgroup = $rPrAuth->{'PAgroup'};
    my $AuthAmt = $rPrAuth->{'AuthAmt'};
    my $UnitsAuth = $rPrAuth->{'UnitsAuth'};
    my $LinesAuth = $rPrAuth->{'LinesAuth'};
    $LinesAuth = 1 unless ( $LinesAuth );
#warn qq|\nsetPALines: PAgroup=${PAgroup}, AuthAmt=${AuthAmt}, UnitsAuth=${UnitsAuth}, LinesAuth=${LinesAuth}/$rPrAuth->{'LinesAuth'}\n|;
    foreach my $key
    ( $self->PAPeriods($form,$LinesAuth,$rPrAuth->{EffDate},$rPrAuth->{ExpDate}) )
    {
      #print qq|key=$key\n|;
      my $rPALines = ();
      $rPALines->{'ClientID'} = $ClientID;
      $rPALines->{'PrAuthID'} = $PrAuthID;
      $rPALines->{'CreateProvID'} = $form->{'LOGINPROVID'};
      $rPALines->{'CreateDate'} = $form->{'TODAY'};
      $rPALines->{'ChangeProvID'} = $form->{'LOGINPROVID'};
      my ($BD,$ED) = split('/',$key);
      $rPALines->{'BegDate'} = $BD;
      $rPALines->{'EndDate'} = $ED;
      $rPALines->{'PAgroup'} = $PAgroup;
#warn qq|\n setPALines: AuthAmt=${AuthAmt},UnitsAuth=${UnitsAuth},LinesAuth=${LinesAuth}\n|;
      $LineCost = sprintf('%.4f',$AuthAmt/$LinesAuth);
      $LineUnits = sprintf('%.4f',$UnitsAuth/$LinesAuth);
#warn qq|\n setPALines: LineCost=${LineCost},LineUnits=${LineUnits}\n|;
      $rPALines->{'Cost'} = $LineCost;
      $rPALines->{'Units'} = $LineUnits;
      $rPALines->{'SCIDs'} = $SCIDs;
      $rPALines->{'Status'} = 'A';                   # because ONLY Approved PAs.
#foreach my $f ( sort keys %{$rPALines} ) { warn " setPALines: rPALines-$f=$rPALines->{$f}\n"; }
      $NEWID = DBA->doUpdate($form,'PALines',$rPALines);
    }
  }
  $sPrAuth->finish();
  return();
}
sub getRVUs
{
  my ($self,$form,$PrAuthID,$EffDate,$ExpDate) = @_;
  my $dbh = myDBI->dbconnect($form->{'DBNAME'});
  my ($Lines,$SCIDs,$AuthRVU,$dlm) = (0,'',0,'');
# count the Lines (monthly periods)
  foreach my $key ( $self->PAPeriods($form,0,$EffDate,$ExpDate) ) { $Lines++; }
  $Lines = 1 unless ( $Lines );
  my $qPrAuthRVU = qq|
select PrAuthRVU.PrAuthID, PrAuthRVU.SCID, PrAuthRVU.AuthRVU
      ,PrAuthRVU.EffDate, PrAuthRVU.ExpDate
      ,xInsurance.Descr, xSC.SCName, xSC.SCNum, xSC.Interchange
  from PrAuthRVU
    left join xSC on xSC.SCID=PrAuthRVU.SCID
    left join xInsurance on xInsurance.ID=xSC.InsID
  where PrAuthRVU.PrAuthID=? and PrAuthRVU.AuthRVU is not null
|;
  $sPrAuthRVU = $dbh->prepare($qPrAuthRVU);
  $sPrAuthRVU->execute($PrAuthID) || $form->dberror($qPrAuthRVU);
  while ( $rPrAuthRVU = $sPrAuthRVU->fetchrow_hashref )
  {
    my $SCID = $rPrAuthRVU->{'Interchange'}
             ? $rPrAuthRVU->{'Interchange'}
             : $rPrAuthRVU->{'SCID'};
    next unless ( $SCID );
    $AuthRVU += $rPrAuthRVU->{'AuthRVU'};
    my $RVU = sprintf('%.4f',$rPrAuthRVU->{'AuthRVU'}/$Lines);
    $SCIDs .= $dlm.$SCID.'/'.$RVU;
    $dlm = chr(253);
  }
  $sPrAuthRVU->finish();
  return($AuthRVU,$Lines,$SCIDs);
}
sub PAPeriods
{
  my ($self,$form,$Lines,$StartDate,$EndDate,$fDate,$cDate) = @_;
  my @Dates = ();
# format can be MM/DD/YYYY or YYYY-MM-DD
  my $dlm = $fDate =~ /\// ? '-' : '/';
  my $CurDate = $cDate ? $cDate : $form->{TODAY};
#warn qq|PAPeriods: StartDate=$StartDate, EndDate=$EndDate, CurDate=$CurDate\n|;
  return() unless ( $StartDate );
  return() unless ( $EndDate );
  my $BDate = $StartDate;
  my $EDate = DBUtil->Date($BDate,1,-1);
  return() unless ( $EDate );
#warn qq|PAPeriods: StartDate=$StartDate, EndDate=$EndDate\n|;
#warn qq|PAPeriods: CurDate=$CurDate, BDate=$BDate, EDate=$EDate\n|;
  while ( $BDate le $EndDate )
  {
    $EDate = $EndDate if ( $EDate gt $EndDate || $Lines == 1 );
    my $fBDate = $fDate eq '' ? $BDate : DBUtil->Date($BDate,'fmt',$fDate);
    my $fEDate = $fDate eq '' ? $EDate : DBUtil->Date($EDate,'fmt',$fDate);
    push(@Dates,"${fBDate}${dlm}${fEDate}");
#warn qq| PAPeriods: 1. CurDate=$CurDate, BDate=$BDate, EDate=$EDate\n|;
    $BDate = DBUtil->Date($EDate,0,1);
    $EDate = DBUtil->Date($BDate,1,-1);
#warn qq| PAPeriods: 2. CurDate=$CurDate, BDate=$BDate, EDate=$EDate\n|;
#warn qq| PAPeriods: check again...\n|;
  }
#warn qq|PAPeriods: Dates=@Dates\n|;
  return(@Dates);
}
############################################################################
1;
