[[myHTML->newPage(%form+Presenting Problems)]]

<SCRIPT LANGUAGE="JavaScript" SRC="/src/cgi/js/vEntry.js"> </SCRIPT>
<SCRIPT LANGUAGE="JavaScript" SRC="/src/cgi/js/vClientMHProblems.js"> </SCRIPT>

<FORM NAME="Problems" ACTION="/cgi/bin/mis.cgi" METHOD="POST" >
<TABLE CLASS="main fullsize" >
  <TR >
    <TD CLASS="strcol" >
      <<<Client_FName_1>>> <<<Client_MName_1>>> <<<Client_LName_1>>> (<<<Client_ClientID_1>>>) <<<Client_SSN_1>>>
      <BR>
      Presenting Problems Page
    </TD>
    <TD CLASS="numcol" >[[gHTML->setLINKS(%form+back)]]</TD>
  </TR>
</TABLE>
<TABLE CLASS="port fullsize" >
  <TR ><TD CLASS="heading" >PRESENTING PROBLEMS</TD></TR>
    <TR ><TD ><TABLE CLASS="home fullsize" >
  <TR >
    <TD CLASS="strcol" >Presenting Problem (Primary)</TD>
    <TD CLASS="strcol" >
      <SELECT NAME="ClientIntake_Problem1_1" >[[DBA->selxTable(%form+xProblems+<<ClientIntake_Problem1_1>>+Catagory Descr CDC)]]</SELECT> 
    </TD>
  </TR>
  <TR >
    <TD CLASS="strcol" >Presenting Problem (Secondary)</TD>
    <TD CLASS="strcol" >
      <SELECT NAME="ClientIntake_Problem2_1" >[[DBA->selxTable(%form+xProblems+<<ClientIntake_Problem2_1>>+Catagory Descr CDC)]]</SELECT> 
    </TD>
  </TR>
  <TR >
    <TD CLASS="strcol" >Presenting Problem (Tertiary)</TD>
    <TD CLASS="strcol" >
      <SELECT NAME="ClientIntake_Problem3_1" >[[DBA->selxTable(%form+xProblems+<<ClientIntake_Problem3_1>>+Catagory Descr CDC)]]</SELECT> 
    </TD>
  </TR>
  <TR ><TD CLASS="port hdrtxt" ><U>History of Presenting Problem</U></TD></TR>
  <TR ><TD CLASS="strcol" COLSPAN="2" >(for Referral Screening specify problems, disposition, referrals if any. If services not appropriate state reason)</TD></TR>
  <TR >
    <TD CLASS="strcol" COLSPAN="2" >
      <TEXTAREA NAME="ClientIntake_Problem_1" COLS="90" ROWS="10" WRAP="virtual" ><<ClientIntake_Problem_1>></TEXTAREA>
    </TD>
  </TR>
  <TR ><TD CLASS="port hdrtxt" ><U>Attempted Solutions by Self or Parent/Teachers</U></TD></TR>
  <TR >
    <TD CLASS="strcol" COLSPAN="2" >
      <INPUT TYPE="checkbox" NAME="ClientMHProblems_PsychTherapy_1" VALUE="1" <<ClientMHProblems_PsychTherapy_1=checkbox>> > Psychological Therapy
      <INPUT TYPE="checkbox" NAME="ClientMHProblems_FamilyTherapy_1" VALUE="1" <<ClientMHProblems_FamilyTherapy_1=checkbox>> > Family Therapy
      <INPUT TYPE="checkbox" NAME="ClientMHProblems_GroupTherapy_1" VALUE="1" <<ClientMHProblems_GroupTherapy_1=checkbox>> > Group Therapy
      <INPUT TYPE="checkbox" NAME="ClientMHProblems_Hospitalization_1" VALUE="1" <<ClientMHProblems_Hospitalization_1=checkbox>> > Hospitalization
      <INPUT TYPE="checkbox" NAME="ClientMHProblems_SpecialDiet_1" VALUE="1" <<ClientMHProblems_SpecialDiet_1=checkbox>> > Special Diet
    </TD>
  </TR>
  <TR >
    <TD CLASS="strcol" COLSPAN="2" >
      <INPUT TYPE="checkbox" NAME="ClientMHProblems_OccupationalTherapy_1" VALUE="1" <<ClientMHProblems_OccupationalTherapy_1=checkbox>> > Occupational Therapy
      <INPUT TYPE="checkbox" NAME="ClientMHProblems_PhysicalTherapy_1" VALUE="1" <<ClientMHProblems_PhysicalTherapy_1=checkbox>> > Physical Therapy
      <INPUT TYPE="checkbox" NAME="ClientMHProblems_SpeechTherapy_1" VALUE="1" <<ClientMHProblems_SpeechTherapy_1=checkbox>> > Speech Therapy
      <INPUT TYPE="checkbox" NAME="ClientMHProblems_VisionTherapy_1" VALUE="1" <<ClientMHProblems_VisionTherapy_1=checkbox>> > Vision Therapy
      <INPUT TYPE="checkbox" NAME="ClientMHProblems_Training_1" VALUE="1" <<ClientMHProblems_Training_1=checkbox>> > Training
    </TD>
  </TR>
  <TR >
    <TD CLASS="strcol" COLSPAN="2" >
      <INPUT TYPE="checkbox" NAME="ClientMHProblems_Medical_1" VALUE="1" <<ClientMHProblems_Medical_1=checkbox>> > Medical
      <INPUT TYPE="checkbox" NAME="ClientMHProblems_OtherTherapy_1" VALUE="1" <<ClientMHProblems_OtherTherapy_1=checkbox>> > Other
      - Please describe any checked items in more detail below:
    </TD>
  </TR>
  <TR>
    <TD CLASS="strcol" COLSPAN="2" >
      <TEXTAREA NAME="ClientMHProblems_OtherTherapyText_1" COLS="90" ROWS="10" WRAP="virtual" ><<ClientMHProblems_OtherTherapyText_1>></TEXTAREA>
    </TD>
  </TR>
    </TABLE></TD></TR>
</TABLE>

<TABLE CLASS="main fullsize" >
  <TR >
    <TD CLASS="numcol" >
      <INPUT TYPE="submit" ONCLICK="return validate(this.form);" NAME="UpdateTables=all&[[myForm->genLink(ClientIntake+ClientHealthHistory.cgi)]]" VALUE="Add/Update -> Health History">
      <INPUT TYPE="submit" ONCLICK="return validate(this.form);" NAME="UpdateTables=all&misPOP=1" VALUE="Add/Update">
    </TD>
  </TR>
</TABLE>

</LOADHIDDEN>
</FORM>
<SCRIPT LANGUAGE="JavaScript">
document.Problems.elements[0].focus();
</SCRIPT>

[[myHTML->rightpane(%form+search)]]
