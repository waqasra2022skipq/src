[[myHTML->newPage(%form+Provider Vacation and Sick Information)]]

<SCRIPT LANGUAGE="JavaScript" SRC="/src/cgi/js/NoEnter.js"> </SCRIPT>
<SCRIPT LANGUAGE="JavaScript" SRC="/src/cgi/js/vEntry.js"> </SCRIPT>
<SCRIPT LANGUAGE="JavaScript" SRC="/src/cgi/js/vProviderHrs.js"> </SCRIPT>
<SCRIPT LANGUAGE="JavaScript" SRC="/src/cgi/js/vNum.js"> </SCRIPT>
<SCRIPT LANGUAGE="JavaScript" >
function vAdd(NumStr,fld) 
{
  if ( !vNum(NumStr,-999,999) )
  { return false; }
  if ( NumStr.value == "" ) { return true; }
  var a = 0;
  if ( fld.value != "" ) { a = fld.value; }
  fld.value = parseFloat(a) + parseFloat(NumStr.value);
  return true;
}
</SCRIPT>

<FORM NAME="ProviderHrs" ACTION="/cgi/bin/mis.cgi" METHOD="POST" >
<TABLE CLASS="main fullsize" >
  <TR >
    <TD CLASS="strcol" >
      <<<Provider_FName_1>>> <<<Provider_MName_1>>> <<<Provider_LName_1>>> 
      <BR>Vacation/Sick Information
    </TD>
    <TD CLASS="numcol" >[[gHTML->setLINKS(%form+back)]]</TD>
  </TR>
</TABLE>
<TABLE CLASS="home fullsize" >
    <TR ><TD ><TABLE CLASS="home fullsize" >
  <TR >
    <TD CLASS="strcol" COLSPAN="2" >Accrual Rate</TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="TEXT" NAME="ProviderHrs_AccrRate_1" VALUE="<<ProviderHrs_AccrRate_1>>" ONFOCUS="select()" ONCHANGE="return vNum(this,7,9);" SIZE=8>
    </TD>
  </TR>
  <TR >
    <TD CLASS="strcol" >Accrued Hours YTD</TD>
    <TD CLASS="strcol" >
      Add
      <INPUT TYPE="TEXT" NAME="AccrHrs" ONFOCUS="select()" ONCHANGE="return vAdd(this,form.ProviderHrs_AccrHrs_1);" SIZE=5>
    </TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="TEXT" NAME="ProviderHrs_AccrHrs_1" VALUE="<<ProviderHrs_AccrHrs_1>>" ONFOCUS="form.UtilHrs.focus();" SIZE=8>
    </TD>
  </TR>
  <TR >
    <TD CLASS="strcol" >Utilized Leave YTD</TD>
    <TD CLASS="strcol" >
      Add
      <INPUT TYPE="TEXT" NAME="UtilHrs" ONFOCUS="select()" ONCHANGE="return vAdd(this,form.ProviderHrs_UtilHrs_1);" SIZE=5>
    </TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="TEXT" NAME="ProviderHrs_UtilHrs_1" VALUE="<<ProviderHrs_UtilHrs_1>>" ONFOCUS="form.CredHrs.focus();" SIZE=8>
    </TD>
  </TR>
  <TR >
    <TD CLASS="strcol" >Credit Hours YTD</TD>
    <TD CLASS="strcol" >
      Add
      <INPUT TYPE="TEXT" NAME="CredHrs" ONFOCUS="select()" ONCHANGE="return vAdd(this,form.ProviderHrs_CredHrs_1);" SIZE=5>
    </TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="TEXT" NAME="ProviderHrs_CredHrs_1" VALUE="<<ProviderHrs_CredHrs_1>>" ONFOCUS="form.ProviderHrs_CoreHrs_1.focus();" SIZE=8>
    </TD>
  </TR>
  <TR >
    <TD CLASS="strcol" COLSPAN="2" >Core Work Hours</TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="TEXT" NAME="ProviderHrs_CoreHrs_1" VALUE="<<ProviderHrs_CoreHrs_1>>" ONFOCUS="select()" SIZE=8>
    </TD>
  </TR>
    </TABLE></TD></TR>
</TABLE>
<TABLE CLASS="main fullsize" >
  <TR >
    <TD CLASS="numcol" >
      <INPUT TYPE="submit" ONCLICK="return validate(this.form);" NAME="UpdateTables=all&misPOP=1" VALUE="Add/Update">
    </TD>
  </TR>
</TABLE>

</LOADHIDDEN>
</FORM>
<SCRIPT LANGUAGE="JavaScript">
document.ProviderHrs.elements[0].focus();
</SCRIPT>

[[myHTML->rightpane(%form+search)]]
