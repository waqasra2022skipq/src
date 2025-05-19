[[myHTML->newHTML(%form+Client History+allleft mismenu checkpopupwindow)]]

<SCRIPT LANGUAGE="JavaScript" SRC="/src/cgi/js/vEntry.js"> </SCRIPT>
<SCRIPT LANGUAGE="JavaScript" SRC="/src/cgi/js/vClientHistory.js"> </SCRIPT>
<SCRIPT LANGUAGE="JavaScript" SRC="/src/cgi/js/serverREQ.js"> </SCRIPT>
<SCRIPT LANGUAGE="JavaScript" SRC="/src/cgi/js/vNum.js"> </SCRIPT>
<SCRIPT LANGUAGE="JavaScript" SRC="/src/cgi/js/qDate.js"> </SCRIPT>

<FORM NAME="History" ACTION="/src/cgi/bin/mis.cgi" METHOD="POST" >
<TABLE CLASS="main fullsize" >
  <TR >
    <TD CLASS="strcol" >
      <<<Client_FName_1>>> <<<Client_MName_1>>> <<<Client_LName_1>>> (<<<Client_ClientID_1>>>) <<<Client_SSN_1>>>
      <BR>
      Education / Vocational / Military / Perspective Page
    </TD>
    <TD CLASS="numcol" >[[gHTML->setLINKS(%form+back)]]</TD>
  </TR>
</TABLE>
<TABLE CLASS="port fullsize" >
    <TR ><TD ><TABLE CLASS="home fullsize" >
  <TR ><TD CLASS="port heading" COLSPAN="4" >EDUCATIONAL / SCHOOL HISTORY</TD></TR>
  <TR ><TD CLASS="port hdrtxt" COLSPAN="4" >Attainment & Difficulties</TD></TR>
  <TR>
    <TD CLASS="strcol" COLSPAN="3" >
      How many schools have you attended? Changes to date?
    </TD>
    <TD CLASS="strcol" >
      <INPUT TYPE=text NAME="ClientIntake_NumSchools_1" VALUE="<<ClientIntake_NumSchools_1>>" ONFOCUS="select()" ONCHANGE="return vNum(this,0,99);" SIZE=2>
    </TD>
  </TR>
  <TR >
    <TD CLASS="strcol" COLSPAN="3" >What is the highest grade in school you have satisfactorily completed?</TD>
    <TD CLASS="strcol" >
      <SELECT NAME="ClientEducation_SchoolGrade_1" >
        [[DBA->selxTable(%form+xSchoolGrades+<<ClientEducation_SchoolGrade_1>>+Descr)]]
      </SELECT> 
    </TD>
  </TR>
  <TR>
    <TD CLASS="strcol" COLSPAN="2" >Did you repeat any grades?</TD>
    <TD CLASS="strcol" >If yes, which grades?<BR>(use ctrl-key for multiples)</TD>
    <TD CLASS="strcol" >
      <SELECT NAME="ClientEducation_RepeatGrade_1" MULTIPLE >
        [[DBA->selxTable(%form+xSchoolGrades+<<ClientEducation_RepeatGrade_1>>+Descr)]]
      </SELECT> 
    </TD>
  </TR>
  <TR>
    <TD CLASS="strcol" COLSPAN="4" >
      Why?
      <INPUT TYPE=text NAME="ClientIntake_RepeatGradeDesc_1" VALUE="<<ClientIntake_RepeatGradeDesc_1>>" MAXLENGTH="25" SIZE="80" >
    </TD>
  </TR>
  <TR> <TD CLASS="strcol" COLSPAN="4" > School district?  </TD> </TR>
  <TR>
    <TD CLASS="strcol" COLSPAN="4" >
      <SELECT ID="LastSchoolDist" NAME="ClientIntake_LastSchoolDist_1" ONCHANGE="createFLD(this,'/cgi/bin/verify.pl?mlt=<<<mlt>>>&type=LastSchoolName','selLastSchoolName','LastSchoolDist','LastSchoolName')" >
        [[DBA->selxTable(%form+xSchoolDistricts+<<ClientIntake_LastSchoolDist_1>>+DistrictName City State Zip CountyName CountyDistrictCode)]]
      </SELECT>
    </TD>
  </TR>
  <TR> <TD CLASS="strcol" COLSPAN="4" > Name of School last attended?  </TD> </TR>
  <TR>
    <TD CLASS="strcol" COLSPAN="4" >
      <SPAN ID="selLastSchoolName">
      <SELECT ID="LastSchoolName" NAME="ClientIntake_LastSchoolName_1" >
        [[DBA->selxTable(%form+xSchoolSites+<<ClientIntake_LastSchoolName_1>>+SchoolSite City State Zip CountyName CountyDistrictCode SiteCode)]]
      </SELECT>
      </SPAN>
    </TD>
  </TR>
  <TR>
    <TD CLASS="strcol" COLSPAN="3" >
      How many months of Training or Technical education have you satisfactorily completed?
      <BR>� Formal/organized training only. For military training, only include training that can be used in civilian life (i.e., electronics, computers)
    </TD>
    <TD CLASS="strcol" >
      <INPUT TYPE=text NAME="ClientEducation_MonthsTechEd_1" VALUE="<<ClientEducation_MonthsTechEd_1>>" ONFOCUS="select()" ONCHANGE="return vNum(this,0,99);" SIZE="2" > Months
    </TD>
  </TR>
  <TR>
    <TD CLASS="strcol" >What subjects did you like in school?</TD>
    <TD CLASS="strcol" COLSPAN="3" >
      <SELECT NAME="ClientIntake_SubjectsLike_1" MULTIPLE >[[DBA->selxTable(%form+xSubjects+<<ClientIntake_SubjectsLike_1>>)]]</SELECT>
    </TD>
  </TR>
  <TR>
    <TD CLASS="strcol" >What subjects did you dislike in school?</TD>
    <TD CLASS="strcol" COLSPAN="3" >
      <SELECT NAME="ClientIntake_SubjectsDisLike_1" MULTIPLE >[[DBA->selxTable(%form+xSubjects+<<ClientIntake_SubjectsDisLike_1>>)]]</SELECT>
    </TD>
  </TR>
    </TABLE></TD></TR>
    <TR ><TD ><TABLE CLASS="home fullsize" >
  <TR ><TD CLASS="port hdrtxt" COLSPAN="4" >Learning Ability/Intellectual Functioning</TD></TR>
  <TR >
    <TD CLASS="strcol" >Would you describe yourself as a:</TD>
    <TD CLASS="strcol" COLSPAN="3" >
      <SELECT NAME="ClientIntake_LearnAbility_1" >[[DBA->selxTable(%form+xLearnAbility+<<ClientIntake_LearnAbility_1>>)]]</SELECT>
    </TD>
  </TR>
  <TR>
    <TD CLASS="strcol" COLSPAN="2" >Have you ever taken an I.Q. test?</TD>
    <TD CLASS="strcol" >If yes, what was your score?</TD>
    <TD CLASS="strcol" >
      <INPUT TYPE=text NAME="ClientIntake_IQ_1" VALUE="<<ClientIntake_IQ_1>>" ONCHANGE="return vNum(this,1,210);" SIZE=5>
    </TD>
  </TR>
    </TABLE></TD></TR>
    <TR ><TD ><TABLE CLASS="home fullsize" >
  <TR ><TD CLASS="port hdrtxt" COLSPAN="4" >Current Daycare Functioning (preschool)</TD></TR>
  <TR>
    <TD CLASS="strcol" COLSPAN="2" >In the past 90 days, how many days was the customer not permitted to return to day care? </TD>
    <TD CLASS="strcol" COLSPAN="2" >
      <INPUT TYPE=text NAME="ClientIntake_AbsentDayCare_1" VALUE="<<ClientIntake_AbsentDayCare_1>>" ONFOCUS="select()" ONCHANGE="return vNum(this,0,66);" SIZE="2" >
    </TD>
  </TR>
    </TABLE></TD></TR>
    <TR ><TD ><TABLE CLASS="home fullsize" >
  <TR ><TD CLASS="port hdrtxt" COLSPAN="4" >Current Educational Functioning<BR>(child,adolescent & adult)</TD></TR>
  <TR>
    <TD CLASS="strcol" COLSPAN="2" >Current school status?</TD>
    <TD CLASS="strcol" COLSPAN="2" >
      <SELECT NAME="ClientIntake_SchoolStat_1" >
        [[DBA->selxTable(%form+xSchoolStat+<<ClientIntake_SchoolStat_1>>+Descr)]]
      </SELECT>
    </TD>
  </TR>
  <TR>
    <TD CLASS="strcol" COLSPAN="2" >
      At any time in the past three months, has this person attended school/college? 
    </TD>
    <TD CLASS="strcol" COLSPAN="2" >
      <INPUT TYPE="radio" NAME="ClientIntake_SchoolLast3_1" VALUE="1" <<ClientIntake_SchoolLast3_1=1>> > Yes
      <INPUT TYPE="radio" NAME="ClientIntake_SchoolLast3_1" VALUE="0" <<ClientIntake_SchoolLast3_1=0>> > No
    </TD>
  </TR>
  <TR>
    <TD CLASS="strcol" COLSPAN="2" >What grade are you currently attending?</TD>
    <TD CLASS="strcol" COLSPAN="2" >
      <SELECT NAME="ClientEducation_CurrentGrade_1" >
        [[DBA->selxTable(%form+xSchoolGrades+<<ClientEducation_CurrentGrade_1>>+Descr)]]
      </SELECT> 
    </TD>
  </TR>
  <TR>
    <TD CLASS="strcol" COLSPAN="2" >What is your current school performance (grades or GPA)?</TD>
    <TD CLASS="strcol" COLSPAN="2" >
      <INPUT TYPE=text NAME="ClientIntake_GPA_1" VALUE="<<ClientIntake_GPA_1>>" >
    </TD>
  </TR>
  <TR>
    <TD CLASS="strcol" COLSPAN="2" >Do you have a special education classification?</TD>
    <TD CLASS="strcol" COLSPAN="2" >
      <SELECT NAME="ClientIntake_SpecEd_1" >
        [[DBA->selxTable(%form+xSpecEd+<<ClientIntake_SpecEd_1>>+Descr)]]
      </SELECT>
    </TD>
  </TR>
  <TR>
    <TD CLASS="strcol" COLSPAN="2" >Are you currently being served on an IEP?</TD>
    <TD CLASS="strcol" COLSPAN="2" >
      <INPUT TYPE="radio" NAME="ClientIntake_IEP_1" VALUE=1 <<ClientIntake_IEP_1=1>> > Yes
      <INPUT TYPE="radio" NAME="ClientIntake_IEP_1" VALUE=0 <<ClientIntake_IEP_1=0>> > No
    </TD>
  </TR>
  <TR>
    <TD CLASS="strcol" COLSPAN="2" >How long have you been receiving special education classes?</TD>
    <TD CLASS="strcol" COLSPAN="2" >
      <SELECT NAME="ClientIntake_SpecEdLength_1" >[[DBA->selxTable(%form+xPeriod+<<ClientIntake_SpecEdLength_1>>)]]</SELECT>
    </TD>
  </TR>
  <TR>
    <TD CLASS="strcol" COLSPAN="2" >In what grade did you start receiving special education classes?</TD>
    <TD CLASS="strcol" COLSPAN="2" >
      <SELECT NAME="ClientEducation_SpecEdStart_1" >
        [[DBA->selxTable(%form+xSchoolGrades+<<ClientEducation_SpecEdStart_1>>+Descr)]]
      </SELECT> 
    </TD>
  </TR>
  <TR>
    <TD CLASS="strcol" COLSPAN="2" >In the past 90 days of the school year, how many days was the customer absent from school?</TD>
    <TD CLASS="strcol" COLSPAN="2" >
      <INPUT TYPE=text NAME="ClientIntake_AbsentSchool_1" VALUE="<<ClientIntake_AbsentSchool_1>>" ONFOCUS="select()" ONCHANGE="return vNum(this,0,66);" SIZE="2" >
    </TD>
  </TR>
  <TR>
    <TD CLASS="strcol" COLSPAN="2" >In the past 90 days of the school year, how many days was the customer suspended from school?</TD>
    <TD CLASS="strcol" COLSPAN="2" >
      <INPUT TYPE=text NAME="ClientIntake_SuspendedSchool_1" VALUE="<<ClientIntake_SuspendedSchool_1>>" ONFOCUS="select()" ONCHANGE="return vNum(this,0,66);" SIZE="2" >
    </TD>
  </TR>
  <TR ><TD CLASS="strcol hdrtxt" COLSPAN="4" >Collaboration with the School System (school age children only)</TD></TR>
  <TR>
    <TD CLASS="strcol" COLSPAN="4" >
      <TEXTAREA NAME="ClientIntake_SchoolCollab_1" COLS=90 ROWS=12 WRAP=virtual ><<ClientIntake_SchoolCollab_1>></TEXTAREA>
    </TD>
  </TR>
    </TABLE></TD></TR>
</TABLE>
<TABLE CLASS="port fullsize" >
    <TR ><TD ><TABLE CLASS="home fullsize" >
  <TR ><TD CLASS="port heading" COLSPAN="2" >VOCATIONAL HISTORY</TD></TR>
  <TR ><TD CLASS="port hdrtxt" COLSPAN="2" >Employment</TD></TR>
  <TR>
    <TD CLASS="strcol" >Employment Status</TD>
    <TD CLASS="strcol" >
      <SELECT NAME="Client_EmplStat_1" >[[DBA->selxTable(%form+xEmplStat+<<Client_EmplStat_1>>+CDC Descr)]]</SELECT>
    </TD>
  </TR>
  <TR>
    <TD CLASS="strcol" >Employment Type</TD>
    <TD CLASS="strcol" >
      <SELECT NAME="Client_EmplType_1" >[[DBA->selxTable(%form+xEmplType+<<Client_EmplType_1>>+CDC Descr)]]</SELECT>
    </TD>
  </TR>
  <TR ><TD CLASS="strcol" COLSPAN="2" >Have you worked at any job outside the home?</TD></TR>
  <TR >
    <TD CLASS="strcol" >If so, what type of work was it?</TD>
    <TD CLASS="strcol" >
      <INPUT TYPE=text NAME="ClientIntake_JobDesc_1" VALUE="<<ClientIntake_JobDesc_1>>" ONFOCUS="select()" SIZE=30>
    </TD>
  </TR>
  <TR >
    <TD CLASS="strcol" >For how long?</TD>
    <TD CLASS="strcol" >
      <SELECT NAME="ClientIntake_JobLength_1" >[[DBA->selxTable(%form+xPeriod+<<ClientIntake_JobLength_1>>)]]</SELECT>
    </TD>
  </TR>
  <TR >
    <TD CLASS="strcol" >Last time you worked?</TD>
    <TD CLASS="strcol" >
      <INPUT TYPE=text NAME="ClientIntake_JobLengthLast_1" VALUE="<<ClientIntake_JobLengthLast_1>>" ONFOCUS="select()" ONCHANGE="return qDate(this)" SIZE=10>
    </TD>
  </TR>
  <TR >
    <TD CLASS="strcol" >What type?</TD>
    <TD CLASS="strcol" >
      <INPUT TYPE=text NAME="ClientIntake_JobDescLast_1" VALUE="<<ClientIntake_JobDescLast_1>>" ONFOCUS="select()" SIZE=30>
    </TD>
  </TR>
  <TR ><TD CLASS="strcol" COLSPAN="2" >Do you have special job skills or training?</TD></TR>
  <TR >
    <TD CLASS="strcol" >What type?</TD>
    <TD CLASS="strcol" >
      <INPUT TYPE=text NAME="ClientIntake_JobSkills_1" VALUE="<<ClientIntake_JobSkills_1>>" ONFOCUS="select()" SIZE=30>
    </TD>
  </TR>
  <TR ><TD CLASS="strcol" COLSPAN="2" >What type of work do you intend to do or have you done as a career?</TD></TR>
  <TR >
    <TD CLASS="strcol" COLSPAN="2" >
      <INPUT TYPE=text NAME="ClientIntake_JobCareer_1" VALUE="<<ClientIntake_JobCareer_1>>" ONFOCUS="select()" SIZE=30>
    </TD>
  </TR>
    </TABLE></TD></TR>
    <TR ><TD ><TABLE CLASS="home fullsize" >
  <TR ><TD CLASS="port hdrtxt" COLSPAN="2" >Military History</TD></TR>
  <TR>
    <TD CLASS="strcol" >Military Service?</TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="radio" NAME="ClientIntake_MilFlag_1" VALUE=0 <<ClientIntake_MilFlag_1=0>> > None
      <INPUT TYPE="radio" NAME="ClientIntake_MilFlag_1" VALUE=1 <<ClientIntake_MilFlag_1=1>> > Active
      <INPUT TYPE="radio" NAME="ClientIntake_MilFlag_1" VALUE=2 <<ClientIntake_MilFlag_1=2>> > Reserve
      <INPUT TYPE="radio" NAME="ClientIntake_MilFlag_1" VALUE=3 <<ClientIntake_MilFlag_1=3>> > Discharged
      <INPUT TYPE="radio" NAME="ClientIntake_MilFlag_1" VALUE=4 <<ClientIntake_MilFlag_1=4>> > Retired
    </TD>
  </TR>
  <TR>
    <TD CLASS="strcol" >What branch of service?</TD>
    <TD CLASS="strcol" >
      <SELECT NAME="ClientIntake_MilBranch_1" >[[DBA->selxTable(%form+xMilBranch+<<ClientIntake_MilBranch_1>>)]]</SELECT>
    </TD>
  </TR>
  <TR>
    <TD CLASS="strcol" >Type of discharge?</TD>
    <TD CLASS="strcol" >
      <SELECT NAME="ClientIntake_MilDis_1" >[[DBA->selxTable(%form+xMilDis+<<ClientIntake_MilDis_1>>)]]</SELECT>
    </TD>
  </TR>
  <TR>
    <TD CLASS="strcol" >Relatives with Military Service?<BR>(use ctrl-key for multiples)</TD>
    <TD CLASS="strcol" >
      <SELECT NAME="ClientIntake_MilRel_1" MULTIPLE SIZE="5" >
        [[DBA->selxTable(%form+xRelationship+<<ClientIntake_MilRel_1>>+Descr)]]
      </SELECT>
    </TD>
  </TR>
    </TABLE></TD></TR>
</TABLE>

<TABLE CLASS="main fullsize" >
  <TR >
    <TD CLASS="numcol" >
      <INPUT TYPE="submit" ONCLICK="return validate(this.form);" NAME="UpdateTables=all&[[myForm->genLink(ClientIntake+ClientMentalStatus.cgi)]]" VALUE="Add/Update -> Mental Status">
      <INPUT TYPE="submit" ONCLICK="return validate(this.form);" NAME="UpdateTables=all&misPOP=1" VALUE="Add/Update">
    </TD>
  </TR>
</TABLE>

<INPUT TYPE="hidden" NAME="post_update" VALUE="PostUpd->updPA(%form+<<<Client_ClientID_1>>>)" >
</LOADHIDDEN>
</FORM>
<SCRIPT LANGUAGE="JavaScript">
document.History.elements[0].focus();
createFLD(document.History.ClientIntake_LastSchoolDist_1,'/cgi/bin/verify.pl?mlt=<<<mlt>>>&type=LastSchoolName','selLastSchoolName','LastSchoolDist','LastSchoolName');
</SCRIPT>

[[myHTML->rightpane(%form+search)]]
