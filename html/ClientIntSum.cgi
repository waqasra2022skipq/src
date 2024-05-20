[[myHTML->newPage(%form+Client Summary)]]

<SCRIPT LANGUAGE="JavaScript" SRC="/cgi/js/vEntry.js"> </SCRIPT>
<SCRIPT LANGUAGE="JavaScript" SRC="/cgi/js/vClientIntSum.js"> </SCRIPT>
<SCRIPT type="text/javascript" src="/cgi/js/ajaxrequest.js"></SCRIPT>

<FORM NAME="Summary" ACTION="/cgi/bin/mis.cgi" METHOD="POST" >
<TABLE CLASS="main fullsize" >
  <TR >
    <TD CLASS="strcol" >
      <<<Client_FName_1>>> <<<Client_MName_1>>> <<<Client_LName_1>>> (<<<Client_ClientID_1>>>) <<<Client_SSN_1>>>
      <BR>
      Summary Page
    </TD>
    <TD CLASS="numcol" >[[gHTML->setLINKS(%form+back)]]</TD>
  </TR>
</TABLE>
<TABLE CLASS="port fullsize" >
    <TR ><TD ><TABLE CLASS="home fullsize" >
  <TR ><TD CLASS="port hdrtxt" >Strengths/Abilities <I>(In Client's Words)</I></TD></TR>
  <TR>
    <TD CLASS="strcol" >
      <INPUT TYPE="text" NAME="ClientSummary_S1_1" VALUE="<<ClientSummary_S1_1>>" ONFOCUS="select()" SIZE="80" >
    </TD>
  </TR>
  <TR>
    <TD CLASS="strcol" >
      <INPUT TYPE="text" NAME="ClientSummary_S2_1" VALUE="<<ClientSummary_S2_1>>" ONFOCUS="select()" SIZE="80" >
    </TD>
  </TR>
  <TR>
    <TD CLASS="strcol" >
      <INPUT TYPE="text" NAME="ClientSummary_S3_1" VALUE="<<ClientSummary_S3_1>>" ONFOCUS="select()" SIZE="80" >
    </TD>
  </TR>
  <TR>
    <TD CLASS="strcol" >
      <INPUT TYPE="text" NAME="ClientSummary_S4_1" VALUE="<<ClientSummary_S4_1>>" ONFOCUS="select()" SIZE="80" >
    </TD>
  </TR>
  <TR ><TD CLASS="port hdrtxt" >Needs, Liabilities and Barriers <I>(In Client's Words)</I></TD></TR>
  <TR>
    <TD CLASS="strcol" >
      <INPUT TYPE="text" NAME="ClientSummary_L1_1" VALUE="<<ClientSummary_L1_1>>" ONFOCUS="select()" SIZE="80" >
    </TD>
  </TR>
  <TR>
    <TD CLASS="strcol" >
      <INPUT TYPE="text" NAME="ClientSummary_L2_1" VALUE="<<ClientSummary_L2_1>>" ONFOCUS="select()" SIZE="80" >
    </TD>
  </TR>
  <TR>
    <TD CLASS="strcol" >
      <INPUT TYPE="text" NAME="ClientSummary_L3_1" VALUE="<<ClientSummary_L3_1>>" ONFOCUS="select()" SIZE="80" >
    </TD>
  </TR>
  <TR>
    <TD CLASS="strcol" >
      <INPUT TYPE="text" NAME="ClientSummary_L4_1" VALUE="<<ClientSummary_L4_1>>" ONFOCUS="select()" SIZE="80" >
    </TD>
  </TR>
  <TR ><TD CLASS="port hdrtxt" >Client's Preferences</TD></TR>
  <TR>
    <TD CLASS="strcol" >
      <TEXTAREA NAME="ClientSummary_Prefs_1" ONFOCUS="select()" WRAP="virtual" COLS="70" ROWS="5" ><<ClientSummary_Prefs_1>></TEXTAREA>
    </TD>
  </TR>
  <TR ><TD CLASS="port hdrtxt" >Client's Overall Expectation from Treatment</TD></TR>
  <TR>
    <TD CLASS="strcol" >
      <TEXTAREA NAME="ClientSummary_Overall_1" ONFOCUS="select()" WRAP="virtual" COLS="70" ROWS="5" ><<ClientSummary_Overall_1>></TEXTAREA>
    </TD>
  </TR>
  <TR ><TD CLASS="port hdrtxt" >Client's Stage of Change</TD></TR>
  <TR >
    <TD CLASS="strcol" >
      <SELECT NAME="ClientSummary_Stage_1" > [[DBA->selxTable(%form+xStageOfChange+<<ClientSummary_Stage_1>>+Descr)]] </SELECT> 
    </TD>
  </TR>
    </TABLE></TD></TR>
    <TR ><TD ><TABLE CLASS="home fullsize" >
  <TR ><TD CLASS="port hdrtxt" COLSPAN="2" >Interpretive Summary<BR>(for Referral Screening specify problems, disposition, referrals if any. If services not appropriate state reason)</TD></TR>
  <TR>
    <TD CLASS="strcol" COLSPAN="2" >
       <TEXTAREA NAME="ClientIntake_Summary_1" COLS=90 ROWS=10 WRAP=virtual ><<ClientIntake_Summary_1>></TEXTAREA>
    </TD>
  </TR>
  <TR ><TD CLASS="port hdrtxt" COLSPAN="2" >Alert</TD></TR>
  <TR>
    <TD CLASS="strcol" >Hospice Alert?
      <input type="checkbox" value="1" name="ClientEmergency_HospiceCheck_1" <<ClientEmergency_HospiceCheck_1=checkbox>>>
    </TD>
  </TR>
  <TR>
    <TD CLASS="strcol" >Should there be an item of concern briefly identify the nature of the concern?</TD>
    <TD CLASS="strcol" >
      <TEXTAREA NAME="ClientEmergency_Alert_1" COLS="80" ROWS="5" WRAP="virtual" ><<ClientEmergency_Alert_1>></TEXTAREA>
    </TD>
  </TR>
    </TABLE></TD></TR>
  <TR ><TD CLASS="port heading" >RECOMMENDATIONS</TD></TR>
    <TR ><TD ><TABLE CLASS="home fullsize" >
  <TR ><TD CLASS="port hdrtxt" >Level of Care</TD></TR>
  <TR >
    <TD CLASS="strcol" >
      <SELECT NAME="ClientIntake_LOC_1" >[[DBA->selxTable(%form+xLOC+<<ClientIntake_LOC_1>>+ID Descr)]]</SELECT> 
    </TD>
  </TR>
  <TR >
    <TD CLASS="port hdrtxt" >
      Service Focus
     <A HREF="javascript:ReportWindow('/docs/ODMHSAS_CDC Service Focus Requirements with AutoPA_20100601.pdf','Requirements')" ONMOUSEOVER="window.status='Requirement for Service Focus'; return true;" ONMOUSEOUT="window.status=''">(Requirements)</A>
    </TD>
  </TR>
  <TR >
    <TD CLASS="strcol" >
      <SELECT NAME="ClientIntake_ServiceFocus_1" SIZE="10" >
        [[DBA->selxTable(%form+xServiceFocus+<<ClientIntake_ServiceFocus_1>>+Descr CDC)]]
      </SELECT> 
    </TD>
  </TR>
  <TR > <TD CLASS="port hdrtxt" >Collaborative Referrals</TD> </TR>
  <TR > <TD CLASS="strcol" WIDTH="40%" >ie: school (or you may enter partial zipcode)</TD> </TR>
  <TR > <TD CLASS="strcol" WIDTH="40%" >To select multiples, enter a 'space' and hit tab for the entire list</TD> </TR>
  <TR>
    <TD CLASS="strcol" >
      Search: <INPUT TYPE="text" ID="SearchRef" NAME="SearchRef" VALUE="" ONFOCUS="select()" ONCHANGE="callAjax('Agency','<<ClientIntake_ReferralsNPI_1>>','selRef','&name=ClientIntake_ReferralsNPI_1&pattern='+this.value,'popup.pl');" SIZE="60" >
<BR><SPAN ID="selRef"></SPAN>
    </TD>
  </TR>
  <TR> <TD CLASS="port hdrtxt" >Services to be provided<BR>(Check all that apply)</TD> </TR>
  <TR >
    <TD CLASS="strcol" >
      <SELECT NAME="ClientIntake_Services_1" MULTIPLE SIZE="10" >
        [[DBA->selxTable(%form+xServices+<<ClientIntake_Services_1>>+Descr)]]
      </SELECT> 
    </TD>
  </TR>
    </TABLE></TD></TR>
</TABLE>

<TABLE CLASS="main fullsize" >
  <TR >
    <TD CLASS="numcol" >
      <INPUT TYPE="submit" ONCLICK="return validate(this.form);" NAME="UpdateTables=all&misPOP=1" VALUE="Add/Update">
    </TD>
  </TR>
</TABLE>

<INPUT TYPE="hidden" NAME="post_update" VALUE="PostUpd->updPA(%form+<<<Client_ClientID_1>>>)" >
</LOADHIDDEN>
</FORM>
<SCRIPT LANGUAGE="JavaScript">
document.Summary.elements[0].focus();
callAjax('Agency','<<ClientIntake_ReferralsNPI_1>>','selRef','&name=ClientIntake_ReferralsNPI_1','popup.pl');
</SCRIPT>

[[myHTML->rightpane(%form+search)]]
