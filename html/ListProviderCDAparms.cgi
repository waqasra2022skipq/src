[[myHTML->newPage(%form+Import CDA Parameters)]]
[[[DBForm->pushLINK()]]]
[[DBA->setProviderCDAparms(%form+<<<Provider_ProvID>>>)]]

<SCRIPT type="text/javascript" SRC="/src/cgi/js/ajaxrequest.js"> </SCRIPT>
<SCRIPT LANGUAGE="JavaScript" SRC="/src/cgi/js/novalidate.js"> </SCRIPT>
<FORM NAME="ListProviderCDAparms" ACTION="/cgi/bin/mis.cgi" METHOD="POST" >

<TABLE CLASS="main fullsize" >
  <TR >
    <TD CLASS="strcol" >
      <<<Provider_FName_1>>> <<<Provider_MName_1>>> <<<Provider_LName_1>>>
      <BR>Import CDA Parameters
    </TD>
    <TD CLASS="numcol" >[[gHTML->setLINKS(%form+back)]]</TD>
  </TR>
</TABLE>
<SPAN ID="ListProviderCDAparms" >
[[myHTML->ListSel(%form+ListProviderCDAparms+<<<Provider_ProvID>>>+<<<LINKID>>>+<<<Provider_Locked_1>>>)]]
</SPAN>

</LOADHIDDEN>
</FORM>
[[myHTML->rightpane(%form+search)]]
