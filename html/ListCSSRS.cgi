[[myHTML->newPage(%form+Client CSSRS)]]

<SCRIPT LANGUAGE="JavaScript" SRC="/cgi/js/novalidate.js"> </SCRIPT>

<FORM NAME="CSSRS" ACTION="/cgi/bin/mis.cgi" METHOD="POST" >
<TABLE CLASS="main fullsize" >
  <TR >
    <TD CLASS="strcol" >
      <<<Client_FName_1>>> <<<Client_MName_1>>> <<<Client_LName_1>>> (<<<Client_ClientID_1>>>) <<<Client_SSN_1>>>
      <BR>C-SSRS (Columbia Suicide Severity Risk and Protective Factors) Page
    </TD>
    <TD CLASS="numcol" >[[gHTML->setLINKS(%form+back)]]</TD>
  </TR>
</TABLE>
<P>
<SPAN ID="ListClientCSSRS" >
[[myHTML->ListSel(%form+ListClientCSSRS+<<<Client_ClientID>>>+<<<LINKID>>>+<<<Client_Locked_1>>>)]]
</SPAN>
<P>
<SPAN ID="ListClientCSSRSs" >
[[myHTML->ListSel(%form+ListClientCSSRSs+<<<Client_ClientID>>>+<<<LINKID>>>+<<<Client_Locked_1>>>)]]
</SPAN>
<P>
<SPAN ID="ListClientCSSRSt" >
[[myHTML->ListSel(%form+ListClientCSSRSt+<<<Client_ClientID>>>+<<<LINKID>>>+<<<Client_Locked_1>>>)]]
</SPAN>
<P>
<TABLE CLASS="main fullsize" >
  <TR >
    <TD CLASS="port strcol" >
      
<BR><BR>

<BR><BR>

    </TD>
  </TR>
</TABLE>

</LOADHIDDEN>
</FORM>
[[myHTML->rightpane(%form+search)]]
