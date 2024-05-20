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
      <BR>ASAM PPC-2 65D-30 (Child)
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
  <TR ><TD CLASS="port hdrtxt" COLSPAN="5" >Child 65D-30 Outpatient ASAM Level I</TD></TR>
    <TR ><TD COLSPAN="5" ><TABLE CLASS="home fullsize" >
  <TR >
    <TD CLASS="strcol" >Transfer</TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="radio" NAME="ClientASAM_Transfer_1" VALUE=1 <<ClientASAM_Transfer_1=1>> > Yes
      <INPUT TYPE="radio" NAME="ClientASAM_Transfer_1" VALUE=0 <<ClientASAM_Transfer_1=0>> > No
    </TD>
  </TR>
  <TR >
    <TD CLASS="strcol" >To Level</TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="text" NAME="ClientASAM_ToLevel_1" VALUE="<<ClientASAM_ToLevel_1>>" ONFOCUS="select()" MAXLENGTH="3" SIZE="3" >
    </TD>
  </TR>
    </TABLE></TD></TR>
    <TR ><TD COLSPAN="5" ><TABLE CLASS="home fullsize" >
  <TR >
    <TD CLASS="strcol" WIDTH="15%" >DIMENSIONS</TD>
    <TD CLASS="strcol" >DISCHARGE CRITERIA</TD>
    <TD CLASS="strcol" >
Check all items in each dimension that apply to the client. Place a check in the appropriate box that indicates validation of lack of validation for discharge or transfer from this level of care.
    </TD>
    <TD CLASS="strcol" style='vertical-align: bottom' WIDTH="5%" >YES</TD>
    <TD CLASS="strcol" style='vertical-align: bottom' WIDTH="5%" >NO</TD>
  </TR>
    </TABLE></TD></TR>
    <TR ><TD COLSPAN="5" ><TABLE CLASS="home fullsize" >
  <TR >
    <TD CLASS="strcol" WIDTH="15%" >ASAM Requirements</TD>
    <TD CLASS="strcol" COLSPAN="2" >
      Meets criteria in one of the six dimensions unless discharged for lack of diagnostic criteria.
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
      b. The client exhibits symptoms of severe intoxication and/or withdrawal, which cannot be safely managed at this level of care.
    </TD>
    <TD CLASS="strcol" COPSPAN="2" >&nbsp;</TD>
  </TR>
    </TABLE></TD></TR>
    <TR ><TD COLSPAN="5" ><TABLE CLASS="home fullsize" >
  <TR >
    <TD CLASS="strcol" WIDTH="15%" ROWSPAN="3" >
      Dimension 2:<BR>Biomedical Conditions and Complications
    </TD>
    <TD CLASS="strcol" COLSPAN="2" >
     The client's status in this dimension is characterized by one of the following:
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
      a. The client’s biomedical conditions, if any, have diminished or stabilized to the extent they can be managed through outpatient appointments at the client’s discretion, and the client does not meet any of the continued stay criteria in this or another dimension that indicates the need for further treatment in ASAM Level I; or
    </TD>
    <TD CLASS="strcol" COLSPAN="2" >&nbsp;</TD>
  </TR>
  <TR >
    <TD CLASS="strcol" COLSPAN="2" >
      <INPUT TYPE="checkbox" NAME="ClientASAM_D2v2_1" VALUE=1 <<ClientASAM_D2v2_1=checkbox>> >
      b. The client has a biomedical condition that is interfering with treatment and that requires treatment in another setting.
    </TD>
    <TD CLASS="strcol" COPSPAN="2" >&nbsp;</TD>
  </TR>
    </TABLE></TD></TR>
    <TR ><TD COLSPAN="5" ><TABLE CLASS="home fullsize" >
  <TR >
    <TD CLASS="strcol" WIDTH="15%" ROWSPAN="3" >
      Dimension 3:<BR>Emotional, Behavioral or Cognitive Conditions and Complications
    </TD>
    <TD CLASS="strcol" COLSPAN="2" >
      The client's status in this dimension is characterized by one of the following:
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
      a. The client’s emotional, behavioral or cognitive conditions, if any, have diminished or stabilized to the extent they can be managed through outpatient appointments at the client’s discretion, and the client does not meet any of the continued stay criteria in this or another dimension that indicates the need for further treatment in ASAM Level I; or
    </TD>
    <TD CLASS="strcol" COLSPAN="2" >&nbsp;</TD>
  </TR>
  <TR >
    <TD CLASS="strcol" COLSPAN="2" >
      <INPUT TYPE="checkbox" NAME="ClientASAM_D3v2_1" VALUE=1 <<ClientASAM_D3v2_1=checkbox>> >
      b. The client has a psychiatric or emotional, behavioral or cognitive condition that is interfering with treatment and that requires additional treatment in another setting.
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
      The client's status in this dimension is characterized by one of the following:
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
      a. The client’s awareness and acceptance of his/her addiction problem and commitment to recovery is sufficient to expect maintenance of a self-directed aftercare plan, based on the following evidence: 1) the client recognizes the severity of the substance abuse problem; 2) the client has an understanding of the self-defeating relationship with substances; 3) the client is applying the skills necessary to maintain sobriety in a mutual self-help group and/or with post-treatment support care; and 4) the client does not meet any of the continued stay criteria in this or another dimension that indicates the need for further treatment in ASAM Level I; or
    </TD>
    <TD CLASS="strcol" COLSPAN="2" >&nbsp;</TD>
  </TR>
  <TR >
    <TD CLASS="strcol" COLSPAN="2" >
      <INPUT TYPE="checkbox" NAME="ClientASAM_D4v2_1" VALUE=1 <<ClientASAM_D4v2_1=checkbox>> >
      b. The client is experiencing escalation in drug seeking behaviors or craving that necessitates treatment in a more intensive level of care.
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
      The client's status in this dimension is characterized by one of the following:
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
      a. The client’s therapeutic gains in addressing craving and relapse issues have been internalized and integrated so the client does not meet any of the ASAM Level I continued stay criteria in this or another dimension that indicates the need for further treatment in ASAM Level I; or
    </TD>
    <TD CLASS="strcol" COLSPAN="2" >&nbsp;</TD>
  </TR>
  <TR >
    <TD CLASS="strcol" COLSPAN="2" >
      <INPUT TYPE="checkbox" NAME="ClientASAM_D5v2_1" VALUE=1 <<ClientASAM_D5v2_1=checkbox>> >
      b. The client is experiencing a worsening of drug-seeking behaviors or craving, requiring treatment in a more intensive level of care.
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
      a. The client’s social system and significant others are supportive of recovery to an extent that the client can adhere to a self-directed treatment plan without substantial risk of relapse/continued use and the client does not meet any of the continued stay criteria in this or another dimension that indicates the need for further treatment at ASAM Level I; or
    </TD>
    <TD CLASS="strcol" COLSPAN="2" >&nbsp;</TD>
  </TR>
  <TR >
    <TD CLASS="strcol" COLSPAN="2" >
      <INPUT TYPE="checkbox" NAME="ClientASAM_D6v2_1" VALUE=1 <<ClientASAM_D6v2_1=checkbox>> >
      b. The client is functioning adequately in assessed areas of deficiency in life tasks including school, work, social functioning or primary relationships and the client does not meet any of the continued stay criteria in this or another dimension that indicates the need for further treatment at ASAM Level I; or
    </TD>
    <TD CLASS="strcol" COLSPAN="2" >&nbsp;</TD>
  </TR>
  <TR >
    <TD CLASS="strcol" COLSPAN="2" >
      <INPUT TYPE="checkbox" NAME="ClientASAM_D6v3_1" VALUE=1 <<ClientASAM_D6v3_1=checkbox>> >
      c. The client’s social system remains non-supportive or has deteriorated. The client is having difficulty in coping with this environment and is at substantial risk of relapse and requires placement in a more intensive level of care.
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

<INPUT TYPE="hidden" NAME="ClientASAM_AdultChild_1" VALUE="CHILD" >
<INPUT TYPE="hidden" NAME="ClientASAM_Type_1" VALUE="DIS" >
<INPUT TYPE="hidden" NAME="ClientASAM_Level_1" VALUE="1" >
</LOADHIDDEN>
</FORM>
<SCRIPT LANGUAGE="JavaScript">
document.ASAM.elements[0].focus();
</SCRIPT>

[[myHTML->rightpane(%form+search)]]
