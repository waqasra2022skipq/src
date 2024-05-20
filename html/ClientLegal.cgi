[[myHTML->newPage(%form+Legal)]]

<SCRIPT LANGUAGE="JavaScript" SRC="/cgi/js/vEntry.js"> </SCRIPT>
<SCRIPT LANGUAGE="JavaScript" SRC="/cgi/js/vClientLegal.js"> </SCRIPT>
<SCRIPT LANGUAGE="JavaScript" SRC="/cgi/js/vPhone.js"> </SCRIPT>
<SCRIPT LANGUAGE="JavaScript" SRC="/cgi/js/vNum.js"> </SCRIPT>

<FORM NAME="Legal" ACTION="/cgi/bin/mis.cgi" METHOD="POST" >
<TABLE CLASS="main fullsize" >
  <TR >
    <TD CLASS="strcol" >
      <<<Client_FName_1>>> <<<Client_MName_1>>> <<<Client_LName_1>>> (<<<Client_ClientID_1>>>) <<<Client_SSN_1>>>
      <BR>
      Legal Page
    </TD>
    <TD CLASS="numcol" >[[gHTML->setLINKS(%form+back)]]</TD>
  </TR>
</TABLE>
<TABLE CLASS="home fullsize" >
  <TR ><TD CLASS="port hdrtxt" COLSPAN="2" >Current Legal</TD></TR>
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
    <TD CLASS="strcol" >Custodial Agency - Custody/Referral Type</TD>
    <TD CLASS="strcol" >
      <SELECT NAME="ClientLegal_CustAgency_1" >
        [[DBA->selxTable(%form+xCustAgency+<<ClientLegal_CustAgency_1>>+Descr)]]
      </SELECT> 
    </TD>
  </TR>
  <TR >
    <TD CLASS="strcol" >JOLTS #</TD>
    <TD CLASS="strcol" >
      <INPUT TYPE=text NAME="ClientLegal_JOLTS_1" VALUE="<<ClientLegal_JOLTS_1>>" ONFOCUS="select()" SIZE="40" >
      (children/adolescents)
    </TD>
  </TR>
  <TR >
    <TD CLASS="strcol" >CASE ID#</TD>
    <TD CLASS="strcol" >
      <INPUT TYPE=text NAME="ClientLegal_CASEID_1" VALUE="<<ClientLegal_CASEID_1>>" ONFOCUS="select()" SIZE="40" >
      (Drug Court #, DOC #, DHS Case # or FamilyID)
    </TD>
  </TR>
  <TR >
    <TD CLASS="strcol" >&nbsp;</TD>
    <TD CLASS="strcol" >
      For Drug Court Case ID must be 3 Letters followed by 7 digits<BR>
      So...Use OSCN.net docket case number, add "D" for drug 2nd letter and truncate the last digit for case numbers with 8 digits.  This will allow for the 10 character maximum.
    </TD>
  </TR>
  <TR ><TD CLASS="port hdrtxt" COLSPAN="2" >Probation and Parole</TD> </TR>
  <TR >
    <TD CLASS="strcol" >Are you on parole or probation?</TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="radio" NAME="ClientLegal_OnPP_1" VALUE=0 <<ClientLegal_OnPP_1=0>> > No
      <INPUT TYPE="radio" NAME="ClientLegal_OnPP_1" VALUE=1 <<ClientLegal_OnPP_1=1>> > Yes · Note duration and level in comments. 
    </TD>
  </TR>
  <TR >
    <TD CLASS="strcol" COLSPAN="2" >
<SPAN ID="ListClientLegalPP" >
[[myHTML->ListSel(%form+ListClientLegalPP+<<<Client_ClientID>>>+<<<LINKID>>>+<<<Client_Locked_1>>>)]]
</SPAN>
    </TD>
  </TR>
  <TR ><TD CLASS="port hdrtxt" COLSPAN="2" >Legal History</TD> </TR>
  <TR >
    <TD CLASS="strcol" >How many times have you been arrested in the past 12 months, or since admission if less than 12 months?</TD>
    <TD CLASS="strcol" >
      <INPUT TYPE=text NAME="ClientLegal_Arrested_1" VALUE="<<ClientLegal_Arrested_1>>" ONFOCUS="select()" ONCHANGE="return vNum(this,0,99);" MAXLENGTH="3" SIZE="3" >
    </TD>
  </TR>
  <TR >
    <TD CLASS="strcol" >Of those arrests, how many have occurred in the past 30 days, or since admission if less than 30 days? </TD>
    <TD CLASS="strcol" >
      <INPUT TYPE=text NAME="ClientLegal_Arrest1_1" VALUE="<<ClientLegal_Arrest1_1>>" ONFOCUS="select()" ONCHANGE="return vNum(this,0,99);" MAXLENGTH="3" SIZE="3" >
    </TD>
  </TR>
  <TR >
    <TD CLASS="strcol" >Are you currently in jail?</TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="radio" NAME="ClientLegal_InJail_1" VALUE=0 <<ClientLegal_InJail_1=0>> > No
      <INPUT TYPE="radio" NAME="ClientLegal_InJail_1" VALUE=1 <<ClientLegal_InJail_1=1>> > Yes
    </TD>
  </TR>
  <TR >
    <TD CLASS="strcol" COLSPAN="2" >
[[myHTML->ListSel(%form+ListClientLegalHx+<<<Client_ClientID>>>+<<<LINKID>>>+<<<Client_Locked_1>>>)]]
    </TD>
  </TR>
</TABLE>
<TABLE CLASS="main fullsize" >
  <TR >
    <TD CLASS="numcol" >
      <INPUT TYPE=submit ONCLICK="return validate(this.form);" NAME="UpdateTables=all&[[myForm->genLink(ClientIntake+ClientSocial.cgi)]]" VALUE="Add/Update -> Social">
      <INPUT TYPE=submit ONCLICK="return validate(this.form);" NAME="UpdateTables=all&misPOP=1" VALUE="Add/Update">
    </TD>
  </TR>
</TABLE>

<INPUT TYPE="hidden" NAME="post_update" VALUE="PostUpd->updPA(%form+<<<Client_ClientID_1>>>)" >
</LOADHIDDEN>
</FORM>
<SCRIPT LANGUAGE="JavaScript">
document.Legal.elements[0].focus();
</SCRIPT>

[[myHTML->rightpane(%form+search)]]
