[[myHTML->newPage(%form+Client GDS)]]

<SCRIPT LANGUAGE="JavaScript" SRC="/src/cgi/js/NoEnter.js"> </SCRIPT>
<SCRIPT LANGUAGE="JavaScript" SRC="/src/cgi/js/vEntry.js"> </SCRIPT>
<SCRIPT LANGUAGE="JavaScript" SRC="/src/cgi/js/vClientGDS.js"> </SCRIPT>
<SCRIPT LANGUAGE="JavaScript" SRC="/src/cgi/js/vDate.js"> </SCRIPT>
<SCRIPT LANGUAGE="JavaScript" SRC="/src/cgi/js/vNum.js"> </SCRIPT>

<FORM NAME="ClientGDS" ACTION="/cgi/bin/mis.cgi" METHOD="POST" >
<TABLE CLASS="main fullsize" >
  <TR >
    <TD CLASS="strcol" >
      <<<Client_FName_1>>> <<<Client_MName_1>>> <<<Client_LName_1>>> (<<<Client_ClientID_1>>>) <<<Client_SSN_1>>>
      <BR>
      Geriatric Depression Scale Page
    </TD>
    <TD CLASS="numcol" >[[gHTML->setLINKS(%form+back)]]</TD>
  </TR>
</TABLE>
<TABLE CLASS="port fullsize" >
    <TR ><TD CLASS="port hdrtxt" ><TABLE CLASS="home fullsize" >
  <TR >
    <TD CLASS="strcol" >Score</TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="TEXT" NAME="ClientGDS_Score_1" VALUE="<<ClientGDS_Score_1>>" ONFOCUS="select()" ONCHANGE="return vNum(this,0,30)" SIZE="6" >
      enter a value between 0 and 30
    </TD>
  </TR>
  <TR >
    <TD CLASS="strcol" >Effective Date</TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="TEXT" NAME="ClientGDS_EffDate_1" VALUE="<<ClientGDS_EffDate_1>>" ONFOCUS="select()" ONCHANGE="return vDate(this)" SIZE="10" >
    </TD>
  </TR>
  <TR >
    <TD CLASS="strcol" >Expire Date</TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="TEXT" NAME="ClientGDS_ExpDate_1" VALUE="<<ClientGDS_ExpDate_1>>" ONFOCUS="select()" ONCHANGE="return vDate(this)" SIZE="10" >
    </TD>
  </TR>
    </TABLE></TD></TR>
</TABLE>
<TABLE CLASS="main fullsize" >
  <TR >
    <TD CLASS="numcol" >
      <INPUT TYPE=submit ONCLICK="return validate(this.form);" NAME="UpdateTables=all&misPOP=1" VALUE="Add/Update">
    </TD>
  </TR>
</TABLE>

</LOADHIDDEN>
</FORM>
<SCRIPT LANGUAGE="JavaScript">
document.ClientGDS.elements[0].focus();
</SCRIPT>
[[myHTML->rightpane(%form+search)]]
