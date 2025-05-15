[[myHTML->newPage(%form+Client ASI)]]
[[[DBA->setClientASI(%form)]]]

<SCRIPT LANGUAGE="JavaScript" SRC="/src/cgi/js/NoEnter.js"> </SCRIPT>
<SCRIPT LANGUAGE="JavaScript" SRC="/src/cgi/js/vEntry.js"> </SCRIPT>
<SCRIPT LANGUAGE="JavaScript" SRC="/src/cgi/js/vClientASI.js"> </SCRIPT>
<SCRIPT LANGUAGE="JavaScript" SRC="/src/cgi/js/vDate.js"> </SCRIPT>
<SCRIPT LANGUAGE="JavaScript" SRC="/src/cgi/js/vTime.js"> </SCRIPT>
<SCRIPT LANGUAGE="JavaScript" SRC="/src/cgi/js/vSSN.js"> </SCRIPT>
<SCRIPT LANGUAGE="JavaScript" SRC="/src/cgi/js/vNum.js"> </SCRIPT>
<SCRIPT LANGUAGE="JavaScript" > 
function setSP(form,id,fld)
{
  if ( id == "M9" )
  { form["ClientASI_SPMedical_1"].value = fld.value; }
  else if ( id == "SPMedical" )
  { form["ClientASI_M9_1"].value = fld.value; }

  else if ( id == "E22" )
  { form["ClientASI_SPEmpSup_1"].value = fld.value; }
  else if ( id == "SPEmpSup" )
  { form["ClientASI_E22_1"].value = fld.value; }

  else if ( id == "D32" )
  { form["ClientASI_SPAlcohol_1"].value = fld.value; }
  else if ( id == "SPAlcohol" )
  { form["ClientASI_D32_1"].value = fld.value; }

  else if ( id == "D33" )
  { form["ClientASI_SPDrugs_1"].value = fld.value; }
  else if ( id == "SPDrugs" )
  { form["ClientASI_D33_1"].value = fld.value; }

  else if ( id == "L30" )
  { form["ClientASI_SPLegal_1"].value = fld.value; }
  else if ( id == "SPLegal" )
  { form["ClientASI_L30_1"].value = fld.value; }

  else if ( id == "F36" )
  { form["ClientASI_SPFamily_1"].value = fld.value; }
  else if ( id == "SPFamily" )
  { form["ClientASI_F36_1"].value = fld.value; }

  else if ( id == "P21" )
  { form["ClientASI_SPPsych_1"].value = fld.value; }
  else if ( id == "SPPsych" )
  { form["ClientASI_P21_1"].value = fld.value; }
  return true;
}
</SCRIPT>

<FORM NAME="ClientASI" ACTION="/cgi/bin/mis.cgi" METHOD="POST" >
<TABLE CLASS="main fullsize" >
  <TR >
    <TD CLASS="strcol" >
      <<<Client_FName_1>>> <<<Client_MName_1>>> <<<Client_LName_1>>> (<<<Client_ClientID_1>>>) <<<Client_SSN_1>>>
      <BR>
      Addiction Severity Index, Fifth Edition
    </TD>
    <TD CLASS="numcol" >[[gHTML->setLINKS(%form+back)]]</TD>
  </TR>
</TABLE>
<TABLE CLASS="home fullsize" >
  <TR ><TD CLASS="port hdrtxt" >Page 1<BR>General Information</TD></TR>
    <TR ><TD ><TABLE CLASS="home fullsize" >
  <TR >
    <TD CLASS="strcol" WIDTH="60%" >
      G1. ID No.
    </TD>
    <TD CLASS="strcol" >
      <<<Client_ClientID_1>>>
    </TD>
  </TR>
  <TR >
    <TD CLASS="strcol" WIDTH="60%" >
      G2. SS No.
    </TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="TEXT" NAME="ClientASI_G2_1" VALUE="<<ClientASI_G2_1>>" ONFOCUS="select()" ONCHANGE="return vSSN(this)" SIZE="11" >
    </TD>
  </TR>
    </TABLE></TD></TR>
    <TR ><TD ><TABLE CLASS="home fullsize" >
  <TR >
    <TD CLASS="strcol" WIDTH="60%" >
      G4. Date of Admission
    </TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="TEXT" NAME="ClientASI_G4_1" VALUE="<<ClientASI_G4_1>>" ONFOCUS="select()" ONCHANGE="return vDate(this,0,this.form)" SIZE="10" >
    </TD>
  </TR>
  <TR >
    <TD CLASS="strcol" WIDTH="60%" >
      G5. Date of Interview
    </TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="TEXT" NAME="ClientASI_G5_1" VALUE="<<ClientASI_G5_1>>" ONFOCUS="select()" ONCHANGE="return vDate(this,0,this.form)" SIZE="10" >
    </TD>
  </TR>
  <TR >
    <TD CLASS="strcol" WIDTH="60%" >
      G6. Time Begun
    </TD>
    <TD CLASS="strcol" >
      <INPUT TYPE=text NAME="ClientASI_G6_1" VALUE="<<ClientASI_G6_1>>" ONFOCUS="select()" ONCHANGE="return vTime(this,1,this)" MAXLENGTH=10 SIZE="10" >
    </TD>
  </TR>
  <TR >
    <TD CLASS="strcol" WIDTH="60%" >
      G7. Time Ended
    </TD>
    <TD CLASS="strcol" >
      <INPUT TYPE=text NAME="ClientASI_G7_1" VALUE="<<ClientASI_G7_1>>" ONFOCUS="select()" ONCHANGE="return vTime(this,1,this)" MAXLENGTH=10 SIZE="10" >
    </TD>
  </TR>
    </TABLE></TD></TR>
    <TR ><TD ><TABLE CLASS="home fullsize" >
  <TR >
    <TD CLASS="strcol" WIDTH="60%" >
      G8. Class
    </TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="radio" NAME="ClientASI_G8_1" VALUE=1 <<ClientASI_G8_1=1>> > Intake
      <INPUT TYPE="radio" NAME="ClientASI_G8_1" VALUE=2 <<ClientASI_G8_1=2>> > Follow-up
    </TD>
  </TR>
  <TR >
    <TD CLASS="strcol" WIDTH="60%" >
      G9. Contact Code
    </TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="radio" NAME="ClientASI_G9_1" VALUE=1 <<ClientASI_G9_1=1>> > In person
      <INPUT TYPE="radio" NAME="ClientASI_G9_1" VALUE=2 <<ClientASI_G9_1=2>> > Telephone (Intake ASI must be in person)
    </TD>
  </TR>
    </TABLE></TD></TR>
    <TR ><TD ><TABLE CLASS="home fullsize" >
  <TR >
    <TD CLASS="strcol" WIDTH="60%" >
      G10. Gender
    </TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="radio" NAME="ClientASI_G10_1" VALUE="M" <<ClientASI_G10_1=M>> > Male
      <INPUT TYPE="radio" NAME="ClientASI_G10_1" VALUE="F" <<ClientASI_G10_1=F>> > Female
    </TD>
  </TR>
  <TR >
    <TD CLASS="strcol" WIDTH="60%" >
      G11. Interviewer Code No. / Initials
    </TD>
    <TD CLASS="strcol" >
      <SELECT NAME="ClientASI_G11_1">[[DBA->selProviders(%form+<<ClientASI_G11_1>>)]]</SELECT> 
    </TD>
  </TR>
    </TABLE></TD></TR>
    <TR ><TD ><TABLE CLASS="home fullsize" >
  <TR >
    <TD CLASS="strcol" WIDTH="60%" >
      G14. How long have you lived at this address?
    </TD>
    <TD CLASS="strcol" >
      <INPUT TYPE=text NAME="ClientASI_G14Y_1" VALUE="<<ClientASI_G14Y_1>>" ONFOCUS="select()" ONCHANGE="return vNum(this,0,99);" SIZE="2" > Years
      <INPUT TYPE=text NAME="ClientASI_G14M_1" VALUE="<<ClientASI_G14M_1>>" ONFOCUS="select()" ONCHANGE="return vNum(this,0,12);" SIZE="2" > Months
    </TD>
  </TR>
  <TR >
    <TD CLASS="strcol" WIDTH="60%" >
      G15. Is this residence owned by you or your family?
    </TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="radio" NAME="ClientASI_G15_1" VALUE=0 <<ClientASI_G15_1=0>> > No
      <INPUT TYPE="radio" NAME="ClientASI_G15_1" VALUE=1 <<ClientASI_G15_1=1>> > Yes
    </TD>
  </TR>
    </TABLE></TD></TR>
    <TR ><TD ><TABLE CLASS="home fullsize" >
  <TR >
    <TD CLASS="strcol" WIDTH="60%" >
      G16. Date of birth
    </TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="TEXT" NAME="ClientASI_G16_1" VALUE="<<ClientASI_G16_1>>" ONFOCUS="select()" ONCHANGE="return vDate(this,0,this.form)" SIZE="10" >
    </TD>
  </TR>
  <TR >
    <TD CLASS="strcol" WIDTH="60%" >
      G17. Of what race do you consider yourself
    </TD>
    <TD CLASS="strcol" >
      <SELECT NAME="ClientASI_G17_1" >
        [[DBA->selxTable(%form+xRaces+<<ClientASI_G17_1>>+Descr)]]
      </SELECT> 
    </TD>
  </TR>
  <TR >
    <TD CLASS="strcol" WIDTH="60%" >
      G18. Do you have a religious preference?
    </TD>
    <TD CLASS="strcol" >
      <SELECT NAME="ClientASI_G18_1">
        [[DBA->selxTable(%form+xReligiousAffiliation+<<ClientASI_G18_1>>+Descr)]]
      </SELECT> 
    </TD>
  </TR>
    </TABLE></TD></TR>
    <TR ><TD ><TABLE CLASS="home fullsize" >
  <TR >
    <TD CLASS="strcol" WIDTH="60%" >
      G19. Have you been in a controlled environment in the past 30 days?
    </TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="radio" NAME="ClientASI_G19_1" VALUE=1 <<ClientASI_G19_1=1>> > No<BR>
      <INPUT TYPE="radio" NAME="ClientASI_G19_1" VALUE=2 <<ClientASI_G19_1=2>> > Jail<BR>
      <INPUT TYPE="radio" NAME="ClientASI_G19_1" VALUE=3 <<ClientASI_G19_1=3>> > Alcohol/Drug Treatment<BR>
      <INPUT TYPE="radio" NAME="ClientASI_G19_1" VALUE=4 <<ClientASI_G19_1=4>> > Medical Treatment<BR>
      <INPUT TYPE="radio" NAME="ClientASI_G19_1" VALUE=5 <<ClientASI_G19_1=5>> > Psychiatric Treatment<BR>
      <INPUT TYPE="radio" NAME="ClientASI_G19_1" VALUE=6 <<ClientASI_G19_1=6>> > Other:
      <INPUT TYPE="TEXT" NAME="ClientASI_G19T_1" VALUE="<<ClientASI_G19T_1>>" ONFOCUS="select()" SIZE=30>
      <BR>� A place, theoretically, without access to drugs/alcohol.
    </TD>
  </TR>
  <TR >
    <TD CLASS="strcol" WIDTH="60%" >
      G20. How many days?
    </TD>
    <TD CLASS="strcol" >
      <INPUT TYPE=text NAME="ClientASI_G20_1" VALUE="<<ClientASI_G20_1>>" ONFOCUS="select()" ONCHANGE="return vNum(this,0,30);" SIZE="2" >
      �"0" if Question G19 is No.
      <BR>Refers to total number of days detained in the past 30 days.
    </TD>
  </TR>
    </TABLE></TD></TR>
    <TR ><TD ><TABLE CLASS="home fullsize" >
  <TR ><TD CLASS="strcol" COLSPAN="3" >SEVERITY PROFILE</TD></TR>
  <TR >
    <TD CLASS="strcol" WIDTH="5%" >&nbsp;</TD>
    <TD CLASS="strcol" >Medical</TD>
    <TD CLASS="strcol" >
      <SELECT NAME="ClientASI_SPMedical_1" ONCHANGE="return setSP(this.form,'SPMedical',this);" >[[DBA->selxTable(%form+xSeverityRatings+<<ClientASI_SPMedical_1>>+ID Descr)]]</SELECT> 
    </TD>
  </TR>
  <TR >
    <TD CLASS="strcol" WIDTH="5%" >&nbsp;</TD>
    <TD CLASS="strcol" >Emp / Sup</TD>
    <TD CLASS="strcol" >
      <SELECT NAME="ClientASI_SPEmpSup_1" ONCHANGE="return setSP(this.form,'SPEmpSup',this);" >[[DBA->selxTable(%form+xSeverityRatings+<<ClientASI_SPEmpSup_1>>+ID Descr)]]</SELECT> 
    </TD>
  </TR>
  <TR >
    <TD CLASS="strcol" WIDTH="5%" >&nbsp;</TD>
    <TD CLASS="strcol" >Alcohol</TD>
    <TD CLASS="strcol" >
      <SELECT NAME="ClientASI_SPAlcohol_1" ONCHANGE="return setSP(this.form,'SPAlcohol',this);" >[[DBA->selxTable(%form+xSeverityRatings+<<ClientASI_SPAlcohol_1>>+ID Descr)]]</SELECT> 
    </TD>
  </TR>
  <TR >
    <TD CLASS="strcol" WIDTH="5%" >&nbsp;</TD>
    <TD CLASS="strcol" >Drugs</TD>
    <TD CLASS="strcol" >
      <SELECT NAME="ClientASI_SPDrugs_1" ONCHANGE="return setSP(this.form,'SPDrugs',this);" >[[DBA->selxTable(%form+xSeverityRatings+<<ClientASI_SPDrugs_1>>+ID Descr)]]</SELECT> 
    </TD>
  </TR>
  <TR >
    <TD CLASS="strcol" WIDTH="5%" >&nbsp;</TD>
    <TD CLASS="strcol" >Legal</TD>
    <TD CLASS="strcol" >
      <SELECT NAME="ClientASI_SPLegal_1" ONCHANGE="return setSP(this.form,'SPLegal',this);" >[[DBA->selxTable(%form+xSeverityRatings+<<ClientASI_SPLegal_1>>+ID Descr)]]</SELECT> 
    </TD>
  </TR>
  <TR >
    <TD CLASS="strcol" WIDTH="5%" >&nbsp;</TD>
    <TD CLASS="strcol" >Fam / Soc</TD>
    <TD CLASS="strcol" >
      <SELECT NAME="ClientASI_SPFamily_1" ONCHANGE="return setSP(this.form,'SPFamily',this);" >[[DBA->selxTable(%form+xSeverityRatings+<<ClientASI_SPFamily_1>>+ID Descr)]]</SELECT> 
    </TD>
  </TR>
  <TR >
    <TD CLASS="strcol" WIDTH="5%" >&nbsp;</TD>
    <TD CLASS="strcol" >Psychiatric</TD>
    <TD CLASS="strcol" >
      <SELECT NAME="ClientASI_SPPsych_1" ONCHANGE="return setSP(this.form,'SPPsych',this);" >[[DBA->selxTable(%form+xSeverityRatings+<<ClientASI_SPPsych_1>>+ID Descr)]]</SELECT> 
    </TD>
  </TR>
    </TABLE></TD></TR>
</TABLE>
<TABLE CLASS="home fullsize" >
  <TR ><TD CLASS="port hdrtxt" >Page 2<BR> Medical Status</TD></TR>
    <TR ><TD ><TABLE CLASS="home fullsize" >
  <TR >
    <TD CLASS="strcol" WIDTH="60%" >
      M1. How many times in your life have you been hospitalized for medical problems?
      <BR>� Include O.D.'s and D.T.'s. Exclude detox, alcohol/drug, psychiatric treatment and childbirth (if no complications). Enter the number of overnight hospitalizations for medical problems.
    </TD>
    <TD CLASS="strcol" >
      <INPUT TYPE=text NAME="ClientASI_M1_1" VALUE="<<ClientASI_M1_1>>" ONFOCUS="select()" ONCHANGE="return vNum(this,0,99);" SIZE="2" >
    </TD>
  </TR>
  <TR >
    <TD CLASS="strcol" WIDTH="60%" >
      M2. How long ago was your last hospitalization for a physical problem?
      <BR>� If no hospitalizations in Question M1, then this is coded "NN".
    </TD>
    <TD CLASS="strcol" >
      <INPUT TYPE=text NAME="ClientASI_M2Y_1" VALUE="<<ClientASI_M2Y_1>>" ONFOCUS="select()" ONCHANGE="return vNum(this,0,99,'NN');" SIZE="2" > Years
      <INPUT TYPE=text NAME="ClientASI_M2M_1" VALUE="<<ClientASI_M2M_1>>" ONFOCUS="select()" ONCHANGE="return vNum(this,0,12,'NN');" SIZE="2" > Months
    </TD>
  </TR>
    </TABLE></TD></TR>
    <TR ><TD ><TABLE CLASS="home fullsize" >
  <TR >
    <TD CLASS="strcol" WIDTH="60%" >
      M3. Do you have any chronic medical problems which continue to interfere with your life?
      <BR>� A chronic medical condition is a serious physical condition that requires regular care, (i.e., medication, dietary restriction) preventing full advantage of their abilities.
    </TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="radio" NAME="ClientASI_M3_1" VALUE=0 <<ClientASI_M3_1=0>> > No
      <INPUT TYPE="radio" NAME="ClientASI_M3_1" VALUE=1 <<ClientASI_M3_1=1>> > Yes � If "Yes", specify in comments.
    </TD>
  </TR>
  <TR >
    <TD CLASS="strcol" WIDTH="60%" >
      M4. Are you taking any prescribed medication on a regular basis for a physical problem?
      <BR>� Medication prescribed by a MD for medical conditions; not psychiatric medicines. Include medicines prescribed whether or not the patient is currently taking them. The intent is to verify chronic medical problems.
    </TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="radio" NAME="ClientASI_M4_1" VALUE=0 <<ClientASI_M4_1=0>> > No
      <INPUT TYPE="radio" NAME="ClientASI_M4_1" VALUE=1 <<ClientASI_M4_1=1>> > Yes � If Yes, specify in comments.
    </TD>
  </TR>
  <TR >
    <TD CLASS="strcol" WIDTH="60%" >
      M5. Do you receive a pension for a physical disability?
      <BR>� Include Workers' compensation, exclude psychiatric disability.
    </TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="radio" NAME="ClientASI_M5_1" VALUE=0 <<ClientASI_M5_1=0>> > No
      <INPUT TYPE="radio" NAME="ClientASI_M5_1" VALUE=1 <<ClientASI_M5_1=1>> > Yes � If Yes, specify in comments.
    </TD>
  </TR>
    </TABLE></TD></TR>
    <TR ><TD ><TABLE CLASS="home fullsize" >
  <TR >
    <TD CLASS="strcol" WIDTH="60%" >
      M6. How many days have you experienced medical problems in the past 30 days?
      <BR>� Include flu, colds, etc. Include serious ailments related to drugs/alcohol, which would continue even if the patient were abstinent (e.g., cirrhosis of liver, abscesses from needles, etc.).
    </TD>
    <TD CLASS="strcol" >
      <INPUT TYPE=text NAME="ClientASI_M6_1" VALUE="<<ClientASI_M6_1>>" ONFOCUS="select()" ONCHANGE="return vNum(this,0,30);" SIZE="2" >
    </TD>
  </TR>
  <TR >
    <TD CLASS="strcol" COLSPAN="2" >
      For Questions M7 & M8, ask the patient to use the Patient Rating scale.
    </TD>
  </TR>
  <TR >
    <TD CLASS="strcol" WIDTH="60%" >
      M7. How troubled or bothered have you been by these medical problems in the past 30 days?
      <BR>� Restrict response to problem days of Question M6.
    </TD>
    <TD CLASS="strcol" >
      <SELECT NAME="ClientASI_M7_1">[[DBA->selxTable(%form+xRateScale+<<ClientASI_M7_1>>+ID Descr)]]</SELECT> 
    </TD>
  </TR>
  <TR >
    <TD CLASS="strcol" WIDTH="60%" >
      M8. How important to you now is treatment for these medical problems?
      <BR>� If client is currently receiving medical treatment, refer to the need for additional medical treatment by the patient.
    </TD>
    <TD CLASS="strcol" >
      <SELECT NAME="ClientASI_M8_1">[[DBA->selxTable(%form+xRateScale+<<ClientASI_M8_1>>+ID Descr)]]</SELECT> 
    </TD>
  </TR>
    </TABLE></TD></TR>
    <TR ><TD ><TABLE CLASS="home fullsize" >
  <TR >
    <TD CLASS="strcol" COLSPAN="2" >
      INTERVIEWER SEVERITY RATING
    </TD>
  </TR>
  <TR >
    <TD CLASS="strcol" WIDTH="60%" >
      M9. How would you rate the patient's need for medical treatment?
      <BR>� Refers to the patient's need for additional medical treatment.
    </TD>
    <TD CLASS="strcol" >
      <SELECT NAME="ClientASI_M9_1" ONCHANGE="return setSP(this.form,'M9',this);" >[[DBA->selxTable(%form+xSeverityRatings+<<ClientASI_M9_1>>+ID Descr)]]</SELECT> 
    </TD>
  </TR>
    </TABLE></TD></TR>
    <TR ><TD ><TABLE CLASS="home fullsize" >
  <TR >
    <TD CLASS="strcol" COLSPAN="2" >
      CONFIDENCE RATINGS
      <BR>Is the above information significantly distorted by:
    </TD>
  </TR>
  <TR >
    <TD CLASS="strcol" WIDTH="60%" >
      M10. Patient's misrepresentation?
    </TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="radio" NAME="ClientASI_M10_1" VALUE=0 <<ClientASI_M10_1=0>> > No
      <INPUT TYPE="radio" NAME="ClientASI_M10_1" VALUE=1 <<ClientASI_M10_1=1>> > Yes
    </TD>
  </TR>
  <TR >
    <TD CLASS="strcol" WIDTH="60%" >
      M11. Patient's inability to understand?
    </TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="radio" NAME="ClientASI_M11_1" VALUE=0 <<ClientASI_M11_1=0>> > No
      <INPUT TYPE="radio" NAME="ClientASI_M11_1" VALUE=1 <<ClientASI_M11_1=1>> > Yes
    </TD>
  </TR>
    </TABLE></TD></TR>
    <TR ><TD ><TABLE CLASS="home fullsize" >
  <TR >
    <TD CLASS="strcol" COLSPAN="2" >
      MEDICAL COMMENTS (Include question number with your notes)
      <TEXTAREA NAME="ClientASI_MCOM_1" COLS="90" ROWS="8" WRAP="virtual" ><<ClientASI_MCOM_1>></TEXTAREA>
    </TD>
  </TR>
    </TABLE></TD></TR>
</TABLE>
<TABLE CLASS="home fullsize" >
  <TR ><TD CLASS="port hdrtxt" >Page 3<BR>Employment/Support Status</TD></TR>
    <TR ><TD ><TABLE CLASS="home fullsize" >
  <TR >
    <TD CLASS="strcol" WIDTH="60%" >
      E1. Education completed:
      <BR>� GED = 12 years, note in comments.
      <BR>� Include formal education only.
    </TD>
    <TD CLASS="strcol" >
      <INPUT TYPE=text NAME="ClientASI_E1Y_1" VALUE="<<ClientASI_E1Y_1>>" ONFOCUS="select()" ONCHANGE="return vNum(this,0,99);" SIZE="2" > Years
      <INPUT TYPE=text NAME="ClientASI_E1M_1" VALUE="<<ClientASI_E1M_1>>" ONFOCUS="select()" ONCHANGE="return vNum(this,0,12);" SIZE="2" > Months
    </TD>
  </TR>
  <TR >
    <TD CLASS="strcol" WIDTH="60%" >
      E2. Training or Technical education completed:
      <BR>� Formal/organized training only. For military training, only include training that can be used in civilian life (i.e., electronics, computers)
    </TD>
    <TD CLASS="strcol" >
      <INPUT TYPE=text NAME="ClientASI_E2_1" VALUE="<<ClientASI_E2_1>>" ONFOCUS="select()" ONCHANGE="return vNum(this,0,99);" SIZE="2" > Months
    </TD>
  </TR>
    </TABLE></TD></TR>
    <TR ><TD ><TABLE CLASS="home fullsize" >
  <TR >
    <TD CLASS="strcol" WIDTH="60%" >
      E3. Do you have a profession, trade, or skill?
      <BR>� Employable, transferable skill acquired through training.
    </TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="radio" NAME="ClientASI_E3_1" VALUE=0 <<ClientASI_E3_1=0>> > No
      <INPUT TYPE="radio" NAME="ClientASI_E3_1" VALUE=1 <<ClientASI_E3_1=1>> > Yes
    </TD>
  </TR>
  <TR >
    <TD CLASS="strcol" WIDTH="60%" >&nbsp;</TD>
    <TD CLASS="strcol" >
      � If "Yes" (specify)
      <INPUT TYPE="TEXT" NAME="ClientASI_E3T_1" VALUE="<<ClientASI_E3T_1>>" ONFOCUS="select()" SIZE=30>
    </TD>
  </TR>
    </TABLE></TD></TR>
    <TR ><TD ><TABLE CLASS="home fullsize" >
  <TR >
    <TD CLASS="strcol" WIDTH="60%" >
      E4. Do you have a valid driver's license?
    </TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="radio" NAME="ClientASI_E4_1" VALUE=0 <<ClientASI_E4_1=0>> > No
      <INPUT TYPE="radio" NAME="ClientASI_E4_1" VALUE=1 <<ClientASI_E4_1=1>> > Yes � Valid license; not suspended/revoked. 
    </TD>
  </TR>
  <TR >
    <TD CLASS="strcol" WIDTH="60%" >
      E5. Do you have an automobile available for use?
      <BR> � Does not require ownership, only requires availability on a regular basis.
    </TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="radio" NAME="ClientASI_E5_1" VALUE=0 <<ClientASI_E5_1=0>> > No
      <INPUT TYPE="radio" NAME="ClientASI_E5_1" VALUE=1 <<ClientASI_E5_1=1>> > Yes � If answer to E4 is "No", then E5 must be "No". 
    </TD>
  </TR>
    </TABLE></TD></TR>
    <TR ><TD ><TABLE CLASS="home fullsize" >
  <TR >
    <TD CLASS="strcol" WIDTH="60%" >
      E6. How long was your longest full time job?
      <BR>� Full time = 35+ hours weekly; does not necessarily mean most recent job.
    </TD>
    <TD CLASS="strcol" >
      <INPUT TYPE=text NAME="ClientASI_E6Y_1" VALUE="<<ClientASI_E6Y_1>>" ONFOCUS="select()" ONCHANGE="return vNum(this,0,99);" SIZE="2" > Years
      <INPUT TYPE=text NAME="ClientASI_E6M_1" VALUE="<<ClientASI_E6M_1>>" ONFOCUS="select()" ONCHANGE="return vNum(this,0,12);" SIZE="2" > Months
    </TD>
  </TR>
  <TR >
    <TD CLASS="strcol" WIDTH="60%" >
      E7. Usual (or last) occupation?
      <BR>(use Hollingshead Categories Reference Sheet)
    </TD>
    <TD CLASS="strcol" >
      <SELECT NAME="ClientASI_E7_1">[[DBA->selxTable(%form+xOccupations+<<ClientASI_E7_1>>+ID Descr)]]</SELECT> 
    </TD>
  </TR>
  <TR >
    <TD CLASS="strcol" WIDTH="60%" >&nbsp;</TD>
    <TD CLASS="strcol" >
      (specify)
      <INPUT TYPE="TEXT" NAME="ClientASI_E7T_1" VALUE="<<ClientASI_E7T_1>>" ONFOCUS="select()" SIZE=30>
    </TD>
  </TR>
    </TABLE></TD></TR>
    <TR ><TD ><TABLE CLASS="home fullsize" >
  <TR >
    <TD CLASS="strcol" WIDTH="60%" >
      E8. Does someone contribute to your support in any way?
      <BR>� Is patient receiving any regular support (i.e., cash, food, housing) from family/friend. Include spouse's contribution; exclude support by an institution.
    </TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="radio" NAME="ClientASI_E8_1" VALUE=0 <<ClientASI_E8_1=0>> > No
      <INPUT TYPE="radio" NAME="ClientASI_E8_1" VALUE=1 <<ClientASI_E8_1=1>> > Yes
    </TD>
  </TR>
  <TR >
    <TD CLASS="strcol" WIDTH="60%" >
      E9. Does this constitute the majority of your support?
    </TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="radio" NAME="ClientASI_E9_1" VALUE=0 <<ClientASI_E9_1=0>> > No � If E8 is "No", then E9 is "N".
      <INPUT TYPE="radio" NAME="ClientASI_E9_1" VALUE=1 <<ClientASI_E9_1=1>> > Yes
    </TD>
  </TR>
    </TABLE></TD></TR>
    <TR ><TD ><TABLE CLASS="home fullsize" >
  <TR >
    <TD CLASS="strcol" WIDTH="60%" >
      E10. Usual employment pattern, past three years?
      <BR>� Answer should represent the majority of the last 3 years, not just the most recent selection. If there are equal times for more than one category, select that which best represents the current situation.
    </TD>
    <TD CLASS="strcol" >
      <SELECT NAME="ClientASI_E10_1">[[DBA->selxTable(%form+xEmployment+<<ClientASI_E10_1>>+ID Descr)]]</SELECT> 
    </TD>
  </TR>
    </TABLE></TD></TR>
    <TR ><TD ><TABLE CLASS="home fullsize" >
  <TR >
    <TD CLASS="strcol" WIDTH="60%" >
      E11. How many days were you paid for working in the past 30?
      <BR>� Include "under the table" work, paid sick days and vacation.
    </TD>
    <TD CLASS="strcol" >
      <INPUT TYPE=text NAME="ClientASI_E11_1" VALUE="<<ClientASI_E11_1>>" ONFOCUS="select()" ONCHANGE="return vNum(this,0,30);" SIZE="2" >
    </TD>
  </TR>
    </TABLE></TD></TR>
</TABLE>
<TABLE CLASS="home fullsize" >
  <TR ><TD CLASS="port hdrtxt" >Page 4<BR>Employment/Support (cont.)</TD></TR>
    <TR ><TD ><TABLE CLASS="home fullsize" >
  <TR >
    <TD CLASS="strcol" COLSPAN="2" >
      For questions E12-17: How much money did you receive from the following sources in the past 30 days?
    </TD>
  </TR>
  <TR >
    <TD CLASS="strcol" WIDTH="60%" >
      E12. Employment?
      <BR>� Net or "take home" pay, include any "under the table" money.
    </TD>
    <TD CLASS="strcol" >
      $<INPUT TYPE=text NAME="ClientASI_E12_1" VALUE="<<ClientASI_E12_1>>" ONFOCUS="select()" ONCHANGE="return vNum(this,0,99999);" SIZE="12" >
    </TD>
  </TR>
  <TR >
    <TD CLASS="strcol" WIDTH="60%" >
      E13. Unemployment Compensation?
    </TD>
    <TD CLASS="strcol" >
      $<INPUT TYPE=text NAME="ClientASI_E13_1" VALUE="<<ClientASI_E13_1>>" ONFOCUS="select()" ONCHANGE="return vNum(this,0,99999);" SIZE="12" >
    </TD>
  </TR>
  <TR >
    <TD CLASS="strcol" WIDTH="60%" >
      E14. Welfare?
      <BR>� Include food stamps, transportation money provided by an agency to go to and from treatment.
    </TD>
    <TD CLASS="strcol" >
      $<INPUT TYPE=text NAME="ClientASI_E14_1" VALUE="<<ClientASI_E14_1>>" ONFOCUS="select()" ONCHANGE="return vNum(this,0,99999);" SIZE="12" >
    </TD>
  </TR>
  <TR >
    <TD CLASS="strcol" WIDTH="60%" >
      E15. Pensions, benefits or Social Security?
      <BR>� Include disability, pensions, retirement, veteran's benefits, SSI & workers' compensation.
    </TD>
    <TD CLASS="strcol" >
      $<INPUT TYPE=text NAME="ClientASI_E15_1" VALUE="<<ClientASI_E15_1>>" ONFOCUS="select()" ONCHANGE="return vNum(this,0,99999);" SIZE="12" >
    </TD>
  </TR>
  <TR >
    <TD CLASS="strcol" WIDTH="60%" >
      E16. Mate, family, or friends?
      <BR>� Money for personal expenses, (i.e. clothing), include unreliable sources of income.  Record cash payments only, include windfalls (unexpected), money from loans, legal gambling, inheritance, tax returns, etc.).
    </TD>
    <TD CLASS="strcol" >
      $<INPUT TYPE=text NAME="ClientASI_E16_1" VALUE="<<ClientASI_E16_1>>" ONFOCUS="select()" ONCHANGE="return vNum(this,0,99999);" SIZE="12" >
    </TD>
  </TR>
    </TABLE></TD></TR>
    <TR ><TD ><TABLE CLASS="home fullsize" >
  <TR >
    <TD CLASS="strcol" WIDTH="60%" >
      E17. Illegal?
      <BR>� Cash obtained from drug dealing, stealing, fencing stolen goods, illegal gambling, prostitution, etc. Do not attempt to convert drugs exchanged to a dollar value.
    </TD>
    <TD CLASS="strcol" >
      $<INPUT TYPE=text NAME="ClientASI_E17_1" VALUE="<<ClientASI_E17_1>>" ONFOCUS="select()" ONCHANGE="return vNum(this,0,99999);" SIZE="12" >
    </TD>
  </TR>
    </TABLE></TD></TR>
    <TR ><TD ><TABLE CLASS="home fullsize" >
  <TR >
    <TD CLASS="strcol" WIDTH="60%" >
      E18. How many people depend on you for the majority of their food, shelter, etc.?
      <BR>� Must be regularly depending on patient, do include alimony/child support, do not include the patient or self-supporting spouse, etc.
    </TD>
    <TD CLASS="strcol" >
      <INPUT TYPE=text NAME="ClientASI_E18_1" VALUE="<<ClientASI_E18_1>>" ONFOCUS="select()" ONCHANGE="return vNum(this,0,30);" SIZE="2" >
    </TD>
  </TR>
    </TABLE></TD></TR>
    <TR ><TD ><TABLE CLASS="home fullsize" >
  <TR >
    <TD CLASS="strcol" WIDTH="60%" >
      E19. How many days have you experienced employment problems in the past 30?
      <BR>� Include inability to find work, if they are actively looking for work, or problems with present job in which that job is jeopardized.
    </TD>
    <TD CLASS="strcol" >
      <INPUT TYPE=text NAME="ClientASI_E19_1" VALUE="<<ClientASI_E19_1>>" ONFOCUS="select()" ONCHANGE="return vNum(this,0,30);" SIZE="2" >
    </TD>
  </TR>
  <TR >
    <TD CLASS="strcol" COLSPAN="2" >
      For Questions E20 & E21, ask the patient to use the Patient Rating scale.
    </TD>
  </TR>
  <TR >
    <TD CLASS="strcol" WIDTH="60%" >
      E20. How troubled or bothered have you been by these employment problems in the past 30 days?
      <BR>� If the patient has been incarcerated or detained during the past 30 days, they cannot have employment problems.  In that case an "N" response is indicated.
    </TD>
    <TD CLASS="strcol" >
      <SELECT NAME="ClientASI_E20_1">[[DBA->selxTable(%form+xRateScale+<<ClientASI_E20_1>>+ID Descr)]]</SELECT> 
    </TD>
  </TR>
  <TR >
    <TD CLASS="strcol" WIDTH="60%" >
      E21. How important to you now is counseling for these employment problems?
      <BR>� Stress help in finding or preparing for a job, not giving them a job.
    </TD>
    <TD CLASS="strcol" >
      <SELECT NAME="ClientASI_E21_1">[[DBA->selxTable(%form+xRateScale+<<ClientASI_E21_1>>+ID Descr)]]</SELECT> 
    </TD>
  </TR>
    </TABLE></TD></TR>
    <TR ><TD ><TABLE CLASS="home fullsize" >
  <TR >
    <TD CLASS="strcol" COLSPAN="2" >
      INTERVIEWER SEVERITY RATING
    </TD>
  </TR>
  <TR >
    <TD CLASS="strcol" WIDTH="60%" >
      E22. How would you rate the patient's need for employment counseling?
    </TD>
    <TD CLASS="strcol" >
      <SELECT NAME="ClientASI_E22_1" ONCHANGE="return setSP(this.form,'E22',this);" >[[DBA->selxTable(%form+xSeverityRatings+<<ClientASI_E22_1>>+ID Descr)]]</SELECT> 
    </TD>
  </TR>
    </TABLE></TD></TR>
    <TR ><TD ><TABLE CLASS="home fullsize" >
  <TR >
    <TD CLASS="strcol" COLSPAN="2" >
      CONFIDENCE RATINGS
    </TD>
  </TR>
  <TR >
    <TD CLASS="strcol" COLSPAN="2" >
      Is the above information significantly distorted by:
    </TD>
  </TR>
  <TR >
    <TD CLASS="strcol" WIDTH="60%" >
      E23. Patient's misrepresentation?
    </TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="radio" NAME="ClientASI_E23_1" VALUE=0 <<ClientASI_E23_1=0>> > No
      <INPUT TYPE="radio" NAME="ClientASI_E23_1" VALUE=1 <<ClientASI_E23_1=1>> > Yes
    </TD>
  </TR>
  <TR >
    <TD CLASS="strcol" WIDTH="60%" >
      E24. Patient's inability to understand?
    </TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="radio" NAME="ClientASI_E24_1" VALUE=0 <<ClientASI_E24_1=0>> > No
      <INPUT TYPE="radio" NAME="ClientASI_E24_1" VALUE=1 <<ClientASI_E24_1=1>> > Yes
    </TD>
  </TR>
    </TABLE></TD></TR>
    <TR ><TD ><TABLE CLASS="home fullsize" >
  <TR >
    <TD CLASS="strcol" COLSPAN="2" >
      EMPLOYMENT/SUPPORT COMMENTS (Include question number with your notes)
      <TEXTAREA NAME="ClientASI_ECOM_1" COLS="90" ROWS="8" WRAP="virtual" ><<ClientASI_ECOM_1>></TEXTAREA>
    </TD>
  </TR>
    </TABLE></TD></TR>
</TABLE>
<TABLE CLASS="home fullsize" >
  <TR ><TD CLASS="port hdrtxt" >Page 5<BR>Alcohol/Drugs</TD></TR>
    <TR ><TD ><TABLE CLASS="home fullsize" >
  <TR >
    <TD CLASS="strcol" COLSPAN="4" >
      Route of Administration Types: 1. Oral 2. Nasal 3. Smoking 4. Non-IV injection 5. IV
      <BR>
      � Note the usual or most recent route. For more than one route, choose the most severe. The routes are listed from least severe to most severe.
    </TD>
  </TR>
  <TR >
    <TD CLASS="strcol" WIDTH="60%" >&nbsp;</TD>
    <TD CLASS="strcol" >
      Past 30 days
    </TD>
    <TD CLASS="strcol" >
      Lifetime (years)
    </TD>
    <TD CLASS="strcol" >
      Route of Admin
    </TD>
  </TR>
  <TR >
    <TD CLASS="strcol" WIDTH="60%" >
      D1. Alcohol (any use at all, 30 days )
    </TD>
    <TD CLASS="strcol" >
      <INPUT TYPE=text NAME="ClientASI_D1D_1" VALUE="<<ClientASI_D1D_1>>" ONFOCUS="select()" ONCHANGE="return vNum(this,0,30);" SIZE="2" >
    </TD>
    <TD CLASS="strcol" >
      <INPUT TYPE=text NAME="ClientASI_D1Y_1" VALUE="<<ClientASI_D1Y_1>>" ONFOCUS="select()" ONCHANGE="return vNum(this,0,30);" SIZE="2" >
    </TD>
    <TD CLASS="strcol" >
      <SELECT NAME="ClientASI_D1R_1">[[DBA->selxTable(%form+xDrugRoutes+<<ClientASI_D1R_1>>+ID Descr)]]</SELECT> 
    </TD>
  </TR>
  <TR >
    <TD CLASS="strcol" WIDTH="60%" >
      D2. Alcohol - to intoxication
    </TD>
    <TD CLASS="strcol" >
      <INPUT TYPE=text NAME="ClientASI_D2D_1" VALUE="<<ClientASI_D2D_1>>" ONFOCUS="select()" ONCHANGE="return vNum(this,0,30);" SIZE="2" >
    </TD>
    <TD CLASS="strcol" >
      <INPUT TYPE=text NAME="ClientASI_D2Y_1" VALUE="<<ClientASI_D2Y_1>>" ONFOCUS="select()" ONCHANGE="return vNum(this,0,30);" SIZE="2" >
    </TD>
    <TD CLASS="strcol" >
      <SELECT NAME="ClientASI_D2R_1">[[DBA->selxTable(%form+xDrugRoutes+<<ClientASI_D2R_1>>+ID Descr)]]</SELECT> 
    </TD>
  </TR>
  <TR >
    <TD CLASS="strcol" WIDTH="60%" >
      D3. Heroin
    </TD>
    <TD CLASS="strcol" >
      <INPUT TYPE=text NAME="ClientASI_D3D_1" VALUE="<<ClientASI_D3D_1>>" ONFOCUS="select()" ONCHANGE="return vNum(this,0,30);" SIZE="2" >
    </TD>
    <TD CLASS="strcol" >
      <INPUT TYPE=text NAME="ClientASI_D3Y_1" VALUE="<<ClientASI_D3Y_1>>" ONFOCUS="select()" ONCHANGE="return vNum(this,0,30);" SIZE="2" >
    </TD>
    <TD CLASS="strcol" >
      <SELECT NAME="ClientASI_D3R_1">[[DBA->selxTable(%form+xDrugRoutes+<<ClientASI_D3R_1>>+ID Descr)]]</SELECT> 
    </TD>
  </TR>
  <TR >
    <TD CLASS="strcol" WIDTH="60%" >
      D4. Methadone
    </TD>
    <TD CLASS="strcol" >
      <INPUT TYPE=text NAME="ClientASI_D4D_1" VALUE="<<ClientASI_D4D_1>>" ONFOCUS="select()" ONCHANGE="return vNum(this,0,30);" SIZE="2" >
    </TD>
    <TD CLASS="strcol" >
      <INPUT TYPE=text NAME="ClientASI_D4Y_1" VALUE="<<ClientASI_D4Y_1>>" ONFOCUS="select()" ONCHANGE="return vNum(this,0,30);" SIZE="2" >
    </TD>
    <TD CLASS="strcol" >
      <SELECT NAME="ClientASI_D4R_1">[[DBA->selxTable(%form+xDrugRoutes+<<ClientASI_D4R_1>>+ID Descr)]]</SELECT> 
    </TD>
  </TR>
  <TR >
    <TD CLASS="strcol" WIDTH="60%" >
      D5. Other Opiates/Analgesics
    </TD>
    <TD CLASS="strcol" >
      <INPUT TYPE=text NAME="ClientASI_D5D_1" VALUE="<<ClientASI_D5D_1>>" ONFOCUS="select()" ONCHANGE="return vNum(this,0,30);" SIZE="2" >
    </TD>
    <TD CLASS="strcol" >
      <INPUT TYPE=text NAME="ClientASI_D5Y_1" VALUE="<<ClientASI_D5Y_1>>" ONFOCUS="select()" ONCHANGE="return vNum(this,0,30);" SIZE="2" >
    </TD>
    <TD CLASS="strcol" >
      <SELECT NAME="ClientASI_D5R_1">[[DBA->selxTable(%form+xDrugRoutes+<<ClientASI_D5R_1>>+ID Descr)]]</SELECT> 
    </TD>
  </TR>
  <TR >
    <TD CLASS="strcol" WIDTH="60%" >
      D6. Barbiturates
    </TD>
    <TD CLASS="strcol" >
      <INPUT TYPE=text NAME="ClientASI_D6D_1" VALUE="<<ClientASI_D6D_1>>" ONFOCUS="select()" ONCHANGE="return vNum(this,0,30);" SIZE="2" >
    </TD>
    <TD CLASS="strcol" >
      <INPUT TYPE=text NAME="ClientASI_D6Y_1" VALUE="<<ClientASI_D6Y_1>>" ONFOCUS="select()" ONCHANGE="return vNum(this,0,30);" SIZE="2" >
    </TD>
    <TD CLASS="strcol" >
      <SELECT NAME="ClientASI_D6R_1">[[DBA->selxTable(%form+xDrugRoutes+<<ClientASI_D6R_1>>+ID Descr)]]</SELECT> 
    </TD>
  </TR>
  <TR >
    <TD CLASS="strcol" WIDTH="60%" >
      D7. Sedatives/Hypnotics/Tranquilizers
    </TD>
    <TD CLASS="strcol" >
      <INPUT TYPE=text NAME="ClientASI_D7D_1" VALUE="<<ClientASI_D7D_1>>" ONFOCUS="select()" ONCHANGE="return vNum(this,0,30);" SIZE="2" >
    </TD>
    <TD CLASS="strcol" >
      <INPUT TYPE=text NAME="ClientASI_D7Y_1" VALUE="<<ClientASI_D7Y_1>>" ONFOCUS="select()" ONCHANGE="return vNum(this,0,30);" SIZE="2" >
    </TD>
    <TD CLASS="strcol" >
      <SELECT NAME="ClientASI_D7R_1">[[DBA->selxTable(%form+xDrugRoutes+<<ClientASI_D7R_1>>+ID Descr)]]</SELECT> 
    </TD>
  </TR>
  <TR >
    <TD CLASS="strcol" WIDTH="60%" >
      D8. Cocaine
    </TD>
    <TD CLASS="strcol" >
      <INPUT TYPE=text NAME="ClientASI_D8D_1" VALUE="<<ClientASI_D8D_1>>" ONFOCUS="select()" ONCHANGE="return vNum(this,0,30);" SIZE="2" >
    </TD>
    <TD CLASS="strcol" >
      <INPUT TYPE=text NAME="ClientASI_D8Y_1" VALUE="<<ClientASI_D8Y_1>>" ONFOCUS="select()" ONCHANGE="return vNum(this,0,30);" SIZE="2" >
    </TD>
    <TD CLASS="strcol" >
      <SELECT NAME="ClientASI_D8R_1">[[DBA->selxTable(%form+xDrugRoutes+<<ClientASI_D8R_1>>+ID Descr)]]</SELECT> 
    </TD>
  </TR>
  <TR >
    <TD CLASS="strcol" WIDTH="60%" >
      D9. Amphetamines
    </TD>
    <TD CLASS="strcol" >
      <INPUT TYPE=text NAME="ClientASI_D9D_1" VALUE="<<ClientASI_D9D_1>>" ONFOCUS="select()" ONCHANGE="return vNum(this,0,30);" SIZE="2" >
    </TD>
    <TD CLASS="strcol" >
      <INPUT TYPE=text NAME="ClientASI_D9Y_1" VALUE="<<ClientASI_D9Y_1>>" ONFOCUS="select()" ONCHANGE="return vNum(this,0,30);" SIZE="2" >
    </TD>
    <TD CLASS="strcol" >
      <SELECT NAME="ClientASI_D9R_1">[[DBA->selxTable(%form+xDrugRoutes+<<ClientASI_D9R_1>>+ID Descr)]]</SELECT> 
    </TD>
  </TR>
  <TR >
    <TD CLASS="strcol" WIDTH="60%" >
      D10. Cannabis
    </TD>
    <TD CLASS="strcol" >
      <INPUT TYPE=text NAME="ClientASI_D10D_1" VALUE="<<ClientASI_D10D_1>>" ONFOCUS="select()" ONCHANGE="return vNum(this,0,30);" SIZE="2" >
    </TD>
    <TD CLASS="strcol" >
      <INPUT TYPE=text NAME="ClientASI_D10Y_1" VALUE="<<ClientASI_D10Y_1>>" ONFOCUS="select()" ONCHANGE="return vNum(this,0,30);" SIZE="2" >
    </TD>
    <TD CLASS="strcol" >
      <SELECT NAME="ClientASI_D10R_1">[[DBA->selxTable(%form+xDrugRoutes+<<ClientASI_D10R_1>>+ID Descr)]]</SELECT> 
    </TD>
  </TR>
  <TR >
    <TD CLASS="strcol" WIDTH="60%" >
      D11. Hallucinogens
    </TD>
    <TD CLASS="strcol" >
      <INPUT TYPE=text NAME="ClientASI_D11D_1" VALUE="<<ClientASI_D11D_1>>" ONFOCUS="select()" ONCHANGE="return vNum(this,0,30);" SIZE="2" >
    </TD>
    <TD CLASS="strcol" >
      <INPUT TYPE=text NAME="ClientASI_D11Y_1" VALUE="<<ClientASI_D11Y_1>>" ONFOCUS="select()" ONCHANGE="return vNum(this,0,30);" SIZE="2" >
    </TD>
    <TD CLASS="strcol" >
      <SELECT NAME="ClientASI_D11R_1">[[DBA->selxTable(%form+xDrugRoutes+<<ClientASI_D11R_1>>+ID Descr)]]</SELECT> 
    </TD>
  </TR>
  <TR >
    <TD CLASS="strcol" WIDTH="60%" >
      D12. Inhalants
    </TD>
    <TD CLASS="strcol" >
      <INPUT TYPE=text NAME="ClientASI_D12D_1" VALUE="<<ClientASI_D12D_1>>" ONFOCUS="select()" ONCHANGE="return vNum(this,0,30);" SIZE="2" >
    </TD>
    <TD CLASS="strcol" >
      <INPUT TYPE=text NAME="ClientASI_D12Y_1" VALUE="<<ClientASI_D12Y_1>>" ONFOCUS="select()" ONCHANGE="return vNum(this,0,30);" SIZE="2" >
    </TD>
    <TD CLASS="strcol" >
      <SELECT NAME="ClientASI_D12R_1">[[DBA->selxTable(%form+xDrugRoutes+<<ClientASI_D12R_1>>+ID Descr)]]</SELECT> 
    </TD>
  </TR>
  <TR >
    <TD CLASS="strcol" WIDTH="60%" >
      D13. More than 1 substance per day (including alcohol)
    </TD>
    <TD CLASS="strcol" >
      <INPUT TYPE=text NAME="ClientASI_D13D_1" VALUE="<<ClientASI_D13D_1>>" ONFOCUS="select()" ONCHANGE="return vNum(this,0,30);" SIZE="2" >
    </TD>
    <TD CLASS="strcol" >
      <INPUT TYPE=text NAME="ClientASI_D13Y_1" VALUE="<<ClientASI_D13Y_1>>" ONFOCUS="select()" ONCHANGE="return vNum(this,0,30);" SIZE="2" >
    </TD>
    <TD CLASS="strcol" >
      <SELECT NAME="ClientASI_D13R_1">[[DBA->selxTable(%form+xDrugRoutes+<<ClientASI_D13R_1>>+ID Descr)]]</SELECT> 
    </TD>
  </TR>
  </TABLE></TD></TR>
  <TR ><TD ><TABLE CLASS="home fullsize" >
  <TR >
    <TD CLASS="strcol" WIDTH="60%" >
      D14. According to the interviewer, which substance(s) is/are the major problem?
      <BR>� Interviewer should determine the major drug or drugs of abuse. Code the number next to the drug in questions 01-12, or "00" = no problem, "15" = alcohol & one or more drugs, "16" = more than one drug but no alcohol. Ask patient when not clear.
    </TD>
    <TD CLASS="strcol" COLSPAN="3" >
      <INPUT TYPE=text NAME="ClientASI_D14_1" VALUE="<<ClientASI_D14_1>>" ONFOCUS="select()" ONCHANGE="return vNum(this,0,16);" SIZE="2" >
    </TD>
  </TR>
  <TR >
    <TD CLASS="strcol" WIDTH="60%" >
      D15. How long was your last period of voluntary abstinence from this major substance?
      <BR>� Last attempt of at least one month, not necessarily Mos.  the longest. Periods of hospitalization/incarceration do not count.  Periods of antabuse, methadone, or naltrexone use during abstinence do count.  �"00" = never abstinent
    </TD>
    <TD CLASS="strcol" COLSPAN="3" >
      <INPUT TYPE=text NAME="ClientASI_D15_1" VALUE="<<ClientASI_D15_1>>" ONFOCUS="select()" ONCHANGE="return vNum(this,0,99);" SIZE="2" > Months
    </TD>
  </TR>
  <TR >
    <TD CLASS="strcol" WIDTH="60%" >
      D16. How many months ago did this abstinence end?
    </TD>
    <TD CLASS="strcol" COLSPAN="3" >
      <INPUT TYPE=text NAME="ClientASI_D16_1" VALUE="<<ClientASI_D16_1>>" ONFOCUS="select()" ONCHANGE="return vNum(this,0,99,'NN');" SIZE="2" > Months
      <BR>� If D15 = "00" then D16 = "NN" Months.
      <BR>� "00" = still abstinent.
    </TD>
  </TR>
  </TABLE></TD></TR>
  <TR ><TD ><TABLE CLASS="home fullsize" >
  <TR >
    <TD CLASS="strcol" COLSPAN="4" >
      How many times have you had:
    </TD>
  </TR>
  <TR >
    <TD CLASS="strcol" WIDTH="60%" >
      D17. Alcohol DT's?
      <BR>� Delirium Tremens (DT's): Occur 24-48 hours after last drink, or significant decrease in alcohol intake, shaking, severe disorientation, fever, hallucinations, they usually require medical attention.
    </TD>
    <TD CLASS="strcol" COLSPAN="3" >
      <INPUT TYPE=text NAME="ClientASI_D17_1" VALUE="<<ClientASI_D17_1>>" ONFOCUS="select()" ONCHANGE="return vNum(this,0,99);" SIZE="2" >
    </TD>
  </TR>
  <TR >
    <TD CLASS="strcol" WIDTH="60%" >
      D18 Overdosed on Drugs?
      <BR>� Overdoses (OD): Requires intervention by someone to recover, not simply sleeping it off, include suicide attempts by OD.
    </TD>
    <TD CLASS="strcol" COLSPAN="3" >
      <INPUT TYPE=text NAME="ClientASI_D18_1" VALUE="<<ClientASI_D18_1>>" ONFOCUS="select()" ONCHANGE="return vNum(this,0,99);" SIZE="2" >
    </TD>
  </TR>
    </TABLE></TD></TR>
</TABLE>
<TABLE CLASS="home fullsize" >
  <TR ><TD CLASS="port hdrtxt" >Page 6<BR>Alcohol/Drugs (cont.)</TD></TR>
    <TR ><TD ><TABLE CLASS="home fullsize" >
  <TR >
    <TD CLASS="strcol" COLSPAN="2" >
      How many times in your life have you been treated for:
    </TD>
  </TR>
  <TR >
    <TD CLASS="strcol" WIDTH="60%" >
      D19. Alcohol abuse?
      <BR>�Include detoxification, halfway houses, in/outpatient counseling, and AA (if 3+ meetings within one month period).
    </TD>
    <TD CLASS="strcol" >
      <INPUT TYPE=text NAME="ClientASI_D19_1" VALUE="<<ClientASI_D19_1>>" ONFOCUS="select()" ONCHANGE="return vNum(this,0,99);" SIZE="2" >
    </TD>
  </TR>
  <TR >
    <TD CLASS="strcol" COLSPAN="2" >
      How many of these were detox only:
    </TD>
  </TR>
  <TR >
    <TD CLASS="strcol" WIDTH="60%" >
      D21. Alcohol?
    </TD>
    <TD CLASS="strcol" >
      <INPUT TYPE=text NAME="ClientASI_D21_1" VALUE="<<ClientASI_D21_1>>" ONFOCUS="select()" ONCHANGE="return vNum(this,0,99,'NN');" SIZE="2" >
    </TD>
  </TR>
  <TR >
    <TD CLASS="strcol" COLSPAN="2" >
      How much would you say you spent during the past 30 days on:
    </TD>
  </TR>
  <TR >
    <TD CLASS="strcol" WIDTH="60%" >
      D23. Alcohol?
    </TD>
    <TD CLASS="strcol" >
      $<INPUT TYPE=text NAME="ClientASI_D23_1" VALUE="<<ClientASI_D23_1>>" ONFOCUS="select()" ONCHANGE="return vNum(this,0,99999);" SIZE="2" >
    </TD>
  </TR>
  </TABLE></TD></TR>
  <TR ><TD ><TABLE CLASS="home fullsize" >
  <TR >
    <TD CLASS="strcol" WIDTH="60%" >&nbsp;</TD>
    <TD CLASS="strcol" >
      How many times in your life have you been treated for :
    </TD>
  </TR>
  <TR >
    <TD CLASS="strcol" WIDTH="60%" >
      D20. Drug abuse?
      <BR>� Include detoxification, halfway houses, in/outpatient counseling, and NA (if 3+ meetings within one month period).
    </TD>
    <TD CLASS="strcol" >
      <INPUT TYPE=text NAME="ClientASI_D20_1" VALUE="<<ClientASI_D20_1>>" ONFOCUS="select()" ONCHANGE="return vNum(this,0,99);" SIZE="2" >
    </TD>
  </TR>
  <TR >
    <TD CLASS="strcol" COLSPAN="2" >
      How many of these were detox only:
    </TD>
  </TR>
  <TR >
    <TD CLASS="strcol" WIDTH="60%" >
      D22. Drugs?
      <BR>� If D19 = "00", then question D21 is "NN" If D20 = "00", then question D22 is "NN"
    </TD>
    <TD CLASS="strcol" >
      <INPUT TYPE=text NAME="ClientASI_D22_1" VALUE="<<ClientASI_D22_1>>" ONFOCUS="select()" ONCHANGE="return vNum(this,0,99,'NN');" SIZE="2" >
    </TD>
  </TR>
  <TR >
    <TD CLASS="strcol" COLSPAN="2" >
      How much would you say you spent during the past 30 days on:
    </TD>
  </TR>
  <TR >
    <TD CLASS="strcol" WIDTH="60%" >
      D24. Drugs?
      <BR>� Only count actual money spent. What is the financial burden caused by drugs/alcohol?
    </TD>
    <TD CLASS="strcol" >
      $<INPUT TYPE=text NAME="ClientASI_D24_1" VALUE="<<ClientASI_D24_1>>" ONFOCUS="select()" ONCHANGE="return vNum(this,0,99999);" SIZE="12" >
    </TD>
  </TR>
  </TABLE></TD></TR>
  <TR ><TD ><TABLE CLASS="home fullsize" >
  <TR >
    <TD CLASS="strcol" WIDTH="60%" >
      D25. How many days have you been treated in an outpatient setting for alcohol or drugs in the past 30 days?
    </TD>
    <TD CLASS="strcol" >
      <INPUT TYPE=text NAME="ClientASI_D25_1" VALUE="<<ClientASI_D25_1>>" ONFOCUS="select()" ONCHANGE="return vNum(this,0,30);" SIZE="2" >
      <BR>� Include AA/NA
    </TD>
  </TR>
  </TABLE></TD></TR>
  <TR ><TD ><TABLE CLASS="home fullsize" >
  <TR >
    <TD CLASS="strcol" COLSPAN="2" >
      How many days in the past 30 have you experienced:
    </TD>
  </TR>
  <TR >
    <TD CLASS="strcol" WIDTH="60%" >
      D26. Alcohol problems?
      � Include: Craving, withdrawal symptoms, disturbing effects of use, or wanting to stop and being unable to.
    </TD>
    <TD CLASS="strcol" >
      <INPUT TYPE=text NAME="ClientASI_D26_1" VALUE="<<ClientASI_D26_1>>" ONFOCUS="select()" ONCHANGE="return vNum(this,0,30);" SIZE="2" >
    </TD>
  </TR>
  <TR >
    <TD CLASS="strcol" COLSPAN="2" >
      For Questions D28+D30, ask the patient to use the Patient Rating scale.
      <BR>The patient is rating the need for additional substance abuse treatment.
    </TD>
  </TR>
  <TR >
    <TD CLASS="strcol" COLSPAN="2" >
      How troubled or bothered have you been in the past 30 days by these:
    </TD>
  </TR>
  <TR >
    <TD CLASS="strcol" WIDTH="60%" >
      D28. Alcohol problems?</TD>
      <BR>� Include: Craving, withdrawal symptoms, disturbing effects of use, or wanting to stop and being unable to.
    <TD CLASS="strcol" >
      <SELECT NAME="ClientASI_D28_1">[[DBA->selxTable(%form+xRateScale+<<ClientASI_D28_1>>+ID Descr)]]</SELECT> 
    </TD>
  </TR>
  <TR >
    <TD CLASS="strcol" COLSPAN="2" >
      How important to you now is treatment for these:
    </TD>
  </TR>
  </TABLE></TD></TR>
  <TR ><TD ><TABLE CLASS="home fullsize" >
  <TR >
    <TD CLASS="strcol" WIDTH="60%" >
      D30. Alcohol problems?
    </TD>
    <TD CLASS="strcol" >
      <SELECT NAME="ClientASI_D30_1">[[DBA->selxTable(%form+xRateScale+<<ClientASI_D30_1>>+ID Descr)]]</SELECT> 
    </TD>
  </TR>
  </TABLE></TD></TR>
  <TR ><TD ><TABLE CLASS="home fullsize" >
  <TR >
    <TD CLASS="strcol" COLSPAN="2" >
      How many days in the past 30 have you experienced:
    </TD>
  </TR>
  <TR >
    <TD CLASS="strcol" WIDTH="60%" >
      D27. Drug problems?
      <BR>� Include: Craving, withdrawal symptoms, disturbing effects of use, or wanting to stop and being unable to.
    </TD>
    <TD CLASS="strcol" >
      <INPUT TYPE=text NAME="ClientASI_D27_1" VALUE="<<ClientASI_D27_1>>" ONFOCUS="select()" ONCHANGE="return vNum(this,0,30);" SIZE="2" >
    </TD>
  </TR>
  <TR >
    <TD CLASS="strcol" COLSPAN="2" >
      For Questions D29+D31, ask the patient to use the Patient Rating scale.  The patient is rating the need for additional substance abuse treatment.
    </TD>
  </TR>
  <TR >
    <TD CLASS="strcol" COLSPAN="2" >
      How troubled or bothered have you been in the past 30 days by these:
    </TD>
  </TR>
  <TR >
    <TD CLASS="strcol" WIDTH="60%" >
      D29. Drug problems?
    </TD>
    <TD CLASS="strcol" >
      <SELECT NAME="ClientASI_D29_1">[[DBA->selxTable(%form+xRateScale+<<ClientASI_D29_1>>+ID Descr)]]</SELECT> 
    </TD>
  </TR>
  <TR >
    <TD CLASS="strcol" COLSPAN="2" >
      How important to you now is treatment for these:
    </TD>
  </TR>
  <TR >
    <TD CLASS="strcol" WIDTH="60%" >
      D31. Drug problems?
    </TD>
    <TD CLASS="strcol" >
      <SELECT NAME="ClientASI_D31_1">[[DBA->selxTable(%form+xRateScale+<<ClientASI_D31_1>>+ID Descr)]]</SELECT> 
    </TD>
  </TR>
  </TABLE></TD></TR>
  <TR ><TD ><TABLE CLASS="home fullsize" >
  <TR >
    <TD CLASS="strcol" COLSPAN="2" >
      INTERVIEWER RATING
    </TD>
  </TR>
  <TR >
    <TD CLASS="strcol" COLSPAN="2" >
      How would you rate the patient's need for treatment for:
    </TD>
  </TR>
  <TR >
    <TD CLASS="strcol" WIDTH="60%" >
      D32. Alcohol problems?
    </TD>
    <TD CLASS="strcol" >
      <SELECT NAME="ClientASI_D32_1" ONCHANGE="return setSP(this.form,'D32',this);" >[[DBA->selxTable(%form+xSeverityRatings+<<ClientASI_D32_1>>+ID Descr)]]</SELECT> 
    </TD>
  </TR>
  <TR >
    <TD CLASS="strcol" WIDTH="60%" >
      D33. Drug problems?
    </TD>
    <TD CLASS="strcol" >
      <SELECT NAME="ClientASI_D33_1" ONCHANGE="return setSP(this.form,'D33',this);" >[[DBA->selxTable(%form+xSeverityRatings+<<ClientASI_D33_1>>+ID Descr)]]</SELECT> 
    </TD>
  </TR>
  </TABLE></TD></TR>
  <TR ><TD ><TABLE CLASS="home fullsize" >
  <TR >
    <TD CLASS="strcol" COLSPAN="2" >
      CONFIDENCE RATINGS
    </TD>
  </TR>
  <TR >
    <TD CLASS="strcol" COLSPAN="2" >
      Is the above information significantly distorted by:
    </TD>
  </TR>
  <TR >
    <TD CLASS="strcol" WIDTH="60%" >
      D34. Patient's misrepresentation?
    </TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="radio" NAME="ClientASI_D34_1" VALUE=0 <<ClientASI_D34_1=0>> > No
      <INPUT TYPE="radio" NAME="ClientASI_D34_1" VALUE=1 <<ClientASI_D34_1=1>> > Yes
    </TD>
  </TR>
  <TR >
    <TD CLASS="strcol" WIDTH="60%" >
      D35. Patient's inability to understand?
    </TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="radio" NAME="ClientASI_D35_1" VALUE=0 <<ClientASI_D35_1=0>> > No
      <INPUT TYPE="radio" NAME="ClientASI_D35_1" VALUE=1 <<ClientASI_D35_1=1>> > Yes
    </TD>
  </TR>
  </TABLE></TD></TR>
  <TR ><TD ><TABLE CLASS="home fullsize" >
  <TR >
    <TD CLASS="strcol" COLSPAN="2" >
      ALCOHOL/DRUGS COMMENTS (Include question number with your notes)
      <TEXTAREA NAME="ClientASI_DCOM_1" COLS="90" ROWS="8" WRAP="virtual" ><<ClientASI_DCOM_1>></TEXTAREA>
    </TD>
  </TR>
    </TABLE></TD></TR>
</TABLE>
<TABLE CLASS="home fullsize" >
  <TR ><TD CLASS="port hdrtxt" >Page 7<BR>Legal Status</TD></TR>
    <TR ><TD ><TABLE CLASS="home fullsize" >
  <TR >
    <TD CLASS="strcol" WIDTH="60%" >
      L1. Was this admission prompted or suggested by the criminal justice system?
    </TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="radio" NAME="ClientASI_L1_1" VALUE=0 <<ClientASI_L1_1=0>> > No
      <INPUT TYPE="radio" NAME="ClientASI_L1_1" VALUE=1 <<ClientASI_L1_1=1>> > Yes � Judge, probation/parole officer, etc.
    </TD>
  </TR>
  <TR >
    <TD CLASS="strcol" WIDTH="60%" >
      L2. Are you on parole or probation?
    </TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="radio" NAME="ClientASI_L2_1" VALUE=0 <<ClientASI_L2_1=0>> > No
      <INPUT TYPE="radio" NAME="ClientASI_L2_1" VALUE=1 <<ClientASI_L2_1=1>> > Yes � Note duration and level in comments. 
    </TD>
  </TR>
  </TABLE></TD></TR>
  <TR ><TD ><TABLE CLASS="home fullsize" >
  <TR >
    <TD CLASS="strcol" COLSPAN="2" >
      How many times in your life have you been arrested and charged with the following:
    </TD>
  </TR>
  <TR >
    <TD CLASS="strcol" WIDTH="60%" >
      L3. Shoplift/Vandal
      <INPUT TYPE=text NAME="ClientASI_L3_1" VALUE="<<ClientASI_L3_1>>" ONFOCUS="select()" ONCHANGE="return vNum(this,0,99);" SIZE="2" >
    </TD>
    <TD CLASS="strcol" >
      L10. Assault
      <INPUT TYPE=text NAME="ClientASI_L10_1" VALUE="<<ClientASI_L10_1>>" ONFOCUS="select()" ONCHANGE="return vNum(this,0,99);" SIZE="2" >
    </TD>
  </TR>
  <TR >
    <TD CLASS="strcol" WIDTH="60%" >
      L4. Parole/Probation Violations
      <INPUT TYPE=text NAME="ClientASI_L4_1" VALUE="<<ClientASI_L4_1>>" ONFOCUS="select()" ONCHANGE="return vNum(this,0,99);" SIZE="2" >
    </TD>
    <TD CLASS="strcol" >
      L11. Arson
      <INPUT TYPE=text NAME="ClientASI_L11_1" VALUE="<<ClientASI_L11_1>>" ONFOCUS="select()" ONCHANGE="return vNum(this,0,99);" SIZE="2" >
    </TD>
  </TR>
  <TR >
    <TD CLASS="strcol" WIDTH="60%" >
      L5. Drug Charges
      <INPUT TYPE=text NAME="ClientASI_L5_1" VALUE="<<ClientASI_L5_1>>" ONFOCUS="select()" ONCHANGE="return vNum(this,0,99);" SIZE="2" >
    </TD>
    <TD CLASS="strcol" >
      L12. Rape
      <INPUT TYPE=text NAME="ClientASI_L12_1" VALUE="<<ClientASI_L12_1>>" ONFOCUS="select()" ONCHANGE="return vNum(this,0,99);" SIZE="2" >
    </TD>
  </TR>
  <TR >
    <TD CLASS="strcol" WIDTH="60%" >
      L6. Forgery
      <INPUT TYPE=text NAME="ClientASI_L6_1" VALUE="<<ClientASI_L6_1>>" ONFOCUS="select()" ONCHANGE="return vNum(this,0,99);" SIZE="2" >
    </TD>
    <TD CLASS="strcol" >
      L13. Homicide/Mansl.
      <INPUT TYPE=text NAME="ClientASI_L13_1" VALUE="<<ClientASI_L13_1>>" ONFOCUS="select()" ONCHANGE="return vNum(this,0,99);" SIZE="2" >
    </TD>
  </TR>
  <TR >
    <TD CLASS="strcol" WIDTH="60%" >
      L7. Weapons Offense
      <INPUT TYPE=text NAME="ClientASI_L7_1" VALUE="<<ClientASI_L7_1>>" ONFOCUS="select()" ONCHANGE="return vNum(this,0,99);" SIZE="2" >
    </TD>
    <TD CLASS="strcol" >
      L14. Prostitution
      <INPUT TYPE=text NAME="ClientASI_L14_1" VALUE="<<ClientASI_L14_1>>" ONFOCUS="select()" ONCHANGE="return vNum(this,0,99);" SIZE="2" >
    </TD>
  </TR>
  <TR >
    <TD CLASS="strcol" WIDTH="60%" >
      L8. Burglary/Larceny/B&E
      <INPUT TYPE=text NAME="ClientASI_L8_1" VALUE="<<ClientASI_L8_1>>" ONFOCUS="select()" ONCHANGE="return vNum(this,0,99);" SIZE="2" >
    </TD>
    <TD CLASS="strcol" >
      L15. Contempt of Court
      <INPUT TYPE=text NAME="ClientASI_L15_1" VALUE="<<ClientASI_L15_1>>" ONFOCUS="select()" ONCHANGE="return vNum(this,0,99);" SIZE="2" >
    </TD>
  </TR>
  <TR >
    <TD CLASS="strcol" WIDTH="60%" >
      L9. Robbery
      <INPUT TYPE=text NAME="ClientASI_L9_1" VALUE="<<ClientASI_L9_1>>" ONFOCUS="select()" ONCHANGE="return vNum(this,0,99);" SIZE="2" >
    </TD>
    <TD CLASS="strcol" >
      L16. Other:
      <INPUT TYPE="TEXT" NAME="ClientASI_L16T_1" VALUE="<<ClientASI_L16T_1>>" ONFOCUS="select()" SIZE=30>
      <INPUT TYPE=text NAME="ClientASI_L16_1" VALUE="<<ClientASI_L16_1>>" ONFOCUS="select()" ONCHANGE="return vNum(this,0,99);" SIZE="2" >
    </TD>
  </TR>
  <TR >
    <TD CLASS="strcol" COLSPAN="2" >
� Include total number of counts, not just convictions. Do not include juvenile (pre-age 18) crimes, unless they were charged as an adult.
� Include formal charges only.
    </TD>
  </TR>
  </TABLE></TD></TR>
  <TR ><TD ><TABLE CLASS="home fullsize" >
  <TR >
    <TD CLASS="strcol" WIDTH="60%" >
      L17. How many of these charges resulted in convictions?
      <BR>� If L3-16 = 00, then question L17 = "NN".
      <BR>� Do not include misdemeanor offenses from questions L18-20 below.
      <BR>� Convictions include fines, probation, incarcerations, suspended sentences, guilty pleas, and plea bargaining.
    </TD>
    <TD CLASS="strcol" >
      <INPUT TYPE=text NAME="ClientASI_L17_1" VALUE="<<ClientASI_L17_1>>" ONFOCUS="select()" ONCHANGE="return vNum(this,0,99,'NN');" SIZE="2" >
    </TD>
  </TR>
  </TABLE></TD></TR>
  <TR ><TD ><TABLE CLASS="home fullsize" >
  <TR >
    <TD CLASS="strcol" COLSPAN="2" >
      How many times in your life have you been charged with the following:
    </TD>
  </TR>
  <TR >
    <TD CLASS="strcol" WIDTH="60%" >
      L18. Disorderly conduct, vagrancy, public intoxication?
    </TD>
    <TD CLASS="strcol" >
      <INPUT TYPE=text NAME="ClientASI_L18_1" VALUE="<<ClientASI_L18_1>>" ONFOCUS="select()" ONCHANGE="return vNum(this,0,99);" SIZE="2" >
    </TD>
  </TR>
  <TR >
    <TD CLASS="strcol" WIDTH="60%" >
      L19. Driving while intoxicated?
    </TD>
    <TD CLASS="strcol" >
      <INPUT TYPE=text NAME="ClientASI_L19_1" VALUE="<<ClientASI_L19_1>>" ONFOCUS="select()" ONCHANGE="return vNum(this,0,99);" SIZE="2" >
    </TD>
  </TR>
  <TR >
    <TD CLASS="strcol" WIDTH="60%" >
      L20. Major driving violations?
      <BR>� Moving violations: speeding, reckless driving, no license, etc.
    </TD>
    <TD CLASS="strcol" >
      <INPUT TYPE=text NAME="ClientASI_L20_1" VALUE="<<ClientASI_L20_1>>" ONFOCUS="select()" ONCHANGE="return vNum(this,0,99);" SIZE="2" >
    </TD>
  </TR>
  </TABLE></TD></TR>
  <TR ><TD ><TABLE CLASS="home fullsize" >
  <TR >
    <TD CLASS="strcol" WIDTH="60%" >
      L21 How many months were you incarcerated in your life?
      <BR>� If incarcerated 2 weeks or more, round this up to 1 month. List total number of months incarcerated.
    </TD>
    <TD CLASS="strcol" >
      <INPUT TYPE=text NAME="ClientASI_L21_1" VALUE="<<ClientASI_L21_1>>" ONFOCUS="select()" ONCHANGE="return vNum(this,0,9999);" SIZE="2" >
    </TD>
  </TR>
  <TR >
    <TD CLASS="strcol" WIDTH="60%" >
      L22. How long was your last incarceration?
      <BR>� Of 2 weeks or more. Enter "NN" if never incarcerated.
    </TD>
    <TD CLASS="strcol" >
      <INPUT TYPE=text NAME="ClientASI_L22_1" VALUE="<<ClientASI_L22_1>>" ONFOCUS="select()" ONCHANGE="return vNum(this,0,999,'NN');" SIZE="2" >
    </TD>
  </TR>
  <TR >
    <TD CLASS="strcol" WIDTH="60%" >
      L23. What was it for?
      <BR>� Use code 03-16, 18-20. If multiple charges, choose most severe. Enter "NN" if never incarcerated.
    </TD>
    <TD CLASS="strcol" >
      <INPUT TYPE=text NAME="ClientASI_L23_1" VALUE="<<ClientASI_L23_1>>" ONFOCUS="select()" ONCHANGE="return vNum(this,0,999,'NN');" SIZE="2" >
    </TD>
  </TR>
  </TABLE></TD></TR>
  <TR ><TD ><TABLE CLASS="home fullsize" >
  <TR >
    <TD CLASS="strcol" WIDTH="60%" >
      L24. Are you presently awaiting charges, trial, or sentence?
    </TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="radio" NAME="ClientASI_L24_1" VALUE=0 <<ClientASI_L24_1=0>> > No
      <INPUT TYPE="radio" NAME="ClientASI_L24_1" VALUE=1 <<ClientASI_L24_1=1>> > Yes
    </TD>
  </TR>
  <TR >
    <TD CLASS="strcol" WIDTH="60%" >
      L25. What for?
      <BR>� Use the number of the type of crime committed: 03-16 and 18-20
      <BR>� Refers to Q. L24. If more than one, choose most severe.
    </TD>
    <TD CLASS="strcol" >
      <INPUT TYPE=text NAME="ClientASI_L25_1" VALUE="<<ClientASI_L25_1>>" ONFOCUS="select()" ONCHANGE="return vNum(this,0,20);" SIZE="2" >
    </TD>
  </TR>
    </TABLE></TD></TR>
</TABLE>
<TABLE CLASS="home fullsize" >
  <TR ><TD CLASS="port hdrtxt" >Page 8<BR>Legal Status (cont.)</TD></TR>
    <TR ><TD ><TABLE CLASS="home fullsize" >
  <TR >
    <TD CLASS="strcol" WIDTH="60%" >
      L26. How many days in the past 30, were you detained or incarcerated?
      <BR>� Include being arrested and released on the same day.
    </TD>
    <TD CLASS="strcol" >
      <INPUT TYPE=text NAME="ClientASI_L26_1" VALUE="<<ClientASI_L26_1>>" ONFOCUS="select()" ONCHANGE="return vNum(this,0,30);" SIZE="2" >
    </TD>
  </TR>
  <TR >
    <TD CLASS="strcol" WIDTH="60%" >
      L27. How many days in the past 30 have you engaged in illegal activities for profit?
      <BR>� Exclude simple drug possession. Include drug dealing, prostitution, selling stolen goods, etc. May be cross checked with Question E17 under Employment/Family Support Section.
    </TD>
    <TD CLASS="strcol" >
      <INPUT TYPE=text NAME="ClientASI_L27_1" VALUE="<<ClientASI_L27_1>>" ONFOCUS="select()" ONCHANGE="return vNum(this,0,30);" SIZE="2" >
    </TD>
  </TR>
  </TABLE></TD></TR>
  <TR ><TD ><TABLE CLASS="home fullsize" >
  <TR >
    <TD CLASS="strcol" COLSPAN="2" >
      For Questions L28-29, ask the patient to use the Patient Rating scale.
    </TD>
  </TR>
  <TR >
    <TD CLASS="strcol" WIDTH="60%" >
      L28. How serious do you feel your present legal problems are?
      <BR>� Exclude civil problems
    </TD>
    <TD CLASS="strcol" >
      <SELECT NAME="ClientASI_L28_1">[[DBA->selxTable(%form+xRateScale+<<ClientASI_L28_1>>+ID Descr)]]</SELECT> 
    </TD>
  </TR>
  <TR >
    <TD CLASS="strcol" WIDTH="60%" >
      L29. How important to you now is counseling or referral for these legal problems?
      <BR>� Patient is rating a need for referral to legal counsel for defense against criminal charges.
    </TD>
    <TD CLASS="strcol" >
      <SELECT NAME="ClientASI_L29_1">[[DBA->selxTable(%form+xRateScale+<<ClientASI_L29_1>>+ID Descr)]]</SELECT> 
    </TD>
  </TR>
  </TABLE></TD></TR>
  <TR ><TD ><TABLE CLASS="home fullsize" >
  <TR >
    <TD CLASS="strcol" COLSPAN="2" >
      INTERVIEWER SEVERITY RATING
    </TD>
  </TR>
  <TR >
    <TD CLASS="strcol" WIDTH="60%" >
      L30. How would you rate the patient's need for legal services or counseling?
    </TD>
    <TD CLASS="strcol" >
      <SELECT NAME="ClientASI_L30_1" ONCHANGE="return setSP(this.form,'L30',this);" >[[DBA->selxTable(%form+xSeverityRatings+<<ClientASI_L30_1>>+ID Descr)]]</SELECT> 
    </TD>
  </TR>
  </TABLE></TD></TR>
  <TR ><TD ><TABLE CLASS="home fullsize" >
  <TR >
    <TD CLASS="strcol" COLSPAN="2" >
      CONFIDENCE RATINGS
    </TD>
  </TR>
  <TR >
    <TD CLASS="strcol" COLSPAN="2" >
      Is the above information significantly distorted by:
    </TD>
  </TR>
  <TR >
    <TD CLASS="strcol" WIDTH="60%" >
      L31. Patient's misrepresentation? 
    </TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="radio" NAME="ClientASI_L31_1" VALUE=0 <<ClientASI_L31_1=0>> > No
      <INPUT TYPE="radio" NAME="ClientASI_L31_1" VALUE=1 <<ClientASI_L31_1=1>> > Yes
    </TD>
  </TR>
  <TR >
    <TD CLASS="strcol" WIDTH="60%" >
      L32. Patient's inability to understand?
    </TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="radio" NAME="ClientASI_L32_1" VALUE=0 <<ClientASI_L32_1=0>> > No
      <INPUT TYPE="radio" NAME="ClientASI_L32_1" VALUE=1 <<ClientASI_L32_1=1>> > Yes
    </TD>
  </TR>
  </TABLE></TD></TR>
  <TR ><TD ><TABLE CLASS="home fullsize" >
  <TR >
    <TD CLASS="strcol" COLSPAN="2" >
      LEGAL COMMENTS (Include question number with your notes)
      <TEXTAREA NAME="ClientASI_LCOM_1" COLS="90" ROWS="8" WRAP="virtual" ><<ClientASI_LCOM_1>></TEXTAREA>
    </TD>
  </TR>
  </TABLE></TD></TR>
</TABLE>
<TABLE CLASS="home fullsize" >
  <TR ><TD ><TABLE CLASS="home fullsize" >
  <TR ><TD CLASS="port hdrtxt" COLSPAN="4" >Family History</TD></TR>
  <TR >
    <TD CLASS="strcol" COLSPAN="4" >
      Have any of your blood-related relatives had what you would call a significant drinking, drug use, or psychiatric problem?  Specifically, was there a problem that did or should have led to treatment?
    </TD>
  </TR>
  <TR ><TD ><TABLE CLASS="home fullsize" >
  <TR >
    <TD CLASS="strcol" WIDTH="60%" >Mother's Side</TD>
    <TD CLASS="strcol" >Alcohol</TD>
    <TD CLASS="strcol" >Drug</TD>
    <TD CLASS="strcol" >Psych.</TD>
  </TR>
  <TR >
    <TD CLASS="strcol" WIDTH="60%" >
     H1. Grandmother
    </TD>
    <TD CLASS="strcol" >
      <INPUT TYPE=text NAME="ClientASI_H1A_1" VALUE="<<ClientASI_H1A_1>>" ONFOCUS="select()" ONCHANGE="return vNum(this,0,1,X,N);" SIZE="2" >
    </TD>
    <TD CLASS="strcol" >
      <INPUT TYPE=text NAME="ClientASI_H1D_1" VALUE="<<ClientASI_H1D_1>>" ONFOCUS="select()" ONCHANGE="return vNum(this,0,1,X,N);" SIZE="2" >
    </TD>
    <TD CLASS="strcol" >
      <INPUT TYPE=text NAME="ClientASI_H1P_1" VALUE="<<ClientASI_H1P_1>>" ONFOCUS="select()" ONCHANGE="return vNum(this,0,1,X,N);" SIZE="2" >
    </TD>
  </TR>
  <TR >
    <TD CLASS="strcol" WIDTH="60%" >
     H2. Grandfather
    </TD>
    <TD CLASS="strcol" >
      <INPUT TYPE=text NAME="ClientASI_H2A_1" VALUE="<<ClientASI_H2A_1>>" ONFOCUS="select()" ONCHANGE="return vNum(this,0,1,X,N);" SIZE="2" >
    </TD>
    <TD CLASS="strcol" >
      <INPUT TYPE=text NAME="ClientASI_H2D_1" VALUE="<<ClientASI_H2D_1>>" ONFOCUS="select()" ONCHANGE="return vNum(this,0,1,X,N);" SIZE="2" >
    </TD>
    <TD CLASS="strcol" >
      <INPUT TYPE=text NAME="ClientASI_H2P_1" VALUE="<<ClientASI_H2P_1>>" ONFOCUS="select()" ONCHANGE="return vNum(this,0,1,X,N);" SIZE="2" >
    </TD>
  </TR>
  <TR >
    <TD CLASS="strcol" WIDTH="60%" >
     H3. Mother
    </TD>
    <TD CLASS="strcol" >
      <INPUT TYPE=text NAME="ClientASI_H3A_1" VALUE="<<ClientASI_H3A_1>>" ONFOCUS="select()" ONCHANGE="return vNum(this,0,1,X,N);" SIZE="2" >
    </TD>
    <TD CLASS="strcol" >
      <INPUT TYPE=text NAME="ClientASI_H3D_1" VALUE="<<ClientASI_H3D_1>>" ONFOCUS="select()" ONCHANGE="return vNum(this,0,1,X,N);" SIZE="2" >
    </TD>
    <TD CLASS="strcol" >
      <INPUT TYPE=text NAME="ClientASI_H3P_1" VALUE="<<ClientASI_H3P_1>>" ONFOCUS="select()" ONCHANGE="return vNum(this,0,1,X,N);" SIZE="2" >
    </TD>
  </TR>
  <TR >
    <TD CLASS="strcol" WIDTH="60%" >
     H4. Aunt
    </TD>
    <TD CLASS="strcol" >
      <INPUT TYPE=text NAME="ClientASI_H4A_1" VALUE="<<ClientASI_H4A_1>>" ONFOCUS="select()" ONCHANGE="return vNum(this,0,1,X,N);" SIZE="2" >
    </TD>
    <TD CLASS="strcol" >
      <INPUT TYPE=text NAME="ClientASI_H4D_1" VALUE="<<ClientASI_H4D_1>>" ONFOCUS="select()" ONCHANGE="return vNum(this,0,1,X,N);" SIZE="2" >
    </TD>
    <TD CLASS="strcol" >
      <INPUT TYPE=text NAME="ClientASI_H4P_1" VALUE="<<ClientASI_H4P_1>>" ONFOCUS="select()" ONCHANGE="return vNum(this,0,1,X,N);" SIZE="2" >
    </TD>
  </TR>
  <TR >
    <TD CLASS="strcol" WIDTH="60%" >
     H5. Uncle
    </TD>
    <TD CLASS="strcol" >
      <INPUT TYPE=text NAME="ClientASI_H5A_1" VALUE="<<ClientASI_H5A_1>>" ONFOCUS="select()" ONCHANGE="return vNum(this,0,1,X,N);" SIZE="2" >
    </TD>
    <TD CLASS="strcol" >
      <INPUT TYPE=text NAME="ClientASI_H5D_1" VALUE="<<ClientASI_H5D_1>>" ONFOCUS="select()" ONCHANGE="return vNum(this,0,1,X,N);" SIZE="2" >
    </TD>
    <TD CLASS="strcol" >
      <INPUT TYPE=text NAME="ClientASI_H5P_1" VALUE="<<ClientASI_H5P_1>>" ONFOCUS="select()" ONCHANGE="return vNum(this,0,1,X,N);" SIZE="2" >
    </TD>
  </TR>
  </TABLE></TD></TR>
  <TR ><TD ><TABLE CLASS="home fullsize" >
  <TR >
    <TD CLASS="strcol" WIDTH="60%" >Father's Side</TD>
    <TD CLASS="strcol" >Alcohol</TD>
    <TD CLASS="strcol" >Drug</TD>
    <TD CLASS="strcol" >Psych.</TD>
  </TR>
  <TR >
    <TD CLASS="strcol" WIDTH="60%" >
     H6. Grandmother
    </TD>
    <TD CLASS="strcol" >
      <INPUT TYPE=text NAME="ClientASI_H6A_1" VALUE="<<ClientASI_H6A_1>>" ONFOCUS="select()" ONCHANGE="return vNum(this,0,1,X,N);" SIZE="2" >
    </TD>
    <TD CLASS="strcol" >
      <INPUT TYPE=text NAME="ClientASI_H6D_1" VALUE="<<ClientASI_H6D_1>>" ONFOCUS="select()" ONCHANGE="return vNum(this,0,1,X,N);" SIZE="2" >
    </TD>
    <TD CLASS="strcol" >
      <INPUT TYPE=text NAME="ClientASI_H6P_1" VALUE="<<ClientASI_H6P_1>>" ONFOCUS="select()" ONCHANGE="return vNum(this,0,1,X,N);" SIZE="2" >
    </TD>
  </TR>
  <TR >
    <TD CLASS="strcol" WIDTH="60%" >
     H7. Grandfather
    </TD>
    <TD CLASS="strcol" >
      <INPUT TYPE=text NAME="ClientASI_H7A_1" VALUE="<<ClientASI_H7A_1>>" ONFOCUS="select()" ONCHANGE="return vNum(this,0,1,X,N);" SIZE="2" >
    </TD>
    <TD CLASS="strcol" >
      <INPUT TYPE=text NAME="ClientASI_H7D_1" VALUE="<<ClientASI_H7D_1>>" ONFOCUS="select()" ONCHANGE="return vNum(this,0,1,X,N);" SIZE="2" >
    </TD>
    <TD CLASS="strcol" >
      <INPUT TYPE=text NAME="ClientASI_H7P_1" VALUE="<<ClientASI_H7P_1>>" ONFOCUS="select()" ONCHANGE="return vNum(this,0,1,X,N);" SIZE="2" >
    </TD>
  </TR>
  <TR >
    <TD CLASS="strcol" WIDTH="60%" >
     H8. Father
    </TD>
    <TD CLASS="strcol" >
      <INPUT TYPE=text NAME="ClientASI_H8A_1" VALUE="<<ClientASI_H8A_1>>" ONFOCUS="select()" ONCHANGE="return vNum(this,0,1,X,N);" SIZE="2" >
    </TD>
    <TD CLASS="strcol" >
      <INPUT TYPE=text NAME="ClientASI_H8D_1" VALUE="<<ClientASI_H8D_1>>" ONFOCUS="select()" ONCHANGE="return vNum(this,0,1,X,N);" SIZE="2" >
    </TD>
    <TD CLASS="strcol" >
      <INPUT TYPE=text NAME="ClientASI_H8P_1" VALUE="<<ClientASI_H8P_1>>" ONFOCUS="select()" ONCHANGE="return vNum(this,0,1,X,N);" SIZE="2" >
    </TD>
  </TR>
  <TR >
    <TD CLASS="strcol" WIDTH="60%" >
     H9. Aunt
    </TD>
    <TD CLASS="strcol" >
      <INPUT TYPE=text NAME="ClientASI_H9A_1" VALUE="<<ClientASI_H9A_1>>" ONFOCUS="select()" ONCHANGE="return vNum(this,0,1,X,N);" SIZE="2" >
    </TD>
    <TD CLASS="strcol" >
      <INPUT TYPE=text NAME="ClientASI_H9D_1" VALUE="<<ClientASI_H9D_1>>" ONFOCUS="select()" ONCHANGE="return vNum(this,0,1,X,N);" SIZE="2" >
    </TD>
    <TD CLASS="strcol" >
      <INPUT TYPE=text NAME="ClientASI_H9P_1" VALUE="<<ClientASI_H9P_1>>" ONFOCUS="select()" ONCHANGE="return vNum(this,0,1,X,N);" SIZE="2" >
    </TD>
  </TR>
  <TR >
    <TD CLASS="strcol" WIDTH="60%" >
     H10. Uncle
    </TD>
    <TD CLASS="strcol" >
      <INPUT TYPE=text NAME="ClientASI_H10A_1" VALUE="<<ClientASI_H10A_1>>" ONFOCUS="select()" ONCHANGE="return vNum(this,0,1,X,N);" SIZE="2" >
    </TD>
    <TD CLASS="strcol" >
      <INPUT TYPE=text NAME="ClientASI_H10D_1" VALUE="<<ClientASI_H10D_1>>" ONFOCUS="select()" ONCHANGE="return vNum(this,0,1,X,N);" SIZE="2" >
    </TD>
    <TD CLASS="strcol" >
      <INPUT TYPE=text NAME="ClientASI_H10P_1" VALUE="<<ClientASI_H10P_1>>" ONFOCUS="select()" ONCHANGE="return vNum(this,0,1,X,N);" SIZE="2" >
    </TD>
  </TR>
  </TABLE></TD></TR>
  <TR ><TD ><TABLE CLASS="home fullsize" >
  <TR >
    <TD CLASS="strcol" WIDTH="60%" >Siblings</TD>
    <TD CLASS="strcol" >Alcohol</TD>
    <TD CLASS="strcol" >Drug</TD>
    <TD CLASS="strcol" >Psych.</TD>
  </TR>
  <TR >
    <TD CLASS="strcol" WIDTH="60%" >
     H11. Brother
    </TD>
    <TD CLASS="strcol" >
      <INPUT TYPE=text NAME="ClientASI_H11A_1" VALUE="<<ClientASI_H11A_1>>" ONFOCUS="select()" ONCHANGE="return vNum(this,0,1,X,N);" SIZE="2" >
    </TD>
    <TD CLASS="strcol" >
      <INPUT TYPE=text NAME="ClientASI_H11D_1" VALUE="<<ClientASI_H11D_1>>" ONFOCUS="select()" ONCHANGE="return vNum(this,0,1,X,N);" SIZE="2" >
    </TD>
    <TD CLASS="strcol" >
      <INPUT TYPE=text NAME="ClientASI_H11P_1" VALUE="<<ClientASI_H11P_1>>" ONFOCUS="select()" ONCHANGE="return vNum(this,0,1,X,N);" SIZE="2" >
    </TD>
  </TR>
  <TR >
    <TD CLASS="strcol" WIDTH="60%" >
     H12. Sister
    </TD>
    <TD CLASS="strcol" >
      <INPUT TYPE=text NAME="ClientASI_H12A_1" VALUE="<<ClientASI_H12A_1>>" ONFOCUS="select()" ONCHANGE="return vNum(this,0,1,X,N);" SIZE="2" >
    </TD>
    <TD CLASS="strcol" >
      <INPUT TYPE=text NAME="ClientASI_H12D_1" VALUE="<<ClientASI_H12D_1>>" ONFOCUS="select()" ONCHANGE="return vNum(this,0,1,X,N);" SIZE="2" >
    </TD>
    <TD CLASS="strcol" >
      <INPUT TYPE=text NAME="ClientASI_H12P_1" VALUE="<<ClientASI_H12P_1>>" ONFOCUS="select()" ONCHANGE="return vNum(this,0,1,X,N);" SIZE="2" >
    </TD>
  </TR>
  </TABLE></TD></TR>
  <TR >
    <TD CLASS="strcol" COLSPAN="4" >
      0 = Clearly No for any relatives in that category 
      <BR>1 = Clearly Yes for any relatives in that category 
      <BR>X = Uncertain or don't know
      <BR>N = Never was a relative
      <BR>�In cases where there is more than one person for a category, record the occurrence of problems for any in that group. Accept the patient's judgment on these questions.
    </TD>
  </TR>
  </TABLE></TD></TR>
</TABLE>
<TABLE CLASS="home fullsize" >
  <TR ><TD CLASS="port hdrtxt" >Page 9<BR>Family/Social Status</TD></TR>
    <TR ><TD ><TABLE CLASS="home fullsize" >
  <TR >
    <TD CLASS="strcol" WIDTH="60%" >
      F1. Marital Status:
      <BR>� Common-law marriage = 1. Specify in comments.
    </TD>
    <TD CLASS="strcol" >
      <SELECT NAME="ClientASI_F1_1">[[DBA->selxTable(%form+xMaritalStat+<<ClientASI_F1_1>>+ID Descr)]]</SELECT> 
    </TD>
  </TR>
  <TR >
    <TD CLASS="strcol" WIDTH="60%" >
      F2. How long have you been in this marital status (Q #F1)?
      <BR>� If never married, then since age 18.
    </TD>
    <TD CLASS="strcol" >
      <INPUT TYPE=text NAME="ClientASI_F2Y_1" VALUE="<<ClientASI_F2Y_1>>" ONFOCUS="select()" ONCHANGE="return vNum(this,0,99);" SIZE="2" > Years
      <INPUT TYPE=text NAME="ClientASI_F2M_1" VALUE="<<ClientASI_F2M_1>>" ONFOCUS="select()" ONCHANGE="return vNum(this,0,12);" SIZE="2" > Months
    </TD>
  </TR>
  <TR >
    <TD CLASS="strcol" WIDTH="60%" >
      F3. Are you satisfied with this situation?
      <BR>� Satisfied = generally liking the situation.
      <BR>� Refers to Questions F1 & F2.
    </TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="radio" NAME="ClientASI_F3_1" VALUE=0 <<ClientASI_F3_1=0>> > No
      <INPUT TYPE="radio" NAME="ClientASI_F3_1" VALUE=1 <<ClientASI_F3_1=1>> > Indifferent
      <INPUT TYPE="radio" NAME="ClientASI_F3_1" VALUE=2 <<ClientASI_F3_1=2>> > Yes
    </TD>
  </TR>
  </TABLE></TD></TR>
  <TR ><TD ><TABLE CLASS="home fullsize" >
  <TR >
    <TD CLASS="strcol" WIDTH="60%" >
      F4. Usual living arrangements (past 3 years):
      <BR>� Choose arrangements most representative of the past 3 years. If there is an even split in time between these arrangements, choose the most recent arrangement.
    </TD>
    <TD CLASS="strcol" >
      <SELECT NAME="ClientASI_F4_1">[[DBA->selxTable(%form+xLivingArrASI+<<ClientASI_F4_1>>+ID Descr)]]</SELECT> 
    </TD>
  </TR>
  <TR >
    <TD CLASS="strcol" WIDTH="60%" >
      F5. How long have you lived in these arrangements?
      <BR>� If with parents or family, since age 18.
      <BR>� Code years and months living in arrangements from Question F4.
    </TD>
    <TD CLASS="strcol" >
      <INPUT TYPE=text NAME="ClientASI_F5Y_1" VALUE="<<ClientASI_F5Y_1>>" ONFOCUS="select()" ONCHANGE="return vNum(this,0,99);" SIZE="2" > Years
      <INPUT TYPE=text NAME="ClientASI_F5M_1" VALUE="<<ClientASI_F5M_1>>" ONFOCUS="select()" ONCHANGE="return vNum(this,0,12);" SIZE="2" > Months
    </TD>
  </TR>
  <TR >
    <TD CLASS="strcol" WIDTH="60%" >
      F6. Are you satisfied with these arrangements? 
    </TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="radio" NAME="ClientASI_F6_1" VALUE=0 <<ClientASI_F6_1=0>> > No
      <INPUT TYPE="radio" NAME="ClientASI_F6_1" VALUE=1 <<ClientASI_F6_1=1>> > Indifferent
      <INPUT TYPE="radio" NAME="ClientASI_F6_1" VALUE=2 <<ClientASI_F6_1=2>> > Yes
    </TD>
  </TR>
  </TABLE></TD></TR>
  <TR ><TD ><TABLE CLASS="home fullsize" >
  <TR >
    <TD CLASS="strcol" COLSPAN="2" >
      Do you live with anyone who:
    </TD>
  </TR>
  <TR >
    <TD CLASS="strcol" WIDTH="60%" >
      F7. Has a current alcohol problem? 
    </TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="radio" NAME="ClientASI_F7_1" VALUE=0 <<ClientASI_F7_1=0>> > No
      <INPUT TYPE="radio" NAME="ClientASI_F7_1" VALUE=1 <<ClientASI_F7_1=1>> > Yes
    </TD>
  </TR>
  <TR >
    <TD CLASS="strcol" WIDTH="60%" >
      F8. Uses non-prescribed drugs? 
      <BR>(or abuses prescribed drugs)
    </TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="radio" NAME="ClientASI_F8_1" VALUE=0 <<ClientASI_F8_1=0>> > No
      <INPUT TYPE="radio" NAME="ClientASI_F8_1" VALUE=1 <<ClientASI_F8_1=1>> > Yes
    </TD>
  </TR>
  </TABLE></TD></TR>
  <TR ><TD ><TABLE CLASS="home fullsize" >
  <TR >
    <TD CLASS="strcol" WIDTH="60%" >
      F9. With whom do you spend most of your free time?
      <BR>� If a girlfriend/boyfriend is considered as family by patient, then they must refer to them as family throughout this section, not a friend.
    </TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="radio" NAME="ClientASI_F9_1" VALUE=1 <<ClientASI_F9_1=1>> > Family
      <INPUT TYPE="radio" NAME="ClientASI_F9_1" VALUE=2 <<ClientASI_F9_1=2>> > Friends
      <INPUT TYPE="radio" NAME="ClientASI_F9_1" VALUE=3 <<ClientASI_F9_1=3>> > Alone
    </TD>
  </TR>
  <TR >
    <TD CLASS="strcol" WIDTH="60%" >
      F10. Are you satisfied with spending your free time this way? 
      <BR>� A satisfied response must indicate that the person generally likes the situation. Referring to Question F9.
    </TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="radio" NAME="ClientASI_F10_1" VALUE=0 <<ClientASI_F10_1=0>> > No
      <INPUT TYPE="radio" NAME="ClientASI_F10_1" VALUE=1 <<ClientASI_F10_1=1>> > Indifferent
      <INPUT TYPE="radio" NAME="ClientASI_F10_1" VALUE=2 <<ClientASI_F10_1=2>> > Yes
    </TD>
  </TR>
  </TABLE></TD></TR>
  <TR ><TD ><TABLE CLASS="home fullsize" >
  <TR >
    <TD CLASS="strcol" WIDTH="60%" >
      F11. How many close friends do you have?
      <BR>� Stress that you mean close. Exclude family members. These are "reciprocal" relationships or mutually supportive relationships.
    </TD>
    <TD CLASS="strcol" >
      <INPUT TYPE=text NAME="ClientASI_F11_1" VALUE="<<ClientASI_F11_1>>" ONFOCUS="select()" ONCHANGE="return vNum(this,0,9);" SIZE="2" >
    </TD>
  </TR>
  </TABLE></TD></TR>
</TABLE>
<TABLE CLASS="home fullsize" >
  <TR ><TD ><TABLE CLASS="home fullsize" >
  <TR >
    <TD CLASS="strcol" COLSPAN="4" >
      Would you say you have had a close reciprocal relationship with any of the following people:
    </TD>
  </TR>
  <TR >
    <TD CLASS="strcol" >
      F12. Mother
    </TD>
    <TD CLASS="strcol" >
      <INPUT TYPE=text NAME="ClientASI_F12_1" VALUE="<<ClientASI_F12_1>>" ONFOCUS="select()" ONCHANGE="return vNum(this,0,1,X,N);" SIZE="2" >
    </TD>
    <TD CLASS="strcol" >
      F15. Sexual Partner/Spouse
    </TD>
    <TD CLASS="strcol" >
      <INPUT TYPE=text NAME="ClientASI_F15_1" VALUE="<<ClientASI_F15_1>>" ONFOCUS="select()" ONCHANGE="return vNum(this,0,1,X,N);" SIZE="2" >
    </TD>
  </TR>
  <TR >
    <TD CLASS="strcol" >
      F13. Father
    </TD>
    <TD CLASS="strcol" >
      <INPUT TYPE=text NAME="ClientASI_F13_1" VALUE="<<ClientASI_F13_1>>" ONFOCUS="select()" ONCHANGE="return vNum(this,0,1,X,N);" SIZE="2" >
    </TD>
    <TD CLASS="strcol" >
      F16. Children
    </TD>
    <TD CLASS="strcol" >
      <INPUT TYPE=text NAME="ClientASI_F16_1" VALUE="<<ClientASI_F16_1>>" ONFOCUS="select()" ONCHANGE="return vNum(this,0,1,X,N);" SIZE="2" >
    </TD>
  </TR>
  <TR >
    <TD CLASS="strcol" >
      F14. Brothers/Sisters
    </TD>
    <TD CLASS="strcol" >
      <INPUT TYPE=text NAME="ClientASI_F14_1" VALUE="<<ClientASI_F14_1>>" ONFOCUS="select()" ONCHANGE="return vNum(this,0,1,X,N);" SIZE="2" >
    </TD>
    <TD CLASS="strcol" >
      F17. Friends
    </TD>
    <TD CLASS="strcol" >
      <INPUT TYPE=text NAME="ClientASI_F17_1" VALUE="<<ClientASI_F17_1>>" ONFOCUS="select()" ONCHANGE="return vNum(this,0,1,X,N);" SIZE="2" >
    </TD>
  </TR>
  <TR >
    <TD CLASS="strcol" COLSPAN="4" >
      0 = Clearly No for all in class 
      <BR>1 = Clearly Yes for any in class 
      <BR>X = Uncertain or "I don't know
      <BR>N = Never was a relative
      <BR>� By reciprocal, you mean "that you would do anything you could to help them out and vice versa".
    </TD>
  </TR>
    </TABLE></TD></TR>
</TABLE>
<TABLE CLASS="home fullsize" >
  <TR ><TD CLASS="port hdrtxt" >Page 10<BR>Family/Social (cont.)</TD></TR>
    <TR ><TD ><TABLE CLASS="home fullsize" >
  <TR >
    <TD CLASS="strcol" COLSPAN="3" >
      Have you had significant periods in which you have experienced serious problems getting along with:
    </TD>
  </TR>
  <TR >
    <TD CLASS="strcol" WIDTH="60%" >&nbsp;</TD>
    <TD CLASS="strcol" >
      Past 30 days
    </TD>
    <TD CLASS="strcol" >
      In Your Life
    </TD>
  </TR>
  <TR >
    <TD CLASS="strcol" WIDTH="60%" >
      F18. Mother
    </TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="radio" NAME="ClientASI_F18D_1" VALUE=0 <<ClientASI_F18D_1=0>> > No
      <INPUT TYPE="radio" NAME="ClientASI_F18D_1" VALUE=1 <<ClientASI_F18D_1=1>> > Yes
    </TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="radio" NAME="ClientASI_F18L_1" VALUE=0 <<ClientASI_F18L_1=0>> > No
      <INPUT TYPE="radio" NAME="ClientASI_F18L_1" VALUE=1 <<ClientASI_F18L_1=1>> > Yes
    </TD>
  </TR>
  <TR >
    <TD CLASS="strcol" WIDTH="60%" >
      F19. Father
    </TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="radio" NAME="ClientASI_F19D_1" VALUE=0 <<ClientASI_F19D_1=0>> > No
      <INPUT TYPE="radio" NAME="ClientASI_F19D_1" VALUE=1 <<ClientASI_F19D_1=1>> > Yes
    </TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="radio" NAME="ClientASI_F19L_1" VALUE=0 <<ClientASI_F19L_1=0>> > No
      <INPUT TYPE="radio" NAME="ClientASI_F19L_1" VALUE=1 <<ClientASI_F19L_1=1>> > Yes
    </TD>
  </TR>
  <TR >
    <TD CLASS="strcol" WIDTH="60%" >
      F20. Brother/Sister
    </TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="radio" NAME="ClientASI_F20D_1" VALUE=0 <<ClientASI_F20D_1=0>> > No
      <INPUT TYPE="radio" NAME="ClientASI_F20D_1" VALUE=1 <<ClientASI_F20D_1=1>> > Yes
    </TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="radio" NAME="ClientASI_F20L_1" VALUE=0 <<ClientASI_F20L_1=0>> > No
      <INPUT TYPE="radio" NAME="ClientASI_F20L_1" VALUE=1 <<ClientASI_F20L_1=1>> > Yes
    </TD>
  </TR>
  <TR >
    <TD CLASS="strcol" WIDTH="60%" >
      F21. Sexual Partner/Spouse
    </TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="radio" NAME="ClientASI_F21D_1" VALUE=0 <<ClientASI_F21D_1=0>> > No
      <INPUT TYPE="radio" NAME="ClientASI_F21D_1" VALUE=1 <<ClientASI_F21D_1=1>> > Yes
    </TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="radio" NAME="ClientASI_F21L_1" VALUE=0 <<ClientASI_F21L_1=0>> > No
      <INPUT TYPE="radio" NAME="ClientASI_F21L_1" VALUE=1 <<ClientASI_F21L_1=1>> > Yes
    </TD>
  </TR>
  <TR >
    <TD CLASS="strcol" WIDTH="60%" >
      F22. Children
    </TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="radio" NAME="ClientASI_F22D_1" VALUE=0 <<ClientASI_F22D_1=0>> > No
      <INPUT TYPE="radio" NAME="ClientASI_F22D_1" VALUE=1 <<ClientASI_F22D_1=1>> > Yes
    </TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="radio" NAME="ClientASI_F22L_1" VALUE=0 <<ClientASI_F22L_1=0>> > No
      <INPUT TYPE="radio" NAME="ClientASI_F22L_1" VALUE=1 <<ClientASI_F22L_1=1>> > Yes
    </TD>
  </TR>
  <TR >
    <TD CLASS="strcol" WIDTH="60%" >
      F23. Other Significant Family (specify)
      <BR><INPUT TYPE="TEXT" NAME="ClientASI_F23T_1" VALUE="<<ClientASI_F23T_1>>" ONFOCUS="select()" SIZE=30>
    </TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="radio" NAME="ClientASI_F23D_1" VALUE=0 <<ClientASI_F23D_1=0>> > No
      <INPUT TYPE="radio" NAME="ClientASI_F23D_1" VALUE=1 <<ClientASI_F23D_1=1>> > Yes
    </TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="radio" NAME="ClientASI_F23L_1" VALUE=0 <<ClientASI_F23L_1=0>> > No
      <INPUT TYPE="radio" NAME="ClientASI_F23L_1" VALUE=1 <<ClientASI_F23L_1=1>> > Yes
    </TD>
  </TR>
  <TR >
    <TD CLASS="strcol" WIDTH="60%" >
      F24. Close Friends
    </TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="radio" NAME="ClientASI_F24D_1" VALUE=0 <<ClientASI_F24D_1=0>> > No
      <INPUT TYPE="radio" NAME="ClientASI_F24D_1" VALUE=1 <<ClientASI_F24D_1=1>> > Yes
    </TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="radio" NAME="ClientASI_F24L_1" VALUE=0 <<ClientASI_F24L_1=0>> > No
      <INPUT TYPE="radio" NAME="ClientASI_F24L_1" VALUE=1 <<ClientASI_F24L_1=1>> > Yes
    </TD>
  </TR>
  <TR >
    <TD CLASS="strcol" WIDTH="60%" >
      F25. Neighbors
    </TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="radio" NAME="ClientASI_F25D_1" VALUE=0 <<ClientASI_F25D_1=0>> > No
      <INPUT TYPE="radio" NAME="ClientASI_F25D_1" VALUE=1 <<ClientASI_F25D_1=1>> > Yes
    </TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="radio" NAME="ClientASI_F25L_1" VALUE=0 <<ClientASI_F25L_1=0>> > No
      <INPUT TYPE="radio" NAME="ClientASI_F25L_1" VALUE=1 <<ClientASI_F25L_1=1>> > Yes
    </TD>
  </TR>
  <TR >
    <TD CLASS="strcol" WIDTH="60%" >
      F26. Co-workers
    </TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="radio" NAME="ClientASI_F26D_1" VALUE=0 <<ClientASI_F26D_1=0>> > No
      <INPUT TYPE="radio" NAME="ClientASI_F26D_1" VALUE=1 <<ClientASI_F26D_1=1>> > Yes
    </TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="radio" NAME="ClientASI_F26L_1" VALUE=0 <<ClientASI_F26L_1=0>> > No
      <INPUT TYPE="radio" NAME="ClientASI_F26L_1" VALUE=1 <<ClientASI_F26L_1=1>> > Yes
    </TD>
  </TR>
  <TR >
    <TD CLASS="strcol" COLSPAN="3" >
      � "Serious problems" mean those that endangered the relationship.
      <BR>� A "problem" requires contact of some sort, either by telephone or in person. If no contact code "N"
    </TD>
  </TR>
  </TABLE></TD></TR>
  <TR ><TD ><TABLE CLASS="home fullsize" >
  <TR >
    <TD CLASS="strcol" COLSPAN="3" >
      Has anyone ever abused you?
    </TD>
  </TR>
  <TR >
    <TD CLASS="strcol" WIDTH="60%" >&nbsp;</TD>
    <TD CLASS="strcol" >
      Past 30 days
    </TD>
    <TD CLASS="strcol" >
      In Your Life
    </TD>
  </TR>
  <TR >
    <TD CLASS="strcol" WIDTH="60%" >
      F27. Emotionally?
      � Made you feel bad through harsh words.
    </TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="radio" NAME="ClientASI_F27D_1" VALUE=0 <<ClientASI_F27D_1=0>> > No
      <INPUT TYPE="radio" NAME="ClientASI_F27D_1" VALUE=1 <<ClientASI_F27D_1=1>> > Yes
    </TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="radio" NAME="ClientASI_F27L_1" VALUE=0 <<ClientASI_F27L_1=0>> > No
      <INPUT TYPE="radio" NAME="ClientASI_F27L_1" VALUE=1 <<ClientASI_F27L_1=1>> > Yes
    </TD>
  </TR>
  <TR >
    <TD CLASS="strcol" WIDTH="60%" >
      F28. Physically?
      � Caused you physical harm.
    </TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="radio" NAME="ClientASI_F28D_1" VALUE=0 <<ClientASI_F28D_1=0>> > No
      <INPUT TYPE="radio" NAME="ClientASI_F28D_1" VALUE=1 <<ClientASI_F28D_1=1>> > Yes
    </TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="radio" NAME="ClientASI_F28L_1" VALUE=0 <<ClientASI_F28L_1=0>> > No
      <INPUT TYPE="radio" NAME="ClientASI_F28L_1" VALUE=1 <<ClientASI_F28L_1=1>> > Yes
    </TD>
  </TR>
  <TR >
    <TD CLASS="strcol" WIDTH="60%" >
      F29. Sexually?
      � Forced sexual advances/acts.
    </TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="radio" NAME="ClientASI_F29D_1" VALUE=0 <<ClientASI_F29D_1=0>> > No
      <INPUT TYPE="radio" NAME="ClientASI_F29D_1" VALUE=1 <<ClientASI_F29D_1=1>> > Yes
    </TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="radio" NAME="ClientASI_F29L_1" VALUE=0 <<ClientASI_F29L_1=0>> > No
      <INPUT TYPE="radio" NAME="ClientASI_F29L_1" VALUE=1 <<ClientASI_F29L_1=1>> > Yes
    </TD>
  </TR>
  </TABLE></TD></TR>
  <TR ><TD ><TABLE CLASS="home fullsize" >
  <TR >
    <TD CLASS="strcol" COLSPAN="3" >
       How many days in the past 30 have you had serious conflicts:
    </TD>
  </TR>
  <TR >
    <TD CLASS="strcol" WIDTH="60%" >
      F30. With your family?
    </TD>
    <TD CLASS="strcol" COLSPAN="2" >
      <INPUT TYPE=text NAME="ClientASI_F30_1" VALUE="<<ClientASI_F30_1>>" ONFOCUS="select()" ONCHANGE="return vNum(this,0,30);" SIZE="2" >
    </TD>
  </TR>
  <TR >
    <TD CLASS="strcol" COLSPAN="3" >
       For Questions F32-35, ask the patient to use the Patient Rating scale.
    </TD>
  </TR>
  <TR >
    <TD CLASS="strcol" COLSPAN="3" >
      How troubled or bothered have you been in the past 30 days by:
    </TD>
  </TR>
  <TR >
    <TD CLASS="strcol" WIDTH="60%" >
      F32. Family problems ?
    </TD>
    <TD CLASS="strcol" COLSPAN="2" >
      <SELECT NAME="ClientASI_F32_1">[[DBA->selxTable(%form+xRateScale+<<ClientASI_F32_1>>+ID Descr)]]</SELECT> 
    </TD>
  </TR>
  <TR >
    <TD CLASS="strcol" COLSPAN="3" >
      How important to you now is treatment or counseling for these:
    </TD>
  </TR>
  <TR >
    <TD CLASS="strcol" WIDTH="60%" >
      F34. Family problems
      <BR>� Patient is rating his/her need for counseling for family problems, not whether they would be willing to attend.
    </TD>
    <TD CLASS="strcol" COLSPAN="2" >
      <SELECT NAME="ClientASI_F34_1">[[DBA->selxTable(%form+xRateScale+<<ClientASI_F34_1>>+ID Descr)]]</SELECT> 
    </TD>
  </TR>
  </TABLE></TD></TR>
  <TR ><TD ><TABLE CLASS="home fullsize" >
  <TR >
    <TD CLASS="strcol" COLSPAN="3" >
      How many days in the past 30 have you had serious conflicts:
    </TD>
  </TR>
  <TR >
    <TD CLASS="strcol" WIDTH="60%" >
      F31. With other people (excluding family)?
    </TD>
    <TD CLASS="strcol" COLSPAN="2" >
      <INPUT TYPE=text NAME="ClientASI_F31_1" VALUE="<<ClientASI_F31_1>>" ONFOCUS="select()" ONCHANGE="return vNum(this,0,30);" SIZE="2" >
    </TD>
  </TR>
  <TR >
    <TD CLASS="strcol" COLSPAN="3" >
      For Questions F32-35, ask the patient to use the Patient Rating scale.
    </TD>
  </TR>
  <TR >
    <TD CLASS="strcol" COLSPAN="3" >
      How troubled or bothered have you been in the past 30 days by:
    </TD>
  </TR>
  <TR >
    <TD CLASS="strcol" WIDTH="60%" >
      F33. Social problems?
    </TD>
    <TD CLASS="strcol" COLSPAN="2" >
      <SELECT NAME="ClientASI_F33_1">[[DBA->selxTable(%form+xRateScale+<<ClientASI_F33_1>>+ID Descr)]]</SELECT> 
    </TD>
  </TR>
  <TR >
    <TD CLASS="strcol" COLSPAN="3" >
How important to you now is treatment or counseling for these:
    </TD>
  </TR>
  <TR >
    <TD CLASS="strcol" WIDTH="60%" >
      F35. Social problems
      <BR>� Include patient's need to seek treatment for such social problems as loneliness, inability to socialize, and dissatisfaction with friends. Patient rating should refer to dissatisfaction, conflicts, or other serious problems.
    </TD>
    <TD CLASS="strcol" COLSPAN="2" >
      <SELECT NAME="ClientASI_F35_1">[[DBA->selxTable(%form+xRateScale+<<ClientASI_F35_1>>+ID Descr)]]</SELECT> 
    </TD>
  </TR>
  </TABLE></TD></TR>
  <TR ><TD ><TABLE CLASS="home fullsize" >
  <TR >
    <TD CLASS="strcol" COLSPAN="3" >
      INTERVIEWER SEVERITY RATING
    </TD>
  </TR>
  <TR >
    <TD CLASS="strcol" WIDTH="60%" >
      F36. How would you rate the patient's need for family and/or social counseling?
    </TD>
    <TD CLASS="strcol" COLSPAN="2" >
      <SELECT NAME="ClientASI_F36_1" ONCHANGE="return setSP(this.form,'F36',this);" >[[DBA->selxTable(%form+xSeverityRatings+<<ClientASI_F36_1>>+ID Descr)]]</SELECT> 
    </TD>
  </TR>
  </TABLE></TD></TR>
  <TR ><TD ><TABLE CLASS="home fullsize" >
  <TR >
    <TD CLASS="strcol" COLSPAN="3" >
      CONFIDENCE RATING
    </TD>
  </TR>
  <TR >
    <TD CLASS="strcol" COLSPAN="3" >
      Is the above information significantly distorted by:
    </TD>
  </TR>
  <TR >
    <TD CLASS="strcol" WIDTH="60%" >
F37. Patient's misrepresentation?
    </TD>
    <TD CLASS="strcol" COLSPAN="2" >
      <INPUT TYPE="radio" NAME="ClientASI_F37_1" VALUE=0 <<ClientASI_F37_1=0>> > No
      <INPUT TYPE="radio" NAME="ClientASI_F37_1" VALUE=1 <<ClientASI_F37_1=1>> > Yes
    </TD>
  </TR>
  <TR >
    <TD CLASS="strcol" WIDTH="60%" >
F38. Patient's inability to understand?
    </TD>
    <TD CLASS="strcol" COLSPAN="2" >
      <INPUT TYPE="radio" NAME="ClientASI_F38_1" VALUE=0 <<ClientASI_F38_1=0>> > No
      <INPUT TYPE="radio" NAME="ClientASI_F38_1" VALUE=1 <<ClientASI_F38_1=1>> > Yes
    </TD>
  </TR>
  </TABLE></TD></TR>
  <TR ><TD ><TABLE CLASS="home fullsize" >
  <TR >
    <TD CLASS="strcol" COLSPAN="3" >
      FAMILY/SOCIAL COMMENTS (Include question number with your notes)
      <TEXTAREA NAME="ClientASI_FCOM_1" COLS="90" ROWS="8" WRAP="virtual" ><<ClientASI_FCOM_1>></TEXTAREA>
    </TD>
  </TR>
    </TABLE></TD></TR>
</TABLE>
<TABLE CLASS="home fullsize" >
  <TR ><TD CLASS="port hdrtxt" >Page 11<BR>Psychiatric Status</TD></TR>
    <TR ><TD ><TABLE CLASS="home fullsize" >
  <TR >
    <TD CLASS="strcol" COLSPAN="3" >
      How many times have you been treated for any psychological or emotional problems:
    </TD>
  </TR>
  <TR >
    <TD CLASS="strcol" WIDTH="60%" >
      P1. In a hospital or inpatient setting?
    </TD>
    <TD CLASS="strcol" COLSPAN="2" >
      <INPUT TYPE=text NAME="ClientASI_P1_1" VALUE="<<ClientASI_P1_1>>" ONFOCUS="select()" ONCHANGE="return vNum(this,0,99);" SIZE="2" >
    </TD>
  </TR>
  <TR >
    <TD CLASS="strcol" WIDTH="60%" >
      P2. Outpatient/private patient?
      <BR>� Do not include substance abuse, employment, or family counseling. Treatment episode = a series of more or less continuous visits or treatment days, not the number of visits or treatment days.
    </TD>
    <TD CLASS="strcol" COLSPAN="2" >
      <INPUT TYPE=text NAME="ClientASI_P2_1" VALUE="<<ClientASI_P2_1>>" ONFOCUS="select()" ONCHANGE="return vNum(this,0,99);" SIZE="2" >
      <BR>� Enter diagnosis in comments if known.
    </TD>
  </TR>
  </TABLE></TD></TR>
  <TR ><TD ><TABLE CLASS="home fullsize" >
  <TR >
    <TD CLASS="strcol" WIDTH="60%" >
      P3. Do you receive a pension for a psychiatric disability? 
    </TD>
    <TD CLASS="strcol" COLSPAN="2" >
      <INPUT TYPE="radio" NAME="ClientASI_P3_1" VALUE=0 <<ClientASI_P3_1=0>> > No
      <INPUT TYPE="radio" NAME="ClientASI_P3_1" VALUE=1 <<ClientASI_P3_1=1>> > Yes
    </TD>
  </TR>
  </TABLE></TD></TR>
  <TR ><TD ><TABLE CLASS="home fullsize" >
  <TR >
    <TD CLASS="strcol" COLSPAN="3" >
      Have you had a significant period of time (that was not a direct result of alcohol/drug use) in which you have:
    </TD>
  </TR>
  <TR >
    <TD CLASS="strcol" WIDTH="60%" >&nbsp;</TD>
    <TD CLASS="strcol" >
      Past 30 days
    </TD>
    <TD CLASS="strcol" >
      Lifetime
    </TD>
  </TR>
  <TR >
    <TD CLASS="strcol" WIDTH="60%" >
      P4. Experienced serious depression, sadness, hopelessness, loss of interest?
    </TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="radio" NAME="ClientASI_P4D_1" VALUE=0 <<ClientASI_P4D_1=0>> > No
      <INPUT TYPE="radio" NAME="ClientASI_P4D_1" VALUE=1 <<ClientASI_P4D_1=1>> > Yes
    </TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="radio" NAME="ClientASI_P4L_1" VALUE=0 <<ClientASI_P4L_1=0>> > No
      <INPUT TYPE="radio" NAME="ClientASI_P4L_1" VALUE=1 <<ClientASI_P4L_1=1>> > Yes
    </TD>
  </TR>
  <TR >
    <TD CLASS="strcol" WIDTH="60%" >
      P5. Experienced serious anxiety/tension-uptight, unreasonably worried, inability to feel relaxed?
    </TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="radio" NAME="ClientASI_P5D_1" VALUE=0 <<ClientASI_P5D_1=0>> > No
      <INPUT TYPE="radio" NAME="ClientASI_P5D_1" VALUE=1 <<ClientASI_P5D_1=1>> > Yes
    </TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="radio" NAME="ClientASI_P5L_1" VALUE=0 <<ClientASI_P5L_1=0>> > No
      <INPUT TYPE="radio" NAME="ClientASI_P5L_1" VALUE=1 <<ClientASI_P5L_1=1>> > Yes
    </TD>
  </TR>
  <TR >
    <TD CLASS="strcol" WIDTH="60%" >
      P6. Experienced hallucinations-saw things/heard voices that others didn�t see/hear?
    </TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="radio" NAME="ClientASI_P6D_1" VALUE=0 <<ClientASI_P6D_1=0>> > No
      <INPUT TYPE="radio" NAME="ClientASI_P6D_1" VALUE=1 <<ClientASI_P6D_1=1>> > Yes
    </TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="radio" NAME="ClientASI_P6L_1" VALUE=0 <<ClientASI_P6L_1=0>> > No
      <INPUT TYPE="radio" NAME="ClientASI_P6L_1" VALUE=1 <<ClientASI_P6L_1=1>> > Yes
    </TD>
  </TR>
  <TR >
    <TD CLASS="strcol" WIDTH="60%" >
      P7. Experienced trouble understanding, concentrating, or remembering?
    </TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="radio" NAME="ClientASI_P7D_1" VALUE=0 <<ClientASI_P7D_1=0>> > No
      <INPUT TYPE="radio" NAME="ClientASI_P7D_1" VALUE=1 <<ClientASI_P7D_1=1>> > Yes
    </TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="radio" NAME="ClientASI_P7L_1" VALUE=0 <<ClientASI_P7L_1=0>> > No
      <INPUT TYPE="radio" NAME="ClientASI_P7L_1" VALUE=1 <<ClientASI_P7L_1=1>> > Yes
    </TD>
  </TR>
  </TABLE></TD></TR>
  <TR ><TD ><TABLE CLASS="home fullsize" >
  <TR >
    <TD CLASS="strcol" COLSPAN="3" >
      Have you had a significant period of time ( despite your alcohol and drug use) in which you have: 0-No 1-Yes
    </TD>
  </TR>
  <TR >
    <TD CLASS="strcol" WIDTH="60%" >&nbsp;</TD>
    <TD CLASS="strcol" >
      Past 30 days
    </TD>
    <TD CLASS="strcol" >
      Lifetime
    </TD>
  </TR>
  <TR >
    <TD CLASS="strcol" WIDTH="60%" >
      P8. Experienced trouble controlling violent behavior including episodes of rage, or violence?
      <BR>� Patient can be under the influence of alcohol / drugs.
    </TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="radio" NAME="ClientASI_P8D_1" VALUE=0 <<ClientASI_P8D_1=0>> > No
      <INPUT TYPE="radio" NAME="ClientASI_P8D_1" VALUE=1 <<ClientASI_P8D_1=1>> > Yes
    </TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="radio" NAME="ClientASI_P8L_1" VALUE=0 <<ClientASI_P8L_1=0>> > No
      <INPUT TYPE="radio" NAME="ClientASI_P8L_1" VALUE=1 <<ClientASI_P8L_1=1>> > Yes
    </TD>
  </TR>
  <TR >
    <TD CLASS="strcol" WIDTH="60%" >
      P9. Experienced serious thoughts of suicide?
      <BR>� Patient seriously considered a plan for taking his/her life. Patient can be under the influence of alcohol/drugs.
    </TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="radio" NAME="ClientASI_P9D_1" VALUE=0 <<ClientASI_P9D_1=0>> > No
      <INPUT TYPE="radio" NAME="ClientASI_P9D_1" VALUE=1 <<ClientASI_P9D_1=1>> > Yes
    </TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="radio" NAME="ClientASI_P9L_1" VALUE=0 <<ClientASI_P9L_1=0>> > No
      <INPUT TYPE="radio" NAME="ClientASI_P9L_1" VALUE=1 <<ClientASI_P9L_1=1>> > Yes
    </TD>
  </TR>
  <TR >
    <TD CLASS="strcol" WIDTH="60%" >
      P10. Attempted suicide?
      <BR>� Include actual suicidal gestures or attempts.
      <BR>� Patient can be under the influence of alcohol / drugs.
    </TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="radio" NAME="ClientASI_P10D_1" VALUE=0 <<ClientASI_P10D_1=0>> > No
      <INPUT TYPE="radio" NAME="ClientASI_P10D_1" VALUE=1 <<ClientASI_P10D_1=1>> > Yes
    </TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="radio" NAME="ClientASI_P10L_1" VALUE=0 <<ClientASI_P10L_1=0>> > No
      <INPUT TYPE="radio" NAME="ClientASI_P10L_1" VALUE=1 <<ClientASI_P10L_1=1>> > Yes
    </TD>
  </TR>
  </TABLE></TD></TR>
  <TR ><TD ><TABLE CLASS="home fullsize" >
  <TR >
    <TD CLASS="strcol" WIDTH="60%" >
      P11. Been prescribed medication for any psychological or emotional problems?
      <BR>� Prescribed for the patient by a physician. Record "Yes" if a medication was prescribed even if the patient is not taking it.
    </TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="radio" NAME="ClientASI_P11D_1" VALUE=0 <<ClientASI_P11D_1=0>> > No
      <INPUT TYPE="radio" NAME="ClientASI_P11D_1" VALUE=1 <<ClientASI_P11D_1=1>> > Yes
    </TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="radio" NAME="ClientASI_P11L_1" VALUE=0 <<ClientASI_P11L_1=0>> > No
      <INPUT TYPE="radio" NAME="ClientASI_P11L_1" VALUE=1 <<ClientASI_P11L_1=1>> > Yes
    </TD>
  </TR>
  </TABLE></TD></TR>
  <TR ><TD ><TABLE CLASS="home fullsize" >
  <TR >
    <TD CLASS="strcol" WIDTH="60%" >
      P12. How many days in the past 30 have you experienced these psychological or emotional problems?
      <BR>� This refers to problems noted in Questions P4-P10.
    </TD>
    <TD CLASS="strcol" COLSPAN="2" >
      <INPUT TYPE=text NAME="ClientASI_P12_1" VALUE="<<ClientASI_P12_1>>" ONFOCUS="select()" ONCHANGE="return vNum(this,0,30);" SIZE="2" >
    </TD>
  </TR>
  <TR >
    <TD CLASS="strcol" COLSPAN="3" >
      For Questions P13-P14, ask the patient to use the Patient Rating scale
    </TD>
  </TR>
  <TR >
    <TD CLASS="strcol" WIDTH="60%" >
      P13. How much have you been troubled or bothered by these psychological or emotional problems in the past 30 days?
    </TD>
    <TD CLASS="strcol" COLSPAN="2" >
      <SELECT NAME="ClientASI_P13_1">[[DBA->selxTable(%form+xRateScale+<<ClientASI_P13_1>>+ID Descr)]]</SELECT> 
      � Patient should be rating the problem days from Question P12.
    </TD>
  </TR>
  <TR >
    <TD CLASS="strcol" WIDTH="60%" >
      P14. How important to you now is treatment for these psychological or emotional problems?
    </TD>
    <TD CLASS="strcol" COLSPAN="2" >
      <SELECT NAME="ClientASI_P14_1">[[DBA->selxTable(%form+xRateScale+<<ClientASI_P14_1>>+ID Descr)]]</SELECT> 
    </TD>
  </TR>
    </TABLE></TD></TR>
</TABLE>
<TABLE CLASS="home fullsize" >
  <TR ><TD CLASS="port hdrtxt" >Page 12<BR>Psychiatric Status (cont.)</TD></TR>
    <TR ><TD ><TABLE CLASS="home fullsize" >
  <TR >
    <TD CLASS="strcol" COLSPAN="2" >
      The following items are to be completed by the interviewer:
    </TD>
  </TR>
  <TR >
    <TD CLASS="strcol" COLSPAN="2" >
      At the time of the interview, the patient was:
    </TD>
  </TR>
  <TR >
    <TD CLASS="strcol" WIDTH="60%" >
      P15. Obviously depressed/withdrawn
    </TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="radio" NAME="ClientASI_P15_1" VALUE=0 <<ClientASI_P15_1=0>> > No
      <INPUT TYPE="radio" NAME="ClientASI_P15_1" VALUE=1 <<ClientASI_P15_1=1>> > Yes
    </TD>
  </TR>
  <TR >
    <TD CLASS="strcol" WIDTH="60%" >
      P16. Obviously hostile
    </TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="radio" NAME="ClientASI_P16_1" VALUE=0 <<ClientASI_P16_1=0>> > No
      <INPUT TYPE="radio" NAME="ClientASI_P16_1" VALUE=1 <<ClientASI_P16_1=1>> > Yes
    </TD>
  </TR>
  <TR >
    <TD CLASS="strcol" WIDTH="60%" >
      P17. Obviously anxious/nervous
    </TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="radio" NAME="ClientASI_P17_1" VALUE=0 <<ClientASI_P17_1=0>> > No
      <INPUT TYPE="radio" NAME="ClientASI_P17_1" VALUE=1 <<ClientASI_P17_1=1>> > Yes
    </TD>
  </TR>
  <TR >
    <TD CLASS="strcol" WIDTH="60%" >
      P18. Having trouble with reality testing, thought disorders, paranoid thinking
    </TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="radio" NAME="ClientASI_P18_1" VALUE=0 <<ClientASI_P18_1=0>> > No
      <INPUT TYPE="radio" NAME="ClientASI_P18_1" VALUE=1 <<ClientASI_P18_1=1>> > Yes
    </TD>
  </TR>
  <TR >
    <TD CLASS="strcol" WIDTH="60%" >
      P19. Having trouble comprehending, concentrating, remembering
    </TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="radio" NAME="ClientASI_P19_1" VALUE=0 <<ClientASI_P19_1=0>> > No
      <INPUT TYPE="radio" NAME="ClientASI_P19_1" VALUE=1 <<ClientASI_P19_1=1>> > Yes
    </TD>
  </TR>
  <TR >
    <TD CLASS="strcol" WIDTH="60%" >
      P20. Having suicidal thoughts
    </TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="radio" NAME="ClientASI_P20_1" VALUE=0 <<ClientASI_P20_1=0>> > No
      <INPUT TYPE="radio" NAME="ClientASI_P20_1" VALUE=1 <<ClientASI_P20_1=1>> > Yes
    </TD>
  </TR>
  </TABLE></TD></TR>
  <TR ><TD ><TABLE CLASS="home fullsize" >
  <TR >
    <TD CLASS="strcol" COLSPAN="2" >
      INTERVIEWER SEVERITY RATING
    </TD>
  </TR>
  <TR >
    <TD CLASS="strcol" WIDTH="60%" >
      P21 . How would you rate the patient's need for psychiatric/psychological treatment?
    </TD>
    <TD CLASS="strcol" >
      <SELECT NAME="ClientASI_P21_1" ONCHANGE="return setSP(this.form,'P21',this);" >[[DBA->selxTable(%form+xSeverityRatings+<<ClientASI_P21_1>>+ID Descr)]]</SELECT> 
    </TD>
  </TR>
  </TABLE></TD></TR>
  <TR ><TD ><TABLE CLASS="home fullsize" >
  <TR >
    <TD CLASS="strcol" COLSPAN="2" >
      CONFIDENCE RATING
    </TD>
  </TR>
  <TR >
    <TD CLASS="strcol" COLSPAN="2" >
      Is the above information significantly distorted by:
    </TD>
  </TR>
  <TR >
    <TD CLASS="strcol" WIDTH="60%" >
      P22 Patient's misrepresentation?
    </TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="radio" NAME="ClientASI_P22_1" VALUE=0 <<ClientASI_P22_1=0>> > No
      <INPUT TYPE="radio" NAME="ClientASI_P22_1" VALUE=1 <<ClientASI_P22_1=1>> > Yes
    </TD>
  </TR>
  <TR >
    <TD CLASS="strcol" WIDTH="60%" >
      P23. Patient's inability to understand?
    </TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="radio" NAME="ClientASI_P23_1" VALUE=0 <<ClientASI_P23_1=0>> > No
      <INPUT TYPE="radio" NAME="ClientASI_P23_1" VALUE=1 <<ClientASI_P23_1=1>> > Yes
    </TD>
  </TR>
  </TABLE></TD></TR>
  <TR ><TD ><TABLE CLASS="home fullsize" >
  <TR >
    <TD CLASS="strcol" COLSPAN="2" >
      PSYCHIATRIC STATUS COMMENTS (Include question number with your notes)
      <TEXTAREA NAME="ClientASI_PCOM_1" COLS="90" ROWS="8" WRAP="virtual" ><<ClientASI_PCOM_1>></TEXTAREA>
    </TD>
  </TR>
  </TABLE></TD></TR>
  <TR ><TD ><TABLE CLASS="home fullsize" >
  <TR >
    <TD CLASS="strcol" WIDTH="30%" >
      G12. Special Code
    </TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="radio" NAME="ClientASI_G12_1" VALUE="1" <<ClientASI_G12_1=1>> > 1. Patient terminated by interviewer
      <BR>
      <INPUT TYPE="radio" NAME="ClientASI_G12_1" VALUE="2" <<ClientASI_G12_1=2>> > 2. Patient refused
      <BR>
      <INPUT TYPE="radio" NAME="ClientASI_G12_1" VALUE="3" <<ClientASI_G12_1=3>> > 3. Patient unable to respond ( language or intellectual barrier, under the influence, etc. )
      <BR>
      <INPUT TYPE="radio" NAME="ClientASI_G12_1" VALUE="N" <<ClientASI_G12_1=N>> > N. Interview completed.
    </TD>
  </TR>
  </TABLE></TD></TR>
</TABLE>
<TABLE CLASS="main fullsize" >
  <TR >
    <TD CLASS="numcol" >
      <INPUT TYPE="submit" ONCLICK="return vDELETE('Are you sure you want to delete this entire ASI record?');" NAME="ClientASI_DELETE_1=1&UpdateTables=all&misPOP=1" VALUE="Delete">
      <INPUT TYPE=submit ONCLICK="return validate(this.form);" NAME="UpdateTables=all&misPOP=1" VALUE="Add/Update">
    </TD>
  </TR>
</TABLE>

<INPUT TYPE="hidden" NAME="subview" VALUE="<<subview>>" >
</LOADHIDDEN>
</FORM>
<SCRIPT LANGUAGE="JavaScript">
document.ClientASI.elements[1].focus();
</SCRIPT>

[[myHTML->rightpane(%form+search)]]
