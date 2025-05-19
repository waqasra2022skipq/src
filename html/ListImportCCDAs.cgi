[[myHTML->newPage(%form+Import CCDA Documtemts)]]
[[[DBForm->pushLINK()]]]

<SCRIPT LANGUAGE="JavaScript" SRC="/src/cgi/js/novalidate.js"> </SCRIPT>
<FORM NAME="ListImportCCDAs" ACTION="/src/cgi/bin/mis.cgi" METHOD="POST" >

<TABLE CLASS="main fullsize" >
  <TR >
    <TD CLASS="strcol" >
      <<<Client_FName_1>>> <<<Client_MName_1>>> <<<Client_LName_1>>>
      <BR>Import CCDA Documents
    </TD>
    <TD CLASS="numcol" >[[gHTML->setLINKS(%form+back)]]</TD>
  </TR>
</TABLE>
<SPAN ID="ListImportCCDAs" >
[[myHTML->ListSel(%form+ListImportCCDAs+<<<Client_ClientID>>>+<<<LINKID>>>+<<<Client_Locked_1>>>)]]
</SPAN>

</LOADHIDDEN>
</FORM>
[[myHTML->rightpane(%form+search)]]
