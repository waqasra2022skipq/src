[[myHTML->newHTML(%form+Client Interventions Performed)]]

<SCRIPT LANGUAGE="JavaScript" SRC="/src/cgi/js/vEntry.js"> </SCRIPT>
<SCRIPT LANGUAGE="JavaScript" SRC="/src/cgi/js/vClientInterventionsPerformed.js"> </SCRIPT>
<SCRIPT LANGUAGE="JavaScript" SRC="/src/cgi/js/vDate.js"> </SCRIPT>
<SCRIPT LANGUAGE="JavaScript" SRC="/src/cgi/js/vNum.js"> </SCRIPT>
<SCRIPT type="text/javascript" src="/src/cgi/js/ajaxrequest.js"></SCRIPT>

<FORM NAME="InterventionsPerformed" ACTION="/src/cgi/bin/mis.cgi" METHOD="POST" >
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
  <TR STYLE= "margin-botton:5px;">
    <TD CLASS="strcol" >Performed</TD>
    <TD CLASS="strcol" COLSPAN="3" >
      <SELECT NAME="ClientInterventionsPerformed_Intervention_1" ID="performedSelect">
        [[DBA->selxTable(%form+xInterventionPerformed+<<ClientInterventionsPerformed_Intervention_1>>+ConceptName ConceptCode)]]
      </SELECT>
    </TD>
  </TR>

  <BR><BR>
  <TR>
  <TD CLASS="strcol">Assessment</TD>
  <TD CLASS="strcol" COLSPAN="3">
    <SELECT NAME="ClientInterventionsPerformed_Assessment_1">
    [[DBA->selxTable(%form+xRiskAssessment+<<ClientInterventionsPerformed_Assessment_1>>+ConceptName ConceptCode)]]
    </SELECT>
  </TD>
</TR>
  
  <TR ID="Reason_TR" STYLE= "display:none;">
    <TD CLASS="strcol" >Reason</TD>
    <TD CLASS="strcol" COLSPAN="3" >
      <SELECT NAME="ClientInterventionsPerformed_Reason_1">
        [[DBA->selxTable(%form+xInterventionPerformedReason+<<ClientInterventionsPerformed_Reason_1>>+ConceptName ConceptCode)]]
      </SELECT>
    </TD>
    
  </TR>
  
  <TR ID="finding_TR" STYLE= "display:none;">
    <TD CLASS="strcol" >
      Finding
    </TD>
    <TD CLASS="strcol" >
        <select NAME="ClientInterventionsPerformed_finding_1" ID="finding" data-value="<<ClientInterventionsPerformed_finding_1>>">
            <OPTION>unselected</OPTION>
            <OPTION VALUE="428171000124102" >Depression screening negative (finding) | 428171000124102 | G8510</OPTION>
            <OPTION VALUE="428181000124104">Depression screening positive (finding) AND Follow-Up Plan Documented | 428181000124104 | G8431</OPTION>
            <OPTION VALUE="G8511">Depression screening positive (finding) BUT Follow-Up Plan not Documented, Reason not Given | G8511</OPTION>
        </select>
    </TD>
  </TR>

  <TR ID="FollowUpPlan_TR" STYLE= "display:none;">
    <TD CLASS="strcol" >
      Follow-Up Plan
    </TD>
    <TD CLASS="strcol" >
        <select NAME="ClientInterventionsPerformed_FollowUpPlan_1" ID="FollowUpPlan" data-value="<<ClientInterventionsPerformed_FollowUpPlan_1>>">
            <OPTION VALUE="306226009">Referral to a provider for additional evaluation and assessment to formulate a follow-up plan for a positive depression screen | 306226009</OPTION>
            <OPTION VALUE="698456001">Pharmacological interventions | 698456001</OPTION>
            <OPTION VALUE="306227000">Other interventions or follow-up for the diagnosis or treatment of depression | 306227000</OPTION>
        </select>
    </TD>
  </TR>

  <TR>
    <TD CLASS="strcol" >
      Not Performed
    </TD>
    <TD CLASS="strcol" >
        <select NAME="ClientInterventionsPerformed_NotPerformed_1" ID="NotPerformed" data-value="<<ClientInterventionsPerformed_NotPerformed_1>>">
            <OPTION value="">unselected</OPTION>
            <OPTION VALUE="454841000124105">Depression screening not done | 454841000124105 | G0444</OPTION>
        </select>
    </TD>
  </TR>

  <TR STYLE= "display:none;" ID="ReasonForExclusion_TR">
    <TD CLASS="strcol" >
      Reason for Exclusion
    </TD>
    <TD CLASS="strcol" >
        <select NAME="ClientInterventionsPerformed_ReasonForExclusion_1" ID="ReasonForExclusion" data-value="<<ClientInterventionsPerformed_ReasonForExclusion_1>>">
            <OPTION value="">unselected</OPTION>
            <OPTION VALUE="400998002">Documentation stating the patient has had a diagnosis of bipolar disorder | 400998002 | G9717</OPTION>
        </select>
    </TD>
  </TR>
  <TR STYLE= "display:none;" ID="ReasonForRejected_TR">
    <TD CLASS="strcol" >Rejected Reason</TD>
    <TD CLASS="strcol" COLSPAN="3" >
      <SELECT NAME="ClientInterventionsPerformed_Rejected_1">
        [[DBA->selxTable(%form+xInterventionPerformedRejected+<<ClientInterventionsPerformed_Rejected_1>>+ConceptName ConceptCode)]]
      </SELECT>
    </TD>
  </TR>
   <TR STYLE= "display:none;" ID="ReasonForException_TR">
    <TD CLASS="strcol" >
      Reason for Exception
    </TD>
    <TD CLASS="strcol" >
        <select STYLE="width: 100px;text-overflow: ellipsis;" NAME="ClientInterventionsPerformed_ReasonForException_1" ID="ReasonForException" data-value="<<ClientInterventionsPerformed_ReasonForException_1>>">
            <OPTION value="">unselected</OPTION>
            <OPTION VALUE="183944003">Patient refuses to participate in or complete the depression screening | 183944003 | G8433</OPTION>
            <OPTION VALUE="G8433">Documentation of medical reason for not screening patient for depression 
            (e.g., cognitive, functional, or motivational limitations that may impact accuracy of results; patient is in an urgent or emergent situation where time is of the essence and to delay treatment would jeopardize the patient’s health status)  | G8433</OPTION>
        </select>
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
<SCRIPT type="text/javascript" src="/src/cgi/js/toggleSelects.js"></SCRIPT>

[[myHTML->rightpane(%form+search)]]
