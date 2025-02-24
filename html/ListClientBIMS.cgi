[[myHTML->newHTML(%form+Client VItal Signs+clock mail managertree collapseipad mismenu)]]

<SCRIPT LANGUAGE="JavaScript" SRC="/cgi/js/novalidate.js"> </SCRIPT>

<FORM NAME="BIMS" ACTION="/cgi/bin/mis.cgi" METHOD="POST" >
<TABLE CLASS="main fullsize" >
  <TR >
    <TD CLASS="strcol" >
      <<<Client_FName_1>>> <<<Client_MName_1>>> <<<Client_LName_1>>> (<<<Client_ClientID_1>>>) <<<Client_SSN_1>>>
    </TD>
    <TD CLASS="numcol" >[[gHTML->setLINKS(%form+back)]]</TD>
  </TR>
</TABLE>
<SPAN ID="ListClientBIMS" >
[[myHTML->ListSel(%form+ListClientBIMS+<<<Client_ClientID>>>+<<<LINKID>>>+<<<Client_Locked_1>>>)]]
</SPAN>
</LOADHIDDEN>
</FORM>
[[myHTML->rightpane(%form+search)]]


