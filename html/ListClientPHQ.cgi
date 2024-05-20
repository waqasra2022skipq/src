[[myHTML->newPage(%form+Client PHQ)]]

<SCRIPT LANGUAGE="JavaScript" SRC="/cgi/js/novalidate.js"> </SCRIPT>

<FORM NAME="PHQ" ACTION="/cgi/bin/mis.cgi" METHOD="POST" >
<TABLE CLASS="main fullsize" >
  <TR >
    <TD CLASS="strcol" >
      <<<Client_FName_1>>> <<<Client_MName_1>>> <<<Client_LName_1>>> (<<<Client_ClientID_1>>>) <<<Client_SSN_1>>>
      <BR>Patient Health Questionare (PHQ) Page
    </TD>
    <TD CLASS="numcol" >[[gHTML->setLINKS(%form+back)]]</TD>
  </TR>
</TABLE>
<P>
<SPAN ID="ListClientPHQ" >
[[myHTML->ListSel(%form+ListClientPHQ+<<<Client_ClientID>>>+<<<LINKID>>>+<<<Client_Locked_1>>>)]]
</SPAN>
<P>
<SPAN ID="ListClientPHQBrief" >
[[myHTML->ListSel(%form+ListClientPHQBrief+<<<Client_ClientID>>>+<<<LINKID>>>+<<<Client_Locked_1>>>)]]
</SPAN>
<P>
<SPAN ID="ListClientPHQ2" >
[[myHTML->ListSel(%form+ListClientPHQ2+<<<Client_ClientID>>>+<<<LINKID>>>+<<<Client_Locked_1>>>)]]
</SPAN>
<P>
<SPAN ID="ListClientPHQ4" >
[[myHTML->ListSel(%form+ListClientPHQ4+<<<Client_ClientID>>>+<<<LINKID>>>+<<<Client_Locked_1>>>)]]
</SPAN>
<P>
<SPAN ID="ListClientPHQ9" >
[[myHTML->ListSel(%form+ListClientPHQ9+<<<Client_ClientID>>>+<<<LINKID>>>+<<<Client_Locked_1>>>)]]
</SPAN>
<P>
<SPAN ID="ListClientTPHQ9" >
[[myHTML->ListSel(%form+ListClientTPHQ9+<<<Client_ClientID>>>+<<<LINKID>>>+<<<Client_Locked_1>>>)]]
</SPAN>
<P>
<SPAN ID="ListClientPHQ15" >
[[myHTML->ListSel(%form+ListClientPHQ15+<<<Client_ClientID>>>+<<<LINKID>>>+<<<Client_Locked_1>>>)]]
</SPAN>
<P>
<TABLE CLASS="main fullsize" >
  <TR >
    <TD CLASS="port strcol" >
     Over time, the severity scores have been a particularly popular use of the measures, and are now used much more commonly than the provisional diagnoses.
<BR><BR>
For example, cutpoints of 5, 10, and 15 represent mild, moderate, and severe levels of depressive, anxiety, and somatic symptoms, on the PHQ-9, GAD-7, and PHQ-15 respectively. Also, a cutpoint of 10 or greater is considered a yellow flag on all 3 measures (i.e., drawing attention to a possible clinically significant condition), while a cutpoint of 15 is a red flag on all 3 measures (i.e., targeting individuals in whom active treatment is probably warranted). 
<BR><BR>
For the ultra-brief measures (PHQ-2 and GAD-2), a score of 3 or greater should prompt administration of the full PHQ-9 and/or GAD-7, as well as a clinical interview to determine whether a mental disorder is present.  
    </TD>
  </TR>
</TABLE>

</LOADHIDDEN>
</FORM>
[[myHTML->rightpane(%form+search)]]
