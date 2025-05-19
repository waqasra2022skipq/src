[[myHTML->newPage(%form+Client CSSRS)]]

<SCRIPT LANGUAGE="JavaScript" SRC="/src/cgi/js/NoEnter.js"> </SCRIPT>
<SCRIPT LANGUAGE="JavaScript" SRC="/src/cgi/js/vEntry.js"> </SCRIPT>
<SCRIPT LANGUAGE="JavaScript" SRC="/src/cgi/js/vClientCSSRS_3.js"> </SCRIPT>
<SCRIPT LANGUAGE="JavaScript" SRC="/src/cgi/js/vDate.js"> </SCRIPT>

<FORM NAME="ClientCSSRS" ACTION="/src/cgi/bin/mis.cgi" METHOD="POST" >
<TABLE CLASS="main fullsize" >
  <TR >
    <TD CLASS="strcol" >
      <<<Client_FName_1>>> <<<Client_MName_1>>> <<<Client_LName_1>>> (<<<Client_ClientID_1>>>) <<<Client_SSN_1>>>
      <BR>
      C-SSRS (Columbia Suicide Severity Risk and Protective Factors)
    </TD>
    <TD CLASS="numcol" >[[gHTML->setLINKS(%form+back)]]</TD>
  </TR>
</TABLE>
<TABLE CLASS="home fullsize" >
  <TR ><TD CLASS="port hdrtxt" >C-SSRS (Columbia Suicide Severity Risk and Protective Factors): Full Scale Lifetime / Recent</TD></TR>
  <TR ><TD CLASS="port strcol" >
<BR><BR>
<BR><BR>
  </TD></TR>
  <TR >
    <TD CLASS="port hdrtxt" >
[[[myHTML->setHTML(%form+ClientCSSRS)]]]
    </TD>
  </TR>
</TABLE>
<TABLE CLASS="main fullsize" >
  <TR >
    <TD CLASS="numcol" >
      <INPUT TYPE="submit" ONCLICK="return vDELETE('Are you sure you want to delete this record?');" NAME="ClientCSSRS_DELETE_1=1&UpdateTables=all&misPOP=1" VALUE="Delete">
      <INPUT TYPE="submit" ONCLICK="return validate(this.form);" NAME="UpdateTables=all&misPOP=1" VALUE="Add/Update">
    </TD>
  </TR>
</TABLE>

</LOADHIDDEN>
</FORM>
<SCRIPT LANGUAGE="JavaScript">
document.ClientCSSRS.elements[0].focus();
// just to OPENTABLES...
//<<<ClientCSSRS_ClientID_1>>>
</SCRIPT>

[[myHTML->rightpane(%form+search)]]
