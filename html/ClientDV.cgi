[[myHTML->newHTML(%form+Trauma+allleft mismenu checkpopupwindow)]]

<SCRIPT LANGUAGE="JavaScript" SRC="/src/cgi/js/vEntry.js"> </SCRIPT>
<SCRIPT LANGUAGE="JavaScript" SRC="/src/cgi/js/vClientDV.js"> </SCRIPT>
<SCRIPT LANGUAGE="JavaScript" SRC="/src/cgi/js/vNum.js"> </SCRIPT>

<FORM NAME="DV" ACTION="/src/cgi/bin/mis.cgi" METHOD="POST" >
<TABLE CLASS="main fullsize" >
  <TR >
    <TD CLASS="strcol" >
      <<<Client_FName_1>>> <<<Client_MName_1>>> <<<Client_LName_1>>> (<<<Client_ClientID_1>>>) <<<Client_SSN_1>>>
      <BR>
      Trauma Page
    </TD>
    <TD CLASS="numcol" >[[gHTML->setLINKS(%form+back)]]</TD>
  </TR>
</TABLE>
<TABLE CLASS="port fullsize" >
    <TR ><TD ><TABLE CLASS="home fullsize" >
  <TR ><TD CLASS="port hdrtxt" COLSPAN="4" >TRAUMA: Violence, Domestic Violence, Sexual</TD></TR>
  <TR >
    <TD CLASS="strcol" >Have you experienced any type of psychological trauma in your life?</TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="radio" NAME="ClientTrauma_Psych_1" VALUE="1" <<ClientTrauma_Psych_1=1>> > Yes
      <INPUT TYPE="radio" NAME="ClientTrauma_Psych_1" VALUE="0" <<ClientTrauma_Psych_1=0>> > No
    </TD>
    <TD CLASS="strcol" COLSPAN="2" >
      [<A HREF="#bottom" >If No, skip to the Family Relations section]</A>
    </TD>
  </TR>
  <TR ><TD CLASS="port hdrtxt" WIDTH="50%" >Crime Related Events</TD><TD>&nbsp;</TD><TD CLASS="homelabel" ># of<BR>Times</TD><TD CLASS="homelabel" >Approximate<BR>Age</TD></TR>
  <TR>
    <TD CLASS="strcol" >Has anyone ever tried to take something directly from you by using force or threat of force, such as a stick-up or mugging?</TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="radio" NAME="ClientTrauma_ThreatOfForce_1" VALUE="1" <<ClientTrauma_ThreatOfForce_1=1>> > Yes
      <INPUT TYPE="radio" NAME="ClientTrauma_ThreatOfForce_1" VALUE="0" <<ClientTrauma_ThreatOfForce_1=0>> > No
    </TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="text" NAME="ClientTrauma_ThreatOfForceTimes_1" VALUE="<<ClientTrauma_ThreatOfForceTimes_1>>" ONFOCUS="select()" MAXLENGTH="2" SIZE="2" >
    </TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="text" NAME="ClientTrauma_ThreatOfForceAge_1" VALUE="<<ClientTrauma_ThreatOfForceAge_1>>" ONFOCUS="select()" MAXLENGTH="2" SIZE="2" >
    </TD>
  </TR>
  <TR>
    <TD CLASS="strcol" >Has anyone ever attempted to rob you or actually robbed you (i.e. stolen your personal belongings)?</TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="radio" NAME="ClientTrauma_Robbed_1" VALUE="1" <<ClientTrauma_Robbed_1=1>> > Yes
      <INPUT TYPE="radio" NAME="ClientTrauma_Robbed_1" VALUE="0" <<ClientTrauma_Robbed_1=0>> > No
    </TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="text" NAME="ClientTrauma_RobbedTimes_1" VALUE="<<ClientTrauma_RobbedTimes_1>>" ONFOCUS="select()" MAXLENGTH="2" SIZE="2" >
    </TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="text" NAME="ClientTrauma_RobbedAge_1" VALUE="<<ClientTrauma_RobbedAge_1>>" ONFOCUS="select()" MAXLENGTH="2" SIZE="2" >
    </TD>
  </TR>
  <TR>
    <TD CLASS="strcol" >Has anyone ever attempted to or succeeded in breaking into your home when you weren't there?</TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="radio" NAME="ClientTrauma_BreakInHomeNT_1" VALUE="1" <<ClientTrauma_BreakInHomeNT_1=1>> > Yes
      <INPUT TYPE="radio" NAME="ClientTrauma_BreakInHomeNT_1" VALUE="0" <<ClientTrauma_BreakInHomeNT_1=0>> > No
    </TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="text" NAME="ClientTrauma_BreakInHomeNTTimes_1" VALUE="<<ClientTrauma_BreakInHomeNTTimes_1>>" ONFOCUS="select()" MAXLENGTH="2" SIZE="2" >
    </TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="text" NAME="ClientTrauma_BreakInHomeNTAge_1" VALUE="<<ClientTrauma_BreakInHomeNTAge_1>>" ONFOCUS="select()" MAXLENGTH="2" SIZE="2" >
    </TD>
  </TR>
  <TR>
    <TD CLASS="strcol" >Has anyone ever tried to or succeeded in breaking into your home while you were there?</TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="radio" NAME="ClientTrauma_BreakInHome_1" VALUE="1" <<ClientTrauma_BreakInHome_1=1>> > Yes
      <INPUT TYPE="radio" NAME="ClientTrauma_BreakInHome_1" VALUE="0" <<ClientTrauma_BreakInHome_1=0>> > No
    </TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="text" NAME="ClientTrauma_BreakInHomeTimes_1" VALUE="<<ClientTrauma_BreakInHomeTimes_1>>" ONFOCUS="select()" MAXLENGTH="2" SIZE="2" >
    </TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="text" NAME="ClientTrauma_BreakInHomeAge_1" VALUE="<<ClientTrauma_BreakInHomeAge_1>>" ONFOCUS="select()" MAXLENGTH="2" SIZE="2" >
    </TD>
  </TR>
  <TR ><TD CLASS="port hdrtxt" WIDTH="50%" >General Disaster and Emotional Trauma</TD><TD>&nbsp;</TD><TD CLASS="homelabel" ># of<BR>Times</TD><TD CLASS="homelabel" >Approximate<BR>Age</TD></TR>
  <TR>
    <TD CLASS="strcol" >Have you ever had a serious accident at work, in a car, or somewhere else?</TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="radio" NAME="ClientTrauma_Accident_1" VALUE="1" <<ClientTrauma_Accident_1=1>> > Yes
      <INPUT TYPE="radio" NAME="ClientTrauma_Accident_1" VALUE="0" <<ClientTrauma_Accident_1=0>> > No
    </TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="text" NAME="ClientTrauma_AccidentTimes_1" VALUE="<<ClientTrauma_AccidentTimes_1>>" ONFOCUS="select()" MAXLENGTH="2" SIZE="2" >
    </TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="text" NAME="ClientTrauma_AccidentAge_1" VALUE="<<ClientTrauma_AccidentAge_1>>" ONFOCUS="select()" MAXLENGTH="2" SIZE="2" >
    </TD>
  </TR>
  <TR ><TD CLASS="strcol" COLSPAN="4" >If yes, please specify:</TD></TR>
  <TR >
    <TD CLASS="strcol" COLSPAN="4" >
      <TEXTAREA NAME="ClientTrauma_AccidentText_1" COLS="90" ROWS="2" WRAP="virtual" ><<ClientTrauma_AccidentText_1>></TEXTAREA>
    </TD>
  </TR>
  <TR>
    <TD CLASS="strcol" >Have you ever experienced a natural disaster such as a tornado, hurricane, flood, major earthquake, etc., where you felt you or your loved ones were in danger of death or injury?</TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="radio" NAME="ClientTrauma_NaturalDisaster_1" VALUE="1" <<ClientTrauma_NaturalDisaster_1=1>> > Yes
      <INPUT TYPE="radio" NAME="ClientTrauma_NaturalDisaster_1" VALUE="0" <<ClientTrauma_NaturalDisaster_1=0>> > No
    </TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="text" NAME="ClientTrauma_NaturalDisasterTimes_1" VALUE="<<ClientTrauma_NaturalDisasterTimes_1>>" ONFOCUS="select()" MAXLENGTH="2" SIZE="2" >
    </TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="text" NAME="ClientTrauma_NaturalDisasterAge_1" VALUE="<<ClientTrauma_NaturalDisasterAge_1>>" ONFOCUS="select()" MAXLENGTH="2" SIZE="2" >
    </TD>
	
  <TR ><TD CLASS="strcol" COLSPAN="4" >If yes, please specify:</TD></TR>
  <TR >
    <TD CLASS="strcol" COLSPAN="4" >
      <TEXTAREA NAME="ClientTrauma_NaturalDisasterText_1" COLS="90" ROWS="2" WRAP="virtual" ><<ClientTrauma_NaturalDisasterText_1>></TEXTAREA>
    </TD>
  </TR>
  <TR>
    <TD CLASS="strcol" >Have you ever experienced a "man-made" disaster such as a train crash, building collapse, bank robbery, fire, etc., where you felt you or your loved ones were in danger of death or injury?</TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="radio" NAME="ClientTrauma_ManMadeDisaster_1" VALUE="1" <<ClientTrauma_ManMadeDisaster_1=1>> > Yes
      <INPUT TYPE="radio" NAME="ClientTrauma_ManMadeDisaster_1" VALUE="0" <<ClientTrauma_ManMadeDisaster_1=0>> > No
    </TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="text" NAME="ClientTrauma_ManMadeDisasterTimes_1" VALUE="<<ClientTrauma_ManMadeDisasterTimes_1>>" ONFOCUS="select()" MAXLENGTH="2" SIZE="2" >
    </TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="text" NAME="ClientTrauma_ManMadeDisasterAge_1" VALUE="<<ClientTrauma_ManMadeDisasterAge_1>>" ONFOCUS="select()" MAXLENGTH="2" SIZE="2" >
    </TD>

  <TR ><TD CLASS="strcol" COLSPAN="4" >If yes, please specify:</TD></TR>
  <TR >
    <TD CLASS="strcol" COLSPAN="4" >
      <TEXTAREA NAME="ClientTrauma_ManMadeDisasterText_1" COLS="90" ROWS="2" WRAP="virtual" ><<ClientTrauma_ManMadeDisasterText_1>></TEXTAREA>
    </TD>
  </TR>
  <TR>
    <TD CLASS="strcol" >Have you ever been exposed to dangerous chemicals or radioactivity that might threaten you health?</TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="radio" NAME="ClientTrauma_DangerChemicals_1" VALUE="1" <<ClientTrauma_DangerChemicals_1=1>> > Yes
      <INPUT TYPE="radio" NAME="ClientTrauma_DangerChemicals_1" VALUE="0" <<ClientTrauma_DangerChemicals_1=0>> > No
    </TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="text" NAME="ClientTrauma_DangerChemicalsTimes_1" VALUE="<<ClientTrauma_DangerChemicalsTimes_1>>" ONFOCUS="select()" MAXLENGTH="2" SIZE="2" >
    </TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="text" NAME="ClientTrauma_DangerChemicalsAge_1" VALUE="<<ClientTrauma_DangerChemicalsAge_1>>" ONFOCUS="select()" MAXLENGTH="2" SIZE="2" >
    </TD>
  </TR>
  <TR>
    <TD CLASS="strcol" >Have you ever been in any other situation in which you were seriously injured?</TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="radio" NAME="ClientTrauma_Injured_1" VALUE="1" <<ClientTrauma_Injured_1=1>> > Yes
      <INPUT TYPE="radio" NAME="ClientTrauma_Injured_1" VALUE="0" <<ClientTrauma_Injured_1=0>> > No
    </TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="text" NAME="ClientTrauma_InjuredTimes_1" VALUE="<<ClientTrauma_InjuredTimes_1>>" ONFOCUS="select()" MAXLENGTH="2" SIZE="2" >
    </TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="text" NAME="ClientTrauma_InjuredAge_1" VALUE="<<ClientTrauma_InjuredAge_1>>" ONFOCUS="select()" MAXLENGTH="2" SIZE="2" >
    </TD>

  <TR ><TD CLASS="strcol" COLSPAN="4" >If yes, please specify:</TD></TR>
  <TR >
    <TD CLASS="strcol" COLSPAN="4" >
      <TEXTAREA NAME="ClientTrauma_InjuredText_1" COLS="90" ROWS="2" WRAP="virtual" ><<ClientTrauma_InjuredText_1>></TEXTAREA>
    </TD>
  </TR>
  <TR>
    <TD CLASS="strcol" >Have you ever been in any other situation in which you feared you might be killed or seriously injured?</TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="radio" NAME="ClientTrauma_FearKilled_1" VALUE="1" <<ClientTrauma_FearKilled_1=1>> > Yes
      <INPUT TYPE="radio" NAME="ClientTrauma_FearKilled_1" VALUE="0" <<ClientTrauma_FearKilled_1=0>> > No
    </TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="text" NAME="ClientTrauma_FearKilledTimes_1" VALUE="<<ClientTrauma_FearKilledTimes_1>>" ONFOCUS="select()" MAXLENGTH="2" SIZE="2" >
    </TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="text" NAME="ClientTrauma_FearKilledAge_1" VALUE="<<ClientTrauma_FearKilledAge_1>>" ONFOCUS="select()" MAXLENGTH="2" SIZE="2" >
    </TD>

  <TR ><TD CLASS="strcol" COLSPAN="4" >If yes, please specify:</TD></TR>
  <TR >
    <TD CLASS="strcol" COLSPAN="4" >
      <TEXTAREA NAME="ClientTrauma_FearKilledText_1" COLS="90" ROWS="2" WRAP="virtual" ><<ClientTrauma_FearKilledText_1>></TEXTAREA>
    </TD>
  </TR>
  <TR>
    <TD CLASS="strcol" >Have you ever been seen someone seriously injured or killed?</TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="radio" NAME="ClientTrauma_SomeoneKilled_1" VALUE="1" <<ClientTrauma_SomeoneKilled_1=1>> > Yes
      <INPUT TYPE="radio" NAME="ClientTrauma_SomeoneKilled_1" VALUE="0" <<ClientTrauma_SomeoneKilled_1=0>> > No
    </TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="text" NAME="ClientTrauma_SomeoneKilledTimes_1" VALUE="<<ClientTrauma_SomeoneKilledTimes_1>>" ONFOCUS="select()" MAXLENGTH="2" SIZE="2" >
    </TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="text" NAME="ClientTrauma_SomeoneKilledAge_1" VALUE="<<ClientTrauma_SomeoneKilledAge_1>>" ONFOCUS="select()" MAXLENGTH="2" SIZE="2" >
    </TD>
  <TR ><TD CLASS="strcol" COLSPAN="4" >If yes, please specify who:</TD></TR>
  <TR >
    <TD CLASS="strcol" COLSPAN="4" >
      <TEXTAREA NAME="ClientTrauma_SomeoneKilledText_1" COLS="90" ROWS="2" WRAP="virtual" ><<ClientTrauma_SomeoneKilledText_1>></TEXTAREA>
    </TD>
  </TR>
  <TR>
    <TD CLASS="strcol" >Have you ever seen dead bodies (other than at a funeral) or had to handle dead bodies for any reason?</TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="radio" NAME="ClientTrauma_DeadBody_1" VALUE="1" <<ClientTrauma_DeadBody_1=1>> > Yes
      <INPUT TYPE="radio" NAME="ClientTrauma_DeadBody_1" VALUE="0" <<ClientTrauma_DeadBody_1=0>> > No
    </TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="text" NAME="ClientTrauma_DeadBodyTimes_1" VALUE="<<ClientTrauma_DeadBodyTimes_1>>" ONFOCUS="select()" MAXLENGTH="2" SIZE="2" >
    </TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="text" NAME="ClientTrauma_DeadBodyAge_1" VALUE="<<ClientTrauma_DeadBodyAge_1>>" ONFOCUS="select()" MAXLENGTH="2" SIZE="2" >
    </TD>
  <TR ><TD CLASS="strcol" COLSPAN="4" >If yes, please specify who:</TD></TR>
  <TR >
    <TD CLASS="strcol" COLSPAN="4" >
      <TEXTAREA NAME="ClientTrauma_DeadBodyText_1" COLS="90" ROWS="2" WRAP="virtual" ><<ClientTrauma_DeadBodyText_1>></TEXTAREA>
    </TD>
  </TR>
  <TR>
    <TD CLASS="strcol" >Have you ever had a close friend or family member murdered, or killed by a drunk driver?</TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="radio" NAME="ClientTrauma_CloseMurder_1" VALUE="1" <<ClientTrauma_CloseMurder_1=1>> > Yes
      <INPUT TYPE="radio" NAME="ClientTrauma_CloseMurder_1" VALUE="0" <<ClientTrauma_CloseMurder_1=0>> > No
    </TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="text" NAME="ClientTrauma_CloseMurderTimes_1" VALUE="<<ClientTrauma_CloseMurderTimes_1>>" ONFOCUS="select()" MAXLENGTH="2" SIZE="2" >
    </TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="text" NAME="ClientTrauma_CloseMurderAge_1" VALUE="<<ClientTrauma_CloseMurderAge_1>>" ONFOCUS="select()" MAXLENGTH="2" SIZE="2" >
    </TD>
  <TR ><TD CLASS="strcol" COLSPAN="4" >If yes, please specify relationship (e.g. mother, grandson, etc.):</TD></TR>
  <TR >
    <TD CLASS="strcol" COLSPAN="4" >
      <TEXTAREA NAME="ClientTrauma_CloseMurderText_1" COLS="90" ROWS="2" WRAP="virtual" ><<ClientTrauma_CloseMurderText_1>></TEXTAREA>
    </TD>
  </TR>
  <TR>
    <TD CLASS="strcol" >Have you ever had a spouse, romantic partner, or child die?</TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="radio" NAME="ClientTrauma_CloseDie_1" VALUE="1" <<ClientTrauma_CloseDie_1=1>> > Yes
      <INPUT TYPE="radio" NAME="ClientTrauma_CloseDie_1" VALUE="0" <<ClientTrauma_CloseDie_1=0>> > No
    </TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="text" NAME="ClientTrauma_CloseDieTimes_1" VALUE="<<ClientTrauma_CloseDieTimes_1>>" ONFOCUS="select()" MAXLENGTH="2" SIZE="2" >
    </TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="text" NAME="ClientTrauma_CloseDieAge_1" VALUE="<<ClientTrauma_CloseDieAge_1>>" ONFOCUS="select()" MAXLENGTH="2" SIZE="2" >
    </TD>
  <TR ><TD CLASS="strcol" COLSPAN="4" >If yes, please specify relationship:</TD></TR>
  <TR >
    <TD CLASS="strcol" COLSPAN="4" >
      <TEXTAREA NAME="ClientTrauma_CloseDieText_1" COLS="90" ROWS="2" WRAP="virtual" ><<ClientTrauma_CloseDieText_1>></TEXTAREA>
    </TD>
  </TR>
  <TR>
    <TD CLASS="strcol" >Have you ever had a serious or life-threatening illness?</TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="radio" NAME="ClientTrauma_SeriousIllness_1" VALUE="1" <<ClientTrauma_SeriousIllness_1=1>> > Yes
      <INPUT TYPE="radio" NAME="ClientTrauma_SeriousIllness_1" VALUE="0" <<ClientTrauma_SeriousIllness_1=0>> > No
    </TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="text" NAME="ClientTrauma_SeriousIllnessTimes_1" VALUE="<<ClientTrauma_SeriousIllnessTimes_1>>" ONFOCUS="select()" MAXLENGTH="2" SIZE="2" >
    </TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="text" NAME="ClientTrauma_SeriousIllnessAge_1" VALUE="<<ClientTrauma_SeriousIllnessAge_1>>" ONFOCUS="select()" MAXLENGTH="2" SIZE="2" >
    </TD>
  <TR ><TD CLASS="strcol" COLSPAN="4" >If yes, please specify:</TD></TR>
  <TR >
    <TD CLASS="strcol" COLSPAN="4" >
      <TEXTAREA NAME="ClientTrauma_SeriousIllnessText_1" COLS="90" ROWS="2" WRAP="virtual" ><<ClientTrauma_SeriousIllnessText_1>></TEXTAREA>
    </TD>
  </TR>
  <TR>
    <TD CLASS="strcol" >Have you ever received news of a serious injury, life-threatening illness, or unexpected death of someone close to you?</TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="radio" NAME="ClientTrauma_CloseThreat_1" VALUE="1" <<ClientTrauma_CloseThreat_1=1>> > Yes
      <INPUT TYPE="radio" NAME="ClientTrauma_CloseThreat_1" VALUE="0" <<ClientTrauma_CloseThreat_1=0>> > No
    </TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="text" NAME="ClientTrauma_CloseThreatTimes_1" VALUE="<<ClientTrauma_CloseThreatTimes_1>>" ONFOCUS="select()" MAXLENGTH="2" SIZE="2" >
    </TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="text" NAME="ClientTrauma_CloseThreatAge_1" VALUE="<<ClientTrauma_CloseThreatAge_1>>" ONFOCUS="select()" MAXLENGTH="2" SIZE="2" >
    </TD>
  <TR ><TD CLASS="strcol" COLSPAN="4" >If yes, please specify:</TD></TR>
  <TR >
    <TD CLASS="strcol" COLSPAN="4" >
      <TEXTAREA NAME="ClientTrauma_CloseThreatText_1" COLS="90" ROWS="2" WRAP="virtual" ><<ClientTrauma_CloseThreatText_1>></TEXTAREA>
    </TD>
  </TR>
  <TR>
    <TD CLASS="strcol" >Have you ever had to engage in combat while in the military service in an official or unofficial war zone?</TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="radio" NAME="ClientTrauma_Combat_1" VALUE="1" <<ClientTrauma_Combat_1=1>> > Yes
      <INPUT TYPE="radio" NAME="ClientTrauma_Combat_1" VALUE="0" <<ClientTrauma_Combat_1=0>> > No
    </TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="text" NAME="ClientTrauma_CombatTimes_1" VALUE="<<ClientTrauma_CombatTimes_1>>" ONFOCUS="select()" MAXLENGTH="2" SIZE="2" >
    </TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="text" NAME="ClientTrauma_CombatAge_1" VALUE="<<ClientTrauma_CombatAge_1>>" ONFOCUS="select()" MAXLENGTH="2" SIZE="2" >
    </TD>
  <TR ><TD CLASS="strcol" COLSPAN="4" >If yes, please where:</TD></TR>
  <TR >
    <TD CLASS="strcol" COLSPAN="4" >
      <TEXTAREA NAME="ClientTrauma_CombatText_1" COLS="90" ROWS="2" WRAP="virtual" ><<ClientTrauma_CombatText_1>></TEXTAREA>
    </TD>
  </TR>
  <TR ><TD CLASS="port hdrtxt" WIDTH="50%" >Physical and Sexual Experiences</TD><TD>&nbsp;</TD><TD CLASS="homelabel" ># of<BR>Times</TD><TD CLASS="homelabel" >Approximate<BR>Age</TD></TR>
  <TR>
    <TD CLASS="strcol" >Has anyone ever made you have intercourse, oral or anal sex against you will?</TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="radio" NAME="ClientTrauma_ForcedSex_1" VALUE="1" <<ClientTrauma_ForcedSex_1=1>> > Yes
      <INPUT TYPE="radio" NAME="ClientTrauma_ForcedSex_1" VALUE="0" <<ClientTrauma_ForcedSex_1=0>> > No
    </TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="text" NAME="ClientTrauma_ForcedSexTimes_1" VALUE="<<ClientTrauma_ForcedSexTimes_1>>" ONFOCUS="select()" MAXLENGTH="2" SIZE="2" >
    </TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="text" NAME="ClientTrauma_ForcedSexAge_1" VALUE="<<ClientTrauma_ForcedSexAge_1>>" ONFOCUS="select()" MAXLENGTH="2" SIZE="2" >
    </TD>
  <TR ><TD CLASS="strcol" COLSPAN="4" >If yes, please specify relationship with person (e.g. stranger, friend, relative, parent, sibling, etc.):</TD></TR>
  <TR >
    <TD CLASS="strcol" COLSPAN="4" >
      <TEXTAREA NAME="ClientTrauma_ForcedSexText_1" COLS="90" ROWS="2" WRAP="virtual" ><<ClientTrauma_ForcedSexText_1>></TEXTAREA>
    </TD>
  <TR>
    <TD CLASS="strcol" >Has anyone ever touched private parts of your body, or made you touch theirs, under force or threat?</TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="radio" NAME="ClientTrauma_ForcedTouch_1" VALUE="1" <<ClientTrauma_ForcedTouch_1=1>> > Yes
      <INPUT TYPE="radio" NAME="ClientTrauma_ForcedTouch_1" VALUE="0" <<ClientTrauma_ForcedTouch_1=0>> > No
    </TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="text" NAME="ClientTrauma_ForcedTouchTimes_1" VALUE="<<ClientTrauma_ForcedTouchTimes_1>>" ONFOCUS="select()" MAXLENGTH="2" SIZE="2" >
    </TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="text" NAME="ClientTrauma_ForcedTouchAge_1" VALUE="<<ClientTrauma_ForcedTouchAge_1>>" ONFOCUS="select()" MAXLENGTH="2" SIZE="2" >
    </TD>
  <TR ><TD CLASS="strcol" COLSPAN="4" >If yes, please specify relationship with person (e.g. stranger, friend, relative, parent, sibling, etc.):</TD></TR>
  <TR >
    <TD CLASS="strcol" COLSPAN="4" >
      <TEXTAREA NAME="ClientTrauma_ForcedTouchText_1" COLS="90" ROWS="2" WRAP="virtual" ><<ClientTrauma_ForcedTouchText_1>></TEXTAREA>
    </TD>
  </TR>
  <TR>
    <TD CLASS="strcol" >Have there been any other situations in which another person tried to force you to have unwanted sexual contact?</TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="radio" NAME="ClientTrauma_ForcedContact_1" VALUE="1" <<ClientTrauma_ForcedContact_1=1>> > Yes
      <INPUT TYPE="radio" NAME="ClientTrauma_ForcedContact_1" VALUE="0" <<ClientTrauma_ForcedContact_1=0>> > No
    </TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="text" NAME="ClientTrauma_ForcedContactTimes_1" VALUE="<<ClientTrauma_ForcedContactTimes_1>>" ONFOCUS="select()" MAXLENGTH="2" SIZE="2" >
    </TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="text" NAME="ClientTrauma_ForcedContactAge_1" VALUE="<<ClientTrauma_ForcedContactAge_1>>" ONFOCUS="select()" MAXLENGTH="2" SIZE="2" >
    </TD>
  </TR>
  <TR>
    <TD CLASS="strcol" >Has anyone, including family members or friends, ever attacked you with a gun, knife, or some other weapon?</TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="radio" NAME="ClientTrauma_CloseAttack_1" VALUE="1" <<ClientTrauma_CloseAttack_1=1>> > Yes
      <INPUT TYPE="radio" NAME="ClientTrauma_CloseAttack_1" VALUE="0" <<ClientTrauma_CloseAttack_1=0>> > No
    </TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="text" NAME="ClientTrauma_CloseAttackTimes_1" VALUE="<<ClientTrauma_CloseAttackTimes_1>>" ONFOCUS="select()" MAXLENGTH="2" SIZE="2" >
    </TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="text" NAME="ClientTrauma_CloseAttackAge_1" VALUE="<<ClientTrauma_CloseAttackAge_1>>" ONFOCUS="select()" MAXLENGTH="2" SIZE="2" >
    </TD>
  </TR>
  <TR>
    <TD CLASS="strcol" >Has anyone, including family members or friends, ever attacked you without a weapon and seriously injured you?</TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="radio" NAME="ClientTrauma_CloseInjured_1" VALUE="1" <<ClientTrauma_CloseInjured_1=1>> > Yes
      <INPUT TYPE="radio" NAME="ClientTrauma_CloseInjured_1" VALUE="0" <<ClientTrauma_CloseInjured_1=0>> > No
    </TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="text" NAME="ClientTrauma_CloseInjuredTimes_1" VALUE="<<ClientTrauma_CloseInjuredTimes_1>>" ONFOCUS="select()" MAXLENGTH="2" SIZE="2" >
    </TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="text" NAME="ClientTrauma_CloseInjuredAge_1" VALUE="<<ClientTrauma_CloseInjuredAge_1>>" ONFOCUS="select()" MAXLENGTH="2" SIZE="2" >
    </TD>
  </TR>
  <TR>
    <TD CLASS="strcol" >Has anyone in your family ever beaten, "spanked" or pushed you hard enough to cause injury?</TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="radio" NAME="ClientTrauma_HardSpank_1" VALUE="1" <<ClientTrauma_HardSpank_1=1>> > Yes
      <INPUT TYPE="radio" NAME="ClientTrauma_HardSpank_1" VALUE="0" <<ClientTrauma_HardSpank_1=0>> > No
    </TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="text" NAME="ClientTrauma_HardSpankTimes_1" VALUE="<<ClientTrauma_HardSpankTimes_1>>" ONFOCUS="select()" MAXLENGTH="2" SIZE="2" >
    </TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="text" NAME="ClientTrauma_HardSpankAge_1" VALUE="<<ClientTrauma_HardSpankAge_1>>" ONFOCUS="select()" MAXLENGTH="2" SIZE="2" >
    </TD>
  </TR>
  <TR ><TD CLASS="port hdrtxt" WIDTH="50%" >Other Events</TD><TD>&nbsp;</TD><TD CLASS="homelabel" ># of<BR>Times</TD><TD CLASS="homelabel" >Approximate<BR>Age</TD></TR>
  <TR>
    <TD CLASS="strcol" >Have you experienced any other extraordinarily stressful situation or event that was not covered?</TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="radio" NAME="ClientTrauma_Other_1" VALUE="1" <<ClientTrauma_Other_1=1>> > Yes
      <INPUT TYPE="radio" NAME="ClientTrauma_Other_1" VALUE="0" <<ClientTrauma_Other_1=0>> > No
    </TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="text" NAME="ClientTrauma_OtherTimes_1" VALUE="<<ClientTrauma_OtherTimes_1>>" ONFOCUS="select()" MAXLENGTH="2" SIZE="2" >
    </TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="text" NAME="ClientTrauma_OtherAge_1" VALUE="<<ClientTrauma_OtherAge_1>>" ONFOCUS="select()" MAXLENGTH="2" SIZE="2" >
    </TD>

  <TR ><TD CLASS="strcol" COLSPAN="4" >If yes, please specify:</TD></TR>
  <TR >
    <TD CLASS="strcol" COLSPAN="4" >
      <TEXTAREA NAME="ClientTrauma_OtherDescr_1" COLS="90" ROWS="2" WRAP="virtual" ><<ClientTrauma_OtherDescr_1>></TEXTAREA>
    </TD>
  </TR>

    </TABLE></TD></TR>
    <TR ><TD ><TABLE CLASS="home fullsize" >
  <TR ><TD CLASS="strcol" >Have any of these people abused you?</TD><TD CLASS="homesublink" >If yes, then <U>Add New</U> below.</TD></TR>
  <TR ><TD CLASS="strcol" >Have you abused anyone?</TD><TD CLASS="homesublink" >If yes, then <U>Add New</U> below.</TD></TR>
  <TR ><TD CLASS="strcol" COLSPAN="2" >Indicate from view of client:  If person abused client indicate Perpetrator; If client abused person indicate Victim.  If both, check both.</TD></TR>
  <TR ><TD CLASS="homesubtitle" COLSPAN="2" >V=victim, P=perpetrator, B=both, N=none</TD></TR>
  <TR >
    <TD COLSPAN="2" >
<SPAN ID="ListClientDVFamily" >
[[myHTML->ListSel(%form+ListClientDVFamily+<<<Client_ClientID>>>+<<<LINKID>>>+<<<Client_Locked_1>>>)]]
</SPAN>
    </TD>
  </TR>
  <TR >
    <TD CLASS="strcol" >Domestic Violence by other than a Family member?</TD>
    <TD CLASS="strcol" >
      <INPUT TYPE=radio NAME="ClientIntake_DV_1" VALUE=1 <<ClientIntake_DV_1=1>> > Yes
      <INPUT TYPE=radio NAME="ClientIntake_DV_1" VALUE=0 <<ClientIntake_DV_1=0>> > No
    </TD>
  </TR>
  <TR >
    <TD CLASS="strcol" >Sexual Assault by other than a Family member?</TD>
    <TD CLASS="strcol" >
      <INPUT TYPE=radio NAME="ClientIntake_SA_1" VALUE=1 <<ClientIntake_SA_1=1>> > Yes
      <INPUT TYPE=radio NAME="ClientIntake_SA_1" VALUE=0 <<ClientIntake_SA_1=0>> > No
    </TD>
  </TR>
  <TR >
    <TD CLASS="strcol" >Have you ever been Battered while pregnant (if applicable)?</TD>
    <TD CLASS="strcol" >
      <INPUT TYPE=radio NAME="MedHx_BatteredWP_1" VALUE=1 <<MedHx_BatteredWP_1=1>> > Yes
      <INPUT TYPE=radio NAME="MedHx_BatteredWP_1" VALUE=0 <<MedHx_BatteredWP_1=0>> > No
    </TD>
  </TR>
  <TR >
    <TD CLASS="strcol" >Have you ever witnessed domestic violence?</TD>
    <TD CLASS="strcol" >
      <INPUT TYPE=radio NAME="ClientIntake_WitnessDV_1" VALUE=1 <<ClientIntake_WitnessDV_1=1>> > Yes
      <INPUT TYPE=radio NAME="ClientIntake_WitnessDV_1" VALUE=0 <<ClientIntake_WitnessDV_1=0>> > No
    </TD>
  </TR>
    </TABLE></TD></TR>
    <TR ><TD ><TABLE CLASS="home fullsize" >
  <TR ><TD CLASS="port hdrtxt" COLSPAN="2" >Treatments</TD></TR>
  <TR ><TD CLASS="strcol" COLSPAN="2" >Have you received any treatment specifically for psychological trauma?</TD></TR>
  <TR><TD CLASS="homesublink" COLSPAN="2" >If yes, then <U>Add New</U> below.</TD></TR>
  <TR >
    <TD COLSPAN="2" >
<SPAN ID="ListClientTreatments" >
[[myHTML->ListSel(%form+ListClientTreatments+<<<Client_ClientID>>>+<<<LINKID>>>+<<<Client_Locked_1>>>)]]
</SPAN>
    </TD>
  </TR>
  <TR ><TD CLASS="port hdrtxt" COLSPAN="2" >TESTING</TD></TR>
  <TR CLASS="list hdrcol" >
    <TD COLSPAN="2" >
      <A HREF="javascript:InputWindow('/src/cgi/bin/mis.cgi?view=IESInp2.cgi&Client_ClientID=<<<Client_ClientID_1>>>&mlt=<<<mlt>>>&misLINKS=<<<misLINKS>>>&NONAVIGATION=1','IES',900,1200)" CLASS="mybutton" >Impact of Events Scale-Revised (IES-R)</A>
    </TD>
  </TR>
  <TR CLASS="list hdrcol" >
    <TD COLSPAN="2" >
[[DBA->isCHILD(%form+<<<Client_DOB_1>>>)      <A HREF="javascript:InputWindow('/src/cgi/bin/mis.cgi?view=ListCATS.cgi&Client_ClientID=<<<Client_ClientID_1>>>&mlt=<<<mlt>>>&misLINKS=<<<misLINKS>>>&NONAVIGATION=1','CATS',900,1200)" CLASS="mybutton" >ENTER Child and Adolescent Trauma Screen (CATS) - Youth Report</A> ]]
[[DBA->isADULT(%form+<<<Client_DOB_1>>>)      <A HREF="javascript:InputWindow('/src/cgi/bin/mis.cgi?view=ListPCL5.cgi&Client_ClientID=<<<Client_ClientID_1>>>&mlt=<<<mlt>>>&misLINKS=<<<misLINKS>>>&NONAVIGATION=1','PCL5',900,1200)" CLASS="mybutton" >ENTER PTSD Checklist for DSM-5 (PCL-5)</A> ]]
    </TD>
  </TR>
    </TABLE></TD></TR>
</TABLE>
<A NAME="bottom" >

<TABLE CLASS="main fullsize" >
  <TR >
    <TD CLASS="numcol" >
      <INPUT TYPE="submit" ONCLICK="return validate(this.form);" NAME="UpdateTables=all&[[myForm->genLink(ClientFamily+ClientFamilyRel.cgi)]]" VALUE="Add/Update -> Family Relations">
      <INPUT TYPE="submit" ONCLICK="return validate(this.form);" NAME="UpdateTables=all&misPOP=1" VALUE="Add/Update">
    </TD>
  </TR>
</TABLE>

</LOADHIDDEN>
</FORM>
<SCRIPT LANGUAGE="JavaScript">
document.DV.elements[0].focus();
</SCRIPT>

[[myHTML->rightpane(%form+search)]]
