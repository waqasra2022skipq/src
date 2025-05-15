[[myHTML->newPage(%form+Client SA)]]

<SCRIPT LANGUAGE="JavaScript" SRC="/src/cgi/js/NoEnter.js"> </SCRIPT>
<SCRIPT LANGUAGE="JavaScript" SRC="/src/cgi/js/vEntry.js"> </SCRIPT>
<SCRIPT LANGUAGE="JavaScript" SRC="/src/cgi/js/vSAbuse.js"> </SCRIPT>
<SCRIPT LANGUAGE="JavaScript" SRC="/src/cgi/js/vDate.js"> </SCRIPT>
<SCRIPT LANGUAGE="JavaScript" SRC="/src/cgi/js/vNum.js"> </SCRIPT>

<FORM NAME="SAbuse" ACTION="/cgi/bin/mis.cgi" METHOD="POST" >
<TABLE CLASS="main fullsize" >
  <TR >
    <TD CLASS="strcol" >
      <<<Client_FName_1>>> <<<Client_MName_1>>> <<<Client_LName_1>>> (<<<Client_ClientID_1>>>) <<<Client_SSN_1>>>
      <BR>
      Substance Abuse View/Edit Page
    </TD>
    <TD CLASS="numcol" >[[gHTML->setLINKS(%form+back)]]</TD>
  </TR>
</TABLE>
<TABLE CLASS="home fullsize" >
  <TR ><TD CLASS="port hdrtxt" COLSPAN="2" >SUBSTANCE ABUSE<BR>information</TD></TR>
  <TR >
    <TD CLASS="strcol" >Drug</TD>
    <TD CLASS="strcol" >
      <SELECT NAME="SAbuse_Drug_1">
        [[DBA->selxTable(%form+xDrugs+<<SAbuse_Drug_1>>+Descr CDC)]]
      </SELECT>
    </TD>
  </TR>
  <TR >
    <TD CLASS="strcol" >Method of use</TD>
    <TD CLASS="strcol" >
      <SELECT NAME="SAbuse_Method_1" >[[DBA->selxTable(%form+xMethods+<<SAbuse_Method_1>>)]]</SELECT>
    </TD>
  </TR>
  <TR >
    <TD CLASS="strcol" >Amount</TD>
    <TD CLASS="strcol" >
      <SELECT NAME="SAbuse_Amount_1" >
        [[DBA->selxTable(%form+xAbuseAmt+<<SAbuse_Amount_1>>+Descr)]]
      </SELECT>
    </TD>
  </TR>
  <TR >
    <TD CLASS="strcol" >Frequency</TD>
    <TD CLASS="strcol" >
      <SELECT NAME="SAbuse_Freq_1" >[[DBA->selxTable(%form+xFreqs+<<SAbuse_Freq_1>>)]]</SELECT>
    </TD>
  </TR>
  <TR >
    <TD CLASS="strcol" >Date First Used</TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="TEXT" NAME="SAbuse_FromDate_1" VALUE="<<SAbuse_FromDate_1>>" ONFOCUS="select()" ONCHANGE="return vDate(this)" MAXLENGTH="10" SIZE=10>
    </TD>
  </TR>
  <TR >
    <TD CLASS="strcol" >Date Last Used</TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="TEXT" NAME="SAbuse_ToDate_1" VALUE="<<SAbuse_ToDate_1>>" ONFOCUS="select()" ONCHANGE="return vDate(this)" MAXLENGTH="10" SIZE=10>
    </TD>
  </TR>
  <TR >
    <TD CLASS="strcol" >Age of first use</TD>
    <TD CLASS="strcol" >
      <INPUT TYPE=text NAME="SAbuse_Age_1" VALUE="<<SAbuse_Age_1>>" ONFOCUS="select()" ONCHANGE="return vNum(this,1,99)" >
    </TD>
  </TR>
  <TR >
    <TD CLASS="strcol" >Age of first regular use</TD>
    <TD CLASS="strcol" >
      <INPUT TYPE=text NAME="SAbuse_AgeReg_1" VALUE="<<SAbuse_AgeReg_1>>" ONFOCUS="select()" ONCHANGE="return vNum(this,1,99)" >
      (3 or more times per week)
    </TD>
  </TR>
  <TR >
    <TD CLASS="strcol" >Drug of Choice</TD>
    <TD CLASS="strcol" >
      <SELECT NAME="SAbuse_Priority_1" >[[DBA->selxTable(%form+xPriority+<<SAbuse_Priority_1>>)]]</SELECT> 
    </TD>
  </TR>
</TABLE>
<TABLE CLASS="main fullsize" >
  <TR >
    <TD CLASS="numcol" >
      <INPUT TYPE="submit" ONCLICK="return vDELETE('Are you sure you want to delete this record?');" NAME="SAbuse_DELETE_1=1&UpdateTables=all&misPOP=1" VALUE="Delete">
      <INPUT TYPE="submit" ONCLICK="return validate(this.form);" NAME="UpdateTables=all&misPOP=1" VALUE="Add/Update">
    </TD>
  </TR>
</TABLE>

</LOADHIDDEN>
</FORM>
<SCRIPT LANGUAGE="JavaScript">
document.SAbuse.elements[0].focus();
</SCRIPT>

[[myHTML->rightpane(%form+search)]]
