[[myHTML->newPage(%form+Client Electronic Documents)]]

<SCRIPT LANGUAGE="JavaScript" SRC="/src/cgi/js/novalidate.js"> </SCRIPT>
<SCRIPT LANGUAGE="JavaScript" src="/src/cgi/js/deleteFile.js"> </SCRIPT>
<FORM NAME="ListClientEDocs" ACTION="/src/cgi/bin/mis.cgi" METHOD="POST" >
<TABLE CLASS="main fullsize" >
  <TR >
    <TD CLASS="strcol" >
      <<<Client_FName_1>>> <<<Client_MName_1>>> <<<Client_LName_1>>> (<<<Client_ClientID_1>>>) <<<Client_SSN_1>>>
      <BR>Electronic Documents Page
    </TD>
    <TD CLASS="numcol" >[[gHTML->setLINKS(%form+back)]]</TD>
  </TR>
</TABLE>
<SPAN ID="ListClientEDocs" >
[[myHTML->ListSel(%form+ListClientEDocs+<<<Client_ClientID>>>+<<<LINKID>>>+<<<Client_Locked_1>>>)]]
</SPAN>


[[SysAccess->verify(%form+Privilege=Rollup) <INPUT TYPE="submit" TITLE="This will roll up client's Prior Auth, Intake Admisssion, Treatment Plan, Electronic Documents, CARS Reviews, Questionnaires, Lab Results, Presecreptions, Risk Assesments, Problems, Discharges, American Society of Addiction Medicine, Teen Addiction Severity Index " ID="Rollup_Button" NAME="UpdateTables=all&MIS_Action=ClientRollup.cgi&Client_ClientID=<<<Client_ClientID>>>" VALUE="Rollup this Client Reports">]]

</LOADHIDDEN>
</FORM>

[[myHTML->list_zip_files_in_table(%form+Client+<<Client_ClientID>>)]]
[[myHTML->rightpane(%form+search)]]
<script src="https://cdn.jsdelivr.net/npm/sweetalert2@11"></script>

