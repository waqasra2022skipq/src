[[myHTML->newPage(%form+Client ASI)]]

<SCRIPT LANGUAGE="JavaScript" SRC="/src/cgi/js/novalidate.js"> </SCRIPT>

<FORM NAME="ClientASI" ACTION="/src/cgi/bin/mis.cgi" METHOD="POST" >
<TABLE CLASS="main fullsize" >
  <TR >
    <TD CLASS="strcol" >
      <<<Client_FName_1>>> <<<Client_MName_1>>> <<<Client_LName_1>>> (<<<Client_ClientID_1>>>) <<<Client_SSN_1>>>
      <BR>Addiction Severity Index (ASI) Page
    </TD>
    <TD CLASS="numcol" >[[gHTML->setLINKS(%form+back)]]</TD>
  </TR>
</TABLE>
<TABLE CLASS="port fullsize" >
  <TR ><TD CLASS="home strcol" >Legend:<BR>G5: Date of Interview<BR>G6: Time Begun<BR>G7: Time End<BR>G8: Class (1=Intake,2=Follow-up)<BR>G9: Contact Code (1=Inperson,2=Telephone)</TD></TR>
  <TR ><TD CLASS="port hdrtxt" >Before Adding a NEW ASI please complete the current ASI.</TD></TR>
  <TR ><TD >
<SPAN ID="ListClientASI" >
[[myHTML->ListSel(%form+ListClientASI+<<<Client_ClientID>>>+<<<LINKID>>>+<<<Client_Locked_1>>>)]]
</SPAN>
  </TD></TR >
</TABLE>

</LOADHIDDEN>
</FORM>
[[myHTML->rightpane(%form+search)]]
