#!/usr/bin/perl
use lib '/var/www/okmis/src/lib';
use DBI;
use DBForm;
use login;
use DBA;
use DBUtil;
############################################################################
my $form = DBForm->parse();
my $xml  = '';

#foreach my $f ( sort keys %{$form} ) { warn ": form-$f=$form->{$f}\n"; }
#warn qq|validateNote: method=$form->{method}\n|;
if ( $form->{method} eq 'vNote' ) {
    my $target = $form->{'target'};
    my $value  = $form->{'value'};

    #warn qq|vNote: target=$target,value=$value\n|;
    my $ProvID   = $form->{'p'};
    my $ClientID = $form->{'c'};
    my $TrID     = $form->{'id'};
    my $SCID     = $form->{'s'};
    my $ContDate = $value;
    my $btime    = $form->{'b'};
    my $etime    = $form->{'e'};
    my $InsID    = DBA->getxref( $form, 'xSC', $SCID, 'InsID' );

 #warn qq|vNote: ProvID=$ProvID,ClientID=$ClientID,btime=$btime,etime=$etime\n|;
 #warn qq|vNote: ContDate=$ContDate,min=$min,max=$max\n|;
    my $msg = '';
    unless ( $ContDate eq '' ) {
        $msg .=
          main->DUP( 'ProvID', $ProvID, $TrID, $ContDate, $btime, $InsID );
        $msg .=
          main->DUP( 'ClientID', $ClientID, $TrID, $ContDate, $btime, $InsID );
        $msg .=
          main->DUP( 'ProvID', $ProvID, $TrID, $ContDate, $etime, $InsID );
        $msg .=
          main->DUP( 'ClientID', $ClientID, $TrID, $ContDate, $etime, $InsID );

        # check duplicate note for Client/ContDate/ServiceCode
        my ( $chkcode, $chkmsg ) =
          cBill->CheckClientDUP( $form, $ClientID, $ProvID, $TrID, $SCID,
            $ContDate );

        #warn qq|vNote: chkcode=$chkcode, chkmsg=$chkmsg\n|;
        $msg .= qq|!!! WARNING !!!\n| . $chkmsg if ($chkcode);
        $msg .=
          main->INPA( $ProvID, $ClientID, $InsID, $TrID, $ContDate, $SCID );
        ##$msg .= main->SignNote($ProvID,$ClientID,$InsID,$TrID,$ContDate,$SCID);
        $msg .= main->MAX( $SCID, $ContDate, $btime, $etime );
    }
    my ( $chkcode, $chkmsg ) = cBill->CheckProblems( $form, $ClientID, $TrID );

    #warn qq|vNote: chkcode=$chkcode, chkmsg=$chkmsg\n|;
    $msg .= qq|!!! WARNING !!!\n| . $chkmsg if ($chkcode);
    $msg .= main->CheckTrPlan( $ProvID, $ClientID, $ContDate );
    $msg .= main->checkHospice($ClientID);

    #warn qq|msg=$msg\n|;
    $xml = qq|<response>\n| . main->iwarn($msg) . qq|</response>|;
}
elsif ( $form->{method} eq 'vProvID' ) {
    my $target = $form->{'target'};
    my $value  = $form->{'value'};

    #warn qq|vProvID: target=$target,value=$value\n|;
    my $ProvID   = $value;
    my $Mod4     = $form->{'m'};
    my $ClientID = $form->{'c'};
    my $TrID     = $form->{'id'};
    my $ContDate = $form->{'d'};

    #warn qq|vProvID: Mod4=$Mod4,ContDate=$ContDate\n|;
    my $btime = $form->{'b'};
    my $etime = $form->{'e'};
    my ( $err, $msg ) = ( '', '' );
    my $InsID = DBA->getxref( $form, 'xSC', $SCID, 'InsID' );
    if ( $value eq '' ) {
        $err = qq|!!! WARNING !!!\nProvider CANNOT be empty\n|;
    }
    else {
        $msg .=
          main->DUP( 'ProvID', $ProvID, $TrID, $ContDate, $btime, $InsID );
        $msg .=
          main->DUP( 'ClientID', $ClientID, $TrID, $ContDate, $btime, $InsID );
        $msg .=
          main->DUP( 'ProvID', $ProvID, $TrID, $ContDate, $etime, $InsID );
        $msg .=
          main->DUP( 'ClientID', $ClientID, $TrID, $ContDate, $etime, $InsID );
    }
    my $Mod4Sel =
      SysAccess->chkPriv( $form, 'TeleMedicine', $ProvID )
      ? qq|Modifiers: <SELECT NAME="Treatment_Mod4_1" >|
      . DBA->selxTable( $form, 'xSCMod4', $Mod4 )
      . qq|</SELECT>|
      : qq|<INPUT TYPE="hidden" NAME="Treatment_Mod4_1" VALUE="" >|;

    #warn qq|msg=$msg\n|;
    #warn qq|Mod4Sel=$Mod4Sel\n|;
    my $out = $err eq ''
      ? qq|
  <command method="setvalue">
    <target>${target}</target>
    <value>${ProvID}</value>
  </command>
  <command method="setcontent">
    <target>Mod4_popup</target>
    <content><![CDATA[${Mod4Sel}]]></content>
  </command>
|
      : main->ierr( $target, $err );
    $out .= main->iwarn($msg);

    #warn qq|out=$out\n|;
    $xml = qq|<response>\n${out}</response>|;
}
elsif ( $form->{method} eq 'vSCID' ) {
    my $target = $form->{'target'};
    my $value  = $form->{'value'};

    #warn qq|vSCID: target=$target,value=$value\n|;
    my $SCID     = $value;
    my $ProvID   = $form->{'p'};
    my $ClientID = $form->{'c'};
    my $TrID     = $form->{'id'};
    my $ContDate = $form->{'d'};
    my $btime    = $form->{'b'};
    my $etime    = $form->{'e'};

#warn qq|vSCID: SCID=$SCID,ProvID=$ProvID,ClientID=$ClientID,TrID=$TrID,ContDate=$ContDate\n|;
    my ( $err, $msg, $Type, $POS, $InsID ) = ( '', '', '', '', '' );
    my $NullGrpSize = qq|  <command method="setvalue">
    <target>GrpSize</target>
    <value></value>
  </command>|;
    if ( $SCID eq '' ) {
        $err = qq|!!! WARNING !!!\nService Code CANNOT be empty\n|;
    }
    else {
#warn qq|target=$target,value=$value,ClientID=$ClientID,SCID=$SCID,ContDate=$ContDate\n|;
        $Type        = DBA->getxref( $form, 'xSC', $SCID, 'Type' );
        $POS         = DBA->getxref( $form, 'xSC', $SCID, 'POS' );
        $InsID       = DBA->getxref( $form, 'xSC', $SCID, 'InsID' );
        $NullGrpSize = '' if ( $Type eq 'GC' || $Type eq 'GR' );
    }

    #warn qq|Type=$Type,POS=$POS,InsID=$InsID\n|;
    #warn qq|err=$err\n|;
    if ( $err eq '' ) {

        # check duplicate note for Client/ContDate/ServiceCode
        my ( $chkcode, $chkmsg ) =
          cBill->CheckClientDUP( $form, $ClientID, $ProvID, $TrID, $SCID,
            $ContDate );

        #warn qq|vSCID: chkcode=$chkcode, chkmsg=$chkmsg\n|;
        $msg .= qq|!!! WARNING !!!\n| . $chkmsg if ($chkcode);
        $msg .=
          main->INPA( $ProvID, $ClientID, $InsID, $TrID, $ContDate, $SCID );

        #    $msg .= main->CheckTrPlan($ProvID,$ClientID,$ContDate);
        $msg .= main->MAX( $SCID, $ContDate, $btime, $etime );
    }

    #warn qq|msg=$msg\n|;
    my $out = $err eq ''
      ? qq|
  <command method="setvalue">
    <target>CurType</target>
    <value>${Type}</value>
  </command>
  <command method="setvalue">
    <target>Treatment_POS_1</target>
    <value>${POS}</value>
  </command>
${NullGrpSize}
|
      : main->ierr( $target, $err );
    $out .= main->iwarn($msg);
    $xml = qq|<response>\n${out}</response>|;
}
elsif ( $form->{method} eq 'vGrpSize' ) {
    my $target = $form->{'target'};
    my $value  = $form->{'value'};

    #warn qq|vGrpSize: target=$target,value=$value\n|;
    my $GrpSize = $value;
    my $CurType = $form->{'ct'};
    my ( $err, $msg ) = ( '', '' );
    if ( $CurType eq 'GC' || $CurType eq 'GR' ) {
        if ( $GrpSize eq '' ) {
            $err =
qq|!!! WARNING !!!\nBased on Service Code, Group Size CANNOT be empty.\n|;
        }
    }
    elsif ( $GrpSize ne '' ) {
        $err =
qq|!!! WARNING !!!\nBased on Service Code, Group Size MUST be empty.\n|;
    }

    #warn qq|GrpSize=$GrpSize,CurType=$CurType\n|;
    #warn qq|err=$err\n|;
    $xml =
      $err eq ''
      ? ''
      : qq|<response>\n| . main->ierr( $target, $err ) . qq|</response>|;
}
elsif ( $form->{method} eq 'vContDate' ) {
    my $target = $form->{'target'};
    my $value  = $form->{'value'};

    #warn qq|vContDate: target=$target,value=$value\n|;
    my $ProvID   = $form->{'p'};
    my $ClientID = $form->{'c'};
    my $TrID     = $form->{'id'};
    my $SCID     = $form->{'s'};
    my $btime    = $form->{'b'};
    my $etime    = $form->{'e'};
    my ( $err, $msg, $ContDate, $min, $max ) = ( '', '', '', '', '' );
    my $InsID = DBA->getxref( $form, 'xSC', $SCID, 'InsID' );

    if ( $value eq '' ) {
        $err = qq|!!! WARNING !!!\nContact Date CANNOT be empty\n|;
    }
    else {
        #warn qq|ProvID=$ProvID,ClientID=$ClientID,btime=$btime,etime=$etime\n|;
        $min = DBUtil->Date( 'today', -24, 0 );
        $max = DBUtil->Date('today');
        ( $err, $ContDate ) =
          DBUtil->vDate( $value, $form->{'TODAY'}, $min, $max );
    }

    #warn qq|ContDate=$ContDate,min=$min,max=$max\n|;
    #warn qq|err=$err\n|;
    if ( $err eq '' ) {
        $msg .=
          main->DUP( 'ProvID', $ProvID, $TrID, $ContDate, $btime, $InsID );
        $msg .=
          main->DUP( 'ClientID', $ClientID, $TrID, $ContDate, $btime, $InsID );
        $msg .=
          main->DUP( 'ProvID', $ProvID, $TrID, $ContDate, $etime, $InsID );
        $msg .=
          main->DUP( 'ClientID', $ClientID, $TrID, $ContDate, $etime, $InsID );

        # check duplicate note for Client/ContDate/ServiceCode
        my ( $chkcode, $chkmsg ) =
          cBill->CheckClientDUP( $form, $ClientID, $ProvID, $TrID, $SCID,
            $ContDate );

        #warn qq|vContDate: chkcode=$chkcode, chkmsg=$chkmsg\n|;
        $msg .= qq|!!! WARNING !!!\n| . $chkmsg if ($chkcode);
        $msg .=
          main->INPA( $ProvID, $ClientID, $InsID, $TrID, $ContDate, $SCID );
        my ( $chkcode, $chkmsg ) =
          cBill->CheckProblems( $form, $ClientID, $TrID );

        #warn qq|vContDate: chkcode=$chkcode, chkmsg=$chkmsg\n|;
        $msg .= qq|!!! WARNING !!!\n| . $chkmsg if ($chkcode);
        $msg .= main->CheckTrPlan( $ProvID, $ClientID, $ContDate );
        $msg .= main->checkHospice($ClientID);
    }
    my $plist =
      gHTML->setClientNoteProblems( $form, 0, $ClientID, $TrID, $ContDate );
    my $tlist =
      gHTML->setClientNoteTrPlanPG( $form, 0, $ClientID, $TrID, $ContDate );

    #warn qq|list=$list\n|;
    #warn qq|msg=$msg\n|;
    my $out = $err eq ''
      ? qq|
  <command method="setvalue">
    <target>${target}</target>
    <value>${ContDate}</value>
  </command>
  <command method="setcontent">
    <target>ProblemsList</target>
    <content><![CDATA[${plist}]]></content>
  </command>
  <command method="setcontent">
    <target>ProblemsGoals</target>
    <content><![CDATA[${tlist}]]></content>
  </command>
|
      : main->ierr( $target, $err );
    $out .= main->iwarn($msg);
    $xml = qq|<response>\n${out}</response>|;
}
elsif ( $form->{method} eq 'vContTime' ) {
    my $target = $form->{'target'};
    my $value  = $form->{'value'};

    #warn qq|vContTime: target=$target,value=$value\n|;
    my $ProvID   = $form->{'p'};
    my $ClientID = $form->{'c'};
    my $TrID     = $form->{'id'};
    my $SCID     = $form->{'s'};
    my $ContDate = $form->{'d'};
    my $itime    = $form->{'t'};
    my ( $err, $msg, $ctime, $ctimeampm, $btime, $etime ) =
      ( '', '', '', '', '', '' );
    my $timeid =
      $target eq 'BeginTime'
      ? 'Treatment_ContLogBegTime_1'
      : 'Treatment_ContLogEndTime_1';
    my $InsID = DBA->getxref( $form, 'xSC', $SCID, 'InsID' );

    #warn qq|target=$target,value=$value,itime=$itime,timeid=$timeid\n|;
    if ( $value eq '' ) { $err = qq|!!! WARNING !!!\nTime CANNOT be empty\n|; }
    else {
        ( $err, $ctime ) = DBUtil->vTime( $value, $form->{'NOW'} );
        $ctimeampm = DBUtil->AMPM($ctime);

        #warn qq|ctime=$ctime,ctimeampm=$ctimeampm\n|;
        #warn qq|err=$err\n|;
        ( $btime, $etime ) = ( $ctime, $itime );
        if ( $target eq 'EndTime' ) { ( $btime, $etime ) = ( $itime, $ctime ); }

        #warn qq|ProvID=$ProvID,ClientID=$ClientID,btime=$btime,etime=$etime\n|;
        $msg .=
          main->DUP( 'ProvID', $ProvID, $TrID, $ContDate, $btime, $InsID );
        $msg .=
          main->DUP( 'ClientID', $ClientID, $TrID, $ContDate, $btime, $InsID );
        $msg .=
          main->DUP( 'ProvID', $ProvID, $TrID, $ContDate, $etime, $InsID );
        $msg .=
          main->DUP( 'ClientID', $ClientID, $TrID, $ContDate, $etime, $InsID );
        if ( $btime ne '' && $etime ne '' ) {
            my ( $bhour, $bminute, $bsecond ) = split( ':', $btime );
            my ( $ehour, $eminute, $esecond ) = split( ':', $etime );
            if ( $etime lt $btime ) {
                $err .=
"\n!!! PROBLEM !!!\nEnding Time BEFORE Beginning Time.\nPlease check!\n";
            }
            elsif ( $ehour - $bhour == 0 && $eminute - $bminute < 15 ) {
                $msg .=
"!!! WARNING !!!\nTreatment duration is LESS THAN 15 minutes.\n";
            }
            elsif ( $ehour - $bhour == 1 && ( $eminute + 60 ) - $bminute < 15 )
            {
                $msg .=
"!!! WARNING !!!\nTreatment duration is LESS THAN 15 minutes.\n";
            }
            elsif ( $ehour - $bhour > 8
                || ( $ehour - $bhour == 8 && $eminute > $bminute ) )
            {
                $msg .=
"!!! WARNING !!!\nTreatment duration is GREATER THAN 8 hours.\n";
            }
            $msg .= main->MAX( $SCID, $ContDate, $btime, $etime );
        }
    }

#warn qq|target=$target,value=$value,timeid=$timeid,ctime=$ctime,ctimeampm=$ctimeampm\n|;
    my $out = $err eq ''
      ? qq|
  <command method="setvalue">
    <target>${target}</target>
    <value>${ctimeampm}</value>
  </command>
  <command method="setvalue">
    <target>${timeid}</target>
    <value>${ctime}</value>
  </command>
  <command method="setcontent">
    <target>${timeid}_display</target>
    <content>${ctime}</content>
  </command>
|
      : main->ierr( $target, $err, $timeid, $timeid . '_display' );
    $out .= main->iwarn($msg);
    $xml = qq|<response>\n${out}</response>|;
}

#warn qq|validateNote: xml=${xml}\n|;
print qq|Content-type: text/xml

<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
${xml}
|;
exit;
############################################################################
sub iwarn {
    my ( $self, $warn ) = @_;
    return ('') if ( $warn eq '' );
    my $out = qq|
  <command method="alert">
    <message>${warn}</message>
  </command>
|;
    return ($out);
}

sub ierr {
    my ( $self, $target, $err, $tid, $cid ) = @_;

    #warn qq|ierr: target=$target,tid=$tid,cid=$cid\n|;
    return ('') if ( $err eq '' );
    my $out = qq|
  <command method="setdefault">
    <target>${target}</target>
  </command>
  <command method="alert">
    <message>${err}</message>
  </command>
  <command method="focus">
    <target>${target}</target>
  </command>
|;
    $out .= qq|
  <command method="setdefault">
    <target>${tid}</target>
  </command>
| if ( $tid ne '' );
    $out .= qq|
  <command method="setcontent">
    <target>${cid}</target>
    <content></content>
  </command>
| if ( $cid ne '' );
    return ($out);
}

sub INPA {
    my ( $self, $ProvID, $ClientID, $InsID, $TrID, $ContDate, $SCID ) = @_;

#warn qq|INPA: ProvID=$ProvID,ClientID=$ClientID,InsID=$InsID,TrID=$TrID,ContDate=$ContDate,SCID=$SCID\n|;
    return () if ( $InsID eq '' );       # Must have a Insurance.
    return () if ( $ContDate eq '' );    # Must have a Date.
    return () if ( $SCID eq '' );        # Must have a SCID.
    my $PAReq = DBA->getxref( $form, 'xSC', $SCID, 'PAReq' );

    #warn qq|INPA: PAREQUIRED: SCID=$SCID,PAReq=$PAReq\n|;
    return () unless ($PAReq);           # Non-Billable OK.
    my $SCNum = DBA->getxref( $form, 'xSC', $SCID, 'SCNum' );

    #warn qq|INPA: NON-BILLABLE: SCID=$SCID,SCNum=$SCNum\n|;
    return () if ( $SCNum =~ /^X/ );     # Non-Billable OK.
    my ( $found, $PRAUTHNUM, $PRAUTHDAYS, $INSDESCR, $AXIS1ACODE, $TRPLANID ) =
      ( 0, '', 0, '', '', '' );
    my $dbh = $form->dbconnect();
    my $sPrAuthRVU =
      $dbh->prepare("select SCID from PrAuthRVU where PrAuthID=?");
    my $sClientPrAuth = $dbh->prepare(
"select ClientPrAuth.ID,ClientPrAuth.PAgroup,ClientPrAuth.PAnumber,to_days(ClientPrAuth.ExpDate)-to_days(curdate()),xInsurance.Descr from ClientPrAuth left join Insurance on Insurance.InsNumID=ClientPrAuth.InsuranceID left join xInsurance on xInsurance.ID=Insurance.InsID where ClientPrAuth.ClientID=? and Insurance.InsID=? and ? between ClientPrAuth.EffDate and ClientPrAuth.ExpDate order by ClientPrAuth.EffDate desc,ClientPrAuth.ExpDate"
    );
    $sClientPrAuth->execute( $ClientID, $InsID, $ContDate )
      || $form->dberror("vSCID: select ClientPrAuth");
    while ( my ( $PrAuthID, $PAgroup, $PAnumber, $PrAuthDays, $InsDescr ) =
        $sClientPrAuth->fetchrow_array )
    {
        $PrAuthDays += 0;
        $PRAUTHNUM  = $PAnumber;
        $PRAUTHDAYS = $PrAuthDays;
        $INSDESCR   = $InsDescr;
        if ( $PAgroup eq '' ) {
            $sPrAuthRVU->execute($PrAuthID)
              || $form->dberror("INPA: select RVU ${PrAuthID}");
            while ( my ($scid) = $sPrAuthRVU->fetchrow_array ) {
                if ( $scid == $SCID ) { $found = 1; last; }
            }
        }
        else {
            my $SCIDs = DBA->getxref( $form, 'xPAgroups', $PAgroup, 'SCIDs' );
            foreach my $scid ( split( chr(253), $SCIDs ) ) {
                if ( $scid == $SCID ) { $found = 1; last; }
            }
            last if ($found);
        }
    }

#warn qq|INPA: found=$found,TrID=$TrID,INSDESCR=$INSDESCR,AXIS1ACODE=$AXIS1ACODE\n|;
#warn qq|INPA: PRAUTHNUM=$PRAUTHNUM,PRAUTHDAYS=$PRAUTHDAYS\n|;
    $sClientPrAuth->finish();
    $sPrAuthRVU->finish();
    my $warn =
      $found
      ? ''
      : qq|!!! WARNING !!!\nSelected Service Code for Contact Date '${ContDate}' not in Prior Authorization.\n|;
    my $ABSPRAUTHDAYS = abs($PRAUTHDAYS);
    if ( $TrID eq '' ) {
        if ( $PRAUTHNUM eq '' ) {
            $warn .=
qq|!!! WARNING !!!\nThis client has no Prior Authorization Number.\nAny treatments that you perform/enter may not be paid!\n|;
        }
        elsif ( $PRAUTHDAYS == 0 ) {
            $warn .=
qq|!!! WARNING !!!\nThis client Authorization expires TODAY.\nAny treatments that you perform/enter may not be paid!\n|;
        }
        elsif ( $PRAUTHDAYS < 0 ) {
            $warn .=
qq|!!! WARNING !!!\nThis client's Prior Authorization has expired ${ABSPRAUTHDAYS} days ago.\n|;
        }
        elsif ( $PRAUTHDAYS <= 15 ) {
            $warn .=
qq|!!! WARNING !!!\nThis client's Prior Authorization will expire in ${PRAUTHDAYS} days.\n|;
        }
    }
    return ($warn);
}

# check duplicate note for Client/ContDate/ContTime
sub DUP {
    my ( $self, $fld, $ID, $MyTrID, $ContDate, $ContTime, $InsID ) = @_;

#warn qq|\n\nDUP1: fld=$fld, ID=$ID, ContDate=$ContDate, ContTime=${ContTime}\n|;
    return () if ( $ContDate eq '' );    # Must have a Date.
    return () if ( $ContTime eq '' );    # Must have a Time.
    return ()
      if ( $InsID eq '356' );  # Don't check for Note with Health Home Insurance
    return ()
      if ( $InsID eq '391' )
      ;    # Don't check for Note with Meaningful Use Insurance
    my $dbh = $form->dbconnect();

    # Skip Health Home and Meaningful Use (InPatient Procedures) Insurance codes
    my $SKIPINS = "and xSC.InsID !='356' and xSC.InsID !='391'";

# Skip T1012 HF codes for Providers (because both Group and Individual are ok)...
    my $T1012 = "and xSC.SCNum NOT LIKE 'T1012 HF%'";

# Skip H0001 HF QJ codes for Providers (because these are 2nd and 3rd events)...
    my $H0001 = "and xSC.SCNum!='H0001 HF QJ'";

    # Skip groups codes for Providers...
    my $Groups =
      $fld eq 'ProvID' ? "and xSC.Type!='GC' and xSC.Type!='GR'" : '';
    my $sTreatment = $dbh->prepare(
"select TrID,ContLogBegTime,ContLogEndTime,xSC.SCID,xSC.SCNum from Treatment left join xSC on xSC.SCID=Treatment.SCID where xSC.SCNum NOT LIKE 'X%' ${SKIPINS} ${T1012} ${H0001} ${Groups} and ${fld}=? and TrID!='${MyTrID}' and ContLogDate=? and ContLogBegTime<=? and ContLogEndTime>=?"
    );

#warn qq|DUP2: select=\nselect TrID,ContLogBegTime,ContLogEndTime,xSC.SCID,xSC.SCNum from Treatment left join xSC on xSC.SCID=Treatment.SCID where xSC.SCNum NOT LIKE 'X%' ${SKIPINS} ${T1012} ${H0001} ${Groups} and ${fld}=? and TrID!='${MyTrID}' and ContLogDate=? and ContLogBegTime<=? and ContLogEndTime>=?\n|;
#warn qq|DUP2: ID=${ID}, ContDate=${ContDate}, ContTime=${ContTime}, ContTime=${ContTime}\n|;
#warn qq|DUP2: fld=${fld}, TrID=${MyTrID}, Groups=${Groups}, T1012=${T1012}, H0001=${H0001}\n|;
    $sTreatment->execute( $ID, $ContDate, $ContTime, $ContTime )
      || $form->dberror("DUP: select Treatment");
    my $rows = $sTreatment->rows;
    my ( $TrID, $BeginTime, $EndTime, $SCID, $SCNum ) =
      $sTreatment->fetchrow_array;
    $sTreatment->finish();
    my $Type = $fld eq 'ProvID' ? 'Provider' : 'Client';

#warn qq|DUP3: fld=$fld, TrID=$TrID, BeginTime=$BeginTime, EndTime=$EndTime, SCID=$SCID, SCNum=$SCNum\n|;
    my $warn =
      $TrID
      ? qq|!!! WARNING !!!\nDuplicate Note for ${Type} on '${ContDate}/${ContTime}'. (${TrID}/${BeginTime}/${EndTime}) (${rows} found)\n|
      : '';

    #warn qq|DUP4: warn=$warn\n|;
    return ($warn);
}

# check note exceeds any maximum for billing
sub MAX {
    my ( $self, $SCID, $ContDate, $BeginTime, $EndTime ) = @_;

#warn qq|\n\nMAX: SCID=${SCID}, ContDate=${ContDate}, BeginTime=${BeginTime}, EndTime=${EndTime}\n|;
    return () if ( $SCID eq '' );         # Must have a SCID.
    return () if ( $ContDate eq '' );     # Must have a Date.
    return () if ( $BeginTime eq '' );    # Must have a BeginTime.
    return () if ( $EndTime eq '' );      # Must have a EndTime.
    my $warn = '';
    my $rxSC =
      cBill->getServiceCode( $form, $SCID, $ContDate, $BeginTime, $EndTime );

    #warn qq|MAX: rxSC->{'SCNum'}, Units=$rxSC->{Units}\n|;
    if ( $rxSC->{'SCNum'} =~ /^H0004/
        && ( $rxSC->{'SCNum'} =~ /HE$/ || $rxSC->{'SCNum'} =~ /HF$/ ) )
    {
        $warn =
          $rxSC->{Units} > 4
          ? qq|!!! WARNING !!!\nIndividual Units over 4 Units may not pay!\n(${BeginTime}/${EndTime})\n|
          : '';
    }
    elsif ( $rxSC->{'SCNum'} =~ /^H0004/
        && ( $rxSC->{'SCNum'} =~ /HE HR$/ || $rxSC->{'SCNum'} =~ /HF HR$/ ) )
    {
        $warn =
          $rxSC->{Units} > 4
          ? qq|!!! WARNING !!!\nFamily Units over 4 Units may not pay!\n(${BeginTime}/${EndTime})\n|
          : '';
    }
    elsif ( $rxSC->{'SCNum'} =~ /^H0004/
        && ( $rxSC->{'SCNum'} =~ /HE HQ$/ || $rxSC->{'SCNum'} =~ /HF HQ$/ ) )
    {
        $warn =
          $rxSC->{Units} > 6
          ? qq|!!! WARNING !!!\nGroup Units over 6 Units may not pay!\n(${BeginTime}/${EndTime})\n|
          : '';
    }

    #warn qq|MAX: warn=${warn}\n|;
    return ($warn);
}

sub CheckTrPlan {
    my ( $self, $ProvID, $ClientID, $ContDate ) = @_;

  #warn qq|CheckTrPlan: ProvID=$ProvID,ClientID=$ClientID,ContDate=$ContDate\n|;
    my $warn = '';
    return ($warn) unless ($ClientID);
    my $dbh = $form->dbconnect();
    my $with =
      $ContDate eq '' ? '' : qq| and '${ContDate}' between EffDate and ExpDate|;
    my $msg =
      $ContDate eq ''
      ? qq|!!! WARNING !!!\nNO Treatment Plan FOUND!\nThis client does not have a valid Treatment Plan in the system.\nThis treatment may not be paid.\nAlso there are NO PROBLEMS/GOALS/OBJECTIVES!\n|
      : qq|!!! WARNING !!!\nNO Treatment Plan FOUND for ${ContDate}!\nThis treatment may not be paid.\nAlso there are NO PROBLEMS/GOALS/OBJECTIVES!\n|;

    #warn qq|CheckTrPlan: with=${with}\nmsg=${msg}|;
    my $s = $dbh->prepare(
"select ID from ClientTrPlan where ClientID=? ${with} order by EffDate desc"
    );
    $s->execute($ClientID)
      || $form->dberror("CheckTrPlan: select ClientTrPlan ${ClientID}");
    my $rows = $s->rows;
    my ($TrPlanID) = $s->fetchrow_array;
    $warn .= $msg unless ($rows);
    $s->finish();

    #warn qq|CheckTrPlan: rows=${rows}, warn=${warn}\n|;
    return ($warn) unless ($ProvID);
    return ($warn) unless ($TrPlanID);
    my $s = $dbh->prepare(
"select ID from ClientTrPlanS where ProvID=? and ClientID=? and TrPlanID=?"
    );
    $s->execute( $ProvID, $ClientID, $TrPlanID );
    my $rows = $s->rows;
    my ($TrPlanSID) = $s->fetchrow_array;
    $s->finish();

    unless ($rows) {
        my $s =
          $dbh->prepare("select FName,LName from Provider where ProvID=?");
        $s->execute($ProvID);
        my ( $FName, $LName ) = $s->fetchrow_array;
        $warn .=
qq|!!! WARNING !!!\nPlease have ${FName} ${LName} electronically sign this client\'s Treatment Plan.\n|;
        $s->finish();
    }

    #warn qq|CheckTrPlan: rows=${rows}, warn=${warn}\n|;
    return ($warn);
}
############################################################################

# Check if HospiceCheck is active
# For this change to work we need to add a new column "HospiceCheck" to  clientemergency
# with tinyint type and null by Default
sub checkHospice {
    my ( $self, $ClientID ) = @_;
    my $warn = '';
    return ($warn) unless ($ClientID);
    my $dbh = $form->dbconnect();
    my $s   = $dbh->prepare(
        "SELECT HospiceCheck FROM ClientEmergency WHERE ClientID=?");
    $s->execute($ClientID);
    my ($HospiceCheck) = $s->fetchrow_array;
    $s->finish();

    if ( $HospiceCheck eq 1 ) {
        $warn .= qq|Must use Hospice service code with GW modifier\n|;

    }

    return $warn;
}
