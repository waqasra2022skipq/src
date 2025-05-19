[[myHTML->newPage(%form+Client Family Problems)]]

<SCRIPT LANGUAGE="JavaScript" SRC="/src/cgi/js/novalidate.js"> </SCRIPT>
<SCRIPT LANGUAGE="JavaScript" SRC="/src/cgi/js/ajaxrequest.js"> </SCRIPT>

<FORM NAME="FamilyProblems" ACTION="/src/cgi/bin/mis.cgi" METHOD="POST" >
<TABLE CLASS="main fullsize" >
  <TR >
    <TD CLASS="strcol" >
      <<<Client_FName_1>>> <<<Client_MName_1>>> <<<Client_LName_1>>> (<<<Client_ClientID_1>>>) <<<Client_SSN_1>>>
      <BR>
      Family Problems Page
    </TD>
    <TD CLASS="numcol" >[[gHTML->setLINKS(%form+back)]]</TD>
  </TR>
</TABLE>
<SPAN ID="ListClientFamilyProblems" >
[[myHTML->ListSel(%form+ListClientFamilyProblems+<<<Client_ClientID>>>+<<<LINKID>>>+<<<Client_Locked_1>>>)]]
</SPAN>
</LOADHIDDEN>
</FORM>
[[myHTML->rightpane(%form+search)]]
