[[myHTML->newPage(%form+Prior Authorization)]]

<SCRIPT LANGUAGE="JavaScript" SRC="/src/cgi/js/chkLock.js"> </SCRIPT>
<SCRIPT LANGUAGE="JavaScript" SRC="/src/cgi/js/vEntry.js"> </SCRIPT>
<SCRIPT LANGUAGE="JavaScript" SRC="/src/cgi/js/vPrAuth.js"> </SCRIPT>
<SCRIPT LANGUAGE="JavaScript" SRC="/src/cgi/js/Utils.js"> </SCRIPT>
<SCRIPT LANGUAGE="JavaScript" SRC="/src/cgi/js/vDate.js"> </SCRIPT>
<SCRIPT LANGUAGE="JavaScript" SRC="/src/cgi/js/mDate.js"> </SCRIPT>
<SCRIPT LANGUAGE="JavaScript" SRC="/src/cgi/js/vTime.js"> </SCRIPT>
<SCRIPT LANGUAGE="JavaScript" SRC="/src/cgi/js/vNum.js"> </SCRIPT>
<script type="text/javascript" src="/src/cgi/js/ajaxrequest.js"></script>

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
  <TR >
    <TD CLASS="numcol" >Entered By:</TD>
    <TD CLASS="strcol" >
      [[DBA->getxref(%form+Provider+<<<ClientPrAuth_CreateProvID_1>>>+FName LName)]] &nbsp;
    </TD>
  </TR>
  <TR >
    <TD CLASS="numcol" >Date:</TD>
    <TD CLASS="strcol" >
      <<<ClientPrAuth_CreateDate_1>>>&nbsp;
    </TD>
  </TR>
  <TR >
    <TD CLASS="strcol" >Type:</TD>
    <TD CLASS="strcol" >
      <SELECT NAME="ClientPrAuth_Type_1" >
        [[DBA->selxTable(%form+xPrAuthType+<<ClientPrAuth_Type_1>>+Descr)]]
      </SELECT> 
    </TD>
  </TR>
  <TR >
    <TD CLASS="strcol" >Transaction Type:</TD>
    <TD CLASS="strcol" >
      <SELECT ID="TransType" NAME="ClientPrAuthCDC_TransType_1" ONCHANGE="callAjax('calcPG',this.value,this.id,'&c=<<<Client_ClientID_1>>>&i=<<<Insurance_InsID_1>>>&p=<<<ClientPrAuth_ID_1>>>&d='+document.ClientPrAuth.ClientPrAuth_EffDate_1.value);" >
        [[DBA->selTransType(%form+<<<ClientPrAuth_ClientID_1>>>+<<ClientPrAuthCDC_TransType_1>>)]]
      </SELECT>
      <A HREF="http://forms.okmis.com/misdocs/CDCTT.html" TARGET="popup" ONCLICK="window.open('http://forms.okmis.com/misdocs/CDCTT.html', 'popup', 'width=900,height=700,menubar=1,scrollbars=1,toolbar=1,status=1,resizable=1'); return false">explain</A> 
    </TD>
  </TR>
  <TR > <TD CLASS="strcol hotmsg" COLSPAN="2" >Date must be a past date before today or today. Make sure it is the same as or before the Effective Date.</TD></TR>
  <TR >
    <TD CLASS="strcol" WIDTH=40% >Transaction/Contact Date:</TD>
    <TD CLASS="strcol" >
      <INPUT TYPE=text NAME="ClientPrAuthCDC_TransDate_1" VALUE="<<ClientPrAuthCDC_TransDate_1>>" ONFOCUS="select();" ONCHANGE="return vDate(this,0,this.form,'','',<<TODAY>>)" MAXLENGTH="10" SIZE="12" >
      <A HREF="http://forms.okmis.com/misdocs/CDCTT.html" TARGET="popup" ONCLICK="window.open('http://forms.okmis.com/misdocs/CDCTD.html', 'popup', 'width=900,height=700,menubar=1,scrollbars=1,toolbar=1,status=1,resizable=1'); return false">explain</A> 
    </TD>
  </TR>
  <TR >
    <TD CLASS="strcol" WIDTH=40% >Transaction/Contact Time:</TD>
    <TD CLASS="strcol" >
      <INPUT TYPE=text NAME="ClientPrAuthCDC_TransTime_1" VALUE="<<ClientPrAuthCDC_TransTime_1>>" ONFOCUS="select();" ONCHANGE="return vTime(this,1,this)" MAXLENGTH="10" SIZE="12" >
    </TD>
  </TR>
  <TR > <TD CLASS="strcol hotmsg" COLSPAN="2" >Date must be today or a date in the future.</TD></TR>
  <TR >
    <TD CLASS="strcol" >Effective Date:</TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="TEXT" ID="EffDate" NAME="ClientPrAuth_EffDate_1" VALUE="<<ClientPrAuth_EffDate_1>>" ONFOCUS="select();" ONCHANGE="vDate(this,0,this.form,'',<<TODAY>>); callAjax('calcPG',this.value,this.id,'&c=<<<Client_ClientID_1>>>&i=<<<Insurance_InsID_1>>>&p=<<<ClientPrAuth_ID_1>>>&t='+document.ClientPrAuth.ClientPrAuthCDC_TransType_1.value);" MAXLENGTH="10" SIZE="12" >
    </TD>
  </TR>
  <TR >
    <TD CLASS="port subtitle" >
      Expiration Date / Length / Treatment Level / Code
    </TD>
    <TD CLASS="strcol subtitle" >
      [[gHTML->ifld(%form+ClientPrAuth_ExpDate_1+displayonly)]]
      /
      [[gHTML->ifld(%form+ClientPrAuth_LOS_1+displayonly)]]
      /
      [[gHTML->ifld(%form+ClientPrAuth_TL_1+displayonly)]]
      /
      [[gHTML->ifld(%form+ClientPrAuth_PAgroup_1+displayonly)]]
      [[DBUtil->isNULL(<<<ClientPrAuth_ID_1>>>)(recalculated from CAR scores and Diagnosis)]]
      <A HREF="http://forms.okmis.com/misdocs/CDCTT.html" TARGET="popup" ONCLICK="window.open('http://forms.okmis.com/misdocs/CDCPG.html', 'popup', 'width=900,height=700,menubar=1,scrollbars=1,toolbar=1,status=1,resizable=1'); return false">explain</A> 
    </TD>
  </TR>
  <TR >
    <TD CLASS="port subtitle" >
      Status / Date / Authorization Number
    </TD>
    <TD CLASS="strcol subtitle" >
      [[gHTML->ifld(%form+ClientPrAuthCDC_Status_1+displayonly)]]
      /
      [[gHTML->ifld(%form+ClientPrAuthCDC_StatusDate_1+displayonly)]]
      /
      [[gHTML->ifld(%form+ClientPrAuth_PAnumber_1+displayonly)]]
    </TD>
  </TR>
  <TR ><TD CLASS="port hdrtxt" COLSPAN="2" ><B>Comments</B></TD></TR>
  <TR >
    <TD CLASS="strcol" WIDTH="25%" >Requesting Comments</TD>
    <TD CLASS="strcol" >
      <TEXTAREA NAME="ClientPrAuth_ReqComments_1" COLS=70 ROWS=5 WRAP=virtual ONFOCUS="select();" ><<ClientPrAuth_ReqComments_1>></TEXTAREA>
    </TD>
  </TR>
  <TR >
    <TD CLASS="strcol" WIDTH="25%" >Other/Additional Comments</TD>
    <TD CLASS="strcol" >
      <TEXTAREA NAME="ClientPrAuth_OthComments_1" COLS=70 ROWS=5 WRAP=virtual ONFOCUS="select();" ><<ClientPrAuth_OthComments_1>></TEXTAREA>
    </TD>
  </TR>
</TABLE>
<TABLE CLASS="main fullsize" >
  <TR>
    <TD CLASS="numcol" >
[[myTables->htmLocked(%form+<<<ClientPrAuth_Locked_1>>>+ClientPrAuth)]]
    </TD>
  </TR>
</TABLE>

<INPUT TYPE="hidden" NAME="post_update" VALUE="PostUpd->updPrAuth(%form+<<<ClientPrAuth_ID_1>>>)" >
</LOADHIDDEN>
</FORM>
<SCRIPT LANGUAGE="JavaScript">
document.ClientPrAuth.elements[0].focus();
</SCRIPT>

[[myHTML->rightpane(%form+search)]]
