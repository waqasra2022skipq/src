[[myHTML->newPage(%form+MIS database Tables Duplicate)]]

<SCRIPT LANGUAGE="JavaScript" SRC="/cgi/js/vEntry.js"> </SCRIPT>
<SCRIPT LANGUAGE="JavaScript" SRC="/cgi/js/vxTableDup.js"> </SCRIPT>

[[*SysAccess->verify(%form+Privilege=AdminTables)]]

<FORM NAME="xTables" ACTION="/cgi/bin/mis.cgi" METHOD="POST" >
<TABLE CLASS="main fullsize" >
  <TR >
    <TD CLASS="strcol" >
      MIS database Duplicate Table 
    </TD>
    <TD CLASS="numcol" >[[gHTML->setLINKS(%form+back)]]</TD>
  </TR>
</TABLE>
<TABLE CLASS="home fullsize" >
  <TR>
    <TD CLASS="port hdrcol" WIDTH="30%" >Duplicate <<<xTables_theTable_1>>></TD>
    <TD CLASS="strcol" >&nbsp;</TD>
  </TR>
  <TR>
    <TD CLASS="strcol" WIDTH="30%" >New Table Name</TD>
    <TD CLASS="strcol" >
       <INPUT TYPE="text" NAME="NewTable" VALUE="" ONFOCUS="select()" SIZE="24" MAXSIZE="24" >
    </TD>
  </TR>
  <TR>
    <TD CLASS="strcol" WIDTH="30%" >New Table Description</TD>
    <TD CLASS="strcol" >
       <INPUT TYPE="text" NAME="NewDescription" VALUE="" ONFOCUS="select()" SIZE="60" >
    </TD>
  </TR>
</TABLE>
<TABLE CLASS="main fullsize" >
  <TR >
    <TD CLASS="numcol" >
      <INPUT TYPE=submit ONCLICK="return validate(this.form);" NAME="misPOP=1" VALUE="Duplicate">
    </TD>
  </TR>
</TABLE>

<INPUT TYPE="hidden" NAME="OrgTableID" VALUE="<<xTables_ID_1>>" >
<INPUT TYPE="hidden" NAME="post_update" VALUE="PostUpd->dupxTable(%form)" >
</LOADHIDDEN>
</FORM>
<SCRIPT LANGUAGE="JavaScript">
document.xTables.elements[0].focus();
</SCRIPT>
[[myHTML->rightpane(%form+search)]]
