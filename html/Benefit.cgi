[[myHTML->newPage(%form+Provider Benefits)]]

<SCRIPT LANGUAGE="JavaScript" SRC="/src/cgi/js/NoEnter.js"> </SCRIPT>
<SCRIPT LANGUAGE="JavaScript" SRC="/src/cgi/js/vEntry.js"> </SCRIPT>
<SCRIPT LANGUAGE="JavaScript" SRC="/src/cgi/js/vBenefit.js"> </SCRIPT>
<SCRIPT LANGUAGE="JavaScript" SRC="/src/cgi/js/vNum.js"> </SCRIPT>

<FORM NAME="Benefit" ACTION="/src/cgi/bin/bin/bin/mis.cgi" METHOD="POST" >
<TABLE CLASS="main fullsize" >
  <TR >
    <TD CLASS="strcol" >
      <<<Provider_FName_1>>> <<<Provider_MName_1>>> <<<Provider_LName_1>>> 
      <BR>Benefit Information
    </TD>
    <TD CLASS="numcol" >[[gHTML->setLINKS(%form+back)]]</TD>
  </TR>
</TABLE>
<TABLE CLASS="home fullsize" >
  <TR >
    <TD CLASS="strcol" WIDTH="50%" >Type</TD>
    <TD CLASS="strcol" >
      <SELECT NAME="EmplInfo_Insurance_1">[[DBA->selProviderIns(%form+<<EmplInfo_Insurance_1>>)]]</SELECT>
    </TD>
  </TR>
  <TR >
    <TD CLASS="strcol" WIDTH="50%" >Threshold for 50% Employer Contribution to Individual Premium</TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="TEXT" NAME="EmplInfo_ThresInd50_1" VALUE="<<EmplInfo_ThresInd50_1>>" onFocus="select()" ONCHANGE="return vNum(this,0,40)" SIZE=10>
      IEs
    </TD>
  <TR >
    <TD CLASS="strcol" WIDTH="50%" >Threshold for 75% Employer Contribution to Individual Premium</TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="TEXT" NAME="EmplInfo_ThresInd75_1" VALUE="<<EmplInfo_ThresInd75_1>>" onFocus="select()" ONCHANGE="return vNum(this,0,50)" SIZE=10>
      IEs
    </TD>
  </TR>
  </TR>
  <TR >
    <TD CLASS="strcol" WIDTH="50%" >Threshold for 100% Employer Contribution to Individual Premium</TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="TEXT" NAME="EmplInfo_ThresInd100_1" VALUE="<<EmplInfo_ThresInd100_1>>" onFocus="select()" ONCHANGE="return vNum(this,0,50)" SIZE=10>
      IEs
    </TD>
  </TR>
  <TR >
    <TD CLASS="strcol" WIDTH="50%" >Threshold for 100% Employer Contribution to Entire Premium</TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="TEXT" NAME="EmplInfo_Thres100_1" VALUE="<<EmplInfo_Thres100_1>>" onFocus="select()" ONCHANGE="return vNum(this,0,50)" SIZE=10>
      IEs
    </TD>
  </TR>
</TABLE>
<TABLE CLASS="home fullsize" >
  <TR >
    <TD CLASS="strcol" WIDTH="20%" >Insurance Application</TD>
    <TD CLASS="strcol" >
      <INPUT TYPE=radio NAME="EmplInfo_InsApp_1" VALUE=1 <<EmplInfo_InsApp_1=1>> > Yes
      <INPUT TYPE=radio NAME="EmplInfo_InsApp_1" VALUE=0 <<EmplInfo_InsApp_1=0>> > No
      <INPUT TYPE=radio NAME="EmplInfo_InsApp_1" VALUE="N" <<EmplInfo_InsApp_1=N>> > N/A
    </TD>
  </TR>
  <TR >
    <TD CLASS="strcol" WIDTH="20%" >Cobra</TD>
    <TD CLASS="strcol" >
      <INPUT TYPE=radio NAME="EmplInfo_COBRA_1" VALUE=1 <<EmplInfo_COBRA_1=1>> > Yes
      <INPUT TYPE=radio NAME="EmplInfo_COBRA_1" VALUE=0 <<EmplInfo_COBRA_1=0>> > No
      <INPUT TYPE=radio NAME="EmplInfo_COBRA_1" VALUE="N" <<EmplInfo_COBRA_1=N>> > N/A
    </TD>
  </TR>
  <TR >
    <TD CLASS="strcol" WIDTH="20%" >401K</TD>
    <TD CLASS="strcol" >
      <INPUT TYPE=radio NAME="EmplInfo_401K_1" VALUE=1 <<EmplInfo_401K_1=1>> > Yes
      <INPUT TYPE=radio NAME="EmplInfo_401K_1" VALUE=0 <<EmplInfo_401K_1=0>> > No
      <INPUT TYPE=radio NAME="EmplInfo_401K_1" VALUE="N" <<EmplInfo_401K_1=N>> > N/A
    </TD>
  </TR>
  <TR >
    <TD CLASS="strcol" WIDTH="20%" >401K %</TD>
    <TD CLASS="strcol" >
      <INPUT TYPE=text NAME="EmplInfo_401Kpercent_1" VALUE="<<EmplInfo_401Kpercent_1>>" ONFOCUS="select()" ONCHANGE="vNum(this,1,100)" SIZE=10>
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
document.Benefit.elements[0].focus();
</SCRIPT>

[[myHTML->rightpane(%form+search)]]
