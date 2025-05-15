[[myHTML->newPage(%form+Client Insurance)]]

<SCRIPT LANGUAGE="JavaScript" SRC="/src/cgi/js/NoEnter.js"> </SCRIPT>
<SCRIPT LANGUAGE="JavaScript" SRC="/src/cgi/js/vEntry.js"> </SCRIPT>
<SCRIPT LANGUAGE="JavaScript" SRC="/src/cgi/js/vInsurance.js"> </SCRIPT>
<SCRIPT LANGUAGE="JavaScript" SRC="/src/cgi/js/serverREQ.js"> </SCRIPT>
<SCRIPT LANGUAGE="JavaScript" SRC="/src/cgi/js/vDate.js"> </SCRIPT>
<SCRIPT LANGUAGE="JavaScript" SRC="/src/cgi/js/vNum.js"> </SCRIPT>
<SCRIPT LANGUAGE="JavaScript" SRC="/src/cgi/js/vZip.js"> </SCRIPT>
<SCRIPT LANGUAGE="JavaScript" SRC="/src/cgi/js/vPhone.js"> </SCRIPT>
<SCRIPT LANGUAGE="JavaScript" SRC="/src/cgi/js/vSSN.js"> </SCRIPT>
<SCRIPT type="text/javascript" src="/src/cgi/js/ajaxrequest.js"></SCRIPT>
<SCRIPT type="text/javascript" src="/src/cgi/js/vCheckAddress.js?v=202006032043"></SCRIPT>
<SCRIPT LANGUAGE="JavaScript" >
$(document).ready(function() {
  var addressVerified = document.getElementsByName('Guarantor_addressVerified_1')[0].value;
  if (addressVerified == 1) {
    document.getElementById('Guarantor_Check_Address_1').innerHTML
      = `<img src="/images/check.jpg" width="20" height="20" style="vertical-align: middle;margin-right: 8px;"><span>Verified</span>`;
  }
});

function initAutocomplete() {
  var autocomplete = new google.maps.places.Autocomplete(
      document.getElementById('autocomplete'), {types: []});
  autocomplete.setFields(['address_component']);
  autocomplete.addListener('place_changed', () => { fillInAddress(autocomplete, 'Guarantor_'); });
}
</SCRIPT>
<SCRIPT TYPE="text/javascript" SRC="/cgi/jquery/jquery-ui-1.11.2/jquery-ui.min.js" ></SCRIPT>
<LINK HREF="/src/cgi/css/autocomplete.css?v=202008071708" REL="stylesheet">

<LINK HREF="/cfg/tabcontent/template6/tabcontent.css" REL="stylesheet" TYPE="text/css" >
<SCRIPT SRC="/cfg/tabcontent/tabcontent.js" TYPE="text/javascript" ></SCRIPT>
<SCRIPT LANGUAGE="JavaScript" TYPE="text/javascript" SRC="/src/cgi/js/tabs.js"></SCRIPT>
<LINK REL="STYLESHEET" TYPE="text/css" HREF="/src/cgi/css/tabs.css" />
<DIV ALIGN=center >
<FORM NAME="Insurance" ACTION="/cgi/bin/mis.cgi" METHOD="POST" >
<TABLE CLASS="main fullsize" >
  <TR >
    <TD CLASS="strcol" >
      <<<Client_FName_1>>> <<<Client_MName_1>>> <<<Client_LName_1>>> (<<<Client_ClientID_1>>>) <<<Client_SSN_1>>>
      <BR>Client's Insurance
    </TD>
    <TD CLASS="numcol" >[[gHTML->setLINKS(%form+back)]]</TD>
  </TR>
</TABLE>

<TABLE CLASS="home fullsize" >
  <TR>
    <TD CLASS="strcol" WIDTH="30%" >Type</TD>
    <TD CLASS="strcol" >
      <SELECT NAME="Insurance_Priority_1" >[[DBA->selxTable(%form+xPriority+<<Insurance_Priority_1>>)]]</SELECT> 
    </TD>
  </TR>
  <TR >
    <TD CLASS="strcol" WIDTH="30%" >Insurance</TD>
    <TD CLASS="strcol" >[[gHTML->InsuranceSelect(%form+<<<Insurance_InsNumID>>>+<<<Insurance_InsID_1>>>)]]</TD>
  </TR>
  <TR >
    <TD CLASS="strcol" WIDTH="30%" >Effective</TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="text" NAME="Insurance_InsNumEffDate_1" VALUE="<<Insurance_InsNumEffDate_1>>" ONFOCUS="select()" ONCHANGE="return vDate(this);" SIZE="10" >
    </TD>
  </TR>
  <TR >
    <TD CLASS="strcol" WIDTH="30%" >Expires</TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="text" NAME="Insurance_InsNumExpDate_1" VALUE="<<Insurance_InsNumExpDate_1>>" ONFOCUS="select()" ONCHANGE="return vDate(this,1);" SIZE="10" >
    </TD>
  </TR>
  <TR >
    <TD CLASS="strcol" WIDTH="30%" >ID Number</TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="text" ID="InsIDNum" NAME="Insurance_InsIDNum_1" VALUE="<<Insurance_InsIDNum_1>>" ONFOCUS="select()" ONCHANGE="callAjax('vInsNum',this.value,this.id,'&c=<<<Client_ClientID_1>>>&i='+document.Insurance.Insurance_InsID_1.value);" MAXLENGTH="30" SIZE="30" > <SPAN ID="msgInsIDNum"></SPAN>
    </TD>
  </TR>
  <TR >
    <TD CLASS="strcol" WIDTH="30%" >Group Number</TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="text" NAME="Insurance_GrpNum_1" VALUE="<<Insurance_GrpNum_1>>" ONFOCUS="select()" SIZE="30" >
      Plan Name
      <INPUT TYPE="text" NAME="Insurance_PlanName_1" VALUE="<<Insurance_PlanName_1>>" ONFOCUS="select()" SIZE="60" >
    </TD>
  </TR>
  <TR >
    <TD CLASS="strcol" WIDTH="30%" >Rx Numbers</TD>
    <TD CLASS="strcol" >
      RxBIN
      <INPUT TYPE="text" NAME="Insurance_RxBIN_1" VALUE="<<Insurance_RxBIN_1>>" ONFOCUS="select()" SIZE="30" >
      RxPCN
      <INPUT TYPE="text" NAME="Insurance_RxPCN_1" VALUE="<<Insurance_RxPCN_1>>" ONFOCUS="select()" SIZE="30" >
      RxGroup
      <INPUT TYPE="text" NAME="Insurance_RxGroup_1" VALUE="<<Insurance_RxGroup_1>>" ONFOCUS="select()" SIZE="30" >
    </TD>
  </TR>
  <TR >
    <TD CLASS="strcol" WIDTH="30%" >Deductible</TD>
    <TD CLASS="strcol" >$
      <INPUT TYPE="text" NAME="Insurance_Deductible_1" VALUE="<<Insurance_Deductible_1>>" ONFOCUS="select()" ONCHANGE="return vNum(this,0,7500);" SIZE="12" >
    </TD>
  </TR>
  <TR >
    <TD CLASS="strcol" WIDTH="30%" >Copay</TD>
    <TD CLASS="strcol" >$
      <INPUT TYPE="text" NAME="Insurance_Copay_1" VALUE="<<Insurance_Copay_1>>" ONFOCUS="select()" ONCHANGE="return vNum(this,0,200);" SIZE="12" >
    </TD>
  </TR>
  <TR >
    <TD CLASS="strcol" WIDTH="30%" >CreditCard Expires</TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="text" NAME="Insurance_CCExpDate_1" VALUE="<<Insurance_CCExpDate_1>>" ONFOCUS="select()" ONCHANGE="return vDate(this,1);" SIZE="10" >
    </TD>
  </TR>
  <TR >
    <TD CLASS="strcol" WIDTH="30%" >Designated Provider</TD>
    <TD CLASS="strcol" >
      <SELECT ID="DesigProvID" NAME="Insurance_DesigProvID_1" ONCHANGE="callAjax('vInsID',this.value,this.id,'&i='+document.Insurance.Insurance_InsID_1.value);" >[[DBA->selProviders(%form+<<Insurance_DesigProvID_1>>)]]</SELECT> <SPAN ID="msgDesigProvID"></SPAN>
    </TD>
  </TR>
  <TR >
    <TD CLASS="strcol hotmsg" COLSPAN="2" >Do not select a Designated Provider unless required under Medicare. The Designated Provider is only used when the Rendering Provider does not have a PIN for the insurance.  The Designated Provider's PIN will then be used for billing instead of the Provider on the note.</TD>
  </TR>
</TABLE>

<TABLE CLASS="home fullsize" >
  <TR >
    <TD CLASS="port hdrtxt" COLSPAN="3" >
      Guarantor Information<BR>(Enter only if NOT Self Guaranteed)
    </TD>
  </TR>
  <TR >
    <TD CLASS="strcol" WIDTH="30%" >Guarantor Relationship</TD>
    <TD CLASS="strcol" >
      <INPUT ID="MCAutocomplete" TYPE="text" VALUE="[[DBA->getxref(%form+xRelationship+<<<Guarantor_ClientRel_1>>>)]]" ONFOCUS="select()" />
      <INPUT TYPE="hidden" NAME="Guarantor_ClientRel_1" VALUE="<<Guarantor_ClientRel_1>>" >
    </TD>
  </TR>
  <TR > <TD CLASS="port hdrtxt" COLSPAN="3" >Identifying Information</TD> </TR>
  <TR >
    <TD CLASS="strcol" WIDTH="30%" >First Name</TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="TEXT" NAME="Guarantor_FName_1" VALUE="<<Guarantor_FName_1>>" ONFOCUS="select()" SIZE=20>
    </TD>
  </TR>
  <TR >
    <TD CLASS="strcol" WIDTH="30%" >Middle Name</TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="TEXT" NAME="Guarantor_MName_1" VALUE="<<Guarantor_MName_1>>" ONFOCUS="select()" SIZE=10>
    </TD>
  </TR>
  <TR >
    <TD CLASS="strcol" WIDTH="30%" >Last Name</TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="TEXT" NAME="Guarantor_LName_1" VALUE="<<Guarantor_LName_1>>" ONFOCUS="select()" SIZE=20>
    </TD>
  </TR>
  <TR >
    <TD CLASS="strcol" WIDTH="30%" >Suffix</TD>
    <TD CLASS="strcol" >
      <SELECT NAME="Guarantor_Suffix_1">
        [[DBA->selxTable(%form+xSuffix+<<Guarantor_Suffix_1>>+Descr)]]
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
    <TD CLASS="strcol" >
      <INPUT TYPE="text" NAME="Guarantor_Addr1_1" VALUE="<<Guarantor_Addr1_1>>" SIZE="30" readonly style="pointer-events: none;background-color:#E9ECEF" >
    </TD>
  </TR>
  <TR >
    <TD CLASS="strcol" >Enter PO Box or Apt #</TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="text" NAME="Guarantor_Addr2_1" VALUE="<<Guarantor_Addr2_1>>" SIZE="30" ONKEYUP="onChangeAddr2('Guarantor_', this.value)" >
    </TD>
  </TR>
  <TR >
    <TD CLASS="strcol" WIDTH="30%" >City</TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="text" NAME="Guarantor_City_1" VALUE="<<Guarantor_City_1>>" SIZE="20" readonly style="pointer-events: none;background-color:#E9ECEF" >
    </TD>
  </TR>
  <TR >
    <TD CLASS="strcol" WIDTH="30%" >County</TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="text" NAME="Guarantor_County_1" VALUE="<<Guarantor_County_1>>" SIZE="20" readonly style="pointer-events: none;background-color:#E9ECEF" >
    </TD>
  </TR>
  <TR >
    <TD CLASS="strcol" WIDTH="30%" >State</TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="text" NAME="Guarantor_ST_1" VALUE="<<Guarantor_ST_1>>" SIZE="20" readonly style="pointer-events: none;background-color:#E9ECEF" >
    </TD>
  </TR>
  <TR >
    <TD CLASS="strcol" WIDTH="30%" >Zip</TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="text" NAME="Guarantor_Zip_1" VALUE="<<Guarantor_Zip_1>>" SIZE="20" readonly style="pointer-events: none;background-color:#E9ECEF" >
    </TD>
  </TR>
  <TR >
    <TD ></TD>
    <TD id="Guarantor_Check_Address_1">
      <A HREF="javascript:callAjax('checkAddress','','',`&Tag=Address&Prefix=Guarantor_&AddrSize=2&Addr1=${document.getElementsByName('Guarantor_Addr1_1')[0].value}&Addr2=${document.getElementsByName('Guarantor_Addr2_1')[0].value}&City=${document.getElementsByName('Guarantor_City_1')[0].value}&State=${document.getElementsByName('Guarantor_ST_1')[0].value}&Zip=${document.getElementsByName('Guarantor_Zip_1')[0].value}`,'usps_ajax.pl')" ONMOUSEOUT="window.status=''">(check address)</A>
    </TD>
    <INPUT TYPE="hidden" NAME="Guarantor_addressVerified_1" VALUE="<<Guarantor_addressVerified_1>>" >
  </TR>
  <TR>
    <TD></TD>
    <TD>
      [[DBUtil->isEQ(<<<LOGINPROVID>>>+91) <A HREF="javascript:void(0);" id="Guarantor_AddressManualInput_Link">Enter address manually</A>]]
      [[myHTML->clientAddressForm(%form+Guarantor_AddressManualInput+Guarantor_+2)]]
    </TD>
  </TR>
  <TR > <TD CLASS="port hdrtxt" COLSPAN="3" >Phone Numbers</TD> </TR>
  <TR >
    <TD CLASS="strcol" WIDTH="30%" >Home Phone</TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="TEL" NAME="Guarantor_HmPh_1" VALUE="<<Guarantor_HmPh_1>>" ONFOCUS="select()" ONCHANGE="return vPhone(this);" SIZE=20>
    </TD>
  </TR>
  <TR >
    <TD CLASS="strcol" WIDTH="30%" >Work Phone</TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="TEL" NAME="Guarantor_WkPh_1" VALUE="<<Guarantor_WkPh_1>>" ONFOCUS="select()" ONCHANGE="return vPhone(this);" SIZE=20>
    </TD>
  </TR>
  <TR >
    <TD CLASS="strcol" WIDTH="30%" >Cell Phone</TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="TEL" NAME="Guarantor_MobPh_1" VALUE="<<Guarantor_MobPh_1>>" ONFOCUS="select()" ONCHANGE="return vPhone(this);" SIZE=20>
  </TR>
  <TR >
    <TD CLASS="strcol" WIDTH="30%" >Fax</TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="TEL" NAME="Guarantor_Fax_1" VALUE="<<Guarantor_Fax_1>>" ONFOCUS="select()" ONCHANGE="return vPhone(this);" SIZE=20>
    </TD>
  </TR>
  <TR >
    <TD CLASS="strcol" WIDTH="30%" >Pager</TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="TEL" NAME="Guarantor_Pgr_1" VALUE="<<Guarantor_Pgr_1>>" ONFOCUS="select()" ONCHANGE="return vPhone(this);" SIZE=20>
    </TD>
  </TR>
  <TR >
    <TD CLASS="strcol" WIDTH="30%" >Other Phone</TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="TEL" NAME="Guarantor_OthPh_1" VALUE="<<Guarantor_OthPh_1>>" ONFOCUS="select()" ONCHANGE="return vPhone(this);" SIZE=20>
    </TD>
  </TR>
  <TR >
    <TD CLASS="strcol" WIDTH="30%" >Other Phone Description</TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="TEXT" NAME="Guarantor_OthPhLbl_1" VALUE="<<Guarantor_OthPhLbl_1>>" ONFOCUS="select()" SIZE=20>
    </TD>
  </TR>
  <TR > <TD CLASS="port hdrtxt" COLSPAN="3" >Demographics</TD> </TR>
  <TR >
    <TD CLASS="strcol" WIDTH="30%" >SSN</TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="TEXT" NAME="Guarantor_SSN_1" VALUE="<<Guarantor_SSN_1>>" ONFOCUS="select()" ONCHANGE="return vSSN(this);" SIZE=11>
    </TD>
  </TR>
  <TR >
    <TD CLASS="strcol" WIDTH="30%" >DOB</TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="TEXT" NAME="Guarantor_DOB_1" VALUE="<<Guarantor_DOB_1>>" ONFOCUS="select()" ONCHANGE="return vDate(this,0,this.form,'Guarantor_Age');" SIZE=10>
    </TD>
  </TR>
  <TR >
    <TD CLASS="strcol" WIDTH="30%" >AGE</TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="TEXT" NAME="Guarantor_Age" VALUE="<<Guarantor_Age>>" ONFOCUS="this.blur()" SIZE=4 >
    </TD>
  </TR>
  <TR >
    <TD CLASS="strcol" WIDTH="30%" >Birth Gender</TD>
    <TD CLASS="strcol" >
      <SELECT NAME="Guarantor_Gend_1">[[DBA->selxTable(%form+xGend+<<Guarantor_Gend_1>>)]]</SELECT> 
    </TD>
  </TR>
  <TR >
    <TD CLASS="strcol" WIDTH="30%" >Race</TD>
    <TD CLASS="strcol" >
      <SELECT NAME="Guarantor_Race_1" >
        [[DBA->selxTable(%form+xRaces+<<Guarantor_Race_1>>+Descr)]]
      </SELECT> 
    </TD>
  </TR>
  <TR >
    <TD CLASS="strcol" WIDTH="30%" >Marital Status</TD>
    <TD CLASS="strcol" >
      <SELECT NAME="Guarantor_MarStat_1">[[DBA->selxTable(%form+xMarStat+<<Guarantor_MarStat_1>>+Descr Text)]]</SELECT> 
    </TD>
  </TR>
  <TR >
    <TD CLASS="strcol" WIDTH="30%" >Spouse Name</TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="TEXT" NAME="Guarantor_SName_1" VALUE="<<Guarantor_SName_1>>" ONFOCUS="select()" SIZE=20>
    </TD>
  </TR>
  <TR >
    <TD CLASS="strcol" WIDTH="30%" >Parental Status</TD>
    <TD CLASS="strcol" >
      <SELECT NAME="Guarantor_ParStat_1">[[DBA->selxTable(%form+xParentalStatus+<<Guarantor_ParStat_1>>)]]</SELECT> 
    </TD>
  </TR>
  <TR >
    <TD CLASS="strcol" WIDTH="30%" >Number of Children</TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="text" NAME="Guarantor_ChSum_1" VALUE="<<Guarantor_ChSum_1>>" ONFOCUS="select()" ONCHANGE="return vNum(this,0,10)" SIZE="10" >
    </TD>
  </TR>
  <TR >
    <TD CLASS="strcol" WIDTH="30%" >Employer</TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="TEXT" NAME="Guarantor_Empl_1" VALUE="<<Guarantor_Empl_1>>" ONFOCUS="select()" SIZE="60" >
    </TD>
  </TR>
  <TR >
    <TD CLASS="strcol" WIDTH="30%" >Position in Employment</TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="TEXT" NAME="Guarantor_EPos_1" VALUE="<<Guarantor_EPos_1>>" ONFOCUS="select()" SIZE="60" >
    </TD>
  </TR>
  <TR >
    <TD CLASS="strcol" WIDTH="30%" >Comments</TD>
    <TD CLASS="strcol" >
       <TEXTAREA NAME="Guarantor_GrtrComments_1" COLS=80 ROWS=5 WRAP="virtual" ><<Guarantor_GrtrComments_1>></TEXTAREA>
    </TD>
  </TR>
</TABLE>
<TABLE CLASS="main fullsize" >
  <TR>
    <TD CLASS="numcol" >
      <INPUT TYPE="submit" ONCLICK="return validate(this.form);" NAME="UpdateTables=all&misPOP=1" VALUE="Add/Update">
      
      [[SysAccess->isHelpDesk(%form) <INPUT TYPE="submit" ONCLICK="return vDELETE('Are you sure you want to delete this record?');" NAME="Insurance_DELETE_1=1&UpdateTables=all&misPOP=1" VALUE="Delete"> ]]

    </TD>
  </TR>
</TABLE>

<INPUT TYPE="hidden" NAME="post_update" VALUE="PostUpd->updPA(%form+<<<Client_ClientID_1>>>)" >
</LOADHIDDEN>
</FORM>
<SCRIPT LANGUAGE="JavaScript">
document.Insurance.elements[0].focus();
</SCRIPT>

[[myHTML->rightpane(%form+search)]]
<script src="https://maps.googleapis.com/maps/api/js?key=AIzaSyAG2JfgYWgk7Q3FDfZQJauF-M4o4H1wqVw&libraries=places&callback=initAutocomplete"
        async defer></script>
<SCRIPT type="text/javascript" src="/src/cgi/js/vMCAutocomplete.js?v=202006082124"></SCRIPT>
<SCRIPT LANGUAGE="JavaScript" >
callAjax('xRelationship','','','&Autocomplete=MCAutocomplete&Target=Guarantor_ClientRel_1','popup.pl');
</SCRIPT>
<script LANGUAGE="JavaScript" src="/src/cgi/js/vClientAddressForm.js?v=202006242248"></script>
<script LANGUAGE="JavaScript">
$(document).ready(function() {
  initClientAddressForm('Guarantor_AddressManualInput', 'Guarantor_AddressManualInput_Link', 'Guarantor_', 2);
});
</script>
