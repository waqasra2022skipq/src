[[myHTML->newPage(%form+Client Income)]]

<SCRIPT LANGUAGE="JavaScript" SRC="/cgi/js/NoEnter.js"> </SCRIPT>
<SCRIPT LANGUAGE="JavaScript" SRC="/cgi/js/vEntry.js"> </SCRIPT>
<SCRIPT LANGUAGE="JavaScript" SRC="/cgi/js/vClientIncome.js"> </SCRIPT>
<SCRIPT LANGUAGE="JavaScript" SRC="/cgi/js/vNum.js"> </SCRIPT>
<SCRIPT LANGUAGE="JavaScript" SRC="/cgi/js/vDate.js"> </SCRIPT>

<FORM NAME="ClientIncome" ACTION="/cgi/bin/mis.cgi" METHOD="POST" >
<TABLE CLASS="main fullsize" >
  <TR >
    <TD CLASS="strcol" >
      <<<Client_FName_1>>> <<<Client_MName_1>>> <<<Client_LName_1>>> (<<<Client_ClientID_1>>>) <<<Client_SSN_1>>>
      <BR>
      Client Income View/Edit Page
    </TD>
    <TD CLASS="numcol" >[[gHTML->setLINKS(%form+back)]]</TD>
  </TR>
</TABLE>
<TABLE CLASS="home fullsize" >
    <TR ><TD CLASS="port hdrtxt" ><TABLE CLASS="home fullsize" >
  <TR ><TD CLASS="port hdrtxt" COLSPAN=2 ><U>Income</U></TD></TR>
  <TR >
    <TD CLASS="strcol" >Source of Income</TD>
    <TD CLASS="strcol" >
      <SELECT NAME="ClientIncome_Src_1" >
        [[DBA->selxTable(%form+xIncome+<<ClientIncome_Src_1>>+Descr)]]
      </SELECT>
    </TD>
  </TR>
  <TR >
    <TD CLASS="strcol" >Last 30 Days</TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="TEXT" NAME="ClientIncome_Amt30_1" VALUE="<<ClientIncome_Amt30_1>>" ONFOCUS="select()" ONCHANGE="return vNum(this,0,99999);" SIZE=12 > 
    </TD>
  </TR>
  <TR >
    <TD CLASS="strcol" >Yearly Amount</TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="TEXT" NAME="ClientIncome_Amt_1" VALUE="<<ClientIncome_Amt_1>>" ONFOCUS="select()" ONCHANGE="return vNum(this,0,99999);" SIZE=12 > 
    </TD>
  </TR>
  <TR >
    <TD CLASS="strcol" >Effective</TD>
    <TD CLASS="strcol" >
      <INPUT TYPE=TEXT SIZE="10" NAME="ClientIncome_EffDate_1" VALUE="<<ClientIncome_EffDate_1>>" ONFOCUS="select()" ONCHANGE="return vDate(this)" SIZE="12" >
    </TD>
  </TR>
  <TR >
    <TD CLASS="strcol" >Expires</TD>
    <TD CLASS="strcol" >
      <INPUT TYPE=TEXT SIZE="10" NAME="ClientIncome_ExpDate_1" VALUE="<<ClientIncome_ExpDate_1>>" ONFOCUS="select()" ONCHANGE="return vDate(this)" SIZE="12" >
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
document.ClientIncome.elements[0].focus();
</SCRIPT>

[[myHTML->rightpane(%form+search)]]
