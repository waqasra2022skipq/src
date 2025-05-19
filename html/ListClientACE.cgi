[[myHTML->newPage(%form+Client ACE)]]

<SCRIPT LANGUAGE="JavaScript" SRC="/src/cgi/js/novalidate.js"> </SCRIPT>

<FORM NAME="ACE" ACTION="/src/cgi/bin/mis.cgi" METHOD="POST" >
<TABLE CLASS="main fullsize" >
  <TR >
    <TD CLASS="strcol" >
      <<<Client_FName_1>>> <<<Client_MName_1>>> <<<Client_LName_1>>> (<<<Client_ClientID_1>>>) <<<Client_SSN_1>>>
    </TD>
    <TD CLASS="numcol" >[[gHTML->setLINKS(%form+back)]]</TD>
  </TR>
  <TR CLASS="port" >
    <TD CLASS="strcol" >
<A HREF="http://forms.okmis.com/Testing/20190222131900_ACE-Resiliency.pdf" TARGET="popup" ONCLICK="window.open('http://forms.okmis.com/Testing/20190222131900_ACE-Resiliency.pdf', 'popup', 'width=1200,height=1200,menubar=1,scrollbars=1,toolbar=1,status=1,resizable=1'); return false">Adverse Childhood Experience ACE What's Your Score?</A>
    </TD>
    <TD CLASS="numcol" >
<A HREF="http://forms.okmis.com/printing/PrintClientACE_Rev2.pdf" TARGET="popup" ONCLICK="window.open('http://forms.okmis.com/printing/PrintClientACE_Rev2.pdf', 'popup', 'width=1200,height=1200,menubar=1,scrollbars=1,toolbar=1,status=1,resizable=1'); return false">Blank Adverse Childhood Experience Form</A>
    </TD>
  </TR>
</TABLE>
<SPAN ID="ListClientACE" >
[[myHTML->ListSel(%form+ListClientACE+<<<Client_ClientID>>>+<<<LINKID>>>+<<<Client_Locked_1>>>)]]
</SPAN>
</LOADHIDDEN>
</FORM>
[[myHTML->rightpane(%form+search)]]
