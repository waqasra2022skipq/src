[[myHTML->newHTML(%form+Physician Note+allleft mismenu checkpopupwindow)]]
[[gHTML->vClient(%form+<<<Client_ClientID_1>>>]]

<SCRIPT LANGUAGE="JavaScript" SRC="/src/cgi/js/Utils.js"> </SCRIPT>
<SCRIPT LANGUAGE="JavaScript" SRC="/src/cgi/js/NoEnter.js"> </SCRIPT>
<SCRIPT LANGUAGE="JavaScript" SRC="/src/cgi/js/vEntry.js"> </SCRIPT>
<SCRIPT type="text/javascript" src="/src/cgi/js/ajaxrequest.js"></SCRIPT>
<SCRIPT LANGUAGE="JavaScript" SRC="/src/cgi/js/vDate.js"> </SCRIPT>
<SCRIPT LANGUAGE="JavaScript" SRC="/src/cgi/js/pickDate.js"> </SCRIPT>
<SCRIPT LANGUAGE="JavaScript" SRC="/src/cgi/js/vTime.js"> </SCRIPT>
<SCRIPT LANGUAGE="JavaScript" SRC="/src/cgi/js/vNum.js"> </SCRIPT>
<SCRIPT LANGUAGE="JavaScript" SRC="/src/cgi/js/vHeight.js"> </SCRIPT>
[[gHTML->vNoteServiceType(%form+<<<LOGINPROVID>>>+<<<Client_ClientID_1>>>+Agent]]
<SCRIPT LANGUAGE="JavaScript" SRC="/src/cgi/js/vNotePhys.js"> </SCRIPT>
</HEAD>

<FORM NAME="Treatment" ACTION="/cgi/bin/mis.cgi" METHOD="POST" >
<TABLE CLASS="main fullsize" >
  <TR >
    <TD CLASS="strcol" > <<<Client_FName_1>>> <<<Client_MName_1>>> <<<Client_LName_1>>> (<<<Client_ClientID_1>>>) <<<Client_SSN_1>>> <BR>Chart Entry Page </TD>
    <TD CLASS="numcol" >[[gHTML->setLINKS(%form+back)]]</TD>
  </TR>
</TABLE>
[[[gHTML->setPhysNote(%form)]]]

<INPUT TYPE="hidden" NAME="Treatment_Type_1" VALUE="2" >
<INPUT TYPE="hidden" NAME="Treatment_ProbNum_1" VALUE="<<Treatment_ProbNum_1>>" >
<INPUT TYPE="hidden" NAME="PhysNotes_ClientID_1" VALUE="<<PhysNotes_ClientID_1>>" >
<INPUT TYPE="hidden" NAME="ClientTherapyNotes_CreateDate_1" VALUE="<<ClientTherapyNotes_CreateDate_1>>" >
<INPUT TYPE="hidden" NAME="TODAY" VALUE="<<TODAY>>" >
<INPUT TYPE="hidden" NAME="AppointmentID" VALUE="<<AppointmentID>>" >

<INPUT TYPE="hidden" NAME="post_update" VALUE="PostUpd->updNote(%form)" >
</LOADHIDDEN>
<SCRIPT LANGUAGE="JavaScript">
callAjax('vNote','<<<Treatment_ContLogDate_1>>>','ContDate','&p=<<<Treatment_ProvID_1>>>&c=<<<Treatment_ClientID_1>>>&id=<<<Treatment_TrID_1>>>&s=<<<Treatment_SCID_1>>>&b=<<<Treatment_ContLogBegTime_1>>>&e=<<<Treatment_ContLogEndTime_1>>>','validateNote.pl');
callAjax('Procedure','<<PhysNotes_InOfficeProcedure_1>>','selIOP','&name=PhysNotes_InOfficeProcedure_1','popup.pl');
callAjax('NPI','<<PhysNotes_RefToNPI_1>>','selREFTO','&name=PhysNotes_RefToNPI_1','popup.pl');
callAjax('Procedure','<<PhysNotes_ReferredProcedure_1>>','selREFP','&name=PhysNotes_ReferredProcedure_1','popup.pl');
document.Treatment.elements[0].focus();
</SCRIPT>
</FORM>

[[myHTML->rightpane(%form+search)]]
