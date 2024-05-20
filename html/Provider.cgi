[[myHTML->newPage(%form+Provider Information)]]

<SCRIPT LANGUAGE="JavaScript" SRC="/cgi/js/NoEnter.js"> </SCRIPT>
<SCRIPT LANGUAGE="JavaScript" SRC="/cgi/js/vEntry.js"> </SCRIPT>
<SCRIPT LANGUAGE="JavaScript" SRC="/cgi/js/vProvider.js?v=202006032043"> </SCRIPT>
<SCRIPT LANGUAGE="JavaScript" SRC="/cgi/js/Utils.js"> </SCRIPT>
<SCRIPT LANGUAGE="JavaScript" SRC="/cgi/js/vZip.js"> </SCRIPT>
<SCRIPT LANGUAGE="JavaScript" SRC="/cgi/js/vDate.js"> </SCRIPT>
<SCRIPT LANGUAGE="JavaScript" SRC="/cgi/js/vPhone.js"> </SCRIPT>
<SCRIPT LANGUAGE="JavaScript" SRC="/cgi/js/vSSN.js"> </SCRIPT>
<SCRIPT type="text/javascript" src="/cgi/js/ajaxrequest.js"></SCRIPT>
<SCRIPT type="text/javascript" src="/cgi/js/vCheckAddress.js?v=202006032043"></SCRIPT>
<SCRIPT LANGUAGE="JavaScript" >
$(document).ready(function() {
  var addressVerified = document.getElementsByName('Provider_addressVerified_1')[0].value;
  if (addressVerified == 1) {
    document.getElementById('Provider_Check_Address_1').innerHTML
      = `<img src="/images/check.jpg" width="20" height="20" style="vertical-align: middle;margin-right: 8px;"><span>Verified</span>`;
  }
});

function initAutocomplete() {
  var autocomplete = new google.maps.places.Autocomplete(
      document.getElementById('autocomplete'), {types: []});
  autocomplete.setFields(['address_component']);
  autocomplete.addListener('place_changed', () => { fillInAddress(autocomplete, 'Provider_'); });
}
</SCRIPT>

<FORM NAME="Provider" ACTION="/cgi/bin/mis.cgi" METHOD="POST" >
<TABLE CLASS="main fullsize" >
  <TR >
    <TD CLASS="strcol" >
      <<<Provider_FName_1>>> <<<Provider_MName_1>>> <<<Provider_LName_1>>> 
      <BR>Demographic Information
    </TD>
    <TD CLASS="numcol" >[[gHTML->setLINKS(%form+back)]]</TD>
  </TR>
  <TR >
    <TD CLASS="hotmsg" COLSPAN="2" >
      [[DBUtil->isNULL(<<<Provider_ProvID_1>>>)NEW PROVIDER]] &nbsp;
    </TD>
  </TR>
</TABLE>
<TABLE CLASS="home fullsize" >
    <TR ><TD ><TABLE CLASS="home fullsize" >
[[gHTML->RestrictedProviderFields(%form+Agent)]]
  <TR >
    <TD CLASS="strcol" >First Name</TD>
    <TD CLASS="strcol" COLSPAN="3" >
      <INPUT TYPE="text" NAME="Provider_FName_1" VALUE="<<Provider_FName_1>>" ONCHANGE="return stringFilter(this,'!@#$%^&*()',1,0,1);" ONFOCUS="select()" SIZE="20" >
    </TD>
  </TR>
  <TR >
    <TD CLASS="strcol" >Last Name</TD>
    <TD CLASS="strcol" COLSPAN="3" >
      <INPUT TYPE="text" NAME="Provider_LName_1" VALUE="<<Provider_LName_1>>" ONCHANGE="return stringFilter(this,'!@#$%^&*()',1,0,1);" ONFOCUS="select()" SIZE="20" >
    </TD>
  </TR>
  <TR >
    <TD CLASS="strcol" >Middle</TD>
    <TD CLASS="strcol" COLSPAN="3" >
      <INPUT TYPE="text" NAME="Provider_MName_1" VALUE="<<Provider_MName_1>>" ONCHANGE="return stringFilter(this,'!@#$%^&*()',1,0,1);" ONFOCUS="select()" SIZE="20" >
    </TD>
  </TR>
  <TR >
    <TD CLASS="strcol" >Suffix</TD>
    <TD CLASS="strcol" COLSPAN="3" >
      <SELECT NAME="Provider_Suffix_1">
        [[DBA->selxTable(%form+xSuffix+<<Provider_Suffix_1>>+Descr)]]
      </SELECT>
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
    <TD CLASS="strcol" >Address 1</TD>
    <TD CLASS="strcol" COLSPAN="3" >
      <INPUT TYPE="text" NAME="Provider_Addr1_1" VALUE="<<Provider_Addr1_1>>" SIZE="30" readonly style="pointer-events: none;background-color:#E9ECEF" >
    </TD>
  </TR>
  <TR >
    <TD CLASS="strcol" >Enter PO Box or Apt #</TD>
    <TD CLASS="strcol" COLSPAN="3" >
      <INPUT TYPE="text" NAME="Provider_Addr2_1" VALUE="<<Provider_Addr2_1>>" SIZE="30" ONKEYUP="onChangeAddr2('Provider_', this.value)" >
    </TD>
  </TR>
  <TR >
    <TD CLASS="strcol" >City</TD>
    <TD CLASS="strcol" COLSPAN="3" >
      <INPUT TYPE="text" NAME="Provider_City_1" VALUE="<<Provider_City_1>>" SIZE="20" readonly style="pointer-events: none;background-color:#E9ECEF" >
    </TD>
  </TR>
  <TR >
    <TD CLASS="strcol" >County</TD>
    <TD CLASS="strcol" COLSPAN="3" >
      <INPUT TYPE="text" NAME="Provider_County_1" VALUE="<<Provider_County_1>>" SIZE="20" readonly style="pointer-events: none;background-color:#E9ECEF" >
    </TD>
  </TR>
  <TR >
    <TD CLASS="strcol" WIDTH="30%" >State</TD>
    <TD CLASS="strcol" COLSPAN="3" >
      <INPUT TYPE="text" NAME="Provider_ST_1" VALUE="<<Provider_ST_1>>" SIZE="20" readonly style="pointer-events: none;background-color:#E9ECEF" >
    </TD>
  </TR>
  <TR >
    <TD CLASS="strcol" >Zip</TD>
    <TD CLASS="strcol" COLSPAN="3" >
      <INPUT TYPE="text" NAME="Provider_Zip_1" VALUE="<<Provider_Zip_1>>" SIZE="20" readonly style="pointer-events: none;background-color:#E9ECEF" >
    </TD>
  </TR>
  <TR >
    <TD ></TD>
    <TD id="Provider_Check_Address_1">
      <A HREF="javascript:callAjax('checkAddress','','',`&Tag=Address&Prefix=Provider_&AddrSize=2&Addr1=${document.getElementsByName('Provider_Addr1_1')[0].value}&Addr2=${document.getElementsByName('Provider_Addr2_1')[0].value}&City=${document.getElementsByName('Provider_City_1')[0].value}&State=${document.getElementsByName('Provider_ST_1')[0].value}&Zip=${document.getElementsByName('Provider_Zip_1')[0].value}`,'usps_ajax.pl')" ONMOUSEOUT="window.status=''">(check address)</A>
    </TD>
    <INPUT TYPE="hidden" NAME="Provider_addressVerified_1" VALUE="<<Provider_addressVerified_1>>" >
  </TR>
  <TR>
    <TD></TD>
    <TD>
      [[DBUtil->isEQ(<<<LOGINPROVID>>>+91) <A HREF="javascript:void(0);" id="Provider_AddressManualInput_Link">Enter address manually</A>]]
      [[myHTML->clientAddressForm(%form+Provider_AddressManualInput+Provider_+2)]]
    </TD>
  </TR>
  <TR >
    <TD CLASS="strcol" >Email Address</TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="EMAIL" NAME="Provider_Email_1" VALUE="<<Provider_Email_1>>" ONFOCUS="select()" SIZE="30" >
    </TD>
    <TD CLASS="strcol" COLSPAN="2" >
      Turn Email Off
      <INPUT TYPE="radio" NAME="Provider_NoMail_1" VALUE="1" <<Provider_NoMail_1=1>> > Yes
      <INPUT TYPE="radio" NAME="Provider_NoMail_1" VALUE="0" <<Provider_NoMail_1=0>> > No
    </TD>
  </TR>
  <TR >
    <TD CLASS="strcol" >Screen Name</TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="text" NAME="Provider_ScreenName_1" VALUE="<<Provider_ScreenName_1>>" ONFOCUS="select()" MAXLENGTH="30" SIZE="30" >
    </TD>
    <TD CLASS="strcol" COLSPAN="2" >
      (used for display when user has multiple logins)
    </TD>
  </TR>
  <TR >
    <TD CLASS="port hdrtxt" COLSPAN="2" >Demographic Information
    </TD>
  </TR>
  <TR >
    <TD CLASS="strcol" >SSN</TD>
    <TD CLASS="strcol" COLSPAN="3" >
      <INPUT TYPE="text" NAME="Provider_SSN_1" VALUE="<<Provider_SSN_1>>" ONFOCUS="select()" ONCHANGE="return vSSN(this)" SIZE="11" >
    </TD>
  </TR>
  <TR >
    <TD CLASS="strcol" >Date of Birth</TD>
    <TD CLASS="strcol" COLSPAN="3" >
      <INPUT TYPE="text" NAME="Provider_DOB_1" VALUE="<<Provider_DOB_1>>" ONFOCUS="select()" ONCHANGE="return vDate(this,0,this.form,'Provider_Age')" SIZE="10" >
      Age:
      <INPUT TYPE="text" NAME="Provider_Age" VALUE="<<Provider_Age>>" ONFOCUS="form.Provider_Gend_1.focus();" SIZE="4" >
    </TD>
  </TR>
  <TR >
    <TD CLASS="strcol" >Gender</TD>
    <TD CLASS="strcol" COLSPAN="3" >
      <SELECT NAME="Provider_Gend_1">
        [[DBA->selxTable(%form+xGend+<<Provider_Gend_1>>+Descr)]]
      </SELECT>
    </TD>
  </TR>
  <TR >
    <TD CLASS="strcol" >Race</TD>
    <TD CLASS="strcol" COLSPAN="3" >
      <SELECT NAME="Provider_Race_1" >
        [[DBA->selxTable(%form+xRaces+<<Provider_Race_1>>+Descr)]]
      </SELECT> 
    </TD>
  </TR>
  <TR >
    <TD CLASS="port hdrtxt" COLSPAN="2" >Phone Numbers</TD>
  </TR>
  <TR >
    <TD CLASS="strcol" >Home Phone</TD>
    <TD CLASS="strcol" COLSPAN="3" >
      <INPUT TYPE="TEL" NAME="Provider_HmPh_1" VALUE="<<Provider_HmPh_1>>" ONFOCUS="select()" ONCHANGE="return vPhone(this)" SIZE="20" >
    </TD>
  </TR>
  <TR >
    <TD CLASS="strcol" >Work Phone</TD>
    <TD CLASS="strcol" COLSPAN="3" >
      <INPUT TYPE="TEL" NAME="Provider_WkPh_1" VALUE="<<Provider_WkPh_1>>" ONFOCUS="select()" ONCHANGE="return vPhone(this)" SIZE="20" >
    </TD>
  </TR>
  <TR >
    <TD CLASS="strcol" >Cell Phone / Carrier</TD>
    <TD CLASS="strcol" COLSPAN="3" >
      <INPUT TYPE="TEL" NAME="Provider_MobPh_1" VALUE="<<Provider_MobPh_1>>" ONFOCUS="select()" ONCHANGE="return vPhone(this)" SIZE="20" >
      <SELECT NAME="Provider_Carrier_1">
        [[DBA->selxTable(%form+xCarrier+<<Provider_Carrier_1>>+Descr)]]
      </SELECT>
    </TD>
  </TR>
  <TR >
    <TD CLASS="strcol" >Fax</TD>
    <TD CLASS="strcol" COLSPAN="3" >
      <INPUT TYPE="TEL" NAME="Provider_Fax_1" VALUE="<<Provider_Fax_1>>" ONFOCUS="select()" ONCHANGE="return vPhone(this)" SIZE="20" >
    </TD>
  </TR>
  <TR >
    <TD CLASS="strcol" >Other Phone</TD>
    <TD CLASS="strcol" COLSPAN="3" >
      <INPUT TYPE="TEL" NAME="Provider_OthPh_1" VALUE="<<Provider_OthPh_1>>" ONFOCUS="select()" ONCHANGE="return vPhone(this)" SIZE="20" >
    </TD>
  </TR>
  <TR >
    <TD CLASS="strcol" >Other Phone Label</TD>
    <TD CLASS="strcol" COLSPAN="3" >
      <INPUT TYPE="text" NAME="Provider_OthPhLbl_1" VALUE="<<Provider_OthPhLbl_1>>" ONFOCUS="select()" SIZE="20" >
    </TD>
  </TR>
  <TR > <TD CLASS="port" STYLE="color: red" COLSPAN="2" >Emergency Information</TD> </TR>
  <TR >
    <TD CLASS="strcol" >Emergency Phone</TD>
    <TD CLASS="strcol" COLSPAN="3" >
      <INPUT TYPE="TEL" NAME="Provider_EmPh_1" VALUE="<<Provider_EmPh_1>>" ONFOCUS="select()" ONCHANGE="return vPhone(this)" SIZE="20" >
    </TD>
  </TR>
  <TR >
    <TD CLASS="strcol" >Emergency Name</TD>
    <TD CLASS="strcol" COLSPAN="3" >
      <INPUT TYPE="text" NAME="Provider_EmCont_1" VALUE="<<Provider_EmCont_1>>" ONFOCUS="select()" SIZE="30" >
    </TD>
  </TR>
  <TR >
    <TD CLASS="strcol" >Relation</TD>
    <TD CLASS="strcol" COLSPAN="3" >
      <SELECT NAME="Provider_EmContRel_1">
        [[DBA->selxTable(%form+xRelationship+<<Provider_EmContRel_1>>+Descr)]]
      </SELECT>
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

<INPUT TYPE="hidden" NAME="post_update" VALUE="DBA->updProvider(%form)" >
</LOADHIDDEN>
</FORM>
<SCRIPT LANGUAGE="JavaScript">
document.Provider.elements[0].focus();
vDate(document.Provider.Provider_DOB_1,1,document.Provider,'Provider_Age');
</SCRIPT>

[[myHTML->rightpane(%form+search)]]
<script src="https://maps.googleapis.com/maps/api/js?key=AIzaSyAG2JfgYWgk7Q3FDfZQJauF-M4o4H1wqVw&libraries=places&callback=initAutocomplete"
        async defer></script>
<script LANGUAGE="JavaScript" src="/cgi/js/vClientAddressForm.js?v=202006242248"></script>
<script LANGUAGE="JavaScript">
$(document).ready(function() {
  initClientAddressForm('Provider_AddressManualInput', 'Provider_AddressManualInput_Link', 'Provider_', 2);
});
</script>
