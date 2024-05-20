[[myHTML->newHTML(%form+Client Interventions Performed)]]

<SCRIPT LANGUAGE="JavaScript" SRC="/cgi/js/vEntry.js"> </SCRIPT>
<SCRIPT LANGUAGE="JavaScript" SRC="/cgi/js/vClientInterventionsPerformed.js"> </SCRIPT>
<SCRIPT LANGUAGE="JavaScript" SRC="/cgi/js/vDate.js"> </SCRIPT>
<SCRIPT LANGUAGE="JavaScript" SRC="/cgi/js/vNum.js"> </SCRIPT>
<SCRIPT type="text/javascript" src="/cgi/js/ajaxrequest.js"></SCRIPT>

<FORM NAME="InterventionsPerformed" ACTION="/cgi/bin/mis.cgi" METHOD="POST" >
<TABLE CLASS="main fullsize" >
  <TR >
    <TD CLASS="strcol" >
      <<<Client_FName_1>>> <<<Client_MName_1>>> <<<Client_LName_1>>> (<<<Client_ClientID_1>>>) <<<Client_SSN_1>>>
      <BR>
      Intervention Performed Page
    </TD>
    <TD CLASS="numcol" >[[gHTML->setLINKS(%form+back)]]</TD>
  </TR>
</TABLE>
<TABLE CLASS="home fullsize" >
  <TR ><TD CLASS="port hdrcol" COLSPAN="2" >Intervention Performed</TD></TR>
  <TR >
    <TD CLASS="strcol" >
      Performed Date
    </TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="text" NAME="ClientInterventionsPerformed_VisitDate_1" VALUE="<<ClientInterventionsPerformed_VisitDate_1>>" ONFOCUS="select()" ONCHANGE="return vDate(this)" MAXLENGTH="10" SIZE="10" >
    </TD>
  </TR>
  <TR >
    <TD CLASS="strcol" >Performed</TD>
    <TD CLASS="strcol" COLSPAN="3" >
      <SELECT NAME="ClientInterventionsPerformed_Intervention_1">
        [[DBA->selxTable(%form+xInterventionPerformed+<<ClientInterventionsPerformed_Intervention_1>>+ConceptName ConceptCode)]]
      </SELECT>
    </TD>
  </TR>
  <TR >
    <TD CLASS="strcol" >Reason</TD>
    <TD CLASS="strcol" COLSPAN="3" >
      <SELECT NAME="ClientInterventionsPerformed_Reason_1">
        [[DBA->selxTable(%form+xInterventionPerformedReason+<<ClientInterventionsPerformed_Reason_1>>+ConceptName ConceptCode)]]
      </SELECT>
    </TD>
  </TR>
  <TR >
    <TD CLASS="strcol" >Rejected Reason</TD>
    <TD CLASS="strcol" COLSPAN="3" >
      <SELECT NAME="ClientInterventionsPerformed_Rejected_1">
        [[DBA->selxTable(%form+xInterventionPerformedRejected+<<ClientInterventionsPerformed_Rejected_1>>+ConceptName ConceptCode)]]
      </SELECT>
    </TD>
  </TR>
</TABLE>

<TABLE CLASS="main fullsize" >
  <TR >
    <TD CLASS="numcol" >
[[SysAccess->verify(%form+Privilege=Agent)      <INPUT TYPE="submit" ONCLICK="return vDELETE('Are you sure you want to delete this Performed record?')" NAME="ClientInterventionsPerformed_DELETE_1=1&UpdateTables=all&misPOP=1" VALUE="Delete" > ]]
      <INPUT TYPE="submit" ONCLICK="return validate(this.form);" NAME="UpdateTables=all&misPOP=1" VALUE="Add/Update">
    </TD>
  </TR>
</TABLE>

</LOADHIDDEN>
</FORM>
<SCRIPT LANGUAGE="JavaScript">
document.InterventionsPerformed.elements[0].focus();
</SCRIPT>

[[myHTML->rightpane(%form+search)]]
