[[myHTML->newPage(%form+Client Hospital Information)]]

<SCRIPT LANGUAGE="JavaScript" SRC="/src/cgi/js/NoEnter.js"> </SCRIPT>
<SCRIPT LANGUAGE="JavaScript" SRC="/src/cgi/js/vEntry.js"> </SCRIPT>
<SCRIPT LANGUAGE="JavaScript" SRC="/src/cgi/js/vHospital.js"> </SCRIPT>
<SCRIPT type="text/javascript" src="/src/cgi/js/ajaxrequest.js"></SCRIPT>
<SCRIPT LANGUAGE="JavaScript" SRC="/src/cgi/js/qDate.js"> </SCRIPT>

<FORM NAME="Hospital" ACTION="/cgi/bin/mis.cgi" METHOD="POST" >
<TABLE CLASS="main fullsize" >
  <TR >
    <TD CLASS="strcol" >
      <<<Client_FName_1>>> <<<Client_MName_1>>> <<<Client_LName_1>>> (<<<Client_ClientID_1>>>) <<<Client_SSN_1>>>
      <BR>
      Treating Facility/Agency View/Edit Page
    </TD>
    <TD CLASS="numcol" >[[gHTML->setLINKS(%form+back)]]</TD>
  </TR>
</TABLE>
<TABLE CLASS="home fullsize" >
  <TR ><TD CLASS="port hdrtxt" COLSPAN="2" ><U>Treatments</U></TD></TR>
  <TR >
    <TD CLASS="strcol" WIDTH="30%" >Inpatient Hospital</TD>
    <TD CLASS="strcol" >
      Search: <INPUT TYPE="text" ID="SearchHosp" NAME="SearchHosp" VALUE="" ONFOCUS="select()" ONCHANGE="callAjax('Agency','<<Hospital_HospIDNPI_1>>','selHosp','&name=Hospital_HospIDNPI_1&pattern='+this.value,'popup.pl');" SIZE="60" >
<BR><SPAN ID="selHosp"></SPAN>
    </TD>
  </TR>
  <TR >
    <TD CLASS="strcol" WIDTH="30%" >Outpatient Facility</TD>
    <TD CLASS="strcol" >
      Search: <INPUT TYPE="text" ID="SearchFac" NAME="SearchFac" VALUE="" ONFOCUS="select()" ONCHANGE="callAjax('Agency','<<Hospital_FacIDNPI_1>>','selFac','&name=Hospital_FacIDNPI_1&pattern='+this.value,'popup.pl');" SIZE="60" >
<BR><SPAN ID="selFac"></SPAN>
    </TD>
  </TR>
  <TR >
    <TD CLASS="strcol" WIDTH="30%" >Type</TD>
    <TD CLASS="strcol" >
      <SELECT NAME="Hospital_Type_1">[[DBA->selxTable(%form+xHospType+<<Hospital_Type_1>>)]]</SELECT> 
    </TD>
  </TR>
  <TR >
    <TD CLASS="strcol" WIDTH="30%" >Intake Date</TD>
    <TD CLASS="strcol" >
      <INPUT TYPE=text NAME="Hospital_IntDate_1" VALUE="<<Hospital_IntDate_1>>" ONFOCUS="select()" ONCHANGE="return qDate(this)" SIZE=10>
      Use ?? for Month/Date, ???? for Year if unknown. (eg. 1999-04-??)
    </TD>
  </TR>
  <TR >
    <TD CLASS="strcol" WIDTH="30%" >Release Date</TD>
    <TD CLASS="strcol" >
      <INPUT TYPE=text NAME="Hospital_RelDate_1" VALUE="<<Hospital_RelDate_1>>" ONFOCUS="select()" ONCHANGE="return qDate(this)" SIZE=10>
    </TD>
  </TR>
  <TR >
    <TD CLASS="strcol" WIDTH="30%" >Length</TD>
    <TD CLASS="strcol" >
      <SELECT NAME="Hospital_Length_1">[[DBA->selxTable(%form+xPeriod+<<Hospital_Length_1>>)]]</SELECT> 
    </TD>
  </TR>
  <TR >
    <TD CLASS="strcol" WIDTH="30%" >Reason</TD>
    <TD CLASS="strcol" >
      <INPUT TYPE=text NAME="Hospital_Reason_1" VALUE="<<Hospital_Reason_1>>" SIZE=60> 
    </TD>
  </TR>
  <TR >
    <TD CLASS="strcol" WIDTH="30%" >Active</TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="radio" NAME="Hospital_Active_1" VALUE=1 <<Hospital_Active_1=1>> > yes
      <INPUT TYPE="radio" NAME="Hospital_Active_1" VALUE=0 <<Hospital_Active_1=0>> > no
    </TD>
  </TR>
</TABLE>
<TABLE CLASS="main fullsize" >
  <TR >
    <TD CLASS="numcol" >
      <INPUT TYPE="submit" ONCLICK="return vDELETE('Are you sure you want to delete this treatment?');" NAME="Hospital_DELETE_1=1&UpdateTables=all&misPOP=1" VALUE="Delete Treatment">
      <INPUT TYPE="submit" ONCLICK="return validate(this.form);" NAME="UpdateTables=all&misPOP=1" VALUE="Add/Update">
    </TD>
  </TR>
</TABLE>

</LOADHIDDEN>
</FORM>
<SCRIPT LANGUAGE="JavaScript">
document.Hospital.elements[0].focus();
callAjax('Agency','<<Hospital_HospIDNPI_1>>','selHosp','&name=Hospital_HospIDNPI_1','popup.pl');
callAjax('Agency','<<Hospital_FacIDNPI_1>>','selFac','&name=Hospital_FacIDNPI_1','popup.pl');
</SCRIPT>

[[myHTML->rightpane(%form+search)]]
