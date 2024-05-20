$qFindTrans = qq|select * from NoteTrans where ClientID=? and ContDate=? and SCNum=? order by ID desc|;
$sFindTrans = $dbh->prepare($qFindTrans);
$qFindNote = qq|select * from Treatment left join xSC on xSC.SCID=Treatment.SCID left join xInsurance on xInsurance.ID=xSC.InsID where ClientID=? and Treatment.ContLogDate=? and xSC.SCNum=? and xInsurance.InsCode=?|;
$sFindNote = $dbh->prepare($qFindNote);






$form->complete();
exit;
################################################################
sub setTrans
{
  my ($self,$ID,$ClientID,$ContDate,$SCNum,$InsCode) = @_;
  my $rNoteTrans = ();
  return() unless ( $ID );
# if it begins with a 'T'? strip 'T' off (ie: from 853 REF*6R*Txxxxxx)
  my $TransID = substr($ID,0,1) eq 'T' ? substr($ID,1) : $ID;
  my $qSelTrans="select * from NoteTrans where ID=?";
  my $sSelTrans=$dbh->prepare($qSelTrans);
  $sSelTrans->execute($TransID) || $form->dberror($qSelTrans);
  if ( my $r = $sSelTrans->fetchrow_hashref ) 
  { $rNoteTrans = $r; }
  elsif ( $ClientID ne '' && $ContDate ne '' && $SCNum ne '' )
  {
    my $qFindURTrans = qq|select * from NoteTrans where ClientID=? and ContDate=? and SCNum=? and RecDate is null order by ID desc|;
    my $sFindURTrans = $dbh->prepare($qFindURTrans);
    $sFindURTrans->execute($ClientID,$ContDate,$SCNum) || $form->dberror($qFindURTrans);
    if ( my $r = $sFindURTrans->fetchrow_hashref )
    { $rNoteTrans = $r; }
    else
    {
      $sFindTrans->execute($ClientID,$ContDate,$SCNum) || $form->dberror($qFindTrans);
      if ( my $r = $sFindTrans->fetchrow_hashref )
      { $rNoteTrans = $r; }
      else
      {
        $sFindTrans->finish();
        $sFindNote->execute($ClientID,$ContDate,$SCNum,$InsCode) || $form->dberror($qFindNote);
        if ( my $r = $sFindNote->fetchrow_hashref )
        { 
          $rNoteTrans->{TrID} = $r->{TrID};
          $rNoteTrans->{ClientID} = $r->{ClientID};
          $rNoteTrans->{ContDate} = $r->{ContLogDate};
          $rNoteTrans->{BillDate} = $r->{BillDate};
          $rNoteTrans->{SCID} = $r->{SCID};
          $rNoteTrans->{SCNum} = $r->{SCNum};
          $rNoteTrans->{Units} = $SVC->{UnitsBilled};
          $rNoteTrans->{BillAmt} = $SVC->{Billed};         # ok, first Trans
          $rNoteTrans->{InsCode} = $CLP->{InsCode};
          $rNoteTrans->{RefID} = ${TheCheckNumber};
          $rNoteTrans->{RecDate} = ${TransDate};
          $rNoteTrans->{PaidAmt} = $SVC->{Paid};
          $rNoteTrans->{DenCode} = $SVC->{DenCode};
          $rNoteTrans->{ReasonCode} = "$SVC->{ReasonCode} $CLP->{ReasonCode}";
          $rNoteTrans->{Code} = 'ER-N';
          $rNoteTrans->{ICN} = $CLP->{PayerCN};
          $rNoteTrans->{SRC} = 'ER';
        }
        $sFindNote->finish();
      }
    }
    $sFindURTrans->finish();
  }
  $sSelTrans->finish();
  return($rNoteTrans);
}
