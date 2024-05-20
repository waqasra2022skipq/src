[[myHTML->newPage(%form+Access Control)]]

<SCRIPT LANGUAGE="JavaScript" SRC="/cgi/js/NoEnter.js"> </SCRIPT>
<SCRIPT LANGUAGE="JavaScript" SRC="/cgi/js/vEntry.js"> </SCRIPT>
<SCRIPT LANGUAGE="JavaScript" SRC="/cgi/js/vProviderACL.js"> </SCRIPT>
<SCRIPT LANGUAGE="JavaScript" SRC="/cgi/js/vDate.js"> </SCRIPT>

[[*SysAccess->verify(%form+Privilege=ProviderACL)]]

<FORM NAME="ProviderACL" ACTION="/cgi/bin/mis.cgi" METHOD="POST" >
<TABLE CLASS="main fullsize" >
  <TR >
    <TD CLASS="strcol" >
      <<<Provider_FName_1>>> <<<Provider_MName_1>>> <<<Provider_LName_1>>> 
      <BR>Access Information
    </TD>
    <TD CLASS="numcol" >[[gHTML->setLINKS(%form+back)]]</TD>
  </TR>
</TABLE>
<TABLE CLASS="home fullsize" >
    <TR ><TD ><TABLE CLASS="home fullsize" >
  <TR>
    <TD CLASS="strcol" WIDTH="30%" >Active</TD>
    <TD CLASS="strcol" >
      <INPUT TYPE=radio NAME="Provider_Active_1" VALUE=1 <<Provider_Active_1=1>> > yes
      <INPUT TYPE=radio NAME="Provider_Active_1" VALUE=0 <<Provider_Active_1=0>> > no
    </TD>
  </TR>
  <TR >
    <TD CLASS="strcol" WIDTH="30%" >Termination Date</TD>
    <TD CLASS="strcol" >
      <INPUT TYPE=text NAME="EmplInfo_TermDate_1" VALUE="<<EmplInfo_TermDate_1>>" ONFOCUS="select()" ONCHANGE="return vDate(this,1)" SIZE="10" >
    </TD>
  </TR>
  <TR ><TD CLASS="port hdrtxt" COLSPAN="3" >Clinic/Manager Information</TD></TR>
  <TR >
    <TD CLASS="strcol" WIDTH="30%" >Manager</TD>
    <TD CLASS="strcol" >
      <SELECT NAME="Manager_ManagerID_1" >[[DBA->selNotManagerOf(%form+<<<Provider_ProvID_1>>>+<<Manager_ManagerID_1>>)]]</SELECT>
    </TD>
  </TR>
  <TR ><TD CLASS="port hdrtxt" COLSPAN="3" >Special Access</TD></TR>
  <TR >
    <TD CLASS="strcol" WIDTH="30%" >Give 
      <<<Provider_Name_1>>> <<<Provider_FName_1>>> <<<Provider_LName_1>>> 
      Additional Access to 
    </TD>
    <TD CLASS="strcol" >
      <SELECT NAME="Provider_ACLID_1" MULTIPLE SIZE="10" >[[DBA->selNotManagerOf(%form+<<<Provider_ProvID_1>>>+<<Provider_ACLID_1>>)]]</SELECT>
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
