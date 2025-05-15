#!/usr/bin/perl
use lib 'C:/xampp/htdocs/src/lib';
use DBI;
use myForm;
use myHTML;
use SysAccess;

############################################################################
my $form = myForm->new();
my $dbh  = myDBI->dbconnect( $form->{'DBNAME'} );

#warn qq|adjNote: ENTER: submit=$form->{'submit'}\n|;
#foreach my $f ( sort keys %{$form} ) { warn "adjNote: form-$f=$form->{$f}\n"; }
if ( !SysAccess->chkPriv( $form, 'ADDTrans' ) ) {
    myDBI->error("Manual Transaction Add / Access Denied!");
}
if ( $form->{'TrID'} eq '' ) {
    myDBI->error("Manual Transaction Add / NO Treatment ID!");
}

my $TrID       = $form->{'TrID'};
my $sTreatment = $dbh->prepare( "
select Treatment.*,xSC.SCNum,xInsurance.InsCode 
 from Treatment 
  left join xSC on xSC.SCID=Treatment.SCID
  left join xInsurance on xInsurance.ID=xSC.InsID
 where TrID=?
" );
$sTreatment->execute($TrID)
  || myDBI->dberror("adjNote: select Treatment ${TrID}");
my $rTreatment = $sTreatment->fetchrow_hashref;

#foreach my $f ( sort keys %{$rTreatment} ) { warn "rTreatment: $f=$rTreatment->{$f}\n"; }

my $url = myHTML->close( 1, $form->{'mlt'} );
if   ( $form->{submit} ) { $url = main->submit(); }
else                     { $url = main->html(); }
$sTreatment->finish();
myDBI->cleanup();

#warn qq|url=${url}\n|;
print $url unless ( $form->{'Browser'} eq 'Telnet' );

#warn qq|adjNote: EXIT: submit=$form->{'submit'}\n|;
exit;

############################################################################
sub submit {
    my $PaidAmt = $form->{'PaidAmt'};
    my $RefID   = $form->{'RefID'};
    my $ICN     = $form->{'ICN'};
    my $DenCode = $form->{'DenCode'};
    my $html    = myHTML->close( 1, $form->{'mlt'} );
    if ( $PaidAmt eq '' || $RefID eq '' ) {
        $html = main->html("PaidAmt or RefID CANNOT be null!");
    }
    elsif ( DBA->updSQLdone($form) ) {
        $html = main->html("updates already done!");
    }
    else {
        #warn qq|update....TrID=$TrID\n|;
        my $RecDate = $form->{'TODAY'};

        # create a NoteTrans record...
        my $rNoteTrans = ();
        $rNoteTrans->{'TrID'}     = $TrID;
        $rNoteTrans->{'ClientID'} = $rTreatment->{'ClientID'};
        $rNoteTrans->{'ContDate'} = $rTreatment->{'ContLogDate'};
        $rNoteTrans->{'BillDate'} = $rTreatment->{'BillDate'};
        $rNoteTrans->{'SCID'}     = $rTreatment->{'SCID'};
        $rNoteTrans->{'SCNum'}    = $rTreatment->{'SCNum'};
        $rNoteTrans->{'InsCode'}  = $rTreatment->{'InsCode'};
        $rNoteTrans->{'BillAmt'}  = $rTreatment->{'BilledAmt'};
        $rNoteTrans->{'Units'}    = $rTreatment->{'Units'};
        $rNoteTrans->{'Code'} =
          'BI';    # 'BI' for an instance, get updated below...
        $rNoteTrans->{'SRC'} = 'CL';

        #foreach my $f ( sort keys %{$r} ) { warn "r: $f=$r->{$f}\n"; }
        my $TransID = DBA->doUpdate( $form, 'NoteTrans', $rNoteTrans )
          ;        # insert the record (no where)

        #warn qq|adjNote: CALLED doUpdate: NoteTrans=${TransID}\n|;
        #warn qq|TrID=${TrID}, TransID=${TransID}\n|;

        my $r835 = ();
        $r835->{'TransID'}    = $TransID;
        $r835->{'ClientID'}   = $rTreatment->{'ClientID'};
        $r835->{'ContDate'}   = $rTreatment->{'ContLogDate'};
        $r835->{'ServCode'}   = $rTreatment->{'SCNum'};
        $r835->{'RecDate'}    = $RecDate;
        $r835->{'InsCode'}    = $rTreatment->{'InsCode'};
        $r835->{'BillAmt'}    = $rTreatment->{'BilledAmt'};
        $r835->{'PaidAmt'}    = $PaidAmt;
        $r835->{'Units'}      = $rTreatment->{'Units'};
        $r835->{'RefID'}      = $RefID;
        $r835->{'ICN'}        = $ICN;
        $r835->{'DenCode'}    = $DenCode;
        $r835->{'ReasonCode'} = $DenCode;

        #foreach my $f ( sort keys %{$r835} ) { warn "r835: $f=$r835->{$f}\n"; }
        my ( $trid, $scid, $code, $type ) =
          uBill->postClaim( $form, $r835, 'CL', 'ADJ' );

#warn qq|adjNote: CALLED postClaim: TrID=${trid}, SCID=${scid}, code=${code}, type=${type}\n|;
        my $code = uBill->setPayDate( $form, $RecDate, $TransID )
          ;    # remove from Payroll, TransID, not TrID
    }
    return ($html);
}

sub html {
    my ( $self, $Client, $Dates ) = @_;
    my $sClient = $dbh->prepare("select * from Client where ClientID=?");
    $sClient->execute( $rTreatment->{'ClientID'} )
      || myDBI->dberror("adjNote: select Client $rPrAUth->{'ClientID'}");
    my $rClient = $sClient->fetchrow_hashref;
    $sClient->finish();
    my $ContDate =
      DBUtil->Date( $rTreatment->{'ContLogDate'}, 'fmt', 'MM/DD/YYYY' );
    my $selDenCodes = DBA->selxTable( $form, 'xDenCodesTrans', '', 'ID Descr' );
    $form->{'FORMID'} = myDBI->getFORMID($form);

    # Start out the display.
    my $html = myHTML->newHTML(
        $form,
        'Manually Add Transaction',
        'CheckPopupWindow noclock countdown_10'
      )
      . qq|
<SCRIPT type="text/javascript" src="/src/cgi/js/ajaxrequest.js"></SCRIPT>
<SCRIPT LANGUAGE="JavaScript" SRC="/src/cgi/js/vNum.js"> </SCRIPT>
<TABLE CLASS="main" >
  <TR>
    <TD CLASS="hdrcol banner" >
      Manually Add Transaction 
    </TD>
  </TR>
  <TR>
    <TD CLASS="hdrcol title" >
      for Note: $rTreatment->{'TrID'}
    </TD>
  </TR>
  <TR>
    <TD CLASS="hdrcol title" >
      $rClient->{'FName'} $rClient->{'LName'}
      ${ContDate} - $rTreatment->{'SCNum'}
    </TD>
  </TR>
</TABLE>
<SCRIPT LANGUAGE="JavaScript" >
function validate(form)
{
  if( form.PaidAmt.value == "" ) { myAlert("PaidAmt cannot be null",'Validation Alert!'); form.PaidAmt.focus(); return false; }
  if( form.RefID.value == "" ) { myAlert("RefID cannot be null",'Validation Alert!'); form.RefID.focus(); return false; }
  return true;
}
</SCRIPT>
<FORM NAME="submit" ACTION="/cgi/bin/adjNote.pl" METHOD="POST">
  <TABLE CLASS="home fullsize" >
    <TR><TD CLASS="hdrtxt" COLSPAN="2" >Please enter Amount and RefID</TD></TR>
    <TR>
      <TD CLASS="strcol" > Amount:</TD>
      <TD CLASS="strcol" > <INPUT TYPE="TEXT" NAME="PaidAmt" VALUE="" ONFOCUS="select()" ONCHANGE="return vNum(this,-3000,3000)" SIZE="12" ></TD>
    </TR>
    <TR>
      <TD CLASS="strcol" > Check # / RefID: </TD>
      <TD CLASS="strcol" > <INPUT TYPE="text" NAME="RefID" VALUE="" ONFOCUS="select()" SIZE="30" > </TD>
    </TR>
    <TR>
      <TD CLASS="strcol" > Claim Control # / ICN: </TD>
      <TD CLASS="strcol" > <INPUT TYPE="text" NAME="ICN" VALUE="" ONFOCUS="select()" SIZE="20" > </TD>
    </TR>
    <TR>
      <TD CLASS="strcol" > Denial Code: </TD>
      <TD CLASS="strcol" >
        <SELECT NAME="DenCode" >
          ${selDenCodes} 
        </SELECT> 
      </TD>
    </TR>
    <TR>
      <TD CLASS="numcol" COLSPAN="2" >
        <INPUT TYPE="submit" ONCLICK="return validate(this.form);" NAME="submit" VALUE="add" >
        <INPUT TYPE="button" NAME="cancel" VALUE="cancel" ONCLICK="javascript: window.close()" >
      </TD>
    </TR>
  </TABLE>
  <INPUT TYPE="hidden" NAME="TrID" VALUE="$form->{TrID}" >
  <INPUT TYPE="hidden" NAME="mlt" VALUE="$form->{mlt}" >
  <INPUT TYPE="hidden" NAME="FORMID" VALUE="$form->{FORMID}" >
  <SCRIPT LANGUAGE="JavaScript">
    document.submit.elements[0].focus();
  </SCRIPT>
</FORM>
    </TD>
  </TR>
</TABLE>
</BODY>
</HTML>
|;
    return ($html);
}
############################################################################
