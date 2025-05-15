[[myHTML->newPage(%form+Authorized Units)]]

<SCRIPT LANGUAGE="JavaScript" SRC="/src/cgi/js/NoEnter.js"> </SCRIPT>
<SCRIPT LANGUAGE="JavaScript" SRC="/src/cgi/js/chkLock.js"> </SCRIPT>
<SCRIPT LANGUAGE="JavaScript" SRC="/src/cgi/js/vEntry.js"> </SCRIPT>
<SCRIPT LANGUAGE="JavaScript" SRC="/src/cgi/js/vPrAuthRVU.js"> </SCRIPT>
<SCRIPT LANGUAGE="JavaScript" SRC="/src/cgi/js/mDate.js"> </SCRIPT>
<SCRIPT LANGUAGE="JavaScript" SRC="/src/cgi/js/vDate.js"> </SCRIPT>
<SCRIPT LANGUAGE="JavaScript" SRC="/src/cgi/js/vAuthNum.js"> </SCRIPT>
<SCRIPT LANGUAGE="JavaScript" SRC="/src/cgi/js/vNum.js"> </SCRIPT>
<SCRIPT LANGUAGE="JavaScript" >
function vAuthUnit(Units,divid)
{
  if ( vNum(Units) )
  { sPANum(Units,divid); }
  else { return false; }
  return true;
}
function sPANum(Units,divid)
{ 
  if ( document.PrAuthRVU.PrAuthRVU_PANum_1.defaultValue == "" )
  {
    if ( Units.value == "" )
    { document.PrAuthRVU.PrAuthRVU_PANum_1.value = ''; }
    else
    { document.PrAuthRVU.PrAuthRVU_PANum_1.value = 'PROVAUTH'; }
  }
} 
</SCRIPT>

<FORM NAME="PrAuthRVU" ACTION="/cgi/bin/mis.cgi" METHOD="POST" >
<TABLE CLASS="main fullsize" >
  <TR >
    <TD CLASS="strcol" >
      <<<Client_FName_1>>> <<<Client_MName_1>>> <<<Client_LName_1>>> (<<<Client_ClientID_1>>>) <<<Client_SSN_1>>>
      <BR>Prior Authorization Periods
    </TD>
    <TD CLASS="numcol" >[[gHTML->setLINKS(%form+back)]]</TD>
  </TR>
</TABLE>
<TABLE CLASS="home fullsize" >
  <TR >
    <TD CLASS="strcol" WIDTH="30%" >Service Code</TD>
    <TD CLASS="strcol" >
      <SELECT NAME="PrAuthRVU_SCID_1" >
        [[DBA->selServiceCodes(%form+<<PrAuthRVU_SCID_1>>+0+<<<LOGINPROVID>>>+<<<Client_ClientID_1>>>+AuthRVUs)]] 
      </SELECT> 
    </TD>
  </TR>
  <TR >
    <TD CLASS="strcol" WIDTH="30%" >Requested Units</TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="TEXT" NAME="PrAuthRVU_ReqRVU_1" VALUE="<<PrAuthRVU_ReqRVU_1>>" ONFOCUS="this.select();" SIZE="4" >
    </TD>
  </TR>
  <TR >
    <TD CLASS="strcol" WIDTH="30%" >Authorized Units</TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="TEXT" NAME="PrAuthRVU_AuthRVU_1" VALUE="<<PrAuthRVU_AuthRVU_1>>" ONFOCUS="this.select();" ONCHANGE="return vAuthUnit(this);" SIZE="4" >
    </TD>
  </TR>
  <TR >
    <TD CLASS="strcol" WIDTH="30%" >Authorization Number</TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="TEXT" NAME="PrAuthRVU_PANum_1" VALUE="<<PrAuthRVU_PANum_1>>" ONFOCUS="this.select();" >
    </TD>
  </TR>
  <TR >
    <TD CLASS="strcol" WIDTH="30%" >From/To Date in Prior Auth</TD>
    <TD CLASS="strcol" ><<<PrAuthRVU_EffDate_1>>>/<<<PrAuthRVU_ExpDate_1>>></TD>
  </TR>
</TABLE>
<TABLE CLASS="main fullsize" >
  <TR>
    <TD CLASS="numcol" >
[[myTables->htmLocked(%form+<<<PrAuthRVU_Locked_1>>>+PrAuthRVU)]]
    </TD>
  </TR>
</TABLE>

<INPUT TYPE=hidden NAME="PrevDate" VALUE="<<PrevDate>>" >
<INPUT TYPE=hidden NAME="post_update" VALUE="PostUpd->updPrAuth(%form+<<<ClientPrAuth_ID_1>>>+1)" >
</LOADHIDDEN>
</FORM>
<SCRIPT LANGUAGE="JavaScript">
if ( document.PrAuthRVU.PrevDate.value != '' )
{
  document.PrAuthRVU.PrAuthRVU_EffDate_1.value = document.PrAuthRVU.PrevDate.value;
  document.PrAuthRVU.PrAuthRVU_ExpDate_1.value = mDate(document.PrAuthRVU.PrAuthRVU_EffDate_1,6,-1);
}
document.PrAuthRVU.elements[0].focus();
</SCRIPT>

[[myHTML->rightpane(%form+search)]]
