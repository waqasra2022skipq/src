[[myHTML->newPage(%form+MIS database Tables)]]
[[[DBForm->pushLINK()]]]

[[*SysAccess->verify(%form+Privilege=AdminTables)]]

<SCRIPT LANGUAGE="JavaScript" SRC="/cgi/js/novalidate.js"> </SCRIPT>
<FORM NAME="ListxTables" ACTION="/cgi/bin/mis.cgi" METHOD="POST" >
<TABLE CLASS="main fullsize" >
  <TR >
    <TD CLASS="strcol" >
      MIS Table Definitions
    </TD>
    <TD CLASS="numcol" >[[gHTML->setLINKS(%form+back)]]</TD>
  </TR>
</TABLE>
<SPAN ID="ListxTables" >
[[myHTML->ListSel(%form+ListxTables++<<<LINKID>>>)]]
</SPAN>

</LOADHIDDEN>
</FORM>
[[myHTML->rightpane(%form+search)]]
