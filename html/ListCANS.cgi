[[myHTML->newPage(%form+Client CANS)]]

<SCRIPT LANGUAGE="JavaScript" SRC="/src/cgi/js/novalidate.js"> </SCRIPT>

<FORM NAME="CANS" ACTION="/src/cgi/bin/mis.cgi" METHOD="POST" >
<TABLE CLASS="main fullsize" >
  <TR >
    <TD CLASS="strcol" >
      <<<Client_FName_1>>> <<<Client_MName_1>>> <<<Client_LName_1>>> (<<<Client_ClientID_1>>>) <<<Client_SSN_1>>>
      <BR>CHILD AND ADOLESCENT NEEDS AND STRENGTHS (CANS-MH) Page
    </TD>
    <TD CLASS="numcol" >[[gHTML->setLINKS(%form+back)]]</TD>
  </TR>
</TABLE>
<P>
<SPAN ID="ListClientCANS" >
[[myHTML->ListSel(%form+ListClientCANS+<<<Client_ClientID>>>+<<<LINKID>>>+<<<Client_Locked_1>>>)]]
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
