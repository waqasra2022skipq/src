[[myHTML->newPage(%form+Client Discharge Summary Page)]]

<SCRIPT LANGUAGE="JavaScript" SRC="/src/cgi/js/NoEnter.js"> </SCRIPT>
<SCRIPT LANGUAGE="JavaScript" SRC="/src/cgi/js/vEntry.js"> </SCRIPT>
<SCRIPT LANGUAGE="JavaScript" SRC="/src/cgi/js/vClientDischarge.js"> </SCRIPT>
<SCRIPT type="text/javascript" src="/src/cgi/js/ajaxrequest.js"></SCRIPT>
<SCRIPT LANGUAGE="JavaScript" SRC="/src/cgi/js/vDate.js"> </SCRIPT>
<SCRIPT LANGUAGE="JavaScript" SRC="/src/cgi/js/vTime.js"> </SCRIPT>
<SCRIPT LANGUAGE="JavaScript" SRC="/src/cgi/js/vNum.js"> </SCRIPT>

[[*SysAccess->verify(%form+Privilege=Discharge)]]

<FORM NAME="ClientDischarge" ACTION="/cgi/bin/mis.cgi" METHOD="POST" >
<TABLE CLASS="main fullsize" >
  <TR >
    <TD CLASS="strcol" >
      <<<Client_FName_1>>> <<<Client_MName_1>>> <<<Client_LName_1>>> (<<<Client_ClientID_1>>>) <<<Client_SSN_1>>>
      <BR>
      Client Discharge Summary Page
    </TD>
    <TD CLASS="numcol" >[[gHTML->setLINKS(%form+back)]]</TD>
  </TR>
</TABLE>
<TABLE CLASS="home fullsize" >
  <TR >
    <TD CLASS="port strcol" >Discharge Service Focus</TD>
    <TD CLASS="strcol" >
      <SELECT NAME="ClientDischarge_ServiceFocus_1" SIZE="10" >
        [[DBA->selxTable(%form+xServiceFocus+<<ClientDischarge_ServiceFocus_1>>+Descr)]]
      </SELECT> 
    </TD>
  </TR>
  <TR >
    <TD CLASS="port strcol" >Discharge Type</TD>
    <TD CLASS="strcol" >
      <SELECT NAME="ClientDischargeCDC_TransType_1" >[[DBA->selTransType(%form+<<<ClientDischarge_ClientID_1>>>+<<ClientDischargeCDC_TransType_1>>+Discharge)]]</SELECT>
      <A HREF="http://forms.okmis.com/misdocs/CDCTT.html" TARGET="popup" ONCLICK="window.open('http://forms.okmis.com/misdocs/CDCTT.html', 'popup', 'width=900,height=700,menubar=1,scrollbars=1,toolbar=1,status=1,resizable=1'); return false">explain</A> 
    </TD>
  </TR>
  <TR >
    <TD CLASS="port strcol" >Original Intake Date</TD>
    <TD CLASS="strcol" >
      <INPUT TYPE=text NAME="ClientDischarge_IntDate_1" VALUE="<<ClientDischarge_IntDate_1>>" ONFOCUS="select()" ONCHANGE="return vDate(this)" SIZE="10" >
    </TD>
  </TR>
  <TR >
    <TD CLASS="port strcol" >Discharge/Contact Date</TD>
    <TD CLASS="strcol" >
      <INPUT TYPE=text NAME="ClientDischargeCDC_TransDate_1" VALUE="<<ClientDischargeCDC_TransDate_1>>" ONFOCUS="select()" ONCHANGE="return vDate(this)" MAXLENGTH="10" SIZE="10" >
      <A HREF="http://forms.okmis.com/misdocs/CDCTT.html" TARGET="popup" ONCLICK="window.open('http://forms.okmis.com/misdocs/CDCTD.html', 'popup', 'width=900,height=700,menubar=1,scrollbars=1,toolbar=1,status=1,resizable=1'); return false">explain</A> 
    </TD>
  </TR>
  <TR >
    <TD CLASS="port strcol" >Discharge/Contact Time</TD>
    <TD CLASS="strcol" >
      <INPUT TYPE=text NAME="ClientDischargeCDC_TransTime_1" VALUE="<<ClientDischargeCDC_TransTime_1>>" ONFOCUS="select()" ONCHANGE="return vTime(this,1,this)" MAXLENGTH="10" SIZE="10" >
    </TD>
  </TR>
  <TR >
    <TD CLASS="port strcol" >
      Status / Date / CDCKey
    </TD>
    <TD CLASS="strcol" >
      [[gHTML->ifld(%form+ClientDischargeCDC_Status_1+displayonly)]]
      /
      [[gHTML->ifld(%form+ClientDischargeCDC_StatusDate_1+displayonly)]]
      /
      [[gHTML->ifld(%form+ClientDischargeCDC_CDCKey_1+displayonly)]]
    </TD>
  </TR>
  <TR >
    <TD CLASS="port strcol" >Persons Involved with Treatment/Transition Planning</TD>
    <TD CLASS="strcol" >
      <INPUT TYPE=text NAME="ClientDischarge_DevelopBy_1" VALUE="<<ClientDischarge_DevelopBy_1>>" ONFOCUS="select()" SIZE="50" >
    </TD>
  </TR>
</TABLE>
<TABLE CLASS="home fullsize" >
  <TR><TD CLASS="strcol" COLSPAN="2" >&nbsp;</TD></TR>
  <TR >
    <TD CLASS="port hdrtxt" COLSPAN="2" >
      Condition at time of Intake
    </TD>
  </TR>
  <TR >
    <TD CLASS="strcol" COLSPAN="2" >
       <TEXTAREA NAME="ClientDischarge_InitCond_1" COLS="80" ROWS="5" WRAP="virtual" ><<ClientDischarge_InitCond_1>></TEXTAREA>
    </TD>
  </TR>
  <TR >
    <TD CLASS="port hdrtxt" COLSPAN="2" >
      Needs identified at Intake
    </TD>
  </TR>
  <TR >
    <TD CLASS="strcol" COLSPAN="2" >
       <TEXTAREA NAME="ClientDischarge_IDNeeds_1" COLS="80" ROWS="5" WRAP="virtual" ><<ClientDischarge_IDNeeds_1>></TEXTAREA>
    </TD>
  </TR>
  <TR >
    <TD CLASS="port hdrtxt" COLSPAN="2" >
      Condition at Discharge
    </TD>
  </TR>
  <TR >
    <TD CLASS="strcol" COLSPAN="2" >
       <TEXTAREA NAME="ClientDischarge_Assessment_1" COLS="80" ROWS="5" WRAP="virtual" ><<ClientDischarge_Assessment_1>></TEXTAREA>
    </TD>
  </TR>
  <TR >
    <TD CLASS="port hdrtxt" COLSPAN="2" >
      Gains/Skills Developed or Goals Reached During Treatment
    </TD>
  </TR>
  <TR >
    <TD CLASS="strcol" COLSPAN="2" >
       <TEXTAREA NAME="ClientDischarge_Gains_1" COLS="80" ROWS="5" WRAP="virtual" ><<ClientDischarge_Gains_1>></TEXTAREA>
    </TD>
  </TR>
  <TR > <TD CLASS="port hdrtxt" COLSPAN="2" >Specific Client Strengths/Needs/Abilities/Preferences</TD> </TR>
  <TR >
    <TD CLASS="strcol" COLSPAN="2" >
       <TEXTAREA NAME="ClientDischarge_Needs_1" COLS="80" ROWS="5" WRAP="virtual" ><<ClientDischarge_Needs_1>></TEXTAREA>
    </TD>
  </TR>
  <TR >
    <TD CLASS="port hdrtxt" COLSPAN="2" >Transistion Plan <FONT SIZE="-2">(written recommendations, specific referrals for implementing aftercare/support services including medications, and consumer's response):</FONT>
    </TD>
  </TR>
  <TR >
    <TD CLASS="strcol" COLSPAN="2" >
       <TEXTAREA NAME="ClientDischarge_DischargePlan_1" COLS="80" ROWS="5" WRAP="virtual" ><<ClientDischarge_DischargePlan_1>></TEXTAREA>
    </TD>
  </TR>
</TABLE>
<TABLE CLASS="home fullsize" >
  <TR ><TD CLASS="port hdrtxt" COLSPAN="2" >CAR SCORES</TD></TR>
  <TR >
    <TD CLASS="strcol" >1. FEELING/MOOD AFFECT</TD>
    <TD CLASS="strcol" >SCORE:
      <INPUT TYPE="TEXT" NAME="ClientDischarge_Dom1Score_1" VALUE="<<ClientDischarge_Dom1Score_1>>" SIZE="6" ONCHANGE="vNum(this,1,50)" >
    </TD>
  </TR>
  <TR >
    <TD CLASS="strcol" >2. THINKING/MENTAL PROCESS</TD>
    <TD CLASS="strcol" >SCORE:
      <INPUT TYPE="TEXT" NAME="ClientDischarge_Dom2Score_1" VALUE="<<ClientDischarge_Dom2Score_1>>" SIZE="6" ONCHANGE="vNum(this,1,50)" >
    </TD>
  </TR>
  <TR >
    <TD CLASS="strcol" >3. SUBSTANCE USE</TD>
    <TD CLASS="strcol" >SCORE:
      <INPUT TYPE="TEXT" NAME="ClientDischarge_Dom3Score_1" VALUE="<<ClientDischarge_Dom3Score_1>>" SIZE="6" ONCHANGE="vNum(this,1,50)" >
    </TD>
  </TR>
  <TR >
    <TD CLASS="strcol" >4. MEDICAL/PHYSICAL</TD>
    <TD CLASS="strcol" >SCORE:
      <INPUT TYPE="TEXT" NAME="ClientDischarge_Dom4Score_1" VALUE="<<ClientDischarge_Dom4Score_1>>" SIZE="6" ONCHANGE="vNum(this,1,50)" >
    </TD>
  </TR>
  <TR >
    <TD CLASS="strcol" >5. FAMILY</TD>
    <TD CLASS="strcol" >SCORE:
      <INPUT TYPE="TEXT" NAME="ClientDischarge_Dom5Score_1" VALUE="<<ClientDischarge_Dom5Score_1>>" SIZE="6" ONCHANGE="vNum(this,1,50)" >
    </TD>
  </TR>
  <TR >
    <TD CLASS="strcol" >6. INTERPERSONAL</TD>
    <TD CLASS="strcol" >SCORE:
      <INPUT TYPE="TEXT" NAME="ClientDischarge_Dom6Score_1" VALUE="<<ClientDischarge_Dom6Score_1>>" SIZE="6" ONCHANGE="vNum(this,1,50)" >
    </TD>
  </TR>
  <TR >
    <TD CLASS="strcol" >7. ROLE PERFORMANCE</TD>
    <TD CLASS="strcol" >SCORE:
      <INPUT TYPE="TEXT" NAME="ClientDischarge_Dom7Score_1" VALUE="<<ClientDischarge_Dom7Score_1>>" SIZE="6" ONCHANGE="vNum(this,1,50)" >
    </TD>
  </TR>
  <TR >
    <TD CLASS="strcol" >8. SOCIO-LEGAL</TD>
    <TD CLASS="strcol" >SCORE:
      <INPUT TYPE="TEXT" NAME="ClientDischarge_Dom8Score_1" VALUE="<<ClientDischarge_Dom8Score_1>>" SIZE="6" ONCHANGE="vNum(this,1,50)" >
    </TD>
  </TR>
  <TR >
    <TD CLASS="strcol" >9. SELF-CARE/BASIC NEEDS</TD>
    <TD CLASS="strcol" >SCORE:
      <INPUT TYPE="TEXT" NAME="ClientDischarge_Dom9Score_1" VALUE="<<ClientDischarge_Dom9Score_1>>" SIZE="6" ONCHANGE="vNum(this,1,50)" >
    </TD>
  </TR>
</TABLE>
<TABLE CLASS="home fullsize" >
  <TR >
    <TD CLASS="port hdrtxt" >Medication Summary (include all medications prescribed when starting the program)</TD>
    <TD CLASS="strcol" >
      <INPUT TYPE=checkbox NAME="ClientDischarge_NoMed_1" VALUE=1 <<ClientDischarge_NoMed_1=checkbox>> > 
      Medication was not provided as part of treatment provided
    </TD>
  </TR>
  <TR >
    <TD CLASS="strcol" COLSPAN="2" >
       <TEXTAREA NAME="ClientDischarge_MedSum_1" COLS="80" ROWS="3" WRAP="virtual" ><<ClientDischarge_MedSum_1>></TEXTAREA>
    </TD>
  </TR>
</TABLE>
<TABLE CLASS="home fullsize" >
  <TR >
    <TD CLASS="port strcol" >Medication Follow-up</TD>
    <TD CLASS="strcol" COLSPAN="2" >
[enter '*' for entire list]
      Search: <INPUT TYPE="text" ID="SearchPhysNPI" NAME="SearchPhysNPI" VALUE="" ONFOCUS="select()" ONCHANGE="callAjax('Physicians','<<ClientDischarge_PhysNPI_1>>','selPhysNPI','&name=ClientDischarge_PhysNPI_1&pattern='+this.value,'popup.pl');" SIZE="60" >
<BR><SPAN ID="selPhysNPI"></SPAN>
    </TD>
  </TR>
  <TR >
    <TD CLASS="port strcol" >Referrals</TD>
    <TD CLASS="strcol" COLSPAN="2" >
[enter '*' for entire list]
      Search: <INPUT TYPE="text" ID="SearchRef" NAME="SearchRef" VALUE="" ONFOCUS="select()" ONCHANGE="callAjax('Agency','<<ClientDischarge_ReferralsNPI_1>>','selRef','&name=ClientDischarge_ReferralsNPI_1&pattern='+this.value,'popup.pl');" SIZE="60" >
<BR><SPAN ID="selRef"></SPAN>
    </TD>
  </TR>
  <TR > <TD CLASS="port strcol" COLSPAN="3" >Other Referral (not in list)</TD> </TR>
  <TR >
    <TD CLASS="strcol" >&nbsp;</TD>
    <TD CLASS="port strcol" >Type</TD>
    <TD CLASS="port strcol" >Name</TD>
  </TR>
  <TR >
    <TD CLASS="strcol" >&nbsp;</TD>
    <TD CLASS="strcol" >
      <INPUT TYPE=text NAME="ClientDischarge_OthRefType_1" VALUE="<<ClientDischarge_OthRefType_1>>" ONFOCUS="select()" SIZE="20" >
    </TD>
    <TD CLASS="strcol" >
      <INPUT TYPE=text NAME="ClientDischarge_OthRefName_1" VALUE="<<ClientDischarge_OthRefName_1>>" ONFOCUS="select()" SIZE="30" >
    </TD>
  </TR>
  <TR >
    <TD CLASS="strcol" >&nbsp;</TD>
    <TD CLASS="port strcol" >Address</TD>
    <TD CLASS="port strcol" >Phone</TD>
  </TR>
  <TR >
    <TD CLASS="strcol" >&nbsp;</TD>
    <TD CLASS="strcol" >
      <INPUT TYPE=text NAME="ClientDischarge_OthRefAddr_1" VALUE="<<ClientDischarge_OthRefAddr_1>>" ONFOCUS="select()" SIZE="50" >
    </TD>
    <TD CLASS="strcol" >
      <INPUT TYPE=text NAME="ClientDischarge_OthRefWkPh_1" VALUE="<<ClientDischarge_OthRefWkPh_1>>" ONFOCUS="select()" SIZE="20" >
    </TD>
  </TR>
</TABLE>
<TABLE CLASS="home fullsize" >
  <TR >
    <TD CLASS="port hdrtxt" COLSPAN="2" >Response of Client
    </TD>
  </TR>
  <TR >
    <TD CLASS="strcol" COLSPAN="2" >
       <TEXTAREA NAME="ClientDischarge_Response_1" COLS="80" ROWS="5" WRAP="virtual" ><<ClientDischarge_Response_1>></TEXTAREA>
    </TD>
  </TR>
</TABLE>
<TABLE CLASS="home fullsize" >
  <TR>
    <TD CLASS="port strcol" >Client was given a copy of this plan</TD>
    <TD CLASS="strcol" >
      <INPUT TYPE=checkbox NAME="ClientDischarge_ClientCopy_1" VALUE=1 <<ClientDischarge_ClientCopy_1=checkbox>> >
    </TD>
  </TR>
  <TR>
    <TD CLASS="port strcol" COLSPAN="2" >Client received resource list information regarding treatment options if symptoms recur or additional services are needed</TD>
  </TR>
  <TR>
    <TD CLASS="port strcol" >Received By</TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="radio" NAME="ClientDischarge_ReceivedBy_1" VALUE="M" <<ClientDischarge_ReceivedBy_1=M>> > Mail
      <INPUT TYPE="radio" NAME="ClientDischarge_ReceivedBy_1" VALUE="P" <<ClientDischarge_ReceivedBy_1=P>> > In Person
    </TD>
  </TR>
  <TR>
    <TD CLASS="port strcol" >Others given copy of this plan</TD>
    <TD CLASS="strcol" >
      <SELECT NAME="ClientDischarge_OthersCopy_1" MULTIPLE SIZE="10" >
        [[DBA->selxTable(%form+xRelationship+<<ClientDischarge_OthersCopy_1>>+Descr)]]
      </SELECT>
    </TD>
  </TR>
</TABLE>
<TABLE CLASS="home fullsize" >
  <TR > <TD CLASS="port hdrtxt" COLSPAN="2" >JOLTS Information </TD> </TR>
  <TR >
    <TD CLASS="port strcol" >Program/Service Effectiveness Ratings</TD>
    <TD CLASS="strcol" >
      <SELECT NAME="ClientDischarge_Effective_1" MULTIPLE SIZE="6" >[[DBA->selxTable(%form+xDisEffective+<<ClientDischarge_Effective_1>>+ID Descr)]]</SELECT>
    </TD>
  </TR>
</TABLE>
<TABLE CLASS="home fullsize" >
  <TR >
    <TD CLASS="port strcol" >Discharge Reason</TD>
    <TD CLASS="strcol" >
      <SELECT NAME="ClientDischarge_Reason_1" >[[DBA->selxTable(%form+xDisReason+<<ClientDischarge_Reason_1>>+Descr Complied)]]</SELECT>
    </TD>
  </TR>
</TABLE>
<TABLE CLASS="home fullsize" >
  <TR >
    <TD CLASS="port strcol" >Discharge Destinations</TD>
    <TD CLASS="strcol" >
      <SELECT NAME="ClientDischarge_Destination_1" >[[DBA->selxTable(%form+xDisDestination+<<ClientDischarge_Destination_1>>)]]</SELECT>
    </TD>
  </TR>
</TABLE>
<TABLE CLASS="home fullsize" >
  <TR >
    <TD CLASS="port hdrtxt" COLSPAN="2" >Follow-up Results <FONT SIZE="-2">(After the followup is completed, any comments or results reguarding the inteview?):</FONT>
    </TD>
  </TR>
  <TR >
    <TD CLASS="strcol" COLSPAN="2" >
       <TEXTAREA NAME="ClientDischarge_FollowUpResults_1" COLS="80" ROWS="5" WRAP="virtual" ><<ClientDischarge_FollowUpResults_1>></TEXTAREA>
    </TD>
  </TR>
</TABLE>
<TABLE CLASS="home fullsize" >
  <TR >
    <TD CLASS="port strcol" >Staff Responsible for Follow-Up of Referrals</TD>
    <TD CLASS="strcol" >
      <SELECT NAME="ClientDischarge_StaffID_1" >[[DBA->selProviders(%form+<<ClientDischarge_StaffID_1>>)]]</SELECT> 
    </TD>
  </TR>
  <TR >
    <TD CLASS="port strcol" >Follow-up Date</TD>
    <TD CLASS="strcol" COLSPAN="2" >
      <INPUT TYPE=text NAME="ClientDischarge_FollowUpDate_1" VALUE="<<ClientDischarge_FollowUpDate_1>>" ONFOCUS="select()" ONCHANGE="return vDate(this)" SIZE="10" >
    </TD>
  </TR>
</TABLE>
<TABLE CLASS="main fullsize" >
  <TR>
    <TD CLASS="numcol" >
[[myTables->htmLocked(%form+<<<ClientDischarge_Locked_1>>>+ClientDischarge)]]
    </TD>
  </TR>
</TABLE>

<INPUT TYPE="hidden" NAME="post_update" VALUE="PostUpd->updDischarge(%form+<<<Client_ClientID_1>>>+<<<ClientDischarge_ID_1>>>)" >
</LOADHIDDEN>
</FORM>
<SCRIPT LANGUAGE="JavaScript">
document.ClientDischarge.elements[0].focus();
callAjax('Physicians','<<ClientDischarge_PhysNPI_1>>','selPhysNPI','&name=ClientDischarge_PhysNPI_1','popup.pl');
callAjax('Agency','<<ClientDischarge_ReferralsNPI_1>>','selRef','&name=ClientDischarge_ReferralsNPI_1','popup.pl');
</SCRIPT>

[[myHTML->rightpane(%form+search)]]
