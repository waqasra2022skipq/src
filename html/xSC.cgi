[[myHTML->newPage(%form+ServiceCodes)]]

<SCRIPT LANGUAGE="JavaScript" SRC="/cgi/js/vEntry.js"> </SCRIPT>
<SCRIPT LANGUAGE="JavaScript" SRC="/cgi/js/vxSC.js"> </SCRIPT>
<SCRIPT LANGUAGE="JavaScript" SRC="/cgi/js/Utils.js"> </SCRIPT>

<FORM NAME="xSC" ACTION="/cgi/bin/mis.cgi" METHOD="POST" >
<TABLE CLASS="main fullsize" >
  <TR >
    <TD CLASS="strcol" >
      Insurance Service Code for:
      <BR><<<xInsurance_Name_1>>>
    </TD>
    <TD CLASS="numcol" >[[gHTML->setLINKS(%form+back)]]</TD>
  </TR>
</TABLE>
<TABLE CLASS="home fullsize" >
  <TR>
    <TD CLASS="strcol" WIDTH="30%" >Number</TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="text" NAME="xSC_SCNum_1" VALUE="<<xSC_SCNum_1>>" ONCHANGE="return stringTrim(this);" ONFOCUS="select()" SIZE="20" >
    </TD>
  </TR>
  <TR>
    <TD CLASS="strcol" WIDTH="30%" >Name</TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="text" NAME="xSC_SCName_1" VALUE="<<xSC_SCName_1>>" ONFOCUS="select()" SIZE="60" >
    </TD>
  </TR>
  <TR>
    <TD CLASS="strcol" WIDTH="30%" >Type</TD>
    <TD CLASS="strcol" >
      <SELECT NAME="xSC_Type_1" >
        [[DBA->selxTable(%form+xSCType+<<xSC_Type_1>>+Descr)]]
      </SELECT> 
      (for PA packet and Note Validation)
    </TD>
  </TR>
  <TR>
    <TD CLASS="strcol" WIDTH="30%" >Service Type (category)</TD>
    <TD CLASS="strcol" >
      <SELECT NAME="xSC_ServiceType_1" >
        [[DBA->selxTable(%form+xServiceType+<<xSC_ServiceType_1>>+Descr)]]
      </SELECT> 
    </TD>
  </TR>
  <TR>
    <TD CLASS="strcol" WIDTH="30%" >Prior Authorization Required</TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="checkbox" NAME="xSC_PAReq_1" VALUE=1 <<xSC_PAReq_1=checkbox>> >
    </TD>
  </TR>
  <TR>
    <TD CLASS="strcol" WIDTH="30%" >Place of Service</TD>
    <TD CLASS="strcol" >
      <SELECT NAME="xSC_POS_1" >
        [[DBA->selxTable(%form+xPOS+<<xSC_POS_1>>+Descr)]]
      </SELECT> 
    </TD>
  </TR>
  <TR>
    <TD CLASS="strcol" WIDTH="30%" >Credentials Required</TD>
    <TD CLASS="strcol" >
      <SELECT NAME="xSC_CredID_1" >
        [[DBA->selxTable(%form+xCredentials+<<xSC_CredID_1>>)]]
      </SELECT> 
    </TD>
  </TR>
  <TR>
    <TD CLASS="strcol" WIDTH="30%" >Restrict to</TD>
    <TD CLASS="strcol" >
      <SELECT NAME="xSC_Restriction_1" >
        [[DBA->selxTable(%form+xSCRestrictions+<<xSC_Restriction_1>>)]]
      </SELECT> 
    </TD>
  </TR>
  <TR>
    <TD CLASS="strcol" WIDTH="30%" >Requires Provider PIN</TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="checkbox" NAME="xSC_PINReq_1" VALUE=1 <<xSC_PINReq_1=checkbox>> >
      (for billing purposes)
    </TD>
  </TR>
  <TR>
    <TD CLASS="strcol" WIDTH="30%" COLSPAN="2" >
      Interchange with
      (use this code for inventory)
    </TD>
  </TR>
  <TR>
    <TD CLASS="strcol" COLSPAN="2" >
      <SELECT NAME="xSC_Interchange_1" >
        [[DBA->selServiceCodes(%form+<<xSC_Interchange_1>>+0+++INSID=<<<xInsurance_ID_1>>>)]]
      </SELECT> 
    </TD>
  </TR>
  <TR>
    <TD CLASS="strcol" WIDTH="30%" >Exclude from Inventory</TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="checkbox" NAME="xSC_ExInv_1" VALUE=1 <<xSC_ExInv_1=checkbox>> >
    </TD>
  </TR>
  <TR>
    <TD CLASS="strcol" WIDTH="30%" >Active</TD>
    <TD CLASS="strcol" >
      <INPUT TYPE=radio NAME="xSC_Active_1" VALUE=1 <<xSC_Active_1=1>> > yes
      <INPUT TYPE=radio NAME="xSC_Active_1" VALUE=0 <<xSC_Active_1=0>> > no
    </TD>
  </TR>
  <TR >
    <TD CLASS="port hdrtxt" COLSPAN="2" >
[[myHTML->ListSel(%form+ListxSCRates+<<<xSC_SCID>>>+<<<LINKID>>>+<<<Provider_Locked_1>>>)]]
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
document.xSC.elements[0].focus();
</SCRIPT>
[[myHTML->rightpane(%form+search)]]
