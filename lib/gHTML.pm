package gHTML;
use SysAccess;
use DBA;
use myDBI;
use DBUtil;
use cBill;
use CDC;
use MgrTree;
use myConfig;
use uCalc;
my $debug = 0;
#############################################################################
# local gHTML variable: access with $gHTML::varname
$PACNT=0;
$PAMAX=0;
#############################################################################
sub vClient
{ 
  my ($self,$form,$ClientID) = @_;
  my $dbh = myDBI->dbconnect($form->{'DBNAME'});
  my $sClient = $dbh->prepare("select * from Client where ClientID=?");
  $sClient->execute($ClientID) || myDBI->dberror("vClient: $ClientID");
  if ( my $rClient = $sClient->fetchrow_hashref )
  {
    $form->error("Client NOT ASSIGNED TO A CLINIC!")
      if ( $rClient->{'clinicClinicID'} eq '' );
  }
  return();
}
sub vNoteInt
{ 
  my ($self, $form) = @_;

  my $script = qq|
<SCRIPT LANGUAGE="JavaScript" >
techniquearray = new Array(
null,|;
  my $delm1 = '';
  my $dbh = myDBI->dbconnect($form->{'DBNAME'});
  my $idx = 1;
  while ( $idx < 4 )
  {
    $script .= qq|${delm1}\nnew Array(|;
    my $delm2 = '';
    my $q = qq|select * from xNoteInt${idx} order by Descr|;
#warn "  q=$q\n";
    my $s = $dbh->prepare($q);
    $s->execute || myDBI->dberror($q);
    while ( my $r = $s->fetchrow_hashref )
    { $script .= qq|${delm2}\nnew Array(0,$r->{ID},"$r->{Descr}")|; $delm2 = ','; }
    $s->finish();
    $delm1 = qq|\n),|;
    $idx++;
  }
  $script .= qq|\n)\n);
</SCRIPT>
<SCRIPT LANGUAGE="JavaScript" SRC="/cgi/js/fillSelect.js" ></SCRIPT>
|;
#warn qq|script=\n${script}\n|;
  return($script);
}
sub vNoteServiceType
{ 
  my ($self,$form,$ProvID,$ClientID,$ReqAccess) = @_;
  my $ForProvID = $ProvID ? $ProvID : $form->{LOGINPROVID};
  my $dbh = myDBI->dbconnect($form->{'DBNAME'});
# see DBA->selServiceCodes - must match to that function.
  my $qxSC = qq|select xSC.SCID, xSC.SCNum, xInsurance.Name, xSC.SCName, xSC.ServiceType, xCredentials.Abbr, xSCRestrictions.Descr as ResDescr, xSC.Restriction from xSC left join xInsurance on xInsurance.ID=xSC.InsID left join okmis_config.xCredentials on xCredentials.ID=xSC.CredID left join okmis_config.xSCRestrictions on xSCRestrictions.ID=xSC.Restriction where xSC.Active=1 |;
  if ( $ReqAccess =~ /INSID=ALL/i ) { null; }    # allow call for all insurance service codes - ProviderPay
  elsif ( $ReqAccess =~ /INSID=/i )              # allow call for one insurance service codes - xSC, xPAgroups, etc.
  { my ($tag,$InsID) = split('=',$ReqAccess); $qxSC .= qq|and xSC.InsID='${InsID}' |; }
  else
  { $qxSC .= DBA->withCredIDs($form,$ForProvID,'xSC','and').DBA->withClientInsIDs($form,$ClientID,1,'xSC','and'); }
  my $qAll = $qxSC . qq| order by xInsurance.Name, xSC.ServiceType, xSC.SCName, xSC.SCNum|;
  my $a0 = '';          # array 0=everything
  my $delm0 = '';
  my $s = $dbh->prepare($qAll);
  $s->execute() || myDBI->dberror($qAll);
  while ( my $r = $s->fetchrow_hashref )
  { 
    $a0 .= qq|${delm0}\nnew Array(0,$r->{SCID},"$r->{Name} $r->{ServiceType} $r->{SCName} $r->{SCNum} \($r->{Abbr}\) \($r->{ResDescr}\)")|;
    $delm0 = ',';
  }
  $s->finish();
  my $a1 = '';          # arrays 1-n are in groups
  my $delm1 = '';
  my $qSF = qq|select ServiceType from xSC where ServiceType is not null group by ServiceType|;
  my $sSF = $dbh->prepare($qSF);
  $sSF->execute || myDBI->dberror($qSF);
  while ( my ($ServiceType) = $sSF->fetchrow_array )
  {
    $a1 .= qq|${delm1}\nnew Array(|;
    my $delm2 = '';
    my $q = $qxSC . qq| and (ServiceType=? or ServiceType is null) order by xInsurance.Name, xSC.ServiceType, xSC.SCName, xSC.SCNum|;
#warn qq|$ServiceType, q=$q\n|;
    my $s = $dbh->prepare($q);
    $s->execute($ServiceType) || myDBI->dberror($q);
    while ( my $r = $s->fetchrow_hashref )
    { 
      $a1 .= qq|${delm2}\nnew Array(0,$r->{SCID},"$r->{Name} $r->{ServiceType} $r->{SCName} $r->{SCNum} \($r->{Abbr}\) \($r->{ResDescr}\)")|;
      $delm2 = ',';
    }
    $s->finish();
    $delm1 = qq|\n),|;
  }
  $sSF->finish();
  my $script = qq|
<SCRIPT LANGUAGE="JavaScript" >
servicetypearray = new Array(
new Array(
${a0}
),
${a1})
);
</SCRIPT>
<SCRIPT LANGUAGE="JavaScript" SRC="/cgi/js/fillSelect.js" ></SCRIPT>
|;
#warn qq|script=\n${script}\n|;
  return($script);
}
sub setNoteMsg
{
  my ($self, $form) = @_;

  if ( $form->{Treatment_TrID_1} eq '' )
  {
    return(qq|<TABLE CLASS="home fullsize" ><TR ><TD CLASS="strcol" >** New Note</TD></TR></TABLE>|);
  }
  my $dbh = myDBI->dbconnect($form->{'DBNAME'});
  my $ProvName = DBA->getxref($form,'Provider',$form->{'Treatment_ProvID_1'},'FName LName');
  my $EnteredBy = DBA->getxref($form,'Provider',$form->{'Treatment_EnteredBy_1'},'FName LName');
  my $out = qq|
<TABLE CLASS="home fullsize" >
  <TR ><TD CLASS="strcol" >** ChartNote for ${ProvName}, entered by ${EnteredBy} on $form->{Treatment_ChartEntryDate_1}</TD></TR>
|;
  if ( SysAccess->getRule($form,'NoteEdit',$form->{Treatment_ProvID_1}) )
  {
    my $d = $form->{Treatment_ProvOKDate_1};
    my $t = $form->{Treatment_ProvOKTime_1};
    my $msg = $d eq '' ? qq|Not yet approved by ${ProvName}| : qq|OK'd by ${ProvName} on ${d} at ${t}|;
    $out .= qq|
  <TR ><TD CLASS="strcol" >** ChartNote ${msg}</TD></TR>
|;
  }

  my $qSCID = qq|
select xInsurance.Name
  from xSC
  left join xInsurance on xInsurance.ID=xSC.InsID
  where xSC.SCID='$form->{Treatment_SCID_1}'
|;
#warn qq|qSCID=\n$qSCID\n|;
  $sSCID=$dbh->prepare($qSCID);
  $sSCID->execute() || myDBI->dberror($qSCID);
  my ($InsName) = $sSCID->fetchrow_array;
  $sSCID->finish();
  my $InsText = $InsName ? qq|Service for ${InsName} Insurance| : qq|NO INSURANCE!|;
  $out .= qq|  <TR ><TD CLASS="strcol" >** ${InsText}</TD></TR>\n|;

# check for Medication Allergies...
  $sClientIntake=$dbh->prepare("select * from ClientIntake where ClientID='$form->{Treatment_ClientID_1}'");
  $sClientIntake->execute() || myDBI->dberror("setNoteMsg: select ClientIntake $form->{Treatment_ClientID_1}");
  my $rClientIntake = $sClientIntake->fetchrow_hashref;
  my $MAR = $rClientIntake->{MAR} eq '' ?
     '':qq|  <TR ><TD CLASS="strcol" >** Medication Allergies: $rClientIntake->{MAR}</TD></TR>\n|;
  $sClientIntake->finish();

#warn qq|RevDate=$form->{Treatment_MgrRevDate_1}\n|;
  my $msg = qq|New Note.|;
  if ( $form->{Treatment_ClinicID_1} eq '' )
  { $msg = qq|<FONT COLOR=red>NO CLINIC ASSIGNED TO CLIENT</FONT>Notes prohibited!|; }
  elsif ( $form->{Treatment_BillStatus_1} == 9 )
  { $msg = qq|Note has a Recoupment. Please check if rebill is necessary|; }
  elsif ( $form->{Treatment_BillStatus_1} == 8 )
  { $msg = qq|Note has been placed On Hold.|; }
  elsif ( $form->{Treatment_BillStatus_1}  > 6)
  { $msg = qq|Note has been signed by Provider and Billed. Text portion of note cannot be changed.|; }
  elsif ( $form->{Treatment_BillStatus_1} == 6 )
  { $msg = qq|Note has been Denied. Please correct and rebill|; }
  elsif ( $form->{Treatment_BillStatus_1} == 5 )
  { $msg = qq|Note has been Reconciled and cannot be changed.|; }
  elsif ( $form->{Treatment_BillStatus_1} == 4 )
  { $msg = qq|Note has been Scholarshipped and cannot be changed.|; }
  elsif ( $form->{Treatment_BillStatus_1} == 3 )
  { $msg = qq|Note has been Billed and is In Process. It cannot be changed until denied.|; }
  elsif ( $form->{Treatment_RevStatus_1} == 3 )
  { $msg = qq|Note has been Approved and ready for billing.|; }
  elsif ( $form->{Treatment_MgrRevDate_1} )
  { $msg = qq|Note has been reviewed and Locked (to change note must be UNreviewed by Manager).|; }
  elsif ( $form->{Treatment_ProvOKDate_1} )
  { $msg = qq|Note waiting to be reviewed.|; }
  elsif ( $form->{Treatment_TrID_1} )
  { $msg = qq|New Note waiting to be OK'd.|; }
  $out .= qq|
  <TR ><TD CLASS="strcol" >** ${msg}</TD></TR>
  ${MAR}
<\TABLE>
|;
  return($out);
}
sub setNoteRev
{
  my ($self, $form) = @_;

  my $dbh = myDBI->dbconnect($form->{'DBNAME'});
  my $out .= qq|
<TABLE CLASS="home fullsize" >
  <TR >
    <TD CLASS="hdrtxt" WIDTH="16%" >Reviewed</TD>
    <TD CLASS="hdrtxt" WIDTH="16%" >Billed</TD>
    <TD CLASS="hdrtxt" WIDTH="16%" >InProcess</TD>
    <TD CLASS="hdrtxt" WIDTH="16%" >Status</TD>
    <TD CLASS="hdrtxt" WIDTH="16%" >Date</TD>
  </TR>
|;
  my $review = DBA->getxref($form,'Provider',$form->{Treatment_MgrProvID_1},'FName LName');
  my $status = DBA->getxref($form,'xBillStatus',$form->{Treatment_BillStatus_1});
  $out .= qq|
  <TR >
    <TD CLASS="hdrcol" WIDTH="16%" >${review}<BR>$form->{'Treatment_MgrRevDate_1'}</TD>
    <TD CLASS="hdrcol" WIDTH="16%" >$form->{'Treatment_BillDate_1'}</TD>
    <TD CLASS="hdrcol" WIDTH="16%" >$form->{'Treatment_CIPDate_1'}</TD>
    <TD CLASS="hdrcol" WIDTH="16%" >${status}</TD>
    <TD CLASS="hdrcol" WIDTH="16%" >$form->{'Treatment_StatusDate_1'}</TD>
  </TR>
<\TABLE>
|;
  return($out);
}
sub setNoteBillInfo
{
  my ($self,$form,$NoteType) = @_;
 warn qq|setNoteBillInfo: NoteType=$NoteType\n| if ( $debug );;
  my $out = qq|
<TABLE CLASS="home fullsize" >
|;
  my $SCIDSel = DBA->selServiceCodes($form,$form->{'Treatment_SCID_1'},0,$form->{'LOGINPROVID'},$form->{'Client_ClientID_1'},'Agent');
  my $CurType = DBA->getxref($form,'xSC',$form->{Treatment_SCID_1},'Type');
  my $ClinicName = DBA->getxref($form,'Provider',$form->{'Treatment_ClinicID_1'},'Name');
  my $ProvName = DBA->getxref($form,'Provider',$form->{'Treatment_ProvID_1'},'FName LName');
# LOCKED note...unless mine or reviewok or Inprocess/Scholarshipped/Reconciled.
  my $EntBy = $form->{Treatment_EnteredBy_1} == $form->{LOGINPROVID} ? 1 : 0;
  my $MyNote = $form->{Treatment_ProvID_1} == $form->{LOGINPROVID} ? 1 : 0;
  my $RevOK = SysAccess->verify($form,'Privilege=NoteReview');
  my $BillStatus = $form->{Treatment_BillStatus_1};
 warn qq|ClientID=$form->{Treatment_ClientID_1}, TrID=$form->{Treatment_TrID_1}, EntBy=$EntBy, MyNote=$MyNote, RevOK=$RevOK, BS=$BillStatus\n| if ( $debug );;
  my $Locked = ( !$EntBy && !$MyNote && !$RevOK ) || ( $BillStatus == 3 || $BillStatus == 4 || $BillStatus == 5 ) ? 1 : 0;
 warn qq|BillInfo: Locked=$Locked\n| if ( $debug );;
#  my $Locked = $form->{Treatment_BillStatus_1} == 3 || $form->{Treatment_BillStatus_1} == 4 || $form->{Treatment_BillStatus_1} == 5 ? 1 : 0;
  my $BillCnt = 10;     # standard inputs/selects in billing info.
  $Locked = 0 if ( $form->{LOGINPROVID} == 91 );
  if ( ${Locked} )
  {
    my $POS = DBA->getxref($form,'xPOS',$form->{Treatment_POS_1});
    my $SCNum = DBA->getxref($form,'xSC',$form->{Treatment_SCID_1},'SCNum');
    my $Mod4 = DBA->getxref($form,'xSCMod4',$form->{Treatment_Mod4_1},'Descr');
#warn qq| Mod4=$form->{Treatment_Mod4_1}/${Mod4}\n|;
    my $SCName = DBA->getxref($form,'xSC',$form->{Treatment_SCID_1},'SCName');
    my $InsID = DBA->getxref($form,'xSC',$form->{Treatment_SCID_1},'InsID');
    my $InsName = DBA->getxref($form,'xInsurance',$InsID,'Name');
    my $CredID = DBA->getxref($form,'xSC',$form->{Treatment_SCID_1},'CredID');
    my $CredAbbr = DBA->getxref($form,'xCredentials',$CredID,'Abbr');
    my $RestID = DBA->getxref($form,'xSC',$form->{Treatment_SCID_1},'Restriction');
    my $ResDescr = DBA->getxref($form,'xSCRestrictions',$RestID,'Descr');
    my $SCID3 = '';
    if ( $form->{Treatment_SCID3_1} )
    {
      my $SC3Num = DBA->getxref($form,'xSC',$form->{Treatment_SCID3_1},'SCNum');
      my $SC3Name = DBA->getxref($form,'xSC',$form->{Treatment_SCID3_1},'SCName');
      $SCID3 = qq|
  <TR >
    <TD COLSPAN="3" >
      <FONT SIZE=-1" >addon Service Code: ${SC3Num} ${SC3Name}</FONT>
    </TD>
  </TR>
|;
    }
 warn qq|SCName=$SCName,$SCNum, Insurance=$InsID,$InsName\n| if ( $debug );;
 warn qq|CredID=$CredID,$CredAbbr, RestID=$RestID,$ResDescr\n| if ( $debug );;
    $out .= qq|
  <TR >
    <INPUT TYPE="hidden" NAME="Treatment_ClinicID_1" VALUE="$form->{'Treatment_ClinicID_1'}" >
    <TD CLASS="port" COLSPAN=3 >Bill to Clinic: ${ClinicName}</TD>
  </TR>
  <TR >
    <TD CLASS="port" WIDTH="16%" COLSPAN="3" >
      <INPUT TYPE="hidden" NAME="Treatment_ProvID_1" VALUE="$form->{'Treatment_ProvID_1'}" >
      ChartNote for ${ProvName}
    </TD>
  </TR>
  <TR > <TD CLASS="hdrtxt" COLSPAN="3" >Service Code - Service Name</TD> </TR>
  <TR >
    <TD COLSPAN="3" >
      <INPUT TYPE="hidden" NAME="Treatment_SCID_1" VALUE="$form->{Treatment_SCID_1}" > ${InsName} ${SCNum} ${Mod4} ${SCName} (${CredAbbr}) (${ResDescr}) &nbsp;
    </TD>
  </TR>
  ${SCID3}
|;
    if ( $NoteType == 1 || $NoteType == 3 )      # Progress or Electronic
    {
      $out .= qq|
  <TR >
    <TD CLASS="hdrtxt" >Place of Service</TD>
    <TD CLASS="hdrtxt" COLSPAN="2" >Group Size
      <A HREF="http://forms.okmis.com/misdocs/TreatmentNotes_GrpSize.html" TARGET="popup" ONCLICK="window.open('http://forms.okmis.com/misdocs/TreatmentNotes_GrpSize.html', 'popup', 'width=900,height=700,menubar=1,scrollbars=1,toolbar=1,status=1,resizable=1'); return false">explain</A> 
    </TD>
  </TR>
  <TR >
    <TD >
      <INPUT TYPE="hidden" ID="Treatment_POS_1" NAME="Treatment_POS_1" VALUE="$form->{Treatment_POS_1}" > ${POS} &nbsp;
    </TD>
    <TD COLSPAN="2" >
      <INPUT TYPE="hidden" ID="GrpSize" NAME="ProgNotes_GrpSize_1" VALUE="$form->{ProgNotes_GrpSize_1}" > $form->{ProgNotes_GrpSize_1} &nbsp;
    </TD>
  </TR>
|;
    }
    else
    {
      $out .= qq|
  <TR >
    <TD CLASS="hdrtxt" COLSPAN="3" >Place of Service</TD>
  </TR>
  <TR >
    <TD COLSPAN=3 >
      <INPUT TYPE="hidden" ID="Treatment_POS_1" NAME="Treatment_POS_1" VALUE="$form->{Treatment_POS_1}" > ${POS} &nbsp;
    </TD>
  </TR>
|;
    }
    $out .= qq|
  <TR >
    <TD CLASS="hdrtxt" WIDTH="50%" >Date of Service</TD>
    <TD CLASS="hdrtxt" WIDTH="25%" >Beginning Time</TD>
    <TD CLASS="hdrtxt" WIDTH="25%" >Ending Time</TD>
  </TR>
  <TR >
    <TD WIDTH="50%" >
      <INPUT TYPE="hidden" NAME="Treatment_ContLogDate_1" VALUE="$form->{Treatment_ContLogDate_1}" > $form->{Treatment_ContLogDate_1} &nbsp;
    </TD>
    <TD WIDTH="25%" >
      <INPUT TYPE="hidden" NAME="BeginTime" VALUE="$form->{BeginTime}" > $form->{BeginTime} &nbsp;
    </TD>
    <TD WIDTH="25%" >
      <INPUT TYPE="hidden" NAME="EndTime" VALUE="$form->{EndTime}" > $form->{EndTime} &nbsp;
    </TD>
  </TR>
|;
  }
  else                    # Unlocked for input
  {
    if ( SysAccess->verify($form,'Privilege=BillClinic') )
    {
      $out .= qq|
  <TR >
    <TD CLASS="port" WIDTH=16% COLSPAN=3 >
      Bill to Clinic &nbsp; &nbsp;
      <SELECT NAME="Treatment_ClinicID_1" >[[DBA->selClinics(%form++<<Treatment_ClinicID_1>>++1)]]</SELECT>
    </TD>
  </TR>
|;
    }
    else
    {
      $out .= qq|
  <TR >
    <INPUT TYPE="hidden" NAME="Treatment_ClinicID_1" VALUE="$form->{'Treatment_ClinicID_1'}" >
    <TD CLASS="port" COLSPAN=3 >Bill to Clinic: ${ClinicName}</TD>
  </TR>
|;
    }
    if ( SysAccess->verify($form,'Privilege=NoteEntry') )
    {
      $out .= qq|
  <TR >
    <TD CLASS="port" WIDTH="16%" COLSPAN="3" >
      ChartNote for 
      <SELECT ID="ProvID" NAME="Treatment_ProvID_1" ONCHANGE="callAjax('vProvID',this.value,this.id,'&c=$form->{Treatment_ClientID_1}&id=$form->{Treatment_TrID_1}&m='+document.Treatment.Treatment_Mod4_1.value+'&d='+document.Treatment.Treatment_ContLogDate_1.value+'&b='+document.Treatment.Treatment_ContLogBegTime_1.value+'&e='+document.Treatment.Treatment_ContLogEndTime_1.value,'validateNote.pl');" >[[DBA->selProviders(%form+<<Treatment_ProvID_1>>)]]</SELECT>
    </TD>
  </TR>
|;
    }
    else
    {
      $out .= qq|
  <TR >
      <INPUT TYPE="hidden" NAME="Treatment_ProvID_1" VALUE="$form->{'Treatment_ProvID_1'}" > ${ProvName}
    </TD>
  </TR>
|;
    }
    my $ServTypeSel = SysAccess->getRule($form,'NoteServiceType') ? qq|<TR><TD COLSPAN="3" ><SELECT NAME="Treatment_ServiceType" ONCHANGE="setSelect(this,servicetypearray,this.form.Treatment_SCID_1)" > | . DBA->selNoteServiceTypes($form,$form->{Treatment_ServType}) . qq| </SELECT></TD></TR>| : qq|<INPUT TYPE="hidden" NAME="Treatment_ServType" VALUE="$form->{'Treatment_ServType'}" >|;
##    $ServTypeSel = $form->{LOGINID} eq 'root' ? qq|<TR><TD COLSPAN="3" ><SELECT NAME="Treatment_ServiceType" ONCHANGE="setSelect(this,servicetypearray,this.form.Treatment_SCID_1)" > | . DBA->selNoteServiceTypes($form,$form->{Treatment_ServType}) . qq| </SELECT></TD></TR>| : $ServTypeSel;
# Mod4 is add modifier for TeleMedicine: i.e.: GT modifier (from xSCMod4)
    my $Mod4 = $form->{'Treatment_Mod4_1'};
    my $Mod4Sel = SysAccess->chkPriv($form,'TeleMedicine',$form->{'Treatment_ProvID_1'}) ?
                  qq|<SELECT DISABLED NAME="Treatment_Mod4_1" >|
                    .DBA->selxTable($form,'xSCMod4',$Mod4).qq|</SELECT>|
                : qq|<INPUT TYPE="hidden" NAME="Treatment_Mod4_1" VALUE="${Mod4}" >|;
    my $POSSel = DBA->selxTable($form,'xPOS',$form->{'Treatment_POS_1'});
    my $SCID3 = '';
    if ( $form->{Treatment_SCID3_1} )
    {
      my $SC3Num = DBA->getxref($form,'xSC',$form->{Treatment_SCID3_1},'SCNum');
      my $SC3Name = DBA->getxref($form,'xSC',$form->{Treatment_SCID3_1},'SCName');
      $SCID3 = qq|
  <TR >
    <TD COLSPAN="3" >
      <FONT SIZE=-1" >addon Service Code: ${SC3Num} ${SC3Name}</FONT>
    </TD>
  </TR>
|;
    }
    $out .= qq|
  <TR >
    <TD CLASS="hdrtxt" COLSPAN="3" >Service Code - Service Name</TD>
  </TR>
  ${ServTypeSel}
  <TR >
    <TD COLSPAN="3" >
      <SELECT ID="SCID" NAME="Treatment_SCID_1" ONCHANGE="callAjax('vSCID',this.value,this.id,'&p='+document.Treatment.Treatment_ProvID_1.value+'&c=$form->{Treatment_ClientID_1}&id=$form->{Treatment_TrID_1}&d='+document.Treatment.Treatment_ContLogDate_1.value+'&b='+document.Treatment.Treatment_ContLogBegTime_1.value+'&e='+document.Treatment.Treatment_ContLogEndTime_1.value,'validateNote.pl');" >${SCIDSel}</SELECT>
      <INPUT TYPE="hidden" ID="CurType" NAME="CurType" VALUE="${CurType}" >
    </TD>
  </TR>
  <TR> <TD COLSPAN="3" ><SPAN ID="Mod4_popup">${Mod4Sel}</SPAN></TD> </TR>
  ${SCID3}
|;
    if ( $NoteType == 1 || $NoteType == 3 )
    {
      $out .= qq|
  <TR >
    <TD CLASS="hdrtxt" >Place of Service</TD>
    <TD CLASS="hdrtxt" COLSPAN="2" >Group Size
      <A HREF="http://forms.okmis.com/misdocs/TreatmentNotes_GrpSize.html" TARGET="popup" ONCLICK="window.open('http://forms.okmis.com/misdocs/TreatmentNotes_GrpSize.html', 'popup', 'width=900,height=700,menubar=1,scrollbars=1,toolbar=1,status=1,resizable=1'); return false">explain</A> 
    </TD>
  </TR>
  <TR >
    <TD >
      <SELECT ID="Treatment_POS_1" NAME="Treatment_POS_1" > ${POSSel} </SELECT> 
    </TD>
    <TD COLSPAN="2" >
      <INPUT TYPE="text" ID="GrpSize" NAME="ProgNotes_GrpSize_1" VALUE="$form->{ProgNotes_GrpSize_1}" SIZE="5" ONFOCUS="select();" ONCHANGE="callAjax('vGrpSize',this.value,this.id,'&ct='+document.Treatment.CurType.value,'validateNote.pl');" >
    </TD>
  </TR>
|;
    }
    else
    {
      $out .= qq|
  <TR >
    <TD CLASS="hdrtxt" COLSPAN="3" >Place of Service</TD>
  </TR>
  <TR >
    <TD COLSPAN=3 >
      <SELECT ID="Treatment_POS_1" NAME="Treatment_POS_1" > ${POSSel} </SELECT> 
    </TD>
  </TR>
|;
    }
    $out .= qq|
  <TR >
    <TD CLASS="hdrtxt" WIDTH="50%" >Date of Service</TD>
    <TD CLASS="hdrtxt" WIDTH="25%" >Beginning Time</TD>
    <TD CLASS="hdrtxt" WIDTH="25%" >Ending Time</TD>
  </TR>
  <TR >
    <TD WIDTH="50%" >
      <A HREF="javascript:show_calendar('Treatment.Treatment_ContLogDate_1');" onmouseover="window.status='Calendar to select date';return true;" onmouseout="window.status='';return true;">
        <IMG SRC="/images/show_calendar.gif" ALT="show calendar" WIDTH="24" HEIGHT="22" BORDER="0">
      </A>
      <INPUT TYPE="text" ID="ContDate" NAME="Treatment_ContLogDate_1" VALUE="$form->{Treatment_ContLogDate_1}" SIZE="15" ONFOCUS="select();" ONCHANGE="callAjax('vContDate',this.value,this.id,'&p='+document.Treatment.Treatment_ProvID_1.value+'&c=$form->{Treatment_ClientID_1}&id=$form->{Treatment_TrID_1}&s='+document.Treatment.Treatment_SCID_1.value+'&b='+document.Treatment.Treatment_ContLogBegTime_1.value+'&e='+document.Treatment.Treatment_ContLogEndTime_1.value,'validateNote.pl');" >
    </TD>
    <TD WIDTH="25%" >
      <INPUT TYPE="text" ID="BeginTime" NAME="BeginTime" VALUE="$form->{BeginTime}" SIZE="15" ONFOCUS="select();" ONCHANGE="callAjax('vContTime',this.value,this.id,'&p='+document.Treatment.Treatment_ProvID_1.value+'&c=$form->{Treatment_ClientID_1}&id=$form->{Treatment_TrID_1}&s='+document.Treatment.Treatment_SCID_1.value+'&d='+document.Treatment.Treatment_ContLogDate_1.value+'&t='+document.Treatment.Treatment_ContLogEndTime_1.value,'validateNote.pl');" >
    </TD>
    <TD WIDTH="25%" >
      <INPUT TYPE="text" ID="EndTime" NAME="EndTime" VALUE="$form->{EndTime}" SIZE="15" ONFOCUS="select();" ONCHANGE="callAjax('vContTime',this.value,this.id,'&p='+document.Treatment.Treatment_ProvID_1.value+'&c=$form->{Treatment_ClientID_1}&id=$form->{Treatment_TrID_1}&s='+document.Treatment.Treatment_SCID_1.value+'&d='+document.Treatment.Treatment_ContLogDate_1.value+'&t='+document.Treatment.Treatment_ContLogBegTime_1.value,'validateNote.pl');" >
    </TD>
  </TR>
|;
    my $BTime = gHTML->ifld($form,'Treatment_ContLogBegTime_1','displayonly');
    my $ETime = gHTML->ifld($form,'Treatment_ContLogEndTime_1','displayonly');
    $out .= qq|
  <TR >
    <TD WIDTH="50%" >&nbsp;</TD>
    <TD WIDTH="25%" >${BTime}</TD>
    <TD WIDTH="25%" >${ETime}</TD>
  </TR>
|;
    # Rebill Note Privilege?
 warn qq|BEFORE REBILL...\n| if ( $debug );;
    if ( SysAccess->verify($form,'Privilege=RebillNote') )
    {
 warn qq|INSIDE REBILL...\n| if ( $debug );;
      $out .= qq|
</TABLE>
<TABLE CLASS="main fullsize" >
  <TR >
    <TD CLASS="numcol" >
|;
 warn qq|BillStatus=$form->{Treatment_Billstatus_1}\n| if ( $debug );
      # Rebill note...check for something that shows it was denied...gone thru billing process.
      if ( $form->{Treatment_BillStatus_1} > 5 )
      { $out .= qq|      <INPUT TYPE="submit" NAME="Treatment_BillStatus_1=1&Treatment_StatusDate_1=$form->{TODAY}&Treatment_CIPDate_1=&Treatment_DenDate_1=&Treatment_DenCode_1=&UpdateTables=all&rebill_note=1&misPOP=1" VALUE="Update/Rebill" > |; $BillCnt++; }
      # Scholarship only if denied or more and AmtDue left, not if set to bill/rebill.
      # NO: write off anything? even a new note that will not be billed(0) or is not billable(2), even AmtDue=0 (NonBill).
      if ( $form->{Treatment_BillStatus_1} < 3 || $form->{Treatment_BillStatus_1} > 5 )
      { $out .= qq|      <INPUT TYPE="submit" NAME="scholarship_note=1&misPOP=1" VALUE="Scholarship" >|; $BillCnt++;}
    }
  $out .= qq|
    </TD>
  </TR>
|;
  }
  $BillCnt++;     # add 1 for this hidden input.
  $out .= qq|
<INPUT TYPE="hidden" NAME="BillCnt" VALUE="$BillCnt" >
</TABLE>
|;
  return($out);
}
sub setNoteTrPlan
{ 
  my ($self, $form) = @_;
  my $out = '';
  my $ClientID = $form->{'Treatment_ClientID_1'};
  my $TrID = $form->{'Treatment_TrID_1'};
  my $ContDate = $form->{'Treatment_ContLogDate_1'};
# LOCKED note...unless mine or reviewok or Billed/Unreviewed (to change a reviewed note then first unreview).
  my $EntBy = $form->{Treatment_EnteredBy_1} == $form->{LOGINPROVID} ? 1 : 0;
  my $MyNote = $form->{Treatment_ProvID_1} == $form->{LOGINPROVID} ? 1 : 0;
  my $RevOK = SysAccess->verify($form,'Privilege=NoteReview');
  my $BillStatus = $form->{Treatment_BillStatus_1};
#warn qq|ClientID=$form->{Treatment_ClientID_1}, TrID=$form->{Treatment_TrID_1}, EntBy=$EntBy, MyNote=$MyNote, RevOK=$RevOK, BS=$BillStatus\n|;
  my $Locked = ( !$EntBy && !$MyNote && !$RevOK ) || ( $BillStatus == 3 || $BillStatus == 4 || $BillStatus == 5 ) ? 1 : 0;
#warn qq|NoteTrPlan: Locked=$Locked\n|;
#warn qq|NoteTrPlan: ContDate=$form->{'Treatment_ContLogDate_1'}\n|;
  $Locked = 0 if ( $form->{LOGINPROVID} == 91 );

  my $arrowdown = myConfig->cfgfile('arrow_down.png',1);
  $out .= qq|
<TABLE CLASS="home fullsize" >
  <TR >
    <TD CLASS="port" >
      Problems Addressed
      <A HREF="javascript:InputWindow('/cgi/bin/mis.cgi?view=ListClientProblems.cgi&Client_ClientID=${ClientID}&mlt=$form->{mlt}&misLINKS=$form->{misLINKS}&NONAVIGATION=1','linkproblems',900,1200)"; return true; >Add/Update PROBLEMS</A>
    </TD>
    <TD CLASS="port numcol" >
      <A HREF="javascript:callAjax('ListClientNoteProblems','','ProblemsList','&id=${id}&Client_ClientID=${ClientID}&Treatment_TrID=${TrID}&Locked=${Locked}&LOGINPROVID=$form->{LOGINPROVID}&LOGINUSERID=$form->{LOGINUSERID}&LOGINUSERDB=$form->{LOGINUSERDB}&mlt=$form->{mlt}&misLINKS=$form->{misLINKS}&LINKID=$form->{LINKID}&d='+document.Treatment.Treatment_ContLogDate_1.value,'popup.pl');" TITLE="refresh problem list">Refresh<IMG SRC="${arrowdown}" HEIGHT="20" WIDTH="20" ></A>
    </TD>
  </TR>
  <TR >
    <TD CLASS="port" COLSPAN="2" >
      <SPAN ID="ProblemsList" >
|.$self->setClientNoteProblems($form,$Locked,$ClientID,$TrID,$ContDate).qq|
      </SPAN>
    </TD>
  </TR>
</TABLE>|;
  $out .= qq|
<TABLE CLASS="home fullsize" >
  <TR >
    <TD CLASS="port" COLSPAN="2" >
      <SPAN ID="ProblemsGoals" >
|.$self->setClientNoteTrPlanPG($form,$Locked,$ClientID,$TrID,$ContDate).qq|
      </SPAN>
    </TD>
  </TR>
</TABLE>|;
  $out .= qq|
<TABLE CLASS="home fullsize" >
  <TR >
    <TD CLASS="port" COLSPAN="2" >
      <SPAN ID="ClientFamilyP" >
|.$self->setClientNoteFamilyP($form,$Locked,$ClientID,$TrID).qq|
      </SPAN>
    </TD>
  </TR>
</TABLE>|;
  return($out);

  my $TrProbNum = $form->{'Treatment_ProbNum_1'};
  my $ContDate = 'curdate()';
  if ( $form->{'Treatment_ContLogDate_1'} )
  { $ContDate = "'" . $form->{'Treatment_ContLogDate_1'} . "'"; }
  my $dbh = myDBI->dbconnect($form->{'DBNAME'});
  my $q = qq|
select TrPlanIP.* from TrPlanIP
    left join TrPlan on TrPlan.TrPlanID=TrPlanIP.TrPlanID
    left join ClientPrAuth on ClientPrAuth.ID=TrPlan.PrAuthID
  where TrPlan.ClientID=$form->{'Client_ClientID_1'}
    and ${ContDate} between ClientPrAuth.EffDate and ClientPrAuth.ExpDate
    and (ClientPrAuth.PAgroup NOT LIKE 'G%' or ClientPrAuth.PAgroup is NULL)
  order by TrPlanIP.ProbNum
|;
#warn "setNoteTrPlan: TrProbNum=$TrProbNum\nq=\n$q\n";
  my $header = ${Locked} ? 'Problems addressed' : 'Check all problems addressed';
  my $blur = $Locked ? qq|ONCLICK="return vUNDO(this,'Note has been locked.');" | : '';
  $out .= qq|
<TABLE CLASS="home fullsize" >
  <TR ><TD CLASS="hdrtxt" COLSPAN="2" >Treatment Plan Problems Addressed</TD></TR>
  <TR >
    <TD CLASS="hdrcol" WIDTH=10% >${header}</TD>
    <TD CLASS="strcol" ><UL><LI>Problem</LI><LI TYPE="square">Goal<UL><LI>Objectives</LI></UL></LI></UL></TD>
  </TR>
|;
  my @alpha = ('','a','b','c','d','e','f');
  my $s = $dbh->prepare($q);
  $s->execute || myDBI->dberror($q);
  my ($ProbCnt, $Bit) = (0,1); 
  while ( my $r = $s->fetchrow_hashref )
  {
    $ProbCnt++;
    my $Prob = $r->{Prob};
    my $ProbNum = $r->{ProbNum};
    my $Goal = $r->{Goal};
    my $Checked = $TrProbNum & $Bit ? 'CHECKED' : '';
    $Bit *= 2;
    $out .= qq|
  <TR >
    <TD CLASS="hdrcol" WIDTH="10%" >
      ${ProbNum} <INPUT TYPE="checkbox" ID="ProbAddrd" NAME="ProbAddrd${ProbCnt}" VALUE="1" ${Checked} ${blur} >
    </TD>
    <TD CLASS="strcol" WIDTH="90%" >
      <UL>
        <LI>${Prob}</LI>
        <LI TYPE="square" >${Goal}
          <UL>
|;
    for (my $i=1; $i<=6; $i++)
    {
      my $ltr = @alpha[$i];
      my $obj = $r->{'Obj'.$i};
      unless ( $obj eq '' )
      {
          $out .= qq|
            <LI>${ProbNum}${ltr}: ${obj}</LI>|;
      }
    }
    $out .= qq|
          </UL>
        </LI>
      </UL>
    </TD>
  </TR>
|;
  }
  $s->finish();
  $out .= qq|</TABLE>|;
  return($out);
}
sub setNoteTxt
{
  my ($self, $form, $NoteType) = @_;
  my $out = '';
# LOCKED note...unless mine or reviewok or Billed/Unreviewed (to change a reviewed note then first unreview).
  my $EntBy = $form->{Treatment_EnteredBy_1} == $form->{LOGINPROVID} ? 1 : 0;
  my $MyNote = $form->{Treatment_ProvID_1} == $form->{LOGINPROVID} ? 1 : 0;
  my $RevOK = SysAccess->verify($form,'Privilege=NoteReview');
  my $BillStatus = $form->{Treatment_BillStatus_1};
#warn qq|ClientID=$form->{Treatment_ClientID_1}, TrID=$form->{Treatment_TrID_1}, EntBy=$EntBy, MyNote=$MyNote, RevOK=$RevOK, BS=$BillStatus\n|;
#foreach my $f ( sort keys %{$form} ) { warn "form: $f=$form->{$f}\n"; }
  #my $Locked = ( !$EntBy && !$MyNote && !$RevOK ) || ( $BillStatus > 0 || $form->{Treatment_MgrRevDate_1} ) ? 1 : 0;
  my $Locked = ( !$EntBy && !$MyNote && !$RevOK ) || ( $BillStatus == 3 || $BillStatus == 4 || $BillStatus == 5 ) ? 1 : 0;
#warn qq|NoteTxt: Locked=$Locked\n|;
#  my $Locked = $form->{Treatment_BillStatus_1} > 0 || $form->{Treatment_MgrRevDate_1} ? 1 : 0;
  $Locked = 0 if ( $form->{LOGINPROVID} == 91 );
  if    ( $NoteType == 1 ) { $out .= gHTML->setNoteTxt1($form,$Locked); }         # Progress
#  elsif ( $NoteType == 2 ) { $out .= gHTML->setNoteTxt2($form,$Locked); }         # Physician
  elsif ( $NoteType == 3 ) { $out .= gHTML->setNoteTxt3($form,$Locked); }         # Electronic
  elsif ( $NoteType == 4 ) { $out .= gHTML->setNoteTxt4($form,$Locked); }         # Medicare
  elsif ( $NoteType == 5 ) { $out .= gHTML->setNoteTxt5($form,$Locked); }         # TFC
  return($out);
}
sub setNoteTxt1
{
  my ($self, $form, $Locked) = @_;
  my $out = $self->setIntComp($form,$Locked);
  $out .= qq|
<TABLE CLASS="home fullsize" >
  <TR ><TD CLASS="port hdrtxt" >Methods Used to Address Problems<BR>(What techniques or activities were used to work on problems?)</TD></TR>
  <TR>
    <TD >
|;
  $out .= ${Locked} 
    ? qq|<INPUT TYPE="hidden" NAME="ProgNotes_Methods_1" VALUE="<<ProgNotes_Methods_1>>" > <<ProgNotes_Methods_1>> &nbsp;|
    : qq|<TEXTAREA COLS="140" ROWS="5" WRAP="virtual" NAME="ProgNotes_Methods_1" ><<ProgNotes_Methods_1>></TEXTAREA>|;
  $out .= qq|
    </TD>
  </TR>
  <TR ><TD CLASS="port hdrtxt" >Progress Made Towards Treatment Goals<BR>(include client's response)</TD></TR>
  <TR>
    <TD >
|;
  $out .= ${Locked} 
    ? qq|<INPUT TYPE="hidden" NAME="ProgNotes_Progress_1" VALUE="<<ProgNotes_Progress_1>>" > [[DBA->getxref(%form+xProgress+<<ProgNotes_Progress_1>>)]] &nbsp;|
    : qq|<SELECT NAME="ProgNotes_Progress_1" >[[DBA->selxTable(%form+xProgress+<<ProgNotes_Progress_1>>)]]</SELECT> |;
  $out .= qq|
    </TD>
  </TR>
  <TR>
    <TD >
|;
  $out .= ${Locked} 
    ? qq|<INPUT TYPE="hidden" NAME="ProgNotes_ProgEvidence_1" VALUE="<<ProgNotes_ProgEvidence_1>>" > <<ProgNotes_ProgEvidence_1>> &nbsp;|
    : qq|<TEXTAREA COLS="140" ROWS="5" WRAP="virtual" NAME="ProgNotes_ProgEvidence_1" ><<ProgNotes_ProgEvidence_1>></TEXTAREA>|;
  $out .= qq|
    </TD>
  </TR>
  <TR ><TD CLASS="port hdrtxt" >Description of Crisis<BR>(For 'Crisis Intervention' Notes Only)</TD></TR>
  <TR>
    <TD >
|;
  $out .= ${Locked} 
    ? qq|<INPUT TYPE="hidden" NAME="ProgNotes_CrisisText_1" VALUE="<<ProgNotes_CrisisText_1>>" > <<ProgNotes_CrisisText_1>> &nbsp;|
    : qq|<TEXTAREA COLS="140" ROWS="5" WRAP="virtual" NAME="ProgNotes_CrisisText_1" ><<ProgNotes_CrisisText_1>></TEXTAREA>|;
  $out .= qq|
    </TD>
  </TR>
  <TR ><TD CLASS="port" >Level of Functioning GAF</TD></TR>
  <TR>
    <TD >
|;
  $out .= ${Locked} 
    ? qq|Current:&nbsp;&nbsp; <INPUT TYPE="hidden" NAME="ProgNotes_GAFCurrent_1" VALUE="<<ProgNotes_GAFCurrent_1>>" > <<ProgNotes_GAFCurrent_1>> &nbsp; &nbsp;&nbsp; Recent Past:&nbsp;&nbsp; <INPUT TYPE="hidden" NAME="ProgNotes_GAFRecent_1" VALUE="<<ProgNotes_GAFRecent_1>>" > <<ProgNotes_GAFRecent_1>> &nbsp;|
    : qq|Current:&nbsp;&nbsp; <INPUT TYPE="text" SIZE="5" NAME="ProgNotes_GAFCurrent_1" VALUE="<<ProgNotes_GAFCurrent_1>>" ONCHANGE="return vNum(this,0,100);" > &nbsp;&nbsp; Recent Past:&nbsp;&nbsp; <INPUT TYPE="text" SIZE="5" NAME="ProgNotes_GAFRecent_1" VALUE="<<ProgNotes_GAFRecent_1>>" ONCHANGE="return vNum(this,0,100);" >|;
  $out .= qq|
    </TD>
  </TR>
</TABLE>
|;
  if ( $form->{'Treatment_ProvID_1'} == $form->{'LOGINPROVID'} )
  {
    my $Therapy .= ${Locked} 
      ? qq|<INPUT TYPE="hidden" NAME="ClientTherapyNotes_Psychotherapy_1" VALUE="<<ClientTherapyNotes_Psychotherapy_1>>" > <<ClientTherapyNotes_Psychotherapy_1>> &nbsp;|
      : qq|<TEXTAREA COLS="140" ROWS="5" WRAP="virtual" NAME="ClientTherapyNotes_Psychotherapy_1" ><<ClientTherapyNotes_Psychotherapy_1>></TEXTAREA>|;
    $out .=qq|
<TABLE CLASS="home fullsize" >
  <TR ><TD CLASS="port hdrtxt" >Psychotherapy note<BR>(HIPAA 45.CFR. Section 164.501)</TD></TR>
  <TR><TD >${Therapy}</TD></TR>
</TABLE>
|;
  }
  return($out);
}
sub setNoteTxt3
{
  my ($self, $form, $Locked) = @_;
  my $html = '';
  $html .= $self->setSCID2($form,$Locked);
  $html .= $self->setIntComp($form,$Locked);
# XXX
#===== ASSESSMENT SECTION ==========================
  $html .= qq|
<HR WIDTH="90%" >
<TABLE CLASS="home fullsize" >
  <TR ><TD CLASS="port hdrtxt" COLSPAN="2" >ASSESSMENT SECTION</TD></TR>
    <TD COLSPAN="2" >
      <INPUT TYPE="checkbox" NAME="Treatment_EdPerformed_1" VALUE="1" <<Treatment_EdPerformed_1=checkbox>> >
      Patient Education Performed
    </TD>
  </TR>
</TABLE>|;
  return($html);
}
sub setNoteTxt4
{
  my ($self, $form, $Locked) = @_;
  my $out = '';
  $out .= $self->setIntComp($form,$Locked);
  $out .= qq|
<TABLE CLASS="home fullsize" >
  <TR ><TD CLASS="port hdrtxt" >Content/Topics Discussed</TD></TR>
  <TR>
    <TD CLASS="strcol" >
|;
  $out .= ${Locked} 
    ? qq|<INPUT TYPE="hidden" NAME="ProgNotes_Methods_1" VALUE="<<ProgNotes_Methods_1>>" > <<ProgNotes_Methods_1>> &nbsp;|
    : qq|<TEXTAREA COLS="140" ROWS="5" WRAP="virtual" NAME="ProgNotes_Methods_1" ><<ProgNotes_Methods_1>></TEXTAREA>|;
  $out .= qq|
    </TD>
  </TR>
  <TR>
    <TD CLASS="strcol" >
|;
  $out .= ${Locked} 
    ? qq|Intervention: [[DBA->getxref(%form+xNoteInt+<<ProgNotes_Intervention_1>>)]] &nbsp; <INPUT TYPE="hidden" NAME="ProgNotes_Intervention_1" VALUE="<<ProgNotes_Intervention_1>>" > |
    : qq|INTERVENTION: <SELECT NAME="ProgNotes_Intervention_1" ONCHANGE="fillSelect(this,techniquearray,this.form.ProgNotes_Techniques_1)" >[[DBA->selxTable(%form+xNoteInt+<<ProgNotes_Intervention_1>>]]</SELECT> |;
  $out .= qq|
    </TD>
  </TR>
  <TR>
    <TD CLASS="strcol" >
|;
  my $Techs = '<BR>' . DBA->matchNoteInt($form,$form->{'ProgNotes_Intervention_1'},$form->{'ProgNotes_Techniques_1'});
  $Techs =~ s/;/<BR>/g;
  $out .= ${Locked} 
    ? qq|Specific Technique(s): ${Techs} &nbsp; <INPUT TYPE="hidden" NAME="ProgNotes_Techniques_1" VALUE="<<ProgNotes_Techniques_1>>" >|
    : qq|SPECIFIC TECHNIQUE(S): <SELECT NAME="ProgNotes_Techniques_1" MULTIPLE SIZE=10 > [[DBA->selxNoteInt(%form+<<ProgNotes_Intervention_1>>+<<ProgNotes_Techniques_1>>)]] </SELECT> |;
  $out .= qq|
    </TD>
  </TR>
  <TR ><TD CLASS="port hdrtxt" >Progress Made Towards Treatment Goals</TD></TR>
  <TR>
    <TD >
|;
  $out .= ${Locked} 
    ? qq|[[DBA->getxref(%form+xProgress+<<ProgNotes_Progress_1>>)]] &nbsp; <INPUT TYPE="hidden" NAME="ProgNotes_Progress_1" VALUE="<<ProgNotes_Progress_1>>" >|
    : qq|<SELECT NAME="ProgNotes_Progress_1" >[[DBA->selxTable(%form+xProgress+<<ProgNotes_Progress_1>>)]]</SELECT>|;
  $out .= qq|
    </TD>
  </TR>
  <TR ><TD CLASS="port hdrtxt" >Specify how Intervention was used to Assist the Patient in Reaching Treatment Goal</TD></TR>
  <TR>
    <TD CLASS="strcol" >
|;
  $out .= ${Locked} 
    ? qq|<INPUT TYPE="hidden" NAME="ProgNotes_ProgEvidence_1" VALUE="<<ProgNotes_ProgEvidence_1>>" > <<ProgNotes_ProgEvidence_1>> &nbsp;|
    : qq|<TEXTAREA COLS="140" ROWS="5" WRAP="virtual" NAME="ProgNotes_ProgEvidence_1" ><<ProgNotes_ProgEvidence_1>></TEXTAREA>|;
  $out .= qq|
    </TD>
  </TR>
  <TR ><TD CLASS="port hdrtxt" >Description Of Crisis<BR>(For 'Crisis Intervention' Notes Only)</TD></TR>
  <TR>
    <TD CLASS="strcol" >
|;
  $out .= ${Locked} 
    ? qq|<INPUT TYPE="hidden" NAME="ProgNotes_CrisisText_1" VALUE="<<ProgNotes_CrisisText_1>>" > <<ProgNotes_CrisisText_1>> &nbsp;|
    : qq|<TEXTAREA COLS="140" ROWS="5" WRAP="virtual" NAME="ProgNotes_CrisisText_1" ><<ProgNotes_CrisisText_1>></TEXTAREA>|;
  $out .= qq|
    </TD>
  </TR>
  <TR>
    <TD CLASS="strcol" >
|;
  $out .= ${Locked} 
    ? qq|Current:&nbsp;&nbsp; <INPUT TYPE="hidden" NAME="ProgNotes_GAFCurrent_1" VALUE="<<ProgNotes_GAFCurrent_1>>" > <<ProgNotes_GAFCurrent_1>> &nbsp; &nbsp;&nbsp; Recent Past (last 30 days):&nbsp;&nbsp; <INPUT TYPE="hidden" NAME="ProgNotes_GAFRecent_1" VALUE="<<ProgNotes_GAFRecent_1>>" > <<ProgNotes_GAFRecent_1>> &nbsp;|
    : qq|Level of Functioning GAF CURRENT:&nbsp;&nbsp; <INPUT TYPE="text" SIZE="5" NAME="ProgNotes_GAFCurrent_1" VALUE="<<ProgNotes_GAFCurrent_1>>" ONCHANGE="return vNum(this,0,100);" > &nbsp;&nbsp; Recent Past (last 30 days):&nbsp;&nbsp; <INPUT TYPE="text" SIZE="5" NAME="ProgNotes_GAFRecent_1" VALUE="<<ProgNotes_GAFRecent_1>>" ONCHANGE="return vNum(this,0,100);" >|;
  $out .= qq|
    </TD>
  </TR>
</TABLE>
|;
  if ( $form->{'Treatment_ProvID_1'} == $form->{'LOGINPROVID'} )
  {
    my $Therapy .= ${Locked} 
      ? qq|<INPUT TYPE="hidden" NAME="ClientTherapyNotes_Psychotherapy_1" VALUE="<<ClientTherapyNotes_Psychotherapy_1>>" > <<ClientTherapyNotes_Psychotherapy_1>> &nbsp;|
      : qq|<TEXTAREA COLS="140" ROWS="5" WRAP="virtual" NAME="ClientTherapyNotes_Psychotherapy_1" ><<ClientTherapyNotes_Psychotherapy_1>></TEXTAREA>|;
    $out .=qq|
<TABLE CLASS="home fullsize" >
  <TR ><TD CLASS="port hdrtxt" >Psychotherapy note<BR>(HIPAA 45.CFR. Section 164.501)</TD></TR>
  <TR><TD >${Therapy}</TD></TR>
</TABLE>
|;
  }
  return($out);
}
sub setNoteTxt5      # return null
{
  my ($self, $form, $Locked) = @_;
  my $out = '';
  return($out);
}
sub setSCID2
{
  my ($self, $form, $Locked) = @_;
  my $out = qq|
<TABLE CLASS="home fullsize" >
  <TR >
    <TD CLASS="hdrtxt" COLSPAN="3" >Secondary Service Code - Service Name</TD>
  </TR>
|;
  if ( $Locked )
  {
    my $SCNum = DBA->getxref($form,'xSC',$form->{Treatment_SCID2_1},'SCNum');
    my $Mod4 = DBA->getxref($form,'xSCMod4',$form->{Treatment_Mod4_1},'Descr');
#warn qq| Mod4=$form->{Treatment_Mod4_1}/${Mod4}\n|;
    my $SCName = DBA->getxref($form,'xSC',$form->{Treatment_SCID2_1},'SCName');
    my $InsID = DBA->getxref($form,'xSC',$form->{Treatment_SCID2_1},'InsID');
    my $InsName = DBA->getxref($form,'xInsurance',$InsID,'Name');
    my $CredID = DBA->getxref($form,'xSC',$form->{Treatment_SCID2_1},'CredID');
    my $CredAbbr = DBA->getxref($form,'xCredentials',$CredID,'Abbr');
    my $RestID = DBA->getxref($form,'xSC',$form->{Treatment_SCID2_1},'Restriction');
    my $ResDescr = DBA->getxref($form,'xSCRestrictions',$RestID,'Descr');
    $out .= qq|
  <TR >
    <TD >
      <INPUT TYPE="hidden" NAME="Treatment_SCID2_1" VALUE="$form->{Treatment_SCID2_1}" > ${InsName} ${SCNum} ${Mod4} ${SCName} (${CredAbbr}) (${ResDescr}) &nbsp;
    </TD>
  </TR>
|;
  }
  else
  {
    my $SCIDSel = DBA->selServiceCodes($form,$form->{'Treatment_SCID2_1'},0,$form->{'LOGINPROVID'},$form->{'Client_ClientID_1'},'Agent',"and xSC.SCNum NOT LIKE 'X%'");
    $out .= qq|
  <TR >
    <TD >
      <SELECT NAME="Treatment_SCID2_1" > ${SCIDSel} </SELECT> 
    </TD>
  </TR>
|;
  }
  $out .= qq|</TABLE>|;
  return($out);
}
sub setIntComp
{
  my ($self, $form, $Locked, $inClientID, $inProvID) = @_;
  my $ProvID = $inProvID ? $inProvID : $form->{'Client_ProvID_1'};
  my $isSet = $form->{'Treatment_Maladaptive_1'}
           || $form->{'Treatment_Interfere_1'}
           || $form->{'Treatment_Sentinel_1'}
           || $form->{'Treatment_PlayOvercome_1'} ? 1 : 0;
  my $LoginProvID = DBA->isIndividual($form,$form->{'LOGINPROVID'});
  my $IndPrimaryProvID = DBA->isIndividual($form,$form->{'Client_ProvID_1'});
#warn qq|LOGINPROVID=$form->{LOGINPROVID}, ProvID=$form->{Client_ProvID_1}\n|;
#warn qq|isSet=$isSet, LoginProvID=$LoginProvID, IndPrimaryProvID=$IndPrimaryProvID\n|;
  return('') unless ( $isSet || $LoginProvID || $IndPrimaryProvID );
  my $out = qq|
<TABLE CLASS="home fullsize" >
  <TR ><TD CLASS="port hdrtxt" COLSPAN="2" >Interactive Complexity</TD></TR>
  <TR>
    <TD CLASS="strcol" >|;
  $out .= ${Locked} 
    ? qq| <INPUT TYPE="hidden" NAME="Treatment_Maladaptive_1" VALUE="<<Treatment_Maladaptive_1>>" > <<Treatment_Maladaptive_1>>| 
    : qq| <INPUT TYPE="checkbox" NAME="Treatment_Maladaptive_1" VALUE="1" <<Treatment_Maladaptive_1=checkbox>> >|;
  $out .= qq|
    </TD>
    <TD CLASS="strcol" >
      1. The need to manage maladaptive communication (related to, e.g., high anxiety, high reactivity, repeated questions, or disagreement) among participants that complicates delivery of care.
    </TD>
  </TR>
  <TR>
    <TD CLASS="strcol" >|;
  $out .= ${Locked} 
    ? qq| <INPUT TYPE="hidden" NAME="Treatment_Interfere_1" VALUE="<<Treatment_Interfere_1>>" > <<Treatment_Interfere_1>>| 
    : qq| <INPUT TYPE="checkbox" NAME="Treatment_Interfere_1" VALUE="1" <<Treatment_Interfere_1=checkbox>> >|;
  $out .= qq|
    </TD>
    <TD CLASS="strcol" >
      2. Caregiver emotions or behaviors that interfere with implementation of the treatment plan.
    </TD>
  </TR>
  <TR>
    <TD CLASS="strcol" >|;
  $out .= ${Locked} 
    ? qq| <INPUT TYPE="hidden" NAME="Treatment_Sentinel_1" VALUE="<<Treatment_Sentinel_1>>" > <<Treatment_Sentinel_1>>| 
    : qq| <INPUT TYPE="checkbox" NAME="Treatment_Sentinel_1" VALUE="1" <<Treatment_Sentinel_1=checkbox>> >|;
  $out .= qq|
    </TD>
    <TD CLASS="strcol" >
      3. Evidence or disclosure of a sentinel event and mandated report to a third party (e.g., abuse or neglect with report to state agency) with initiation of discussion of the sentinel event and/or report with patient and other visit participants.
    </TD>
  </TR>
  <TR>
    <TD CLASS="strcol" >|;
  $out .= ${Locked} 
    ? qq| <INPUT TYPE="hidden" NAME="Treatment_PlayOvercome_1" VALUE="<<Treatment_PlayOvercome_1>>" > <<Treatment_PlayOvercome_1>>| 
    : qq| <INPUT TYPE="checkbox" NAME="Treatment_PlayOvercome_1" VALUE="1" <<Treatment_PlayOvercome_1=checkbox>> >|;
  $out .= qq|
    </TD>
    <TD CLASS="strcol" >
      4. Use of play equipment, physical devices, interpreter or translator to overcome barriers to diagnostic or therapeutic interaction with a patient who is not fluent in the same language or who has not developed or lost expressive or receptive language skills to use or understand typical language.
    </TD>
  </TR>
</TABLE>
|;
#  <TR ><TD CLASS="strcol" COLSPAN="2" >Selection of any box will ADD-ON 90785 service code to PRIMARY PROCEDURE codes 90791, 90792, 90832, 90834, 90837, or 90853.</TD></TR>
#  <TR ><TD CLASS="strcol" COLSPAN="2" >90785 WILL NOT be an add-on for 90839, 90840, 90846, 90847, 90849</TD></TR>
  return($out);
}
####################
# Client Problems
sub setClientNoteProblems
{
  my ($self,$form,$Locked,$ClientID,$TrID,$ContDate) = @_;
 warn qq|setClientNoteProblems: ContDate=$ContDate\n| if ( $debug );
  my $dbh = myDBI->dbconnect($form->{'DBNAME'});
  my $with = $ContDate eq '' ? '' : qq| and ClientProblems.InitiatedDate <= '${ContDate}' and (ClientProblems.ResolvedDate is null or ClientProblems.ResolvedDate <= '${ContDate}')|;
  my $out .= qq|
<TABLE CLASS="home fullsize" >
  <TR >
    <TD CLASS="port hdrstr" >&nbsp;</TD>
    <TD CLASS="port hdrstr" >ICD10</TD>
    <TD CLASS="port hdrstr" >icdName</TD>
    <TD CLASS="port hdrtxt" >sctName</TD>
    <TD CLASS="port hdrtxt" >InitiatedDate</TD>
    <TD CLASS="port hdrtxt" >ResolvedDate</TD>
    <TD CLASS="port hdrtxt" >Status</TD>
  </TR>
|;
  my $blur = $Locked ? qq|ONCLICK="return vUNDO(this,'Note has been locked.');" | : '';
  my $row = 0;
##
# first gather the NoteProblems because those were the CHECKED problems
#   when the note was saved
# then gather the ClientProblems that are not in the NoteProblems
#   (NoteProblems UUID is null because there isn't one)
#   to get the UNCHECKED problems
##
  my $s = $dbh->prepare("select misICD10.ICD10,misICD10.icdName,misICD10.sctName,ClientNoteProblems.UUID,ClientNoteProblems.Priority,ClientNoteProblems.InitiatedDate,ClientNoteProblems.ResolvedDate from ClientNoteProblems inner join okmis_config.misICD10 on misICD10.ID=ClientNoteProblems.UUID where ClientNoteProblems.ClientID=? and ClientNoteProblems.TrID=? order by ClientNoteProblems.Priority");
  $s->execute($ClientID,$TrID) || myDBI->dberror("Physician Note: select ClientNoteProblems");
  while ( my $r = $s->fetchrow_hashref )
  {
    $row++;
    my $class = int($row/2) == $row/2 ? 'rpteven' : 'rptodd';
    my $Status = $r->{'ResolvedDate'} eq '' ? 'active' : 'complete';
    $out .= qq|
  <TR CLASS="${class}" >
    <TD ALIGN="center" >
      <INPUT TYPE="checkbox" NAME="NoteProblems" VALUE="$r->{UUID}" CHECKED ${blur} >
    </TD>
    <TD ALIGN="left" >$r->{'ICD10'}</TD>
    <TD ALIGN="left" >$r->{'icdName'}</TD>
    <TD ALIGN="left" >$r->{'sctName'}</TD>
    <TD ALIGN="left" >$r->{'InitiatedDate'}</TD>
    <TD ALIGN="left" >$r->{'ResolvedDate'}</TD>
    <TD ALIGN="left" >${Status}</TD>
  </TR>|;
  }
#warn qq| setClientNoteProblems: CHECK TrID=$TrID\n|;
# add those NOT CHECKED...
 warn qq|setClientNoteProblems: with=$with\n| if ( $debug );
  my $s = $dbh->prepare("select misICD10.ICD10,misICD10.icdName,misICD10.sctName,ClientProblems.UUID,ClientProblems.Priority,ClientProblems.InitiatedDate,ClientProblems.ResolvedDate from ClientProblems inner join okmis_config.misICD10 on misICD10.ID=ClientProblems.UUID left join ClientNoteProblems on ClientNoteProblems.UUID=ClientProblems.UUID and ClientNoteProblems.TrID='${TrID}' where ClientProblems.ClientID=? and ClientNoteProblems.UUID is null ${with} order by ClientProblems.Priority");
  $s->execute($ClientID) || myDBI->dberror("Physician Note: select ClientProblems");
  while ( my $r = $s->fetchrow_hashref )
  {
    $row++;
    my $class = int($row/2) == $row/2 ? 'rpteven' : 'rptodd';
    my $Status = $r->{'ResolvedDate'} eq '' ? 'active' : 'complete';
    $out .= qq|
  <TR CLASS="${class}" >
    <TD ALIGN="center" >
      <INPUT TYPE="checkbox" NAME="NoteProblems" VALUE="$r->{UUID}" ${blur} >
    </TD>
    <TD ALIGN="left" >$r->{ICD10}</TD>
    <TD ALIGN="left" >$r->{icdName}</TD>
    <TD ALIGN="left" >$r->{sctName}</TD>
    <TD ALIGN="left" >$r->{InitiatedDate}</TD>
    <TD ALIGN="left" >$r->{ResolvedDate}</TD>
    <TD ALIGN="left" >${Status}</TD>
  </TR>|;
  }
  $out .= qq|
</TABLE>|;
  $s->finish();
  return($out);
}
sub setClientNoteTrPlanPG
{
  my ($self,$form,$Locked,$ClientID,$TrID,$ContDate) = @_;
  my $dbh = myDBI->dbconnect($form->{'DBNAME'});
  my ($out,$effdate,$expdate) = ('','','');
  my $header = ${Locked} ? 'Problems addressed' : 'Check all problems addressed';
  my @alpha = ('','a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z');
  my $blur = $Locked ? qq|ONCLICK="return vUNDO(this,'Note has been locked.');" | : '';
  my $rows = 0;
##
# displays ALL TrPlanPG and tests if checked by 
#   testing NoteTrPlanPG with ClientID/TrID/TrPlanPGID
#   if there then it was CHECK when note was saved last time
##
  my $sClientNoteTrPlanPG = $dbh->prepare("select * from ClientNoteTrPlanPG where ClientID=? and TrID=? and TrPlanPGID=?");
  my $sPG = $dbh->prepare("select * from ClientTrPlanPG where TrPlanID=? order by Priority");
  my $sOBJ = $dbh->prepare("select * from ClientTrPlanOBJ where TrPlanPGID=? order by Priority");
  my $with = $ContDate eq '' ? '' : qq| and '${ContDate}' between EffDate and ExpDate|;
#warn qq|setClientNoteTrPlanPG: with=${with}\n|;
  my $s = $dbh->prepare("select * from ClientTrPlan where ClientID=? and Locked=1 ${with} order by EffDate desc");
  $s->execute($ClientID) || myDBI->dberror("setClientNoteTrPlan: select ClientTrPlan ${ClientID}");
  while ( my $r = $s->fetchrow_hashref )
  {
    $rows++;
    my $class = int($rows/2) == $rows/2 ? 'rpteven' : 'rptodd';
    my $TrPlanID = $r->{'ID'};
    $sPG->execute($TrPlanID) || myDBI->dberror("setClientNoteTrPlan: select ClientTrPlanPG ${TrPlanID}");
    while ( my $rPG = $sPG->fetchrow_hashref )
    {
      my $PGID = $rPG->{'ID'};
      my $Num = int($rPG->{'Priority'}/10);
      my $Checked = '';
      $sClientNoteTrPlanPG->execute($ClientID,$TrID,$PGID)
                     || myDBI->dberror("setClientNoteTrPlan: select ClientNoteTrPlanPG ${ClientID} ${TrID} ${PGID}");
      if ( my $rTest = $sClientNoteTrPlanPG->fetchrow_hashref ) { $Checked = 'CHECKED'; }
      $out .= qq|
  <TR >
    <TD CLASS="hdrcol" WIDTH="10%" >
      ${Num} <INPUT TYPE="checkbox" NAME="NoteTrPlanPG" VALUE="$rPG->{'ID'}" ${Checked} ${blur} >
    </TD>
    <TD CLASS="strcol" WIDTH="90%" >
      <UL>
        <LI>$rPG->{Prob}</LI>
        <LI TYPE="square" >$rPG->{Goal}
          <UL>
|;
      $sOBJ->execute($rPG->{'ID'}) || myDBI->dberror("setClientNoteTrPlan: select ClientTrPlanOBJ $r->{ID}");
      while ( my $rOBJ = $sOBJ->fetchrow_hashref )
      {
        my $i = int($rOBJ->{'Priority'}/10);
        my $ltr = @alpha[$i];
        $out .= qq|\n            <LI>${Num}${ltr}: $rOBJ->{Obj}</LI>|;
      }
    }
    $out .= qq|
          </UL>
        </LI>
      </UL>
    </TD>
  </TR>
|;
    $effdate = DBUtil->Date($r->{'EffDate'},'fmt','MM/DD/YYYY');
    $expdate = DBUtil->Date($r->{'ExpDate'},'fmt','MM/DD/YYYY');
    last;   # we ONLY want the latest ClientTrPlan
  }
  my $dateheader = $rows ? qq|${effdate} - ${expdate}| : qq|NO Treatment Plan FOUND!<BR>(possibly not signed by Primary Provider?)|;
  my $html = qq|
<TABLE CLASS="home fullsize" >
  <TR ><TD CLASS="hdrtxt" COLSPAN="2" >Client Treatment Plan Problems, Goals and Objectives</TD></TR>
  <TR ><TD CLASS="hdrtxt" COLSPAN="2" >${dateheader}</TD></TR>
  <TR >
    <TD CLASS="hdrcol" WIDTH="10%" >${header}</TD>
    <TD CLASS="strcol" ><UL><LI>Problem</LI><LI TYPE="square">Goal<UL><LI>Objectives</LI></UL></LI></UL></TD>
  </TR>
${out}
</TABLE>
|;
  $s->finish();
  $sPG->finish();
  $sOBJ->finish();
  $sClientNoteTrPlanPG->finish();
  return($html);
}
## KLS
sub setClientNoteFamilyP
{
  my ($self,$form,$Locked,$ClientID,$TrID) = @_;
  my $dbh = myDBI->dbconnect($form->{'DBNAME'});
  my $out .= qq|
<TABLE CLASS="home fullsize" >
  <TR >
    <TD CLASS="hdrtxt" COLSPAN="2" >Treatment Informants</TD>
    <TD CLASS="hdrtxt" COLSPAN="2" >Treatment Participants</TD>
  </TR>
  <TR >
    <TD CLASS="port hdrstr" >&nbsp;</TD>
    <TD CLASS="port hdrstr" >Family Member</TD>
    <TD CLASS="port hdrstr" >&nbsp;</TD>
    <TD CLASS="port hdrstr" >Family Member</TD>
  </TR>
|;
  my $blur = $Locked ? qq|ONCLICK="return vUNDO(this,'Note has been locked.');" | : '';
  my $row = 0;
  my $header = ${Locked} ? 'Problems addressed' : 'Check all problems addressed';
##
# displays ALL ClientFamily members and tests if checked by 
#   selecting ClientNoteFamilyP with ClientID/TrID/ClientFamilyID
#   if there then it was CHECK when note was saved last time
##
  my $sClientNoteFamilyI = $dbh->prepare("select * from ClientNoteFamilyI where ClientID=? and TrID=? and ClientFamilyID=?");
  my $sClientNoteFamilyP = $dbh->prepare("select * from ClientNoteFamilyP where ClientID=? and TrID=? and ClientFamilyID=?");
  my $sClientFamily = $dbh->prepare("select ClientFamily.*,xRelationship.Descr as Relation from ClientFamily left join okmis_config.xRelationship on xRelationship.ID=ClientFamily.Rel where ClientID=? order by Age");
  $sClientFamily->execute($ClientID) || myDBI->dberror("setClientNoteFamilyP: select ClientFamily ${ClientID}");
  while ( my $rClientFamily = $sClientFamily->fetchrow_hashref )
  {
    $row++;
    my $class = int($row/2) == $row/2 ? 'rpteven' : 'rptodd';
    my $CheckedI = '';
    $sClientNoteFamilyI->execute($ClientID,$TrID,$rClientFamily->{'ID'})
       || myDBI->dberror("setClientNoteFamilyI: select ClientNoteFamilyI ${ClientID} ${TrID} $rClientFamily->{'ID'}");
    if ( my $rTest = $sClientNoteFamilyI->fetchrow_hashref ) { $CheckedI = 'CHECKED'; }
    my $CheckedP = '';
    $sClientNoteFamilyP->execute($ClientID,$TrID,$rClientFamily->{'ID'})
       || myDBI->dberror("setClientNoteFamilyP: select ClientNoteFamilyP ${ClientID} ${TrID} $rClientFamily->{'ID'}");
    if ( my $rTest = $sClientNoteFamilyP->fetchrow_hashref ) { $CheckedP = 'CHECKED'; }
    $out .= qq|
  <TR CLASS="${class}" >
    <TD ALIGN="center" >
      <INPUT TYPE="checkbox" NAME="NoteFamilyI" VALUE="$rClientFamily->{ID}" ${CheckedI} ${blur} >
    </TD>
    <TD ALIGN="left" >
      $rClientFamily->{FName}
      $rClientFamily->{LName}
      $rClientFamily->{Relation}
      (Age: $rClientFamily->{Age})
    </TD>
    <TD ALIGN="center" >
      <INPUT TYPE="checkbox" NAME="NoteFamilyP" VALUE="$rClientFamily->{ID}" ${CheckedP} ${blur} >
    </TD>
    <TD ALIGN="left" >
      $rClientFamily->{FName}
      $rClientFamily->{LName}
      $rClientFamily->{Relation}
      (Age: $rClientFamily->{Age})
    </TD>
  </TR>|;
  }
  $out .= qq|
</TABLE>|;
  $sClientFamily->finish();
  $sClientNoteFamilyI->finish();
  $sClientNoteFamilyP->finish();
  return($out);
}
####################
sub setNoteButtons
{
  my ($self, $form, $NoteType) = @_;

  my $out = qq|
<TABLE CLASS="site fullsize" >
  <TR >
    <TD CLASS="numcol" >
|;
# LOCKED note...mine or reviewok or Inprocess/Scholarshipped/Reconciled
  my $EntBy = $form->{Treatment_EnteredBy_1} == $form->{LOGINPROVID} ? 1 : 0;
  my $MyNote = $form->{Treatment_ProvID_1} == $form->{LOGINPROVID} ? 1 : 0;
  my $RevOK = SysAccess->verify($form,'Privilege=NoteReview');
  my $BillStatus = $form->{Treatment_BillStatus_1};
#warn qq|ClientID=$form->{Treatment_ClientID_1}, TrID=$form->{Treatment_TrID_1}, EntBy=$EntBy, MyNote=$MyNote, RevOK=$RevOK, BS=$BillStatus\n|;
  my $Locked = ( !$EntBy && !$MyNote && !$RevOK ) || ( $BillStatus == 3 || $BillStatus == 4 || $BillStatus == 5 ) ? 1 : 0;
#warn qq|NoteButtons: Locked=$Locked\n|;
#warn qq|Locked=$Locked\n|;
#warn qq|gHTML.pm: TrID=$form->{Treatment_TrID_1}, Locked=$Locked\n|;
#warn qq|gHTML.pm: TrID=$form->{Treatment_TrID_1}, RevStatus=$form->{Treatment_RevStatus_1}\n|;
#warn qq|gHTML.pm: TrID=$form->{Treatment_TrID_1}, BillStatus=$form->{Treatment_BillStatus_1}\n|;
  $Locked = 0 if ( $form->{LOGINPROVID} == 91 );
  if ( ${Locked} )
  { null; }
  # UPDATE NOTE? must have an assigned clinic to update
  elsif ( $form->{Treatment_ClinicID_1} eq '' )
  { null; }
  else       # some update ok.
  {
#   DELETE?  # must exist and new notes only.
    if ( $form->{Treatment_TrID_1} && ($form->{Treatment_BillStatus_1} == 0 || $form->{Treatment_BillStatus_1} == 1 || $form->{Treatment_BillStatus_1} == 2) )
    { $out .= qq|      <INPUT TYPE="submit" ONCLICK="return vDELETE('Are you sure you want to delete this note?')" NAME="delete_note=1&Treatment_DELETE_1=1&UpdateTables=all&misPOP=1" VALUE="Delete Note" > |; }
    # ONLY BILLING SECTION if MgrRevDate set (see above).
    # on new note and update by Provider on note.
    if ( $form->{Treatment_ProvID_1} == $form->{LOGINPROVID} )
    { 
#warn qq|gHTML: ProvID=LOGINPROVID: RevStatus=$form->{Treatment_RevStatus_1}\n|;
      if ( $form->{Treatment_RevStatus_1} == 1 )
      {
        $out .= qq| <INPUT TYPE="submit" ONCLICK="return validate(this.form)" NAME="approve_note=1&misPOP=1" VALUE="Approve Changes" > |;
        $out .= qq| <INPUT TYPE="submit" ONCLICK="return validate(this.form)" NAME="reject_note=1&misPOP=1" VALUE="Reject Changes" > |;
      }
      elsif ( $form->{Treatment_RevStatus_1} == 0 || $form->{Treatment_RevStatus_1} == 2 )
      {
        if ( SysAccess->verify($form,'Privilege=NoteReview') )
        {
          $out .= qq| <INPUT TYPE="submit" ONCLICK="return validate(this.form)" NAME="UpdateTables=all&manager_review=1&misPOP=1" VALUE="Manager Update/Review" > |;
        }
        $out .= qq| <INPUT TYPE="submit" ONCLICK="return validate(this.form)" NAME="UpdateTables=all&misPOP=1" VALUE="Add/Update" > |;
      }
      elsif ( $form->{Treatment_RevStatus_1} == 3 && $form->{Treatment_BillStatus_1} < 3 )
      {
        if ( $form->{Treatment_MgrProvID_1} == $form->{LOGINPROVID} )     # must have had NoteReview access.
        { $out .= qq| <INPUT TYPE="submit" ONCLICK="return validate(this.form)" NAME="UpdateTables=all&manager_unreview=1&misPOP=1" VALUE="Manager UNREVIEW" > |; }
      }
    }
    elsif ( $form->{Treatment_EnteredBy_1} == $form->{LOGINPROVID} )
    {
      if ( $form->{Treatment_RevStatus_1} == 0 )
      { $out .= qq| <INPUT TYPE="submit" ONCLICK="return validate(this.form)" NAME="UpdateTables=all&misPOP=1" VALUE="Add/Update" > |; }
    }
    # Provider has Privilege to review the note.
    elsif ( SysAccess->verify($form,'Privilege=NoteReview') )
    {
#warn qq|gHTML: NoteReview: MgrProvID=$form->{Treatment_MgrProvID_1}\n|;
#warn qq|gHTML: NoteReview: BillStatus=$form->{Treatment_BillStatus_1}\n|;
#warn qq|gHTML: NoteReview: RevStatus=$form->{Treatment_RevStatus_1}\n|;
      # entered by Data Entry - wait on Provider
      if ( $form->{Treatment_RevStatus_1} == 0 ) { null; }
      # someone comes in before reviewed to update (considered Manager review)
      elsif ( $form->{Treatment_RevStatus_1} == 2 )        # can't allow just update, then skips Logging.
      { $out .= qq| <INPUT TYPE="submit" ONCLICK="return validate(this.form)" NAME="UpdateTables=all&manager_review=1&misPOP=1" VALUE="Manager Update/Review" > |; }
      # Manager comes back to update, has to UNREVIEW note first (comes back in above)
      elsif ( $form->{Treatment_MgrProvID_1} == $form->{LOGINPROVID} && $form->{Treatment_BillStatus_1} < 3 )
      {
        $out .= qq| <INPUT TYPE="submit" ONCLICK="return validate(this.form)" NAME="UpdateTables=all&manager_unreview=1&misPOP=1" VALUE="Manager UNREVIEW" > |;
        $out .= qq| <INPUT TYPE="submit" ONCLICK="return validate(this.form)" NAME="UpdateTables=all&misPOP=1" VALUE="Add/Update" > |;
      }
    }

  }
  if ( $form->{LOGINPROVID} == 91 ) { $out .= qq| <INPUT TYPE="submit" ONCLICK="return validate(this.form)" NAME="UpdateTables=all&misPOP=1" VALUE="Add/Update" > |; }
# Debbie Wolfe for okpsych fixes.
##if ( $form->{LOGINPROVID} == 115 ) { $out .= qq| <INPUT TYPE="submit" ONCLICK="return validate(this.form)" NAME="UpdateTables=all&misPOP=1" VALUE="Add/Update" > |; }
  $out .= qq|
    </TD>
  </TR>
</TABLE>
|;
  my $TrID = $form->{Treatment_TrID_1};
#warn qq|KLS: TrID=${TrID}, Type=$form->{'Treatment_Type_1'}\n|;
  if ( $TrID ne '' && SysAccess->getRule($form,'NoteEdit',$form->{Treatment_ProvID_1}) )
  {
    my $log = $form->{Treatment_Type_1} == 2 ? 'ShowPhysNotesLog' : 'ShowProgNotesLog';
#warn qq|KLS: TrID=${TrID}, log=${log}\n|;
    $out .= '<BR>' . myHTML->ListSel($form,$log,$TrID,$form->{'LINKID'},1);
  }
  return($out);
}
sub setPhysNote
{
  my ($self,$form,$ClientID) = @_;
  my $dbh = myDBI->dbconnect($form->{'DBNAME'});
  my $ClientID = $form->{'Treatment_ClientID_1'};
  my $TrID = $form->{'Treatment_TrID_1'};
  my $ContDate = $form->{'Treatment_ContLogDate_1'};
  my $EntBy = $form->{Treatment_EnteredBy_1} == $form->{LOGINPROVID} ? 1 : 0;
  my $MyNote = $form->{Treatment_ProvID_1} == $form->{LOGINPROVID} ? 1 : 0;
  my $RevOK = SysAccess->verify($form,'Privilege=NoteReview');
  my $BillStatus = $form->{Treatment_BillStatus_1};
# LOCKED note...unless mine or reviewok or Billed/Unreviewed (to change a reviewed note then first unreview).
  my $Locked = ( !$EntBy && !$MyNote && !$RevOK ) || ( $BillStatus == 3 || $BillStatus == 4 || $BillStatus == 5 ) ? 1 : 0;
  $Locked = 0 if ( $form->{LOGINPROVID} == 91 );
  my $arrowdown = myConfig->cfgfile('arrow_down.png',1);

#===== PhysNote ==========================
  my $html = qq|
<HR WIDTH="90%" >
<TABLE CLASS="port fullsize" >
  <TR ><TD CLASS="heading" >Physician Note (${TrID})</TD></TR>
</TABLE>
|;
  $html .= $self->setNoteMsg($form);
  $html .= $self->setNoteRev($form);
  $html .= $self->setNoteBillInfo($form,2);
  $html .= $self->setSCID2($form,$Locked);
  $html .= $self->setIntComp($form,$Locked);
  $html .= qq|
<TABLE CLASS="home fullsize" >
  <TR >
    <TD CLASS="port" COLSPAN="2" >
      <SPAN ID="ClientFamilyP" >
|.$self->setClientNoteFamilyP($form,$Locked,$ClientID,$TrID).qq|
      </SPAN>
    </TD>
  </TR>
</TABLE>
|;
#===== SUBJECTIVE SECTION ==========================
  $html .= qq|
<HR WIDTH="90%" >
<TABLE CLASS="home fullsize" >
  <TR ><TD CLASS="port hdrtxt" COLSPAN="2" >SUBJECTIVE SECTION</TD></TR>
  <TR> <TD CLASS="strcol" COLSPAN="2" >Referral Reason</TD> </TR>
  <TR>
    <TD CLASS="strcol" COLSPAN="2" >
      <INPUT TYPE="text" NAME="PhysNotes_RefReason_1" VALUE="<<PhysNotes_RefReason_1>>" SIZE="60" >
    </TD>
  </TR>
  <TR> <TD CLASS="strcol" COLSPAN="2" >Referral Detail</TD> </TR>
  <TR>
    <TD CLASS="strcol" COLSPAN="2" >
      <TEXTAREA COLS="140" ROWS="5" WRAP="virtual" NAME="PhysNotes_RefDetail_1" ><<PhysNotes_RefDetail_1>></TEXTAREA>
    </TD>
  </TR>
  <TR> <TD CLASS="strcol" COLSPAN="2" >Chief Complaint</TD> </TR>
  <TR>
    <TD CLASS="strcol" COLSPAN="2" >
      <TEXTAREA COLS="140" ROWS="2" WRAP="virtual" NAME="PhysNotes_Complaint_1" ><<PhysNotes_Complaint_1>></TEXTAREA>
    </TD>
  </TR>
  <TR> <TD CLASS="strcol" COLSPAN="2" >Health Concerns</TD> </TR>
  <TR>
    <TD CLASS="strcol" COLSPAN="2" >
      <TEXTAREA COLS="140" ROWS="2" WRAP="virtual" NAME="PhysNotes_Concerns_1" ><<PhysNotes_Concerns_1>></TEXTAREA>
    </TD>
  </TR>
  <TR> <TD CLASS="strcol" COLSPAN="2" >History of Present Illness</TD> </TR>
  <TR>
    <TD CLASS="strcol" COLSPAN="2" >
      <TEXTAREA COLS="140" ROWS="5" WRAP="virtual" NAME="PhysNotes_PresentHistory_1" ><<PhysNotes_PresentHistory_1>></TEXTAREA>
    </TD>
  </TR>
  <TR> <TD CLASS="strcol" COLSPAN="2" >Past, Family, and Social History</TD> </TR>
  <TR>
    <TD CLASS="strcol" COLSPAN="2" >
      <TEXTAREA COLS="140" ROWS="5" WRAP="virtual" NAME="PhysNotes_SocialHistory_1" ><<PhysNotes_SocialHistory_1>></TEXTAREA>
    </TD>
  </TR>
</TABLE>
|;
  if ( $form->{'Treatment_ProvID_1'} == $form->{'LOGINPROVID'} )
  {
    my $Therapy .= ${Locked} 
      ? qq|<INPUT TYPE="hidden" NAME="ClientTherapyNotes_Psychotherapy_1" VALUE="<<ClientTherapyNotes_Psychotherapy_1>>" > <<ClientTherapyNotes_Psychotherapy_1>> &nbsp;|
      : qq|<TEXTAREA COLS="140" ROWS="5" WRAP="virtual" NAME="ClientTherapyNotes_Psychotherapy_1" ><<ClientTherapyNotes_Psychotherapy_1>></TEXTAREA>|;
    $html .=qq|
<TABLE CLASS="home fullsize" >
  <TR ><TD CLASS="port" >Psychotherapy note (HIPAA 45.CFR. Section 164.501)</TD></TR>
  <TR><TD >${Therapy}</TD></TR>
</TABLE>
|;
  }

#===== OBJECTIVE SECTION ==========================
  $html .= qq|
<HR WIDTH="90%" >
<TABLE CLASS="home fullsize" >
  <TR ><TD CLASS="port hdrtxt" COLSPAN="10" >OBJECTIVE SECTION</TD></TR>
  <TR >
    <TD CLASS="port" COLSPAN="10" >
      Vital Signs
      <A HREF="javascript:InputWindow('/cgi/bin/mis.cgi?view=ListClientVitalSigns.cgi&Client_ClientID=${ClientID}&mlt=$form->{mlt}&misLINKS=$form->{misLINKS}&NONAVIGATION=1','linkvitals',900,1100)"; return true; >Add/Update VITAL SIGNS</A>
    </TD>
  </TR>
  <TR >
    <TD CLASS="port hdrtxt" >Date</TD>
    <TD CLASS="port hdrtxt" >Height</TD>
    <TD CLASS="port hdrtxt" >Weight</TD>
    <TD CLASS="port hdrtxt" >Waist</TD>
    <TD CLASS="port hdrtxt" >Temp</TD>
    <TD CLASS="port hdrtxt" >BP</TD>
    <TD CLASS="port hdrtxt" >Pulse</TD>
    <TD CLASS="port hdrtxt" >Oxi</TD>
    <TD CLASS="port hdrtxt" >BS</TD>
    <TD CLASS="port hdrtxt" >Resp</TD>
  </TR>
|;
  my $row = 0;
  my $s = $dbh->prepare("select * from ClientVitalSigns where ClientID=? order by VDate desc");
  $s->execute($ClientID) || myDBI->dberror("Physician Note: select ClientVitalSigns");
  while ( my $r = $s->fetchrow_hashref )
  {
    $row++;
    my $class = int($row/2) == $row/2 ? 'rpteven' : 'rptodd';
    my $Height = $r->{'HeightFeet'} eq '' ? '' : qq|$r->{'HeightFeet'} ft.|;
    $Height .= $r->{'HeightInches'} eq '' ? '' : qq| $r->{'HeightInches'} in.|;
    my $Weight = $r->{'Weight'} eq '' ? '' : qq|$r->{'Weight'} lbs.|;
    my $Waist = $r->{'Waist'} eq '' ? '' : qq|$r->{'Waist'} in.|;
    my $Temp = $r->{'Temperature'} eq '' ? '' : qq|$r->{'Temperature'} F|;
    my $BP = qq|$r->{'BPSystolic'} / $r->{'BPDiastolic'}|;
    $html .= qq|  <TR CLASS="${class}" >
                   <TD ALIGN="center" >$r->{VDate}</TD>
                   <TD ALIGN="center" >${Height}</TD>
                   <TD ALIGN="center" >$r->{Weight}</TD>
                   <TD ALIGN="center" >$r->{Waist}</TD>
                   <TD ALIGN="center" >${Temp}</TD>
                   <TD ALIGN="center" >${BP}</TD>
                   <TD ALIGN="center" >$r->{Pulse}</TD>
                   <TD ALIGN="center" >$r->{Oximetry}</TD>
                   <TD ALIGN="center" >$r->{BloodSugar}</TD>
                   <TD ALIGN="center" >$r->{Respiration}</TD>
                 </TR>
|;
  }
  $html .= qq|
  <TR> <TD CLASS="strcol" COLSPAN="2" >Review of Systems</TD> </TR>
  <TR>
    <TD CLASS="strcol" COLSPAN="2" >
      <TEXTAREA COLS="140" ROWS="10" WRAP="virtual" NAME="PhysNotes_Review_1" ><<PhysNotes_Review_1>></TEXTAREA>
    </TD>
  </TR>
  <TR> <TD CLASS="strcol" COLSPAN="10" >Objective Findings</TD> </TR>
  <TR>
    <TD CLASS="strcol" COLSPAN="10" >
      <TEXTAREA COLS="140" ROWS="5" WRAP="virtual" NAME="PhysNotes_Findings_1" ><<PhysNotes_Findings_1>></TEXTAREA>
    </TD>
  </TR>
</TABLE>
|;
  $s->finish();
# XXX
#===== ASSESSMENT SECTION ==========================
  $html .= qq|
<HR WIDTH="90%" >
<TABLE CLASS="home fullsize" >
  <TR ><TD CLASS="port hdrtxt" COLSPAN="2" >ASSESSMENT SECTION</TD></TR>
  <TR ><TD CLASS="port" COLSPAN="2" >Progress Note (include client's response)</TD></TR>
  <TR>
    <TD COLSPAN="2" >
|;
  $html .= ${Locked} 
    ? qq|<INPUT TYPE="hidden" NAME="PhysNotes_Progress_1" VALUE="<<PhysNotes_Progress_1>>" > [[DBA->getxref(%form+xProgress+<<PhysNotes_Progress_1>>)]] &nbsp;|
    : qq|<SELECT NAME="PhysNotes_Progress_1" >[[DBA->selxTable(%form+xProgress+<<PhysNotes_Progress_1>>)]]</SELECT> |;
  $html .= qq|
    </TD>
  </TR>
  <TR>
    <TD COLSPAN="2" >
|;
  $html .= ${Locked} 
    ? qq|<INPUT TYPE="hidden" NAME="PhysNotes_ProgEvidence_1" VALUE="<<PhysNotes_ProgEvidence_1>>" > <<PhysNotes_ProgEvidence_1>> &nbsp;|
    : qq|<TEXTAREA COLS="140" ROWS="5" WRAP="virtual" NAME="PhysNotes_ProgEvidence_1" ><<PhysNotes_ProgEvidence_1>></TEXTAREA>|;
  $html .= qq|
    </TD>
  </TR>
  <TR >
    <TD CLASS="port" >
      Problems Addressed
      <A HREF="javascript:InputWindow('/cgi/bin/mis.cgi?view=ListClientProblems.cgi&Client_ClientID=${ClientID}&mlt=$form->{mlt}&misLINKS=$form->{misLINKS}&NONAVIGATION=1','linkproblems',900,1200)"; return true; >Add/Update PROBLEMS</A>
    </TD>
    <TD CLASS="port numcol" >
      <A HREF="javascript:callAjax('ListClientNoteProblems','','ProblemsList','&id=${id}&Client_ClientID=${ClientID}&Treatment_TrID=${TrID}&Locked=${Locked}&LOGINPROVID=$form->{LOGINPROVID}&LOGINUSERID=$form->{LOGINUSERID}&LOGINUSERDB=$form->{LOGINUSERDB}&mlt=$form->{mlt}&misLINKS=$form->{misLINKS}&LINKID=$form->{LINKID}&d='+document.Treatment.Treatment_ContLogDate_1.value,'popup.pl');" TITLE="refresh problem list">Refresh<IMG SRC="${arrowdown}" HEIGHT="20" WIDTH="20" ></A>
    </TD>
  </TR>
  <TR >
    <TD CLASS="port" COLSPAN="2" >
      <SPAN ID="ProblemsList" >
|.$self->setClientNoteProblems($form,$Locked,$ClientID,$TrID,$ContDate).qq|
      </SPAN>
    </TD>
  </TR>
  <TR >
    <TD CLASS="port" COLSPAN="2" >
      Risk Assessment
      <A HREF="javascript:InputWindow('/cgi/bin/mis.cgi?view=ListClientRiskAssessment.cgi&Client_ClientID=${ClientID}&mlt=$form->{mlt}&misLINKS=$form->{misLINKS}&NONAVIGATION=1','linkassessment',900,1200)"; return true; >Add/Update RISK ASSESSMENTS</A>
    </TD>
  </TR>
  <TR >
    <TD CLASS="port" COLSPAN="2" >
      Interventions Ordered
      <A HREF="javascript:InputWindow('/cgi/bin/mis.cgi?view=ListClientInterventionsOrdered.cgi&Client_ClientID=${ClientID}&mlt=$form->{mlt}&misLINKS=$form->{misLINKS}&NONAVIGATION=1','linkinterventionso',900,1200)"; return true; >Add/Update INTERVENTIONS ORDERED</A>
    </TD>
  </TR>
  <TR >
    <TD CLASS="port" COLSPAN="2" >
      Interventions Performed
      <A HREF="javascript:InputWindow('/cgi/bin/mis.cgi?view=ListClientInterventionsPerformed.cgi&Client_ClientID=${ClientID}&mlt=$form->{mlt}&misLINKS=$form->{misLINKS}&NONAVIGATION=1','linkinterventionsp',900,1200)"; return true; >Add/Update INTERVENTIONS PERFORMED</A>
    </TD>
  </TR>
  <TR>
    <TD COLSPAN="2" >
      <INPUT TYPE="checkbox" NAME="Treatment_EdPerformed_1" VALUE="1" <<Treatment_EdPerformed_1=checkbox>> >
      Patient Education Performed
    </TD>
  </TR>
</TABLE>|;
#===== PLAN SECTION ==========================
  my $DocMedsDescr = DBA->getxref($form,'xProcedureRejected',$form->{'PhysNotes_DocMeds_1'},'ConceptName ConceptCode');
  my $DocMeds = ${Locked} 
    ? qq|<INPUT TYPE="hidden" NAME="PhysNotes_DocMeds_1" VALUE="$form->{'PhysNotes_DocMeds_1'}" > ${DocMedsDescr}| 
    : qq|<SELECT NAME="PhysNotes_DocMeds_1">
        |.DBA->selxTable($form,'xProcedureRejected',$form->{PhysNotes_DocMeds_1},'ConceptName ConceptCode').qq|
      </SELECT>|;
  $html .= qq|
<HR WIDTH="90%" >
<TABLE CLASS="home fullsize" >
  <TR ><TD CLASS="port hdrtxt" COLSPAN="6" >PLAN SECTION</TD></TR>
  <TR >
    <TD CLASS="strcol" >Documentation of current medications (leave unselected or rejected reason)</TD>
    <TD CLASS="strcol" COLSPAN="5" >
      ${DocMeds}
    </TD>
  </TR>
  <TR ><TD CLASS="port" COLSPAN="6" >Current Medications (Active)</TD></TR>
  <TR >
    <TD CLASS="port hdrstr" >DrugID</TD>
    <TD CLASS="port hdrstr" >Medication</TD>
    <TD CLASS="port hdrtxt" >Dosage</TD>
    <TD CLASS="port hdrtxt" >Route</TD>
    <TD CLASS="port hdrtxt" >Refills</TD>
    <TD CLASS="port hdrtxt" >Date</TD>
  </TR>
|;
#foreach my $f ( sort keys %{$form} ) { warn "form: $f=$form->{$f}\n"; }
  my $row = 0;
  my $s = $dbh->prepare("select * from ClientMeds where ClientID=? and Active=1 order by Active desc, DrugInfo, PrescriptionDate");
  $s->execute($ClientID) || myDBI->dberror("Physician Note: select ClientMeds");
  while ( my $r = $s->fetchrow_hashref )
  {
    $row++;
    my $class = int($row/2) == $row/2 ? 'rpteven' : 'rptodd';
    $html .= qq|
  <TR CLASS="${class}" >
    <TD ALIGN="left" >$r->{DrugID}</TD>
    <TD ALIGN="left" >$r->{DrugInfo}</TD>
    <TD ALIGN="center" >$r->{DosageFrequencyDescription}</TD>
    <TD ALIGN="center" >$r->{Route}</TD>
    <TD ALIGN="center" >$r->{Refills}</TD>
    <TD ALIGN="center" >$r->{PrescriptionDate}</TD>
  </TR>
|;
  }
  $s->finish();
  $html .= qq|
  <TR >
    <TD CLASS="port" COLSPAN="6" >
      <SPAN ID="ProblemsGoals" >
|.$self->setClientNoteTrPlanPG($form,$Locked,$ClientID,$TrID,$ContDate).qq|
      </SPAN>
    </TD>
  </TR>
</TABLE>|;
#===== PROCEDURES ==========================
  my $Role = NewCrop->hasRole($form);
  my $LabLink = $Role ? qq|<A HREF="javascript:ScreenWindow('/cgi/bin/NewCrop.cgi?ClientID=${ClientID}&requestedPage=lab-orders&mlt=$form->{'mlt'}&misLINKS=$form->{'misLINKS'}','labs')" >Update Online LABS</A>| : 'Access required (Role) for lab request entry';
  $html .= qq|
<HR WIDTH="90%" >
<TABLE CLASS="home fullsize" >
  <TR ><TD CLASS="port hdrtxt" COLSPAN="2" >PROCEDURES</TD></TR>
  <TR ><TD CLASS="port hdrstr" >Lab Requests ${LabLink}</TD></TR>
  <TR >
    <TD CLASS="port" >
      Medical Procedures
      <A HREF="javascript:InputWindow('/cgi/bin/mis.cgi?view=ListClientProcedures.cgi&Client_ClientID=${ClientID}&mlt=$form->{mlt}&misLINKS=$form->{misLINKS}&NONAVIGATION=1','linkprocedure',900,1200)"; return true; >Add/Update MEDICAL PROCEDURES</A>
    </TD>
  </TR>
</TABLE>
|;
#===== END ==========================
  $html .= $self->setNoteButtons($form,2);

  return($html);
}
sub ClientMU
{
  my ($self,$form,$ClientID) = @_;
#warn qq|ClientMU: ClientID=${ClientID}\n|;
  my $dbh = myDBI->dbconnect($form->{'DBNAME'});
  my $sClient = $dbh->prepare("select * from Client where ClientID=?");
  $sClient->execute($ClientID) || myDBI->dberror("ClientMU: select Client ${ClientID}");
  my $rClient = $sClient->fetchrow_hashref;
  my $sProvider = $dbh->prepare("select * from Provider where ProvID=?");
  $sProvider->execute($rClient->{'ProvID'}) || myDBI->dberror("ClientMU: select PrimaryProvider $rClient->{'ProvID'}");
  my $rPrimaryProvider = $sProvider->fetchrow_hashref;
  my $PriProvFullName = DBA->subxml($rPrimaryProvider->{'FName'}).' '.DBA->subxml($rPrimaryProvider->{'LName'});
  my $sClientReferrals = $dbh->prepare("select * from ClientReferrals where ClientID=?");
  $sClientReferrals->execute($ClientID) || myDBI->dberror("ClientMU: select ClientReferrals ${ClientID}");
  my $rClientReferrals = $sClientReferrals->fetchrow_hashref;
#foreach my $f ( sort keys %{$rClientReferrals} ) { warn qq|ClientMU: $f=$rClientReferrals->{$f}\n|; }
#warn qq|ClientMU: RefPhysNPI=$rClientReferrals->{RefPhysNPI}, ReferredBy1NPI=$rClientReferrals->{ReferredBy1NPI}\n|;
  my $RefProvNPI = $rClientReferrals->{'RefPhysNPI'} eq ''
                   ? $rClientReferrals->{'ReferredBy1NPI'}
                   : $rClientReferrals->{'RefPhysNPI'};
#warn qq|ClientMU: ClientID=${ClientID}, RefProvID=${RefProvID}\n|;
  my $rRef = DBA->selxref($form,'xNPI','NPI',$RefProvNPI);
#foreach my $f ( sort keys %{$rRef} ) { warn qq|ClientMU: $f=$rRef->{$f}\n|; }
#warn qq|ClientMU: EntityTypeCode=$rRef->{EntityTypeCode}, ProvOrgName=$r->{ProvOrgName}\n|;
  my $PriRefFullName = $rRef->{'EntityTypeCode'} == 1 
                       ? DBA->subxml($rRef->{'ProvFirstName'}).' '.DBA->subxml($rRef->{'ProvLastName'})
                       : DBA->subxml($rRef->{'ProvOrgName'});
  my $PriRefFirstName = DBA->subxml($rRef->{'ProvFirstName'});
  my $PriRefLastName = DBA->subxml($rRef->{'ProvLastName'});
  $sProvider->execute($rClient->{'clinicClinicID'}) || myDBI->dberror("ClientMU: select Clinic $rClient->{'clinicClinicID'}");
  my $rClinic = $sProvider->fetchrow_hashref;
  my $ClinicFullName = DBA->subxml($rClinic->{'FName'}).' '.DBA->subxml($rClinic->{'LName'});
  my $ClinicFirstName = DBA->subxml($rClinic->{'FName'});
  my $ClinicLastName = DBA->subxml($rClinic->{'LName'});
  my $ClinicAddr = $rClinic->{'Addr1'};
  $ClinicAddr .= ', ' . $rClinic->{'Addr2'} if ( $rClinic->{'Addr2'} ne '' );
  my $ClinicCSZ = $rClinic->{'City'} . ', ' . $rClinic->{'ST'} . '  ' . $rClinic->{'Zip'};
  my $ClinicTel = $rClinic->{'WkPh'};
  my $sTreatment = $dbh->prepare("select * from Treatment where ClientID=? order by ContLogDate desc");
  $sTreatment->execute($ClientID) || myDBI->dberror("ClientMU: select Treatment ${ClientID}");
  my $rTreatment = $sTreatment->fetchrow_hashref;
  my $TrID = $rTreatment->{'TrID'};
  my $ContDate = DBUtil->Date($rTreatment->{'ContLogDate'},'fmt','MM/DD/YYYY');
  my $Duration = DBUtil->getDuration($rTreatment->{'ContLogBegTime'},$rTreatment->{'ContLogEndTime'}) / 60;
  $sProvider->execute($rTreatment->{'ProvID'}) || myDBI->dberror("ClientMU: select Provider $rTreatment->{'ProvID'}");
  my $rNoteProv = $sProvider->fetchrow_hashref;
  my $NoteProvFullName = DBA->subxml($rNoteProv->{'FName'}).' '.DBA->subxml($rNoteProv->{'LName'});
  my $NoteProvFirstName = DBA->subxml($rNoteProv->{'FName'});
  my $NoteProvLastName = DBA->subxml($rNoteProv->{'LName'});
  $sProvider->execute($rTreatment->{'EnteredBy'}) || myDBI->dberror("ClientMU: select EnteredBy $rTreatment->{'EnteredBy'}");
  my $rEnteredBy = $sProvider->fetchrow_hashref;
  my $EnteredByFullName = DBA->subxml($rEnteredBy->{'FName'}).' '.DBA->subxml($rEnteredBy->{'LName'});
  my $EnteredByFirstName = DBA->subxml($rEnteredBy->{'FName'});
  my $EnteredByLastName = DBA->subxml($rEnteredBy->{'LName'});
  my $sClientNoteFamilyI = $dbh->prepare("select * from ClientNoteFamilyI where TrID=?");
  $sClientNoteFamilyI->execute($TrID) || myDBI->dberror("ClientMU: select ClientNoteFamilyI ${TrID}");
  my $rClientNoteFamilyI = $sClientNoteFamilyI->fetchrow_hashref;
  my $InformantFullName = DBA->subxml($rClientNoteFamilyI->{'FName'}).' '.DBA->subxml($rClientNoteFamilyI->{'LName'}).' ('.DBA->getxref($form,'xRelationship',$rClientNoteFamilyI->{Rel},'Descr').')';
  my $InformantFirstName = DBA->subxml($rClientNoteFamilyI->{'FName'});
  my $InformantLastName = DBA->subxml($rClientNoteFamilyI->{'LName'});
  my $CareTeamMembers = '';
  my $sClientTrPlanS = $dbh->prepare("select Provider.FName,Provider.LName from ClientTrPlanS left join ClientTrPlan on ClientTrPlan.ID=ClientTrPlanS.TrPlanID left join Provider on Provider.ProvID=ClientTrPlanS.ProvID where ClientTrPlan.ClientID=? and '$rTreatment->{ContLogDate}' between ClientTrPlan.EffDate and ClientTrPlan.ExpDate");
  $sClientTrPlanS->execute($ClientID) || myDBI->dberror("ClientMU: select ClientTrPlanS ${ClientID}/${ContDate}");
  while ( my $rClientTrPlanS = $sClientTrPlanS->fetchrow_hashref )
  {
    $CareTeamMembers .= DBA->subxml($rClientTrPlanS->{'FName'}).' '.DBA->subxml($rClientTrPlanS->{'LName'}).'<BR>';
  }
  my $ParticipantsList = '';
  my $sClientNoteFamilyP = $dbh->prepare("select * from ClientNoteFamilyP where TrID=?");
  $sClientNoteFamilyP->execute($TrID) || myDBI->dberror("ClientMU: select ClientNoteFamilyP ${TrID}");
  while ( my $rClientNoteFamilyP = $sClientNoteFamilyP->fetchrow_hashref )
  {
    $ParticipantsList .= DBA->subxml($rClientNoteFamilyP->{'FName'}).' '.DBA->subxml($rClientNoteFamilyP->{'LName'}).' ('.DBA->getxref($form,'xRelationship',$rClientNoteFamilyP->{Rel},'Descr').')<BR>' . DBA->subxml($rClientNoteFamilyP->{'FName'}).'<BR>'.DBA->subxml($rClientNoteFamilyP->{'LName'}).'<BR>';
  }
  my $ProblemsList = '';
  my $s = $dbh->prepare("select misICD10.ICD10,misICD10.icdName,misICD10.sctName,misICD10.SNOMEDID,ClientNoteProblems.UUID,ClientNoteProblems.Priority,ClientNoteProblems.InitiatedDate,ClientNoteProblems.ResolvedDate from ClientNoteProblems inner join okmis_config.misICD10 on misICD10.ID=ClientNoteProblems.UUID where ClientNoteProblems.ClientID=? and ClientNoteProblems.TrID=? order by ClientNoteProblems.Priority");
  $s->execute($ClientID,$TrID) || myDBI->dberror("Physician Note: select ClientNoteProblems");
  while ( my $r = $s->fetchrow_hashref )
  { $ProblemsList .= qq|$r->{'sctName'} SNOMED-CT: $r->{'SNOMEDID'}<BR>|; }
  $s->finish();

  my $out = qq|
  <TR >
    <TD COLSPAN="2" >
<SPAN ID="VISITINFORMATION" >
<TABLE CLASS="home fullsize" >
  <TR >
    <TD CLASS="strcol" WIDTH="30%" >Referring or Transitioning Providers Name:</TD>
    <TD CLASS="strcol" WIDTH="40%" >
      ${PriRefFullName}<BR>
      ${PriRefFirstName}<BR>
      ${PriRefLastName}<BR>
    </TD>
    <TD CLASS="strcol label" WIDTH="30%" >Note: Referring Provider or Primary Referral</TD>
  </TR>
  <TR >
    <TD CLASS="strcol" WIDTH="30%" >Office Contact Information:</TD>
    <TD CLASS="strcol" WIDTH="40%" >
      ${ClinicFullName}<BR>
      ${ClinicFirstName}<BR>
      ${ClinicLastName}<BR>
      ${ClinicTel}<BR>
      ${ClinicAddr}<BR>
      ${ClinicCSZ}
    </TD>
    <TD CLASS="strcol label" WIDTH="30%" >Note: Assigned Clinic</TD>
  </TR>
  <TR >
    <TD CLASS="strcol" WIDTH="30%" >Author/Legal Authenticator/Authenticator of Electronic Medical Record:</TD>
    <TD CLASS="strcol" WIDTH="40%" >
      ${NoteProvFullName}<BR>
      ${NoteProvFirstName}<BR>
      ${NoteProvLastName}<BR>
      ${ContDate}<BR>
    </TD>
    <TD CLASS="strcol label" WIDTH="30%" >Note: Provider of last visit</TD>
  </TR>
  <TR >
    <TD CLASS="strcol" WIDTH="30%" >Data Enterer during visit:</TD>
    <TD CLASS="strcol" WIDTH="40%" >
      ${EnteredByFullName}<BR>
      ${EnteredByFirstName}<BR>
      ${EnteredByLastName}<BR>
    </TD>
    <TD CLASS="strcol label" WIDTH="30%" >Note: EnteredBy of last visit</TD>
  </TR>
  <TR >
    <TD CLASS="strcol" WIDTH="30%" >Informants:</TD>
    <TD CLASS="strcol" WIDTH="40%" >
      ${InformantFullName}<BR>
      ${InformantFirstName}<BR>
      ${InformantLastName}<BR>
    </TD>
    <TD CLASS="strcol label" WIDTH="30%" >Note: Informant of last visit</TD>
  </TR>
  <TR >
    <TD CLASS="strcol" WIDTH="30%" >Electronic Medical Record Custodian:</TD>
    <TD CLASS="strcol" WIDTH="40%" >
      Millennium Information Services
    </TD>
    <TD CLASS="strcol label" WIDTH="30%" >hardcoded</TD>
  </TR>
  <TR >
    <TD CLASS="strcol" WIDTH="30%" >Information Recipient:</TD>
    <TD CLASS="strcol" WIDTH="40%" >
      ${PriProvFullName}<BR>
    </TD>
    <TD CLASS="strcol label" WIDTH="30%" >Note: Primary Provider</TD>
  </TR>
  <TR >
    <TD CLASS="strcol" WIDTH="30%" >Visit Date:</TD>
    <TD CLASS="strcol" WIDTH="40%" >
      ${ContDate}<BR>
      #${TrID}
    </TD>
    <TD CLASS="strcol label" WIDTH="30%" >Note: ContLogDate of last visit</TD>
  </TR>
  <TR >
    <TD CLASS="strcol" WIDTH="30%" >Care Team Members:</TD>
    <TD CLASS="strcol" WIDTH="40%" >
      ${CareTeamMembers}
    </TD>
    <TD CLASS="strcol label" WIDTH="30%" >Note: Treatment Plan Signers</TD>
  </TR>
  <TR >
    <TD CLASS="strcol" WIDTH="30%" >Other Participants in event:</TD>
    <TD CLASS="strcol" WIDTH="40%" >
      ${ParticipantsList}
    </TD>
    <TD CLASS="strcol label" WIDTH="30%" >Note: Participants of last visit</TD>
  </TR>
  <TR >
    <TD CLASS="strcol" WIDTH="30%" >Event Documentation Details or Documentation of Event:</TD>
    <TD CLASS="strcol" WIDTH="40%" >
      ${NoteProvFullName}<BR>
      ${Duration} minute encounter<BR>
    </TD>
    <TD CLASS="strcol" WIDTH="30%" >
      ${ProblemsList}
    </TD>
  </TR>
</TABLE>
</SPAN>
    </TD>
  </TR>
|;
  $sClient->finish();
  $sClientReferrals->finish();
  $sProvider->finish();
  $sTreatment->finish();
  $sClientNoteFamilyI->finish();
  $sClientTrPlanS->finish();
  $sClientNoteFamilyP->finish();
  return($out);
}
####################
sub setASAMButtons
{
  my ($self,$form) = @_;

#warn qq|ENTER: setASAMButtons: subview=$form->{'subview'}\n|;
  my $view = qq|ASAM_CHILD_ADM_L05.cgi|;
  my $label = qq|Adolescent Admission Level .05|;
  my $url = myForm->genLink('ClientASAM',$view,'new');
  my $Buttons = qq|       <INPUT TYPE=submit ONCLICK="return validate(this.form,'${NewLabel} information','${vmsg}')" ONMOUSEOVER="window.status='add button'; return true;" ONMOUSEOUT="window.status=''" NAME="${url}&UpdateTables=all&pushID=$form->{LINKID}" VALUE="${label}" >|;
  $view = qq|ASAM_CHILD_ADM_L10.cgi|;
  $label = qq|Adolescent Admission Level 1|;
  $url = myForm->genLink('ClientASAM',$view,'new');
  $Buttons .= qq|       <INPUT TYPE=submit ONCLICK="return validate(this.form,'${NewLabel} information','${vmsg}')" ONMOUSEOVER="window.status='add button'; return true;" ONMOUSEOUT="window.status=''" NAME="${url}&UpdateTables=all&pushID=$form->{LINKID}" VALUE="${label}" >|;
  $view = qq|ASAM_CHILD_ADM_L21.cgi|;
  $label = qq|Adolescent Admission Level 2.1|;
  $url = myForm->genLink('ClientASAM',$view,'new');
  $Buttons .= qq|       <INPUT TYPE=submit ONCLICK="return validate(this.form,'${NewLabel} information','${vmsg}')" ONMOUSEOVER="window.status='add button'; return true;" ONMOUSEOUT="window.status=''" NAME="${url}&UpdateTables=all&pushID=$form->{LINKID}" VALUE="${label}" >|;
  $view = qq|ASAM_CHILD_DIS_L05.cgi|;
  $label = qq|Adolescent Discharge Level .05|;
  $url = myForm->genLink('ClientASAM',$view,'new');
  $Buttons .= qq|       <INPUT TYPE=submit ONCLICK="return validate(this.form,'${NewLabel} information','${vmsg}')" ONMOUSEOVER="window.status='add button'; return true;" ONMOUSEOUT="window.status=''" NAME="${url}&UpdateTables=all&pushID=$form->{LINKID}" VALUE="${label}" >|;
  $view = qq|ASAM_CHILD_DIS_L10.cgi|;
  $label = qq|Adolescent Discharge Level 1|;
  $url = myForm->genLink('ClientASAM',$view,'new');
  $Buttons .= qq|       <INPUT TYPE=submit ONCLICK="return validate(this.form,'${NewLabel} information','${vmsg}')" ONMOUSEOVER="window.status='add button'; return true;" ONMOUSEOUT="window.status=''" NAME="${url}&UpdateTables=all&pushID=$form->{LINKID}" VALUE="${label}" >|;
  $view = qq|ASAM_ADULT_ADM_L05.cgi|;
  $label = qq|Adult Admission Level .05|;
  $url = myForm->genLink('ClientASAM',$view,'new');
  $Buttons .= qq|       <INPUT TYPE=submit ONCLICK="return validate(this.form,'${NewLabel} information','${vmsg}')" ONMOUSEOVER="window.status='add button'; return true;" ONMOUSEOUT="window.status=''" NAME="${url}&UpdateTables=all&pushID=$form->{LINKID}" VALUE="${label}" >|;
  $view = qq|ASAM_ADULT_ADM_L10.cgi|;
  $label = qq|Adult Admission Level 1|;
  $url = myForm->genLink('ClientASAM',$view,'new');
  $Buttons .= qq|       <INPUT TYPE=submit ONCLICK="return validate(this.form,'${NewLabel} information','${vmsg}')" ONMOUSEOVER="window.status='add button'; return true;" ONMOUSEOUT="window.status=''" NAME="${url}&UpdateTables=all&pushID=$form->{LINKID}" VALUE="${label}" >|;
  $view = qq|ASAM_ADULT_ADM_L21.cgi|;
  $label = qq|Adult Admission Level 2.1|;
  $url = myForm->genLink('ClientASAM',$view,'new');
  $Buttons .= qq|       <INPUT TYPE=submit ONCLICK="return validate(this.form,'${NewLabel} information','${vmsg}')" ONMOUSEOVER="window.status='add button'; return true;" ONMOUSEOUT="window.status=''" NAME="${url}&UpdateTables=all&pushID=$form->{LINKID}" VALUE="${label}" >|;
  $view = qq|ASAM_ADULT_DIS_L05.cgi|;
  $label = qq|Adult Discharge Level .05|;
  $url = myForm->genLink('ClientASAM',$view,'new');
  $Buttons .= qq|       <INPUT TYPE=submit ONCLICK="return validate(this.form,'${NewLabel} information','${vmsg}')" ONMOUSEOVER="window.status='add button'; return true;" ONMOUSEOUT="window.status=''" NAME="${url}&UpdateTables=all&pushID=$form->{LINKID}" VALUE="${label}" >|;
  $view = qq|ASAM_ADULT_DIS_L10.cgi|;
  $label = qq|Adult Discharge Level 1|;
  $url = myForm->genLink('ClientASAM',$view,'new');
  $Buttons .= qq|       <INPUT TYPE=submit ONCLICK="return validate(this.form,'${NewLabel} information','${vmsg}')" ONMOUSEOVER="window.status='add button'; return true;" ONMOUSEOUT="window.status=''" NAME="${url}&UpdateTables=all&pushID=$form->{LINKID}" VALUE="${label}" >|;
  my $out = qq|
<TABLE CLASS="main fullsize" >
  <TR > <TD CLASS="strcol" > ADD buttons </TD><TD CLASS="numcol" > ${Buttons} </TD> </TR>
</TABLE>
|;
  return($out);
}
sub disTFCTimes
{ 
  my ($self, $form) = @_;

  my $Reviewed = $form->{Treatment_MgrRevDate_1} eq '' ? 0 : 1;
$Reviewed=0;   # DO NOT TURN THIS ON YET!!!
  my $ContDate = 'curdate()';
#warn "ContLogDate=$form->{'Treatment_ContLogDate_1'}\n";
  if ( $form->{'Treatment_ContLogDate_1'} )
  { $ContDate = "'" . $form->{'Treatment_ContLogDate_1'} . "'"; }
  my $dbh = myDBI->dbconnect($form->{'DBNAME'});

##
# store in hashed array because MySQL would not select nulls, ie null Type.
##
  my $xTFCTimes = {};
  my $sTFCTimes = $dbh->prepare("select * from TFCTimes where NoteID=? order by BegTime");
  $sTFCTimes->execute($form->{Treatment_TrID_1}) || myDBI->dberror("TFCTimes select");
  $form->{OPENTABLES} .= ',TFCTimes';
  while ( my $rTFCTimes = $sTFCTimes->fetchrow_hashref )
  { 
#foreach my $f ( sort keys %{$rTFCTimes} ) { warn "rTFCTimes: $f=$rTFCTimes->{$f}\n"; }
    my $key = qq|$rTFCTimes->{TrPlanIPID}_$rTFCTimes->{IntLoc}|;
#warn qq|key=$key\n|;
    push(@{$xTFCTimes->{$key}},$rTFCTimes);
  }

  my $q = qq|select TrPlanIP.* from TrPlan
               left join TrPlanIP on TrPlanIP.TrPlanID=TrPlan.TrPlanID
               left join ClientPrAuth on ClientPrAuth.ID=TrPlan.PrAuthID
               where TrPlan.ClientID=$form->{'Client_ClientID_1'}
                 and ${ContDate} between ClientPrAuth.EffDate and ClientPrAuth.ExpDate
               order by TrPlanIP.ProbNum
            |;
#warn "disTFCTimes: q=\n$q\n";
  my $header = ${Reviewed} ? 'Problem#' : 'Problem#';
  my $out = qq|
<TABLE CLASS="port fullsize" >
  <TR ><TD CLASS="hdrcol" ><B>Interventions Addressed</B></TD></TR>
</TABLE>
<TABLE CLASS="home fullsize" >
  <TR >
    <TD CLASS="hdrcol" WIDTH=10% >$header</TD>
    <TD CLASS="strcol" ><UL><LI>Problem</LI><LI TYPE="square">Goal<UL><LI>Begin Time / End Time / Interventions (2 episodes max per day)</LI></UL></LI></UL></TD>
  </TR>
|;
  my @IntLocs = ('A','B','C','D','E','F');
  my $s = $dbh->prepare($q);
  $s->execute || myDBI->dberror($q);
  while ( my $r = $s->fetchrow_hashref )
  {
#warn qq|ID=$r->{ID}\n|;
    my $Prob = $r->{Prob};
    my $ProbNum = $r->{ProbNum};
    my $Goal = $r->{Goal};
    my @Ints = ($r->{Help1}, $r->{Help2}, $r->{Help3}, $r->{Help4}, $r->{Help5}, $r->{Help6});
    $out .= qq|
  <TR >
    <TD CLASS="hdrcol" WIDTH=10% >
      $ProbNum
|;
    $out .= qq|
    </TD>
    <TD CLASS="strcol" WIDTH="90%" >
      <UL>
        <LI>$Prob</LI>
        <LI TYPE="square">$Goal
          <UL>
|;
    my $idx=0;
    foreach $Int ( @Ints )
    { 
      if ( $Int ne '' )
      { 
        my $plusInt = '/ ' . $Int;
        my $j=1;
        my $key = qq|$r->{ID}_$IntLocs[${idx}]|;
#warn qq|INPUT: key=$key\n|;
        foreach my $rTFCTimes ( @{$xTFCTimes->{$key}} )
        {
          $out .= qq|
            <LI> $rTFCTimes->{BegTime} / $rTFCTimes->{EndTime} ${plusInt} </LI>
|;
          $plusInt = '';
          $j++;
        }
        $out .= qq|            <LI> __:__:__ / __:__:__ ${plusInt} </LI>| unless ( $j > 1 );
      }
      $idx++;
    }
    $out .= qq|
          </UL>
        </LI>
      </UL>
    </TD>
  </TR>
|;
  }
  $s->finish();
  $out .= qq|
</TABLE>
<TABLE CLASS="home fullsize" >
  <TR>
    <TD CLASS="numcol" >
      <INPUT TYPE="submit" ONCLICK="return validate(this.form)" NAME="view=TFCTimes.cgi&Client_ClientID=$form->{Client_ClientID_1}&Treatment_TrID=$form->{Treatment_TrID_1}&UpdateTables=all" VALUE="Add/Update Times" >
    </TD>
  </TR>
</TABLE>
|;
  return($out);
}
#############################################################################
sub RestrictedProviderOptions
{
  my ($self,$form) = @_;
  my $html = '';

  if ( SysAccess->chkPriv($form,'SiteAdmin') 
       && $form->{'DBNAME'} =~ /okmis_mms|okmis_dev|okmms_dev/ 
       && $form->{'LOGINPROVID'} == $form->{'Provider_ProvID'} )     # looking at yourself
  {
    my $root = SysAccess->chkPriv($form,'root') 
             ? qq|      <LI><A HREF="/cgi/bin/mis.cgi?view=ListxTables.cgi&mlt=$form->{'mlt'}&misLINKS=$form->{'misLINKS'}" ONMOUSEOVER="window.status='xTables'; return true;" ONMOUSEOUT="window.status=''" >xTables</A> <BR /></LI>|
             : '';
    $html .= qq|
  <LI><A HREF="javascript:void(0)">xTables</A>
    <UL CLASS="sub" >
      <LI><A HREF="/cgi/bin/mis.cgi?view=ListInsurance.cgi&mlt=$form->{'mlt'}&misLINKS=$form->{'misLINKS'}" ONMOUSEOVER="window.status='Insurance'; return true;" ONMOUSEOUT="window.status=''" >Insurance</A> <BR /></LI>
      ${root}
      <LI><A HREF="/cgi/bin/mis.cgi?view=ListNS.cgi&mlt=$form->{'mlt'}&misLINKS=$form->{'misLINKS'}" ONMOUSEOVER="window.status='NeedSkills'; return true;" ONMOUSEOUT="window.status=''" >NeedSkills</A> <BR /></LI>
    </Ul>
  </LI>
|;
  }

  if ( SysAccess->chkPriv($form,'Agent') )
  {
    if ( $form->{'Provider_Type_1'} == 2 )                          # looking at Agency type Provider record.
    {
      $html .= qq|
  <LI><A HREF="/cgi/bin/mis.cgi?view=AgencyControl.cgi&Provider_ProvID=$form->{'Provider_ProvID'}&mlt=$form->{'mlt'}&misLINKS=$form->{'misLINKS'}">Agency Control</A></LI>
|;
    }
    if ( $form->{'LOGINPROVID'} == $form->{'Provider_ProvID'} )     # looking at yourself
    {
      $html .= qq|
  <LI><A HREF="javascript:ReportWindow('/cgi/bin/ListMISEmails.cgi?action=1&mlt=$form->{'mlt'}','MISEmails')" ONMOUSEOVER="window.status='MIS Emails'; return true;" ONMOUSEOUT="window.status=''" >MIS Emails</A></LI>
 <LI><A HREF="/cgi/bin/mis.cgi?view=ListMisEDocs.cgi&Provider_ProvID=90&mlt=$form->{'mlt'}&misLINKS=$form->{'misLINKS'}">Millennium Forms</A></LI>
|;
    }
    $html .= qq|
  <LI><A HREF="/cgi/bin/mis.cgi?view=AgencyControl2.cgi&Provider_ProvID=$form->{'Provider_ProvID'}&mlt=$form->{'mlt'}&misLINKS=$form->{'misLINKS'}">Agency URL Control</A></LI>
|;
  }
  if ( SysAccess->chkPriv($form,'MUAgent') )       # Meaningful use testing on Get Well Agency only
  {
    $html .= qq|
  <LI><A HREF="javascript:void(0)" ONMOUSEOVER="window.status='Meaningful Use Menu'; return true;" ONMOUSEOUT="window.status=''" >Meaningful Use</A>
    <UL CLASS="sub" >
      <LI><A HREF="/cgi/bin/mis.cgi?view=ListPhiMail.cgi&Provider_ProvID=$form->{'Provider_ProvID'}&mlt=$form->{'mlt'}&misLINKS=$form->{'misLINKS'}">PhiMail Received</A></LI>
      <LI><A HREF="javascript:InputWindow('https://www.emrdirect.com/web','sandbox',900,1200)" ONMOUSEOVER="window.status='sandbox'; return true;" ONMOUSEOUT="window.status=''" >EMR Mail Sandbox</A></LI>
      <LI><A HREF="/cgi/bin/mis.cgi?view=ListCDSrules.cgi&Provider_ProvID=$form->{'Provider_ProvID'}&mlt=$form->{'mlt'}" ONMOUSEOVER="window.status='CDS Rules'; return true;" ONMOUSEOUT="window.status=''" >CDS Rules</A></LI>
      <LI><A HREF="javascript:InputWindow('/cgi/bin/setPT.cgi?Provider_ProvID=$form->{'Provider_ProvID'}&mlt=$form->{'mlt'}&misLINKS=$form->{'misLINKS'}&NONAVIGATION=1','Triggers',500,800)" >Set CDS Triggers for $form->{'LOGINNAME'}</A></LI>
      <LI><A HREF="/cgi/bin/mis.cgi?view=ListProviderCDAparms.cgi&Provider_ProvID=$form->{'Provider_ProvID'}&mlt=$form->{'mlt'}&misLINKS=$form->{'misLINKS'}">CDA Parameters</A></LI> ]]
      <LI><A HREF="/cgi/bin/mis.cgi?view=ListExportFiles.cgi&Provider_ProvID=$form->{'Provider_ProvID'}&mlt=$form->{'mlt'}&misLINKS=$form->{'misLINKS'}">Export Files and Documents</A></LI> ]]
      <LI><A HREF="/cgi/bin/mis.cgi?view=ListProviderJobs.cgi&Provider_ProvID=$form->{'Provider_ProvID'}&mlt=$form->{'mlt'}&misLINKS=$form->{'misLINKS'}">Provider Jobs (crontab)</A></LI> ]]
      <LI><A HREF="javascript:InputWindow('/cgi/bin/mu.cgi?mlt=$form->{'mlt'}','testrest',900,1200)" ONMOUSEOVER="window.status='testrest'; return true;" ONMOUSEOUT="window.status=''" >Application Access (/index.shtml?ls=mu)</A></LI>
      <LI><A HREF="javascript:InputWindow('/cgi/bin/pop.cgi?Client_ClientID=53159&mlt=$form->{'mlt'}&NONAVIGATION=1','testpop',400,800)" ONMOUSEOVER="window.status='testpop'; return true;" ONMOUSEOUT="window.status=''" >test pop up</A></LI>
      <LI><A HREF="javascript:ReportWindow('/cgi/bin/disFILEs.pl?Provider_ProvID=$form->{'Provider_ProvID'}&mlt=$form->{'mlt'}&misLINKS=$form->{'misLINKS'}','Display FILEs')" >Display FILEs</A></LI> ]]
    </UL>
  </LI>
  <LI><A HREF="/cgi/bin/mis.cgi?view=QRDA.cgi&Provider_ProvID=$form->{'Provider_ProvID'}&mlt=$form->{'mlt'}&misLINKS=$form->{'misLINKS'}">QRDA TEST ONLY</A></LI>
|;
  }
  if ( SysAccess->chkPriv($form,'root') )
  {
    $html .= qq|
  <LI><A HREF="/cgi/bin/mis.cgi?view=ProviderPWD.cgi&Provider_ProvID=$form->{'Provider_ProvID'}&UserLogin_UserID=$form->{'Provider_ProvID'}&mlt=$form->{'mlt'}&misLINKS=$form->{'misLINKS'}">Password Control</A></LI>
|;
  }
  return($html);
}
sub RestrictedProviderFields
{
  my ($self,$form,$Access) = @_;
  return() unless ( SysAccess->chkPriv($form,$Access) );
  my $TYPE1 = $form->{'Provider_Type_1'} == 1 ? 'CHECKED' : '';
  my $TYPE2 = $form->{'Provider_Type_1'} == 2 ? 'CHECKED' : '';
  my $TYPE3 = $form->{'Provider_Type_1'} == 3 ? 'CHECKED' : '';
  my $TYPE4 = $form->{'Provider_Type_1'} == 4 ? 'CHECKED' : '';
  my $html = qq|
  <TR >
    <TD CLASS="strcol" >Type of record</TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="radio" NAME="Provider_Type_1" VALUE=1 ${TYPE1} > Group or Association
      <INPUT TYPE="radio" NAME="Provider_Type_1" VALUE=2 ${TYPE2} > Agency
      <INPUT TYPE="radio" NAME="Provider_Type_1" VALUE=3 ${TYPE3} > Clinic
      <INPUT TYPE="radio" NAME="Provider_Type_1" VALUE=4 ${TYPE4} > Provider
    </TD>
  </TR>
|;
  return($html);
}
sub RestrictedContractsFields
{
  my ($self, $form, $Access) = @_;
  my $Priv = qq|Privilege=${Access}|;
  my $userid2,$password2;
  my $UseSpecialty,$UseReferring,$UseRendering,$UseSFacility,$ContractType,$ContractCode,$ServMeasure,$SourceCode;
  if ( SysAccess->verify($form,$Priv) )
  {
    $userid2 = qq|<INPUT TYPE="text" NAME="Contracts_DMHuserid2_1" VALUE="$form->{Contracts_DMHuserid2_1}" ONFOCUS="select()" SIZE="60" >|;
    $password2 = qq|<INPUT TYPE="text" NAME="Contracts_DMHpassword2_1" VALUE="$form->{Contracts_DMHpassword2_1}" ONFOCUS="select()" SIZE="60" >|;
    if ( $form->{Contracts_UseSpecialty_1} ) { $UseSpecialtyYes = qq|CHECKED|; } else { $UseSpecialtyNo = qq|CHECKED|; }
    if ( $form->{Contracts_UseReferring_1} ) { $UseReferringYes = qq|CHECKED|; } else { $UseReferringNo = qq|CHECKED|; }
    if ( $form->{Contracts_UseRendering_1} ) { $UseRenderingYes = qq|CHECKED|; } else { $UseRenderingNo = qq|CHECKED|; }
    if ( $form->{Contracts_UseSFacility_1} ) { $UseSFacilityYes = qq|CHECKED|; } else { $UseSFacilityNo = qq|CHECKED|; }
    $UseSpecialty = qq| <INPUT TYPE="radio" NAME="Contracts_UseSpecialty_1" VALUE="1" ${UseSpecialtyYes} > yes <INPUT TYPE="radio" NAME="Contracts_UseSpecialty_1" VALUE="0" ${UseSpecialtyNo} > no (HIPAA 837 2310A)|;
    $UseReferring = qq| <INPUT TYPE="radio" NAME="Contracts_UseReferring_1" VALUE="1" ${UseReferringYes} > yes <INPUT TYPE="radio" NAME="Contracts_UseReferring_1" VALUE="0" ${UseReferringNo} > no (HIPAA 837 2310A)|;
    $UseRendering = qq| <INPUT TYPE="radio" NAME="Contracts_UseRendering_1" VALUE="1" ${UseRenderingYes} > yes <INPUT TYPE="radio" NAME="Contracts_UseRendering_1" VALUE="0" ${UseRenderingNo} > no (HIPAA 837 2310B)|;
    $UseSFacility = qq| <INPUT TYPE="radio" NAME="Contracts_UseSFacility_1" VALUE="1" ${UseSFacilityYes} > yes <INPUT TYPE="radio" NAME="Contracts_UseSFacility_1" VALUE="0" ${UseSFacilityNo} > no (HIPAA 837 2310D)|;
    $ContractType = qq|
      <SELECT NAME="Contracts_ContractType_1" >
        |.DBA->selxTable($form,'xContractType',$form->{Contracts_ContractType_1},'ID Descr').qq|
      </SELECT>|;
    $ContractCode = qq|
      <SELECT NAME="Contracts_ContractCode_1" >
        |.DBA->selxTable($form,'xContractCode',$form->{Contracts_ContractCode_1},'ID Descr').qq|
      </SELECT>|;
    $ServMeasure = qq|
      <SELECT NAME="Contracts_ServMeasure_1" >
        |.DBA->selxTable($form,'xServMeasure',$form->{Contracts_ServMeasure_1},'ID Descr').qq|
      </SELECT>|;
    $SourceCode = qq|
      <SELECT NAME="Contracts_SourceCode_1" >
        |.DBA->selxTable($form,'xContractSource',$form->{Contracts_SourceCode_1},'ID Descr').qq|
      </SELECT>|;
  }
  else
  {
    $userid2 = 'hidden';
    $password2 = 'hidden';
    if ( $form->{Contracts_UseSpecialty_1} ) { $UseSpecialty = qq|Yes|; } else { $UseSpecialty = qq|No|; }
    if ( $form->{Contracts_UseReferring_1} ) { $UseReferring = qq|Yes|; } else { $UseReferring = qq|No|; }
    if ( $form->{Contracts_UseRendering_1} ) { $UseRendering = qq|Yes|; } else { $UseRendering = qq|No|; }
    if ( $form->{Contracts_UseSFacility_1} ) { $UseSFacility = qq|Yes|; } else { $UseSFacility = qq|No|; }
    $ContractType = DBA->getxref($form,'xContractType',$form->{Contracts_ContractType_1},'ID Descr');
    $ContractCode = DBA->getxref($form,'xContractCode',$form->{Contracts_ContractCode_1},'ID Descr');
    $ServMeasure = DBA->getxref($form,'xServMeasure',$form->{Contracts_ServMeasure_1},'ID Descr');
    $SourceCode = DBA->getxref($form,'xContractSource',$form->{Contracts_SourceCode_1},'ID Descr');
  }
  my $str = qq|
  <TR><TD CLASS="port hdrtxt" " COLSPAN="2" >Restricted Electronic Data</TD></TR>
  <TR>
    <TD CLASS="strcol" " WIDTH="25%" >DMH userid2</TD>
    <TD CLASS="strcol" " >${userid2}</TD>
  </TR>
  <TR>
    <TD CLASS="strcol" " WIDTH="25%" >DMH password2</TD>
    <TD CLASS="strcol" " >${password2}</TD>
  </TR>
  <TR>
    <TD CLASS="strcol" " WIDTH="25%" >Use Specialty Code</TD>
    <TD CLASS="strcol" " >${UseSpecialty} (use for Individual Providers) [for Taxonomy in Billing 2000A]</TD>
  </TR>
  <TR>
    <TD CLASS="strcol" WIDTH="25%" >Use Referring Provider</TD>
    <TD CLASS="strcol" >${UseReferring}</TD>
  </TR>
  <TR>
    <TD CLASS="strcol" WIDTH="25%" >Use Rendering Provider</TD>
    <TD CLASS="strcol" >${UseRendering} (NOT IF Individual, uses Specialty Code and Clinic NPI)</TD>
  </TR>
  <TR>
    <TD CLASS="strcol" WIDTH="25%" >Use Service Facility</TD>
    <TD CLASS="strcol" >${UseSFacility}</TD>
  </TR>
  <TR>
    <TD CLASS="strcol" >&nbsp;</TD>
    <TD CLASS="strcol" >(HIPAA 837 2300 section: create CN1 if Contract Code)</TD>
  </TR>
  <TR>
    <TD CLASS="strcol" WIDTH="25%" >Contract Code (CN1-04)</TD>
    <TD CLASS="strcol" >${ContractCode} (turn off Specialty Code)</TD>
  </TR>
  <TR>
    <TD CLASS="strcol" WIDTH="25%" >Contract Type (CN1-01)</TD>
    <TD CLASS="strcol" >${ContractType}    (required for Contract Code)</TD>
  </TR>
  <TR>
    <TD CLASS="strcol" >&nbsp;</TD>
    <TD CLASS="strcol" >(HIPAA 837 2400 section: required for all services)</TD>
  </TR>
  <TR>
    <TD CLASS="strcol" WIDTH="25%" >Service Measurement (SV1-03)</TD>
    <TD CLASS="strcol" >${ServMeasure}</TD>
  </TR>
  <TR>
    <TD CLASS="strcol" WIDTH="25%" >Source Code (HCP-04)</TD>
    <TD CLASS="strcol" >${SourceCode} (for HCP services [ie: DMH])</TD>
  </TR>
|;
  return($str);
}
sub RestrictedCredentialsFields
{
  my ($self, $form, $Access) = @_;
  my $Priv = qq|Privilege=${Access}|;
  return unless ( SysAccess->verify($form,$Priv) );
  my $userid2 = qq|<INPUT TYPE="text" NAME="Credentials_DMHuserid2_1" VALUE="$form->{Credentials_DMHuserid2_1}" ONFOCUS="select()" SIZE="60" >|;
  my $password2 = qq|<INPUT TYPE="text" NAME="Credentials_DMHpassword2_1" VALUE="$form->{Credentials_DMHpassword2_1}" ONFOCUS="select()" SIZE="60" >|;
  my $html = qq|
<TABLE CLASS="home fullsize" >
  <TR><TD CLASS="port hdrtxt" " COLSPAN="2" >Restricted Electronic Data</TD></TR>
  <TR>
    <TD CLASS="strcol" " WIDTH="25%" >DMH userid2</TD>
    <TD CLASS="strcol" " >${userid2}</TD>
  </TR>
  <TR>
    <TD CLASS="strcol" " WIDTH="25%" >DMH password2</TD>
    <TD CLASS="strcol" " >${password2}</TD>
  </TR>
</TABLE>
|;
  return($html);
}
#############################################################################
sub setLINKS
{
  my ($self,$form,$type,$popCNT) = @_;
  my $html = '';
  my $misPOP = $popCNT eq '' ? 1 : $popCNT;
#warn qq|setLINKS: type=$type\n|;
#warn qq|setLINKS: NONAVIGATION=$form->{'NONAVIGATION'}\n|;
  return('&nbsp;') if ( $form->{'NONAVIGATION'} );    # newHTML withOUT left/right/back navigation
  if ( $type =~ /back/i )
  {
    if ( $form->{'Provider_ProvID'} && $form->{Provider_ProvID} ne 'new' )
    {
      $html .= qq|
      <A HREF="/cgi/bin/ChartList.cgi?Provider_ProvID=$form->{'LOGINPROVID'}&mlt=$form->{mlt}" TITLE="Click here to <BR>access your own Chart List. <BR>Make sure you commit any update first with the Add/Update button." ><IMG SRC="/images/MyNotes.gif" WIDTH="30" HEIGHT="30" BORDER="0" ></A>
      <A HREF="/cgi/bin/ClientList.cgi?Provider_ProvID=$form->{'LOGINPROVID'}&mlt=$form->{mlt}" TITLE="Click here to <BR>access your own Client List. <BR>Make sure you commit any updates first with the Add/Update button." ><IMG SRC="/images/MyClients.gif" ALT="" WIDTH="30" HEIGHT="30" BORDER="0" ></A>
|;
      if ( $form->{'LOGINPROVID'} != $form->{Provider_ProvID} )
      {
        $html .= qq|
      <A HREF="/cgi/bin/ChartList.cgi?Provider_ProvID=$form->{'Provider_ProvID'}&mlt=$form->{mlt}" TITLE="Use this button to access the selected Providers Chart List. <BR>Make sure you commit any updates first with the Add/Update button." ><IMG SRC="/images/clipboard.gif" ALT="" WIDTH="30" HEIGHT="30" BORDER="0" ></A>
      <A HREF="/cgi/bin/ClientList.cgi?Provider_ProvID=$form->{'Provider_ProvID'}&mlt=$form->{mlt}" TITLE="Use this button to access the selected Providers Client List. <BR>Make sure you commit any updates first with the Add/Update button." ><IMG SRC="/images/icon_folder.gif" ALT="" WIDTH="30" HEIGHT="30" BORDER="0" ></A>
|;
      }
      $html .= qq|
      <A HREF="/cgi/bin/ProviderPage.cgi?Provider_ProvID=$form->{'Provider_ProvID'}&mlt=$form->{mlt}" TITLE="Use this button to access the Provider Page. <BR>Make sure you commit any updates first with the Add/Update button." ><IMG SRC="/images/icon_profile.gif" ALT="" WIDTH="30" HEIGHT="30" BORDER="0" ></A>
|;
    }
    if ( $form->{'Client_ClientID'} && $form->{Client_ClientID} ne 'new' )
    {
      my $ClientPage = qq|/cgi/bin/ClientPage.cgi?Client_ClientID=$form->{Client_ClientID}&mlt=$form->{mlt}|;
      $html .= qq|
      <A HREF="/cgi/bin/ChartList.cgi?Client_ClientID=$form->{'Client_ClientID'}&mlt=$form->{mlt}" TITLE="Use this button to access this Clients Chart List. <BR>Make sure you commit any updates first with the Add/Update button." ><IMG SRC="/images/ClientCharts.gif" ALT="" WIDTH="30" HEIGHT="30" BORDER="0" ></A>
      <A HREF="${ClientPage}" TITLE="Use this button to access the Client Page. <BR>Make sure you commit any updates first with the Add/Update button." ><IMG SRC="/images/icon_profile.gif" ALT="" WIDTH="30" HEIGHT="30" BORDER="0" ></A>
|;
    }
    $html .= qq|
      <A HREF="/cgi/bin/mis.cgi?misPOP=${misPOP}&mlt=$form->{mlt}&misLINKS=$form->{misLINKS}" TITLE="Use this button to CANCEL and go back <BR>without making any updates." ><IMG SRC="|.myConfig->cfgfile('undo_green.png',1).qq|" HEIGHT="30" WIDTH="40" BORDER="0" ></A>\n|;
  }
  return($html);
}
#############################################################################
sub setTabs
{
  my ($self,$form,$in) = @_;
  my ($out,$tabhdr,$tabtext) = ('','','');
  my ($tabcnt,$junk,$rest) = (0,'','');
  my @tabhdrs = ();
  my @tabtexts = ();
  my $tabid = DBUtil->genToken();
  foreach my $line ( split("\n",$in) )
  {
    if ( $line =~ /^<!--TAB:/ )
    {
      if ( $tabcnt ) { push(@tabhdrs,$tabhdr); push(@tabtexts,$tabtext); }
      else { $out .= "\n<!--TABSGOHERE-->\n"; }
      ($junk,$tabhdr,$rest) = split(':',$line);
      $tabtext = ''; $tabcnt++;
    }
    elsif ( $line =~ /^<!--ENDTABS/ )
    {
      if ( $tabcnt ) { push(@tabhdrs,$tabhdr); push(@tabtexts,$tabtext); }
      else { $out .= "\n<!--TABSGOHERE-->\n"; }
      $tabtext = ''; $tabcnt = 0;
    }
    elsif ( $tabcnt ) { $tabtext .= $line . "\n"; }
    else { $out .= $line . "\n"; }
  }
  ($tabcnt,$tabtext) = (0,'');
  foreach my $tabs ( @tabhdrs )
  {
    my $text = $tabtexts[$tabcnt];
    $tabcnt++;
    $tabtext .= $self->bldTab('atab',$tabid,$tabcnt,$text,@tabhdrs);
  }
  $out =~ s/<!--TABSGOHERE-->/$tabtext/;
  return($out);
}
sub bldTab
{
  my $self = shift;
  my $cls = shift;
  my $tab = shift;
  my $num = shift;
  my $text = shift;
  my @labels = @_;
#warn qq|tab=$tab, num=$num, text=$text, labels=@labels\n|;
  my $min = 1; my $max = $#labels + 1;
#warn qq|min=$min, max=$max\n|;
  my $style = $num == 1 ? 'block' : 'none';
  my $out = qq|<DIV STYLE="display:${style}" ID="${tab}${num}" >\n  <UL class="${cls}">\n|;
  for ($i=$min; $i<=$max; $i++)
  {
     if ( $i == $num )
     { $out .= qq|    <LI CLASS="${cls}_selected" ONCLICK="showTab('${tab}',${i},${min},${max});">$labels[$i-1]</LI>\n|; }
     else
     { $out .= qq|    <LI ONCLICK="showTab('${tab}',${i},${min},${max});">$labels[$i-1]</LI>\n|; }
  }
  $out .= qq|  </UL>\n${text}\n</DIV>\n|;
#warn qq|out=$out\n|;
  return($out);
}
sub setTab
{
  my $self = shift;
  my $w = shift;
  my $f = shift;
  my @tabs = @_;
  my ($hdrs,$text) = ('','');
  for ($i=0; $i<=$#tabs; $i++)
  {
    my ($tab,$html) = split(chr(253),$tabs[$i]);
#warn qq|setTab: i=$i, tab=$tab\n|;
    my $tabid = DBUtil->genToken();
    $hdrs .= qq|
      <li>
        <a href="#" rel="${tabid}">
          ${tab}
        </a>
      </li>
|;
    $text .= qq|
      <div id="${tabid}" class="tabcontent">
        ${html}
      </div>
|;
  }
  return('') if ( $text eq '' );
#  <div style="width: 500px; margin: 0 auto; padding: 120px 0 40px; font: 0.85em arial;" >
  my $width = $w ? qq|width: ${w};| : '';
  my $font = $f ? qq|font: ${f};| : '';
  my $html = qq|
  <div style="${width} ${font} margin: 0 auto; padding: 10px 0 40px;" >
    <ul class="tabs" >
${hdrs}
    </ul>
    <div class="tabcontents" >
${text}
    </div>
  </div>
|;

#warn qq|setTab: html=$html\n|;
  return($html);
}
#############################################################################
#############################################################################
# Front door Tree stuff.
############################################################################
sub misSiteMsg
{
  my ($self,$form) = @_;
  my $dbh = myDBI->dbconnect($form->{'DBNAME'});
  my $out = qq|
  <TABLE CLASS="home" >
    <TR > <TD CLASS="port hdrcol heading" >Site Message Section</TD> </TR>
|;
  my $qxMessages=qq|select EffDate,Message from xMessages where ExpDate is null order by EffDate desc|;
  my $sxMessages=$dbh->prepare($qxMessages);
  $sxMessages->execute() || myDBI->dberror($qxMessages);
  while ( my ($EffDate,$Msg) = $sxMessages->fetchrow_array )
  {
    my $dif = DBUtil->Date('','diff',$EffDate);
    my $clr = $dif < 8 ? 'red' : 'black';
    my $new = $dif < 8 ? 'NEW:' : 'FYI:';
    $out .= qq|
    <TR>
      <TD CLASS="home" ><UL><LI><FONT COLOR="${clr}" >${new} ${EffDate}</FONT></LI><LI>${Msg}</LI></UL></TD>
    </TR>
|;
  }
  $sxMessages->finish();
  $out .= qq|</TABLE>|;
  return($out);
}
sub misFeatures
{
  my ($self,$form) = @_;
  my $out = qq|
<TABLE CLASS="home" >
  <TR ><TD CLASS="port hdrcol" >Additional FEATUREs<BR>click on the links below for more information</TD></TR>
  <TR><TD CLASS="home" >
    <A HREF="javascript:ReportWindow('http://forms.okmis.com/misdocs/EmailReminders.htm','HelpWindow')" >Emailing Reminders</A> from the Administration->Set up Reminder menu option.
    <A HREF="javascript:ReportWindow('http://forms.okmis.com/misdocs/EmailReminders.htm','HelpWindow')" ><IMG " HEIGHT="20" WIDTH="20" SRC="/images/ques.jpg" ALT="" BORDER="0" ></A>
  </TD></TR>
  <TR><TD CLASS="home" >
    <A HREF="javascript:ReportWindow('http://forms.okmis.com/misdocs/SecureEmail.htm','HelpWindow')" >Secure Email within MIS</A> using the 'Email' icon under the date/time on the left side of your screen.
    <A HREF="javascript:ReportWindow('http://forms.okmis.com/misdocs/SecureEmail.htm','HelpWindow')" ><IMG " HEIGHT="20" WIDTH="20" SRC="/images/ques.jpg" ALT="" BORDER="0" ></A>
  </TD></TR>
</TABLE>
|;
  return($out);
}
sub misGuide
{
  my ($self,$form) = @_;
  my $out = qq|
<TABLE CLASS="home" >
  <TR CLASS="port" ><TD CLASS="hdrcol title" >Guide to Managerial Tree</TD></TR>
  <TR CLASS="home" >
    <TD CLASS="strcol title" >
    Notes updated every 30 minutes.
    <BR>Select <IMG SRC="/images/icon_folder.gif" ALT="Client-List by Provider" BORDER="0" > for Client list by Provider.
    <BR>Select <IMG SRC="/images/clipboard.gif" ALT="Chart-List by Provider" BORDER="0" > for Chart list by Provider.
    <BR>Click the <FONT COLOR=blue >Provider Name</FONT> for personal information.
    <BR>(Unreviewed/Unbilled) notes: A <FONT COLOR=red >Red Number</FONT> indicates attention needed.
    <BR>Click the <FONT COLOR=blue >Email Address</FONT> to email the provider.
    <BR>Select <IMG SRC="/images/hideshow_infoshown.gif" ALT="Hide or Show Client-List" BORDER="0" > for list of active Clients assigned to this Provider.
    </TD>
  </TR>
</TABLE>
|;
  return($out);
}
sub htmB32
{
  my ($self,$form) = @_;
  my $dbh = myDBI->dbconnect($form->{'DBNAME'});
#foreach my $f ( sort keys %{$form} ) { warn "gHTML-htmB32: form-$f=$form->{$f}\n"; }
  my $cnt;
  my $ClientID = $form->{'Client_ClientID_1'};
  $sClientBasis32 = $dbh->prepare("select * from ClientBasis32 where ClientID=? order by EffDate desc");
  $sClientBasis32->execute($ClientID);
  my @FirstAvg = ();
  my @SecondAvg = ();
  my @LastAvg = ();
  while ( $rClientBasis32 = $sClientBasis32->fetchrow_hashref )
  {
#warn qq|htmB32: CALL with $rClientBasis32->{ClientID}, $rClientBasis32->{ID}\n|;
    $cnt++;
    my @counts = uCalc->calcB32($form,$rClientBasis32);
#for ($k=1; $k<=5; $k++) { warn qq|htmB32: cnt:${cnt} k=${k}, tot=$counts[$k][2] / cnt=$counts[$k][1]\n|; }
    if ( $cnt == 1 )
    {
      $FirstAvg[1] = sprintf("%.2f",$counts[1][1] ? $counts[1][2] / $counts[1][1] : 0);
      $FirstAvg[2] = sprintf("%.2f",$counts[2][1] ? $counts[2][2] / $counts[2][1] : 0);
      $FirstAvg[3] = sprintf("%.2f",$counts[3][1] ? $counts[3][2] / $counts[3][1] : 0);
      $FirstAvg[4] = sprintf("%.2f",$counts[4][1] ? $counts[4][2] / $counts[4][1] : 0);
      $FirstAvg[5] = sprintf("%.2f",$counts[5][1] ? $counts[5][2] / $counts[5][1] : 0);
    }
    if ( $cnt <= 2 )     # either 1st or 2nd
    {
      $SecondAvg[1] = sprintf("%.2f",$counts[1][1] ? $counts[1][2] / $counts[1][1] : 0);
      $SecondAvg[2] = sprintf("%.2f",$counts[2][1] ? $counts[2][2] / $counts[2][1] : 0);
      $SecondAvg[3] = sprintf("%.2f",$counts[3][1] ? $counts[3][2] / $counts[3][1] : 0);
      $SecondAvg[4] = sprintf("%.2f",$counts[4][1] ? $counts[4][2] / $counts[4][1] : 0);
      $SecondAvg[5] = sprintf("%.2f",$counts[5][1] ? $counts[5][2] / $counts[5][1] : 0);
    }
    $LastAvg[1] = sprintf("%.2f",$counts[1][1] ? $counts[1][2] / $counts[1][1] : 0);
    $LastAvg[2] = sprintf("%.2f",$counts[2][1] ? $counts[2][2] / $counts[2][1] : 0);
    $LastAvg[3] = sprintf("%.2f",$counts[3][1] ? $counts[3][2] / $counts[3][1] : 0);
    $LastAvg[4] = sprintf("%.2f",$counts[4][1] ? $counts[4][2] / $counts[4][1] : 0);
    $LastAvg[5] = sprintf("%.2f",$counts[5][1] ? $counts[5][2] / $counts[5][1] : 0);
  }
  $sClientBasis32->finish;
#warn qq|htmB32:1: SecondAvg=$SecondAvg[1], FirstAvg=$FirstAvg[1]\n|;
#warn qq|htmB32:2: SecondAvg=$SecondAvg[2], FirstAvg=$FirstAvg[2]\n|;
#warn qq|htmB32:3: SecondAvg=$SecondAvg[3], FirstAvg=$FirstAvg[3]\n|;
#warn qq|htmB32:4: SecondAvg=$SecondAvg[4], FirstAvg=$FirstAvg[4]\n|;
#warn qq|htmB32:5: SecondAvg=$SecondAvg[5], FirstAvg=$FirstAvg[5]\n|;
#warn qq|htmB32:1: LastAvg=$LastAvg[1], FirstAvg=$FirstAvg[1]\n|;
#warn qq|htmB32:2: LastAvg=$LastAvg[2], FirstAvg=$FirstAvg[2]\n|;
#warn qq|htmB32:3: LastAvg=$LastAvg[3], FirstAvg=$FirstAvg[3]\n|;
#warn qq|htmB32:4: LastAvg=$LastAvg[4], FirstAvg=$FirstAvg[4]\n|;
#warn qq|htmB32:5: LastAvg=$LastAvg[5], FirstAvg=$FirstAvg[5]\n|;
  my $html .= qq|
  <TR CLASS="rptodd" >
    <TD COLSPAN="2" >Trend</TD>
    <TD >|.sprintf("%.2f",$SecondAvg[1] - $FirstAvg[1]).qq|</TD>
    <TD >|.sprintf("%.2f",$SecondAvg[2] - $FirstAvg[2]).qq|</TD>
    <TD >|.sprintf("%.2f",$SecondAvg[3] - $FirstAvg[3]).qq|</TD>
    <TD >|.sprintf("%.2f",$SecondAvg[4] - $FirstAvg[4]).qq|</TD>
    <TD >|.sprintf("%.2f",$SecondAvg[5] - $FirstAvg[5]).qq|</TD>
    <TD COLSPAN="3" >(Previous minus Current)</TD>
  </TR>
  <TR CLASS="rptodd" >
    <TD COLSPAN="2" >Overall</TD>
    <TD >|.sprintf("%.2f",$LastAvg[1] - $FirstAvg[1]).qq|</TD>
    <TD >|.sprintf("%.2f",$LastAvg[2] - $FirstAvg[2]).qq|</TD>
    <TD >|.sprintf("%.2f",$LastAvg[3] - $FirstAvg[3]).qq|</TD>
    <TD >|.sprintf("%.2f",$LastAvg[4] - $FirstAvg[4]).qq|</TD>
    <TD >|.sprintf("%.2f",$LastAvg[5] - $FirstAvg[5]).qq|</TD>
    <TD COLSPAN="3" >(First minus Current)</TD>
  </TR>
|;
  return($html);
}
############################################################################
# hdrs default to row headers in sql statement.
# just default to table-sortable: default'.
# types are: default, alphanumeric, numeric, ignorecase, currency, currency_comma, date.
sub rptSQL
{
  my ($self,$form,$sql,$hdrs,$just,$vfmt) = @_;
#warn qq|rptSQL: sql=$sql\n|;
  my ($out,$html,$cnt) = ('','',0);
  (my $str = $sql) =~ s/^\s*(.*?)\s*$/$1/g;
  my ($s1,$s2) = split(' ',$str,2);              # split select ....
  my $vars = substr($s2,0,index($s2,' from '));  # substr only vars.
  my @colhdrs = ();
  my @coljust = ();
  my @colvfmt = ();
  foreach my $var ( split(',',$vars) )
  { 
    (my $name = $var) =~ s/^\s*(.*?)\s*$/$1/g;
    if ( index($name,'.') >= 0 ) 
    { ($table,$name) = split('\.',$name,2); }
    if ( index($name,' as ') >= 0 ) 
    { ($fld,$name) = split(' as ',$name,2); }
    push(@colhdrs,$name);
    push(@coljust,'default');
  }
  if ( $hdrs )
  {
    my $i=0;
    foreach $val ( split(':',$hdrs) ) 
    { $colhdrs[$i] = $val unless ( $val eq '' ); $i++; }
  }
  if ( $just )
  {
    my $i=0;
    foreach $val ( split(':',$just) ) 
    { $coljust[$i] = $val unless ( $val eq '' ); $i++; }
  }
  if ( $vfmt )
  {
    my $i=0;
    foreach $val ( split(':',$vfmt) ) 
    { $colvfmt[$i] = $val unless ( $val eq '' ); $i++; }
  }
  
  $html = qq|
<SCRIPT LANGUAGE="JavaScript" SRC="/cgi/js/tablesort.js"> </SCRIPT>
<LINK HREF="/cgi/css/tablesort.css" REL="stylesheet" TYPE="text/css">
<TABLE class="chartsort table-autosort table-stripeclass:alternate">
<THEAD>|;
  for ($i=0; $i<=$#colhdrs; $i++)
  { $hdr .= qq|    <TH CLASS="table-sortable:$coljust[$i]" >$colhdrs[$i]</TH>\n|; }
  $html .= qq|
  <TR >\n${hdr}\n</TR>
</THEAD>
<TBODY>
|;
  my $dbh = myDBI->dbconnect($form->{'DBNAME'});
  my $s = $dbh->prepare($sql);
  $s->execute || myDBI->dberror($q);
  while ( my @r = $s->fetchrow_array )
  {
    $cnt++;
    my $even = int($cnt/2) == $cnt/2 ? '1' : '0';
    my $class = $even ? qq|CLASS="alternate"| : '';
    my ($cols,$i) = ('',0);
    foreach my $f ( @r )
    { 
      $f = DBUtil->Date($f,'fmt',$colvfmt[$i]) if ( $colvfmt[$i] );
      $cols .= qq|<TD>${f}</TD>|;
      $i++;
    }
    $html .= qq|  <TR ${class} > ${cols} </TR>\n|;
  }
  $s->finish();
  $html .= qq|\n</TBODY>\n|;
  return($html);
}
sub htmlReport
{
  my ($self,$rpt,$hdrcnt) = @_;
#warn qq|htmlReport: hdrcnt=${hdrcnt}\n|;
#warn qq|htmlReport: rpt=${rpt}\n|;
  my @colhdrs = ();
  my @coljust = ();
  my @colsort = ();
  my $html = qq|
<SCRIPT LANGUAGE="JavaScript" SRC="/cgi/js/utils.js"> </SCRIPT>
<SCRIPT LANGUAGE="JavaScript" SRC="/cgi/js/tablesort.js"> </SCRIPT>
<LINK HREF="/cgi/css/tablesort.css" REL="stylesheet" TYPE="text/css">
|;
  my $cnt=0;
  foreach my $line ( split("\n",$rpt) )
  { 
    $cnt++;
#warn qq|line=$line\n|;
#warn qq|cnt=$cnt, hdrcnt=$hdrcnt\n|;
    if ( $cnt < $hdrcnt )
    { $html .= qq|<DIV>${line}</DIV>\n|; }
    elsif ( $cnt == $hdrcnt )
    {
      $html .= qq|<TABLE class="chartsort table-autosort table-stripeclass:alternate" >|;
      foreach my $cell ( split('\t',$line) ) { push(@colhdrs,$cell); }
    }
    elsif ( $cnt == $hdrcnt+1 )
    {
      my $even = int($cnt/2) == $cnt/2 ? '1' : '0';
      my $class = $even ? qq|CLASS="alternate"| : '';
      my $cells = '';
      foreach my $cell ( split('\t',$line) )
      {
        my ($just,$sort) = ('','');
        if ( $cell =~ /^\d{1,4}\-\d{1,2}\-\d{2,2}$/ )
        { $just = 'center'; $sort = 'date'; }
        elsif ( $cell =~ /^\d{1,2}\-\d{1,2}\-\d{2,4}$/ )
        { $just = 'center'; $sort = 'date'; }
        elsif ( $cell =~ /^\d{1,2}\/\d{1,2}\/\d{2,4}$/ )
        { $just = 'center'; $sort = 'date'; }
        elsif ( $cell =~ /^-{0,1}\d*\.{1}\d{1,2}$/ )
        { $just = 'right'; $sort = 'currency'; }
        elsif ( $cell =~ /^-{0,1}\d*\.{0,1}\d+$/ )
        { $just = 'right'; $sort = 'numeric'; }
        elsif ( $cell =~ /[^0-9]/ )
        { $just = 'left'; $sort = 'alphanumeric'; }        # tried left and text???
        else { $just = 'left'; $sort = 'alphanumeric'; }
#warn qq|just=$just, $colhdrs[$i]\n|;
        push(@coljust,$just);
        push(@colsort,$sort);
        $cells .= qq|<TD STYLE="text-align:${just}" >${cell}</TD>|;
      }
      my $hdrs = '';
      for ( my $i=0; $i<=$#colhdrs; $i++ )
      { 
        my $sort = $colsort[$i] eq '' ? 'alphanumeric' : $colsort[$i]; 
        $hdrs .= qq|    <TH CLASS="table-sortable:${sort}" >$colhdrs[$i]</TH>\n|;
      }
      $html .= qq|<THEAD><TR >\n${hdrs}\n</TR></THEAD>\n<TBODY>\n|;
      $html .= qq|  <TR ${class} >${cells}</TR>\n|;
    }
    else
    {
      my $even = int($cnt/2) == $cnt/2 ? '1' : '0';
      my $class = $even ? qq|CLASS="alternate"| : '';
      my $cells = '';
      my $i = 0;
      foreach my $cell ( split('\t',$line) )
      {
        my $just = $coljust[$i] eq '' ? 'left' : $coljust[$i]; 
        $cells .= qq|<TD STYLE="text-align:${just}" >${cell}</TD>|;
        $i++;
      }
      $html .= qq|  <TR ${class} >${cells}</TR>\n|;
    }
  }
  if ( $cnt == $hdrcnt ) # never got beyond header, at least put it out.
  {
    my $hdrs = '';
    for ( my $i=0; $i<=$#colhdrs; $i++ )
    { 
      my $sort = $colsort[$i] eq '' ? 'alphanumeric' : $colsort[$i]; 
      $hdrs .= qq|    <TH CLASS="table-sortable:${sort}" >$colhdrs[$i]</TH>\n|;
    }
    $html .= qq|<THEAD><TR >\n${hdrs}\n</TR></THEAD>\n<TBODY>\n|;
  }
  $html .= qq|\n</TBODY>\n</TABLE>\n|;
  return($html);
}
#############################################################################
# these are the Clinics the ReqProvID has access to.
sub selClinics
{
  my ($self,$form,$ReqProvID,$SelectedIDs,$rtnList) = @_;
#warn qq|selCLinics: Sel=$SelectedIDs\n|;
  my $ForProvID = $ReqProvID ? $ReqProvID : $form->{LOGINPROVID};
  my $list = ();
  my $dbh = myDBI->dbconnect($form->{'DBNAME'});
  my $q = qq|select SiteACL.*,Provider.Name from SiteACL left join Provider on Provider.ProvID=SiteACL.AccessID where SiteACL.ProvID=? and SiteACL.AccessOK=1 and SiteACL.Type='Clinic' and Provider.Active=1|;
#warn qq|selClinics: q=$q\n|;
  my $s = $dbh->prepare($q);
  $s->execute($ForProvID) || myDBI->dberror($q);
  while (my $r = $s->fetchrow_hashref)
  { $list->{"$r->{Name} ($r->{AccessID})"} = $r->{AccessID}; }
  return($list) if ( $rtnList );
  my $SelStmt = DBA->makeSelect($form,$SelectedIDs,$list,'Provider','Name');
  return($SelStmt);
}
# these are the Providers the ReqProvID has access to
sub selProviders
{
  my ($self,$form,$ReqProvID,$SelectedIDs,$rtnList) = @_;
#warn qq|selProviders: Req=${ReqProvID}, Sel=$SelectedIDs\n|;
  my $ForProvID = $ReqProvID ? $ReqProvID : $form->{LOGINPROVID};
  my $list = ();
  my $dbh = myDBI->dbconnect($form->{'DBNAME'});
  my $q = qq|select SiteACL.*,Provider.LName,Provider.FName from SiteACL left join Provider on Provider.ProvID=SiteACL.AccessID where SiteACL.ProvID=? and SiteACL.AccessOK=1 and SiteACL.Type='Provider' and Provider.Active=1|;
#warn qq|selProviders: q=$q\n|;
  my $s = $dbh->prepare($q);
  $s->execute($ForProvID) || myDBI->dberror($q);
  while (my $r = $s->fetchrow_hashref)
  { $list->{"$r->{LName}, $r->{FName} ($r->{AccessID})"} = $r->{AccessID}; }
  return($list) if ( $rtnList );
  my $SelStmt = DBA->makeSelect($form,$SelectedIDs,$list,'Provider','LName:FName');
  return($SelStmt);
}
#############################################################################
sub InsuranceSelect
{
  my ($self,$form,$ID,$InsID) = @_;
#warn qq|InsuranceSelect: ID=$ID, InsID=$InsID\n|;
  my $dbh = myDBI->dbconnect($form->{'DBNAME'});
  my $SelStmt = '';
  my $AGENT = SysAccess->verify($form,'Privilege=Agent');
  if ( !$AGENT && $ID ne 'new' && $InsID ne '' )
  {
    my $qPrAuth = qq|select ClientPrAuth.*, xInsurance.Name from ClientPrAuth left join xInsurance on xInsurance.ID='${InsID}' where ClientPrAuth.InsuranceID='${ID}'|;
#warn qq|q=\n$qPrAuth\n|;
    my $sPrAuth = $dbh->prepare($qPrAuth);
    $sPrAuth->execute() || myDBI->dberror($qPrAuth);
    while ( my $rPrAuth = $sPrAuth->fetchrow_hashref )
    { 
      if ( $rPrAuth->{PAnumber} eq '' )
      {
        if ( CDC->isLocked($form,$rPrAuth->{ID}) )
        { $SelStmt = qq|<INPUT TYPE="hidden" ID="InsID" NAME="LockedIns" VALUE="${InsID}" >$rPrAuth->{Name}   (Insurance locked waiting for PA authorization)|; }
      }
      else
      { $SelStmt = qq|<INPUT TYPE="hidden" ID="InsID" NAME="LockedIns" VALUE="${InsID}" >$rPrAuth->{Name}   (Insurance locked with Authorized PA)|; }
      last if ( $SelStmt ne '' );
    }
    $sPrAuth->finish();
  }
  if ( $SelStmt eq '' )
  {
    $SelStmt = qq|
      <SELECT ID="InsID" NAME="Insurance_InsID_1" ONCHANGE="callAjax('vInsID',this.value,this.id,'&d='+document.Insurance.Insurance_InsID_1.value);" >
| . DBA->selInsurance($form,$InsID). qq|
      </SELECT> 
      <SPAN ID="msgInsID"></SPAN>|;
  }
  return($SelStmt);
}
#############################################################################
sub genPopUp
{
  my ($self) = @_;
  my $html = qq|
<SCRIPT LANGUAGE="JavaScript">newtextMsg('prpa','Click here to Print this Prior Authorization');</SCRIPT>
<SCRIPT LANGUAGE="JavaScript">newtextMsg('PAlog','Click here to Print the logged activity');</SCRIPT>
<SCRIPT LANGUAGE="JavaScript">newtextMsg('invpa','Click here to Print Inventory for this Prior Authorization');</SCRIPT>
<SCRIPT LANGUAGE="JavaScript">newtextMsg('prapp','Click here to Print an Approved PA');</SCRIPT>
<SCRIPT LANGUAGE="JavaScript">newtextMsg('prtp','Click here to Print this Treatment Plan');</SCRIPT>
<SCRIPT LANGUAGE="JavaScript">newtextMsg('prcdc','Click here to Print the CDC');</SCRIPT>
|;
  return($html);
}
sub getAgencyName()
{
  my ($self,$form,$PIN) = @_;
  my $dbh = myDBI->dbconnect($form->{'DBNAME'});
  my $AgencyName = '';
    my $qContracts = qq|
select Contracts.PIN,Provider.Name,ProviderControl.NPI
 from Contracts
  left join Provider on Provider.ProvID=Contracts.ProvID
  left join ProviderControl on ProviderControl.ProvID=Contracts.ProvID
  left join xInsurance on xInsurance.ID=Contracts.InsID
 where xInsurance.Descr LIKE '%medicaid%' and Contracts.PIN=?
 order by Contracts.PIN, xInsurance.Name|;
    my $sContracts = $dbh->prepare($qContracts);
    $sContracts->execute($PIN);
    if ( $rContracts = $sContracts->fetchrow_hashref )
    { $AgencyName = qq|Agency: $rContracts->{Name} ($rContracts->{NPI}/${PIN})|; }
    else
    {
      my $qCredentials = qq|
select Credentials.*,Provider.FName,Provider.LName,ProviderControl.NPI
 from Credentials
  left join Provider on Provider.ProvID=Credentials.ProvID
  left join ProviderControl on ProviderControl.ProvID=Credentials.ProvID
  left join xInsurance on xInsurance.ID=Credentials.InsID
  left join okmis_config.xCredentials on xCredentials.ID=Credentials.CredID
 where xInsurance.Descr LIKE '%medicaid%'
   and (xCredentials.Abbr='indlbhp' or xCredentials.Abbr='indpsych')
   and Credentials.PIN=?
 order by Credentials.Rank|;
      my $sCredentials = $dbh->prepare($qCredentials);
      $sCredentials->execute($PIN);
      if ( $rCredentials = $sCredentials->fetchrow_hashref )
      { $AgencyName = qq|Provider: $rCredentials->{LName}, $rCredentials->{FName} ($rCredentials->{NPI}/${PIN})|; }
      $sCredentials->finish();
    }
    $sContracts->finish();
  return($AgencyName);
}
sub setFilterSearch
{
  my ($self,$func,$formname,$searchlist,$alpha) = @_;
#<SCRIPT TYPE="text/javascript">
#<!--
#var ${func} = new ${func}list(document.${formname}.${searchlist});
#//-->
#</SCRIPT>
  my $add = $alpha ? qq|
<P>
or Select:
<A HREF="javascript:${func}.set('^A')" TITLE="Show items starting with A">A</A>
<A HREF="javascript:${func}.set('^B')" TITLE="Show items starting with B">B</A>
<A HREF="javascript:${func}.set('^C')" TITLE="Show items starting with C">C</A>
<A HREF="javascript:${func}.set('^D')" TITLE="Show items starting with D">D</A>
<A HREF="javascript:${func}.set('^E')" TITLE="Show items starting with E">E</A>
<A HREF="javascript:${func}.set('^F')" TITLE="Show items starting with F">F</A>
<A HREF="javascript:${func}.set('^G')" TITLE="Show items starting with G">G</A>
<A HREF="javascript:${func}.set('^H')" TITLE="Show items starting with H">H</A>
<A HREF="javascript:${func}.set('^I')" TITLE="Show items starting with I">I</A>
<A HREF="javascript:${func}.set('^J')" TITLE="Show items starting with J">J</A>
<A HREF="javascript:${func}.set('^K')" TITLE="Show items starting with K">K</A>
<A HREF="javascript:${func}.set('^L')" TITLE="Show items starting with L">L</A>
<A HREF="javascript:${func}.set('^M')" TITLE="Show items starting with M">M</A>
<A HREF="javascript:${func}.set('^N')" TITLE="Show items starting with N">N</A>
<A HREF="javascript:${func}.set('^O')" TITLE="Show items starting with O">O</A>
<A HREF="javascript:${func}.set('^P')" TITLE="Show items starting with P">P</A>
<A HREF="javascript:${func}.set('^Q')" TITLE="Show items starting with Q">Q</A>
<A HREF="javascript:${func}.set('^R')" TITLE="Show items starting with R">R</A>
<A HREF="javascript:${func}.set('^S')" TITLE="Show items starting with S">S</A>
<A HREF="javascript:${func}.set('^T')" TITLE="Show items starting with T">T</A>
<A HREF="javascript:${func}.set('^U')" TITLE="Show items starting with U">U</A>
<A HREF="javascript:${func}.set('^V')" TITLE="Show items starting with V">V</A>
<A HREF="javascript:${func}.set('^W')" TITLE="Show items starting with W">W</A>
<A HREF="javascript:${func}.set('^X')" TITLE="Show items starting with X">X</A>
<A HREF="javascript:${func}.set('^Y')" TITLE="Show items starting with Y">Y</A>
<A HREF="javascript:${func}.set('^Z')" TITLE="Show items starting with Z">Z</A>
</P>
| : '';
  my $html = qq|
    <TD CLASS="strcol" >
<P>
Filter by regular expression:<BR>
      <INPUT TYPE="text" ID="${func}regexp" NAME="${func}regexp" VALUE="" ONFOCUS="select()" MAXLENGTH="30" SIZE="30" >
      <INPUT TYPE="button" ONCLICK="${func}.set(this.form.${func}regexp.value)" value="Filter">
</P>
${add}
    </TD>
|;
  return($html);
}
sub setFilterScript
{
  my ($self,$func,$formname,$searchlist) = @_;
  my $html = qq|
<SCRIPT TYPE="text/javascript">
<!--
var ${func} = new ${func}list(document.${formname}.${searchlist});
//-->
</SCRIPT>
|;
  return($html);
}
sub getTag
{
  my ($self,$form,$AID) = @_;
  my $dbh = myDBI->dbconnect($form->{'DBNAME'});
  my $s = $dbh->prepare("select AgencyTag from ProviderControl where ProvID=?");
  $s->execute($AID) || myDBI->dberror("getTag: $AID");
  my ($Tag) = $s->fetchrow_array;
  if ( $Tag eq '' )
  { my ($pfx,$db) = split('_',$form->{'DBNAME'}); $Tag = $db; }
  $s->finish();
  return($Tag);
}
sub ifld()
{
  my ($self,$form,$name,$type) = @_;
#warn "ifld: name=$name, type=$type\n";
#foreach my $f ( sort keys %{$form} ) { warn "ifld: $f=$form->{$f}\n"; }
  my $val = $form->{$name};
  my $html = '';
  if ( $type =~ /readonly/i )
  { $html .= qq|<INPUT TYPE="text" ID="${name}" NAME="${name}" VALUE="${val}" READLONLY >\n|; }
  elsif ( $type =~ /displayonly/i )
  { $html .= qq|<INPUT TYPE="hidden" ID="${name}" NAME="${name}" VALUE="${val}" > <SPAN ID="${name}_display">${val}</SPAN>\n|; }
  return($html);
}
#############################################################################
1;
