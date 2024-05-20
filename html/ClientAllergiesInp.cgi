[[myHTML->newPage(%form+Client Allergies)]]

<SCRIPT LANGUAGE="JavaScript" SRC="/cgi/js/NoEnter.js"> </SCRIPT>
<SCRIPT LANGUAGE="JavaScript" SRC="/cgi/js/vEntry.js"> </SCRIPT>
<SCRIPT LANGUAGE="JavaScript" SRC="/cgi/js/vClientAllergies.js"> </SCRIPT>
<SCRIPT LANGUAGE="JavaScript" SRC="/cgi/js/popuplist.js"> </SCRIPT>
<SCRIPT LANGUAGE="JavaScript" SRC="/cgi/js/ajaxrequest.js"> </SCRIPT>
<SCRIPT LANGUAGE="JavaScript" SRC="/cgi/js/vDate.js"> </SCRIPT>
<SCRIPT LANGUAGE="JavaScript" SRC="/cgi/js/vNum.js"> </SCRIPT>

<FORM NAME="ClientAllergies" ACTION="/cgi/bin/mis.cgi" METHOD="POST" >
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
  <TR ><TD CLASS="port hdrtxt" COLSPAN="3" >ALLERGY<BR>information</TD></TR>
  <TR >
    <TD CLASS="strcol" >Allergy</TD>
    <TD CLASS="strcol" >
      <SELECT NAME="ClientAllergies_AID_1" ID="ClientAllergies_AID_1" SIZE="10" >
        [[DBA->iselxTable(%form+xAllergies+<<ClientAllergies_AID_1>>+Descr)]]
      </SELECT>
    </TD>
[[gHTML->setFilterSearch(allergy+ClientAllergies+ClientAllergies_AID_1+1)]]
  </TR>
  <TR >
    <TD CLASS="strcol" >Severity</TD>
    <TD CLASS="strcol" >
      <SELECT NAME="ClientAllergies_Severity_1">
        [[DBA->selxTable(%form+xSeverity+<<ClientAllergies_Severity_1>>+Descr+0+Descr)]]
      </SELECT> 
[[gHTML->setFilterScript(allergy+ClientAllergies+ClientAllergies_AID_1)]]
    </TD>
  </TR>
  <TR >
    <TD CLASS="strcol" >Start Date</TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="text" NAME="ClientAllergies_StartDate_1" VALUE="<<ClientAllergies_StartDate_1>>" ONFOCUS="select()" ONCHANGE="return vDate(this,1)" SIZE="10" >
    </TD>
  </TR>
  <TR >
    <TD CLASS="strcol" >End Date</TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="text" NAME="ClientAllergies_EndDate_1" VALUE="<<ClientAllergies_EndDate_1>>" ONFOCUS="select()" ONCHANGE="return vDate(this,1)" SIZE="10" >
    </TD>
  </TR>
  <TR >
    <TD CLASS="strcol" >Reaction</TD>
    <TD CLASS="strcol" >
      <SELECT NAME="ClientAllergies_RID_1">
        [[DBA->selxTable(%form+xAdverseReaction+<<ClientAllergies_RID_1>>+ConceptName)]]
      </SELECT> 
    </TD>
  </TR>
  <TR >
    <TD CLASS="strcol" >Comments</TD>
    <TD CLASS="strcol" COLSPAN="2" >
      <TEXTAREA NAME="ClientAllergies_Comments_1" COLS="90" ROWS="8" WRAP="virtual" ><<ClientAllergies_Comments_1>></TEXTAREA>
    </TD>
  </TR>
</TABLE>
<TABLE CLASS="main fullsize" >
  <TR >
    <TD CLASS="numcol" >
      <INPUT TYPE="submit" ONCLICK="return vDELETE('Are you sure you want to delete this record?');" NAME="ClientAllergies_DELETE_1=1&UpdateTables=all&misPOP=1" VALUE="Delete">
      <INPUT TYPE="submit" ONCLICK="return validate(this.form);" NAME="UpdateTables=all&misPOP=1" VALUE="Add/Update">
    </TD>
  </TR>
</TABLE>

</LOADHIDDEN>
</FORM>
<SCRIPT LANGUAGE="JavaScript">
document.ClientAllergies.elements[0].focus();
</SCRIPT>

[[myHTML->rightpane(%form+search)]]
