[[myHTML->newHTML(%form+American Society of Addiction Medicine)]]

<SCRIPT LANGUAGE="JavaScript" SRC="/src/cgi/js/NoEnter.js"> </SCRIPT>
<SCRIPT LANGUAGE="JavaScript" SRC="/src/cgi/js/vEntry.js"> </SCRIPT>
<SCRIPT LANGUAGE="JavaScript" SRC="/src/cgi/js/vClientASAM.js"> </SCRIPT>
<SCRIPT LANGUAGE="JavaScript" SRC="/src/cgi/js/vNum.js"> </SCRIPT>
<SCRIPT LANGUAGE="JavaScript" SRC="/src/cgi/js/vDate.js"> </SCRIPT>

<FORM NAME="ASAM" ACTION="/src/cgi/bin/mis.cgi" METHOD="POST" >
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
  <TR ><TD CLASS="port hdrtxt" COLSPAN="5" >Adult 65D-30 Outpatient ASAM Level .05</TD></TR>
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
      Discharge from this level of care requires that the client meet the criteria in one of the six dimensions.
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
      a. The client has a condition in Dimension 2 that precludes continued participation in this level of care and requires transfer to another level; or
    </TD>
    <TD CLASS="strcol" COLSPAN="2" >&nbsp;</TD>
  </TR>
  <TR >
    <TD CLASS="strcol" COLSPAN="2" >
      <INPUT TYPE="checkbox" NAME="ClientASAM_D2v2_1" VALUE=1 <<ClientASAM_D2v2_1=checkbox>> >
      b. The client has no biomedical conditions or they are stable.
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
      a. The client has a condition in Dimension 3 that precludes continued participation in this level of care and requires transfer to another level; or
    </TD>
    <TD CLASS="strcol" COLSPAN="2" >&nbsp;</TD>
  </TR>
  <TR >
    <TD CLASS="strcol" COLSPAN="2" >
      <INPUT TYPE="checkbox" NAME="ClientASAM_D3v2_1" VALUE=1 <<ClientASAM_D3v2_1=checkbox>> >
      b. The client has no emotional, behavioral or cognitive conditions or they are stable and are being actively addressed.
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
      a. The client has remained stable in Dimension 4 and does not meet any other criteria that indicates the need for continued service at this level of care; or
    </TD>
    <TD CLASS="strcol" COLSPAN="2" >&nbsp;</TD>
  </TR>
  <TR >
    <TD CLASS="strcol" COLSPAN="2" >
      <INPUT TYPE="checkbox" NAME="ClientASAM_D4v2_1" VALUE=1 <<ClientASAM_D4v2_1=checkbox>> >
      b. The client is no longer willing to examine personal substance use patterns, despite program efforts, and a recommendation is being made for further assessment and follow-up.
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
      a. The client has demonstrated the personal skills necessary to make responsible choices about alcohol/other drug use, and does not meet criteria indicating the need for continued service at this level of care; or
    </TD>
    <TD CLASS="strcol" COLSPAN="2" >&nbsp;</TD>
  </TR>
  <TR >
    <TD CLASS="strcol" COLSPAN="2" >
      <INPUT TYPE="checkbox" NAME="ClientASAM_D5v2_1" VALUE=1 <<ClientASAM_D5v2_1=checkbox>> >
      b. The client has not integrated the skills necessary to avoid harmful or inappropriate substance use, despite professional interventions, and a recommendation is being made for further assessment and follow-up.
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
      a. The client has resolved problems in his/her living environment or demonstrates the needed coping skills necessary to achieve personal goals and does not meet criteria indicating a need for continued service at this level of care; or
    </TD>
    <TD CLASS="strcol" COLSPAN="2" >&nbsp;</TD>
  </TR>
  <TR >
    <TD CLASS="strcol" COLSPAN="2" >
      <INPUT TYPE="checkbox" NAME="ClientASAM_D6v2_1" VALUE=1 <<ClientASAM_D6v2_1=checkbox>> >
      b. The client no longer is willing to examine problems in his/her living environment, despite program efforts. Since these problems persist, a recommendation is being made for appropriate living and support services.
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
<INPUT TYPE="hidden" NAME="ClientASAM_Type_1" VALUE="DIS" >
<INPUT TYPE="hidden" NAME="ClientASAM_Level_1" VALUE=".05" >
</LOADHIDDEN>
</FORM>
<SCRIPT LANGUAGE="JavaScript">
document.ASAM.elements[0].focus();
</SCRIPT>

[[myHTML->rightpane(%form+search)]]
