[[myHTML->newPage(%form+Client Admissions)]]

<SCRIPT LANGUAGE="JavaScript" SRC="/src/cgi/js/novalidate.js"> </SCRIPT>
<FORM NAME="ListAdmit" ACTION="/src/cgi/bin/mis.cgi" METHOD="POST" >
<TABLE CLASS="main fullsize" >
  <TR >
    <TD CLASS="strcol" >
      <<<Client_FName_1>>> <<<Client_MName_1>>> <<<Client_LName_1>>> (<<<Client_ClientID_1>>>) <<<Client_SSN_1>>>
      <BR>List Client Admits Page
      [[DBUtil->isEQ(<<Client_Active_1>>+1)<SPAN STYLE="color: red" >(IsActive)</SPAN>]]
      [[DBUtil->isEQ(<<Client_Active_1>>+0)<SPAN STYLE="color: red" >(NotActive)</SPAN>]]
    </TD>
    <TD CLASS="numcol" >[[gHTML->setLINKS(%form+back)]]</TD>
  </TR>
</TABLE>
<SPAN ID="ListClientAdmits" >
[[myHTML->ListSel(%form+ListClientAdmits+<<<Client_ClientID>>>+<<<LINKID>>>+<<<Client_Locked_1>>>)]]
</SPAN>

<TABLE CLASS="main fullsize" >
  <TR >
    <TD CLASS="numcol" >
      [[DBUtil->isEQ(<<Client_Active_1>>+1)<INPUT TYPE="submit" ONCLICK="return validate(this.form);" NAME="Client_Active_1=0&UpdateTables=all&misPOP=1" VALUE="DE-Activate Client">]]
      [[DBUtil->isEQ(<<Client_Active_1>>+0)<INPUT TYPE="submit" ONCLICK="return validate(this.form);" NAME="Client_Active_1=1&UpdateTables=all&misPOP=1" VALUE="Activate Client">]]
    </TD>
  </TR>
</TABLE>

</LOADHIDDEN>
</FORM>
[[myHTML->rightpane(%form+search)]]
