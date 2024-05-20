[[myHTML->newPage(%form+Client Health History+++++accordionopen)]]

<SCRIPT LANGUAGE="JavaScript" SRC="/cgi/js/vEntry.js"> </SCRIPT>
<SCRIPT LANGUAGE="JavaScript" SRC="/cgi/js/vClientHealthHistory.js"> </SCRIPT>
<SCRIPT LANGUAGE="JavaScript" SRC="/cgi/js/ajaxrequest.js"> </SCRIPT>
<SCRIPT LANGUAGE="JavaScript" SRC="/cgi/js/vDate.js"> </SCRIPT>
<SCRIPT LANGUAGE="JavaScript" SRC="/cgi/js/vNum.js"> </SCRIPT>

<FORM NAME="HealthHistory" ACTION="/cgi/bin/mis.cgi" METHOD="POST" >
<TABLE CLASS="main fullsize" >
  <TR >
    <TD CLASS="strcol" >
      <<<Client_FName_1>>> <<<Client_MName_1>>> <<<Client_LName_1>>> (<<<Client_ClientID_1>>>) <<<Client_SSN_1>>>
      <BR>
      Health History Page
    </TD>
    <TD CLASS="numcol" >[[gHTML->setLINKS(%form+back)]]</TD>
  </TR>
</TABLE>
<TABLE CLASS="port fullsize" >
  <TR ><TD CLASS="heading" >HEALTH HISTORY</TD></TR>
    <TR ><TD ><TABLE CLASS="home fullsize" >
<TABLE CLASS="home fullsize" >
  <TR ><TD CLASS="port hdrtxt" WIDTH="50%" >Overall Health Status</TD><TD>&nbsp;</TD></TR>
  <TR >
    <TD CLASS="strcol" COLSPAN="2" >
      <SELECT NAME="ClientHealth_OverallHealth_1" >
        [[DBA->selxTable(%form+xHealthStatus+<<ClientHealth_OverallHealth_1>>+ConceptName ConceptCode)]]
      </SELECT>
    </TD>
  </TR>
  <TR ><TD CLASS="port hdrtxt" WIDTH="50%" >Hospitalization History</TD><TD>&nbsp;</TD></TR>
  <TR >
    <TD CLASS="strcol" COLSPAN="2" >
      How many times in your life have you been hospitalized overnight for medical problems?
      <BR>· Include O.D.'s and D.T.'s. Exclude detox, alcohol/drug, psychiatric treatment and childbirth (if no complications).
    </TD>
  </TR>
  <TR >
    <TD CLASS="strcol" COLSPAN="2" >
      <INPUT TYPE="text" NAME="ClientHealth_HospOverNight_1" VALUE="<<ClientHealth_HospOverNight_1>>" ONFOCUS="select()" ONCHANGE="return vNum(this,0,99);" SIZE="2" >
    </TD>
  </TR>
  <TR ><TD CLASS="strcol" COLSPAN="2" >Describe reasons for all overnight Hospitalizations</TD></TR>
  <TR >
    <TD CLASS="strcol" COLSPAN="2" >
      <TEXTAREA NAME="ClientIntake_PhysHist_1" COLS=90 ROWS=8 WRAP=virtual ><<ClientIntake_PhysHist_1>></TEXTAREA>
    </TD>
  </TR>
</TABLE>
  <div class="accordionItem">
    <h2>Health Appraisal Questionaire Male + Female Version <img id="accordionImage" class="accordionImage" src="/images/sorted_down.gif" > (click here to expand/collapse)</h2>
    <div>
[[[myHTML->setHTML(%form+ClientCDCHA)]]]
    </div>
  </div>
  <div class="accordionItem">
    <h2 >Sexual History, Including HIV/AIDS & STD At-Risk Behaviors <img id="accordionImage" class="accordionImage" src="/images/sorted_down.gif" > (click here to expand/collapse)</h2>
    <div>
<TABLE CLASS="home fullsize" >
  <TR >
    <TD CLASS="strcol" COLSPAN="2" >
      <INPUT TYPE=checkbox NAME="ClientHealth_RefusedQues_1" VALUE=1 <<ClientHealth_RefusedQues_1=checkbox>> >
      Client refused to answer questions about sexual history
    </TD>
  </TR>
  <TR name="pregnant_sec" id="pregnant_sec">
    <TD CLASS="strcol" >Are you pregnant?</TD>
    <TD CLASS="strcol" >
	<SELECT NAME="ClientHealth_PrenatalStatus_1" >
        [[DBA->selxTable(%form+xPrenatalStatus+<<ClientHealth_PrenatalStatus_1>>+Name)]]
      </SELECT>
<!--
      <INPUT TYPE="text" NAME="ClientIntake_PregnantDate_1" VALUE="<<ClientIntake_PregnantDate_1>>" ONFOCUS="select()" ONCHANGE="return vDate(this,1);" SIZE="10" >
-->    </TD>
  </TR>

  <TR name="pregnant_sec_2" id="pregnant_sec_2"><TD CLASS="strcol" COLSPAN="2" >Prenatal Care needed: (if yes: describe conditions)</TD></TR>
  <TR name="pregnant_sec_3" id="pregnant_sec_3">
    <TD CLASS="strcol" COLSPAN="2" >
      <TEXTAREA NAME="ClientHealth_PrenatalCare_1" COLS="90" ROWS="8" WRAP="virtual" ><<ClientHealth_PrenatalCare_1>></TEXTAREA>
    </TD>
  </TR>

  <TR >
    <TD CLASS="strcol" >
      Age began dating:
      <SELECT NAME="ClientHealth_AgeDating_1" >
        [[DBA->selxTable(%form+xAgeActive+<<ClientHealth_AgeDating_1>>+Descr)]]
      </SELECT>
    </TD>
    <TD CLASS="strcol" >
      Age began sexual activity (if pertinent):
      <SELECT NAME="ClientHealth_AgeSexual_1" >
        [[DBA->selxTable(%form+xAgeActive+<<ClientHealth_AgeSexual_1>>+Descr)]]
      </SELECT>
    </TD>
  <TR >
    <TD CLASS="strcol" >Sexual Orientation / Expression (if applicable, select one)?</TD>
    <TD CLASS="strcol" >
      <SELECT NAME="ClientHealth_SexPref_1" >
        [[DBA->selxTable(%form+xSexualOrientation+<<ClientHealth_SexPref_1>>+ConceptName)]]
      </SELECT>
    </TD>
  </TR>
  <TR >
    <TD CLASS="strcol" >Gender Identity/Identify (if applicable, select one)?</TD>
    <TD CLASS="strcol" >
      <SELECT NAME="ClientHealth_SexID_1" >
        [[DBA->selxTable(%form+xGenderIdentity+<<ClientHealth_SexID_1>>+ConceptName)]]
      </SELECT>
    </TD>
  </TR>
  <TR >
    <TD CLASS="strcol" >Are you sexually active or want to be sexually active?</TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="radio" NAME="ClientHealth_SexActive_1" VALUE=1 <<ClientHealth_SexActive_1=1>> > Yes
      <INPUT TYPE="radio" NAME="ClientHealth_SexActive_1" VALUE=0 <<ClientHealth_SexActive_1=0>> > No
      <INPUT TYPE="radio" NAME="ClientHealth_SexActive_1" VALUE=R <<ClientHealth_SexActive_1=R>> > Refused to answer
    </TD>
  </TR>
  <TR >
    <TD CLASS="strcol" >
      Have you ever had vaginal intercourse?
    </TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="radio" NAME="ClientHealth_Intercourse_1" VALUE=1 <<ClientHealth_Intercourse_1=1>> > Yes
      <INPUT TYPE="radio" NAME="ClientHealth_Intercourse_1" VALUE=0 <<ClientHealth_Intercourse_1=0>> > No
      <INPUT TYPE="radio" NAME="ClientHealth_Intercourse_1" VALUE=R <<ClientHealth_Intercourse_1=R>> > Refused to answer
    </TD>
  </TR>
  <TR >
    <TD CLASS="strcol" >Any Sexual problems?</TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="radio" NAME="ClientHealth_SexProb_1" VALUE=1 <<ClientHealth_SexProb_1=1>> > Yes
      <INPUT TYPE="radio" NAME="ClientHealth_SexProb_1" VALUE=0 <<ClientHealth_SexProb_1=0>> > No
      <INPUT TYPE="radio" NAME="ClientHealth_SexProb_1" VALUE=R <<ClientHealth_SexProb_1=R>> > Refused to answer
    </TD>
  </TR>
  <TR >
    <TD CLASS="strcol" COLSPAN="2" >
      If yes, explain:
      <INPUT TYPE="text" NAME="ClientHealth_SexProbDescr_1" VALUE="<<ClientHealth_SexProbDescr_1>>" MAXLENGTH="60" SIZE="60" >
    </TD>
  </TR>
  <TR ><TD CLASS="strcol" COLSPAN="2" >Sexually transmitted diseases/treatment? (use ctrl-key to select multiples)</TD></TR>
  <TR >
    <TD CLASS="strcol" COLSPAN="2" >
      If yes, which:
      <SELECT NAME="ClientHealth_STD_1" MULTIPLE SIZE="10" >
        [[DBA->selxTable(%form+xSTD+<<ClientHealth_STD_1>>+Descr)]]
      </SELECT>
    </TD>
  </TR>
  <TR >
    <TD CLASS="strcol" >Are you more sexually active while using chemicals?</TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="radio" NAME="ClientHealth_SexChems_1" VALUE=1 <<ClientHealth_SexChems_1=1>> > Yes
      <INPUT TYPE="radio" NAME="ClientHealth_SexChems_1" VALUE=0 <<ClientHealth_SexChems_1=0>> > No
      <INPUT TYPE="radio" NAME="ClientHealth_SexChems_1" VALUE=R <<ClientHealth_SexChems_1=R>> > Refused to answer
    </TD>
  </TR>
  <TR >
    <TD CLASS="strcol" >Have you traded sex for drugs or money?</TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="radio" NAME="ClientHealth_SexTrade_1" VALUE=1 <<ClientHealth_SexTrade_1=1>> > Yes
      <INPUT TYPE="radio" NAME="ClientHealth_SexTrade_1" VALUE=0 <<ClientHealth_SexTrade_1=0>> > No
      <INPUT TYPE="radio" NAME="ClientHealth_SexTrade_1" VALUE=R <<ClientHealth_SexTrade_1=R>> > Refused to answer
    </TD>
  </TR>
  <TR >
    <TD CLASS="strcol" >Do you feel guilty about any sexual behavior?</TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="radio" NAME="ClientHealth_SexGuilt_1" VALUE=1 <<ClientHealth_SexGuilt_1=1>> > Yes
      <INPUT TYPE="radio" NAME="ClientHealth_SexGuilt_1" VALUE=0 <<ClientHealth_SexGuilt_1=0>> > No
      <INPUT TYPE="radio" NAME="ClientHealth_SexGuilt_1" VALUE=R <<ClientHealth_SexGuilt_1=R>> > Refused to answer
    </TD>
  </TR>
</TABLE>
    </div>
  </div>
<TABLE CLASS="home fullsize" >
  <TR >
    <TD CLASS="port hdrtxt" WIDTH="50%" >Medication / Food Allergies</TD>
    <TD CLASS="strcol" >
      NO Allergies reported
      <SELECT NAME="ClientIntake_NoAllergies_1">
        [[DBA->selxTable(%form+xNoAllergies+<<ClientIntake_NoAllergies_1>>+Descr)]]
      </SELECT> 
    </TD>
  </TR>
  <TR >
    <TD CLASS="port hdrcol" COLSPAN="2" >
      Client Allergies
      <A HREF="javascript:callAjax('ListClientAllergies','','ListClientAllergies','&active=1&Locked=0&Client_ClientID=<<<Client_ClientID>>>&LOGINPROVID=<<<LOGINPROVID>>>&LOGINUSERID=<<<LOGINUSERID>>>&LINKID=<<<LINKID>>>&mlt=<<<mlt>>>&LOGINUSERDB=<<<LOGINUSERDB>>>','popup.pl');" TITLE="Show ONLY Active Allergies for Client">Active Only</A>
      /
      <A HREF="javascript:callAjax('ListClientAllergies','','ListClientAllergies','&active=0&Locked=0&Client_ClientID=<<<Client_ClientID>>>&LOGINPROVID=<<<LOGINPROVID>>>&LOGINUSERID=<<<LOGINUSERID>>>&LINKID=<<<LINKID>>>&mlt=<<<mlt>>>&LOGINUSERDB=<<<LOGINUSERDB>>>','popup.pl');" TITLE="Show ALL Allergies for Client">Show All</A>
    </TD>
  </TR>
  <TR >
    <TD COLSPAN="2" >
<SPAN ID="ListClientAllergies" >
[[myHTML->ListSel(%form+ListClientAllergies+<<<Client_ClientID>>>+<<<LINKID>>>+<<<Client_Locked_1>>>)]]
</SPAN>
    </TD>
  </TR>
  <TR ><TD CLASS="port hdrtxt" WIDTH="50%" >Immunizations</TD><TD>&nbsp;</TD></TR>
  <TR ><TD CLASS="strcol" COLSPAN="2" >Are your immunizations up to date (child &amp; adolescent)?</TD></TR>
  <TR >
    <TD CLASS="strcol" >If no, What are you lacking?</TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="text" NAME="ClientHealth_ImmunizeDesc_1" VALUE="<<ClientHealth_ImmunizeDesc_1>>" ONFOCUS="select()" SIZE="70" >
    </TD>
  </TR>

<TR ><TD CLASS="port hdrtxt" WIDTH="50%" >COVID Vaccination</TD><TD>&nbsp;</TD></TR>
  <TR >
    <TD CLASS="strcol" >
      COVID Dose 1:
      <SELECT NAME="ClientHealth_COVIDDose1_1" >
        [[DBA->selxTable(%form+xCOVIDVaccines+<<ClientHealth_COVIDDose1_1>>+Descr)]]
      </SELECT>
      
    </TD>
    <TD CLASS="strcol" >
        Date:
    	<INPUT TYPE="text" NAME="ClientHealth_COVIDDose1Date_1" VALUE="<<ClientHealth_COVIDDose1Date_1>>" ONFOCUS="select()" ONCHANGE="return vDate(this,1);" SIZE="10" >
    </TD>
  </TR>
<TR >
    <TD CLASS="strcol" >
      COVID Dose 2:
      <SELECT NAME="ClientHealth_COVIDDose2_1" >
        [[DBA->selxTable(%form+xCOVIDVaccines+<<ClientHealth_COVIDDose2_1>>+Descr)]]
      </SELECT>
    </TD>
    <TD CLASS="strcol" >
        Date:
    	<INPUT TYPE="text" NAME="ClientHealth_COVIDDose2Date_1" VALUE="<<ClientHealth_COVIDDose2Date_1>>" ONFOCUS="select()" ONCHANGE="return vDate(this,1);" SIZE="10" >
    </TD>
  </TR>
<TR >
    <TD CLASS="strcol" >
      COVID Dose 3:
      <SELECT NAME="ClientHealth_COVIDDose3_1" >
        [[DBA->selxTable(%form+xCOVIDVaccines+<<ClientHealth_COVIDDose3_1>>+Descr)]]
      </SELECT>
      </TD>
    <TD CLASS="strcol" >
        Date:
    	<INPUT TYPE="text" NAME="ClientHealth_COVIDDose3Date_1" VALUE="<<ClientHealth_COVIDDose3Date_1>>" ONFOCUS="select()" ONCHANGE="return vDate(this,1);" SIZE="10" >
    </TD>
  </TR>
<TR >
    <TD CLASS="strcol" >
      COVID Dose 4:
      <SELECT NAME="ClientHealth_COVIDDose4_1" >
        [[DBA->selxTable(%form+xCOVIDVaccines+<<ClientHealth_COVIDDose4_1>>+Descr)]]
      </SELECT>
      </TD>
    <TD CLASS="strcol" >
        Date:
    	<INPUT TYPE="text" NAME="ClientHealth_COVIDDose4Date_1" VALUE="<<ClientHealth_COVIDDose4Date_1>>" ONFOCUS="select()" ONCHANGE="return vDate(this,1);" SIZE="10" >
    </TD>
  </TR>
<TR >
    <TD CLASS="strcol" >
      COVID Infection 1 Date:
      <INPUT TYPE="text" NAME="ClientHealth_COVIDInfection1Date_1" VALUE="<<ClientHealth_COVIDInfection1Date_1>>" ONFOCUS="select()" ONCHANGE="return vDate(this,1);" SIZE="10" >
    </TD>
    <TD CLASS="strcol" >&nbsp;</TD>
  </TR>
<TR >
    <TD CLASS="strcol" >
      COVID Infection 2 Date:
      <INPUT TYPE="text" NAME="ClientHealth_COVIDInfection2Date_1" VALUE="<<ClientHealth_COVIDInfection2Date_1>>" ONFOCUS="select()" ONCHANGE="return vDate(this,1);" SIZE="10" >
    </TD>
    <TD CLASS="strcol" >&nbsp;</TD>
  </TR>
<TR >
    <TD CLASS="strcol" >
      COVID Infection 3 Date:
      <INPUT TYPE="text" NAME="ClientHealth_COVIDInfection3Date_1" VALUE="<<ClientHealth_COVIDInfection3Date_1>>" ONFOCUS="select()" ONCHANGE="return vDate(this,1);" SIZE="10" >
    </TD>
    <TD CLASS="strcol" >&nbsp;</TD>
  </TR>
<TR >
    <TD CLASS="strcol" >
      COVID Infection 4 Date:
      <INPUT TYPE="text" NAME="ClientHealth_COVIDInfection4Date_1" VALUE="<<ClientHealth_COVIDInfection4Date_1>>" ONFOCUS="select()" ONCHANGE="return vDate(this,1);" SIZE="10" >
    </TD>
    <TD CLASS="strcol" >&nbsp;</TD>
  </TR>
 <TR >
    <TD CLASS="strcol" >
      COVID Therapeutic 1:
      <SELECT NAME="ClientHealth_COVIDTherapeutic1_1" >
        [[DBA->selxTable(%form+xCOVIDTherapeutic+<<ClientHealth_COVIDTherapeutic1_1>>+Name)]]
      </SELECT>
      </TD>
    <TD CLASS="strcol" >
        Date:
    	<INPUT TYPE="text" NAME="ClientHealth_COVIDTherapeutic1Date_1" VALUE="<<ClientHealth_COVIDTherapeutic1Date_1>>" ONFOCUS="select()" ONCHANGE="return vDate(this,1);" SIZE="10" >
    </TD>
  </TR>
<TR >
    <TD CLASS="strcol" >
      COVID Therapeutic 2:
      <SELECT NAME="ClientHealth_COVIDTherapeutic2_1" >
        [[DBA->selxTable(%form+xCOVIDTherapeutic+<<ClientHealth_COVIDTherapeutic2_1>>+Name)]]
      </SELECT>
      </TD>
    <TD CLASS="strcol" >
        Date:
    	<INPUT TYPE="text" NAME="ClientHealth_COVIDTherapeutic2Date_1" VALUE="<<ClientHealth_COVIDTherapeutic2Date_1>>" ONFOCUS="select()" ONCHANGE="return vDate(this,1);" SIZE="10" >
    </TD>
  </TR>
<TR >
    <TD CLASS="strcol" >
      COVID Therapeutic 3:
      <SELECT NAME="ClientHealth_COVIDTherapeutic3_1" >
        [[DBA->selxTable(%form+xCOVIDTherapeutic+<<ClientHealth_COVIDTherapeutic3_1>>+Name)]]
      </SELECT>
      </TD>
    <TD CLASS="strcol" >
        Date:
    	<INPUT TYPE="text" NAME="ClientHealth_COVIDTherapeutic3Date_1" VALUE="<<ClientHealth_COVIDTherapeutic3Date_1>>" ONFOCUS="select()" ONCHANGE="return vDate(this,1);" SIZE="10" >
    </TD>
  </TR>
<TR >
    <TD CLASS="strcol" >
      COVID Therapeutic 4:
      <SELECT NAME="ClientHealth_COVIDTherapeutic4_1" >
        [[DBA->selxTable(%form+xCOVIDTherapeutic+<<ClientHealth_COVIDTherapeutic4_1>>+Name)]]
      </SELECT>
      </TD>
    <TD CLASS="strcol" >
        Date:
    	<INPUT TYPE="text" NAME="ClientHealth_COVIDTherapeutic4Date_1" VALUE="<<ClientHealth_COVIDTherapeutic4Date_1>>" ONFOCUS="select()" ONCHANGE="return vDate(this,1);" SIZE="10" >
    </TD>
  </TR>

  <TR >
    <TD CLASS="strcol" COLSPAN="2" >
N95 Mask Request: 
      <INPUT TYPE="radio" NAME="ClientHealth_ClientHealthN95_1" VALUE="1" <<ClientHealth_ClientHealthN95_1=1>> > Yes
      <INPUT TYPE="radio" NAME="ClientHealth_ClientHealthN95_1" VALUE="0" <<ClientHealth_ClientHealthN95_1=0>> > No

    </TD>
  </TR>
  <TR >
    <TD CLASS="strcol" COLSPAN="2" >
COVID Home Test Kit Request: 
      <INPUT TYPE="radio" NAME="ClientHealth_ClientHealthHKR_1" VALUE="1" <<ClientHealth_ClientHealthHKR_1=1>> > Yes
      <INPUT TYPE="radio" NAME="ClientHealth_ClientHealthHKR_1" VALUE="0" <<ClientHealth_ClientHealthHKR_1=0>> > No
    </TD>
  </TR>

  <TR >



  <TR ><TD CLASS="port hdrtxt" WIDTH="50%" >Hearing / Vision</TD><TD>&nbsp;</TD></TR>
  <TR >
    <TD CLASS="strcol" >
      Hearing Screening Date:
      <INPUT TYPE="text" NAME="ClientHealth_HearingDate_1" VALUE="<<ClientHealth_HearingDate_1>>" ONFOCUS="select()" ONCHANGE="return vDate(this,1);" SIZE="10" >
    </TD>
    <TD CLASS="strcol" >&nbsp;</TD>
  </TR>
  <TR >
    <TD CLASS="strcol" COLSPAN="2" >
      <INPUT TYPE="radio" NAME="ClientHealth_HearingPass_1" VALUE="1" <<ClientHealth_HearingPass_1=1>> > Pass
      <INPUT TYPE="radio" NAME="ClientHealth_HearingPass_1" VALUE="0" <<ClientHealth_HearingPass_1=0>> > Fail
      <INPUT TYPE="radio" NAME="ClientHealth_HearingPass_1" VALUE="A" <<ClientHealth_HearingPass_1=A>> > Aided
    </TD>
  </TR>
  <TR >
    <TD CLASS="strcol" >
      Vision Screening Date:
      <INPUT TYPE="text" NAME="ClientHealth_VisionDate_1" VALUE="<<ClientHealth_VisionDate_1>>" ONFOCUS="select()" ONCHANGE="return vDate(this,1);" SIZE="10" >
    </TD>
    <TD CLASS="strcol" >&nbsp;</TD>
  </TR>
  <TR >
    <TD CLASS="strcol" COLSPAN="2" >
      <INPUT TYPE="radio" NAME="ClientHealth_VisionPass_1" VALUE="1" <<ClientHealth_VisionPass_1=1>> > Pass
      <INPUT TYPE="radio" NAME="ClientHealth_VisionPass_1" VALUE="0" <<ClientHealth_VisionPass_1=0>> > Fail
      <INPUT TYPE="radio" NAME="ClientHealth_VisionPass_1" VALUE="A" <<ClientHealth_VisionPass_1=A>> > Aided
    </TD>
  </TR>
  <TR >
    </TABLE></TD></TR>
</TABLE>
<TABLE CLASS="home fullsize" >
  <TR ><TD CLASS="port hdrtxt" COLSPAN="2" >Current biomedical conditions/complications (select New to add)</TD></TR>
  <TR >
    <TD CLASS="port hdrcol" >
      Client Problems
      <A HREF="javascript:callAjax('ListClientProblems','','ListClientProblems','&active=1&Locked=0&Client_ClientID=<<<Client_ClientID>>>&LOGINPROVID=<<<LOGINPROVID>>>&LOGINUSERID=<<<LOGINUSERID>>>&LOGINUSERDB=<<<LOGINUSERDB>>>&mlt=<<<mlt>>>&LINKID=<<<LINKID>>>','popup.pl');" TITLE="Show ONLY Active Problems for Client" >Active Only</A>
      /
      <A HREF="javascript:callAjax('ListClientProblems','','ListClientProblems','&active=0&Locked=0&Client_ClientID=<<<Client_ClientID>>>&LOGINPROVID=<<<LOGINPROVID>>>&LOGINUSERID=<<<LOGINUSERID>>>&LOGINUSERDB=<<<LOGINUSERDB>>>&mlt=<<<mlt>>>&LINKID=<<<LINKID>>>','popup.pl');" TITLE="Show ALL Problems for Client" >Show All</A>
    </TD>
  </TR>
  <TR >
    <TD "port hdrtxt" COLSPAN="2" >
<SPAN ID="ListClientProblems" >
[[myHTML->ListSel(%form+ListClientProblems+<<<Client_ClientID>>>+<<<LINKID>>>+<<<Client_Locked_1>>>)]]
</SPAN>
    </TD>
  </TR>
  </TR>
    <TD CLASS="strcol" >Previous conditions described:</TD>
    <TD CLASS="strcol" ><<MedHx_BioMedical_1>></TD>
  </TR>
</TABLE>

<TABLE CLASS="main fullsize" >
  <TR >
    <TD CLASS="numcol" >
      <INPUT TYPE=submit ONCLICK="return validate(this.form);" NAME="UpdateTables=all&[[myForm->genLink(ClientIntake+ListClientMeds.cgi)]]" VALUE="Add/Update -> Medications">
      <INPUT TYPE="submit" ONCLICK="return validate(this.form);" NAME="UpdateTables=all&misPOP=1" VALUE="Add/Update">
    </TD>
  </TR>
</TABLE>

</LOADHIDDEN>
</FORM>
<SCRIPT LANGUAGE="JavaScript">
document.HealthHistory.elements[0].focus();
// just to OPENTABLES...  <<<ClientCDCHA_ClientID_1>>>

     if('M' === '<<Client_Gend_1>>') {
        //alert("Hiding this section for Gender=Male");
     	document.getElementById("pregnant_sec").style.visibility="hidden";
	document.getElementById("pregnant_sec_2").style.visibility="hidden";
	document.getElementById("pregnant_sec_3").style.visibility="hidden";
     }
</script>
[[myHTML->rightpane(%form+search)]]
