[[myHTML->newHTML(%form+Client Discharges+allleft mismenu)]]

<SCRIPT LANGUAGE="JavaScript" >
function validate(form) { return true; }
</SCRIPT>
<FORM NAME="ListDischarge" ACTION="/src/cgi/bin/mis.cgi" METHOD="POST" >
<TABLE CLASS="main fullsize" >
  <TR >
    <TD CLASS="strcol" >
      <<<Client_FName_1>>> <<<Client_MName_1>>> <<<Client_LName_1>>> (<<<Client_ClientID_1>>>) <<<Client_SSN_1>>>
      <BR>
      List Client Discharges Page
      [[DBUtil->isEQ(<<Client_Active_1>>+1)<SPAN STYLE="color: red" >(IsActive)</SPAN>]]
      [[DBUtil->isEQ(<<Client_Active_1>>+0)<SPAN STYLE="color: red" >(NotActive)</SPAN>]]
    </TD>
    <TD CLASS="numcol" >[[gHTML->setLINKS(%form+back)]]</TD>
  </TR>
</TABLE>
<SPAN ID="ListClientDischarge" >
[[myHTML->ListSel(%form+ListClientDischarge+<<<Client_ClientID>>>+<<<LINKID>>>+<<<Client_Locked_1>>>)]]
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
