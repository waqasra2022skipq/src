[[myHTML->newPage(%form+Available Insurance)]]

<SCRIPT LANGUAGE="JavaScript" SRC="/cgi/js/vEntry.js"> </SCRIPT>
<SCRIPT LANGUAGE="JavaScript" SRC="/cgi/js/vProviderIns.js"> </SCRIPT>
<SCRIPT LANGUAGE="JavaScript" SRC="/cgi/js/vNum.js"> </SCRIPT>

<FORM NAME="ProviderIns" ACTION="/cgi/bin/mis.cgi" METHOD="POST" >
<TABLE CLASS="main fullsize" >
  <TR >
    <TD CLASS="strcol" >
      <<<Provider_FName_1>>> <<<Provider_MName_1>>> <<<Provider_LName_1>>> 
      Provider Insurance Information
    </TD>
    <TD CLASS="numcol" >[[gHTML->setLINKS(%form+back)]]</TD>
  </TR>
</TABLE>
<TABLE CLASS="home fullsize" >
    <TR ><TD CLASS="port hdrtxt" ><TABLE CLASS="home fullsize" >
  <TR>
    <TD CLASS="strcol" WIDTH="15%" >Description</TD>
    <TD CLASS="strcol" >
       <INPUT TYPE="text" NAME="ProviderIns_Descr_1" VALUE="<<ProviderIns_Descr_1>>" ONFOCUS="select()" SIZE=60>
    </TD>
  </TR>
  <TR>
    <TD CLASS="strcol" WIDTH="15%" >Type</TD>
    <TD CLASS="strcol" >
       <INPUT TYPE="text" NAME="ProviderIns_Type_1" VALUE="<<ProviderIns_Type_1>>" ONFOCUS="select()" SIZE=20>
    </TD>
  </TR>
  <TR>
    <TD CLASS="strcol" WIDTH="15%" >Premium</TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="TEXT" NAME="ProviderIns_Premium_1" VALUE="<<ProviderIns_Premium_1>>" ONFOCUS="select()" SIZE=20 ONCHANGE="return vNum(this,0,4000)" >
    </TD>
  </TR>
  <TR>
    <TD CLASS="strcol" WIDTH="15%" >BaseCost</TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="TEXT" NAME="ProviderIns_BaseCost_1" VALUE="<<ProviderIns_BaseCost_1>>" ONFOCUS="select()" SIZE=20 ONCHANGE="return vNum(this,0,4000)" >
    </TD>
  </TR>
  <TR >
    <TD CLASS="strcol" WIDTH="15%" >Active</TD>
    <TD CLASS="strcol" >
      <INPUT TYPE=radio NAME="ProviderIns_Active_1" VALUE="1" <<ProviderIns_Active_1=1>> > yes
      <INPUT TYPE=radio NAME="ProviderIns_Active_1" VALUE="0" <<ProviderIns_Active_1=0>> > no
    </TD>
  </TR>
    </TABLE></TD></TR>
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
document.ProviderIns.elements[0].focus();
</SCRIPT>
[[myHTML->rightpane(%form+search)]]
