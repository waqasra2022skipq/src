[[myHTML->newPage(%form+Contracts)]]

<SCRIPT LANGUAGE="JavaScript" SRC="/cgi/js/vEntry.js"> </SCRIPT>
<SCRIPT LANGUAGE="JavaScript" SRC="/cgi/js/vProviderContracts.js"> </SCRIPT>
<SCRIPT LANGUAGE="JavaScript" SRC="/cgi/js/serverREQ.js"> </SCRIPT>

[[*SysAccess->verify(%form+hasProviderAccess)]]

<FORM NAME="Contracts" ACTION="/cgi/bin/mis.cgi" METHOD="POST" >
<TABLE CLASS="main fullsize" >
  <TR >
    <TD CLASS="strcol" >
      <<<Provider_FName_1>>> <<<Provider_MName_1>>> <<<Provider_LName_1>>> 
      <BR>
      Contract Information
    </TD>
    <TD CLASS="numcol" >[[gHTML->setLINKS(%form+back)]]</TD>
  </TR>
</TABLE>
<TABLE CLASS="home fullsize" >
    <TR ><TD ><TABLE CLASS="home fullsize" >
  <TR><TD CLASS="hdrtxt" >Contract Information</TD></TR>
  <TR>
    <TD CLASS="strcol" >Assoc. Insurance</TD>
    <TD CLASS="strcol" >
      <SELECT ID="InsID" NAME="Contracts_InsID_1" ONCHANGE="createFLD(this,'/cgi/bin/verify.pl?mlt=<<<mlt>>>&type=EFT','selEFT')" >
        [[DBA->selxTable(%form+xInsurance+<<Contracts_InsID_1>>+Name)]]
      </SELECT>
    </TD>
  </TR>
  <TR>
    <TD CLASS="strcol" >Provider has setup Contract with Insurance</TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="radio" NAME="Contracts_setContract_1" VALUE="1" <<Contracts_setContract_1=1>> > yes
      <INPUT TYPE="radio" NAME="Contracts_setContract_1" VALUE="0" <<Contracts_setContract_1=0>> > no
      <INPUT TYPE="radio" NAME="Contracts_setContract_1" VALUE="N" <<Contracts_setContract_1=N>> > n/a
    </TD>
  </TR>
  <TR>
    <TD CLASS="strcol" >Provider has setup Prior Authorization</TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="radio" NAME="Contracts_setPA_1" VALUE="1" <<Contracts_setPA_1=1>> > yes
      <INPUT TYPE="radio" NAME="Contracts_setPA_1" VALUE="0" <<Contracts_setPA_1=0>> > no
      <INPUT TYPE="radio" NAME="Contracts_setPA_1" VALUE="N" <<Contracts_setPA_1=N>> > n/a
    </TD>
  </TR>
  <TR>
    <TD CLASS="strcol" >Provider has faxed EFT Enrollment to Insurance</TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="radio" NAME="Contracts_setInsEFT_1" VALUE="1" <<Contracts_setInsEFT_1=1>> > yes
      <INPUT TYPE="radio" NAME="Contracts_setInsEFT_1" VALUE="0" <<Contracts_setInsEFT_1=0>> > no
      <INPUT TYPE="radio" NAME="Contracts_setInsEFT_1" VALUE="N" <<Contracts_setInsEFT_1=N>> > n/a
    </TD>
  </TR>
  <TR>
    <TD CLASS="strcol" >Provider has faxed ERA Enrollment to Clearing House</TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="radio" NAME="Contracts_setBillEFT_1" VALUE="1" <<Contracts_setBillEFT_1=1>> > yes
      <INPUT TYPE="radio" NAME="Contracts_setBillEFT_1" VALUE="0" <<Contracts_setBillEFT_1=0>> > no
      <INPUT TYPE="radio" NAME="Contracts_setBillEFT_1" VALUE="N" <<Contracts_setBillEFT_1=N>> > n/a
    </TD>
  </TR>
  <TR>
    <TD CLASS="strcol" >&nbsp;</TD>
    <TD CLASS="strcol" >
      <SPAN ID="selEFT"> </SPAN>
    </TD>
  </TR>
  <TR>
    <TD CLASS="strcol" >Contract Manager</TD>
    <TD CLASS="strcol" >
      <SELECT NAME="Contracts_MgrID_1">[[DBA->selProviders(%form+<<Contracts_MgrID_1>>)]]</SELECT> 
      (who to contact at this Agency)
    </TD>
  </TR>
  <TR>
    <TD CLASS="strcol" >PIN</TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="text" NAME="Contracts_PIN_1" VALUE="<<Contracts_PIN_1>>" SIZE="50" > 
    </TD>
  </TR>
  <TR >
    <TD CLASS="strcol" >PIN Qualifier</TD>
    <TD CLASS="strcol" >
      <SELECT NAME="Contracts_RefID_1">[[DBA->selxTable(%form+xRefID+<<Contracts_RefID_1>>+ID Descr)]]</SELECT> 
    </TD>
  </TR>
  <TR>
    <TD CLASS="strcol" >Master PIN</TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="text" NAME="Contracts_MasterPIN_1" VALUE="<<Contracts_MasterPIN_1>>" SIZE="50" > 
      (for multiple locations)
    </TD>
  </TR>
  <TR >
    <TD CLASS="strcol" >Account ID</TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="text" NAME="Contracts_OrgID_1" VALUE="<<Contracts_OrgID_1>>" ONFOCUS="select()" SIZE="30" >
      (ex: Medicaid Org ID)
    </TD>
  </TR>
  <TR >
    <TD CLASS="strcol" >TaxID</TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="text" NAME="Contracts_TaxID_1" VALUE="<<Contracts_TaxID_1>>" ONFOCUS="select()" SIZE="30" >
    </TD>
  </TR>
  <TR>
    <TD CLASS="strcol" COLSPAN="2" >Taxonomy</TD>
  </TR>
  <TR>
    <TD CLASS="strcol" COLSPAN="2" >
      <SELECT NAME="Contracts_Taxonomy_1" >
        [[DBA->selxTable(%form+xTaxonomy+<<Contracts_Taxonomy_1>>+ID Spec Class Type)]]
      </SELECT>
    </TD>
  </TR>
  <TR >
    <TD CLASS="strcol hotmsg" COLSPAN="2" >Billing/rendering Provider taxonomy codes MUST match the OHCA Master Provider List (MPL), billing/rendering Provider addresses MUST ALSO match the OHCA MPL.  Check the OHCA Provider Contract to verify.</TD>
  </TR>
  <TR>
    <TD CLASS="strcol" >To Be Billed</TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="radio" NAME="Contracts_BillFlag_1" VALUE="1" <<Contracts_BillFlag_1=1>> > yes
      <INPUT TYPE="radio" NAME="Contracts_BillFlag_1" VALUE="0" <<Contracts_BillFlag_1=0>> > no
    </TD>
  </TR>
  <TR>
    <TD CLASS="strcol" >Billing Type</TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="radio" NAME="Contracts_BillType_1" VALUE="EL" <<Contracts_BillType_1=EL>> > Electronic
      <INPUT TYPE="radio" NAME="Contracts_BillType_1" VALUE="BH" <<Contracts_BillType_1=BH>> > Black HCFA
      <INPUT TYPE="radio" NAME="Contracts_BillType_1" VALUE="RH" <<Contracts_BillType_1=RH>> > Red HCFA (for pre-printed forms)
      <INPUT TYPE="radio" NAME="Contracts_BillType_1" VALUE="SS" <<Contracts_BillType_1=SS>> > Report
    </TD>
  </TR>
  <TR>
    <TD CLASS="strcol" >Use Agency address for Billing/Payto Provider (not Clinic Address)</TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="radio" NAME="Contracts_UseAgency_1" VALUE="1" <<Contracts_UseAgency_1=1>> > yes
      <INPUT TYPE="radio" NAME="Contracts_UseAgency_1" VALUE="0" <<Contracts_UseAgency_1=0>> > no
    </TD>
  </TR>
  <TR>
    <TD CLASS="strcol" >Auto Reconcile</TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="radio" NAME="Contracts_AutoReconcile_1" VALUE="1" <<Contracts_AutoReconcile_1=1>> > yes
      <INPUT TYPE="radio" NAME="Contracts_AutoReconcile_1" VALUE="0" <<Contracts_AutoReconcile_1=0>> > no
    </TD>
  </TR>
  <TR>
    <TD CLASS="strcol" >Auto Pay</TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="radio" NAME="Contracts_AutoPay_1" VALUE="1" <<Contracts_AutoPay_1=1>> > yes
      <INPUT TYPE="radio" NAME="Contracts_AutoPay_1" VALUE="0" <<Contracts_AutoPay_1=0>> > no
    </TD>
  </TR>
    </TABLE></TD></TR>
    <TR ><TD ><TABLE CLASS="home fullsize" >
[[gHTML->RestrictedContractsFields(%form+Agent)]]
    </TABLE></TD></TR>
</TABLE>
<TABLE CLASS="main fullsize" >
  <TR>
    <TD CLASS="numcol" >
      <INPUT TYPE="submit" ONCLICK="return validate(this.form);" NAME="UpdateTables=all&misPOP=1" VALUE="Add/Update" >
    </TD>
  </TR>
</TABLE>

<INPUT TYPE="hidden" NAME="post_update" VALUE="PostUpd->updContracts(%form)" >
</LOADHIDDEN>
</FORM>
<SCRIPT LANGUAGE="JavaScript">
document.Contracts.elements[0].focus();
createFLD(document.Contracts.Contracts_InsID_1,'/cgi/bin/verify.pl?mlt=<<<mlt>>>&type=EFT','selEFT','selEFT');
</SCRIPT>
[[myHTML->rightpane(%form+search)]]
