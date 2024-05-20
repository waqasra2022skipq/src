[[myHTML->newPage(%form+ClientBasis32)]]

<SCRIPT LANGUAGE="JavaScript" SRC="/cgi/js/vEntry.js"> </SCRIPT>
<SCRIPT LANGUAGE="JavaScript" SRC="/cgi/js/vClientBasis32.js"> </SCRIPT>
<SCRIPT LANGUAGE="JavaScript" SRC="/cgi/js/vNum.js"> </SCRIPT>
<SCRIPT LANGUAGE="JavaScript" SRC="/cgi/js/vDate.js"> </SCRIPT>

<FORM NAME="ClientBasis32" ACTION="/cgi/bin/mis.cgi" METHOD="POST" >
<TABLE CLASS="main fullsize" >
  <TR >
    <TD CLASS="strcol" COLSPAN="2" >
      <<<Client_FName_1>>> <<<Client_MName_1>>> <<<Client_LName_1>>> (<<<Client_ClientID_1>>>) <<<Client_SSN_1>>>
    <BR>Client Basis 32 View/Edit Page
    </TD>
    <TD CLASS="numcol" >[[gHTML->setLINKS(%form+back)]]</TD>
  </TR>
</TABLE>
<HR WIDTH="90%">
<TABLE CLASS="home fullsize" >
  <TR >
    <TD CLASS="porttitle" COLSPAN="5" >
      <FONT SIZE=+1><B>Client Basis-32 (Behavior And Symptom Identification Scale)</B></FONT>
    </TD>
  </TR>
  <TR><TD CLASS="strcol"COLSPAN="5" >&nbsp;</TD></TR>
  <TR><TD CLASS="strcol"COLSPAN="5" ><B>Instructions To Respondent:</B></TD></TR>
  <TR>
    <TD CLASS="strcol"COLSPAN="5" >
      Below is a list of problem areas of life functioning in which some people experience difficulty. Using the scale below, fill in the box with the answer that best describes how much difficulty you have been having in each area <B>DURING THE PAST WEEK.</B>
    </TD>
  </TR>
  <TR><TD CLASS="strcol"COLSPAN="5" >&nbsp;</TD></TR>
  <TR>
    <TD CLASS="strcol">0= No Difficulty </TD>
    <TD CLASS="strcol">1= A Little Difficulty </TD>
    <TD CLASS="strcol">2= Moderate Difficulty</TD>
    <TD CLASS="strcol">3= Quite A Bit of Difficulty</TD>
    <TD CLASS="strcol">4= Extreme Difficulty</TD>
  </TR>
  <TR><TD CLASS="strcol"COLSPAN="5" >&nbsp;</TD></TR>
  <TR><TD CLASS="strcol"COLSPAN="5" >Please do not leave any questions blank.</TD></TR>
  <TR>
    <TD CLASS="strcol"COLSPAN="5" >
     If there is an area that you consider to be inapplicable, indicate that it is <B>0= No Difficulty</B>
    </TD>
  </TR>
</TABLE>
<HR WIDTH="90%">
<TABLE CLASS="home fullsize" >
  <TR>
    <TD CLASS="strcol"COLSPAN="2" >Effective left blank will be today.</TD>
    <TD CLASS="strcol"COLSPAN="2" >Expired Date should left blank.</TD>
  </TR>
  <TR >
    <TD CLASS="strcol"ALIGN=right >Effective:</TD>
    <TD CLASS="strcol">
      <INPUT TYPE="TEXT" NAME="ClientBasis32_EffDate_1" VALUE="<<ClientBasis32_EffDate_1>>" ONFOCUS="select()" ONCHANGE="return vDate(this)" SIZE=10 >
    <TD CLASS="strcol"ALIGN=right >Expires:</TD>
    <TD CLASS="strcol">
      <INPUT TYPE="TEXT" NAME="ClientBasis32_ExpDate_1" VALUE="<<ClientBasis32_ExpDate_1>>" ONFOCUS="select()" ONCHANGE="return vDate(this)" SIZE=10 >
    </TD>
  </TR>
  <TR><TD CLASS="strcol"ALIGN=left COLSPAN="4" >&nbsp;</TD></TR>
</TABLE>
<TABLE CLASS="home fullsize" >
  <TR >
    <TD CLASS="port hdrtxt" COLSPAN="2" >
      IN THE PAST WEEK, how much difficulty have you been having in the area of:
    </TD>
  </TR>
  <TR >
    <TD CLASS="strcol"ALIGN=left >
      1. Managing day-to-day life. (For example, getting places on time, handling money making every day decisions)
    </TD>
    <TD CLASS="strcol"ALIGN=left >
      <INPUT TYPE="TEXT" NAME="ClientBasis32_B01_1" VALUE="<<ClientBasis32_B01_1>>" ONFOCUS="select()" ONCHANGE="return validateScore(this.form,this)" SIZE=6 >
    </TD>
  </TR>
  <TR >
    <TD CLASS="strcol"ALIGN=left >
      2. Household responsibilities. (For example, shopping, cooking, laundry, cleaning, other chores)
    </TD>
    <TD CLASS="strcol"ALIGN=left >
      <INPUT TYPE="TEXT" NAME="ClientBasis32_B02_1" VALUE="<<ClientBasis32_B02_1>>" ONFOCUS="select()" ONCHANGE="return validateScore(this.form,this)" SIZE=6 >
    </TD>
  </TR>
  <TR >
    <TD CLASS="strcol"ALIGN=left >
      3. Work. (For example, completing task, performance level, finding/ keeping a job)
    </TD>
    <TD CLASS="strcol"ALIGN=left >
      <INPUT TYPE="TEXT" NAME="ClientBasis32_B03_1" VALUE="<<ClientBasis32_B03_1>>" ONFOCUS="select()" ONCHANGE="return validateScore(this.form,this)" SIZE=6 >
    </TD>
  </TR>
  <TR >
    <TD CLASS="strcol"ALIGN=left >
      4. School (For example, academic performance, competing assignments attendance)
    </TD>
    <TD CLASS="strcol"ALIGN=left >
      <INPUT TYPE="TEXT" NAME="ClientBasis32_B04_1" VALUE="<<ClientBasis32_B04_1>>" ONFOCUS="select()" ONCHANGE="return validateScore(this.form,this)" SIZE=6 >
    </TD>
  </TR>
  <TR >
    <TD CLASS="strcol"ALIGN=left >
      5. Leisure time or recreational activities
    </TD>
    <TD CLASS="strcol"ALIGN=left >
      <INPUT TYPE="TEXT" NAME="ClientBasis32_B05_1" VALUE="<<ClientBasis32_B05_1>>" ONFOCUS="select()" ONCHANGE="return validateScore(this.form,this)" SIZE=6 >
    </TD>
  </TR>
  <TR >
    <TD CLASS="strcol"ALIGN=left >
      6. Adjusting to major life stresses. (For example, separation, divorce, moving, new job, new school, a death)
    </TD>
    <TD CLASS="strcol"ALIGN=left >
      <INPUT TYPE="TEXT" NAME="ClientBasis32_B06_1" VALUE="<<ClientBasis32_B06_1>>" ONFOCUS="select()" ONCHANGE="return validateScore(this.form,this)" SIZE=6 >
    </TD>
  </TR>
  <TR >
    <TD CLASS="strcol"ALIGN=left >
      7. Relationship with family members
    </TD>
    <TD CLASS="strcol"ALIGN=left >
      <INPUT TYPE="TEXT" NAME="ClientBasis32_B07_1" VALUE="<<ClientBasis32_B07_1>>" ONFOCUS="select()" ONCHANGE="return validateScore(this.form,this)" SIZE=6 >
    </TD>
  </TR>
  <TR >
    <TD CLASS="strcol"ALIGN=left >
      8. Getting along with people outside of the family
    </TD>
    <TD CLASS="strcol"ALIGN=left >
      <INPUT TYPE="TEXT" NAME="ClientBasis32_B08_1" VALUE="<<ClientBasis32_B08_1>>" ONFOCUS="select()" ONCHANGE="return validateScore(this.form,this)" SIZE=6 >
    </TD>
  </TR>
  <TR >
    <TD CLASS="strcol"ALIGN=left >
      9. Isolation or feelings of loneliness
    </TD>
    <TD CLASS="strcol"ALIGN=left >
      <INPUT TYPE="TEXT" NAME="ClientBasis32_B09_1" VALUE="<<ClientBasis32_B09_1>>" ONFOCUS="select()" ONCHANGE="return validateScore(this.form,this)" SIZE=6 >
    </TD>
  </TR>
  <TR >
    <TD CLASS="strcol"ALIGN=left >
      10. Being able to feel close to others
    </TD>
    <TD CLASS="strcol"ALIGN=left >
      <INPUT TYPE="TEXT" NAME="ClientBasis32_B10_1" VALUE="<<ClientBasis32_B10_1>>" ONFOCUS="select()" ONCHANGE="return validateScore(this.form,this)" SIZE=6 >
    </TD>
  </TR>
  <TR >
    <TD CLASS="strcol"ALIGN=left >
      11. Being realistic about yourself or others
    </TD>
    <TD CLASS="strcol"ALIGN=left >
      <INPUT TYPE="TEXT" NAME="ClientBasis32_B11_1" VALUE="<<ClientBasis32_B11_1>>" ONFOCUS="select()" ONCHANGE="return validateScore(this.form,this)" SIZE=6 >
    </TD>
  </TR>
  <TR >
    <TD CLASS="strcol"ALIGN=left >
      12. Recognizing and expressing emotions appropriately
    </TD>
    <TD CLASS="strcol"ALIGN=left >
      <INPUT TYPE="TEXT" NAME="ClientBasis32_B12_1" VALUE="<<ClientBasis32_B12_1>>" ONFOCUS="select()" ONCHANGE="return validateScore(this.form,this)" SIZE=6 >
    </TD>
  </TR>
  <TR >
    <TD CLASS="strcol"ALIGN=left >
      13. Developing independence, autonomy
    </TD>
    <TD CLASS="strcol"ALIGN=left >
      <INPUT TYPE="TEXT" NAME="ClientBasis32_B13_1" VALUE="<<ClientBasis32_B13_1>>" ONFOCUS="select()" ONCHANGE="return validateScore(this.form,this)" SIZE=6 >
    </TD>
  </TR>
  <TR >
    <TD CLASS="strcol"ALIGN=left >
      14. Goals or directions in life
    </TD>
    <TD CLASS="strcol"ALIGN=left >
      <INPUT TYPE="TEXT" NAME="ClientBasis32_B14_1" VALUE="<<ClientBasis32_B14_1>>" ONFOCUS="select()" ONCHANGE="return validateScore(this.form,this)" SIZE=6 >
    </TD>
  </TR>
  <TR >
    <TD CLASS="strcol"ALIGN=left >
      15. Lack of self confidence, feeling bad about yourself
    </TD>
    <TD CLASS="strcol"ALIGN=left >
      <INPUT TYPE="TEXT" NAME="ClientBasis32_B15_1" VALUE="<<ClientBasis32_B15_1>>" ONFOCUS="select()" ONCHANGE="return validateScore(this.form,this)" SIZE=6 >
    </TD>
  </TR>
  <TR >
    <TD CLASS="strcol"ALIGN=left >
      16. Apathy, lack of interest in things
    </TD>
    <TD CLASS="strcol"ALIGN=left >
      <INPUT TYPE="TEXT" NAME="ClientBasis32_B16_1" VALUE="<<ClientBasis32_B16_1>>" ONFOCUS="select()" ONCHANGE="return validateScore(this.form,this)" SIZE=6 >
    </TD>
  </TR>
  <TR >
    <TD CLASS="strcol"ALIGN=left >
      17. Depression, Hopelessness
    </TD>
    <TD CLASS="strcol"ALIGN=left >
      <INPUT TYPE="TEXT" NAME="ClientBasis32_B17_1" VALUE="<<ClientBasis32_B17_1>>" ONFOCUS="select()" ONCHANGE="return validateScore(this.form,this)" SIZE=6 >
    </TD>
  </TR>
  <TR >
    <TD CLASS="strcol"ALIGN=left >
      18. Suicidal feelings or behavior
    </TD>
    <TD CLASS="strcol"ALIGN=left >
      <INPUT TYPE="TEXT" NAME="ClientBasis32_B18_1" VALUE="<<ClientBasis32_B18_1>>" ONFOCUS="select()" ONCHANGE="return validateScore(this.form,this)" SIZE=6 >
    </TD>
  </TR>
  <TR >
    <TD CLASS="strcol"ALIGN=left >
      19. Physical symptoms (For example, headaches, aches and pains, sleep disturbance, stomach aches, dizziness)
    </TD>
    <TD CLASS="strcol"ALIGN=left >
      <INPUT TYPE="TEXT" NAME="ClientBasis32_B19_1" VALUE="<<ClientBasis32_B19_1>>" ONFOCUS="select()" ONCHANGE="return validateScore(this.form,this)" SIZE=6 >
    </TD>
  </TR>
  <TR >
    <TD CLASS="strcol"ALIGN=left >
      20. Fear, anxiety, or panic
    </TD>
    <TD CLASS="strcol"ALIGN=left >
      <INPUT TYPE="TEXT" NAME="ClientBasis32_B20_1" VALUE="<<ClientBasis32_B20_1>>" ONFOCUS="select()" ONCHANGE="return validateScore(this.form,this)" SIZE=6 >
    </TD>
  </TR>
  <TR >
    <TD CLASS="strcol"ALIGN=left >
      21. Confusion, concentration, memory
    </TD>
    <TD CLASS="strcol"ALIGN=left >
      <INPUT TYPE="TEXT" NAME="ClientBasis32_B21_1" VALUE="<<ClientBasis32_B21_1>>" ONFOCUS="select()" ONCHANGE="return validateScore(this.form,this)" SIZE=6 >
    </TD>
  </TR>
  <TR >
    <TD CLASS="strcol"ALIGN=left >
      22. Disturbing or unreal thoughts or beliefs
    </TD>
    <TD CLASS="strcol"ALIGN=left >
      <INPUT TYPE="TEXT" NAME="ClientBasis32_B22_1" VALUE="<<ClientBasis32_B22_1>>" ONFOCUS="select()" ONCHANGE="return validateScore(this.form,this)" SIZE=6 >
    </TD>
  </TR>
  <TR >
    <TD CLASS="strcol"ALIGN=left >
      23. Hearing voices, seeing things
    </TD>
    <TD CLASS="strcol"ALIGN=left >
      <INPUT TYPE="TEXT" NAME="ClientBasis32_B23_1" VALUE="<<ClientBasis32_B23_1>>" ONFOCUS="select()" ONCHANGE="return validateScore(this.form,this)" SIZE=6 >
    </TD>
  </TR>
  <TR >
    <TD CLASS="strcol"ALIGN=left >
      24. Manic, bizarre behavior
    </TD>
    <TD CLASS="strcol"ALIGN=left >
      <INPUT TYPE="TEXT" NAME="ClientBasis32_B24_1" VALUE="<<ClientBasis32_B24_1>>" ONFOCUS="select()" ONCHANGE="return validateScore(this.form,this)" SIZE=6 >
    </TD>
  </TR>
  <TR >
    <TD CLASS="strcol"ALIGN=left >
      25. Mood swings, unstable moods
    </TD>
    <TD CLASS="strcol"ALIGN=left >
      <INPUT TYPE="TEXT" NAME="ClientBasis32_B25_1" VALUE="<<ClientBasis32_B25_1>>" ONFOCUS="select()" ONCHANGE="return validateScore(this.form,this)" SIZE=6 >
    </TD>
  </TR>
  <TR >
    <TD CLASS="strcol"ALIGN=left >
      26. Uncontrollable, compulsive behavior, (For example, eating disorder, hand washing, hurting yourself)
    </TD>
    <TD CLASS="strcol"ALIGN=left >
      <INPUT TYPE="TEXT" NAME="ClientBasis32_B26_1" VALUE="<<ClientBasis32_B26_1>>" ONFOCUS="select()" ONCHANGE="return validateScore(this.form,this)" SIZE=6 >
    </TD>
  </TR>
  <TR >
    <TD CLASS="strcol"ALIGN=left >
      27. Sexual activity or preoccupation
    </TD>
    <TD CLASS="strcol"ALIGN=left >
      <INPUT TYPE="TEXT" NAME="ClientBasis32_B27_1" VALUE="<<ClientBasis32_B27_1>>" ONFOCUS="select()" ONCHANGE="return validateScore(this.form,this)" SIZE=6 >
    </TD>
  </TR>
  <TR >
    <TD CLASS="strcol"ALIGN=left >
      28. Drinking alcoholic beverages
    </TD>
    <TD CLASS="strcol"ALIGN=left >
      <INPUT TYPE="TEXT" NAME="ClientBasis32_B28_1" VALUE="<<ClientBasis32_B28_1>>" ONFOCUS="select()" ONCHANGE="return validateScore(this.form,this)" SIZE=6 >
    </TD>
  </TR>
  <TR >
    <TD CLASS="strcol"ALIGN=left >
      29. Taking illegal drugs, misusing drugs
    </TD>
    <TD CLASS="strcol"ALIGN=left >
      <INPUT TYPE="TEXT" NAME="ClientBasis32_B29_1" VALUE="<<ClientBasis32_B29_1>>" ONFOCUS="select()" ONCHANGE="return validateScore(this.form,this)" SIZE=6 >
    </TD>
  </TR>
  <TR >
    <TD CLASS="strcol"ALIGN=left >
      30. Controlling temper, outburst of anger , violence
    </TD>
    <TD CLASS="strcol"ALIGN=left >
      <INPUT TYPE="TEXT" NAME="ClientBasis32_B30_1" VALUE="<<ClientBasis32_B30_1>>" ONFOCUS="select()" ONCHANGE="return validateScore(this.form,this)" SIZE=6 >
    </TD>
  </TR>
  <TR >
    <TD CLASS="strcol"ALIGN=left >
      31. Impulsive, illegal, or reckless behavior
    </TD>
    <TD CLASS="strcol"ALIGN=left >
      <INPUT TYPE="TEXT" NAME="ClientBasis32_B31_1" VALUE="<<ClientBasis32_B31_1>>" ONFOCUS="select()" ONCHANGE="return validateScore(this.form,this)" SIZE=6 >
    </TD>
  </TR>
  <TR >
    <TD CLASS="strcol"ALIGN=left >
      32. Feeling satisfaction with your life
    </TD>
    </TD>
    <TD CLASS="strcol"ALIGN=left >
      <INPUT TYPE="TEXT" NAME="ClientBasis32_B32_1" VALUE="<<ClientBasis32_B32_1>>" ONFOCUS="select()" ONCHANGE="return validateScore(this.form,this)" SIZE=6 >
    </TD>
  </TR>
</TABLE>
<TABLE CLASS="home fullsize" >
  <TR >
    <TD CLASS="strcol"ALIGN=left >
      Average:
      <INPUT TYPE="TEXT" NAME="ClientBasis32_Avg_1" VALUE="<<ClientBasis32_Avg_1>>" ONFOCUS="this.blur()" SIZE=6 >
    </TD>
    <TD CLASS="strcol"ALIGN=left >
      Total:
      <INPUT TYPE="TEXT" NAME="ClientBasis32_Tot_1" VALUE="<<ClientBasis32_Tot_1>>" ONFOCUS="this.blur()" SIZE=6 >
    </TD>
  </TR>
</TABLE>
<TABLE CLASS="main fullsize" >
  <TR >
    <TD CLASS="numcol" >
      <INPUT TYPE="submit" ONCLICK="return vDELETE('Are you sure you want to delete?')" NAME="ClientBasis32_DELETE_1=1&UpdateTables=all&misPOP=1" VALUE="Delete" >
      <INPUT TYPE="button" VALUE="Set Avg/Total" ONCLICK="javascript:validateScore(this.form,form.ClientBasis32_B01_1)" >
      <INPUT TYPE="submit" ONCLICK="return validate(this.form);" NAME="UpdateTables=all&misPOP=1" VALUE="Add/Update">
    </TD>
  </TR>
</TABLE>

</LOADHIDDEN>
<SCRIPT LANGUAGE="JavaScript">
document.ClientBasis32.elements[0].focus();
</SCRIPT>
</FORM>
[[myHTML->rightpane(%form+search)]]
