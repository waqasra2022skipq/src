[[myHTML->newPage(%form+Client Journals)]]
[[[DBForm->pushLINK()]]]

<SCRIPT LANGUAGE="JavaScript" SRC="/cgi/js/novalidate.js"> </SCRIPT>
<FORM NAME="ListClientJournals" ACTION="/cgi/bin/mis.cgi" METHOD="POST" >

<TABLE CLASS="main fullsize" >
  <TR >
    <TD CLASS="strcol" >
      <<<Client_FName_1>>> <<<Client_MName_1>>> <<<Client_LName_1>>>
      <BR>Client Journal Entries
    </TD>
    <TD CLASS="numcol" >[[gHTML->setLINKS(%form+back)]]</TD>
  </TR>
</TABLE>
<SPAN ID="ListClientJournals" >
[[myHTML->ListSel(%form+ListClientJournals+<<<Client_ClientID>>>+<<<LINKID>>>+<<<Client_Locked_1>>>)]]
</SPAN>

</LOADHIDDEN>
</FORM>
[[myHTML->rightpane(%form+search)]]
