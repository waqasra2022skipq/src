[[myHTML->newHTML(%form+Client ASAM+clock mail managertree collapseipad mismenu)]]

<SCRIPT LANGUAGE="JavaScript" SRC="/src/cgi/js/novalidate.js"> </SCRIPT>

<FORM NAME="ASAM" ACTION="/src/cgi/bin/mis.cgi" METHOD="POST" >
<TABLE CLASS="main fullsize" >
  <TR >
    <TD CLASS="strcol" >
      <<<Client_FName_1>>> <<<Client_MName_1>>> <<<Client_LName_1>>> (<<<Client_ClientID_1>>>) <<<Client_SSN_1>>>
      <BR>ASAM Page
    </TD>
    <TD CLASS="numcol" >[[gHTML->setLINKS(%form+back)]]</TD>
  </TR>
</TABLE>
<SPAN ID="ListClientASAM" >
[[myHTML->ListSel(%form+ListClientASAM+<<<Client_ClientID>>>+<<<LINKID>>>+<<<Client_Locked_1>>>)]]
</SPAN>
[[[gHTML->setASAMButtons(%form)]]]

</LOADHIDDEN>
</FORM>
[[myHTML->rightpane(%form+search)]]
