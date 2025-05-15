[[myHTML->newPage(%form+Client CDSrules)]]

<SCRIPT LANGUAGE="JavaScript" SRC="/src/cgi/js/vEntry.js"> </SCRIPT>
<SCRIPT LANGUAGE="JavaScript" SRC="/src/cgi/js/vCDSrules.js"> </SCRIPT>

<FORM NAME="CDSrules" ACTION="/cgi/bin/mis.cgi" METHOD="POST" >
<TABLE CLASS="main fullsize" >
  <TR >
    <TD CLASS="strcol" >
      <<<Provider_ScreenName_1>>>
      <BR>
      Clinical Decision Support Rules
    </TD>
    <TD CLASS="numcol" >[[gHTML->setLINKS(%form+back)]]</TD>
  </TR>
</TABLE>
<TABLE CLASS="home fullsize" >
  <TR ><TD CLASS="port hdrtxt" COLSPAN="2" >CDS Rule Information</TD></TR>
  <TR >
    <TD CLASS="strcol" >RuleID</TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="text" NAME="CDSrules_RuleID_1" VALUE="<<CDSrules_RuleID_1>>" ONFOCUS="select()" SIZE="100" >
    </TD>
  </TR>
  <TR >
    <TD CLASS="strcol" >Name</TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="text" NAME="CDSrules_Name_1" VALUE="<<CDSrules_Name_1>>" ONFOCUS="select()" SIZE="100" >
    </TD>
  </TR>
  <TR >
    <TD CLASS="strcol" >CommandText</TD>
    <TD CLASS="strcol" >
      <TEXTAREA NAME="CDSrules_CommandText_1" COLS="100" ROWS="5" WRAP="virtual" ><<CDSrules_CommandText_1>></TEXTAREA>
    </TD>
  </TR>
  <TR >
    <TD CLASS="strcol" >AlertMessage</TD>
    <TD CLASS="strcol" >
      <TEXTAREA NAME="CDSrules_AlertMessage_1" COLS="100" ROWS="5" WRAP="virtual" ><<CDSrules_AlertMessage_1>></TEXTAREA>
    </TD>
  </TR>
  <TR >
    <TD CLASS="strcol" >ReferenceLink</TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="text" NAME="CDSrules_ReferenceLink_1" VALUE="<<CDSrules_ReferenceLink_1>>" ONFOCUS="select()" SIZE="160" >
    </TD>
  </TR>
  <TR >
    <TD CLASS="strcol" >InfoLink</TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="text" NAME="CDSrules_InfoLink_1" VALUE="<<CDSrules_InfoLink_1>>" ONFOCUS="select()" SIZE="160" >
    </TD>
  </TR>
  <TR >
    <TD CLASS="strcol" >Funding</TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="text" NAME="CDSrules_Funding_1" VALUE="<<CDSrules_Funding_1>>" ONFOCUS="select()" SIZE="100" >
    </TD>
  </TR>
  <TR >
    <TD CLASS="strcol" >Author</TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="text" NAME="CDSrules_Author_1" VALUE="<<CDSrules_Author_1>>" ONFOCUS="select()" SIZE="100" >
    </TD>
  </TR>
  <TR >
    <TD CLASS="strcol" >Release Date</TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="text" NAME="CDSrules_ReleaseDate_1" VALUE="<<CDSrules_ReleaseDate_1>>" ONFOCUS="select()" SIZE="12" >
    </TD>
  </TR>
  <TR >
    <TD CLASS="strcol" >IsEnabled</TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="radio" NAME="CDSrules_IsEnabled_1" VALUE="1" <<CDSrules_IsEnabled_1=1>> > Yes
      <INPUT TYPE="radio" NAME="CDSrules_IsEnabled_1" VALUE="0" <<CDSrules_IsEnabled_1=0>> > No
    </TD>
  </TR>
  <TR >
    <TD CLASS="strcol" >Biblio</TD>
    <TD CLASS="strcol" >
      <TEXTAREA NAME="CDSrules_Biblio_1" COLS="100" ROWS="5" WRAP="virtual" ><<CDSrules_Biblio_1>></TEXTAREA>
    </TD>
  </TR>
  <TR >
    <TD CLASS="strcol" >RowVersion</TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="text" NAME="CDSrules_RowVersion_1" VALUE="<<CDSrules_RowVersion_1>>" ONFOCUS="select()" SIZE="100" >
    </TD>
  </TR>
  <TR >
    <TD CLASS="strcol" >RuleID2</TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="text" NAME="CDSrules_RuleID2_1" VALUE="<<CDSrules_RuleID2_1>>" ONFOCUS="select()" SIZE="100" >
    </TD>
  </TR>
</TABLE>

<TABLE CLASS="main fullsize" >
  <TR >
    <TD CLASS="numcol" >
      <INPUT TYPE="submit" ONCLICK="return vDELETE('Are you sure you want to delete this record?');" NAME="CDSrules_DELETE_1=1&UpdateTables=all&misPOP=1" VALUE="Delete">
      <INPUT TYPE="submit" ONCLICK="return validate(this.form);" NAME="UpdateTables=all&misPOP=1" VALUE="Add/Update">
    </TD>
  </TR>
</TABLE>

</LOADHIDDEN>
</FORM>
<SCRIPT LANGUAGE="JavaScript">
document.CDSrules.elements[0].focus();
</SCRIPT>

[[myHTML->rightpane(%form+search)]]
