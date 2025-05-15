[[myHTML->newPage(%form+Prior Authorization)]]

<SCRIPT LANGUAGE="JavaScript" SRC="/src/cgi/js/vEntry.js"> </SCRIPT>
<SCRIPT LANGUAGE="JavaScript" SRC="/src/cgi/js/vPrAuthDates.js"> </SCRIPT>
<SCRIPT LANGUAGE="JavaScript" SRC="/src/cgi/js/vDate.js"> </SCRIPT>
<SCRIPT LANGUAGE="JavaScript" SRC="/src/cgi/js/vTime.js"> </SCRIPT>

<FORM NAME="ClientPrAuth" ACTION="/cgi/bin/mis.cgi" METHOD="POST" >
<TABLE CLASS="main fullsize" >
  <TR >
    <TD CLASS="strcol" >
      <<<Client_FName_1>>> <<<Client_MName_1>>> <<<Client_LName_1>>> (<<<Client_ClientID_1>>>) <<<Client_SSN_1>>>
      <BR>
      Client's Prior Authorization
    </TD>
    <TD CLASS="numcol" >[[gHTML->setLINKS(%form+back)]]</TD>
  </TR>
</TABLE>
<TABLE CLASS="port fullsize" >
  <TR >
    <TD CLASS="heading" >[[DBUtil->isNULL(<<<ClientPrAuth_ID_1>>>)New Prior Authorization]] &nbsp; </TD>
  </TR>
  <TR >
    <TD CLASS="heading" >
      Client has [[DBA->getxref(%form+xInsurance+<<<Insurance_InsID_1>>>+Name)]] Insurance
    </TD>
  </TR>
</TABLE>
<TABLE CLASS="home fullsize" >
  </TR>
  <TR > <TD CLASS="strcol hotmsg" COLSPAN="2" >Date must be today or a date in the future.</TD></TR>
  <TR >
    <TD CLASS="strcol" >Effective Date:</TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="TEXT" ID="EffDate" NAME="ClientPrAuth_EffDate_1" VALUE="<<ClientPrAuth_EffDate_1>>" ONFOCUS="select();" ONCHANGE="vDate(this,0,this.form,'',<<TODAY>>);" MAXLENGTH="10" SIZE="12" >
    </TD>
  </TR>
  <TR >
    <TD CLASS="strcol" >Expire Date:</TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="TEXT" ID="ExpDate" NAME="ClientPrAuth_ExpDate_1" VALUE="<<ClientPrAuth_ExpDate_1>>" ONFOCUS="select();" ONCHANGE="vDate(this,0,this.form,'',<<TODAY>>);" MAXLENGTH="10" SIZE="12" >
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
document.ClientPrAuth.elements[0].focus();
</SCRIPT>

[[myHTML->rightpane(%form+search)]]
