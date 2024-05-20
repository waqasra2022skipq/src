[[myHTML->newPage(%form+Client SBIRT)]]

<SCRIPT LANGUAGE="JavaScript" SRC="/cgi/js/novalidate.js"> </SCRIPT>

<FORM NAME="SBIRT" ACTION="/cgi/bin/mis.cgi" METHOD="POST" >
<TABLE CLASS="main fullsize" >
  <TR >
    <TD CLASS="strcol" >
      <<<Client_FName_1>>> <<<Client_MName_1>>> <<<Client_LName_1>>> (<<<Client_ClientID_1>>>) <<<Client_SSN_1>>>
    </TD>
    <TD CLASS="numcol" >[[gHTML->setLINKS(%form+back)]]</TD>
  </TR>
</TABLE>
<TABLE CLASS="port fullsize" >
  <TR><TD CLASS="port numcol" ><A HREF="javascript:ReportWindow('http://www.sbirttraining.com/oklahoma-program')" >Training website</A></TD></TR>
</TABLE>
<SPAN ID="ListClientSBIRT" >
[[myHTML->ListSel(%form+ListClientSBIRT+<<<Client_ClientID>>>+<<<LINKID>>>+<<<Client_Locked_1>>>)]]
</SPAN>
</LOADHIDDEN>
</FORM>
[[myHTML->rightpane(%form+search)]]
