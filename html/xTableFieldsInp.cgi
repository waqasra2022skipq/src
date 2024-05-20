[[myHTML->newPage(%form+MIS database Tables Input generator)]]

<SCRIPT LANGUAGE="JavaScript" SRC="/cgi/js/vEntry.js"> </SCRIPT>
<SCRIPT LANGUAGE="JavaScript" SRC="/cgi/js/vxTableFields.js"> </SCRIPT>

[[*SysAccess->verify(%form+Privilege=AdminTables)]]

<FORM NAME="xTableFields" ACTION="/cgi/bin/mis.cgi" METHOD="POST" >
<TABLE CLASS="main fullsize" >
  <TR >
    <TD CLASS="strcol" >
      MIS database Tables Input generator
    </TD>
    <TD CLASS="numcol" >[[gHTML->setLINKS(%form+back)]]</TD>
  </TR>
</TABLE>
<TABLE CLASS="home fullsize" >
  <TR>
    <TD CLASS="strcol" WIDTH="30%" >Field Name</TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="text" NAME="xTableFields_theField_1" VALUE="<<xTableFields_theField_1>>" ONFOCUS="select()" SIZE="24" MAXSIZE="24" >
    </TD>
  </TR>
  <TR>
    <TD CLASS="strcol" WIDTH="30%" >Sequence</TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="text" NAME="xTableFields_theSeq_1" VALUE="<<xTableFields_theSeq_1>>" ONFOCUS="select()" SIZE="12" MAXSIZE="12" >
    </TD>
  </TR>
  <TR>
    <TD CLASS="strcol" WIDTH="30%" >agent</TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="radio" NAME="xTableFields_agent_1" VALUE="1" <<xTableFields_agent_1=1>> > yes
      <INPUT TYPE="radio" NAME="xTableFields_agent_1" VALUE="0" <<xTableFields_agent_1=0>> > no
    </TD>
  </TR>
  <TR>
    <TD CLASS="strcol" WIDTH="30%" >Type</TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="text" NAME="xTableFields_theType_1" VALUE="<<xTableFields_theType_1>>" ONFOCUS="select()" SIZE="12" MAXSIZE="12" >
    </TD>
  </TR>
  <TR>
    <TD CLASS="strcol" WIDTH="30%" >text</TD>
    <TD CLASS="strcol" >
       <TEXTAREA NAME="xTableFields_theText_1" COLS="90" ROWS="3" WRAP="virtual" ><<xTableFields_theText_1>></TEXTAREA>
    </TD>
  </TR>
  <TR>
    <TD CLASS="strcol" WIDTH="30%" >pre text</TD>
    <TD CLASS="strcol" >
       <TEXTAREA NAME="xTableFields_thePreText_1" COLS="90" ROWS="3" WRAP="virtual" ><<xTableFields_thePreText_1>></TEXTAREA>
    </TD>
  </TR>
  <TR>
    <TD CLASS="strcol" WIDTH="30%" >textpost</TD>
    <TD CLASS="strcol" >
       <TEXTAREA NAME="xTableFields_thePostText_1" COLS="90" ROWS="3" WRAP="virtual" ><<xTableFields_thePostText_1>></TEXTAREA>
    </TD>
  </TR>
  <TR>
    <TD CLASS="strcol" WIDTH="30%" >theValues</TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="text" NAME="xTableFields_theValues_1" VALUE="<<xTableFields_theValues_1>>" ONFOCUS="select()" SIZE="60" MAXSIZE="60" >
    </TD>
  </TR>
  <TR>
    <TD CLASS="strcol" WIDTH="30%" >descriptors</TD>
    <TD CLASS="strcol" >
       <TEXTAREA NAME="xTableFields_descriptors_1" COLS="90" ROWS="3" WRAP="virtual" ><<xTableFields_descriptors_1>></TEXTAREA>
    </TD>
  </TR>
  <TR>
    <TD CLASS="strcol" WIDTH="30%" >onchange</TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="text" NAME="xTableFields_onchange_1" VALUE="<<xTableFields_onchange_1>>" ONFOCUS="select()" SIZE="60" MAXSIZE="60" >
    </TD>
  </TR>
  <TR>
    <TD CLASS="strcol" WIDTH="30%" >colspan</TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="text" NAME="xTableFields_colspan_1" VALUE="<<xTableFields_colspan_1>>" ONFOCUS="select()" SIZE="60" MAXSIZE="60" >
    </TD>
  </TR>
  <TR>
    <TD CLASS="strcol" WIDTH="30%" >Size</TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="text" NAME="xTableFields_theSize_1" VALUE="<<xTableFields_theSize_1>>" ONFOCUS="select()" SIZE="60" MAXSIZE="60" >
    </TD>
  </TR>
  <TR>
    <TD CLASS="strcol" WIDTH="30%" >Style</TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="text" NAME="xTableFields_theStyle_1" VALUE="<<xTableFields_theStyle_1>>" ONFOCUS="select()" SIZE="60" MAXSIZE="60" >
    </TD>
  </TR>
  <TR>
    <TD CLASS="strcol" WIDTH="30%" >additional arguments</TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="text" NAME="xTableFields_theArgs_1" VALUE="<<xTableFields_theArgs_1>>" ONFOCUS="select()" SIZE="60" MAXSIZE="60" >
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
document.xTableFields.elements[0].focus();
</SCRIPT>
[[myHTML->rightpane(%form+search)]]
