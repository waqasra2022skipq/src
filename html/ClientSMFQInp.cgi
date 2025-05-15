[[myHTML->newPage(%form+Client SMFQ)]]

<SCRIPT LANGUAGE="JavaScript" SRC="/src/cgi/js/NoEnter.js"> </SCRIPT>
<SCRIPT LANGUAGE="JavaScript" SRC="/src/cgi/js/vEntry.js"> </SCRIPT>
<SCRIPT LANGUAGE="JavaScript" SRC="/src/cgi/js/vClientSMFQ.js"> </SCRIPT>
<SCRIPT LANGUAGE="JavaScript" SRC="/src/cgi/js/vDate.js"> </SCRIPT>

<FORM NAME="ClientSMFQ" ACTION="/cgi/bin/mis.cgi" METHOD="POST" >
<TABLE CLASS="main fullsize" >
  <TR >
    <TD CLASS="strcol" >
      <<<Client_FName_1>>> <<<Client_MName_1>>> <<<Client_LName_1>>> (<<<Client_ClientID_1>>>) <<<Client_SSN_1>>>
      <BR>
      Short Mood and Feeling questionnaire
    </TD>
    <TD CLASS="numcol" >[[gHTML->setLINKS(%form+back)]]</TD>
  </TR>
</TABLE>
<TABLE CLASS="home fullsize" >
  <TR ><TD CLASS="port hdrtxt" >MOOD AND FEELING QUESTIONNAIRE: Short Version</TD></TR>
  <TR ><TD CLASS="port strcol" >This form is about how you might have been feeling or acting recently.<BR><BR>
For each question, please check how you have been feeling or acting <B>in the past two weeks</B>.<BR><BR>
If a sentence was not true about you, check NOT TRUE.<BR>
If a sentence was only sometimes true, check SOMETIMES.<BR>
If a sentence was true about you most of the time, check TRUE.<BR><BR>
<B>Score the MFQ as follows:</B><BR>
NOT TRUE = 0<BR>
SOMETIMES = 1<BR>
TRUE = 2</TD></TR>
  <TR >
    <TD CLASS="port hdrtxt" >
[[[myHTML->setHTML(%form+ClientSMFQ)]]]
    </TD>
  </TR>
</TABLE>
<TABLE CLASS="main fullsize" >
  <TR >
    <TD CLASS="numcol" >
      <INPUT TYPE="submit" ONCLICK="return vDELETE('Are you sure you want to delete this record?');" NAME="ClientSMFQ_DELETE_1=1&UpdateTables=all&misPOP=1" VALUE="Delete">
      <INPUT TYPE="submit" ONCLICK="return validate(this.form);" NAME="UpdateTables=all&misPOP=1" VALUE="Add/Update">
    </TD>
  </TR>
</TABLE>

</LOADHIDDEN>
</FORM>
<SCRIPT LANGUAGE="JavaScript">
document.ClientSMFQ.elements[0].focus();
// just to OPENTABLES...
//<<<ClientSMFQ_ClientID_1>>>
</SCRIPT>

[[myHTML->rightpane(%form+search)]]
