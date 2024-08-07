package uBill;
use cBill;
my $debug=1;
############################################################################
# set unrec flag unless just added a tranaction.
sub setBilledAmt
{
  my ($self, $form, $TrID, $unrec) = @_;
#warn qq|\nsetBilledAmt: $TrID\n|;
  my $dbh = myDBI->dbconnect($form->{'DBNAME'});

  my $sTreatment = $dbh->prepare("select * from Treatment where TrID=?");
  $sTreatment->execute($TrID) || $form->dberror("setBilledAmt: select Treatment (${TrID})");
  my $rTreatment = $sTreatment->fetchrow_hashref;
  return($rTreatment->{BilledAmt},$rTreatment->{IncAmt},$rTreatment->{SchAmt},$rTreatment->{AmtDue})
    if ( $rTreatment->{'BillStatus'} == 5 && $unrec );

  my $rBilled = cBill->getServiceCode($form,$rTreatment->{SCID},$rTreatment->{ContLogDate},$rTreatment->{ContLogBegTime},$rTreatment->{ContLogEndTime},$rTreatment->{TrID},$rTreatment->{BillDate});
  my $rAddon1 = cBill->getServiceCode($form,$rTreatment->{SCID2},$rTreatment->{ContLogDate},$rTreatment->{ContLogBegTime},$rTreatment->{ContLogEndTime},$rTreatment->{TrID},$rTreatment->{BillDate});
  my $rAddon2 = cBill->getServiceCode($form,$rTreatment->{SCID3},$rTreatment->{ContLogDate},$rTreatment->{ContLogBegTime},$rTreatment->{ContLogEndTime},$rTreatment->{TrID},$rTreatment->{BillDate});
  my $rAddon4 = cBill->getServiceCode($form,$rTreatment->{SCID4},$rTreatment->{ContLogDate},$rTreatment->{ContLogBegTime},$rTreatment->{ContLogEndTime},$rTreatment->{TrID},$rTreatment->{BillDate});
  my $rAddon5 = cBill->getServiceCode($form,$rTreatment->{SCID5},$rTreatment->{ContLogDate},$rTreatment->{ContLogBegTime},$rTreatment->{ContLogEndTime},$rTreatment->{TrID},$rTreatment->{BillDate});
  my $rAddon6 = cBill->getServiceCode($form,$rTreatment->{SCID6},$rTreatment->{ContLogDate},$rTreatment->{ContLogBegTime},$rTreatment->{ContLogEndTime},$rTreatment->{TrID},$rTreatment->{BillDate});
  my $BilledAmt = $rBilled->{'BillAmt'}+$rAddon1->{'BillAmt'}+$rAddon2->{'BillAmt'}+$rAddon4->{'BillAmt'}+$rAddon5->{'BillAmt'}+$rAddon6->{'BillAmt'};
#warn qq|setBilledAmt: BilledAmt=$BilledAmt\n|;
#warn qq|setBilledAmt: BillAmt=$rBilled->{BillAmt}\n|;
#warn qq|setBilledAmt: BillAmt1=$rAddon1->{BillAmt}\n|;
#warn qq|setBilledAmt: BillAmt2=$rAddon2->{BillAmt}\n|;

  my $CurAmtDue = $rTreatment->{'AmtDue'};        # save for last trans Scholarshipped (should be 0).
  my $LastCode = '';                              # save because we don't want to update where writtenoff.
  my ($tcnt,$SchAmt,$RecAmt) = (0,0,0);
  my $sNoteTrans = $dbh->prepare("select * from NoteTrans where TrID=? order by ID");
  $sNoteTrans->execute($TrID);
  while ( $rNoteTrans = $sNoteTrans->fetchrow_hashref )
  { 
    $tcnt++;
#warn qq|  1: $rNoteTrans->{SCNum}, $rNoteTrans->{SCID}, B=$rNoteTrans->{BillAmt}, $rTreatment->{SCID}, $rTreatment->{SCID2}\n|;
#warn qq|  1: Add1Amt=$Add1Amt, Add2Amt=$Add2Amt\n|;
    $RecAmt += $rNoteTrans->{'PaidAmt'};
    $SchAmt += $rNoteTrans->{'PaidAmt'} if ( $rNoteTrans->{Code} eq 'SR' );
    $LastCode = $rNoteTrans->{Code};
#warn qq|  x: PaidAmt=$rNoteTrans->{'PaidAmt'}, RecAmt=$RecAmt, SchAmt=$SchAmt\n|;
#warn qq|  2: Add1Amt=$Add1Amt, Add2Amt=$Add2Amt\n|;
  }
  $sNoteTrans->finish();
  $sTreatment->finish();

# fix the BilledAmt to TOTAL Reconciled if Scholarshipped already!  these had been previously fixed.
  $BilledAmt = $RecAmt       if ( $CurAmtDue == 0 && $LastCode eq 'SR' && $RecAmt > 0 );
  $BilledAmt = sprintf("%.2f",$BilledAmt);
  $RecAmt = sprintf("%.2f",$RecAmt);
  $SchAmt = sprintf("%.2f",$SchAmt);
  my $IncAmt = sprintf("%.2f",$RecAmt - $SchAmt);
  my $AmtDue = $RecAmt < 0 ? $BilledAmt : $RecAmt > $BilledAmt ? 0 : $BilledAmt - $RecAmt;
  $AmtDue = 0 if ( $AmtDue < 0 );
  $AmtDue = sprintf("%.2f",$AmtDue);
#warn qq|ENDLOOP B=$BilledAmt, $rxSC->{BillAmt}, $Add1Amt, $Add2Amt\n|;
#warn qq|ENDLOOP I=$IncAmt, R=$RecAmt, S=$SchAmt, A=$AmtDue\n|;
#warn qq|SAVED: LastCode=$LastCode, CurAmtDue=$CurAmtDue\n|;

# now update the Treatment table amounts...
#warn qq|setBilledAmt: BilledAmt=${BilledAmt}\n|;
#warn qq|setBilledAmt: IncAmt=${IncAmt}\n|;
#warn qq|setBilledAmt: SchAmt=${SchAmt}\n|;
#warn qq|setBilledAmt: AmtDue=${AmtDue}\n|;
  my $sTreatment = $dbh->prepare("update Treatment set BilledAmt=?,IncAmt=?,SchAmt=?,AmtDue=? where TrID=?");
  $sTreatment->execute($BilledAmt,$IncAmt,$SchAmt,$AmtDue,$TrID) || $form->dberror("setBilledAmt: update Treatment (${TrID})");
  $sTreatment->finish();
  return($BilledAmt,$IncAmt,$SchAmt,$AmtDue);
}
sub setBillStatus()
{
  my ($self, $form, $TrID, $Status, $Date, $StatusMsg) = @_;
  return(0) if ( $TrID eq '' );
  return(0) if ( $Status eq '' );
  my $dbh = myDBI->dbconnect($form->{'DBNAME'});
  my $qNote = qq|select BillStatus,AmtDue from Treatment where TrID=?|;
  my $sNote = $dbh->prepare($qNote);
  $sNote->execute($TrID) || $form->dberror($qNote);
  my ($CurrStatus,$AmtDue) = $sNote->fetchrow_array;
  $sNote->finish();
# don't set if wanting to deny(6)
#      when already reconciled(5) or recoupment(9) or scholarshipped(4).
#   835 may have denied a rebill right after a recoupment.
#   835 may have denied a rebill when they've already scholarshipped.
#warn qq|setBillStatus: $TrID, $Status, $Date, $CurrStatus\n|;
  return(0) if ( $Status == 6 && 
      ($CurrStatus == 5 || $CurrStatus == 9 || $CurrStatus == 4 || $AmtDue <= 0) );
# don't set if wanting to scholarship(4) and note already reconciled(5)
  return(0) if ( $Status == 4 && $CurrStatus == 5 );
  $Date = $form->{TODAY} if ( $Date eq '' );
#warn qq|setBillStatus: set: $TrID, $Status, $Date\n|;
  my $qStatus = qq|update Treatment set BillStatus=?, StatusDate=?, StatusMsg=? where TrID=?|;
  my $sStatus = $dbh->prepare($qStatus);
  $sStatus->execute($Status,$Date,$StatusMsg,$TrID) || $form->dberror($qStatus);
  $sStatus->finish();
  return(1);
}
sub setRevStatus()
{
  my ($self, $form, $TrID, $Status) = @_;
  return(0) if ( $TrID eq '' );
  return(0) if ( $Status eq '' );
  my $dbh = myDBI->dbconnect($form->{'DBNAME'});
  my $qStatus = qq|update Treatment set RevStatus=? where TrID=?|;
#warn qq|setRevStatus: qStatus=$qStatus: vars: Status=$Status, TrID=$TrID\n|;
  my $sStatus = $dbh->prepare($qStatus);
  $sStatus->execute($Status,$TrID) || $form->dberror($qStatus);
  $sStatus->finish();
  return(1);
}
sub setPayDate()
{
  my ($self,$form,$MarkDate,$ID,$TrID) = @_;
  return(0) if ( $MarkDate eq '' );
#warn qq|setPayDate: MarkDate=${MarkDate}, ID=${ID}, TrID=${TrID}\n|;
  my $dbh = myDBI->dbconnect($form->{'DBNAME'});
  unless ( $ID eq '' )
  {
    my $sNoteTrans = $dbh->prepare("update NoteTrans set PaidDate=? where ID=? and PaidDate is null");
    $sNoteTrans->execute($MarkDate,$ID) || $form->dberror("setPayDate: select NoteTrans ${TrID}");
    $sNoteTrans->finish();
  }
  unless ( $TrID eq '' )
  {
    my $sTreatment = $dbh->prepare("update Treatment set PaidDate=? where TrID=? and PaidDate is null");
    $sTreatment->execute($MarkDate,$TrID) || $form->dberror("setPayDate: select Treatment ${TrID}");
    $sTreatment->finish();
  }
  return(1);
}
############################################################################
sub fixUnbillable()
{
  my ($self, $form, $TrID) = @_;
  return(0) if ( $TrID eq '' );
  my $dbh = myDBI->dbconnect($form->{'DBNAME'});
  my $qNote = qq|select BillDate,BillStatus from Treatment where TrID=?|;
  my $sNote = $dbh->prepare($qNote);
  $sNote->execute($TrID) || $form->dberror($qNote);
  my ($BillDate,$CurrStatus) = $sNote->fetchrow_array;
  $sNote->finish();
# don't set if BillStatus not Unbillable
#warn qq|fixUnbillable: check: $TrID, $BillDate, $CurrStatus\n|;
  return(0) if ( $CurrStatus != 2 );
# Status is 'new' if never Billed else 'rebill'.
  my $Status = $BillDate eq '' ? 0 : 1;
#warn qq|fixUnbillable: set: $TrID, $Status\n|;
  my $qStatus = qq|update Treatment set BillStatus=?, StatusDate=?, StatusMsg=NULL where TrID=?|;
  my $sStatus = $dbh->prepare($qStatus);
  $sStatus->execute($Status,$form->{TODAY},$TrID) || $form->dberror($qStatus);
  $sStatus->finish();
  return(1);
}
############################################################################
# Always execute set... routines above (if needed) before these fix... routines
# ie. setBilledAmt if needed because used here...
sub fixBillDate()
{
  my ($self, $form, $TrID, $BillDate) = @_;
  return(0) if ( $TrID eq '' );
  return(0) if ( $BillDate eq '' );
  my $dbh = myDBI->dbconnect($form->{'DBNAME'});
  my $qBill = qq|update Treatment set BillDate=? where TrID=? and BillDate is null|;
  my $sBill = $dbh->prepare($qBill);
  $sBill->execute($BillDate,$TrID) || $form->dberror($qBill);
  $sBill->finish();
  return(1);
}
sub fixBillStatus()
{
  my ($self, $form, $TrID, $StatusMsg) = @_;
  return(0) if ( $TrID eq '' );
  my $dbh = myDBI->dbconnect($form->{'DBNAME'});
  my ($BilledAmt,$IncAmt,$SchAmt,$AmtDue) =(0,0,0,0);
  my $qBilled = qq|select BilledAmt,IncAmt,SchAmt,AmtDue from Treatment where TrID=?|;
#warn qq|qBilled=$qBilled\n|;
  my $sBilled = $dbh->prepare($qBilled);
  $sBilled->execute($TrID) || $form->dberror($qBilled);
  if ( ($BilledAmt,$IncAmt,$SchAmt,$AmtDue) = $sBilled->fetchrow_array )
  {
#warn qq|fixBillStatus: check: $TrID, BilledAmt=$BilledAmt, IncAmt=$SchAmt, IncAmt=$SchAmt, AmtDue=$AmtDue\n|;
    my $Status=5;
    if ( $IncAmt > 0 ) { $Status = 5; }       # reconciled
    elsif ( $SchAmt > 0 ) { $Status = 4; }    # scholarship
    elsif ( $AmtDue > 0 ) { $Status = 7; }    # adjusted
    else { $Status = 4; }                     # Due=0 and nothing paid, non-bill/scholarshipped
    my $qStatus = qq|update Treatment set BillStatus=?, StatusDate='$form->{TODAY}', StatusMsg=? where TrID=?|;
    my $sStatus = $dbh->prepare($qStatus);
    $sStatus->execute($Status,$StatusMsg,$TrID) || $form->dberror($qStatus);
    $sStatus->finish();
  }
  $sBilled->finish();
  return(1);
}
##
# this one makes sure the RevStatus matches up to the existing Review Dates
sub fixRevStatus()
{
  my ($self, $form, $TrID) = @_;
  return(0) if ( $TrID eq '' );
  my $dbh = myDBI->dbconnect($form->{'DBNAME'});
  my $qTreatment = qq|select ProvOKDate,MgrRevDate,RevStatus from Treatment where TrID=?|;
#warn qq|qTreatment=$qTreatment: vars: TrID=$TrID\n|;
  my $sTreatment = $dbh->prepare($qTreatment);
  $sTreatment->execute($TrID) || $form->dberror($qTreatment);
  if ( my ($ProvDT,$MgrDT,$RevStatus) = $sTreatment->fetchrow_array )
  {
#warn qq|fixRevStatus: check: $TrID, ProvDT=$ProvDT, MgrDT=$MgrDT, RevStatus=$RevStatus\n|;
    my $Status = 0;
    if ( $ProvDT && $MgrDT) { $Status = 3; }
    elsif ( $ProvDT ) { $Status = 2; }
    elsif ( $MgrDT ) { $Status = 1; }
    else { $Status = 0; }
    my $qStatus = qq|update Treatment set RevStatus=${Status} where TrID=?|;
#warn qq|RevStatus: qStatus=$qStatus: vars: TrID=$TrID\n|;
    my $sStatus = $dbh->prepare($qStatus);
    $sStatus->execute($TrID) || $form->dberror($qStatus);
    $sStatus->finish();
  }
  $sTreatment->finish();
  return(1);
}
##
# this one makes sure Review Dates match up to the given RevStatus(Status)
sub fixRevDates()
{
  my ($self, $form, $TrID, $Status) = @_;
#warn qq|fixRevDates: TrID=$TrID, Status=$Status\n|;
  return(0) if ( $TrID eq '' );
  return(0) if ( $Status eq '' );
  my ($s, $m, $h, $day, $mon, $year) = localtime;
  my $curtime = sprintf('%02d:%02d:%02d', $h, $m, $s);
  my $dbh = myDBI->dbconnect($form->{'DBNAME'});
  my $qTreatment = qq|select ProvOKDate,MgrRevDate,RevStatus from Treatment where TrID=?|;
#warn qq|fixRevDates: qTreatment=$qTreatment: vars: TrID=$TrID\n|;
  my $sTreatment = $dbh->prepare($qTreatment);
  $sTreatment->execute($TrID) || $form->dberror($qTreatment);
  if ( ($ProvDT,$MgrDT,$RevStatus) = $sTreatment->fetchrow_array )
  {
#warn qq|fixRevDates: check: $TrID, ProvDT=$ProvDT, MgrDT=$MgrDT, RevStatus=$RevStatus\n|;
    my $u = "RevStatus=$Status";
    if ( $Status == 3 )               # note approved
    {
      if ( $ProvDT eq '' )
      { $u .= qq|, ProvOKDate='$form->{TODAY}', ProvOKTime='${curtime}'|; }
      if ( $MgrDT eq '' )
      { $u .= qq|, MgrProvID='$form->{LOGINPROVID}', MgrRevDate='$form->{TODAY}', MgrRevTime='${curtime}'|; }
    }
    elsif ( $Status == 2 )            # Manager approval needed
    {
      if ( $ProvDT eq '' )
      { $u .= qq|, ProvOKDate='$form->{TODAY}', ProvOKTime='${curtime}'|; }
      $u .= qq|, MgrProvID=NULL, MgrRevDate=NULL, MgrRevTime=NULL|; 
    }
    elsif ( $Status == 1 )            # Provider approval needed afer change
    {
      if ( $MgrDT eq '' )
      { $u .= qq|, MgrProvID='$form->{LOGINPROVID}', MgrRevDate='$form->{TODAY}', MgrRevTime='${curtime}'|; }
      $u .= qq|, ProvOKDate=NULL, ProvOKTime=NULL|; 
    }
    elsif ( $Status == 0 )            # new - Provider approval needed
    {
      $u .= qq|, ProvOKDate=NULL, ProvOKTime=NULL|; 
      $u .= qq|, MgrProvID=NULL, MgrRevDate=NULL, MgrRevTime=NULL|; 
    }
    else { return(0); }
    unless ( $u eq '' )
    {
      my $qStatus = qq|update Treatment set ${u} where TrID=?|;
#warn qq|fixRevStatus: qStatus=$qStatus: vars: TrID=$TrID\n|;
      my $sStatus = $dbh->prepare($qStatus);
      $sStatus->execute($TrID) || $form->dberror($qStatus);
      $sStatus->finish();
    }
  }
  $sTreatment->finish();
  return(1);
}
############################################################################
# SRC=BD, BI, BS, CL, DA, ER, HH, MA, MD, MR, MS, SR
# Code=ADJ, AR, BI, 
#      ER, ER-C, ER-I, ER-N, ER-R, ER-T, 
#      FR, FX, ID-B, ID-R, IR, KS, MD, MR, PR, SR
sub postClaim
{
  my ($self,$form,$record,$SRC,$Code,$StatusMsg) = @_;
#warn qq|postClaim: enter...\n|;
#foreach my $f ( sort keys %{$record} ) { warn "postClaim: record-$f=$record->{$f}\n"; }
#warn qq|postClaim: WATCH: TrID=$record->{'TrID'}\n|;
  my $TransID = $record->{'TransID'};
  my $TrID = $record->{'TrID'};
  my $ClientID = $record->{'ClientID'};
  my $ContDate = $record->{'ContDate'};
  my $ServCode = $record->{'ServCode'};
  my $ICN = $record->{'ICN'};
  my $r = $self->selTrans($form,$TransID,$TrID,$SRC,$Code,$ClientID,$ContDate,$ServCode,$ICN);
#foreach my $f ( sort keys %{$r} ) { warn "postClaim: after: r-$f=$r->{$f}\n"; }
  return('','','','NOT FOUND!') unless ( $r->{'TrID'} );    # error out!

  my $TrID = $r->{'TrID'};
  my $TransID = $r->{'ID'};                       # reset to new '' or found trans
  $r->{'SRC'} = $SRC;                             # calling resource
  $r->{'Code'} = $Code unless ( $Code eq '' );    # substitute unless null
  $r->{'RecDate'} = $record->{'RecDate'};         # must be given.
  $r->{'PaidDate'} = $record->{'PaidDate'};       # must be given. (Payroll)
  $r->{'RefID'}   = $record->{'RefID'};           # must be given.
  $r->{'PaidAmt'} = $record->{'PaidAmt'};         # must be given.
  $r->{'PayerID'} = $record->{'PayerID'};         # must be given.
  $r->{'ICN'} = $record->{'ICN'};                 # must be given.
  $r->{'DenCode'} = $record->{'DenCode'};         # must be given.
  $r->{'RemarkCode'} = $record->{'RemarkCode'};   
  $r->{'TransType'} = $record->{'TransType'};   
  $r->{'AdjAmt'} = $record->{'AdjAmt'};   
  $r->{'ReasonCode'} = $record->{'ReasonCode'};   # must be given.
  $r->{'AdjCode'} = $record->{'AdjCode'};         # must be given.
  $r->{'RenProvID'} = $record->{'RenProvID'};     # must be given.
  $r->{'InsPaidID'} = $record->{'InsPaidID'};     # must be given.
  $r->{'ChangeProvID'} = $form->{'LOGINPROVID'};  # always updated.
# leave as is unless given
  $r->{'BillDate'} = $record->{'BillDate'}        unless ( $record->{'BillDate'} eq '' );
  $r->{'BillAmt'} = $record->{'BillAmt'}          unless ( $record->{'BillAmt'} eq '' || $record->{'BillAmt'} < 0 );
  $r->{'Units'}   = $record->{'Units'}            unless ( $record->{'Units'} eq '' || $record->{'Units'} < 0 );
  $r->{'InsCode'} = $record->{'InsCode'}          unless ( $record->{'InsCode'} eq '' );
#print qq|postClaim: set...TransID/ID=${TransID}/$r->{'ID'}\n|;
#foreach my $f ( sort keys %{$r} ) { print "postClaim: set: r-$f=$r->{$f}\n"; }
#print qq|postClaim: CODE=$r->{'Code'}\n|;
  my $UID = $TransID eq ''            # insert or update only (RecDate is null as safety)
          ? DBA->doUpdate($form,'NoteTrans',$r)
          : DBA->doUpdate($form,'NoteTrans',$r,"ID=${TransID} and RecDate is null",'',1);
  my $SCID = $r->{'SCID'};
  my $RecDate = $r->{'RecDate'};
  my $DenCode = $r->{'DenCode'};
  my $RemarkCode = $r->{'RemarkCode'};  
  my $PaidAmt = $r->{'PaidAmt'};
  my $BS;
#print qq|postClaim: PaidAmt=$r->{'PaidAmt'}\n|;
#print qq|postClaim: Code=$r->{'Code'}\n|;
  if ( $r->{PaidAmt} > 0 ||
       $r->{'Code'} eq 'SR' || 
       $r->{'Code'} eq 'AR' ) { $BS = $self->reconcileClaim($form,$TrID,$RecDate,$r->{'Code'},$StatusMsg); }
  elsif ( $r->{PaidAmt} < 0 ) { $BS = $self->voidClaim($form,$TrID,$RecDate,$DenCode,$StatusMsg); }
  else                        { $BS = $self->denyClaim($form,$TrID,$RecDate,$DenCode,$StatusMsg, $RemarkCode); }
  my ($BilledAmt,$IncAmt,$SchAmt,$AmtDue) = $self->setBilledAmt($form,$TrID);
# return these...
  my $Msg = $self->claimMessage($BS,$AmtDue,$PaidAmt,$DenCode);
#print qq|postClaim: return: TrID=${TrID}\n|;
#warn qq|postClaim: Msg=${Msg}\n|;
  return($TrID,$SCID,$r->{'Code'},$Msg);
}
sub selTrans
{
  my ($self,$form,$TransID,$TrID,$SRC,$Code,$ClientID,$ContDate,$ServCode,$ICN) = @_;
#warn qq|selTrans: TransID=${TransID},TrID=${TrID},Code=${Code}\n|;
#warn qq|selTrans: ClientID=${ClientID},ContDate=${ContDate},ServCode=${ServCode}\n|;
  my $rNoteTrans = ();
  if ( $TransID )
  {
  my $dbh = myDBI->dbconnect($form->{'DBNAME'});
    my $sNoteTrans = $dbh->prepare("select * from NoteTrans where BINARY ID=?");
    $sNoteTrans->execute($TransID) || $form->dberror("selTrans: select ${TransID}");
    if ( my $r = $sNoteTrans->fetchrow_hashref )
    { 
      $rNoteTrans = $r; 
      if ( $r->{RecDate} eq '' )                 # update
      { $rNoteTrans->{'Code'} = 'ER'; }
      else                                       # insert
      {
        delete $rNoteTrans->{ID};                # make sure we insert a new one.
        delete $rNoteTrans->{PaidDate};          # make sure it's selected for Payroll.
        delete $rNoteTrans->{BillAmt};           # when inserting, we did not bill.
        $rNoteTrans->{'Code'} = 'ER-I';
        $rNoteTrans->{'CreateProvID'} = $form->{'LOGINPROVID'};
        $rNoteTrans->{'CreateDate'}   = $form->{'TODAY'};
      }
      delete $rNoteTrans->{ChangeDate};          # don't keep
#warn qq|selTrans: select with TransID=${TransID}\n|;
    }
    else
    { $rNoteTrans = $self->FindTransUR($form,$SRC,$Code,$TrID,$ClientID,$ContDate,$ServCode,$ICN); }
    $sNoteTrans->finish();
  }
  else
  { $rNoteTrans = $self->FindTransUR($form,$SRC,$Code,$TrID,$ClientID,$ContDate,$ServCode,$ICN); }
#warn qq|selTrans: return\n| if ( $debug );
  return($rNoteTrans);
}
sub FindTransUR
{
  my ($self,$form,$SRC,$Code,$TrID,$ClientID,$ContDate,$ServCode,$ICN) = @_;
#warn qq|FindTransUR: SRC=${SRC},Code=${Code},TrID=${TrID}\n|;
#warn qq|FindTransUR: ClientID=${ClientID},ContDate=${ContDate},ServCode=${ServCode}\n|;
  my $dbh = myDBI->dbconnect($form->{'DBNAME'});
  my $rNoteTrans = ();
  my $where = $TrID && $ServCode
            ? qq|TrID='${TrID}' and SCNum='${ServCode}'| 
            : qq|ClientID='${ClientID}' and ContDate='${ContDate}' and SCNum='${ServCode}'|;
  my $sNoteTrans = $dbh->prepare("select * from NoteTrans where ${where} and RecDate is null order by ID desc");
  $sNoteTrans->execute() || $form->dberror("FindTransUR: select ${where}");
  if ( my $r = $sNoteTrans->fetchrow_hashref ) # update
  { 
    $rNoteTrans = $r; 
    $rNoteTrans->{Code} = 'ER-T';
    delete $rNoteTrans->{ChangeDate};          # don't keep
#warn qq|FindTransUR: select where ${where}\n|;
  }
  else
  { $rNoteTrans = $self->FindTransICN($form,$SRC,$Code,$TrID,$ClientID,$ContDate,$ServCode,$ICN); }
  $sNoteTrans->finish();
#warn qq|FindTransUR: return\n| if ( $debug );
  return($rNoteTrans);
}
sub FindTransICN
{
  my ($self,$form,$SRC,$Code,$TrID,$ClientID,$ContDate,$ServCode,$ICN) = @_;
#warn qq|FindTransICN: SRC=${SRC},Code=${Code},TrID=${TrID}\n|;
#warn qq|FindTransICN: ClientID=${ClientID},ContDate=${ContDate},ServCode=${ServCode},ICN=${ICN}\n|;
  my $dbh = myDBI->dbconnect($form->{'DBNAME'});
  my $rNoteTrans = ();
  if ( $ICN eq '' ) 
  { $rNoteTrans = $self->FindTrans($form,$SRC,$Code,$TrID,$ClientID,$ContDate,$ServCode); }
  else
  {
    my $where = $TrID
              ? qq|TrID='${TrID}' and ICN='${ICN}'| 
              : qq|ClientID='${ClientID}' and ContDate='${ContDate}' and SCNum='${ServCode}' and ICN='${ICN}'|;
    my $sNoteTrans = $dbh->prepare("select * from NoteTrans where ${where} order by ID desc");
    $sNoteTrans->execute() || $form->dberror("FindTransICN: select ${where}");
    if ( my $r = $sNoteTrans->fetchrow_hashref ) # insert
    { 
      $rNoteTrans = $r; 
      delete $rNoteTrans->{ID};                  # make sure we insert a new one.
      delete $rNoteTrans->{PaidDate};            # make sure it's selected for Payroll.
      delete $rNoteTrans->{BillAmt};             # when inserting, we did not bill.
      delete $rNoteTrans->{ChangeDate};          # don't keep
      $rNoteTrans->{Code} = 'ER-C';
      $rNoteTrans->{'CreateProvID'} = $form->{'LOGINPROVID'};
      $rNoteTrans->{'CreateDate'}   = $form->{'TODAY'};
#warn qq|FindTransICN: select where ${where}\n|;
    }
    else
    { $rNoteTrans = $self->FindTrans($form,$SRC,$Code,$TrID,$ClientID,$ContDate,$ServCode); }
    $sNoteTrans->finish();
  }
#warn qq|FindTransICN: return\n| if ( $debug );
  return($rNoteTrans);
}
sub FindTrans
{
  my ($self,$form,$SRC,$Code,$TrID,$ClientID,$ContDate,$ServCode) = @_;
#warn qq|FindTrans: SRC=${SRC},Code=${Code},TrID=${TrID}\n|;
#warn qq|FindTrans: ClientID=${ClientID},ContDate=${ContDate},ServCode=${ServCode}\n|;
  my $dbh = myDBI->dbconnect($form->{'DBNAME'});
  my $rNoteTrans = ();
  my $where = $TrID && $ServCode 
            ? qq|TrID='${TrID}' and SCNum='${ServCode}'| 
            : qq|ClientID='${ClientID}' and ContDate='${ContDate}' and SCNum='${ServCode}'|;
  my $sNoteTrans = $dbh->prepare("select * from NoteTrans where ${where} order by ID desc");
  $sNoteTrans->execute() || $form->dberror("FindTrans: select ${where}");
  if ( my $r = $sNoteTrans->fetchrow_hashref ) # insert
  { 
    $rNoteTrans = $r; 
    delete $rNoteTrans->{ID};                  # make sure we insert a new one.
    delete $rNoteTrans->{PaidDate};            # make sure it's selected for Payroll.
    delete $rNoteTrans->{BillAmt};             # when inserting, we did not bill.
    delete $rNoteTrans->{ChangeDate};          # don't keep
    $rNoteTrans->{Code} = 'ER-R';
    $rNoteTrans->{'CreateProvID'} = $form->{'LOGINPROVID'};
    $rNoteTrans->{'CreateDate'}   = $form->{'TODAY'};
#warn qq|FindTrans: select where ${where}\n|;
  }
  else
  { $rNoteTrans = $self->FindNote($form,$SRC,$Code,$TrID,$ClientID,$ContDate,$ServCode); }
  $sNoteTrans->finish();
#warn qq|FindTrans: return\n| if ( $debug );
  return($rNoteTrans);
}
sub FindNote
{
  my ($self,$form,$SRC,$Code,$TrID,$ClientID,$ContDate,$ServCode) = @_;
#warn qq|FindNote: SRC=${SRC},Code=${Code},TrID=${TrID}\n|;
#warn qq|FindNote: ClientID=${ClientID},ContDate=${ContDate},ServCode=${ServCode}\n|;
  my $dbh = myDBI->dbconnect($form->{'DBNAME'});
  my $rNoteTrans = ();
  my $where = $TrID 
            ? qq|Treatment.TrID='${TrID}'| 
            : qq|Treatment.ClientID='${ClientID}' and Treatment.ContLogDate='${ContDate}' and xSC.SCNum='${ServCode}'|;
  my $sNoteTrans = $dbh->prepare("select * from Treatment left join xSC on xSC.SCID=Treatment.SCID left join xInsurance on xInsurance.ID=xSC.InsID where ${where}");
  $sNoteTrans->execute() || $form->dberror("FindNote: select ${where}");
  if ( my $r = $sNoteTrans->fetchrow_hashref ) # insert
  { $rNoteTrans = $self->defNoteTrans($form,$r->{'TrID'},$SRC,$Code); }
#warn qq|FindNote: select where ${where}\n|;
  $sNoteTrans->finish();
#warn qq|FindNote: return\n| if ( $debug );
  return($rNoteTrans);
}
sub defNoteTrans()
{
  my ($self,$form,$TrID,$SRC,$Code) = @_;
#warn qq|defNoteTrans: TrID=${TrID}, SRC=${SRC}, Code=${Code}\n|;
  my $dbh = myDBI->dbconnect($form->{'DBNAME'});
  my $sTreatment = $dbh->prepare("select * from Treatment where TrID=?");
  $sTreatment->execute($TrID) || $form->dberror("defNoteTrans: select Treatment ${TrID}");
  my $rTreatment = $sTreatment->fetchrow_hashref;
  my $rxSC = cBill->getServiceCode($form,$rTreatment->{SCID},$rTreatment->{ContLogDate},$rTreatment->{ContLogBegTime},$rTreatment->{ContLogEndTime},$rTreatment->{TrID},$rTreatment->{BillDate});
  my $rNoteTrans = ();           # NO ID! so insert.
  $rNoteTrans->{'TrID'} = $rTreatment->{'TrID'};
  $rNoteTrans->{'ClientID'} = $rTreatment->{'ClientID'};
  $rNoteTrans->{'ProvID'} = $rTreatment->{'ProvID'};
  $rNoteTrans->{'ContDate'} = $rTreatment->{'ContLogDate'};
  $rNoteTrans->{'SCID'} = $rTreatment->{'SCID'};
  $rNoteTrans->{'SCNum'} = $rTreatment->{'Mod4'} eq '' ? $rxSC->{'SCNum'} : $rxSC->{'SCNum'}.' '.$rTreatment->{'Mod4'};
  $rNoteTrans->{'Units'} = $rxSC->{'Units'};
  $rNoteTrans->{'Duration'} = $rxSC->{'Duration'};
  $rNoteTrans->{'BillAmt'} = $rxSC->{'BillAmt'};
  $rNoteTrans->{'InsCode'} = $rxSC->{'InsCode'};
  $rNoteTrans->{'SRC'} = $SRC;
  $rNoteTrans->{'Code'} = 'ER-N';
  $rNoteTrans->{'CreateProvID'} = $form->{'LOGINPROVID'};
  $rNoteTrans->{'CreateDate'}   = $form->{'TODAY'};
  $rNoteTrans->{'ChangeProvID'} = $form->{'LOGINPROVID'};
  $sTreatment->finish();
#foreach my $f ( sort keys %{$rNoteTrans} ) { warn "defNoteTrans: rNoteTrans-$f=$rNoteTrans->{$f}\n"; }
  return($rNoteTrans);
}
sub reconcileClaim
{
  my ($self,$form,$TrID,$RecDate,$Code,$StatusMsg) = @_;
  my $rUpdate = ();                      # first null these...
  $rUpdate->{'TrID'} = $TrID;
  $rUpdate->{'CIPDate'} = '';
  $rUpdate->{'DenDate'} = '';
  $rUpdate->{'DenCode'} = '';
  $rUpdate->{'COPLDate'} = '';
#foreach my $f ( sort keys %{$rUpdate} ) { warn "reconcileClaim1: $f=$rUpdate->{$f}\n"; }
  my $UID = DBA->doUpdate($form,'Treatment',$rUpdate,"TrID=$TrID",'',1);
  my $rUpdate = ();                      # then set RecDate if not set...
  $rUpdate->{'TrID'} = $TrID;
  $rUpdate->{'RecDate'} = $RecDate;
  $rUpdate->{'PaidDate'} = $RecDate if ( $Code eq 'SR' );
#foreach my $f ( sort keys %{$rUpdate} ) { warn "reconcileClaim2: $f=$rUpdate->{$f}\n"; }
  my $UID = DBA->doUpdate($form,'Treatment',$rUpdate,"TrID=$TrID and RecDate is null",'',1);
  my $BillStatus = $Code eq 'SR' ? 4 : 5;
#warn qq|reconcileClaim: TrID: ${TrID}: BillStatus=${BillStatus}\n|;
  $self->setBillStatus($form,$TrID,$BillStatus,$RecDate,$StatusMsg);
  return($BillStatus);
}
sub denyClaim
{
  my ($self,$form,$TrID,$RecDate,$DenCode,$StatusMsg, $RemarkCode) = @_;
  my $rUpdate = ();
  $rUpdate->{'TrID'} = $TrID;
  $rUpdate->{'DenDate'} = $RecDate;
  $rUpdate->{'DenCode'} = $DenCode;
  $rUpdate->{'RemarkCode'} = $RemarkCode;
#foreach my $f ( sort keys %{$rUpdate} ) { warn "denyClaim: $f=$rUpdate->{$f}\n"; }
  my $UID = DBA->doUpdate($form,'Treatment',$rUpdate,"TrID=$TrID and RecDate is null",'',1);
#warn qq|denyClaim: TrID: ${TrID}: DenDate=${RecDate}\n|;
  $self->setBillStatus($form,$TrID,'6',$RecDate,$StatusMsg);
  return(6);
}
sub voidClaim
{
  my ($self,$form,$TrID,$RecDate,$DenCode,$StatusMsg) = @_;
  my $rUpdate = ();
  $rUpdate->{'TrID'} = $TrID;
  $rUpdate->{'DenDate'} = $RecDate;
  $rUpdate->{'DenCode'} = $DenCode;
# void even if RecDate is not null
#foreach my $f ( sort keys %{$rUpdate} ) { warn "voidClaim: $f=$rUpdate->{$f}\n"; }
  my $UID = DBA->doUpdate($form,'Treatment',$rUpdate,"TrID=$TrID",'',1);
#warn qq|denyClaim: TrID: ${TrID}: RecDate=${RecDate}\n|;
  $self->setBillStatus($form,$TrID,'9',$RecDate,$StatusMsg);
  return(9);
}
sub claimMessage
{
  my ($self,$BillStatus,$AmtDue,$PaidAmt,$DenCode) = @_;
#warn "claimMessage: BillStatus=$BillStatus, AmtDue=$AmtDue, PaidAmt=$PaidAmt, DenCode=$DenCode\n";
  my $msg = '';
  if ( $BillStatus == 4 )
  { $msg .= qq|${PaidAmt} Amount Written Off|; }
  elsif ( $BillStatus == 5 )
  {
    if ( $AmtDue > 0 )       # partial then rebill
    { $msg .= qq|Partial Reconciled Claim; Rebill ${AmtDue}|; }
    else
    { $msg .= qq|Reconciled Claim|; }
  }
  elsif ( $BillStatus == 6 || $BillStatus == 9 )
  {
    if ( $PaidAmt == 0 ) { $msg .= qq|Denied Claim|; }
    elsif ( $PaidAmt < 0 ) { $msg .= qq|Void/Recoupment|; }
    elsif ( $AmtDue > 0 ) { $msg .= qq|Partial Denied Claim; Rebill ${AmtDue}|; }
    else  { $msg .= qq|Partial Denied Claim|; }
    $msg .= qq| DenCode NULL!| unless ( $DenCode );
  }
#warn "claimMessage: msg=$msg\n";
  return($msg);
}
############################################################################
1;
