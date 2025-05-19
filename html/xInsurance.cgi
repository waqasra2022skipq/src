[[myHTML->newPage(%form+Insurance)]]

<SCRIPT LANGUAGE="JavaScript" SRC="/src/cgi/js/vEntry.js"> </SCRIPT>
<SCRIPT LANGUAGE="JavaScript" SRC="/src/cgi/js/vxInsurance.js"> </SCRIPT>
<SCRIPT LANGUAGE="JavaScript" SRC="/src/cgi/js/vZip.js"> </SCRIPT>
<SCRIPT LANGUAGE="JavaScript" SRC="/src/cgi/js/vPhone.js"> </SCRIPT>
<SCRIPT LANGUAGE="JavaScript" SRC="/src/cgi/js/Utils.js"> </SCRIPT>
<SCRIPT type="text/javascript" src="/src/cgi/js/ajaxrequest.js"></SCRIPT>
<SCRIPT type="text/javascript" src="/src/cgi/js/vCheckAddress.js?v=202006032043"></SCRIPT>
<SCRIPT LANGUAGE="JavaScript" >
$(document).ready(function() {
  var addressVerified = document.getElementsByName('xInsurance_addressVerified_1')[0].value;
  if (addressVerified == 1) {
    document.getElementById('xInsurance_Check_Address_1').innerHTML
      = `<img src="/images/check.jpg" width="20" height="20" style="vertical-align: middle;margin-right: 8px;"><span>Verified</span>`;
  }
});

function initAutocomplete() {
  var autocomplete = new google.maps.places.Autocomplete(
      document.getElementById('autocomplete'), {types: []});
  autocomplete.setFields(['address_component']);
  autocomplete.addListener('place_changed', () => { fillInAddress(autocomplete, 'xInsurance_'); });
}
</SCRIPT>

[[*SysAccess->verify(%form+Privilege=SiteAdmin)]]

<FORM NAME="xInsurance" ACTION="/src/cgi/bin/mis.cgi" METHOD="POST" >
<TABLE CLASS="main fullsize" >
  <TR >
    <TD CLASS="strcol" >
      Insurance Information
      <BR>Entry Update
    </TD>
    <TD CLASS="numcol" >[[gHTML->setLINKS(%form+back)]]</TD>
  </TR>
</TABLE>
<TABLE CLASS="home fullsize" >
  <TR CLASS="port" > <TD CLASS="hdrtxt" COLSPAN="2" >Identifying Information</TD></TR>
  <TR>
    <TD CLASS="strcol" WIDTH="30%" >Regions</TD>
    <TD CLASS="strcol" >
      <SELECT NAME="xInsurance_Regions_1" MULTIPLE SIZE="10" >
        [[DBA->selxTable(%form+xState+<<xInsurance_Regions_1>>+Descr)]]
      </SELECT>
    </TD>
  </TR>
  <TR>
    <TD CLASS="strcol" WIDTH="30%" >Name</TD>
    <TD CLASS="strcol" >
       <INPUT TYPE="text" NAME="xInsurance_Name_1" VALUE="<<xInsurance_Name_1>>" ONFOCUS="select()" SIZE=30>
    </TD>
  </TR>
  <TR>
    <TD CLASS="strcol" ALIGN=left WIDTH=25% >Insurance Type</TD>
    <TD CLASS="strcol" ALIGN=left >
      <SELECT NAME="xInsurance_InsType_1" > [[DBA->selxTable(%form+xInsType+<<xInsurance_InsType_1>>)]]</SELECT> 
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
    <TD CLASS="strcol" WIDTH="30%" >Address 1</TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="text" NAME="xInsurance_Addr1_1" VALUE="<<xInsurance_Addr1_1>>" readonly style="pointer-events: none;background-color:#E9ECEF" >
    </TD>
  </TR>
  <TR >
    <TD CLASS="strcol" WIDTH="30%" >Enter PO Box or Apt #</TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="text" NAME="xInsurance_Addr2_1" VALUE="<<xInsurance_Addr2_1>>" ONKEYUP="onChangeAddr2('xInsurance_', this.value)" >
    </TD>
  </TR>
  <TR >
    <TD CLASS="strcol" WIDTH="30%" >City</TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="text" NAME="xInsurance_City_1" VALUE="<<xInsurance_City_1>>" readonly style="pointer-events: none;background-color:#E9ECEF" >
    </TD>
  </TR>
  <TR >
    <TD CLASS="strcol" WIDTH="30%" >State</TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="text" NAME="xInsurance_ST_1" VALUE="<<xInsurance_ST_1>>" readonly style="pointer-events: none;background-color:#E9ECEF" >
    </TD>
  </TR>
  <TR >
    <TD CLASS="strcol" WIDTH="30%" >Zip</TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="text" NAME="xInsurance_Zip_1" VALUE="<<xInsurance_Zip_1>>" readonly style="pointer-events: none;background-color:#E9ECEF" >
    </TD>
  </TR>
  <TR >
    <TD ></TD>
    <TD id="xInsurance_Check_Address_1">
      <A HREF="javascript:callAjax('checkAddress','','',`&Tag=Address&Prefix=xInsurance_&AddrSize=2&Addr1=${document.getElementsByName('xInsurance_Addr1_1')[0].value}&Addr2=${document.getElementsByName('xInsurance_Addr2_1')[0].value}&City=${document.getElementsByName('xInsurance_City_1')[0].value}&State=${document.getElementsByName('xInsurance_ST_1')[0].value}&Zip=${document.getElementsByName('xInsurance_Zip_1')[0].value}`,'usps_ajax.pl')" ONMOUSEOUT="window.status=''">(check address)</A>
    </TD>
    <INPUT TYPE="hidden" NAME="xInsurance_addressVerified_1" VALUE="<<xInsurance_addressVerified_1>>" >
  </TR>
  <TR>
    <TD></TD>
    <TD>
      [[DBUtil->isEQ(<<<LOGINPROVID>>>+91) <A HREF="javascript:void(0);" id="xInsurance_AddressManualInput_Link">Enter address manually</A>]]
      [[myHTML->clientAddressForm(%form+xInsurance_AddressManualInput+xInsurance_+2)]]
    </TD>
  </TR>
  <TR>
    <TD CLASS="strcol" WIDTH="30%" >Mgr First Name</TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="text" NAME="xInsurance_MgrFName_1" VALUE="<<xInsurance_MgrFName_1>>" ONFOCUS="select()" SIZE=20>
    </TD>
  </TR>
  <TR>
    <TD CLASS="strcol" WIDTH="30%" >Mgr Last Name</TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="text" NAME="xInsurance_MgrLName_1" VALUE="<<xInsurance_MgrLName_1>>" ONFOCUS="select()" SIZE=20>
    </TD>
  </TR>
  <TR>
    <TD CLASS="strcol" WIDTH="30%" >Phone 1</TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="TEL" NAME="xInsurance_Ph1_1" VALUE="<<xInsurance_Ph1_1>>" ONFOCUS="select()" ONCHANGE="return vPhone(this);" SIZE=20>
    </TD>
  </TR>
  <TR>
    <TD CLASS="strcol" WIDTH="30%" >Phone 2</TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="TEL" NAME="xInsurance_Ph2_1" VALUE="<<xInsurance_Ph2_1>>" ONFOCUS="select()" ONCHANGE="return vPhone(this);" SIZE=20>
    </TD>
  </TR>
  <TR>
    <TD CLASS="strcol" WIDTH="30%" >Fax</TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="TEL" NAME="xInsurance_Fax_1" VALUE="<<xInsurance_Fax_1>>" ONFOCUS="select()" ONCHANGE="return vPhone(this);" SIZE=20>
    </TD>
  </TR>
  <TR>
    <TD CLASS="strcol" WIDTH="30%" >Email Address</TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="EMAIL" NAME="xInsurance_Email_1" VALUE="<<xInsurance_Email_1>>" ONFOCUS="select()" SIZE=30>
    </TD>
  </TR>
  <TR>
    <TD CLASS="strcol" WIDTH="30%" >Note Type</TD>
    <TD CLASS="strcol" >
      <SELECT NAME="xInsurance_NoteType_1">[[DBA->selxTable(%form+xNoteType+<<xInsurance_NoteType_1>>)]]</SELECT>
    </TD>
  </TR>
  <TR>
    <TD CLASS="strcol" WIDTH="30%" >Current</TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="radio" NAME="xInsurance_Active_1" VALUE=1 <<xInsurance_Active_1=1>> > yes
      <INPUT TYPE="radio" NAME="xInsurance_Active_1" VALUE=0 <<xInsurance_Active_1=0>> > no
    </TD>
  </TR>
</TABLE>
<TABLE CLASS="home fullsize" >
  <TR CLASS="port" > <TD CLASS="hdrtxt" COLSPAN="3" >Billing Information</TD></TR>
  <TR>
    <TD CLASS="strcol" WIDTH="30%" >Insurance Code</TD>
    <TD CLASS="strcol" >
      <SELECT NAME="xInsurance_InsCode_1">[[DBA->selxTable(%form+xInsCode+<<xInsurance_InsCode_1>>+ID Descr)]]</SELECT>
    </TD>
    <TD CLASS="strcol" >
      (SBR09)
    </TD>
  </TR>
  <TR>
    <TD CLASS="strcol" WIDTH="30%" >Submitter ID</TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="text" NAME="xInsurance_SubID_1" VALUE="<<xInsurance_SubID_1>>" ONFOCUS="select()" SIZE=15>
    </TD>
    <TD CLASS="strcol" >
      (Millennium Information Service Account ID)
      (ISA06/GS02/NM109,LOOP 1000A)
    </TD>
  </TR>
  <TR>
    <TD CLASS="strcol" WIDTH="30%" >Payer Name</TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="text" NAME="xInsurance_PayName_1" VALUE="<<xInsurance_PayName_1>>" ONFOCUS="select()" SIZE=60>
    </TD>
    <TD CLASS="strcol" >
      (NM103,LOOP 2010BB)
    </TD>
  </TR>
  <TR>
    <TD CLASS="strcol" WIDTH="30%" >Payer ID</TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="text" NAME="xInsurance_PayID_1" VALUE="<<xInsurance_PayID_1>>" ONFOCUS="select()" SIZE=10>
    </TD>
    <TD CLASS="strcol" >
      (NM109,LOOP 2010BB)
    </TD>
  </TR>
  <TR>
    <TD CLASS="strcol" WIDTH="30%" >Receiver Name</TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="text" NAME="xInsurance_RecName_1" VALUE="<<xInsurance_RecName_1>>" ONFOCUS="select()" SIZE=60>
    </TD>
    <TD CLASS="strcol" >
      (NM103,LOOP 1000B&2010BB)
    </TD>
  </TR>
  <TR>
    <TD CLASS="strcol" WIDTH="30%" >Receiver ID</TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="text" NAME="xInsurance_RecID_1" VALUE="<<xInsurance_RecID_1>>" ONFOCUS="select()" SIZE=10>
      (comes back in GS02 or REF*2U)
    </TD>
    <TD CLASS="strcol" >
      (ISA08/GS03/NM109,LOOP 1000B&2010BB)
    </TD>
  </TR>
</TABLE>
<TABLE CLASS="home fullsize" >
  <TR CLASS="port" > <TD CLASS="hdrtxt" COLSPAN="3" >Clearing House Information<BR>to be set by Keith Stephenson</TD></TR>
  <TR>
    <TD CLASS="strcol" WIDTH="30%" >ClearingHouse (do not change)</TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="text" NAME="xInsurance_ClearingHouse_1" VALUE="<<xInsurance_ClearingHouse_1>>" ONCHANGE="return stringFilter(this,' !@#$%^&*()',0,0,0);" ONFOCUS="select()" SIZE="15" >
    </TD>
    <TD CLASS="strcol" >
      Remit
      <INPUT TYPE="radio" NAME="xInsurance_ClearingHouseRemit_1" VALUE=1 <<xInsurance_ClearingHouseRemit_1=1>> > yes
      <INPUT TYPE="radio" NAME="xInsurance_ClearingHouseRemit_1" VALUE=0 <<xInsurance_ClearingHouseRemit_1=0>> > no
    </TD>
  </TR>
  <TR>
    <TD CLASS="strcol" WIDTH="30%" >Sender Interchange ID Qualifier</TD>
    <TD CLASS="strcol" >
      <SELECT NAME="xInsurance_ISASQ_1">[[DBA->selxTable(%form+xISAQ+<<xInsurance_ISASQ_1>>+ID Descr)]]</SELECT>
    </TD>
    <TD CLASS="strcol" >
      (ISA05)
    </TD>
  </TR>
  <TR>
    <TD CLASS="strcol" WIDTH="30%" >Sender Interchange ID</TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="text" NAME="xInsurance_SenderID_1" VALUE="<<xInsurance_SenderID_1>>" ONFOCUS="select()" SIZE="15" > w/ClearingHouse
    </TD>
    <TD CLASS="strcol" >
      (ISA06 defaults to Submitter ID)
    </TD>
  </TR>
  <TR>
    <TD CLASS="strcol" WIDTH="30%" >Sender Application Code</TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="text" NAME="xInsurance_SenderCode_1" VALUE="<<xInsurance_SenderCode_1>>" ONFOCUS="select()" SIZE="15" > w/ClearingHouse
    </TD>
    <TD CLASS="strcol" >
      (GS02 defaults to Sender Interchange ID)
    </TD>
  </TR>
  <TR>
    <TD CLASS="strcol" WIDTH="30%" >Receiver Interchange ID Qualifier</TD>
    <TD CLASS="strcol" >
      <SELECT NAME="xInsurance_ISARQ_1">[[DBA->selxTable(%form+xISAQ+<<xInsurance_ISARQ_1>>+ID Descr)]]</SELECT>
    </TD>
    <TD CLASS="strcol" >
      (ISA07)
    </TD>
  </TR>
  <TR>
    <TD CLASS="strcol" WIDTH="30%" >Receiver Interchange ID</TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="text" NAME="xInsurance_ReceiverID_1" VALUE="<<xInsurance_ReceiverID_1>>" ONFOCUS="select()" SIZE="15" > w/ClearingHouse
    </TD>
    <TD CLASS="strcol" >
      (ISA08 defaults to Receiver ID)
    </TD>
  </TR>
  <TR>
    <TD CLASS="strcol" WIDTH="30%" >Receiver Application Code</TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="text" NAME="xInsurance_ReceiverCode_1" VALUE="<<xInsurance_ReceiverCode_1>>" ONFOCUS="select()" SIZE="15" > w/ClearingHouse
    </TD>
    <TD CLASS="strcol" >
      (GS03 defaults to Receiver Interchange ID)
    </TD>
  </TR>
</TABLE>
<TABLE CLASS="home fullsize" >
  <TR CLASS="port" > <TD CLASS="hdrtxt" COLSPAN="3" >Additional Information<BR>(to be set by Keith Stephenson)</TD></TR>
  <TR>
    <TD CLASS="strcol" WIDTH="30%" >Descr (do not change)</TD>
    <TD CLASS="strcol" COLSPAN="2" >
      <INPUT TYPE="text" NAME="xInsurance_Descr_1" VALUE="<<xInsurance_Descr_1>>" ONCHANGE="return stringFilter(this,' !@#$%^&*()',0,0,0);" ONFOCUS="select()" SIZE="15" >
    </TD>
  </TR>
  <TR>
    <TD CLASS="strcol" WIDTH="30%" >Help Link(do not change)</TD>
    <TD CLASS="strcol" COLSPAN="2" >
      <INPUT TYPE="text" NAME="xInsurance_Help_1" VALUE="<<xInsurance_Help_1>>" ONFOCUS="select()" SIZE="80" >
    </TD>
  </TR>
  <TR>
    <TD CLASS="strcol" WIDTH="30%" >Comments</TD>
    <TD CLASS="strcol" COLSPAN="2" >
      <TEXTAREA NAME="xInsurance_Comments_1" COLS="90" ROWS="5" WRAP="virtual" ><<xInsurance_Comments_1>></TEXTAREA>
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
[[myHTML->ListSel(%form+ListxSC+<<<xInsurance_ID>>>+<<<LINKID>>>+<<<xInsurance_Locked_1>>>)]]

</LOADHIDDEN>
</FORM>
<SCRIPT LANGUAGE="JavaScript">
document.xInsurance.elements[0].focus();
</SCRIPT>
[[myHTML->rightpane(%form+search)]]
<script src="https://maps.googleapis.com/maps/api/js?key=AIzaSyAG2JfgYWgk7Q3FDfZQJauF-M4o4H1wqVw&libraries=places&callback=initAutocomplete"
        async defer></script>
<script LANGUAGE="JavaScript" src="/src/cgi/js/vClientAddressForm.js?v=202006242248"></script>
<script LANGUAGE="JavaScript">
$(document).ready(function() {
  initClientAddressForm('xInsurance_AddressManualInput', 'xInsurance_AddressManualInput_Link', 'xInsurance_', 2);
});
</script>
