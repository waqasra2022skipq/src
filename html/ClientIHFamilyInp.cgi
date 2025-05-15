[[myHTML->newPage(%form+Family Relations)]]

<SCRIPT LANGUAGE="JavaScript" SRC="/src/cgi/js/NoEnter.js"> </SCRIPT>
<SCRIPT LANGUAGE="JavaScript" SRC="/src/cgi/js/vEntry.js"> </SCRIPT>
<SCRIPT LANGUAGE="JavaScript" SRC="/src/cgi/js/vClientFamily.js"> </SCRIPT>
<SCRIPT LANGUAGE="JavaScript" SRC="/src/cgi/js/vNum.js"> </SCRIPT>
<SCRIPT LANGUAGE="JavaScript" SRC="/src/cgi/js/ajaxrequest.js"> </SCRIPT>
<SCRIPT TYPE="text/javascript" SRC="/cgi/jquery/jquery-ui-1.11.2/jquery-ui.min.js" ></SCRIPT>
<LINK HREF="/src/cgi/css/autocomplete.css?v=202008071708" REL="stylesheet">

<FORM NAME="ClientFamily" ACTION="/cgi/bin/mis.cgi" METHOD="POST" >
<TABLE CLASS="main fullsize" >
  <TR >
    <TD CLASS="strcol" >
      <<<Client_FName_1>>> <<<Client_MName_1>>> <<<Client_LName_1>>> (<<<Client_ClientID_1>>>) <<<Client_SSN_1>>>
      <BR>
      Family Relationship Members
    </TD>
    <TD CLASS="numcol" >[[gHTML->setLINKS(%form+back)]]</TD>
  </TR>
</TABLE>
<TABLE CLASS="home fullsize" >
    <TR ><TD CLASS="port hdrtxt" ><TABLE CLASS="home fullsize" >
  <TR ><TD CLASS="port hdrtxt" COLSPAN="2" >FAMILY MEMBER</TD></TR>
  <TR >
    <TD CLASS="strcol" >First Name</TD>
    <TD CLASS="strcol" >
      <INPUT TYPE=text NAME="ClientFamily_FName_1" VALUE="<<ClientFamily_FName_1>>" ONFOCUS="select()" SIZE=20>
    </TD>
  </TR>
  <TR >
    <TD CLASS="strcol" >Last Name</TD>
    <TD CLASS="strcol" >
      <INPUT TYPE=text NAME="ClientFamily_LName_1" VALUE="<<ClientFamily_LName_1>>" ONFOCUS="select()" SIZE=20>
    </TD>
  </TR>
  <TR >
    <TD CLASS="strcol" >Age</TD>
    <TD CLASS="strcol" >
      <INPUT TYPE=text NAME="ClientFamily_Age_1" VALUE="<<ClientFamily_Age_1>>" ONCHANGE="return vNum(this,1,99)" ONFOCUS="select()" >
    </TD>
  </TR>
  <TR >
    <TD CLASS="strcol" >Relationship</TD>
    <TD CLASS="strcol" >
      <INPUT ID="MCAutocomplete" TYPE="text" VALUE="[[DBA->getxref(%form+xRelationship+<<<ClientFamily_Rel_1>>>)]]" ONFOCUS="select()" SIZE="20" />
      <INPUT TYPE="hidden" NAME="ClientFamily_Rel_1" VALUE="<<ClientFamily_Rel_1>>" >
    </TD>
  </TR>
  <TR >
    <TD CLASS="strcol" >Living Inhome</TD>
    <TD CLASS="strcol" >
      <INPUT TYPE=radio NAME="ClientFamily_Inhome_1" VALUE=1 <<ClientFamily_Inhome_1=1>> > yes
      <INPUT TYPE=radio NAME="ClientFamily_Inhome_1" VALUE=0 <<ClientFamily_Inhome_1=0>> > no
    </TD>
  </TR>
  <TR >
    <TD CLASS="strcol" >Relationship value</TD>
    <TD CLASS="strcol" >
      <INPUT TYPE=text NAME="ClientFamily_RelValue_1" VALUE="<<ClientFamily_RelValue_1>>" ONCHANGE="return vNum(this,1,10)" ONFOCUS="select()" > 
      (1=bad, 10=excellent)
    </TD>
  </TR>
  <TR >
    <TD CLASS="strcol" >Relationship value description</TD>
    <TD CLASS="strcol" >
      <INPUT TYPE=text NAME="ClientFamily_RelValueDesc_1" VALUE="<<ClientFamily_RelValueDesc_1>>" ONFOCUS="select()" SIZE=60>
    </TD>
  </TR>
    </TABLE></TD></TR>
</TABLE>
<TABLE CLASS="main fullsize" >
  <TR >
    <TD CLASS="numcol" >
      <INPUT TYPE="submit" ONCLICK="return vDELETE('Are you sure you want to delete this family member, will delete all associations for SA-DV-Relations?');" NAME="ClientFamily_DELETE_1=1&UpdateTables=all&misPOP=1" VALUE="Delete">
      <INPUT TYPE="submit" ONCLICK="return validate(this.form);" NAME="UpdateTables=all&misPOP=1" VALUE="Add/Update">
    </TD>
  </TR>
</TABLE>

</LOADHIDDEN>
</FORM>
<SCRIPT LANGUAGE="JavaScript">
document.ClientFamily.elements[0].focus();
</SCRIPT>

[[myHTML->rightpane(%form+search)]]

<SCRIPT type="text/javascript" src="/src/cgi/js/vMCAutocomplete.js?v=202006082124"></SCRIPT>
<SCRIPT LANGUAGE="JavaScript" >
callAjax('xRelationship','','','&Autocomplete=MCAutocomplete&Target=ClientFamily_Rel_1','popup.pl');
</SCRIPT>
