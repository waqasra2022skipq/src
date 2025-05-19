[[myHTML->newHTML(%form+Client IES+clock)]]
<SCRIPT LANGUAGE="JavaScript" SRC="/src/cgi/js/vEntry.js"> </SCRIPT>
<SCRIPT LANGUAGE="JavaScript" SRC="/src/cgi/js/vIES.js"> </SCRIPT>
<SCRIPT LANGUAGE="JavaScript" SRC="/src/cgi/js/vNum.js"> </SCRIPT>
<FORM NAME="submit" ACTION="/src/cgi/bin/mis.cgi" METHOD="POST">
  <TABLE CLASS="home fullsize" >
    <TR ><TD CLASS="port hdrtxt" COLSPAN="2" >Impact of Events Scale-Revised (IES-R)</TD></TR>
    <TR ><TD CLASS="strcol" COLSPAN="2" >Answer the following questions about the most distressing psychological trauma event and your distress level over the past 7 days.</TD></TR>
    <TR ><TD CLASS="strcol" COLSPAN="2" >0 = Not at all   1 = A little bit   2 = Moderately   3 = Quite a bit   4 = Extremely.</TD></TR>
    <TR >
      <TD CLASS="strcol" >
        1.  Any reminder brought back feelings about it.
      </TD>
      <TD CLASS="strcol" >
        <INPUT TYPE="text" NAME="IES_AnyReminder_1" VALUE="<<IES_AnyReminder_1>>" ONFOCUS="select()" ONCHANGE="return validateScore(this.form,this)" SIZE="3" >
      </TD>
    </TR>
    <TR >
      <TD CLASS="strcol" >
        2.  I had trouble staying asleep.
      </TD>
      <TD CLASS="strcol" >
        <INPUT TYPE="text" NAME="IES_TroubleSleeping_1" VALUE="<<IES_TroubleSleeping_1>>" ONFOCUS="select()" ONCHANGE="return validateScore(this.form,this)" SIZE="3" >
      </TD>
    </TR>
    <TR >
      <TD CLASS="strcol" >
        3.  Other things kept making me think about it.
      </TD>
      <TD CLASS="strcol" >
        <INPUT TYPE="text" NAME="IES_ThinkAbout_1" VALUE="<<IES_ThinkAbout_1>>" ONFOCUS="select()" ONCHANGE="return validateScore(this.form,this)" SIZE="3" >
      </TD>
    </TR>
    <TR >
      <TD CLASS="strcol" >
        4.  I felt irritable and angry.
      </TD>
      <TD CLASS="strcol" >
        <INPUT TYPE="text" NAME="IES_Irritable_1" VALUE="<<IES_Irritable_1>>" ONFOCUS="select()" ONCHANGE="return validateScore(this.form,this)" SIZE="3" >
      </TD>
    </TR>
    <TR >
      <TD CLASS="strcol" >
        5.  I avoided letting myself get upset when I thought about it or was reminded of it.
      </TD>
      <TD CLASS="strcol" >
        <INPUT TYPE="text" NAME="IES_AvoidedUpset_1" VALUE="<<IES_AvoidedUpset_1>>" ONFOCUS="select()" ONCHANGE="return validateScore(this.form,this)" SIZE="3" >
      </TD>
    </TR>
    <TR >
      <TD CLASS="strcol" >
        6.  I thought about it when I didn't mean to.
      </TD>
      <TD CLASS="strcol" >
        <INPUT TYPE="text" NAME="IES_ThoughtsAbout_1" VALUE="<<IES_ThoughtsAbout_1>>" ONFOCUS="select()" ONCHANGE="return validateScore(this.form,this)" SIZE="3" >
      </TD>
    </TR>
    <TR >
      <TD CLASS="strcol" >
        7.  I felt as if it hadn't happened or wasn't real.
      </TD>
      <TD CLASS="strcol" >
        <INPUT TYPE="text" NAME="IES_WasntReal_1" VALUE="<<IES_WasntReal_1>>" ONFOCUS="select()" ONCHANGE="return validateScore(this.form,this)" SIZE="3" >
      </TD>
    </TR>
    <TR >
      <TD CLASS="strcol" >
        8.  I stayed away from reminders of it.
      </TD>
      <TD CLASS="strcol" >
        <INPUT TYPE="text" NAME="IES_AvoidReminders_1" VALUE="<<IES_AvoidReminders_1>>" ONFOCUS="select()" ONCHANGE="return validateScore(this.form,this)" SIZE="3" >
      </TD>
    </TR>
    <TR >
      <TD CLASS="strcol" >
        9.  Pictures about it popped into my mind.
      </TD>
      <TD CLASS="strcol" >
        <INPUT TYPE="text" NAME="IES_PicturesAbout_1" VALUE="<<IES_PicturesAbout_1>>" ONFOCUS="select()" ONCHANGE="return validateScore(this.form,this)" SIZE="3" >
      </TD>
    </TR>
    <TR >
      <TD CLASS="strcol" >
        10. I was jumpy and easily startled.
      </TD>
      <TD CLASS="strcol" >
        <INPUT TYPE="text" NAME="IES_EasilyStartled_1" VALUE="<<IES_EasilyStartled_1>>" ONFOCUS="select()" ONCHANGE="return validateScore(this.form,this)" SIZE="3" >
      </TD>
    </TR>
    <TR >
      <TD CLASS="strcol" >
        11. I tried not to think about it.
      </TD>
      <TD CLASS="strcol" >
        <INPUT TYPE="text" NAME="IES_NotThinkAbout_1" VALUE="<<IES_NotThinkAbout_1>>" ONFOCUS="select()" ONCHANGE="return validateScore(this.form,this)" SIZE="3" >
      </TD>
    </TR>
    <TR >
      <TD CLASS="strcol" >
        12. I was aware that I still had a lot of feelings about it, but I didn't deal with them.
      </TD>
      <TD CLASS="strcol" >
        <INPUT TYPE="text" NAME="IES_DidntDeal_1" VALUE="<<IES_DidntDeal_1>>" ONFOCUS="select()" ONCHANGE="return validateScore(this.form,this)" SIZE="3" >
      </TD>
    </TR>
    <TR >
      <TD CLASS="strcol" >
        13. My feelings about it were kind of numb.
      </TD>
      <TD CLASS="strcol" >
        <INPUT TYPE="text" NAME="IES_KindOfNumb_1" VALUE="<<IES_KindOfNumb_1>>" ONFOCUS="select()" ONCHANGE="return validateScore(this.form,this)" SIZE="3" >
      </TD>
    </TR>
    <TR >
      <TD CLASS="strcol" >
        14. I found myself acting or feeling like I was back at that time.
      </TD>
      <TD CLASS="strcol" >
        <INPUT TYPE="text" NAME="IES_BackAtTime_1" VALUE="<<IES_BackAtTime_1>>" ONFOCUS="select()" ONCHANGE="return validateScore(this.form,this)" SIZE="3" >
      </TD>
    </TR>
    <TR >
      <TD CLASS="strcol" >
        15. I had trouble falling asleep.
      </TD>
      <TD CLASS="strcol" >
        <INPUT TYPE="text" NAME="IES_TroubleAsleep_1" VALUE="<<IES_TroubleAsleep_1>>" ONFOCUS="select()" ONCHANGE="return validateScore(this.form,this)" SIZE="3" >
      </TD>
    </TR>
    <TR >
      <TD CLASS="strcol" >
        16. I had waves of strong feelings about it.
      </TD>
      <TD CLASS="strcol" >
        <INPUT TYPE="text" NAME="IES_StrongFeelings_1" VALUE="<<IES_StrongFeelings_1>>" ONFOCUS="select()" ONCHANGE="return validateScore(this.form,this)" SIZE="3" >
      </TD>
    </TR>
    <TR >
      <TD CLASS="strcol" >
        17. I tried to remove it from my memory.
      </TD>
      <TD CLASS="strcol" >
        <INPUT TYPE="text" NAME="IES_RemoveMemory_1" VALUE="<<IES_RemoveMemory_1>>" ONFOCUS="select()" ONCHANGE="return validateScore(this.form,this)" SIZE="3" >
      </TD>
    </TR>
    <TR >
      <TD CLASS="strcol" >
        18. I had trouble concentrating.
      </TD>
      <TD CLASS="strcol" >
        <INPUT TYPE="text" NAME="IES_TroubleCon_1" VALUE="<<IES_TroubleCon_1>>" ONFOCUS="select()" ONCHANGE="return validateScore(this.form,this)" SIZE="3" >
      </TD>
    </TR>
    <TR >
      <TD CLASS="strcol" >
        19. Reminders of it caused me to have physical reactions, such as sweating, trouble breathing, nausea, or a pounding heart.
      </TD>
      <TD CLASS="strcol" >
        <INPUT TYPE="text" NAME="IES_PhysicalReactions_1" VALUE="<<IES_PhysicalReactions_1>>" ONFOCUS="select()" ONCHANGE="return validateScore(this.form,this)" SIZE="3" >
      </TD>
    </TR>
    <TR >
      <TD CLASS="strcol" >
        20. I had dreams about it.
      </TD>
      <TD CLASS="strcol" >
        <INPUT TYPE="text" NAME="IES_DreamsAbout_1" VALUE="<<IES_DreamsAbout_1>>" ONFOCUS="select()" ONCHANGE="return validateScore(this.form,this)" SIZE="3" >
      </TD>
    </TR>
    <TR >
      <TD CLASS="strcol" >
        21. I felt watchful and on-guard.
      </TD>
      <TD CLASS="strcol" >
        <INPUT TYPE="text" NAME="IES_Watchful_1" VALUE="<<IES_Watchful_1>>" ONFOCUS="select()" ONCHANGE="return validateScore(this.form,this)" SIZE="3" >
      </TD>
    </TR>
    <TR >
      <TD CLASS="strcol" >
        22. I tried not to talk about it.	
      </TD>
      <TD CLASS="strcol" >
        <INPUT TYPE="text" NAME="IES_NotTalk_1" VALUE="<<IES_NotTalk_1>>" ONFOCUS="select()" ONCHANGE="return validateScore(this.form,this)" SIZE="3" >
      </TD>
    </TR>
    <TR >
      <TD CLASS="strcol" COLSPAN="2" >
        Average:
        <INPUT TYPE="TEXT" NAME="IES_Average_1" VALUE="<<IES_Average_>>" ONFOCUS="this.blur()" SIZE="6" >
       <BR>
        Total:
        <INPUT TYPE="TEXT" NAME="IES_Score_1" VALUE="<<IES_Score_1>>" ONFOCUS="this.blur()" SIZE="6" >
       <BR>
       A score >31 was 81% sensitive and 91% specific for treatment need (Positive).
      </TD>
    </TR>
  </TABLE>
  <TABLE CLASS="main fullsize" >
    <TR>
      <TD CLASS="numcol" COLSPAN="2" >
        <INPUT TYPE="button" VALUE="Calc Total" ONCLICK="javascript:validateScore(this.form,form.IES_AnyReminder_1)" >
        <INPUT TYPE="button" NAME="cancel" VALUE="Cancel" ONCLICK="javascript: window.close()" >
        <INPUT TYPE="submit" ONCLICK="return validate(this.form);" NAME="UpdateTables=all" VALUE="Add/Update" >
      </TD>
    </TR>
  </TABLE>
<INPUT TYPE="hidden" NAME="CLOSEWINDOW" VALUE="CLOSE">
</LOADHIDDEN>
</FORM>
<SCRIPT LANGUAGE="JavaScript">
  document.submit.elements[0].focus();
</SCRIPT>
[[myHTML->rightpane(%form)]]
