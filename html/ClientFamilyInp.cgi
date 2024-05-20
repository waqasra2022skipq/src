[[myHTML->newPage(%form+Family Member)]]

<SCRIPT LANGUAGE="JavaScript" SRC="/cgi/js/NoEnter.js"> </SCRIPT>
<SCRIPT LANGUAGE="JavaScript" SRC="/cgi/js/vEntry.js"> </SCRIPT>
<SCRIPT LANGUAGE="JavaScript" SRC="/cgi/js/vClientFamily.js"> </SCRIPT>
<SCRIPT LANGUAGE="JavaScript" SRC="/cgi/js/vZip.js"> </SCRIPT>
<SCRIPT LANGUAGE="JavaScript" SRC="/cgi/js/vNum.js"> </SCRIPT>
<SCRIPT LANGUAGE="JavaScript" SRC="/cgi/js/vPhone.js"> </SCRIPT>
<SCRIPT LANGUAGE="JavaScript" SRC="/cgi/js/vDate.js"> </SCRIPT>
<SCRIPT LANGUAGE="JavaScript" SRC="/cgi/js/ajaxrequest.js"> </SCRIPT>
<SCRIPT type="text/javascript" src="/cgi/js/vCheckAddress.js?v=202006032043"></SCRIPT>
<SCRIPT TYPE="text/javascript" SRC="/cgi/jquery/jquery-ui-1.11.2/jquery-ui.min.js" ></SCRIPT>
<LINK HREF="/cgi/css/autocomplete.css?v=202008071708" REL="stylesheet">
<SCRIPT LANGUAGE="JavaScript" >
$(document).ready(function() {
  var addressVerified = document.getElementsByName('ClientFamily_addressVerified_1')[0].value;
  if (addressVerified == 1) {
    document.getElementById('ClientFamily_Check_Address_1').innerHTML
      = `<img src="/images/check.jpg" width="20" height="20" style="vertical-align: middle;margin-right: 8px;"><span>Verified</span>`;
  }
});

function initAutocomplete() {
  var autocomplete = new google.maps.places.Autocomplete(
      document.getElementById('autocomplete'), {types: []});
  autocomplete.setFields(['address_component']);
  autocomplete.addListener('place_changed', () => { fillInAddress(autocomplete, 'ClientFamily_'); });
}
</SCRIPT>

<FORM NAME="ClientFamily" ACTION="/cgi/bin/mis.cgi" METHOD="POST" >
<TABLE CLASS="main fullsize" >
  <TR >
    <TD CLASS="strcol" >
      <<<Client_FName_1>>> <<<Client_MName_1>>> <<<Client_LName_1>>> (<<<Client_ClientID_1>>>) <<<Client_SSN_1>>>
      <BR>
      Family Member
    </TD>
    <TD CLASS="numcol" >[[gHTML->setLINKS(%form+back)]]</TD>
  </TR>
</TABLE>
<TABLE CLASS="home fullsize" >
  <TR ><TD CLASS="hdrtxt" COLSPAN="2" >Name/Relation</TD></TR>
  <TR >
    <TD CLASS="strcol" >First Name</TD>
    <TD CLASS="strcol" >
      <INPUT TYPE=text NAME="ClientFamily_FName_1" VALUE="<<ClientFamily_FName_1>>" ONFOCUS="select()" SIZE="20" >
    </TD>
  </TR>
  <TR >
    <TD CLASS="strcol" >Middle Name/Initial</TD>
    <TD CLASS="strcol" >
      <INPUT TYPE=text NAME="ClientFamily_MName_1" VALUE="<<ClientFamily_MName_1>>" ONFOCUS="select()" SIZE="20" >
    </TD>
  </TR>
  <TR >
    <TD CLASS="strcol" >Last Name</TD>
    <TD CLASS="strcol" >
      <INPUT TYPE=text NAME="ClientFamily_LName_1" VALUE="<<ClientFamily_LName_1>>" ONFOCUS="select()" SIZE="20" >
    </TD>
  </TR>
  <TR >
    <TD CLASS="strcol" >Suffix</TD>
    <TD CLASS="strcol" >
      <SELECT NAME="ClientFamily_Suffix_1">
        [[DBA->selxTable(%form+xSuffix+<<ClientFamily_Suffix_1>>+Descr)]]
      </SELECT>
    </TD>
  </TR>
  <TR >
    <TD CLASS="strcol" >Relationship</TD>
    <TD CLASS="strcol" >
      <INPUT ID="MCAutocomplete" TYPE="text" VALUE="[[DBA->getxref(%form+xRelationship+<<<ClientFamily_Rel_1>>>++,+++,)]]" ONFOCUS="select()" SIZE="20" />
      <INPUT TYPE="hidden" NAME="ClientFamily_Rel_1" VALUE="<<ClientFamily_Rel_1>>" >
    </TD>
  </TR>
  <TR >
    <TD CLASS="strcol" >Legal Guardian</TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="checkbox" NAME="ClientFamily_Guardian_1" VALUE=1 <<ClientFamily_Guardian_1=checkbox>> ONFOCUS="select()" >
    </TD>
  </TR>
  <TR >
    <TD CLASS="strcol" >If 18 or older? Guardian type</TD>
    <TD CLASS="strcol" >
      <SELECT NAME="ClientFamily_GuardianType_1">
        [[DBA->selxTable(%form+xGuardianType+<<ClientFamily_GuardianType_1>>+Descr)]]
      </SELECT>
    </TD>
  </TR>
  <TR >
    <TD CLASS="strcol" >Emergency Contact</TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="checkbox" NAME="ClientFamily_EmerContact_1" VALUE=1 <<ClientFamily_EmerContact_1=checkbox>> ONFOCUS="select()" >
    </TD>
  </TR>
</TABLE>
<TABLE CLASS="home fullsize" >
  <TR ><TD CLASS="hdrtxt" COLSPAN="4" >Demographic Information</TD></TR>
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
      <INPUT TYPE="TEXT" NAME="ClientFamily_Addr1_1" VALUE="<<ClientFamily_Addr1_1>>" SIZE="30" readonly style="pointer-events: none;background-color:#E9ECEF" >
    </TD>
  </TR>
  <TR >
    <TD CLASS="strcol" >Enter PO Box or Apt #</TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="TEXT" NAME="ClientFamily_Addr2_1" VALUE="<<ClientFamily_Addr2_1>>" SIZE="30" ONKEYUP="onChangeAddr2('ClientFamily_', this.value)" >
    </TD>
  </TR>
  <TR >
    <TD CLASS="strcol" >City</TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="TEXT" NAME="ClientFamily_City_1" VALUE="<<ClientFamily_City_1>>" SIZE="20" readonly style="pointer-events: none;background-color:#E9ECEF" >
    </TD>
  </TR>
  <TR >
    <TD CLASS="strcol" >County</TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="TEXT" NAME="ClientFamily_County_1" VALUE="<<ClientFamily_County_1>>" SIZE="20" readonly style="pointer-events: none;background-color:#E9ECEF" >
    </TD>
  </TR>
  <TR >
    <TD CLASS="strcol" >State</TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="text" NAME="ClientFamily_ST_1" VALUE="<<ClientFamily_ST_1>>" SIZE="20" readonly style="pointer-events: none;background-color:#E9ECEF" >
    </TD>
  </TR>
  <TR >
    <TD CLASS="strcol" >Zip</TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="text" NAME="ClientFamily_Zip_1" VALUE="<<ClientFamily_Zip_1>>" SIZE="20" readonly style="pointer-events: none;background-color:#E9ECEF" >
    </TD>
  </TR>
  <TR >
    <TD ></TD>
    <TD id="ClientFamily_Check_Address_1">
      <A HREF="javascript:callAjax('checkAddress','','',`&Tag=Address&Prefix=ClientFamily_&AddrSize=2&Addr1=${document.getElementsByName('ClientFamily_Addr1_1')[0].value}&Addr2=${document.getElementsByName('ClientFamily_Addr2_1')[0].value}&City=${document.getElementsByName('ClientFamily_City_1')[0].value}&State=${document.getElementsByName('ClientFamily_ST_1')[0].value}&Zip=${document.getElementsByName('ClientFamily_Zip_1')[0].value}`,'usps_ajax.pl')" ONMOUSEOUT="window.status=''">(check address)</A>
    </TD>
    <INPUT TYPE="hidden" NAME="ClientFamily_addressVerified_1" VALUE="<<ClientFamily_addressVerified_1>>" >
  </TR>
  <TR>
    <TD></TD>
    <TD>
      [[DBUtil->isEQ(<<<LOGINPROVID>>>+91) <A HREF="javascript:void(0);" id="ClientFamily_AddressManualInput_Link">Enter address manually</A>]]
      [[myHTML->clientAddressForm(%form+ClientFamily_AddressManualInput+ClientFamily_+2)]]
    </TD>
  </TR>
  <TR >
    <TD CLASS="strcol" >Home Phone</TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="TEL" NAME="ClientFamily_HmPh_1" VALUE="<<ClientFamily_HmPh_1>>" ONFOCUS="select()" ONCHANGE="return vPhone(this)" SIZE="20" >
    </TD>
  </TR>
  <TR >
    <TD CLASS="strcol" >Work Phone</TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="TEL" NAME="ClientFamily_WkPh_1" VALUE="<<ClientFamily_WkPh_1>>" ONFOCUS="select()" ONCHANGE="return vPhone(this)" SIZE="20" >
    </TD>
  </TR>
  <TR >
    <TD CLASS="strcol" >Cell Phone / Carrier</TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="TEL" NAME="ClientFamily_Cell_1" VALUE="<<ClientFamily_Cell_1>>" ONFOCUS="select()" ONCHANGE="return vPhone(this)" SIZE="20" >
      <SELECT NAME="ClientFamily_Carrier_1">
        [[DBA->selxTable(%form+xCarrier+<<ClientFamily_Carrier_1>>+Descr Access)]]
      </SELECT> 
    </TD>
  </TR>
  <TR >
    <TD CLASS="strcol" >Fax</TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="TEL" NAME="ClientFamily_Fax_1" VALUE="<<ClientFamily_Fax_1>>" ONFOCUS="select()" ONCHANGE="return vPhone(this)" SIZE="20" >
    </TD>
  </TR>
  <TR >
    <TD CLASS="strcol" >Other Phone</TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="TEL" NAME="ClientFamily_OthPh_1" VALUE="<<ClientFamily_OthPh_1>>" ONFOCUS="select()" ONCHANGE="return vPhone(this)" SIZE="20" >
    </TD>
  </TR>
  <TR >
    <TD CLASS="strcol" >Other Phone Label</TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="TEXT" NAME="ClientFamily_OthPhLbl_1" VALUE="<<ClientFamily_OthPhLbl_1>>" ONFOCUS="select()" SIZE="20" >
    </TD>
  </TR>
  <TR >
    <TD CLASS="strcol" >Email</TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="EMAIL" NAME="ClientFamily_Email_1" VALUE="<<ClientFamily_Email_1>>" ONFOCUS="select()" SIZE="30" >
    </TD>
  </TR>
  <TR >
    <TD CLASS="strcol" >SSN</TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="TEXT" NAME="ClientFamily_SSN_1" VALUE="<<ClientFamily_SSN_1>>" ONFOCUS="select()" ONCHANGE="return vSSN(this)" SIZE="11" >
  </TR>
  <TR >
    <TD CLASS="strcol" >Date of Birth</TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="TEXT" NAME="ClientFamily_DOB_1" VALUE="<<ClientFamily_DOB_1>>" ONFOCUS="select()" ONCHANGE="return vDate(this,0,this.form,'ClientFamily_Age_1')" SIZE="10" >
      Age:
      <INPUT TYPE=text NAME="ClientFamily_Age_1" VALUE="<<ClientFamily_Age_1>>" ONCHANGE="return vNum(this,1,99)" ONFOCUS="select()" >
  </TR>
  <TR >
    <TD CLASS="strcol" >Birth Gender</TD>
    <TD CLASS="strcol" >
      <SELECT NAME="ClientFamily_Gend_1">
        [[DBA->selxTable(%form+xGend+<<ClientFamily_Gend_1>>+Descr)]]
      </SELECT> 
  </TR>
  <TR >
    <TD CLASS="strcol" >Race</TD>
    <TD CLASS="strcol" >
      <SELECT NAME="ClientFamily_Race_1" >
        [[DBA->selxTable(%form+xRaces+<<ClientFamily_Race_1>>+Descr)]]
      </SELECT> 
  </TR>
  <TR >
    <TD CLASS="strcol" >Marital Status</TD>
    <TD CLASS="strcol" >
      <SELECT NAME="ClientFamily_MarStat_1">
        [[DBA->selxTable(%form+xMarStat+<<ClientFamily_MarStat_1>>+Descr Text)]]
      </SELECT> 
  </TR>
  <TR >
    <TD CLASS="strcol" >Spouse Name</TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="TEXT" NAME="ClientFamily_Spouse_1" VALUE="<<ClientFamily_Spouse_1>>" ONFOCUS="select()" SIZE="20" >
  </TR>
  <TR >
    <TD CLASS="strcol" >Parental Status</TD>
    <TD CLASS="strcol" >
      <SELECT NAME="ClientFamily_ParStat_1">
        [[DBA->selxTable(%form+xParentalStatus+<<ClientFamily_ParStat_1>>+Descr)]]
      </SELECT> 
  </TR>
  <TR >
    <TD CLASS="strcol" ># of Children</TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="TEXT" NAME="ClientFamily_ChSum_1" VALUE="<<ClientFamily_ChSum_1>>" ONFOCUS="select()" ONCHANGE="return vNum(this,0,10);" SIZE="10" > 
  </TR>
  <TR >
    <TD CLASS="strcol" >Employer</TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="TEXT" NAME="ClientFamily_Empl_1" VALUE="<<ClientFamily_Empl_1>>" ONFOCUS="select()" SIZE="20" >
  </TR>
  <TR >
    <TD CLASS="strcol" >Position</TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="TEXT" NAME="ClientFamily_EPos_1" VALUE="<<ClientFamily_EPos_1>>" ONFOCUS="select()" SIZE="20" >
  </TR>
  <TR >
    <TD CLASS="strcol" >Special Instructions</TD>
    <TD CLASS="strcol" >
      <TEXTAREA NAME="ClientFamily_Comments_1" COLS="70" ROWS="5" WRAP="virtual" ><<ClientFamily_Comments_1>></TEXTAREA>
    </TD>
  </TR>
</TABLE>
<TABLE CLASS="home fullsize" >
  <TR ><TD CLASS="hdrtxt" COLSPAN="4" >Value of Relationship</TD></TR>
  <TR >
    <TD CLASS="strcol" >Living Inhome</TD>
    <TD CLASS="strcol" >
      <INPUT TYPE=radio NAME="ClientFamily_Inhome_1" VALUE=1 <<ClientFamily_Inhome_1=1>> > yes
      <INPUT TYPE=radio NAME="ClientFamily_Inhome_1" VALUE=0 <<ClientFamily_Inhome_1=0>> > no
    </TD>
  </TR>
  <TR >
    <TD CLASS="strcol" >Relationship value</TD>
    <TD CLASS="strcol" >
      <INPUT TYPE=text NAME="ClientFamily_RelValue_1" VALUE="<<ClientFamily_RelValue_1>>" ONCHANGE="return vNum(this,1,10)" ONFOCUS="select()" > 
      (1=bad, 10=excellent)
    </TD>
  </TR>
  <TR >
    <TD CLASS="strcol" >Relationship value description</TD>
    <TD CLASS="strcol" >
      <INPUT TYPE=text NAME="ClientFamily_RelValueDesc_1" VALUE="<<ClientFamily_RelValueDesc_1>>" ONFOCUS="select()" SIZE="60" >
    </TD>
  </TR>
</TABLE>
<TABLE CLASS="home fullsize" >
  <TR ><TD CLASS="hdrtxt" COLSPAN="4" >Reported Problems</TD></TR>
  <TR >
    <TD CLASS="strcol" >Alcohol Problem</TD>
    <TD CLASS="strcol" >
      <INPUT TYPE=radio NAME="ClientFamily_AbuseAlcohol_1" VALUE=1 <<ClientFamily_AbuseAlcohol_1=1>> > yes
      <INPUT TYPE=radio NAME="ClientFamily_AbuseAlcohol_1" VALUE=0 <<ClientFamily_AbuseAlcohol_1=0>> > no
    </TD>
  </TR>
  <TR >
    <TD CLASS="strcol" >Drug Problem</TD>
    <TD CLASS="strcol" >
      <INPUT TYPE=radio NAME="ClientFamily_AbuseDrugs_1" VALUE=1 <<ClientFamily_AbuseDrugs_1=1>> > yes
      <INPUT TYPE=radio NAME="ClientFamily_AbuseDrugs_1" VALUE=0 <<ClientFamily_AbuseDrugs_1=0>> > no
    </TD>
  </TR>
  <TR >
    <TD CLASS="strcol" >Psychological Problem</TD>
    <TD CLASS="strcol" >
      <INPUT TYPE=radio NAME="ClientFamily_AbusePsych_1" VALUE=1 <<ClientFamily_AbusePsych_1=1>> > yes
      <INPUT TYPE=radio NAME="ClientFamily_AbusePsych_1" VALUE=0 <<ClientFamily_AbusePsych_1=0>> > no
    </TD>
  </TR>
  <TR >
    <TD CLASS="strcol" >Emotional Abuse</TD>
    <TD CLASS="strcol" >
      <INPUT TYPE=radio NAME="ClientFamily_AbuseEmotion_1" VALUE=V <<ClientFamily_AbuseEmotion_1=V>> > victim
      <INPUT TYPE=radio NAME="ClientFamily_AbuseEmotion_1" VALUE=P <<ClientFamily_AbuseEmotion_1=P>> > perpetrator
      <INPUT TYPE=radio NAME="ClientFamily_AbuseEmotion_1" VALUE=B <<ClientFamily_AbuseEmotion_1=B>> > both
      <INPUT TYPE=radio NAME="ClientFamily_AbuseEmotion_1" VALUE=N <<ClientFamily_AbuseEmotion_1=N>> > none
    </TD>
  </TR>
  <TR >
    <TD CLASS="strcol" >Physical Abuse</TD>
    <TD CLASS="strcol" >
      <INPUT TYPE=radio NAME="ClientFamily_AbusePhysical_1" VALUE=V <<ClientFamily_AbusePhysical_1=V>> > victim
      <INPUT TYPE=radio NAME="ClientFamily_AbusePhysical_1" VALUE=P <<ClientFamily_AbusePhysical_1=P>> > perpetrator
      <INPUT TYPE=radio NAME="ClientFamily_AbusePhysical_1" VALUE=B <<ClientFamily_AbusePhysical_1=B>> > both
      <INPUT TYPE=radio NAME="ClientFamily_AbusePhysical_1" VALUE=N <<ClientFamily_AbusePhysical_1=N>> > none
    </TD>
  </TR>
  <TR >
    <TD CLASS="strcol" >Sexual Abuse</TD>
    <TD CLASS="strcol" >
      <INPUT TYPE=radio NAME="ClientFamily_AbuseSexual_1" VALUE=V <<ClientFamily_AbuseSexual_1=V>> > victim
      <INPUT TYPE=radio NAME="ClientFamily_AbuseSexual_1" VALUE=P <<ClientFamily_AbuseSexual_1=P>> > perpetrator
      <INPUT TYPE=radio NAME="ClientFamily_AbuseSexual_1" VALUE=B <<ClientFamily_AbuseSexual_1=B>> > both
      <INPUT TYPE=radio NAME="ClientFamily_AbuseSexual_1" VALUE=N <<ClientFamily_AbuseSexual_1=N>> > none
    </TD>
  </TR>
</TABLE>
<TABLE CLASS="home fullsize" >
  <TR >
    <TD CLASS="port hdrtxt" WIDTH="50%" >
      Family Problem Information
      <A HREF="javascript:callAjax('ListClientFamilyProblems','','ListClientFamilyProblems','&active=1&Locked=0&Client_ClientID=<<<Client_ClientID>>>&ClientFamily_ID=<<<ClientFamily_ID>>>&LOGINPROVID=<<<LOGINPROVID>>>&LOGINUSERID=<<<LOGINUSERID>>>&LOGINUSERDB=<<<LOGINUSERDB>>>&mlt=<<<mlt>>>&LINKID=<<<LINKID>>>','popup.pl');" TITLE="Show ONLY Active Family Problems for Client" >Active Only</A>
      /
      <A HREF="javascript:callAjax('ListClientFamilyProblems','','ListClientFamilyProblems','&active=0&Locked=0&Client_ClientID=<<<Client_ClientID>>>&ClientFamily_ID=<<<ClientFamily_ID>>>&LOGINPROVID=<<<LOGINPROVID>>>&LOGINUSERID=<<<LOGINUSERID>>>&LOGINUSERDB=<<<LOGINUSERDB>>>&mlt=<<<mlt>>>&LINKID=<<<LINKID>>>','popup.pl');" TITLE="Show ALL Family Problems for Client" >Show All</A>
    </TD>
    <TD WIDTH="50%" >&nbsp;</TD>
  </TR>
  <TR >
    <TD COLSPAN="2" >
<SPAN ID="ListClientFamilyProblems" >
[[myHTML->ListSel(%form+ListClientFamilyProblems+<<<ClientFamily_ID>>>+<<<LINKID>>>+<<<Client_Locked_1>>>)]]
</SPAN>
    </TD>
  </TR>
</TABLE>
<TABLE CLASS="home fullsize" >
  <TR ><TD CLASS="hdrtxt" COLSPAN="4" >Military History</TD></TR>
  <TR>
    <TD CLASS="strcol" >Military Service?</TD>
    <TD CLASS="strcol" >
      <INPUT TYPE=radio NAME="ClientFamily_MilFlag_1" VALUE=0 <<ClientFamily_MilFlag_1=0>> > None
      <INPUT TYPE=radio NAME="ClientFamily_MilFlag_1" VALUE=1 <<ClientFamily_MilFlag_1=1>> > Active
      <INPUT TYPE=radio NAME="ClientFamily_MilFlag_1" VALUE=2 <<ClientFamily_MilFlag_1=2>> > Reserve
      <INPUT TYPE=radio NAME="ClientFamily_MilFlag_1" VALUE=3 <<ClientFamily_MilFlag_1=3>> > Discharged
      <INPUT TYPE=radio NAME="ClientFamily_MilFlag_1" VALUE=4 <<ClientFamily_MilFlag_1=4>> > Retired
    </TD>
  </TR>
  <TR>
    <TD CLASS="strcol" >What branch of service?</TD>
    <TD CLASS="strcol" >
      <SELECT NAME="ClientFamily_MilBranch_1" >
        [[DBA->selxTable(%form+xMilBranch+<<ClientFamily_MilBranch_1>>+Descr)]]
      </SELECT> 
    </TD>
  </TR>
  <TR>
    <TD CLASS="strcol" >Type of discharge?</TD>
    <TD CLASS="strcol" >
      <SELECT NAME="ClientFamily_MilDis_1" >
        [[DBA->selxTable(%form+xMilDis+<<ClientFamily_MilDis_1>>+Descr)]]
      </SELECT> 
    </TD>
  </TR>
</TABLE>
<TABLE CLASS="main fullsize" >
  <TR>
    <TD CLASS="numcol" >
      <INPUT TYPE="submit" ONCLICK="return vDELETE('Are you sure you want to delete this entire Family member?');" NAME="ClientFamily_DELETE_1=1&UpdateTables=all&misPOP=1" VALUE="Delete Family Member">
      <INPUT TYPE="submit" ONCLICK="return validate(this.form);" NAME="UpdateTables=all&misPOP=1" VALUE="Add/Update">
    </TD>
  </TR>
</TABLE>

</LOADHIDDEN>
</FORM>
<SCRIPT LANGUAGE="JavaScript">
document.ClientFamily.elements[0].focus();
</SCRIPT>
[[myHTML->rightpane(%form+search)]]
<script src="https://maps.googleapis.com/maps/api/js?key=AIzaSyAG2JfgYWgk7Q3FDfZQJauF-M4o4H1wqVw&libraries=places&callback=initAutocomplete"
        async defer></script>
<SCRIPT type="text/javascript" src="/cgi/js/vMCAutocomplete.js?v=202006082124"></SCRIPT>
<SCRIPT LANGUAGE="JavaScript" >
callAjax('xRelationship','','','&Autocomplete=MCAutocomplete&Target=ClientFamily_Rel_1','popup.pl');
</SCRIPT>
<script LANGUAGE="JavaScript" src="/cgi/js/vClientAddressForm.js?v=202006242248"></script>
<script LANGUAGE="JavaScript">
$(document).ready(function() {
  initClientAddressForm('ClientFamily_AddressManualInput', 'ClientFamily_AddressManualInput_Link', 'ClientFamily_', 2);
});
</script>
