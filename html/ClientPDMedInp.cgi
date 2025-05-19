[[myHTML->newPage(%form+Medications)]]

<SCRIPT LANGUAGE="JavaScript" SRC="/src/cgi/js/NoEnter.js"> </SCRIPT>
<SCRIPT LANGUAGE="JavaScript" SRC="/src/cgi/js/vEntry.js"> </SCRIPT>
<SCRIPT LANGUAGE="JavaScript" SRC="/src/cgi/js/vPDMed.js"> </SCRIPT>
<SCRIPT type="text/javascript" src="/src/cgi/js/ajaxrequest.js"></SCRIPT>
<SCRIPT LANGUAGE="JavaScript" SRC="/src/cgi/js/qDate.js"> </SCRIPT>
<SCRIPT LANGUAGE="JavaScript" SRC="/src/cgi/js/vNum.js"> </SCRIPT>
<SCRIPT LANGUAGE="JavaScript" >
function vDelete(form)
{
  if ( confirm("Are you sure you want to delete this Medication?") ) { return true; }
  return false;
}
</SCRIPT>

<FORM NAME="Meds" ACTION="/src/cgi/bin/mis.cgi" METHOD="POST" >
<TABLE CLASS="main fullsize" >
  <TR >
    <TD CLASS="strcol" >
      <<<Client_FName_1>>> <<<Client_MName_1>>> <<<Client_LName_1>>> (<<<Client_ClientID_1>>>) <<<Client_SSN_1>>>
      <BR>
      Medications View/Edit Page
    </TD>
    <TD CLASS="numcol" >[[gHTML->setLINKS(%form+back)]]</TD>
  </TR>
</TABLE>
<TABLE CLASS="home fullsize" >
    <TR ><TD ><TABLE CLASS="home fullsize" >
  <TR ><TD CLASS="port hdrtxt" COLSPAN=2 >MEDICATION</TD></TR>
  <TR >
    <TD CLASS="strcol" COLSPAN="2" >To 'Search:' enter text into the box and then 'tab' to the Selection List.</TD>
  </TR>
  <TR >
    <TD CLASS="strcol" >Physician</TD>
    <TD CLASS="strcol" >
      Search: <INPUT TYPE="text" ID="SearchPhysNPI" NAME="SearchPhysNPI" VALUE="" ONFOCUS="select()" ONCHANGE="callAjax('Physicians','<<PDMed_PhysNPI_1>>','selPhysNPI','&name=PDMed_PhysNPI_1&pattern='+this.value,'popup.pl');" SIZE="60" >
    </TD>
  </TR>
  <TR >
    <TD CLASS="strcol" >&nbsp;</TD>
    <TD CLASS="strcol" >
<SPAN ID="selPhysNPI"></SPAN>
    </TD>
  </TR>
  <TR >
    <TD CLASS="strcol" >Medication</TD>
    <TD CLASS="strcol" >
      Search: <INPUT TYPE="text" ID="SearchMedID" NAME="SearchMedID" VALUE="" ONFOCUS="select()" ONCHANGE="callAjax('Medications','<<PDMed_MedID_1>>','selMedID','&name=PDMed_MedID_1&pattern='+this.value,'popup.pl');" SIZE="60" >
    </TD>
  </TR>
  <TR >
    <TD CLASS="strcol" >&nbsp;</TD>
    <TD CLASS="strcol" >
<SPAN ID="selMedID"></SPAN>
    </TD>
  </TR>
  <TR >
    <TD CLASS="strcol" >Type</TD>
    <TD CLASS="strcol" >
      <SELECT NAME="PDMed_MedType_1">
        [[DBA->selxTable(%form+xMedType+<<PDMed_MedType_1>>+Descr)]]
      </SELECT>
    </TD>
  </TR>
  <TR >
    <TD CLASS="strcol" >Dosage/Strength</TD>
    <TD CLASS="strcol" >
      <SELECT NAME="PDMed_MedDos_1">
        [[DBA->selxTable(%form+xMedDos+<<PDMed_MedDos_1>>+Descr+0+Descr)]]
      </SELECT>
    </TD>
  </TR>
  <TR >
    <TD CLASS="strcol" >#Pills/Tabs</TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="text" NAME="PDMed_Pills_1" VALUE="<<PDMed_Pills_1>>" ONFOCUS="select()" ONCHANGE="return vNum(this,0,300)" SIZE=10>
    </TD>
  </TR>
  <TR >
    <TD CLASS="strcol" >Route</TD>
    <TD CLASS="strcol" >
      <SELECT NAME="PDMed_Route_1">
        [[DBA->selxTable(%form+xMedRoute+<<PDMed_Route_1>>+ID Descr)]]
      </SELECT>
    </TD>
  </TR>
  <TR >
    <TD CLASS="strcol" >Frequency</TD>
    <TD CLASS="strcol" >
      <SELECT NAME="PDMed_MedFreq_1">
        [[DBA->selxTable(%form+xMedFreq+<<PDMed_MedFreq_1>>+Text)]]
      </SELECT>
    </TD>
  </TR>
  <TR >
    <TD CLASS="strcol" >Start Date</TD>
    <TD CLASS="strcol" >
      <INPUT TYPE=text NAME="PDMed_StartDate_1" VALUE="<<PDMed_StartDate_1>>" ONFOCUS="select()" ONCHANGE="return qDate(this,1)" SIZE=15>
    </TD>
  </TR>
  <TR >
    <TD CLASS="strcol" >Side Effects</TD>
    <TD CLASS="strcol" >
      <SELECT NAME="PDMed_MedSEff_1">
        [[DBA->selxTable(%form+xSideEff+<<PDMed_MedSEff_1>>+Descr+0+Descr)]]
      </SELECT>
    </TD>
  </TR>
  <TR >
    <TD CLASS="strcol" >#Dispensed</TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="text" NAME="PDMed_Count_1" VALUE="<<PDMed_Count_1>>" ONFOCUS="select()" ONCHANGE="return vNum(this,1,300)" SIZE=10>
    </TD>
  </TR>
  <TR >
    <TD CLASS="strcol" >Refills</TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="text" NAME="PDMed_Refills_1" VALUE="<<PDMed_Refills_1>>" ONFOCUS="select()" ONCHANGE="return vNum(this,1,300)" SIZE=10>
    </TD>
  </TR>
  <TR >
    <TD CLASS="strcol" >Benefits</TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="text" NAME="PDMed_Benefits_1" VALUE="<<PDMed_Benefits_1>>" ONFOCUS="select()" size=20 >
    </TD>
  </TR>
  <TR >
    <TD CLASS="strcol" >Current</TD>
    <TD CLASS="strcol" >
      <INPUT TYPE=radio NAME="PDMed_MedActive_1" VALUE=1 <<PDMed_MedActive_1=1>> > yes
      <INPUT TYPE=radio NAME="PDMed_MedActive_1" VALUE=0 <<PDMed_MedActive_1=0>> > no
    </TD>
  </TR>
    </TABLE></TD></TR>
</TABLE>
<TABLE CLASS="main fullsize" >
  <TR >
    <TD CLASS="numcol" >
      <INPUT TYPE="submit" ONCLICK="return vDelete(this.form);" NAME="PDMed_DELETE_1=1&UpdateTables=all&misPOP=1" VALUE="Delete Medication">
      <INPUT TYPE="submit" ONCLICK="return validate(this.form);" NAME="UpdateTables=all&misPOP=1" VALUE="Add/Update">
    </TD>
  </TR>
</TABLE>

</LOADHIDDEN>
</FORM>

<SCRIPT LANGUAGE="JavaScript">
document.Meds.elements[0].focus();
callAjax('Physicians','<<PDMed_PhysNPI_1>>','selPhysNPI','&name=PDMed_PhysNPI_1','popup.pl');
callAjax('Medications','<<PDMed_MedID_1>>','selMedID','&name=PDMed_MedID_1','popup.pl');
</SCRIPT>
[[myHTML->rightpane(%form+search)]]
