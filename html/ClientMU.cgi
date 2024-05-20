[[myHTML->newHTML(%form+Client Intake+misall mismenu medalerts)]]

<SCRIPT LANGUAGE="JavaScript" SRC="/cgi/js/vEntry.js"> </SCRIPT>
<SCRIPT LANGUAGE="JavaScript" SRC="/cgi/js/vClientMU.js"> </SCRIPT>
<SCRIPT type="text/javascript" src="/cgi/js/ajaxrequest.js"></SCRIPT>
<SCRIPT LANGUAGE="JavaScript" SRC="/cgi/js/vDate.js"> </SCRIPT>
<SCRIPT LANGUAGE="JavaScript" SRC="/cgi/js/vTime.js"> </SCRIPT>
<SCRIPT LANGUAGE="JavaScript" SRC="/cgi/js/vPhone.js"> </SCRIPT>
<SCRIPT LANGUAGE="JavaScript" SRC="/cgi/js/vNum.js"> </SCRIPT>
<SCRIPT LANGUAGE="JavaScript" SRC="/cgi/js/vZip.js"> </SCRIPT>
<LINK HREF="/cfg/menuV2.css" REL="stylesheet" TYPE="text/css" >
[[uHTML->hClientRuleAlerts(%form+<<<Client_ClientID_1>>>)]]
<SCRIPT type="text/javascript" src="/cgi/menu/js/menuV2.js" ></SCRIPT>
<SCRIPT type="text/javascript" src="/cgi/js/vCheckAddress.js?v=202006032043"></SCRIPT>
<SCRIPT LANGUAGE="JavaScript" >
$(document).ready(function() {
  var addressVerified = document.getElementsByName('Client_addressVerified_1')[0].value;
  if (addressVerified == 1) {
    document.getElementById('Client_Check_Address_1').innerHTML
      = `<img src="/images/check.jpg" width="20" height="20" style="vertical-align: middle;margin-right: 8px;"><span>Verified</span>`;
  }
});

function initAutocomplete() {
  var autocomplete = new google.maps.places.Autocomplete(
      document.getElementById('autocomplete'), {types: []});
  autocomplete.setFields(['address_component']);
  autocomplete.addListener('place_changed', () => { fillInAddress(autocomplete, 'Client_'); });
}
</SCRIPT>

<FORM NAME="Intake" ACTION="/cgi/bin/mis.cgi" METHOD="POST" >
<TABLE CLASS="main fullsize" >
  <TR >
    <TD CLASS="strcol" >[[myHTML->getHTML(%form+MU.menu+1)]]</TD>
    <TD CLASS="strcol" >
      <<<Client_FName_1>>> <<<Client_MName_1>>> <<<Client_LName_1>>> (<<<Client_ClientID_1>>>) <<<Client_SSN_1>>>
      <BR>
      Meaningful Use Access Screen
    </TD>
    <TD CLASS="numcol" >[[gHTML->setLINKS(%form+back)]]</TD>
  </TR>
</TABLE>
<TABLE CLASS="home fullsize" >
  <TR ><TD CLASS="port hdrtxt" COLSPAN="2" >IDENTIFING INFORMATION</TD></TR>
  <TR ><TD CLASS="port hdrtxt" >Client Name Information</TD></TR>
  <TR >
    <TD CLASS="strcol" >First Name</TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="text" NAME="Client_FName_1" VALUE="<<Client_FName_1>>" ONCHANGE="return stringFilter(this,' !@#$%^&*()',1,0,1);" ONFOCUS="select()" SIZE="20" >
    </TD>
  </TR>
  <TR >
    <TD CLASS="strcol" >Last Name</TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="text" NAME="Client_LName_1" VALUE="<<Client_LName_1>>" ONCHANGE="return stringFilter(this,'!@#$%^&*()',1,0,1);" ONFOCUS="select()" SIZE="20" >
    </TD>
  </TR>
  <TR >
    <TD CLASS="strcol" >Maiden / Previous Name</TD>
    <TD CLASS="strcol" ALIGN=left >
      <INPUT TYPE="text" NAME="Client_MaidenName_1" VALUE="<<Client_MaidenName_1>>" ONCHANGE="return stringFilter(this,'!@#$%^&*()',1,0,1);" ONFOCUS="select()" SIZE="20" >
    </TD>
  </TR>
  <TR >
    <TD CLASS="strcol" >Middle Name</TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="text" NAME="Client_MName_1" VALUE="<<Client_MName_1>>" ONCHANGE="return stringFilter(this,' !@#$%^&*()',1,0,1);" ONFOCUS="select()" SIZE="10" >
    </TD>
  </TR>
  <TR >
    <TD CLASS="strcol" >Suffix</TD>
    <TD CLASS="strcol" >
      <SELECT NAME="Client_Suffix_1" >
        [[DBA->selxTable(%form+xSuffix+<<Client_Suffix_1>>+Descr)]]
      </SELECT>
    </TD>
  </TR>
  <TR ><TD CLASS="port hdrtxt" >Biographical Information</TD></TR>
  <TR >
    <TD CLASS="strcol" >Birth Gender</TD>
    <TD CLASS="strcol" >
      <SELECT NAME="Client_Gend_1" >
        [[DBA->selxTable(%form+xGend+<<Client_Gend_1>>+Descr)]]
      </SELECT> 
    </TD>
  </TR>
  <TR >
    <TD CLASS="strcol" >Date of Birth</TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="date" NAME="Client_DOB_1" VALUE="<<Client_DOB_1>>" ONFOCUS="select()" ONCHANGE="return vDate(this,0,this.form,'Client_Age')" SIZE="10" >
      Age:
      <INPUT TYPE="text" NAME="Client_Age" VALUE="<<Client_Age>>" ONFOCUS="form.Client_Gend_1.focus();" SIZE="4" >
    </TD>
  </TR>
  <TR >
    <TD CLASS="strcol" >
      [[myHTML->setxTable(%form+xRaces+<<Client_Race_1>>+Client_Race_1+checkbox+1)]]
    </TD>
    <TD CLASS="strcol" >
      <SPAN ID="Client_Race_1_display" ></SPAN>
    </TD>
  </TR>
  <TR >
    <TD CLASS="strcol" >
      [[myHTML->setxTable(%form+xEthnicity+<<Client_Ethnicity_1>>+Client_Ethnicity_1+checkbox+1)]]
    </TD>
    <TD CLASS="strcol" >
      <SPAN ID="Client_Ethnicity_1_display" ></SPAN>
    </TD>
  </TR>
  <TR ><TD CLASS="port hdrtxt" >Language Information</TD></TR>
  <TR >
    <TD CLASS="strcol" >Preferred Language</TD>
    <TD CLASS="strcol" >
      <SELECT NAME="ClientSocial_PreLang_1" >
        [[DBA->selxTable(%form+xLanguages+<<ClientSocial_PreLang_1>>+English AltID)]]
      </SELECT>
    </TD>
  </TR>
  <TR ><TD CLASS="port hdrtxt" >Address Information</TD></TR>
  <TR >
    <TD CLASS="strcol" >Enter Address</TD>
    <TD CLASS="strcol" >
      <input id="autocomplete"
             type="text"
             size="50"/>
    </TD>
  </TR>
  <TR >
    <TD CLASS="strcol" >Address 1</TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="text" NAME="Client_Addr1_1" VALUE="<<Client_Addr1_1>>" SIZE="30" readonly style="pointer-events: none;background-color:#E9ECEF" >
    </TD>
  </TR>
  <TR >
    <TD CLASS="strcol" >Enter PO Box or Apt #</TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="text" NAME="Client_Addr2_1" VALUE="<<Client_Addr2_1>>" SIZE="30" ONKEYUP="onChangeAddr2('Client_', this.value)" >
    </TD>
  </TR>
  <TR >
    <TD CLASS="strcol" >City</TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="text" NAME="Client_City_1" VALUE="<<Client_City_1>>" SIZE="20" readonly style="pointer-events: none;background-color:#E9ECEF" >
    </TD>
  </TR>
  <TR >
    <TD CLASS="strcol" >County</TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="text" NAME="Client_County_1" VALUE="<<Client_County_1>>" SIZE="20" readonly style="pointer-events: none;background-color:#E9ECEF" >
    </TD>
  </TR>
  <TR >
    <TD CLASS="strcol" >State</TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="text" NAME="Client_ST_1" VALUE="<<Client_ST_1>>" SIZE="20" readonly style="pointer-events: none;background-color:#E9ECEF" >
    </TD>
  </TR>
  <TR >
    <TD CLASS="strcol" >Zip</TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="text" NAME="Client_Zip_1" VALUE="<<Client_Zip_1>>" SIZE="20" readonly style="pointer-events: none;background-color:#E9ECEF" >
    </TD>
  </TR>
  <TR >
    <TD ></TD>
    <TD id="Client_Check_Address_1">
      <A HREF="javascript:callAjax('checkAddress','','',`&Tag=Address&Prefix=Client_&AddrSize=2&Addr1=${document.getElementsByName('Client_Addr1_1')[0].value}&Addr2=${document.getElementsByName('Client_Addr2_1')[0].value}&City=${document.getElementsByName('Client_City_1')[0].value}&State=${document.getElementsByName('Client_ST_1')[0].value}&Zip=${document.getElementsByName('Client_Zip_1')[0].value}`,'usps_ajax.pl')" ONMOUSEOUT="window.status=''">(check address)</A>
    </TD>
    <INPUT TYPE="hidden" NAME="Client_addressVerified_1" VALUE="<<Client_addressVerified_1>>" >
  </TR>
  <TR>
    <TD></TD>
    <TD>
      [[DBUtil->isEQ(<<<LOGINPROVID>>>+91) <A HREF="javascript:void(0);" id="Client_AddressManualInput_Link">Enter address manually</A>]]
      [[myHTML->clientAddressForm(%form+Client_AddressManualInput+Client_+2)]]
    </TD>
  </TR>
  <TR ><TD CLASS="port hdrtxt" >Phone Numbers</TD></TR>
  <TR >
    <TD CLASS="strcol" >Home Phone</TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="TEL" NAME="Client_HmPh_1" VALUE="<<Client_HmPh_1>>" ONFOCUS="select()" ONCHANGE="return vPhone(this)" SIZE="20">
    </TD>
  </TR>
  <TR >
    <TD CLASS="strcol" >Mobile Phone / Carrier</TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="TEL" NAME="Client_MobPh_1" VALUE="<<Client_MobPh_1>>" ONFOCUS="select()" ONCHANGE="return vPhone(this)" SIZE="20">
      <SELECT NAME="Client_Carrier_1" >
        [[DBA->selxTable(%form+xCarrier+<<Client_Carrier_1>>+Descr Access)]]
      </SELECT> 
    </TD>
  </TR>
</TABLE>
<TABLE CLASS="main fullsize" >
  <TR>
    <TD CLASS="numcol" >
      <INPUT TYPE="submit" ONCLICK="return validate(this.form);" NAME="UpdateTables=all&[[myForm->genLink(ClientIntake+ClientMUA.cgi)]]" VALUE="Add/Update -> Client Health" >
      <INPUT TYPE="submit" ONCLICK="return validate(this.form);" NAME="UpdateTables=all&misPOP=1" VALUE="Add/Update" >
    </TD>
  </TR>
</TABLE>

<INPUT TYPE="hidden" NAME="ProviderID" VALUE="<<ProviderID>>" >
</LOADHIDDEN>
</FORM>
<SCRIPT LANGUAGE="JavaScript">
document.Intake.elements[0].focus();
doShow('Client_Race_1','Client_Race_1_display');
doDisableCheck('2186-5','Client_Ethnicity_1','Client_Ethnicity_1_display');
vDate(document.Intake.Client_DOB_1,1,document.Intake,'Client_Age');
</SCRIPT>

[[myHTML->rightpane(%form+search)]]
<script src="https://maps.googleapis.com/maps/api/js?key=AIzaSyAG2JfgYWgk7Q3FDfZQJauF-M4o4H1wqVw&libraries=places&callback=initAutocomplete"
        async defer></script>
<script LANGUAGE="JavaScript" src="/cgi/js/vClientAddressForm.js?v=202006242248"></script>
<script LANGUAGE="JavaScript">
$(document).ready(function() {
  initClientAddressForm('Client_AddressManualInput', 'Client_AddressManualInput_Link', 'Client_', 2);
});
</script>
