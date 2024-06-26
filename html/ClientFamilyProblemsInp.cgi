[[myHTML->newPage(%form+Presenting Family Problems)]]

<SCRIPT LANGUAGE="JavaScript" SRC="/cgi/js/vEntry.js"> </SCRIPT>
<SCRIPT LANGUAGE="JavaScript" SRC="/cgi/js/vClientFamilyProblems.js"> </SCRIPT>
<SCRIPT LANGUAGE="JavaScript" SRC="/cgi/js/popuplist.js"> </SCRIPT>
<SCRIPT LANGUAGE="JavaScript" SRC="/cgi/js/ajaxrequest.js"> </SCRIPT>
<SCRIPT LANGUAGE="JavaScript" SRC="/cgi/js/vDate.js"> </SCRIPT>

<FORM NAME="ClientProblems" ACTION="/cgi/bin/mis.cgi" METHOD="POST" >
<HR WIDTH="90%" >
<TABLE CLASS="main fullsize" >
  <TR >
    <TD CLASS="strcol" >
      <<<Client_FName_1>>> <<<Client_MName_1>>> <<<Client_LName_1>>> (<<<Client_ClientID_1>>>) <<<Client_SSN_1>>>
      <BR>
      Bio Medical Family Problem Page
    </TD>
    <TD CLASS="numcol" >[[gHTML->setLINKS(%form+back)]]</TD>
  </TR>
</TABLE>
<TABLE CLASS="home fullsize" >
  <TR ><TD CLASS="port hdrtxt" COLSPAN="2" >BIO MEDICAL PROBLEM</TD></TR>
  <TR >
    <TD CLASS="strcol" >
      Date Initiated:
      <INPUT TYPE="text" NAME="ClientFamilyProblems_InitiatedDate_1" VALUE="<<ClientFamilyProblems_InitiatedDate_1>>" ONCHANGE="vDate(this)" SIZE="12" >
    </TD>
    <TD CLASS="strcol" >
      Date Resolved:
      <INPUT TYPE="text" NAME="ClientFamilyProblems_ResolvedDate_1" VALUE="<<ClientFamilyProblems_ResolvedDate_1>>" ONCHANGE="vDate(this,1)" SIZE="12" >
    </TD>
  </TR>
  <TR > <TD CLASS="strcol" COLSPAN="2" >&nbsp;</TD> </TR>
  <TR > <TD CLASS="hdrtxt" COLSPAN="2" >Enter phrase in the Filter to populate/narrow the select list.</TD> </TR>
  <TR > <TD CLASS="hdrtxt" COLSPAN="2" >Then select from the list in order to show the choices for that problem.</TD> </TR>
  <TR > <TD CLASS="strcol" COLSPAN="2" >&nbsp;</TD> </TR>
  <TR >
    <TD CLASS="strcol" COLSPAN="2" >Use these radio buttons to limit the Filter or Select</TD>
  </TR>
  <TR >
    <TD CLASS="strcol" COLSPAN="2" >
      &nbsp;&nbsp;
      <INPUT TYPE="radio" NAME="LIMSEL" VALUE="1" > finding only
      &nbsp;&nbsp;
      <INPUT TYPE="radio" NAME="LIMSEL" VALUE="2" > disorder only
      &nbsp;&nbsp;
      <INPUT TYPE="radio" NAME="LIMSEL" VALUE="0" > all
    </TD>
  </TR>
  <TR >
[[gHTML->setFilterSearch(problem+ClientProblems+ICD10Search+0)]]
  </TR>
  <TR >
    <TD CLASS="strcol" COLSPAN="2" >
      Select one from the checklist below:<BR>
      <SELECT NAME="ICD10Search" ID="ICD10Search" ONCHANGE="callAjax('pProblem',this.value,this.id,'&name=ClientFamilyProblems_UUID_1','popup.pl');" >
        [[DBA->iselxTable(%form+misICD10+<<ClientFamilyProblems_UUID_1>>+sctName SNOMEDID icdName ICD10)]]
      </SELECT>
[[gHTML->setFilterScript(problem+ClientProblems+ICD10Search)]]
    </TD>
  </TR>
  <TR > <TD CLASS="strcol" COLSPAN="2" >&nbsp;</TD> </TR>
  <TR >
    <TD CLASS="strcol" COLSPAN="2" >
      Bio Medical Problem:<BR>
      <SPAN ID="ICD10Check" >
        [[DBA->ichkxTable(%form+misICD10+<<ClientFamilyProblems_UUID_1>>+sctName SNOMEDID icdName ICD10 Rule+ClientFamilyProblems_UUID_1)]]
      </SPAN>
    </TD>
  </TR>
  <TR >
    <TD CLASS="port title" COLSPAN="2" >
ICD10 problems address specific disorders, findings, and events; and can, at times, have additional specific details to address the issue. The FILTER is used to narrow the enormous problem list and to group specific selections which you can then choose the most correct selection. If only one specific selection is available, that one will be checked. Otherwise, select the most correct one of the additional choices. (If the selected ICD10 problem has only one specificer, MIS will display TRUE.  If the selected ICD10 problem has more than one specifier, choose the most accurate selection or select OTHERWISE TRUE, if additional specifier information is unavailable).
    </TD>
  </TR>
  <TR>
    <TD CLASS="strcol" COLSPAN="2" >
      <INPUT TYPE="checkbox" NAME="ClientFamilyProblems_negationInd_1" VALUE="1" <<ClientFamilyProblems_negationInd_1=checkbox>> >
      Patient denies problem
    </TD>
  </TR>
  <TR>
    <TD CLASS="strcol" COLSPAN="2" >
      Notes/Comments:
      <BR>
      <TEXTAREA COLS="120" ROWS="7" WRAP="virtual" NAME="ClientFamilyProblems_Comments_1" ONFOCUS="select();" ><<ClientFamilyProblems_Comments_1>></TEXTAREA>
    </TD>
  </TR>
</TABLE>
<HR WIDTH="90%" >
<TABLE CLASS="main fullsize" >
  <TR>
    <TD CLASS="numcol" >
[[DBUtil->isEQ(<<<LOGINPROVID>>>+91)      <INPUT TYPE="submit" ONCLICK="return vDELETE('Are you sure you want to delete this record?');" NAME="ClientFamilyProblems_DELETE_1=1&UpdateTables=all&misPOP=1" VALUE="Delete">]]
[[DBUtil->isEQ(<<<LOGINPROVID>>>+90)      <INPUT TYPE="submit" ONCLICK="return vDELETE('Are you sure you want to delete this record?');" NAME="ClientFamilyProblems_DELETE_1=1&UpdateTables=all&misPOP=1" VALUE="Delete">]]
      <INPUT TYPE="submit" ONCLICK="return validate(this.form);" NAME="UpdateTables=all&misPOP=1" VALUE="Add/Update">
    </TD>
  </TR>
</TABLE>

<INPUT TYPE="hidden" NAME="post_update" VALUE="PostUpd->renumClientFamilyProblems(%form+<<<Client_ClientID_1>>>)" >
</LOADHIDDEN>
</FORM>
<SCRIPT LANGUAGE="JavaScript">
document.ClientProblems.elements[0].focus();
</SCRIPT>

[[myHTML->rightpane(%form+search)]]
