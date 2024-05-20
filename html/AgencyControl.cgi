[[myHTML->newPage(%form+Agency Control)]]

<SCRIPT LANGUAGE="JavaScript" SRC="/cgi/js/NoEnter.js"> </SCRIPT>
<SCRIPT LANGUAGE="JavaScript" SRC="/cgi/js/vEntry.js"> </SCRIPT>
<SCRIPT LANGUAGE="JavaScript" SRC="/cgi/js/vAgencyControl.js"> </SCRIPT>
<SCRIPT LANGUAGE="JavaScript" SRC="/cgi/js/vDate.js"> </SCRIPT>
<SCRIPT LANGUAGE="JavaScript" SRC="/cgi/js/vNum.js"> </SCRIPT>

<FORM NAME="AgencyControl" ACTION="/cgi/bin/mis.cgi" METHOD="POST" >
<TABLE CLASS="main fullsize" >
  <TR >
    <TD CLASS="strcol" >
      <<<Provider_FName_1>>> <<<Provider_MName_1>>> <<<Provider_LName_1>>> 
      (<<<Provider_ProvID_1>>>)
      <BR>Provider Control
    </TD>
    <TD CLASS="numcol" >[[gHTML->setLINKS(%form+back)]]</TD>
  </TR>
</TABLE>
<HR WIDTH="90%" >
<TABLE CLASS="home fullsize" >

  <TR>
    <TD CLASS="strcol" WIDTH="30%" >Agency Status</TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="radio" NAME="ProviderControl_AgencyStatus_1" VALUE="1" <<ProviderControl_AgencyStatus_1=1>> > yes
      <INPUT TYPE="radio" NAME="ProviderControl_AgencyStatus_1" VALUE="0" <<ProviderControl_AgencyStatus_1=0>> > no
    </TD>
  </TR>

  <TR >
    <TD CLASS="strcol" WIDTH="30%" >Termination Date</TD>
    <TD CLASS="strcol" >
      <INPUT TYPE=text NAME="ProviderControl_TermDate_1" VALUE="<<ProviderControl_TermDate_1>>" ONFOCUS="select()" ONCHANGE="return vDate(this,1)" SIZE="10" >
    </TD>
  </TR>
  
  <TR > <TD CLASS="port hdrtxt" COLSPAN="3" ><B>Agency Information</B></TD> </TR>
  <TR>
    <TD CLASS="strcol" WIDTH="30%" >NoteEdit</TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="radio" NAME="ProviderControl_NoteEdit_1" VALUE=1 <<ProviderControl_NoteEdit_1=1>> > yes
      <INPUT TYPE="radio" NAME="ProviderControl_NoteEdit_1" VALUE=0 <<ProviderControl_NoteEdit_1=0>> > no
      <BR>Notes/TrPlans must be Signed by Provider/Manager
    </TD>
  </TR>
  <TR>
    <TD CLASS="strcol" WIDTH="30%" >Note Service Type</TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="radio" NAME="ProviderControl_NoteServiceType_1" VALUE=1 <<ProviderControl_NoteServiceType_1=1>> > yes
      <INPUT TYPE="radio" NAME="ProviderControl_NoteServiceType_1" VALUE=0 <<ProviderControl_NoteServiceType_1=0>> > no
      <BR>Use selection to narrow Notes/Treatments by Service Type
    </TD>
  </TR>
  <TR>
    <TD CLASS="strcol" WIDTH="30%" >Generate Invoices</TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="radio" NAME="ProviderControl_GenerateInvoices_1" VALUE=1 <<ProviderControl_GenerateInvoices_1=1>> > yes
      <INPUT TYPE="radio" NAME="ProviderControl_GenerateInvoices_1" VALUE=0 <<ProviderControl_GenerateInvoices_1=0>> > no
      <BR>Generate Invoices each week after Reconcile Remittances are done.
    </TD>
  </TR>
  <TR >
    <TD CLASS="strcol" WIDTH="30%" >Financial Manager</TD>
    <TD CLASS="strcol" >
      <SELECT NAME="ProviderControl_FinMgrID_1">[[DBA->selProviders(%form+<<ProviderControl_FinMgrID_1>>)]]</SELECT> 
      (as for Invoicing contact)
    </TD>
  </TR>
  <TR>
    <TD CLASS="strcol" WIDTH="30%" >Use BilledDate for Payroll</TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="radio" NAME="ProviderControl_PayrollByBillDate_1" VALUE=1 <<ProviderControl_PayrollByBillDate_1=1>> > yes
      <INPUT TYPE="radio" NAME="ProviderControl_PayrollByBillDate_1" VALUE=0 <<ProviderControl_PayrollByBillDate_1=0>> > no
      <BR>Payroll will be run on notes billed (BillDate) instead of reconciled (RecDate)
    </TD>
  </TR>
  <TR>
    <TD CLASS="strcol" WIDTH="30%" >Enable Billing</TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="radio" NAME="ProviderControl_EnableBill_1" VALUE=1 <<ProviderControl_EnableBill_1=1>> > yes
      <INPUT TYPE="radio" NAME="ProviderControl_EnableBill_1" VALUE=0 <<ProviderControl_EnableBill_1=0>> > no
      <BR>Enable Billing each Monday on site.
    </TD>
  </TR>
  <TR>
    <TD CLASS="strcol" WIDTH="30%" >Enable CDC</TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="radio" NAME="ProviderControl_EnableCDC_1" VALUE=1 <<ProviderControl_EnableCDC_1=1>> > yes
      <INPUT TYPE="radio" NAME="ProviderControl_EnableCDC_1" VALUE=0 <<ProviderControl_EnableCDC_1=0>> > no
      <BR>Enable sending of CDCs on site.
    </TD>
  </TR>
  <TR>
    <TD CLASS="strcol" WIDTH="30%" >Logout in Minutes</TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="text" NAME="ProviderControl_minToLogOut_1" VALUE="<<ProviderControl_minToLogOut_1>>" ONFOCUS="select()" ONCHANGE="return vNum(this,1,60);" MAXLENGTH="5" SIZE="5" > default minutes for user to be timed out and logged out.
    </TD>
  </TR>
  <TR>
    <TD CLASS="strcol" WIDTH="30%" >Agency LOGO</TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="submit" ONMOUSEOVER="window.status='upload button'; return true;" ONMOUSEOUT="window.status=''" NAME="view=LOGOUpload.cgi&Provider_ProvID=<<<Provider_ProvID_1>>>&pushID=<<<LINKID>>>" VALUE="upload" >
      <IMG SRC="<<ProviderControl_LOGO_1>>" BORDER=0>
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

<INPUT TYPE=hidden NAME="post_update" VALUE="DBA->updProvider(%form)" >
</LOADHIDDEN>
</FORM>
<SCRIPT LANGUAGE="JavaScript">
document.AgencyControl.elements[0].focus();
</SCRIPT>

[[myHTML->rightpane(%form+search)]]
