[[myHTML->newPage(%form+Client PHQ)]]

<SCRIPT LANGUAGE="JavaScript" SRC="/cgi/js/NoEnter.js"> </SCRIPT>
<SCRIPT LANGUAGE="JavaScript" SRC="/cgi/js/vEntry.js"> </SCRIPT>
<SCRIPT LANGUAGE="JavaScript" SRC="/cgi/js/vClientPHQ.js"> </SCRIPT>
<SCRIPT LANGUAGE="JavaScript" SRC="/cgi/js/vDate.js"> </SCRIPT>

<FORM NAME="ClientPHQ" ACTION="/cgi/bin/mis.cgi" METHOD="POST" >
<TABLE CLASS="main fullsize" >
  <TR >
    <TD CLASS="strcol" >
      <<<Client_FName_1>>> <<<Client_MName_1>>> <<<Client_LName_1>>> (<<<Client_ClientID_1>>>) <<<Client_SSN_1>>>
      <BR>
      Patient Health Questionnaire (PHQ) View/Edit Page
    </TD>
    <TD CLASS="numcol" >[[gHTML->setLINKS(%form+back)]]</TD>
  </TR>
</TABLE>
<TABLE CLASS="home fullsize" >
  <TR ><TD CLASS="port hdrtxt" >PHQ</TD></TR>
  <TR ><TD CLASS="port" >This questionnaire is an important part of providing you with the best health care possible. Your answers will help in understanding problems that you may have. Please answer every question to the best of your ability unless you are requested to skip over a question.</TD></TR>
  <TR >
    <TD CLASS="port hdrtxt" >
[[[myHTML->setHTML(%form+ClientPHQ)]]]
    </TD>
  </TR>
</TABLE>
<TABLE CLASS="main fullsize" >
  <TR >
    <TD CLASS="numcol" >
      <INPUT TYPE="submit" ONCLICK="return vDELETE('Are you sure you want to delete this record?');" NAME="ClientPHQ_DELETE_1=1&UpdateTables=all&misPOP=1" VALUE="Delete">
      <INPUT TYPE="submit" ONCLICK="return validate(this.form);" NAME="UpdateTables=all&misPOP=1" VALUE="Add/Update">
    </TD>
  </TR>
</TABLE>
<TABLE CLASS="home fullsize" >
  <TR >
    <TD CLASS="port" >
Somatoform Disorder if at least 3 of #1a-m bother the patient a lot and lack an adequate biological explanation. 
<BR><BR>
Major Depressive Syndrome if #2a or b and five or more of #2a-i are at least More than half the days (count #2i if present at all). 
<BR><BR>
Other Depressive Syndrome if #2a or b and two, three, or four of #2a-i are at least More than half the days (count #2i if present at all). Note: the diagnoses of Major Depressive Disorder and Other Depressive Disorder requires ruling out normal bereavement (mild symptoms, duration less than 2 months), a history of a manic episode (Bipolar Disorder) and a physical disorder, medication or other drug as the biological cause of the depressive symptoms. 
<BR><BR>
Page 2 Panic Syndrome if #3a-d are all YES and 4 or more of #4a-k are YES. 
<BR><BR>
Other Anxiety Syndrome if #5a and answers to three or more of #5b-g are More than half the days. Note: The diagnoses of Panic Disorder and Other Anxiety Disorder require ruling out a physical disorder, medication or other drug as the biological cause of the anxiety symptoms. 
<BR><BR>
Page 3 Bulimia Nervosa if #6a,b, and c and #8 are YES; 
<BR><BR>
Binge Eating Disorder the same but #8 is either NO or left blank. 
<BR><BR>
Alcohol abuse if any of #10a-e are YES. 
    </TD>
  </TR>
</TABLE>

</LOADHIDDEN>
</FORM>
<SCRIPT LANGUAGE="JavaScript">
document.ClientPHQ.elements[0].focus();
// just to OPENTABLES...
//<<<ClientPHQ_ClientID_1>>>
</SCRIPT>

[[myHTML->rightpane(%form+search)]]
