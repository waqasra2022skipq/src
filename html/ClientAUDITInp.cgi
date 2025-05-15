[[myHTML->newPage(%form+Client AUDIT)]]

<SCRIPT LANGUAGE="JavaScript" SRC="/src/cgi/js/vEntry.js"> </SCRIPT>
<SCRIPT LANGUAGE="JavaScript" SRC="/src/cgi/js/vClientAUDIT.js?v=202008260004"> </SCRIPT>
<SCRIPT LANGUAGE="JavaScript" SRC="/src/cgi/js/vDate.js"> </SCRIPT>
<SCRIPT LANGUAGE="JavaScript" SRC="/src/cgi/js/vNum.js"> </SCRIPT>

<FORM NAME="ClientAUDIT" ACTION="/cgi/bin/mis.cgi" METHOD="POST" >
<TABLE CLASS="main fullsize" >
  <TR >
    <TD CLASS="strcol" >
      <<<Client_FName_1>>> <<<Client_MName_1>>> <<<Client_LName_1>>> (<<<Client_ClientID_1>>>) <<<Client_SSN_1>>>
      <BR>
      Substance Abuse View/Edit Page
    </TD>
    <TD CLASS="numcol" >[[gHTML->setLINKS(%form+back)]]</TD>
  </TR>
</TABLE>
<TABLE CLASS="home fullsize" >
  <TR><TD CLASS="port hdrtxt" >AUDIT (Alcohol Use Disorders Identification Test)</TD></TR>
  <TR><TD CLASS="home strcol heading" >The Alcohol Use Disorders Identification Test: Interview Version</TD></TR>
  <TR><TD CLASS="home strcol" >Read questions as written. Record answers carefully. Begin the AUDIT by saying "Now I am going to ask you some questions about your use of alcoholic beverages during this past year." Explain what is meant by "alcoholic beverages" by using local examples of beer, wine, vodka, etc. Code answers in terms of "standard drinks" Check the correct answer to the right.</TD></TR>
  <TR >
    <TD CLASS="port hdrtxt" >
[[[myHTML->setHTML(%form+ClientAUDIT)]]]
    </TD>
  </TR>
  <TR><TD CLASS="home strcol" >Scoring: Add up the points associated with your answers above. Scores between 8 and 15 are most appropriate for simple advice focused on the reduction of hazardous drinking. Scores between 16 and 19 suggest brief counseling and continued monitoring. AUDIT scores of 20 or above clearly warrant further diagnostic evaluation for alcohol dependence.</TD></TR>
  <TR><TD CLASS="home strcol" >A score >= 8 is 81.4% sensitive and 94.6% specificity for detecting hazardous drinking. AUDIT: Positive or Negative</TD></TR>
  <TR><TD CLASS="home strcol heading" >If Positive, complete ASI, T-ASI, ASAM as required by regulations.</TD></TR>
</TABLE>
<TABLE CLASS="main fullsize" >
  <TR >
    <TD CLASS="numcol" >
      <INPUT TYPE="submit" ONCLICK="return vDELETE('Are you sure you want to delete this record?');" NAME="ClientAUDIT_DELETE_1=1&UpdateTables=all&misPOP=1" VALUE="Delete">
      <INPUT TYPE="submit" ONCLICK="return validate(this.form);" NAME="UpdateTables=all&misPOP=1" VALUE="Add/Update">
    </TD>
  </TR>
</TABLE>

</LOADHIDDEN>
</FORM>
<SCRIPT LANGUAGE="JavaScript">
  document.ClientAUDIT.elements[0].focus();
  $(document).ready(function() {
    $('form[name="ClientAUDIT"] input[name^="ClientAUDIT_q"]').change(function() {
      validateInputs(document.ClientAUDIT);
    });
  });
// just to OPENTABLES...
//<<<ClientAUDIT_ClientID_1>>>
</SCRIPT>

[[myHTML->rightpane(%form+search)]]
