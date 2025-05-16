[[myHTML->newPage(%form+Client Health History+++++accordion)]]

<SCRIPT LANGUAGE="JavaScript" SRC="/src/cgi/js/vEntry.js"> </SCRIPT>
<SCRIPT LANGUAGE="JavaScript" SRC="/src/cgi/js/vClientHealthHistory.js"> </SCRIPT>
<SCRIPT LANGUAGE="JavaScript" SRC="/src/cgi/js/ajaxrequest.js"> </SCRIPT>
<SCRIPT LANGUAGE="JavaScript" SRC="/src/cgi/js/vDate.js"> </SCRIPT>
<SCRIPT LANGUAGE="JavaScript" SRC="/src/cgi/js/vNum.js"> </SCRIPT>
<LINK HREF="/cfg/menuV2.css" REL="stylesheet" TYPE="text/css" >
<SCRIPT type="text/javascript" src="/cgi/menu/js/menuV2.js" ></SCRIPT>

<FORM NAME="HealthHistory" ACTION="/cgi/bin/mis.cgi" METHOD="POST" >
<TABLE CLASS="main fullsize" >
  <TR >
    <TD CLASS="strcol" >[[myHTML->getHTML(%form+MU.menu+1)]]</TD>
    <TD CLASS="strcol" >
      <<<Client_FName_1>>> <<<Client_MName_1>>> <<<Client_LName_1>>> (<<<Client_ClientID_1>>>) <<<Client_SSN_1>>>
      <BR>
      Health History Page
    </TD>
    <TD CLASS="numcol" >[[gHTML->setLINKS(%form+back)]]</TD>
  </TR>
</TABLE>

<P>
<TABLE CLASS="home fullsize" >
  <TR ><TD CLASS="port hdrtxt" COLSPAN="2" >ALLERGIES</TD></TR>
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
</TABLE>

<P>
<TABLE CLASS="home fullsize" >
  <TR ><TD CLASS="port hdrtxt" COLSPAN="2" >MEDICATIONS</TD></TR>
  <TR >
    <TD CLASS="port hdrtxt" WIDTH="50%" >
      Medication Information
      <A HREF="javascript:callAjax('ShowClientMeds','','ShowClientMeds','&active=1&Locked=0&Client_ClientID=<<<Client_ClientID>>>&LOGINPROVID=<<<LOGINPROVID>>>&LOGINUSERID=<<<LOGINUSERID>>>&LINKID=<<<LINKID>>>&mlt=<<<mlt>>>&LOGINUSERDB=<<<LOGINUSERDB>>>','popup.pl');" TITLE="Show ONLY Active Medications for Client">Active Only</A>
      /
      <A HREF="javascript:callAjax('ShowClientMeds','','ShowClientMeds','&active=0&Locked=0&Client_ClientID=<<<Client_ClientID>>>&LOGINPROVID=<<<LOGINPROVID>>>&LOGINUSERID=<<<LOGINUSERID>>>&LINKID=<<<LINKID>>>&mlt=<<<mlt>>>&LOGINUSERDB=<<<LOGINUSERDB>>>','popup.pl');" TITLE="Show ALL Medications for Client">Show All</A>
    </TD>
    <TD CLASS="numcol" WIDTH="50%" >
      <A HREF="javascript:ReportWindow('/src/cgi/bin/mis.cgi?view=ClientMUTI.cgi&Client_ClientID=<<<Client_ClientID>>>&mlt=<<<mlt>>>&misLINKS=<<<misLINKS>>>','NewCrop',900,1500);" TITLE="Manually Add NewCrop Medications for testing only">Add NewCrop Medications</A>
    </TD>
  </TR>
  <TR >
    <TD COLSPAN="2" >
<SPAN ID="ShowClientMeds" >
[[myHTML->ListSel(%form+ShowClientMeds+<<<Client_ClientID>>>+<<<LINKID>>>+<<<Client_Locked_1>>>)]]
</SPAN>
    </TD>
  </TR>
  <TR >
    <TD CLASS="port hdrtxt" >
      Administered Medications are those with PrescriptionDate = ContactDate
    </TD>
    <TD WIDTH="50%" >&nbsp;</TD>
  </TR>
</TABLE>

<P>
<TABLE CLASS="home fullsize" >
  <TR ><TD CLASS="port hdrtxt" COLSPAN="2" >PROBLEMS</TD></TR>
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

<P>
<TABLE CLASS="home fullsize" >
  <TR ><TD CLASS="port hdrtxt" COLSPAN="2" >ENCOUNTERS</TD></TR>
  <TR >
    <TD COLSPAN="2" >
<SPAN ID="ShowClientNotes" >
[[myHTML->ListSel(%form+ShowClientNotes+<<<Client_ClientID>>>+<<<LINKID>>>+<<<Client_Locked_1>>>)]]
</SPAN>
    </TD>
  </TR>
</TABLE>

<P>
<TABLE CLASS="home fullsize" >
  <TR ><TD CLASS="port hdrtxt" COLSPAN="2" >IMMUNIZATIONA</TD></TR>
  <TR ><TD CLASS="port hdrtxt" WIDTH="50%" >Vaccine Information</TD><TD WIDTH="50%" >&nbsp;</TD></TR>
  <TR >
    <TD COLSPAN="2" >
<SPAN ID="ListClientVaccines" >
[[myHTML->ListSel(%form+ListClientVaccines+<<<Client_ClientID>>>+<<<LINKID>>>+<<<Client_Locked_1>>>)]]
</SPAN>
    </TD>
  </TR>
  <TR ><TD CLASS="strcol" COLSPAN="2" >Are your immunizations up to date (child &amp; adolescent)?</TD></TR>
  <TR >
    <TD CLASS="strcol" >If no, What are you lacking?</TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="text" NAME="ClientHealth_ImmunizeDesc_1" VALUE="<<ClientHealth_ImmunizeDesc_1>>" ONFOCUS="select()" SIZE=70>
    </TD>
  </TR>
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
</TABLE>

<P>
<TABLE CLASS="home fullsize" >
  <TR ><TD CLASS="port hdrtxt" COLSPAN="2" >VITAL SIGNS</TD></TR>
  <TR ><TD CLASS="port hdrtxt" WIDTH="50%" >Vitals Information</TD><TD WIDTH="50%" >&nbsp;</TD></TR>
  <TR >
    <TD COLSPAN="2" >
<SPAN ID="ListClientVitalSigns" >
[[myHTML->ListSel(%form+ListClientVitalSigns+<<<Client_ClientID>>>+<<<LINKID>>>+<<<Client_Locked_1>>>)]]
</SPAN>
    </TD>
  </TR>
</TABLE>

<P>
<TABLE CLASS="home fullsize" >
  <TR ><TD CLASS="port hdrtxt" COLSPAN="2" >SUBSTANCE ABUSE</TD></TR>
  <TR ><TD CLASS="hdrtxt" COLSPAN="2" >Tobacco/Nicotine Use</TD></TR></TR>
  <TR >
    <TD CLASS="strcol" COLSPAN="2" >
      How many times per day do you use nicotine?
      <INPUT TYPE="text" NAME="MedHx_DailyTobaccoUse_1" VALUE="<<MedHx_DailyTobaccoUse_1>>" ONFOCUS="select()" MAXLENGTH="2" SIZE="2" >
    </TD">
  </TR>
  <TR ><TD CLASS="port hdrtxt" COLSPAN="2" >TOBACCO SCREEN<BR>(add multiple screenings from the Client Page Testing menu)</TD></TR>
  <TR CLASS="list hdrcol" >
    <TD COLSPAN="2" >
<A HREF="javascript:InputWindow('/src/cgi/bin/mis.cgi?view=ListClientSATobacco.cgi&Client_ClientID=<<<Client_ClientID_1>>>&mlt=<<<mlt>>>&misLINKS=<<<misLINKS>>>&NONAVIGATION=1','TOBACCO',900,1200)" CLASS="mybutton" >ENTER TOBACCO Screening (add new or edit last screening)</A>
    </TD>
  </TR>
</TABLE>

<P>
<TABLE CLASS="home fullsize" >
  <TR ><TD CLASS="port hdrtxt" COLSPAN="2" >PROCEDURES</TD></TR>
  <TR ><TD CLASS="port hdrtxt" WIDTH="50%" >Procedures Information</TD><TD WIDTH="50%" >&nbsp;</TD></TR>
  <TR >
    <TD COLSPAN="2" >
<SPAN ID="ListClientProcedures" >
[[myHTML->ListSel(%form+ListClientProcedures+<<<Client_ClientID>>>+<<<LINKID>>>+<<<Client_Locked_1>>>)]]
</SPAN>
    </TD>
  </TR>
</TABLE>

<P>
<TABLE CLASS="home fullsize" >
  <TR ><TD CLASS="port hdrtxt" COLSPAN="2" >LABS</TD></TR>
  <TR ><TD CLASS="port hdrtxt" WIDTH="50%" >Lab Results Information</TD><TD WIDTH="50%" >&nbsp;</TD></TR>
  <TR >
    <TD COLSPAN="2" >
<SPAN ID="ListClientLabs" >
[[myHTML->ListSel(%form+ListClientLabs+<<<Client_ClientID>>>+<<<LINKID>>>+<<<Client_Locked_1>>>)]]
</SPAN>
    </TD>
  </TR>
</TABLE>

<P>
<TABLE CLASS="home fullsize" >
  <TR ><TD CLASS="port hdrtxt" COLSPAN="2" >UDI</TD></TR>
  <TR ><TD CLASS="port hdrtxt" WIDTH="50%" >Part of LABS above:</TD><TD WIDTH="50%" >&nbsp;</TD></TR>
</TABLE>

<P>
<TABLE CLASS="home fullsize" >
  <TR ><TD CLASS="port hdrtxt" COLSPAN="2" >HEALTH INFORMATION</TD></TR>
  <TR ><TD CLASS="port hdrtxt" WIDTH="50%" >Overall Health Status</TD><TD>&nbsp;</TD></TR>
  <TR >
    <TD CLASS="strcol" COLSPAN="2" >
      <SELECT NAME="ClientHealth_OverallHealth_1" >
        [[DBA->selxTable(%form+xHealthStatus+<<ClientHealth_OverallHealth_1>>+ConceptName ConceptCode)]]
      </SELECT>
    </TD>
  </TR>
  <TR ><TD CLASS="port hdrtxt" >Handicaps/Disabilities/Limitations/Challenges</TD></TR>
  <TR ><TD CLASS="strcol" COLSPAN="2" >Are you experiencing any chronic medical, ambulatory, speech, hearing or visual functioning problems?</TD></TR>
  <TR>
    <TD CLASS="strcol" >Handicap 1</TD>
    <TD CLASS="strcol" COLSPAN="2" >
      <SELECT NAME="ClientDevl_Handicap1_1" ONCHANGE="callAjax('FunctionalStatus','','selFS1','&name=ClientDevl_FuncStatus1_1&Handicap='+this.value,'popup.pl');" >
        [[DBA->selxTable(%form+xHandicap+<<ClientDevl_Handicap1_1>>+CDC Descr)]]
      </SELECT>
    </TD>
  </TR>
  <TR>
    <TD CLASS="strcol" >Functional Status 1</TD>
    <TD CLASS="strcol" >
      <SPAN ID="selFS1">
      <SELECT NAME="ClientDevl_FuncStatus1_1" >
        [[DBA->selxTable(%form+xFunctionalStatus+<<ClientDevl_FuncStatus1_1>>+ConceptName+++Handicap='<<ClientDevl_Handicap1_1>>')]]
      </SELECT>
      </SPAN>
    </TD>
  </TR>
  <TR>
    <TD CLASS="strcol" >Handicap 2</TD>
    <TD CLASS="strcol" COLSPAN="2" >
      <SELECT NAME="ClientDevl_Handicap2_1" ONCHANGE="callAjax('FunctionalStatus','','selFS2','&name=ClientDevl_FuncStatus2_1&Handicap='+this.value,'popup.pl');" >
        [[DBA->selxTable(%form+xHandicap+<<ClientDevl_Handicap2_1>>+CDC Descr)]]
      </SELECT>
    </TD>
  </TR>
  <TR>
    <TD CLASS="strcol" >Functional Status 2</TD>
    <TD CLASS="strcol" >
      <SPAN ID="selFS2">
      <SELECT NAME="ClientDevl_FuncStatus2_1" >
        [[DBA->selxTable(%form+xFunctionalStatus+<<ClientDevl_FuncStatus2_1>>+ConceptName+++Handicap='<<ClientDevl_Handicap2_1>>')]]
      </SELECT>
      </SPAN>
    </TD>
  </TR>
  <TR>
    <TD CLASS="strcol" >Handicap 3</TD>
    <TD CLASS="strcol" COLSPAN="2" >
      <SELECT NAME="ClientDevl_Handicap3_1" ONCHANGE="callAjax('FunctionalStatus','','selFS3','&name=ClientDevl_FuncStatus3_1&Handicap='+this.value,'popup.pl');" >
        [[DBA->selxTable(%form+xHandicap+<<ClientDevl_Handicap3_1>>+CDC Descr)]]
      </SELECT>
    </TD>
  </TR>
  <TR>
    <TD CLASS="strcol" >Functional Status 3</TD>
    <TD CLASS="strcol" >
      <SPAN ID="selFS3">
      <SELECT NAME="ClientDevl_FuncStatus3_1" >
        [[DBA->selxTable(%form+xFunctionalStatus+<<ClientDevl_FuncStatus3_1>>+ConceptName+++Handicap='<<ClientDevl_Handicap3_1>>')]]
      </SELECT>
      </SPAN>
    </TD>
  </TR>
  <TR>
    <TD CLASS="strcol" >Handicap 4</TD>
    <TD CLASS="strcol" COLSPAN="2" >
      <SELECT NAME="ClientDevl_Handicap4_1" ONCHANGE="callAjax('FunctionalStatus','','selFS4','&name=ClientDevl_FuncStatus4_1&Handicap='+this.value,'popup.pl');" >
        [[DBA->selxTable(%form+xHandicap+<<ClientDevl_Handicap4_1>>+CDC Descr)]]
      </SELECT>
    </TD>
  </TR>
  <TR>
    <TD CLASS="strcol" >Functional Status 4</TD>
    <TD CLASS="strcol" >
      <SPAN ID="selFS4">
      <SELECT NAME="ClientDevl_FuncStatus4_1" >
        [[DBA->selxTable(%form+xFunctionalStatus+<<ClientDevl_FuncStatus4_1>>+ConceptName+++Handicap='<<ClientDevl_Handicap4_1>>')]]
      </SELECT>
      </SPAN>
    </TD>
  </TR>
  <TR ><TD CLASS="strcol" COLSPAN="2" >Client's adjustment to disabilities or disorders?</TD></TR>
  <TR >
    <TD CLASS="strcol" COLSPAN="2" >
      <TEXTAREA NAME="MedHx_AdjDis_1" COLS="90" ROWS="2" WRAP=virtual ><<MedHx_AdjDis_1>></TEXTAREA>
    </TD>
  </TR>
</TABLE>

<TABLE CLASS="main fullsize" >
  <TR >
    <TD CLASS="numcol" >
      <INPUT TYPE="submit" ONCLICK="return validate(this.form);" NAME="UpdateTables=all&[[myForm->genLink(ClientIntake+ClientMUB.cgi)]]" VALUE="Add/Update -> Client Overall Health">
      <INPUT TYPE="submit" ONCLICK="return validate(this.form);" NAME="UpdateTables=all&misPOP=1" VALUE="Add/Update">
    </TD>
  </TR>
</TABLE>

</LOADHIDDEN>
</FORM>
<SCRIPT LANGUAGE="JavaScript">
document.HealthHistory.elements[0].focus();
// just to OPENTABLES...  <<<ClientCDCHA_ClientID_1>>>
</SCRIPT>

[[myHTML->rightpane(%form+search)]]
