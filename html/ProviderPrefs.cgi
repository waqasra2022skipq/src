[[myHTML->newPage(%form+Preferences)]]

<SCRIPT LANGUAGE="JavaScript" SRC="/src/cgi/js/NoEnter.js"> </SCRIPT>
<SCRIPT LANGUAGE="JavaScript" SRC="/src/cgi/js/vEntry.js"> </SCRIPT>

<FORM NAME="Prefs" ACTION="/cgi/bin/mis.cgi" METHOD="POST" >
<TABLE CLASS="main fullsize" >
  <TR >
    <TD CLASS="strcol" >
      <<<Provider_FName_1>>> <<<Provider_MName_1>>> <<<Provider_LName_1>>> 
      <BR>Preferences
    </TD>
    <TD CLASS="numcol" >[[gHTML->setLINKS(%form+back)]]</TD>
  </TR>
</TABLE>
<TABLE CLASS="home fullsize" >
  <TR >
    <TD CLASS="strcol" WIDTH="30%" >List Clients on Manager Tree</TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="radio" NAME="ProviderPrefs_ListClients_1" VALUE="1" <<ProviderPrefs_ListClients_1=1>> > Yes
      <INPUT TYPE="radio" NAME="ProviderPrefs_ListClients_1" VALUE="0" <<ProviderPrefs_ListClients_1=0>> > No
    </TD>
  </TR>
  <TR >
    <TD CLASS="strcol" WIDTH="30%" >Use Tabs on Manager Tree for Clinics</TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="radio" NAME="ProviderPrefs_TreeTabs_1" VALUE="1" <<ProviderPrefs_TreeTabs_1=1>> > Yes
      <INPUT TYPE="radio" NAME="ProviderPrefs_TreeTabs_1" VALUE="0" <<ProviderPrefs_TreeTabs_1=0>> > No
    </TD>
  </TR>
  [[SysAccess->verify(%form+Privilege=Agent)  <TR >]]
  [[SysAccess->verify(%form+Privilege=Agent)    <TD CLASS="strcol" WIDTH="30%" >Place me on the MIS Emails Listing</TD>]]
  [[SysAccess->verify(%form+Privilege=Agent)    <TD CLASS="strcol" >]]
  [[SysAccess->verify(%form+Privilege=Agent)      <INPUT TYPE="radio" NAME="ProviderPrefs_MISEmails_1" VALUE="1" <<ProviderPrefs_MISEmails_1=1>> > yes]]
  [[SysAccess->verify(%form+Privilege=Agent)      <INPUT TYPE="radio" NAME="ProviderPrefs_MISEmails_1" VALUE="0" <<ProviderPrefs_MISEmails_1=0>> > no]]
  [[SysAccess->verify(%form+Privilege=Agent)    </TD>]]
  [[SysAccess->verify(%form+Privilege=Agent)  </TR>]]
</TABLE>
<TABLE CLASS="main fullsize" >
  <TR>
    <TD CLASS="numcol" >
      <INPUT TYPE="submit" ONCLICK="return validate(this.form);" NAME="UpdateTables=all&misPOP=1" VALUE="Add/Update">
    </TD>
  </TR>
</TABLE>

</LOADHIDDEN>
</FORM>
<SCRIPT LANGUAGE="JavaScript">
document.Prefs.elements[0].focus();
</SCRIPT>

[[myHTML->rightpane(%form+search)]]
