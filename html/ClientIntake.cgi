[[myHTML->newPage(%form+Client Intake+++++lhcautocomplete)]]

<SCRIPT LANGUAGE="JavaScript" SRC="/cgi/js/NoEnter.js"> </SCRIPT>
<SCRIPT LANGUAGE="JavaScript" SRC="/cgi/js/vClientIntake.js?v=202009290648"> </SCRIPT>
<SCRIPT type="text/javascript" src="/cgi/js/ajaxrequest.js"></SCRIPT>
<SCRIPT LANGUAGE="JavaScript" SRC="/cgi/js/vDate.js?345345"> </SCRIPT>
<SCRIPT LANGUAGE="JavaScript" SRC="/cgi/js/vTime.js"> </SCRIPT>
<SCRIPT LANGUAGE="JavaScript" SRC="/cgi/js/vPhone.js"> </SCRIPT>
<SCRIPT LANGUAGE="JavaScript" SRC="/cgi/js/vNum.js"> </SCRIPT>
<SCRIPT LANGUAGE="JavaScript" SRC="/cgi/js/vZip.js"> </SCRIPT>
<SCRIPT type="text/javascript" src="/cgi/js/vCheckAddress.js?v=202006032043"></SCRIPT>
<SCRIPT TYPE="text/javascript" SRC="/cgi/jquery/jquery-1.12.4.js" ></SCRIPT>
<SCRIPT TYPE="text/javascript" src="https://ajax.googleapis.com/ajax/libs/jquery/3.3.1/jquery.min.js"></SCRIPT>
<script src="https://lhcforms-static.nlm.nih.gov/autocomplete-lhc-versions/17.0.3/autocomplete-lhc.min.js"></script>
<SCRIPT TYPE="text/javascript" SRC="/cgi/jquery/jquery-ui-1.12.1/jquery-ui.min.js" ></SCRIPT>
<SCRIPT LANGUAGE="JavaScript" >
$(document).ready(function() {
  var addressVerified = document.getElementsByName('Client_addressVerified_1')[0].value;
  if (addressVerified == 1) {
    document.getElementById('Client_Check_Address_1').innerHTML
      = `<img src="/images/check.jpg" width="20" height="20" style="vertical-align: middle;margin-right: 8px;"><span>Verified</span>`;
  }
  var addressVerifiedTransBy = document.getElementsByName('ClientReferrals_TransaddressVerified_1')[0].value;
  if (addressVerifiedTransBy == 1) {
    document.getElementById('ClientReferrals_TransCheck_Address_1').innerHTML
      = `<img src="/images/check.jpg" width="20" height="20" style="vertical-align: middle;margin-right: 8px;"><span>Verified</span>`;
  }

  var homeless = $("#Client_Homeless_1").prop("checked");
  showAddrFormFields(homeless);

  if ($("INPUT[NAME='Client_Addr1_1']").val() === "Homeless-Streets") {
    $("#Homeless-Streets").prop("checked", true);
    $("INPUT[NAME='Client_Zip_1']").prop('readonly', true);
    $("INPUT[NAME='Client_Zip_1']").css('pointer-events', 'none');
    $("INPUT[NAME='Client_Zip_1']").css('background-color', '#E9ECEF');
  }
  if ($("INPUT[NAME='Client_Addr1_1']").val() === "Homeless-Shelter") {
    $("#Homeless-Shelter").prop("checked", true);
    $("INPUT[NAME='Client_Zip_1']").prop('readonly', false);
    $("INPUT[NAME='Client_Zip_1']").css('pointer-events', 'auto');
    $("INPUT[NAME='Client_Zip_1']").css('background-color', 'white');
  }

  $("#Client_Homeless_1").click(function() {
    var homeless = $(this).prop("checked");
    initAddrForm(homeless);
  });

  $("#Homeless-Streets").click(function() {
    $("INPUT[NAME='Client_Addr1_1']").val('Homeless-Streets');
    $("INPUT[NAME='Client_Zip_1']").val('99999');
    $("INPUT[NAME='Client_Zip_1']").prop('readonly', true);
    $("INPUT[NAME='Client_Zip_1']").css('pointer-events', 'none');
    $("INPUT[NAME='Client_Zip_1']").css('background-color', '#E9ECEF');
  });
  $("#Homeless-Shelter").click(function() {
    $("INPUT[NAME='Client_Addr1_1']").val('Homeless-Shelter');
    $("INPUT[NAME='Client_Zip_1']").prop('readonly', false);
    $("INPUT[NAME='Client_Zip_1']").css('pointer-events', 'auto');
    $("INPUT[NAME='Client_Zip_1']").css('background-color', 'white');
  });
});

function initAddrForm(homeless) {
  $("#autocomplete").val('');
  $("INPUT[NAME='Client_Addr1_1']").val('');
  $("INPUT[NAME='Client_Addr2_1']").val('');
  $("INPUT[NAME='Client_City_1']").val('');
  $("INPUT[NAME='Client_County_1']").val('');
  $("INPUT[NAME='Client_ST_1']").val('');
  $("INPUT[NAME='Client_Zip_1']").val('');

  $("#Homeless-Streets").prop("checked", false);
  $("#Homeless-Shelter").prop("checked", false);

  showAddrFormFields(homeless);
}

function showAddrFormFields(homeless) {
  if (homeless === true) {
    $("#autocomplete_FormField").hide();
    $("#Client_Addr2_FormField").hide();
    $("#Client_City_FormField").hide();
    $("#Client_County_FormField").hide();
    $("#Client_ST_FormField").hide();
    $("#Client_Check_Address_FormField").hide();

    $("#Homeless-Detail").show();
  } else {
    $("#autocomplete_FormField").show();
    $("#Client_Addr2_FormField").show();
    $("#Client_City_FormField").show();
    $("#Client_County_FormField").show();
    $("#Client_ST_FormField").show();
    $("#Client_Check_Address_FormField").show();

    $("#Homeless-Detail").hide();
  }
}

function initAutocomplete() {
  var autocomplete = new google.maps.places.Autocomplete(
      document.getElementById('autocomplete'), {types: []});
  autocomplete.setFields(['address_component']);
  autocomplete.addListener('place_changed', () => { fillInAddress(autocomplete, 'Client_'); });

  var autocompleteTransportedBy = new google.maps.places.Autocomplete(
      document.getElementById('autoCompleteTransportedBy'), {types: []});
  autocompleteTransportedBy.setFields(['address_component']);
  autocompleteTransportedBy.addListener('place_changed', () => { fillInAddress(autocompleteTransportedBy, 'ClientReferrals_Trans', 1); });
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
  <TR ><TD CLASS="port hdrtxt" COLSPAN="2" >REFERRAL SOURCE / REASON</TD></TR>
  <TR >
    <TD CLASS="strcol" >&nbsp;</TD>
    <TD CLASS="strcol" >ie: or you may enter partial zipcode</TD>
  </TR>
  <TR >
    <TD CLASS="strcol" >Primary Referral</TD>
    <TD CLASS="strcol" >
      Search: <INPUT ID="LHCAutocompletePrimaryReferral" TYPE="text" VALUE="[[DBA->getxref(%form+xNPI+<<<ClientReferrals_ReferredBy1NPI_1>>>+Type ProvOrgName NPI+++ - )]]" ONFOCUS="select()" SIZE="60" />
      <INPUT TYPE="hidden" ID="ClientReferrals_ReferredBy1NPI_1" NAME="ClientReferrals_ReferredBy1NPI_1" VALUE="<<ClientReferrals_ReferredBy1NPI_1>>" >
    </TD>
  </TR>
  <TR >
    <TD CLASS="strcol" >Referral Type</TD>
    <TD CLASS="strcol" >
      <SELECT NAME="ClientReferrals_ReferredBy1Type_1" >
        [[DBA->selxTable(%form+xReferralTypes+<<ClientReferrals_ReferredBy1Type_1>>+CDC Descr)]]
      </SELECT>
    </TD>
  </TR>
  <TR >
    <TD CLASS="strcol" >Alternate Contact Person</TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="text" NAME="ClientReferrals_ReferredCont1_1" VALUE="<<ClientReferrals_ReferredCont1_1>>" ONFOCUS="select()" SIZE="30" MAXLENGTH="30" >
    </TD>
  </TR>
  <TR >
    <TD CLASS="strcol" >Referral Date</TD>
    <TD CLASS="strcol" >
      <INPUT TYPE=text NAME="ClientReferrals_RefDate_1" VALUE="<<ClientReferrals_RefDate_1>>" ONFOCUS="select()" ONCHANGE="return vDate(this)" MAXLENGTH="10" SIZE="10" >
      Expire Date
      <INPUT TYPE=text NAME="ClientReferrals_ExpDate_1" VALUE="<<ClientReferrals_ExpDate_1>>" ONFOCUS="select()" ONCHANGE="return vDate(this)" MAXLENGTH="10" SIZE="10" >
    </TD>
  </TR>
  <TR >
    <TD CLASS="strcol" >Secondary Referral</TD>
    <TD CLASS="strcol" >
      Search: <INPUT ID="LHCAutocompleteSecondaryReferral" TYPE="text" VALUE="[[DBA->getxref(%form+xNPI+<<<ClientReferrals_ReferredBy2NPI_1>>>+Type ProvOrgName NPI+++ - )]]" ONFOCUS="select()" SIZE="60" />
      <INPUT TYPE="hidden" ID="ClientReferrals_ReferredBy2NPI_1" NAME="ClientReferrals_ReferredBy2NPI_1" VALUE="<<ClientReferrals_ReferredBy2NPI_1>>" >
    </TD>
  </TR>
  <TR >
    <TD CLASS="strcol" >Referral Type</TD>
    <TD CLASS="strcol" >
      <SELECT NAME="ClientReferrals_ReferredBy2Type_1" >
        [[DBA->selxTable(%form+xReferralTypes+<<ClientReferrals_ReferredBy2Type_1>>+CDC Descr)]]
      </SELECT>
    </TD>
  </TR>
  <TR >
    <TD CLASS="strcol" >Alternate Contact Person</TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="text" NAME="ClientReferrals_ReferredCont2_1" VALUE="<<ClientReferrals_ReferredCont2_1>>" ONFOCUS="select()" SIZE="30" MAXLENGTH="30" >
    </TD>
  </TR>
  <TR >
    <TD CLASS="strcol" >Referral Date</TD>
    <TD CLASS="strcol" >
      <INPUT TYPE=text NAME="ClientReferrals_RefDate2_1" VALUE="<<ClientReferrals_RefDate2_1>>" ONFOCUS="select()" ONCHANGE="return vDate(this)" MAXLENGTH="10" SIZE="10" >
    </TD>
  </TR>
  <TR > <TD CLASS="strcol" COLSPAN="2" ><HR></TD> </TR>
  <TR >
    <TD CLASS="strcol" >Reason for Hospitalization (Procedure)</TD>
    <TD CLASS="strcol" >
      <SELECT NAME="ClientReferrals_InPatientProcCode_1" >
        [[DBA->selxTable(%form+xInPatientProcedures+<<ClientReferrals_InPatientProcCode_1>>+ConceptName ConceptCode)]]
      </SELECT>
    </TD>
  </TR>
  <TR >
    <TD CLASS="strcol" >Hospitalization Discharge Status</TD>
    <TD CLASS="strcol" >
      <SELECT NAME="ClientReferrals_InPatientDisStatus_1" >
        [[DBA->selxTable(%form+xDischargeStatus+<<ClientReferrals_InPatientDisStatus_1>>+ConceptName ConceptCode)]]
      </SELECT>
    </TD>
  </TR>
  <TR > <TD CLASS="strcol" COLSPAN="2" ><HR></TD> </TR>
  <TR >
    <TD CLASS="strcol" >Referring Physician</TD>
    <TD CLASS="strcol" >
      Search: <INPUT ID="LHCAutocompleteReferringPhysician" TYPE="text" VALUE="[[DBA->getxref(%form+xNPI+<<<ClientReferrals_RefPhysNPI_1>>>+ProvLastName ProvFirstName NPI+++ - )]]" ONFOCUS="select()" SIZE="60" />
      <INPUT TYPE="hidden" ID="ClientReferrals_RefPhysNPI_1" NAME="ClientReferrals_RefPhysNPI_1" VALUE="<<ClientReferrals_RefPhysNPI_1>>" >
    </TD>
  </TR>
  <TR >
    <TD CLASS="strcol" >Referral Date</TD>
    <TD CLASS="strcol" >
      <INPUT TYPE=text NAME="ClientReferrals_RefPhysDate_1" VALUE="<<ClientReferrals_RefPhysDate_1>>" ONFOCUS="select()" ONCHANGE="return vDate(this)" MAXLENGTH="10" SIZE="10" >
    </TD>
  </TR>
  <TR >
    <TD CLASS="strcol" >Transport Contact</TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="text" NAME="ClientReferrals_TransBy_1" VALUE="<<ClientReferrals_TransBy_1>>" ONFOCUS="select()" SIZE="80" >
    </TD>
  </TR>
  <TR >
    <TD CLASS="strcol" >Enter Address</TD>
    <TD CLASS="strcol" >
      <input id="autoCompleteTransportedBy"
             type="text"
             size="50"/>
    </TD>
  </TR>
  <TR >
    <TD CLASS="strcol" >Address</TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="text" NAME="ClientReferrals_TransAddr_1" VALUE="<<ClientReferrals_TransAddr_1>>" ONFOCUS="select()" SIZE="30" style="pointer-events: none;background-color:#E9ECEF" >
    </TD>
  </TR>
  <TR >
    <TD CLASS="strcol" >City</TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="text" NAME="ClientReferrals_TransCity_1" VALUE="<<ClientReferrals_TransCity_1>>" ONFOCUS="select()" SIZE="20" style="pointer-events: none;background-color:#E9ECEF" >
    </TD>
  </TR>
  <TR >
    <TD CLASS="strcol" >County</TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="text" NAME="ClientReferrals_TransCounty_1" VALUE="<<ClientReferrals_TransCounty_1>>" ONFOCUS="select()" SIZE="20" style="pointer-events: none;background-color:#E9ECEF" >
    </TD>
  </TR>
  <TR >
    <TD CLASS="strcol" >State</TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="text" NAME="ClientReferrals_TransST_1" VALUE="<<ClientReferrals_TransST_1>>" ONFOCUS="select()" SIZE="20" style="pointer-events: none;background-color:#E9ECEF" >
    </TD>
  </TR>
  <TR >
    <TD CLASS="strcol" >Zip</TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="text" NAME="ClientReferrals_TransZip_1" VALUE="<<ClientReferrals_TransZip_1>>" ONFOCUS="select()" SIZE="20" style="pointer-events: none;background-color:#E9ECEF" >
    </TD>
  </TR>
  <TR >
    <TD ></TD>
    <TD id="ClientReferrals_TransCheck_Address_1">
      <A HREF="javascript:callAjax('checkAddress','','',`&Tag=Address&Prefix=ClientReferrals_Trans&AddrSize=1&Addr1=${document.getElementsByName('ClientReferrals_TransAddr_1')[0].value}&Addr2=&City=${document.getElementsByName('ClientReferrals_TransCity_1')[0].value}&State=${document.getElementsByName('ClientReferrals_TransST_1')[0].value}&Zip=${document.getElementsByName('ClientReferrals_TransZip_1')[0].value}`,'usps_ajax.pl')" ONMOUSEOUT="window.status=''">(check address)</A>
    </TD>
    <INPUT TYPE="hidden" NAME="ClientReferrals_TransaddressVerified_1" VALUE="<<ClientReferrals_TransaddressVerified_1>>" >
  </TR>
  <TR>
    <TD></TD>
    <TD>
      [[DBUtil->isEQ(<<<LOGINPROVID>>>+91) <A HREF="javascript:void(0);" id="Trans_AddressManualInput_Link">Enter address manually</A>]]
      [[DBUtil->isEQ(<<<LOGINPROVID>>>+90) <A HREF="javascript:void(0);" id="Trans_AddressManualInput_Link">Enter address manually</A>]]
      [[DBUtil->isEQ(<<<LOGINPROVID>>>+89) <A HREF="javascript:void(0);" id="Trans_AddressManualInput_Link">Enter address manually</A>]]
      [[myHTML->clientAddressForm(%form+Trans_AddressManualInput+ClientReferrals_Trans+1)]]
    </TD>
  </TR>
  <TR >
    <TD CLASS="strcol" >Phone</TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="TEL" NAME="ClientReferrals_TransPh_1" VALUE="<<ClientReferrals_TransPh_1>>" ONFOCUS="select()" ONCHANGE="return vPhone(this)" SIZE="20" >
    </TD>
  </TR>
  <TR > <TD CLASS="strcol" COLSPAN="2" ><HR></TD> </TR>
  <TR >
    <TD CLASS="strcol" >
      Is Patient's Condition Related to:
    </TD>
    <TD CLASS="strcol" >
      Employment (Current or Present) 
        <INPUT TYPE="radio" NAME="ClientReferrals_Employed_1" VALUE="1" <<ClientReferrals_Employed_1=1>> > yes
        <INPUT TYPE="radio" NAME="ClientReferrals_Employed_1" VALUE="0" <<ClientReferrals_Employed_1=0>> > no
      <BR>
      Auto Accident? 
        <INPUT TYPE="radio" NAME="ClientReferrals_AutoAccident_1" VALUE="1" <<ClientReferrals_AutoAccident_1=1>> > yes
        <INPUT TYPE="radio" NAME="ClientReferrals_AutoAccident_1" VALUE="0" <<ClientReferrals_AutoAccident_1=0>> > no
      <BR>
      Place (State) OK
        <SELECT NAME="ClientReferrals_AutoAccidentST_1">
          [[DBA->selxTable(%form+xState+<<ClientReferrals_AutoAccidentST_1>>+Descr)]]
        </SELECT>
      <BR>
      Other Accident? 
        <INPUT TYPE="radio" NAME="ClientReferrals_OtherAccident_1" VALUE="1" <<ClientReferrals_OtherAccident_1=1>> > yes
        <INPUT TYPE="radio" NAME="ClientReferrals_OtherAccident_1" VALUE="0" <<ClientReferrals_OtherAccident_1=0>> > no
    </TD>
  </TR>
  <TR > <TD CLASS="strcol" COLSPAN="2" >Initial Referral Questionnaire</TD> </TR>
  <TR >
    <TD CLASS="strcol" >#1. Reason for Referral</TD>
    <TD CLASS="strcol" >
       <TEXTAREA NAME="ClientReferrals_RefReason_1" COLS="70" ROWS="3" WRAP="virtual" ><<ClientReferrals_RefReason_1>></TEXTAREA>
    </TD>
  </TR>
  <TR >
    <TD CLASS="strcol" >
      #2. (Tobacco) Do you Use Tobacco?
    </TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="radio" NAME="ClientReferrals_UseTobacco_1" VALUE="1" <<ClientReferrals_UseTobacco_1=1>> > yes
      <INPUT TYPE="radio" NAME="ClientReferrals_UseTobacco_1" VALUE="0" <<ClientReferrals_UseTobacco_1=0>> > no
    </TD>
  </TR>
  <TR >
    <TD CLASS="strcol indent" >
      Are you interested in Tobacco Cessation?
    </TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="radio" NAME="ClientReferrals_TobaccoCessation_1" VALUE="1" <<ClientReferrals_TobaccoCessation_1=1>> > yes
      <INPUT TYPE="radio" NAME="ClientReferrals_TobaccoCessation_1" VALUE="0" <<ClientReferrals_TobaccoCessation_1=0>> > no
    </TD>
  </TR>
  <tr>
    <td class="strcol">
      #3. Risk
    </td>
  </tr>
  <tr>
    <td class="strcol indent">
      a. Does this individual pose a danger to themselves or others?
    </td>
    <td class="strcol">
      <input type="radio" name="ClientReferrals_Harmfulintent_1" value="0" checked=""> Neither

      <input type="radio" name="ClientReferrals_Harmfulintent_1" value="1" <<ClientReferrals_Harmfulintent_1=1>> > Suicidal

      <input type="radio" name="ClientReferrals_Harmfulintent_1" value="2" <<ClientReferrals_Harmfulintent_1=2>> > Homicidal

      <input type="radio" name="ClientReferrals_Harmfulintent_1" value="3" <<ClientReferrals_Harmfulintent_1=3>> > Both
    </td>
  </tr>
  <tr>
    <td class="strcol indent" style="padding-left:55px">
      (i) Do you have a plan?
    </td>
    <td class="strcol">
      <input type="radio" name="ClientReferrals_SuicidePlan_1" value="1" <<ClientReferrals_SuicidePlan_1=1>> > yes
      <input type="radio" name="ClientReferrals_SuicidePlan_1" value="" <<ClientReferrals_SuicidePlan_1=>> > no
    </td>
  </tr>
  <tr>
    <td class="strcol indent" style="padding-left:55px">
      (ii). Do you have thoughts of hurting others?
    </td>
    <td class="strcol">
      <input type="radio" name="ClientReferrals_RiskOthers_1" value="1" <<ClientReferrals_RiskOthers_1=1>> > yes
      <input type="radio" name="ClientReferrals_RiskOthers_1" value=""  <<ClientReferrals_RiskOthers_1=>> > no
    </td>
  </tr>
  <TR >
    <TD CLASS="strcol" >
      #4. (Trauma) Have you experienced or witnessed trauma?
    </TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="radio" NAME="ClientReferrals_WitnessTrauma_1" VALUE="1" <<ClientReferrals_WitnessTrauma_1=1>> > yes
      <INPUT TYPE="radio" NAME="ClientReferrals_WitnessTrauma_1" VALUE="0" <<ClientReferrals_WitnessTrauma_1=0>> > no
    </TD>
  </TR>
  <TR >
    <TD CLASS="strcol" >
      #5. (Drugs/Alcohol) Do you currently use Alcohol or Drugs?
    </TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="radio" NAME="ClientReferrals_UseAlcoholDrugs_1" VALUE="1" <<ClientReferrals_UseAlcoholDrugs_1=1>> > yes
      <INPUT TYPE="radio" NAME="ClientReferrals_UseAlcoholDrugs_1" VALUE="0" <<ClientReferrals_UseAlcoholDrugs_1=0>> > no
    </TD>
  </TR>
  <TR >
    <TD CLASS="strcol indent" >
      Will you be receiving treatment here for that?
    </TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="radio" NAME="ClientReferrals_RecieveADT_1" VALUE="1" <<ClientReferrals_RecieveADT_1=1>> > yes
      <INPUT TYPE="radio" NAME="ClientReferrals_RecieveADT_1" VALUE="0" <<ClientReferrals_RecieveADT_1=0>> > no
    </TD>
  </TR>
  <TR >
    <TD CLASS="strcol" >
      #6. (Mood) Do you experience excessive Anxiety/Worry?
    </TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="radio" NAME="ClientReferrals_MoodDisorder_1" VALUE="1" <<ClientReferrals_MoodDisorder_1=1>> > yes
      <INPUT TYPE="radio" NAME="ClientReferrals_MoodDisorder_1" VALUE="0" <<ClientReferrals_MoodDisorder_1=0>> > no
    </TD>
  </TR>
  <TR >
    <TD CLASS="strcol tophdr" COLSPAN="2" >
      A YES INDICATES A SCREENING NEEDS COMPLETED.
      Give this to the assigned Case Manager to complete appropriate Screenings before Assessment.
      Schedule the Assessment Intake.
    </TD>
  </TR>
</TABLE>
<TABLE CLASS="home fullsize" >
  <TR ><TD CLASS="port hdrtxt" COLSPAN="2" >I. Initial Intake Information</TD></TR>
  <TR >
    <TD CLASS="strcol" >Return to referral source?</TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="radio" NAME="ClientReferrals_ReturnToRef_1" VALUE=0 <<ClientReferrals_ReturnToRef_1=0>> > No
      <INPUT TYPE="radio" NAME="ClientReferrals_ReturnToRef_1" VALUE=1 <<ClientReferrals_ReturnToRef_1=1>> > Yes
    </TD>
  </TR>
  <TR >
    <TD CLASS="strcol" >Inappropriate/Ineligible for services, Referred to</TD>
    <TD CLASS="strcol" >
      Search: <INPUT ID="LHCAutocompleteReferredto" TYPE="text" VALUE="[[DBA->getxref(%form+xNPI+<<<ClientReferrals_ReferredToNPI_1>>>+Type ProvOrgName NPI+++ - )]]" ONFOCUS="select()" SIZE="60" />
      <INPUT TYPE="hidden" ID="ClientReferrals_ReferredToNPI_1" NAME="ClientReferrals_ReferredToNPI_1" VALUE="<<ClientReferrals_ReferredToNPI_1>>" >
    </TD>
  </TR>
  <TR >
    <TD CLASS="strcol" >Intake Date/Time/Provider<BR>(entered by eg. H0031 or 90801 note)</TD>
    <TD CLASS="strcol" >
<SPAN ID="ListClientAdmits" >
[[myHTML->ListSel(%form+ListClientAdmits+<<<Client_ClientID>>>+<<<LINKID>>>+<<<Client_Locked_1>>>)]]
</SPAN>
    </TD>
  </TR>
</TABLE>
<TABLE CLASS="home fullsize" >
  <TR ><TD CLASS="port hdrtxt" COLSPAN="2" >IDENTIFING INFORMATION</TD></TR>
  <TR ><TD CLASS="port hdrtxt" >Name and Address</TD><TD>&nbsp;</TD></TR>
  <TR >
    <TD CLASS="strcol" >First Name</TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="text" NAME="Client_FName_1" VALUE="<<Client_FName_1>>" ONCHANGE="return stringFilter(this,'!@#$%^&*()',1,0,1);" ONFOCUS="select()" SIZE="20" >
    </TD>
  </TR>
  <TR >
    <TD CLASS="strcol" >Last Name</TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="text" NAME="Client_LName_1" VALUE="<<Client_LName_1>>" ONCHANGE="return stringFilter(this,'!@#$%^&*()',1,0,1);" ONFOCUS="select()" SIZE="20" >
    </TD>
  </TR>
  <TR >
    <TD CLASS="strcol" >Maiden Name</TD>
    <TD CLASS="strcol" >
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
      <SELECT NAME="Client_Suffix_1">
        [[DBA->selxTable(%form+xSuffix+<<Client_Suffix_1>>+Descr)]]
      </SELECT>
    </TD>
  </TR>
  <TR >
    <TD CLASS="strcol" >Homeless</TD>
    <TD>
      <INPUT TYPE="checkbox" ID="Client_Homeless_1" NAME="Client_Homeless_1" VALUE="1" <<Client_Homeless_1=checkbox>> >&nbsp;
      <SPAN ID="Homeless-Detail" >
        <INPUT TYPE="radio" NAME="Homeless_Detail" VALUE="Homeless-Streets" ID="Homeless-Streets" > Homeless streets
        <INPUT TYPE="radio" NAME="Homeless_Detail" VALUE="Homeless-Shelter" ID="Homeless-Shelter" > Homeless shelter
      </SPAN>
    </TD>
  </TR>
  <TR ID="autocomplete_FormField" >
    <TD CLASS="strcol" >Enter Address</TD>
    <TD CLASS="strcol" >
      <input id="autocomplete"
             type="text"
             size="50"/>
    </TD>
  </TR>
  <TR ID="Client_Addr1_FormField">
    <TD CLASS="strcol" >Address 1</TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="text" NAME="Client_Addr1_1" VALUE="<<Client_Addr1_1>>" SIZE="30" readonly style="pointer-events: none;background-color:#E9ECEF" >
    </TD>
  </TR>
  <TR ID="Client_Addr2_FormField" >
    <TD CLASS="strcol" >Enter PO Box or Apt #</TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="text" NAME="Client_Addr2_1" VALUE="<<Client_Addr2_1>>" SIZE="30" ONKEYUP="onChangeAddr2('Client_', this.value)" >
    </TD>
  </TR>
  <TR ID="Client_City_FormField" >
    <TD CLASS="strcol" >City</TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="text" NAME="Client_City_1" VALUE="<<Client_City_1>>" SIZE="20" readonly style="pointer-events: none;background-color:#E9ECEF" >
    </TD>
  </TR>
  <TR ID="Client_County_FormField" >
    <TD CLASS="strcol" >County</TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="text" NAME="Client_County_1" VALUE="<<Client_County_1>>" SIZE="20" readonly style="pointer-events: none;background-color:#E9ECEF" >
    </TD>
  </TR>
  <TR ID="Client_ST_FormField" >
    <TD CLASS="strcol" >State</TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="text" NAME="Client_ST_1" VALUE="<<Client_ST_1>>" SIZE="20" readonly style="pointer-events: none;background-color:#E9ECEF" >
    </TD>
  </TR>
  <TR ID="Client_Zip_FormField" >
    <TD CLASS="strcol" >Zip</TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="text" NAME="Client_Zip_1" VALUE="<<Client_Zip_1>>" SIZE="20" readonly style="pointer-events: none;background-color:#E9ECEF" >
    </TD>
  </TR>
  <TR ID="Client_Check_Address_FormField" >
    <TD ></TD>
    <TD id="Client_Check_Address_1">
      <A HREF="javascript:callAjax('checkAddress','','',`&Tag=Address&Prefix=Client_&AddrSize=2&Addr1=${document.getElementsByName('Client_Addr1_1')[0].value}&Addr2=${document.getElementsByName('Client_Addr2_1')[0].value}&City=${document.getElementsByName('Client_City_1')[0].value}&State=${document.getElementsByName('Client_ST_1')[0].value}&Zip=${document.getElementsByName('Client_Zip_1')[0].value}`,'usps_ajax.pl')" ONMOUSEOUT="window.status=''">(check address)</A>
    </TD>
    <INPUT TYPE="hidden" NAME="Client_addressVerified_1" VALUE="<<Client_addressVerified_1>>" >
  </TR>
  <TR >
    <TD></TD>
    <TD>
      [[DBUtil->isEQ(<<<LOGINPROVID>>>+91) <A HREF="javascript:void(0);" id="Client_AddressManualInput_Link">Enter address manually</A>]]
      [[DBUtil->isEQ(<<<LOGINPROVID>>>+90) <A HREF="javascript:void(0);" id="Client_AddressManualInput_Link">Enter address manually</A>]]
      [[DBUtil->isEQ(<<<LOGINPROVID>>>+89) <A HREF="javascript:void(0);" id="Client_AddressManualInput_Link">Enter address manually</A>]]
      [[myHTML->clientAddressForm(%form+Client_AddressManualInput+Client_+2)]]
    </TD>
  </TR>
  <TR ><TD CLASS="port hdrtxt" >Phone Numbers</TD><TD>&nbsp;</TD></TR>
  <TR >
    <TD CLASS="strcol" >Home Phone</TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="TEL" NAME="Client_HmPh_1" VALUE="<<Client_HmPh_1>>" ONFOCUS="select()" ONCHANGE="return vPhone(this)" SIZE="20">
    </TD>
  </TR>
  <TR >
    <TD CLASS="strcol" >Work Phone</TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="TEL" NAME="Client_WkPh_1" VALUE="<<Client_WkPh_1>>" ONFOCUS="select()" ONCHANGE="return vPhone(this)" SIZE="20">
    </TD>
  </TR>
  <TR >
    <TD CLASS="strcol" >Cell Phone / Carrier</TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="TEL" NAME="Client_MobPh_1" VALUE="<<Client_MobPh_1>>" ONFOCUS="select()" ONCHANGE="return vPhone(this)" SIZE="20" >
      <SELECT NAME="Client_Carrier_1">
        [[DBA->selxTable(%form+xCarrier+<<Client_Carrier_1>>+Descr Access)]]
      </SELECT>
    </TD>
  </TR>
  <TR >
    <TD CLASS="strcol" >Email</TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="EMAIL" NAME="Client_Email_1" VALUE="<<Client_Email_1>>" ONFOCUS="select()" SIZE="30" >
    </TD>
  </TR>
  <TR ><TD CLASS="port hdrtxt" >Demographic Information</TD><TD>&nbsp;</TD></TR>
  <TR >
    <TD CLASS="strcol" >SSN</TD>
    <TD CLASS="strcol" ><<<Client_SSN_1>>></TD>
  </TR>
<TR>
    <TD CLASS="strcol" >Driver License Number</TD>
 <TD CLASS="strcol" ><INPUT TYPE="text" NAME="Client_DLNum_1" VALUE="<<Client_DLNum_1>>" ONFOCUS="select()" SIZE="15" ></TD>
</TR>
  <TR>
    <TD CLASS="strcol" >Driver License State</TD>
    <TD CLASS="strcol" >
      <SELECT NAME="Client_DLstate_1">
        [[DBA->selxTable(%form+xState+<<Client_DLstate_1>>+Descr)]]
      </SELECT>
    </TD>
 </TR>
  <TR >
    <TD CLASS="strcol" >Date of Birth</TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="date" NAME="Client_DOB_1" VALUE="<<Client_DOB_1>>" ONFOCUS="select()" ONCHANGE="return vDate(this,0,this.form,'Client_Age')" SIZE="10" >
      Age:
      <INPUT TYPE="text" NAME="Client_Age" ID="Client_Age" VALUE="<<Client_Age>>" ONFOCUS="form.ClientIntake_POB_1.focus();" SIZE="4" >
    </TD>
  </TR>
  <TR >
    <TD CLASS="strcol" >Place of Birth</TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="text" NAME="ClientIntake_POB_1" VALUE="<<ClientIntake_POB_1>>" ONFOCUS="select()" SIZE="35" >
    </TD>
  </TR>
  <TR >
    <TD CLASS="strcol" >Order of Birth</TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="text" NAME="ClientIntake_BirthOrder_1" VALUE="<<ClientIntake_BirthOrder_1>>" ONFOCUS="select()" ONCHANGE="vNum(this,1,20);" SIZE="12" >
    </TD>
  </TR>
  <TR >
    <TD CLASS="strcol" >Marital Status</TD>
    <TD CLASS="strcol" >
      <SELECT NAME="ClientRelations_MarStat_1">
        [[DBA->selxTable(%form+xMarStat+<<ClientRelations_MarStat_1>>+Descr Text)]]
      </SELECT>
    </TD>
  </TR>
  <TR >
    <TD CLASS="strcol" >Eyes</TD>
    <TD CLASS="strcol" >
      <SELECT NAME="Client_Eyes_1">
        [[DBA->selxTable(%form+xEyes+<<Client_Eyes_1>>+Descr)]]
      </SELECT>
    </TD>
  </TR>
  <TR >
    <TD CLASS="strcol" >Hair</TD>
    <TD CLASS="strcol" >
      <SELECT NAME="Client_Hair_1">
        [[DBA->selxTable(%form+xHair+<<Client_Hair_1>>+Descr)]]
      </SELECT>
    </TD>
  </TR>
  <TR >
    <TD CLASS="strcol" >Birth Gender</TD>
    <TD CLASS="strcol" >
      <SELECT NAME="Client_Gend_1">
        [[DBA->selxTable(%form+xGend+<<Client_Gend_1>>+Descr)]]
      </SELECT> 
    </TD>
  </TR>
  <TR >
    <TD CLASS="strcol" >
      [[myHTML->setxTable(%form+xRaces+<<Client_Race_1>>+Client_Race_1+checkbox+0)]]
    </TD>
    <TD CLASS="strcol" >
      <SPAN ID="Client_Race_1_display" ></SPAN>
    </TD>
  </TR>
  <TR >
    <TD CLASS="strcol" >
      [[myHTML->setxTable(%form+xEthnicity+<<Client_Ethnicity_1>>+Client_Ethnicity_1+checkbox+0)]]
    </TD>
    <TD CLASS="strcol" >
      <SPAN ID="Client_Ethnicity_1_display" ></SPAN>
    </TD>
  </TR>
</TABLE>
<TABLE CLASS="home fullsize" >
  <TR ><TD CLASS="port hdrtxt" COLSPAN="2" >Assigned Clinic</TD></TR>
  <TR >
    <TD CLASS="strcol" >Clinic Name</TD>
    <TD CLASS="strcol" >
      <SELECT NAME="Client_clinicClinicID_1" >[[DBA->selClinics(%form++<<Client_clinicClinicID_1>>++1)]]</SELECT>
    </TD>
  </TR>
</TABLE>
<TABLE CLASS="home fullsize" >
  <TR ><TD CLASS="port hdrtxt" COLSPAN="2" >Primary Insurance Information</TD></TR>
  <TR >
    <TD CLASS="strcol" >Insurance</TD>
    <TD CLASS="strcol" >
      <SELECT NAME="Insurance_InsID_1" >
        [[DBA->selInsurance(%form+<<Insurance_InsID_1>>)]]
      </SELECT> 
    </TD>
  </TR>
  <TR >
    <TD CLASS="strcol" >Insurance ID</TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="text" NAME="Insurance_InsIDNum_1" VALUE="<<Insurance_InsIDNum_1>>" ONFOCUS="select()" MAXLENGTH="30" SIZE="30" >
    </TD>
  </TR>
  <TR >
    <TD CLASS="strcol" >Effective</TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="text" NAME="Insurance_InsNumEffDate_1" VALUE="<<Insurance_InsNumEffDate_1>>" ONFOCUS="select()" ONCHANGE="return vDate(this);" SIZE="10" >
    </TD>
  </TR>
  <TR >
    <TD CLASS="strcol" >Expires</TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="text" NAME="Insurance_InsNumExpDate_1" VALUE="<<Insurance_InsNumExpDate_1>>" ONFOCUS="select()" ONCHANGE="return vDate(this);" SIZE="10" >
    </TD>
  </TR>
  <TR >
    <TD CLASS="strcol" >Deductible</TD>
    <TD CLASS="strcol" >$
      <INPUT TYPE="text" NAME="Insurance_Deductible_1" VALUE="<<Insurance_Deductible_1>>" ONFOCUS="select()" ONCHANGE="return vNum(this,0,3000);" SIZE="12" >
    </TD>
  </TR>
  <TR >
    <TD CLASS="strcol" >Copay</TD>
    <TD CLASS="strcol" >$
      <INPUT TYPE="text" NAME="Insurance_Copay_1" VALUE="<<Insurance_Copay_1>>" ONFOCUS="select()" ONCHANGE="return vNum(this,0,200);" SIZE="12" >
    </TD>
  </TR>
</TABLE>
<TABLE CLASS="main fullsize" >
  <TR>
    <TD CLASS="numcol" >
      <INPUT TYPE="submit" ONCLICK="return validate(this.form);" NAME="UpdateTables=all&[[myForm->genLink(ClientEmergency+ClientEmergency.cgi)]]" VALUE="Add/Update -> Client Emergency">
      <INPUT TYPE="submit" ONCLICK="return validate(this.form);" NAME="UpdateTables=all&misPOP=1" VALUE="Add/Update">
    </TD>
  </TR>
</TABLE>

<INPUT TYPE="hidden" NAME="ProviderID" VALUE="<<ProviderID>>" >
<INPUT TYPE="hidden" NAME="post_update" VALUE="PostUpd->updPA(%form+<<<Client_ClientID_1>>>)" >
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
  initClientAddressForm('Trans_AddressManualInput', 'Trans_AddressManualInput_Link', 'ClientReferrals_Trans', 1);
  initClientAddressForm('Client_AddressManualInput', 'Client_AddressManualInput_Link', 'Client_', 2);

  new Def.Autocompleter.Search(
    'LHCAutocompletePrimaryReferral',
    `/cgi/bin/popup_api.pl?method=Agency&mlt=<<mlt>>`,
    {tableFormat: true, valueCols: [0, 1, 6],
      colHeaders: ['Type', 'Org Name', 'Address', 'City', 'State', 'Zip', 'NPI']
    });
  Def.Autocompleter.Event.observeListSelections('LHCAutocompletePrimaryReferral', function(data) {
    var code = data.item_code;
    if (data.item_code === null) code = '';
    $('#ClientReferrals_ReferredBy1NPI_1').val(code);
  });

  new Def.Autocompleter.Search(
    'LHCAutocompleteSecondaryReferral',
    `/cgi/bin/popup_api.pl?method=Agency&mlt=<<mlt>>`,
    {tableFormat: true, valueCols: [0, 1, 6],
      colHeaders: ['Type', 'Org Name', 'Address', 'City', 'State', 'Zip', 'NPI']
    });
  Def.Autocompleter.Event.observeListSelections('LHCAutocompleteSecondaryReferral', function(data) {
    var code = data.item_code;
    if (data.item_code === null) code = '';
    $('#ClientReferrals_ReferredBy2NPI_1').val(code);
  });

  new Def.Autocompleter.Search(
    'LHCAutocompleteReferringPhysician',
    `/cgi/bin/popup_api.pl?method=Physicians&mlt=<<mlt>>`,
    {tableFormat: true, valueCols: [0, 1, 6],
      colHeaders: ['Last Name', 'First Name', 'Address', 'City', 'State', 'Zip', 'NPI']
    });
  Def.Autocompleter.Event.observeListSelections('LHCAutocompleteReferringPhysician', function(data) {
    var code = data.item_code;
    if (data.item_code === null) code = '';
    $('#ClientReferrals_RefPhysNPI_1').val(code);
  });

  new Def.Autocompleter.Search(
    'LHCAutocompleteReferredto',
    `/cgi/bin/popup_api.pl?method=Agency&mlt=<<mlt>>`,
    {tableFormat: true, valueCols: [0, 1, 6],
      colHeaders: ['Type', 'Org Name', 'Address', 'City', 'State', 'Zip', 'NPI']
    });
  Def.Autocompleter.Event.observeListSelections('LHCAutocompleteReferredto', function(data) {
    var code = data.item_code;
    if (data.item_code === null) code = '';
    $('#ClientReferrals_ReferredToNPI_1').val(code);
  });
});
</script>
