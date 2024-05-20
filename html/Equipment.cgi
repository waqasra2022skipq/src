[[myHTML->newPage(%form+Equipment)]]

<SCRIPT LANGUAGE="JavaScript" SRC="/cgi/js/NoEnter.js"> </SCRIPT>
<SCRIPT LANGUAGE="JavaScript" SRC="/cgi/js/vEntry.js"> </SCRIPT>
<SCRIPT LANGUAGE="JavaScript" SRC="/cgi/js/vEquipment.js"> </SCRIPT>
<SCRIPT LANGUAGE="JavaScript" SRC="/cgi/js/vDate.js"> </SCRIPT>

<FORM NAME="Equipment" ACTION="/cgi/bin/mis.cgi" METHOD="POST" >
<TABLE CLASS="main fullsize" >
  <TR >
    <TD CLASS="strcol" >
      <<<Provider_FName_1>>> <<<Provider_MName_1>>> <<<Provider_LName_1>>> 
      <BR>Edit/View Equipment
    </TD>
    <TD CLASS="numcol" >[[gHTML->setLINKS(%form+back)]]</TD>
  </TR>
</TABLE>
<TABLE CLASS="home fullsize" >
  <TR >
    <TD CLASS="strcol" WIDTH="30%" >Description</TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="TEXT" NAME="Equipment_Descr_1" VALUE="<<Equipment_Descr_1>>" SIZE=80 > 
    </TD>
  </TR>
  <TR >
    <TD CLASS="strcol" WIDTH="30%" >Manufacturer</TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="TEXT" NAME="Equipment_Manufacturer_1" VALUE="<<Equipment_Manufacturer_1>>" SIZE=80 > 
    </TD>
  </TR>
  <TR >
    <TD CLASS="strcol" WIDTH="30%" >Make</TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="TEXT" NAME="Equipment_Make_1" VALUE="<<Equipment_Make_1>>" SIZE=30 > 
    </TD>
  </TR>
  <TR >
    <TD CLASS="strcol" WIDTH="30%" >Model</TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="TEXT" NAME="Equipment_Model_1" VALUE="<<Equipment_Model_1>>" ONFOCUS="select()" SIZE=30 >
    </TD>
  </TR>
  <TR >
    <TD CLASS="strcol" WIDTH="30%" >Serial #</TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="TEXT" NAME="Equipment_Serial_1" VALUE="<<Equipment_Serial_1>>" ONFOCUS="select()" SIZE=30 > 
    </TD>
  </TR>
  <TR >
    <TD CLASS="strcol" WIDTH="30%" >Date Out</TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="TEXT" NAME="Equipment_OutDate_1" VALUE="<<Equipment_OutDate_1>>" ONFOCUS="select()" ONCHANGE="return vDate(this)" SIZE=10 > 
    </TD>
  </TR>
  <TR >
    <TD CLASS="strcol" WIDTH="30%" >Date In</TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="TEXT" NAME="Equipment_InDate_1" VALUE="<<Equipment_InDate_1>>" ONFOCUS="select()" ONCHANGE="return vDate(this)" SIZE=10 > 
    </TD>
  </TR>
  <TR >
    <TD CLASS="strcol" WIDTH="30%" >Comments</TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="TEXT" NAME="Equipment_Comments_1" VALUE="<<Equipment_Comments_1>>" ONFOCUS="select()" SIZE=80 > 
    </TD>
  </TR>
</TABLE>
<TABLE CLASS="main fullsize" >
  <TR>
    <TD CLASS="numcol" >
      <INPUT TYPE="submit" ONCLICK="return vDELETE('Are you sure you want to delete this record?');" NAME="Equipment_DELETE_1=1&UpdateTables=all&misPOP=1" VALUE="Delete">
      <INPUT TYPE="submit" ONCLICK="return validate(this.form);" NAME="UpdateTables=all&misPOP=1" VALUE="Add/Update">
    </TD>
  </TR>
</TABLE>

</LOADHIDDEN>
</FORM>
<SCRIPT LANGUAGE="JavaScript">
document.Equipment.elements[0].focus();
</SCRIPT>

[[myHTML->rightpane(%form+search)]]
