[[myHTML->newPage(%form+Timesheet Entry)]]

<SCRIPT LANGUAGE="JavaScript" SRC="/src/cgi/js/NoEnter.js"> </SCRIPT>
<SCRIPT LANGUAGE="JavaScript" SRC="/src/cgi/js/vEntry.js"> </SCRIPT>
<SCRIPT LANGUAGE="JavaScript" SRC="/src/cgi/js/vProviderTimesheet.js"> </SCRIPT>
<SCRIPT LANGUAGE="JavaScript" SRC="/src/cgi/js/vNum.js"> </SCRIPT>

[[*SysAccess->verify(%form+Privilege=ProviderPay)]]

<FORM NAME="ProviderPay" ACTION="/cgi/bin/mis.cgi" METHOD="POST" >
<TABLE CLASS="main fullsize" >
  <TR >
    <TD CLASS="strcol" >
      <<<Provider_FName_1>>> <<<Provider_MName_1>>> <<<Provider_LName_1>>> 
      <BR>Provider's Clock in/out entry
    </TD>
    <TD CLASS="numcol" >[[gHTML->setLINKS(%form+back)]]</TD>
  </TR>
</TABLE>
<TABLE CLASS="home fullsize" >
  <TR >
    <TD CLASS="strcol" WIDTH="30%" >Clock In DateTime</TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="TEXT" NAME="Timesheet_LoginTime_1" VALUE="<<Timesheet_LoginTime_1>>" ONFOCUS="select()" ONCHANGE="return vNum(this,20040101,20100101000000);" SIZE=20 >
    </TD>
  </TR>
  <TR >
    <TD CLASS="strcol" WIDTH="30%" >Clock Out DateTime</TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="TEXT" NAME="Timesheet_LogoutTime_1" VALUE="<<Timesheet_LogoutTime_1>>" ONFOCUS="select()" ONCHANGE="return vNum(this,20040101,20100101000000);" SIZE=20 >
    </TD>
  </TR>
</TABLE>
<TABLE CLASS="main fullsize" >
  <TR>
    <TD CLASS="numcol" >
      <INPUT TYPE="submit" ONCLICK="return vDELETE('Are you sure you want to delete this entry?');" NAME="Timesheet_DELETE_1=1&UpdateTables=all&misPOP=1" VALUE="Delete">
      <INPUT TYPE="submit" ONCLICK="return validate(this.form);" NAME="UpdateTables=all&misPOP=1" VALUE="Add/Update">
    </TD>
  </TR>
</TABLE>

</LOADHIDDEN>
</FORM>
<SCRIPT LANGUAGE="JavaScript">
document.ProviderPay.elements[0].focus();
</SCRIPT>

[[myHTML->rightpane(%form+search)]]
