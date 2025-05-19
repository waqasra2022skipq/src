[[myHTML->newPage(%form+Needs and Skills)]]

<SCRIPT LANGUAGE="JavaScript" SRC="/src/cgi/js/vEntry.js"> </SCRIPT>
<SCRIPT LANGUAGE="JavaScript" SRC="/src/cgi/js/vxNS.js"> </SCRIPT>

[[*SysAccess->verify(%form+Privilege=AdminTables)]]

<FORM NAME="xNS" ACTION="/src/cgi/bin/mis.cgi" METHOD="POST" >
<TABLE CLASS="main fullsize" >
  <TR >
    <TD CLASS="strcol" >
      Needs/Skills<BR>Problems and Goals Listing
    </TD>
    <TD CLASS="numcol" >[[gHTML->setLINKS(%form+back)]]</TD>
  </TR>
</TABLE>
<TABLE CLASS="home fullsize" >
  <TR>
    <TD CLASS="strcol" WIDTH="30%" >Description</TD>
    <TD CLASS="strcol" >
       <INPUT TYPE="text" NAME="xNS_Descr_1" VALUE="<<xNS_Descr_1>>" ONFOCUS="select()" SIZE=60>
    </TD>
  </TR>
  <TR>
    <TD CLASS="strcol" WIDTH="30%" >Active</TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="radio" NAME="xNS_Active_1" VALUE=1 <<xNS_Active_1=1>> > yes
      <INPUT TYPE="radio" NAME="xNS_Active_1" VALUE=0 <<xNS_Active_1=0>> > no
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
<SPAN ID="ListxPG" >
[[myHTML->ListSel(%form+ListxPG+<<<xNS_ID>>>+<<<LINKID>>>)]]
</SPAN>

</LOADHIDDEN>
</FORM>
<SCRIPT LANGUAGE="JavaScript">
document.xNS.elements[0].focus();
</SCRIPT>
[[myHTML->rightpane(%form+search)]]
