[[myHTML->newPage(%form+Client Treatment Plan)]]

<SCRIPT LANGUAGE="JavaScript" SRC="/src/cgi/js/chkLock.js"> </SCRIPT>
<SCRIPT LANGUAGE="JavaScript" SRC="/src/cgi/js/vEntry.js"> </SCRIPT>
<SCRIPT LANGUAGE="JavaScript" SRC="/src/cgi/js/vTrPlan.js"> </SCRIPT>
<SCRIPT type="text/javascript" src="/src/cgi/js/ajaxrequest.js"></SCRIPT>
<SCRIPT LANGUAGE="JavaScript" SRC="/src/cgi/js/mDate.js"> </SCRIPT>
<SCRIPT LANGUAGE="JavaScript" SRC="/src/cgi/js/vDate.js"> </SCRIPT>

<FORM NAME="ClientTrPlan" ACTION="/src/cgi/bin/mis.cgi" METHOD="POST" >
<TABLE CLASS="main fullsize" >
  <TR >
    <TD CLASS="strcol" >
      <<<Client_FName_1>>> <<<Client_MName_1>>> <<<Client_LName_1>>> (<<<Client_ClientID_1>>>) <<<Client_SSN_1>>>
      <BR>
      Client's Treatment Plan
    </TD>
    <TD CLASS="numcol" >[[gHTML->setLINKS(%form+back)]]</TD>
  </TR>
</TABLE>
<TABLE CLASS="home fullsize" >
  <TR ><TD CLASS="port hdrtxt" >Treatment Plan</TD></TR>
  <TR ><TD CLASS="hdrcol" >Type</TD></TR>
  <TR >
    <TD CLASS="hdrcol" >
      <SELECT NAME="ClientTrPlan_Type_1" >
        [[DBA->selxTable(%form+xTrPlanType+<<ClientTrPlan_Type_1>>+Descr)]]
      </SELECT> 
    </TD>
  </TR>
  <TR ><TD CLASS="hdrcol" >Effective Date</TD></TR>
  <TR >
    <TD CLASS="hdrcol" >
      <INPUT TYPE="text" NAME="ClientTrPlan_EffDate_1" VALUE="<<ClientTrPlan_EffDate_1>>" ONFOCUS="select();" ONCHANGE="return vSetDate(this,1,this.form,'ClientTrPlan_ExpDate_1',6,-1)" SIZE="10" >
    </TD>
  </TR>
  <TR ><TD CLASS="hdrcol" >Expire Date</TD></TR>
  <TR >
    <TD CLASS="hdrcol" >
      <INPUT TYPE="text" NAME="ClientTrPlan_ExpDate_1" VALUE="<<ClientTrPlan_ExpDate_1>>" ONFOCUS="select();" ONCHANGE="return vDate(this)" MAXLENGTH="10" SIZE="10" >
    </TD>
  </TR>
  <TR ><TD >&nbsp;</TD></TR>
  <TR ><TD ><B>Leave Any Inapplicable Fields Blank</B></TD></TR>
  <TR > <TD CLASS="port hdrtxt" >Persons Involved with Treatment/Transition Planning</TD> </TR>
  <TR >
    <TD CLASS="strcol" >
      <INPUT TYPE="text" NAME="ClientTrPlan_PersonsInvolved_1" VALUE="<<ClientTrPlan_PersonsInvolved_1>>" ONFOCUS="select();" SIZE="50" >
    </TD>
  </TR>
  <TR ><TD CLASS="port hdrtxt" >Strengths/Needs/Abilities/Preferences<BR>(In Client's Words)</TD></TR>
  <TR>
    <TD CLASS="strcol" >
      <INPUT TYPE="text" NAME="ClientTrPlan_SA1_1" VALUE="<<ClientTrPlan_SA1_1>>" ONFOCUS="select();" SIZE="100" >
    </TD>
  </TR>
  <TR>
    <TD CLASS="strcol" >
      <INPUT TYPE="text" NAME="ClientTrPlan_SA2_1" VALUE="<<ClientTrPlan_SA2_1>>" ONFOCUS="select();" SIZE="100" >
    </TD>
  </TR>
  <TR>
    <TD CLASS="strcol" >
      <INPUT TYPE="text" NAME="ClientTrPlan_SA3_1" VALUE="<<ClientTrPlan_SA3_1>>" ONFOCUS="select();" SIZE="100" >
    </TD>
  </TR>
  <TR>
    <TD CLASS="strcol" >
      <INPUT TYPE="text" NAME="ClientTrPlan_SA4_1" VALUE="<<ClientTrPlan_SA4_1>>" ONFOCUS="select();" SIZE="100" >
    </TD>
  </TR>
  <TR ><TD CLASS="hdrtxt" >Liabilities and Needs<BR>(In Client's Words)</TD></TR>
  <TR>
    <TD CLASS="strcol" >
      <INPUT TYPE="text" NAME="ClientTrPlan_L1_1" VALUE="<<ClientTrPlan_L1_1>>" ONFOCUS="select();" SIZE="100" >
    </TD>
  </TR>
  <TR>
    <TD CLASS="strcol" >
      <INPUT TYPE="text" NAME="ClientTrPlan_L2_1" VALUE="<<ClientTrPlan_L2_1>>" ONFOCUS="select();" SIZE="100" >
    </TD>
  </TR>
  <TR>
    <TD CLASS="strcol" >
      <INPUT TYPE="text" NAME="ClientTrPlan_L3_1" VALUE="<<ClientTrPlan_L3_1>>" ONFOCUS="select();" SIZE="100" >
    </TD>
  </TR>
  <TR>
    <TD CLASS="strcol" >
      <INPUT TYPE="text" NAME="ClientTrPlan_L4_1" VALUE="<<ClientTrPlan_L4_1>>" ONFOCUS="select();" SIZE="100" >
    </TD>
  </TR>
  <TR ><TD CLASS="port hdrtxt" >Theoretical Approach Being Utilized with Individual Psychotherapy</TD></TR>
  <TR>
    <TD CLASS="hdrcol" >
      <SELECT NAME="ClientTrPlan_Theoretical_1" SIZE="7" MULTIPLE >
        [[DBA->selxTable(%form+xTrPlanTheoretical+<<ClientTrPlan_Theoretical_1>>+Descr)]]
      </SELECT> 
    </TD>
  </TR>
  <TR ><TD CLASS="port hdrtxt" >Client's Preferences</TD></TR>
  <TR>
    <TD CLASS="strcol" >
      <TEXTAREA COLS="120" ROWS="5" WRAP="virtual" NAME="ClientTrPlan_Preferences_1" ONFOCUS="select();" ><<ClientTrPlan_Preferences_1>></TEXTAREA>
    </TD>
  </TR>
  <TR ><TD CLASS="port hdrtxt" >Discharge Criteria</TD></TR>
  <TR>
    <TD CLASS="strcol" >
      <TEXTAREA COLS="120" ROWS="5" WRAP="virtual" NAME="ClientTrPlan_DischargeCriteria_1" ONFOCUS="select();" ><<ClientTrPlan_DischargeCriteria_1>></TEXTAREA>
    </TD>
  </TR>
  <TR>
    <TD CLASS="strcol" >
      <INPUT TYPE="checkbox" NAME="ClientTrPlan_Agrees_1" VALUE=1 <<ClientTrPlan_Agrees_1=1>> ONFOCUS="select();" >
      <B>Client Agrees</B>
    </TD>
  </TR>
  <TR>
    <TD CLASS="strcol" >
      <B>Estimated Date of Discharge</B>
      <INPUT TYPE="text" NAME="ClientTrPlan_EstDischargeDate_1" VALUE="<<ClientTrPlan_EstDischargeDate_1>>" ONFOCUS="select();" ONCHANGE="return vDate(this,1)" SIZE="15" >
    </TD>
  </TR>
</TABLE>
<TABLE CLASS="home fullsize" >
  <TR ><TD CLASS="port hdrtxt" >Interpretive Summary/Additional Information</TD></TR>
  <TR>
    <TD CLASS="strcol" >
      <TEXTAREA COLS="120" ROWS="7" WRAP="virtual" NAME="ClientTrPlan_Summary_1" ONFOCUS="select();" ><<ClientTrPlan_Summary_1>></TEXTAREA>
    </TD>
  </TR>
  <TR ><TD CLASS="hdrtxt" >Historical Information<BR>(relevant to current diagnosis and treatment)</TD></TR>
  <TR>
    <TD CLASS="strcol" >
      <TEXTAREA COLS="120" ROWS="7" WRAP="virtual" NAME="ClientTrPlan_Comments_1" ONFOCUS="select();" ><<ClientTrPlan_Comments_1>></TEXTAREA>
    </TD>
  </TR>
</TABLE>
<TABLE CLASS="home fullsize" >
  <TR> <TD CLASS="port hdrtxt" COLSPAN="2" >Treatment Recommendations / Transition Plan</TD> </TR>
  <TR ><TD CLASS="hdrtxt" >Transition Plan</TD><TD >&nbsp;</TD></TR>
  <TR>
    <TD CLASS="strcol" COLSPAN="2" >
      <TEXTAREA COLS="120" ROWS="5" WRAP="virtual" NAME="ClientTrPlan_TransitionPlan_1" ONFOCUS="select();" ><<ClientTrPlan_TransitionPlan_1>></TEXTAREA>
    </TD>
  </TR>
  <TR > <TD CLASS="strcol" COLSPAN="2" >Collaborative Referrals</TD> </TR>
  <TR>
    <TD CLASS="strcol" COLSPAN="2" >
      [to select multiples, enter a 'space' and hit tab for the entire list]
      <BR>
      Search: <INPUT TYPE="text" ID="SearchRef" NAME="SearchRef" VALUE="" ONFOCUS="select();" ONCHANGE="callAjax('Agency','<<ClientTrPlan_ReferralsNPI_1>>','selRef','&name=ClientTrPlan_ReferralsNPI_1&pattern='+this.value,'popup.pl');" SIZE="60" >
<BR><SPAN ID="selRef"></SPAN>
    </TD>
  </TR>
  <TR> <TD CLASS="strcol" >Services to be provided<BR>(Check all that apply)</TD> </TR>
  <TR >
    <TD CLASS="strcol" >
      <SELECT NAME="ClientTrPlan_Services_1" SIZE="10" MULTIPLE >
        [[DBA->selxTable(%form+xServices+<<ClientTrPlan_Services_1>>+Descr)]]
      </SELECT> 
    </TD>
  </TR>
  <TR >
    <TD CLASS="strcol" WIDTH="30%" >Staff Responsible for Follow-Up of Referrals</TD>
    <TD CLASS="strcol" >
      <SELECT NAME="ClientTrPlan_StaffID_1" SIZE="10" >[[DBA->selProviders(%form+<<ClientTrPlan_StaffID_1>>)]]</SELECT> 
    </TD>
  </TR>
</TABLE>
<TABLE CLASS="home fullsize" >
  <TR><TD CLASS="port hdrtxt" COLSPAN="2" >Client received resource list information regarding treatment options<BR>(if symptoms recur or additional services are needed)</TD></TR>
  <TR>
    <TD CLASS="strcol" WIDTH="30%" >Received By</TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="radio" NAME="ClientTrPlan_ReceivedBy_1" VALUE="M" <<ClientTrPlan_ReceivedBy_1=M>> > Mail
      <INPUT TYPE="radio" NAME="ClientTrPlan_ReceivedBy_1" VALUE="P" <<ClientTrPlan_ReceivedBy_1=P>> > In Person
    </TD>
  </TR>
  <TR>
    <TD CLASS="strcol" WIDTH="30%" >Client was given a copy of this plan</TD>
    <TD CLASS="strcol" >
      <INPUT TYPE=checkbox NAME="ClientTrPlan_ClientCopy_1" VALUE=1 <<ClientTrPlan_ClientCopy_1=checkbox>> >
    </TD>
  </TR>
  <TR>
    <TD CLASS="strcol" WIDTH="30%" >Others given copy of this plan</TD>
    <TD CLASS="strcol" >
      <SELECT NAME="ClientTrPlan_OthersCopy_1" MULTIPLE SIZE="10" >
        [[DBA->selxTable(%form+xRelationship+<<ClientTrPlan_OthersCopy_1>>+Descr)]]
      </SELECT>
    </TD>
  </TR>
</TABLE>
<TABLE CLASS="home fullsize" >
  <TR ><TD CLASS="port hdrtxt" COLSPAN="2" >Treatment Plan Signatures</TD></TR>
  <TR>
    <TD CLASS="strcol" WIDTH=20% >Client:</TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="text" NAME="ClientTrPlan_ClSigDate_1" VALUE="<<ClientTrPlan_ClSigDate_1>>" ONFOCUS="select();" ONCHANGE="return vDate(this,1)" SIZE="15" >
    </TD>
  </TR>
  <TR>
    <TD CLASS="strcol" WIDTH=20% >Parent/Guardian:</TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="text" NAME="ClientTrPlan_PGSigDate_1" VALUE="<<ClientTrPlan_PGSigDate_1>>" ONFOCUS="select();" ONCHANGE="return vDate(this,1)" SIZE="15" >
    </TD>
  </TR>
  <TR>
    <TD CLASS="strcol" WIDTH=20% >Physician:</TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="text" NAME="ClientTrPlan_PhSigDate_1" VALUE="<<ClientTrPlan_PhSigDate_1>>" ONFOCUS="select();" ONCHANGE="return vDate(this,1)" SIZE="15" >
      Required on all TxPlans only if Meds prescribed
    </TD>
  </TR>
</TABLE>
<TABLE CLASS="main fullsize" >
  <TR>
    <TD CLASS="numcol" >
[[myTables->htmLocked(%form+<<<ClientTrPlan_Locked_1>>>+ClientTrPlan)]]
    </TD>
  </TR>
</TABLE>
<TABLE CLASS="home fullsize" >
  <TR >
    <TD CLASS="port hdrtxt" >
      Please Enter Treatment Plan/Problems Goals and Objectives to COMPLETE
    </TD>
  </TR>
  <TR >
    <TD CLASS="port hdrtxt" >
<SPAN ID="ListClientTrPlanPG" >
[[myHTML->ListSel(%form+ListClientTrPlanPG+<<<ClientTrPlan_ID>>>+<<<LINKID>>>+<<<ClientTrPlan_Locked_1>>>)]]
</SPAN>
    </TD>
  </TR>
</TABLE>

<INPUT TYPE="hidden" NAME="post_update" VALUE="PostUpd->updClientTrPlan(%form+<<<ClientTrPlan_ID>>>)" >
</LOADHIDDEN>
</FORM>
<SCRIPT LANGUAGE="JavaScript">
document.ClientTrPlan.elements[0].focus();
callAjax('Agency','<<ClientTrPlan_ReferralsNPI_1>>','selRef','&name=ClientTrPlan_ReferralsNPI_1','popup.pl');
</SCRIPT>

[[myHTML->rightpane(%form+search)]]
