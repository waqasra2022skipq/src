[[myHTML->newPage(%form+TFC Times)]]

<SCRIPT LANGUAGE="JavaScript" SRC="/cgi/js/NoEnter.js"> </SCRIPT>
<SCRIPT LANGUAGE="JavaScript" SRC="/cgi/js/vEntry.js"> </SCRIPT>
<SCRIPT LANGUAGE="JavaScript" SRC="/cgi/js/vTFCTimes.js"> </SCRIPT>

<<<Client_FName_1>>> <<<Client_MName_1>>> <<<Client_LName_1>>> 
<FONT CLASS=subtitle > (<<<Client_ClientID_1>>>) <<<Client_SSN_1>>> </FONT>
<FORM NAME="TFCTimes" ACTION="/cgi/bin/mis.cgi" METHOD="POST" >
<DIV ALIGN="center" >
<HR WIDTH="90%" >
<!-- KEEP the TrID IN HERE OTHERWISE THE Treatment TABLE IS NOT READ -->
<TABLE CLASS="port fullsize" >
  <TR >
    <TD CLASS="port hdrtxt" >TrID: <<<Treatment_TrID_1>>></TD>
    <TD CLASS="port numcol" >Date: <<<Treatment_ContLogDate_1>>></TD>
  </TR>
</TABLE>
[[gHTML->disTFCTimes(%form)]]
<TABLE CLASS="main fullsize" >
  <TR >
    <TD CLASS="numcol" >
      <INPUT TYPE="submit" ONCLICK="return validate(this.form);" NAME="misPOP=1" VALUE="Cancel">
      <INPUT TYPE="submit" ONCLICK="return validate(this.form);" NAME="UpdateTables=all&misPOP=1" VALUE="Add/Update">
    </TD>
  </TR>
</TABLE>
<HR WIDTH="90%" >

</LOADHIDDEN>
</FORM>
<SCRIPT LANGUAGE="JavaScript">
document.TFCTimes.elements[0].focus();
</SCRIPT>

[[myHTML->rightpane(%form+search)]]
