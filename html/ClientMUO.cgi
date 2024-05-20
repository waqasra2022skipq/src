[[myHTML->newPage(%form+Client Intake)]]

<SCRIPT LANGUAGE="JavaScript" SRC="/cgi/js/novalidate.js"> </SCRIPT>
<LINK HREF="/cfg/menuV2.css" REL="stylesheet" TYPE="text/css" >
<SCRIPT type="text/javascript" src="/cgi/menu/js/menuV2.js" ></SCRIPT>

<FORM NAME="Intake" ACTION="/cgi/bin/mis.cgi" METHOD="POST" >
<TABLE CLASS="main fullsize" >
  <TR >
    <TD CLASS="strcol" >[[myHTML->getHTML(%form+MU.menu+1)]]</TD>
    <TD CLASS="strcol" >
      <<<Client_FName_1>>> <<<Client_MName_1>>> <<<Client_LName_1>>> (<<<Client_ClientID_1>>>) <<<Client_SSN_1>>>
      <BR>
      Treatment History
    </TD>
    <TD CLASS="numcol" >[[gHTML->setLINKS(%form+back)]]</TD>
  </TR>
</TABLE>
<TABLE CLASS="home fullsize" >
  <TR ><TD CLASS="port hdrtxt" COLSPAN="2" >OBSERVATION INFORMATION</TD></TR>
  <TR >
    <TD COLSPAN="2" >
<SPAN ID="ListClientTreatments" >
[[myHTML->ListSel(%form+ListClientTreatments+<<<Client_ClientID>>>+<<<LINKID>>>+<<<Client_Locked_1>>>)]]
</SPAN>
    </TD>
  </TR>
  <TR ><TD CLASS="port hdrtxt" WIDTH="50%" >Last Visit Information</TD><TD>&nbsp;</TD></TR>
[[gHTML->ClientMU(%form+<<<Client_ClientID>>>)]]
  <TR >
    <TD COLSPAN="2" >
<SPAN ID="ShowClientNotes" >
[[myHTML->ListSel(%form+ShowClientNotes+<<<Client_ClientID>>>+<<<LINKID>>>+<<<Client_Locked_1>>>)]]
</SPAN>
    </TD>
  </TR>
</TABLE>
<TABLE CLASS="main fullsize" >
  <TR >
    <TD CLASS="numcol" >
      <INPUT TYPE=submit ONCLICK="return validate(this.form);" NAME="[[myForm->genLink(ClientMeds+ClientMU.cgi)]]" VALUE="Client Information">
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
