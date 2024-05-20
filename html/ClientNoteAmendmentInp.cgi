[[myHTML->newHTML(%form+Client Note Amendment+noclock countdown_10)]]

<SCRIPT LANGUAGE="JavaScript" SRC="/cgi/js/vEntry.js"> </SCRIPT>
<SCRIPT LANGUAGE="JavaScript" SRC="/cgi/js/vClientNoteAmendments.js"> </SCRIPT>
<SCRIPT LANGUAGE="JavaScript" SRC="/cgi/js/vDate.js"> </SCRIPT>

<FORM NAME="ClientNoteAmendments" ACTION="/cgi/bin/mis.cgi" METHOD="POST" >
<TABLE CLASS="main fullsize" >
  <TR >
    <TD CLASS="strcol" >
      <<<Client_FName_1>>> <<<Client_MName_1>>> <<<Client_LName_1>>> (<<<Client_ClientID_1>>>) <<<Client_SSN_1>>>
      <BR>
      Note or Visit Ammendment
    </TD>
  </TR>
</TABLE>
<TABLE CLASS="home fullsize" >
  <TR ><TD CLASS="port hdrtxt" >Client Note Amendments</TD></TR>
  <TR >
    <TD CLASS="port hdrtxt" >
[[[myHTML->setHTML(%form+ClientNoteAmendments)]]]
    </TD>
  </TR>
</TABLE>
<TABLE CLASS="main fullsize" >
  <TR>
    <TD CLASS="numcol" >
      <INPUT TYPE="submit" ONCLICK="return vDELETE('Are you sure you want to delete this record?');" NAME="ClientNoteAmendments_DELETE_1=1&UpdateTables=all" VALUE="Delete">
      <INPUT TYPE="button" NAME="cancel" VALUE="Cancel" ONCLICK="javascript: window.close()" >
      <INPUT TYPE="submit" ONCLICK="return validate(this.form);" NAME="UpdateTables=all" VALUE="Add/Update">
    </TD>
  </TR>
</TABLE>

<INPUT TYPE="hidden" NAME="CLOSEWINDOW" VALUE="CLOSE">
</LOADHIDDEN>
<SCRIPT LANGUAGE="JavaScript" >
// just to OPENTABLES...
//<<<Treatment_TrID_1>>>
//<<<ClientNoteAmendments_ID_1>>>
  document.ClientNoteAmendments.elements[0].focus();
</SCRIPT>
</FORM>
