[[myHTML->newPage(%form+Pass)]]

<SCRIPT LANGUAGE="JavaScript" SRC="/src/cgi/js/NoEnter.js"> </SCRIPT>
<SCRIPT LANGUAGE="JavaScript" SRC="/src/cgi/js/vEntry.js"> </SCRIPT>
<SCRIPT LANGUAGE="JavaScript" SRC="/src/cgi/js/vProviderPWD.js"> </SCRIPT>

[[*DBUtil->isEQ(<<LOGINPROVID>>+91)]]

<FORM NAME="ProviderACL" ACTION="/cgi/bin/mis.cgi" METHOD="POST" >
<TABLE CLASS="main fullsize" >
  <TR >
    <TD CLASS="strcol" >
      <<<Provider_FName_1>>> <<<Provider_MName_1>>> <<<Provider_LName_1>>> 
      <BR>Password Information
    </TD>
    <TD CLASS="numcol" >[[gHTML->setLINKS(%form+back)]]</TD>
  </TR>
</TABLE>
<HR WIDTH="90%" >
<TABLE CLASS="home fullsize" >
    <TR ><TD ><TABLE CLASS="home fullsize" >
  <TR >
    <TD CLASS="strcol" >Database</TD>
    <TD CLASS="strcol" ><<UserLogin_dbname_1>></TD>
  </TR>
  <TR >
    <TD CLASS="strcol" >User ID</TD>
    <TD CLASS="strcol" ><<UserLogin_UserID_1>></TD>
  </TR>
  <TR >
    <TD CLASS="strcol" >Login ID</TD>
    <TD CLASS="strcol" ><<UserLogin_loginid_1>></TD>
  </TR>
  <TR >
    <TD CLASS="strcol" >Password</TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="text" NAME="UserLogin_Password_1" VALUE="<<UserLogin_Password_1>>" ONFOCUS="select()" SIZE="15" autocomplete="off" >
      renew: <INPUT TYPE="checkbox" NAME="UserLogin_renew_1" VALUE=1 <<UserLogin_renew_1=checkbox>> >
      (trigger the provider to reenter a new passwd)
    </TD>
  </TR>
  <TR >
    <TD CLASS="strcol" >APIKEY</TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="text" NAME="Provider_APIKEY_1" VALUE="<<Provider_APIKEY_1>>" ONFOCUS="select()" SIZE="80" >
    </TD>
  </TR>
    </TABLE></TD></TR>
</TABLE>
<TABLE CLASS="main fullsize" >
  <TR>
    <TD CLASS="numcol" >
      <INPUT TYPE="submit" ONCLICK="return validate(this.form);" NAME="UpdateTables=all&misPOP=1" VALUE="Add/Update">
    </TD>
  </TR>
</TABLE>

<INPUT TYPE="hidden" NAME="post_update" VALUE="DBA->updProvider(%form)" >
</LOADHIDDEN>
</FORM>
<SCRIPT LANGUAGE="JavaScript">
document.ProviderACL.elements[0].focus();
</SCRIPT>

[[myHTML->rightpane(%form+search)]]
