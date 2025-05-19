[[myHTML->newPage(%form+Client Discharge Summary Page)]]

<SCRIPT LANGUAGE="JavaScript" SRC="/src/cgi/js/NoEnter.js"> </SCRIPT>
<SCRIPT LANGUAGE="JavaScript" SRC="/src/cgi/js/vEntry.js"> </SCRIPT>
<SCRIPT type="text/javascript" src="/src/cgi/js/ajaxrequest.js"></SCRIPT>
<SCRIPT LANGUAGE="JavaScript" SRC="/src/cgi/js/vClientDischarge.js"> </SCRIPT>
<SCRIPT LANGUAGE="JavaScript" SRC="/src/cgi/js/vDate.js"> </SCRIPT>
<SCRIPT LANGUAGE="JavaScript" SRC="/src/cgi/js/vTime.js"> </SCRIPT>
<SCRIPT LANGUAGE="JavaScript" SRC="/src/cgi/js/vNum.js"> </SCRIPT>

[[*SysAccess->verify(%form+Privilege=Discharge)]]

<FORM NAME="ClientDischarge" ACTION="/src/cgi/bin/mis.cgi" METHOD="POST" >
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
    <TD CLASS="port strcol" >Follow-up Date</TD>
    <TD CLASS="strcol" COLSPAN="2" >
      <INPUT TYPE=text NAME="ClientDischarge_FollowUpDate_1" VALUE="<<ClientDischarge_FollowUpDate_1>>" ONFOCUS="select()" ONCHANGE="return vDate(this)" SIZE="10" >
    </TD>
  </TR>
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
<TABLE CLASS="main fullsize" >
  <TR >
    <TD CLASS="numcol" >
[[SysAccess->verify(%form+Privilege=Discharge)      <INPUT TYPE="submit" ONCLICK="return validate(this.form)" NAME="UpdateTables=all&misPOP=1" VALUE="Add/Update"> ]]
    </TD>
  </TR>
</TABLE>

</LOADHIDDEN>
</FORM>
<SCRIPT LANGUAGE="JavaScript">
document.ClientDischarge.elements[0].focus();
// just to OPENTABLES...
//<<<ClientDischargeCDC_ClientID_1>>>
callAjax('Physicians','<<ClientDischarge_PhysNPI_1>>','selPhysNPI','&name=ClientDischarge_PhysNPI_1','popup.pl');
</SCRIPT>

[[myHTML->rightpane(%form+search)]]
