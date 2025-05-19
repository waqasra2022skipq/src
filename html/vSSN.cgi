[[myHTML->newPage(%form+SSN Entry)]]

<SCRIPT LANGUAGE="JavaScript" SRC="/src/cgi/js/vSSN.js"> </SCRIPT>
<SCRIPT LANGUAGE="JavaScript" SRC="/src/cgi/js/vEntry.js"> </SCRIPT>
<SCRIPT LANGUAGE="JavaScript">
function validate(form) 
{ 
  if ( vSSN(form.SSN) )
  { return vEntry("notnull",form.SSN); }
  else { return false; }
}
</SCRIPT>

<FORM NAME="vSSN" ONSUBMIT="return validate(this);" ACTION="/src/cgi/bin/vClient.cgi" METHOD="POST" >
<TABLE CLASS="main fullsize" >
  <TR >
    <TD CLASS="strcol" >
      Client Lookup<BR>by Social Security Number
    </TD>
    <TD CLASS="numcol" >[[gHTML->setLINKS(%form+back)]]</TD>
  </TR>
</TABLE>
<TABLE CLASS="home fullsize" >
  <TR >
    <TD CLASS="port hdrtxt" COLSPAN="3" >
      Please enter the Social Security Number
    </TD>
  </TR>
  <TR >
    <TD CLASS="strcol" >SSN</TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="text" NAME="SSN" VALUE="<<SSN>>" ONCHANGE="return validate(this.form)" ONFOCUS="select()" SIZE=11>
    </TD>
    <TD CLASS="numcol" ><INPUT TYPE="submit" VALUE="search"></TD>
  </TR>
</TABLE>

<INPUT TYPE="hidden" NAME="ProviderID" VALUE="<<ProviderID>>" >
</LOADHIDDEN>
</FORM>
<SCRIPT LANGUAGE="JavaScript">
document.vSSN.elements[0].focus();
</SCRIPT>

[[myHTML->rightpane(%form+search)]]
