[[myHTML->newPage(%form+Projects)]]

<SCRIPT LANGUAGE="JavaScript" SRC="/cgi/js/vEntry.js"> </SCRIPT>
<SCRIPT LANGUAGE="JavaScript" SRC="/cgi/js/vProjects.js"> </SCRIPT>
<SCRIPT LANGUAGE="JavaScript" SRC="/cgi/js/vDate.js"> </SCRIPT>

<FORM NAME="Projects" ACTION="/cgi/bin/mis.cgi" METHOD="POST" >
<TABLE CLASS="main fullsize" >
  <TR >
    <TD CLASS="header" >
      Projects
    </TD>
    <TD CLASS="numcol" >[[gHTML->setLINKS(%form+back)]]</TD>
  </TR>
</TABLE>
<TABLE CLASS="home fullsize" >
    <TR ><TD CLASS="port hdrtxt" ><TABLE CLASS="home fullsize" >
  <TR>
    <TD CLASS="strcol" WIDTH="15%" >Priority</TD>
    <TD CLASS="strcol" >
      <SELECT NAME="Projects_Priority_1">[[DBA->selxTable(%form+xProjectPriority+<<Projects_Priority_1>>)]]</SELECT> 
    </TD>
  </TR>
  <TR>
    <TD CLASS="strcol" WIDTH="15%" >Type</TD>
    <TD CLASS="strcol" >
      <SELECT NAME="Projects_Type_1">[[DBA->selxTable(%form+xProjectType+<<Projects_Type_1>>)]]</SELECT> 
    </TD>
  </TR>
  <TR>
    <TD CLASS="strcol" WIDTH="15%" >Subject</TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="text" NAME="Projects_Subject_1" VALUE="<<Projects_Subject_1>>" ONFOCUS="select()" SIZE="60" >
    </TD>
  </TR>
  <TR>
    <TD CLASS="strcol" WIDTH="15%" >Requested By</TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="text" NAME="Projects_ReqBy_1" VALUE="<<Projects_ReqBy_1>>" ONFOCUS="select()" SIZE="60" >
    </TD>
  </TR>
  <TR>
    <TD CLASS="strcol" WIDTH="15%" >Details</TD>
    <TD CLASS="strcol" >
      <TEXTAREA NAME="Projects_Details_1" COLS="80" ROWS="22" WRAP="virtual" onFocus="select()" ><<Projects_Details_1>></TEXTAREA>
    </TD>
  </TR>
  <TR >
    <TD CLASS="strcol" WIDTH="15%" >Effective Date</TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="TEXT" NAME="Projects_EffDate_1" VALUE="<<Projects_EffDate_1>>" ONFOCUS="select()" ONCHANGE="return vDate(this);" SIZE="12" > 
    </TD>
  </TR>
  <TR >
    <TD CLASS="strcol" WIDTH="15%" >Done Date</TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="TEXT" NAME="Projects_ExpDate_1" VALUE="<<Projects_ExpDate_1>>" ONFOCUS="select()" ONCHANGE="return vDate(this);" SIZE="12" > 
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
document.Projects.elements[0].focus();
</SCRIPT>
[[myHTML->rightpane(%form+search)]]
