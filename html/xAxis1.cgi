[[myHTML->newPage(%form+Denial Codes Entry)]]

<SCRIPT LANGUAGE="JavaScript" SRC="/src/cgi/js/NoEnter.js"> </SCRIPT>
<SCRIPT LANGUAGE="JavaScript" SRC="/src/cgi/js/vEntry.js"> </SCRIPT>
<SCRIPT LANGUAGE="JavaScript" SRC="/src/cgi/js/vxAxis1.js"> </SCRIPT>
<SCRIPT LANGUAGE="JavaScript" SRC="/src/cgi/js/vDate.js"> </SCRIPT>
<SCRIPT LANGUAGE="JavaScript" SRC="/src/cgi/js/vNum.js"> </SCRIPT>

<FORM NAME="Axis1" ACTION="/cgi/bin/mis.cgi" METHOD="POST" >
<TABLE CLASS="main fullsize" >
  <TR >
    <TD CLASS="strcol" >Denial Code View/Edit</TD>
    <TD CLASS="numcol" >[[gHTML->setLINKS(%form+back)]]</TD>
  </TR>
</TABLE>
<TABLE CLASS="home fullsize" >
    <TR ><TD CLASS="port hdrtxt" ><TABLE CLASS="home fullsize" >
  <TR >
    <TD CLASS="strcol" WIDTH="30%" >Descr</TD>
    <TD CLASS="strcol" >
       <INPUT TYPE="text" NAME="xAxis1_Descr_1" VALUE="<<xAxis1_Descr_1>>" ONFOCUS="select()" SIZE="80" >
    </TD>
  </TR>
  <TR >
    <TD CLASS="strcol" WIDTH="30%" >ICD9</TD>
    <TD CLASS="strcol" >
       <INPUT TYPE="text" NAME="xAxis1_ICD9_1" VALUE="<<xAxis1_ICD9_1>>" ONFOCUS="select()" SIZE="10" >
    </TD>
  </TR>
  <TR >
    <TD CLASS="strcol" WIDTH="30%" >ICD10</TD>
    <TD CLASS="strcol" >
       <INPUT TYPE="text" NAME="xAxis1_ICD10_1" VALUE="<<xAxis1_ICD10_1>>" ONFOCUS="select()" SIZE="10" >
    </TD>
  </TR>
  <TR >
    <TD CLASS="strcol" WIDTH="30%" >Descr for ICD10</TD>
    <TD CLASS="strcol" >
       <INPUT TYPE="text" NAME="xAxis1_Descr2_1" VALUE="<<xAxis1_Descr2_1>>" ONFOCUS="select()" SIZE="80" >
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
document.Axis1.elements[0].focus();
</SCRIPT>

[[myHTML->rightpane(%form+search)]]
