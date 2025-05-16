[[myHTML->newPage(%form+Gambling)]]

<SCRIPT LANGUAGE="JavaScript" SRC="/src/cgi/js/vEntry.js"> </SCRIPT>
<SCRIPT LANGUAGE="JavaScript" SRC="/src/cgi/js/vClientGambling.js"> </SCRIPT>
<SCRIPT LANGUAGE="JavaScript" SRC="/src/cgi/js/vNum.js"> </SCRIPT>

<FORM NAME="Gambling" ACTION="/cgi/bin/mis.cgi" METHOD="POST" >
<TABLE CLASS="main fullsize" >
  <TR >
    <TD CLASS="strcol" >
      <<<Client_FName_1>>> <<<Client_MName_1>>> <<<Client_LName_1>>> (<<<Client_ClientID_1>>>) <<<Client_SSN_1>>>
      <BR>
      Gambling Page
    </TD>
    <TD CLASS="numcol" >[[gHTML->setLINKS(%form+back)]]</TD>
  </TR>
</TABLE>
<TABLE CLASS="port fullsize" >
    <TR ><TD ><TABLE CLASS="home fullsize" >
  <TR ><TD CLASS="port hdrtxt" COLSPAN="2" >GAMBLING</TD></TR>
  <TR>
    <TD CLASS="strcol" > Do you have a history of gambling: </TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="radio" NAME="Gambling_History_1" VALUE=1 <<Gambling_History_1=1>> > Yes
      <INPUT TYPE="radio" NAME="Gambling_History_1" VALUE=0 <<Gambling_History_1=0>> > No
    </TD>
  </TR>
  <TR><TD CLASS="strcol" COLSPAN="2" >If yes, please provide the following information:.</TD></TR>
  <TR>
    <TD CLASS="strcol" >During the past 12 months, have you become restless irritable or anxious when trying to stop/cut down on gambling?</TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="radio" NAME="Gambling_Anxious_1" VALUE=1 <<Gambling_Anxious_1=1>> > Yes
      <INPUT TYPE="radio" NAME="Gambling_Anxious_1" VALUE=0 <<Gambling_Anxious_1=0>> > No
    </TD>
  </TR>
  <TR>
    <TD CLASS="strcol" >During the past 12 months, have you tried to keep your family or friends from knowing how much you gambled?</TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="radio" NAME="Gambling_KeepFrom_1" VALUE=1 <<Gambling_KeepFrom_1=1>> > Yes
      <INPUT TYPE="radio" NAME="Gambling_KeepFrom_1" VALUE=0 <<Gambling_KeepFrom_1=0>> > No
    </TD>
  </TR>
  <TR>
    <TD CLASS="strcol" >During the past 12 months did you have such financial trouble as a result of your gambling that you had to get help with living expenses from family, friends or welfare?</TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="radio" NAME="Gambling_FinHelp_1" VALUE=1 <<Gambling_FinHelp_1=1>> > Yes
      <INPUT TYPE="radio" NAME="Gambling_FinHelp_1" VALUE=0 <<Gambling_FinHelp_1=0>> > No
    </TD>
  </TR>
  <TR>
    <TD CLASS="strcol" >Any Yes answer is Positive.
     <A HREF="javascript:ReportWindow('/src/cgi/bin/printBSGS.cgi?IDs=<<<Gambling_ID_1>>>&mlt=<<<mlt>>>&misLINKS=<<<misLINKS>>>','PrintBSGS')" ONMOUSEOVER="window.status='Print Brief BioSocial Screen'; return true;" ONMOUSEOUT="window.status=''"><IMG SRC="/images/icon_print.gif" ALT="" BORDER="0" > Brief BioSocial Gambling Screen (save changes first)</A>
    </TD>
  </TR>
  <TR><TD CLASS="port hdrtxt" > If Positive, complete SOGS</TD></TR>
  <TR>
    <TD CLASS="strcol" > Do you have any debts related to, or as a result of, gambling?</TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="radio" NAME="Gambling_Debts_1" VALUE=1 <<Gambling_Debts_1=1>> > Yes
      <INPUT TYPE="radio" NAME="Gambling_Debts_1" VALUE=0 <<Gambling_Debts_1=0>> > No
    </TD>
  </TR>
  <TR>
    <TD CLASS="strcol" > If yes, please describe:</TD>
    <TD CLASS="strcol" >
      <TEXTAREA NAME="Gambling_DebtsText_1" COLS="70" ROWS="10" WRAP="virtual" ><<Gambling_DebtsText_1>></TEXTAREA>
    </TD>
  </TR>
  <TR>
    <TD CLASS="strcol" > Current financial status:</TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="radio" NAME="Gambling_FinanceStatus_1" VALUE=G <<Gambling_FinanceStatus_1=G>> > Good
      <INPUT TYPE="radio" NAME="Gambling_FinanceStatus_1" VALUE=F <<Gambling_FinanceStatus_1=F>> > Fair
      <INPUT TYPE="radio" NAME="Gambling_FinanceStatus_1" VALUE=P <<Gambling_FinanceStatus_1=P>> > Poor
    </TD>
  </TR>
  <TR>
    <TD CLASS="strcol" > Please describe:</TD>
    <TD CLASS="strcol" >
      <TEXTAREA NAME="Gambling_FinanceStatusText_1" COLS="70" ROWS="10" WRAP="virtual" ><<Gambling_FinanceStatusText_1>></TEXTAREA>
    </TD>
  </TR>
  <TR>
    <TD CLASS="strcol" > Have you ever lost time from work or school due to gambling?</TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="radio" NAME="Gambling_LostTime_1" VALUE=1 <<Gambling_LostTime_1=1>> > Yes
      <INPUT TYPE="radio" NAME="Gambling_LostTime_1" VALUE=0 <<Gambling_LostTime_1=0>> > No
    </TD>
  </TR>
  <TR>
    <TD CLASS="strcol" > Has gambling ever made your home life unhappy?</TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="radio" NAME="Gambling_LifeUnhappy_1" VALUE=1 <<Gambling_LifeUnhappy_1=1>> > Yes
      <INPUT TYPE="radio" NAME="Gambling_LifeUnhappy_1" VALUE=0 <<Gambling_LifeUnhappy_1=0>> > No
    </TD>
  </TR>
  <TR>
    <TD CLASS="strcol" > Has gambling affected your reputation?</TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="radio" NAME="Gambling_Reputation_1" VALUE=1 <<Gambling_Reputation_1=1>> > Yes
      <INPUT TYPE="radio" NAME="Gambling_Reputation_1" VALUE=0 <<Gambling_Reputation_1=0>> > No
    </TD>
  </TR>
  <TR>
    <TD CLASS="strcol" > Have you ever felt remorse after gambling?</TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="radio" NAME="Gambling_FeltRemorse_1" VALUE=1 <<Gambling_FeltRemorse_1=1>> > Yes
      <INPUT TYPE="radio" NAME="Gambling_FeltRemorse_1" VALUE=0 <<Gambling_FeltRemorse_1=0>> > No
    </TD>
  </TR>
  <TR>
    <TD CLASS="strcol" > Have you ever gambled to get money to pay debts or solve financial difficulties?</TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="radio" NAME="Gambling_PayDebts_1" VALUE=1 <<Gambling_PayDebts_1=1>> > Yes
      <INPUT TYPE="radio" NAME="Gambling_PayDebts_1" VALUE=0 <<Gambling_PayDebts_1=0>> > No
    </TD>
  </TR>
  <TR>
    <TD CLASS="strcol" > Has gambling ever caused a decrease in your ambition or efficiency?</TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="radio" NAME="Gambling_Ambition_1" VALUE=1 <<Gambling_Ambition_1=1>> > Yes
      <INPUT TYPE="radio" NAME="Gambling_Ambition_1" VALUE=0 <<Gambling_Ambition_1=0>> > No
    </TD>
  </TR>
  <TR>
    <TD CLASS="strcol" > After losing, do you feel you must return as soon as possible to win back your losses?</TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="radio" NAME="Gambling_WinBack_1" VALUE=1 <<Gambling_WinBack_1=1>> > Yes
      <INPUT TYPE="radio" NAME="Gambling_WinBack_1" VALUE=0 <<Gambling_WinBack_1=0>> > No
    </TD>
  </TR>
  <TR>
    <TD CLASS="strcol" > After winning, do you have a strong urge to return and win more?</TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="radio" NAME="Gambling_WinMore_1" VALUE=1 <<Gambling_WinMore_1=1>> > Yes
      <INPUT TYPE="radio" NAME="Gambling_WinMore_1" VALUE=0 <<Gambling_WinMore_1=0>> > No
    </TD>
  </TR>
  <TR>
    <TD CLASS="strcol" > Do you often gamble until you run out of money?</TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="radio" NAME="Gambling_RunOut_1" VALUE=1 <<Gambling_RunOut_1=1>> > Yes
      <INPUT TYPE="radio" NAME="Gambling_RunOut_1" VALUE=0 <<Gambling_RunOut_1=0>> > No
    </TD>
  </TR>
  <TR>
    <TD CLASS="strcol" > Have you ever borrowed money to finance your gambling?</TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="radio" NAME="Gambling_Borrowed_1" VALUE=1 <<Gambling_Borrowed_1=1>> > Yes
      <INPUT TYPE="radio" NAME="Gambling_Borrowed_1" VALUE=0 <<Gambling_Borrowed_1=0>> > No
    </TD>
  </TR>
  <TR>
    <TD CLASS="strcol" > Have you ever sold anything to finance your gambling?</TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="radio" NAME="Gambling_Sold_1" VALUE=1 <<Gambling_Sold_1=1>> > Yes
      <INPUT TYPE="radio" NAME="Gambling_Sold_1" VALUE=0 <<Gambling_Sold_1=0>> > No
    </TD>
  </TR>
  <TR>
    <TD CLASS="strcol" > Are you reluctant to use "gambling money" for normal expenditures?</TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="radio" NAME="Gambling_Reluctant_1" VALUE=1 <<Gambling_Reluctant_1=1>> > Yes
      <INPUT TYPE="radio" NAME="Gambling_Reluctant_1" VALUE=0 <<Gambling_Reluctant_1=0>> > No
    </TD>
  </TR>
  <TR>
    <TD CLASS="strcol" > Does gambling make you careless of the welfare of yourself and your family?</TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="radio" NAME="Gambling_Careless_1" VALUE=1 <<Gambling_Careless_1=1>> > Yes
      <INPUT TYPE="radio" NAME="Gambling_Careless_1" VALUE=0 <<Gambling_Careless_1=0>> > No
    </TD>
  </TR>
  <TR>
    <TD CLASS="strcol" > Do you ever gamble longer than planned?</TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="radio" NAME="Gambling_Longer_1" VALUE=1 <<Gambling_Longer_1=1>> > Yes
      <INPUT TYPE="radio" NAME="Gambling_Longer_1" VALUE=0 <<Gambling_Longer_1=0>> > No
    </TD>
  </TR>
  <TR>
    <TD CLASS="strcol" > Have you ever gambled to escape worry or trouble?</TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="radio" NAME="Gambling_Escape_1" VALUE=1 <<Gambling_Escape_1=1>> > Yes
      <INPUT TYPE="radio" NAME="Gambling_Escape_1" VALUE=0 <<Gambling_Escape_1=0>> > No
    </TD>
  </TR>
  <TR>
    <TD CLASS="strcol" > Have you ever committed or considered committing an illegal act to finance gambling?</TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="radio" NAME="Gambling_IllegalAct_1" VALUE=1 <<Gambling_IllegalAct_1=1>> > Yes
      <INPUT TYPE="radio" NAME="Gambling_IllegalAct_1" VALUE=0 <<Gambling_IllegalAct_1=0>> > No
    </TD>
  </TR>
  <TR>
    <TD CLASS="strcol" > Has gambling ever caused you to have difficulty sleeping?</TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="radio" NAME="Gambling_DifSleeping_1" VALUE=1 <<Gambling_DifSleeping_1=1>> > Yes
      <INPUT TYPE="radio" NAME="Gambling_DifSleeping_1" VALUE=0 <<Gambling_DifSleeping_1=0>> > No
    </TD>
  </TR>
  <TR>
    <TD CLASS="strcol" > Do arguments, disappointments or frustrations create within you an urge to gamble?</TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="radio" NAME="Gambling_Arguments_1" VALUE=1 <<Gambling_Arguments_1=1>> > Yes
      <INPUT TYPE="radio" NAME="Gambling_Arguments_1" VALUE=0 <<Gambling_Arguments_1=0>> > No
    </TD>
  </TR>
  <TR>
    <TD CLASS="strcol" > Do you ever get the urge to celebrate any good fortune with a few hours of gambling?</TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="radio" NAME="Gambling_Celebrate_1" VALUE=1 <<Gambling_Celebrate_1=1>> > Yes
      <INPUT TYPE="radio" NAME="Gambling_Celebrate_1" VALUE=0 <<Gambling_Celebrate_1=0>> > No
    </TD>
  </TR>
  <TR>
    <TD CLASS="strcol" > Have you ever considered self destruction as a result of your gambling?</TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="radio" NAME="Gambling_SelfDestruct_1" VALUE=1 <<Gambling_SelfDestruct_1=1>> > Yes
      <INPUT TYPE="radio" NAME="Gambling_SelfDestruct_1" VALUE=0 <<Gambling_SelfDestruct_1=0>> > No
    </TD>
  </TR>
  <TR><TD CLASS="port hdrtxt" > TREATMENTS</TD></TR>
  <TR>
    <TD CLASS="strcol" > Have you ever received gambling treatment before?</TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="radio" NAME="Gambling_Treatment_1" VALUE=1 <<Gambling_Treatment_1=1>> > Yes
      <INPUT TYPE="radio" NAME="Gambling_Treatment_1" VALUE=0 <<Gambling_Treatment_1=0>> > No
    </TD>
  </TR>
  <TR> <TD CLASS="strcol" > If Yes (last 3), Where: Type: (Circle) When: How Long:</TD></TR>
  <TR >
    <TD COLSPAN="2" >
<SPAN ID="ListClientTreatments" >
[[myHTML->ListSel(%form+ListClientTreatments+<<<Client_ClientID>>>+<<<LINKID>>>+<<<Client_Locked_1>>>)]]
</SPAN>
    </TD>
  </TR>
  <TR><TD CLASS="port hdrtxt" > OTHER BEHAVIORAL ADDICTIONS</TD></TR>
  <TR>
    <TD CLASS="strcol" > Do you have a history of other behavioral addictions?</TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="radio" NAME="Gambling_Addictions_1" VALUE=1 <<Gambling_Addictions_1=1>> > Yes
      <INPUT TYPE="radio" NAME="Gambling_Addictions_1" VALUE=0 <<Gambling_Addictions_1=0>> > No
    </TD>
  </TR>
  <TR >
    <TD CLASS="strcol" > If yes, check all that apply: </TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="checkbox" NAME="Gambling_EatDisorder_1" VALUE="1" <<Gambling_EatDisorder_1=checkbox>> > Eating disorder
      <INPUT TYPE="checkbox" NAME="Gambling_Shopping_1" VALUE="1" <<Gambling_Shopping_1=checkbox>> > Excessive shopping
      <INPUT TYPE="checkbox" NAME="Gambling_Exercise_1" VALUE="1" <<Gambling_Exercise_1=checkbox>> > Exercise
    </TD>
  </TR>
  <TR >
    <TD CLASS="strcol" > &nbsp;</TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="checkbox" NAME="Gambling_Multilation_1" VALUE="1" <<Gambling_Multilation_1=checkbox>> > Self-multilation
      <INPUT TYPE="checkbox" NAME="Gambling_Sex_1" VALUE="1" <<Gambling_Sex_1=checkbox>> > Sex
      <INPUT TYPE="checkbox" NAME="Gambling_Pornography_1" VALUE="1" <<Gambling_Pornography_1=checkbox>> > Pornography
    </TD>
  </TR>
  <TR >
    <TD CLASS="strcol" > &nbsp;</TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="checkbox" NAME="Gambling_OtherAddictions_1" VALUE="1" <<Gambling_OtherAddictions_1=checkbox>> > Other
      <INPUT TYPE="TEXT" NAME="Gambling_OtherAddictionsText_1" VALUE="<<Gambling_OtherAddictionsText_1>>" ONFOCUS="select()" SIZE="35">
    </TD>
  </TR>
  <TR>
    <TD CLASS="strcol" > If any of the above are checked, please describe:</TD>
    <TD CLASS="strcol" >
      <TEXTAREA NAME="Gambling_AddictionsText_1" COLS="70" ROWS="10" WRAP="virtual" ><<Gambling_AddictionsText_1>></TEXTAREA>
    </TD>
  </TR>
    </TABLE></TD></TR>
</TABLE>
<TABLE CLASS="main fullsize" >
  <TR >
    <TD CLASS="numcol" >
      <INPUT TYPE="submit" ONCLICK="return validate(this.form);" NAME="UpdateTables=all&[[myForm->genLink(ClientIntake+ClientDV.cgi)]]" VALUE="Add/Update -> Trauma">
      <INPUT TYPE="submit" ONCLICK="return validate(this.form);" NAME="UpdateTables=all&misPOP=1" VALUE="Add/Update">
    </TD>
  </TR>
</TABLE>

</LOADHIDDEN>
</FORM>
<SCRIPT LANGUAGE="JavaScript">
document.Gambling.elements[0].focus();
</SCRIPT>

[[myHTML->rightpane(%form+search)]]
