[[myHTML->newPage(%form+Needs and Skills)]]
[[[DBForm->pushLINK()]]]

[[*SysAccess->verify(%form+Privilege=AdminTables)]]

<SCRIPT LANGUAGE="JavaScript" SRC="/src/cgi/js/novalidate.js"> </SCRIPT>
<FORM NAME="ListNS" ACTION="/cgi/bin/mis.cgi" METHOD="POST" >
<TABLE CLASS="main fullsize" >
  <TR >
    <TD CLASS="strcol" >
      Need/Skill<BR>Codes
    </TD>
    <TD CLASS="numcol" >[[gHTML->setLINKS(%form+back)]]</TD>
  </TR>
</TABLE>
<SPAN ID="ListxNS" >
[[myHTML->ListSel(%form+ListxNS++<<<LINKID>>>)]]
</SPAN>

</LOADHIDDEN>
</FORM>
[[myHTML->rightpane(%form+search)]]
