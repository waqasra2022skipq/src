[[myHTML->newPage(%form+Medicare Note)]]
[[gHTML->vClient(%form+<<<Client_ClientID_1>>>]]

<SCRIPT LANGUAGE="JavaScript" SRC="/cgi/js/NoEnter.js"> </SCRIPT>
<SCRIPT LANGUAGE="JavaScript" SRC="/cgi/js/vEntry.js"> </SCRIPT>
<SCRIPT LANGUAGE="JavaScript" SRC="/cgi/js/vDate.js"> </SCRIPT>
<SCRIPT LANGUAGE="JavaScript" SRC="/cgi/js/pickDate.js"> </SCRIPT>
<SCRIPT LANGUAGE="JavaScript" SRC="/cgi/js/vTime.js"> </SCRIPT>
<SCRIPT LANGUAGE="JavaScript" SRC="/cgi/js/vNum.js"> </SCRIPT>
[[gHTML->vNoteServiceType(%form+<<<LOGINPROVID>>>+<<<Client_ClientID_1>>>+Agent]]
[[gHTML->vNoteInt(%form)]]
<SCRIPT LANGUAGE="JavaScript" SRC="/cgi/js/vNoteMedi.js"> </SCRIPT>
<SCRIPT type="text/javascript" src="/cgi/js/ajaxrequest.js"></SCRIPT>
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
  <TR ><TD CLASS="heading" >Medicare Note (<<<Treatment_TrID_1>>>)</TD></TR>
</TABLE>
[[[gHTML->setNoteMsg(%form)]]]
[[[gHTML->setNoteRev(%form)]]]
[[[gHTML->setNoteBillInfo(%form+4)]]]

<HR WIDTH="90%" >
[[[gHTML->setNoteTrPlan(%form)]]]
<HR WIDTH="90%" >
[[[gHTML->setNoteTxt(%form+4)]]]
[[[gHTML->setNoteButtons(%form+4)]]]

<INPUT TYPE="hidden" NAME="Treatment_Type_1" VALUE="4" >
<INPUT TYPE="hidden" NAME="Treatment_ProbNum_1" VALUE="<<Treatment_ProbNum_1>>" >
<INPUT TYPE="hidden" NAME="ProgNotes_ClientID_1" VALUE="<<ProgNotes_ClientID_1>>" >
<INPUT TYPE="hidden" NAME="ClientTherapyNotes_CreateDate_1" VALUE="<<ClientTherapyNotes_CreateDate_1>>" >
<INPUT TYPE="hidden" NAME="TODAY" VALUE="<<TODAY>>" >
<INPUT TYPE="hidden" NAME="AppointmentID" VALUE="<<AppointmentID>>" >

<INPUT TYPE="hidden" NAME="post_update" VALUE="PostUpd->updNote(%form)" >
</LOADHIDDEN>
<SCRIPT LANGUAGE="JavaScript">
document.Treatment.elements[0].focus();
callAjax('vNote','<<<Treatment_ContLogDate_1>>>','ContDate','&p=<<<Treatment_ProvID_1>>>&c=<<<Treatment_ClientID_1>>>&id=<<<Treatment_TrID_1>>>&s=<<<Treatment_SCID_1>>>&b=<<<Treatment_ContLogBegTime_1>>>&e=<<<Treatment_ContLogEndTime_1>>>','validateNote.pl');
</SCRIPT>
</FORM>

[[myHTML->rightpane(%form+search)]]
