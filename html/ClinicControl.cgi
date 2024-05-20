[[myHTML->newPage(%form+Clinic Control)]]

<SCRIPT LANGUAGE="JavaScript" SRC="/cgi/js/NoEnter.js"> </SCRIPT>
<SCRIPT LANGUAGE="JavaScript" SRC="/cgi/js/vEntry.js"> </SCRIPT>
<SCRIPT LANGUAGE="JavaScript" SRC="/cgi/js/vClinicControl.js"> </SCRIPT>
<SCRIPT LANGUAGE="JavaScript" SRC="/cgi/js/vNum.js"> </SCRIPT>

<FORM NAME="ClinicControl" ACTION="/cgi/bin/mis.cgi" METHOD="POST" >
<TABLE CLASS="main fullsize" >
  <TR >
    <TD CLASS="strcol" >
      <<<Provider_FName_1>>> <<<Provider_MName_1>>> <<<Provider_LName_1>>> 
      (<<<Provider_ProvID_1>>>)
      <BR>Clinic Control
    </TD>
    <TD CLASS="numcol" >[[gHTML->setLINKS(%form+back)]]</TD>
  </TR>
</TABLE>
<HR WIDTH="90%" >
<TABLE CLASS="home fullsize" >
    <TR ><TD ><TABLE CLASS="home fullsize" >
  <TR><TD COLSPAN="2" >Health Information Identifiers</TD></TR>
  <TR>
    <TD CLASS="strcol" >NPI #</TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="text" NAME="ProviderControl_NPI_1" VALUE="<<ProviderControl_NPI_1>>" ONFOCUS="select()" ONCHANGE="return vNum(this,1000000000)" MAXLENGTH="10" SIZE="10" >
    </TD>
  </TR>
  <TR>
    <TD CLASS="strcol" >CLIA #</TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="text" NAME="ProviderControl_CLIA_1" VALUE="<<ProviderControl_CLIA_1>>" ONFOCUS="select()" SIZE="30" >
      Clinical Laboratory Improvement Amendments
    </TD>
  </TR>
  <TR>
    <TD CLASS="strcol" >OID</TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="text" NAME="ProviderControl_OID_1" VALUE="<<ProviderControl_OID_1>>" ONFOCUS="select()" SIZE="30" >
    </TD>
  </TR>
    </TABLE></TD></TR>
    <TR ><TD ><TABLE CLASS="home fullsize" >
  <TR><TD COLSPAN="2" >Access and Passwords</TD></TR>
  <TR>
    <TD CLASS="strcol" >Passwords</TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="text" NAME="ProviderControl_Passwords_1" VALUE="<<ProviderControl_Passwords_1>>" ONFOCUS="select()" SIZE="120" >
    </TD>
  </TR>
  <TR>
    <TD CLASS="strcol" >PECOS</TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="text" NAME="ProviderControl_PECOS_1" VALUE="<<ProviderControl_PECOS_1>>" ONFOCUS="select()" SIZE="120" >
    </TD>
  </TR>
  <TR>
    <TD CLASS="strcol" >AVAILITY</TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="text" NAME="ProviderControl_AVAILITY_1" VALUE="<<ProviderControl_AVAILITY_1>>" ONFOCUS="select()" SIZE="120" >
    </TD>
  </TR>
  <TR>
    <TD CLASS="strcol" >OHCA</TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="text" NAME="ProviderControl_OHCA_1" VALUE="<<ProviderControl_OHCA_1>>" ONFOCUS="select()" SIZE="120" >
    </TD>
  </TR>
  <TR>
    <TD CLASS="strcol" >PICIS</TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="text" NAME="ProviderControl_PICIS_1" VALUE="<<ProviderControl_PICIS_1>>" ONFOCUS="select()" SIZE="120" >
    </TD>
  </TR>
  <TR>
    <TD CLASS="strcol" >TRICARE</TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="text" NAME="ProviderControl_TRICARE_1" VALUE="<<ProviderControl_TRICARE_1>>" ONFOCUS="select()" SIZE="120" >
    </TD>
  </TR>
  <TR>
    <TD CLASS="strcol" >Logout in Minutes</TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="text" NAME="ProviderControl_minToLogOut_1" VALUE="<<ProviderControl_minToLogOut_1>>" ONFOCUS="select()" ONCHANGE="return vNum(this,1,60);" MAXLENGTH="5" SIZE="5" > default minutes for user to be timed out and logged out.
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

<INPUT TYPE="hidden" NAME="post_update" VALUE="DBA->updProvider(%form)" >
</LOADHIDDEN>
</FORM>
<SCRIPT LANGUAGE="JavaScript">
document.ClinicControl.elements[0].focus();
</SCRIPT>

[[myHTML->rightpane(%form+search)]]
