[[myHTML->newPage(%form+MIS database Tables Input generator)]]

<SCRIPT LANGUAGE="JavaScript" SRC="/src/cgi/js/vEntry.js"> </SCRIPT>
<SCRIPT LANGUAGE="JavaScript" SRC="/src/cgi/js/vxTables.js"> </SCRIPT>

[[*SysAccess->verify(%form+Privilege=AdminTables)]]

<FORM NAME="xTables" ACTION="/src/cgi/bin/mis.cgi" METHOD="POST" >
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
    <TD CLASS="strcol" WIDTH="30%" >Table Name</TD>
    <TD CLASS="strcol" >
       <INPUT TYPE="text" NAME="xTables_theTable_1" VALUE="<<xTables_theTable_1>>" ONFOCUS="select()" SIZE="24" MAXSIZE="24" >
    </TD>
  </TR>
  <TR>
    <TD CLASS="strcol" WIDTH="30%" >Description</TD>
    <TD CLASS="strcol" >
       <INPUT TYPE="text" NAME="xTables_Descr_1" VALUE="<<xTables_Descr_1>>" ONFOCUS="select()" SIZE="60" >
    </TD>
  </TR>
  <TR>
    <TD CLASS="strcol" WIDTH="30%" >Active</TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="radio" NAME="xTables_Active_1" VALUE="1" <<xTables_Active_1=1>> > yes
      <INPUT TYPE="radio" NAME="xTables_Active_1" VALUE="0" <<xTables_Active_1=0>> > no
    </TD>
  </TR>
  <TR>
    <TD CLASS="strcol" WIDTH="30%" >New Questions</TD>
    <TD CLASS="strcol" >
      <TEXTAREA NAME="NewQuestions" COLS="70" ROWS="5" WRAP="virtual" ></TEXTAREA>
    </TD>
  </TR>
</TABLE>
<TABLE CLASS="main fullsize" >
  <TR>
    <TD CLASS="numcol" >
      <INPUT TYPE="submit" ONCLICK="return validate(this.form);" NAME="post_update=PostUpd->addxTableQues(%form)&UpdateTables=all&misPOP=1" VALUE="AddNewQuestions">
      <INPUT TYPE="submit" ONCLICK="return validate(this.form);" NAME="post_update=PostUpd->reseqxTable(%form)&UpdateTables=all&misPOP=1" VALUE="Renumber/Add/Update">
      <INPUT TYPE="submit" ONCLICK="return validate(this.form);" NAME="UpdateTables=all&misPOP=1" VALUE="Add/Update">
    </TD>
  </TR>
</TABLE>
<SPAN ID="ListxTableFields" >
[[myHTML->ListSel(%form+ListxTableFields+<<<xTables_ID>>>+<<<LINKID>>>)]]
</SPAN>

</LOADHIDDEN>
</FORM>
<SCRIPT LANGUAGE="JavaScript">
document.xTables.elements[0].focus();
</SCRIPT>
[[myHTML->rightpane(%form+search)]]
