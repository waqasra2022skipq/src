[[myHTML->newPage(%form+Agency Control)]]

<SCRIPT LANGUAGE="JavaScript" SRC="/src/cgi/js/NoEnter.js"> </SCRIPT>
<SCRIPT LANGUAGE="JavaScript" SRC="/src/cgi/js/vEntry.js"> </SCRIPT>
<SCRIPT LANGUAGE="JavaScript" SRC="/src/cgi/js/vAgencyControl.js"> </SCRIPT>
<SCRIPT LANGUAGE="JavaScript" SRC="/src/cgi/js/vDate.js"> </SCRIPT>

[[*SysAccess->verify(%form+Privilege=Agent)]]

<FORM NAME="AgencyControl" ACTION="/cgi/bin/mis.cgi" METHOD="POST" >
<TABLE CLASS="main fullsize" >
  <TR >
    <TD CLASS="strcol" >
      <<<Provider_FName_1>>> <<<Provider_MName_1>>> <<<Provider_LName_1>>> 
      (<<<Provider_ProvID_1>>>)
      <BR>Provider Control
    </TD>
    <TD CLASS="numcol" >[[gHTML->setLINKS(%form+back)]]</TD>
  </TR>
</TABLE>
<HR WIDTH="90%" >
<TABLE CLASS="home fullsize" >
  <TR > <TD CLASS="port hdrtxt" COLSPAN="3" ><B>Agency URL Information</B></TD> </TR>
  <TR >
    <TD CLASS="strcol" WIDTH="30%" >Login Screen</TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="text" NAME="ProviderControl_LoginScreen_1" VALUE="<<ProviderControl_LoginScreen_1>>" ONFOCUS="select()" SIZE="50" >
    </TD>
  </TR>
  <TR >
    <TD CLASS="strcol" WIDTH="30%" >Agency Server url</TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="text" NAME="ProviderControl_Server_1" VALUE="<<ProviderControl_Server_1>>" ONFOCUS="select()" SIZE="50" >
    </TD>
  </TR>
  <TR >
    <TD CLASS="strcol" WIDTH="30%" >Agency Header</TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="text" NAME="ProviderControl_Header_1" VALUE="<<ProviderControl_Header_1>>" ONFOCUS="select()" SIZE="50" >
    </TD>
  </TR>
  <TR >
    <TD CLASS="strcol" WIDTH="30%" >Agency Footer</TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="text" NAME="ProviderControl_Footer_1" VALUE="<<ProviderControl_Footer_1>>" ONFOCUS="select()" SIZE="50" >
    </TD>
  </TR>
  <TR>
    <TD CLASS="strcol" WIDTH="30%" >Agency Tag ID</TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="text" NAME="ProviderControl_AgencyTag_1" VALUE="<<ProviderControl_AgencyTag_1>>" ONFOCUS="select()" SIZE="10" >
    </TD>
  </TR>
  <TR>
    <TD CLASS="strcol" WIDTH="30%" >Scheduler url</TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="text" NAME="ProviderControl_Scheduler_1" VALUE="<<ProviderControl_Scheduler_1>>" ONFOCUS="select()" SIZE="50" >
    </TD>
  </TR>
  <TR>
    <TD CLASS="strcol" WIDTH="30%" >ShiftExec url</TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="text" NAME="ProviderControl_ShiftExec_1" VALUE="<<ProviderControl_ShiftExec_1>>" ONFOCUS="select()" SIZE="50" >
    </TD>
  </TR>
  <TR>
    <TD CLASS="strcol" WIDTH="30%" >Passwords</TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="text" NAME="ProviderControl_Passwords_1" VALUE="<<ProviderControl_Passwords_1>>" ONFOCUS="select()" SIZE="120" >
    </TD>
  </TR>
</TABLE>
<TABLE CLASS="main fullsize" >
  <TR>
    <TD CLASS="numcol" >
      <INPUT TYPE="submit" ONCLICK="return validate(this.form);" NAME="UpdateTables=all&misPOP=1" VALUE="Add/Update">
    </TD>
  </TR>
</TABLE>

<INPUT TYPE=hidden NAME="post_update" VALUE="DBA->updProvider(%form)" >
</LOADHIDDEN>
</FORM>
<SCRIPT LANGUAGE="JavaScript">
document.AgencyControl.elements[0].focus();
</SCRIPT>

[[myHTML->rightpane(%form+search)]]
