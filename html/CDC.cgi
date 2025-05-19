[[myHTML->newPage(%form+Customer Data Core Information)]]

<SCRIPT LANGUAGE="JavaScript" SRC="/src/cgi/js/chkLock.js" > </SCRIPT>
<SCRIPT LANGUAGE="JavaScript" SRC="/src/cgi/js/NoEnter.js" > </SCRIPT>
<SCRIPT LANGUAGE="JavaScript" SRC="/src/cgi/js/vEntry.js" > </SCRIPT>
<SCRIPT type="text/javascript" src="/src/cgi/js/ajaxrequest.js"></SCRIPT>
<SCRIPT LANGUAGE="JavaScript" SRC="/src/cgi/js/vCDC.js" > </SCRIPT>
<SCRIPT LANGUAGE="JavaScript" SRC="/src/cgi/js/vZip.js" > </SCRIPT>
<SCRIPT LANGUAGE="JavaScript" SRC="/src/cgi/js/Utils.js" > </SCRIPT>
<SCRIPT LANGUAGE="JavaScript" SRC="/src/cgi/js/vDate.js" > </SCRIPT>
<SCRIPT LANGUAGE="JavaScript" SRC="/src/cgi/js/vTime.js" > </SCRIPT>
<SCRIPT LANGUAGE="JavaScript" SRC="/src/cgi/js/vNum.js" > </SCRIPT>

<FORM NAME="CDC" ACTION="/src/cgi/bin/mis.cgi" METHOD="POST" >
<TABLE CLASS="main fullsize" >
  <TR >
    <TD CLASS="strcol" >
      <<<Client_FName_1>>> <<<Client_MName_1>>> <<<Client_LName_1>>> (<<<Client_ClientID_1>>>) <<<Client_SSN_1>>>
      <BR>
      Client Data Core
    </TD>
    <TD CLASS="numcol" >[[gHTML->setLINKS(%form+back)]]</TD>
  </TR>
</TABLE>
[[CDC->genHTML(%form+<<<Insurance_InsID_1>>>+<<<ClientPrAuth_ID_1>>>)]]
<TABLE CLASS="home fullsize" >
  <TR >
    <TD CLASS="port hdrtxt" COLSPAN="2" >
      CDC Information
      <BR>Identifying Information
    </TD>
  </TR>
  <TR>
    <TD CLASS="strcol" >First Name</TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="text" NAME="Client_FName_1" VALUE="<<Client_FName_1>>" ONCHANGE="return stringFilter(this,' !@#$%^&*()',1,0,1);" ONFOCUS="select()" SIZE="20" >
    </TD>
  </TR>
  <TR >
    <TD CLASS="strcol" >Last Name</TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="text" NAME="Client_LName_1" VALUE="<<Client_LName_1>>" ONCHANGE="return stringFilter(this,' !@#$%^&*()',1,0,1);" ONFOCUS="select()" SIZE="20" >
    </TD>
  </TR>
  <TR >
    <TD CLASS="strcol" >Maiden Name</TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="text" NAME="Client_MaidenName_1" VALUE="<<Client_MaidenName_1>>" ONCHANGE="return stringFilter(this,' !@#$%^&*()',1,0,1);" ONFOCUS="select()" SIZE="20" >
    </TD>
  </TR>
  <TR >
    <TD CLASS="strcol" >Middle Name</TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="text" NAME="Client_MName_1" VALUE="<<Client_MName_1>>" ONCHANGE="return stringFilter(this,' !@#$%^&*()',1,0,1);" ONFOCUS="select()" SIZE="10" >
    </TD>
  </TR>
  <TR >
    <TD CLASS="strcol" >Address 1</TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="text" NAME="Client_Addr1_1" VALUE="<<Client_Addr1_1>>" ONCHANGE="return stringFilter(this,':!@#$%^&*()',0,1,1);" ONFOCUS="select()" SIZE="30" >
    </TD>
  </TR>
  <TR >
    <TD CLASS="strcol" >Address 2</TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="text" NAME="Client_Addr2_1" VALUE="<<Client_Addr2_1>>" ONCHANGE="return stringFilter(this,':!@#$%^&*()',0,1,1);" ONFOCUS="select()" SIZE="30" >
    </TD>
  </TR>
  <TR >
    <TD CLASS="strcol" >City</TD>
    <TD CLASS="strcol" >
      <SELECT NAME="Client_City_1">
        [[DBA->selxTable(%form+xOKCities+<<Client_City_1>>+ID)]]
      </SELECT> 
    </TD>
  </TR>
  <TR >
    <TD CLASS="strcol" >County</TD>
    <TD CLASS="strcol" >
      <SELECT NAME="Client_County_1" >[[DBA->selxTable(%form+xCountyOK+<<Client_County_1>>+CDC Descr)]]</SELECT> 
    </TD>
  </TR>
  <TR >
    <TD CLASS="strcol" >State</TD>
    <TD CLASS="strcol" >
      <SELECT NAME="Client_ST_1">
        [[DBA->selxTable(%form+xState+<<Client_ST_1>>+Descr)]]
      </SELECT>
    </TD>
  </TR>
  <TR >
    <TD CLASS="strcol" >Zip</TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="text" NAME="Client_Zip_1" VALUE="<<Client_Zip_1>>" ONFOCUS="select()" MAXLENGTH="10" SIZE="10" ONCHANGE="return vZip(this)" >
    </TD>
  </TR>
  <TR ><TD CLASS="port hdrtxt" COLSPAN="2" >Section I</TD></TR>
  <TR >
    <TD CLASS="strcol" >Transaction Type</TD>
    <TD CLASS="strcol" >
      <SELECT NAME="ClientPrAuthCDC_TransType_1" >[[DBA->selTransType(%form+<<<ClientPrAuth_ClientID_1>>>+<<ClientPrAuthCDC_TransType_1>>)]]</SELECT>
      <A HREF="http://forms.okmis.com/misdocs/CDCTT.html" TARGET="popup" ONCLICK="window.open('http://forms.okmis.com/misdocs/CDCTT.html', 'popup', 'width=900,height=700,menubar=1,scrollbars=1,toolbar=1,status=1,resizable=1'); return false" >explain</A> 
    </TD>
  </TR>
  <TR >
    <TD CLASS="strcol" >Transaction/Contact Date</TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="text" NAME="ClientPrAuthCDC_TransDate_1" VALUE="<<ClientPrAuthCDC_TransDate_1>>" ONFOCUS="select()" ONCHANGE="return vDate(this)" MAXLENGTH="10" SIZE="10" >
      <A HREF="http://forms.okmis.com/misdocs/CDCTT.html" TARGET="popup" ONCLICK="window.open('http://forms.okmis.com/misdocs/CDCTD.html', 'popup', 'width=900,height=700,menubar=1,scrollbars=1,toolbar=1,status=1,resizable=1'); return false" >explain</A> 
    </TD>
  </TR>
  <TR >
    <TD CLASS="strcol" >Transaction/Contact Time</TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="text" NAME="ClientPrAuthCDC_TransTime_1" VALUE="<<ClientPrAuthCDC_TransTime_1>>" ONFOCUS="select()" ONCHANGE="return vTime(this,1,this)" MAXLENGTH="10" SIZE="10" >
    </TD>
  </TR>
  <TR >
    <TD CLASS="strcol" >Date of Birth</TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="text" NAME="Client_DOB_1" VALUE="<<Client_DOB_1>>" ONFOCUS="select()" ONCHANGE="return vDate(this,0,this.form,'Client_Age')" SIZE="10" >
      Age:
      <INPUT TYPE="text" NAME="Client_Age" VALUE="<<Client_Age>>" ONFOCUS="form.ClientIntake_ServiceFocus_1.focus();" SIZE="4" >
    </TD>
  </TR>
  <TR >
    <TD CLASS="strcol" >
      <U>Service Focus</U>
      <A HREF="/docs/Prior Auth_CDC Service Focus Requirements with AutoPA_20100601.pdf" TARGET="popup" ONCLICK="window.open('/docs/Prior Auth_CDC Service Focus Requirements with AutoPA_20100601.pdf', 'popup', 'width=900,height=700,menubar=1,scrollbars=1,toolbar=1,status=1,resizable=1'); return false">(Requirements)</A> 
    </TD>
    <TD CLASS="strcol" >
      <SELECT NAME="ClientIntake_ServiceFocus_1" SIZE="10" >
        [[DBA->selxTable(%form+xServiceFocus+<<ClientIntake_ServiceFocus_1>>+Descr)]]
      </SELECT> 
    </TD>
  </TR>
  <TR >
    <TD CLASS="strcol" >
      [[myHTML->setxTable(%form+xRaces+<<Client_Race_1>>+Client_Race_1+checkbox+0)]]
    </TD>
    <TD CLASS="strcol" >
      <SPAN ID="Client_Race_1_display" ></SPAN>
    </TD>
  </TR>
  <TR >
    <TD CLASS="strcol" >
      [[myHTML->setxTable(%form+xEthnicity+<<Client_Ethnicity_1>>+Client_Ethnicity_1+checkbox+0)]]
    </TD>
    <TD CLASS="strcol" >
      <SPAN ID="Client_Ethnicity_1_display" ></SPAN>
    </TD>
  </TR>
  <TR >
    <TD CLASS="strcol" >SSN</TD>
    <TD CLASS="strcol" ><<<Client_SSN_1>>></TD>
  </TR>
  <TR >
    <TD CLASS="strcol" >Birth Gender</TD>
    <TD CLASS="strcol" >
      <SELECT NAME="Client_Gend_1" >[[DBA->selxTable(%form+xGend+<<Client_Gend_1>>)]]</SELECT> 
    </TD>
  </TR>
  <TR >
    <TD CLASS="strcol" >Primary Referral</TD>
    <TD CLASS="strcol" >
      Search: <INPUT TYPE="text" ID="SearchRefBy1" NAME="SearchRefBy1" VALUE="" ONFOCUS="select()" ONCHANGE="callAjax('Agency','<<ClientReferrals_ReferredBy1NPI_1>>','selRefBy1','&name=ClientReferrals_ReferredBy1NPI_1&pattern='+this.value,'popup.pl');" SIZE="60" >
<BR><SPAN ID="selRefBy1"></SPAN>
    </TD>
  </TR>
  <TR >
    <TD CLASS="strcol" >Referral Type</TD>
    <TD CLASS="strcol" >
      <SELECT NAME="ClientReferrals_ReferredBy1Type_1" >
        [[DBA->selxTable(%form+xReferralTypes+<<ClientReferrals_ReferredBy1Type_1>>+CDC Descr)]]
      </SELECT>
    </TD>
  </TR>
  <TR >
    <TD CLASS="strcol" >Secondary Referral</TD>
    <TD CLASS="strcol" >
      Search: <INPUT TYPE="text" ID="SearchRefBy2" NAME="SearchRefBy2" VALUE="" ONFOCUS="select()" ONCHANGE="callAjax('Agency','<<ClientReferrals_ReferredBy2NPI_1>>','selRefBy2','&name=ClientReferrals_ReferredBy2NPI_1&pattern='+this.value,'popup.pl');" SIZE="60" >
<BR><SPAN ID="selRefBy2"></SPAN>
    </TD>
  </TR>
  <TR >
    <TD CLASS="strcol" >Referral Type</TD>
    <TD CLASS="strcol" >
      <SELECT NAME="ClientReferrals_ReferredBy2Type_1" >
        [[DBA->selxTable(%form+xReferralTypes+<<ClientReferrals_ReferredBy2Type_1>>+CDC Descr)]]
      </SELECT>
    </TD>
  </TR>
  
  <tr>
    <td class="strcol">
      #3. Risk
    </td>
  </tr>
  <tr>
    <td class="strcol indent">
      a. Does this individual pose a danger to themselves or others?
    </td>
    <td class="strcol">
      <input type="radio" name="ClientReferrals_Harmfulintent_1" value="0" checked=""> Neither

      <input type="radio" name="ClientReferrals_Harmfulintent_1" value="1" <<ClientReferrals_Harmfulintent_1=1>> > Suicidal

      <input type="radio" name="ClientReferrals_Harmfulintent_1" value="2" <<ClientReferrals_Harmfulintent_1=2>> > Homicidal

      <input type="radio" name="ClientReferrals_Harmfulintent_1" value="3" <<ClientReferrals_Harmfulintent_1=3>> > Both
    </td>
  </tr>
  <tr>
    <td class="strcol indent" style="padding-left:55px">
      (i) Do you have a plan?
    </td>
    <td class="strcol">
      <input type="radio" name="ClientReferrals_SuicidePlan_1" value="1" <<ClientReferrals_SuicidePlan_1=1>> > yes
      <input type="radio" name="ClientReferrals_SuicidePlan_1" value="" <<ClientReferrals_SuicidePlan_1=>> > no
    </td>
  </tr>
  <tr>
    <td class="strcol indent" style="padding-left:55px">
      (ii). Do you have thoughts of hurting others?
    </td>
    <td class="strcol">
      <input type="radio" name="ClientReferrals_RiskOthers_1" value="1" <<ClientReferrals_RiskOthers_1=1>> > yes
      <input type="radio" name="ClientReferrals_RiskOthers_1" value=""  <<ClientReferrals_RiskOthers_1=>> > no
    </td>
  </tr>


  <TR ><TD CLASS="strcol" COLSPAN="2" >County of Residence and Zip (see above)</TD></TR>
  <TR ><TD CLASS="port hdrtxt" COLSPAN="2" >Section II & III</TD></TR>
  <TR >
    <TD CLASS="strcol" >Client Residence</TD>
    <TD CLASS="strcol" >
      <SELECT NAME="ClientRelations_Residence_1" >
        [[DBA->selxTable(%form+xResidence+<<ClientRelations_Residence_1>>+CDC Descr)]]
      </SELECT>
    </TD>
  </TR>
  <TR >
    <TD CLASS="strcol" >Structure of family you live with?</TD>
    <TD CLASS="strcol" >
      <SELECT NAME="ClientRelations_LivesWith_1" >
        [[DBA->selxTable(%form+xLivesWith+<<ClientRelations_LivesWith_1>>+APS Descr)]]
      </SELECT>
    </TD>
  </TR>
  <TR >
    <TD CLASS="strcol" >Client has been continuously homeless for a year or more?</TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="radio" NAME="ClientRelations_HomelessLong_1" VALUE="1" <<ClientRelations_HomelessLong_1=1>> > Yes
      <INPUT TYPE="radio" NAME="ClientRelations_HomelessLong_1" VALUE="0" <<ClientRelations_HomelessLong_1=0>> > No
    </TD>
  </TR>
  <TR >
    <TD CLASS="strcol" >Client has had at least 4 episodes of homelessness in the past 3 years?</TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="radio" NAME="ClientRelations_HomelessMany_1" VALUE="1" <<ClientRelations_HomelessMany_1=1>> > Yes
      <INPUT TYPE="radio" NAME="ClientRelations_HomelessMany_1" VALUE="0" <<ClientRelations_HomelessMany_1=0>> > No
    </TD>
  </TR>
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
  <TR >
    <TD CLASS="strcol" >What is the highest grade in school you have satisfactorily completed?</TD>
    <TD CLASS="strcol" >
      <SELECT NAME="ClientEducation_SchoolGrade_1" >
        [[DBA->selxTable(%form+xSchoolGrades+<<ClientEducation_SchoolGrade_1>>+Descr ID)]]
      </SELECT> 
    </TD>
  </TR>
  <TR>
    <TD CLASS="strcol" >Current school status?</TD>
    <TD CLASS="strcol" >
      <SELECT NAME="ClientIntake_SchoolStat_1" >
        [[DBA->selxTable(%form+xSchoolStat+<<ClientIntake_SchoolStat_1>>+Descr)]]
      </SELECT>
    </TD>
  </TR>
  <TR>
    <TD CLASS="strcol" >
      At any time in the past three months, has this person attended school/college? 
    </TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="radio" NAME="ClientIntake_SchoolLast3_1" VALUE="1" <<ClientIntake_SchoolLast3_1=1>> > Yes
      <INPUT TYPE="radio" NAME="ClientIntake_SchoolLast3_1" VALUE="0" <<ClientIntake_SchoolLast3_1=0>> > No
    </TD>
  </TR>
  <TR>
    <TD CLASS="strcol" >What grade are you currently attending?</TD>
    <TD CLASS="strcol" >
      <SELECT NAME="ClientEducation_CurrentGrade_1" >
        [[DBA->selxTable(%form+xSchoolGrades+<<ClientEducation_CurrentGrade_1>>+Descr ID)]]
      </SELECT> 
    </TD>
  </TR>
  <TR>
    <TD CLASS="strcol" >Military Service?</TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="radio" NAME="ClientIntake_MilFlag_1" VALUE="0" <<ClientIntake_MilFlag_1=0>> > None
      <INPUT TYPE="radio" NAME="ClientIntake_MilFlag_1" VALUE="1" <<ClientIntake_MilFlag_1=1>> > Active
      <INPUT TYPE="radio" NAME="ClientIntake_MilFlag_1" VALUE="2" <<ClientIntake_MilFlag_1=2>> > Reserve
      <INPUT TYPE="radio" NAME="ClientIntake_MilFlag_1" VALUE="3" <<ClientIntake_MilFlag_1=3>> > Discharged
      <INPUT TYPE="radio" NAME="ClientIntake_MilFlag_1" VALUE="4" <<ClientIntake_MilFlag_1=4>> > Retired
    </TD>
  </TR>
  <TR >
    <TD CLASS="strcol" >Marital Status</TD>
    <TD CLASS="strcol" >
      <SELECT NAME="ClientRelations_MarStat_1" >
        [[DBA->selxTable(%form+xMarStat+<<ClientRelations_MarStat_1>>+Descr Text)]]
      </SELECT>
    </TD>
  </TR>
  <TR >
    <TD CLASS="strcol" >Client is pregnant? If so, enter Est. Date of Birth/Delivery</TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="text" NAME="ClientIntake_PregnantDate_1" VALUE="<<ClientIntake_PregnantDate_1>>" ONFOCUS="select()" ONCHANGE="return vDate(this,1);" SIZE="10" >
    </TD>
  </TR>
  <TR ><TD CLASS="hdrtxt" COLSPAN="2" >Income including SSI and SSDI</TD></TR>
  <TR >
    <TD CLASS="port hdrtxt" COLSPAN="2" >
<SPAN ID="ListClientIncome" >
[[myHTML->ListSel(%form+ListClientIncome+<<<Client_ClientID>>>+<<<LINKID>>>+<<<Client_Locked_1>>>)]]
</SPAN>
    </TD>
  </TR>
  <TR >
    <TD CLASS="strcol" >Number of people who contribute to or must live on the total annual income: (1-15)</TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="text" NAME="ClientResources_IncomeDeps_1" VALUE="<<ClientResources_IncomeDeps_1>>" ONFOCUS="select()" ONCHANGE="return vNum(this,1,15);" SIZE="5">
    </TD>
  </TR>
  <TR ><TD CLASS="strcol" COLSPAN="2" ><U>- Add Medicare and Medicaid insurances from Client Page</U></TD></TR>
  <TR>
    <TD CLASS="strcol" >Does client SPEAK English well?</TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="radio" NAME="ClientSocial_SpeakEnglish_1" VALUE="1" <<ClientSocial_SpeakEnglish_1=1>> > Yes
      <INPUT TYPE="radio" NAME="ClientSocial_SpeakEnglish_1" VALUE="0" <<ClientSocial_SpeakEnglish_1=0>> > No
    </TD>
  </TR>
  <TR >
    <TD CLASS="strcol" >Preferred Language:</TD>
    <TD CLASS="strcol" >
      <SELECT NAME="ClientSocial_PreLang_1">
        [[DBA->selxTable(%form+xLanguages+<<ClientSocial_PreLang_1>>+English)]]
      </SELECT>
    </TD>
  </TR>
  <TR >
    <TD CLASS="strcol" >Secondary Language:</TD>
    <TD CLASS="strcol" >
      <SELECT NAME="ClientSocial_SecLang_1">
        [[DBA->selxTable(%form+xLanguages+<<ClientSocial_SecLang_1>>+English)]]
      </SELECT>
    </TD>
  </TR>
  <TR ><TD CLASS="strcol" COLSPAN="2" ><U>- update Handicap information on Diagnosis screen</U></TD></TR>
  <TR >
    <TD CLASS="strcol" >Legal Status</TD>
    <TD CLASS="strcol" >
      <SELECT NAME="ClientLegal_LegalStatus_1" >
        [[DBA->selxTable(%form+xLegalStatus+<<ClientLegal_LegalStatus_1>>+CDC Descr)]]
      </SELECT> 
    </TD>
  </TR>
  <TR >
    <TD CLASS="strcol" WIDTH=40% >County of Jurisdiction/Commitment</TD>
    <TD CLASS="strcol" >
      <SELECT NAME="ClientLegal_CommitmentCounty_1" >
        [[DBA->selxTable(%form+xCountyOK+<<ClientLegal_CommitmentCounty_1>>+CDC Descr)]]
      </SELECT> 
    </TD>
  </TR>
  <TR >
    <TD CLASS="strcol" >Do you currently smoke?</TD>
    <TD CLASS="strcol" >If yes, then <U>Add New</U> below.</TD>
  </TR>
  <TR >
    <TD CLASS="strcol" >If yes, how many times per day do you use tobacco?</TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="text" NAME="MedHx_DailyTobaccoUse_1" VALUE="<<MedHx_DailyTobaccoUse_1>>" ONFOCUS="select()" MAXLENGTH="2" SIZE="2" >
    </TD">
  </TR>
  <TR ><TD CLASS="strcol" COLSPAN="2" >Do you currently use and of the following drugs? (for History select 'current no' and for Current select 'current yes' below)</TD></TR>
  <TR ><TD CLASS="port hdrtxt" COLSPAN="2" ><U>Tobacco/Nicotine Use</U>, <U>Alcohol Use</U>, and <U>Drug Use</U> (History and Current)</TD></TR>
  <TR >
    <TD CLASS="port hdrtxt" COLSPAN="2" >
<SPAN ID="ListClientSA" >
[[myHTML->ListSel(%form+ListClientSA+<<<Client_ClientID>>>+<<<LINKID>>>+<<<Client_Locked_1>>>)]]
</SPAN>
    </TD>
  </TR>
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
  <TR >
    <TD CLASS="strcol" >Level Of Care</TD>
    <TD CLASS="strcol" >
      <SELECT NAME="ClientIntake_LOC_1" >[[DBA->selxTable(%form+xLOC+<<ClientIntake_LOC_1>>+ID Descr)]]</SELECT> 
    </TD>
  </TR>
  <TR ><TD CLASS="strcol" COLSPAN="2" ><U>CARS Scores 1-9</U></TD></TR>
  <TR >
    <TD CLASS="strcol" >Feeling/Mood</TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="text" NAME="PDDom_Dom1Score_1" VALUE="<<PDDom_Dom1Score_1>>" ONCHANGE="return vNum(this,1,50)" ONFOCUS="return chkLock(this,'Authorization Locked!','');" MAXLENGTH="5" SIZE="5" > (CAR 1)
    </TD>
  </TR>
  <TR >
    <TD CLASS="strcol" >Thinking/Mental</TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="text" NAME="PDDom_Dom2Score_1" VALUE="<<PDDom_Dom2Score_1>>" ONCHANGE="return vNum(this,1,50)" ONFOCUS="return chkLock(this,'Authorization Locked!','');" MAXLENGTH="5" SIZE="5" > (CAR 2)
    </TD>
  </TR>
  <TR >
    <TD CLASS="strcol" >Substance Abuse</TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="text" NAME="PDDom_Dom3Score_1" VALUE="<<PDDom_Dom3Score_1>>" ONCHANGE="return vNum(this,1,50)" ONFOCUS="return chkLock(this,'Authorization Locked!','');" MAXLENGTH="5" SIZE="5" > (CAR 3)
    </TD>
  </TR>
  <TR >
    <TD CLASS="strcol" >Medical/Physical</TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="text" NAME="PDDom_Dom4Score_1" VALUE="<<PDDom_Dom4Score_1>>" ONCHANGE="return vNum(this,1,50)" ONFOCUS="return chkLock(this,'Authorization Locked!','');" MAXLENGTH="5" SIZE="5" > (CAR 4)
    </TD>
  </TR>
  <TR >
    <TD CLASS="strcol" >Family</TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="text" NAME="PDDom_Dom5Score_1" VALUE="<<PDDom_Dom5Score_1>>" ONCHANGE="return vNum(this,1,50)" ONFOCUS="return chkLock(this,'Authorization Locked!','');" MAXLENGTH="5" SIZE="5" > (CAR 5)
    </TD>
  </TR>
  <TR >
    <TD CLASS="strcol" >Interpersonal</TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="text" NAME="PDDom_Dom6Score_1" VALUE="<<PDDom_Dom6Score_1>>" ONCHANGE="return vNum(this,1,50)" ONFOCUS="return chkLock(this,'Authorization Locked!','');" MAXLENGTH="5" SIZE="5" > (CAR 6)
    </TD>
  </TR>
  <TR >
    <TD CLASS="strcol" >Role Performance</TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="text" NAME="PDDom_Dom7Score_1" VALUE="<<PDDom_Dom7Score_1>>" ONCHANGE="return vNum(this,1,50)" ONFOCUS="return chkLock(this,'Authorization Locked!','');" MAXLENGTH="5" SIZE="5" > (CAR 7)
    </TD>
  </TR>
  <TR >
    <TD CLASS="strcol" >Socio-Legal</TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="text" NAME="PDDom_Dom8Score_1" VALUE="<<PDDom_Dom8Score_1>>" ONCHANGE="return vNum(this,1,50)" ONFOCUS="return chkLock(this,'Authorization Locked!','');" MAXLENGTH="5" SIZE="5" > (CAR 8)
    </TD>
  </TR>
  <TR >
    <TD CLASS="strcol" >Self-Care/Basic Needs</TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="text" NAME="PDDom_Dom9Score_1" VALUE="<<PDDom_Dom9Score_1>>" ONCHANGE="return vNum(this,1,50)" ONFOCUS="return chkLock(this,'Authorization Locked!','');" MAXLENGTH="5" SIZE="5" > (CAR 9)
    </TD>
  </TR>
  <TR ><TD CLASS="strcol" COLSPAN="2" ><U>- update ASI/TASI from the Client Menu - Testing screens</U></TD></TR>
  <TR><TD CLASS="port strcol" COLSPAN="2" ><B>Client Problems (First 5 problems are sent in with Prior Authorization)</B></TD></TR>
  <TR>
    <TD CLASS="strcol" COLSPAN="2" >
<SPAN ID="ListClientProblems" >
[[myHTML->ListSel(%form+ListClientProblems+<<<Client_ClientID>>>+<<<LINKID>>>+<<<Client_Locked_1>>>)]]
</SPAN>
    </TD>
  </TR>
</TABLE>
<TABLE CLASS="home fullsize" >
  <TR ><TD CLASS="strcol" COLSPAN="2" ><U>- SMI and SED calculated from Treatment Level</U></TD></TR>
  <TR >
    <TD CLASS="strcol" >In the past 30 days, how many times has the customer been arrested, or since admission if less than 30 days ago? (00-99)</TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="text" NAME="ClientLegal_Arrest1_1" VALUE="<<ClientLegal_Arrest1_1>>" ONFOCUS="select()" ONCHANGE="return vNum(this,0,99);" MAXLENGTH="3" SIZE="3" >
    </TD>
  </TR>
  <TR >
    <TD CLASS="strcol" >In the past 12 months, how many times has the customer been arrested, or since admission if less than 12 months ago? (00-99)</TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="text" NAME="ClientLegal_Arrested_1" VALUE="<<ClientLegal_Arrested_1>>" ONFOCUS="select()" ONCHANGE="return vNum(this,0,99);" MAXLENGTH="3" SIZE="3" >
    </TD>
  </TR>
  <TR >
    <TD CLASS="strcol" >In the past 30 days, how many times has the customer attended self-help/support groups, or since admission if less than 30 days.</TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="text" NAME="ClientResources_SelfHelp30_1" VALUE="<<ClientResources_SelfHelp30_1>>" ONFOCUS="select()" ONCHANGE="return vNum(this,0,30);" SIZE="5" >
    </TD>
  </TR>
  <TR >
    <TD CLASS="strcol" >CASE ID#</TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="text" NAME="ClientLegal_CASEID_1" VALUE="<<ClientLegal_CASEID_1>>" ONFOCUS="select()" SIZE="40" >
      (Drug Court #, DOC #, DHS Case # or FamilyID)
    </TD>
  </TR>
  <TR >
    <TD CLASS="strcol" >Descriptive</TD>
    <TD CLASS="strcol" >
      For Drug Court Case ID must be 3 Letters followed by 7 digits<BR>
      So...Use OSCN.net docket case number, add "D" for drug 2nd letter and truncate the last digit for case numbers with 8 digits.  This will allow for the 10 character maximum.
    </TD>
  </TR>
  <TR ><TD CLASS="strcol" COLSPAN="2" ><U>- Clinician Of Record NPI update on Primary Provider Page</U></TD></TR>
  <TR ><TD CLASS="port hdrtxt" COLSPAN="2" >Section IV</TD></TR>
  <TR >
    <TD CLASS="strcol" >Custodial Agency - Custody/Referral Type</TD>
    <TD CLASS="strcol" >
      <SELECT NAME="ClientLegal_CustAgency_1" >
        [[DBA->selxTable(%form+xCustAgency+<<ClientLegal_CustAgency_1>>+Descr)]]
      </SELECT> 
    </TD>
  </TR>
  <TR ><TD CLASS="strcol" COLSPAN="2" ><U>- out-of-home Placement in Residence above.</U></TD></TR>
  <TR >
    <TD CLASS="strcol" >In the past 90 days, how many days in a restrictive placement?</TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="text" NAME="MedHx_RestrictivePlacement_1" VALUE="<<MedHx_RestrictivePlacement_1>>" ONFOCUS="select()" ONCHANGE="return vNum(this,0,90);" SIZE=2>
    </TD>
  </TR>
  <TR >
    <TD CLASS="strcol" >In the past 90 days, on how many days did an incident of self-harm occur?</TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="text" NAME="MedHx_SelfHarm_1" VALUE="<<MedHx_SelfHarm_1>>" ONFOCUS="select()" ONCHANGE="return vNum(this,0,90);" SIZE=2>
    </TD>
  </TR>
  <TR>
    <TD CLASS="strcol" >In the past 90 days of the school year, how many days was the customer absent from school?</TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="text" NAME="ClientIntake_AbsentSchool_1" VALUE="<<ClientIntake_AbsentSchool_1>>" ONFOCUS="select()" ONCHANGE="return vNum(this,0,66);" SIZE="2" >
    </TD>
  </TR>
  <TR>
    <TD CLASS="strcol" >In the past 90 days of the school year, how many days was the customer suspended from school?</TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="text" NAME="ClientIntake_SuspendedSchool_1" VALUE="<<ClientIntake_SuspendedSchool_1>>" ONFOCUS="select()" ONCHANGE="return vNum(this,0,66);" SIZE="2" >
    </TD>
  </TR>
  <TR>
    <TD CLASS="strcol" >In the past 90 days, how many days was the customer not permitted to return to day care? </TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="text" NAME="ClientIntake_AbsentDayCare_1" VALUE="<<ClientIntake_AbsentDayCare_1>>" ONFOCUS="select()" ONCHANGE="return vNum(this,0,66);" SIZE="2" >
    </TD>
  </TR>
</TABLE>
<TABLE CLASS="main fullsize" >
  <TR>
    <TD CLASS="numcol" >
      Verify changes Client information and verifies CDC
      <INPUT TYPE="submit" ONCLICK="return validate(this.form);" NAME="UpdateTables=all&[[myForm->genLink(PDDom+PDDom.cgi)]]" VALUE="Add/Update -> CAR Scores">
      <INPUT TYPE="submit" ONCLICK="return validate(this.form);" NAME="UpdateTables=all&misPOP=1&ClientPrAuthCDC_CDCOK_1=1" VALUE="Verify/Add/Update" >
    </TD>
  </TR>
</TABLE>

<INPUT TYPE="hidden" NAME="post_update" VALUE="PostUpd->updPrAuth(%form+<<<ClientPrAuth_ID_1>>>)" >
</LOADHIDDEN>
<SCRIPT LANGUAGE="JavaScript" >
// just to OPENTABLES...
//<<<ClientIntake_ServiceFocus_1>>> <<<ClientResources_SelfHelp30_1>>> <<<MedHx_SelfHarm_1>>> <<<PDDom_Dom1Score_1>>> <<<ClientSocial_Axis5Curr_1>>>
document.CDC.elements[0].focus();
callAjax('Agency','<<ClientReferrals_ReferredBy1NPI_1>>','selRefBy1','&name=ClientReferrals_ReferredBy1NPI_1','popup.pl');
callAjax('Agency','<<ClientReferrals_ReferredBy2NPI_1>>','selRefBy2','&name=ClientReferrals_ReferredBy2NPI_1','popup.pl');
doShow('Client_Race_1','Client_Race_1_display');
doDisableCheck('2186-5','Client_Ethnicity_1','Client_Ethnicity_1_display');
vDate(document.CDC.Client_DOB_1,1,document.CDC,'Client_Age');
</SCRIPT>
</FORM>

[[myHTML->rightpane(%form+search)]]
