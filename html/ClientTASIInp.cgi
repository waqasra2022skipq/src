[[myHTML->newPage(%form+Client TASI)]]

<SCRIPT LANGUAGE="JavaScript" SRC="/cgi/js/NoEnter.js"> </SCRIPT>
<SCRIPT LANGUAGE="JavaScript" SRC="/cgi/js/vEntry.js"> </SCRIPT>
<SCRIPT LANGUAGE="JavaScript" SRC="/cgi/js/vClientTASI.js"> </SCRIPT>
<SCRIPT LANGUAGE="JavaScript" SRC="/cgi/js/vDate.js"> </SCRIPT>
<SCRIPT LANGUAGE="JavaScript" SRC="/cgi/js/vAge.js"> </SCRIPT>
<SCRIPT LANGUAGE="JavaScript" SRC="/cgi/js/vNum.js"> </SCRIPT>

<FORM NAME="ClientTASI" ACTION="/cgi/bin/mis.cgi" METHOD="POST" >
<TABLE CLASS="main fullsize" >
  <TR >
    <TD CLASS="strcol" >
      <<<Client_FName_1>>> <<<Client_MName_1>>> <<<Client_LName_1>>> (<<<Client_ClientID_1>>>) <<<Client_SSN_1>>>
      <BR>
      Teen Addiction Severity Index (T-ASI)
    </TD>
    <TD CLASS="numcol" >[[gHTML->setLINKS(%form+back)]]</TD>
  </TR>
</TABLE>
<TABLE CLASS="home fullsize" >
  <TR ><TD CLASS="port hdrtxt" >Page 2<BR>Information</TD></TR>
    <TR ><TD ><TABLE CLASS="home fullsize" >
  <TR >
    <TD CLASS="strcol" >Name</TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="text" NAME="ClientTASI_Name_1" VALUE="<<ClientTASI_Name_1>>" ONFOCUS="select()" SIZE=60>
    </TD>
  </TR>
  <TR >
    <TD CLASS="strcol" >Informant(s) Name</TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="text" NAME="ClientTASI_InfName_1" VALUE="<<ClientTASI_InfName_1>>" ONFOCUS="select()" SIZE=60>
    </TD>
  </TR>
  <TR >
    <TD CLASS="strcol" >Relationship</TD>
    <TD CLASS="strcol" >
      <SELECT NAME="ClientTASI_InfRel_1" MULTIPLE SIZE=10 >
        [[DBA->selxTable(%form+xRelationship+<<ClientTASI_InfRel_1>>+Descr)]]
      </SELECT>
    </TD>
  </TR>
  <TR >
    <TD CLASS="strcol" >Current Address</TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="text" NAME="ClientTASI_Addr1_1" VALUE="<<ClientTASI_Addr1_1>>" ONFOCUS="select()" SIZE=80>
    </TD>
  </TR>
  <TR >
    <TD CLASS="strcol" >&nbsp;</TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="text" NAME="ClientTASI_Addr2_1" VALUE="<<ClientTASI_Addr2_1>>" ONFOCUS="select()" SIZE=80>
    </TD>
  </TR>
  <TR >
    <TD CLASS="strcol" >&nbsp;</TD>
    <TD CLASS="strcol" >
      City
      <INPUT TYPE="text" NAME="ClientTASI_City_1" VALUE="<<ClientTASI_City_1>>" ONFOCUS="select()" SIZE=20>
      State
      <SELECT NAME="ClientTASI_ST_1">
        [[DBA->selxTable(%form+xState+<<ClientTASI_ST_1>>+Descr)]]
      </SELECT> 
      Zip
      <INPUT TYPE="text" NAME="ClientTASI_Zip_1" VALUE="<<ClientTASI_Zip_1>>" ONFOCUS="select()" MAXLENGTH=9 SIZE=9>
    </TD>
  </TR>
  <TR >
    <TD CLASS="strcol" >ID Number</TD>
    <TD CLASS="strcol" >
      <<<ClientTASI_ClientID_1>>>
    </TD>
  </TR>
  <TR >
    <TD CLASS="strcol" >Admission Date</TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="text" NAME="ClientTASI_AdmDate_1" VALUE="<<ClientTASI_AdmDate_1>>" ONFOCUS="select()" ONCHANGE="return vDate(this,0,this.form)" SIZE=10>
    </TD>
  </TR>
  <TR >
    <TD CLASS="strcol" >Interview Date</TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="text" NAME="ClientTASI_IntDate_1" VALUE="<<ClientTASI_IntDate_1>>" ONFOCUS="select()" ONCHANGE="return vDate(this,0,this.form)" SIZE=10>
    </TD>
  </TR>
  <TR >
    <TD CLASS="strcol" >Class</TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="radio" NAME="ClientTASI_Class_1" VALUE=1 <<ClientTASI_Class_1=1>> > Intake
      <INPUT TYPE="radio" NAME="ClientTASI_Class_1" VALUE=2 <<ClientTASI_Class_1=2>> > Follow-up
    </TD>
  </TR>
  <TR >
    <TD CLASS="strcol" >Contact</TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="radio" NAME="ClientTASI_Contact_1" VALUE=1 <<ClientTASI_Contact_1=1>> > Interview
      <INPUT TYPE="radio" NAME="ClientTASI_Contact_1" VALUE=2 <<ClientTASI_Contact_1=2>> > Phone
      <INPUT TYPE="radio" NAME="ClientTASI_Contact_1" VALUE=3 <<ClientTASI_Contact_1=3>> > Mail
    </TD>
  </TR>
  <TR >
    <TD CLASS="strcol" >Birth Gender</TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="radio" NAME="ClientTASI_Gend_1" VALUE="M" <<ClientTASI_Gend_1=M>> > Male
      <INPUT TYPE="radio" NAME="ClientTASI_Gend_1" VALUE="F" <<ClientTASI_Gend_1=F>> > Female
    </TD>
  </TR>
  <TR >
    <TD CLASS="strcol" >Interviewer (Initials)</TD>
    <TD CLASS="strcol" >
      <SELECT NAME="ClientTASI_StaffID_1">[[DBA->selProviders(%form+<<ClientTASI_StaffID_1>>)]]</SELECT> 
    </TD>
  </TR>
  <TR >
    <TD CLASS="strcol" >Status</TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="radio" NAME="ClientTASI_Status_1" VALUE=1 <<ClientTASI_Status_1=1>> > Patient Terminated
      <INPUT TYPE="radio" NAME="ClientTASI_Status_1" VALUE=2 <<ClientTASI_Status_1=2>> > Patient Refused
      <INPUT TYPE="radio" NAME="ClientTASI_Status_1" VALUE=3 <<ClientTASI_Status_1=3>> > Patient Unable to Respond
    </TD>
  </TR>
  <TR >
    <TD CLASS="strcol" >Birthdate</TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="text" NAME="ClientTASI_DOB_1" VALUE="<<ClientTASI_DOB_1>>" ONFOCUS="select()" ONCHANGE="return vDate(this,0,this.form)" SIZE=10>
    </TD>
  </TR>
  <TR >
    <TD CLASS="strcol" >Race</TD>
    <TD CLASS="strcol" >
      <SELECT NAME="ClientTASI_Race_1" >
        [[DBA->selxTable(%form+xRaces+<<ClientTASI_Race_1>>+Descr)]]
      </SELECT> 
    </TD>
  </TR>
  <TR >
    <TD CLASS="strcol" >Religious Preference</TD>
    <TD CLASS="strcol" >
      <SELECT NAME="ClientTASI_Religion_1">
        [[DBA->selxTable(%form+xReligiousAffiliation+<<ClientTASI_Religion_1>>+Descr)]]
      </SELECT> 
    </TD>
  </TR>
    </TABLE></TD></TR>
</TABLE>
<TABLE CLASS="home fullsize" >
  <TR ><TD CLASS="port hdrtxt" >Page 3<BR>Information</TD></TR>
    <TR ><TD ><TABLE CLASS="home fullsize" >
  <TR >
    <TD CLASS="strcol" COLSPAN="2" >
      Have you been in a controlled environment in the past year?
    </TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="radio" NAME="ClientTASI_ContEnvi_1" VALUE="n" <<ClientTASI_ContEnvi_1=n>> > No<BR>
      <INPUT TYPE="radio" NAME="ClientTASI_ContEnvi_1" VALUE="dc" <<ClientTASI_ContEnvi_1=dc>> > Detention Center<BR>
      <INPUT TYPE="radio" NAME="ClientTASI_ContEnvi_1" VALUE="ct" <<ClientTASI_ContEnvi_1=ct>> > Chemical Treatment<BR>
      <INPUT TYPE="radio" NAME="ClientTASI_ContEnvi_1" VALUE="mt" <<ClientTASI_ContEnvi_1=mt>> > Medical Treatment<BR>
      <INPUT TYPE="radio" NAME="ClientTASI_ContEnvi_1" VALUE="pt" <<ClientTASI_ContEnvi_1=pt>> > Psychiatric Treatment<BR>
    </TD>
  </TR>
  <TR >
    <TD CLASS="strcol" COLSPAN="2" >How many days</TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="text" NAME="ClientTASI_CEDays_1" VALUE="<<ClientTASI_CEDays_1>>" ONFOCUS="select()" ONCHANGE="return vNum(this,0,30);" SIZE=2>
    </TD>
  </TR>
  <TR >
    <TD CLASS="strcol" COLSPAN="2" >Record dates:</TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="text" NAME="ClientTASI_CEDates_1" VALUE="<<ClientTASI_CEDates_1>>" ONFOCUS="select()" SIZE=60>
    </TD>
  </TR>
    </TABLE></TD></TR>
    <TR ><TD CLASS="port hdrtxt" COLSPAN="3" ><TABLE CLASS="home fullsize" >
  <TR ><TD CLASS="strcol" COLSPAN="3" >SEVERITY PROFILE</TD></TR>
  <TR >
    <TD CLASS="strcol" WIDTH="5%" >&nbsp;</TD>
    <TD CLASS="strcol" >Chemical (substance) use</TD>
    <TD CLASS="strcol" >
      <SELECT NAME="ClientTASI_SPChemical_1">
        [[DBA->selxTable(%form+xRateScale+<<ClientTASI_SPChemical_1>>+ID Descr)]]
      </SELECT> 
    </TD>
  </TR>
  <TR >
    <TD CLASS="strcol" WIDTH="5%" >&nbsp;</TD>
    <TD CLASS="strcol" >School</TD>
    <TD CLASS="strcol" >
      <SELECT NAME="ClientTASI_SPSchool_1">
        [[DBA->selxTable(%form+xRateScale+<<ClientTASI_SPSchool_1>>+ID Descr)]]
      </SELECT> 
    </TD>
  </TR>
  <TR >
    <TD CLASS="strcol" WIDTH="5%" >&nbsp;</TD>
    <TD CLASS="strcol" >Emp/Sup</TD>
    <TD CLASS="strcol" >
      <SELECT NAME="ClientTASI_SPEmpSup_1">
        [[DBA->selxTable(%form+xRateScale+<<ClientTASI_SPEmpSup_1>>+ID Descr)]]
      </SELECT> 
    </TD>
  </TR>
  <TR >
    <TD CLASS="strcol" WIDTH="5%" >&nbsp;</TD>
    <TD CLASS="strcol" >Family</TD>
    <TD CLASS="strcol" >
      <SELECT NAME="ClientTASI_SPFamily_1">
        [[DBA->selxTable(%form+xRateScale+<<ClientTASI_SPFamily_1>>+ID Descr)]]
      </SELECT> 
    </TD>
  </TR>
  <TR >
    <TD CLASS="strcol" WIDTH="5%" >&nbsp;</TD>
    <TD CLASS="strcol" >Peer/Soc</TD>
    <TD CLASS="strcol" >
      <SELECT NAME="ClientTASI_SPPeerSoc_1">
        [[DBA->selxTable(%form+xRateScale+<<ClientTASI_SPPeerSoc_1>>+ID Descr)]]
      </SELECT> 
    </TD>
  </TR>
  <TR >
    <TD CLASS="strcol" WIDTH="5%" >&nbsp;</TD>
    <TD CLASS="strcol" >Legal</TD>
    <TD CLASS="strcol" >
      <SELECT NAME="ClientTASI_SPLegal_1">
        [[DBA->selxTable(%form+xRateScale+<<ClientTASI_SPLegal_1>>+ID Descr)]]
      </SELECT> 
    </TD>
  </TR>
  <TR >
    <TD CLASS="strcol" WIDTH="5%" >&nbsp;</TD>
    <TD CLASS="strcol" >Psychiatric</TD>
    <TD CLASS="strcol" >
      <SELECT NAME="ClientTASI_SPPsych_1">
        [[DBA->selxTable(%form+xRateScale+<<ClientTASI_SPPsych_1>>+ID Descr)]]
      </SELECT> 
    </TD>
  </TR>
    </TABLE></TD></TR>
</TABLE>
<TABLE CLASS="home fullsize" >
  <TR ><TD CLASS="port hdrtxt" >Page 4<BR>Chemical (Substance) Use</TD></TR>
    <TR ><TD ><TABLE CLASS="home fullsize" >
  <TR >
    <TD CLASS="strcol" COLSPAN=5 >
      1. What chemicals have you used in the past month?
    </TD>
  </TR>
  <TR >
    <TD CLASS="strcol" >Drugs</TD>
    <TD CLASS="strcol" >Route</TD>
    <TD CLASS="strcol" >No.ofDays</TD>
    <TD CLASS="strcol" >Age Started</TD>
    <TD CLASS="strcol" >&nbsp;</TD>
  </TR>
  <TR >
    <TD CLASS="strcol" >&nbsp;</TD>
    <TD CLASS="strcol" >&nbsp;</TD>
    <TD CLASS="strcol" >&nbsp;</TD>
    <TD CLASS="strcol" >(yrs./mos.)</TD>
    <TD CLASS="strcol" >&nbsp;</TD>
  </TR>
  <TR >
    <TD CLASS="strcol" >
      <SELECT NAME="ClientTASI_D1D1_1">
        [[DBA->selxTable(%form+xDrugs+<<ClientTASI_D1D1_1>>+Descr)]]
      </SELECT>
    </TD>
    <TD CLASS="strcol" >
      <SELECT NAME="ClientTASI_D1R1_1">
        [[DBA->selxTable(%form+xDrugRoutes+<<ClientTASI_D1R1_1>>+ID Descr)]]
      </SELECT> 
    </TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="text" NAME="ClientTASI_D1C1_1" VALUE="<<ClientTASI_D1C1_1>>" ONFOCUS="select()" ONCHANGE="return vNum(this,0,30);" SIZE=2>
    </TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="text" NAME="ClientTASI_D1A1_1" VALUE="<<ClientTASI_D1A1_1>>" ONFOCUS="select()" SIZE=5 ONCHANGE="return vAge(this)" >
    </TD>
    <TD CLASS="strcol" >&nbsp;</TD>
  </TR>
  <TR >
    <TD CLASS="strcol" >
      <SELECT NAME="ClientTASI_D1D2_1">
        [[DBA->selxTable(%form+xDrugs+<<ClientTASI_D1D2_1>>+Descr)]]
      </SELECT>
    </TD>
    <TD CLASS="strcol" >
      <SELECT NAME="ClientTASI_D1R2_1">
        [[DBA->selxTable(%form+xDrugRoutes+<<ClientTASI_D1R2_1>>+ID Descr)]]
      </SELECT> 
    </TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="text" NAME="ClientTASI_D1C2_1" VALUE="<<ClientTASI_D1C2_1>>" ONFOCUS="select()" ONCHANGE="return vNum(this,0,30);" SIZE=2>
    </TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="text" NAME="ClientTASI_D1A2_1" VALUE="<<ClientTASI_D1A2_1>>" ONFOCUS="select()" SIZE=5 ONCHANGE="return vAge(this)" >
    </TD>
    <TD CLASS="strcol" >&nbsp;</TD>
  </TR>
  <TR >
    <TD CLASS="strcol" >
      <SELECT NAME="ClientTASI_D1D3_1">
        [[DBA->selxTable(%form+xDrugs+<<ClientTASI_D1D3_1>>+Descr)]]
      </SELECT>
    </TD>
    <TD CLASS="strcol" >
      <SELECT NAME="ClientTASI_D1R3_1">
        [[DBA->selxTable(%form+xDrugRoutes+<<ClientTASI_D1R3_1>>+ID Descr)]]
      </SELECT> 
    </TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="text" NAME="ClientTASI_D1C3_1" VALUE="<<ClientTASI_D1C3_1>>" ONFOCUS="select()" ONCHANGE="return vNum(this,0,30);" SIZE=2>
    </TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="text" NAME="ClientTASI_D1A3_1" VALUE="<<ClientTASI_D1A3_1>>" ONFOCUS="select()" SIZE=5 ONCHANGE="return vAge(this)" >
    </TD>
    <TD CLASS="strcol" >&nbsp;</TD>
  </TR>
  <TR >
    <TD CLASS="strcol" COLSPAN=5 >
      2. Are there chemicals you have used before that you have not used in the past month?
    </TD>
  </TR>
  <TR >
    <TD CLASS="strcol" >Drugs</TD>
    <TD CLASS="strcol" >Route</TD>
    <TD CLASS="strcol" >Age Started</TD>
    <TD CLASS="strcol" >Age Stopped</TD>
    <TD CLASS="strcol" >Frequency</TD>
  </TR>
  <TR >
    <TD CLASS="strcol" >&nbsp;</TD>
    <TD CLASS="strcol" >&nbsp;</TD>
    <TD CLASS="strcol" >(yrs./mos.)</TD>
    <TD CLASS="strcol" >(yrs./mos.)</TD>
    <TD CLASS="strcol" >&nbsp;</TD>
  </TR>
  <TR >
    <TD CLASS="strcol" >
      <SELECT NAME="ClientTASI_D2D1_1">
        [[DBA->selxTable(%form+xDrugs+<<ClientTASI_D2D1_1>>+Descr)]]
      </SELECT>
    </TD>
    <TD CLASS="strcol" >
      <SELECT NAME="ClientTASI_D2R1_1">
        [[DBA->selxTable(%form+xDrugRoutes+<<ClientTASI_D2R1_1>>+ID Descr)]]
      </SELECT> 
    </TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="text" NAME="ClientTASI_D2B1_1" VALUE="<<ClientTASI_D2B1_1>>" ONFOCUS="select()" SIZE=5 ONCHANGE="return vAge(this)" >
    </TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="text" NAME="ClientTASI_D2E1_1" VALUE="<<ClientTASI_D2E1_1>>" ONFOCUS="select()" SIZE=5 ONCHANGE="return vAge(this)" >
    </TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="text" NAME="ClientTASI_D2F1_1" VALUE="<<ClientTASI_D2F1_1>>" ONFOCUS="select()" ONCHANGE="return vNum(this,0,30);" SIZE=2>
    </TD>
  </TR>
  <TR >
    <TD CLASS="strcol" >
      <SELECT NAME="ClientTASI_D2D2_1">
        [[DBA->selxTable(%form+xDrugs+<<ClientTASI_D2D2_1>>+Descr)]]
      </SELECT>
    </TD>
    <TD CLASS="strcol" >
      <SELECT NAME="ClientTASI_D2R2_1">
        [[DBA->selxTable(%form+xDrugRoutes+<<ClientTASI_D2R2_1>>+ID Descr)]]
      </SELECT> 
    </TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="text" NAME="ClientTASI_D2B2_1" VALUE="<<ClientTASI_D2B2_1>>" ONFOCUS="select()" SIZE=5 ONCHANGE="return vAge(this)" >
    </TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="text" NAME="ClientTASI_D2E2_1" VALUE="<<ClientTASI_D2E2_1>>" ONFOCUS="select()" SIZE=5 ONCHANGE="return vAge(this)" >
    </TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="text" NAME="ClientTASI_D2F2_1" VALUE="<<ClientTASI_D2F2_1>>" ONFOCUS="select()" ONCHANGE="return vNum(this,0,30);" SIZE=2>
    </TD>
  </TR>
  <TR >
    <TD CLASS="strcol" >
      <SELECT NAME="ClientTASI_D2D3_1">
        [[DBA->selxTable(%form+xDrugs+<<ClientTASI_D2D3_1>>+Descr)]]
      </SELECT>
    </TD>
    <TD CLASS="strcol" >
      <SELECT NAME="ClientTASI_D2R3_1">
        [[DBA->selxTable(%form+xDrugRoutes+<<ClientTASI_D2R3_1>>+ID Descr)]]
      </SELECT> 
    </TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="text" NAME="ClientTASI_D2B3_1" VALUE="<<ClientTASI_D2B3_1>>" ONFOCUS="select()" SIZE=5 ONCHANGE="return vAge(this)" >
    </TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="text" NAME="ClientTASI_D2E3_1" VALUE="<<ClientTASI_D2E3_1>>" ONFOCUS="select()" SIZE=5 ONCHANGE="return vAge(this)" >
    </TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="text" NAME="ClientTASI_D2F3_1" VALUE="<<ClientTASI_D2F3_1>>" ONFOCUS="select()" ONCHANGE="return vNum(this,0,30);" SIZE=2>
    </TD>
  </TR>
  <TR >
    <TD CLASS="strcol" >
      <SELECT NAME="ClientTASI_D2D4_1">
        [[DBA->selxTable(%form+xDrugs+<<ClientTASI_D2D4_1>>+Descr)]]
      </SELECT>
    </TD>
    <TD CLASS="strcol" >
      <SELECT NAME="ClientTASI_D2R4_1">
        [[DBA->selxTable(%form+xDrugRoutes+<<ClientTASI_D2R4_1>>+ID Descr)]]
      </SELECT> 
    </TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="text" NAME="ClientTASI_D2B4_1" VALUE="<<ClientTASI_D2B4_1>>" ONFOCUS="select()" SIZE=5 ONCHANGE="return vAge(this)" >
    </TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="text" NAME="ClientTASI_D2E4_1" VALUE="<<ClientTASI_D2E4_1>>" ONFOCUS="select()" SIZE=5 ONCHANGE="return vAge(this)" >
    </TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="text" NAME="ClientTASI_D2F4_1" VALUE="<<ClientTASI_D2F4_1>>" ONFOCUS="select()" ONCHANGE="return vNum(this,0,30);" SIZE=2>
    </TD>
  </TR>
  <TR >
    <TD CLASS="strcol" COLSPAN=5 >
      3. Name Combinations of drugs or alcohol that you have used in the past month.
    </TD>
  </TR>
  <TR >
    <TD CLASS="strcol" >Drugs</TD>
    <TD CLASS="strcol" >No.ofDays</TD>
    <TD CLASS="strcol" >&nbsp;</TD>
    <TD CLASS="strcol" >&nbsp;</TD>
    <TD CLASS="strcol" >&nbsp;</TD>
  </TR>
  <TR >
    <TD CLASS="strcol" >
      <SELECT NAME="ClientTASI_D3D1_1">
        [[DBA->selxTable(%form+xDrugs+<<ClientTASI_D3D1_1>>+Descr)]]
      </SELECT>
    </TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="text" NAME="ClientTASI_D3C1_1" VALUE="<<ClientTASI_D3C1_1>>" ONFOCUS="select()" ONCHANGE="return vNum(this,0,30);" SIZE=2>
    </TD>
    <TD CLASS="strcol" >&nbsp;</TD>
    <TD CLASS="strcol" >&nbsp;</TD>
    <TD CLASS="strcol" >&nbsp;</TD>
  </TR>
  <TR >
    <TD CLASS="strcol" >
      <SELECT NAME="ClientTASI_D3D2_1">
        [[DBA->selxTable(%form+xDrugs+<<ClientTASI_D3D2_1>>+Descr)]]
      </SELECT>
    </TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="text" NAME="ClientTASI_D3C2_1" VALUE="<<ClientTASI_D3C2_1>>" ONFOCUS="select()" ONCHANGE="return vNum(this,0,30);" SIZE=2>
    </TD>
    <TD CLASS="strcol" >&nbsp;</TD>
    <TD CLASS="strcol" >&nbsp;</TD>
    <TD CLASS="strcol" >&nbsp;</TD>
  </TR>
  <TR >
    <TD CLASS="strcol" >
      <SELECT NAME="ClientTASI_D3D3_1">
        [[DBA->selxTable(%form+xDrugs+<<ClientTASI_D3D3_1>>+Descr)]]
      </SELECT>
    </TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="text" NAME="ClientTASI_D3C3_1" VALUE="<<ClientTASI_D3C3_1>>" ONFOCUS="select()" ONCHANGE="return vNum(this,0,30);" SIZE=2>
    </TD>
    <TD CLASS="strcol" >&nbsp;</TD>
    <TD CLASS="strcol" >&nbsp;</TD>
    <TD CLASS="strcol" >&nbsp;</TD>
  </TR>
  <TR >
    <TD CLASS="strcol" >
      <SELECT NAME="ClientTASI_D3D4_1">
        [[DBA->selxTable(%form+xDrugs+<<ClientTASI_D3D4_1>>+Descr)]]
      </SELECT>
    </TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="text" NAME="ClientTASI_D3C4_1" VALUE="<<ClientTASI_D3C4_1>>" ONFOCUS="select()" ONCHANGE="return vNum(this,0,30);" SIZE=2>
    </TD>
    <TD CLASS="strcol" >&nbsp;</TD>
    <TD CLASS="strcol" >&nbsp;</TD>
    <TD CLASS="strcol" >&nbsp;</TD>
  </TR>
  <TR >
    <TD CLASS="strcol" COLSPAN=5 >
      COMMENTS
      <TEXTAREA NAME="ClientTASI_D3COM_1" COLS=90 ROWS=8 WRAP=virtual ><<ClientTASI_D3COM_1>></TEXTAREA>
    </TD>
  </TR>
    </TABLE></TD></TR>
</TABLE>
<TABLE CLASS="home fullsize" >
  <TR ><TD CLASS="port hdrtxt" >Page 5<BR>Chemical (Substance) Use (cont.)</TD></TR>
    <TR ><TD ><TABLE CLASS="home fullsize" >
  <TR >
    <TD CLASS="strcol" COLSPAN="3" >
      4. Which chemical(s) or combination of checmicals do you believe is/are your major problem(s)? Prioritize.
    </TD>
  </TR>
  <TR >
    <TD CLASS="strcol" COLSPAN="3" >Drugs</TD>
  </TR>
  <TR >
    <TD CLASS="strcol" COLSPAN="3" >
      <SELECT NAME="ClientTASI_D4D1_1">
        [[DBA->selxTable(%form+xDrugs+<<ClientTASI_D4D1_1>>+Descr)]]
      </SELECT>
    </TD>
  </TR>
  <TR >
    <TD CLASS="strcol" COLSPAN="3" >
      5. Why do you believe the drug(s) is/are a major problem? Reason. (Comments)
    </TD>
  </TR>
  <TR >
    <TD CLASS="strcol" WIDTH="5%" >&nbsp;</TD>
    <TD CLASS="strcol" COLSPAN="2" >
      Problem Area:
      <UL><LI>peer/soc</LI> <LI>legal</LI> <LI>emp/sup</LI> <LI>psych</LI> <LI>family</LI> <LI>loss of control and/or craving</LI> <LI>school</LI></UL>
    </TD>
  </TR>
  <TR >
    <TD CLASS="strcol" WIDTH="5%" >&nbsp;</TD>
    <TD CLASS="strcol" COLSPAN="2" >
      <TEXTAREA NAME="ClientTASI_D5COM_1" COLS=90 ROWS=4 WRAP=virtual ><<ClientTASI_D5COM_1>></TEXTAREA>
    </TD>
  </TR>
  <TR >
    <TD CLASS="strcol" COLSPAN="3" >
      6. Duration of your last period of voluntary abstinence from all abused chemicals?
      <INPUT TYPE="text" NAME="ClientTASI_D6C_1" VALUE="<<ClientTASI_D6C_1>>" ONFOCUS="select()" ONCHANGE="return vNum(this,0,30);" SIZE=2>
    </TD>
  </TR>
  <TR >
    <TD CLASS="strcol" COLSPAN="3" >
      7. How many months ago did this abstinence end?
      <INPUT TYPE="text" NAME="ClientTASI_D7C_1" VALUE="<<ClientTASI_D7C_1>>" ONFOCUS="select()" ONCHANGE="return vNum(this,0,30);" SIZE=2>
    </TD>
  </TR>
  <TR >
    <TD CLASS="strcol" COLSPAN="3" >
      8. How many times have you:
    </TD>
  </TR>
  <TR >
    <TD CLASS="strcol" WIDTH="5%" >&nbsp;</TD>
    <TD CLASS="strcol" COLSPAN="2" >
      Had an alcohol blackout?
      <INPUT TYPE="text" NAME="ClientTASI_D8A_1" VALUE="<<ClientTASI_D8A_1>>" ONFOCUS="select()" ONCHANGE="return vNum(this,0,30);" SIZE=2>
    </TD>
  </TR>
  <TR >
    <TD CLASS="strcol" WIDTH="5%" >&nbsp;</TD>
    <TD CLASS="strcol" COLSPAN="2" >
      Overdosed on drugs?
      <INPUT TYPE="text" NAME="ClientTASI_D8O_1" VALUE="<<ClientTASI_D8O_1>>" ONFOCUS="select()" ONCHANGE="return vNum(this,0,30);" SIZE=2>
    </TD>
  </TR>
  <TR >
    <TD CLASS="strcol" COLSPAN="3" >
      9. How many times in your life have you been treated for:
    </TD>
  </TR>
  <TR >
    <TD CLASS="strcol" WIDTH="5%" >&nbsp;</TD>
    <TD CLASS="strcol" COLSPAN="2" >
      Alcohol abuse or dependence
      <INPUT TYPE="text" NAME="ClientTASI_D9A_1" VALUE="<<ClientTASI_D9A_1>>" ONFOCUS="select()" ONCHANGE="return vNum(this,0,30);" SIZE=2>
    </TD>
  </TR>
  <TR >
    <TD CLASS="strcol" WIDTH="5%" >&nbsp;</TD>
    <TD CLASS="strcol" COLSPAN="2" >
      Drug abuse or dependence
      <INPUT TYPE="text" NAME="ClientTASI_D9D_1" VALUE="<<ClientTASI_D9D_1>>" ONFOCUS="select()" ONCHANGE="return vNum(this,0,30);" SIZE=2>
    </TD>
  </TR>
  <TR >
    <TD CLASS="strcol" WIDTH="5%" >&nbsp;</TD>
    <TD CLASS="strcol" COLSPAN="2" >
      Alcohol & drug abuse or dependence
      <INPUT TYPE="text" NAME="ClientTASI_D9AD_1" VALUE="<<ClientTASI_D9AD_1>>" ONFOCUS="select()" ONCHANGE="return vNum(this,0,30);" SIZE=2>
    </TD>
  </TR>
  <TR >
    <TD CLASS="strcol" COLSPAN="3" >
      10. How many of these were detox only?
    </TD>
  </TR>
  <TR >
    <TD CLASS="strcol" WIDTH="5%" >&nbsp;</TD>
    <TD CLASS="strcol" COLSPAN="2" >
      Alcohol
      <INPUT TYPE="text" NAME="ClientTASI_D10A_1" VALUE="<<ClientTASI_D10A_1>>" ONFOCUS="select()" ONCHANGE="return vNum(this,0,30);" SIZE=2>
    </TD>
  </TR>
  <TR >
    <TD CLASS="strcol" WIDTH="5%" >&nbsp;</TD>
    <TD CLASS="strcol" COLSPAN="2" >
      Drug
      <INPUT TYPE="text" NAME="ClientTASI_D10D_1" VALUE="<<ClientTASI_D10D_1>>" ONFOCUS="select()" ONCHANGE="return vNum(this,0,30);" SIZE=2>
    </TD>
  </TR>
  <TR >
    <TD CLASS="strcol" COLSPAN="3" >
      COMMENTS
      <TEXTAREA NAME="ClientTASI_D10COM_1" COLS=90 ROWS=8 WRAP=virtual ><<ClientTASI_D10COM_1>></TEXTAREA>
    </TD>
  </TR>
    </TABLE></TD></TR>
</TABLE>
<TABLE CLASS="home fullsize" >
  <TR ><TD CLASS="port hdrtxt" >Page 6<BR>Chemical (Substance) Use (cont.)</TD></TR>
    <TR ><TD ><TABLE CLASS="home fullsize" >
  <TR >
    <TD CLASS="strcol" COLSPAN="3" >
      11. How much money would you say you spent during the past month on:
    </TD>
  </TR>
  <TR >
    <TD CLASS="strcol" WIDTH="5%" >&nbsp;</TD>
    <TD CLASS="strcol" COLSPAN="2" >
      Alcohol
      <INPUT TYPE="text" NAME="ClientTASI_D11A_1" VALUE="<<ClientTASI_D11A_1>>" ONFOCUS="select()" ONCHANGE="return vNum(this,0,10000);" SIZE=2>
    </TD>
  </TR>
  <TR >
    <TD CLASS="strcol" WIDTH="5%" >&nbsp;</TD>
    <TD CLASS="strcol" COLSPAN="2" >
      Drugs
      <INPUT TYPE="text" NAME="ClientTASI_D11D_1" VALUE="<<ClientTASI_D11D_1>>" ONFOCUS="select()" ONCHANGE="return vNum(this,0,10000);" SIZE=2>
    </TD>
  </TR>
  <TR >
    <TD CLASS="strcol" COLSPAN="3" >
      12. Did you obtain the drugs through:
    </TD>
  </TR>
  <TR >
    <TD CLASS="strcol" WIDTH="5%" >&nbsp;</TD>
    <TD CLASS="strcol" COLSPAN="2" >
      Sexual favors 
      <INPUT TYPE=checkbox NAME="ClientTASI_D12S_1" VALUE=1 <<ClientTASI_D12S_1=checkbox>> >
    </TD>
  </TR>
  <TR >
    <TD CLASS="strcol" WIDTH="5%" >&nbsp;</TD>
    <TD CLASS="strcol" COLSPAN="2" >
      Illegal activities
      <INPUT TYPE=checkbox NAME="ClientTASI_D12I_1" VALUE=1 <<ClientTASI_D12I_1=checkbox>> >
    </TD>
  </TR>
  <TR >
    <TD CLASS="strcol" COLSPAN="2" >
      13. How many days have you been treated in an outpatient setting for alcohol or drugs in the past month?
    </TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="text" NAME="ClientTASI_D13D_1" VALUE="<<ClientTASI_D13D_1>>" ONFOCUS="select()" ONCHANGE="return vNum(this,0,30);" SIZE=2>
    </TD>
  </TR>
  <TR >
    <TD CLASS="strcol" COLSPAN="2" >
      14. How many meetings have you been attending self-help groups (AA, NA, etc.) in the past month?
    </TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="text" NAME="ClientTASI_D14M_1" VALUE="<<ClientTASI_D14M_1>>" ONFOCUS="select()" ONCHANGE="return vNum(this,0,30);" SIZE=2>
    </TD>
  </TR>
  <TR >
    <TD CLASS="strcol" COLSPAN="2" >
      15. How many days have you been attending self-help groups (AA, NA, etc.) since your lastfollow-up meeting?
    </TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="text" NAME="ClientTASI_D15D_1" VALUE="<<ClientTASI_D15D_1>>" ONFOCUS="select()" ONCHANGE="return vNum(this,0,30);" SIZE=2>
    </TD>
  </TR>
  <TR >
    <TD CLASS="strcol" COLSPAN="2" >
      16. How many days have you been treated in an outpatient setting for alcohol or drugs sinceyour last follow-up meeting?
    </TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="text" NAME="ClientTASI_D16D_1" VALUE="<<ClientTASI_D16D_1>>" ONFOCUS="select()" ONCHANGE="return vNum(this,0,30);" SIZE=2>
    </TD>
  </TR>
  <TR >
    <TD CLASS="strcol" COLSPAN="2" >
      17. How many days have you been treated in an inpatient or a residential facility for alcoholor drugs since your last follow-up meeting?
    </TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="text" NAME="ClientTASI_D17D_1" VALUE="<<ClientTASI_D17D_1>>" ONFOCUS="select()" ONCHANGE="return vNum(this,0,30);" SIZE=2>
    </TD>
  </TR>
  <TR >
    <TD CLASS="strcol" COLSPAN="3" >
      18. How many days in the past month have you experienced:
    </TD>
  </TR>
  <TR >
    <TD CLASS="strcol" WIDTH="5%" >&nbsp;</TD>
    <TD CLASS="strcol" COLSPAN="2" >
      Alcohol problems
      <INPUT TYPE="text" NAME="ClientTASI_D18A_1" VALUE="<<ClientTASI_D18A_1>>" ONFOCUS="select()" ONCHANGE="return vNum(this,0,30);" SIZE=2>
    </TD>
  </TR>
  <TR >
    <TD CLASS="strcol" WIDTH="5%" >&nbsp;</TD>
    <TD CLASS="strcol" COLSPAN="2" >
      Drug problems
      <INPUT TYPE="text" NAME="ClientTASI_D18D_1" VALUE="<<ClientTASI_D18D_1>>" ONFOCUS="select()" ONCHANGE="return vNum(this,0,30);" SIZE=2>
    </TD>
  </TR>
  <TR >
    <TD CLASS="strcol" COLSPAN="3" >
      COMMENTS
      <TEXTAREA NAME="ClientTASI_D18COM_1" COLS=90 ROWS=8 WRAP=virtual ><<ClientTASI_D18COM_1>></TEXTAREA>
    </TD>
  </TR>
    </TABLE></TD></TR>
</TABLE>
<TABLE CLASS="home fullsize" >
  <TR ><TD CLASS="port hdrtxt" >Page 7<BR>Chemical (Substance) Use (cont.)</TD></TR>
    <TR ><TD ><TABLE CLASS="home fullsize" >
  <TR ><TD CLASS="port hdrtxt" COLSPAN="3" >USE THE PATIENT'S RATING SCALE FOR 19 & 20</TD></TR>
  <TR >
    <TD CLASS="strcol" COLSPAN="3" >
      19. How troubled or bothered have you been in the past month by:
    </TD>
  </TR>
  <TR >
    <TD CLASS="strcol" WIDTH="5%" >&nbsp;</TD>
    <TD CLASS="strcol" >Alcohol problems</TD>
    <TD CLASS="strcol" >
      <SELECT NAME="ClientTASI_D19A_1">
        [[DBA->selxTable(%form+xRateScale+<<ClientTASI_D19A_1>>+ID Descr)]]
      </SELECT> 
    </TD>
  </TR>
  <TR >
    <TD CLASS="strcol" WIDTH="5%" >&nbsp;</TD>
    <TD CLASS="strcol" >Drug problems</TD>
    <TD CLASS="strcol" >
      <SELECT NAME="ClientTASI_D19D_1">
        [[DBA->selxTable(%form+xRateScale+<<ClientTASI_D19D_1>>+ID Descr)]]
      </SELECT> 
    </TD>
  </TR>
  <TR >
    <TD CLASS="strcol" COLSPAN="3" >
      20. How important to you now is treatment for:
    </TD>
  </TR>
  <TR >
    <TD CLASS="strcol" WIDTH="5%" >&nbsp;</TD>
    <TD CLASS="strcol" >Alcohol problems</TD>
    <TD CLASS="strcol" >
      <SELECT NAME="ClientTASI_D20A_1">
        [[DBA->selxTable(%form+xRateScale+<<ClientTASI_D20A_1>>+ID Descr)]]
      </SELECT> 
    </TD>
  </TR>
  <TR >
    <TD CLASS="strcol" WIDTH="5%" >&nbsp;</TD>
    <TD CLASS="strcol" >Drug problems</TD>
    <TD CLASS="strcol" >
      <SELECT NAME="ClientTASI_D20D_1">
        [[DBA->selxTable(%form+xRateScale+<<ClientTASI_D20D_1>>+ID Descr)]]
      </SELECT> 
    </TD>
  </TR>
  <TR ><TD CLASS="port hdrtxt" COLSPAN="3" >INTERVIEWER SEVERITY RATING</TD></TR>
  <TR >
    <TD CLASS="strcol" COLSPAN="3" >
      21. How would you rate the patient's need for treatment for:
    </TD>
  </TR>
  <TR >
    <TD CLASS="strcol" WIDTH="5%" >&nbsp;</TD>
    <TD CLASS="strcol" >Alcohol abuse or dependence</TD>
    <TD CLASS="strcol" >
      <SELECT NAME="ClientTASI_D21A_1">
        [[DBA->selxTable(%form+xRateScale+<<ClientTASI_D21A_1>>+ID Descr)]]
      </SELECT> 
    </TD>
  </TR>
  <TR >
    <TD CLASS="strcol" WIDTH="5%" >&nbsp;</TD>
    <TD CLASS="strcol" >Drug abuse or dependence</TD>
    <TD CLASS="strcol" >
      <SELECT NAME="ClientTASI_D21D_1">
        [[DBA->selxTable(%form+xRateScale+<<ClientTASI_D21D_1>>+ID Descr)]]
      </SELECT> 
    </TD>
  </TR>
  <TR ><TD CLASS="port hdrtxt" COLSPAN="3" >CONFIDENCE RATING</TD></TR>
  <TR ><TD CLASS="strcol" COLSPAN="3" >Is the above information significantly distorted by:</TD></TR>
  <TR >
    <TD CLASS="strcol" WIDTH="5%" >&nbsp;</TD>
    <TD CLASS="strcol" COLSPAN="2" >
      22. Patient's misrepresentation?
      <INPUT TYPE="radio" NAME="ClientTASI_D22_1" VALUE="y" <<ClientTASI_D22_1=y>> > Yes
      <INPUT TYPE="radio" NAME="ClientTASI_D22_1" VALUE="n" <<ClientTASI_D22_1=n>> > No
    </TD>
  </TR>
  <TR >
    <TD CLASS="strcol" WIDTH="5%" >&nbsp;</TD>
    <TD CLASS="strcol" COLSPAN="2" >
      23. Patient's inability to understand?
      <INPUT TYPE="radio" NAME="ClientTASI_D23_1" VALUE="y" <<ClientTASI_D23_1=y>> > Yes
      <INPUT TYPE="radio" NAME="ClientTASI_D23_1" VALUE="n" <<ClientTASI_D23_1=n>> > No
    </TD>
  </TR>
  <TR >
    <TD CLASS="strcol" COLSPAN="3" >
      COMMENTS
      <TEXTAREA NAME="ClientTASI_D23COM_1" COLS=90 ROWS=8 WRAP=virtual ><<ClientTASI_D23COM_1>></TEXTAREA>
    </TD>
  </TR>
    </TABLE></TD></TR>
</TABLE>
<TABLE CLASS="home fullsize" >
  <TR ><TD CLASS="port hdrtxt" >Page 8<BR>School Status</TD></TR>
    <TR ><TD ><TABLE CLASS="home fullsize" >
  <TR >
    <TD CLASS="strcol" >
      1. Are you in school?
      <INPUT TYPE="radio" NAME="ClientTASI_S1_1" VALUE="y" <<ClientTASI_S1_1=y>> > Yes
      <INPUT TYPE="radio" NAME="ClientTASI_S1_1" VALUE="n" <<ClientTASI_S1_1=n>> > No
    </TD>
  </TR>
  <TR >
    <TD CLASS="strcol" >
      2. School days missed in the last month. 
      <INPUT TYPE="text" NAME="ClientTASI_S2_1" VALUE="<<ClientTASI_S2_1>>" ONFOCUS="select()" ONCHANGE="return vNum(this,0,30);" SIZE=2>
    </TD>
  </TR>
  <TR >
    <TD CLASS="strcol" >
      3. Missed in the last three months. 
      <INPUT TYPE="text" NAME="ClientTASI_S3_1" VALUE="<<ClientTASI_S3_1>>" ONFOCUS="select()" ONCHANGE="return vNum(this,0,30);" SIZE=2>
    </TD>
  </TR>
  <TR >
    <TD CLASS="strcol" >
      4. School days late in the last month. 
      <INPUT TYPE="text" NAME="ClientTASI_S4_1" VALUE="<<ClientTASI_S4_1>>" ONFOCUS="select()" ONCHANGE="return vNum(this,0,30);" SIZE=2>
    </TD>
  </TR>
  <TR >
    <TD CLASS="strcol" >
      5. Late in the last three months. 
      <INPUT TYPE="text" NAME="ClientTASI_S5_1" VALUE="<<ClientTASI_S5_1>>" ONFOCUS="select()" ONCHANGE="return vNum(this,0,30);" SIZE=2>
    </TD>
  </TR>
  <TR >
    <TD CLASS="strcol" >
      6. School days spent in detention or any other measures taken for disciplinary reasonslast month. (Principal's or school counselor's office.) 
      <INPUT TYPE="text" NAME="ClientTASI_S6_1" VALUE="<<ClientTASI_S6_1>>" ONFOCUS="select()" ONCHANGE="return vNum(this,0,30);" SIZE=2>
    </TD>
  </TR>
  <TR >
    <TD CLASS="strcol" >
      7. In the last three months. 
      <INPUT TYPE="text" NAME="ClientTASI_S7_1" VALUE="<<ClientTASI_S7_1>>" ONFOCUS="select()" ONCHANGE="return vNum(this,0,30);" SIZE=2>
    </TD>
  </TR>
  <TR >
    <TD CLASS="strcol" >
      8. School days suspended in the last month. 
      <INPUT TYPE="text" NAME="ClientTASI_S8_1" VALUE="<<ClientTASI_S8_1>>" ONFOCUS="select()" ONCHANGE="return vNum(this,0,30);" SIZE=2>
    </TD>
  </TR>
  <TR >
    <TD CLASS="strcol" >
      9. In the last three months. 
      <INPUT TYPE="text" NAME="ClientTASI_S9_1" VALUE="<<ClientTASI_S9_1>>" ONFOCUS="select()" ONCHANGE="return vNum(this,0,30);" SIZE=2>
    </TD>
  </TR>
  <TR >
    <TD CLASS="strcol" >
      10. School days you skipped classes in the last month. 
      <INPUT TYPE="text" NAME="ClientTASI_S10_1" VALUE="<<ClientTASI_S10_1>>" ONFOCUS="select()" ONCHANGE="return vNum(this,0,30);" SIZE=2>
    </TD>
  </TR>
  <TR >
    <TD CLASS="strcol" >
      11. In the last three months. 
      <INPUT TYPE="text" NAME="ClientTASI_S11_1" VALUE="<<ClientTASI_S11_1>>" ONFOCUS="select()" ONCHANGE="return vNum(this,0,30);" SIZE=2>
    </TD>
  </TR>
  <TR >
    <TD CLASS="strcol" >
      12. Grade average last report card.
      <INPUT TYPE="text" NAME="ClientTASI_S12_1" VALUE="<<ClientTASI_S12_1>>" ONFOCUS="select()" ONCHANGE="return vNum(this,0,30);" SIZE=2>
    </TD>
  </TR>
  <TR >
    <TD CLASS="strcol" >
      13. Grade average last year. 
      <INPUT TYPE="text" NAME="ClientTASI_S13_1" VALUE="<<ClientTASI_S13_1>>" ONFOCUS="select()" ONCHANGE="return vNum(this,0,30);" SIZE=2>
    </TD>
  </TR>
  <TR >
    <TD CLASS="strcol" >
      14. Have you participated in any extracurricular activity during the past month? 
      <INPUT TYPE="radio" NAME="ClientTASI_S14_1" VALUE="y" <<ClientTASI_S14_1=y>> > Yes
      <INPUT TYPE="radio" NAME="ClientTASI_S14_1" VALUE="n" <<ClientTASI_S14_1=n>> > No
    </TD>
  </TR>
  <TR >
    <TD CLASS="strcol" >
      15. Have you attended any extracurricular activity during the past month? 
      <INPUT TYPE="radio" NAME="ClientTASI_S15_1" VALUE="y" <<ClientTASI_S15_1=y>> > Yes
      <INPUT TYPE="radio" NAME="ClientTASI_S15_1" VALUE="n" <<ClientTASI_S15_1=n>> > No
    </TD>
  </TR>
  <TR >
    <TD CLASS="strcol" >
      COMMENTS
      <TEXTAREA NAME="ClientTASI_S15COM_1" COLS=90 ROWS=8 WRAP=virtual ><<ClientTASI_S15COM_1>></TEXTAREA>
    </TD>
  </TR>
    </TABLE></TD></TR>
</TABLE>
<TABLE CLASS="home fullsize" >
  <TR ><TD CLASS="port hdrtxt" >Page 9<BR>School Status (cont.)</TD></TR>
    <TR ><TD ><TABLE CLASS="home fullsize" >
  <TR ><TD CLASS="port hdrtxt" COLSPAN="3" >USE THE PATIENT'S RATING SCALE FOR 16 & 17</TD></TR>
  <TR >
    <TD CLASS="strcol" COLSPAN="2" >
      16. How troubled or bothered have you been by these school problems in the past month?
    </TD>
    <TD CLASS="strcol" >
      <SELECT NAME="ClientTASI_S16_1">
        [[DBA->selxTable(%form+xRateScale+<<ClientTASI_S16_1>>+ID Descr)]]
      </SELECT> 
    </TD>
  </TR>
  <TR >
    <TD CLASS="strcol" COLSPAN="2" >
      17. How important to you now is counseling for these school problems? 
    </TD>
    <TD CLASS="strcol" >
      <SELECT NAME="ClientTASI_S17_1">
        [[DBA->selxTable(%form+xRateScale+<<ClientTASI_S17_1>>+ID Descr)]]
      </SELECT> 
    </TD>
  </TR>
  <TR ><TD CLASS="port hdrtxt" COLSPAN="3" >INTERVIEWER SEVERITY RATING</TD></TR>
  <TR >
    <TD CLASS="strcol" COLSPAN="2" >
      18. How would you rate the need for school counseling?
    </TD>
    <TD CLASS="strcol" >
      <SELECT NAME="ClientTASI_S18_1">
        [[DBA->selxTable(%form+xRateScale+<<ClientTASI_S18_1>>+ID Descr)]]
      </SELECT> 
    </TD>
  </TR>
  <TR ><TD CLASS="port hdrtxt" COLSPAN="3" >CONFIDENCE RATING</TD></TR>
  <TR ><TD CLASS="strcol" COLSPAN="3" >Is the above information significantly distorted by:</TD></TR>
  <TR >
    <TD CLASS="strcol" WIDTH="5%" >&nbsp;</TD>
    <TD CLASS="strcol" COLSPAN="2" >
      19. Patient's misrepresentation?
      <INPUT TYPE="radio" NAME="ClientTASI_S19_1" VALUE="y" <<ClientTASI_S19_1=y>> > Yes
      <INPUT TYPE="radio" NAME="ClientTASI_S19_1" VALUE="n" <<ClientTASI_S19_1=n>> > No
    </TD>
  </TR>
  <TR >
    <TD CLASS="strcol" WIDTH="5%" >&nbsp;</TD>
    <TD CLASS="strcol" COLSPAN="2" >
      20. Patient's ability to understand?
      <INPUT TYPE="radio" NAME="ClientTASI_S20_1" VALUE="y" <<ClientTASI_S20_1=y>> > Yes
      <INPUT TYPE="radio" NAME="ClientTASI_S20_1" VALUE="n" <<ClientTASI_S20_1=n>> > No
    </TD>
  </TR>
  <TR >
    <TD CLASS="strcol" COLSPAN="3" >
      COMMENTS
      <TEXTAREA NAME="ClientTASI_S20COM_1" COLS=90 ROWS=8 WRAP=virtual ><<ClientTASI_S20COM_1>></TEXTAREA>
    </TD>
    </TABLE></TD></TR>
</TABLE>
<TABLE CLASS="home fullsize" >
  <TR ><TD CLASS="port hdrtxt" >Page 10<BR>Employment/Support Status</TD></TR>
    <TR ><TD ><TABLE CLASS="home fullsize" >
  <TR >
    <TD CLASS="strcol" >
      1. Education completed. (yrs/mos)
    </TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="text" NAME="ClientTASI_E1_1" VALUE="<<ClientTASI_E1_1>>" ONFOCUS="select()" SIZE=5 ONCHANGE="return vAge(this)" >
    </TD>
  </TR>
  <TR >
    <TD CLASS="strcol" >
      2. If you are not in school, when did you leave? (yrs/mos)
    </TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="text" NAME="ClientTASI_E2_1" VALUE="<<ClientTASI_E2_1>>" ONFOCUS="select()" SIZE=5 ONCHANGE="return vAge(this)" >
    </TD>
  </TR>
  <TR >
    <TD CLASS="strcol" >
      3. Training or technical education completed. (yrs/mos)
    </TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="text" NAME="ClientTASI_E3_1" VALUE="<<ClientTASI_E3_1>>" ONFOCUS="select()" SIZE=5 ONCHANGE="return vAge(this)" >
    </TD>
  </TR>
  <TR >
    <TD CLASS="strcol" >
      4. Do you have a profession, trade, or skill? 
    </TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="radio" NAME="ClientTASI_E4_1" VALUE="y" <<ClientTASI_E4_1=y>> > Yes
      <INPUT TYPE="radio" NAME="ClientTASI_E4_1" VALUE="n" <<ClientTASI_E4_1=n>> > No
    </TD>
  </TR>
  <TR >
    <TD CLASS="strcol" COLSPAN="2" >
      Specify
      <INPUT TYPE="text" NAME="ClientTASI_E4S_1" VALUE="<<ClientTASI_E4S_1>>" ONFOCUS="select()" SIZE=60>
    </TD>
  </TR>
  <TR >
    <TD CLASS="strcol" COLSPAN="2" >
      Key for 5 & 6:<BR>
      1=full-time worker (40 hrs./week) or student<BR>
      2=part-time worker (reg. hrs.) or student<BR>
      3=part-time (irreg. hrs.)<BR>
      4=unemployed
    </TD>
  </TR>
  <TR >
    <TD CLASS="strcol" >
      5. Usual employment pattern during the past month. 
    </TD>
    <TD CLASS="strcol" >
      <SELECT NAME="ClientTASI_E5_1">
        [[DBA->selxTable(%form+xEmplStat+<<ClientTASI_E5_1>>+Descr)]]
      </SELECT> 
    </TD>
  </TR>
  <TR >
    <TD CLASS="strcol" >
      6. During the past three months.
    </TD>
    <TD CLASS="strcol" >
      <SELECT NAME="ClientTASI_E6_1">
        [[DBA->selxTable(%form+xEmplStat+<<ClientTASI_E6_1>>+Descr)]]
      </SELECT> 
    </TD>
  <TR >
    <TD CLASS="strcol" >
      7. How long was your longest period of employment during the past year? 
    </TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="text" NAME="ClientTASI_E7_1" VALUE="<<ClientTASI_E7_1>>" ONFOCUS="select()" ONCHANGE="return vNum(this,0,30);" SIZE=2>
    </TD>
  </TR>
  <TR >
    <TD CLASS="strcol" >
      8. How many days were you paid for working during the past month? 
    </TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="text" NAME="ClientTASI_E8_1" VALUE="<<ClientTASI_E8_1>>" ONFOCUS="select()" ONCHANGE="return vNum(this,0,30);" SIZE=2>
    </TD>
  </TR>
  <TR >
    <TD CLASS="strcol" >
      9. During the past three months? 
    </TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="text" NAME="ClientTASI_E9_1" VALUE="<<ClientTASI_E9_1>>" ONFOCUS="select()" ONCHANGE="return vNum(this,0,30);" SIZE=2>
    </TD>
  </TR>
  <TR >
    <TD CLASS="strcol" >
      10. How many days were you late for work during the past month? 
    </TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="text" NAME="ClientTASI_E10_1" VALUE="<<ClientTASI_E10_1>>" ONFOCUS="select()" ONCHANGE="return vNum(this,0,30);" SIZE=2>
    </TD>
  </TR>
  <TR >
    <TD CLASS="strcol" >
      11. During the past three months?
    </TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="text" NAME="ClientTASI_E11_1" VALUE="<<ClientTASI_E11_1>>" ONFOCUS="select()" ONCHANGE="return vNum(this,0,30);" SIZE=2>
    </TD>
  </TR>
  <TR >
    <TD CLASS="strcol" COLSPAN="2" >
      COMMENTS
      <TEXTAREA NAME="ClientTASI_E11COM_1" COLS=90 ROWS=8 WRAP=virtual ><<ClientTASI_E11COM_1>></TEXTAREA>
    </TD>
  </TR>
    </TABLE></TD></TR>
</TABLE>
<TABLE CLASS="home fullsize" >
  <TR ><TD CLASS="port hdrtxt" >Page 11<BR>Employment/Support Status (cont.)</TD></TR>
    <TR ><TD ><TABLE CLASS="home fullsize" >
  <TR >
    <TD CLASS="strcol" >
      12. How many days did you miss work during the past month? 
    </TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="text" NAME="ClientTASI_E12_1" VALUE="<<ClientTASI_E12_1>>" ONFOCUS="select()" ONCHANGE="return vNum(this,0,30);" SIZE=2>
    </TD>
  </TR>
  <TR >
    <TD CLASS="strcol" >
      13. During the past three months?
    </TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="text" NAME="ClientTASI_E13_1" VALUE="<<ClientTASI_E13_1>>" ONFOCUS="select()" ONCHANGE="return vNum(this,0,30);" SIZE=2>
    </TD>
  </TR>
  <TR >
    <TD CLASS="strcol" >
      14. How many days did you miss work due to being sick during the past month?
    </TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="text" NAME="ClientTASI_E14_1" VALUE="<<ClientTASI_E14_1>>" ONFOCUS="select()" ONCHANGE="return vNum(this,0,30);" SIZE=2>
    </TD>
  </TR>
  <TR >
    <TD CLASS="strcol" >
      15. During the past three months?
    </TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="text" NAME="ClientTASI_E15_1" VALUE="<<ClientTASI_E15_1>>" ONFOCUS="select()" ONCHANGE="return vNum(this,0,30);" SIZE=2>
    </TD>
  </TR>
  <TR >
    <TD CLASS="strcol" >
      16. How many times were you fired from a job during the past month?
    </TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="text" NAME="ClientTASI_E16_1" VALUE="<<ClientTASI_E16_1>>" ONFOCUS="select()" ONCHANGE="return vNum(this,0,30);" SIZE=2>
    </TD>
  </TR>
  <TR >
    <TD CLASS="strcol" >
      17. During the past year?
    </TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="text" NAME="ClientTASI_E17_1" VALUE="<<ClientTASI_E17_1>>" ONFOCUS="select()" ONCHANGE="return vNum(this,0,30);" SIZE=2>
    </TD>
  </TR>
  <TR >
    <TD CLASS="strcol" >
      18. How many times were you laid off during the past month?
    </TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="text" NAME="ClientTASI_E18_1" VALUE="<<ClientTASI_E18_1>>" ONFOCUS="select()" ONCHANGE="return vNum(this,0,30);" SIZE=2>
    </TD>
  </TR>
  <TR >
    <TD CLASS="strcol" >
      19. During the past three months? 
    </TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="text" NAME="ClientTASI_E19_1" VALUE="<<ClientTASI_E19_1>>" ONFOCUS="select()" ONCHANGE="return vNum(this,0,30);" SIZE=2>
    </TD>
  </TR>
  <TR ><TD CLASS="port hdrtxt" COLSPAN="2" >USE THE PATIENT'S RATING SCALE FOR 20 & 21</TD></TR>
  </TR>
  <TR >
    <TD CLASS="strcol" >
      20. How satisfied were you with your job performance during the past month?
    </TD>
    <TD CLASS="strcol" >
      <SELECT NAME="ClientTASI_E20_1">
        [[DBA->selxTable(%form+xRateScale+<<ClientTASI_E20_1>>+ID Descr)]]
      </SELECT> 
    </TD>
  </TR>
  <TR >
    <TD CLASS="strcol" >
      21. During the past year?
    </TD>
    <TD CLASS="strcol" >
      <SELECT NAME="ClientTASI_E21_1">
        [[DBA->selxTable(%form+xRateScale+<<ClientTASI_E21_1>>+ID Descr)]]
      </SELECT> 
    </TD>
  <TR >
    <TD CLASS="strcol" >
      22. If unemployed, how many days were you looking for a job during the past month?
    </TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="text" NAME="ClientTASI_E22_1" VALUE="<<ClientTASI_E22_1>>" ONFOCUS="select()" ONCHANGE="return vNum(this,0,30);" SIZE=2>
    </TD>
  </TR>
  <TR >
    <TD CLASS="strcol" >
      23. During the past three months?
    </TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="text" NAME="ClientTASI_E23_1" VALUE="<<ClientTASI_E23_1>>" ONFOCUS="select()" ONCHANGE="return vNum(this,0,30);" SIZE=2>
    </TD>
  </TR>
  <TR >
    <TD CLASS="strcol" >
      24. How many days have you experienced employment or job problems during thepast month?
    </TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="text" NAME="ClientTASI_E24_1" VALUE="<<ClientTASI_E24_1>>" ONFOCUS="select()" ONCHANGE="return vNum(this,0,30);" SIZE=2>
    </TD>
  </TR>
  <TR >
    <TD CLASS="strcol" >
      25. During the past three months?
    </TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="text" NAME="ClientTASI_E25_1" VALUE="<<ClientTASI_E25_1>>" ONFOCUS="select()" ONCHANGE="return vNum(this,0,30);" SIZE=2>
    </TD>
  </TR>
  <TR >
    <TD CLASS="strcol" >
      26. Does someone or a government agency contribute to your support in any ways?
    </TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="radio" NAME="ClientTASI_E26_1" VALUE="y" <<ClientTASI_E26_1=y>> > Yes
      <INPUT TYPE="radio" NAME="ClientTASI_E26_1" VALUE="n" <<ClientTASI_E26_1=n>> > No
    </TD>
  </TR>
  <TR >
    <TD CLASS="strcol" >
      27. If yes, does this source provide a majority of your support? 
    </TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="radio" NAME="ClientTASI_E27_1" VALUE="y" <<ClientTASI_E27_1=y>> > Yes
      <INPUT TYPE="radio" NAME="ClientTASI_E27_1" VALUE="n" <<ClientTASI_E27_1=n>> > No
    </TD>
  </TR>
  <TR >
    <TD CLASS="strcol" COLSPAN="2" >
      COMMENTS
      <TEXTAREA NAME="ClientTASI_E27COM_1" COLS=90 ROWS=8 WRAP=virtual ><<ClientTASI_E27COM_1>></TEXTAREA>
    </TD>
  </TR>
    </TABLE></TD></TR>
</TABLE>
<TABLE CLASS="home fullsize" >
  <TR ><TD CLASS="port hdrtxt" >Page 12<BR>Employment/Support Status (cont.)</TD></TR>
    <TR ><TD ><TABLE CLASS="home fullsize" >
  <TR >
    <TD CLASS="strcol" COLSPAN="2" >
      28. What percentage of your income is generated by illegal activity?
    </TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="text" NAME="ClientTASI_E28_1" VALUE="<<ClientTASI_E28_1>>" ONFOCUS="select()" ONCHANGE="return vNum(this,0,100);" SIZE=3>
    </TD>
  </TR>
  <TR >
    <TD CLASS="strcol" COLSPAN="2" >
      29. How many people depend on you for the majority of their food, shelter, etc.?
    </TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="text" NAME="ClientTASI_E29_1" VALUE="<<ClientTASI_E29_1>>" ONFOCUS="select()" ONCHANGE="return vNum(this,0,30);" SIZE=2>
    </TD>
  </TR>
  <TR ><TD CLASS="port hdrtxt" COLSPAN="3" >USE THE PATIENT'S RATING SCALE FOR 30 & 31</TD></TR>
  <TR >
    <TD CLASS="strcol" COLSPAN="2" >
      30. How troubled or bothered have you been by any unemployment problems in thepast month?
    </TD>
    <TD CLASS="strcol" >
      <SELECT NAME="ClientTASI_E30_1">
        [[DBA->selxTable(%form+xRateScale+<<ClientTASI_E30_1>>+ID Descr)]]
      </SELECT> 
    </TD>
  </TR>
  <TR >
    <TD CLASS="strcol" COLSPAN="2" >
      31. How important to you now is counseling for these job problems? 
    </TD>
    <TD CLASS="strcol" >
      <SELECT NAME="ClientTASI_E31_1">
        [[DBA->selxTable(%form+xRateScale+<<ClientTASI_E31_1>>+ID Descr)]]
      </SELECT> 
    </TD>
  </TR>
  <TR ><TD CLASS="port hdrtxt" COLSPAN="3" >INTERVIEWER SEVERITY RATING</TD></TR>
  <TR >
    <TD CLASS="strcol" COLSPAN="2" >
      32. How would you rate the patient's need for employment counseling?
    </TD>
    <TD CLASS="strcol" >
      <SELECT NAME="ClientTASI_E32_1">
        [[DBA->selxTable(%form+xRateScale+<<ClientTASI_E32_1>>+ID Descr)]]
      </SELECT> 
    </TD>
  </TR>
  <TR ><TD CLASS="port hdrtxt" COLSPAN="3" >CONFIDENCE RATING</TD></TR>
  <TR ><TD CLASS="strcol" COLSPAN="3" >Is the above information significantly distorted by:</TD></TR>
  <TR >
    <TD CLASS="strcol" WIDTH="5%" >&nbsp;</TD>
    <TD CLASS="strcol" COLSPAN="2" >
      33. Patient's misrepresentation?
      <INPUT TYPE="radio" NAME="ClientTASI_E33_1" VALUE="y" <<ClientTASI_E33_1=y>> > Yes
      <INPUT TYPE="radio" NAME="ClientTASI_E33_1" VALUE="n" <<ClientTASI_E33_1=n>> > No
    </TD>
  </TR>
  <TR >
    <TD CLASS="strcol" WIDTH="5%" >&nbsp;</TD>
    <TD CLASS="strcol" COLSPAN="2" >
      34. Patient's ability to understand?
      <INPUT TYPE="radio" NAME="ClientTASI_E34_1" VALUE="y" <<ClientTASI_E34_1=y>> > Yes
      <INPUT TYPE="radio" NAME="ClientTASI_E34_1" VALUE="n" <<ClientTASI_E34_1=n>> > No
    </TD>
  </TR>
  <TR >
    <TD CLASS="strcol" COLSPAN="3" >
      COMMENTS
      <TEXTAREA NAME="ClientTASI_E34COM_1" COLS=90 ROWS=8 WRAP=virtual ><<ClientTASI_E34COM_1>></TEXTAREA>
    </TD>
  </TR>
    </TABLE></TD></TR>
</TABLE>
<TABLE CLASS="home fullsize" >
  <TR ><TD CLASS="port hdrtxt" >Page 13<BR>Family Relations</TD></TR>
    <TR ><TD ><TABLE CLASS="home fullsize" >
  <TR >
    <TD CLASS="strcol" COLSPAN="2" >
      1. What are your current living arrangements?
    </TD>
    <TD CLASS="strcol" >
      <SELECT NAME="ClientTASI_F1_1">
        [[DBA->selxTable(%form+xLivingArrTASI+<<ClientTASI_F1_1>>+ID Descr)]]
      </SELECT> 
    </TD>
  </TR>
  <TR >
    <TD CLASS="strcol" COLSPAN="2" >
      2. How long have you lived in these arrangements?
    </TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="text" NAME="ClientTASI_F2_1" VALUE="<<ClientTASI_F2_1>>" ONFOCUS="select()" ONCHANGE="return vNum(this,0,30);" SIZE=2>
    </TD>
  </TR>
  <TR >
    <TD CLASS="strcol" COLSPAN="2" >
      3. Are you satisfied with these arrangements?
    </TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="radio" NAME="ClientTASI_F3_1" VALUE="y" <<ClientTASI_F3_1=y>> > Yes
      <INPUT TYPE="radio" NAME="ClientTASI_F3_1" VALUE="n" <<ClientTASI_F3_1=n>> > No
    </TD>
  </TR>
  <TR >
    <TD CLASS="strcol" COLSPAN="3" >
      4. Have you experienced serious conflicts or problems with:
    </TD>
  </TR>
  <TR >
    <TD CLASS="strcol" WIDTH="5%" >&nbsp;</TD>
    <TD CLASS="strcol" >
      Mother
    </TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="radio" NAME="ClientTASI_F4M_1" VALUE="y" <<ClientTASI_F4M_1=y>> > Yes
      <INPUT TYPE="radio" NAME="ClientTASI_F4M_1" VALUE="n" <<ClientTASI_F4M_1=n>> > No
    </TD>
  </TR>
  <TR >
    <TD CLASS="strcol" WIDTH="5%" >&nbsp;</TD>
    <TD CLASS="strcol" >
      Father
    </TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="radio" NAME="ClientTASI_F4F_1" VALUE="y" <<ClientTASI_F4F_1=y>> > Yes
      <INPUT TYPE="radio" NAME="ClientTASI_F4F_1" VALUE="n" <<ClientTASI_F4F_1=n>> > No
    </TD>
  </TR>
  <TR >
    <TD CLASS="strcol" WIDTH="5%" >&nbsp;</TD>
    <TD CLASS="strcol" >
      Siblings
    </TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="radio" NAME="ClientTASI_F4S_1" VALUE="y" <<ClientTASI_F4S_1=y>> > Yes
      <INPUT TYPE="radio" NAME="ClientTASI_F4S_1" VALUE="n" <<ClientTASI_F4S_1=n>> > No
    </TD>
  </TR>
  <TR >
    <TD CLASS="strcol" WIDTH="5%" >&nbsp;</TD>
    <TD CLASS="strcol" >
      Other family members
    </TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="radio" NAME="ClientTASI_F4O_1" VALUE="y" <<ClientTASI_F4O_1=y>> > Yes
      <INPUT TYPE="radio" NAME="ClientTASI_F4O_1" VALUE="n" <<ClientTASI_F4O_1=n>> > No
    </TD>
  </TR>
  <TR >
    <TD CLASS="strcol" WIDTH="5%" >&nbsp;</TD>
    <TD CLASS="strcol" >
      Caretaker
    </TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="radio" NAME="ClientTASI_F4C_1" VALUE="y" <<ClientTASI_F4C_1=y>> > Yes
      <INPUT TYPE="radio" NAME="ClientTASI_F4C_1" VALUE="n" <<ClientTASI_F4C_1=n>> > No
    </TD>
  </TR>
  <TR >
    <TD CLASS="strcol" COLSPAN="2" >
      5a. How many days in the past month?
    </TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="text" NAME="ClientTASI_F5a_1" VALUE="<<ClientTASI_F5a_1>>" ONFOCUS="select()" ONCHANGE="return vNum(this,0,30);" SIZE=2>
    </TD>
  </TR>
  <TR >
    <TD CLASS="strcol" COLSPAN="2" >
      5b. How many days in the past three months?
    </TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="text" NAME="ClientTASI_F5b_1" VALUE="<<ClientTASI_F5b_1>>" ONFOCUS="select()" ONCHANGE="return vNum(this,0,30);" SIZE=2>
    </TD>
  </TR>
  <TR ><TD CLASS="port hdrtxt" COLSPAN="3" >USE THE PATIENT'S RATING SCALE FOR 6-11</TD></TR>
  <TR >
    <TD CLASS="strcol" COLSPAN="2" >
      6. How much do members of your family support and/or help one another?
    </TD>
    <TD CLASS="strcol" >
      <SELECT NAME="ClientTASI_F6_1">
        [[DBA->selxTable(%form+xRateScale+<<ClientTASI_F6_1>>+ID Descr)]]
      </SELECT> 
    </TD>
  </TR>
  <TR >
    <TD CLASS="strcol" COLSPAN="2" >
      7. How often do members of your family fight and/or have conflicts with one another?
    </TD>
    <TD CLASS="strcol" >
      <SELECT NAME="ClientTASI_F7_1">
        [[DBA->selxTable(%form+xRateScale+<<ClientTASI_F7_1>>+ID Descr)]]
      </SELECT> 
    </TD>
  </TR>
  <TR >
    <TD CLASS="strcol" COLSPAN="2" >
      8. How often do members of your family participate in activities together?
    </TD>
    <TD CLASS="strcol" >
      <SELECT NAME="ClientTASI_F8_1">
        [[DBA->selxTable(%form+xRateScale+<<ClientTASI_F8_1>>+ID Descr)]]
      </SELECT> 
    </TD>
  </TR>
  <TR >
    <TD CLASS="strcol" COLSPAN="2" >
      9. How much are rules enforced in your house?
    </TD>
    <TD CLASS="strcol" >
      <SELECT NAME="ClientTASI_F9_1">
        [[DBA->selxTable(%form+xRateScale+<<ClientTASI_F9_1>>+ID Descr)]]
      </SELECT> 
    </TD>
  </TR>
  <TR >
    <TD CLASS="strcol" COLSPAN="2" >
      10. How much are you able to confide in your parents/caretaker?
    </TD>
    <TD CLASS="strcol" >
      <SELECT NAME="ClientTASI_F10_1">
        [[DBA->selxTable(%form+xRateScale+<<ClientTASI_F10_1>>+ID Descr)]]
      </SELECT> 
    </TD>
  </TR>
  <TR >
    <TD CLASS="strcol" COLSPAN="2" >
      11. How much are you able to express yourself and be heard in your family?
    </TD>
    <TD CLASS="strcol" >
      <SELECT NAME="ClientTASI_F11_1">
        [[DBA->selxTable(%form+xRateScale+<<ClientTASI_F11_1>>+ID Descr)]]
      </SELECT> 
    </TD>
  </TR>
  <TR >
    <TD CLASS="strcol" COLSPAN="2" >
      COMMENTS
      <TEXTAREA NAME="ClientTASI_F11COM_1" COLS=90 ROWS=8 WRAP=virtual ><<ClientTASI_F11COM_1>></TEXTAREA>
    </TD>
  </TR>
    </TABLE></TD></TR>
</TABLE>
<TABLE CLASS="home fullsize" >
  <TR ><TD CLASS="port hdrtxt" >Page 14<BR>Family Relations (cont.)</TD></TR>
    <TR ><TD ><TABLE CLASS="home fullsize" >
  <TR >
    <TD CLASS="strcol" COLSPAN="2" >
      12. Have you been physically abused by any member of your family in the past month?
    </TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="radio" NAME="ClientTASI_F12_1" VALUE="y" <<ClientTASI_F12_1=y>> > Yes
      <INPUT TYPE="radio" NAME="ClientTASI_F12_1" VALUE="n" <<ClientTASI_F12_1=n>> > No
    </TD>
  </TR>
  <TR >
    <TD CLASS="strcol" COLSPAN="2" >
      13. In the past three months?
    </TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="radio" NAME="ClientTASI_F13_1" VALUE="y" <<ClientTASI_F13_1=y>> > Yes
      <INPUT TYPE="radio" NAME="ClientTASI_F13_1" VALUE="n" <<ClientTASI_F13_1=n>> > No
    </TD>
  </TR>
  <TR >
    <TD CLASS="strcol" COLSPAN="2" >
      14. Have you participated in sexual activity with any member of your family in the past month(excluding spouse)?
    </TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="radio" NAME="ClientTASI_F14_1" VALUE="y" <<ClientTASI_F14_1=y>> > Yes
      <INPUT TYPE="radio" NAME="ClientTASI_F14_1" VALUE="n" <<ClientTASI_F14_1=n>> > No
    </TD>
  </TR>
  <TR >
    <TD CLASS="strcol" COLSPAN="2" >
      15. In the past three months?
    </TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="radio" NAME="ClientTASI_F15_1" VALUE="y" <<ClientTASI_F15_1=y>> > Yes
      <INPUT TYPE="radio" NAME="ClientTASI_F15_1" VALUE="n" <<ClientTASI_F15_1=n>> > No
    </TD>
  </TR>
  <TR ><TD CLASS="port hdrtxt" COLSPAN="3" >USE THE PATIENT'S RATING SCALE FOR 16 & 17</TD></TR>
  <TR >
    <TD CLASS="strcol" COLSPAN="2" >
      16. How troubled or bothered have you been in the past month by family problems?
    </TD>
    <TD CLASS="strcol" >
      <SELECT NAME="ClientTASI_F16_1">
        [[DBA->selxTable(%form+xRateScale+<<ClientTASI_F16_1>>+ID Descr)]]
      </SELECT> 
    </TD>
  </TR>
  <TR >
    <TD CLASS="strcol" COLSPAN="2" >
      17. How important to you now is treatment or counseling for family problems?
    </TD>
    <TD CLASS="strcol" >
      <SELECT NAME="ClientTASI_F17_1">
        [[DBA->selxTable(%form+xRateScale+<<ClientTASI_F17_1>>+ID Descr)]]
      </SELECT> 
    </TD>
  </TR>
  <TR ><TD CLASS="port hdrtxt" COLSPAN="3" >INTERVIEWER SEVERITY RATING</TD></TR>
  <TR >
    <TD CLASS="strcol" COLSPAN="2" >
      18. How would you rate the patients need for family counseling?
    </TD>
    <TD CLASS="strcol" >
      <SELECT NAME="ClientTASI_F18_1">
        [[DBA->selxTable(%form+xRateScale+<<ClientTASI_F18_1>>+ID Descr)]]
      </SELECT> 
    </TD>
  </TR>
  <TR ><TD CLASS="port hdrtxt" COLSPAN="3" >CONFIDENCE RATING</TD></TR>
  <TR ><TD CLASS="strcol" COLSPAN="3" >Is the above information significantly distorted by:</TD></TR>
  <TR >
    <TD CLASS="strcol" WIDTH="5%" >&nbsp;</TD>
    <TD CLASS="strcol" COLSPAN="2" >
      19. Patient's misrepresentation?
      <INPUT TYPE="radio" NAME="ClientTASI_F19_1" VALUE="y" <<ClientTASI_F19_1=y>> > Yes
      <INPUT TYPE="radio" NAME="ClientTASI_F19_1" VALUE="n" <<ClientTASI_F19_1=n>> > No
    </TD>
  </TR>
  <TR >
    <TD CLASS="strcol" WIDTH="5%" >&nbsp;</TD>
    <TD CLASS="strcol" COLSPAN="2" >
      20. Patient's inability to understand?
      <INPUT TYPE="radio" NAME="ClientTASI_F20_1" VALUE="y" <<ClientTASI_F20_1=y>> > Yes
      <INPUT TYPE="radio" NAME="ClientTASI_F20_1" VALUE="n" <<ClientTASI_F20_1=n>> > No
    </TD>
  </TR>
  <TR >
    <TD CLASS="strcol" COLSPAN="3" >
      COMMENTS
      <TEXTAREA NAME="ClientTASI_F20COM_1" COLS=90 ROWS=8 WRAP=virtual ><<ClientTASI_F20COM_1>></TEXTAREA>
    </TD>
  </TR>
    </TABLE></TD></TR>
</TABLE>
<TABLE CLASS="home fullsize" >
  <TR ><TD CLASS="port hdrtxt" >Page 15<BR>Peer/Social Relationships</TD></TR>
    <TR ><TD ><TABLE CLASS="home fullsize" >
  <TR >
    <TD CLASS="strcol" COLSPAN="2" >
      1. How many close friends do you have?
    </TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="text" NAME="ClientTASI_R1_1" VALUE="<<ClientTASI_R1_1>>" ONFOCUS="select()" ONCHANGE="return vNum(this,0,30);" SIZE=2>
    </TD>
  </TR>
  <TR >
    <TD CLASS="strcol" COLSPAN="3" >
      2. How many close friends do you have that regularly use:
    </TD>
  </TR>
  <TR >
    <TD CLASS="strcol" WIDTH="5%" >&nbsp;</TD>
    <TD CLASS="strcol" >
      Alcohol?
    </TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="text" NAME="ClientTASI_R2A_1" VALUE="<<ClientTASI_R2A_1>>" ONFOCUS="select()" ONCHANGE="return vNum(this,0,30);" SIZE=2>
    </TD>
  </TR>
  <TR >
    <TD CLASS="strcol" WIDTH="5%" >&nbsp;</TD>
    <TD CLASS="strcol" >
      Marijuana?
    </TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="text" NAME="ClientTASI_R2M_1" VALUE="<<ClientTASI_R2M_1>>" ONFOCUS="select()" ONCHANGE="return vNum(this,0,30);" SIZE=2>
    </TD>
  </TR>
  <TR >
    <TD CLASS="strcol" WIDTH="5%" >&nbsp;</TD>
    <TD CLASS="strcol" >
      Cocaine?
    </TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="text" NAME="ClientTASI_R2C_1" VALUE="<<ClientTASI_R2C_1>>" ONFOCUS="select()" ONCHANGE="return vNum(this,0,30);" SIZE=2>
    </TD>
  </TR>
  <TR >
    <TD CLASS="strcol" WIDTH="5%" >&nbsp;</TD>
    <TD CLASS="strcol" >
      Other illicit drugs?
    </TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="text" NAME="ClientTASI_R2O_1" VALUE="<<ClientTASI_R2O_1>>" ONFOCUS="select()" ONCHANGE="return vNum(this,0,30);" SIZE=2>
    </TD>
  </TR>
  <TR >
    <TD CLASS="strcol" COLSPAN="2" >
      3. How many serious conflicts/arguments have you had with your friends in the past month (excludeyour boy/girlfriend)?
    </TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="text" NAME="ClientTASI_R3_1" VALUE="<<ClientTASI_R3_1>>" ONFOCUS="select()" ONCHANGE="return vNum(this,0,30);" SIZE=2>
    </TD>
  </TR>
  <TR >
    <TD CLASS="strcol" COLSPAN="2" >
      4. In the past three months?
    </TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="text" NAME="ClientTASI_R4_1" VALUE="<<ClientTASI_R4_1>>" ONFOCUS="select()" ONCHANGE="return vNum(this,0,30);" SIZE=2>
    </TD>
  </TR>
  <TR ><TD CLASS="port hdrtxt" COLSPAN="3" >USE THE PATIENT'S RATING SCALE FOR 5</TD></TR>
  <TR >
    <TD CLASS="strcol" COLSPAN="2" >
      5. How satisfied are you with the quality of these relationships with friends?
    </TD>
    <TD CLASS="strcol" >
      <SELECT NAME="ClientTASI_R5_1">
        [[DBA->selxTable(%form+xRateScale+<<ClientTASI_R5_1>>+ID Descr)]]
      </SELECT> 
    </TD>
  </TR>
  <TR >
    <TD CLASS="strcol" COLSPAN="3" >
      6. Do you have a boy/girlfriend?
      <INPUT TYPE="radio" NAME="ClientTASI_R6_1" VALUE="y" <<ClientTASI_R6_1=y>> > Yes
      <INPUT TYPE="radio" NAME="ClientTASI_R6_1" VALUE="n" <<ClientTASI_R6_1=n>> > No
    </TD>
  </TR>
  <TR >
    <TD CLASS="strcol" COLSPAN="2" >
      7. How many months has this person been your boy/girlfriend?
    </TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="text" NAME="ClientTASI_R7_1" VALUE="<<ClientTASI_R7_1>>" ONFOCUS="select()" ONCHANGE="return vNum(this,0,30);" SIZE=2>
    </TD>
  </TR>
  <TR >
    <TD CLASS="strcol" COLSPAN="2" >
      8. How many boy/girlfriends have you had in the past year?
    </TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="text" NAME="ClientTASI_R8_1" VALUE="<<ClientTASI_R8_1>>" ONFOCUS="select()" ONCHANGE="return vNum(this,0,30);" SIZE=2>
    </TD>
  </TR>
  <TR >
    <TD CLASS="strcol" COLSPAN="3" >
      9. Does you current boy/girlfriend regularly use:
    </TD>
  </TR>
  <TR >
    <TD CLASS="strcol" WIDTH="5%" >&nbsp;</TD>
    <TD CLASS="strcol" >
      Alcohol?
    </TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="text" NAME="ClientTASI_R9A_1" VALUE="<<ClientTASI_R9A_1>>" ONFOCUS="select()" ONCHANGE="return vNum(this,0,30);" SIZE=2>
    </TD>
  </TR>
  <TR >
    <TD CLASS="strcol" WIDTH="5%" >&nbsp;</TD>
    <TD CLASS="strcol" >
      Marijuana?
    </TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="text" NAME="ClientTASI_R9M_1" VALUE="<<ClientTASI_R9M_1>>" ONFOCUS="select()" ONCHANGE="return vNum(this,0,30);" SIZE=2>
    </TD>
  </TR>
  <TR >
    <TD CLASS="strcol" WIDTH="5%" >&nbsp;</TD>
    <TD CLASS="strcol" >
      Cocaine?
    </TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="text" NAME="ClientTASI_R9C_1" VALUE="<<ClientTASI_R9C_1>>" ONFOCUS="select()" ONCHANGE="return vNum(this,0,30);" SIZE=2>
    </TD>
  </TR>
  <TR >
    <TD CLASS="strcol" WIDTH="5%" >&nbsp;</TD>
    <TD CLASS="strcol" >
      Other illicit drugs?
    </TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="text" NAME="ClientTASI_R9O_1" VALUE="<<ClientTASI_R9O_1>>" ONFOCUS="select()" ONCHANGE="return vNum(this,0,30);" SIZE=2>
    </TD>
  </TR>
  <TR >
    <TD CLASS="strcol" COLSPAN="2" >
      10. Total number of serious conflicts/arguments with all boy/girlfriend(s) in past month.
    </TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="text" NAME="ClientTASI_R10_1" VALUE="<<ClientTASI_R10_1>>" ONFOCUS="select()" ONCHANGE="return vNum(this,0,30);" SIZE=2>
    </TD>
  </TR>
  <TR >
    <TD CLASS="strcol" COLSPAN="2" >
      11. In the past three months?
    </TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="text" NAME="ClientTASI_R11_1" VALUE="<<ClientTASI_R11_1>>" ONFOCUS="select()" ONCHANGE="return vNum(this,0,30);" SIZE=2>
    </TD>
  </TR>
  <TR >
    <TD CLASS="strcol" COLSPAN="3" >
      COMMENTS
      <TEXTAREA NAME="ClientTASI_R11COM_1" COLS=90 ROWS=8 WRAP=virtual ><<ClientTASI_R11COM_1>></TEXTAREA>
    </TD>
  </TR>
    </TABLE></TD></TR>
</TABLE>
<TABLE CLASS="home fullsize" >
  <TR ><TD CLASS="port hdrtxt" >Page 16<BR>Peer/Social Relationships (cont.)</TD></TR>
    <TR ><TD ><TABLE CLASS="home fullsize" >
  <TR ><TD CLASS="port hdrtxt" COLSPAN="3" >USE THE PATIENT'S RATING SCALE FOR 12</TD></TR>
  <TR >
    <TD CLASS="strcol" COLSPAN="2" >
      12. How satisfied are you with the quality of these boy/girlfriend relationships?
    </TD>
    <TD CLASS="strcol" >
      <SELECT NAME="ClientTASI_R12_1">
        [[DBA->selxTable(%form+xRateScale+<<ClientTASI_R12_1>>+ID Descr)]]
      </SELECT> 
    </TD>
  </TR>
  <TR >
    <TD CLASS="strcol" COLSPAN="2" >
      13. With whom do you spend most of your free time?
      <UL><LI>1=family</LI> <LI>2=friends</LI> <LI>3=gang</LI> <LI>4=boy/girlfriend</LI> <LI>5=alone</LI></UL>
    </TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="text" NAME="ClientTASI_R13_1" VALUE="<<ClientTASI_R13_1>>" ONFOCUS="select()" ONCHANGE="return vNum(this,1,5);" SIZE=2>
    </TD>
  </TR>
  <TR ><TD CLASS="port hdrtxt" COLSPAN="3" >USE THE PATIENT'S RATING SCALE FOR 14 & 15</TD></TR>
  <TR >
    <TD CLASS="strcol" COLSPAN="2" >
      14. How troubled or bothered have you been in the past month by problems with friends?
    </TD>
    <TD CLASS="strcol" >
      <SELECT NAME="ClientTASI_R14_1">
        [[DBA->selxTable(%form+xRateScale+<<ClientTASI_R14_1>>+ID Descr)]]
      </SELECT> 
    </TD>
  </TR>
  <TR >
    <TD CLASS="strcol" COLSPAN="2" >
      15. How important to you now is treatment or counseling for problems with friends?
    </TD>
    <TD CLASS="strcol" >
      <SELECT NAME="ClientTASI_R15_1">
        [[DBA->selxTable(%form+xRateScale+<<ClientTASI_R15_1>>+ID Descr)]]
      </SELECT> 
    </TD>
  </TR>
  <TR ><TD CLASS="port hdrtxt" COLSPAN="3" >INTERVIEWER SEVERITY RATING</TD></TR>
  <TR >
    <TD CLASS="strcol" COLSPAN="2" >
      16. How would you rate the patient's need for relationship counseling?
    </TD>
    <TD CLASS="strcol" >
      <SELECT NAME="ClientTASI_R16_1">
        [[DBA->selxTable(%form+xRateScale+<<ClientTASI_R16_1>>+ID Descr)]]
      </SELECT> 
    </TD>
  </TR>
  <TR ><TD CLASS="port hdrtxt" COLSPAN="3" >CONFIDENCE RATING</TD></TR>
  <TR ><TD CLASS="strcol" COLSPAN="3" >Is the above information significantly distorted by:</TD></TR>
  <TR >
    <TD CLASS="strcol" WIDTH="5%" >&nbsp;</TD>
    <TD CLASS="strcol" COLSPAN="2" >
      17. Patient's misrepresentation?
      <INPUT TYPE="radio" NAME="ClientTASI_R17_1" VALUE="y" <<ClientTASI_R17_1=y>> > Yes
      <INPUT TYPE="radio" NAME="ClientTASI_R17_1" VALUE="n" <<ClientTASI_R17_1=n>> > No
    </TD>
  </TR>
  <TR >
    <TD CLASS="strcol" WIDTH="5%" >&nbsp;</TD>
    <TD CLASS="strcol" COLSPAN="2" >
      18. Patient's inability to understand?
      <INPUT TYPE="radio" NAME="ClientTASI_R18_1" VALUE="y" <<ClientTASI_R18_1=y>> > Yes
      <INPUT TYPE="radio" NAME="ClientTASI_R18_1" VALUE="n" <<ClientTASI_R18_1=n>> > No
    </TD>
  </TR>
  <TR >
    <TD CLASS="strcol" COLSPAN="3" >
      COMMENTS
      <TEXTAREA NAME="ClientTASI_R18COM_1" COLS=90 ROWS=8 WRAP=virtual ><<ClientTASI_R18COM_1>></TEXTAREA>
    </TD>
  </TR>
    </TABLE></TD></TR>
</TABLE>
<TABLE CLASS="home fullsize" >
  <TR ><TD CLASS="port hdrtxt" >Page 17<BR>Legal Status</TD></TR>
    <TR ><TD ><TABLE CLASS="home fullsize" >
  <TR >
    <TD CLASS="strcol" COLSPAN="2" >
      1. Was this admission prompted by or suggested by the criminal justice system judge probation/parole officer, etc.)?
    </TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="radio" NAME="ClientTASI_L1_1" VALUE="y" <<ClientTASI_L1_1=y>> > Yes
      <INPUT TYPE="radio" NAME="ClientTASI_L1_1" VALUE="n" <<ClientTASI_L1_1=n>> > No
    </TD>
  </TR>
  <TR >
    <TD CLASS="strcol" COLSPAN="2" >
      2. Are you on probation or parole?
    </TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="radio" NAME="ClientTASI_L2_1" VALUE="y" <<ClientTASI_L2_1=y>> > Yes
      <INPUT TYPE="radio" NAME="ClientTASI_L2_1" VALUE="n" <<ClientTASI_L2_1=n>> > No
    </TD>
  </TR>
  <TR >
    <TD CLASS="strcol" COLSPAN="2" >
      3. How many times in your life have you been stopped and/or arrested with any criminal offenses?
    </TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="text" NAME="ClientTASI_L3_1" VALUE="<<ClientTASI_L3_1>>" ONFOCUS="select()" ONCHANGE="return vNum(this,0,30);" SIZE=2>
    </TD>
  </TR>
  <TR >
    <TD CLASS="strcol" >&nbsp;</TD>
    <TD CLASS="strcol" >Offense</TD>
    <TD CLASS="strcol" >Age (yrs/mos)</TD>
  </TR>
  <TR >
    <TD CLASS="strcol" >&nbsp;</TD>
    <TD CLASS="strcol" >
      <SELECT NAME="ClientTASI_L3O1_1">
        [[DBA->selxTable(%form+xLegalCharge+<<ClientTASI_L3O1_1>>+Descr)]]
      </SELECT> 
    </TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="text" NAME="ClientTASI_L3A1_1" VALUE="<<ClientTASI_L3A1_1>>" ONFOCUS="select()" SIZE=5 ONCHANGE="return vAge(this)" >
    </TD>
  </TR>
  <TR >
    <TD CLASS="strcol" >&nbsp;</TD>
    <TD CLASS="strcol" >
      <SELECT NAME="ClientTASI_L3O2_1">
        [[DBA->selxTable(%form+xLegalCharge+<<ClientTASI_L3O2_1>>+Descr)]]
      </SELECT> 
    </TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="text" NAME="ClientTASI_L3A2_1" VALUE="<<ClientTASI_L3A2_1>>" ONFOCUS="select()" SIZE=5 ONCHANGE="return vAge(this)" >
    </TD>
  </TR>
  <TR >
    <TD CLASS="strcol" >&nbsp;</TD>
    <TD CLASS="strcol" >
      <SELECT NAME="ClientTASI_L3O3_1">
        [[DBA->selxTable(%form+xLegalCharge+<<ClientTASI_L3O3_1>>+Descr)]]
      </SELECT> 
    </TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="text" NAME="ClientTASI_L3A3_1" VALUE="<<ClientTASI_L3A3_1>>" ONFOCUS="select()" SIZE=5 ONCHANGE="return vAge(this)" >
    </TD>
  </TR>
  <TR >
    <TD CLASS="strcol" >&nbsp;</TD>
    <TD CLASS="strcol" >
      <SELECT NAME="ClientTASI_L3O4_1">
        [[DBA->selxTable(%form+xLegalCharge+<<ClientTASI_L3O4_1>>+Descr)]]
      </SELECT> 
    </TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="text" NAME="ClientTASI_L3A4_1" VALUE="<<ClientTASI_L3A4_1>>" ONFOCUS="select()" SIZE=5 ONCHANGE="return vAge(this)" >
    </TD>
  </TR>
  <TR >
    <TD CLASS="strcol" COLSPAN="2" >
      4. How many of these charges resulted in convictions?
    </TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="text" NAME="ClientTASI_L4_1" VALUE="<<ClientTASI_L4_1>>" ONFOCUS="select()" ONCHANGE="return vNum(this,0,30);" SIZE=2>
    </TD>
  </TR>
  <TR >
    <TD CLASS="strcol" COLSPAN="2" >
      5. How many months of your life were you incarcerated, placed in a youth detention center, or placedin a court ordered arrangement?
    </TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="text" NAME="ClientTASI_L5_1" VALUE="<<ClientTASI_L5_1>>" ONFOCUS="select()" ONCHANGE="return vNum(this,0,30);" SIZE=2>
    </TD>
  </TR>
  <TR >
    <TD CLASS="strcol" COLSPAN="2" >
      6. How long was your last incarceration?
    </TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="text" NAME="ClientTASI_L6_1" VALUE="<<ClientTASI_L6_1>>" ONFOCUS="select()" ONCHANGE="return vNum(this,0,30);" SIZE=2>
    </TD>
  </TR>
  <TR >
    <TD CLASS="strcol" COLSPAN="2" >
      7. What was it for? (If multiple charges, code most severe.)
    </TD>
    <TD CLASS="strcol" >
      <SELECT NAME="ClientTASI_L7_1">
        [[DBA->selxTable(%form+xLegalCharge+<<ClientTASI_L7_1>>+Descr)]]
      </SELECT> 
    </TD>
  </TR>
  <TR >
    <TD CLASS="strcol" COLSPAN="2" >
      8. Are you presently awaiting charges, trial, or sentence?
    </TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="radio" NAME="ClientTASI_L8_1" VALUE="y" <<ClientTASI_L8_1=y>> > Yes
      <INPUT TYPE="radio" NAME="ClientTASI_L8_1" VALUE="n" <<ClientTASI_L8_1=n>> > No
    </TD>
  </TR>
  <TR >
    <TD CLASS="strcol" COLSPAN="2" >
      9. What was it for? (If multiple charges, code most severe.)
    </TD>
    <TD CLASS="strcol" >
      <SELECT NAME="ClientTASI_L9_1">
        [[DBA->selxTable(%form+xLegalCharge+<<ClientTASI_L9_1>>+Descr)]]
      </SELECT> 
    </TD>
  </TR>
  <TR >
    <TD CLASS="strcol" COLSPAN="3" >
      COMMENTS
      <TEXTAREA NAME="ClientTASI_L9COM_1" COLS=90 ROWS=8 WRAP=virtual ><<ClientTASI_L9COM_1>></TEXTAREA>
    </TD>
  </TR>
    </TABLE></TD></TR>
</TABLE>
<TABLE CLASS="home fullsize" >
  <TR ><TD CLASS="port hdrtxt" >Page 18<BR>Legal Status (cont.)</TD></TR>
    <TR ><TD ><TABLE CLASS="home fullsize" >
  <TR >
    <TD CLASS="strcol" COLSPAN="2" >
      10. How many days in the past month were you detained or incarcerated?
    </TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="text" NAME="ClientTASI_L10_1" VALUE="<<ClientTASI_L10_1>>" ONFOCUS="select()" ONCHANGE="return vNum(this,0,30);" SIZE=2>
    </TD>
  </TR>
  <TR >
    <TD CLASS="strcol" COLSPAN="2" >
      11. How many days in the past month have you engaged in illegal activities for profit?
    </TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="text" NAME="ClientTASI_L11_1" VALUE="<<ClientTASI_L11_1>>" ONFOCUS="select()" ONCHANGE="return vNum(this,0,30);" SIZE=2>
    </TD>
  </TR>
  <TR ><TD CLASS="port hdrtxt" COLSPAN="3" >USE THE PATIENT'S RATING SCALE FOR 12 & 13</TD></TR>
  <TR >
    <TD CLASS="strcol" COLSPAN="2" >
      12. How serious do you feel your present legal problems are (exclude civil problems)?
    </TD>
    <TD CLASS="strcol" >
      <SELECT NAME="ClientTASI_L12_1">
        [[DBA->selxTable(%form+xRateScale+<<ClientTASI_L12_1>>+ID Descr)]]
      </SELECT> 
    </TD>
  </TR>
  <TR >
    <TD CLASS="strcol" COLSPAN="2" >
      13. How important to you now is counseling or referral for these legal problems?
    </TD>
    <TD CLASS="strcol" >
      <SELECT NAME="ClientTASI_L13_1">
        [[DBA->selxTable(%form+xRateScale+<<ClientTASI_L13_1>>+ID Descr)]]
      </SELECT> 
    </TD>
  </TR>
  <TR ><TD CLASS="port hdrtxt" COLSPAN="3" >INTERVIEWER SEVERITY RATING</TD></TR>
  <TR >
    <TD CLASS="strcol" COLSPAN="2" >
      14. How would you rate the patient's need for legal services or counseling?
    </TD>
    <TD CLASS="strcol" >
      <SELECT NAME="ClientTASI_L14_1">
        [[DBA->selxTable(%form+xRateScale+<<ClientTASI_L14_1>>+ID Descr)]]
      </SELECT> 
    </TD>
  </TR>
  <TR ><TD CLASS="port hdrtxt" COLSPAN="3" >CONFIDENCE RATING</TD></TR>
  <TR ><TD CLASS="strcol" COLSPAN="3" >Is the above information significantly distorted by:</TD></TR>
  <TR >
    <TD CLASS="strcol" WIDTH="5%" >&nbsp;</TD>
    <TD CLASS="strcol" COLSPAN="2" >
      15. Patient's misrepresentation?
      <INPUT TYPE="radio" NAME="ClientTASI_L15_1" VALUE="y" <<ClientTASI_L15_1=y>> > Yes
      <INPUT TYPE="radio" NAME="ClientTASI_L15_1" VALUE="n" <<ClientTASI_L15_1=n>> > No
    </TD>
  </TR>
  <TR >
    <TD CLASS="strcol" WIDTH="5%" >&nbsp;</TD>
    <TD CLASS="strcol" COLSPAN="2" >
      16. Patient's inability to understand?
      <INPUT TYPE="radio" NAME="ClientTASI_L16_1" VALUE="y" <<ClientTASI_L16_1=y>> > Yes
      <INPUT TYPE="radio" NAME="ClientTASI_L16_1" VALUE="n" <<ClientTASI_L16_1=n>> > No
    </TD>
  </TR>
  <TR >
    <TD CLASS="strcol" COLSPAN="3" >
      COMMENTS
      <TEXTAREA NAME="ClientTASI_L16COM_1" COLS=90 ROWS=8 WRAP=virtual ><<ClientTASI_L16COM_1>></TEXTAREA>
    </TD>
  </TR>
    </TABLE></TD></TR>
</TABLE>
<TABLE CLASS="home fullsize" >
  <TR ><TD CLASS="port hdrtxt" >Page 19<BR>Psychiatric Status</TD></TR>
    <TR ><TD ><TABLE CLASS="home fullsize" >
  <TR >
    <TD CLASS="strcol" COLSPAN="3" >
      1. How many times have you: been treated fro any psychological or emotional problems
    </TD>
  </TR>
  <TR >
    <TD CLASS="strcol" WIDTH="5%" >&nbsp;</TD>
    <TD CLASS="strcol" COPSPAN=2 >
      <INPUT TYPE="text" NAME="ClientTASI_P1I_1" VALUE="<<ClientTASI_P1I_1>>" ONFOCUS="select()" ONCHANGE="return vNum(this,0,30);" SIZE=2>
      in the hospital (as an inpatient)?
    </TD>
  </TR>
  <TR >
    <TD CLASS="strcol" WIDTH="5%" >&nbsp;</TD>
    <TD CLASS="strcol" COPSPAN=2 >
      <INPUT TYPE="text" NAME="ClientTASI_P1O_1" VALUE="<<ClientTASI_P1O_1>>" ONFOCUS="select()" ONCHANGE="return vNum(this,0,30);" SIZE=2>
      as an outpatient or private patient?
    </TD>
  </TR>
  <TR >
    <TD CLASS="strcol" WIDTH="5%" >&nbsp;</TD>
    <TD CLASS="strcol" COPSPAN=2 >
      <INPUT TYPE="text" NAME="ClientTASI_P1T_1" VALUE="<<ClientTASI_P1T_1>>" ONFOCUS="select()" ONCHANGE="return vNum(this,0,30);" SIZE=2>
      Total
    </TD>
  </TR>
  <TR >
    <TD CLASS="strcol" COLSPAN="3" >
      Have you had a significant period (that was not a direct result of drug/alcohol use) in which you:
    </TD>
  </TR>
  <TR >
    <TD CLASS="strcol" WIDTH="5%" >&nbsp;</TD>
    <TD CLASS="strcol" COLSPAN="2" >
      2. experienced serious depression?
      <INPUT TYPE="radio" NAME="ClientTASI_P2_1" VALUE="y" <<ClientTASI_P2_1=y>> > Yes
      <INPUT TYPE="radio" NAME="ClientTASI_P2_1" VALUE="n" <<ClientTASI_P2_1=n>> > No
    </TD>
  </TR>
  <TR >
    <TD CLASS="strcol" WIDTH="5%" >&nbsp;</TD>
    <TD CLASS="strcol" COLSPAN="2" >
      3. experienced serious anxiety or tension?
      <INPUT TYPE="radio" NAME="ClientTASI_P3_1" VALUE="y" <<ClientTASI_P3_1=y>> > Yes
      <INPUT TYPE="radio" NAME="ClientTASI_P3_1" VALUE="n" <<ClientTASI_P3_1=n>> > No
    </TD>
  </TR>
  <TR >
    <TD CLASS="strcol" WIDTH="5%" >&nbsp;</TD>
    <TD CLASS="strcol" COLSPAN="2" >
      4. experienced delusions?
      <INPUT TYPE="radio" NAME="ClientTASI_P4_1" VALUE="y" <<ClientTASI_P4_1=y>> > Yes
      <INPUT TYPE="radio" NAME="ClientTASI_P4_1" VALUE="n" <<ClientTASI_P4_1=n>> > No
    </TD>
  </TR>
  <TR >
    <TD CLASS="strcol" WIDTH="5%" >&nbsp;</TD>
    <TD CLASS="strcol" COLSPAN="2" >
      5. experienced hallucinations?
      <INPUT TYPE="radio" NAME="ClientTASI_P5_1" VALUE="y" <<ClientTASI_P5_1=y>> > Yes
      <INPUT TYPE="radio" NAME="ClientTASI_P5_1" VALUE="n" <<ClientTASI_P5_1=n>> > No
    </TD>
  </TR>
  <TR >
    <TD CLASS="strcol" WIDTH="5%" >&nbsp;</TD>
    <TD CLASS="strcol" COLSPAN="2" >
      6. experienced trouble understanding, concentrating, or remembering?
      <INPUT TYPE="radio" NAME="ClientTASI_P6_1" VALUE="y" <<ClientTASI_P6_1=y>> > Yes
      <INPUT TYPE="radio" NAME="ClientTASI_P6_1" VALUE="n" <<ClientTASI_P6_1=n>> > No
    </TD>
  </TR>
  <TR >
    <TD CLASS="strcol" WIDTH="5%" >&nbsp;</TD>
    <TD CLASS="strcol" COLSPAN="2" >
      7. experienced trouble controlling violent behavior?
      <INPUT TYPE="radio" NAME="ClientTASI_P7_1" VALUE="y" <<ClientTASI_P7_1=y>> > Yes
      <INPUT TYPE="radio" NAME="ClientTASI_P7_1" VALUE="n" <<ClientTASI_P7_1=n>> > No
    </TD>
  </TR>
  <TR >
    <TD CLASS="strcol" WIDTH="5%" >&nbsp;</TD>
    <TD CLASS="strcol" COLSPAN="2" >
      8. experienced serious thoughts of suicide?
      <INPUT TYPE="radio" NAME="ClientTASI_P8_1" VALUE="y" <<ClientTASI_P8_1=y>> > Yes
      <INPUT TYPE="radio" NAME="ClientTASI_P8_1" VALUE="n" <<ClientTASI_P8_1=n>> > No
    </TD>
  </TR>
  <TR >
    <TD CLASS="strcol" WIDTH="5%" >&nbsp;</TD>
    <TD CLASS="strcol" COLSPAN="2" >
      9. attempted suicide?
      <INPUT TYPE="radio" NAME="ClientTASI_P9_1" VALUE="y" <<ClientTASI_P9_1=y>> > Yes
      <INPUT TYPE="radio" NAME="ClientTASI_P9_1" VALUE="n" <<ClientTASI_P9_1=n>> > No
    </TD>
  </TR>
  <TR >
    <TD CLASS="strcol" WIDTH="5%" >&nbsp;</TD>
    <TD CLASS="strcol" COLSPAN="2" >
      10. Have you taken prescribed medication for any psychological/emotional problem?
      <INPUT TYPE="radio" NAME="ClientTASI_P10_1" VALUE="y" <<ClientTASI_P10_1=y>> > Yes
      <INPUT TYPE="radio" NAME="ClientTASI_P10_1" VALUE="n" <<ClientTASI_P10_1=n>> > No
    </TD>
  </TR>
  <TR >
    <TD CLASS="strcol" WIDTH="5%" >&nbsp;</TD>
    <TD CLASS="strcol" COLSPAN="2" >
      11. How many days in the past month have you experienced these psychological or emotionalproblems?
      <INPUT TYPE="text" NAME="ClientTASI_P11_1" VALUE="<<ClientTASI_P11_1>>" ONFOCUS="select()" ONCHANGE="return vNum(this,0,31);" SIZE="2" >
    </TD>
  </TR>
  <TR ><TD CLASS="port hdrtxt" COLSPAN="3" >USE THE PATIENT'S RATING SCALE FOR 12 & 13</TD></TR>
  <TR >
    <TD CLASS="strcol" COLSPAN="2" >
      12. How much have you been troubled or bothered by these psychological or emotional problemsin the past month?
    </TD>
    <TD CLASS="strcol" >
      <SELECT NAME="ClientTASI_P12_1">
        [[DBA->selxTable(%form+xRateScale+<<ClientTASI_P12_1>>+ID Descr)]]
      </SELECT> 
    </TD>
  </TR>
  <TR >
    <TD CLASS="strcol" COLSPAN="2" >
      13.  How important to you now is treatment for these psychological problems?
    </TD>
    <TD CLASS="strcol" >
      <SELECT NAME="ClientTASI_P13_1">
        [[DBA->selxTable(%form+xRateScale+<<ClientTASI_P13_1>>+ID Descr)]]
      </SELECT> 
    </TD>
  </TR>
  <TR >
    <TD CLASS="strcol" COLSPAN="3" >
      COMMENTS
      <TEXTAREA NAME="ClientTASI_P13COM_1" COLS=90 ROWS=8 WRAP=virtual ><<ClientTASI_P13COM_1>></TEXTAREA>
    </TD>
  </TR>
    </TABLE></TD></TR>
</TABLE>
<TABLE CLASS="home fullsize" >
  <TR ><TD CLASS="port hdrtxt" >Page 20<BR>Psychiatric Status (cont.)</TD></TR>
    <TR ><TD ><TABLE CLASS="home fullsize" >
  <TR >
    <TD CLASS="strcol" COLSPAN="3" >
      THE FOLLOWING ITEMS ARE TO BE COMPLETED BY THE INTERVIEWER
    </TD>
  </TR>
  <TR >
    <TD CLASS="strcol" COLSPAN="3" >
      At the time of the interview, is the patient:
    </TD>
  </TR>
  <TR >
    <TD CLASS="strcol" WIDTH="5%" >&nbsp;</TD>
    <TD CLASS="strcol" COLSPAN="2" >
      14. obviously depressed/withdrawn?
      <INPUT TYPE="radio" NAME="ClientTASI_P14_1" VALUE="y" <<ClientTASI_P14_1=y>> > Yes
      <INPUT TYPE="radio" NAME="ClientTASI_P14_1" VALUE="n" <<ClientTASI_P14_1=n>> > No
    </TD>
  </TR>
  <TR >
    <TD CLASS="strcol" WIDTH="5%" >&nbsp;</TD>
    <TD CLASS="strcol" COLSPAN="2" >
      15. obviously hostile?
      <INPUT TYPE="radio" NAME="ClientTASI_P15_1" VALUE="y" <<ClientTASI_P15_1=y>> > Yes
      <INPUT TYPE="radio" NAME="ClientTASI_P15_1" VALUE="n" <<ClientTASI_P15_1=n>> > No
    </TD>
  </TR>
  <TR >
    <TD CLASS="strcol" WIDTH="5%" >&nbsp;</TD>
    <TD CLASS="strcol" >
      16. obviously anxious/nervous?
      <INPUT TYPE="radio" NAME="ClientTASI_P16_1" VALUE="y" <<ClientTASI_P16_1=y>> > Yes
      <INPUT TYPE="radio" NAME="ClientTASI_P16_1" VALUE="n" <<ClientTASI_P16_1=n>> > No
    </TD>
  </TR>
  <TR >
    <TD CLASS="strcol" WIDTH="5%" >&nbsp;</TD>
    <TD CLASS="strcol" COLSPAN="2" >
      17. having trouble with reality testing, thought disorders, paranoid thinking?
      <INPUT TYPE="radio" NAME="ClientTASI_P17_1" VALUE="y" <<ClientTASI_P17_1=y>> > Yes
      <INPUT TYPE="radio" NAME="ClientTASI_P17_1" VALUE="n" <<ClientTASI_P17_1=n>> > No
    </TD>
  </TR>
  <TR >
    <TD CLASS="strcol" WIDTH="5%" >&nbsp;</TD>
    <TD CLASS="strcol" COLSPAN="2" >
      18. having trouble comprehending, concentrating, remembering?
      <INPUT TYPE="radio" NAME="ClientTASI_P18_1" VALUE="y" <<ClientTASI_P18_1=y>> > Yes
      <INPUT TYPE="radio" NAME="ClientTASI_P18_1" VALUE="n" <<ClientTASI_P18_1=n>> > No
    </TD>
  </TR>
  <TR >
    <TD CLASS="strcol" WIDTH="5%" >&nbsp;</TD>
    <TD CLASS="strcol" COLSPAN="2" >
      19. having suicidal thoughts?
      <INPUT TYPE="radio" NAME="ClientTASI_P19_1" VALUE="y" <<ClientTASI_P19_1=y>> > Yes
      <INPUT TYPE="radio" NAME="ClientTASI_P19_1" VALUE="n" <<ClientTASI_P19_1=n>> > No
    </TD>
  </TR>
  <TR ><TD CLASS="port hdrtxt" COLSPAN="3" >INTERVIEWER SEVERITY RATING</TD></TR>
  <TR >
    <TD CLASS="strcol" COLSPAN="2" >
      20. How would you rate the patient's need for psychiatric/psychological treatment? 
    </TD>
    <TD CLASS="strcol" >
      <SELECT NAME="ClientTASI_P20_1">
        [[DBA->selxTable(%form+xRateScale+<<ClientTASI_P20_1>>+ID Descr)]]
      </SELECT> 
    </TD>
  </TR>
  <TR ><TD CLASS="port hdrtxt" COLSPAN="3" >CONFIDENCE RATING</TD></TR>
  <TR ><TD CLASS="strcol" COLSPAN="3" >Is the above information significantly distorted by:</TD></TR>
  <TR >
    <TD CLASS="strcol" WIDTH="5%" >&nbsp;</TD>
    <TD CLASS="strcol" COLSPAN="2" >
      21. Patient's misrepresentation?
      <INPUT TYPE="radio" NAME="ClientTASI_P21_1" VALUE="y" <<ClientTASI_P21_1=y>> > Yes
      <INPUT TYPE="radio" NAME="ClientTASI_P21_1" VALUE="n" <<ClientTASI_P21_1=n>> > No
    </TD>
  </TR>
  <TR >
    <TD CLASS="strcol" WIDTH="5%" >&nbsp;</TD>
    <TD CLASS="strcol" COLSPAN="2" >
      22. Patient's inability to understand?
      <INPUT TYPE="radio" NAME="ClientTASI_P22_1" VALUE="y" <<ClientTASI_P22_1=y>> > Yes
      <INPUT TYPE="radio" NAME="ClientTASI_P22_1" VALUE="n" <<ClientTASI_P22_1=n>> > No
    </TD>
  </TR>
  <TR >
    <TD CLASS="strcol" COLSPAN="3" >
      COMMENTS
      <TEXTAREA NAME="ClientTASI_P22COM_1" COLS=90 ROWS=8 WRAP=virtual ><<ClientTASI_P22COM_1>></TEXTAREA>
    </TD>
  </TR>
    </TABLE></TD></TR>
</TABLE>
<TABLE CLASS="main fullsize" >
  <TR >
    <TD CLASS="numcol" >
      <INPUT TYPE="submit" ONCLICK="return vDELETE('Are you sure you want to delete this entire TASI record?');" NAME="ClientTASI_DELETE_1=1&UpdateTables=all&misPOP=1" VALUE="Delete">
      <INPUT TYPE="submit" ONCLICK="return validate(this.form);" NAME="UpdateTables=all&misPOP=1" VALUE="Add/Update">
    </TD>
  </TR>
</TABLE>

<INPUT TYPE="hidden" NAME="subview" VALUE="<<subview>>" >
</LOADHIDDEN>
</FORM>
<SCRIPT LANGUAGE="JavaScript">
document.ClientTASI.elements[0].focus();
</SCRIPT>

[[myHTML->rightpane(%form+search)]]
