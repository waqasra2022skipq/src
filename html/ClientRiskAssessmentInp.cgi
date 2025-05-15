[[myHTML->newHTML(%form+Client Risk Assessment+clock mail managertree collapseipad mismenu)]]

<SCRIPT LANGUAGE="JavaScript" SRC="/src/cgi/js/vEntry.js"> </SCRIPT>
<SCRIPT LANGUAGE="JavaScript" SRC="/src/cgi/js/vClientRiskAssessment.js"> </SCRIPT>
<SCRIPT LANGUAGE="JavaScript" SRC="/src/cgi/js/vDate.js"> </SCRIPT>
<SCRIPT LANGUAGE="JavaScript" SRC="/src/cgi/js/vNum.js"> </SCRIPT>
<SCRIPT type="text/javascript" src="/src/cgi/js/ajaxrequest.js"></SCRIPT>

<FORM NAME="RiskAssessment" ACTION="/cgi/bin/mis.cgi" METHOD="POST" >
<TABLE CLASS="main fullsize" >
  <TR >
    <TD CLASS="strcol" >
      <<<Client_FName_1>>> <<<Client_MName_1>>> <<<Client_LName_1>>> (<<<Client_ClientID_1>>>) <<<Client_SSN_1>>>
      <BR>
      Risk Assessment Page
    </TD>
    <TD CLASS="numcol" >[[gHTML->setLINKS(%form+back)]]</TD>
  </TR>
</TABLE>
<TABLE CLASS="home fullsize" >
  <TR ><TD CLASS="port hdrcol" COLSPAN="2" >Risk Assessment</TD></TR>
  <TR >
    <TD CLASS="strcol" >
      Assess Date
    </TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="text" NAME="ClientRiskAssessment_VisitDate_1" VALUE="<<ClientRiskAssessment_VisitDate_1>>" ONFOCUS="select()" ONCHANGE="return vDate(this)" MAXLENGTH="10" SIZE="10" >
    </TD>
  </TR>
  <TR >
    <TD CLASS="strcol" >Assessment</TD>
    <TD CLASS="strcol" COLSPAN="3" >
      <SELECT NAME="ClientRiskAssessment_Assessment_1">
        [[DBA->selxTable(%form+xRiskAssessment+<<ClientRiskAssessment_Assessment_1>>+ConceptName ConceptCode)]]
      </SELECT>
    </TD>
  </TR>
  <TR >
    <TD CLASS="strcol" >Result</TD>
    <TD CLASS="strcol" COLSPAN="3" >
      <SELECT NAME="ClientRiskAssessment_Result_1">
        [[DBA->selxTable(%form+xRiskAssessmentResult+<<ClientRiskAssessment_Result_1>>+ConceptName ConceptCode)]]
      </SELECT>
    </TD>
  </TR>
  <TR >
    <TD CLASS="strcol" >Rejected Reason</TD>
    <TD CLASS="strcol" COLSPAN="3" >
      <SELECT NAME="ClientRiskAssessment_Rejected_1">
        [[DBA->selxTable(%form+xRiskAssessmentRejected+<<ClientRiskAssessment_Rejected_1>>+ConceptName ConceptCode)]]
      </SELECT>
    </TD>
  </TR>
</TABLE>

<TABLE CLASS="main fullsize" >
  <TR >
    <TD CLASS="numcol" >
[[SysAccess->verify(%form+Privilege=Agent)      <INPUT TYPE="submit" ONCLICK="return vDELETE('Are you sure you want to delete this Assessment record?')" NAME="ClientRiskAssessment_DELETE_1=1&UpdateTables=all&misPOP=1" VALUE="Delete" > ]]
      <INPUT TYPE="submit" ONCLICK="return validate(this.form);" NAME="UpdateTables=all&misPOP=1" VALUE="Add/Update">
    </TD>
  </TR>
</TABLE>

</LOADHIDDEN>
</FORM>
<SCRIPT LANGUAGE="JavaScript">
document.RiskAssessment.elements[0].focus();
</SCRIPT>

[[myHTML->rightpane(%form+search)]]
