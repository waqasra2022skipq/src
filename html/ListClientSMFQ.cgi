[[myHTML->newHTML(%form+Client Short Mood and Feeling Questionnaire+clock mail managertree collapseipad mismenu)]]

<SCRIPT LANGUAGE="JavaScript" SRC="/cgi/js/novalidate.js"> </SCRIPT>

<FORM NAME="SMFQ" ACTION="/cgi/bin/mis.cgi" METHOD="POST" >
<TABLE CLASS="main fullsize" >
  <TR >
    <TD CLASS="strcol" >
      <<<Client_FName_1>>> <<<Client_MName_1>>> <<<Client_LName_1>>> (<<<Client_ClientID_1>>>) <<<Client_SSN_1>>>
    </TD>
    <TD CLASS="numcol" >[[gHTML->setLINKS(%form+back)]]</TD>
  </TR>
  <TR CLASS="port" >
    <TD CLASS="numcol" COLSPAN="2" >
<A HREF="http://forms.okmis.com/90/Testing:20190215111947_AngoldMFQarticle.pdf" TARGET="popup" ONCLICK="window.open('http://forms.okmis.com/90/Testing:20190215111947_AngoldMFQarticle.pdf', 'popup', 'width=1200,height=1200,menubar=1,scrollbars=1,toolbar=1,status=1,resizable=1'); return false">MOOD AND FEELINGS DIRECTIONS</A>
<BR>
<A HREF="http://forms.okmis.com/90/Testing:20190215111737_MFQChildSelfReportShort.pdf" TARGET="popup" ONCLICK="window.open('http://forms.okmis.com/90/Testing:20190215111737_MFQChildSelfReportShort.pdf', 'popup', 'width=1200,height=1200,menubar=1,scrollbars=1,toolbar=1,status=1,resizable=1'); return false">MOOD AND FEELINGS CHILD SELF-REPORT Short</A>
<BR>
<A HREF="http://forms.okmis.com/90/Testing:20190215111659_MFQParentReportChildShort.pdf" TARGET="popup" ONCLICK="window.open('http://forms.okmis.com/90/Testing:20190215111659_MFQParentReportChildShort.pdf', 'popup', 'width=1200,height=1200,menubar=1,scrollbars=1,toolbar=1,status=1,resizable=1'); return false">MOOD AND FEELINGS PARENT REPORT ON CHILD Short</A>
    </TD>
  </TR>
</TABLE>
<SPAN ID="ListClientSMFQ" >
[[myHTML->ListSel(%form+ListClientSMFQ+<<<Client_ClientID>>>+<<<LINKID>>>+<<<Client_Locked_1>>>)]]
</SPAN>
<TABLE CLASS="port fullsize" >
  <TR >
    <TD CLASS="strcol" >
Depression column child/parent.
<BR>
If only Child section is completed, then if the total is 'greater than or equal to 8' then - red positive (indicate 60% selectivity and 85% specificity).
<BR>
If Parent section is also completed, then if the combined total is 'greater than or equal to 12' then - red positive (indicate 70% selectivity and 85% specificity).
    </TD>
  </TR>
</TABLE>
</LOADHIDDEN>
</FORM>
[[myHTML->rightpane(%form+search)]]
