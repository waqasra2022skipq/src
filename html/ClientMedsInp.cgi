[[myHTML->newPage(%form+Client Medications)]]

<SCRIPT LANGUAGE="JavaScript" SRC="/cgi/js/vEntry.js"> </SCRIPT>
<SCRIPT LANGUAGE="JavaScript" SRC="/cgi/js/vClientMeds.js"> </SCRIPT>
<SCRIPT LANGUAGE="JavaScript" SRC="/cgi/js/vDate.js"> </SCRIPT>

<FORM NAME="ClientMeds" ACTION="/cgi/bin/mis.cgi" METHOD="POST" >
<TABLE CLASS="main fullsize" >
  <TR >
    <TD CLASS="strcol" >
      <<<Client_FName_1>>> <<<Client_MName_1>>> <<<Client_LName_1>>> (<<<Client_ClientID_1>>>) <<<Client_SSN_1>>>
      <BR>
      Client Medications
    </TD>
    <TD CLASS="numcol" >[[gHTML->setLINKS(%form+back)]]</TD>
  </TR>
</TABLE>
<TABLE CLASS="home fullsize" >
  <TR ><TD CLASS="port hdrtxt" COLSPAN="2" >Medications Information</TD></TR>
  <TR >
    <TD CLASS="strcol" >PrescriptionDate (effectiveTimeLow/High)</TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="text" NAME="ClientMeds_PrescriptionDate_1" VALUE="<<ClientMeds_PrescriptionDate_1>>" ONFOCUS="select()" SIZE="20" >
    </TD>
  </TR>
  <TR >
    <TD CLASS="strcol" >ExternalDrugRoute (routeCodeCode)</TD>
    <TD CLASS="strcol" >
      <SELECT NAME="ClientMeds_ExternalDrugRoute_1" >
        [[DBA->selxTable(%form+xDrugRouteOfAdmin+<<ClientMeds_ExternalDrugRoute_1>>+ID Descr)]]
      </SELECT>
    </TD>
  </TR>
  <TR >
    <TD CLASS="strcol" >Route (routeCodeDisplayName)</TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="text" NAME="ClientMeds_Route_1" VALUE="<<ClientMeds_Route_1>>" ONFOCUS="select()" SIZE="20" >
    </TD>
  </TR>
  <TR >
    <TD CLASS="strcol" >Strength (doseQuantityValue)</TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="text" NAME="ClientMeds_Strength_1" VALUE="<<ClientMeds_Strength_1>>" ONFOCUS="select()" SIZE="20" >
    </TD>
  </TR>
  <TR >
    <TD CLASS="strcol" >StrengthUOM (doesQuantityUnit)</TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="text" NAME="ClientMeds_StrengthUOM_1" VALUE="<<ClientMeds_StrengthUOM_1>>" ONFOCUS="select()" SIZE="20" >
    </TD>
  </TR>
  <TR >
    <TD CLASS="strcol" >DosageFrequencyDescription (instructions)</TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="text" NAME="ClientMeds_DosageFrequencyDescription_1" VALUE="<<ClientMeds_DosageFrequencyDescription_1>>" ONFOCUS="select()" SIZE="20" >
    </TD>
  </TR>
  <TR >
    <TD CLASS="strcol" >rxcui (manufacturedMaterialCode)</TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="text" NAME="ClientMeds_rxcui_1" VALUE="<<ClientMeds_rxcui_1>>" ONFOCUS="select()" SIZE="20" >
    </TD>
  </TR>
  <TR >
    <TD CLASS="strcol" >DrugInfo (manufacturedMaterialDisplayName)</TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="text" NAME="ClientMeds_DrugInfo_1" VALUE="<<ClientMeds_DrugInfo_1>>" ONFOCUS="select()" SIZE="20" >
    </TD>
  </TR>
  <TR >
    <TD CLASS="strcol" >Active
    <TD CLASS="strcol" >
      <INPUT TYPE="radio" NAME="ClientMeds_Active_1" VALUE=1 <<ClientMeds_Active_1=1>> > yes
      <INPUT TYPE="radio" NAME="ClientMeds_Active_1" VALUE=0 <<ClientMeds_Active_1=0>> > no
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
document.ClientMeds.elements[0].focus();
</SCRIPT>

[[myHTML->rightpane(%form+search)]]
