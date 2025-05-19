[[myHTML->newPage(%form+CAR Scores)]]

<SCRIPT LANGUAGE="JavaScript" SRC="/src/cgi/js/chkLock.js"> </SCRIPT>
<SCRIPT LANGUAGE="JavaScript" SRC="/src/cgi/js/vEntry.js"> </SCRIPT>
<SCRIPT LANGUAGE="JavaScript" SRC="/src/cgi/js/vPDDom.js"> </SCRIPT>
<SCRIPT LANGUAGE="JavaScript" SRC="/src/cgi/js/vNum.js"> </SCRIPT>

<FORM NAME="PDDom" ACTION="/src/cgi/bin/mis.cgi" METHOD="POST" >
<TABLE CLASS="main fullsize" >
  <TR >
    <TD CLASS="strcol" >
      <<<Client_FName_1>>> <<<Client_MName_1>>> <<<Client_LName_1>>> (<<<Client_ClientID_1>>>) <<<Client_SSN_1>>>
      <BR>
      Client's CAR Scores
    </TD>
    <TD CLASS="numcol" >[[gHTML->setLINKS(%form+back)]]</TD>
  </TR>
</TABLE>
<TABLE CLASS="home fullsize" >
    <TR ><TD ><TABLE CLASS="home fullsize" >
  <TR><TD CLASS="heading" COLSPAN="3" >Level of Treatment: <<<ClientPrAuth_TL_1>>></TD></TR>
  <TR><TD CLASS="hdrtxt" COLSPAN="3" >Document descriptive symptoms below for each domain and score</TD></TR>
  <TR><TD CLASS="rptmsg" COLSPAN="3" >Leave Any Inapplicable Fields Blank</TD></TR>
  <TR>
    <TD CLASS="hdrcol" >1-9=Above Average</TD>
    <TD CLASS="hdrcol" >10-19=Average</TD>
    <TD CLASS="hdrcol" >20-29=Slight</TD>
  </TR>
  <TR>
    <TD CLASS="hdrcol" >30-39=Moderate</TD>
    <TD CLASS="hdrcol" >40-49=Severe</TD>
    <TD CLASS="hdrcol" >50=Extreme Impairment</TD>
  </TR>
  <TR >
    <TD CLASS="port hdrtxt" COLSPAN="2" >1. FEELING/MOOD AFFECT</TD>
    </TD>
    <TD CLASS="port numcol" >SCORE:
      <INPUT TYPE="TEXT" NAME="PDDom_Dom1Score_1" VALUE="<<PDDom_Dom1Score_1>>" ONFOCUS="select()" ONCHANGE="vNum(this,1,50)" SIZE=6>
    </TD>
  </TR>
  <TR >
    <TD CLASS="strcol" COLSPAN="3" >Problem areas:<BR>
      <INPUT TYPE="checkbox" NAME="PDDom_Dom1Mood_1" VALUE=1 <<PDDom_Dom1Mood_1=1>> ONFOCUS="select()" >
      Mood lability
      <INPUT TYPE="checkbox" NAME="PDDom_Dom1Coping_1" VALUE=1 <<PDDom_Dom1Coping_1=1>> ONFOCUS="select()" >
      Coping skills
      <INPUT TYPE="checkbox" NAME="PDDom_Dom1Suicidal_1" VALUE=1 <<PDDom_Dom1Suicidal_1=1>> ONFOCUS="select()" >
      Suicidal/homicidal ideation/plan
      <INPUT TYPE="checkbox" NAME="PDDom_Dom1Depression_1" VALUE=1 <<PDDom_Dom1Depression_1=1>> ONFOCUS="select()" >
      Depression
    </TD>
  </TR>
  <TR >
    <TD CLASS="strcol" COLSPAN="3" >
      <INPUT TYPE="checkbox" NAME="PDDom_Dom1Anger_1" VALUE=1 <<PDDom_Dom1Anger_1=1>> ONFOCUS="select()" >
      Anger
      <INPUT TYPE="checkbox" NAME="PDDom_Dom1Anxiety_1" VALUE=1 <<PDDom_Dom1Anxiety_1=1>> ONFOCUS="select()" >
      Anxiety
      <INPUT TYPE="checkbox" NAME="PDDom_Dom1Euphoria_1" VALUE=1 <<PDDom_Dom1Euphoria_1=1>> ONFOCUS="select()" >
      Euphoria
      <INPUT TYPE="checkbox" NAME="PDDom_Dom1Change_1" VALUE=1 <<PDDom_Dom1Change_1=1>> ONFOCUS="select()" >
      Change in appetite/sleep patterns
    </TD>
  </TR>
  <TR >
    <TD CLASS="strcol" COLSPAN="3" >Evidenced by (specific examples, symptom frequency, duration and internsity)<BR>
      <TEXTAREA NAME="PDDom_Dom1Text_1" COLS="80" ROWS="5" WRAP="virtual" ONFOCUS="select()" ><<PDDom_Dom1Text_1>></TEXTAREA>
    </TD>
  </TR>
  <TR >
    <TD CLASS="port hdrtxt" COLSPAN="2" >2. THINKING/MENTAL PROCESS</TD>
    <TD CLASS="port numcol" >SCORE:
      <INPUT TYPE="TEXT" NAME="PDDom_Dom2Score_1" VALUE="<<PDDom_Dom2Score_1>>" ONFOCUS="select()" ONCHANGE="vNum(this,1,50)" SIZE=6>
    </TD>
  </TR>
  <TR >
    <TD CLASS="strcol" COLSPAN="3" >
      Oriented x (0-4)
      <INPUT TYPE="TEXT" NAME="PDDom_Dom2Oriented_1" VALUE="<<PDDom_Dom2Oriented_1>>" ONFOCUS="select()" ONCHANGE="vNum(this,0,4)" SIZE=6>
      MMSE score (if administered 0-30)
      <INPUT TYPE="TEXT" NAME="PDDom_Dom2MMSE_1" VALUE="<<PDDom_Dom2MMSE_1>>" ONFOCUS="select()" ONCHANGE="vNum(this,0,30)" SIZE=6>
    </TD>
  </TR>
  <TR >
    <TD CLASS="strcol" COLSPAN="3" >Problem areas:<BR>
      <INPUT TYPE="checkbox" NAME="PDDom_Dom2Memory_1" VALUE=1 <<PDDom_Dom2Memory_1=1>> ONFOCUS="select()" >
      Memory
      <INPUT TYPE="checkbox" NAME="PDDom_Dom2Cognitive_1" VALUE=1 <<PDDom_Dom2Cognitive_1=1>> ONFOCUS="select()" >
      Cognitive process
      <INPUT TYPE="checkbox" NAME="PDDom_Dom2Concentration_1" VALUE=1 <<PDDom_Dom2Concentration_1=1>> ONFOCUS="select()" >
      Concentration
      <INPUT TYPE="checkbox" NAME="PDDom_Dom2Judgment_1" VALUE=1 <<PDDom_Dom2Judgment_1=1>> ONFOCUS="select()" >
      Judgment
      <INPUT TYPE="checkbox" NAME="PDDom_Dom2Obsessions_1" VALUE=1 <<PDDom_Dom2Obsessions_1=1>> ONFOCUS="select()" >
      Obsessions
      <INPUT TYPE="checkbox" NAME="PDDom_Dom2Delusions_1" VALUE=1 <<PDDom_Dom2Delusions_1=1>> ONFOCUS="select()" >
      Delusions/hallucinations
    </TD>
  </TR>
  <TR >
    <TD CLASS="strcol" COLSPAN="3" >
      <INPUT TYPE="checkbox" NAME="PDDom_Dom2Belief_1" VALUE=1 <<PDDom_Dom2Belief_1=1>> ONFOCUS="select()" >
      Belief system
      <INPUT TYPE="checkbox" NAME="PDDom_Dom2Learning_1" VALUE=1 <<PDDom_Dom2Learning_1=1>> ONFOCUS="select()" >
      Learning disabilities
      <INPUT TYPE="checkbox" NAME="PDDom_Dom2Impulse_1" VALUE=1 <<PDDom_Dom2Impulse_1=1>> ONFOCUS="select()" >
      Impulse Control
    </TD>
  </TR>
  <TR >
    <TD CLASS="strcol" COLSPAN="3" >Evidenced by (specific examples, symptom frequency, duration and intensity)<BR>
      <TEXTAREA NAME="PDDom_Dom2Text_1" COLS="80" ROWS="5" WRAP="virtual" ONFOCUS="select()" ><<PDDom_Dom2Text_1>></TEXTAREA>
    </TD>
  </TR>
  <TR >
    <TD CLASS="port hdrtxt" COLSPAN="2" >3. SUBSTANCE USE</TD>
    <TD CLASS="port numcol" >SCORE:
      <INPUT TYPE="TEXT" NAME="PDDom_Dom3Score_1" VALUE="<<PDDom_Dom3Score_1>>" ONFOCUS="select()" ONCHANGE="vNum(this,1,50)" SIZE=6>
    </TD>
  </TR>
  <TR >
    <TD CLASS="strcol" COLSPAN="3" >Functional impact of current use<BR>
      <TEXTAREA NAME="PDDom_Dom3Text_1" COLS="80" ROWS="5" WRAP="virtual" ONFOCUS="select()" ><<PDDom_Dom3Text_1>></TEXTAREA>
    </TD>
  </TR>
  <TR >
    <TD CLASS="port hdrtxt" COLSPAN="2" >4. MEDICAL/PHYSICAL</TD>
    <TD CLASS="port numcol" >SCORE:
      <INPUT TYPE="TEXT" NAME="PDDom_Dom4Score_1" VALUE="<<PDDom_Dom4Score_1>>" ONFOCUS="select()" ONCHANGE="vNum(this,1,50)" SIZE=6>
    </TD>
  </TR>
  <TR >
    <TD CLASS="strcol" COLSPAN="3" >Impact/limitations on day-to-day function<BR>
      <TEXTAREA NAME="PDDom_Dom4Text_1" COLS="80" ROWS="5" WRAP="virtual" ONFOCUS="select()" ><<PDDom_Dom4Text_1>></TEXTAREA>
    </TD>
  </TR>
  <TR >
    <TD CLASS="port hdrtxt" COLSPAN="2" >5. FAMILY</TD>
    <TD CLASS="port numcol" >SCORE:
      <INPUT TYPE="TEXT" NAME="PDDom_Dom5Score_1" VALUE="<<PDDom_Dom5Score_1>>" ONFOCUS="select()" ONCHANGE="vNum(this,1,50)" SIZE=6>
    </TD>
  </TR>
  <TR >
    <TD CLASS="strcol" COLSPAN="3" >Problem areas:<BR>
      <INPUT TYPE="checkbox" NAME="PDDom_Dom5Parenting_1" VALUE=1 <<PDDom_Dom5Parenting_1=1>> ONFOCUS="select()" >
      Parenting
      <INPUT TYPE="checkbox" NAME="PDDom_Dom5Conflict_1" VALUE=1 <<PDDom_Dom5Conflict_1=1>> ONFOCUS="select()" >
      Conflict
      <INPUT TYPE="checkbox" NAME="PDDom_Dom5Violence_1" VALUE=1 <<PDDom_Dom5Violence_1=1>> ONFOCUS="select()" >
      Abuse/violence
      <INPUT TYPE="checkbox" NAME="PDDom_Dom5Communication_1" VALUE=1 <<PDDom_Dom5Communication_1=1>> ONFOCUS="select()" >
      Communication
      <INPUT TYPE="checkbox" NAME="PDDom_Dom5Marital_1" VALUE=1 <<PDDom_Dom5Marital_1=1>> ONFOCUS="select()" >
      Marital
      <INPUT TYPE="checkbox" NAME="PDDom_Dom5Sibling_1" VALUE=1 <<PDDom_Dom5Sibling_1=1>> ONFOCUS="select()" >
      Sibling
      <INPUT TYPE="checkbox" NAME="PDDom_Dom5ParentChild_1" VALUE=1 <<PDDom_Dom5ParentChild_1=1>> ONFOCUS="select()" >
      Parent/child
    </TD>
  </TR>
  <TR >
    <TD CLASS="strcol" COLSPAN="3" >Evidenced by (specific examples, frequency, duration and intensity)<BR>
      <TEXTAREA NAME="PDDom_Dom5Text_1" COLS="80" ROWS="5" WRAP="virtual" ONFOCUS="select()" ><<PDDom_Dom5Text_1>></TEXTAREA>
    </TD>
  </TR>
  <TR >
    <TD CLASS="port hdrtxt" COLSPAN="2" >6. INTERPERSONAL</TD>
    <TD CLASS="port numcol" >SCORE:
      <INPUT TYPE="TEXT" NAME="PDDom_Dom6Score_1" VALUE="<<PDDom_Dom6Score_1>>" ONFOCUS="select()" ONCHANGE="vNum(this,1,50)" SIZE=6>
    </TD>
  </TR>
  <TR >
    <TD CLASS="strcol" COLSPAN="3" >Problem areas:<BR>
      <INPUT TYPE="checkbox" NAME="PDDom_Dom6Peers_1" VALUE=1 <<PDDom_Dom6Peers_1=1>> ONFOCUS="select()" >
      Peers/friends
      <INPUT TYPE="checkbox" NAME="PDDom_Dom6Social_1" VALUE=1 <<PDDom_Dom6Social_1=1>> ONFOCUS="select()" >
      Social interaction
      <INPUT TYPE="checkbox" NAME="PDDom_Dom6Withdrawal_1" VALUE=1 <<PDDom_Dom6Withdrawal_1=1>> ONFOCUS="select()" >
      Withdrawal
      <INPUT TYPE="checkbox" NAME="PDDom_Dom6Friends_1" VALUE=1 <<PDDom_Dom6Friends_1=1>> ONFOCUS="select()" >
      Make/keep friends
      <INPUT TYPE="checkbox" NAME="PDDom_Dom6Conflict_1" VALUE=1 <<PDDom_Dom6Conflict_1=1>> ONFOCUS="select()" >
      Conflict
    </TD>
  </TR>
  <TR >
    <TD CLASS="strcol" COLSPAN="3" >Evidenced by (specific examples, frequency, duration and intensity)<BR>
      <TEXTAREA NAME="PDDom_Dom6Text_1" COLS="80" ROWS="5" WRAP="virtual" ONFOCUS="select()" ><<PDDom_Dom6Text_1>></TEXTAREA>
    </TD>
  </TR>
  <TR >
    <TD CLASS="port hdrtxt" COLSPAN="2" >7. ROLE PERFORMANCE</TD>
    <TD CLASS="port numcol" >SCORE:
      <INPUT TYPE="TEXT" NAME="PDDom_Dom7Score_1" VALUE="<<PDDom_Dom7Score_1>>" ONFOCUS="select()" ONCHANGE="vNum(this,1,50)" SIZE=6>
    </TD>
  </TR>
  <TR >
    <TD CLASS="strcol" COLSPAN="3" >Problem areas:<BR>
      <INPUT TYPE="checkbox" NAME="PDDom_Dom7Employment_1" VALUE=1 <<PDDom_Dom7Employment_1=1>> ONFOCUS="select()" >
      Employment/Volunteer
      <INPUT TYPE="checkbox" NAME="PDDom_Dom7School_1" VALUE=1 <<PDDom_Dom7School_1=1>> ONFOCUS="select()" >
      School/daycare
      <INPUT TYPE="checkbox" NAME="PDDom_Dom7Home_1" VALUE=1 <<PDDom_Dom7Home_1=1>> ONFOCUS="select()" >
      Home management
      <INPUT TYPE="checkbox" NAME="PDDom_Dom7Other_1" VALUE=1 <<PDDom_Dom7Other_1=1>> ONFOCUS="select()" >
      Other
      <INPUT TYPE="TEXT" NAME="PDDom_Dom7OText_1" VALUE="<<PDDom_Dom7OText_1>>" ONFOCUS="select()" SIZE=25>
    </TD>
  </TR>
  <TR >
    <TD CLASS="strcol" COLSPAN="3" >Effectiveness of functioning in identified role<BR>
      <TEXTAREA NAME="PDDom_Dom7Descr_1" COLS="80" ROWS="5" WRAP="virtual" ONFOCUS="select()" ><<PDDom_Dom7Descr_1>></TEXTAREA>
    </TD>
  </TR>
  <TR >
    <TD CLASS="strcol" COLSPAN="3" >Evidenced by (specific examples, frequency, duration and intensity)<BR>
      <TEXTAREA NAME="PDDom_Dom7Text_1" COLS="80" ROWS="5" WRAP="virtual" ONFOCUS="select()" ><<PDDom_Dom7Text_1>></TEXTAREA>
    </TD>
  </TR>
  <TR >
    <TD CLASS="port hdrtxt" COLSPAN="2" >8. SOCIO-LEGAL</TD>
    <TD CLASS="port numcol" >SCORE:
      <INPUT TYPE="TEXT" NAME="PDDom_Dom8Score_1" VALUE="<<PDDom_Dom8Score_1>>" ONFOCUS="select()" ONCHANGE="vNum(this,1,50)" SIZE=6>
    </TD>
  </TR>
  <TR >
    <TD CLASS="strcol" COLSPAN="3" >Problem areas:<BR>
      <INPUT TYPE="checkbox" NAME="PDDom_Dom8Rules_1" VALUE=1 <<PDDom_Dom8Rules_1=1>> ONFOCUS="select()" >
      Ability to follow rules/laws
      <INPUT TYPE="checkbox" NAME="PDDom_Dom8Authority_1" VALUE=1 <<PDDom_Dom8Authority_1=1>> ONFOCUS="select()" >
      Authority issues
      <INPUT TYPE="checkbox" NAME="PDDom_Dom8Legal_1" VALUE=1 <<PDDom_Dom8Legal_1=1>> ONFOCUS="select()" >
      Legal issues
      <INPUT TYPE="checkbox" NAME="PDDom_Dom8Aggression_1" VALUE=1 <<PDDom_Dom8Aggression_1=1>> ONFOCUS="select()" >
      Aggression
    </TD>
  </TR>
  <TR >
    <TD CLASS="strcol" COLSPAN="3" >
      <INPUT TYPE="checkbox" NAME="PDDom_Dom8Probation_1" VALUE=1 <<PDDom_Dom8Probation_1=1>> ONFOCUS="select()" >
      Probation/parole
      <INPUT TYPE="checkbox" NAME="PDDom_Dom8Moral_1" VALUE=1 <<PDDom_Dom8Moral_1=1>> ONFOCUS="select()" >
      Abides by personal ethical/moral value system
      <INPUT TYPE="checkbox" NAME="PDDom_Dom8Antisocial_1" VALUE=1 <<PDDom_Dom8Antisocial_1=1>> ONFOCUS="select()" >
      Antisocial behaviors
    </TD>
  </TR>
  <TR >
    <TD CLASS="strcol" COLSPAN="3" >Evidenced by (specific examples, frequency, duration and intensity)<BR>
      <TEXTAREA NAME="PDDom_Dom8Text_1" COLS="80" ROWS="5" WRAP="virtual" ONFOCUS="select()" ><<PDDom_Dom8Text_1>></TEXTAREA>
    </TD>
  </TR>
  <TR >
    <TD CLASS="port hdrtxt" COLSPAN="2" >9. SELF-CARE/BASIC NEEDS</TD>
    <TD CLASS="port numcol" >SCORE:
      <INPUT TYPE="TEXT" NAME="PDDom_Dom9Score_1" VALUE="<<PDDom_Dom9Score_1>>" ONFOCUS="select()" ONCHANGE="vNum(this,1,50)" SIZE=6>
    </TD>
  </TR>
  <TR >
    <TD CLASS="strcol" COLSPAN="3" >Problem areas:<BR>
      <INPUT TYPE="checkbox" NAME="PDDom_Dom9Hygiene_1" VALUE=1 <<PDDom_Dom9Hygiene_1=1>> ONFOCUS="select()" >
      Hygiene
      <INPUT TYPE="checkbox" NAME="PDDom_Dom9Food_1" VALUE=1 <<PDDom_Dom9Food_1=1>> ONFOCUS="select()" >
      Food
      <INPUT TYPE="checkbox" NAME="PDDom_Dom9Clothing_1" VALUE=1 <<PDDom_Dom9Clothing_1=1>> ONFOCUS="select()" >
      Clothing
      <INPUT TYPE="checkbox" NAME="PDDom_Dom9Shelter_1" VALUE=1 <<PDDom_Dom9Shelter_1=1>> ONFOCUS="select()" >
      Shelter
      <INPUT TYPE="checkbox" NAME="PDDom_Dom9Medical_1" VALUE=1 <<PDDom_Dom9Medical_1=1>> ONFOCUS="select()" >
      Medical/dental needs
      <INPUT TYPE="checkbox" NAME="PDDom_Dom9Transportation_1" VALUE=1 <<PDDom_Dom9Transportation_1=1>> ONFOCUS="select()" >
      Transportation
    </TD>
  </TR>
  <TR >
    <TD CLASS="strcol" COLSPAN="3" >Evidenced by (specific examples, frequency, duration and intensity)<BR>
      <TEXTAREA NAME="PDDom_Dom9Text_1" COLS="80" ROWS="5" WRAP="virtual" ONFOCUS="select()" ><<PDDom_Dom9Text_1>></TEXTAREA>
    </TD>
  </TR>
  <TR >
    <TD CLASS="port hdrtxt" COLSPAN="3" >10. COMMUNITY INTEGRATION<BR>(in fulfillment of CARF and JCAHO standards)</TD>
  </TR>
  <TR >
    <TD CLASS="strcol" COLSPAN="3" >Descriptors:<BR>
      <TEXTAREA NAME="PDDom_Dom10Text_1" COLS="80" ROWS="5" WRAP="virtual" ONFOCUS="select()" ><<PDDom_Dom10Text_1>></TEXTAREA>
    </TD>
  </TR>
  <TR >
    <TD CLASS="port hdrtxt" COLSPAN="3" >11. CARE GIVER RESOURCES<BR>(<B>REQUIRED</B> domain for clients under 21)</TD>
  </TR>
  <TR >
    <TD CLASS="strcol" COLSPAN="3" >Descriptors:<BR>
      <TEXTAREA NAME="PDDom_Dom11Text_1" COLS="80" ROWS="5" WRAP="virtual" ONFOCUS="select()" ><<PDDom_Dom11Text_1>></TEXTAREA>
    </TD>
  </TR>
  <TR >
    <TD CLASS="port hdrtxt" COLSPAN="3" >12. COMMUNICATION<BR>(<B>REQUIRED</B> for ICF/MR level of care)</TD>
  </TR>
  <TR >
    <TD CLASS="strcol" COLSPAN="3" >
      <INPUT TYPE="checkbox" NAME="PDDom_Dom12ESL_1" VALUE=1 <<PDDom_Dom12ESL_1=1>> ONFOCUS="select()" >
      ESL
      <INPUT TYPE="checkbox" NAME="PDDom_Dom12Hearing_1" VALUE=1 <<PDDom_Dom12Hearing_1=1>> ONFOCUS="select()" >
      Hearing impaired
      <INPUT TYPE="checkbox" NAME="PDDom_Dom12Nonverbal_1" VALUE=1 <<PDDom_Dom12Nonverbal_1=1>> ONFOCUS="select()" >
      Non-verbal
      <INPUT TYPE="checkbox" NAME="PDDom_Dom12Interpreter_1" VALUE=1 <<PDDom_Dom12Interpreter_1=1>> ONFOCUS="select()" >
      Uses interpreter
      <INPUT TYPE="checkbox" NAME="PDDom_Dom12Signs_1" VALUE=1 <<PDDom_Dom12Signs_1=1>> ONFOCUS="select()" >
      Signs
    </TD>
  </TR>
  <TR >
    <TD CLASS="strcol" COLSPAN="3" >
      <INPUT TYPE="checkbox" NAME="PDDom_Dom12Mechanical_1" VALUE=1 <<PDDom_Dom12Mechanical_1=1>> ONFOCUS="select()" >
      Uses mechanical device
      <INPUT TYPE="checkbox" NAME="PDDom_Dom12Speech_1" VALUE=1 <<PDDom_Dom12Speech_1=1>> ONFOCUS="select()" >
      Speech impaired
      <INPUT TYPE="checkbox" NAME="PDDom_Dom12Fluency_1" VALUE=1 <<PDDom_Dom12Fluency_1=1>> ONFOCUS="select()" >
      Fluency
    </TD>
  </TR>
  <TR >
    <TD CLASS="strcol" COLSPAN="3" >
      <TEXTAREA NAME="PDDom_Dom12Text_1" COLS="80" ROWS="5" WRAP="virtual" ONFOCUS="select()" ><<PDDom_Dom12Text_1>></TEXTAREA>
    </TD>
  </TR>
    </TABLE></TD></TR>
</TABLE>

<TABLE CLASS="main fullsize" >
  <TR>
    <TD CLASS="numcol" >
[[myTables->htmLocked(%form+<<<ClientPrAuth_Locked_1>>>+PDDom)]]
    </TD>
  </TR>
</TABLE>
<INPUT TYPE="hidden" NAME="post_update" VALUE="PostUpd->updPrAuth(%form+<<<ClientPrAuth_ID_1>>>)" >
</LOADHIDDEN>
</FORM>
<SCRIPT LANGUAGE="JavaScript">
document.PDDom.elements[0].focus();
</SCRIPT>

[[myHTML->rightpane(%form+search)]]
