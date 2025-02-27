[[myHTML->newPage(%form+Client MHSF)]]

<SCRIPT LANGUAGE="JavaScript" SRC="/cgi/js/NoEnter.js"> </SCRIPT>
<SCRIPT LANGUAGE="JavaScript" SRC="/cgi/js/vEntry.js"> </SCRIPT>
<SCRIPT LANGUAGE="JavaScript" SRC="/cgi/js/vClientMMSE.js"> </SCRIPT>
<SCRIPT LANGUAGE="JavaScript" SRC="/cgi/js/vDate.js"> </SCRIPT>
<SCRIPT LANGUAGE="JavaScript" SRC="/cgi/js/calculateScore.js"> </SCRIPT>

<FORM NAME="ClientMMSE" ACTION="/cgi/bin/mis.cgi" METHOD="POST" >
<TABLE CLASS="main fullsize" >
  <TR >
    <TD CLASS="strcol" >
      <<<Client_FName_1>>> <<<Client_MName_1>>> <<<Client_LName_1>>> (<<<Client_ClientID_1>>>) <<<Client_SSN_1>>>
      <BR>
      Mini</br>-Mental State Examination (MMSE) View/Edit Page
    </TD>
    <TD CLASS="numcol" >[[gHTML->setLINKS(%form+back)]]</TD>
  </TR>
</TABLE>
<TABLE CLASS="home fullsize" >
  <TR ><TD CLASS="port hdrtxt" >Mini</br>-Mental State Examination (MMSE)</TD></TR>
  <TR ><TD CLASS="hdrtxt"><b>Instructions:</b>

Ask the questions in the order listed. Score one point for each correct response within each question or activity.
</TD></TR>
  <TR><TD ><div name="TotalDiv" id="TotalDiv"><b>TOTAL: <<ClientMMSE_Score_1>></b> </div></TD></TR>
  <TR >
    <TD CLASS="port txt" >
[[[myHTML->setHTML(%form+ClientMMSE)]]]
    </TD>
  </TR>
</TABLE>
<TABLE CLASS="main fullsize" >
  <TR >
    <TD CLASS="numcol" >
      <INPUT TYPE="submit" ONCLICK="return vDELETE('Are you sure you want to delete this record?');" NAME="ClientMMSE_DELETE_1=1&UpdateTables=all&misPOP=1" VALUE="Delete">
      <INPUT TYPE="submit" ONCLICK="return validate(this.form);" NAME="UpdateTables=all&misPOP=1" VALUE="Add/Update">
    </TD>
  </TR>
<TR ><TD CLASS="subtitle strcol" style="background-color: white; color: black" ><b class="hdrtxt">Instructions for administration and scoring of the MMSE 
Orientation (10 points):</b><br/> 
</br>- Ask for the date. Then specifically ask for parts omitted (e.g., "Can you also tell me what season it is?"). One point for each correct answer. </br>
</br>- Ask in turn, "Can you tell me the name of this hospital (town, county, etc.)?" One point for each correct answer. </br>
<p>
Registration (3 points): 
</br>- Say the names of three unrelated objects clearly and slowly, allowing approximately one second for each. After you have said all three, ask the patient to repeat them. The number of objects the patient names correctly upon the first repetition determines the score (0</br>-3). If the patient does not repeat all three objects the first time, continue saying the names until the patient is able to repeat all three items, up to six trials. Record the number of trials it takes for the patient to learn the words. If the patient does not eventually learn all three, recall cannot be meaningfully tested. 
</br>- After completing this task, tell the patient, "Try to remember the words, as I will ask for them in a little while." 
Attention and Calculation (5 points): 
</br>- Ask the patient to begin with 100 and count backward by sevens. Stop after five subtractions (93, 86, 79, 72, 65). Score the total number of correct answers. 
</br>- If the patient cannot or will not perform the subtraction task, ask the patient to spell the word "world" backwards. The score is the number of letters in correct order (e.g., dlrow=5, dlorw=3). 
Recall (3 points): 
</br>- Ask the patient if he or she can recall the three words you previously asked him or her to remember. Score the total number of correct answers (0-3). 
Language and Praxis (9 points): 
</br>- Naming: Show the patient a wrist watch and ask the patient what it is. Repeat with a pencil. Score one point for each correct naming (0-2). 
</br>- Repetition: Ask the patient to repeat the sentence after you ("No ifs, ands, or buts."). Allow only one trial. Score 0 or 1. 
</br>- 3</br>-Stage Command: Give the patient a piece of blank paper and say, "Take this paper in your right hand, fold it in half, and put it on the floor." Score one point for each part of the command correctly executed. 
</br>- Reading: On a blank piece of paper print the sentence, "Close your eyes," in letters large enough for the patient to see clearly. Ask the patient to read the sentence and do what it says. Score one point only if the patient actually closes his or her eyes. This is not a test of memory, so you may prompt the patient to "do what it says" after the patient reads the sentence. 
</br>- Writing: Give the patient a blank piece of paper and ask him or her to write a sentence for you. Do not dictate a sentence; it should be written spontaneously. The sentence must contain a subject and a verb and make sense. Correct grammar and punctuation are not necessary. 
</br>- Copying: Show the patient the picture of two intersecting pentagons and ask the patient to copy the figure exactly as it is. All ten angles must be present and two must intersect to score one point. Ignore tremor and rotation. 
(Folstein, Folstein & McHugh, 1975) 
</p>
</TD></TR>
</TABLE>

</LOADHIDDEN>
</FORM>
<SCRIPT LANGUAGE="JavaScript">
document.ClientMMSE.elements[0].focus();
function totalScore() {
}
totalScore();
// just to OPENTABLES...
//<<<ClientMMSE_ClientID_1>>>
</SCRIPT>

[[myHTML->rightpane(%form+search)]]
