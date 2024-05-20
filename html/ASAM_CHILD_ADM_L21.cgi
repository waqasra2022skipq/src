[[myHTML->newHTML(%form+American Society of Addiction Medicine)]]

<SCRIPT LANGUAGE="JavaScript" SRC="/cgi/js/NoEnter.js"> </SCRIPT>
<SCRIPT LANGUAGE="JavaScript" SRC="/cgi/js/vEntry.js"> </SCRIPT>
<SCRIPT LANGUAGE="JavaScript" SRC="/cgi/js/vClientASAM.js"> </SCRIPT>
<SCRIPT LANGUAGE="JavaScript" SRC="/cgi/js/vNum.js"> </SCRIPT>
<SCRIPT LANGUAGE="JavaScript" SRC="/cgi/js/vDate.js"> </SCRIPT>

<FORM NAME="ASAM" ACTION="/cgi/bin/mis.cgi" METHOD="POST" >
<TABLE CLASS="main fullsize" >
  <TR >
    <TD CLASS="strcol" >
      <<<Client_FName_1>>> <<<Client_MName_1>>> <<<Client_LName_1>>> (<<<Client_ClientID_1>>>) <<<Client_SSN_1>>>
      <BR>ASAM PPC-2 65D-30 (Adolescent)
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
  <TR ><TD CLASS="port hdrtxt" COLSPAN="5" >Adolescent 65D-30 Intensive Outpatient ASAM Level II.1</TD></TR>
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
      Must meet Dimension 1 and 2, and at least one of Dimensions 3, 4, 5, or 6. Transfer criteria: Clients may be transferred to this level of care when they have met essential treatment objectives in a more intensive level and require this intensity of service provided at this level of care in at least one dimension. A client may transfer from ASAM Level I when services at that level have been insufficient to address the client's needs or when ASAM Level I has consisted of motivational interventions to prepare the client for participation in a more intensive level of care for which admission criteria are met.
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
    <TD CLASS="strcol" WIDTH="15%" ROWSPAN="4" >
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
      b. The client's intoxication or withdrawal risks symptoms/risks can be managed at this level of care.
    </TD>
    <TD CLASS="strcol" COLSPAN="2" >&nbsp;</TD>
  </TR>
  <TR >
    <TD CLASS="strcol" COLSPAN="2" >
      <INPUT TYPE="checkbox" NAME="ClientASAM_D1v3_1" VALUE=1 <<ClientASAM_D1v3_1=checkbox>> >
      c. The client has made a commitment to sustain treatment and to follow treatment recommendations or has external supports that promote engagement in treatment.
    </TD>
    <TD CLASS="strcol" COLSPAN="2" >&nbsp;</TD>
  </TR>
    </TABLE></TD></TR>
    <TR ><TD COLSPAN="5" ><TABLE CLASS="home fullsize" >
  <TR >
    <TD CLASS="strcol" WIDTH="15%" ROWSPAN="3" >
      Dimension 2:<BR>Biomedical Conditions and Complications
    </TD>
    <TD CLASS="strcol" COLSPAN="2" >
      None or not a distraction from treatment and manageable in ASAM Level II. The client's status in this dimension is characterized by one of the following:
    </TD>
    <TD CLASS="strcol" WIDTH="5%" >
      <INPUT TYPE="radio" NAME="ClientASAM_D2_1" VALUE=1 <<ClientASAM_D2_1=1>> >
    </TD>
    <TD CLASS="strcol" WIDTH="5%" >
      <INPUT TYPE="radio" NAME="ClientASAM_D2_1" VALUE=0 <<ClientASAM_D2_1=0>> >
    </TD>
  </TR>
  <TR >
    <TD CLASS="strcol" COLSPAN="2" >
      <INPUT TYPE="checkbox" NAME="ClientASAM_D2v1_1" VALUE=1 <<ClientASAM_D2v1_1=checkbox>> >
      a. The client's biomedical conditions, if any, are stable or are being concurrently addressed and will not interfere with treatment at this level of care; or
    </TD>
    <TD CLASS="strcol" COLSPAN="2" >&nbsp;</TD>
  </TR>
  <TR >
    <TD CLASS="strcol" COLSPAN="2" >
      <INPUT TYPE="checkbox" NAME="ClientASAM_D2v2_1" VALUE=1 <<ClientASAM_D2v2_1=checkbox>> >
      b. The client's biomedical conditions are not severe enough to warrant inpatient treatment but are sufficient to distract from recovery efforts. Such conditions require medical monitoring and/or medical management, which can be provided by the intensive outpatient program or through a concurrent arrangement with another treatment provider.
    </TD>
    <TD CLASS="strcol" COLSPAN="2" >&nbsp;</TD>
  </TR>
    </TABLE></TD></TR>
    <TR ><TD COLSPAN="5" ><TABLE CLASS="home fullsize" >
  <TR >
    <TD CLASS="strcol" WIDTH="15%" ROWSPAN="6" >
      Dimension 3:<BR>Emotional, Behavioral or Cognitive Conditions and Complications
    </TD>
    <TD CLASS="strcol" COLSPAN="2" >
      The client's status in Dimension 3 is characterize by at least one of the following:
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
      a. Dangerous Lethality: The client is at mild risk of behaviors endangering self, others or property and requires frequent monitoring to assure that there is a reasonable likelihood of safety between IOP sessions. However, his or her condition is not so severe as to require daily supervision;`
    </TD>
    <TD CLASS="strcol" COLSPAN="2" >&nbsp;</TD>
  </TR>
  <TR >
    <TD CLASS="strcol" COLSPAN="2" >
      <INPUT TYPE="checkbox" NAME="ClientASAM_D3v2_1" VALUE=1 <<ClientASAM_D3v2_1=checkbox>> >
      b. Interference with Addiction Recovery Efforts: The client's recovery efforts are negatively affected by an emotional, behavioral or cognitive problem, which causes mild interference with and requires increased intensity to support treatment participation and/or compliance;
    </TD>
    <TD CLASS="strcol" COLSPAN="2" >&nbsp;</TD>
  </TR>
  <TR >
    <TD CLASS="strcol" COLSPAN="2" >
      <INPUT TYPE="checkbox" NAME="ClientASAM_D3v3_1" VALUE=1 <<ClientASAM_D3v3_1=checkbox>> >
      c. Social Functioning: The client symptoms are causing mild to moderate difficulty in social functioning, but not to such a degree that he or she is unable to manage the activities of daily living or to fulfill responsibilities at home, school, work or community;
    </TD>
    <TD CLASS="strcol" COLSPAN="2" >&nbsp;</TD>
  </TR>
  <TR >
    <TD CLASS="strcol" COLSPAN="2" >
      <INPUT TYPE="checkbox" NAME="ClientASAM_D3v4_1" VALUE=1 <<ClientASAM_D3v4_1=checkbox>> >
      d. Ability for Self-Care: The client is experiencing mild to moderate impairment in ability to manage the activities of daily living, and thus requires frequent monitoring and treatment interventions. Problems may involve poor hygiene secondary to exacerbation of a chronic mental illness. Poor self-care or lack of independent living skills in an older client who is transitioning to adulthood, or in a younger adolescent who lacks adequate family supports;
    </TD>
    <TD CLASS="strcol" COLSPAN="2" >&nbsp;</TD>
  </TR>
  <TR >
    <TD CLASS="strcol" COLSPAN="2" >
      <INPUT TYPE="checkbox" NAME="ClientASAM_D3v5_1" VALUE=1 <<ClientASAM_D3v5_1=checkbox>> >
      e. Course of Illness: The client's history and present situation suggest that an emotional, behavioral or cognitive condition would become unstable without frequent monitoring and maintenance.
    </TD>
    <TD CLASS="strcol" COLSPAN="2" >&nbsp;</TD>
  </TR>
    </TABLE></TD></TR>
    <TR ><TD COLSPAN="5" ><TABLE CLASS="home fullsize" >
  <TR >
    <TD CLASS="strcol" WIDTH="15%" ROWSPAN="3" >
      Dimension 4:<BR>Readiness to Change
    </TD>
    <TD CLASS="strcol" COLSPAN="2" >
      The client status in Dimension 4 is characterized by (a) or (b):
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
      a. The client requires structured therapy and a programmatic milieu to promote progress through the stages of change, as evidenced by behaviors such as the following: [1] the adolescent is verbally compliant, but does not demonstrate consistent behaviors; [2] the client is only passively involved in treatment; or [3] the client demonstrates variable compliance with attendance at outpatient sessions or self- or mutual-help meetings or support groups. Such interventions are not feasible or are not likely to succeed in a level I services; or
    </TD>
    <TD CLASS="strcol" COLSPAN="2" >&nbsp;</TD>
  </TR>
  <TR >
    <TD CLASS="strcol" COLSPAN="2" >
      <INPUT TYPE="checkbox" NAME="ClientASAM_D4v2_1" VALUE=1 <<ClientASAM_D4v2_1=checkbox>> >
      b. The client's perspective inhibits his or her ability to make progress through the stages of change. The client thus requires structured therapy and a programmatic milieu. Such interventions are not feasible or are not likely to succeed in a Level II.1 service.
    </TD>
    <TD CLASS="strcol" COLSPAN="2" >&nbsp;</TD>
  </TR>
    </TABLE></TD></TR>
    <TR ><TD COLSPAN="5" ><TABLE CLASS="home fullsize" >
  <TR >
    <TD CLASS="strcol" WIDTH="15%" ROWSPAN="4" >
      Dimension 5:<BR>Relapse/ Continued Use Potential
    </TD>
    <TD CLASS="strcol" COLSPAN="2" >
      The client status in Dimension 5 is characterized by one of the following:
    </TD>
    <TD CLASS="strcol" WIDTH="5%" >
      <INPUT TYPE="radio" NAME="ClientASAM_D5_1" VALUE=1 <<ClientASAM_D5_1=1>> >
    </TD>
    <TD CLASS="strcol" WIDTH="5%" >
      <INPUT TYPE="radio" NAME="ClientASAM_D5_1" VALUE=0 <<ClientASAM_D5_1=0>> >
    </TD>
  </TR>
  <TR >
    <TD CLASS="strcol" COLSPAN="2" >
      <INPUT TYPE="checkbox" NAME="ClientASAM_D5v1_1" VALUE=1 <<ClientASAM_D5v1_1=checkbox>> >
      a. There is a high likelihood of alcohol or drug use without close outpatient monitoring and structured support, as indicated by the client's lack of awareness of relapse triggers, difficulty in postponing immediate gratification, and/or ambivalence/resistance to treatment; or
    </TD>
    <TD CLASS="strcol" COLSPAN="2" >&nbsp;</TD>
  </TR>
  <TR >
    <TD CLASS="strcol" COLSPAN="2" >
      <INPUT TYPE="checkbox" NAME="ClientASAM_D5v2_1" VALUE=1 <<ClientASAM_D5v2_1=checkbox>> >
      b. The client is assessed as being unable to interrupt his or her impulsive and self-defeating behaviors, which threaten abstinence in the absence of ongoing clinical support; or
    </TD>
    <TD CLASS="strcol" COLSPAN="2" >&nbsp;</TD>
  </TR>
  <TR >
    <TD CLASS="strcol" COLSPAN="2" >
      <INPUT TYPE="checkbox" NAME="ClientASAM_D5v3_1" VALUE=1 <<ClientASAM_D5v3_1=checkbox>> >
      c. Despite active participation in treatment, the client is experiencing an intensification of addiction symptoms (such as craving and drug seeking behavior) with associated moderate risk of relapse.
    </TD>
    <TD CLASS="strcol" COLSPAN="2" >&nbsp;</TD>
  </TR>
    </TABLE></TD></TR>
    <TR ><TD COLSPAN="5" ><TABLE CLASS="home fullsize" >
  <TR >
    <TD CLASS="strcol" WIDTH="15%" ROWSPAN="4" >
      Dimension 6:<BR>Recovery Environment
    </TD>
    <TD CLASS="strcol" COLSPAN="2" >
      The client's status in this dimension is characterized by one of the following:
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
      b. The client lacks social contacts, or has inappropriate social contacts that jeopardize recovery, or has few friends or peers who do not use alcohol or other drugs. He or she also has insufficient resources or skills necessary to maintain an adequate level of functioning without the services of a level II.1 program, but is capable of maintaining an adequate level of functioning between sessions; or
    </TD>
    <TD CLASS="strcol" COLSPAN="2" >&nbsp;</TD>
  </TR>
  <TR >
    <TD CLASS="strcol" COLSPAN="2" >
      <INPUT TYPE="checkbox" NAME="ClientASAM_D6v3_1" VALUE=1 <<ClientASAM_D6v3_1=checkbox>> >
      c. The client family is supportive of recovery but family conflicts and related family dysfunction impedes the client's ability to learn the skills necessary to achieve and maintain abstinence.
    </TD>
    <TD CLASS="strcol" COLSPAN="2" >&nbsp;</TD>
  </TR>
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

<INPUT TYPE="hidden" NAME="ClientASAM_AdultChild_1" VALUE="CHILD" >
<INPUT TYPE="hidden" NAME="ClientASAM_Type_1" VALUE="ADM" >
<INPUT TYPE="hidden" NAME="ClientASAM_Level_1" VALUE="2.1" >
</LOADHIDDEN>
</FORM>
<SCRIPT LANGUAGE="JavaScript">
document.ASAM.elements[0].focus();
</SCRIPT>

[[myHTML->rightpane(%form+search)]]
