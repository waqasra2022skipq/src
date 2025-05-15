[[myHTML->newPage(%form+Client Social)]]

<SCRIPT LANGUAGE="JavaScript" SRC="/src/cgi/js/vEntry.js"> </SCRIPT>
<SCRIPT LANGUAGE="JavaScript" SRC="/src/cgi/js/vClientSocial.js"> </SCRIPT>
<SCRIPT LANGUAGE="JavaScript" SRC="/src/cgi/js/vNum.js"> </SCRIPT>

<FORM NAME="Social" ACTION="/cgi/bin/mis.cgi" METHOD="POST" >
<TABLE CLASS="main fullsize" >
  <TR >
    <TD CLASS="strcol" >
      <<<Client_FName_1>>> <<<Client_MName_1>>> <<<Client_LName_1>>> (<<<Client_ClientID_1>>>) <<<Client_SSN_1>>>
      <BR>
      Social Page
    </TD>
    <TD CLASS="numcol" >[[gHTML->setLINKS(%form+back)]]</TD>
  </TR>
</TABLE>
<TABLE CLASS="port fullsize" >
  <TR ><TD CLASS="heading" COLSPAN="2" >SOCIAL</TD></TR>
    <TR ><TD ><TABLE CLASS="home fullsize" >
  <TR ><TD CLASS="port hdrtxt" COLSPAN="2" >Cultural</TD></TR>
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
    <TD CLASS="strcol" >Tribal Affiliation (CDIB Card):</TD>
    <TD CLASS="strcol" >
      <SELECT NAME="ClientSocial_Tribe_1">
        [[DBA->selxTable(%form+xTribe+<<ClientSocial_Tribe_1>>+Descr)]]
      </SELECT> 
    </TD>
  </TR>
  <TR >
    <TD CLASS="strcol" COLSPAN="2" >
      Describe any traditional practices you participate in:
    </TD>
  </TR>
  <TR >
    <TD CLASS="strcol" COLSPAN="2" >
      <TEXTAREA NAME="ClientSocial_TribePart_1" COLS="90" ROWS="2" WRAP="virtual" ><<ClientSocial_TribePart_1>></TEXTAREA>
    </TD>
  </TR>
  <TR >
    <TD CLASS="strcol" >Gang Affiliation:</TD>
    <TD CLASS="strcol" >
      <INPUT TYPE=text NAME="ClientSocial_Gang_1" VALUE="<<ClientSocial_Gang_1>>" ONFOCUS="select()" SIZE="70" >
    </TD>
  </TR>
  <TR >
    <TD CLASS="strcol" COLSPAN="2" >
      What do you value about your gang involvement?
    </TD>
  </TR>
  <TR >
    <TD CLASS="strcol" COLSPAN="2" >
      <TEXTAREA NAME="ClientSocial_GangValue_1" COLS="90" ROWS="2" WRAP="virtual" ><<ClientSocial_GangValue_1>></TEXTAREA>
    </TD>
  </TR>
  <TR >
    <TD CLASS="strcol" >Other Social/Cultural Affiliation:</TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="text" NAME="ClientSocial_OtherAffiliation_1" VALUE="<<ClientSocial_OtherAffiliation_1>>" ONFOCUS="select()" SIZE="70" >
    </TD>
  </TR>
  <TR >
    <TD CLASS="strcol" COLSPAN="2" >
      What do you value about this social/cultural involvement?
    </TD>
  </TR>
  <TR >
    <TD CLASS="strcol" COLSPAN="2" >
      <TEXTAREA NAME="ClientSocial_OtherValue_1" COLS="90" ROWS="2" WRAP="virtual" ><<ClientSocial_OtherValue_1>></TEXTAREA>
    </TD>
  </TR>
  <TR >
    <TD CLASS="strcol" COLSPAN="2" >
      What is unique or interesting about you?
    </TD>
  </TR>
  <TR >
    <TD CLASS="strcol" COLSPAN="2" >
      <TEXTAREA NAME="ClientSocial_UniqueYou_1" COLS="90" ROWS="2" WRAP="virtual" ><<ClientSocial_UniqueYou_1>></TEXTAREA>
    </TD>
  </TR>
  <TR >
    <TD CLASS="strcol" COLSPAN="2" >
      What is important to you?
    </TD>
  </TR>
  <TR >
    <TD CLASS="strcol" COLSPAN="2" >
      <TEXTAREA NAME="ClientSocial_ImportantYou_1" COLS="90" ROWS="2" WRAP="virtual" ><<ClientSocial_ImportantYou_1>></TEXTAREA>
    </TD>
  </TR>
    </TABLE></TD></TR>
    <TR ><TD ><TABLE CLASS="home fullsize" >
  <TR ><TD CLASS="port hdrtxt" COLSPAN="2" >Language</TD></TR>
  <TR >
    <TD CLASS="strcol" >Preferred Language:</TD>
    <TD CLASS="strcol" >
      <SELECT NAME="ClientSocial_PreLang_1">
        [[DBA->selxTable(%form+xLanguages+<<ClientSocial_PreLang_1>>+English)]]
      </SELECT>
      <BR>If child/client is non-verbal,<BR>report the language preference of the child's/client's caregiver/guardian/parent.
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
  <TR>
    <TD CLASS="strcol" >Does client READ English well?</TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="radio" NAME="ClientSocial_ReadEnglish_1" VALUE=1 <<ClientSocial_ReadEnglish_1=1>> > Yes
      <INPUT TYPE="radio" NAME="ClientSocial_ReadEnglish_1" VALUE=0 <<ClientSocial_ReadEnglish_1=0>> > No
    </TD>
  </TR>
  <TR>
    <TD CLASS="strcol" >Does client WRITE English well?</TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="radio" NAME="ClientSocial_WriteEnglish_1" VALUE=1 <<ClientSocial_WriteEnglish_1=1>> > Yes
      <INPUT TYPE="radio" NAME="ClientSocial_WriteEnglish_1" VALUE=0 <<ClientSocial_WriteEnglish_1=0>> > No
    </TD>
  </TR>
  <TR>
    <TD CLASS="strcol" >Does client SPEAK English well?</TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="radio" NAME="ClientSocial_SpeakEnglish_1" VALUE=1 <<ClientSocial_SpeakEnglish_1=1>> > Yes
      <INPUT TYPE="radio" NAME="ClientSocial_SpeakEnglish_1" VALUE=0 <<ClientSocial_SpeakEnglish_1=0>> > No
    </TD>
  </TR>
  <TR >
    <TD CLASS="strcol" VALIGN="top" COLSPAN="2" >If no, please describe:</TD>
  </TR>
  <TR >
    <TD CLASS="strcol" COLSPAN="2" >
      <TEXTAREA NAME="ClientSocial_LangProbs_1" COLS=90 ROWS=2 WRAP="virtual" ><<ClientSocial_LangProbs_1>></TEXTAREA>
    </TD>
  </TR>
  <TR >
    <TD CLASS="strcol" >Reading Literacy Level :</TD>
    <TD CLASS="strcol" >
      <SELECT NAME="ClientSocial_ReadingLiteracy_1">
        [[DBA->selxTable(%form+xLiteracyFindings+<<ClientSocial_ReadingLiteracy_1>>+ConceptName)]]
      </SELECT>
    </TD>
  </TR>
  <TR >
    <TD CLASS="strcol" >Writing Literacy Level :</TD>
    <TD CLASS="strcol" >
      <SELECT NAME="ClientSocial_WritingLiteracy_1">
        [[DBA->selxTable(%form+xLiteracyFindings+<<ClientSocial_WritingLiteracy_1>>+ConceptName)]]
      </SELECT>
    </TD>
  </TR>
    </TABLE></TD></TR>
    <TR ><TD ><TABLE CLASS="home fullsize" >
  <TR ><TD CLASS="port hdrtxt" COLSPAN="2" >Religion/Spirituality</TD></TR>
  <TR >
    <TD CLASS="strcol" COLSPAN="2" >Were you raised in the country or city?
      <INPUT TYPE="radio" NAME="ClientSocial_RaisedIn_1" VALUE=City <<ClientSocial_RaisedIn_1=City>> > City
      <INPUT TYPE="radio" NAME="ClientSocial_RaisedIn_1" VALUE=Country <<ClientSocial_RaisedIn_1=Country>> > Country
    </TD>
  </TR>
  <TR >
    <TD CLASS="strcol" COLSPAN="2" >Where do you prefer to live?
      <INPUT TYPE="radio" NAME="ClientSocial_PreferLive_1" VALUE=City <<ClientSocial_PreferLive_1=City>> > City
      <INPUT TYPE="radio" NAME="ClientSocial_PreferLive_1" VALUE=Suburbs <<ClientSocial_PreferLive_1=Suburbs>> > Suburbs
      <INPUT TYPE="radio" NAME="ClientSocial_PreferLive_1" VALUE=Town <<ClientSocial_PreferLive_1=Town>> > Town
      <INPUT TYPE="radio" NAME="ClientSocial_PreferLive_1" VALUE=Country <<ClientSocial_PreferLive_1=Country>> > Country
    </TD>
  </TR>
  <TR>
    <TD CLASS="strcol" COLSPAN="2" >Does client see a traditional healer?
      <INPUT TYPE="radio" NAME="ClientSocial_Healer_1" VALUE="1" <<ClientSocial_Healer_1=1>> > Yes
      <INPUT TYPE="radio" NAME="ClientSocial_Healer_1" VALUE="0" <<ClientSocial_Healer_1=0>> > No
    </TD>
  </TR>
  <TR >
    <TD CLASS="strcol" COLSPAN="2" >Do you feel aspects of treatment will conflict with your cultural and spiritual background?
    </TD>
  </TR>
  <TR ><TD CLASS="strcol" VALIGN="top" COLSPAN="2" >If yes, how?</TD></TR>
  <TR >
    <TD CLASS="strcol" COLSPAN="2" >
      <TEXTAREA NAME="ClientSocial_ReligionDiff_1" COLS=90 ROWS=2 WRAP="virtual" ><<ClientSocial_ReligionDiff_1>></TEXTAREA>
    </TD>
  </TR>
  <TR >
    <TD CLASS="strcol" COLSPAN="2" >What meaning does God, Spirituality, or Higher Power play in your life?
    </TD>
  </TR>
  <TR>
    <TD CLASS="strcol" COLSPAN="2" >
      <TEXTAREA NAME="ClientSocial_ReligionMean_1" COLS=90 ROWS=2 WRAP="virtual" ><<ClientSocial_ReligionMean_1>></TEXTAREA>
    </TD>
  </TR>
  <TR >
    <TD CLASS="strcol" >Did you attend church as a child?
      <INPUT TYPE="radio" NAME="ClientSocial_ReligionChild_1" VALUE=1 <<ClientSocial_ReligionChild_1=1>> > yes
      <INPUT TYPE="radio" NAME="ClientSocial_ReligionChild_1" VALUE=0 <<ClientSocial_ReligionChild_1=0>> > no
    </TD>
    <TD CLASS="strcol" >Which religion?
      <SELECT NAME="ClientSocial_Religion_1" >
        [[DBA->selxTable(%form+xReligiousAffiliation+<<ClientSocial_Religion_1>>+Descr)]]
      </SELECT> 
    </TD>
  </TR>
  <TR >
    <TD CLASS="strcol" >Do you currently attend church or religious services?
      <INPUT TYPE="radio" NAME="ClientSocial_ReligionAttend_1" VALUE=1 <<ClientSocial_ReligionAttend_1=1>> > yes
      <INPUT TYPE="radio" NAME="ClientSocial_ReligionAttend_1" VALUE=0 <<ClientSocial_ReligionAttend_1=0>> > no
    </TD>
    <TD CLASS="strcol" >Which religion?
      <SELECT NAME="ClientSocial_ReligionName_1" >
        [[DBA->selxTable(%form+xReligiousAffiliation+<<ClientSocial_ReligionName_1>>+Descr)]]
      </SELECT> 
    </TD>
  </TR>
  <TR >
    <TD CLASS="strcol" >Have your behaviors impacted your views of spirituality?
      <INPUT TYPE="radio" NAME="ClientSocial_ReligionViews_1" VALUE=1 <<ClientSocial_ReligionViews_1=1>> > yes
      <INPUT TYPE="radio" NAME="ClientSocial_ReligionViews_1" VALUE=0 <<ClientSocial_ReligionViews_1=0>> > no
    </TD>
    <TD CLASS="strcol" >&nbsp;</TD>
  </TR>
  <TR >
    <TD CLASS="strcol" COLSPAN="2" >Have you had any exceptionally good or bad experiences with the church?</TD>
  </TR>
  <TR ><TD CLASS="strcol" VALIGN="top" COLSPAN="2" >If yes, please describe:</TD></TR>
  <TR >
    <TD CLASS="strcol" COLSPAN="2" >
      <TEXTAREA NAME="ClientSocial_ReligionExp_1" COLS=90 ROWS=2 WRAP="virtual" ><<ClientSocial_ReligionExp_1>></TEXTAREA>
    </TD>
  </TR>
    </TABLE></TD></TR>
    <TR ><TD ><TABLE CLASS="home fullsize" >
  <TR ><TD CLASS="port hdrtxt" COLSPAN="2" >Recreational/Leisure</TD></TR>
  <TR >
    <TD CLASS="strcol" COLSPAN="2" >
      � If a girlfriend/boyfriend is considered as family by patient, then they must refer to them as family throughout this section, not a friend.
    </TD>
  </TR>
  <TR >
    <TD CLASS="strcol" >
      With whom do you spend most of your free time?
    </TD>
    <TD CLASS="strcol" ALIGN=left >
      <INPUT TYPE="radio" NAME="ClientSocial_WhoSpendTime_1" VALUE=1 <<ClientSocial_WhoSpendTime_1=1>> > Family
      <INPUT TYPE="radio" NAME="ClientSocial_WhoSpendTime_1" VALUE=2 <<ClientSocial_WhoSpendTime_1=2>> > Friends
      <INPUT TYPE="radio" NAME="ClientSocial_WhoSpendTime_1" VALUE=3 <<ClientSocial_WhoSpendTime_1=3>> > Alone
    </TD>
  </TR>
  <TR >
    <TD CLASS="strcol" >
      Are you satisfied with spending your free time this way?
      � A satisfied response must indicate that the person generally likes the situation. Referring to above.
    </TD>
    <TD CLASS="strcol" ALIGN=left >
      <INPUT TYPE="radio" NAME="ClientSocial_SatSpendTime_1" VALUE=0 <<ClientSocial_SatSpendTime_1=0>> > No
      <INPUT TYPE="radio" NAME="ClientSocial_SatSpendTime_1" VALUE=1 <<ClientSocial_SatSpendTime_1=1>> > Indifferent
      <INPUT TYPE="radio" NAME="ClientSocial_SatSpendTime_1" VALUE=2 <<ClientSocial_SatSpendTime_1=2>> > Yes
    </TD>
  </TR>
  <TR >
    <TD CLASS="strcol" >
      How many close friends do you have?
      � Stress that you mean close. Exclude family members. These are "reciprocal" relationships or mutually supportive relationships.
    </TD>
    <TD CLASS="strcol" ALIGN=left >
      <INPUT TYPE=text NAME="ClientSocial_NumCloseFriends_1" VALUE="<<ClientSocial_NumCloseFriends_1>>" ONFOCUS="select()" ONCHANGE="return vNum(this,0,9);" SIZE="2" >
    </TD>
  </TR>
  <TR ><TD CLASS="strcol" COLSPAN="2" >Any special interests or hobbies?</TD></TR>
  <TR >
    <TD CLASS="strcol" COLSPAN="2" >If yes, please describe:</TD>
  </TR>
  <TR >
    <TD CLASS="strcol" COLSPAN="2" >
      <INPUT TYPE=text NAME="ClientSocial_Hobby_1" VALUE="<<ClientSocial_Hobby_1>>" ONFOCUS="select()" SIZE="70" >
    </TD>
  </TR>
  <TR ><TD CLASS="strcol" COLSPAN="2" >What do you do or have you done for fun or enjoyment? Risk Taking?</TD></TR>
  <TR >
    <TD CLASS="strcol" COLSPAN="2" >
      <TEXTAREA NAME="ClientSocial_RecDesc_1" COLS="90" ROWS="4" WRAP="virtual" ><<ClientSocial_RecDesc_1>></TEXTAREA>
    </TD>
  </TR>
    </TABLE></TD></TR>
    <TR ><TD ><TABLE CLASS="home fullsize" >
  <TR ><TD CLASS="port hdrtxt" COLSPAN="3" >Present stressors<BR>(Check those that apply and comment as needed)</TD></TR>
  <TR >
    <TD CLASS="strcol" >
      <INPUT TYPE=checkbox NAME="ClientSocial_StressDeath_1" VALUE=1 <<ClientSocial_StressDeath_1=checkbox>> >
      Recent death
    </TD>
    <TD CLASS="strcol" >
      <INPUT TYPE=checkbox NAME="ClientSocial_StressDivorce_1" VALUE=1 <<ClientSocial_StressDivorce_1=checkbox>> >
      Divorce
    </TD>
    <TD CLASS="strcol" >
      <INPUT TYPE=checkbox NAME="ClientSocial_StressSeparation_1" VALUE=1 <<ClientSocial_StressSeparation_1=checkbox>> >
      Separation from a significant relationship
    </TD>
  </TR>
  <TR >
    <TD CLASS="strcol" COLSPAN="3" >Comments:
      <TEXTAREA NAME="ClientSocial_StressDesc_1" COLS="90" ROWS="2" WRAP="virtual" ><<ClientSocial_StressDesc_1>></TEXTAREA>
    </TD>
  </TR>
  <TR >
    <TD CLASS="strcol" COLSPAN="3" >
      <INPUT TYPE=checkbox NAME="ClientSocial_RelDestrFlag_1" VALUE=1 <<ClientSocial_RelDestrFlag_1=checkbox>> >
      Emotionally unable by past history to remain separated from a destructive relationship 
      (i.e. living with<BR>chemical abuser, physical emotional/sexual abuser).
    </TD>
  </TR>
  <TR >
    <TD CLASS="strcol" COLSPAN="3" >Comments:
      <TEXTAREA NAME="ClientSocial_RelDestrDesc_1" COLS="90" ROWS="2" WRAP="virtual" ><<ClientSocial_RelDestrDesc_1>></TEXTAREA>
    </TD>
  </TR>
  <TR >
    <TD CLASS="strcol" COLSPAN="3" >
      <INPUT TYPE=checkbox NAME="ClientSocial_RelPDFlag_1" VALUE=1 <<ClientSocial_RelPDFlag_1=checkbox>> >
      Involves self in relationships with personality-disordered individuals.
    </TD>
  </TR>
  <TR >
    <TD CLASS="strcol" COLSPAN="3" >Comments:
      <TEXTAREA NAME="ClientSocial_RelPDDesc_1" COLS="90" ROWS="2" WRAP="virtual" ><<ClientSocial_RelPDDesc_1>></TEXTAREA>
    </TD>
  </TR>
  <TR >
    <TD CLASS="strcol" COLSPAN="3" >
      <INPUT TYPE=checkbox NAME="ClientSocial_RelIntimateFlag_1" VALUE=1 <<ClientSocial_RelIntimateFlag_1=checkbox>> >
      Experiences anxiety, boundary difficulties and separation issues in intimate relationships.
    </TD>
  </TR>
  <TR >
    <TD CLASS="strcol" COLSPAN="3" >Comments: 
      <TEXTAREA NAME="ClientSocial_RelIntimateDesc_1" COLS="90" ROWS="2" WRAP="virtual" ><<ClientSocial_RelIntimateDesc_1>></TEXTAREA>
    </TD>
  </TR>
  <TR >
    <TD CLASS="strcol" COLSPAN="3" >
      <INPUT TYPE=checkbox NAME="ClientSocial_RelNeedsFlag_1" VALUE=1 <<ClientSocial_RelNeedsFlag_1=checkbox>> >
      Assumes responsibility for meeting others needs to the exclusion of their own.
    </TD>
  </TR>
  <TR >
    <TD CLASS="strcol" COLSPAN="3" >Comments: 
      <TEXTAREA NAME="ClientSocial_RelNeedsDesc_1" COLS="90" ROWS="2" WRAP="virtual" ><<ClientSocial_RelNeedsDesc_1>></TEXTAREA>
    </TD>
  </TR>
    </TABLE></TD></TR>
    <TR ><TD ><TABLE CLASS="home fullsize" >
  <TR ><TD CLASS="port hdrtxt" COLSPAN="2" >Level of social functioning<BR>(i.e. client's and therapist's opinion of social/peer interaction)</TD></TR>
  <TR>
    <TD CLASS="strcol" COLSPAN="2" >
      <TEXTAREA NAME="ClientSocial_RelSocialDesc_1" COLS="90" ROWS="12" WRAP="virtual" ><<ClientSocial_RelSocialDesc_1>></TEXTAREA>
    </TD>
  </TR>
    </TABLE></TD></TR>
</TABLE>

<TABLE CLASS="main fullsize" >
  <TR >
    <TD CLASS="numcol" >
      <INPUT TYPE="submit" ONCLICK="return validate(this.form);" NAME="UpdateTables=all&[[myForm->genLink(ClientIntake+ClientHistory.cgi)]]" VALUE="Add/Update -> Education / Vocation">
      <INPUT TYPE="submit" ONCLICK="return validate(this.form);" NAME="UpdateTables=all&misPOP=1" VALUE="Add/Update">
    </TD>
  </TR>
</TABLE>

<INPUT TYPE="hidden" NAME="post_update" VALUE="PostUpd->updPA(%form+<<<Client_ClientID_1>>>)" >
</LOADHIDDEN>
</FORM>
<SCRIPT LANGUAGE="JavaScript">
document.Social.elements[0].focus();
doShow('Client_Race_1','Client_Race_1_display');
doDisableCheck('2186-5','Client_Ethnicity_1','Client_Ethnicity_1_display');
</SCRIPT>

[[myHTML->rightpane(%form+search)]]
