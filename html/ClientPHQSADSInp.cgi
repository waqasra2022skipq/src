[[myHTML->newPage(%form+Client PHQSADS)]]

<SCRIPT LANGUAGE="JavaScript" SRC="/cgi/js/NoEnter.js"> </SCRIPT>
<SCRIPT LANGUAGE="JavaScript" SRC="/cgi/js/vEntry.js"> </SCRIPT>
<SCRIPT LANGUAGE="JavaScript" SRC="/cgi/js/vClientPHQSADS.js"> </SCRIPT>
<SCRIPT LANGUAGE="JavaScript" SRC="/cgi/js/vDate.js"> </SCRIPT>

<FORM NAME="ClientPHQSADS" ACTION="/cgi/bin/mis.cgi" METHOD="POST" >
<TABLE CLASS="main fullsize" >
  <TR >
    <TD CLASS="strcol" >
      <<<Client_FName_1>>> <<<Client_MName_1>>> <<<Client_LName_1>>> (<<<Client_ClientID_1>>>) <<<Client_SSN_1>>>
      <BR>
      Patient Health Questionnaire (PHQSADS) View/Edit Page
    </TD>
    <TD CLASS="numcol" >[[gHTML->setLINKS(%form+back)]]</TD>
  </TR>
</TABLE>
<TABLE CLASS="home fullsize" >
  <TR ><TD CLASS="port hdrtxt" >PHQ SADS</TD></TR>
  <TR ><TD CLASS="port" >This questionnaire is an important part of providing you with the best health care possible. Your answers will help in understanding problems that you may have. Please answer every question to the best of your ability unless you are requested to skip over a question.</TD></TR>
  <TR >
    <TD CLASS="port hdrtxt" >
[[[myHTML->setHTML(%form+ClientPHQSADS)]]]
    </TD>
  </TR>
</TABLE>
<TABLE CLASS="main fullsize" >
  <TR >
    <TD CLASS="numcol" >
      <INPUT TYPE="submit" ONCLICK="return vDELETE('Are you sure you want to delete this record?');" NAME="ClientPHQSADS_DELETE_1=1&UpdateTables=all&misPOP=1" VALUE="Delete">
      <INPUT TYPE="submit" ONCLICK="return validate(this.form);" NAME="UpdateTables=all&misPOP=1" VALUE="Add/Update">
    </TD>
  </TR>
</TABLE>

</LOADHIDDEN>
</FORM>
<SCRIPT LANGUAGE="JavaScript">
document.ClientPHQSADS.elements[0].focus();
// just to OPENTABLES...
//<<<ClientPHQSADS_ClientID_1>>>
</SCRIPT>

[[myHTML->rightpane(%form+search)]]
