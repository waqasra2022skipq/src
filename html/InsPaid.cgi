[[myHTML->newPage(%form+Insurance Payment)]]

<SCRIPT LANGUAGE="JavaScript" SRC="/cgi/js/vEntry.js"> </SCRIPT>
<SCRIPT LANGUAGE="JavaScript" SRC="/cgi/js/vInsPaid.js"> </SCRIPT>
<SCRIPT LANGUAGE="JavaScript" SRC="/cgi/js/vDate.js"> </SCRIPT>
<SCRIPT LANGUAGE="JavaScript" SRC="/cgi/js/vNum.js"> </SCRIPT>

[[*SysAccess->verify(%form+Privilege=CashTrans)]]

<FORM NAME="InsPaid" ACTION="/cgi/bin/mis.cgi" METHOD="POST" >
<TABLE CLASS="main fullsize" >
  <TR >
    <TD CLASS="strcol" >
      <<<Client_FName_1>>> <<<Client_MName_1>>> <<<Client_LName_1>>> (<<<Client_ClientID_1>>>) <<<Client_SSN_1>>>
      <BR>
      Client Paid View/Edit Page
    </TD>
    <TD CLASS="numcol" >[[gHTML->setLINKS(%form+back)]]</TD>
  </TR>
</TABLE>
<TABLE CLASS="home fullsize" >
    <TR ><TD CLASS="port hdrtxt" ><TABLE CLASS="home fullsize" >
  <TR>
    <TD CLASS="strcol" >Type</TD>
    <TD CLASS="strcol" >
      <SELECT NAME="InsPaid_Type_1" >
        [[DBA->selxTable(%form+xInsPaidTypes+<<InsPaid_Type_1>>+ID)]]
      </SELECT> 
    </TD>
  </TR>
  <TR>
    <TD CLASS="strcol" >Reference</TD>
    <TD CLASS="strcol" >
      <SELECT NAME="InsPaid_RefID_1" >[[DBA->selxTable(%form+xInsPaidRefIDs+<<InsPaid_RefID_1>>)]]<SELECT>
    </TD>
  </TR>
  <TR>
    <TD CLASS="strcol" >Transaction Date</TD>
    <TD CLASS="strcol" >
       <INPUT TYPE="text" NAME="InsPaid_TransDate_1" VALUE="<<InsPaid_TransDate_1>>" ONFOCUS="select()" ONCHANGE="return vDate(this,1);" SIZE="12" >
    </TD>
  </TR>
  <TR>
    <TD CLASS="strcol" >Amount $</TD>
    <TD CLASS="strcol" >
       <INPUT TYPE="text" NAME="InsPaid_PaidAmt_1" VALUE="<<InsPaid_PaidAmt_1>>" ONFOCUS="select()" ONCHANGE="return vNum(this,-3000,3000);" SIZE="12" >
    </TD>
  </TR>
  <TR>
    <TD CLASS="strcol" >Check #</TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="text" NAME="InsPaid_ICN_1" VALUE="<<InsPaid_ICN_1>>" ONFOCUS="select()" ONCHANGE="return vNum(this,0,999999999);" SIZE="12">
      (please enter for check or money orders)
    </TD>
  </TR>
  <TR>
    <TD CLASS="strcol" >Reconciled Amount</TD>
    <TD CLASS="strcol" >$ <<<InsPaid_RecAmt_1>>></TD>
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
document.InsPaid.elements[0].focus();
</SCRIPT>
[[myHTML->rightpane(%form+search)]]
