[[myHTML->newPage(%form+Client Intake)]]

<SCRIPT LANGUAGE="JavaScript" SRC="/src/cgi/js/novalidate.js"> </SCRIPT>

<FORM NAME="Intake" ACTION="/cgi/bin/mis.cgi" METHOD="POST" >
<TABLE CLASS="main fullsize" >
  <TR >
    <TD CLASS="strcol" >
      <<<Client_FName_1>>> <<<Client_MName_1>>> <<<Client_LName_1>>> (<<<Client_ClientID_1>>>) <<<Client_SSN_1>>>
      <BR>
      Treatment History
    </TD>
    <TD CLASS="numcol" >[[gHTML->setLINKS(%form+back)]]</TD>
  </TR>
</TABLE>
<TABLE CLASS="home fullsize" >
  <TR ><TD CLASS="port hdrtxt" COLSPAN="2" >TEST INFORMATION</TD></TR>
  <TR ><TD CLASS="port hdrtxt" WIDTH="50%" >NewCrop Medication Information</TD><TD WIDTH="50%" >&nbsp;</TD></TR>
  <TR >
    <TD COLSPAN="2" >
<SPAN ID="ListClientMeds" >
[[myHTML->ListSel(%form+ListClientMeds+<<<Client_ClientID>>>+<<<LINKID>>>+<<<Client_Locked_1>>>)]]
</SPAN>
    </TD>
  </TR>
</TABLE>

<INPUT TYPE="hidden" NAME="ProviderID" VALUE="<<ProviderID>>" >
</LOADHIDDEN>
</FORM>
<SCRIPT LANGUAGE="JavaScript">
document.Intake.elements[0].focus();
</SCRIPT>

[[myHTML->rightpane(%form+search)]]
