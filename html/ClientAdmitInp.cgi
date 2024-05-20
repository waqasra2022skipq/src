[[myHTML->newPage(%form+Client Admissions)]]

<SCRIPT LANGUAGE="JavaScript" SRC="/cgi/js/vEntry.js"> </SCRIPT>
<SCRIPT LANGUAGE="JavaScript" SRC="/cgi/js/vClientAdmit.js"> </SCRIPT>
<SCRIPT LANGUAGE="JavaScript" SRC="/cgi/js/vDate.js"> </SCRIPT>
<SCRIPT LANGUAGE="JavaScript" SRC="/cgi/js/vTime.js"> </SCRIPT>

<FORM NAME="Admit" ACTION="/cgi/bin/mis.cgi" METHOD="POST" >
<TABLE CLASS="main fullsize" >
  <TR >
    <TD CLASS="strcol" >
      <<<Client_FName_1>>> <<<Client_MName_1>>> <<<Client_LName_1>>> (<<<Client_ClientID_1>>>) <<<Client_SSN_1>>>
      <BR>Admit Page
    </TD>
    <TD CLASS="numcol" >[[gHTML->setLINKS(%form+back)]]</TD>
  </TR>
</TABLE>
<TABLE CLASS="home fullsize" >
  <TR >
    <TD CLASS="port hdrtxt" COLSPAN="2" >
      ADMIT<BR>Intake
    </TD>
  </TR>
  <TR >
    <TD CLASS="strcol" WIDTH=30% >Intake Date</TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="text" NAME="ClientAdmit_AdmitDate_1" VALUE="<<ClientAdmit_AdmitDate_1>>" ONFOCUS="select()" ONCHANGE="return vDate(this);" SIZE="10" >
    </TD>
  </TR>
  <TR >
    <TD CLASS="strcol" WIDTH=30% >Intake Time</TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="text" NAME="ClientAdmit_AdmitTime_1" VALUE="<<ClientAdmit_AdmitTime_1>>" ONFOCUS="select()" ONCHANGE="return vTime(this,1,this,'07:00:00','19:00:00');" SIZE="15" >
    </TD>
  </TR>
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
document.Admit.elements[0].focus();
</SCRIPT>

[[myHTML->rightpane(%form+search)]]
