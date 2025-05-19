[[myHTML->newPage(%form+Client Intake)]]

<SCRIPT type="text/javascript" SRC="/src/cgi/js/ajaxrequest.js"> </SCRIPT>
<SCRIPT LANGUAGE="JavaScript" SRC="/src/cgi/js/novalidate.js"> </SCRIPT>
<LINK HREF="/cfg/menuV2.css" REL="stylesheet" TYPE="text/css" >
<SCRIPT type="text/javascript" src="/cgi/menu/js/menuV2.js" ></SCRIPT>

<FORM NAME="Intake" ACTION="/src/cgi/bin/mis.cgi" METHOD="POST" >
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
  <TR >
    <TD CLASS="port hdrtxt" WIDTH="50%" >
      Medication Information
      <A HREF="javascript:callAjax('ShowClientMeds','','ShowClientMeds','&active=1&Locked=0&Client_ClientID=<<<Client_ClientID>>>&LOGINPROVID=<<<LOGINPROVID>>>&LOGINUSERID=<<<LOGINUSERID>>>&LINKID=<<<LINKID>>>&mlt=<<<mlt>>>&LOGINUSERDB=<<<LOGINUSERDB>>>','popup.pl');" TITLE="Show ONLY Active Medications for Client">Active Only</A>
      /
      <A HREF="javascript:callAjax('ShowClientMeds','','ShowClientMeds','&active=0&Locked=0&Client_ClientID=<<<Client_ClientID>>>&LOGINPROVID=<<<LOGINPROVID>>>&LOGINUSERID=<<<LOGINUSERID>>>&LINKID=<<<LINKID>>>&mlt=<<<mlt>>>&LOGINUSERDB=<<<LOGINUSERDB>>>','popup.pl');" TITLE="Show ALL Medications for Client">Show All</A>
    </TD>
    <TD CLASS="numcol" WIDTH="50%" >
      <A HREF="javascript:ReportWindow('/cgi/bin/mis.cgi?view=ClientMUTI.cgi&Client_ClientID=<<<Client_ClientID>>>&mlt=<<<mlt>>>&misLINKS=<<<misLINKS>>>','NewCrop',900,1500);" TITLE="Manually Add NewCrop Medications for testing only">Add NewCrop Medications</A>
    </TD>
  </TR>
  <TR >
    <TD COLSPAN="2" >
<SPAN ID="ShowClientMeds" >
[[myHTML->ListSel(%form+ShowClientMeds+<<<Client_ClientID>>>+<<<LINKID>>>+<<<Client_Locked_1>>>)]]
</SPAN>
    </TD>
  </TR>
  <TR >
    <TD CLASS="port hdrtxt" >
      Administered Medications are those with PrescriptionDate = ContactDate
    </TD>
    <TD WIDTH="50%" >&nbsp;</TD>
  </TR>
  <TR ><TD CLASS="port hdrtxt" COLSPAN="2" >TEST INFORMATION</TD></TR>
  <TR ><TD CLASS="port hdrtxt" WIDTH="50%" >Lab Results Information</TD><TD WIDTH="50%" >&nbsp;</TD></TR>
  <TR >
    <TD COLSPAN="2" >
<SPAN ID="ListClientLabs" >
[[myHTML->ListSel(%form+ListClientLabs+<<<Client_ClientID>>>+<<<LINKID>>>+<<<Client_Locked_1>>>)]]
</SPAN>
    </TD>
  </TR>
</TABLE>
<TABLE CLASS="main fullsize" >
  <TR >
    <TD CLASS="numcol" >
      <INPUT TYPE="submit" ONCLICK="return validate(this.form);" NAME="UpdateTables=all&[[myForm->genLink(ClientIntake+ClientMUO.cgi)]]" VALUE="Add/Update -> Client Observable Information" >
      <INPUT TYPE="submit" ONCLICK="return validate(this.form);" NAME="UpdateTables=all&misPOP=1" VALUE="Add/Update" >
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
