[[myHTML->newPage(%form+Client Intake)]]

<SCRIPT type="text/javascript" src="/cgi/js/ajaxrequest.js"></SCRIPT>
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
    <TD CLASS="strcol" >
      <<<Client_FName_1>>> <<<Client_MName_1>>> <<<Client_LName_1>>> (<<<Client_ClientID_1>>>) <<<Client_SSN_1>>>
      <BR>
      Intake Assessment
    </TD>
    <TD CLASS="numcol" >[[gHTML->setLINKS(%form+back)]]</TD>
  </TR>
</TABLE>
<TABLE CLASS="home fullsize" >
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

[[myHTML->rightpane(%form+search)]]
<script src="https://maps.googleapis.com/maps/api/js?key=AIzaSyAG2JfgYWgk7Q3FDfZQJauF-M4o4H1wqVw&libraries=places&callback=initAutocomplete"
        async defer></script>
<script LANGUAGE="JavaScript" src="/cgi/js/vClientAddressForm.js?v=202006242248"></script>
<script LANGUAGE="JavaScript">
$(document).ready(function() {
  initClientAddressForm('Client_AddressManualInput', 'Client_AddressManualInput_Link', 'Client_', 2);
});
</script>
