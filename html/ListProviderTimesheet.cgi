[[myHTML->newHTML(%form+Timesheet+allleft mismenu checkpopupwindow)]]

<SCRIPT LANGUAGE="JavaScript" SRC="/src/cgi/js/novalidate.js"> </SCRIPT>
<FORM NAME="Provider" ACTION="/src/cgi/bin/mis.cgi" METHOD="POST" >
<TABLE CLASS="main fullsize" >
  <TR >
    <TD CLASS="strcol" >
      <<<Provider_FName_1>>> <<<Provider_MName_1>>> <<<Provider_LName_1>>> 
      <BR>Provider Time Sheet Information
    </TD>
    <TD CLASS="numcol" >[[gHTML->setLINKS(%form+back)]]</TD>
  </TR>
</TABLE>
<SPAN ID="ListProviderTimesheet" >
[[myHTML->ListSel(%form+ListProviderTimesheet+<<<Provider_ProvID>>>+<<<LINKID>>>+<<<Provider_Locked_1>>>)]]
</SPAN>

</LOADHIDDEN>
</FORM>
[[myHTML->rightpane(%form+search)]]
