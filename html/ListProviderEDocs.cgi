[[myHTML->newPage(%form+Provider Electronic Documents)]]
[[[DBForm->pushLINK()]]]

<SCRIPT LANGUAGE="JavaScript" src="/cgi/js/deleteFile.js"> </SCRIPT>
<SCRIPT LANGUAGE="JavaScript" SRC="/cgi/js/novalidate.js"> </SCRIPT>
<FORM NAME="ListProviderEDocs" ACTION="/cgi/bin/mis.cgi" METHOD="POST" >
<TABLE CLASS="main fullsize" >
  <TR >
    <TD CLASS="strcol" >
      <<<Provider_FName_1>>> <<<Provider_MName_1>>> <<<Provider_LName_1>>>
      <BR>Electronic Documents Page
    </TD>
    <TD CLASS="numcol" >[[gHTML->setLINKS(%form+back)]]</TD>
  </TR>
</TABLE>
<SPAN ID="ListProviderEDocs" >
[[myHTML->ListSel(%form+ListProviderEDocs+<<<Provider_ProvID>>>+<<<LINKID>>>+<<<Provider_Locked_1>>>++and ProviderEDocs.Type!=40)]]

</SPAN>

[[SysAccess->verify(%form+Privilege=Rollup) <INPUT TYPE="submit" TITLE="<<rollUpMessage>>" ID="Rollup_Button" NAME="UpdateTables=all&MIS_Action=ProviderRollup.cgi&Provider_ProvID=<<<Provider_ProvID>>>" VALUE="Rollup this <<provType>> Reports">]]


</LOADHIDDEN>
</FORM>

[[myHTML->list_zip_files_in_table(%form+Provider+<<Provider_ProvID>>)]]

[[myHTML->rightpane(%form+search)]]
<script src="https://cdn.jsdelivr.net/npm/sweetalert2@11"></script>
