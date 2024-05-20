[[myHTML->newPage(%form+Problems and Goals)]]

<SCRIPT LANGUAGE="JavaScript" SRC="/cgi/js/vEntry.js"> </SCRIPT>
<SCRIPT LANGUAGE="JavaScript" SRC="/cgi/js/vxPG.js"> </SCRIPT>
<SCRIPT LANGUAGE="JavaScript" SRC="/cgi/js/vNum.js"> </SCRIPT>

[[*SysAccess->verify(%form+Privilege=AdminTables)]]

<FORM NAME="xPG" ACTION="/cgi/bin/mis.cgi" METHOD="POST" >
<TABLE CLASS="main fullsize" >
  <TR >
    <TD CLASS="strcol" >
      Need/Skill: <<<xNS_Descr_1>>>
      <BR>Problem and Goal
    </TD>
    <TD CLASS="numcol" >[[gHTML->setLINKS(%form+back)]]</TD>
  </TR>
</TABLE>
<TABLE CLASS="home fullsize" >
  <TR>
    <TD CLASS="strcol" WIDTH="30%" >Number</TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="TEXT" NAME="xPG_Num_1" VALUE="<<xPG_Num_1>>" ONCHANGE="return vNum(this,1,200)" SIZE="4" >
    </TD>
  </TR>
  <TR>
    <TD CLASS="strcol" WIDTH="30%" >Problem</TD>
    <TD CLASS="strcol" >
      <TEXTAREA NAME="xPG_Problem_1" COLS="70" ROWS="5" WRAP="virtual" ><<xPG_Problem_1>></TEXTAREA>
    </TD>
  </TR>
  <TR>
    <TD CLASS="strcol" WIDTH="30%" >Goal</TD>
    <TD CLASS="strcol" >
      <TEXTAREA NAME="xPG_Goal_1" COLS="70" ROWS="5" WRAP="virtual" ><<xPG_Goal_1>></TEXTAREA>
    </TD>
  </TR>
  <TR>
    <TD CLASS="strcol" WIDTH="30%" >Active</TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="radio" NAME="xPG_Active_1" VALUE=1 <<xPG_Active_1=1>> > yes
      <INPUT TYPE="radio" NAME="xPG_Active_1" VALUE=0 <<xPG_Active_1=0>> > no
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
<SPAN ID="ListxOBJ" >
[[myHTML->ListSel(%form+ListxOBJ+<<<xPG_ID>>>+<<<LINKID>>>)]]
</SPAN>

</LOADHIDDEN>
</FORM>
<SCRIPT LANGUAGE="JavaScript">
document.xPG.elements[0].focus();
</SCRIPT>
[[myHTML->rightpane(%form+search)]]
