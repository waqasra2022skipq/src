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
  <TR ><TD CLASS="port hdrtxt" WIDTH="50%" >Hospitalization History</TD><TD>&nbsp;</TD></TR>
  <TR >
    <TD CLASS="strcol" COLSPAN="2" >
      How many times in your life have you been hospitalized overnight for medical problems?
      <BR>� Include O.D.'s and D.T.'s. Exclude detox, alcohol/drug, psychiatric treatment and childbirth (if no complications).
    </TD>
  </TR>
  <TR >
    <TD CLASS="strcol" COLSPAN="2" >
      <INPUT TYPE="text" NAME="ClientHealth_HospOverNight_1" VALUE="<<ClientHealth_HospOverNight_1>>" ONFOCUS="select()" ONCHANGE="return vNum(this,0,99);" SIZE=2>
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
  <TR >
    <TD CLASS="strcol" >Client is pregnant? If so, enter Est. Date of Birth/Delivery</TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="text" NAME="ClientIntake_PregnantDate_1" VALUE="<<ClientIntake_PregnantDate_1>>" ONFOCUS="select()" ONCHANGE="return vDate(this,1);" SIZE="10" >
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
        [[DBA->selxTable(%form+xSexualOrientation+<<ClientHealth_SexPref_1>>+ConceptName ConceptCode)]]
      </SELECT>
    </TD>
  </TR>
  <TR >
    <TD CLASS="strcol" >Gender Identity/Identify (if applicable, select one)?</TD>
    <TD CLASS="strcol" >
      <SELECT NAME="ClientHealth_SexID_1" >
        [[DBA->selxTable(%form+xGenderIdentity+<<ClientHealth_SexID_1>>+ConceptName ConceptCode)]]
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

<TABLE CLASS="main fullsize" >
  <TR >
    <TD CLASS="numcol" >
      <INPUT TYPE="submit" ONCLICK="return validate(this.form);" NAME="UpdateTables=all&[[myForm->genLink(ClientIntake+ClientMUO.cgi)]]" VALUE="Add/Update -> Health Observations">
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
