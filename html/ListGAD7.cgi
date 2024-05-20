[[myHTML->newPage(%form+Client GAD7)]]

<SCRIPT LANGUAGE="JavaScript" SRC="/cgi/js/novalidate.js"> </SCRIPT>

<FORM NAME="GAD7" ACTION="/cgi/bin/mis.cgi" METHOD="POST" >
<TABLE CLASS="main fullsize" >
  <TR >
    <TD CLASS="strcol" >
      <<<Client_FName_1>>> <<<Client_MName_1>>> <<<Client_LName_1>>> (<<<Client_ClientID_1>>>) <<<Client_SSN_1>>>
    </TD>
    <TD CLASS="numcol" >[[gHTML->setLINKS(%form+back)]]</TD>
  </TR>
</TABLE>
<SPAN ID="ListClientGAD7" >
[[myHTML->ListSel(%form+ListClientGAD7+<<<Client_ClientID>>>+<<<LINKID>>>+<<<Client_Locked_1>>>)]]
</SPAN>
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
