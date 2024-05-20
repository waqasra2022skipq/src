[[myHTML->newPage(%form+Objective)]]

<SCRIPT LANGUAGE="JavaScript" SRC="/cgi/js/vEntry.js"> </SCRIPT>
<SCRIPT LANGUAGE="JavaScript" SRC="/cgi/js/vxOBJ.js"> </SCRIPT>
<SCRIPT LANGUAGE="JavaScript" SRC="/cgi/js/vNum.js"> </SCRIPT>

[[*SysAccess->verify(%form+Privilege=AdminTables)]]

<FORM NAME="xOBJ" ACTION="/cgi/bin/mis.cgi" METHOD="POST" >
<TABLE CLASS="main fullsize" >
  <TR >
    <TD CLASS="strcol" >
      Problem: <<<xPG_Num_1>>> <<<xPG_Problem_1>>>
      <BR>Objectives
    </TD>
    <TD CLASS="numcol" >[[gHTML->setLINKS(%form+back)]]</TD>
  </TR>
</TABLE>
<TABLE CLASS="home fullsize" >
  <TR>
    <TD CLASS="strcol" WIDTH="30%" >Number</TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="TEXT" NAME="xOBJ_Num_1" VALUE="<<xOBJ_Num_1>>" ONCHANGE="return vNum(this,1,200)" SIZE="4" >
    </TD>
  </TR>
  <TR>
    <TD CLASS="strcol" WIDTH="30%" >Description</TD>
    <TD CLASS="strcol" >
      <TEXTAREA NAME="xOBJ_Descr_1" COLS="70" ROWS="5" WRAP="virtual" ><<xOBJ_Descr_1>></TEXTAREA>
    </TD>
  </TR>
  <TR>
    <TD CLASS="strcol" WIDTH="30%" >Active</TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="radio" NAME="xOBJ_Active_1" VALUE=1 <<xOBJ_Active_1=1>> > yes
      <INPUT TYPE="radio" NAME="xOBJ_Active_1" VALUE=0 <<xOBJ_Active_1=0>> > no
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

</LOADHIDDEN>
</FORM>
<SCRIPT LANGUAGE="JavaScript">
document.xOBJ.elements[0].focus();
</SCRIPT>
[[myHTML->rightpane(%form+search)]]
