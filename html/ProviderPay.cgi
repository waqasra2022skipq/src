[[myHTML->newPage(%form+Provider Pay)]]

<SCRIPT LANGUAGE="JavaScript" SRC="/src/cgi/js/NoEnter.js"> </SCRIPT>
<SCRIPT LANGUAGE="JavaScript" SRC="/src/cgi/js/vEntry.js"> </SCRIPT>
<SCRIPT LANGUAGE="JavaScript" SRC="/src/cgi/js/vProviderPay.js"> </SCRIPT>
<SCRIPT LANGUAGE="JavaScript" SRC="/src/cgi/js/vNum.js"> </SCRIPT>
<SCRIPT LANGUAGE="JavaScript" SRC="/src/cgi/js/vDate.js"> </SCRIPT>

[[*SysAccess->verify(%form+Privilege=ProviderPay)]]

<FORM NAME="ProviderPay" ACTION="/src/cgi/bin/mis.cgi" METHOD="POST" >
<TABLE CLASS="main fullsize" >
  <TR >
    <TD CLASS="strcol" >
      <<<Provider_FName_1>>> <<<Provider_MName_1>>> <<<Provider_LName_1>>> 
      <BR>Edit/View Pay Rate
    </TD>
    <TD CLASS="numcol" >[[gHTML->setLINKS(%form+back)]]</TD>
  </TR>
</TABLE>
<TABLE CLASS="home fullsize" >
  <TR >
    <TD CLASS="strcol" WIDTH="30%" >Manager/Rate</TD>
    <TD CLASS="strcol" >
      <SELECT NAME="ProviderPay_MgrID_1" >[[DBA->selPayMgrIDs(%form+<<ProviderPay_MgrID_1>>)]]</SELECT>
    </TD>
  </TR>
  <TR >
    <TD CLASS="strcol" WIDTH="30%" >Rate</TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="TEXT" NAME="ProviderPay_Rate_1" VALUE="<<ProviderPay_Rate_1>>" ONFOCUS="select()" ONCHANGE="return vNum(this,0,200000);" SIZE=20 >
    </TD>
  </TR>
  <TR >
    <TD CLASS="strcol" WIDTH="30%" >Type</TD>
    <TD CLASS="strcol" >
      <SELECT NAME="ProviderPay_Type_1" >[[DBA->selxTable(%form+xPayType+<<ProviderPay_Type_1>>)]]</SELECT>
    </TD>
  </TR>
  <TR >
    <TD CLASS="strcol" WIDTH="30%" >Commission</TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="TEXT" NAME="ProviderPay_Commission_1" VALUE="<<ProviderPay_Commission_1>>" ONFOCUS="select()" ONCHANGE="return vNum(this,0,100);" SIZE=10 > %  (i.e. 10.00%)
    </TD>
  </TR>
  <TR >
    <TD CLASS="strcol" WIDTH="30%" >Service Code</TD>
    <TD CLASS="strcol" >
      <SELECT NAME="ProviderPay_SCID_1" >
        [[DBA->selServiceCodes(%form+<<ProviderPay_SCID_1>>+0+++INSID=ALL)]]
      </SELECT> 
    </TD>
  </TR>
  <TR>
    <TD CLASS="strcol" WIDTH="30%" >Use as Manager for others</TD>
    <TD CLASS="strcol" >
      <INPUT TYPE=radio NAME="ProviderPay_isMgr_1" VALUE=1 <<ProviderPay_isMgr_1=1>> > yes
      <INPUT TYPE=radio NAME="ProviderPay_isMgr_1" VALUE=0 <<ProviderPay_isMgr_1=0>> > no
    </TD>
  </TR>
  <TR >
    <TD CLASS="strcol" WIDTH="30%" >Effective Date</TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="TEXT" NAME="ProviderPay_EffDate_1" VALUE="<<ProviderPay_EffDate_1>>" onFocus="select()" ONCHANGE="return vDate(this)" SIZE=12 > 
    </TD>
  </TR>
  <TR >
    <TD CLASS="strcol" WIDTH="30%" >Expiration Date</TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="TEXT" NAME="ProviderPay_ExpDate_1" VALUE="<<ProviderPay_ExpDate_1>>" onFocus="select()" ONCHANGE="return vDate(this,1)" SIZE=12 > 
    </TD>
  </TR>
</TABLE>
<TABLE CLASS="main fullsize" >
  <TR>
    <TD CLASS="numcol" >
      <INPUT TYPE="submit" ONCLICK="return vDELETE('Are you sure you want to delete this record?');" NAME="ProviderPay_DELETE_1=1&UpdateTables=all&misPOP=1" VALUE="Delete">
      <INPUT TYPE="submit" ONCLICK="return validate(this.form);" NAME="UpdateTables=all&misPOP=1" VALUE="Add/Update">
    </TD>
  </TR>
</TABLE>

</LOADHIDDEN>
</FORM>
<SCRIPT LANGUAGE="JavaScript">
document.ProviderPay.elements[0].focus();
</SCRIPT>

[[myHTML->rightpane(%form+search)]]
