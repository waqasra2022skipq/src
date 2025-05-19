[[myHTML->newPage(%form+TASI Listing)]]

<SCRIPT LANGUAGE="JavaScript" SRC="/src/cgi/js/novalidate.js"> </SCRIPT>

<FORM NAME="ClientTASI" ACTION="/src/cgi/bin/mis.cgi" METHOD="POST" >
<TABLE CLASS="main fullsize" >
  <TR >
    <TD CLASS="strcol" >
      <<<Client_FName_1>>> <<<Client_MName_1>>> <<<Client_LName_1>>> (<<<Client_ClientID_1>>>) <<<Client_SSN_1>>>
      <BR>
      Teen Addiction Severity Index (T-ASI) Page
    </TD>
    <TD CLASS="numcol" >[[gHTML->setLINKS(%form+back)]]</TD>
  </TR>
</TABLE>
<TABLE CLASS="port fullsize" >
  <TR ><TD CLASS="port hdrtxt" ><B>Before Adding a NEW TASI please complete the current TASI.</B></TD></TR>
  <TR ><TD >
<SPAN ID="ListClientTASI" >
[[myHTML->ListSel(%form+ListClientTASI+<<<Client_ClientID>>>+<<<LINKID>>>+<<<Client_Locked_1>>>)]]
</SPAN>
  </TD></TR >
</TABLE>

</LOADHIDDEN>
</FORM>
[[myHTML->rightpane(%form+search)]]
