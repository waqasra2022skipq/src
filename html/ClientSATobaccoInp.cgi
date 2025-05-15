[[myHTML->newHTML(%form+Client SATobacco)]]

<SCRIPT LANGUAGE="JavaScript" SRC="/src/cgi/js/NoEnter.js"> </SCRIPT>
<SCRIPT LANGUAGE="JavaScript" SRC="/src/cgi/js/vEntry.js"> </SCRIPT>
<SCRIPT LANGUAGE="JavaScript" SRC="/src/cgi/js/vClientSATobacco.js"> </SCRIPT>
<SCRIPT LANGUAGE="JavaScript" SRC="/src/cgi/js/vDate.js"> </SCRIPT>
<SCRIPT LANGUAGE="JavaScript" SRC="/src/cgi/js/vTime.js"> </SCRIPT>

<FORM NAME="SATobacco" ACTION="/cgi/bin/mis.cgi" METHOD="POST" >
<TABLE CLASS="main fullsize" >
  <TR >
    <TD CLASS="strcol" >
      <<<Client_FName_1>>> <<<Client_MName_1>>> <<<Client_LName_1>>> (<<<Client_ClientID_1>>>) <<<Client_SSN_1>>>
      <BR>
      Substance Abuse Tobacco 
    </TD>
    <TD CLASS="numcol" >[[gHTML->setLINKS(%form+back)]]</TD>
  </TR>
</TABLE>
<TABLE CLASS="home fullsize" >
  <TR ><TD CLASS="port hdrtxt" >Tobacco Screening Information</TD></TR>
  <TR ><TD ><TABLE CLASS="home fullsize" >
  <TR >
    <TD CLASS="strcol" >Visit Date</TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="text" NAME="ClientSATobacco_vdate_1" VALUE="<<ClientSATobacco_vdate_1>>" ONFOCUS="select()" ONCHANGE="return vDate(this,0,this.form)" SIZE="10" >
    </TD>
  </TR>
  <TR >
    <TD CLASS="strcol" >Start Time</TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="text" NAME="ClientSATobacco_stime_1" VALUE="<<ClientSATobacco_stime_1>>" ONFOCUS="select()" ONCHANGE="return vTime(this,1,this)" MAXLENGTH="10" SIZE="10" >
    </TD>
  </TR>
  </TABLE></TD></TR>
  <TR ><TD ><TABLE CLASS="home fullsize" >
  <TR ><TD CLASS="port hdrtxt" >Ask every client every time (1 minute)</TD></TR>
  <TR >
    <TD CLASS="strcol" >
      <SELECT NAME="ClientSATobacco_SmokingStatus_1" >
        [[DBA->selxTable(%form+xSmokingStatus+<<ClientSATobacco_SmokingStatus_1>>+ID Descr)]]
      </SELECT> 
    </TD>
    <TD CLASS="strcol" >
      Does not smoke = 4<BR>
      Recently quit  = 3<BR>
      Light smoker (less than 25 cigarettes per day) = 8<BR>
      Heavy smoker (25+ cigarettes per day) = 7<BR>
    </TD>
  </TR>
  <TR ><TD CLASS="hdrtxt" >Date range of smoking status?</TD></TR>
  <TR >
    <TD CLASS="strcol" >Start Date</TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="text" NAME="ClientSATobacco_StartDate_1" VALUE="<<ClientSATobacco_StartDate_1>>" ONFOCUS="select()" ONCHANGE="return vDate(this,0)" SIZE="10" >
    </TD>
  </TR>
  <TR >
    <TD CLASS="strcol" >End Date</TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="text" NAME="ClientSATobacco_EndDate_1" VALUE="<<ClientSATobacco_EndDate_1>>" ONFOCUS="select()" ONCHANGE="return vDate(this,0)" SIZE="10" >
    </TD>
  </TR>
  <TR >
    <TD CLASS="strcol" >Age of first use</TD>
    <TD CLASS="strcol" >
      <INPUT TYPE=text NAME="ClientSATobacco_Age_1" VALUE="<<ClientSATobacco_Age_1>>" ONFOCUS="select()" ONCHANGE="return vNum(this,1,99)" >
    </TD>
  </TR>
  <TR >
    <TD CLASS="strcol" >
      Have you used smokeless tobacco product in the last 30 days [SAMHSA]?
    </TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="radio" NAME="ClientSATobacco_smokeless_1" VALUE="1" <<ClientSATobacco_smokeless_1=1>> > Yes
      <INPUT TYPE="radio" NAME="ClientSATobacco_smokeless_1" VALUE="0" <<ClientSATobacco_smokeless_1=0>> > No
    </TD>
  </TR>
  </TABLE></TD></TR>
  <TR ><TD ><TABLE CLASS="home fullsize" >
  <TR ><TD CLASS="port hdrtxt" >Advise all tobacco users of the consequences (1 minute)</TD></TR>
  <TR >
    <TD CLASS="strcol" >
      <INPUT TYPE="checkbox" NAME="ClientSATobacco_benefits_1" VALUE="1" <<ClientSATobacco_benefits_1=checkbox>> > Benefits of quitting
    </TD>
  </TR>
  <TR >
    <TD CLASS="strcol" >
      <INPUT TYPE="checkbox" NAME="ClientSATobacco_harms_1" VALUE="1" <<ClientSATobacco_harms_1=checkbox>> > Harms of continuing
    </TD>
  </TR>
  <TR >
    <TD CLASS="strcol" >
      <INPUT TYPE="checkbox" NAME="ClientSATobacco_message_1" VALUE="1" <<ClientSATobacco_message_1=checkbox>> > Personalized message to quit
    </TD>
  </TR>
  <TR >
    <TD CLASS="strcol" >
      <INPUT TYPE="checkbox" NAME="ClientSATobacco_difficulty_1" VALUE="1" <<ClientSATobacco_difficulty_1=checkbox>> > Recognize difficulty of quitting
    </TD>
  </TR>
  </TABLE></TD></TR>
  <TR ><TD ><TABLE CLASS="home fullsize" >
  <TR ><TD CLASS="port hdrtxt" >Assess willingness to make a quit attempt (1 minute)</TD></TR>
  <TR >
    <TD CLASS="strcol" >Readiness to quit in next 30 days:
    <TD CLASS="strcol" >
      <INPUT TYPE="radio" NAME="ClientSATobacco_quit30_1" VALUE="1" <<ClientSATobacco_quit30_1=1>> > Yes
      <INPUT TYPE="radio" NAME="ClientSATobacco_quit30_1" VALUE="0" <<ClientSATobacco_quit30_1=0>> > No
    </TD>
  </TR>
  <TR >
    <TD CLASS="strcol" >Reason for not quitting</TD>
    <TD CLASS="strcol" >
      <TEXTAREA NAME="ClientSATobacco_reason_1" COLS="90" ROWS="8" WRAP="virtual" ><<ClientSATobacco_reason_1>></TEXTAREA>
    </TD>
  </TR>
  </TABLE></TD></TR>
  <TR ><TD ><TABLE CLASS="home fullsize" >
  <TR ><TD CLASS="port hdrtxt" COLSPAN="2" >Assist with treatment and referrals (3+ minutes)</TD></TR>
  <TR >
    <TD CLASS="strcol" >Set Quit Date</TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="text" NAME="ClientSATobacco_qdate_1" VALUE="<<ClientSATobacco_qdate_1>>" ONFOCUS="select()" ONCHANGE="return vDate(this,0,this.form)" SIZE="10" >
    </TD>
  </TR>
  <TR >
    <TD CLASS="strcol" COLSPAN="2" >
      <INPUT TYPE="checkbox" NAME="ClientSATobacco_problem_1" VALUE="1" <<ClientSATobacco_problem_1=checkbox>> > Problem solving
    </TD>
  </TR>
  <TR >
    <TD CLASS="strcol" COLSPAN="2" >
      <INPUT TYPE="checkbox" NAME="ClientSATobacco_materials_1" VALUE="1" <<ClientSATobacco_materials_1=checkbox>> > Provider materials
    </TD>
  </TR>
  <TR >
    <TD CLASS="strcol" COLSPAN="2" >
      <INPUT TYPE="checkbox" NAME="ClientSATobacco_identify_1" VALUE="1" <<ClientSATobacco_identify_1=checkbox>> > Identify Support
    </TD>
  </TR>
  <TR >
    <TD CLASS="strcol" COLSPAN="2" >
      <INPUT TYPE="checkbox" NAME="ClientSATobacco_refer_1" VALUE="1" <<ClientSATobacco_refer_1=checkbox>> > Refer to 1 800 QUIT NOW
    </TD>
  </TR>
  <TR >
    <TD CLASS="strcol" COLSPAN="2" >
      <INPUT TYPE="checkbox" NAME="ClientSATobacco_pharma_1" VALUE="1" <<ClientSATobacco_pharma_1=checkbox>> > Pharmacotherapy
    </TD>
  </TR>
  </TABLE></TD></TR>
  <TR ><TD ><TABLE CLASS="home fullsize" >
  <TR ><TD CLASS="port hdrtxt" >Arrange follow up (1 minute)</TD></TR>
  <TR >
    <TD CLASS="strcol" >
      <INPUT TYPE="checkbox" NAME="ClientSATobacco_assess_1" VALUE="1" <<ClientSATobacco_assess_1=checkbox>> > Assess smoking status at every visit
    </TD>
  </TR>
  <TR >
    <TD CLASS="strcol" >
      <INPUT TYPE="checkbox" NAME="ClientSATobacco_ask_1" VALUE="1" <<ClientSATobacco_ask_1=checkbox>> > Ask client about the quitting process
    </TD>
  </TR>
  <TR >
    <TD CLASS="strcol" >
      <INPUT TYPE="checkbox" NAME="ClientSATobacco_reinforce_1" VALUE="1" <<ClientSATobacco_reinforce_1=checkbox>> > Reinforce the steps the client is taking to quit
    </TD>
  </TR>
  <TR >
    <TD CLASS="strcol" >
      <INPUT TYPE="checkbox" NAME="ClientSATobacco_encourage_1" VALUE="1" <<ClientSATobacco_encourage_1=checkbox>> > Provider encouragement
    </TD>
  </TR>
  <TR >
    <TD CLASS="strcol" >
      <INPUT TYPE="checkbox" NAME="ClientSATobacco_followup_1" VALUE="1" <<ClientSATobacco_followup_1=checkbox>> > Set follow up appointment
    </TD>
  </TR>
  </TABLE></TD></TR>
  <TR ><TD ><TABLE CLASS="home fullsize" >
  <TR >
    <TD CLASS="strcol" >Comments</TD>
    <TD CLASS="strcol" >
      <TEXTAREA NAME="ClientSATobacco_comments_1" COLS="90" ROWS="8" WRAP="virtual" ><<ClientSATobacco_comments_1>></TEXTAREA>
    </TD>
  </TR>
  <TR >
    <TD CLASS="strcol" >End Time</TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="text" NAME="ClientSATobacco_etime_1" VALUE="<<ClientSATobacco_etime_1>>" ONFOCUS="select()" ONCHANGE="return vTime(this,1,this)" MAXLENGTH="10" SIZE="10" >
    </TD>
  </TR>
  </TABLE></TD></TR>
  <TR ><TD ><TABLE CLASS="home fullsize" >
  </TABLE></TD></TR>
</TABLE>
<TABLE CLASS="main fullsize" >
  <TR >
    <TD CLASS="numcol" >
      <INPUT TYPE="submit" ONCLICK="return vDELETE('Are you sure you want to delete this record?');" NAME="ClientSATobacco_DELETE_1=1&UpdateTables=all&misPOP=1" VALUE="Delete">
      <INPUT TYPE=submit ONCLICK="return validate(this.form);" NAME="UpdateTables=all&misPOP=1" VALUE="Add/Update">
    </TD>
  </TR>
</TABLE>

</LOADHIDDEN>
</FORM>
<SCRIPT LANGUAGE="JavaScript">
document.SATobacco.elements[0].focus();
// just to OPENTABLES...
//<<<ClientSATobacco_ClientID_1>>>
</SCRIPT>

[[myHTML->rightpane(%form+search)]]
