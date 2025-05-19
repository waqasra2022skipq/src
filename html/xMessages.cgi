[[myHTML->newPage(%form+Site Messages)]]

<SCRIPT LANGUAGE="JavaScript" SRC="/src/cgi/js/vEntry.js"> </SCRIPT>
<SCRIPT LANGUAGE="JavaScript" SRC="/src/cgi/js/vxMessages.js"> </SCRIPT>
<SCRIPT LANGUAGE="JavaScript" SRC="/src/cgi/js/vDate.js"> </SCRIPT>

<FORM NAME="xMessages" ACTION="/src/cgi/bin/mis.cgi" METHOD="POST" >
<TABLE CLASS="main fullsize" >
  <TR >
    <TD CLASS="strcol" >
      <<<Provider_FName_1>>> <<<Provider_MName_1>>> <<<Provider_LName_1>>> 
      Site Message Information
    </TD>
    <TD CLASS="numcol" >[[gHTML->setLINKS(%form+back)]]</TD>
  </TR>
</TABLE>
<TABLE CLASS="home fullsize" >
    <TR ><TD CLASS="port hdrtxt" ><TABLE CLASS="home fullsize" >
  <TR>
    <TD CLASS="strcol" WIDTH=15% >Message</TD>
    <TD CLASS="strcol" >
      <TEXTAREA NAME="xMessages_Message_1" COLS="80" ROWS="22" WRAP="virtual" onFocus="select()" ><<xMessages_Message_1>></TEXTAREA>
    </TD>
  </TR>
  <TR >
    <TD CLASS="strcol" WIDTH=15% >Effective Date</TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="TEXT" NAME="xMessages_EffDate_1" VALUE="<<xMessages_EffDate_1>>" ONFOCUS="select()" ONCHANGE="return vDate(this);" SIZE="12" > 
    </TD>
  </TR>
  <TR >
    <TD CLASS="strcol" WIDTH=15% >Done Date</TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="TEXT" NAME="xMessages_ExpDate_1" VALUE="<<xMessages_ExpDate_1>>" ONFOCUS="select()" ONCHANGE="return vDate(this,1);" SIZE="12" > 
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

</LOADHIDDEN>
</FORM>
<SCRIPT LANGUAGE="JavaScript">
document.xMessages.elements[0].focus();
</SCRIPT>
[[myHTML->rightpane(%form+search)]]
