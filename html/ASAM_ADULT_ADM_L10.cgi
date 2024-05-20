[[myHTML->newHTML(%form+American Society of Addiction Medicine)]]

<SCRIPT LANGUAGE="JavaScript" SRC="/cgi/js/NoEnter.js"> </SCRIPT>
<SCRIPT LANGUAGE="JavaScript" SRC="/cgi/js/vEntry.js"> </SCRIPT>
<SCRIPT LANGUAGE="JavaScript" SRC="/cgi/js/vClientASAM.js"> </SCRIPT>
<SCRIPT LANGUAGE="JavaScript" SRC="/cgi/js/vNum.js"> </SCRIPT>
<SCRIPT LANGUAGE="JavaScript" SRC="/cgi/js/vDate.js"> </SCRIPT>

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
  <TR ><TD CLASS="port hdrtxt" COLSPAN="5" >Adult 65D-30 Outpatient ASAM Level I</TD></TR>
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
      Meets criteria in all six dimensions.
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
      The client's status in this dimension is characterized by one of the following:
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
      None or very stable - The client's biomedical conditions, if any, are stable enough to participate in outpatient treatment.
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
      None or very stable - The situation is characterized by all of the following:
    </TD>
    <TD CLASS="strcol" WIDTH="5%" >
      <INPUT TYPE="radio" NAME="ClientASAM_D3_1" VALUE=1 <<ClientASAM_D3_1=1>> >
    </TD>
    <TD CLASS="strcol" WIDTH="5%" >
      <INPUT TYPE="radio" NAME="ClientASAM_D3_1" VALUE=0 <<ClientASAM_D3_1=0>> >
    </TD>
  </TR>
  <TR >
    <TD CLASS="strcol" COLSPAN="2" >
      <INPUT TYPE="checkbox" NAME="ClientASAM_D3v1_1" VALUE=1 <<ClientASAM_D3v1_1=checkbox>> >
      a. The client's anxiety, guilt and/or depression, if present, appear to be related to substance-related problems rather than to a coexisting psychiatric/emotional/behavioral or cognitive condition. If they are related to such a condition, appropriate care is being provided concurrent with ASAM Level I; and
    </TD>
    <TD CLASS="strcol" COLSPAN="2" >&nbsp;</TD>
  </TR>
  <TR >
    <TD CLASS="strcol" COLSPAN="2" >
      <INPUT TYPE="checkbox" NAME="ClientASAM_D3v2_1" VALUE=1 <<ClientASAM_D3v2_1=checkbox>> >
      b. The client's mental status does not preclude his/her ability to understand the materials presented or to participate in the treatment process; and
    </TD>
    <TD CLASS="strcol" COLSPAN="2" >&nbsp;</TD>
  </TR>
  <TR >
    <TD CLASS="strcol" COLSPAN="2" >
      <INPUT TYPE="checkbox" NAME="ClientASAM_D3v3_1" VALUE=1 <<ClientASAM_D3v3_1=checkbox>> >
      c. The client is assessed as not posing a risk of harm to self or others.
    </TD>
    <TD CLASS="strcol" COLSPAN="2" >&nbsp;</TD>
  </TR>
  <TR >
    <TD CLASS="strcol" COLSPAN="2" ><B>Dual Diagnosed Enhanced Programs</B></TD>
    <TD CLASS="strcol" COLSPAN="2" >&nbsp;</TD>
  </TR>
  <TR >
    <TD CLASS="strcol" COLSPAN="2" >In addition to the foregoing criteria, either (a) or (b) and (c) and (d) characterize the client's status in Dimension 3.</TD>
    <TD CLASS="strcol" COLSPAN="2" >&nbsp;</TD>
  </TR>
  <TR >
    <TD CLASS="strcol" COLSPAN="2" >
      <INPUT TYPE="checkbox" NAME="ClientASAM_D3v4_1" VALUE=1 <<ClientASAM_D3v4_1=checkbox>> >
      a. The client has a severe and persistent mental illness that impairs his or her ability to follow through consistently with mental health appointments and psychotropic medication. The client maintains the ability to access service such as assertive community treatment and intensive case management or supportive living designed to help the client remain engaged in treatment; or
    </TD>
    <TD CLASS="strcol" COLSPAN="2" >&nbsp;</TD>
  </TR>
  <TR >
    <TD CLASS="strcol" COLSPAN="2" >
      <INPUT TYPE="checkbox" NAME="ClientASAM_D3v5_1" VALUE=1 <<ClientASAM_D3v5_1=checkbox>> >
      b. The client has a severe and persistent mental disorder or other emotional, behavioral or cognitive problems, or substanceinduced disorder; and
    </TD>
    <TD CLASS="strcol" COLSPAN="2" >&nbsp;</TD>
  </TR>
  <TR >
    <TD CLASS="strcol" COLSPAN="2" >
      <INPUT TYPE="checkbox" NAME="ClientASAM_D3v6_1" VALUE=1 <<ClientASAM_D3v6_1=checkbox>> >
      c. The client's mental health functioning is such that he or she has impaired ability to: [1] understand the information presented, and [2] participate in treatment planning and the treatment process. Mental health management is required to stabilize mood, cognition and behavior; and
    </TD>
    <TD CLASS="strcol" COLSPAN="2" >&nbsp;</TD>
  </TR>
  <TR >
    <TD CLASS="strcol" COLSPAN="2" >
      <INPUT TYPE="checkbox" NAME="ClientASAM_D3v7_1" VALUE=1 <<ClientASAM_D3v7_1=checkbox>> >
      d. The client is assessed as not posing a risk of harm to self or others and is not vulnerable to victimization by another.
    </TD>
    <TD CLASS="strcol" COLSPAN="2" >&nbsp;</TD>
  </TR>
    </TABLE></TD></TR>
    <TR ><TD COLSPAN="5" ><TABLE CLASS="home fullsize" >
  <TR >
    <TD CLASS="strcol" WIDTH="15%" ROWSPAN="5" >
      Dimension 4:<BR>Readiness to Change
    </TD>
    <TD CLASS="strcol" COLSPAN="2" >
      The situation is characterized by (a) and (b) or (c) or (d):
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
      a. The client wants to adhere to the treatment plan and attend all scheduled activities; and
    </TD>
    <TD CLASS="strcol" COLSPAN="2" >&nbsp;</TD>
  </TR>
  <TR >
    <TD CLASS="strcol" COLSPAN="2" >
      <INPUT TYPE="checkbox" NAME="ClientASAM_D4v2_1" VALUE=1 <<ClientASAM_D4v2_1=checkbox>> >
      b. The client admits to a substance abuse and/or a mental health problem but requires monitoring and motivating strategies. A structured residential program is not required; or
    </TD>
    <TD CLASS="strcol" COLSPAN="2" >&nbsp;</TD>
  </TR>
  <TR >
    <TD CLASS="strcol" COLSPAN="2" >
      <INPUT TYPE="checkbox" NAME="ClientASAM_D4v3_1" VALUE=1 <<ClientASAM_D4v3_1=checkbox>> >
      c. The client is ambivalent about or does not recognize that he or she has a substance related and/or mental health problem; or
    </TD>
    <TD CLASS="strcol" COLSPAN="2" >&nbsp;</TD>
  </TR>
  <TR >
    <TD CLASS="strcol" COLSPAN="2" >
      <INPUT TYPE="checkbox" NAME="ClientASAM_D4v4_1" VALUE=1 <<ClientASAM_D4v4_1=checkbox>> >
      d. The client may not recognize that they have a substance-related and/or mental health problem. They may require monitoring and motivating strategies to engage in treatment and to progress through the stages of change.
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
      Able to maintain abstinence and pursue recovery goals with minimal support - The client is assessed as being able to achieve or maintain abstinence and recovery goals only with support and scheduled counseling to assist in dealing with issues that include mental preoccupation with alcohol or other drugs, craving, peer pressure, lifestyle, attitude changes and other treatment plans issues.
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
    <TD CLASS="strcol" COLSPAN="2" >In addition to the criteria listed above, the client is assessed as able to achieve or maintain mental health functioning and related goals only with support and scheduled therapeutic contact to assist him or her in dealing with issues that include (but are not limited to) impulses to harm self or others and difficulty in coping with his or her affects, impulses or cognition.</TD>
    <TD CLASS="strcol" COLSPAN="2" >&nbsp;</TD>
  </TR>
    </TABLE></TD></TR>
    <TR ><TD COLSPAN="5" ><TABLE CLASS="home fullsize" >
  <TR >
    <TD CLASS="strcol" WIDTH="15%" ROWSPAN="9" >
      Dimension 6:<BR>Recovery Environment
    </TD>
    <TD CLASS="strcol" COLSPAN="2" >
      The situation is characterized by one of the following:
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
      a. A sufficiently supportive psychosocial environment makes outpatient treatment feasible; or
    </TD>
    <TD CLASS="strcol" COLSPAN="2" >&nbsp;</TD>
  </TR>
  <TR >
    <TD CLASS="strcol" COLSPAN="2" >
      <INPUT TYPE="checkbox" NAME="ClientASAM_D6v2_1" VALUE=1 <<ClientASAM_D6v2_1=checkbox>> >
      b. Although the client does not have an ideal primary or social support system to assist with sobriety, he or she has demonstrated motivation and willingness to obtain such a support system; or
    </TD>
    <TD CLASS="strcol" COLSPAN="2" >&nbsp;</TD>
  </TR>
  <TR >
    <TD CLASS="strcol" COLSPAN="2" >
      <INPUT TYPE="checkbox" NAME="ClientASAM_D6v3_1" VALUE=1 <<ClientASAM_D6v3_1=checkbox>> >
      c. Family and significant others are supportive but require professional interventions to improve the client's chance of treatment success and recovery.
    </TD>
    <TD CLASS="strcol" COLSPAN="2" >&nbsp;</TD>
  </TR>
  <TR >
    <TD CLASS="strcol" COLSPAN="2" ><B>Dual Diagnosed Enhanced Programs</B></TD>
    <TD CLASS="strcol" COLSPAN="2" >&nbsp;</TD>
  </TR>
  <TR >
    <TD CLASS="strcol" COLSPAN="2" >In addition to the criteria listed above, (a) or (b) or (c) characterizes the client's status in Dimension 6.</TD>
    <TD CLASS="strcol" COLSPAN="2" >&nbsp;</TD>
  </TR>
  <TR >
    <TD CLASS="strcol" COLSPAN="2" >
      <INPUT TYPE="checkbox" NAME="ClientASAM_D6v4_1" VALUE=1 <<ClientASAM_D6v4_1=checkbox>> >
      a. The client does not have an adequate primary or social support system and has mild impairment in his or her ability to obtain a support system; or
    </TD>
    <TD CLASS="strcol" COLSPAN="2" >&nbsp;</TD>
  </TR>
  <TR >
    <TD CLASS="strcol" COLSPAN="2" >
      <INPUT TYPE="checkbox" NAME="ClientASAM_D6v5_1" VALUE=1 <<ClientASAM_D6v5_1=checkbox>> >
      b. The family guardian or significant others require active family therapy or systems interventions to improve the client's chances of treatment success and recovery; or
    </TD>
    <TD CLASS="strcol" COLSPAN="2" >&nbsp;</TD>
  </TR>
  <TR >
    <TD CLASS="strcol" COLSPAN="2" >
      <INPUT TYPE="checkbox" NAME="ClientASAM_D6v6_1" VALUE=1 <<ClientASAM_D6v6_1=checkbox>> >
      c. The client's status in Dimension 6 is characterized by all of the following: (1) the client has a severe and persistent mental disorder or emotional, behavioral or cognitive problem, and (2) the client does not have an adequate family or social support system, and (3) the client is chronically impaired, however, not in imminent danger, had limited ability to establish a supportive recovery environment. (The client however, does not have access to intensive outreach and case management services that can provide structure and allow him or her to work toward stabilizing both the substance and mental health related disorders). The client does however, have access to intensive outreach and case management services that can provide structure and allow them to work toward stabilizing both the substance related and mental disorders.
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
<INPUT TYPE="hidden" NAME="ClientASAM_Level_1" VALUE="1" >
</LOADHIDDEN>
</FORM>
<SCRIPT LANGUAGE="JavaScript">
document.ASAM.elements[0].focus();
</SCRIPT>

[[myHTML->rightpane(%form+search)]]
