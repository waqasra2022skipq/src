[[myHTML->newPage(%form+Client Medications)]]

<SCRIPT type="text/javascript" SRC="/cgi/js/ajaxrequest.js"> </SCRIPT>
<SCRIPT LANGUAGE="JavaScript" SRC="/cgi/js/novalidate.js"> </SCRIPT>

<FORM NAME="Meds" ACTION="/cgi/bin/mis.cgi" METHOD="POST" >
<TABLE CLASS="main fullsize" >
  <TR >
    <TD CLASS="strcol" >
      <<<Client_FName_1>>> <<<Client_MName_1>>> <<<Client_LName_1>>> (<<<Client_ClientID_1>>>) <<<Client_SSN_1>>>
      <BR>
      Medications Page
    </TD>
    <TD CLASS="numcol" >[[gHTML->setLINKS(%form+back)]]</TD>
  </TR>
</TABLE>
<TABLE CLASS="home fullsize" >
  <TR >
    <TD CLASS="port hdrtxt" >
      CURRENT MEDICATIONS
      [[DBA->getClientMedCount(%form+<<<Client_ClientID_1>>>+PDMed)]]
    </TD>
  </TR>
  <TR >
    <TD CLASS="port hdrcol" >
      Client Reported Medications
      <A HREF="javascript:callAjax('ListClientPDMeds','','ListClientPDMeds','&active=1&Locked=0&Client_ClientID=<<<Client_ClientID>>>&LOGINPROVID=<<<LOGINPROVID>>>&LOGINUSERID=<<<LOGINUSERID>>>&LINKID=<<<LINKID>>>&mlt=<<<mlt>>>&LOGINUSERDB=<<<LOGINUSERDB>>>','popup.pl');" TITLE="Show ONLY Active Medications for Client">Active Only</A>
      /
      <A HREF="javascript:callAjax('ListClientPDMeds','','ListClientPDMeds','&active=0&Locked=0&Client_ClientID=<<<Client_ClientID>>>&LOGINPROVID=<<<LOGINPROVID>>>&LOGINUSERID=<<<LOGINUSERID>>>&LINKID=<<<LINKID>>>&mlt=<<<mlt>>>&LOGINUSERDB=<<<LOGINUSERDB>>>','popup.pl');" TITLE="Show ALL Medications for Client">Show All</A>
    </TD>
  </TR>
  <TR >
    <TD COLSPAN="2" >
<SPAN ID="ListClientPDMeds" >
[[myHTML->ListSel(%form+ListClientPDMeds+<<<Client_ClientID>>>+<<<LINKID>>>+<<<Client_Locked_1>>>)]]
</SPAN>
    </TD>
  </TR>
</TABLE>
<P>
<TABLE CLASS="home fullsize" >
  <TR >
    <TD CLASS="port hdrtxt" >
      ONLINE MEDICATIONS
      [[DBA->getClientMedCount(%form+<<<Client_ClientID_1>>>+ClientMeds)]]
    </TD> 
  </TR>
  <TR >
    <TD CLASS="port hdrcol" >
      Client Medications
      <A HREF="javascript:callAjax('ShowClientMeds','','ShowClientMeds','&active=1&Locked=0&Client_ClientID=<<<Client_ClientID>>>&LOGINPROVID=<<<LOGINPROVID>>>&LOGINUSERID=<<<LOGINUSERID>>>&LINKID=<<<LINKID>>>&mlt=<<<mlt>>>&LOGINUSERDB=<<<LOGINUSERDB>>>','popup.pl');" TITLE="Show ONLY Active Medications for Client">Active Only</A>
      /
      <A HREF="javascript:callAjax('ShowClientMeds','','ShowClientMeds','&active=0&Locked=0&Client_ClientID=<<<Client_ClientID>>>&LOGINPROVID=<<<LOGINPROVID>>>&LOGINUSERID=<<<LOGINUSERID>>>&LINKID=<<<LINKID>>>&mlt=<<<mlt>>>&LOGINUSERDB=<<<LOGINUSERDB>>>','popup.pl');" TITLE="Show ALL Medications for Client">Show All</A>
    </TD>
  </TR>
  <TR >
    <TD >
<SPAN ID="ShowClientMeds" >
[[myHTML->ListSel(%form+ShowClientMeds+<<<Client_ClientID>>>+<<<LINKID>>>+<<<Client_Locked_1>>>++and ClientMeds.Active=1)]]
</SPAN>
    </TD>
  </TR>
</TABLE>
<TABLE CLASS="main fullsize" >
  <TR >
    <TD CLASS="numcol" >
      <INPUT TYPE="submit" ONCLICK="return validate(this.form);" NAME="UpdateTables=all&[[myForm->genLink(ClientIntake+ClientDevl.cgi)]]" VALUE="Add/Update -> Development">
      <INPUT TYPE="submit" ONCLICK="return validate(this.form);" NAME="UpdateTables=all&misPOP=1" VALUE="Add/Update">
    </TD>
  </TR>
</TABLE>

</LOADHIDDEN>
</FORM>
[[myHTML->rightpane(%form+search)]]
