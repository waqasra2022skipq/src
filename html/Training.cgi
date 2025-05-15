[[myHTML->newPage(%form+Training)]]

<SCRIPT LANGUAGE="JavaScript" SRC="/src/cgi/js/NoEnter.js"> </SCRIPT>
<SCRIPT LANGUAGE="JavaScript" SRC="/src/cgi/js/vEntry.js"> </SCRIPT>
<SCRIPT LANGUAGE="JavaScript" SRC="/src/cgi/js/vTraining.js"> </SCRIPT>
<SCRIPT LANGUAGE="JavaScript" SRC="/src/cgi/js/vDate.js"> </SCRIPT>

<FORM NAME="Training" ACTION="/cgi/bin/mis.cgi" METHOD="POST" >
<TABLE CLASS="main fullsize" >
  <TR >
    <TD CLASS="strcol" >
      <<<Provider_FName_1>>> <<<Provider_MName_1>>> <<<Provider_LName_1>>> 
      <BR>Edit/View Training
    </TD>
    <TD CLASS="numcol" >[[gHTML->setLINKS(%form+back)]]</TD>
  </TR>
</TABLE>
<TABLE CLASS="home fullsize" >
  <TR >
    <TD CLASS="strcol" WIDTH="20%" >Description</TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="TEXT" NAME="Training_Descr_1" VALUE="<<Training_Descr_1>>" SIZE=80 > 
    </TD>
  </TR>
  <TR >
    <TD CLASS="strcol" WIDTH="20%" >Date</TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="TEXT" NAME="Training_Date_1" VALUE="<<Training_Date_1>>" ONFOCUS="select()" ONCHANGE="return vDate(this)" SIZE=10 > 
    </TD>
  </TR>
</TABLE>
<TABLE CLASS="main fullsize" >
  <TR>
    <TD CLASS="numcol" >
      <INPUT TYPE="submit" ONCLICK="return vDELETE('Are you sure you want to delete this record?');" NAME="Training_DELETE_1=1&UpdateTables=all&misPOP=1" VALUE="Delete">
      <INPUT TYPE="submit" ONCLICK="return validate(this.form);" NAME="UpdateTables=all&misPOP=1" VALUE="Add/Update">
    </TD>
  </TR>
</TABLE>

</LOADHIDDEN>
</FORM>
<SCRIPT LANGUAGE="JavaScript">
document.Training.elements[0].focus();
</SCRIPT>

[[myHTML->rightpane(%form+search)]]
