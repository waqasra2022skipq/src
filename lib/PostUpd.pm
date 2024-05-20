package PostUpd;
use DBA;
use myDBI;
use DBUtil;
use myConfig;
use cBill;
use uBill;
use Inv;
use CDC;
use URI::Escape;
use JSON;
############################################################################
sub newClient
{
  my ($self,$form) = @_;
  my $dbh = myDBI->dbconnect($form->{'DBNAME'});
  my $ClientID=$form->{Client_ClientID_1};
  my $ProvID=$form->{Client_ProvID_1};
  my $InsID=$form->{Insurance_InsID_1};
  my $PrAuthID=$form->{ClientPrAuth_ID_1};
#warn qq|ENTER newClient: ClientID=$form->{Client_ClientID_1}, ProvID=$form->{Client_ProvID_1}, PrAuthID=$form->{ClientPrAuth_ID_1}, InsID=$form->{Insurance_InsID_1}\n|;
#warn qq|ENTER newClient: ClientID=${ClientID}, ProvID=${ProvID}, PrAuthID=${PrAuthID}, InsID=$InsID, PrAuth_Type=$form->{ClientPrAuth_Type_1}\n|;
# set these...
  my $s = $dbh->prepare("update Client set HmPh=MobPh where ClientID=? and HmPh is null");
  $s->execute($ClientID) || myDBI->dberror("newClient: update HmPh ${ClientID}!");
  $s->finish();

# set the real ClientACL table for this client
#   all Client Access based on ClientACl, so we need to update it...
#   it uses the Providers SiteACL + the ClientAccess to update ClientACL...
  SysAccess->rebldClientACL($form,$ClientID,$ProvID,1);
  unless ( $form->{'Insurance_EligibleType_1'} eq 'No' )      # add Eligible for this month
  {
    my ($FromDate,$ToDate) = DBUtil->Date('','monthly');
    $sx = $dbh->prepare("select * from xEligibleType where Descr=?");
    $sx->execute($form->{'Insurance_EligibleType_1'}) || myDBI->dberror("newClient: select xEligibleType!");
    my $rx = $sx->fetchrow_hashref;
    $sx->finish();
    my $r = ();
    $r->{'ClientID'}=$ClientID;
    $r->{'PlanDescr'}=$form->{'Insurance_EligibleType_1'};
    $r->{'InsCode'}=$rx->{'InsCode'};
    $r->{'ServiceType'}=$rx->{'ServiceType'};
    $r->{'FromDate'}=$FromDate;
    $r->{'ToDate'}=$ToDate;
    $r->{'Coverage'}='IND';
    $r->{'Benefit'}='1';
    $r->{'BenefitDescr'}='Initial Check';
#foreach my $f ( sort keys %{$rx} ) { warn "newClient: rx-$f=$rx->{$f}\n"; }
    my $ID = DBA->doUpdate($form,'Eligible',$r);
  }

# set Contact CDC (21) TransType but only for newClients
#warn qq|newClient: check getRule: EnableCDC\n|;
  if ( SysAccess->getRule($form,'EnableCDC') )
  {
#warn qq|newClient: YES getRule: EnableCDC\n|;
    $sClientReferrals = $dbh->prepare("select RefDate from ClientReferrals where ClientID='${ClientID}'");
    $sClientReferrals->execute() || myDBI->dberror("newClient: select ClientReferrals ${ClientID}");
    my ($RefDate) = $sClientReferrals->fetchrow_array;
    $sClientReferrals->finish();
#   calcPG is done again in setPrAuthTL (updPrAuth)
    my $PAgroup = DBA->isIndMedicaid($form,$ClientID) ? 'PG030' : 'PG038';
    my ($months,$days) = DBA->calcLOS($form,$InsID,$PAgroup);
    my $r = ();
    $r->{'PAgroup'} = $PAgroup;
                                 # FIX Inventory to handle days... FIX
    $r->{'LOS'} = $months;       # FIX get rid of LOS because it is only months FIX
    $r->{'EffDate'} = $RefDate;
    $r->{'ExpDate'} = DBUtil->Date($EffDate,$months,$days);
    DBA->doUpdate($form,'ClientPrAuth',$r,"ID=$PrAuthID");

    my $r = ();
    $r->{'TransDate'} = $RefDate;
    $r->{'TransTime'} = '09:00:00';
    $r->{'TransType'} = $PAgroup =~ /PG030|DH502/ ? 23 : 21;
    # auto Send on new client?
    ##$r->{'Status'} = $r->{'TransType'} == 21 ? 'Send' : 'Waiting';
    $r->{'Status'} = 'New';
    $r->{'StatusDate'} = $form->{'TODAY'};
    DBA->doUpdate($form,'ClientPrAuthCDC',$r,"ClientPrAuthID=$PrAuthID");
#warn qq|newClient: PAgroup=$PAgroup, TransType=$r->{TransType}\n|;
  }
  my $str = PostUpd->updPrAuth($form,$PrAuthID,1);
  return();     # return no error message
}
sub updPA       # only for UN-Authorized (Expired after today and No PAnumber)
{
  my ($self,$form,$ClientID) = @_;
#warn qq|\n\nENTER updPA: ClientID=$ClientID\n|;
#foreach my $f ( sort keys %{$form} ) { warn "updPA: form-$f=$form->{$f}\n"; }
  return() if ( $ClientID eq '' );
  my $dbh = myDBI->dbconnect($form->{'DBNAME'});
# set these...can be updated from ClientIntake.cgi screen...
  my $s = $dbh->prepare("update Client set HmPh=MobPh where ClientID=? and HmPh is null");
  $s->execute($ClientID) || myDBI->dberror("newClient: update HmPh $ClientID!");
  $s->finish();

  my $qPrAuth = qq|select ID from ClientPrAuth where ClientPrAuth.ClientID=${ClientID} and ClientPrAuth.ExpDate>='$form->{TODAY}' and ClientPrAuth.PAnumber is null|;
#warn qq|updPA: qPrAuth=$qPrAuth\n|;
  my $sPrAuth = $dbh->prepare($qPrAuth);
  $sPrAuth->execute() || myDBI->dberror("updPA: ${qPrAuth}");
  while ( my ($PrAuthID) = $sPrAuth->fetchrow_array )
  {
#warn qq|updPA: PrAuthID=$PrAuthID\n|;
    PostUpd->updPrAuth($form,$PrAuthID,1);
  }
  $sPrAuth->finish();
  return();     # return no error message
}
sub updPrAuth
{
  my ($self,$form,$PID,$RVU) = @_;
#foreach my $f ( sort keys %{$form} ) { warn "updPrAuth: form-$f=$form->{$f}\n"; }
  my $PrAuthID = $PID ? $PID : $form->{'ClientPrAuth_ID'};
#warn qq|\n\nENTER updPrAuth: PID=$PID, PrAuthID=$PrAuthID, RVU=$RVU\n|;
  return() unless ( $PrAuthID );

  my $dbh = myDBI->dbconnect($form->{'DBNAME'});
  my $sPrAuth = $dbh->prepare("select ClientPrAuth.*,Insurance.InsID from ClientPrAuth left join Insurance on Insurance.InsNumID=ClientPrAuth.InsuranceID where ClientPrAuth.ID='${PrAuthID}'");
  $sPrAuth->execute() || myDBI->dberror("updPrAuth: select ${PrAuthID}");
  if ( my $rPrAuth = $sPrAuth->fetchrow_hashref )
  {
#warn qq|updPrAuth: ClientID=$rPrAuth->{ClientID}, PrAuthID=${PrAuthID}\n|;
# set the Treatment Level/PAgroup only for those UN-Approved PAs.
#   and the PAgroup only for those Treatment Levels in xPAgroup.
    my ($TL,$PAgroup) = PostUpd->setPrAuthTL($form,$rPrAuth);

# set the dates from PA into RVU.
    my $sUpdRVU = $dbh->prepare("update PrAuthRVU set EffDate='$rPrAuth->{EffDate}', ExpDate='$rPrAuth->{ExpDate}' where PrAuthID='${PrAuthID}'");
    $sUpdRVU->execute() || myDBI->dberror("updPrAuth: RVU for dates");
    $sUpdRVU->finish();
# ask by PrAuthRVU.cgi
#   set the PA number only if RVUs exist and PANum is not null.
    PostUpd->setPrAuthNum($form,$rPrAuth->{ID}) if ( $RVU );

    # set the Prior Auth if needed...
    my $msg = CDC->setPA($form,$rPrAuth->{ID});

#warn qq|updPrAuth: CLOSE=$form->{'CLOSE'}\n|;
    if ( $form->{'CLOSE'} eq $PrAuthID )
    {
      my $sUpdCLOSE = $dbh->prepare("update ClientPrAuth set ExpDate='$rPrAuth->{EffDate}' where ID='${PrAuthID}'");
#warn "update ClientPrAuth set ExpDate='$rPrAuth->{EffDate}' where ID='${PrAuthID}'\n";
      $sUpdCLOSE->execute() || myDBI->dberror("updPrAuth: CLOSE for dates");
      $sUpdCLOSE->finish();
      my $sUpdCLOSE = $dbh->prepare("update ClientPrAuthCDC set Status='Closed',StatusDate='$form->{TODAY}',Fail=NULL where ClientPrAuthID='${PrAuthID}'");
      $sUpdCLOSE->execute() || myDBI->dberror("updPrAuth: CLOSE for dates");
      $sUpdCLOSE->finish();
    }
    if ( $form->{'REOPEN'} eq $PrAuthID )
    {
      my ($months,$days) = DBA->calcLOS($form,$rPrAuth->{'InsID'},$rPrAuth->{'PAgroup'});
      my $ExpDate = DBUtil->Date($rPrAuth->{'EffDate'},$months,$days);
      my $sUpdREOPEN = $dbh->prepare("update ClientPrAuth set ExpDate='${ExpDate}' where ID='${PrAuthID}'");
#warn "update ClientPrAuth set ExpDate='${ExpDate}' where ID='${PrAuthID}'\n";
      $sUpdREOPEN->execute() || myDBI->dberror("updPrAuth: REOPEN for dates");
      $sUpdREOPEN->finish();
      my $sUpdREOPEN = $dbh->prepare("update ClientPrAuthCDC set Status='New',StatusDate='$form->{TODAY}' where ClientPrAuthID='${PrAuthID}'");
      $sUpdREOPEN->execute() || myDBI->dberror("updPrAuth: REOPEN for dates");
      $sUpdREOPEN->finish();
    }

    # set the PALines for Approved PAs...
    Inv->setPALines($form,$rPrAuth->{'ID'});
  }
  $sPrAuth->finish();
  return();     # return no error message
}
sub setPrAuthTL
{
  my ($self,$form,$rPrAuth,$force) = @_;
  my $ClientID=$rPrAuth->{'ClientID'};
  my $PrAuthID=$rPrAuth->{'ID'};
  my $InsID=$rPrAuth->{'InsID'};
  return() if ( $PrAuthID eq '' );
  return() unless ( $rPrAuth->{PAnumber} eq '' || $force );

  my $dbh = myDBI->dbconnect($form->{'DBNAME'});
  my ($isAdult,$TL) = TLevel->getTreatmentLevel($form,$ClientID,'18',$PrAuthID);
#warn qq|setPrAuthTL: isAdult=$isAdult, TL=$TL\n|;
  my $qUpd = $TL eq '' ? qq|update ClientPrAuth set TL=NULL|
                       : qq|update ClientPrAuth set TL='${TL}'|;
# FIX FIX LevelCode in ClientPrAuth determines which way the Inventory goes
#   using PGCodes(Amounts) or RVUs(Units)
  my $PAgroup = CDC->calcPG($form,$ClientID,$InsID,$PrAuthID);
#warn qq|setPrAuthTL: PAgroup=${PAgroup}\n|;
  $qUpd .= qq|,PAgroup='${PAgroup}'|;
  ##$qUpd .= qq|,CDCOK=1| if ( $PAgroup eq '' || $PAgroup eq 'PG038' );
  $qUpd .= qq| where ID='${PrAuthID}'|;
#warn qq|setPrAuthTL: qUpd=$qUpd\n|;
  my $sUpd = $dbh->prepare($qUpd);
  $sUpd->execute() || myDBI->dberror("setPrAuthTL: ${qUpd}");
  $sUpd->finish();
  return($TL,$PAgroup);
}
sub NewJournal
{
  my ($self, $form) = @_;
  my $result = '';
#warn qq|NewJournal: ENTER: new=$form->{NEWJOURNAL}: ID=$form->{ClientJournals_ID} \n|;
  if ( $form->{NEWJOURNAL} eq 'new' )
  {
    my $Subject = qq|New Journal Entry: $form->{Client_ClientID_1}|;
    my $Text = $form->{ClientJournals_Summary_1};
    DBUtil->emailP($form, $form->{Client_ProvID_1}, $Subject, $Text, '', 1);
  }
  return($result);
}
sub updNote
{
  my ($self, $form) = @_;
#warn qq|PostUpd: updNote: ENTER: $form->{Treatment_TrID_1} \n|;
  my $dbh = myDBI->dbconnect($form->{'DBNAME'});
  my $ClientID=$form->{'Treatment_ClientID_1'};
  my $TrID=$form->{'Treatment_TrID_1'};
  my $SCID=$form->{'Treatment_SCID_1'};
  my $ContLogDate=$form->{'Treatment_ContLogDate_1'};
  my $ContLogBegTime=$form->{'Treatment_ContLogBegTime_1'};
  my $ContLogEndTime=$form->{'Treatment_ContLogEndTime_1'};
  my $BillDate=$form->{'Treatment_BillDate_1'};
  my $rxSC = cBill->getServiceCode($form,$SCID,$ContLogDate,$ContLogBegTime,$ContLogEndTime,$TrID,$BillDate);
#foreach my $f ( sort keys %{$rxSC} ) { warn "updNote 1: rxSC-$f=$rxSC->{$f}\n"; }
#my $sT= $dbh->prepare("select * from Treatment where TrID=?");
#$sT->execute($form->{'Treatment_TrID_1'}) || myDBI->dberror("updNote: set $form->{Treatment_TrID_1}");
#my $rT= $sT->fetchrow_hashref;
#$sT->finish();
#foreach my $f ( sort keys %{$rT} ) { warn "updNote 1: rT-$f=$rT->{$f}\n"; }
#warn qq|
#PostUpd: updNote: 
# ClientID=$form->{'Treatment_ClientID_1'}=
# TrID=$form->{'Treatment_TrID_1'}=
# SCID=$form->{'Treatment_SCID_1'}=
# SCNum=$form->{'Treatment_SCNum_1'}=
# BillStatus=$form->{'Treatment_BillStatus_1'}=
# BilledAmt=$form->{'Treatment_BilledAmt_1'}=
# IncAmt=$form->{'Treatment_IncAmt_1'}=
# SchAmt=$form->{'Treatment_SchAmt_1'}=
# AmtDue=$form->{'Treatment_AmtDue_1'}=
# Maladaptive=$form->{'Treatment_Maladaptive_1'}=
# Interfere=$form->{'Treatment_Interfere_1'}=
# Sentinel=$form->{'Treatment_Sentinel_1'}=
# PlayOvercome=$form->{'Treatment_PlayOvercome_1'}=
#\n|;
  my $result = '';
  my ($s, $m, $h, $day, $mon, $year) = localtime;
  my $curtime = sprintf('%02d:%02d:%02d', $h, $m, $s);
  my $inTable = 'ProgNotes';
  if ( $form->{Treatment_Type_1} == 2 ) { $inTable = 'PhysNotes'; }
#warn qq|PostUpd: updNote: delete=$form->{Treatment_DELETE_1}, Sch=$form->{note_scholarship} \n|;
  my $dbh = myDBI->dbconnect($form->{'DBNAME'});
  if ( $form->{rebill_note} || $form->{delete_note} || $form->{skip_note} )
  { null; }                 # everythings done in xSQL...
  elsif ( $form->{scholarship_note} )
  { 
    my $RecDate = $form->{'TODAY'};
    my ($BilledAmt,$IncAmt,$SchAmt,$AmtDue) = uBill->setBilledAmt($form,$TrID);
    my $r835 = ();
    $r835->{'TrID'}      = $TrID;
    $r835->{'BillDate'}  = $RecDate;
    $r835->{'RecDate'}   = $RecDate;
    $r835->{'PaidDate'}  = $RecDate;
    $r835->{'RefID'}     = 'Write Off Note';
    $r835->{'PaidAmt'}   = $AmtDue;
    my ($trid,$scid,$code,$type) = uBill->postClaim($form,$r835,'MS','SR');
    # did we reconcile this note before it was even billed?
    uBill->fixBillDate($form,$TrID,$RecDate);
    # don't leave it unreviewed.
    uBill->fixRevDates($form,$TrID,3);
  }
  elsif ( $form->{manager_unreview} )
  {
#warn qq|updNote: manager_unreview: $form->{Treatment_TrID_1} \n|;
    my $q = qq|update Treatment set MgrProvID=NULL, MgrRevDate=NULL, MgrRevTime=NULL where TrID=?|;
    my $s = $dbh->prepare($q);
    $s->execute($TrID) || myDBI->dberror($q);
    $s->finish();
    uBill->setRevStatus($form,$TrID,2);
  }
  elsif ( $form->{manager_review} )
  {
#warn qq|updNote: manager_review: $form->{Treatment_TrID_1} \n|;
    my $Status = 3;
    # take care of those that can review their own notes.
    if ( $form->{Treatment_ProvID_1} == $form->{LOGINPROVID} )
    {
      PostUpd->setProvDT($form,$TrID,$form->{TODAY},$curtime);
      $form->{Treatment_ProvOKDate_1} = $form->{TODAY};
      $form->{Treatment_ProvOKTime_1} = $curtime;
#warn qq|updNote: review own notes: $form->{Treatment_TrID_1},$form->{TODAY},$curtime\n|;
    }
    PostUpd->setMgrDT($form,$TrID,$form->{LOGINPROVID},$form->{TODAY},$curtime);
#   Rule for signing notes could be based on LOGINPROVID or Owner of note.
#     both should be a part of the same agency rules.
#   RevStatus:  0 = Provider needed, 1 = Provider needed after changes, 2 = Mgr needed, 3 = Note approved
    if ( !SysAccess->getRule($form,'NoteEdit',$form->{Treatment_ProvID_1}) )   # Rule set for signing notes?
    {
      if ( $form->{Treatment_ProvOKDate_1} ) { $Status = 3; }                  # ready to bill
      else { $Status = 1; }                                                    # need Provider to ok.
#warn qq|PostUpd:updNote: NO RULE: Status=$Status\n|;
    }
    elsif ( $form->{"${inTable}_CHANGED"} )
    {
      # save and set for Provider to look at only if not this same provider.
      if ( $form->{Treatment_ProvID_1} != $form->{LOGINPROVID} )
      {
        # save changes in a log.
        my $ID = DBA->insLog($form,$inTable,'NoteID',$TrID,$inTable . 'Log');

#warn "NOTESIGN RULE AND CHANGED: inTable=${inTable}, ProvID=$form->{Treatment_ProvID_1},LOGINPROVID=$form->{LOGINPROVID}, TrID=$form->{Treatment_TrID_1}\n";
#warn qq|update Treatment set RevStatus=3,ProvID=$form->{Treatment_ProvID_1},ProvOKDate='$form->{Treatment_ProvOKDate_1}',ProvOKTime='$form->{Treatment_ProvOKTime_1}' where TrID=$form->{Treatment_TrID_1};\n|;
#warn qq|delete from ${inTable}Log where LogID=$ID;\n|;
        # add Manager dates to Log
        my $q = qq|update ${inTable}Log set ProvID=?,ProvOKDate=?,ProvOKTime=?,MgrProvID=?,MgrRevDate=?,MgrRevTime=? where LogID=?|;
        my $s = $dbh->prepare($q);
        $s->execute($form->{Treatment_ProvID_1},$form->{Treatment_ProvOKDate_1},$form->{Treatment_ProvOKTime_1},
                    $form->{LOGINPROVID},$form->{TODAY},$curtime,$ID) || myDBI->dberror($q);
        $s->finish();

        # unset Provider approve datetime.
        PostUpd->setProvDT($form,$TrID,'','');
        $Status = 1;
      }
    }
    uBill->setRevStatus($form,$TrID,$Status);
  }
  elsif ( $form->{approve_note} )             # after Manager changes
  {
#warn qq|updNote: approve_note: $form->{Treatment_TrID_1}\n|;
    PostUpd->setProvDT($form,$TrID,$form->{TODAY},$curtime);
    uBill->setRevStatus($form,$TrID,3);
  }
  elsif ( $form->{reject_note} )
  {
#warn qq|PostUpd: updNote: reject_note: $form->{Treatment_TrID_1}\n|;
    PostUpd->setProvDT($form,$TrID,$form->{TODAY},$curtime);
    PostUpd->setMgrDT($form,$TrID,'','');
    uBill->setRevStatus($form,$TrID,2);
  }
  #   as if Provider entered, not Data Entry.
  elsif ( $form->{Treatment_ProvID_1} == $form->{LOGINPROVID}      # Owner of the note
       || $form->{Treatment_Type_1} == 3                           # Electronic note
       || ($rxSC->{InsID} == 100 && $rxSC->{'SCNum'} =~ /^G9/)     # Medicaid or HH Gcode Bundle
        )
  {
#my $kk="${inTable}_CHANGED";
#warn qq|PostUpd: updNote: owner: $form->{Treatment_TrID_1},CHANGED=${kk}=$form->{${kk}}\n|;
    # Owner approves or changes something reset DT.
    if ( $form->{'Treatment_ProvOKDate_1'} eq '' || $form->{"${inTable}_CHANGED"} )
    {
      PostUpd->setProvDT($form,$TrID,$form->{TODAY},$curtime);
      uBill->setRevStatus($form,$TrID,2);
    }
  }
  # if they changed something in the text of the note...
  # not the owner...flag for Provider...because MgrRevDate locks...so it's DataEntry?
  elsif ( $form->{"${inTable}_CHANGED"} )
  {
#warn qq|PostUpd: updNote: else: $form->{Treatment_TrID_1}\n|;
    PostUpd->setProvDT($form,$TrID,'','');
    uBill->setRevStatus($form,$TrID,0);
  }
#warn qq|updNote: END Status=$form->{Treatment_BillStatus_1}\n|;
# this fixes the note since they updated it (possibly for billing)
#   it will only affect Unbillable notes (BillStatus=2)
  uBill->fixUnbillable($form,$TrID);
# set the PrAuthID.
  my $PrAuthID = Inv->setNotePrAuthID($form,$TrID);
  if ( $form->{Treatment_Type_1} == 3 && $form->{Treatment_Path_1} eq '' )      # Electronic Note
  {
     $form->{fwdLINK} = qq|/cgi/bin/mis.cgi?view=NoteUpload.cgi&Client_ClientID=$ClientID&Treatment_TrID=${TrID}&mlt=$form->{mlt}&misLINKS=$form->{misLINKS}|;
     $form->{misPOP} = 1;
  }
  if ( $form->{'AppointmentID'} )
  {
    my $sDelete = $dbh->prepare("delete from Appointments where ID='$form->{'AppointmentID'}'");
    $sDelete->execute() || myDBI->dberror("delete Appointments: $form->{'AppointmentID'}");
    $sDelete->finish();
  }
  #  PRIMARY PROCEDURE codes G8434 G8510 for Health Home Depression Screening...
#warn qq|PostUpd: updNote: check SCNum=$rxSC->{SCNum}\n|;
  if ( $rxSC->{'SCNum'} eq 'G8431'
    || $rxSC->{'SCNum'} eq 'G8432'  
    || $rxSC->{'SCNum'} eq 'G8434'  
    || $rxSC->{'SCNum'} eq 'G8510' )
  {
#warn qq|PostUpd: updNote: update SCNum=$rxSC->{SCNum}, ClientID=${ClientID}, ContLogDate=${ContLogDate}\n|;
    my $sUpdate = $dbh->prepare("update ClientPHQ9 set TrID=? where ClientID=? and TestDate=?");
    $sUpdate->execute($TrID,$ClientID,$ContLogDate) || myDBI->dberror("updNote: ${TrID} ${ClientID} ${ContLogDate}");
    $sUpdate->finish();
    my $sUpdate = $dbh->prepare("update ClientTPHQ9 set TrID=? where ClientID=? and TestDate=?");
    $sUpdate->execute($TrID,$ClientID,$ContLogDate) || myDBI->dberror("updNote: ${TrID} ${ClientID} ${ContLogDate}");
    $sUpdate->finish();
  }
#warn qq|PostUpd: updNote: check BillStatus=$form->{Treatment_BillStatus_1}\n|;
  if ( $form->{'Treatment_BillStatus_1'} !~ /3|4|5/ )              # inprocess/scholar/reconcile
  {
    my $Maladaptive=$form->{'Treatment_Maladaptive_1'};
    my $Interfere=$form->{'Treatment_Interfere_1'};
    my $Sentinel=$form->{'Treatment_Sentinel_1'};
    my $PlayOvercome=$form->{'Treatment_PlayOvercome_1'};
    my $SCID3 = '';
    if ( $Maladaptive || $Interfere || $Sentinel || $PlayOvercome )
    {
#warn qq|PostUpd: updNote: check SCID3=${Maladaptive},${Interfere},${Sentinel},${PlayOvercome}\n|;
      # Selection of any 1 of 4 boxes will ADD-ON 90785 service code to 
      #  PRIMARY PROCEDURE codes 90791, 90792, 90832, 90834, 90837, or 90853.
      if ( $rxSC->{'SCNum'} eq '90791'
        || $rxSC->{'SCNum'} eq '90792'
        || $rxSC->{'SCNum'} eq '90832'
        || $rxSC->{'SCNum'} eq '90834'
        || $rxSC->{'SCNum'} eq '90837'
        || $rxSC->{'SCNum'} eq '90853' )
      {
        my $sxSC = $dbh->prepare("select SCID from xSC where SCNum='90785' and InsID=? and CredID=?");
        $sxSC->execute($rxSC->{'InsID'},$rxSC->{'CredID'}) 
           || myDBI->dberror("set90785: $rxSC->{'TrID'},$rxSC->{'SCID'}");
        ($SCID3) = $sxSC->fetchrow_array;
        $sxSC->finish();
      }
    }
#warn qq|PostUpd: updNote: check SCID3=${SCID3}=$rxSC->{SCNum}=\n|;
    if ( $SCID3 )
    {
      my $sUpdate = $dbh->prepare("update Treatment set SCID3=? where TrID=?");
      $sUpdate->execute($SCID3,$TrID) || myDBI->dberror("set90785: ${SCID3} ${TrID}");
      $sUpdate->finish();
    }
    else
    {
      my $sUpdate = $dbh->prepare("update Treatment set SCID3=NULL where TrID=?");
      $sUpdate->execute($TrID) || myDBI->dberror("set90785: NULL ${TrID}");
      $sUpdate->finish();
    }
    $self->updNoteProblems($form,$ClientID,$TrID,$form->{'NoteProblems'});
    $self->updNoteTrPlanPG($form,$ClientID,$TrID,$form->{'NoteTrPlanPG'});
    $self->updNoteFamilyP($form,$ClientID,$TrID,$form->{'NoteFamilyI'},'FamilyI');
    $self->updNoteFamilyP($form,$ClientID,$TrID,$form->{'NoteFamilyP'},'FamilyP');
    $self->updNoteMeds($form,$ClientID,$TrID);               # these are Active ClientMeds...
    if ( $form->{Treatment_Type_1} == 2 )                    # only Physician notes...
    { $self->updNoteProcedures($form,$ClientID,$TrID); }     # set the DocMeds Procedure...
    my ($code,$msg) = cBill->CheckNote($form,$form->{'Treatment_TrID_1'});
    if ( $code && $msg ne '' )
    {
      my $sUnBill = $dbh->prepare("update Treatment set BillStatus=2, StatusMsg=? where TrID=?");
      $sUnBill->execute($msg,$form->{'Treatment_TrID_1'}) || myDBI->dberror("updNote: set UnBill $form->{Treatment_TrID_1}");
      $sUnBill->finish();
    }
    my ($BilledAmt,$IncAmt,$SchAmt,$AmtDue) = uBill->setBilledAmt($form,$form->{'Treatment_TrID_1'});
  }
  return($result);
}
sub setProvDT
{
  my ($self, $form, $TrID, $date, $time) = @_;
  my $dbh = myDBI->dbconnect($form->{'DBNAME'});
  my $q = $date eq '' ?  qq|update Treatment set ProvOKDate=NULL, ProvOKTime=NULL where TrID=?|
                      : qq|update Treatment set ProvOKDate='${date}', ProvOKTime='${time}' where TrID=?|;
#warn qq|setProvDT: $TrID, date=$date, time=$time \nq=$q\n|;
  my $s = $dbh->prepare($q);
  $s->execute($form->{Treatment_TrID_1}) || myDBI->dberror($q);
  $s->finish();
  return(1);
}
sub setMgrDT
{
  my ($self, $form, $TrID, $mgr, $date, $time) = @_;
  my $dbh = myDBI->dbconnect($form->{'DBNAME'});
  my $q = qq|update Treatment set MgrProvID=?, MgrRevDate=?, MgrRevTime=? where TrID=?|;
  my $s = $dbh->prepare($q);
  $s->execute($mgr,$date,$time,$form->{Treatment_TrID_1}) || myDBI->dberror($q);
  $s->finish();
  return(1);
}
sub updNoteProblems
{
  my ($self,$form,$ClientID,$TrID,$UUIDs) = @_;
  return() unless ( $ClientID );
  return() unless ( $TrID );
#warn qq|updNoteProblems: ClientID=$ClientID, TrID=$TrID, UUIDs=$UUIDs\n|;
  my $dbh = myDBI->dbconnect($form->{'DBNAME'});
  my $sClientProblems = $dbh->prepare("select ClientProblems.*,misICD10.ICD10 from ClientProblems left join okmis_config.misICD10 on misICD10.ID=ClientProblems.UUID where ClientProblems.ClientID=? and ClientProblems.UUID=?");
  my $sLock = $dbh->prepare("update ClientNoteProblems set Locked=1 where ID=?");
# first unlocked everyone...
  my $sUnLock = $dbh->prepare("update ClientNoteProblems set Locked=0 where TrID=?");
  $sUnLock->execute($TrID) || myDBI->dberror("updNoteProblems: UnLock ${TrID}");
  $sUnLock->finish();
  foreach my $UUID ( split(chr(253),$UUIDs) )
  {
    $sClientProblems->execute($ClientID,$UUID);
    my $rClientProblems = $sClientProblems->fetchrow_hashref;
    my $r = ();
    $r->{'ClientID'}=$ClientID;
    $r->{'TrID'}=$TrID;
    $r->{'CreateProvID'}=$form->{'LOGINPROVID'};
    $r->{'CreateDate'}=$form->{'TODAY'};
    $r->{'ChangeProvID'}=$form->{'LOGINPROVID'};
    $r->{'UUID'}=$UUID;
    $r->{'Priority'}=$rClientProblems->{'Priority'};
    $r->{'Active'}=$rClientProblems->{'Active'};
    $r->{'InitiatedDate'}=$rClientProblems->{'InitiatedDate'};
    $r->{'ResolvedDate'}=$rClientProblems->{'ResolvedDate'};
    my $where = qq|TrID='${TrID}' and UUID='${UUID}'|;
#foreach my $f ( sort keys %{$r} ) { warn "updNoteProblems: r-$f=$r->{$f}\n"; }
    my $ID = DBA->doUpdate($form,'ClientNoteProblems',$r,$where);
    $sLock->execute($ID) || myDBI->dberror("updNoteProblems: Lock ${ID}");
  }
  $sClientProblems->finish();
  $sLock->finish();
# delete those left unlocked...
  my $sDelete = $dbh->prepare("delete from ClientNoteProblems where TrID=? and Locked=0");
  $sDelete->execute($TrID) || myDBI->dberror("updNoteProblems: delete ${TrID}");
  $sDelete->finish();
  return(1);
}
sub updNoteTrPlanPG
{
  my ($self,$form,$ClientID,$TrID,$PGIDs) = @_;
  return() unless ( $ClientID );
  return() unless ( $TrID );
#warn qq|updNoteTrPlanPG: ClientID=$ClientID, TrID=$TrID, PGIDs=$PGIDs\n|;
  my $dbh = myDBI->dbconnect($form->{'DBNAME'});
# we lock it now, but unLockTrPlan routine is needed to check all notes for Client/TrPlan
  my $sLock = $dbh->prepare("update ClientNoteTrPlanPG set Locked=1 where ID=?");
# CHECK IF DELETED COMES THRU HERE??
# first unlocked everyone...
  my $sUnLock = $dbh->prepare("update ClientNoteTrPlanPG set Locked=0 where TrID=?");
  $sUnLock->execute($TrID) || myDBI->dberror("updNoteTrPlanPG: UnLock ${TrID}");
  $sUnLock->finish();
  foreach my $PGID ( split(chr(253),$PGIDs) )
  {
    my $r = ();
    $r->{'ClientID'}=$ClientID;
    $r->{'TrID'}=$TrID;
    $r->{'TrPlanPGID'}=$PGID;
    $r->{'CreateProvID'}=$form->{'LOGINPROVID'};
    $r->{'CreateDate'}=$form->{'TODAY'};
    $r->{'ChangeProvID'}=$form->{'LOGINPROVID'};
    my $where = qq|TrID='${TrID}' and TrPlanPGID='${PGID}'|;
#foreach my $f ( sort keys %{$r} ) { warn "updNoteTrPlanPG: r-$f=$r->{$f}\n"; }
    my $ID = DBA->doUpdate($form,'ClientNoteTrPlanPG',$r,$where);
    $sLock->execute($ID) || myDBI->dberror("updNoteTrPlanPG: Lock ${ID}");
  }
  $sLock->finish();
# delete those left unlocked...
  my $sDelete = $dbh->prepare("delete from ClientNoteTrPlanPG where TrID=? and Locked=0");
  $sDelete->execute($TrID) || myDBI->dberror("updNoteTrPlanPG: delete ${TrID}");
  $sDelete->finish();
# not needed here because lock based on Signed TP by PrimaryProvider
  DBA->lockTrPlan($form,'',$TrID);    # double check all PGs are locked for this TrID...
  return(1);
}
sub updNoteFamilyP
{
  my ($self,$form,$ClientID,$TrID,$FPIDs,$table) = @_;
  return() unless ( $ClientID );
  return() unless ( $TrID );
# CHECK IF DELETED COMES THRU HERE??
#foreach my $f ( sort keys %{$form} ) { warn "updNote${table}: form-$f=$form->{$f}\n"; }
#warn qq|updNote${table}: ClientID=$ClientID, TrID=$TrID, FPIDs=$FPIDs\n|;
  my $dbh = myDBI->dbconnect($form->{'DBNAME'});
  my $sClientFamily = $dbh->prepare("select * from ClientFamily where ClientID=? and ID=?");
# we lock it now, but unLockTrPlan routine is needed to check all notes for Client/TrPlan
  my $sLock = $dbh->prepare("update ClientNote${table} set Locked=1 where ID=?");
# first unlocked everyone...
  my $sUnLock = $dbh->prepare("update ClientNote${table} set Locked=0 where TrID=?");
  $sUnLock->execute($TrID) || myDBI->dberror("updNote${table}: UnLock ${TrID}");
  $sUnLock->finish();
  foreach my $FPID ( split(chr(253),$FPIDs) )
  {
    $sClientFamily->execute($ClientID,$FPID);
    my $rClientFamily = $sClientFamily->fetchrow_hashref;
    my $r = ();
    $r->{'ClientID'}=$ClientID;
    $r->{'TrID'}=$TrID;
    $r->{'ClientFamilyID'}=$FPID;
    $r->{'CreateProvID'}=$form->{'LOGINPROVID'};
    $r->{'CreateDate'}=$form->{'TODAY'};
    $r->{'ChangeProvID'}=$form->{'LOGINPROVID'};
    $r->{'ChangeProvID'}=$form->{'LOGINPROVID'};
    $r->{'FName'}=$rClientFamily->{'FName'};
    $r->{'LName'}=$rClientFamily->{'LName'};
    $r->{'Rel'}=$rClientFamily->{'Rel'};
    my $where = qq|TrID='${TrID}' and ClientFamilyID='${FPID}'|;
#foreach my $f ( sort keys %{$r} ) { warn "updNote${table}: r-$f=$r->{$f}\n"; }
    my $ID = DBA->doUpdate($form,"ClientNote${table}",$r,$where);
    $sLock->execute($ID) || myDBI->dberror("updNote${table}: Lock ${ID}");
  }
  $sClientFamily->finish();
  $sLock->finish();
# delete those left unlocked...
  my $sDelete = $dbh->prepare("delete from ClientNote${table} where TrID=? and Locked=0");
  $sDelete->execute($TrID) || myDBI->dberror("updNote${table}: delete ${TrID}");
  $sDelete->finish();
  return(1);
}
sub updNoteMeds
{
  my ($self,$form,$ClientID,$TrID) = @_;
  return() unless ( $ClientID );
  return() unless ( $TrID );
#warn qq|updNoteMeds: ClientID=$ClientID, TrID=$TrID\n|;
  my $dbh = myDBI->dbconnect($form->{'DBNAME'});
  my $sDelete = $dbh->prepare("delete from ClientNoteMeds where TrID=?");
  $sDelete->execute($TrID) || myDBI->dberror("updNoteMeds: delete ClientNoteMeds ${TrID}");
  $sDelete->finish();
  my $sClientMeds = $dbh->prepare("select * from ClientMeds where ClientID=? and Active=1 order by DrugInfo, PrescriptionDate");
  $sClientMeds->execute($ClientID) || myDBI->dberror("updNoteMeds: select ClientMeds ${ClientID}");
  while ( my $rClientMeds = $sClientMeds->fetchrow_hashref )
  {
    my $r = ();
    $r->{'ClientID'}=$ClientID;
    $r->{'TrID'}=$TrID;
    $r->{'CreateProvID'}=$form->{'LOGINPROVID'};
    $r->{'CreateDate'}=$form->{'TODAY'};
    $r->{'ChangeProvID'}=$form->{'LOGINPROVID'};
    $r->{'ClientMedsID'}=$rClientMeds->{'ID'};
#foreach my $f ( sort keys %{$r} ) { warn "updNoteMeds: r-$f=$r->{$f}\n"; }
    my $ID = DBA->doUpdate($form,'ClientNoteMeds',$r);
  }
  $sClientMeds->finish();
  return(1);
}
sub updNoteProcedures      # this sub updates the actual ClientProcedure, not a record pointing to 1.
{
  my ($self,$form,$ClientID,$TrID) = @_;
  return() unless ( $ClientID );
  return() unless ( $TrID );
#foreach my $f ( sort keys %{$form} ) { warn "updNoteProcedures: form-$f=$form->{$f}\n"; }
#warn qq|updNoteProcedures: ClientID=$ClientID, TrID=$TrID\n|;
  my $dbh = myDBI->dbconnect($form->{'DBNAME'});
  my $sProviderControl = $dbh->prepare("select * from ProviderControl where ProvID=?");
  $sProviderControl->execute($form->{'Treatment_ClinicID_1'});
  my $rClinic = $sProviderControl->fetchrow_hashref;
  $sProviderControl->finish();
  my $r = ();
  $r->{'ClientID'}=$ClientID;
  $r->{'TrID'}=$TrID;
  $r->{'CreateProvID'}=$form->{'LOGINPROVID'};
  $r->{'CreateDate'}=$form->{'TODAY'};
  $r->{'ChangeProvID'}=$form->{'LOGINPROVID'};
  $r->{'PerformerNPI'} = $rClinic->{'NPI'};                 # Bill-To Clinic NPI
  $r->{'StartDate'} = $form->{'Treatment_ContLogDate_1'};   # 2011-10-05
  $r->{'EndDate'} = $form->{'Treatment_ContLogDate_1'};     # 2011-10-05
  $r->{'Active'} = 1;
  $r->{'ProcedureID'} = '428191000124101';                  # Documentation of current medications (procedure)
  $r->{'Rejected'} = $form->{'PhysNotes_DocMeds_1'};        # ie: SNOMEDCT_397745006
#foreach my $f ( sort keys %{$r} ) { warn "updNoteProcedures: r-$f=$r->{$f}\n"; }
  my $ID = DBA->doUpdate($form,'ClientProcedures',$r,"ClientID=${ClientID} and TrID=${TrID}");
  return(1);
}
sub updClientVitalSigns
{
  my ($self,$form,$ID) = @_;
  my $dbh = myDBI->dbconnect($form->{'DBNAME'});
#warn qq|updCLientVitalSigns:$ID\n|;
  my $sClientVitalSigns = $dbh->prepare("select * from ClientVitalSigns where ID=?");
  $sClientVitalSigns->execute($ID) || myDBI->dberror("updClientVitalSigns: select ID=${ID}");
  my $rClientVitalSigns = $sClientVitalSigns->fetchrow_hashref;
  $sClientVitalSigns->finish();
  my $BMI = DBA->getBMI($form,$rClientVitalSigns);
  my $BSA = DBA->getBSA($form,$rClientVitalSigns);
#warn qq|updCLientVitalSigns: ID=${ID}, BMI=${BMI}\n|;
  my $sUpdate = $dbh->prepare("update ClientVitalSigns set BMI=?,BSA=? where ID=?");
  $sUpdate->execute($BMI,$BSA,$ID) || myDBI->dberror("updClientVitalSigns: update ID=${ID}, BMI=${BMI}");
  $sUpdate->finish();
  return();
}
############################################################################
sub setPrAuthNum
{
  my ($self,$form,$PrAuthID) = @_;
#warn "KLS ENTER->setPrAuthNum: PrAuthID=$PrAuthID\n";
  return (1) if ( !$PrAuthID );

  my ($PrevPANum,$PANum,$Many) = ('','',0);
  my $dbh = myDBI->dbconnect($form->{'DBNAME'});
  my $s = $dbh->prepare("select * from PrAuthRVU where PrAuthID=${PrAuthID}");
  $s->execute || myDBI->dberror("setPrAuthNum: select PrAuthRVU ${PrAuthID}");
  while ( my $r = $s->fetchrow_hashref )
  {
    if ( $r->{PANum} ne '' )
    {
      $PANum = $r->{PANum};
      $Many = 1 if ( $PANum ne $PrevPANum && $PrevPANum ne '' );
      $PrevPANum = $PANum;
    }
  }
#warn "SET->setPrAuthNum: PrAuthID=$PrAuthID, PANum=$PANum, Many=$Many\n";
  if ( $PANum eq '' )
  {
    $s = $dbh->prepare("update ClientPrAuth set Locked=0 where ID='${PrAuthID}'");
    $s->execute() || myDBI->dberror("setPrAuthNum: unlock ClientPrAuth ${PrAuthID}");
  }
  else
  {
    $PANum = 'MULTIPLE' if ( $Many );
    $s = $dbh->prepare("update ClientPrAuth set Locked=1,PAnumber='${PANum}' where ID='${PrAuthID}'");
    $s->execute() || myDBI->dberror("setPrAuthNum: update ClientPrAuth ${PrAuthID}");
    $s = $dbh->prepare("update ClientPrAuthCDC set Status='Approved',StatusDate='$form->{TODAY}',Fail=NULL,Reason=NULL where ClientPrAuthID='${PrAuthID}'");
    $s->execute() || myDBI->dberror("setPrAuthNum: update ClientPrAuthCDC ${PrAuthID}");
  }
  $s->finish();
  return('');     # return no error message
}
############################################################################
sub updClientTrPlan
{
  my ($self,$form,$TrPlanID) = @_;
#warn qq|updClientTrPlan: WHAT TO DO!!!: TrPlanID=$TrPlanID\n|;
  return();
}
sub updTrPlan
{
  my ($self, $form) = @_;
#warn "KLS ENTER->updTrPlan: =\n";

  my $dbh = myDBI->dbconnect($form->{'DBNAME'});
  if ( $form->{TrPlan_Sign} )
  {
    my $LOGINPROVID = $form->{LOGINPROVID};
    return(0) unless ( $LOGINPROVID );
    my $ClientID = $form->{TrPlan_ClientID_1};
    return(0) unless ( $ClientID );
    my $TrPlanID = $form->{TrPlan_TrPlanID_1};
    return(0) unless ( $TrPlanID );
    my $qTrPlanS = qq|select * from TrPlanS where TrPlanS.ProvID=? and TrPlanS.ClientID=? and TrPlanS.TrPlanID=?|;
#warn qq|qTrPlanS=$qTrPlanS\n${LOGINPROVID},${ClientID},${TrPlanID}|;
    my $sTrPlanS = $dbh->prepare($qTrPlanS);
    $sTrPlanS->execute($LOGINPROVID,$ClientID,$TrPlanID) || myDBI->dberror($qTrPlanS);
    if ( my $rTrPlanS = $sTrPlanS->fetchrow_hashref )
    { warn qq|no signed trplan\n|; }
    else
    {
      my ($s, $m, $h, $day, $mon, $year) = localtime;
      my $curtime = sprintf('%02d:%02d:%02d', $h, $m, $s);
      my $r = ();
      $r->{ClientID} = $form->{TrPlan_ClientID_1};
      $r->{TrPlanID} = $form->{TrPlan_TrPlanID_1};
      $r->{ProvID} = $form->{LOGINPROVID};
      $r->{SignDate} = $form->{TODAY};
      $r->{SignTime} = $curtime;
      $r->{CreateProvID} = $form->{LOGINPROVID};
      $r->{CreateDate} = $form->{TODAY};
      $r->{ChangeProvID} = $form->{LOGINPROVID};
      my $qInsert = DBA->genInsert($form,'TrPlanS',$r);
#warn qq|qInsert=$qInsert\n|;
      my $sInsert = $dbh->prepare($qInsert);
      $sInsert->execute() || myDBI->dberror($qInsert);
      $sInsert->finish();
    }
    $sTrPlanS->finish();
  }
  else { warn qq| NO SIGN TRPLAN\n|; }
  return('');
}
sub updEDocs
{
  my ($self,$form,$table,$ID) = @_;
#warn qq|Check DELETE: $form->{"${table}_DELETE_1"}, $table, $ID\n|;
  if ( $form->{"${table}_DELETE_1"} )
  {
#warn qq|YES DELETE: PATH=$form->{"${table}_Path_1"}\n|;
    my $file = $form->{DOCROOT} . $form->{"${table}_Path_1"};
    if ( -f $file )
    {
      warn qq|DELETE: file=$file\n|;
      unlink($file);
    }
  }
  elsif ( $form->{'DBNAME'} eq 'okmis_mms' && $form->{"${table}_ProvID_1"} == 90 )
  {
warn qq|updEDocs sync: ID=$form->{"${table}_ID_1"}\n|;
    DBUtil->sysfile('syncEDoc',$form->{"${table}_ID_1"},$form->{LOGINID});
  }
#warn qq|updEDocs END: $form->{DBNAME}, ProvID=$form->{"${table}_ProvID_1"}\n|;
  return('');
}
sub updDischarge
{
  my ($self,$form,$inClientID,$inID) = @_;
  my $dbh = myDBI->dbconnect($form->{'DBNAME'});
  my $DischargeID = $inID ? $inID : $form->{'ClientDischarge_ID_1'};
  my $ClientID = $inClientID ? $inClientID : $form->{'ClientDischarge_ClientID_1'};
#warn qq|updDischarge: inID=$inID, ID=$DischargeID, inClientID=$inClientID, ClientID=$ClientID\n|;
# get the default InsID, then match if Intake/Discharge PA
  my $sInsurance = $dbh->prepare("select InsNumID from Insurance where ClientID=? and Insurance.Priority=1 order by InsNumEffDate desc" );
  $sInsurance->execute($ClientID) || myDBI->dberror("updDischarge: select Client Insurance");
  my ($InsuranceID) = $sInsurance->fetchrow_array();
#warn qq|updDischarge: selected-InsuranceID=$InsuranceID\n|;
  $sInsurance->finish();
# find / locate the PrAuth during the Intake period
  my $IntPrAuthID = $form->{'ClientDischarge_IntPrAuthID_1'};
  my $IntDate = $form->{'ClientDischarge_IntDate_1'};
#warn qq|updDischarge: IntPrAuthID=$IntPrAuthID, IntDate=$IntDate\n|;
  my $qPrAuth = qq|select ClientPrAuth.ID,ClientPrAuth.InsuranceID from ClientPrAuth left join ClientPrAuthCDC on ClientPrAuthCDC.ClientPrAuthID=ClientPrAuth.ID left join Insurance on Insurance.InsNumID=ClientPrAuth.InsuranceID where ClientPrAuth.ClientID='${ClientID}' and Insurance.Priority=1 and ClientPrAuth.ExpDate>='${IntDate}' and ClientPrAuthCDC.TransType!=21 order by ClientPrAuth.ID|;
#warn qq|qPrAuth=$qPrAuth\n|;
  my $sPrAuth = $dbh->prepare($qPrAuth);
  $sPrAuth->execute() || myDBI->dberror($qPrAuth);
  if ( my ($PrAuthID,$PAInsuranceID) = $sPrAuth->fetchrow_array )
  {
#warn qq|updDischarge inside1: ID=$DischargeID: set-IntPrAuthID=$PrAuthID\n|;
    $IntPrAuthID = $PrAuthID;
    my $r = (); $r->{ID}=$DischargeID; $r->{IntPrAuthID}=$PrAuthID;
    DBA->doUpdate($form,'ClientDischarge',$r,"ID=$DischargeID");
    $InsuranceID = $PAInsuranceID;
  }
  $sPrAuth->finish();

# find / locate the PrAuth during the Discharge period
  my $DisPrAuthID = $form->{'ClientDischarge_DisPrAuthID_1'};
  my $DisDate = $form->{'ClientDischargeCDC_TransDate_1'};
#warn qq|updDischarge: DisPrAuthID=$DisPrAuthID, DisDate=$DisDate\n|;
  my $qPrAuth = qq|select ClientPrAuth.ID,ClientPrAuth.InsuranceID from ClientPrAuth left join ClientPrAuthCDC on ClientPrAuthCDC.ClientPrAuthID=ClientPrAuth.ID left join Insurance on Insurance.InsNumID=ClientPrAuth.InsuranceID where ClientPrAuth.ClientID='${ClientID}' and Insurance.Priority=1 and ClientPrAuth.EffDate<='${DisDate}' and ClientPrAuthCDC.TransType!=21 and ClientPrAuthCDC.TransType<60 order by ClientPrAuth.ID desc|;
#warn qq|qPrAuth=$qPrAuth\n|;
  my $sPrAuth = $dbh->prepare($qPrAuth);
  $sPrAuth->execute() || myDBI->dberror($qPrAuth);
  if ( my ($PrAuthID,$PAInsuranceID) = $sPrAuth->fetchrow_array )
  {
#warn qq|updDischarge inside2: ID=$DischargeID: set-DisPrAuthID=$PrAuthID\n|;
    $DisPrAuthID = $PrAuthID;
    my $r = (); $r->{ID}=$DischargeID; $r->{DisPrAuthID}=$PrAuthID;
    DBA->doUpdate($form,'ClientDischarge',$r,"ID=$DischargeID");
    $InsuranceID = $PAInsuranceID;
  }
  $sPrAuth->finish();
#warn qq|updDischarge: set-InsuranceID=$InsuranceID\n|;
  my $r = (); $r->{ID}=$DischargeID; $r->{InsuranceID}=$InsuranceID;
  DBA->doUpdate($form,'ClientDischarge',$r,"ID=$DischargeID");
  CDC->setDIS($form,$DischargeID);
  if ( $form->{'CLOSE'} eq $DischargeID )
  {
    my $sUpdCLOSE = $dbh->prepare("update ClientDischargeCDC set Status='Closed',StatusDate='$form->{TODAY}',Fail=NULL where ClientDischargeID='${DischargeID}'");
    $sUpdCLOSE->execute() || myDBI->dberror("updDischarge: CLOSE ${DischargeID}");
    $sUpdCLOSE->finish();
  }
  if ( $form->{'REOPEN'} eq $DischargeID )
  {
    my $sUpdREOPEN = $dbh->prepare("update ClientDischargeCDC set Status='New',StatusDate='$form->{TODAY}' where ClientDischargeID='${DischargeID}'");
    $sUpdREOPEN->execute() || myDBI->dberror("updDischarge: REOPEN ${DischargeID}");
    $sUpdREOPEN->finish();
  }
  return();
}
sub updAppt
{
  my ($self,$form) = @_;
  if ( $form->{'CreateNote'} )
  {
    my $dbh = myDBI->dbconnect($form->{'DBNAME'});
    $qClient = qq|select * from Client where ClientID=?|;
    $sClient = $dbh->prepare($qClient);
    $sClient->execute($form->{'Appointments_ClientID_1'});
    $rClient = $sClient->fetchrow_hashref;
    $form->{'Client_ClientID'} = $form->{'Appointments_ClientID_1'};
    foreach my $f ( sort keys %{$rClient} ) { $form->{"Client_${f}_1"}=$rClient->{$f}; }
    $form->{'AppointmentID'} = $form->{'Appointments_ID_1'};
    $form->{'AppointmentProvID'} = $form->{'Appointments_ProvID_1'};
    $form->{'AppointmentClientID'} = $form->{'Appointments_ClientID_1'};
    $form->{'AppointmentContactDate'} = $form->{'Appointments_ContactDate_1'};
    $form->{'AppointmentBeginTime'} = $form->{'Appointments_BeginTime_1'};
    $form->{'AppointmentNotes'} = $form->{'Appointments_Notes_1'};
    $form->{'MIS_Action'} = 'Note';
    $form->{'Treatment_TrID'} = 'new';
    $sClient->finish();
  }
  return();
}
sub updContracts
{
  my ($self,$form) = @_;
  my $dbh = myDBI->dbconnect($form->{'DBNAME'});
  my $sxInsurance = $dbh->prepare("select * from xInsurance where ID=?");
  $sxInsurance->execute($form->{'Contracts_InsID_1'});
  my $rxInsurance = $sxInsurance->fetchrow_hashref;
  my $InsDescr = $rxInsurance->{'Descr'};
  my $rContracts = ();
  $rContracts->{'ID'} = $form->{'Contracts_ID_1'};
#warn qq|ClearingHouse=$rxInsurance->{'ClearingHouse'}\n|;
#warn qq|BillType=$form->{'Contracts_BillType_1'}\n|;
  if ( $rxInsurance->{'PayID'} eq '' || $rxInsurance->{'ClearingHouse'} eq '' )
  {
    if ( $form->{'Contracts_BillType_1'} eq 'EL' )
    {
      $rContracts->{'BillType'} = 'BH';
      my $ID = DBA->doUpdate($form,'Contracts',$rContracts,"ID='$rContracts->{ID}'");
#foreach my $f ( sort keys %{$rContracts} ) { warn qq|rContracts-${f}=$rContracts->{$f}\n|; }
      DBA->setAlert($form,"Contract not available for Electronic Billing, PayerID or ClearingHouse missing, reset to BH.");
    }
  }
  my $sProvider = $dbh->prepare("select * from Provider where ProvID=?");
  $sProvider->execute($form->{'Contracts_ProvID_1'});
  my $rClinic = $sProvider->fetchrow_hashref;
  my $AgencyID = MgrTree->getAgency($form,$form->{'Contracts_ProvID_1'});
  $sProvider->execute($AgencyID);
  my $rAgency = $sProvider->fetchrow_hashref;
  my $Message = qq|
Insurance Contract Add/Update for:
$rAgency->{Name}
$rClinic->{FName} $rClinic->{LName}
${InsDescr} ($ID)
UseReferring=$rContracts->{'UseReferring'}; UseRendering=$rContracts->{'UseRendering'}; UseSFacility=$rContracts->{'UseSFacility'}; ContractType=$rContracts->{'ContractType'}; ServMeasure=$rContracts->{'ServMeasure'};
|;
  DBUtil->email($form, 'support@okmis.com', 'Add/Update: Insurance Contract', $Message, '', 1);
  $sxInsurance->finish();
  $sProvider->finish();
  return();
}
sub updGDS
{
  my ($self,$form,$table) = @_;
#foreach my $f ( sort keys %{$form} ) { warn "updGDS: form-$f=$form->{$f}\n"; }
  my $ID = $form->{"${table}_ID_1"};
warn qq|Check updGDS: table=${table}, ID=${ID}\n|;
  my $dbh = myDBI->dbconnect($form->{'DBNAME'});
  my $sClientGDS = $dbh->prepare("select * from ${table} where ID=?");
  $sClientGDS->execute($ID);
  if ( my $rClientGDS = $sClientGDS->fetchrow_hashref )
  {
    my $score = 0;
    if ( $table eq 'ClientGDSS' )               # Short Form
    {
      $score++ if ( $rClientGDS->{'q1'} == 0 ); 
      $score++ if ( $rClientGDS->{'q2'} == 1 ); 
      $score++ if ( $rClientGDS->{'q3'} == 1 ); 
      $score++ if ( $rClientGDS->{'q4'} == 1 ); 
      $score++ if ( $rClientGDS->{'q5'} == 0 ); 
      $score++ if ( $rClientGDS->{'q6'} == 1 ); 
      $score++ if ( $rClientGDS->{'q7'} == 0 ); 
      $score++ if ( $rClientGDS->{'q8'} == 1 ); 
      $score++ if ( $rClientGDS->{'q9'} == 1 ); 
      $score++ if ( $rClientGDS->{'q10'} == 1 ); 
      $score++ if ( $rClientGDS->{'q11'} == 0 ); 
      $score++ if ( $rClientGDS->{'q12'} == 1 ); 
      $score++ if ( $rClientGDS->{'q13'} == 0 ); 
      $score++ if ( $rClientGDS->{'q14'} == 1 ); 
      $score++ if ( $rClientGDS->{'q15'} == 1 ); 
    }
    elsif ( $table eq 'ClientGDSL' )            # Long Form
    {
      $score++ if ( $rClientGDS->{'q1'} == 0 ); 
      $score++ if ( $rClientGDS->{'q2'} == 1 ); 
      $score++ if ( $rClientGDS->{'q3'} == 1 ); 
      $score++ if ( $rClientGDS->{'q4'} == 1 ); 
      $score++ if ( $rClientGDS->{'q5'} == 0 ); 
      $score++ if ( $rClientGDS->{'q6'} == 1 ); 
      $score++ if ( $rClientGDS->{'q7'} == 0 ); 
      $score++ if ( $rClientGDS->{'q8'} == 1 ); 
      $score++ if ( $rClientGDS->{'q9'} == 0 ); 
      $score++ if ( $rClientGDS->{'q10'} == 1 ); 
      $score++ if ( $rClientGDS->{'q11'} == 1 ); 
      $score++ if ( $rClientGDS->{'q12'} == 1 ); 
      $score++ if ( $rClientGDS->{'q13'} == 1 ); 
      $score++ if ( $rClientGDS->{'q14'} == 1 ); 
      $score++ if ( $rClientGDS->{'q15'} == 0 ); 
      $score++ if ( $rClientGDS->{'q16'} == 1 ); 
      $score++ if ( $rClientGDS->{'q17'} == 1 ); 
      $score++ if ( $rClientGDS->{'q18'} == 1 ); 
      $score++ if ( $rClientGDS->{'q19'} == 0 ); 
      $score++ if ( $rClientGDS->{'q20'} == 1 ); 
      $score++ if ( $rClientGDS->{'q21'} == 0 ); 
      $score++ if ( $rClientGDS->{'q22'} == 1 ); 
      $score++ if ( $rClientGDS->{'q23'} == 1 ); 
      $score++ if ( $rClientGDS->{'q24'} == 1 ); 
      $score++ if ( $rClientGDS->{'q25'} == 1 ); 
      $score++ if ( $rClientGDS->{'q26'} == 1 );
      $score++ if ( $rClientGDS->{'q27'} == 0 );
      $score++ if ( $rClientGDS->{'q28'} == 1 );
      $score++ if ( $rClientGDS->{'q29'} == 0 );
      $score++ if ( $rClientGDS->{'q30'} == 0 );
    }
warn qq|updGDS: ${table}: YES UPDATE: Score=${score}\n|;
    my $sUpdate = $dbh->prepare("update ${table} set Score=? where ID=?");
    $sUpdate->execute($score,$ID);
    $sUpdate->finish();
  }
  else { warn qq|updGDS: ${table}: ${ID} NOT FOUND!\n|; }
  $sClientGDS->finish();
  return('');
}
sub updSOGS
{
  my ($self,$form) = @_;
#warn qq|Check SOGS: $form->{"SOGS_ID_1"}\n|;
  my $dbh = myDBI->dbconnect($form->{'DBNAME'});
  my $sSOGS = $dbh->prepare("select * from SOGS where ID=?");
  $sSOGS->execute($form->{'SOGS_ID_1'});
  if ( my $rSOGS = $sSOGS->fetchrow_hashref )
  {
    my $cnt = 0;
    $cnt++ if ( $rSOGS->{'A6'} eq 'Most of the time I lost'
             || $rSOGS->{'A6'} eq 'Every time I lost' );
#warn qq|cnt=$cnt\n|;
    $cnt++ if ( $rSOGS->{'A7'} eq 'Yes in the past but not now'
             || $rSOGS->{'A7'} eq 'Yes' );
#warn qq|cnt=$cnt\n|;
    $cnt++ if ( $rSOGS->{'A8'} eq 'Yes less than half the time I lose'
             || $rSOGS->{'A8'} eq 'Yes most of the time' );
#warn qq|cnt=$cnt\n|;
    $cnt++ if ( $rSOGS->{'A9'} eq 'Yes' );
#warn qq|cnt=$cnt\n|;
    $cnt++ if ( $rSOGS->{'A10'} eq 'Yes' );
#warn qq|cnt=$cnt\n|;
    $cnt++ if ( $rSOGS->{'A11'} eq 'Yes' );
#warn qq|cnt=$cnt\n|;
    $cnt++ if ( $rSOGS->{'A12'} eq 'Yes' );
#warn qq|cnt=$cnt\n|;
    $cnt++ if ( $rSOGS->{'A13'} eq 'Yes' );
#warn qq|cnt=$cnt\n|;
    $cnt++ if ( $rSOGS->{'A15'} eq 'Yes' );
#warn qq|cnt=$cnt\n|;
    $cnt++ if ( $rSOGS->{'A16'} eq 'Yes' );
#warn qq|cnt=$cnt\n|;
    $cnt++ if ( $rSOGS->{'A17'} eq 'Yes' );
#warn qq|cnt=$cnt\n|;
    $cnt++ if ( $rSOGS->{'A18a'} eq 'Yes' );
#warn qq|cnt=$cnt\n|;
    $cnt++ if ( $rSOGS->{'A18b'} eq 'Yes' );
#warn qq|cnt=$cnt\n|;
    $cnt++ if ( $rSOGS->{'A18c'} eq 'Yes' );
#warn qq|cnt=$cnt\n|;
    $cnt++ if ( $rSOGS->{'A18d'} eq 'Yes' );
#warn qq|cnt=$cnt\n|;
    $cnt++ if ( $rSOGS->{'A18e'} eq 'Yes' );
#warn qq|cnt=$cnt\n|;
    $cnt++ if ( $rSOGS->{'A18f'} eq 'Yes' );
#warn qq|cnt=$cnt\n|;
    $cnt++ if ( $rSOGS->{'A18g'} eq 'Yes' );
#warn qq|cnt=$cnt\n|;
    $cnt++ if ( $rSOGS->{'A18h'} eq 'Yes' );
#warn qq|cnt=$cnt\n|;
    $cnt++ if ( $rSOGS->{'A18i'} eq 'Yes' );
#warn qq|updSOGS: YES UPDATE: TotalScore=$cnt\n|;
    my $sUpdate = $dbh->prepare("update SOGS set TotalScore=? where ID=?");
    $sUpdate->execute($cnt,$form->{'SOGS_ID_1'});
    $sUpdate->finish();
  }
  else { warn qq|updSOGS: NOT FOUND.\n|; }
  $sSOGS->finish();
  return('');
}
sub updSOGSGSI
{
  my ($self,$form) = @_;
#warn qq|Check SOGSGSI: $form->{"SOGSGSI_ID_1"}\n|;
  my $dbh = myDBI->dbconnect($form->{'DBNAME'});
  my $sSOGSGSI = $dbh->prepare("select * from SOGSGSI where ID=?");
  $sSOGSGSI->execute($form->{'SOGSGSI_ID_1'});
  if ( my $rSOGSGSI = $sSOGSGSI->fetchrow_hashref )
  {
    my $TotalLost=$rSOGSGSI->{'A7'}+$rSOGSGSI->{'A8'}+$rSOGSGSI->{'A9'}+$rSOGSGSI->{'A10'}+$rSOGSGSI->{'A11'}+$rSOGSGSI->{'A12'}+$rSOGSGSI->{'A13'};
    my $AvgLost=$TotalLost/7;
    my $TotalPast=$rSOGSGSI->{'G37aM'}+$rSOGSGSI->{'G37bM'}+$rSOGSGSI->{'G37cM'}+$rSOGSGSI->{'G37dM'}+$rSOGSGSI->{'G37eM'}+$rSOGSGSI->{'G37fM'}+$rSOGSGSI->{'G37gM'}+$rSOGSGSI->{'G37hM'}+$rSOGSGSI->{'G37hM'};
    my $AvgPast=$TotalPast/9;
#warn qq|updSOGSGSI: YES UPDATE: TotalLost=$TotalLost, TotalPast=$TotalPast\n|;
    my $sUpdate = $dbh->prepare("update SOGSGSI set TotalLost=?,AvgLost=?,TotalPast=?,AvgPast=? where ID=?");
    $sUpdate->execute($TotalLost,$AvgLost,$TotalPast,$AvgPast,$form->{'SOGSGSI_ID_1'});
    $sUpdate->finish();
  }
  else { warn qq|updSOGSGSI: NOT FOUND.\n|; }
  $sSOGSGSI->finish();
  return('');
}
sub renumClientProblems
{
  my ($self,$form,$ClientID) = @_;
#warn qq|renumClientProblems : ${ClientID}\n|;
  my $dbh = myDBI->dbconnect($form->{'DBNAME'});
  my $num = 10;
  my $sUpdate = $dbh->prepare("update ClientProblems set Priority=? where ID=?");
  my $sClientProblems = $dbh->prepare("select * from ClientProblems where ClientID=? order by Priority");
  $sClientProblems->execute($ClientID);
  while ( my $rClientProblems = $sClientProblems->fetchrow_hashref )
  {
#warn qq|renumClientProblems: ID=$rClientProblems->{'ID'}, Priority=$rClientProblems->{'Priority'}, num=$num\n|;
    $sUpdate->execute($num,$rClientProblems->{'ID'});
    $num+=10;
  }
  $sClientProblems->finish();
  $sUpdate->finish();
  return();
}
sub renumClientTrPlanPG
{
  my ($self,$form,$TrPlanID) = @_;
  my $dbh = myDBI->dbconnect($form->{'DBNAME'});
  my $num = 10;
  my $sUpdate = $dbh->prepare("update ClientTrPlanPG set Priority=? where ID=?");
  my $sClientTrPlanPG = $dbh->prepare("select * from ClientTrPlanPG where TrPlanID=? order by Priority");
  $sClientTrPlanPG->execute($TrPlanID);
  while ( my $rClientTrPlanPG = $sClientTrPlanPG->fetchrow_hashref )
  {
#warn qq|renumClientTrPlanPG: ID=$rClientTrPlanPG->{'ID'}, Priority=$rClientTrPlanPG->{'Priority'}, num=$num\n|;
    $sUpdate->execute($num,$rClientTrPlanPG->{'ID'});
    $num+=10;
  }
  $sClientTrPlanPG->finish();
  $sUpdate->finish();
  return();
}
sub renumClientTrPlanOBJ
{
  my ($self,$form,$TrPlanPGID) = @_;
  my $dbh = myDBI->dbconnect($form->{'DBNAME'});
  my $num = 10;
  my $sUpdate = $dbh->prepare("update ClientTrPlanOBJ set Priority=? where ID=?");
  my $sClientTrPlanOBJ = $dbh->prepare("select * from ClientTrPlanOBJ where TrPlanPGID=? order by Priority");
  $sClientTrPlanOBJ->execute($TrPlanPGID);
  while ( my $rClientTrPlanOBJ = $sClientTrPlanOBJ->fetchrow_hashref )
  {
#warn qq|renumClientTrPlanOBJ: ID=$rClientTrPlanOBJ->{'ID'}, Priority=$rClientTrPlanOBJ->{'Priority'}, num=$num\n|;
    $sUpdate->execute($num,$rClientTrPlanOBJ->{'ID'});
    $num+=10;
  }
  $sClientTrPlanOBJ->finish();
  $sUpdate->finish();
  return();
}
sub renumClientFamilyProblems
{
  my ($self,$form,$ClientFamilyID) = @_;
#warn qq|renumClientFamilyProblems : ${ClientFamilyID}\n|;
  my $dbh = myDBI->dbconnect($form->{'DBNAME'});
  my $num = 10;
  my $sUpdate = $dbh->prepare("update ClientFamilyProblems set Priority=? where ID=?");
  my $sClientFamilyProblems = $dbh->prepare("select * from ClientFamilyProblems where ClientFamilyID=? order by Priority");
  $sClientFamilyProblems->execute($ClientFamilyID);
  while ( my $rClientFamilyProblems = $sClientFamilyProblems->fetchrow_hashref )
  {
#warn qq|renumClientFamilyProblems: ID=$rClientFamilyProblems->{'ID'}, Priority=$rClientFamilyProblems->{'Priority'}, num=$num\n|;
    $sUpdate->execute($num,$rClientFamilyProblems->{'ID'});
    $num+=10;
  }
  $sClientFamilyProblems->finish();
  $sUpdate->finish();
  return();
}
sub renumProviderCDAparms
{
  my ($self,$form,$ProvID) = @_;
#warn qq|renumProviderCDAparms : ${ProvID}\n|;
  my $dbh = myDBI->dbconnect($form->{'DBNAME'});
  my $num = 10;
  my $sUpdate = $dbh->prepare("update ProviderCDAparms set Priority=? where ID=?");
  my $sProviderCDAparms = $dbh->prepare("select * from ProviderCDAparms where ProvID=? order by Priority");
  $sProviderCDAparms->execute($ProvID);
  while ( my $rProviderCDAparms = $sProviderCDAparms->fetchrow_hashref )
  {
#warn qq|renumProviderCDAparms: ID=$rProviderCDAparms->{'ID'}, Priority=$rProviderCDAparms->{'Priority'}, num=$num\n|;
    $sUpdate->execute($num,$rProviderCDAparms->{'ID'});
    $num+=10;
  }
  $sProviderCDAparms->finish();
  $sUpdate->finish();
  return();
}
sub updDeviceInfo
{
  my ($self,$form) = @_;
#foreach my $f ( sort keys %{$form} ) { warn "updDeviceInfo: form-$f=$form->{$f}\n"; }
#my $udi = "=/W4146EB0010T0475=,000025=A99971312345600=>014032=%7D013032&,1000000000000XYZ123";
  my $rudi = ();
  my $udi = $form->{'ClientProcedures_udi_1'};
#warn qq|udi: ${udi}\n|;
  my $encoded_udi = uri_escape($udi);
#warn qq|encoded_udi: ${encoded_udi}\n|;
  my $url = "https://accessgudid.nlm.nih.gov/api/v1/parse_udi.json?udi=${encoded_udi}";
#warn qq|url1: ${url}\n|;
  my $jsonData = `curl "${url}" 2>/dev/null`;
  if ( $jsonData eq '' )
  {
    $rudi->{'di'} = 'none'; 
    $rudi->{'devicePublishDate'} = '';
    $rudi->{'catalogNumber'} = '';
    $rudi->{'deviceHCTP'} = '';
    $rudi->{'gmdnPTName'} = '';
    $rudi->{'gmdnPTDefinition'} = '';
    $rudi->{'brandName'} = '';
    $rudi->{'versionModelNumber'} = '';
    $rudi->{'companyName'} = '';
    $rudi->{'MRISafetyStatus'} = '';
    $rudi->{'labeledContainsNRL'} = '';
    $rudi->{'labeledNoNRL'} = '';
    $rudi->{'error'} = "EMPTY data string on lookup for: ${udi}."; 
    DBA->setAlert($form,"EMPTY data string on lookup for:\n${udi}.");
#foreach my $f ( sort keys %{$rudi} ) { warn "url1: $f=$rudi->{$f}\n"; }
    my $NEWID = DBA->doUpdate($form,'ClientProcedures',$rudi,"ID=$form->{'ClientProcedures_ID_1'}");
    return();
  }
#warn qq|jsonData1: ${jsonData}\n|;
  my $json = JSON->new->allow_nonref;
  $rudi = $json->decode( $jsonData );
#foreach my $f ( sort keys %{$rudi} ) { warn "rudi1: $f=$rudi->{$f}\n"; }
  my $url = "https://accessgudid.nlm.nih.gov/api/v1/devices/lookup.json?di=$rudi->{di}";
#warn qq|url2: ${url}\n|;
  my $jsonData = `curl "${url}" 2>/dev/null`;
#warn qq|jsonData2: ${jsonData}\n|;
  if ( $jsonData eq '' )
  {
    $rudi->{'di'} = 'none'; 
    $rudi->{'devicePublishDate'} = '';
    $rudi->{'catalogNumber'} = '';
    $rudi->{'deviceHCTP'} = '';
    $rudi->{'gmdnPTName'} = '';
    $rudi->{'gmdnPTDefinition'} = '';
    $rudi->{'brandName'} = '';
    $rudi->{'versionModelNumber'} = '';
    $rudi->{'companyName'} = '';
    $rudi->{'MRISafetyStatus'} = '';
    $rudi->{'labeledContainsNRL'} = '';
    $rudi->{'labeledNoNRL'} = '';
    $rudi->{'error'} = "EMPTY data string on lookup for DEVICEID: ${di}."; 
    DBA->setAlert($form,"EMPTY data string on lookup for DEVICEID:\n${di}.");
#foreach my $f ( sort keys %{$rudi} ) { warn "url2: $f=$rudi->{$f}\n"; }
    my $NEWID = DBA->doUpdate($form,'ClientProcedures',$rudi,"ID=$form->{'ClientProcedures_ID_1'}");
    return();
  }
  my $rparm = $json->decode( $jsonData );
foreach my $f ( sort keys %{$rparm} ) { warn "rparm: $f=$rparm->{$f}\n"; }
foreach my $f ( sort keys %{$rparm->{'gudid'}} ) { warn "rparm gudid: $f=$rparm->{'gudid'}->{$f}\n"; }
foreach my $f ( sort keys %{ $rparm->{'gudid'}->{'device'} } ) { warn "rparm: $f=$rparm->{'gudid'}->{'device'}->{$f}\n"; }
foreach my $f ( sort keys %{ $rparm->{'gudid'}->{'device'}->{'gmdnTerms'}->{'gmdn'} } ) { warn "rparm gmdnTerms-gmdn: $f=$rparm->{'gudid'}->{'device'}->{'gmdnTerms'}->{'gmdn'}->{$f}\n"; }
foreach my $f ( sort keys %{ $rparm->{'gudid'}->{'device'}->{'sterilization'} } ) { warn "rparm sterilization: $f=$rparm->{'gudid'}->{'device'}->{'sterilization'}->{$f}\n"; }
  $rudi->{'error'} = $rparm->{'error'};
  $rudi->{'devicePublishDate'} = $rparm->{'gudid'}->{'device'}->{'devicePublishDate'};
  $rudi->{'catalogNumber'} = $rparm->{'gudid'}->{'device'}->{'catalogNumber'};
  $rudi->{'deviceHCTP'} = $rparm->{'gudid'}->{'device'}->{'deviceHCTP'};
  $rudi->{'gmdnPTName'} = $rparm->{'gudid'}->{'device'}->{'gmdnTerms'}->{'gmdn'}->{'gmdnPTName'};
  $rudi->{'gmdnPTDefinition'} = $rparm->{'gudid'}->{'device'}->{'gmdnTerms'}->{'gmdn'}->{'gmdnPTDefinition'};
  $rudi->{'brandName'} = $rparm->{'gudid'}->{'device'}->{'brandName'};
  $rudi->{'versionModelNumber'} = $rparm->{'gudid'}->{'device'}->{'versionModelNumber'};
  $rudi->{'companyName'} = $rparm->{'gudid'}->{'device'}->{'companyName'};
  $rudi->{'MRISafetyStatus'} = $rparm->{'gudid'}->{'device'}->{'MRISafetyStatus'};
  $rudi->{'labeledContainsNRL'} = $rparm->{'gudid'}->{'device'}->{'labeledContainsNRL'};
  $rudi->{'labeledNoNRL'} = $rparm->{'gudid'}->{'device'}->{'labeledNoNRL'};
  delete $rudi->{'udi'};     # returned udi is shorter than requested so DON'T update??
foreach my $f ( sort keys %{$rudi} ) { warn "rudi2: $f=$rudi->{$f}\n"; }
  if ( $rudi->{'error'} eq '' )
  { $rudi->{'error'} = ''; }                # make sure we update error to NULL
  else
  { DBA->setAlert($form,"error:\n$rudi->{error}."); $rudi->{'di'} = 'none' if $rudi->{'di'} eq ''; }
  my $NEWID = DBA->doUpdate($form,'ClientProcedures',$rudi,"ID=$form->{'ClientProcedures_ID_1'}");
  return();
}
sub setClientRuleAlerts
{
  my ($self,$form,$ClientID,$ForProvID) = @_;
  return() unless ( SysAccess->chkPriv($form,'CDSAlerts',$ForProvID) );
  my @ruleids=();
#warn qq|setClientRuleAlerts: ${ClientID}/${ForProvID}\n|;
  my $ProvID = $ForProvID ? $ForProvID : $form->{LOGINPROVID};
#warn qq|setClientRuleAlerts: ProvID=${ProvID}\n|;
  my $dbh = myDBI->dbconnect($form->{'DBNAME'});
  my $sDelete = $dbh->prepare("delete from ClientRuleAlerts where ClientID='${ClientID}'");
  $sDelete->execute() || myDBI->dberror("setClientRuleAlerts: delete ClientRuleAlerts ${ClientID}=${ClientID}");
  $sDelete->finish();
  my $sInsert = $dbh->prepare("insert into ClientRuleAlerts (ClientID,RuleID,ChangeProvID) values (?,?,?)");
  my $sCDSrules = $dbh->prepare("select * from CDSrules where IsEnabled=1");
  $sCDSrules->execute() || myDBI->dberror("setClientRuleAlerts: select:");
  while ( my $rCDSrules = $sCDSrules->fetchrow_hashref )
  {
    (my $sql = $rCDSrules->{'CommandText'}) =~ s/\@PatientId/$ClientID/g;
#warn qq|setClientRuleAlerts: sql=${sql}\n|;
    my $s = $dbh->prepare($sql);
    $s->execute() || myDBI->dberror("setClientRuleAlerts: ${sql}:");
    my $r = $s->fetchrow_hashref;
    my $cnt = $s->rows;
#warn qq|setClientRuleAlerts: Name=$rCDSrules->{'Name'}, cnt=${cnt}\n|;
    $s->finish();
    if ( $cnt )
    {
      my $RuleID = $rCDSrules->{'RuleID'};
      $sInsert->execute($ClientID,$RuleID,$ProvID)
        || myDBI->dberror("setClientRuleAlerts: insert ClientRuleAlerts ${ClientID}/${RuleID}");
      push(@ruleids,$RuleID);
    }
  }
  $sInsert->finish();
  $sCDSrules->finish();
#warn qq|setClientRuleAlerts: @ruleids\n|;
  return();
}
sub updCronJob
{
  my ($self,$form,$ID) = @_;
warn qq|updCronJob: DELETE=$form->{"ProviderJobs_DELETE_1"}, ID=${ID}\n|;
#foreach my $f ( sort keys %{$form} ) { warn "updCronJob: form-$f=$form->{$f}\n"; }
##crontab -l -u okmms | grep "genCCDAs DBNAME=okmms_dev\\\&ID=2"
  my ($user,$acct) = split('_',$form->{'DBNAME'},2);
  my $BIN = myConfig->cfg('BIN');
# 1st remove the job from the crontab...
  my $ID = $form->{'ProviderJobs_ID_1'};
  my $jobname = DBA->getxref($form,'xCronJobs',$form->{'ProviderJobs_Command_1'},'Descr');
  my $job = $jobname.' DBNAME='.$form->{DBNAME}."\\\\\\\&ID=".$ID;
warn qq|Remove Job: job=${job}\n|;
  my $outfile = qq|/home/${user}/logs/${jobname}.$form->{'DBNAME'}.${ID}.cronout|;
warn qq|outfile=${outfile}\n|;
  my $delcron = qq|crontab -l |.'|'.qq| grep -v "${job}" > ${outfile} 2>&1|;
warn qq|Cron Command: delcron=${delcron}\n|;
warn "system: ${delcron} | crontab -";
  my $delcode = system("${delcron} | crontab -");
warn qq|delcode=${delcode}\n|;
  unless ( $form->{"ProviderJobs_DELETE_1"} )      # add it back...
  {
    my ($hrs,$min,$sec) = split(':',$form->{'ProviderJobs_CronTime_1'},3);
    my $dom = $form->{'ProviderJobs_CronDay_1'} eq '' ? '*' : $form->{'ProviderJobs_CronDay_1'};
    my $month = $form->{'ProviderJobs_CronMonth_1'} eq '' ? '*' : $form->{'ProviderJobs_CronMonth_1'};
    my $week = $form->{'ProviderJobs_CronWeek_1'} eq '' ? '*' : $form->{'ProviderJobs_CronWeek_1'};
    my $addcron = qq|(crontab -l; echo "${min} ${hrs} ${dom} ${month} ${week} ${BIN}/${jobname} DBNAME=$form->{'DBNAME'}\\&ID=${ID} >> ${outfile} 2>&1")|;
warn qq|addcron=${addcron}\n|;
   my $addcode = system("${addcron} | crontab -");
warn qq|addcode=${addcode}\n|;
  }
warn qq|updCronJob: END: \n|;
  return('');
}
sub setDepressionTrID
{
  my ($self,$form,$table) = @_;
  my $dbh = myDBI->dbconnect($form->{'DBNAME'});
  my $id = $table.'_ID_1';
  my $ID = $form->{$id};
#foreach my $f ( sort keys %{$form} ) { warn "setDepressionTrID: form-$f=$form->{$f}\n"; }
#warn qq|updDepressionTrID: ${table}, ${ID}\n|;
  my $sPHQ9 = $dbh->prepare("select * from ${table} where ID=?");
  $sPHQ9->execute($ID) || myDBI->dberror("setDepressionTrID: select ID=${ID}");
  if ( my $rPHQ9 = $sPHQ9->fetchrow_hashref )
  {
    my $ClientID = $rPHQ9->{'ClientID'};
    my $ContDate = $rPHQ9->{'TestDate'};
#warn qq|updDepressionTrID: ${ClientID}, ${ContDate}\n|;
    my $sTreatment = $dbh->prepare("select * from Treatment left join xSC on xSC.SCID=Treatment.SCID where Treatment.ClientID=? and ContLogDate=? and (SCNum='G8431' or SCNum='G8432' or SCNum='G8434' or SCNum='G8510')");
    $sTreatment->execute($ClientID,$ContDate) || myDBI->dberror("updTreatment: select ${ClientID}/${ContDate}");
    if ( my $rTreatment = $sTreatment->fetchrow_hashref )
    {
#warn qq|setDepressionTrID: TrID=$rTreatment->{TrID}\n|;
      my $sUpdate = $dbh->prepare("update ${table} set TrID=? where ID=?");
      $sUpdate->execute($TrID,$ID) || myDBI->dberror("setDepressionTrID: update ID=${ID}, TrID=${TrID}");
      $sUpdate->finish();
    }
    $sTreatment->finish();
  }
  $sPHQ9->finish();
  return();
}
sub dupxTable
{
  my ($self,$form) = @_;
warn qq|\n\nENTER dupxTable: \n|;
foreach my $f ( sort keys %{$form} ) { warn "dupxTable: form-$f=$form->{$f}\n"; }
  my $TableID = $form->{'OrgTableID'};
  my $NewTable = $form->{'NewTable'};
  my $NewDescr = $form->{'NewDescription'};
  return('Missing TableID!') if ( $TableID eq '' );

  my $dbh = myDBI->dbconnect($form->{'DBNAME'});
  my $cdbh = myDBI->dbconnect('okmis_config');
  my $sxTables = $cdbh->prepare("select * from xTables where ID=?");
  $sxTables->execute($TableID) || myDBI->dberror("dupxTable: select xTables ${TableID}!");
  if ( my $rxTables = $sxTables->fetchrow_hashref )
  {
    my $r = $rxTables;
    $r->{'ID'} = '';
    $r->{'CreateProvID'} = '';
    $r->{'CreateDate'} = '';
    $r->{'ChangeProvID'} = '';
    $r->{'theTable'} = $NewTable;
    $r->{'Descr'} = $NewDescr;
    $r->{'Active'} = 1;
    my $qInsert = DBA->genInsert($form,'xTables',$r);
warn qq|qInsert=$qInsert\n|;
    my $sInsert = $cdbh->prepare($qInsert);
    $sInsert->execute() || myDBI->dberror($qInsert);
    my $NEWID = $sInsert->{'mysql_insertid'};
    $sInsert->finish();
foreach my $f ( sort keys %{$r} ) { warn "dupxTable: r-$f=$r->{$f}\n"; }
    my $sxTableFields = $cdbh->prepare("select * from xTableFields where TableID=?");
warn qq|dupxTable: TableID=${TableID}\n|;
    $sxTableFields->execute($TableID) || myDBI->dberror("dupxTable: select xTableFields ${TableID}");
    my $cnt = $sxTableFields->rows;
warn qq|dupxTable: cnt=${cnt}\n|;
    while ( my $rxTableFields = $sxTableFields->fetchrow_hashref )
    {
warn qq|dupxTable: FID=$rxTableFields->{'ID'}\n|;
      my $r = $rxTableFields;
      $r->{'ID'} = '';
      $r->{'CreateProvID'} = '';
      $r->{'CreateDate'} = '';
      $r->{'ChangeProvID'} = '';
      $r->{'TableID'} = $NEWID;
      my $qInsert = DBA->genInsert($form,'xTableFields',$r);
warn qq|qInsert=$qInsert\n|;
      my $sInsert = $cdbh->prepare($qInsert);
      $sInsert->execute() || myDBI->dberror($qInsert);
      $sInsert->finish();
    }
    $sxTableFields->finish();
  }
  $sxTables->finish();
  return();
}
sub reseqxTable
{
  my ($self,$form) = @_;
warn qq|\n\nENTER reseqxTable: \n|;
foreach my $f ( sort keys %{$form} ) { warn "reseqxTable: form-$f=$form->{$f}\n"; }
  my $TableID = $form->{'xTables_ID_1'};
  my $cdbh = myDBI->dbconnect('okmis_config');
  my $seq = 0;
  my $uxTableFields=$cdbh->prepare("update xTableFields set theSeq=? where ID=?");
  my $sxTableFields = $cdbh->prepare("select * from xTableFields where TableID=? order by theSeq");
  $sxTableFields->execute($TableID);
  while ( my $rxTableFields = $sxTableFields->fetchrow_hashref )
  {
#warn qq| update: ${seq}:$rxTableFields->{theField}: $rxTableFields->{ID}\n|;
    $uxTableFields->execute($seq,$rxTableFields->{ID}) || $form->dberror("FAILED: $rxTableFields->{ID}: update");
    $seq++;
  }
  $uxTableFields->finish();
  $sxTableFields->finish();
  return();
}
sub addxTableQues
{
  my ($self,$form) = @_;
warn qq|\n\nENTER addxTableQues: \n|;
foreach my $f ( sort keys %{$form} ) { warn "addxTableQues: form-$f=$form->{$f}\n"; }
  my $TableID = $form->{'xTables_ID_1'};
  my $NewQuestions = $form->{'NewQuestions'};
warn qq|addxTableQues: NewQuestions=${NewQuestions}\n|;
  my $cdbh = myDBI->dbconnect('okmis_config');
  my $seq = 0; 
  my $v = "'0|1'";
  my $d = "'absent|present'";
  my $theArgs = qq|'print-descriptors'|;
  foreach my $ques ( split("\n",$NewQuestions) )
  {
    $ques =~ s/\r//g;
    $ques =~ s/\n//g;
    $ques =~ s/\t//g;
warn qq|addxTableQues: q=${q}\n|;
    $seq++;
    my $q = qq|INSERT INTO `xTableFields` (`ID`, `CreateProvID`, `CreateDate`, `ChangeProvID`, `ChangeDate`, `FormID`, `Locked`, `TableID`, `theField`, `theSeq`, `agent`, `theType`, `theText`, `thePreText`, `thePostText`, `theValues`, `descriptors`, `onchange`, `colspan`, `theSize`, `theStyle`, `theArgs`) VALUES (NULL,NULL,'$form->{'TODAY'}',NULL,NULL,NULL,NULL,${TableID},'q${seq}',${seq},'0','radio','${ques}',NULL,NULL,${v},${d},NULL,'3',NULL,NULL,${theArgs})|;
    my $sxTableFields = $cdbh->prepare($q);
    $sxTableFields->execute();
    $sxTableFields->finish();
    $theArgs = 'NULL';
  }
  return();
}
############################################################################
1;
