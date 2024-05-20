[[myHTML->newPage(%form+TFC Note)]]

<SCRIPT LANGUAGE="JavaScript" SRC="/cgi/js/NoEnter.js"> </SCRIPT>
<SCRIPT LANGUAGE="JavaScript" SRC="/cgi/js/vEntry.js"> </SCRIPT>
<SCRIPT LANGUAGE="JavaScript" SRC="/cgi/js/vDate.js"> </SCRIPT>
<SCRIPT LANGUAGE="JavaScript" SRC="/cgi/js/vTime.js"> </SCRIPT>
<SCRIPT LANGUAGE="JavaScript" SRC="/cgi/js/vNum.js"> </SCRIPT>
[[gHTML->vNoteServiceType(%form+<<<LOGINPROVID>>>+<<<Client_ClientID_1>>>+Agent]]
<SCRIPT LANGUAGE="JavaScript" SRC="/cgi/js/validateNote.js"> </SCRIPT>
</HEAD>

<FORM NAME="Treatment" ACTION="/cgi/bin/mis.cgi" METHOD="POST" >
<TABLE CLASS="main fullsize" >
  <TR >
    <TD CLASS="strcol" > <<<Client_FName_1>>> <<<Client_MName_1>>> <<<Client_LName_1>>> (<<<Client_ClientID_1>>>) <<<Client_SSN_1>>> <BR>Chart Entry Page </TD>
    <TD CLASS="numcol" >[[gHTML->setLINKS(%form+back)]]</TD>
  </TR>
</TABLE>
<HR WIDTH="90%" >
<TABLE CLASS="port fullsize" >
  <TR ><TD CLASS="heading" COLSPAN=7 >TFC Note Entry</TD></TR>
</TABLE>
[[[gHTML->setNoteMsg(%form)]]]
<TABLE CLASS="home fullsize" >
  <TR ><TD COLSPAN=7 >&nbsp;</TD></TR>
  <TR >
    <TD WIDTH=15% ALIGN=center ><B>TrID</B></TD>
    <TD WIDTH=15% ALIGN=center ><B>Entry Date</B></TD>
    <TD WIDTH=15% ALIGN=center ><B>Reviewed</B></TD>
    <TD WIDTH=15% ALIGN=center ><B>Billed</B></TD>
    <TD WIDTH=15% ALIGN=center ><B>InProcess</B></TD>
    <TD WIDTH=15% ALIGN=center ><B>Reconciled</B></TD>
    <TD WIDTH=15% ALIGN=center ><B>Scholarshipped</B></TD>
  </TR>
  <TR >
    <TD WIDTH=15% ALIGN=center ><<<Treatment_TrID_1>>>&nbsp;</TD>
    <TD WIDTH=15% ALIGN=center ><<<Treatment_ChartEntryDate_1>>>&nbsp;</TD>
    <TD WIDTH=15% ALIGN=center >
[[SysAccess->verify(%form+Privilege=NoteReview)      <INPUT TYPE=text NAME="Treatment_MgrRevDate_1" VALUE="<<Treatment_MgrRevDate_1>>" ONFOCUS="this.blur()" SIZE="15" > ]]
[[!SysAccess->verify(%form+Privilege=NoteReview)      <INPUT TYPE="hidden" NAME="Treatment_MgrRevDate_1" VALUE="<<Treatment_MgrRevDate_1>>" > <<<Treatment_MgrRevDate_1>>>]]
    </TD>
    <TD WIDTH=15% ALIGN=center ><<<Treatment_BillDate_1>>>&nbsp;</TD>
    <TD WIDTH=15% ALIGN=center ><<<Treatment_CIPDate_1>>>&nbsp;</TD>
    <TD WIDTH=15% ALIGN=center ><<<Treatment_RecDate_1>>>&nbsp;</TD>
    <TD WIDTH=15% ALIGN=center ><<<Treatment_COPLDate_1>>>&nbsp;</TD>
  </TR>
  <TR >
    <TD WIDTH=15% ALIGN=center >&nbsp;</TD>
    <TD WIDTH=15% ALIGN=center >&nbsp;</TD>
    <TD WIDTH=15% ALIGN=center >
[[SysAccess->verify(%form+Privilege=NoteReview)      <INPUT TYPE="checkbox" NAME="MgrRevFlag" VALUE=1 <<MgrRevFlag=checkbox>> ONCLICK="vMgrRev(form)" > Reviewed ]]
[[!SysAccess->verify(%form+Privilege=NoteReview)      <INPUT TYPE="hidden" NAME="MgrRevFlag" VALUE="" >]]
      &nbsp;
    </TD>
    <TD WIDTH=15% ALIGN=center >&nbsp;</TD>
    <TD WIDTH=15% ALIGN=center >&nbsp;</TD>
    <TD WIDTH=15% ALIGN=center >&nbsp;</TD>
    <TD WIDTH=15% ALIGN=center >&nbsp;</TD>
  </TR>
  <TR ><TD COLSPAN=7 >&nbsp;</TD></TR>
</TABLE>
<TABLE CLASS="home fullsize" >
  <TR ><TD COLSPAN=3 >&nbsp;</TD></TR>
  <TR >
    <TD ><B>Service Code - Service Name</B></TD>
    <TD ><B>Place of Service</B></TD>
    <TD ><B>Date of Service</B></TD>
  </TR>
  <TR >
    <TD >
      <SELECT NAME="Treatment_SCID_1" ONCHANGE="return vSCID(this);" >
        [[DBA->selServiceCodes(%form+<<Treatment_SCID_1>>+0+<<<LOGINPROVID>>>+<<<Client_ClientID_1>>>+Agent)]] 
      </SELECT> 
    </TD>
    <TD ALIGN=center >
      <SELECT NAME="Treatment_POS_1" >
        [[DBA->selxTable(%form+xPOS+<<Treatment_POS_1>>+Descr)]]
      </SELECT> 
    </TD>
    <TD >
      <INPUT TYPE=text NAME="Treatment_ContLogDate_1" VALUE="<<Treatment_ContLogDate_1>>" ONFOCUS="select()" ONCHANGE="return vDate(this,1,this.form,0,'<<BEGCONTDATE>>','<<ENDCONTDATE>>');" SIZE=15>
    </TD>
  </TR>
  <TR ><TD COLSPAN=3 >&nbsp;</TD></TR>
</TABLE>
<HR WIDTH="90%" >

[[gHTML->disTFCTimes(%form)]]

<TABLE CLASS="home fullsize" >
  <TR ><TD CLASS="port hdrtxt" COLSPAN=3 ><B>Interventions</B></TD></TR>
  <TR >
    <TD CLASS="strcol" >
      Time-out(s) Number:
      <INPUT TYPE=text NAME="TFCNotes_TimeOuts_1" VALUE="<<TFCNotes_TimeOuts_1>>" ONCHANGE="return vNum(this,0,20);" SIZE=5 >
    </TD>
    <TD CLASS="strcol" >
      Length of Time:
      <INPUT TYPE=text NAME="TFCNotes_TOLength_1" VALUE="<<TFCNotes_TOLength_1>>" ONCHANGE="return vNum(this,0,200);" SIZE=5 >
      (min.)
    </TD>
    <TD CLASS="strcol" >
      Place:
      <INPUT TYPE=text NAME="TFCNotes_Place_1" VALUE="<<TFCNotes_Place_1>>" SIZE=35 >
    </TD>
  </TR>
  <TR >
    <TD CLASS="strcol" COLSPAN=2 >
      Loss of Privileges What?
      <INPUT TYPE=text NAME="TFCNotes_LOP_1" VALUE="<<TFCNotes_LOP_1>>" SIZE=50 >
    </TD>
    <TD CLASS="strcol" >
      Duration?
      <INPUT TYPE=text NAME="TFCNotes_LOPLength_1" VALUE="<<TFCNotes_LOPLength_1>>" ONCHANGE="return vNum(this,0,200);" SIZE=5 >
      (min.)
    </TD>
  </TR>
  <TR >
    <TD CLASS="strcol" COLSPAN=3 >
      Reason(s):
      <INPUT TYPE=text NAME="TFCNotes_LOPReason_1" VALUE="<<TFCNotes_LOPReason_1>>" SIZE=70 >
    </TD>
  </TR>
  <TR >
    <TD CLASS="strcol" COLSPAN=3 >
      Positive reinforcement:
      <INPUT TYPE=text NAME="TFCNotes_PositiveR_1" VALUE="<<TFCNotes_PositiveR_1>>" SIZE=70 >
    </TD>
  </TR>
  <TR >
    <TD CLASS="strcol" COLSPAN=3 >
      Negative reinforcement:
      <INPUT TYPE=text NAME="TFCNotes_NegativeR_1" VALUE="<<TFCNotes_NegativeR_1>>" SIZE=70 >
    </TD>
  </TR>
  <TR >
    <TD CLASS="strcol" >
      <INPUT TYPE=checkbox NAME="TFCNotes_CA_1" VALUE=1 <<TFCNotes_CA_1=checkbox>> >
      Contracting
    </TD>
    <TD CLASS="strcol" COLSPAN=2 >
      Incident report completed:
      <INPUT TYPE=radio NAME="TFCNotes_IR_1" VALUE=1 <<TFCNotes_IR_1=1>> > yes
      <INPUT TYPE=radio NAME="TFCNotes_IR_1" VALUE=0 <<TFCNotes_IR_1=0>> > no
    </TD>
  </TR>
</TABLE>
[[[gHTML->setNoteButtons(%form+5)]]]

<INPUT TYPE="hidden" NAME="Treatment_Type_1" VALUE="5" >
<INPUT TYPE="hidden" NAME="TODAY" VALUE="<<TODAY>>" >
<INPUT TYPE="hidden" NAME="AppointmentID" VALUE="<<AppointmentID>>" >

<INPUT TYPE="hidden" NAME="post_update" VALUE="PostUpd->updNote(%form)" >
</LOADHIDDEN>
</FORM>
<SCRIPT LANGUAGE="JavaScript">
[[SysAccess->verify(%form+Privilege=NoteReview)      if ( document.Treatment.Treatment_MgrRevDate_1.value != '' ) { document.Treatment.MgrRevFlag.checked = 1 } ]]
document.Treatment.elements[1].focus();
</SCRIPT>

[[myHTML->rightpane(%form+search)]]
