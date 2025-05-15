[[myHTML->newHTML(%form+American Society of Addiction Medicine)]]

<SCRIPT LANGUAGE="JavaScript" SRC="/src/cgi/js/NoEnter.js"> </SCRIPT>
<SCRIPT LANGUAGE="JavaScript" SRC="/src/cgi/js/vEntry.js"> </SCRIPT>
<SCRIPT LANGUAGE="JavaScript" SRC="/src/cgi/js/vClientASAM.js"> </SCRIPT>
<SCRIPT LANGUAGE="JavaScript" SRC="/src/cgi/js/vNum.js"> </SCRIPT>
<SCRIPT LANGUAGE="JavaScript" SRC="/src/cgi/js/vDate.js"> </SCRIPT>

<FORM NAME="ASAM" ACTION="/cgi/bin/mis.cgi" METHOD="POST" >
<TABLE CLASS="main fullsize" >
  <TR >
    <TD CLASS="strcol" COLSPAN="2" >
      <<<Client_FName_1>>> <<<Client_MName_1>>> <<<Client_LName_1>>> (<<<Client_ClientID_1>>>) <<<Client_SSN_1>>>
      <BR>ASAM PPC-2 65D-30 (Adult)
    </TD>
    <TD CLASS="numcol" >[[gHTML->setLINKS(%form+back)]]</TD>
  </TR>
</TABLE>
<HR WIDTH="90%" >
<TABLE CLASS="home fullsize" >
    <TR ><TD COLSPAN="5" ><TABLE CLASS="port fullsize" >
  <TR >
    <TD CLASS="strcol" >Interviewer </TD>
    <TD CLASS="strcol" >
      <SELECT NAME="ClientASAM_Interviewer_1">
        [[DBA->selProviders(%form+<<ClientASAM_Interviewer_1>>]]
      </SELECT> 
    </TD>
  </TR>
  <TR >
    <TD CLASS="strcol" >Interview Date </TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="text" NAME="ClientASAM_TestDate_1" VALUE="<<ClientASAM_TestDate_1>>" ONFOCUS="select()" ONCHANGE="return vDate(this)" MAXLENGTH="10" SIZE="10" >
    </TD>
  </TR>
    </TABLE></TD></TR>
</TABLE>
<TABLE CLASS="home fullsize" >
  <TR ><TD CLASS="port hdrtxt" COLSPAN="5" >Adult 65D-30 Outpatient ASAM Level II.1</TD></TR>
    <TR ><TD COLSPAN="5" ><TABLE CLASS="home fullsize" >
  <TR >
    <TD CLASS="strcol" WIDTH="15%" >DIMENSIONS</TD>
    <TD CLASS="strcol" >ADMISSION CRITERIA</TD>
    <TD CLASS="strcol" >
      Check all items in each dimension that apply to the client. Place a check in the appropriate box that indicates validation or lack of validation for placement into this level of care.
    </TD>
    <TD CLASS="strcol" style='vertical-align: bottom' WIDTH="5%" >YES</TD>
    <TD CLASS="strcol" style='vertical-align: bottom' WIDTH="5%" >NO</TD>
  </TR>
    </TABLE></TD></TR>
    <TR ><TD COLSPAN="5" ><TABLE CLASS="home fullsize" >
  <TR >
    <TD CLASS="strcol" WIDTH="15%" >ASAM Requirements</TD>
    <TD CLASS="strcol" COLSPAN="2" >
      Must meet Dimensions 1, 2, or 3 and one of Dimensions 4, 5, or 6. Transfer criteria: Clients may be transferred to this level of care when they have met essential treatment objectives in a more intensive level and require this intensity of service provided at this level of care in at least one dimension. A client may transfer from ASAM Level I when services at that level have been insufficient to address the client's needs or when ASAM Level I has consisted of motivational interventions to prepare the client for participation in a more intensive level of care for which admission criteria are met.
    </TD>
    <TD CLASS="strcol" WIDTH="5%" >
      <INPUT TYPE="radio" NAME="ClientASAM_Meets_1" VALUE=1 <<ClientASAM_Meets_1=1>> >
    </TD>
    <TD CLASS="strcol" WIDTH="5%" >
      <INPUT TYPE="radio" NAME="ClientASAM_Meets_1" VALUE=0 <<ClientASAM_Meets_1=0>> >
    </TD>
  </TR>
    </TABLE></TD></TR>
    <TR ><TD COLSPAN="5" ><TABLE CLASS="home fullsize" >
  <TR >
    <TD CLASS="strcol" WIDTH="15%" ROWSPAN="3" >
      Dimension 1:<BR>Acute Intoxication and/or Withdrawal Potential
    </TD>
    <TD CLASS="strcol" COLSPAN="2" >
      The client's situation in this dimension is characterized by one of the following:
    </TD>
    <TD CLASS="strcol" WIDTH="5%" >
      <INPUT TYPE="radio" NAME="ClientASAM_D1_1" VALUE=1 <<ClientASAM_D1_1=1>> >
    </TD>
    <TD CLASS="strcol" WIDTH="5%" >
      <INPUT TYPE="radio" NAME="ClientASAM_D1_1" VALUE=0 <<ClientASAM_D1_1=0>> >
    </TD>
  </TR>
  <TR >
    <TD CLASS="strcol" COLSPAN="2" >
      <INPUT TYPE="checkbox" NAME="ClientASAM_D1v1_1" VALUE=1 <<ClientASAM_D1v1_1=checkbox>> >
      a. Client is free from intoxication or withdrawal symptoms/risks; or
    </TD>
    <TD CLASS="strcol" COLSPAN="2" >&nbsp;</TD>
  </TR>
  <TR >
    <TD CLASS="strcol" COLSPAN="2" >
      <INPUT TYPE="checkbox" NAME="ClientASAM_D1v2_1" VALUE=1 <<ClientASAM_D1v2_1=checkbox>> >
      b. The client's intoxication or withdrawal symptoms/risks can be managed at this level of care.
    </TD>
    <TD CLASS="strcol" COPSPAN="2" >&nbsp;</TD>
  </TR>
    </TABLE></TD></TR>
    <TR ><TD COLSPAN="5" ><TABLE CLASS="home fullsize" >
  <TR >
    <TD CLASS="strcol" WIDTH="15%" >
      Dimension 2:<BR>Biomedical Conditions and Complications
    </TD>
    <TD CLASS="strcol" COLSPAN="2" >
      None or not a distraction from treatment and manageable in ASAM Level II.1. The client's biomedical conditions, if any, are stable or are being concurrently addressed and will not interfere with treatment at this level of care.
    </TD>
    <TD CLASS="strcol" WIDTH="5%" >
      <INPUT TYPE="radio" NAME="ClientASAM_D2_1" VALUE=1 <<ClientASAM_D2_1=1>> >
    </TD>
    <TD CLASS="strcol" WIDTH="5%" >
      <INPUT TYPE="radio" NAME="ClientASAM_D2_1" VALUE=0 <<ClientASAM_D2_1=0>> >
    </TD>
  </TR>
    </TABLE></TD></TR>
    <TR ><TD COLSPAN="5" ><TABLE CLASS="home fullsize" >
  <TR >
    <TD CLASS="strcol" WIDTH="15%" ROWSPAN="10" >
      Dimension 3:<BR>Emotional, Behavioral or Cognitive Conditions and Complications
    </TD>
    <TD CLASS="strcol" COLSPAN="2" >
      Problems in Dimension 3 are not necessary for admission to a Level II.1 program. However, if any of the Dimension 3 conditions are present, the client must be admitted to either a Dual Diagnosis Capableor Dual Diagnosis Enhanced program, depending on the client's level of functioning, stability and degree of impairment in this dimension.
    </TD>
    <TD CLASS="strcol" WIDTH="5%" >
      <INPUT TYPE="radio" NAME="ClientASAM_D3_1" VALUE=1 <<ClientASAM_D3_1=1>> >
    </TD>
    <TD CLASS="strcol" WIDTH="5%" >
      <INPUT TYPE="radio" NAME="ClientASAM_D3_1" VALUE=0 <<ClientASAM_D3_1=0>> >
    </TD>
  </TR>
  <TR >
    <TD CLASS="strcol" COLSPAN="2" ><B>Dual Diagnosed Capable Programs</B></TD>
    <TD CLASS="strcol" COLSPAN="2" >&nbsp;</TD>
  </TR>
  <TR >
    <TD CLASS="strcol" COLSPAN="2" >The client's status in Dimension 3 is characterized by (a) or (b):</TD>
    <TD CLASS="strcol" COLSPAN="2" >&nbsp;</TD>
  </TR>
  <TR >
    <TD CLASS="strcol" COLSPAN="2" >
      <INPUT TYPE="checkbox" NAME="ClientASAM_D3v1_1" VALUE=1 <<ClientASAM_D3v1_1=checkbox>> >
      a. The client engages in abuse of family members or significant others, and requires intensive outpatient treatment to reduce the risk of further deterioration; or
    </TD>
    <TD CLASS="strcol" COLSPAN="2" >&nbsp;</TD>
  </TR>
  <TR >
    <TD CLASS="strcol" COLSPAN="2" >
      <INPUT TYPE="checkbox" NAME="ClientASAM_D3v2_1" VALUE=1 <<ClientASAM_D3v2_1=checkbox>> >
      b. The client has a diagnosed emotional, behavioral or cognitive disorder that requires intensive outpatient monitoring to minimize distractions from their treatment or recovery.
    </TD>
    <TD CLASS="strcol" COLSPAN="2" >&nbsp;</TD>
  </TR>
  <TR >
    <TD CLASS="strcol" COLSPAN="2" ><B>Dual Diagnosed Enhanced Programs</B></TD>
    <TD CLASS="strcol" COLSPAN="2" >&nbsp;</TD>
  </TR>
  <TR >
    <TD CLASS="strcol" COLSPAN="2" >The client's status in Dimension 3 is characterized by (a) or (b) or (c):</TD>
    <TD CLASS="strcol" COLSPAN="2" >&nbsp;</TD>
  </TR>
  <TR >
    <TD CLASS="strcol" COLSPAN="2" >
      <INPUT TYPE="checkbox" NAME="ClientASAM_D3v3_1" VALUE=1 <<ClientASAM_D3v3_1=checkbox>> >
      a. The client has a diagnosed emotional, behavioral or cognitive disorder that requires management because the client's history suggests a high potential for distracting him or her from treatment; such a disorder requires stabilization concurrent with addiction treatment; or
    </TD>
    <TD CLASS="strcol" COLSPAN="2" >&nbsp;</TD>
  </TR>
  <TR >
    <TD CLASS="strcol" COLSPAN="2" >
      <INPUT TYPE="checkbox" NAME="ClientASAM_D3v4_1" VALUE=1 <<ClientASAM_D3v4_1=checkbox>> >
      b. The client is assessed as at mild risk of behaviors endangering self, others or property; or
    </TD>
    <TD CLASS="strcol" COLSPAN="2" >&nbsp;</TD>
  </TR>
  <TR >
    <TD CLASS="strcol" COLSPAN="2" >
      <INPUT TYPE="checkbox" NAME="ClientASAM_D3v5_1" VALUE=1 <<ClientASAM_D3v5_1=checkbox>> >
      c. The client is at significant risk of victimization by another. However, the risk is not severe enough to require 24-hour supervision.
    </TD>
    <TD CLASS="strcol" COLSPAN="2" >&nbsp;</TD>
  </TR>
    </TABLE></TD></TR>
    <TR ><TD COLSPAN="5" ><TABLE CLASS="home fullsize" >
  <TR >
    <TD CLASS="strcol" WIDTH="15%" ROWSPAN="8" >
      Dimension 4:<BR>Readiness to Change
    </TD>
    <TD CLASS="strcol" COLSPAN="2" >
      Resistance high enough to require a structured program but not so high as to render outpatient treatment ineffective. The client's status in this dimension is characterized by one of the following:
    </TD>
    <TD CLASS="strcol" WIDTH="5%" >
      <INPUT TYPE="radio" NAME="ClientASAM_D4_1" VALUE=1 <<ClientASAM_D4_1=1>> >
    </TD>
    <TD CLASS="strcol" WIDTH="5%" >
      <INPUT TYPE="radio" NAME="ClientASAM_D4_1" VALUE=0 <<ClientASAM_D4_1=0>> >
    </TD>
  </TR>
  <TR >
    <TD CLASS="strcol" COLSPAN="2" >
      <INPUT TYPE="checkbox" NAME="ClientASAM_D4v1_1" VALUE=1 <<ClientASAM_D4v1_1=checkbox>> >
      a. The client requires structured therapy and a programmatic milieu to promote treatment progress and recovery because of failure at different levels of care. Such interventions are not likely to succeed at ASAM Level I service; or
    </TD>
    <TD CLASS="strcol" COLSPAN="2" >&nbsp;</TD>
  </TR>
  <TR >
    <TD CLASS="strcol" COLSPAN="2" >
      <INPUT TYPE="checkbox" NAME="ClientASAM_D4v2_1" VALUE=1 <<ClientASAM_D4v2_1=checkbox>> >
      b. The client's perspective inhibits his/her ability to make behavior changes without clinically-directed and repeated structured motivational interventions. Such interventions are not feasible or not likely to succeed at ASAM Level I service. The client's resistance, however, is not so high to render the treatment ineffective.
    </TD>
    <TD CLASS="strcol" COLSPAN="2" >&nbsp;</TD>
  </TR>
  <TR >
    <TD CLASS="strcol" COLSPAN="2" ><B>Dual Diagnosed Enhanced Programs</B></TD>
    <TD CLASS="strcol" COLSPAN="2" >&nbsp;</TD>
  </TR>
  <TR >
    <TD CLASS="strcol" COLSPAN="2" >The client's status in Dimension 4 is characterized by (a) or (b) or (c):</TD>
    <TD CLASS="strcol" COLSPAN="2" >&nbsp;</TD>
  </TR>
  <TR >
    <TD CLASS="strcol" COLSPAN="2" >
      <INPUT TYPE="checkbox" NAME="ClientASAM_D4v3_1" VALUE=1 <<ClientASAM_D4v3_1=checkbox>> >
      a. The client is reluctant to agree to treatment and is ambivalent about his or her commitment to change a co-occurring mental health problem; or
    </TD>
    <TD CLASS="strcol" COLSPAN="2" >&nbsp;</TD>
  </TR>
  <TR >
    <TD CLASS="strcol" COLSPAN="2" >
      <INPUT TYPE="checkbox" NAME="ClientASAM_D4v4_1" VALUE=1 <<ClientASAM_D4v4_1=checkbox>> >
      b. The client's follow through in treatment is so poor or inconsistent that Level services are not succeeding or are not feasible; or
    </TD>
    <TD CLASS="strcol" COLSPAN="2" >&nbsp;</TD>
  </TR>
  <TR >
    <TD CLASS="strcol" COLSPAN="2" >
      <INPUT TYPE="checkbox" NAME="ClientASAM_D4v5_1" VALUE=1 <<ClientASAM_D4v5_1=checkbox>> >
      c. The client is assessed as requiring intensive services to improve his or her awareness of the need to change. The client has such limited awareness of or commitment to change that he or she cannot maintain an adequate level of functioning with out Level II.1 services.
    </TD>
    <TD CLASS="strcol" COLSPAN="2" >&nbsp;</TD>
  </TR>
    </TABLE></TD></TR>
    <TR ><TD COLSPAN="5" ><TABLE CLASS="home fullsize" >
  <TR >
    <TD CLASS="strcol" WIDTH="15%" ROWSPAN="3" >
      Dimension 5:<BR>Relapse/ Continued Use Potential
    </TD>
    <TD CLASS="strcol" COLSPAN="2" >
      Despite active participation at a less intensive level of care, the client is experiencing intensification of addiction symptoms (cravings/drug seeking related behavior) and is deteriorating in his/her level of functioning despite revisions in the treatment plan.
    </TD>
    <TD CLASS="strcol" WIDTH="5%" >
      <INPUT TYPE="radio" NAME="ClientASAM_D5_1" VALUE=1 <<ClientASAM_D5_1=1>> >
    </TD>
    <TD CLASS="strcol" WIDTH="5%" >
      <INPUT TYPE="radio" NAME="ClientASAM_D5_1" VALUE=0 <<ClientASAM_D5_1=0>> >
    </TD>
  </TR>
  <TR >
    <TD CLASS="strcol" COLSPAN="2" ><B>Dual Diagnosed Enhanced Programs</B></TD>
    <TD CLASS="strcol" COLSPAN="2" >&nbsp;</TD>
  </TR>
  <TR >
    <TD CLASS="strcol" COLSPAN="2" >The client's status in Dimension 5 is characterized by psychiatric symptoms that pose a moderate risk of relapse to the alcohol, drug or psychiatric disorder. The client has impaired recognition or understanding of and difficulty in managing relapse issues and requires Level II.1 Dual Diagnosis Enhanced Program services to maintain and adequate level of functioning.</TD>
    <TD CLASS="strcol" COLSPAN="2" >&nbsp;</TD>
  </TR>
    </TABLE></TD></TR>
    <TR ><TD COLSPAN="5" ><TABLE CLASS="home fullsize" >
  <TR >
    <TD CLASS="strcol" WIDTH="15%" ROWSPAN="5" >
      Dimension 6:<BR>Recovery Environment
    </TD>
    <TD CLASS="strcol" COLSPAN="2" >
      Environment not supportive, but with structure and support the client can cope. The situation is characterized by one of the following:
    </TD>
    <TD CLASS="strcol" WIDTH="5%" >
      <INPUT TYPE="radio" NAME="ClientASAM_D6_1" VALUE=1 <<ClientASAM_D6_1=1>> >
    </TD>
    <TD CLASS="strcol" WIDTH="5%" >
      <INPUT TYPE="radio" NAME="ClientASAM_D6_1" VALUE=0 <<ClientASAM_D6_1=0>> >
    </TD>
  </TR>
  <TR >
    <TD CLASS="strcol" COLSPAN="2" >
      <INPUT TYPE="checkbox" NAME="ClientASAM_D6v1_1" VALUE=1 <<ClientASAM_D6v1_1=checkbox>> >
      a. Continued exposure to current job, school or living environment will make recovery unlikely, and the client has insufficient or severely limited resources or skills needed to maintain an adequate level of functioning without this level of service; or
    </TD>
    <TD CLASS="strcol" COLSPAN="2" >&nbsp;</TD>
  </TR>
  <TR >
    <TD CLASS="strcol" COLSPAN="2" >
      <INPUT TYPE="checkbox" NAME="ClientASAM_D6v2_1" VALUE=1 <<ClientASAM_D6v2_1=checkbox>> >
      b. The client lacks social contacts, or has inappropriate social contacts that jeopardize recovery, or has few friends or peers who do not use alcohol/drugs. The client also has insufficient or severely limited resources or skills to maintain an adequate level of functioning without this level of service.
    </TD>
    <TD CLASS="strcol" COLSPAN="2" >&nbsp;</TD>
  </TR>
  <TR >
    <TD CLASS="strcol" COLSPAN="2" ><B>Dual Diagnosed Enhanced Programs</B></TD>
    <TD CLASS="strcol" COLSPAN="2" >&nbsp;</TD>
  </TR>
  <TR >
    <TD CLASS="strcol" COLSPAN="2" >
      A living, working, social and/or community environment that is not supportive of good mental functioning characterizes the client status in Dimension 6. The client has insufficient resources and skills to deal with this situation.
    </TD>
    <TD CLASS="strcol" COLSPAN="2" >&nbsp;</TD>
  </TR>
    </TABLE></TD></TR>
    <TR ><TD COLSPAN="5" ><TABLE CLASS="home fullsize" >
  <TR ><TD CLASS="strcol" COLSPAN="5" >Recommendations/Notes:</TD></TR>
  <TR >
    <TD CLASS="strcol" COLSPAN="5" >
      <TEXTAREA NAME="ClientASAM_Notes_1" COLS="90" ROWS="8" WRAP=virtual ><<ClientASAM_Notes_1>></TEXTAREA>
    </TD>
  </TR>
    </TABLE></TD></TR>
</TABLE>
<TABLE CLASS="main fullsize" >
  <TR >
    <TD CLASS="numcol" >
      <INPUT TYPE="submit" ONCLICK="return vDELETE('Are you sure you want to delete this record?');" NAME="ClientASAM_DELETE_1=1&UpdateTables=all&misPOP=1" VALUE="Delete">
      <INPUT TYPE="submit" ONCLICK="return validate(this.form);" NAME="UpdateTables=all&misPOP=1" VALUE="Add/Update">
    </TD>
  </TR>
</TABLE>

<INPUT TYPE="hidden" NAME="ClientASAM_AdultChild_1" VALUE="ADULT" >
<INPUT TYPE="hidden" NAME="ClientASAM_Type_1" VALUE="ADM" >
<INPUT TYPE="hidden" NAME="ClientASAM_Level_1" VALUE="2.1" >
</LOADHIDDEN>
</FORM>
<SCRIPT LANGUAGE="JavaScript">
document.ASAM.elements[0].focus();
</SCRIPT>

[[myHTML->rightpane(%form+search)]]
