[[myHTML->newPage(%form+Client Opioid Registry)]]

<SCRIPT LANGUAGE="JavaScript" SRC="/src/cgi/js/NoEnter.js"> </SCRIPT>
<SCRIPT LANGUAGE="JavaScript" SRC="/src/cgi/js/vEntry.js"> </SCRIPT>
<SCRIPT LANGUAGE="JavaScript" SRC="/src/cgi/js/vDate.js"> </SCRIPT>

<FORM NAME="ClientOpioidRegistry" ACTION="/cgi/bin/mis.cgi" METHOD="POST" >
<TABLE CLASS="main fullsize" >
  <TR >
    <TD CLASS="strcol" >
      <<<Client_FName_1>>> <<<Client_MName_1>>> <<<Client_LName_1>>> (<<<Client_ClientID_1>>>) <<<Client_SSN_1>>>
      <BR>
      Opioid Registry View/Edit Page
    </TD>
    <TD CLASS="numcol" >[[gHTML->setLINKS(%form+back)]]</TD>
  </TR>
</TABLE>
<TABLE CLASS="home fullsize" >
  <TR >
    <TD CLASS="strcol" WIDTH=30% >Title</TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="TEXT" NAME="ClientOpioidRegistry_Title_1" VALUE="<<ClientOpioidRegistry_Title_1>>" ONFOCUS="select()" SIZE=35>
    </TD>
  </TR>
  <TR >
    <TD CLASS="strcol" WIDTH=30% >Description</TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="TEXT" NAME="ClientOpioidRegistry_Descr_1" VALUE="<<ClientOpioidRegistry_Descr_1>>" ONFOCUS="select()" SIZE=70>
    </TD>
  </TR>
  <TR >
    <TD CLASS="strcol" WIDTH=30% >Path</TD>
    <TD CLASS="strcol" >
      <<ClientOpioidRegistry_Path_1>>
    </TD>
  </TR>
</TABLE>
<TABLE CLASS="main fullsize" >
  <TR >
    <TD CLASS="numcol" >
      <INPUT TYPE="submit" ONCLICK="return vDELETE('Are you sure you want to delete this record?');" NAME="ClientOpioidRegistry_DELETE_1=1&UpdateTables=all&misPOP=1" VALUE="Delete">
      <INPUT TYPE="submit" ONCLICK="return validate(this.form);" NAME="UpdateTables=all&misPOP=1" VALUE="Add/Update">
    </TD>
  </TR>
</TABLE>

</LOADHIDDEN>
</FORM>
<SCRIPT LANGUAGE="JavaScript">
document.ClientOpioidRegistry.elements[0].focus();
// just to OPENTABLES...
//<<<ClientOpioidRegistry_ClientID_1>>>
</SCRIPT>

[[myHTML->rightpane(%form+search)]]
