[[myHTML->newHTML(%form+Client Probation and Parole)]]

<SCRIPT LANGUAGE="JavaScript" SRC="/src/cgi/js/NoEnter.js"> </SCRIPT>
<SCRIPT LANGUAGE="JavaScript" SRC="/src/cgi/js/vEntry.js"> </SCRIPT>
<SCRIPT LANGUAGE="JavaScript" SRC="/src/cgi/js/vClientLegalPP.js"> </SCRIPT>
<SCRIPT LANGUAGE="JavaScript" SRC="/src/cgi/js/vPhone.js"> </SCRIPT>
<SCRIPT type="text/javascript" src="/src/cgi/js/ajaxrequest.js"></SCRIPT>
<SCRIPT type="text/javascript" src="/src/cgi/js/vCheckAddress.js?v=202006032043"></SCRIPT>
<SCRIPT LANGUAGE="JavaScript" >
$(document).ready(function() {
  var addressVerified = document.getElementsByName('ClientLegalPP_addressVerified_1')[0].value;
  if (addressVerified == 1) {
    document.getElementById('ClientLegalPP_Check_Address_1').innerHTML
      = `<img src="/images/check.jpg" width="20" height="20" style="vertical-align: middle;margin-right: 8px;"><span>Verified</span>`;
  }
});

function initAutocomplete() {
  var autocomplete = new google.maps.places.Autocomplete(
      document.getElementById('autocomplete'), {types: []});
  autocomplete.setFields(['address_component']);
  autocomplete.addListener('place_changed', () => { fillInAddress(autocomplete, 'ClientLegalPP_', 1); });
}
</SCRIPT>

<FORM NAME="ClientLegalPP" ACTION="/src/cgi/bin/mis.cgi" METHOD="POST" >
<TABLE CLASS="main fullsize" >
  <TR >
    <TD CLASS="strcol" >
      <<<Client_FName_1>>> <<<Client_MName_1>>> <<<Client_LName_1>>> (<<<Client_ClientID_1>>>) <<<Client_SSN_1>>>
    </TD>
    <TD CLASS="numcol" >[[gHTML->setLINKS(%form+back)]]</TD>
  </TR>
</TABLE>
<TABLE CLASS="home fullsize" >
  <TR ><TD CLASS="port hdrtxt" COLSPAN="2" >Probation and Parole</TD></TR>
  <TR >
    <TD CLASS="strcol" >Case Worker / Worker Officer</TD>
    <TD CLASS="strcol" >
       <INPUT TYPE="text" NAME="ClientLegalPP_Name_1" VALUE="<<ClientLegalPP_Name_1>>" ONFOCUS="select()" SIZE="20" >
    </TD>
  </TR>
  <TR >
    <TD CLASS="strcol" >Enter Address</TD>
    <TD CLASS="strcol" >
      <input id="autocomplete"
             type="text"
             size="50"/>
    </TD>
  </TR>
  <TR >
    <TD CLASS="strcol" >Address</TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="text" NAME="ClientLegalPP_Addr_1" VALUE="<<ClientLegalPP_Addr_1>>" ONFOCUS="select()" SIZE="20" readonly style="pointer-events: none;background-color:#E9ECEF" >
    </TD>
  </TR>
  <TR >
    <TD CLASS="strcol" >City</TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="text" NAME="ClientLegalPP_City_1" VALUE="<<ClientLegalPP_City_1>>" ONFOCUS="select()" SIZE="20" readonly style="pointer-events: none;background-color:#E9ECEF" >,&nbsp;
    </TD>
  </TR>
  <TR >
    <TD CLASS="strcol" >State</TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="text" NAME="ClientLegalPP_ST_1" VALUE="<<ClientLegalPP_ST_1>>" SIZE="20" readonly style="pointer-events: none;background-color:#E9ECEF" >
    </TD>
  </TR>
  <TR >
    <TD CLASS="strcol" >Zip</TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="text" NAME="ClientLegalPP_Zip_1" VALUE="<<ClientLegalPP_Zip_1>>" SIZE="20" readonly style="pointer-events: none;background-color:#E9ECEF" >
    </TD>
  </TR>
  <TR >
    <TD ></TD>
    <TD id="ClientLegalPP_Check_Address_1">
      <A HREF="javascript:callAjax('checkAddress','','',`&Tag=Address&Prefix=ClientLegalPP_&AddrSize=1&Addr1=${document.getElementsByName('ClientLegalPP_Addr_1')[0].value}&Addr2=&City=${document.getElementsByName('ClientLegalPP_City_1')[0].value}&State=${document.getElementsByName('ClientLegalPP_ST_1')[0].value}&Zip=${document.getElementsByName('ClientLegalPP_Zip_1')[0].value}`,'usps_ajax.pl')" ONMOUSEOUT="window.status=''">(check address)</A>
    </TD>
    <INPUT TYPE="hidden" NAME="ClientLegalPP_addressVerified_1" VALUE="<<ClientLegalPP_addressVerified_1>>" >
  </TR>
  <TR>
    <TD></TD>
    <TD>
      [[DBUtil->isEQ(<<<LOGINPROVID>>>+91) <A HREF="javascript:void(0);" id="ClientLegalPP_AddressManualInput_Link">Enter address manually</A>]]
      [[myHTML->clientAddressForm(%form+ClientLegalPP_AddressManualInput+ClientLegalPP_+1)]]
    </TD>
  </TR>
  <TR >
    <TD CLASS="strcol" >Work Phone</TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="TEL" NAME="ClientLegalPP_WkPh_1" VALUE="<<ClientLegalPP_WkPh_1>>" ONFOCUS="select()" ONCHANGE="vPhone(this)" SIZE="20" >
    </TD>
  </TR>
  <TR >
    <TD CLASS="strcol" >Cell Phone</TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="TEL" NAME="ClientLegalPP_Cell_1" VALUE="<<ClientLegalPP_Cell_1>>" ONFOCUS="select()" ONCHANGE="vPhone(this)" SIZE="20" >
    </TD>
  </TR>
  <TR >
    <TD CLASS="strcol" >Custodial Agency</TD>
    <TD CLASS="strcol" >
      <SELECT NAME="ClientLegalPP_CustAgency_1" >
        [[DBA->selxTable(%form+xCustAgency+<<ClientLegalPP_CustAgency_1>>+Descr)]]
      </SELECT> 
    </TD>
  </TR>
  <TR >
    <TD CLASS="strcol" >Legal Guardian</TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="checkbox" NAME="ClientLegalPP_Guardian_1" VALUE=1 <<ClientLegalPP_Guardian_1=checkbox>> ONFOCUS="select()" >
    </TD>
  </TR>
  <TR >
    <TD CLASS="strcol" >Emergency Contact</TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="checkbox" NAME="ClientLegalPP_EmerContact_1" VALUE=1 <<ClientLegalPP_EmerContact_1=checkbox>> ONFOCUS="select()" >
    </TD>
  </TR>
</TABLE>
<TABLE CLASS="main fullsize" >
  <TR >
    <TD CLASS="numcol" >
      <INPUT TYPE="submit" ONCLICK="return vDELETE('Are you sure you want to delete this record?');" NAME="ClientLegalPP_DELETE_1=1&UpdateTables=all&misPOP=1" VALUE="Delete">
      <INPUT TYPE=submit ONCLICK="return validate(this.form);" NAME="UpdateTables=all&misPOP=1" VALUE="Add/Update">
    </TD>
  </TR>
</TABLE>

</LOADHIDDEN>
</FORM>
<SCRIPT LANGUAGE="JavaScript">
document.ClientLegalPP.elements[0].focus();
</SCRIPT>

[[myHTML->rightpane(%form+search)]]
<script src="https://maps.googleapis.com/maps/api/js?key=AIzaSyAG2JfgYWgk7Q3FDfZQJauF-M4o4H1wqVw&libraries=places&callback=initAutocomplete"
        async defer></script>
<script LANGUAGE="JavaScript" src="/src/cgi/js/vClientAddressForm.js?v=202006242248"></script>
<script LANGUAGE="JavaScript">
$(document).ready(function() {
  initClientAddressForm('ClientLegalPP_AddressManualInput', 'ClientLegalPP_AddressManualInput_Link', 'ClientLegalPP_', 1);
});
</script>
