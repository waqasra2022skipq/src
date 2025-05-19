[[myHTML->newPage(%form+Mental Status)]]

<SCRIPT LANGUAGE="JavaScript" SRC="/src/cgi/js/vEntry.js"> </SCRIPT>
<SCRIPT LANGUAGE="JavaScript" SRC="/src/cgi/js/vClientMentalStatus.js"> </SCRIPT>
<SCRIPT LANGUAGE="JavaScript" SRC="/src/cgi/js/vNum.js"> </SCRIPT>

<FORM NAME="MentalStat" ACTION="/src/cgi/bin/mis.cgi" METHOD="POST" >
<TABLE CLASS="main fullsize" >
  <TR >
    <TD CLASS="strcol" >
      <<<Client_FName_1>>> <<<Client_MName_1>>> <<<Client_LName_1>>> (<<<Client_ClientID_1>>>) <<<Client_SSN_1>>>
      <BR>
      Mental Status Page
    </TD>
    <TD CLASS="numcol" >[[gHTML->setLINKS(%form+back)]]</TD>
  </TR>
</TABLE>
<TABLE CLASS="home fullsize" >
    <TR ><TD ><TABLE CLASS="home fullsize" >
  <TR ><TD CLASS="hdrtxt" COLSPAN="4" >Physical</TD></TR>
  <TR >
    <TD CLASS="strcol" WIDTH="20%" >Appearance
    <TD CLASS="strcol" >
      <INPUT TYPE="radio" NAME="MentalStat_Appearance_1" VALUE="Same as stated age" <<MentalStat_Appearance_1=Same as stated age>> > 
      Same as stated age
    <TD CLASS="strcol" >
      <INPUT TYPE="radio" NAME="MentalStat_Appearance_1" VALUE="Younger than stated age" <<MentalStat_Appearance_1=Younger than stated age>> > 
      Younger than stated age
    <TD CLASS="strcol" >
      <INPUT TYPE="radio" NAME="MentalStat_Appearance_1" VALUE="Older than stated age" <<MentalStat_Appearance_1=Older than stated age>> > 
      Older than stated age
  </TR>
  <TR><TD CLASS="strcol" COLSPAN="4" >&nbsp;</TD></TR>
  <TR >
    <TD CLASS="strcol" WIDTH="20%" >Manner of Dress
    <TD CLASS="strcol" >
      <INPUT TYPE="radio" NAME="MentalStat_Dress_1" VALUE="Appropriate" <<MentalStat_Dress_1=Appropriate>> > 
      Appropriate
    <TD CLASS="strcol" >
      <INPUT TYPE="radio" NAME="MentalStat_Dress_1" VALUE="Meticulous" <<MentalStat_Dress_1=Meticulous>> > 
      Meticulous
    <TD CLASS="strcol" >
      <INPUT TYPE="radio" NAME="MentalStat_Dress_1" VALUE="Disheveled/Dirty" <<MentalStat_Dress_1=Disheveled/Dirty>> > 
      Disheveled/Dirty
  </TR>
  <TR >
    <TD CLASS="strcol" WIDTH="20%" >&nbsp;</TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="radio" NAME="MentalStat_Dress_1" VALUE="Stylist/Modern" <<MentalStat_Dress_1=Stylist/Modern>> > 
      Stylist/Modern
    <TD CLASS="strcol" >
      <INPUT TYPE="radio" NAME="MentalStat_Dress_1" VALUE="Unusual/Bizarre/unseasonal" <<MentalStat_Dress_1=Unusual/Bizarre/unseasonal>> > 
      Unusual/Bizarre/unseasonal
    <TD CLASS="strcol" >&nbsp;</TD>
  </TR>
  <TR><TD CLASS="strcol" COLSPAN="4" >&nbsp;</TD></TR>
  <TR >
    <TD CLASS="strcol" WIDTH="20%" >Hygiene
    <TD CLASS="strcol" >
      <INPUT TYPE="radio" NAME="MentalStat_Hygiene_1" VALUE="Good" <<MentalStat_Hygiene_1=Good>> > 
      Good
    <TD CLASS="strcol" >
      <INPUT TYPE="radio" NAME="MentalStat_Hygiene_1" VALUE="Unkempt" <<MentalStat_Hygiene_1=Unkempt>> > 
      Unkempt
    <TD CLASS="strcol" >
      <INPUT TYPE="radio" NAME="MentalStat_Hygiene_1" VALUE="Poor" <<MentalStat_Hygiene_1=Poor>> > 
      Poor
  </TR>
  <TR >
    <TD CLASS="strcol" WIDTH="20%" >&nbsp;</TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="radio" NAME="MentalStat_Hygiene_1" VALUE="Neglected/Unclean" <<MentalStat_Hygiene_1=Neglected/Unclean>> > 
      Neglected/Unclean
    <TD CLASS="strcol" >&nbsp;</TD>
    <TD CLASS="strcol" >&nbsp;</TD>
  </TR>
  <TR><TD CLASS="strcol" COLSPAN="4" >&nbsp;</TD></TR>
  <TR >
    <TD CLASS="strcol" WIDTH="20%" >Nutrition
    <TD CLASS="strcol" >
      <INPUT TYPE="radio" NAME="MentalStat_Nutrition_1" VALUE="Height/Weight Appropriate" <<MentalStat_Nutrition_1=Height/Weight Appropriate>> > 
      Height/Weight Appropriate
    <TD CLASS="strcol" >
      <INPUT TYPE="radio" NAME="MentalStat_Nutrition_1" VALUE="Obese" <<MentalStat_Nutrition_1=Obese>> > 
      Obese
    <TD CLASS="strcol" >
      <INPUT TYPE="radio" NAME="MentalStat_Nutrition_1" VALUE="Malnourished" <<MentalStat_Nutrition_1=Malnourished>> > 
      Malnourished
  </TR>
  <TR >
    <TD CLASS="strcol" WIDTH="20%" >&nbsp;</TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="radio" NAME="MentalStat_Nutrition_1" VALUE="Frail/Wasted" <<MentalStat_Nutrition_1=Frail/Wasted>> > 
      Frail/Wasted
    <TD CLASS="strcol" >&nbsp;</TD>
    <TD CLASS="strcol" >&nbsp;</TD>
  </TR>
  <TR><TD CLASS="strcol" COLSPAN="4" >&nbsp;</TD></TR>
  <TR ><TD CLASS="strcol" COLSPAN="4" >Prosthetic Devices<BR>(Check all that apply)
  </TR>
  <TR >
    <TD CLASS="strcol" WIDTH="20%" >&nbsp;</TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="checkbox" NAME="MentalStat_PDNR_1" VALUE=1 <<MentalStat_PDNR_1=checkbox>> > 
      None Reported
    <TD CLASS="strcol" >
      <INPUT TYPE="checkbox" NAME="MentalStat_Glasses_1" VALUE=1 <<MentalStat_Glasses_1=checkbox>> > 
      Glasses
    <TD CLASS="strcol" >
      <INPUT TYPE="checkbox" NAME="MentalStat_HearAid_1" VALUE=1 <<MentalStat_HearAid_1=checkbox>> > 
      Hearing Aid
  </TR>
  <TR >
    <TD CLASS="strcol" WIDTH="20%" >&nbsp;</TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="checkbox" NAME="MentalStat_Cane_1" VALUE=1 <<MentalStat_Cane_1=checkbox>> > 
      Cane
    <TD CLASS="strcol" >
      <INPUT TYPE="checkbox" NAME="MentalStat_Crutches_1" VALUE=1 <<MentalStat_Crutches_1=checkbox>> > 
      Crutches
    <TD CLASS="strcol" >
      <INPUT TYPE="checkbox" NAME="MentalStat_Walker_1" VALUE=1 <<MentalStat_Walker_1=checkbox>> > 
      Walker
  </TR>
  <TR >
    <TD CLASS="strcol" WIDTH="20%" >&nbsp;</TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="checkbox" NAME="MentalStat_LegBrace_1" VALUE=1 <<MentalStat_LegBrace_1=checkbox>> > 
      Leg Braces
    <TD CLASS="strcol" >
      <INPUT TYPE="checkbox" NAME="MentalStat_Wheelchair_1" VALUE=1 <<MentalStat_Wheelchair_1=checkbox>> > 
      Wheelchair
    <TD CLASS="strcol" >&nbsp;</TD>
  </TR>
  <TR><TD CLASS="strcol" COLSPAN="4" >&nbsp;</TD></TR>
    </TABLE></TD></TR>
    <TR ><TD ><TABLE CLASS="home fullsize" >
  <TR ><TD CLASS="hdrtxt" COLSPAN="4" >Interview Behavior</TD></TR>
  <TR >
    <TD CLASS="strcol" WIDTH="20%" >Posture
    <TD CLASS="strcol" >
      <INPUT TYPE="radio" NAME="MentalStat_Posture_1" VALUE="Normal" <<MentalStat_Posture_1=Normal>> > 
      Normal
    <TD CLASS="strcol" >
      <INPUT TYPE="radio" NAME="MentalStat_Posture_1" VALUE="Slumped Posture" <<MentalStat_Posture_1=Slumped Posture>> > 
      Slumped Posture
    <TD CLASS="strcol" >
      <INPUT TYPE="radio" NAME="MentalStat_Posture_1" VALUE="Rigid/Tense Posture" <<MentalStat_Posture_1=Rigid/Tense Posture>> > 
      Rigid/Tense Posture
  </TR>
  <TR><TD CLASS="strcol" COLSPAN="4" >&nbsp;</TD></TR>
  <TR >
    <TD CLASS="strcol" WIDTH="20%" >Facial Expression
    <TD CLASS="strcol" >
      <INPUT TYPE="radio" NAME="MentalStat_Facial_1" VALUE="Normal and Responsive" <<MentalStat_Facial_1=Normal and Responsive>> > 
      Normal and Responsive
    <TD CLASS="strcol" >
      <INPUT TYPE="radio" NAME="MentalStat_Facial_1" VALUE="Avoids Eye Contact" <<MentalStat_Facial_1=Avoids Eye Contact>> > 
      Avoids Eye Contact
    <TD CLASS="strcol" >
      <INPUT TYPE="radio" NAME="MentalStat_Facial_1" VALUE="Incongruent with Topic" <<MentalStat_Facial_1=Incongruent with Topic>> > 
      Incongruent with Topic
  </TR>
  <TR >
    <TD CLASS="strcol" WIDTH="20%" >&nbsp;</TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="radio" NAME="MentalStat_Facial_1" VALUE="Expressionless" <<MentalStat_Facial_1=Expressionless>> > 
      Expressionless
    <TD CLASS="strcol" >
      <INPUT TYPE="radio" NAME="MentalStat_Facial_1" VALUE="Hostile" <<MentalStat_Facial_1=Hostile>> > 
      Hostile
    <TD CLASS="strcol" >
      <INPUT TYPE="radio" NAME="MentalStat_Facial_1" VALUE="Worried" <<MentalStat_Facial_1=Worried>> > 
      Worried
  </TR>
  <TR >
    <TD CLASS="strcol" WIDTH="20%" >&nbsp;</TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="radio" NAME="MentalStat_Facial_1" VALUE="Happy" <<MentalStat_Facial_1=Happy>> > 
      Happy
    <TD CLASS="strcol" >
      <INPUT TYPE="radio" NAME="MentalStat_Facial_1" VALUE="Sad" <<MentalStat_Facial_1=Sad>> > 
      Sad
    <TD CLASS="strcol" >
      <INPUT TYPE="radio" NAME="MentalStat_Facial_1" VALUE="Inappropriate" <<MentalStat_Facial_1=Inappropriate>> > 
      Inappropriate
  </TR>
  <TR><TD CLASS="strcol" COLSPAN="4" >&nbsp;</TD></TR>
    </TABLE></TD></TR>
    <TR ><TD ><TABLE CLASS="home fullsize" >
  <TR ><TD CLASS="hdrtxt" COLSPAN="4" >Motor Activity</TD></TR>
  <TR >
    <TD CLASS="strcol" WIDTH="20%" >Gait
    <TD CLASS="strcol" >
      <INPUT TYPE="radio" NAME="MentalStat_Gait_1" VALUE="Normal/Ambulatory" <<MentalStat_Gait_1=Normal/Ambulatory>> > 
      Normal/Ambulatory
    <TD CLASS="strcol" >
      <INPUT TYPE="radio" NAME="MentalStat_Gait_1" VALUE="Shuffling" <<MentalStat_Gait_1=Shuffling>> > 
      Shuffling
    <TD CLASS="strcol" >
      <INPUT TYPE="radio" NAME="MentalStat_Gait_1" VALUE="Poor Coordination" <<MentalStat_Gait_1=Poor Coordination>> > 
      Poor Coordination
  </TR>
  <TR >
    <TD CLASS="strcol" WIDTH="20%" >&nbsp;</TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="radio" NAME="MentalStat_Gait_1" VALUE="Wide-based" <<MentalStat_Gait_1=Wide-based>> > 
      Wide-based
    <TD CLASS="strcol" >
      <INPUT TYPE="radio" NAME="MentalStat_Gait_1" VALUE="Right leg weakness" <<MentalStat_Gait_1=Right leg weakness>> > 
      Right leg weakness
    <TD CLASS="strcol" >
      <INPUT TYPE="radio" NAME="MentalStat_Gait_1" VALUE="Left leg weakness" <<MentalStat_Gait_1=Left leg weakness>> > 
      Left leg weakness
  </TR>
  <TR >
    <TD CLASS="strcol" WIDTH="20%" >&nbsp;</TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="radio" NAME="MentalStat_Gait_1" VALUE="Cannot be assessed/Bedfast" <<MentalStat_Gait_1=Cannot be assessed/Bedfast>> > 
      Cannot be assessed/Bedfast
    <TD CLASS="strcol" >&nbsp;</TD>
    <TD CLASS="strcol" >&nbsp;</TD>
  </TR>
  <TR><TD CLASS="strcol" COLSPAN="4" >&nbsp;</TD></TR>
  <TR >
    <TD CLASS="strcol" WIDTH="20%" >Motor Behavior
    <TD CLASS="strcol" >
      <INPUT TYPE="radio" NAME="MentalStat_Motor_1" VALUE="Normal" <<MentalStat_Motor_1=Normal>> > 
      Normal
    <TD CLASS="strcol" >
      <INPUT TYPE="radio" NAME="MentalStat_Motor_1" VALUE="Restlessness/Fidgety" <<MentalStat_Motor_1=Restlessness/Fidgety>> > 
      Restlessness/Fidgety
    <TD CLASS="strcol" >
      <INPUT TYPE="radio" NAME="MentalStat_Motor_1" VALUE="Physical Agitation" <<MentalStat_Motor_1=Physical Agitation>> > 
      Physical Agitation
  </TR>
  <TR >
    <TD CLASS="strcol" WIDTH="20%" >&nbsp;</TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="radio" NAME="MentalStat_Motor_1" VALUE="Slowed" <<MentalStat_Motor_1=Slowed>> > 
      Slowed
    <TD CLASS="strcol" >
      <INPUT TYPE="radio" NAME="MentalStat_Motor_1" VALUE="Ideographic/Unusual" <<MentalStat_Motor_1=Ideographic/Unusual>> > 
      Ideographic/Unusual
    <TD CLASS="strcol" >
      <INPUT TYPE="radio" NAME="MentalStat_Motor_1" VALUE="Tremor" <<MentalStat_Motor_1=Tremor>> > 
      Tremor
  </TR>
  <TR >
    <TD CLASS="strcol" WIDTH="20%" >&nbsp;</TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="radio" NAME="MentalStat_Motor_1" VALUE="Tic" <<MentalStat_Motor_1=Tic>> > 
      Tic
    <TD CLASS="strcol" >&nbsp;</TD>
    <TD CLASS="strcol" >&nbsp;</TD>
  </TR>
  <TR><TD CLASS="strcol" COLSPAN="4" >&nbsp;</TD></TR>
    </TABLE></TD></TR>
    <TR ><TD ><TABLE CLASS="home fullsize" >
  <TR ><TD CLASS="hdrtxt" COLSPAN="4" >Speech</TD></TR>
  <TR >
    <TD CLASS="strcol" WIDTH="20%" >Quantity
    <TD CLASS="strcol" >
      <INPUT TYPE="radio" NAME="MentalStat_SpeechQuan_1" VALUE="Normal" <<MentalStat_SpeechQuan_1=Normal>> > 
      Normal
    <TD CLASS="strcol" >
      <INPUT TYPE="radio" NAME="MentalStat_SpeechQuan_1" VALUE="Talkative" <<MentalStat_SpeechQuan_1=Talkative>> > 
      Talkative
    <TD CLASS="strcol" >
      <INPUT TYPE="radio" NAME="MentalStat_SpeechQuan_1" VALUE="Minimally Responsive" <<MentalStat_SpeechQuan_1=Minimally Responsive>> > 
      Minimally Responsive
  </TR>
  <TR >
    <TD CLASS="strcol" WIDTH="20%" >&nbsp;</TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="radio" NAME="MentalStat_SpeechQuan_1" VALUE="Unspontaneous" <<MentalStat_SpeechQuan_1=Unspontaneous>> > 
      Unspontaneous
    <TD CLASS="strcol" >&nbsp;</TD>
    <TD CLASS="strcol" >&nbsp;</TD>
  </TR>
  <TR><TD CLASS="strcol" COLSPAN="4" >&nbsp;</TD></TR>
  <TR >
    <TD CLASS="strcol" WIDTH="20%" >Quality
    <TD CLASS="strcol" >
      <INPUT TYPE="radio" NAME="MentalStat_SpeechQual_1" VALUE="Normal" <<MentalStat_SpeechQual_1=Normal>> > 
      Normal
    <TD CLASS="strcol" >
      <INPUT TYPE="radio" NAME="MentalStat_SpeechQual_1" VALUE="Loud" <<MentalStat_SpeechQual_1=Loud>> > 
      Loud
    <TD CLASS="strcol" >
      <INPUT TYPE="radio" NAME="MentalStat_SpeechQual_1" VALUE="Soft" <<MentalStat_SpeechQual_1=Soft>> > 
      Soft
  </TR>
  <TR >
    <TD CLASS="strcol" WIDTH="20%" >&nbsp;</TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="radio" NAME="MentalStat_SpeechQual_1" VALUE="Rapid" <<MentalStat_SpeechQual_1=Rapid>> > 
      Rapid
    <TD CLASS="strcol" >
      <INPUT TYPE="radio" NAME="MentalStat_SpeechQual_1" VALUE="Slow" <<MentalStat_SpeechQual_1=Slow>> > 
      Slow
    <TD CLASS="strcol" >
      <INPUT TYPE="radio" NAME="MentalStat_SpeechQual_1" VALUE="Pressured" <<MentalStat_SpeechQual_1=Pressured>> > 
      Pressured
  </TR>
  <TR >
    <TD CLASS="strcol" WIDTH="20%" >&nbsp;</TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="radio" NAME="MentalStat_SpeechQual_1" VALUE="Hesitant" <<MentalStat_SpeechQual_1=Hesitant>> > 
      Hesitant
    <TD CLASS="strcol" >
      <INPUT TYPE="radio" NAME="MentalStat_SpeechQual_1" VALUE="Emotional" <<MentalStat_SpeechQual_1=Emotional>> > 
      Emotional
    <TD CLASS="strcol" >
      <INPUT TYPE="radio" NAME="MentalStat_SpeechQual_1" VALUE="Monotonous" <<MentalStat_SpeechQual_1=Monotonous>> > 
      Monotonous
  </TR>
  <TR >
    <TD CLASS="strcol" WIDTH="20%" >&nbsp;</TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="radio" NAME="MentalStat_SpeechQual_1" VALUE="Word Salad" <<MentalStat_SpeechQual_1=Word Salad>> > 
      Word Salad
    <TD CLASS="strcol" >
      <INPUT TYPE="radio" NAME="MentalStat_SpeechQual_1" VALUE="Clanging" <<MentalStat_SpeechQual_1=Clanging>> > 
      Clanging
    <TD CLASS="strcol" >
      <INPUT TYPE="radio" NAME="MentalStat_SpeechQual_1" VALUE="Slurred" <<MentalStat_SpeechQual_1=Slurred>> > 
      Slurred
  </TR>
  <TR >
    <TD CLASS="strcol" WIDTH="20%" >&nbsp;</TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="radio" NAME="MentalStat_SpeechQual_1" VALUE="Stutter" <<MentalStat_SpeechQual_1=Stutter>> > 
      Stutter
    <TD CLASS="strcol" >
      <INPUT TYPE="radio" NAME="MentalStat_SpeechQual_1" VALUE="Unintelligible" <<MentalStat_SpeechQual_1=Unintelligible>> > 
      Unintelligible
    <TD CLASS="strcol" >
      <INPUT TYPE="radio" NAME="MentalStat_SpeechQual_1" VALUE="Language Barrier" <<MentalStat_SpeechQual_1=Language Barrier>> > 
      Language Barrier
  </TR>
  <TR><TD CLASS="strcol" COLSPAN="4" >&nbsp;</TD></TR>
  <TR >
    <TD CLASS="strcol" WIDTH="20%" >Impairment
    <TD CLASS="strcol" >
      <INPUT TYPE="radio" NAME="MentalStat_SpeechImpair_1" VALUE="None Reported" <<MentalStat_SpeechImpair_1=None Reported>> > 
      None Reported
    <TD CLASS="strcol" >
      <INPUT TYPE="radio" NAME="MentalStat_SpeechImpair_1" VALUE="Stuttering" <<MentalStat_SpeechImpair_1=Stuttering>> > 
      Stuttering
    <TD CLASS="strcol" >
      <INPUT TYPE="radio" NAME="MentalStat_SpeechImpair_1" VALUE="Heavy Accent" <<MentalStat_SpeechImpair_1=Heavy Accent>> > 
      Heavy Accent
  </TR>
  <TR >
    <TD CLASS="strcol" WIDTH="20%" >&nbsp;</TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="radio" NAME="MentalStat_SpeechImpair_1" VALUE="Articulation Problem" <<MentalStat_SpeechImpair_1=Articulation Problem>> > 
      Articulation Problem
    <TD CLASS="strcol" >
      <INPUT TYPE="radio" NAME="MentalStat_SpeechImpair_1" VALUE="Aphasia" <<MentalStat_SpeechImpair_1=Aphasia>> > 
      Aphasia
    <TD CLASS="strcol" >
      <INPUT TYPE="radio" NAME="MentalStat_SpeechImpair_1" VALUE="Echolalia" <<MentalStat_SpeechImpair_1=Echolalia>> > 
      Echolalia
  </TR>
  <TR><TD CLASS="strcol" COLSPAN="4" >&nbsp;</TD></TR>
    </TABLE></TD></TR>
    <TR ><TD ><TABLE CLASS="home fullsize" >
  <TR ><TD CLASS="hdrtxt" COLSPAN="4" >Interviewer-Patient Relationship</TD></TR>
  <TR >
    <TD CLASS="strcol" WIDTH="20%" >&nbsp;</TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="radio" NAME="MentalStat_IPRel_1" VALUE="Appropriate" <<MentalStat_IPRel_1=Appropriate>> > 
      Appropriate
    <TD CLASS="strcol" >
      <INPUT TYPE="radio" NAME="MentalStat_IPRel_1" VALUE="Domineering" <<MentalStat_IPRel_1=Domineering>> > 
      Domineering
    <TD CLASS="strcol" >
      <INPUT TYPE="radio" NAME="MentalStat_IPRel_1" VALUE="Submissive" <<MentalStat_IPRel_1=Submissive>> > 
      Submissive
  </TR>
  <TR >
    <TD CLASS="strcol" WIDTH="20%" >&nbsp;</TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="radio" NAME="MentalStat_IPRel_1" VALUE="Provocative" <<MentalStat_IPRel_1=Provocative>> > 
      Provocative
    <TD CLASS="strcol" >
      <INPUT TYPE="radio" NAME="MentalStat_IPRel_1" VALUE="Seductive" <<MentalStat_IPRel_1=Seductive>> > 
      Seductive
    <TD CLASS="strcol" >
      <INPUT TYPE="radio" NAME="MentalStat_IPRel_1" VALUE="Suspicious" <<MentalStat_IPRel_1=Suspicious>> > 
      Suspicious
  </TR>
  <TR >
    <TD CLASS="strcol" WIDTH="20%" >&nbsp;</TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="radio" NAME="MentalStat_IPRel_1" VALUE="Manipulative" <<MentalStat_IPRel_1=Manipulative>> > 
      Manipulative
    <TD CLASS="strcol" >
      <INPUT TYPE="radio" NAME="MentalStat_IPRel_1" VALUE="Uncooperative" <<MentalStat_IPRel_1=Uncooperative>> > 
      Uncooperative
    <TD CLASS="strcol" >&nbsp;</TD>
  </TR>
  <TR><TD CLASS="strcol" COLSPAN="4" >&nbsp;</TD></TR>
    </TABLE></TD></TR>
    <TR ><TD ><TABLE CLASS="home fullsize" >
  <TR><TD CLASS="hdrtxt" COLSPAN="4" >Affect</TD></TR>
  <TR >
    <TD CLASS="strcol" WIDTH="20%" >&nbsp;</TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="radio" NAME="MentalStat_Affect_1" VALUE="Appropriate/Congruent" <<MentalStat_Affect_1=Appropriate/Congruent>> > 
      Appropriate/Congruent
    <TD CLASS="strcol" >
      <INPUT TYPE="radio" NAME="MentalStat_Affect_1" VALUE="Flat" <<MentalStat_Affect_1=Flat>> > 
      Flat
    <TD CLASS="strcol" >
      <INPUT TYPE="radio" NAME="MentalStat_Affect_1" VALUE="Restricted" <<MentalStat_Affect_1=Restricted>> > 
      Restricted
  </TR>
  <TR >
    <TD CLASS="strcol" WIDTH="20%" >&nbsp;</TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="radio" NAME="MentalStat_Affect_1" VALUE="Tearful" <<MentalStat_Affect_1=Tearful>> > 
      Tearful
    <TD CLASS="strcol" >
      <INPUT TYPE="radio" NAME="MentalStat_Affect_1" VALUE="Labile" <<MentalStat_Affect_1=Labile>> > 
      Labile
    <TD CLASS="strcol" >
      <INPUT TYPE="radio" NAME="MentalStat_Affect_1" VALUE="Dramatized" <<MentalStat_Affect_1=Dramatized>> > 
      Dramatized
  </TR>
  <TR >
    <TD CLASS="strcol" WIDTH="20%" >&nbsp;</TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="radio" NAME="MentalStat_Affect_1" VALUE="Contradictory/Incongruent" <<MentalStat_Affect_1=Contradictory/Incongruent>> > 
      Contradictory/Incongruent
    <TD CLASS="strcol" >&nbsp;</TD>
    <TD CLASS="strcol" >&nbsp;</TD>
  </TR>
  <TR><TD CLASS="strcol" COLSPAN="4" >&nbsp;</TD></TR>
    </TABLE></TD></TR>
    <TR ><TD ><TABLE CLASS="home fullsize" >
  <TR><TD CLASS="hdrtxt" COLSPAN="4" >Mood</TD></TR>
  <TR >
    <TD CLASS="strcol" WIDTH="20%" >&nbsp;</TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="radio" NAME="MentalStat_Mood_1" VALUE="Appropriate/Congruent" <<MentalStat_Mood_1=Appropriate/Congruent>> > 
      Appropriate/Congruent
    <TD CLASS="strcol" >
      <INPUT TYPE="radio" NAME="MentalStat_Mood_1" VALUE="Calm" <<MentalStat_Mood_1=Calm>> > 
      Calm
    <TD CLASS="strcol" >
      <INPUT TYPE="radio" NAME="MentalStat_Mood_1" VALUE="Cheerful" <<MentalStat_Mood_1=Cheerful>> > 
      Cheerful
  </TR>
  <TR >
    <TD CLASS="strcol" WIDTH="20%" >&nbsp;</TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="radio" NAME="MentalStat_Mood_1" VALUE="Anxious" <<MentalStat_Mood_1=Anxious>> > 
      Anxious
    <TD CLASS="strcol" >
      <INPUT TYPE="radio" NAME="MentalStat_Mood_1" VALUE="Depressed" <<MentalStat_Mood_1=Depressed>> > 
      Depressed
    <TD CLASS="strcol" >
      <INPUT TYPE="radio" NAME="MentalStat_Mood_1" VALUE="Fearful" <<MentalStat_Mood_1=Fearful>> > 
      Fearful
  </TR>
  <TR >
    <TD CLASS="strcol" WIDTH="20%" >&nbsp;</TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="radio" NAME="MentalStat_Mood_1" VALUE="Sad" <<MentalStat_Mood_1=Sad>> > 
      Sad
    <TD CLASS="strcol" >
      <INPUT TYPE="radio" NAME="MentalStat_Mood_1" VALUE="Pessimistic" <<MentalStat_Mood_1=Pessimistic>> > 
      Pessimistic
    <TD CLASS="strcol" >
      <INPUT TYPE="radio" NAME="MentalStat_Mood_1" VALUE="Optimistic" <<MentalStat_Mood_1=Optimistic>> > 
      Optimistic
  </TR>
  <TR >
    <TD CLASS="strcol" WIDTH="20%" >&nbsp;</TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="radio" NAME="MentalStat_Mood_1" VALUE="Elated" <<MentalStat_Mood_1=Elated>> > 
      Elated
    <TD CLASS="strcol" >
      <INPUT TYPE="radio" NAME="MentalStat_Mood_1" VALUE="Euphoric" <<MentalStat_Mood_1=Euphoric>> > 
      Euphoric
    <TD CLASS="strcol" >
      <INPUT TYPE="radio" NAME="MentalStat_Mood_1" VALUE="Irritable" <<MentalStat_Mood_1=Irritable>> > 
      Irritable
  </TR>
  <TR >
    <TD CLASS="strcol" WIDTH="20%" >&nbsp;</TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="radio" NAME="MentalStat_Mood_1" VALUE="Angry" <<MentalStat_Mood_1=Angry>> > 
      Angry
    <TD CLASS="strcol" >
      <INPUT TYPE="radio" NAME="MentalStat_Mood_1" VALUE="Antagonistic" <<MentalStat_Mood_1=Antagonistic>> > 
      Antagonistic
    <TD CLASS="strcol" >
      <INPUT TYPE="radio" NAME="MentalStat_Mood_1" VALUE="Apathetic" <<MentalStat_Mood_1=Apathetic>> > 
      Apathetic
  </TR>
  <TR><TD CLASS="strcol" COLSPAN="4" >&nbsp;</TD></TR>
    </TABLE></TD></TR>
    <TR ><TD ><TABLE CLASS="home fullsize" >
  <TR><TD CLASS="hdrtxt" COLSPAN="4" >Thought Processes<BR>(Check all that apply)</TD></TR>
  <TR >
    <TD CLASS="strcol" WIDTH="20%" >&nbsp;</TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="checkbox" NAME="MentalStat_Logical_1" VALUE=1 <<MentalStat_Logical_1=checkbox>> > 
      Logical and Coherent
    <TD CLASS="strcol" >
      <INPUT TYPE="checkbox" NAME="MentalStat_Egocentric_1" VALUE=1 <<MentalStat_Egocentric_1=checkbox>> > 
      Egocentric
    <TD CLASS="strcol" >
      <INPUT TYPE="checkbox" NAME="MentalStat_Blocking_1" VALUE=1 <<MentalStat_Blocking_1=checkbox>> > 
      Blocking
  </TR>
  <TR >
    <TD CLASS="strcol" WIDTH="20%" >&nbsp;</TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="checkbox" NAME="MentalStat_Circumstantial_1" VALUE=1 <<MentalStat_Circumstantial_1=checkbox>> > 
      Circumstantial
    <TD CLASS="strcol" >
      <INPUT TYPE="checkbox" NAME="MentalStat_Tangential_1" VALUE=1 <<MentalStat_Tangential_1=checkbox>> > 
      Tangential
    <TD CLASS="strcol" >
      <INPUT TYPE="checkbox" NAME="MentalStat_Incoherent_1" VALUE=1 <<MentalStat_Incoherent_1=checkbox>> > 
      Incoherent
  </TR>
  <TR >
    <TD CLASS="strcol" WIDTH="20%" >&nbsp;</TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="checkbox" NAME="MentalStat_Flight_1" VALUE=1 <<MentalStat_Flight_1=checkbox>> > 
      Flight of Ideas
    <TD CLASS="strcol" >
      <INPUT TYPE="checkbox" NAME="MentalStat_Neologisms_1" VALUE=1 <<MentalStat_Neologisms_1=checkbox>> > 
      Neologisms
    <TD CLASS="strcol" >
      <INPUT TYPE="checkbox" NAME="MentalStat_Perseveration_1" VALUE=1 <<MentalStat_Perseveration_1=checkbox>> > 
      Perseveration
  </TR>
  <TR >
    <TD CLASS="strcol" WIDTH="20%" >&nbsp;</TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="checkbox" NAME="MentalStat_Evasive_1" VALUE=1 <<MentalStat_Evasive_1=checkbox>> > 
      Evasive
    <TD CLASS="strcol" >
      <INPUT TYPE="checkbox" NAME="MentalStat_Distracted_1" VALUE=1 <<MentalStat_Distracted_1=checkbox>> > 
      Distracted
    <TD CLASS="strcol" >
      <INPUT TYPE="checkbox" NAME="MentalStat_Loose_1" VALUE=1 <<MentalStat_Loose_1=checkbox>> > 
      Loose Associations
  </TR>
  <TR >
    <TD CLASS="strcol" WIDTH="20%" >&nbsp;</TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="checkbox" NAME="MentalStat_Clang_1" VALUE=1 <<MentalStat_Clang_1=checkbox>> > 
      Clang Associations
    <TD CLASS="strcol" >
      <INPUT TYPE="checkbox" NAME="MentalStat_Autistic_1" VALUE=1 <<MentalStat_Autistic_1=checkbox>> > 
      Autistic
    <TD CLASS="strcol" >
      <INPUT TYPE="checkbox" NAME="MentalStat_Magical_1" VALUE=1 <<MentalStat_Magical_1=checkbox>> > 
      Magical
  </TR>
  <TR><TD CLASS="strcol" COLSPAN="4" >&nbsp;</TD></TR>
    </TABLE></TD></TR>
    <TR ><TD ><TABLE CLASS="home fullsize" >
  <TR><TD CLASS="hdrtxt" COLSPAN="4" >Preoccupations<BR>(Check all that apply)</TD></TR>
  <TR >
    <TD CLASS="strcol" WIDTH="20%" >&nbsp;
    <TD CLASS="strcol" >
      <INPUT TYPE="checkbox" NAME="MentalStat_PONR_1" VALUE=1 <<MentalStat_PONR_1=checkbox>> > 
      None Reported
    <TD CLASS="strcol" >
      <INPUT TYPE="checkbox" NAME="MentalStat_Obsessions_1" VALUE=1 <<MentalStat_Obsessions_1=checkbox>> > 
      Obsessions
    <TD CLASS="strcol" >
      <INPUT TYPE="checkbox" NAME="MentalStat_Compulsions_1" VALUE=1 <<MentalStat_Compulsions_1=checkbox>> > 
      Compulsions
  </TR>
  <TR >
    <TD CLASS="strcol" WIDTH="20%" >&nbsp;
    <TD CLASS="strcol" >
      <INPUT TYPE="checkbox" NAME="MentalStat_Phobias_1" VALUE=1 <<MentalStat_Phobias_1=checkbox>> > 
      Phobias
    <TD CLASS="strcol" >
      <INPUT TYPE="checkbox" NAME="MentalStat_Suicide_1" VALUE=1 <<MentalStat_Suicide_1=checkbox>> > 
      Suicide
    <TD CLASS="strcol" >
      <INPUT TYPE="checkbox" NAME="MentalStat_Violent_1" VALUE=1 <<MentalStat_Violent_1=checkbox>> > 
      Violent Acts
  </TR>
  <TR >
    <TD CLASS="strcol" WIDTH="20%" >&nbsp;
    <TD CLASS="strcol" >
      <INPUT TYPE="checkbox" NAME="MentalStat_SomaticConcerns_1" VALUE=1 <<MentalStat_SomaticConcerns_1=checkbox>> > 
      Somatic Concerns
    <TD CLASS="strcol" >
      <INPUT TYPE="checkbox" NAME="MentalStat_Worthlessness_1" VALUE=1 <<MentalStat_Worthlessness_1=checkbox>> > 
      Worthlessness
    <TD CLASS="strcol" >
      <INPUT TYPE="checkbox" NAME="MentalStat_Guilt_1" VALUE=1 <<MentalStat_Guilt_1=checkbox>> > 
      Guilt
  </TR>
  <TR >
    <TD CLASS="strcol" WIDTH="20%" >&nbsp;
    <TD CLASS="strcol" >
      <INPUT TYPE="checkbox" NAME="MentalStat_Sex_1" VALUE=1 <<MentalStat_Sex_1=checkbox>> > 
      Sex
    <TD CLASS="strcol" >
      <INPUT TYPE="checkbox" NAME="MentalStat_ReligiousIssues_1" VALUE=1 <<MentalStat_ReligiousIssues_1=checkbox>> > 
      Religious Issues
    <TD CLASS="strcol" >
      <INPUT TYPE="checkbox" NAME="MentalStat_RetAuthority_1" VALUE=1 <<MentalStat_RetAuthority_1=checkbox>> > 
      Retribution Authority
  </TR>
  <TR >
    <TD CLASS="strcol" WIDTH="20%" >&nbsp;
    <TD CLASS="strcol" >
      <INPUT TYPE="checkbox" NAME="MentalStat_RetFamily_1" VALUE=1 <<MentalStat_RetFamily_1=checkbox>> > 
      Retribution peers/family
    <TD CLASS="strcol" >&nbsp;
    <TD CLASS="strcol" >&nbsp;
  </TR>
  <TR >
    <TD CLASS="strcol" WIDTH="20%" >&nbsp;
    <TD CLASS="strcol" COLSPAN="3" >
      <INPUT TYPE="checkbox" NAME="MentalStat_POOther_1" VALUE=1 <<MentalStat_POOther_1=checkbox>> > 
      Other
      <INPUT TYPE=text NAME="MentalStat_POOtherDesc_1" VALUE="<<MentalStat_POOtherDesc_1>>" SIZE=50>
    </TABLE></TD></TR>
    <TR ><TD ><TABLE CLASS="home fullsize" >
  <TR><TD CLASS="hdrtxt" COLSPAN="4" >Delusions<BR>(Check all that apply)</TD></TR>
  <TR >
    <TD CLASS="strcol" WIDTH="20%" >&nbsp;
    <TD CLASS="strcol" >
      <INPUT TYPE="checkbox" NAME="MentalStat_DLNR_1" VALUE=1 <<MentalStat_DLNR_1=checkbox>> > 
      None Reported
    <TD CLASS="strcol" >
      <INPUT TYPE="checkbox" NAME="MentalStat_PerFamily_1" VALUE=1 <<MentalStat_PerFamily_1=checkbox>> > 
      Persecution peers/family
    <TD CLASS="strcol" >
      <INPUT TYPE="checkbox" NAME="MentalStat_PerAuthority_1" VALUE=1 <<MentalStat_PerAuthority_1=checkbox>> > 
      Persecution Authority
  </TR>
  <TR >
    <TD CLASS="strcol" WIDTH="20%" >&nbsp;
    <TD CLASS="strcol" >
      <INPUT TYPE="checkbox" NAME="MentalStat_SomaticComplaints_1" VALUE=1 <<MentalStat_SomaticComplaints_1=checkbox>> > 
      Somatic Complaints
    <TD CLASS="strcol" >
      <INPUT TYPE="checkbox" NAME="MentalStat_IdeasOfRef_1" VALUE=1 <<MentalStat_IdeasOfRef_1=checkbox>> > 
      Ideas Of Reference
    <TD CLASS="strcol" >
      <INPUT TYPE="checkbox" NAME="MentalStat_Broadcasting_1" VALUE=1 <<MentalStat_Broadcasting_1=checkbox>> > 
      Thought Broadcasting
  </TR>
  <TR >
    <TD CLASS="strcol" WIDTH="20%" >&nbsp;
    <TD CLASS="strcol" >
      <INPUT TYPE="checkbox" NAME="MentalStat_Jealousy_1" VALUE=1 <<MentalStat_Jealousy_1=checkbox>> > 
      Jealousy
    <TD CLASS="strcol" >
      <INPUT TYPE="checkbox" NAME="MentalStat_Grandiosity_1" VALUE=1 <<MentalStat_Grandiosity_1=checkbox>> > 
      Grandiosity
    <TD CLASS="strcol" >
      <INPUT TYPE="checkbox" NAME="MentalStat_Influenced_1" VALUE=1 <<MentalStat_Influenced_1=checkbox>> > 
      Influenced by others
  </TR>
  <TR >
    <TD CLASS="strcol" WIDTH="20%" >&nbsp;
    <TD CLASS="strcol" >
      <INPUT TYPE="checkbox" NAME="MentalStat_Religious_1" VALUE=1 <<MentalStat_Religious_1=checkbox>> > 
      Religious
    <TD CLASS="strcol" >
      <INPUT TYPE="checkbox" NAME="MentalStat_Control_1" VALUE=1 <<MentalStat_Control_1=checkbox>> > 
      Control
    <TD CLASS="strcol" >&nbsp;
  </TR>
  <TR >
    <TD CLASS="strcol" WIDTH="20%" >&nbsp;
    <TD CLASS="strcol" COLSPAN="3" >
      <INPUT TYPE="checkbox" NAME="MentalStat_DLOther_1" VALUE=1 <<MentalStat_DLOther_1=checkbox>> > 
      Other
      <INPUT TYPE=text NAME="MentalStat_DLOtherDesc_1" VALUE="<<MentalStat_DLOtherDesc_1>>" SIZE=50>
    </TABLE></TD></TR>
    <TR ><TD ><TABLE CLASS="home fullsize" >
  <TR><TD CLASS="hdrtxt" COLSPAN="4" >Hallucinations<BR>(Check all that apply)</TD></TR>
  <TR >
    <TD CLASS="strcol" WIDTH="20%" >&nbsp;
    <TD CLASS="strcol" >
      <INPUT TYPE="checkbox" NAME="MentalStat_HLNR_1" VALUE=1 <<MentalStat_HLNR_1=checkbox>> > 
      None Reported
    <TD CLASS="strcol" >
      <INPUT TYPE="checkbox" NAME="MentalStat_Auditory_1" VALUE=1 <<MentalStat_Auditory_1=checkbox>> > 
      Auditory
    <TD CLASS="strcol" >
      <INPUT TYPE="checkbox" NAME="MentalStat_Visual_1" VALUE=1 <<MentalStat_Visual_1=checkbox>> > 
      Visual
  </TR>
  <TR >
    <TD CLASS="strcol" WIDTH="20%" >&nbsp;
    <TD CLASS="strcol" >
      <INPUT TYPE="checkbox" NAME="MentalStat_Olfactory_1" VALUE=1 <<MentalStat_Olfactory_1=checkbox>> > 
      Olfactory
    <TD CLASS="strcol" >
      <INPUT TYPE="checkbox" NAME="MentalStat_Kinesthetic_1" VALUE=1 <<MentalStat_Kinesthetic_1=checkbox>> > 
      Kinesthetic
    <TD CLASS="strcol" >&nbsp;
    </TABLE></TD></TR>
    <TR ><TD ><TABLE CLASS="home fullsize" >
  <TR><TD CLASS="hdrtxt" COLSPAN="4" >Consciousness<BR>(Check all that apply)</TD></TR>
  <TR >
    <TD CLASS="strcol" WIDTH="20%" >&nbsp;
    <TD CLASS="strcol" >
      <INPUT TYPE="checkbox" NAME="MentalStat_Alert_1" VALUE=1 <<MentalStat_Alert_1=checkbox>> > 
      Alert
      &nbsp; &nbsp;
      <INPUT TYPE="checkbox" NAME="MentalStat_Lethargy_1" VALUE=1 <<MentalStat_Lethargy_1=checkbox>> > 
      Lethargy
    <TD CLASS="strcol" >
      <INPUT TYPE="checkbox" NAME="MentalStat_Stupor_1" VALUE=1 <<MentalStat_Stupor_1=checkbox>> > 
      Stupor
      &nbsp; &nbsp;
      <INPUT TYPE="checkbox" NAME="MentalStat_Coma_1" VALUE=1 <<MentalStat_Coma_1=checkbox>> > 
      Coma
    <TD CLASS="strcol" >&nbsp;
  </TR>
  <TR >
    <TD CLASS="strcol" WIDTH="20%" >&nbsp;
    <TD CLASS="strcol" COLSPAN="3" >
      <INPUT TYPE="checkbox" NAME="MentalStat_Faint_1" VALUE=1 <<MentalStat_Faint_1=checkbox>> > 
      Recent history of loss of consciousness
  </TR>
  <TR >
    <TD CLASS="strcol" WIDTH="20%" >&nbsp;
    <TD CLASS="strcol" COLSPAN="3" >
      <INPUT TYPE="checkbox" NAME="MentalStat_Seizures_1" VALUE=1 <<MentalStat_Seizures_1=checkbox>> > 
      Recent history of seizures
  </TR>
  <TR >
    <TD CLASS="strcol" WIDTH="20%" >&nbsp;
    <TD CLASS="strcol" COLSPAN="3" >
      <INPUT TYPE="checkbox" NAME="MentalStat_Blackouts_1" VALUE=1 <<MentalStat_Blackouts_1=checkbox>> > 
      Recent history of blackouts
    </TABLE></TD></TR>
</TABLE>
<TABLE CLASS="home fullsize" >
    <TR ><TD ><TABLE CLASS="home fullsize" >
  <TR ><TD CLASS="hdrtxt" COLSPAN="3" >Orientation</TD></TR>
  <TR >
    <TD CLASS="strcol" WIDTH="20%" >&nbsp;
    <TD CLASS="strcol" >
      <INPUT TYPE="radio" NAME="MentalStat_Orientation_1" VALUE="Oriented in all spheres" <<MentalStat_Orientation_1=Oriented in all spheres>> > 
      Oriented in all spheres (including situation)
    </TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="radio" NAME="MentalStat_Orientation_1" VALUE="Oriented to Person Only" <<MentalStat_Orientation_1=Oriented to Person Only>> > 
      Oriented to Person Only
    </TD>
  </TR>
  <TR >
    <TD CLASS="strcol" WIDTH="20%" >&nbsp;
    <TD CLASS="strcol" >
      <INPUT TYPE="radio" NAME="MentalStat_Orientation_1" VALUE="Oriented to Person and Place Only" <<MentalStat_Orientation_1=Oriented to Person and Place Only>> > 
      Oriented to Person and Place Only
    </TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="radio" NAME="MentalStat_Orientation_1" VALUE="Oriented to Person and Time Only" <<MentalStat_Orientation_1=Oriented to Person and Time Only>> > 
      Oriented to Person and Time Only
    </TD>
  </TR>
    </TABLE></TD></TR>
    <TR ><TD ><TABLE CLASS="home fullsize" >
  <TR><TD CLASS="hdrtxt" COLSPAN="3" >Attention/Concentration<BR>(Serial 7's WORLD backwards)</TD></TR>
  <TR >
    <TD CLASS="strcol" WIDTH="20%" >&nbsp;
    <TD CLASS="strcol" >
      <INPUT TYPE="radio" NAME="MentalStat_Attention_1" VALUE="Normal" <<MentalStat_Attention_1=Normal>> > 
      Normal
    <TD CLASS="strcol" >
      <INPUT TYPE="radio" NAME="MentalStat_Attention_1" VALUE="Mildly Impaired" <<MentalStat_Attention_1=Mildly Impaired>> > 
      Mildly Impaired
  </TR>
  <TR >
    <TD CLASS="strcol" WIDTH="20%" >&nbsp;
    <TD CLASS="strcol" >
      <INPUT TYPE="radio" NAME="MentalStat_Attention_1" VALUE="Moderately Impaired" <<MentalStat_Attention_1=Moderately Impaired>> > 
      Moderately Impaired
    </TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="radio" NAME="MentalStat_Attention_1" VALUE="Severely Impaired" <<MentalStat_Attention_1=Severely Impaired>> > 
      Severely Impaired
    </TD>
  </TR>
    </TABLE></TD></TR>
    <TR ><TD ><TABLE CLASS="home fullsize" >
  <TR ><TD CLASS="hdrtxt" COLSPAN="3" >Memory</TD></TR>
  <TR >
    <TD CLASS="strcol" WIDTH="20%" >&nbsp;
    <TD CLASS="strcol" >
      <INPUT TYPE="radio" NAME="MentalStat_Memory_1" VALUE="Intact" <<MentalStat_Memory_1=Intact>> > 
      Intact
    </TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="radio" NAME="MentalStat_Memory_1" VALUE="Immediate Memory Deficit" <<MentalStat_Memory_1=Immediate Memory Deficit>> > 
      Immediate Memory Deficit
    </TD>
  </TR>
  <TR >
    <TD CLASS="strcol" WIDTH="20%" >&nbsp;
    <TD CLASS="strcol" >
      <INPUT TYPE="radio" NAME="MentalStat_Memory_1" VALUE="Recent Memory Deficit" <<MentalStat_Memory_1=Recent Memory Deficit>> > 
      Recent Memory Deficit
    </TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="radio" NAME="MentalStat_Memory_1" VALUE="Remote Memory Deficit" <<MentalStat_Memory_1=Remote Memory Deficit>> > 
      Remote Memory Deficit
    </TD>
  </TR>
    </TABLE></TD></TR>
    <TR ><TD ><TABLE CLASS="home fullsize" >
  <TR><TD CLASS="hdrtxt" COLSPAN="3" >Estimated Intellectual Ability</TD></TR>
  <TR >
    <TD CLASS="strcol" WIDTH="20%" >&nbsp;
    <TD CLASS="strcol" >
      <INPUT TYPE="radio" NAME="MentalStat_IntAbility_1" VALUE="Superior" <<MentalStat_IntAbility_1=Superior>> > 
      Superior
    </TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="radio" NAME="MentalStat_IntAbility_1" VALUE="Above Average" <<MentalStat_IntAbility_1=Above Average>> > 
      Above Average
    </TD>
  </TR>
  <TR >
    <TD CLASS="strcol" WIDTH="20%" >&nbsp;
    <TD CLASS="strcol" >
      <INPUT TYPE="radio" NAME="MentalStat_IntAbility_1" VALUE="Average" <<MentalStat_IntAbility_1=Average>> > 
      Average
    </TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="radio" NAME="MentalStat_IntAbility_1" VALUE="Below Average" <<MentalStat_IntAbility_1=Below Average>> > 
      Below Average
    </TD>
  </TR>
  <TR >
    <TD CLASS="strcol" WIDTH="20%" >&nbsp;
    <TD CLASS="strcol" >
      <INPUT TYPE="radio" NAME="MentalStat_IntAbility_1" VALUE="Borderline Developmentally Disabled" <<MentalStat_IntAbility_1=Borderline Developmentally Disabled>> > 
      Borderline Developmentally Disabled
    </TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="radio" NAME="MentalStat_IntAbility_1" VALUE="Developmentally Disabled" <<MentalStat_IntAbility_1=Developmentally Disabled>> > 
      Developmentally Disabled
    </TD>
  </TR>
    </TABLE></TD></TR>
    <TR ><TD ><TABLE CLASS="home fullsize" >
  <TR ><TD CLASS="hdrtxt" COLSPAN="3" >Insight</TD></TR>
  <TR >
    <TD CLASS="strcol" WIDTH="20%" >&nbsp;
    <TD CLASS="strcol" >
      <INPUT TYPE="radio" NAME="MentalStat_Insight_1" VALUE="Good/Full Ownership of Problems" <<MentalStat_Insight_1=Good/Full Ownership of Problems>> > 
      Good/Full Ownership of Problems
    </TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="radio" NAME="MentalStat_Insight_1" VALUE="Fair/Partial Ownership of Problems" <<MentalStat_Insight_1=Fair/Partial Ownership of Problems>> > 
      Fair/Partial Ownership of Problems
    </TD>
  </TR>
  <TR >
    <TD CLASS="strcol" WIDTH="20%" >&nbsp;
    <TD CLASS="strcol" >
      <INPUT TYPE="radio" NAME="MentalStat_Insight_1" VALUE="Poor/Blames Others for Problems" <<MentalStat_Insight_1=Poor/Blames Others for Problems>> > 
      Poor/Blames Others for Problems
    </TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="radio" NAME="MentalStat_Insight_1" VALUE="Extremely Limited/Does Not Recognize Problems" <<MentalStat_Insight_1=Extremely Limited/Does Not Recognize Problems>> > 
      Extremely Limited/Does Not Recognize Problems
    </TD>
  </TR>
    </TABLE></TD></TR>
    <TR ><TD ><TABLE CLASS="home fullsize" >
  <TR ><TD CLASS="hdrtxt" COLSPAN="3" >Judgement<BR>(Ability to Delay Gratification)</TD></TR>
  <TR >
    <TD CLASS="strcol" WIDTH="20%" >&nbsp;
    <TD CLASS="strcol" >
      <INPUT TYPE="radio" NAME="MentalStat_Judgement_1" VALUE="Good" <<MentalStat_Judgement_1=Good>> > 
      Good
    </TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="radio" NAME="MentalStat_Judgement_1" VALUE="Fair" <<MentalStat_Judgement_1=Fair>> > 
      Fair
    </TD>
  </TR>
  <TR >
    <TD CLASS="strcol" WIDTH="20%" >&nbsp;
    <TD CLASS="strcol" >
      <INPUT TYPE="radio" NAME="MentalStat_Judgement_1" VALUE="Poor" <<MentalStat_Judgement_1=Poor>> > 
      Poor
    </TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="radio" NAME="MentalStat_Judgement_1" VALUE="Impaired" <<MentalStat_Judgement_1=Impaired>> > 
      Problems
    </TD>
  </TR>
    </TABLE></TD></TR>
    <TR ><TD ><TABLE CLASS="home fullsize" >
  <TR ><TD CLASS="hdrtxt" COLSPAN="3" >Skills of Independence</TD></TR>
  <TR >
    <TD CLASS="strcol" WIDTH="20%" >&nbsp;
    <TD CLASS="strcol" >
      <INPUT TYPE="radio" NAME="MentalStat_Independence_1" VALUE="Good/Manage All Life Decisions" <<MentalStat_Independence_1=Good/Manage All Life Decisions>> > 
      Good/Manage All Life Decisions
    </TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="radio" NAME="MentalStat_Independence_1" VALUE="Fair/Impaired Financial Ability" <<MentalStat_Independence_1=Fair/Impaired Financial Ability>> > 
      Fair/Impaired Financial Ability
    </TD>
  </TR>
  <TR >
    <TD CLASS="strcol" WIDTH="20%" >&nbsp;
    <TD CLASS="strcol" >
      <INPUT TYPE="radio" NAME="MentalStat_Independence_1" VALUE="Poor/Impaired ADL Management" <<MentalStat_Independence_1=Poor/Impaired ADL Management>> > 
      Poor/Impaired ADL Management
    </TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="radio" NAME="MentalStat_Independence_1" VALUE="Impaired/Requires Custodian" <<MentalStat_Independence_1=Impaired/Requires Custodian>> > 
      Impaired/Requires Custodian
    </TD>
    </TD>
  </TR>
    </TABLE></TD></TR>
    <TR ><TD ><TABLE CLASS="home fullsize" >
  <TR ><TD CLASS="hdrtxt" COLSPAN="2" >Mental Status Exam Screen</TD></TR>
  <TR>
    <TD CLASS="strcol" WIDTH="20%" >&nbsp;</TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="radio" NAME="MentalStat_MentalExam_1" VALUE=1 <<MentalStat_MentalExam_1=1>> > Positive
      <INPUT TYPE="radio" NAME="MentalStat_MentalExam_1" VALUE=0 <<MentalStat_MentalExam_1=0>> > Negative
    </TD>
  </TR>
  <TR ><TD CLASS="hdrtxt" COLSPAN="2" >MMSE score (if administered 0-30)</TD></TR>
  <TR>
    <TD CLASS="hdrtxt" COLSPAN="2" >
      <INPUT TYPE="TEXT" NAME="MentalStat_MMSE_1" VALUE="<<MentalStat_MMSE_1>>" ONFOCUS="select()" ONCHANGE="vNum(this,0,30)" SIZE="6" >
    </TD>
  </TR>
    </TABLE></TD></TR>
</TABLE>

<TABLE CLASS="main fullsize" >
  <TR >
    <TD CLASS="numcol" >
      <INPUT TYPE="submit" ONCLICK="return validate(this.form);" NAME="UpdateTables=all&[[myForm->genLink(ClientIntake+ClientIntSum.cgi)]]" VALUE="Add/Update -> Interpretive Summary">
      <INPUT TYPE="submit" ONCLICK="return validate(this.form);" NAME="UpdateTables=all&misPOP=1" VALUE="Add/Update">
    </TD>
  </TR>
</TABLE>

</LOADHIDDEN>
</FORM>
<SCRIPT LANGUAGE="JavaScript">
document.MentalStat.elements[0].focus();
</SCRIPT>

[[myHTML->rightpane(%form+search)]]
