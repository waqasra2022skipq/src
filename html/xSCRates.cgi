[[myHTML->newPage(%form+Rates)]]

<SCRIPT LANGUAGE="JavaScript" SRC="/src/cgi/js/vEntry.js"> </SCRIPT>
<SCRIPT LANGUAGE="JavaScript" SRC="/src/cgi/js/vxSCRates.js"> </SCRIPT>
<SCRIPT LANGUAGE="JavaScript" SRC="/src/cgi/js/vNum.js"> </SCRIPT>
<SCRIPT LANGUAGE="JavaScript" SRC="/src/cgi/js/vDate.js"> </SCRIPT>

<FORM NAME="xSCRates" ACTION="/cgi/bin/mis.cgi" METHOD="POST" >
<TABLE CLASS="main fullsize" >
  <TR >
    <TD CLASS="strcol" >
      SERVICE CODE RATES for:
      <BR><<<xSC_SCNum_1>>> <<<xSC_SCName_1>>>
    </TD>
    <TD CLASS="numcol" >[[gHTML->setLINKS(%form+back)]]</TD>
  </TR>
</TABLE>
<TABLE CLASS="home fullsize" >
  <TR >
    <TD CLASS="strcol" WIDTH="30%" >Service Rate: </TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="TEXT" NAME="xSCRates_ServiceRate_1" VALUE="<<xSCRates_ServiceRate_1>>" ONFOCUS="select()" ONCHANGE="return vNum(this,0,8000);" SIZE=10 > 
    </TD>
  </TR>
  <TR >
    <TD CLASS="strcol" WIDTH="30%" >Hours/Unit: </TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="TEXT" NAME="xSCRates_HrsPerUnit_1" VALUE="<<xSCRates_HrsPerUnit_1>>" ONFOCUS="select()" ONCHANGE="return vNum(this,0,8);" SIZE=10 > 
      (IEs)
    </TD>
  </TR>
  <TR >
    <TD CLASS="strcol" WIDTH="30%" >Unit Label: </TD>
    <TD CLASS="strcol" >
      <SELECT NAME="xSCRates_UnitLbl_1" >[[DBA->selxTable(%form+xSCUnitLbl+<<xSCRates_UnitLbl_1>>)]]</SELECT>
    </TD>
  </TR>
  <TR >
    <TD CLASS="strcol" WIDTH="30%" >Rate %: </TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="TEXT" NAME="xSCRates_RatePct_1" VALUE="<<xSCRates_RatePct_1>>" ONFOCUS="select()" ONCHANGE="return vNum(this,0,1);" SIZE=6 > 
    </TD>
  </TR>
  <TR >
    <TD CLASS="strcol" WIDTH="30%" >Commission %: </TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="TEXT" NAME="xSCRates_CommissionPct_1" VALUE="<<xSCRates_CommissionPct_1>>" ONFOCUS="select()" ONCHANGE="return vNum(this,0,1);" SIZE=6 > 
    </TD>
  </TR>
  <TR >
    <TD CLASS="strcol" WIDTH="30%" >RVU Multiplier: </TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="TEXT" NAME="xSCRates_RVUPct_1" VALUE="<<xSCRates_RVUPct_1>>" ONFOCUS="select()" ONCHANGE="return vNum(this,0,5);" SIZE=6 > 
    </TD>
  </TR>
  <TR>
    <TD CLASS="strcol" WIDTH="30%" >Effective Date</TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="TEXT" NAME="xSCRates_EffDate_1" VALUE="<<xSCRates_EffDate_1>>" ONFOCUS="select()" ONCHANGE="return vDate(this);" SIZE=12 > 
    </TD>
  </TR>
  <TR>
    <TD CLASS="strcol" WIDTH="30%" >Expiration Date</TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="TEXT" NAME="xSCRates_ExpDate_1" VALUE="<<xSCRates_ExpDate_1>>" ONFOCUS="select()" ONCHANGE="return vDate(this,1);" SIZE=12 > 
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
document.xSCRates.elements[0].focus();
</SCRIPT>
[[myHTML->rightpane(%form+search)]]
