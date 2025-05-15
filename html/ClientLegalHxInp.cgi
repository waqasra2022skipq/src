[[myHTML->newHTML(%form+Client Legal History)]]

<SCRIPT LANGUAGE="JavaScript" SRC="/src/cgi/js/NoEnter.js"> </SCRIPT>
<SCRIPT LANGUAGE="JavaScript" SRC="/src/cgi/js/vEntry.js"> </SCRIPT>
<SCRIPT LANGUAGE="JavaScript" SRC="/src/cgi/js/vClientLegalHx.js"> </SCRIPT>
<SCRIPT LANGUAGE="JavaScript" SRC="/src/cgi/js/qDate.js"> </SCRIPT>

<FORM NAME="ClientLegalHx" ACTION="/cgi/bin/mis.cgi" METHOD="POST" >
<TABLE CLASS="main fullsize" >
  <TR >
    <TD CLASS="strcol" >
      <<<Client_FName_1>>> <<<Client_MName_1>>> <<<Client_LName_1>>> (<<<Client_ClientID_1>>>) <<<Client_SSN_1>>>
      <BR>
      Client Legal History View/Edit Page
    </TD>
    <TD CLASS="numcol" >[[gHTML->setLINKS(%form+back)]]</TD>
  </TR>
</TABLE>
<TABLE CLASS="home fullsize" >
    <TR ><TD CLASS="port hdrtxt" ><TABLE CLASS="home fullsize" >
  <TR > <TD CLASS="port hdrtxt" COLSPAN=2 >LEGAL HISTORY</TD> </TR>
  <TR >
    <TD CLASS="strcol" >Offense Date</TD>
    <TD CLASS="strcol" >
      <INPUT TYPE=text NAME="ClientLegalHx_Date_1" VALUE="<<ClientLegalHx_Date_1>>" ONFOCUS="select()" ONCHANGE="return qDate(this)" SIZE="10" >
    </TD>
  </TR>
  <TR >
    <TD CLASS="strcol" >City</TD>
    <TD CLASS="strcol" >
      <INPUT TYPE=text NAME="ClientLegalHx_City_1" VALUE="<<ClientLegalHx_City_1>>" ONFOCUS="select()" >
    </TD>
  </TR>
  <TR >
    <TD CLASS="strcol" >State</TD>
    <TD CLASS="strcol" >
      <SELECT NAME="ClientLegalHx_ST_1">
        [[DBA->selxTable(%form+xState+<<ClientLegalHx_ST_1>>+Descr)]]
      </SELECT>
    </TD>
  </TR>
  <TR >
    <TD CLASS="strcol" >Type</TD>
    <TD CLASS="strcol" >
      <SELECT NAME="ClientLegalHx_Type_1">
        [[DBA->selxTable(%form+xLegalType+<<ClientLegalHx_Type_1>>+Descr)]]
      </SELECT>
    </TD>
  </TR>
  <TR >
    <TD CLASS="strcol" >Charge</TD>
    <TD CLASS="strcol" >
      <SELECT NAME="ClientLegalHx_Charge_1">
        [[DBA->selxTable(%form+xLegalCharge+<<ClientLegalHx_Charge_1>>+Descr)]]
      </SELECT>
    </TD>
  </TR>
  <TR >
    <TD CLASS="strcol" >OutCome</TD>
    <TD CLASS="strcol" >
      <SELECT NAME="ClientLegalHx_OutCome_1">
        [[DBA->selxTable(%form+xLegalOutCome+<<ClientLegalHx_OutCome_1>>+Descr)]]
      </SELECT>
    </TD>
  </TR>
    </TABLE></TD></TR>
</TABLE>
<TABLE CLASS="main fullsize" >
  <TR >
    <TD CLASS="numcol" >
      <INPUT TYPE="submit" ONCLICK="return vDELETE('Are you sure you want to delete this record?');" NAME="ClientLegalHx_DELETE_1=1&UpdateTables=all&misPOP=1" VALUE="Delete">
      <INPUT TYPE=submit ONCLICK="return validate(this.form);" NAME="UpdateTables=all&misPOP=1" VALUE="Add/Update">
    </TD>
  </TR>
</TABLE>

<INPUT TYPE="hidden" NAME="ClientLegalHx_DELETE_1" VALUE=<<ClientLegalHx_DELETE_1>> >
</LOADHIDDEN>
</FORM>
<SCRIPT LANGUAGE="JavaScript">
document.ClientLegalHx.elements[0].focus();
</SCRIPT>

[[myHTML->rightpane(%form+search)]]
