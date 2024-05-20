[[myHTML->newPage(%form+Client Review)]]

<SCRIPT LANGUAGE="JavaScript" TYPE="text/javascript" SRC="/cgi/js/tabs.js"></SCRIPT>
<LINK REL="STYLESHEET" TYPE="text/css" HREF="/cgi/css/tabs.css" />
<SCRIPT LANGUAGE="JavaScript" SRC="/cgi/js/vEntry.js"> </SCRIPT>
<SCRIPT LANGUAGE="JavaScript" SRC="/cgi/js/vDate.js"> </SCRIPT>
<SCRIPT LANGUAGE="JavaScript">
function validate(form) { return true; } 
</SCRIPT>
</HEAD>
<BODY>
<FORM NAME="ClientReview" ACTION="/cgi/bin/mis.cgi" METHOD="POST" >
<TABLE CLASS="main fullsize" >
  <TR >
    <TD CLASS="strcol" >
      <<<Client_FName_1>>> <<<Client_MName_1>>> <<<Client_LName_1>>> (<<<Client_ClientID_1>>>) <<<Client_SSN_1>>> <<<ClientLegal_JOLTS_1>>>
      <BR>
      Client Review
    </TD>
    <TD CLASS="numcol" >[[gHTML->setLINKS(%form+back)]]</TD>
  </TR>
</TABLE>
<TABLE CLASS="home fullsize" >
  <TR >
    <TD CLASS="strcol" >
      Review Date:
      <INPUT TYPE="text" NAME="ClientReview_RevDate_1" VALUE="<<ClientReview_RevDate_1>>" ONCHANGE="return vDate(this,1)" SIZE="10" >
    </TD>
  </TR>
    <TD CLASS="strcol" >
<!--TAB:Client Information:-->
<TABLE CLASS="home fullsize" >
  <TR >
    <TD CLASS="port hdrtxt" >
      CLIENT INFORMATION
    </TD>
  </TR>
  <TR >
    <TD CLASS="strcol" >
      <INPUT TYPE="checkbox" NAME="ClientReview_ClientInfoNeeded_1" VALUE=1 <<ClientReview_ClientInfoNeeded_1=checkbox>> >
      Correction Needed
    </TD>
  </TR>
  <TR ><TD CLASS="strcol" >Comments</TD></TR>
  <TR >
    <TD CLASS="strcol" >
      <TEXTAREA NAME="ClientReview_ClientInfoComments_1" COLS=80 ROWS=5 WRAP="virtual" ><<ClientReview_ClientInfoComments_1>></TEXTAREA>
    </TD>
  </TR>
  <TR >
    <TD CLASS="strcol" >
      <INPUT TYPE="checkbox" NAME="ClientReview_ReferralCompleted_1" VALUE=1 <<ClientReview_ReferralCompleted_1=checkbox>> >
      Referral Completed
    </TD>
  </TR>
</TABLE>
<!--TAB:Consents:-->
<TABLE CLASS="home fullsize" >
  <TR >
    <TD CLASS="port hdrtxt" >
      CONSENTS
    </TD>
  </TR>
  <TR >
    <TD CLASS="strcol" >
      <INPUT TYPE="checkbox" NAME="ClientReview_ConsentNeeded_1" VALUE=1 <<ClientReview_ConsentNeeded_1=checkbox>> >
      Consent Needed
    </TD>
  </TR>
  <TR ><TD CLASS="strcol" >Comments</TD></TR>
  <TR >
    <TD CLASS="strcol" >
      <TEXTAREA NAME="ClientReview_ConsentComments_1" COLS=80 ROWS=5 WRAP="virtual" ><<ClientReview_ConsentComments_1>></TEXTAREA>
    </TD>
  </TR>
  <TR >
    <TD CLASS="strcol" >
      <INPUT TYPE="checkbox" NAME="ClientReview_PaymentAgreement_1" VALUE=1 <<ClientReview_PaymentAgreement_1=checkbox>> >
      Payment Agreement
    </TD>
  </TR>
  <TR >
    <TD CLASS="strcol" >
      <INPUT TYPE="checkbox" NAME="ClientReview_ConsentToTransport_1" VALUE=1 <<ClientReview_ConsentToTransport_1=checkbox>> >
      Consent To Transport
    </TD>
  </TR>
</TABLE>
<!--TAB:Initial Intake Assessment:-->
<TABLE CLASS="home fullsize" >
  <TR >
    <TD CLASS="port hdrtxt" >
      INITIAL INTAKE ASSESSMENT
    </TD>
  </TR>
  <TR >
    <TD CLASS="strcol" >
      <INPUT TYPE="checkbox" NAME="ClientReview_InitialIntakeNeeded_1" VALUE=1 <<ClientReview_InitialIntakeNeeded_1=checkbox>> >
      Initial Intake  Needed
    </TD>
  </TR>
  <TR ><TD CLASS="strcol" >Comments</TD></TR>
  <TR >
    <TD CLASS="strcol" >
      <TEXTAREA NAME="ClientReview_InitialIntakeComments_1" COLS=80 ROWS=5 WRAP="virtual" ><<ClientReview_InitialIntakeComments_1>></TEXTAREA>
    </TD>
  </TR>
  <TR >
    <TD CLASS="strcol" >
      <INPUT TYPE="checkbox" NAME="ClientReview_ReferralReasons_1" VALUE=1 <<ClientReview_ReferralReasons_1=checkbox>> >
      Referral Reasons
    </TD>
  </TR>
  <TR >
    <TD CLASS="strcol" >
      <INPUT TYPE="checkbox" NAME="ClientReview_IdentifyingInfo_1" VALUE=1 <<ClientReview_IdentifyingInfo_1=checkbox>> >
      Identifying Information
    </TD>
  </TR>
</TABLE>
<!--TAB:Treatment Plan:-->
<TABLE CLASS="home fullsize" >
  <TR >
    <TD CLASS="port hdrtxt" >
      TREATMENT PLAN
    </TD>
  </TR>
  <TR >
    <TD CLASS="strcol" >
      <INPUT TYPE="checkbox" NAME="ClientReview_TrPlanNeeded_1" VALUE=1 <<ClientReview_TrPlanNeeded_1=checkbox>> >
      Treatment Plan Needed
    </TD>
  </TR>
  <TR ><TD CLASS="strcol" >Comments</TD></TR>
  <TR >
    <TD CLASS="strcol" >
      <TEXTAREA NAME="ClientReview_TrPlanComments_1" COLS=80 ROWS=5 WRAP="virtual" ><<ClientReview_TrPlanComments_1>></TEXTAREA>
    </TD>
  </TR>
  <TR >
    <TD CLASS="strcol" >
      <INPUT TYPE="checkbox" NAME="ClientReview_ProblemsIdentified_1" VALUE=1 <<ClientReview_ProblemsIdentified_1=checkbox>> >
      Problems Identified
    </TD>
  </TR>
</TABLE>
<!--TAB:Progress Notes:-->
<TABLE CLASS="home fullsize" >
  <TR >
    <TD CLASS="port hdrtxt" >
      PROGRESS NOTES
    </TD>
  </TR>
  <TR >
    <TD CLASS="strcol" >
      <INPUT TYPE="checkbox" NAME="ClientReview_ProgressNotesNeeded_1" VALUE=1 <<ClientReview_ProgressNotesNeeded_1=checkbox>> >
      Progress Notes  Needed
    </TD>
  </TR>
  <TR ><TD CLASS="strcol" >Comments</TD></TR>
  <TR >
    <TD CLASS="strcol" >
      <TEXTAREA NAME="ClientReview_ProgressNotesComments_1" COLS=80 ROWS=5 WRAP="virtual" ><<ClientReview_ProgressNotesComments_1>></TEXTAREA>
    </TD>
  </TR>
  <TR >
    <TD CLASS="strcol" >
      <INPUT TYPE="checkbox" NAME="ClientReview_InitialTrPlanNote_1" VALUE=1 <<ClientReview_InitialTrPlanNote_1=checkbox>> >
      Initial Treatment Plan Note Completed
    </TD>
  </TR>
</TABLE>
<!--TAB:Discharge Summary:-->
<TABLE CLASS="home fullsize" >
  <TR >
    <TD CLASS="port hdrtxt" >
      DISCHARGE SUMMARY
    </TD>
  </TR>
  <TR >
    <TD CLASS="strcol" >
      <INPUT TYPE="checkbox" NAME="ClientReview_DischargeSummaryNeeded_1" VALUE=1 <<ClientReview_DischargeSummaryNeeded_1=checkbox>> >
      Discharge Summary Needed
    </TD>
  </TR>
  <TR ><TD CLASS="strcol" >Comments</TD></TR>
  <TR >
    <TD CLASS="strcol" >
      <TEXTAREA NAME="ClientReview_DischargeSummaryComments_1" COLS=80 ROWS=5 WRAP="virtual" ><<ClientReview_DischargeSummaryComments_1>></TEXTAREA>
    </TD>
  </TR>
  <TR >
    <TD CLASS="strcol" >
      <INPUT TYPE="checkbox" NAME="ClientReview_AdmissionDateDocumented_1" VALUE=1 <<ClientReview_AdmissionDateDocumented_1=checkbox>> >
      Admission Date Documented
    </TD>
  </TR>
  <TR >
    <TD CLASS="strcol" >
      <INPUT TYPE="checkbox" NAME="ClientReview_DischargeDateDocumented_1" VALUE=1 <<ClientReview_DischargeDateDocumented_1=checkbox>> >
      Discharge Date Documented
    </TD>
  </TR>
  <TR >
    <TD CLASS="strcol" >
      <INPUT TYPE="checkbox" NAME="ClientReview_ReasonForDischargeDocumented_1" VALUE=1 <<ClientReview_ReasonForDischargeDocumented_1=checkbox>> >
      Reason For Discharge Documented
    </TD>
  </TR>
  <TR >
    <TD CLASS="strcol" >
      <INPUT TYPE="checkbox" NAME="ClientReview_ProgressDocumented_1" VALUE=1 <<ClientReview_ProgressDocumented_1=checkbox>> >
      Progress Documented
    </TD>
  </TR>
  <TR >
    <TD CLASS="strcol" >
      <INPUT TYPE="checkbox" NAME="ClientReview_SkillsDevelopedDocumented_1" VALUE=1 <<ClientReview_SkillsDevelopedDocumented_1=checkbox>> >
      Skills Developed Documented
    </TD>
  </TR>
  <TR >
    <TD CLASS="strcol" >
      <INPUT TYPE="checkbox" NAME="ClientReview_TransitionPlanDocumented_1" VALUE=1 <<ClientReview_TransitionPlanDocumented_1=checkbox>> >
      Transition Plan Documented
    </TD>
  </TR>
  <TR >
    <TD CLASS="strcol" >
      <INPUT TYPE="checkbox" NAME="ClientReview_NeedsDocumented_1" VALUE=1 <<ClientReview_NeedsDocumented_1=checkbox>> >
      Needs/Preferences Documented
    </TD>
  </TR>
  <TR >
    <TD CLASS="strcol" >
      <INPUT TYPE="checkbox" NAME="ClientReview_GAFScoresDocumented_1" VALUE=1 <<ClientReview_GAFScoresDocumented_1=checkbox>> >
      GAF Scores Documented
    </TD>
  </TR>
  <TR >
    <TD CLASS="strcol" >
      <INPUT TYPE="checkbox" NAME="ClientReview_ReferralsDocumented_1" VALUE=1 <<ClientReview_ReferralsDocumented_1=checkbox>> >
      Referrals Documented
    </TD>
  </TR>
  <TR >
    <TD CLASS="strcol" >
      <INPUT TYPE="checkbox" NAME="ClientReview_MedicationsDocumented_1" VALUE=1 <<ClientReview_MedicationsDocumented_1=checkbox>> >
      Medications Documented
    </TD>
  </TR>
  <TR >
    <TD CLASS="strcol" >
      <INPUT TYPE="checkbox" NAME="ClientReview_FollowUpDocumented_1" VALUE=1 <<ClientReview_FollowUpDocumented_1=checkbox>> >
      Follow Up Documented
    </TD>
  </TR>
  <TR >
    <TD CLASS="strcol" >
      <INPUT TYPE="checkbox" NAME="ClientReview_ProviderDocumented_1" VALUE=1 <<ClientReview_ProviderDocumented_1=checkbox>> >
      Provider Documented
    </TD>
  </TR>
  <TR ><TD CLASS="strcol" >Additional Comments</TD></TR>
  <TR >
    <TD CLASS="strcol" >
      <TEXTAREA NAME="ClientReview_AdditionalComments_1" COLS=80 ROWS=5 WRAP="virtual" ><<ClientReview_AdditionalComments_1>></TEXTAREA>
    </TD>
  </TR>
</TABLE>
<!--ENDTABS-->
<TABLE CLASS="home fullsize" >
  <TR >
    <TD CLASS="numcol" >
      <INPUT TYPE="submit" ONCLICK="return vDELETE('Are you sure you want to delete this review?');" NAME="ClientReview_DELETE_1=1&UpdateTables=all&misPOP=1" VALUE="DELETE Entire Review">
      <INPUT TYPE="submit" ONCLICK="return validate(this.form);" NAME="UpdateTables=all&misPOP=1" VALUE="Add/Update">
    </TD>
  </TR>
</TABLE>
    </TD>
  </TR>
</TABLE>
</LOADHIDDEN>
</FORM>
<SCRIPT LANGUAGE="JavaScript">
document.ClientReview.elements[0].focus();
</SCRIPT>

[[myHTML->rightpane(%form+search)]]
