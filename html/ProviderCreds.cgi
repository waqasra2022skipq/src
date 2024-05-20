[[myHTML->newPage(%form+Credentials)]]

<SCRIPT LANGUAGE="JavaScript" SRC="/cgi/js/NoEnter.js"> </SCRIPT>
<SCRIPT LANGUAGE="JavaScript" SRC="/cgi/js/vEntry.js"> </SCRIPT>
<SCRIPT LANGUAGE="JavaScript" SRC="/cgi/js/vCredentials.js"> </SCRIPT>
<SCRIPT LANGUAGE="JavaScript" SRC="/cgi/js/vDate.js"> </SCRIPT>
<SCRIPT LANGUAGE="JavaScript" SRC="/cgi/js/vNum.js"> </SCRIPT>
<SCRIPT TYPE="text/javascript" SRC="/cgi/jquery/jquery-ui-1.11.2/jquery-ui.min.js" ></SCRIPT>
<SCRIPT type="text/javascript" src="/cgi/js/ajaxrequest.js"></SCRIPT>
<LINK HREF="/cgi/css/autocomplete.css?v=202008071708" REL="stylesheet">

<FORM NAME="Credentials" ACTION="/cgi/bin/mis.cgi" METHOD="POST" >
<TABLE CLASS="main fullsize" >
  <TR >
    <TD CLASS="strcol" >
      <<<Provider_FName_1>>> <<<Provider_MName_1>>> <<<Provider_LName_1>>> 
      <BR>Uniform Provider Creditialing Application
(63 O.S. Supp. 1998, Section 1-106.2)
    </TD>
    <TD CLASS="numcol" >[[gHTML->setLINKS(%form+back)]]</TD>
  </TR>
</TABLE>
<HR WIDTH="90%" >
<TABLE CLASS="home fullsize" >
    <TR ><TD CLASS="port heading" ><TABLE CLASS="home fullsize" >
  <TR> <TD CLASS="homesubtitle" COLSPAN="2" >SUBMIT THIS FORM TO THE HOSPITAL, MANAGED CARE ORGANIZATION, OR OTHER ENTITY REQUIRING CREDENTIALS VERIFICATION. </TD> </TR>
  <TR> <TD CLASS="homesubtitle" COLSPAN="2" >Oklahoma State Department of Health ODH Form 606 Protective Health Services (05/01) </TD> </TR>
  <TR> <TD CLASS="strcol" >This form must be completed in full and typed or printed legibly (i.e. do not state "see CV"). Write "N/A" in areas that do not apply to you. All time must be accounted for since entry into medical or other professional school.  If additional space is needed to complete information or explanations, use Section 14.</TD> </TR>
    </TABLE></TD></TR>
    <TR ><TD CLASS="port hdrtxt" ><TABLE CLASS="home fullsize" >
  <TR> <TD CLASS="strcol" >Name of facility/organization this application will be submitted to: </TD> </TR>
  <TR>
    <TD CLASS="strcol" >
      <INPUT TYPE="TEXT" NAME="ProviderCreds_ApplicationOrg_1" VALUE="<<ProviderCreds_ApplicationOrg_1>>" SIZE="70" > 
    </TD>
  </TR>
    </TABLE></TD></TR>
    <TR ><TD CLASS="port hdrtxt" ><TABLE CLASS="home fullsize" >
    </TABLE></TD></TR>
    <TR ><TD ><TABLE CLASS="home fullsize" >
  <TR> <TD CLASS="port hdrtxt" COLSPAN="2" >SECTION 1: PERSONAL INFORMATION</TD> </TR>
  <TR> <TD CLASS="strcol" COLSPAN="2" >NAME</TD> </TR>
  <TR>
    <TD CLASS="strcol" >Last </TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="TEXT" NAME="ProviderCreds_LName_1" VALUE="<<ProviderCreds_LName_1>>" SIZE="50" > 
    </TD>
  </TR>
  <TR>
    <TD CLASS="strcol" >First </TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="TEXT" NAME="ProviderCreds_FName_1" VALUE="<<ProviderCreds_FName_1>>" SIZE="50" > 
    </TD>
  </TR>
  <TR>
    <TD CLASS="strcol" >Middle </TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="TEXT" NAME="ProviderCreds_MName_1" VALUE="<<ProviderCreds_MName_1>>" SIZE="50" > 
    </TD>
  </TR>
  <TR>
    <TD CLASS="strcol" >Suffix</TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="TEXT" NAME="ProviderCreds_Suff_1" VALUE="<<ProviderCreds_Suff_1>>" SIZE="50" > 
    </TD>
  </TR>
  <TR>
    <TD CLASS="strcol" >Professional Degree </TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="TEXT" NAME="ProviderCreds_Degree_1" VALUE="<<ProviderCreds_Degree_1>>" SIZE="50" > 
    </TD>
  </TR>
  <TR>
    <TD CLASS="strcol" >Gender:</TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="TEXT" NAME="ProviderCreds_Gend_1" VALUE="<<ProviderCreds_Gend_1>>" SIZE="50" > 
    </TD>
  </TR>
  <TR>
    <TD CLASS="strcol" >Other Name By Which You Have Been Known </TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="TEXT" NAME="ProviderCreds_Alias1_1" VALUE="<<ProviderCreds_Alias1_1>>" SIZE="50" > 
    </TD>
  </TR>
  <TR>
    <TD CLASS="strcol" >Dates This Name Was Used: </TD>
    <TD CLASS="strcol" >
      From: <INPUT TYPE="TEXT" NAME="ProviderCreds_Alias1DateFrom_1" VALUE="<<ProviderCreds_Alias1DateFrom_1>>" ONCHANGE="return vDate(this);" MAXLENGTH="10" SIZE="10" > 
      To: <INPUT TYPE="TEXT" NAME="ProviderCreds_Alias1DateEnd_1" VALUE="<<ProviderCreds_Alias1DateEnd_1>>" ONCHANGE="return vDate(this);" MAXLENGTH="10" SIZE="10" > 
    </TD>
  </TR>
  <TR>
    <TD CLASS="strcol" >Other Name By Which You Have Been Know</TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="TEXT" NAME="ProviderCreds_Alias2_1" VALUE="<<ProviderCreds_Alias2_1>>" SIZE="50" > 
    </TD>
  </TR>
  <TR>
    <TD CLASS="strcol" >Dates This Name Was Used: </TD>
    <TD CLASS="strcol" >
      From: <INPUT TYPE="TEXT" NAME="ProviderCreds_Alias2DateFrom_1" VALUE="<<ProviderCreds_Alias2DateFrom_1>>" ONCHANGE="return vDate(this);" MAXLENGTH="10" SIZE="10" > 
      To: <INPUT TYPE="TEXT" NAME="ProviderCreds_Alias2DateEnd_1" VALUE="<<ProviderCreds_Alias2DateEnd_1>>" ONCHANGE="return vDate(this);" MAXLENGTH="10" SIZE="10" > 
    </TD>
  </TR>
  <TR>
    <TD CLASS="strcol" >Social Security Number </TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="TEXT" NAME="ProviderCreds_SSN_1" VALUE="<<ProviderCreds_SSN_1>>" SIZE="50" > 
    </TD>
  </TR>
  <TR>
    <TD CLASS="strcol" > NPID (formerly UPIN)</TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="TEXT" NAME="ProviderCreds_NPI_1" VALUE="<<ProviderCreds_NPI_1>>" SIZE="50" > 
    </TD>
  </TR>
  <TR>
    <TD CLASS="strcol" >Date of Birth:  </TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="TEXT" NAME="ProviderCreds_DOB_1" VALUE="<<ProviderCreds_DOB_1>>" ONCHANGE="return vDate(this);" MAXLENGTH="10" SIZE="10" > 
    </TD>
  </TR>
  <TR>
    <TD CLASS="strcol" >Place of Birth </TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="TEXT" NAME="ProviderCreds_PlaceOfBirth_1" VALUE="<<ProviderCreds_PlaceOfBirth_1>>" SIZE="50" > 
    </TD>
  </TR>
  <TR>
    <TD CLASS="strcol" >Citizenship </TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="TEXT" NAME="ProviderCreds_Citizenship_1" VALUE="<<ProviderCreds_Citizenship_1>>" SIZE="50" > 
    </TD>
  </TR>
  <TR>
    <TD CLASS="strcol" >Visa Type </TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="TEXT" NAME="ProviderCreds_VisaType_1" VALUE="<<ProviderCreds_VisaType_1>>" SIZE="50" > 
    </TD>
  </TR>
  <TR>
    <TD CLASS="strcol" >Visa Number (provide copy)</TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="TEXT" NAME="ProviderCreds_VisaNum_1" VALUE="<<ProviderCreds_VisaNum_1>>" SIZE="50" > 
    </TD>
  </TR>
  <TR>
    <TD CLASS="strcol" >Expiration Date </TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="TEXT" NAME="ProviderCreds_VisaExpire_1" VALUE="<<ProviderCreds_VisaExpire_1>>" ONCHANGE="return vDate(this);" MAXLENGTH="10" SIZE="10" > 
    </TD>
  </TR>
  <TR>
    <TD CLASS="strcol" >Your Personal Medicare Number </TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="TEXT" NAME="ProviderCreds_MedicarePIN_1" VALUE="<<ProviderCreds_MedicarePIN_1>>" SIZE="50" > 
    </TD>
  </TR>
  <TR>
    <TD CLASS="strcol" >Your Personal Medicaid Number </TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="TEXT" NAME="ProviderCreds_MedicaidPIN_1" VALUE="<<ProviderCreds_MedicaidPIN_1>>" SIZE="50" > 
    </TD>
  </TR>
    </TABLE></TD></TR>
    <TR ><TD ><TABLE CLASS="home fullsize" >
  <TR> <TD CLASS="port hdrtxt" COLSPAN="2" >SECTION 2: DIRECTORY INFORMATION </TD> </TR>
  <TR> <TD CLASS="strcol" COLSPAN="2" >Mailing Address For All ProviderCreds Correspondence: </TD> </TR>
  <TR>
    <TD CLASS="strcol" >Street Address </TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="TEXT" NAME="ProviderCreds_DirectoryAddr1_1" VALUE="<<ProviderCreds_DirectoryAddr1_1>>" SIZE="50" > 
    </TD>
  </TR>
  <TR>
    <TD CLASS="strcol" >Suite Number </TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="TEXT" NAME="ProviderCreds_DirectoryAddr2_1" VALUE="<<ProviderCreds_DirectoryAddr2_1>>" SIZE="50" > 
    </TD>
  </TR>
  <TR>
    <TD CLASS="strcol" >City </TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="TEXT" NAME="ProviderCreds_DirectoryCity_1" VALUE="<<ProviderCreds_DirectoryCity_1>>" SIZE="50" > 
    </TD>
  </TR>
  <TR>
    <TD CLASS="strcol" >State </TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="TEXT" NAME="ProviderCreds_DirectoryST_1" VALUE="<<ProviderCreds_DirectoryST_1>>" SIZE="50" > 
    </TD>
  </TR>
  <TR>
    <TD CLASS="strcol" >Zip Code </TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="TEXT" NAME="ProviderCreds_DirectoryZIP_1" VALUE="<<ProviderCreds_DirectoryZIP_1>>" SIZE="50" > 
    </TD>
  </TR>
  <TR>
    <TD CLASS="strcol" >Phone Number </TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="TEXT" NAME="ProviderCreds_DirectoryPh_1" VALUE="<<ProviderCreds_DirectoryPh_1>>" SIZE="50" > 
    </TD>
  </TR>
  <TR>
    <TD CLASS="strcol" >Fax Number </TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="TEXT" NAME="ProviderCreds_DirectoryFax_1" VALUE="<<ProviderCreds_DirectoryFax_1>>" SIZE="50" > 
    </TD>
  </TR>
  <TR>
    <TD CLASS="strcol" >Emergency or Pager Number </TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="TEXT" NAME="ProviderCreds_DirectoryPgr_1" VALUE="<<ProviderCreds_DirectoryPgr_1>>" SIZE="50" > 
    </TD>
  </TR>
  <TR>
    <TD CLASS="strcol" >Answering Service Number </TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="TEXT" NAME="ProviderCreds_DirectoryAnsSvc_1" VALUE="<<ProviderCreds_DirectoryAnsSvc_1>>" SIZE="50" > 
    </TD>
  </TR>
  <TR>
    <TD CLASS="strcol" >E-Mail Address </TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="EMAIL" NAME="ProviderCreds_DirectoryEmail_1" VALUE="<<ProviderCreds_DirectoryEmail_1>>" SIZE="50" > 
    </TD>
  </TR>
  <TR>
    <TD CLASS="strcol" >Contact Person For ProviderCreds Correspondence: </TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="TEXT" NAME="ProviderCreds_DirectoryMgr_1" VALUE="<<ProviderCreds_DirectoryMgr_1>>" SIZE="50" > 
    </TD>
  </TR>
  <TR> <TD CLASS="strcol" COLSPAN="2" >Office Street Address: </TD> </TR>
  <TR>
    <TD CLASS="strcol" >Street Address </TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="TEXT" NAME="ProviderCreds_Off1Addr1_1" VALUE="<<ProviderCreds_Off1Addr1_1>>" SIZE="50" > 
    </TD>
  </TR>
  <TR>
    <TD CLASS="strcol" >Suite Number </TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="TEXT" NAME="ProviderCreds_Off1Addr2_1" VALUE="<<ProviderCreds_Off1Addr2_1>>" SIZE="50" > 
    </TD>
  </TR>
  <TR>
    <TD CLASS="strcol" >City </TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="TEXT" NAME="ProviderCreds_Off1City_1" VALUE="<<ProviderCreds_Off1City_1>>" SIZE="50" > 
    </TD>
  </TR>
  <TR>
    <TD CLASS="strcol" >State </TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="TEXT" NAME="ProviderCreds_Off1ST_1" VALUE="<<ProviderCreds_Off1ST_1>>" SIZE="50" > 
    </TD>
  </TR>
  <TR>
    <TD CLASS="strcol" >Zip Code </TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="TEXT" NAME="ProviderCreds_Off1Zip_1" VALUE="<<ProviderCreds_Off1Zip_1>>" SIZE="50" > 
    </TD>
  </TR>
  <TR>
    <TD CLASS="strcol" >Phone Number </TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="TEXT" NAME="ProviderCreds_Off1Ph_1" VALUE="<<ProviderCreds_Off1Ph_1>>" SIZE="50" > 
    </TD>
  </TR>
  <TR>
    <TD CLASS="strcol" >Fax Number </TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="TEXT" NAME="ProviderCreds_Off1Fax_1" VALUE="<<ProviderCreds_Off1Fax_1>>" SIZE="50" > 
    </TD>
  </TR>
  <TR>
    <TD CLASS="strcol" >Emergency or Pager Number </TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="TEXT" NAME="ProviderCreds_Off1Pgr_1" VALUE="<<ProviderCreds_Off1Pgr_1>>" SIZE="50" > 
    </TD>
  </TR>
  <TR>
    <TD CLASS="strcol" >Answering Service Number </TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="TEXT" NAME="ProviderCreds_Off1AnsSvc_1" VALUE="<<ProviderCreds_Off1AnsSvc_1>>" SIZE="50" > 
    </TD>
  </TR>
  <TR>
    <TD CLASS="strcol" >E-Mail Address </TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="EMAIL" NAME="ProviderCreds_Off1Email_1" VALUE="<<ProviderCreds_Off1Email_1>>" SIZE="50" > 
    </TD>
  </TR>
  <TR> <TD CLASS="strcol" COLSPAN="2" >Office Mailing Address: </TD> </TR>
  <TR>
    <TD CLASS="strcol" >Street Address </TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="TEXT" NAME="ProviderCreds_Off2Addr1_1" VALUE="<<ProviderCreds_Off2Addr1_1>>" SIZE="50" > 
    </TD>
  </TR>
  <TR>
    <TD CLASS="strcol" >Suite Number </TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="TEXT" NAME="ProviderCreds_Off2Addr2_1" VALUE="<<ProviderCreds_Off2Addr2_1>>" SIZE="50" > 
    </TD>
  </TR>
  <TR>
    <TD CLASS="strcol" >City </TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="TEXT" NAME="ProviderCreds_Off2City_1" VALUE="<<ProviderCreds_Off2City_1>>" SIZE="50" > 
    </TD>
  </TR>
  <TR>
    <TD CLASS="strcol" >State </TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="TEXT" NAME="ProviderCreds_Off2ST_1" VALUE="<<ProviderCreds_Off2ST_1>>" SIZE="50" > 
    </TD>
  </TR>
  <TR>
    <TD CLASS="strcol" >Zip Code </TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="TEXT" NAME="ProviderCreds_Off2Zip_1" VALUE="<<ProviderCreds_Off2Zip_1>>" SIZE="50" > 
    </TD>
  </TR>
  <TR>
    <TD CLASS="strcol" >Phone Number </TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="TEXT" NAME="ProviderCreds_Off2Ph_1" VALUE="<<ProviderCreds_Off2Ph_1>>" SIZE="50" > 
    </TD>
  </TR>
  <TR>
    <TD CLASS="strcol" >Fax Number </TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="TEXT" NAME="ProviderCreds_Off2Fax_1" VALUE="<<ProviderCreds_Off2Fax_1>>" SIZE="50" > 
    </TD>
  </TR>
  <TR>
    <TD CLASS="strcol" >Emergency or Pager Number</TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="TEXT" NAME="ProviderCreds_Off2Pgr_1" VALUE="<<ProviderCreds_Off2Pgr_1>>" SIZE="50" > 
    </TD>
  </TR>
  <TR>
    <TD CLASS="strcol" >Answering Service Number</TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="TEXT" NAME="ProviderCreds_Off2AnsSvc_1" VALUE="<<ProviderCreds_Off2AnsSvc_1>>" SIZE="50" > 
    </TD>
  </TR>
  <TR>
    <TD CLASS="strcol" >E-Mail Addres</TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="EMAIL" NAME="ProviderCreds_Off2Email_1" VALUE="<<ProviderCreds_Off2Email_1>>" SIZE="50" > 
    </TD>
  </TR>
  <TR> <TD CLASS="strcol" COLSPAN="2" >Office Billing Address (If Different From Claims Payment Address): </TD> </TR>
  <TR>
    <TD CLASS="strcol" >Street Address </TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="TEXT" NAME="ProviderCreds_Off3Addr1_1" VALUE="<<ProviderCreds_Off3Addr1_1>>" SIZE="50" > 
    </TD>
  </TR>
  <TR>
    <TD CLASS="strcol" >Suite Number </TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="TEXT" NAME="ProviderCreds_Off3Addr2_1" VALUE="<<ProviderCreds_Off3Addr2_1>>" SIZE="50" > 
    </TD>
  </TR>
  <TR>
    <TD CLASS="strcol" >City </TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="TEXT" NAME="ProviderCreds_Off3City_1" VALUE="<<ProviderCreds_Off3City_1>>" SIZE="50" > 
    </TD>
  </TR>
  <TR>
    <TD CLASS="strcol" >State </TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="TEXT" NAME="ProviderCreds_Off3ST_1" VALUE="<<ProviderCreds_Off3ST_1>>" SIZE="50" > 
    </TD>
  </TR>
  <TR>
    <TD CLASS="strcol" >Zip Code </TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="TEXT" NAME="ProviderCreds_Off3Zip_1" VALUE="<<ProviderCreds_Off3Zip_1>>" SIZE="50" > 
    </TD>
  </TR>
  <TR>
    <TD CLASS="strcol" >Phone Number </TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="TEXT" NAME="ProviderCreds_Off3Ph_1" VALUE="<<ProviderCreds_Off3Ph_1>>" SIZE="50" > 
    </TD>
  </TR>
  <TR>
    <TD CLASS="strcol" >Fax Number </TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="TEXT" NAME="ProviderCreds_Off3Fax_1" VALUE="<<ProviderCreds_Off3Fax_1>>" SIZE="50" > 
    </TD>
  </TR>
  <TR>
    <TD CLASS="strcol" >Emergency or Pager Number</TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="TEXT" NAME="ProviderCreds_Off3Pgr_1" VALUE="<<ProviderCreds_Off3Pgr_1>>" SIZE="50" > 
    </TD>
  </TR>
  <TR>
    <TD CLASS="strcol" >Answering Service Number </TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="TEXT" NAME="ProviderCreds_Off3AnsSvc_1" VALUE="<<ProviderCreds_Off3AnsSvc_1>>" SIZE="50" > 
    </TD>
  </TR>
  <TR>
    <TD CLASS="strcol" >E-Mail Address</TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="EMAIL" NAME="ProviderCreds_Off3Email_1" VALUE="<<ProviderCreds_Off3Email_1>>" SIZE="50" > 
    </TD>
  </TR>
  <TR> <TD CLASS="strcol" COLSPAN="2" >Claims Payment Address (If Different From Office Billing Address): </TD> </TR>
  <TR>
    <TD CLASS="strcol" >Street Address </TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="TEXT" NAME="ProviderCreds_Off4Addr1_1" VALUE="<<ProviderCreds_Off4Addr1_1>>" SIZE="50" > 
    </TD>
  </TR>
  <TR>
    <TD CLASS="strcol" >Suite Number </TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="TEXT" NAME="ProviderCreds_Off4Addr2_1" VALUE="<<ProviderCreds_Off4Addr2_1>>" SIZE="50" > 
    </TD>
  </TR>
  <TR>
    <TD CLASS="strcol" >City </TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="TEXT" NAME="ProviderCreds_Off4City_1" VALUE="<<ProviderCreds_Off4City_1>>" SIZE="50" > 
    </TD>
  </TR>
  <TR>
    <TD CLASS="strcol" >State </TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="TEXT" NAME="ProviderCreds_Off4ST_1" VALUE="<<ProviderCreds_Off4ST_1>>" SIZE="50" > 
    </TD>
  </TR>
  <TR>
    <TD CLASS="strcol" >Zip Code </TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="TEXT" NAME="ProviderCreds_Off4Zip_1" VALUE="<<ProviderCreds_Off4Zip_1>>" SIZE="50" > 
    </TD>
  </TR>
  <TR>
    <TD CLASS="strcol" >Phone Number </TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="TEXT" NAME="ProviderCreds_Off4Ph_1" VALUE="<<ProviderCreds_Off4Ph_1>>" SIZE="50" > 
    </TD>
  </TR>
  <TR>
    <TD CLASS="strcol" >Fax Number </TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="TEXT" NAME="ProviderCreds_Off4Fax_1" VALUE="<<ProviderCreds_Off4Fax_1>>" SIZE="50" > 
    </TD>
  </TR>
  <TR>
    <TD CLASS="strcol" >Emergency or Pager Number</TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="TEXT" NAME="ProviderCreds_Off4Pgr_1" VALUE="<<ProviderCreds_Off4Pgr_1>>" SIZE="50" > 
    </TD>
  </TR>
  <TR>
    <TD CLASS="strcol" >Answering Service Number </TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="TEXT" NAME="ProviderCreds_Off4AnsSvc_1" VALUE="<<ProviderCreds_Off4AnsSvc_1>>" SIZE="50" > 
    </TD>
  </TR>
  <TR>
    <TD CLASS="strcol" >E-Mail Addres</TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="EMAIL" NAME="ProviderCreds_Off4Email_1" VALUE="<<ProviderCreds_Off4Email_1>>" SIZE="50" > 
    </TD>
  </TR>
  <TR>
    <TD CLASS="strcol" >Make Checks Payable To: </TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="TEXT" NAME="ProviderCreds_Off1Mgr_1" VALUE="<<ProviderCreds_Off1Mgr_1>>" SIZE="50" > 
    </TD>
  </TR>
  </TR>
    </TABLE></TD></TR>
    <TR ><TD ><TABLE CLASS="home fullsize" >
  <TR> <TD CLASS="port hdrtxt" COLSPAN="2" >SECTION 3: CURRENT PROFESSIONAL PRACTICE</TD> </TR>
  <TR>
    <TD CLASS="strcol" >Primary Specialty (or field of practice)</TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="TEXT" NAME="ProviderCreds_SpecialtyPrimary_1" VALUE="<<ProviderCreds_SpecialtyPrimary_1>>" SIZE="50" > 
    </TD>
  </TR>
  <TR>
    <TD CLASS="strcol" >Subspecialty </TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="TEXT" NAME="ProviderCreds_SubspecialtyPrimary_1" VALUE="<<ProviderCreds_SubspecialtyPrimary_1>>" SIZE="50" > 
    </TD>
  </TR>
  <TR>
    <TD CLASS="strcol" > % Of Time </TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="TEXT" NAME="ProviderCreds_SpecailtyPrimaryTime_1" VALUE="<<ProviderCreds_SpecailtyPrimaryTime_1>>" SIZE="50" > 
    </TD>
  </TR>
  <TR>
    <TD CLASS="strcol" >Secondary Specialty </TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="TEXT" NAME="ProviderCreds_SpecialtySecondary_1" VALUE="<<ProviderCreds_SpecialtySecondary_1>>" SIZE="50" > 
    </TD>
  </TR>
  <TR>
    <TD CLASS="strcol" >Subspecialty</TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="TEXT" NAME="ProviderCreds_SubspecialtySecondary_1" VALUE="<<ProviderCreds_SubspecialtySecondary_1>>" SIZE="50" > 
    </TD>
  </TR>
  <TR>
    <TD CLASS="strcol" > % Of Time </TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="TEXT" NAME="ProviderCreds_SpecialtySecondaryTime_1" VALUE="<<ProviderCreds_SpecialtySecondaryTime_1>>" SIZE="50" > 
    </TD>
  </TR>
  <TR>
    <TD CLASS="strcol" COLSPAN="2" >Do you wish to be listed as:
      <INPUT TYPE="radio" NAME="ProviderCreds_ProviderListType_1" VALUE="P" <<ProviderCreds_ProviderListType_1=P>> > Primary Care Provider 
      <INPUT TYPE="radio" NAME="ProviderCreds_ProviderListType_1" VALUE="S" <<ProviderCreds_ProviderListType_1=S>> > Specialist 
      <INPUT TYPE="radio" NAME="ProviderCreds_ProviderListType_1" VALUE="H" <<ProviderCreds_ProviderListType_1=H>> > Hospitalist 
      <INPUT TYPE="radio" NAME="ProviderCreds_ProviderListType_1" VALUE="C" <<ProviderCreds_ProviderListType_1=C>> > On-Call  
      <INPUT TYPE="radio" NAME="ProviderCreds_ProviderListType_1" VALUE="O" <<ProviderCreds_ProviderListType_1=O>> > Other (specify) 
    </TD>
  </TR>
  <TR>
    <TD CLASS="strcol" >Other (specify) </TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="TEXT" NAME="ProviderCreds_ProviderListTypeSpecify_1" VALUE="<<ProviderCreds_ProviderListTypeSpecify_1>>" SIZE="50" > 
    </TD>
  </TR>
  <TR> <TD CLASS="strcol" COLSPAN="2" >If you are a primary care physician, list special diagnostic or treatment procedures performed in your office(s): </TD> </TR>
  <TR>
    <TD CLASS="strcol" COLSPAN="2" >
<TEXTAREA NAME="ProviderCreds_SpecialProcedureSpecify_1" COLS=90 ROWS="12" WRAP="virtual" ><<ProviderCreds_SpecialProcedureSpecify_1>></TEXTAREA>
    </TD>
  </TR>
  <TR>
    <TD CLASS="strcol" COLSPAN="2" >
      <INPUT TYPE="radio" NAME="ProviderCreds_NewPt_1" VALUE=1 <<ProviderCreds_NewPt_1=1>> > Yes
      <INPUT TYPE="radio" NAME="ProviderCreds_NewPt_1" VALUE=0 <<ProviderCreds_NewPt_1=0>> > No
Are you accepting new patients?
    </TD>
  </TR>
  <TR>
    <TD CLASS="strcol" COLSPAN="2" >
      <INPUT TYPE="radio" NAME="ProviderCreds_FuturePt_1" VALUE=1 <<ProviderCreds_FuturePt_1=1>> > Yes
      <INPUT TYPE="radio" NAME="ProviderCreds_FuturePt_1" VALUE=0 <<ProviderCreds_FuturePt_1=0>> > No
Are you willing, in the future to accept new patients?
    </TD>
  </TR>
  <TR>
    <TD CLASS="strcol" COLSPAN="2" >
      <INPUT TYPE="radio" NAME="ProviderCreds_AdmitPt_1" VALUE=1 <<ProviderCreds_AdmitPt_1=1>> > Yes
      <INPUT TYPE="radio" NAME="ProviderCreds_AdmitPt_1" VALUE=0 <<ProviderCreds_AdmitPt_1=0>> > No
Do you admit your own patients to hospitals?
    </TD>
  </TR>
  <TR>
    <TD CLASS="strcol" COLSPAN="2" >If no, please explain how your patients will be admitted, which hospital and who will provide patient care.</TD>
  </TR>
  <TR>
    <TD CLASS="strcol" COLSPAN="2" >
      <INPUT TYPE="radio" NAME="ProviderCreds_CurrentPt_1" VALUE=1 <<ProviderCreds_CurrentPt_1=1>> > Yes
      <INPUT TYPE="radio" NAME="ProviderCreds_CurrentPt_1" VALUE=0 <<ProviderCreds_CurrentPt_1=0>> > No
Are you willing to accept current patients if they convert to the healthcare plan to which you are applying?
    </TD>
  </TR>
  <TR>
    <TD CLASS="strcol" COLSPAN="2" >
      <INPUT TYPE="radio" NAME="ProviderCreds_IPHPHAMember_1" VALUE=1 <<ProviderCreds_IPHPHAMember_1=1>> > Yes
      <INPUT TYPE="radio" NAME="ProviderCreds_IPHPHAMember_1" VALUE=0 <<ProviderCreds_IPHPHAMember_1=0>> > No
Are you a member of an Independent Practice Association or a Physician Hospital Association?  If yes,
    </TD>
  </TR>
  <TR>
    <TD CLASS="strcol" COLSPAN="2" >complete the following</TD>
  </TR>
  <TR>
    <TD CLASS="strcol" >Name:</TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="TEXT" NAME="ProviderCreds_IPHPHA1_1" VALUE="<<ProviderCreds_IPHPHA1_1>>" SIZE="50" > 
    </TD>
  </TR>
  <TR>
    <TD CLASS="strcol" >Street Address </TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="TEXT" NAME="ProviderCreds_IPHPHA1Addr1_1" VALUE="<<ProviderCreds_IPHPHA1Addr1_1>>" SIZE="50" > 
    </TD>
  </TR>
  <TR>
    <TD CLASS="strcol" >Suite Number </TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="TEXT" NAME="ProviderCreds_IPHPHA1Addr2_1" VALUE="<<ProviderCreds_IPHPHA1Addr2_1>>" SIZE="50" > 
    </TD>
  </TR>
  <TR>
    <TD CLASS="strcol" >City </TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="TEXT" NAME="ProviderCreds_IPHPHA1City_1" VALUE="<<ProviderCreds_IPHPHA1City_1>>" SIZE="50" > 
    </TD>
  </TR>
  <TR>
    <TD CLASS="strcol" >State </TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="TEXT" NAME="ProviderCreds_IPHPHA1ST_1" VALUE="<<ProviderCreds_IPHPHA1ST_1>>" SIZE="50" > 
    </TD>
  </TR>
  <TR>
    <TD CLASS="strcol" >Zip Code </TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="TEXT" NAME="ProviderCreds_IPHPHA1Zip_1" VALUE="<<ProviderCreds_IPHPHA1Zip_1>>" SIZE="50" > 
    </TD>
  </TR>
  <TR>
    <TD CLASS="strcol" >Phone Number </TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="TEXT" NAME="ProviderCreds_IPHPHA1Ph_1" VALUE="<<ProviderCreds_IPHPHA1Ph_1>>" SIZE="50" > 
    </TD>
  </TR>
  <TR>
    <TD CLASS="strcol" >Fax Number </TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="TEXT" NAME="ProviderCreds_IPHPHA1Fax_1" VALUE="<<ProviderCreds_IPHPHA1Fax_1>>" SIZE="50" > 
    </TD>
  </TR>
  <TR>
    <TD CLASS="strcol" >Answering Service Number </TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="TEXT" NAME="ProviderCreds_IPHPHA1AnsSvc_1" VALUE="<<ProviderCreds_IPHPHA1AnsSvc_1>>" SIZE="50" > 
    </TD>
  </TR>
  <TR>
    <TD CLASS="strcol" >Name: </TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="TEXT" NAME="ProviderCreds_IPHPHA2_1" VALUE="<<ProviderCreds_IPHPHA2_1>>" SIZE="50" > 
    </TD>
  </TR>
  <TR>
    <TD CLASS="strcol" >Street Address </TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="TEXT" NAME="ProviderCreds_IPHPHA2Addr1_1" VALUE="<<ProviderCreds_IPHPHA2Addr1_1>>" SIZE="50" > 
    </TD>
  </TR>
  <TR>
    <TD CLASS="strcol" >Suite Number </TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="TEXT" NAME="ProviderCreds_IPHPHA2Addr2_1" VALUE="<<ProviderCreds_IPHPHA2Addr2_1>>" SIZE="50" > 
    </TD>
  <TR>
    <TD CLASS="strcol" >City </TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="TEXT" NAME="ProviderCreds_IPHPHA2City_1" VALUE="<<ProviderCreds_IPHPHA2City_1>>" SIZE="50" > 
    </TD>
  <TR>
    <TD CLASS="strcol" >State </TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="TEXT" NAME="ProviderCreds_IPHPHA2ST_1" VALUE="<<ProviderCreds_IPHPHA2ST_1>>" SIZE="50" > 
    </TD>
  <TR>
    <TD CLASS="strcol" >Zip Code </TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="TEXT" NAME="ProviderCreds_IPHPHA2Zip_1" VALUE="<<ProviderCreds_IPHPHA2Zip_1>>" SIZE="50" > 
    </TD>
  <TR>
    <TD CLASS="strcol" >Phone Number </TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="TEXT" NAME="ProviderCreds_IPHPHA2Ph_1" VALUE="<<ProviderCreds_IPHPHA2Ph_1>>" SIZE="50" > 
    </TD>
  </TR>
  <TR>
    <TD CLASS="strcol" >Fax Number </TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="TEXT" NAME="ProviderCreds_IPHPHA2Fax_1" VALUE="<<ProviderCreds_IPHPHA2Fax_1>>" SIZE="50" > 
    </TD>
  </TR>
  <TR>
    <TD CLASS="strcol" >Answering Service Number</TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="TEXT" NAME="ProviderCreds_IPHPHA2AnsSvc_1" VALUE="<<ProviderCreds_IPHPHA2AnsSvc_1>>" SIZE="50" > 
    </TD>
  </TR>
  <TR>
    <TD CLASS="strcol" >List any restrictions on your practice (i.e. patient age and gender): </TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="TEXT" NAME="ProviderCreds_Restrictions_1" VALUE="<<ProviderCreds_Restrictions_1>>" SIZE="50" > 
    </TD>
  </TR>
    </TABLE></TD></TR>
    <TR ><TD ><TABLE CLASS="home fullsize" >
  <TR> <TD CLASS="port hdrtxt" COLSPAN="2" >SECTION 4: EDUCATION </TD> </TR>
  <TR> <TD CLASS="strcol" COLSPAN="2" >Medical/Dental/Graduate Professional Schools </TD> </TR>
  <TR> <TD CLASS="strcol" COLSPAN="2" >List all, completed or not. Continue in Section 14 if needed. </TD> </TR>
  <TR>
    <TD CLASS="strcol" >(1) Institution </TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="TEXT" NAME="ProviderCreds_School1_1" VALUE="<<ProviderCreds_School1_1>>" SIZE="50" > 
    </TD>
  </TR>
  <TR>
    <TD CLASS="strcol" >Degree Awarded</TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="TEXT" NAME="ProviderCreds_School1Degree_1" VALUE="<<ProviderCreds_School1Degree_1>>" SIZE="50" > 
    </TD>
  </TR>
  <TR>
    <TD CLASS="strcol" >Mailing Address </TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="TEXT" NAME="ProviderCreds_School1Addr_1" VALUE="<<ProviderCreds_School1Addr_1>>" SIZE="50" > 
    </TD>
  </TR>
  <TR>
    <TD CLASS="strcol" >City </TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="TEXT" NAME="ProviderCreds_School1City_1" VALUE="<<ProviderCreds_School1City_1>>" SIZE="50" > 
    </TD>
  </TR>
  <TR>
    <TD CLASS="strcol" >State </TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="TEXT" NAME="ProviderCreds_School1ST_1" VALUE="<<ProviderCreds_School1ST_1>>" SIZE="50" > 
    </TD>
  </TR>
  <TR>
    <TD CLASS="strcol" >Zip Code</TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="TEXT" NAME="ProviderCreds_School1Zip_1" VALUE="<<ProviderCreds_School1Zip_1>>" SIZE="50" > 
    </TD>
  </TR>
  <TR>
    <TD CLASS="strcol" >Telephone Number:</TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="TEXT" NAME="ProviderCreds_School1Ph_1" VALUE="<<ProviderCreds_School1Ph_1>>" SIZE="50" > 
    </TD>
  </TR>
  <TR>
    <TD CLASS="strcol" >Dates Attended (mo/day/year) </TD>
    <TD CLASS="strcol" >
      From: <INPUT TYPE="TEXT" NAME="ProviderCreds_School1Start_1" VALUE="<<ProviderCreds_School1Start_1>>" ONCHANGE="return vDate(this);" MAXLENGTH="10" SIZE="10" > 
      To: <INPUT TYPE="TEXT" NAME="ProviderCreds_School1End_1" VALUE="<<ProviderCreds_School1End_1>>" ONCHANGE="return vDate(this);" MAXLENGTH="10" SIZE="10" > 
    </TD>
  </TR>
  <TR>
    <TD CLASS="strcol" >Graduation Date </TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="TEXT" NAME="ProviderCreds_School1GradDate_1" VALUE="<<ProviderCreds_School1GradDate_1>>" ONCHANGE="return vDate(this);" MAXLENGTH="10" SIZE="10" > 
    </TD>
  </TR>
  <TR>
    <TD CLASS="strcol" >(2) Institution </TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="TEXT" NAME="ProviderCreds_School2_1" VALUE="<<ProviderCreds_School2_1>>" SIZE="50" > 
    </TD>
  </TR>
  <TR>
    <TD CLASS="strcol" >Degree Awarded</TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="TEXT" NAME="ProviderCreds_School2Degree_1" VALUE="<<ProviderCreds_School2Degree_1>>" SIZE="50" > 
    </TD>
  </TR>
  <TR>
    <TD CLASS="strcol" >Mailing Address </TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="TEXT" NAME="ProviderCreds_School2Addr_1" VALUE="<<ProviderCreds_School2Addr_1>>" SIZE="50" > 
    </TD>
  </TR>
  <TR>
    <TD CLASS="strcol" >City </TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="TEXT" NAME="ProviderCreds_School2City_1" VALUE="<<ProviderCreds_School2City_1>>" SIZE="50" > 
    </TD>
  </TR>
  <TR>
    <TD CLASS="strcol" >State </TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="TEXT" NAME="ProviderCreds_School2ST_1" VALUE="<<ProviderCreds_School2ST_1>>" SIZE="50" > 
    </TD>
  </TR>
  <TR>
    <TD CLASS="strcol" >Zip Code</TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="TEXT" NAME="ProviderCreds_School2Zip_1" VALUE="<<ProviderCreds_School2Zip_1>>" SIZE="50" > 
    </TD>
  </TR>
  <TR>
    <TD CLASS="strcol" >Telephone Number:</TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="TEXT" NAME="ProviderCreds_School2Ph_1" VALUE="<<ProviderCreds_School2Ph_1>>" SIZE="50" > 
    </TD>
  </TR>
  <TR>
    <TD CLASS="strcol" >Dates Attended (mo/day/year) </TD>
    <TD CLASS="strcol" >
      From: <INPUT TYPE="TEXT" NAME="ProviderCreds_School2Start_1" VALUE="<<ProviderCreds_School2Start_1>>" ONCHANGE="return vDate(this);" MAXLENGTH="10" SIZE="10" > 
      To: <INPUT TYPE="TEXT" NAME="ProviderCreds_School2End_1" VALUE="<<ProviderCreds_School2End_1>>" ONCHANGE="return vDate(this);" MAXLENGTH="10" SIZE="10" > 
    </TD>
  </TR>
  <TR>
    <TD CLASS="strcol" >Graduation Date </TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="TEXT" NAME="ProviderCreds_School2GradDate_1" VALUE="<<ProviderCreds_School2GradDate_1>>" ONCHANGE="return vDate(this);" MAXLENGTH="10" SIZE="10" > 
    </TD>
  </TR>
  <TR>
    <TD CLASS="strcol" >(3) Institution </TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="TEXT" NAME="ProviderCreds_School3_1" VALUE="<<ProviderCreds_School3_1>>" SIZE="50" > 
    </TD>
  </TR>
  <TR>
    <TD CLASS="strcol" >Degree Awarded</TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="TEXT" NAME="ProviderCreds_School3Degree_1" VALUE="<<ProviderCreds_School3Degree_1>>" SIZE="50" > 
    </TD>
  </TR>
  <TR>
    <TD CLASS="strcol" >Mailing Address </TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="TEXT" NAME="ProviderCreds_School3Addr_1" VALUE="<<ProviderCreds_School3Addr_1>>" SIZE="50" > 
    </TD>
  </TR>
  <TR>
    <TD CLASS="strcol" >City </TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="TEXT" NAME="ProviderCreds_School3City_1" VALUE="<<ProviderCreds_School3City_1>>" SIZE="50" > 
    </TD>
  </TR>
  <TR>
    <TD CLASS="strcol" >State </TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="TEXT" NAME="ProviderCreds_School3ST_1" VALUE="<<ProviderCreds_School3ST_1>>" SIZE="50" > 
    </TD>
  </TR>
  <TR>
    <TD CLASS="strcol" >Zip Code</TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="TEXT" NAME="ProviderCreds_School3Zip_1" VALUE="<<ProviderCreds_School3Zip_1>>" SIZE="50" > 
    </TD>
  </TR>
  <TR>
    <TD CLASS="strcol" >Telephone Number:</TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="TEXT" NAME="ProviderCreds_School3Ph_1" VALUE="<<ProviderCreds_School3Ph_1>>" SIZE="50" > 
    </TD>
  </TR>
  <TR>
    <TD CLASS="strcol" >Dates Attended (mo/day/year) </TD>
    <TD CLASS="strcol" >
      From: <INPUT TYPE="TEXT" NAME="ProviderCreds_School3Start_1" VALUE="<<ProviderCreds_School3Start_1>>" ONCHANGE="return vDate(this);" MAXLENGTH="10" SIZE="10" > 
      To: <INPUT TYPE="TEXT" NAME="ProviderCreds_School3End_1" VALUE="<<ProviderCreds_School3End_1>>" ONCHANGE="return vDate(this);" MAXLENGTH="10" SIZE="10" > 
    </TD>
  </TR>
  <TR>
    <TD CLASS="strcol" >Graduation Date </TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="TEXT" NAME="ProviderCreds_School3GradDate_1" VALUE="<<ProviderCreds_School3GradDate_1>>" ONCHANGE="return vDate(this);" MAXLENGTH="10" SIZE="10" > 
    </TD>
  </TR>
  </TR>
    </TABLE></TD></TR>
    <TR ><TD ><TABLE CLASS="home fullsize" >
  <TR> <TD CLASS="port hdrtxt" COLSPAN="2" >SECTION 5: TRAINING Internship/Residency/Fellowship/Preceptorship/Other </TD> </TR>
  <TR>
    <TD CLASS="strcol" COLSPAN="2" >List all, completed or not. If you require additional space, continue in Section 14, or attach a separate sheet. 
  <TR>
    <TD CLASS="strcol" COLSPAN="2" >(1) Type of Program:</TD>
  </TR>
  <TR>
    <TD CLASS="strcol" COLSPAN="2" >
      <INPUT TYPE="checkbox" NAME="ProviderCreds_Train1Intern_1" VALUE="1" <<ProviderCreds_Train1Intern_1=checkbox>> > Internship 
      <INPUT TYPE="checkbox" NAME="ProviderCreds_Train1Res_1" VALUE="1" <<ProviderCreds_Train1Res_1=checkbox>> > Residency 
      <INPUT TYPE="checkbox" NAME="ProviderCreds_Train1Fellow_1" VALUE="1" <<ProviderCreds_Train1Fellow_1=checkbox>> > Fellowship 
      <INPUT TYPE="checkbox" NAME="ProviderCreds_Train1Precept_1" VALUE="1" <<ProviderCreds_Train1Precept_1=checkbox>> > Preceptorship 
      <INPUT TYPE="checkbox" NAME="ProviderCreds_Train1Other_1" VALUE="1" <<ProviderCreds_Train1Other_1=checkbox>> > Other (specify)
    </TD>
  </TR>
  <TR>
    <TD CLASS="strcol" COLSPAN="2" > Other (specify)
      <INPUT TYPE="TEXT" NAME="ProviderCreds_Train1Specify_1" VALUE="<<ProviderCreds_Train1Specify_1>>" SIZE="50" > 
    </TD>
  </TR>
  <TR>
    <TD CLASS="strcol" COLSPAN="2" >
Was program successfully completed: 
      <INPUT TYPE="radio" NAME="ProviderCreds_Train1Complete_1" VALUE=1 <<ProviderCreds_Train1Complete_1=1>> > Yes
      <INPUT TYPE="radio" NAME="ProviderCreds_Train1Complete_1" VALUE=0 <<ProviderCreds_Train1Complete_1=0>> > No
    </TD>
  </TR>
  <TR>
    <TD CLASS="strcol" >Specialty </TD>
    <TD CLASS="strcol" >
      <INPUT ID="MCAutocompleteTrain1Specialty" TYPE="text" VALUE="[[DBA->getxrefWithDef(%form+xOccupationSnomed+<<<ProviderCreds_Train1Specialty_1>>>+Description)]]" ONFOCUS="select()" SIZE="50" />
      <INPUT TYPE="hidden" NAME="ProviderCreds_Train1Specialty_1" VALUE="<<ProviderCreds_Train1Specialty_1>>" >
    </TD>
  </TR>
  <TR>
    <TD CLASS="strcol" >Institution </TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="TEXT" NAME="ProviderCreds_Train1_1" VALUE="<<ProviderCreds_Train1_1>>" SIZE="50" > 
    </TD>
  </TR>
  <TR>
    <TD CLASS="strcol" >Your Program Director </TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="TEXT" NAME="ProviderCreds_Train1Director_1" VALUE="<<ProviderCreds_Train1Director_1>>" SIZE="50" > 
    </TD>
  </TR>
  <TR>
    <TD CLASS="strcol" >Address </TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="TEXT" NAME="ProviderCreds_Train1Addr_1" VALUE="<<ProviderCreds_Train1Addr_1>>" SIZE="50" > 
    </TD>
  </TR>
  <TR>
    <TD CLASS="strcol" >City </TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="TEXT" NAME="ProviderCreds_Train1City_1" VALUE="<<ProviderCreds_Train1City_1>>" SIZE="50" > 
    </TD>
  </TR>
  <TR>
    <TD CLASS="strcol" >State </TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="TEXT" NAME="ProviderCreds_Train1ST_1" VALUE="<<ProviderCreds_Train1ST_1>>" SIZE="50" > 
    </TD>
  </TR>
  <TR>
    <TD CLASS="strcol" >Zip Code </TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="TEXT" NAME="ProviderCreds_Train1Zip_1" VALUE="<<ProviderCreds_Train1Zip_1>>" SIZE="50" > 
    </TD>
  </TR>
  <TR>
    <TD CLASS="strcol" >Phone Number </TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="TEXT" NAME="ProviderCreds_Train1Ph_1" VALUE="<<ProviderCreds_Train1Ph_1>>" SIZE="50" > 
    </TD>
  </TR>
  <TR>
    <TD CLASS="strcol" >Dates Attended (mo/day/year) </TD>
    <TD CLASS="strcol" >
      From: <INPUT TYPE="TEXT" NAME="ProviderCreds_Train1Start_1" VALUE="<<ProviderCreds_Train1Start_1>>" ONCHANGE="return vDate(this);" MAXLENGTH="10" SIZE="10" > 
      To: <INPUT TYPE="TEXT" NAME="ProviderCreds_Train1End_1" VALUE="<<ProviderCreds_Train1End_1>>" ONCHANGE="return vDate(this);" MAXLENGTH="10" SIZE="10" > 
    </TD>
  </TR>
  <TR>
    <TD CLASS="strcol" COLSPAN="2" >(2) Type of Program: </TD>
  </TR>
  <TR>
    <TD CLASS="strcol" COLSPAN="2" >
      <INPUT TYPE="checkbox" NAME="ProviderCreds_Train2Intern_1" VALUE="1" <<ProviderCreds_Train2Intern_1=checkbox>> > Internship 
      <INPUT TYPE="checkbox" NAME="ProviderCreds_Train2Res_1" VALUE="1" <<ProviderCreds_Train2Res_1=checkbox>> > Residency 
      <INPUT TYPE="checkbox" NAME="ProviderCreds_Train2Fellow_1" VALUE="1" <<ProviderCreds_Train2Fellow_1=checkbox>> > Fellowship 
      <INPUT TYPE="checkbox" NAME="ProviderCreds_Train2Precept_1" VALUE="1" <<ProviderCreds_Train2Precept_1=checkbox>> > Preceptorship 
      <INPUT TYPE="checkbox" NAME="ProviderCreds_Train2Other_1" VALUE="1" <<ProviderCreds_Train2Other_1=checkbox>> > Other (specify)
    </TD>
  </TR>
  <TR>
    <TD CLASS="strcol" COLSPAN="2" > Other (specify)
      <INPUT TYPE="TEXT" NAME="ProviderCreds_Train2Specify_1" VALUE="<<ProviderCreds_Train2Specify_1>>" SIZE="50" > 
    </TD>
  </TR>
  <TR>
    <TD CLASS="strcol" COLSPAN="2" >
Was program successfully completed? 
      <INPUT TYPE="radio" NAME="ProviderCreds_Train2Complete_1" VALUE=1 <<ProviderCreds_Train2Complete_1=1>> > Yes
      <INPUT TYPE="radio" NAME="ProviderCreds_Train2Complete_1" VALUE=0 <<ProviderCreds_Train2Complete_1=0>> > No
    </TD>
  </TR>
  <TR>
    <TD CLASS="strcol" >Specialty </TD>
    <TD CLASS="strcol" >
      <INPUT ID="MCAutocompleteTrain2Specialty" TYPE="text" VALUE="[[DBA->getxrefWithDef(%form+xOccupationSnomed+<<<ProviderCreds_Train2Specialty_1>>>+Description)]]" ONFOCUS="select()" SIZE="50" />
      <INPUT TYPE="hidden" NAME="ProviderCreds_Train2Specialty_1" VALUE="<<ProviderCreds_Train2Specialty_1>>" >
    </TD>
  </TR>
  <TR>
    <TD CLASS="strcol" >Institution </TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="TEXT" NAME="ProviderCreds_Train2_1" VALUE="<<ProviderCreds_Train2_1>>" SIZE="50" > 
    </TD>
  </TR>
  <TR>
    <TD CLASS="strcol" >Your Program Director </TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="TEXT" NAME="ProviderCreds_Train2Director_1" VALUE="<<ProviderCreds_Train2Director_1>>" SIZE="50" > 
    </TD>
  </TR>
  <TR>
    <TD CLASS="strcol" >Address </TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="TEXT" NAME="ProviderCreds_Train2Addr_1" VALUE="<<ProviderCreds_Train2Addr_1>>" SIZE="50" > 
    </TD>
  </TR>
  <TR>
    <TD CLASS="strcol" >City </TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="TEXT" NAME="ProviderCreds_Train2City_1" VALUE="<<ProviderCreds_Train2City_1>>" SIZE="50" > 
    </TD>
  </TR>
  <TR>
    <TD CLASS="strcol" >State </TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="TEXT" NAME="ProviderCreds_Train2ST_1" VALUE="<<ProviderCreds_Train2ST_1>>" SIZE="50" > 
    </TD>
  </TR>
  <TR>
    <TD CLASS="strcol" >Zip Code </TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="TEXT" NAME="ProviderCreds_Train2Zip_1" VALUE="<<ProviderCreds_Train2Zip_1>>" SIZE="50" > 
    </TD>
  </TR>
  <TR>
    <TD CLASS="strcol" >Phone Number </TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="TEXT" NAME="ProviderCreds_Train2Ph_1" VALUE="<<ProviderCreds_Train2Ph_1>>" SIZE="50" > 
    </TD>
  </TR>
  <TR>
    <TD CLASS="strcol" >Dates Attended (mo/day/year) </TD>
    <TD CLASS="strcol" >
      From: <INPUT TYPE="TEXT" NAME="ProviderCreds_Train2Start_1" VALUE="<<ProviderCreds_Train2Start_1>>" ONCHANGE="return vDate(this);" MAXLENGTH="10" SIZE="10" > 
      To: <INPUT TYPE="TEXT" NAME="ProviderCreds_Train2End_1" VALUE="<<ProviderCreds_Train2End_1>>" ONCHANGE="return vDate(this);" MAXLENGTH="10" SIZE="10" > 
    </TD>
  </TR>
  <TR>
    <TD CLASS="strcol" COLSPAN="2" >(3) Type of Program:</TD>
  </TR>
  <TR>
    <TD CLASS="strcol" COLSPAN="2" >
      <INPUT TYPE="checkbox" NAME="ProviderCreds_Train3Intern_1" VALUE="1" <<ProviderCreds_Train3Intern_1=checkbox>> > Internship 
      <INPUT TYPE="checkbox" NAME="ProviderCreds_Train3Res_1" VALUE="1" <<ProviderCreds_Train3Res_1=checkbox>> > Residency 
      <INPUT TYPE="checkbox" NAME="ProviderCreds_Train3Fellow_1" VALUE="1" <<ProviderCreds_Train3Fellow_1=checkbox>> > Fellowship 
      <INPUT TYPE="checkbox" NAME="ProviderCreds_Train3Precept_1" VALUE="1" <<ProviderCreds_Train3Precept_1=checkbox>> > Preceptorship 
      <INPUT TYPE="checkbox" NAME="ProviderCreds_Train3Other_1" VALUE="1" <<ProviderCreds_Train3Other_1=checkbox>> > Other (specify)
    </TD>
  </TR>
  <TR>
    <TD CLASS="strcol" COLSPAN="2" > Other (specify)
      <INPUT TYPE="TEXT" NAME="ProviderCreds_Train3Specify_1" VALUE="<<ProviderCreds_Train3Specify_1>>" SIZE="50" > 
    </TD>
  </TR>
  <TR>
    <TD CLASS="strcol" COLSPAN="2" >
Was program successfully completed? 
      <INPUT TYPE="radio" NAME="ProviderCreds_Train3Complete_1" VALUE=1 <<ProviderCreds_Train3Complete_1=1>> > Yes
      <INPUT TYPE="radio" NAME="ProviderCreds_Train3Complete_1" VALUE=0 <<ProviderCreds_Train3Complete_1=0>> > No
    </TD>
  </TR>
  <TR>
    <TD CLASS="strcol" >Specialty </TD>
    <TD CLASS="strcol" >
      <INPUT ID="MCAutocompleteTrain3Specialty" TYPE="text" VALUE="[[DBA->getxrefWithDef(%form+xOccupationSnomed+<<<ProviderCreds_Train3Specialty_1>>>+Description)]]" ONFOCUS="select()" SIZE="50" />
      <INPUT TYPE="hidden" NAME="ProviderCreds_Train3Specialty_1" VALUE="<<ProviderCreds_Train3Specialty_1>>" >
    </TD>
  </TR>
  <TR>
    <TD CLASS="strcol" >Institution </TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="TEXT" NAME="ProviderCreds_Train3_1" VALUE="<<ProviderCreds_Train3_1>>" SIZE="50" > 
    </TD>
  </TR>
  <TR>
    <TD CLASS="strcol" >Your Program Director </TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="TEXT" NAME="ProviderCreds_Train3Director_1" VALUE="<<ProviderCreds_Train3Director_1>>" SIZE="50" > 
    </TD>
  </TR>
  <TR>
    <TD CLASS="strcol" >Address </TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="TEXT" NAME="ProviderCreds_Train3Addr_1" VALUE="<<ProviderCreds_Train3Addr_1>>" SIZE="50" > 
    </TD>
  </TR>
  <TR>
    <TD CLASS="strcol" >City </TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="TEXT" NAME="ProviderCreds_Train3City_1" VALUE="<<ProviderCreds_Train3City_1>>" SIZE="50" > 
    </TD>
  </TR>
  <TR>
    <TD CLASS="strcol" >State </TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="TEXT" NAME="ProviderCreds_Train3ST_1" VALUE="<<ProviderCreds_Train3ST_1>>" SIZE="50" > 
    </TD>
  </TR>
  <TR>
    <TD CLASS="strcol" >Zip Code </TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="TEXT" NAME="ProviderCreds_Train3Zip_1" VALUE="<<ProviderCreds_Train3Zip_1>>" SIZE="50" > 
    </TD>
  </TR>
  <TR>
    <TD CLASS="strcol" >Phone Number </TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="TEXT" NAME="ProviderCreds_Train3Ph_1" VALUE="<<ProviderCreds_Train3Ph_1>>" SIZE="50" > 
    </TD>
  </TR>
  <TR>
    <TD CLASS="strcol" >Dates Attended (mo/day/year) </TD>
    <TD CLASS="strcol" >
      From: <INPUT TYPE="TEXT" NAME="ProviderCreds_Train3Start_1" VALUE="<<ProviderCreds_Train3Start_1>>" ONCHANGE="return vDate(this);" MAXLENGTH="10" SIZE="10" > 
      To: <INPUT TYPE="TEXT" NAME="ProviderCreds_Train3End_1" VALUE="<<ProviderCreds_Train3End_1>>" ONCHANGE="return vDate(this);" MAXLENGTH="10" SIZE="10" > 
    </TD>
  </TR>
  <TR>
    <TD CLASS="strcol" COLSPAN="2" >(4) Type of Program:</TD>
  </TR>
  <TR>
    <TD CLASS="strcol" COLSPAN="2" >
      <INPUT TYPE="checkbox" NAME="ProviderCreds_Train4Intern_1" VALUE="1" <<ProviderCreds_Train4Intern_1=checkbox>> > Internship 
      <INPUT TYPE="checkbox" NAME="ProviderCreds_Train4Res_1" VALUE="1" <<ProviderCreds_Train4Res_1=checkbox>> > Residency 
      <INPUT TYPE="checkbox" NAME="ProviderCreds_Train4Fellow_1" VALUE="1" <<ProviderCreds_Train4Fellow_1=checkbox>> > Fellowship 
      <INPUT TYPE="checkbox" NAME="ProviderCreds_Train4Precept_1" VALUE="1" <<ProviderCreds_Train4Precept_1=checkbox>> > Preceptorship 
      <INPUT TYPE="checkbox" NAME="ProviderCreds_Train4Other_1" VALUE="1" <<ProviderCreds_Train4Other_1=checkbox>> > Other (specify)
    </TD>
  </TR>
  <TR>
    <TD CLASS="strcol" COLSPAN="2" > Other (specify)
      <INPUT TYPE="TEXT" NAME="ProviderCreds_Train4Specify_1" VALUE="<<ProviderCreds_Train4Specify_1>>" SIZE="50" > 
    </TD>
  </TR>
  <TR>
    <TD CLASS="strcol" COLSPAN="2" >
Was program successfully completed? 
      <INPUT TYPE="radio" NAME="ProviderCreds_Train4Complete_1" VALUE=1 <<ProviderCreds_Train4Complete_1=1>> > Yes
      <INPUT TYPE="radio" NAME="ProviderCreds_Train4Complete_1" VALUE=0 <<ProviderCreds_Train4Complete_1=0>> > No
    </TD>
  </TR>
  <TR>
    <TD CLASS="strcol" >Specialty </TD>
    <TD CLASS="strcol" >
      <INPUT ID="MCAutocompleteTrain4Specialty" TYPE="text" VALUE="[[DBA->getxrefWithDef(%form+xOccupationSnomed+<<<ProviderCreds_Train4Specialty_1>>>+Description)]]" ONFOCUS="select()" SIZE="50" />
      <INPUT TYPE="hidden" NAME="ProviderCreds_Train4Specialty_1" VALUE="<<ProviderCreds_Train4Specialty_1>>" >
    </TD>
  </TR>
  <TR>
    <TD CLASS="strcol" >Institution </TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="TEXT" NAME="ProviderCreds_Train4_1" VALUE="<<ProviderCreds_Train4_1>>" SIZE="50" > 
    </TD>
  </TR>
  <TR>
    <TD CLASS="strcol" >Your Program Director </TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="TEXT" NAME="ProviderCreds_Train4Director_1" VALUE="<<ProviderCreds_Train4Director_1>>" SIZE="50" > 
    </TD>
  </TR>
  <TR>
    <TD CLASS="strcol" >Address </TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="TEXT" NAME="ProviderCreds_Train4Addr_1" VALUE="<<ProviderCreds_Train4Addr_1>>" SIZE="50" > 
    </TD>
  </TR>
  <TR>
    <TD CLASS="strcol" >City </TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="TEXT" NAME="ProviderCreds_Train4City_1" VALUE="<<ProviderCreds_Train4City_1>>" SIZE="50" > 
    </TD>
  </TR>
  <TR>
    <TD CLASS="strcol" >State </TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="TEXT" NAME="ProviderCreds_Train4ST_1" VALUE="<<ProviderCreds_Train4ST_1>>" SIZE="50" > 
    </TD>
  </TR>
  <TR>
    <TD CLASS="strcol" >Zip Code </TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="TEXT" NAME="ProviderCreds_Train4Zip_1" VALUE="<<ProviderCreds_Train4Zip_1>>" SIZE="50" > 
    </TD>
  </TR>
  <TR>
    <TD CLASS="strcol" >Phone Number </TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="TEXT" NAME="ProviderCreds_Train4Ph_1" VALUE="<<ProviderCreds_Train4Ph_1>>" SIZE="50" > 
    </TD>
  </TR>
  <TR>
    <TD CLASS="strcol" >Dates Attended (mo/day/year) </TD>
    <TD CLASS="strcol" >
      From: <INPUT TYPE="TEXT" NAME="ProviderCreds_Train4Start_1" VALUE="<<ProviderCreds_Train4Start_1>>" ONCHANGE="return vDate(this);" MAXLENGTH="10" SIZE="10" > 
      To: <INPUT TYPE="TEXT" NAME="ProviderCreds_Train4End_1" VALUE="<<ProviderCreds_Train4End_1>>" ONCHANGE="return vDate(this);" MAXLENGTH="10" SIZE="10" > 
    </TD>
  </TR>
  </TR>
    </TABLE></TD></TR>
    <TR ><TD ><TABLE CLASS="home fullsize" >
  <TR> <TD CLASS="port hdrtxt" COLSPAN="2" >SECTION 6: ACADEMIC APPOINTMENTS </TD> </TR>
  <TR>
    <TD CLASS="strcol" COLSPAN="2" >List all, past and present. If additional space is needed, copy this sheet or continue in Section 14. </TD>
  </TR>
  <TR>
    <TD CLASS="strcol" >(1) Institution</TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="TEXT" NAME="ProviderCreds_Academic1_1" VALUE="<<ProviderCreds_Academic1_1>>" SIZE="50" > 
    </TD>
  </TR>
  <TR>
    <TD CLASS="strcol" >Address </TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="TEXT" NAME="ProviderCreds_Academic1Addr_1" VALUE="<<ProviderCreds_Academic1Addr_1>>" SIZE="50" > 
    </TD>
  </TR>
  <TR>
    <TD CLASS="strcol" >City </TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="TEXT" NAME="ProviderCreds_Academic1City_1" VALUE="<<ProviderCreds_Academic1City_1>>" SIZE="50" > 
    </TD>
  </TR>
  <TR>
    <TD CLASS="strcol" >State </TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="TEXT" NAME="ProviderCreds_Academic1ST_1" VALUE="<<ProviderCreds_Academic1ST_1>>" SIZE="50" > 
    </TD>
  </TR>
  <TR>
    <TD CLASS="strcol" >Zip Code </TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="TEXT" NAME="ProviderCreds_Academic1Zip_1" VALUE="<<ProviderCreds_Academic1Zip_1>>" SIZE="50" > 
    </TD>
  </TR>
  <TR>
    <TD CLASS="strcol" >Phone Number </TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="TEXT" NAME="ProviderCreds_Academic1Ph_1" VALUE="<<ProviderCreds_Academic1Ph_1>>" SIZE="50" > 
    </TD>
  </TR>
  <TR>
    <TD CLASS="strcol" >Position/Rank </TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="TEXT" NAME="ProviderCreds_Academic1Postion_1" VALUE="<<ProviderCreds_Academic1Postion_1>>" SIZE="50" > 
    </TD>
  </TR>
  <TR>
    <TD CLASS="strcol" >Inclusive Dates (mo/day/year) </TD>
    <TD CLASS="strcol" >
      From: <INPUT TYPE="TEXT" NAME="ProviderCreds_Academic1Start_1" VALUE="<<ProviderCreds_Academic1Start_1>>" ONCHANGE="return vDate(this);" MAXLENGTH="10" SIZE="10" > 
      To: <INPUT TYPE="TEXT" NAME="ProviderCreds_Academic1End_1" VALUE="<<ProviderCreds_Academic1End_1>>" ONCHANGE="return vDate(this);" MAXLENGTH="10" SIZE="10" > 
    </TD>
  </TR>
  <TR>
    <TD CLASS="strcol" >(2) Institution</TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="TEXT" NAME="ProviderCreds_Academic2_1" VALUE="<<ProviderCreds_Academic2_1>>" SIZE="50" > 
    </TD>
  </TR>
  <TR>
    <TD CLASS="strcol" >Address </TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="TEXT" NAME="ProviderCreds_Academic2Addr_1" VALUE="<<ProviderCreds_Academic2Addr_1>>" SIZE="50" > 
    </TD>
  </TR>
  <TR>
    <TD CLASS="strcol" >City </TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="TEXT" NAME="ProviderCreds_Academic2City_1" VALUE="<<ProviderCreds_Academic2City_1>>" SIZE="50" > 
    </TD>
  </TR>
  <TR>
    <TD CLASS="strcol" >State </TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="TEXT" NAME="ProviderCreds_Academic2ST_1" VALUE="<<ProviderCreds_Academic2ST_1>>" SIZE="50" > 
    </TD>
  </TR>
  <TR>
    <TD CLASS="strcol" >Zip Code </TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="TEXT" NAME="ProviderCreds_Academic2Zip_1" VALUE="<<ProviderCreds_Academic2Zip_1>>" SIZE="50" > 
    </TD>
  </TR>
  <TR>
    <TD CLASS="strcol" >Phone Number </TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="TEXT" NAME="ProviderCreds_Academic2Ph_1" VALUE="<<ProviderCreds_Academic2Ph_1>>" SIZE="50" > 
    </TD>
  </TR>
  <TR>
    <TD CLASS="strcol" >Position/Rank </TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="TEXT" NAME="ProviderCreds_Academic2Postion_1" VALUE="<<ProviderCreds_Academic2Postion_1>>" SIZE="50" > 
    </TD>
  </TR>
  <TR>
    <TD CLASS="strcol" >Inclusive Dates (mo/day/year) </TD>
    <TD CLASS="strcol" >
      From: <INPUT TYPE="TEXT" NAME="ProviderCreds_Academic2Start_1" VALUE="<<ProviderCreds_Academic2Start_1>>" ONCHANGE="return vDate(this);" MAXLENGTH="10" SIZE="10" > 
      To: <INPUT TYPE="TEXT" NAME="ProviderCreds_Academic2End_1" VALUE="<<ProviderCreds_Academic2End_1>>" ONCHANGE="return vDate(this);" MAXLENGTH="10" SIZE="10" > 
    </TD>
  </TR>
  <TR>
    <TD CLASS="strcol" >(3) Institution</TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="TEXT" NAME="ProviderCreds_Academic3_1" VALUE="<<ProviderCreds_Academic3_1>>" SIZE="50" > 
    </TD>
  </TR>
  <TR>
    <TD CLASS="strcol" >Address </TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="TEXT" NAME="ProviderCreds_Academic3Addr_1" VALUE="<<ProviderCreds_Academic3Addr_1>>" SIZE="50" > 
    </TD>
  </TR>
  <TR>
    <TD CLASS="strcol" >City </TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="TEXT" NAME="ProviderCreds_Academic3City_1" VALUE="<<ProviderCreds_Academic3City_1>>" SIZE="50" > 
    </TD>
  </TR>
  <TR>
    <TD CLASS="strcol" >State </TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="TEXT" NAME="ProviderCreds_Academic3ST_1" VALUE="<<ProviderCreds_Academic3ST_1>>" SIZE="50" > 
    </TD>
  </TR>
  <TR>
    <TD CLASS="strcol" >Zip Code </TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="TEXT" NAME="ProviderCreds_Academic3Zip_1" VALUE="<<ProviderCreds_Academic3Zip_1>>" SIZE="50" > 
    </TD>
  </TR>
  <TR>
    <TD CLASS="strcol" >Phone Number </TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="TEXT" NAME="ProviderCreds_Academic3Ph_1" VALUE="<<ProviderCreds_Academic3Ph_1>>" SIZE="50" > 
    </TD>
  </TR>
  <TR>
    <TD CLASS="strcol" >Position/Rank </TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="TEXT" NAME="ProviderCreds_Academic3Postion_1" VALUE="<<ProviderCreds_Academic3Postion_1>>" SIZE="50" > 
    </TD>
  </TR>
  <TR>
    <TD CLASS="strcol" >Inclusive Dates (mo/day/year) </TD>
    <TD CLASS="strcol" >
      From: <INPUT TYPE="TEXT" NAME="ProviderCreds_Academic3Start_1" VALUE="<<ProviderCreds_Academic3Start_1>>" ONCHANGE="return vDate(this);" MAXLENGTH="10" SIZE="10" > 
      To: <INPUT TYPE="TEXT" NAME="ProviderCreds_Academic3End_1" VALUE="<<ProviderCreds_Academic3End_1>>" ONCHANGE="return vDate(this);" MAXLENGTH="10" SIZE="10" > 
    </TD>
  </TR>
  </TR>
    </TABLE></TD></TR>
    <TR ><TD ><TABLE CLASS="home fullsize" >
  <TR> <TD CLASS="port hdrtxt" COLSPAN="2" >SECTION 7: HEALTH CARE AFFILIATIONS </TD> </TR>
  <TR>
    <TD CLASS="strcol" COLSPAN="2" >List, in chronological order, all hospital/health system affiliations where you have ever been employed, practiced, associated, or privileged for the purpose of providing patient care.  Do not list affiliations that were part of your training (Section 5). If additional space is required, copy this sheet or continue in Section 14. </TD>
  </TR>
  <TR>
    <TD CLASS="strcol" COLSPAN="2" >Indicate which of these is your "current primary and secondary admitting facility" (where you currently spend the greatest portion of your time). </TD>
  </TR>
  <TR>
    <TD CLASS="strcol" >(1) Facility Name </TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="TEXT" NAME="ProviderCreds_Hospital1_1" VALUE="<<ProviderCreds_Hospital1_1>>" SIZE="50" > 
    </TD>
  </TR>
  <TR>
    <TD CLASS="strcol" COLSPAN="2" >
      <INPUT TYPE="radio" NAME="ProviderCreds_Hospital1Priority_1" VALUE="P" <<ProviderCreds_Hospital1Priority_1=P>> >Primary
      <INPUT TYPE="radio" NAME="ProviderCreds_Hospital1Priority_1" VALUE="S" <<ProviderCreds_Hospital1Priority_1=S>> >Secondary
    </TD>
  </TR>
  <TR>
    <TD CLASS="strcol" >Complete Mailing Address </TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="TEXT" NAME="ProviderCreds_Hospital1Addr_1" VALUE="<<ProviderCreds_Hospital1Addr_1>>" SIZE="50" > 
    </TD>
  </TR>
  <TR>
    <TD CLASS="strcol" >City </TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="TEXT" NAME="ProviderCreds_Hospital1City_1" VALUE="<<ProviderCreds_Hospital1City_1>>" SIZE="50" > 
    </TD>
  </TR>
  <TR>
    <TD CLASS="strcol" >State </TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="TEXT" NAME="ProviderCreds_Hospital1ST_1" VALUE="<<ProviderCreds_Hospital1ST_1>>" SIZE="50" > 
    </TD>
  </TR>
  <TR>
    <TD CLASS="strcol" >Zip Code </TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="TEXT" NAME="ProviderCreds_Hospital1Zip_1" VALUE="<<ProviderCreds_Hospital1Zip_1>>" SIZE="50" > 
    </TD>
  </TR>
  <TR>
    <TD CLASS="strcol" >Telephone Number </TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="TEXT" NAME="ProviderCreds_Hospital1Ph_1" VALUE="<<ProviderCreds_Hospital1Ph_1>>" SIZE="50" > 
    </TD>
  </TR>
  <TR>
    <TD CLASS="strcol" >Dates of Appointment (mo/day/year) </TD>
    <TD CLASS="strcol" >
      From: <INPUT TYPE="TEXT" NAME="ProviderCreds_Hospital1Start_1" VALUE="<<ProviderCreds_Hospital1Start_1>>" ONCHANGE="return vDate(this);" MAXLENGTH="10" SIZE="10" > 
      To: <INPUT TYPE="TEXT" NAME="ProviderCreds_Hospital1End_1" VALUE="<<ProviderCreds_Hospital1End_1>>" ONCHANGE="return vDate(this);" MAXLENGTH="10" SIZE="10" > 
    </TD>
  </TR>
  <TR>
    <TD CLASS="strcol" >Staff Category </TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="TEXT" NAME="ProviderCreds_Hospital1StaffCategory_1" VALUE="<<ProviderCreds_Hospital1StaffCategory_1>>" SIZE="50" > 
    </TD>
  </TR>
  <TR>
    <TD CLASS="strcol" >Reason for Discontinuance </TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="TEXT" NAME="ProviderCreds_Hospital1Reason_1" VALUE="<<ProviderCreds_Hospital1Reason_1>>" SIZE="50" > 
    </TD>
  </TR>
  <TR>
    <TD CLASS="strcol" >Department or Service</TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="TEXT" NAME="ProviderCreds_Hospital1Dept_1" VALUE="<<ProviderCreds_Hospital1Dept_1>>" SIZE="50" > 
    </TD>
  </TR>
  <TR>
    <TD CLASS="strcol" >(2) Facility Name</TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="TEXT" NAME="ProviderCreds_Hospital2_1" VALUE="<<ProviderCreds_Hospital2_1>>" SIZE="50" > 
    </TD>
  </TR>
  <TR>
    <TD CLASS="strcol" COLSPAN="2" >
      <INPUT TYPE="radio" NAME="ProviderCreds_Hospital2Priority_1" VALUE="P" <<ProviderCreds_Hospital2Priority_1=P>> >Primary
      <INPUT TYPE="radio" NAME="ProviderCreds_Hospital2Priority_1" VALUE="S" <<ProviderCreds_Hospital2Priority_1=S>> >Secondary
    </TD>
  </TR>
  <TR>
    <TD CLASS="strcol" >Complete Mailing Address </TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="TEXT" NAME="ProviderCreds_Hospital2Addr_1" VALUE="<<ProviderCreds_Hospital2Addr_1>>" SIZE="50" > 
    </TD>
  </TR>
  <TR>
    <TD CLASS="strcol" >City </TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="TEXT" NAME="ProviderCreds_Hospital2City_1" VALUE="<<ProviderCreds_Hospital2City_1>>" SIZE="50" > 
    </TD>
  </TR>
  <TR>
    <TD CLASS="strcol" >State </TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="TEXT" NAME="ProviderCreds_Hospital2ST_1" VALUE="<<ProviderCreds_Hospital2ST_1>>" SIZE="50" > 
    </TD>
  </TR>
  <TR>
    <TD CLASS="strcol" >Zip Code </TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="TEXT" NAME="ProviderCreds_Hospital2Zip_1" VALUE="<<ProviderCreds_Hospital2Zip_1>>" SIZE="50" > 
    </TD>
  </TR>
  <TR>
    <TD CLASS="strcol" >Telephone Number </TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="TEXT" NAME="ProviderCreds_Hospital2Ph_1" VALUE="<<ProviderCreds_Hospital2Ph_1>>" SIZE="50" > 
    </TD>
  </TR>
  <TR>
    <TD CLASS="strcol" >Dates of Appointment (mo/day/year) </TD>
    <TD CLASS="strcol" >
      From: <INPUT TYPE="TEXT" NAME="ProviderCreds_Hospital2Start_1" VALUE="<<ProviderCreds_Hospital2Start_1>>" ONCHANGE="return vDate(this);" MAXLENGTH="10" SIZE="10" > 
      To: <INPUT TYPE="TEXT" NAME="ProviderCreds_Hospital2End_1" VALUE="<<ProviderCreds_Hospital2End_1>>" ONCHANGE="return vDate(this);" MAXLENGTH="10" SIZE="10" > 
    </TD>
  </TR>
  <TR>
    <TD CLASS="strcol" >Staff Category </TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="TEXT" NAME="ProviderCreds_Hospital2StaffCategory_1" VALUE="<<ProviderCreds_Hospital2StaffCategory_1>>" SIZE="50" > 
    </TD>
  </TR>
  <TR>
    <TD CLASS="strcol" >Reason for Discontinuance </TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="TEXT" NAME="ProviderCreds_Hospital2Reason_1" VALUE="<<ProviderCreds_Hospital2Reason_1>>" SIZE="50" > 
    </TD>
  </TR>
  <TR>
    <TD CLASS="strcol" >Department or Service </TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="TEXT" NAME="ProviderCreds_Hospital2Dept_1" VALUE="<<ProviderCreds_Hospital2Dept_1>>" SIZE="50" > 
    </TD>
  </TR>
  <TR>
    <TD CLASS="strcol" >(3) Facility Name </TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="TEXT" NAME="ProviderCreds_Hospital3_1" VALUE="<<ProviderCreds_Hospital3_1>>" SIZE="50" > 
    </TD>
  </TR>
  <TR>
    <TD CLASS="strcol" COLSPAN="2" >
      <INPUT TYPE="radio" NAME="ProviderCreds_Hospital3Priority_1" VALUE="P" <<ProviderCreds_Hospital3Priority_1=P>> >Primary
      <INPUT TYPE="radio" NAME="ProviderCreds_Hospital3Priority_1" VALUE="S" <<ProviderCreds_Hospital3Priority_1=S>> >Secondary
    </TD>
  </TR>
  <TR>
    <TD CLASS="strcol" >Complete Mailing Address </TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="TEXT" NAME="ProviderCreds_Hospital3Addr_1" VALUE="<<ProviderCreds_Hospital3Addr_1>>" SIZE="50" > 
    </TD>
  </TR>
  <TR>
    <TD CLASS="strcol" >City </TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="TEXT" NAME="ProviderCreds_Hospital3City_1" VALUE="<<ProviderCreds_Hospital3City_1>>" SIZE="50" > 
    </TD>
  </TR>
  <TR>
    <TD CLASS="strcol" >State </TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="TEXT" NAME="ProviderCreds_Hospital3ST_1" VALUE="<<ProviderCreds_Hospital3ST_1>>" SIZE="50" > 
    </TD>
  </TR>
  <TR>
    <TD CLASS="strcol" >Zip Code </TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="TEXT" NAME="ProviderCreds_Hospital3Zip_1" VALUE="<<ProviderCreds_Hospital3Zip_1>>" SIZE="50" > 
    </TD>
  </TR>
  <TR>
    <TD CLASS="strcol" >Telephone Number </TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="TEXT" NAME="ProviderCreds_Hospital3Ph_1" VALUE="<<ProviderCreds_Hospital3Ph_1>>" SIZE="50" > 
    </TD>
  </TR>
  <TR>
    <TD CLASS="strcol" >Dates of Appointment (mo/day/year) </TD>
    <TD CLASS="strcol" >
      From: <INPUT TYPE="TEXT" NAME="ProviderCreds_Hospital3Start_1" VALUE="<<ProviderCreds_Hospital3Start_1>>" ONCHANGE="return vDate(this);" MAXLENGTH="10" SIZE="10" > 
      To: <INPUT TYPE="TEXT" NAME="ProviderCreds_Hospital3End_1" VALUE="<<ProviderCreds_Hospital3End_1>>" ONCHANGE="return vDate(this);" MAXLENGTH="10" SIZE="10" > 
    </TD>
  </TR>
  <TR>
    <TD CLASS="strcol" >Staff Category </TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="TEXT" NAME="ProviderCreds_Hospital3StaffCategory_1" VALUE="<<ProviderCreds_Hospital3StaffCategory_1>>" SIZE="50" > 
    </TD>
  </TR>
  <TR>
    <TD CLASS="strcol" >Reason for Discontinuance </TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="TEXT" NAME="ProviderCreds_Hospital3Reason_1" VALUE="<<ProviderCreds_Hospital3Reason_1>>" SIZE="50" > 
    </TD>
  </TR>
  <TR>
    <TD CLASS="strcol" >Department or Service </TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="TEXT" NAME="ProviderCreds_Hospital3Dept_1" VALUE="<<ProviderCreds_Hospital3Dept_1>>" SIZE="50" > 
    </TD>
  </TR>
  </TR>
    </TABLE></TD></TR>
    <TR ><TD ><TABLE CLASS="home fullsize" >
  <TR> <TD CLASS="port hdrtxt" COLSPAN="2" >SECTION 8: OTHER PROFESSIONAL WORK HISTORY </TD> </TR>
  <TR>
    <TD CLASS="strcol" COLSPAN="2" >List, chronologically, all professional work history (i.e. clinics, partnerships, solo/group practices, employment). Include secondary agencies or clinics such as public health and family planning where you perform duties. Account for all time gaps of thirty (30) days or more. If additional space is needed, copy this page or continue in Section 14. </TD>
  </TR>
  <TR>
    <TD CLASS="strcol" >(1) Name </TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="TEXT" NAME="ProviderCreds_Work1_1" VALUE="<<ProviderCreds_Work1_1>>" SIZE="50" > 
    </TD>
  </TR>
  <TR>
    <TD CLASS="strcol" >(1) Nature of Affiliation </TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="TEXT" NAME="ProviderCreds_Work1Nature_1" VALUE="<<ProviderCreds_Work1Nature_1>>" SIZE="50" > 
    </TD>
  </TR>
  <TR>
    <TD CLASS="strcol" >Mailing Address </TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="TEXT" NAME="ProviderCreds_Work1Addr_1" VALUE="<<ProviderCreds_Work1Addr_1>>" SIZE="50" > 
    </TD>
  </TR>
  <TR>
    <TD CLASS="strcol" >City </TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="TEXT" NAME="ProviderCreds_Work1City_1" VALUE="<<ProviderCreds_Work1City_1>>" SIZE="50" > 
    </TD>
  </TR>
  <TR>
    <TD CLASS="strcol" >State </TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="TEXT" NAME="ProviderCreds_Work1ST_1" VALUE="<<ProviderCreds_Work1ST_1>>" SIZE="50" > 
    </TD>
  </TR>
  <TR>
    <TD CLASS="strcol" >Zip Code </TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="TEXT" NAME="ProviderCreds_Work1Zip_1" VALUE="<<ProviderCreds_Work1Zip_1>>" SIZE="50" > 
    </TD>
  </TR>
  <TR>
    <TD CLASS="strcol" >Telephone Number </TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="TEXT" NAME="ProviderCreds_Work1Ph_1" VALUE="<<ProviderCreds_Work1Ph_1>>" SIZE="50" > 
    </TD>
  </TR>
  <TR>
    <TD CLASS="strcol" >Dates of Affiliation (mo/day/year) </TD>
    <TD CLASS="strcol" >
      From: <INPUT TYPE="TEXT" NAME="ProviderCreds_Work1Start_1" VALUE="<<ProviderCreds_Work1Start_1>>" ONCHANGE="return vDate(this);" MAXLENGTH="10" SIZE="10" > 
      To: <INPUT TYPE="TEXT" NAME="ProviderCreds_Work1End_1" VALUE="<<ProviderCreds_Work1End_1>>" ONCHANGE="return vDate(this);" MAXLENGTH="10" SIZE="10" > 
    </TD>
  </TR>
  <TR>
    <TD CLASS="strcol" >Reason for Discontinuance </TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="TEXT" NAME="ProviderCreds_Work1Reason_1" VALUE="<<ProviderCreds_Work1Reason_1>>" SIZE="50" > 
    </TD>
  </TR>
  <TR>
    <TD CLASS="strcol" >(2) Name </TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="TEXT" NAME="ProviderCreds_Work2_1" VALUE="<<ProviderCreds_Work2_1>>" SIZE="50" > 
    </TD>
  </TR>
  <TR>
    <TD CLASS="strcol" >(2) Nature of Affiliation </TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="TEXT" NAME="ProviderCreds_Work2Nature_1" VALUE="<<ProviderCreds_Work2Nature_1>>" SIZE="50" > 
    </TD>
  </TR>
  <TR>
    <TD CLASS="strcol" >Mailing Address </TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="TEXT" NAME="ProviderCreds_Work2Addr_1" VALUE="<<ProviderCreds_Work2Addr_1>>" SIZE="50" > 
    </TD>
  </TR>
  <TR>
    <TD CLASS="strcol" >City </TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="TEXT" NAME="ProviderCreds_Work2City_1" VALUE="<<ProviderCreds_Work2City_1>>" SIZE="50" > 
    </TD>
  </TR>
  <TR>
    <TD CLASS="strcol" >State </TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="TEXT" NAME="ProviderCreds_Work2ST_1" VALUE="<<ProviderCreds_Work2ST_1>>" SIZE="50" > 
    </TD>
  </TR>
  <TR>
    <TD CLASS="strcol" >Zip Code </TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="TEXT" NAME="ProviderCreds_Work2Zip_1" VALUE="<<ProviderCreds_Work2Zip_1>>" SIZE="50" > 
    </TD>
  </TR>
  <TR>
    <TD CLASS="strcol" >Telephone Number </TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="TEXT" NAME="ProviderCreds_Work2Ph_1" VALUE="<<ProviderCreds_Work2Ph_1>>" SIZE="50" > 
    </TD>
  </TR>
  <TR>
    <TD CLASS="strcol" >Dates of Affiliation (mo/day/year) </TD>
    <TD CLASS="strcol" >
      From: <INPUT TYPE="TEXT" NAME="ProviderCreds_Work2Start_1" VALUE="<<ProviderCreds_Work2Start_1>>" ONCHANGE="return vDate(this);" MAXLENGTH="10" SIZE="10" > 
      To: <INPUT TYPE="TEXT" NAME="ProviderCreds_Work2End_1" VALUE="<<ProviderCreds_Work2End_1>>" ONCHANGE="return vDate(this);" MAXLENGTH="10" SIZE="10" > 
    </TD>
  </TR>
  <TR>
    <TD CLASS="strcol" >Reason for Discontinuance </TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="TEXT" NAME="ProviderCreds_Work2Reason_1" VALUE="<<ProviderCreds_Work2Reason_1>>" SIZE="50" > 
    </TD>
  </TR>
  <TR>
    <TD CLASS="strcol" >(3) Name </TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="TEXT" NAME="ProviderCreds_Work3_1" VALUE="<<ProviderCreds_Work3_1>>" SIZE="50" > 
    </TD>
  </TR>
  <TR>
    <TD CLASS="strcol" >(3) Nature of Affiliation </TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="TEXT" NAME="ProviderCreds_Work3Nature_1" VALUE="<<ProviderCreds_Work3Nature_1>>" SIZE="50" > 
    </TD>
  </TR>
  <TR>
    <TD CLASS="strcol" >Mailing Address </TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="TEXT" NAME="ProviderCreds_Work3Addr_1" VALUE="<<ProviderCreds_Work3Addr_1>>" SIZE="50" > 
    </TD>
  </TR>
  <TR>
    <TD CLASS="strcol" >City </TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="TEXT" NAME="ProviderCreds_Work3City_1" VALUE="<<ProviderCreds_Work3City_1>>" SIZE="50" > 
    </TD>
  </TR>
  <TR>
    <TD CLASS="strcol" >State </TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="TEXT" NAME="ProviderCreds_Work3ST_1" VALUE="<<ProviderCreds_Work3ST_1>>" SIZE="50" > 
    </TD>
  </TR>
  <TR>
    <TD CLASS="strcol" >Zip Code </TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="TEXT" NAME="ProviderCreds_Work3Zip_1" VALUE="<<ProviderCreds_Work3Zip_1>>" SIZE="50" > 
    </TD>
  </TR>
  <TR>
    <TD CLASS="strcol" >Telephone Number </TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="TEXT" NAME="ProviderCreds_Work3Ph_1" VALUE="<<ProviderCreds_Work3Ph_1>>" SIZE="50" > 
    </TD>
  </TR>
  <TR>
    <TD CLASS="strcol" >Dates of Affiliation (mo/day/year) </TD>
    <TD CLASS="strcol" >
      From: <INPUT TYPE="TEXT" NAME="ProviderCreds_Work3Start_1" VALUE="<<ProviderCreds_Work3Start_1>>" ONCHANGE="return vDate(this);" MAXLENGTH="10" SIZE="10" > 
      To: <INPUT TYPE="TEXT" NAME="ProviderCreds_Work3End_1" VALUE="<<ProviderCreds_Work3End_1>>" ONCHANGE="return vDate(this);" MAXLENGTH="10" SIZE="10" > 
    </TD>
  </TR>
  <TR>
    <TD CLASS="strcol" >Reason for Discontinuance </TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="TEXT" NAME="ProviderCreds_Work3Reason_1" VALUE="<<ProviderCreds_Work3Reason_1>>" SIZE="50" > 
    </TD>
  </TR>
  <TR>
    <TD CLASS="strcol" COLSPAN="2" >US Military/Public Health Service </TD>
  </TR>
  <TR>
    <TD CLASS="strcol" COLSPAN="2" >List all medical and surgical locations and dates. </TD>
  </TR>
  <TR>
    <TD CLASS="strcol" >Dates</TD>
    <TD CLASS="strcol" >
      From: <INPUT TYPE="TEXT" NAME="ProviderCreds_MilPH1Start_1" VALUE="<<ProviderCreds_MilPH1Start_1>>" SIZE="50" > 
      To: <INPUT TYPE="TEXT" NAME="ProviderCreds_MilPH1End_1" VALUE="<<ProviderCreds_MilPH1End_1>>" SIZE="50" > 
    </TD>
  </TR>
  <TR>
    <TD CLASS="strcol" >Location </TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="TEXT" NAME="ProviderCreds_MilPH1Loc_1" VALUE="<<ProviderCreds_MilPH1Loc_1>>" SIZE="50" > 
    </TD>
  </TR>
  <TR>
    <TD CLASS="strcol" >Branch of Service </TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="TEXT" NAME="ProviderCreds_MilPH1Branch_1" VALUE="<<ProviderCreds_MilPH1Branch_1>>" SIZE="50" > 
    </TD>
  </TR>
  <TR>
    <TD CLASS="strcol" >Dates</TD>
    <TD CLASS="strcol" >
      From: <INPUT TYPE="TEXT" NAME="ProviderCreds_MilPH2Start_1" VALUE="<<ProviderCreds_MilPH2Start_1>>" SIZE="50" > 
      To: <INPUT TYPE="TEXT" NAME="ProviderCreds_MilPH2End_1" VALUE="<<ProviderCreds_MilPH2End_1>>" SIZE="50" > 
    </TD>
  </TR>
  <TR>
    <TD CLASS="strcol" >Location </TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="TEXT" NAME="ProviderCreds_MilPH2Loc_1" VALUE="<<ProviderCreds_MilPH2Loc_1>>" SIZE="50" > 
    </TD>
  </TR>
  <TR>
    <TD CLASS="strcol" >Branch of Service </TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="TEXT" NAME="ProviderCreds_MilPH2Branch_1" VALUE="<<ProviderCreds_MilPH2Branch_1>>" SIZE="50" > 
    </TD>
  </TR>
  </TR>
    </TABLE></TD></TR>
    <TR ><TD ><TABLE CLASS="home fullsize" >
  <TR> <TD CLASS="port hdrtxt" COLSPAN="2" >SECTION 9: PROFESSIONAL LICENSE</TD> </TR>
  <TR>
    <TD CLASS="strcol" COLSPAN="2" >List all pending, current, and past professional licenses, registrations, and certifications to practice in your field.  Include states where you have ever applied to practice. Examples of "type" of license are MD, DO, DDS, PA, DC, CRNA, MSW, etc. </TD>
  </TR>
  <TR>
    <TD CLASS="strcol" >State </TD>
    <TD CLASS="strcol" >
      <SELECT NAME="ProviderCreds_License1ST_1">
        [[DBA->selxTable(%form+xState+<<ProviderCreds_License1ST_1>>+Descr)]]
      </SELECT>
    </TD>
  </TR>
  <TR>
    <TD CLASS="strcol" >Type </TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="TEXT" NAME="ProviderCreds_License1Type_1" VALUE="<<ProviderCreds_License1Type_1>>" SIZE="50" > 
    </TD>
  </TR>
  <TR>
    <TD CLASS="strcol" >Number </TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="TEXT" NAME="ProviderCreds_License1Num_1" VALUE="<<ProviderCreds_License1Num_1>>" SIZE="50" > 
    </TD>
  </TR>
  <TR>
    <TD CLASS="strcol" >Original Date of Issue </TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="TEXT" NAME="ProviderCreds_License1Start_1" VALUE="<<ProviderCreds_License1Start_1>>" ONCHANGE="return vDate(this);" MAXLENGTH="10" SIZE="10" > 
    </TD>
  </TR>
  <TR>
    <TD CLASS="strcol" >Expiration Date </TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="TEXT" NAME="ProviderCreds_License1Expire_1" VALUE="<<ProviderCreds_License1Expire_1>>" ONCHANGE="return vDate(this);" MAXLENGTH="10" SIZE="10" > 
    </TD>
  </TR>
  <TR>
    <TD CLASS="strcol" >State </TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="TEXT" NAME="ProviderCreds_License2ST_1" VALUE="<<ProviderCreds_License2ST_1>>" SIZE="50" > 
    </TD>
  </TR>
  <TR>
    <TD CLASS="strcol" >Type </TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="TEXT" NAME="ProviderCreds_License2Type_1" VALUE="<<ProviderCreds_License2Type_1>>" SIZE="50" > 
    </TD>
  </TR>
  <TR>
    <TD CLASS="strcol" >Number </TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="TEXT" NAME="ProviderCreds_License2Num_1" VALUE="<<ProviderCreds_License2Num_1>>" SIZE="50" > 
    </TD>
  </TR>
  <TR>
    <TD CLASS="strcol" >Original Date of Issue </TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="TEXT" NAME="ProviderCreds_License2Start_1" VALUE="<<ProviderCreds_License2Start_1>>" ONCHANGE="return vDate(this);" MAXLENGTH="10" SIZE="10" > 
    </TD>
  </TR>
  <TR>
    <TD CLASS="strcol" >Expiration Date </TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="TEXT" NAME="ProviderCreds_License2Expire_1" VALUE="<<ProviderCreds_License2Expire_1>>" ONCHANGE="return vDate(this);" MAXLENGTH="10" SIZE="10" > 
    </TD>
  </TR>
  <TR>
    <TD CLASS="strcol" >State </TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="TEXT" NAME="ProviderCreds_License3ST_1" VALUE="<<ProviderCreds_License3ST_1>>" SIZE="50" > 
    </TD>
  </TR>
  <TR>
    <TD CLASS="strcol" >Type </TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="TEXT" NAME="ProviderCreds_License3Type_1" VALUE="<<ProviderCreds_License3Type_1>>" SIZE="50" > 
    </TD>
  </TR>
  <TR>
    <TD CLASS="strcol" >Number </TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="TEXT" NAME="ProviderCreds_License3Num_1" VALUE="<<ProviderCreds_License3Num_1>>" SIZE="50" > 
    </TD>
  </TR>
  <TR>
    <TD CLASS="strcol" >Original Date of Issue </TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="TEXT" NAME="ProviderCreds_License3Start_1" VALUE="<<ProviderCreds_License3Start_1>>" ONCHANGE="return vDate(this);" MAXLENGTH="10" SIZE="10" > 
    </TD>
  </TR>
  <TR>
    <TD CLASS="strcol" >Expiration Date </TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="TEXT" NAME="ProviderCreds_License3Expire_1" VALUE="<<ProviderCreds_License3Expire_1>>" ONCHANGE="return vDate(this);" MAXLENGTH="10" SIZE="10" > 
    </TD>
  </TR>
  <TR>
    <TD CLASS="strcol" >State </TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="TEXT" NAME="ProviderCreds_License4ST_1" VALUE="<<ProviderCreds_License4ST_1>>" SIZE="50" > 
    </TD>
  </TR>
  <TR>
    <TD CLASS="strcol" >Type </TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="TEXT" NAME="ProviderCreds_License4Type_1" VALUE="<<ProviderCreds_License4Type_1>>" SIZE="50" > 
    </TD>
  </TR>
  <TR>
    <TD CLASS="strcol" >Number </TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="TEXT" NAME="ProviderCreds_License4Num_1" VALUE="<<ProviderCreds_License4Num_1>>" SIZE="50" > 
    </TD>
  </TR>
  <TR>
    <TD CLASS="strcol" >Original Date of Issue </TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="TEXT" NAME="ProviderCreds_License4Start_1" VALUE="<<ProviderCreds_License4Start_1>>" ONCHANGE="return vDate(this);" MAXLENGTH="10" SIZE="10" > 
    </TD>
  </TR>
  <TR>
    <TD CLASS="strcol" >Expiration Date </TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="TEXT" NAME="ProviderCreds_License4Expire_1" VALUE="<<ProviderCreds_License4Expire_1>>" ONCHANGE="return vDate(this);" MAXLENGTH="10" SIZE="10" > 
    </TD>
  </TR>
  <TR>
    <TD CLASS="strcol" >USMLE/ECFMG Number </TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="TEXT" NAME="ProviderCreds_USMLEECFMG_1" VALUE="<<ProviderCreds_USMLEECFMG_1>>" SIZE="50" > 
    </TD>
  </TR>
  <TR>
    <TD CLASS="strcol" >Certification Date </TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="TEXT" NAME="ProviderCreds_USMLEECFMGDate_1" VALUE="<<ProviderCreds_USMLEECFMGDate_1>>" ONCHANGE="return vDate(this);" MAXLENGTH="10" SIZE="10" > 
    </TD>
  </TR>
  </TR>
    </TABLE></TD></TR>
    <TR ><TD ><TABLE CLASS="home fullsize" >
  <TR> <TD CLASS="port hdrtxt" COLSPAN="2" >SECTION 10: CERTIFICATIONS AND REGISTRATIONS </TD> </TR>
  <TR>
    <TD CLASS="strcol" COLSPAN="2" >List all other current certifications and registrations</TD>
  </TR>
  <TR>
    <TD CLASS="strcol" COLSPAN="2" >(DEA=Federal Drug Enforcement Administration; BNDD=the Oklahoma CDS; CDS=Controlled Dangerous Substances)</TD>
  </TR>
  <TR>
    <TD CLASS="strcol" >State </TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="TEXT" NAME="ProviderCreds_DEA1ST_1" VALUE="<<ProviderCreds_DEA1ST_1>>" SIZE="50" > 
    </TD>
  </TR>
  <TR>
    <TD CLASS="strcol" >Type </TD>
    <TD CLASS="strcol" >DEA </TD>
  </TR>
  <TR>
    <TD CLASS="strcol" >Number </TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="TEXT" NAME="ProviderCreds_DEA1Num_1" VALUE="<<ProviderCreds_DEA1Num_1>>" SIZE="50" > 
    </TD>
  </TR>
  <TR>
    <TD CLASS="strcol" >Original Date of Issue </TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="TEXT" NAME="ProviderCreds_DEA1Start_1" VALUE="<<ProviderCreds_DEA1Start_1>>" ONCHANGE="return vDate(this);" MAXLENGTH="10" SIZE="10" > 
    </TD>
  </TR>
  <TR>
    <TD CLASS="strcol" >Expiration Date </TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="TEXT" NAME="ProviderCreds_DEA1Expire_1" VALUE="<<ProviderCreds_DEA1Expire_1>>" ONCHANGE="return vDate(this);" MAXLENGTH="10" SIZE="10" > 
    </TD>
  </TR>
  <TR>
    <TD CLASS="strcol" >State </TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="TEXT" NAME="ProviderCreds_DEA2ST_1" VALUE="<<ProviderCreds_DEA2ST_1>>" SIZE="50" > 
    </TD>
  </TR>
  <TR>
    <TD CLASS="strcol" >Type </TD>
    <TD CLASS="strcol" >DEA </TD>
  </TR>
  <TR>
    <TD CLASS="strcol" >Number </TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="TEXT" NAME="ProviderCreds_DEA2Num_1" VALUE="<<ProviderCreds_DEA2Num_1>>" SIZE="50" > 
    </TD>
  </TR>
  <TR>
    <TD CLASS="strcol" >Original Date of Issue </TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="TEXT" NAME="ProviderCreds_DEA2Start_1" VALUE="<<ProviderCreds_DEA2Start_1>>" ONCHANGE="return vDate(this);" MAXLENGTH="10" SIZE="10" > 
    </TD>
  </TR>
  <TR>
    <TD CLASS="strcol" >Expiration Date </TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="TEXT" NAME="ProviderCreds_DEA2Expire_1" VALUE="<<ProviderCreds_DEA2Expire_1>>" ONCHANGE="return vDate(this);" MAXLENGTH="10" SIZE="10" > 
    </TD>
  </TR>
  <TR>
    <TD CLASS="strcol" >State </TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="TEXT" NAME="ProviderCreds_BNDDST_1" VALUE="<<ProviderCreds_BNDDST_1>>" SIZE="50" > 
    </TD>
  </TR>
  <TR>
    <TD CLASS="strcol" >Type </TD>
    <TD CLASS="strcol" >BNDD </TD>
  </TR>
  <TR>
    <TD CLASS="strcol" >Number </TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="TEXT" NAME="ProviderCreds_BNDDNum_1" VALUE="<<ProviderCreds_BNDDNum_1>>" SIZE="50" > 
    </TD>
  </TR>
  <TR>
    <TD CLASS="strcol" >Original Date of Issue </TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="TEXT" NAME="ProviderCreds_BNDDStart_1" VALUE="<<ProviderCreds_BNDDStart_1>>" ONCHANGE="return vDate(this);" MAXLENGTH="10" SIZE="10" > 
    </TD>
  </TR>
  <TR>
    <TD CLASS="strcol" >Expiration Date </TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="TEXT" NAME="ProviderCreds_BNDDExpire_1" VALUE="<<ProviderCreds_BNDDExpire_1>>" ONCHANGE="return vDate(this);" MAXLENGTH="10" SIZE="10" > 
    </TD>
  </TR>
  <TR>
    <TD CLASS="strcol" >State </TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="TEXT" NAME="ProviderCreds_CDSST_1" VALUE="<<ProviderCreds_CDSST_1>>" SIZE="50" > 
    </TD>
  </TR>
  <TR>
    <TD CLASS="strcol" >Type </TD>
    <TD CLASS="strcol" >CDS </TD>
  </TR>
  <TR>
    <TD CLASS="strcol" >Number </TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="TEXT" NAME="ProviderCreds_CDSNum_1" VALUE="<<ProviderCreds_CDSNum_1>>" SIZE="50" > 
    </TD>
  </TR>
  <TR>
    <TD CLASS="strcol" >Original Date of Issue </TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="TEXT" NAME="ProviderCreds_CDSStart_1" VALUE="<<ProviderCreds_CDSStart_1>>" ONCHANGE="return vDate(this);" MAXLENGTH="10" SIZE="10" > 
    </TD>
  </TR>
  <TR>
    <TD CLASS="strcol" >Expiration Date </TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="TEXT" NAME="ProviderCreds_CDSExpire_1" VALUE="<<ProviderCreds_CDSExpire_1>>" ONCHANGE="return vDate(this);" MAXLENGTH="10" SIZE="10" > 
    </TD>
  </TR>
  <TR>
    <TD CLASS="strcol" COLSPAN="2" >BOARD CERTIFICATION </TD>
  </TR>
  <TR>
    <TD CLASS="strcol" COLSPAN="2" >
Are you Board Certified?  
      <INPUT TYPE="radio" NAME="ProviderCreds_Board1Cert_1" VALUE=1 <<ProviderCreds_Board1Cert_1=1>> > Yes
      <INPUT TYPE="radio" NAME="ProviderCreds_Board1Cert_1" VALUE=0 <<ProviderCreds_Board1Cert_1=0>> > No
    </TD>
  </TR>
  <TR>
    <TD CLASS="strcol" >Name of Board </TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="TEXT" NAME="ProviderCreds_Board1_1" VALUE="<<ProviderCreds_Board1_1>>" SIZE="50" > 
    </TD>
  </TR>
  <TR>
    <TD CLASS="strcol" >Date Initially Certified </TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="TEXT" NAME="ProviderCreds_Board1Start_1" VALUE="<<ProviderCreds_Board1Start_1>>" ONCHANGE="return vDate(this);" MAXLENGTH="10" SIZE="10" > 
    </TD>
  </TR>
  <TR>
    <TD CLASS="strcol" >Date Most Recently Recertified </TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="TEXT" NAME="ProviderCreds_Board1Renewed_1" VALUE="<<ProviderCreds_Board1Renewed_1>>" ONCHANGE="return vDate(this);" MAXLENGTH="10" SIZE="10" > 
    </TD>
  </TR>
  <TR>
    <TD CLASS="strcol" >Date Certification Expires </TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="TEXT" NAME="ProviderCreds_Board1Expire_1" VALUE="<<ProviderCreds_Board1Expire_1>>" ONCHANGE="return vDate(this);" MAXLENGTH="10" SIZE="10" > 
    </TD>
  </TR>
  <TR>
    <TD CLASS="strcol" COLSPAN="2" >
      <INPUT TYPE="radio" NAME="ProviderCreds_BoardFailure_1" VALUE=1 <<ProviderCreds_BoardFailure_1=1>> > Yes
      <INPUT TYPE="radio" NAME="ProviderCreds_BoardFailure_1" VALUE=0 <<ProviderCreds_BoardFailure_1=0>> > No
Have you ever been examined by any specialty board but failed to pass? If yes, provide details.
    </TD>
  </TR>
  <TR>
    <TD CLASS="strcol" COLSPAN="2" >SUBSPECIALTY CERTIFICATION AND ADDED QUALIFICATIONS </TD>
  </TR>
  <TR>
    <TD CLASS="strcol" >Subspecialty or Added Qualification </TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="TEXT" NAME="ProviderCreds_Board2Specialty_1" VALUE="<<ProviderCreds_Board2Specialty_1>>" SIZE="50" > 
    </TD>
  </TR>
  <TR>
    <TD CLASS="strcol" >Name of Board </TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="TEXT" NAME="ProviderCreds_Board2_1" VALUE="<<ProviderCreds_Board2_1>>" SIZE="50" > 
    </TD>
  </TR>
  <TR>
    <TD CLASS="strcol" >Date Initially Certified </TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="TEXT" NAME="ProviderCreds_Board2Start_1" VALUE="<<ProviderCreds_Board2Start_1>>" ONCHANGE="return vDate(this);" MAXLENGTH="10" SIZE="10" > 
    </TD>
  </TR>
  <TR>
    <TD CLASS="strcol" >Date Most Recently Recertified </TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="TEXT" NAME="ProviderCreds_Board2Renew_1" VALUE="<<ProviderCreds_Board2Renew_1>>" ONCHANGE="return vDate(this);" MAXLENGTH="10" SIZE="10" > 
    </TD>
  </TR>
  <TR>
    <TD CLASS="strcol" >Date Certification Expires </TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="TEXT" NAME="ProviderCreds_Board2Expire_1" VALUE="<<ProviderCreds_Board2Expire_1>>" ONCHANGE="return vDate(this);" MAXLENGTH="10" SIZE="10" > 
    </TD>
  </TR>
  <TR>
    <TD CLASS="strcol" >Subspecialty or Added Qualification </TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="TEXT" NAME="ProviderCreds_Board3Specialty_1" VALUE="<<ProviderCreds_Board3Specialty_1>>" SIZE="50" > 
    </TD>
  </TR>
  <TR>
    <TD CLASS="strcol" >Name of Board </TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="TEXT" NAME="ProviderCreds_Board3_1" VALUE="<<ProviderCreds_Board3_1>>" SIZE="50" > 
    </TD>
  </TR>
  <TR>
    <TD CLASS="strcol" >Date Initially Certified </TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="TEXT" NAME="ProviderCreds_Board3Start_1" VALUE="<<ProviderCreds_Board3Start_1>>" ONCHANGE="return vDate(this);" MAXLENGTH="10" SIZE="10" > 
    </TD>
  </TR>
  <TR>
    <TD CLASS="strcol" >Date Most Recently Recertified </TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="TEXT" NAME="ProviderCreds_Board3Renew_1" VALUE="<<ProviderCreds_Board3Renew_1>>" ONCHANGE="return vDate(this);" MAXLENGTH="10" SIZE="10" > 
    </TD>
  </TR>
  <TR>
    <TD CLASS="strcol" >Date Certification Expires </TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="TEXT" NAME="ProviderCreds_Board3Expire_1" VALUE="<<ProviderCreds_Board3Expire_1>>" ONCHANGE="return vDate(this);" MAXLENGTH="10" SIZE="10" > 
    </TD>
  </TR>
  <TR> <TD CLASS="strcol" COLSPAN="2" >BOARD QUALIFICATIONS </TD> </TR>
  <TR>
    <TD CLASS="strcol" COLSPAN="2" >
      <INPUT TYPE="radio" NAME="ProviderCreds_BoardQEligible_1" VALUE=1 <<ProviderCreds_BoardQEligible_1=1>> > Yes
      <INPUT TYPE="radio" NAME="ProviderCreds_BoardQEligible_1" VALUE=0 <<ProviderCreds_BoardQEligible_1=0>> > No
If you are not certified, are you qualified to sit for the exam in a primary or subspecialty board or added qualification?
    </TD>
  </TR>
  <TR>
    <TD CLASS="strcol" COLSPAN="2" >
      <INPUT TYPE="radio" NAME="ProviderCreds_BoardQPlan_1" VALUE=1 <<ProviderCreds_BoardQPlan_1=1>> > Yes
      <INPUT TYPE="radio" NAME="ProviderCreds_BoardQPlan_1" VALUE=0 <<ProviderCreds_BoardQPlan_1=0>> > No
Are you planning to take the exam?
    </TD>
  </TR>
  <TR>
    <TD CLASS="strcol" COLSPAN="2" >
      <INPUT TYPE="radio" NAME="ProviderCreds_BoardQSched_1" VALUE=1 <<ProviderCreds_BoardQSched_1=1>> > Yes
      <INPUT TYPE="radio" NAME="ProviderCreds_BoardQSched_1" VALUE=0 <<ProviderCreds_BoardQSched_1=0>> > No
Are you scheduled to take the exam? If yes, attach confirmation letter.
    </TD>
  </TR>
  <TR> <TD CLASS="strcol" COLSPAN="2" >Date Scheduled: </TD> </TR>
  <TR>
    <TD CLASS="strcol" >Oral </TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="TEXT" NAME="ProviderCreds_BoardQOral_1" VALUE="<<ProviderCreds_BoardQOral_1>>" ONCHANGE="return vDate(this);" MAXLENGTH="10" SIZE="10" > 
    </TD>
  </TR>
  <TR>
    <TD CLASS="strcol" >Written </TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="TEXT" NAME="ProviderCreds_BoardQWritten_1" VALUE="<<ProviderCreds_BoardQWritten_1>>" ONCHANGE="return vDate(this);" MAXLENGTH="10" SIZE="10" > 
    </TD>
  </TR>
  <TR>
    <TD CLASS="strcol" >Other </TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="TEXT" NAME="ProviderCreds_BoardQOther_1" VALUE="<<ProviderCreds_BoardQOther_1>>" ONCHANGE="return vDate(this);" MAXLENGTH="10" SIZE="10" > 
    </TD>
  </TR>
  <TR>
    <TD CLASS="strcol" >Subspecialty or Added Qualification </TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="TEXT" NAME="ProviderCreds_BoardQSpecialty_1" VALUE="<<ProviderCreds_BoardQSpecialty_1>>" SIZE="50" > 
    </TD>
  </TR>
  <TR>
    <TD CLASS="strcol" >Name of Board</TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="TEXT" NAME="ProviderCreds_BoardQ_1" VALUE="<<ProviderCreds_BoardQ_1>>" SIZE="50" > 
    </TD>
  </TR>
  <TR>
    <TD CLASS="strcol" >Date Qualified </TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="TEXT" NAME="ProviderCreds_BoardQStart_1" VALUE="<<ProviderCreds_BoardQStart_1>>" ONCHANGE="return vDate(this);" MAXLENGTH="10" SIZE="10" > 
    </TD>
  </TR>
  <TR>
    <TD CLASS="strcol" >Date Qualification Expires </TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="TEXT" NAME="ProviderCreds_BoardQExpire_1" VALUE="<<ProviderCreds_BoardQExpire_1>>" ONCHANGE="return vDate(this);" MAXLENGTH="10" SIZE="10" > 
    </TD>
  </TR>
  <TR> <TD CLASS="strcol" COLSPAN="2" >Classifications: </TD> </TR>
  <TR>
    <TD CLASS="strcol" COLSPAN="2" >
      <INPUT TYPE="radio" NAME="ProviderCreds_CPR_1" VALUE=1 <<ProviderCreds_CPR_1=1>> > Yes
      <INPUT TYPE="radio" NAME="ProviderCreds_CPR_1" VALUE=0 <<ProviderCreds_CPR_1=0>> > No
Are you certified in CPR?
    </TD>
  </TR>
  <TR>
    <TD CLASS="strcol" >Expires</TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="TEXT" NAME="ProviderCreds_CPRExpire_1" VALUE="<<ProviderCreds_CPRExpire_1>>" SIZE="50" > 
    </TD>
  </TR>
  <TR>
    <TD CLASS="strcol" COLSPAN="2" >
      <INPUT TYPE="radio" NAME="ProviderCreds_BLS_1" VALUE=1 <<ProviderCreds_BLS_1=1>> > Yes
      <INPUT TYPE="radio" NAME="ProviderCreds_BLS_1" VALUE=0 <<ProviderCreds_BLS_1=0>> > No
Basic Life Support (BLS)
    </TD>
  </TR>
  <TR>
    <TD CLASS="strcol" >Expires</TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="TEXT" NAME="ProviderCreds_BLSExpire_1" VALUE="<<ProviderCreds_BLSExpire_1>>" SIZE="50" > 
    </TD>
  </TR>
  <TR>
    <TD CLASS="strcol" COLSPAN="2" >
      <INPUT TYPE="radio" NAME="ProviderCreds_ACLS_1" VALUE=1 <<ProviderCreds_ACLS_1=1>> > Yes
      <INPUT TYPE="radio" NAME="ProviderCreds_ACLS_1" VALUE=0 <<ProviderCreds_ACLS_1=0>> > No
Advanced Cardiac Life Support (ACLS)
    </TD>
  </TR>
  <TR>
    <TD CLASS="strcol" >Expires</TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="TEXT" NAME="ProviderCreds_ACLSExpire_1" VALUE="<<ProviderCreds_ACLSExpire_1>>" SIZE="50" > 
    </TD>
  </TR>
  <TR>
    <TD CLASS="strcol" COLSPAN="2" >
      <INPUT TYPE="radio" NAME="ProviderCreds_CoreC_1" VALUE=1 <<ProviderCreds_CoreC_1=1>> > Yes
      <INPUT TYPE="radio" NAME="ProviderCreds_CoreC_1" VALUE=0 <<ProviderCreds_CoreC_1=0>> > No
Health Care Provider (CoreC)
    </TD>
  </TR>
  <TR>
    <TD CLASS="strcol" >Expires</TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="TEXT" NAME="ProviderCreds_CoreCExpire_1" VALUE="<<ProviderCreds_CoreCExpire_1>>" SIZE="50" > 
    </TD>
  </TR>
  <TR>
    <TD CLASS="strcol" COLSPAN="2" >
      <INPUT TYPE="radio" NAME="ProviderCreds_ATLS_1" VALUE=1 <<ProviderCreds_ATLS_1=1>> > Yes
      <INPUT TYPE="radio" NAME="ProviderCreds_ATLS_1" VALUE=0 <<ProviderCreds_ATLS_1=0>> > No
Advanced Trauma Life Support (ATLS)
    </TD>
  </TR>
  <TR>
    <TD CLASS="strcol" >Expires</TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="TEXT" NAME="ProviderCreds_ATLSExpire_1" VALUE="<<ProviderCreds_ATLSExpire_1>>" SIZE="50" > 
    </TD>
  </TR>
  <TR>
    <TD CLASS="strcol" COLSPAN="2" >
      <INPUT TYPE="radio" NAME="ProviderCreds_NALS_1" VALUE=1 <<ProviderCreds_NALS_1=1>> > Yes
      <INPUT TYPE="radio" NAME="ProviderCreds_NALS_1" VALUE=0 <<ProviderCreds_NALS_1=0>> > No
Neonatal Advanced Life Support (NALS)
    </TD>
  </TR>
  <TR>
    <TD CLASS="strcol" >Expires</TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="TEXT" NAME="ProviderCreds_NALSExpire_1" VALUE="<<ProviderCreds_NALSExpire_1>>" SIZE="50" > 
    </TD>
  </TR>
  <TR>
    <TD CLASS="strcol" COLSPAN="2" >
      <INPUT TYPE="radio" NAME="ProviderCreds_PALS_1" VALUE=1 <<ProviderCreds_PALS_1=1>> > Yes
      <INPUT TYPE="radio" NAME="ProviderCreds_PALS_1" VALUE=0 <<ProviderCreds_PALS_1=0>> > No
Pediatric Advanced Life Support (PALS)
    </TD>
  </TR>
  <TR>
    <TD CLASS="strcol" >Expires</TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="TEXT" NAME="ProviderCreds_PALSExpire_1" VALUE="<<ProviderCreds_PALSExpire_1>>" SIZE="50" > 
    </TD>
  </TR>
  <TR>
    <TD CLASS="strcol" COLSPAN="2" >
      <INPUT TYPE="radio" NAME="ProviderCreds_OtherCert_1" VALUE=1 <<ProviderCreds_OtherCert_1=1>> > Yes
      <INPUT TYPE="radio" NAME="ProviderCreds_OtherCert_1" VALUE=0 <<ProviderCreds_OtherCert_1=0>> > No
Other
    </TD>
  </TR>
  <TR>
    <TD CLASS="strcol" >Other: </TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="TEXT" NAME="ProviderCreds_OtherCertSpecify_1" VALUE="<<ProviderCreds_OtherCertSpecify_1>>" SIZE="50" > 
    </TD>
  </TR>
  <TR>
    <TD CLASS="strcol" >Expires</TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="TEXT" NAME="ProviderCreds_OtherCertExpire_1" VALUE="<<ProviderCreds_OtherCertExpire_1>>" SIZE="50" > 
    </TD>
  </TR>
  </TR>
    </TABLE></TD></TR>
    <TR ><TD ><TABLE CLASS="home fullsize" >
  <TR> <TD CLASS="port hdrtxt" COLSPAN="2" >SECTION 11: OFFICE INFORMATION</TD> </TR>
  <TR> <TD CLASS="strcol" >Primary Office</TD> </TR>
  <TR>
    <TD CLASS="strcol" >Group Name </TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="TEXT" NAME="ProviderCreds_Office1_1" VALUE="<<ProviderCreds_Office1_1>>" SIZE="50" > 
    </TD>
  </TR>
  <TR>
    <TD CLASS="strcol" >Name As It Appears On Your W-9 (if applicable) </TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="TEXT" NAME="ProviderCreds_Office1W9ID_1" VALUE="<<ProviderCreds_Office1W9ID_1>>" SIZE="50" > 
    </TD>
  </TR>
  <TR>
    <TD CLASS="strcol" >Business Owned By</TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="TEXT" NAME="ProviderCreds_Office1Owner_1" VALUE="<<ProviderCreds_Office1Owner_1>>" SIZE="50" > 
    </TD>
  </TR>
  <TR>
    <TD CLASS="strcol" COLSPAN="2" >Type of Practice</TD>
  </TR>
  <TR>
    <TD CLASS="strcol" COLSPAN="2" >
      <INPUT TYPE="radio" NAME="ProviderCreds_Office1PracticeType_1" VALUE="S" <<ProviderCreds_Office1PracticeType_1=S>> > Solo 
      <INPUT TYPE="radio" NAME="ProviderCreds_Office1PracticeType_1" VALUE="P" <<ProviderCreds_Office1PracticeType_1=P>> > Partnership 
      <INPUT TYPE="radio" NAME="ProviderCreds_Office1PracticeType_1" VALUE="G" <<ProviderCreds_Office1PracticeType_1=G>> > Single-Specialty Group  
      <INPUT TYPE="radio" NAME="ProviderCreds_Office1PracticeType_1" VALUE="M" <<ProviderCreds_Office1PracticeType_1=M>> > Multi-Specialty Group  
      <INPUT TYPE="radio" NAME="ProviderCreds_Office1PracticeType_1" VALUE="O" <<ProviderCreds_Office1PracticeType_1=O>> > Other
    </TD>
  </TR>
  <TR>
    <TD CLASS="strcol" >Other (specify) </TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="TEXT" NAME="ProviderCreds_Office1PracticeTypeOther_1" VALUE="<<ProviderCreds_Office1PracticeTypeOther_1>>" SIZE="50" > 
    </TD>
  </TR>
  <TR>
    <TD CLASS="strcol" >Office Manager </TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="TEXT" NAME="ProviderCreds_Office1Manager_1" VALUE="<<ProviderCreds_Office1Manager_1>>" SIZE="50" > 
    </TD>
  </TR>
  <TR>
    <TD CLASS="strcol" >Nurse Coordinator </TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="TEXT" NAME="ProviderCreds_Office1Nurse_1" VALUE="<<ProviderCreds_Office1Nurse_1>>" SIZE="50" > 
    </TD>
  </TR>
  <TR>
    <TD CLASS="strcol" >Group Medicare Number </TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="TEXT" NAME="ProviderCreds_Office1MedicarePIN_1" VALUE="<<ProviderCreds_Office1MedicarePIN_1>>" SIZE="50" > 
    </TD>
  </TR>
  <TR>
    <TD CLASS="strcol" >Group Medicaid Number </TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="TEXT" NAME="ProviderCreds_Office1MedicaidPIN_1" VALUE="<<ProviderCreds_Office1MedicaidPIN_1>>" SIZE="50" > 
    </TD>
  </TR>
  <TR>
    <TD CLASS="strcol" >IRS Tax ID Number </TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="TEXT" NAME="ProviderCreds_Office1TaxID_1" VALUE="<<ProviderCreds_Office1TaxID_1>>" SIZE="50" > 
    </TD>
  </TR>
  <TR>
    <TD CLASS="strcol" COLSPAN="2" >
      Does this office have lab service? 
      <INPUT TYPE="radio" NAME="ProviderCreds_Office1Lab_1" VALUE=1 <<ProviderCreds_Office1Lab_1=1>> > Yes
      <INPUT TYPE="radio" NAME="ProviderCreds_Office1Lab_1" VALUE=0 <<ProviderCreds_Office1Lab_1=0>> > No
    </TD>
  </TR>
  <TR>
    <TD CLASS="strcol" COLSPAN="2" >
      Reference Lab? 
      <INPUT TYPE="radio" NAME="ProviderCreds_Office1RefLab_1" VALUE=1 <<ProviderCreds_Office1RefLab_1=1>> > Yes
      <INPUT TYPE="radio" NAME="ProviderCreds_Office1RefLab_1" VALUE=0 <<ProviderCreds_Office1RefLab_1=0>> > No
    </TD>
  </TR>
  <TR>
    <TD CLASS="strcol" COLSPAN="2" >
      On Site? 
      <INPUT TYPE="radio" NAME="ProviderCreds_Office1OnSiteLab_1" VALUE=1 <<ProviderCreds_Office1OnSiteLab_1=1>> > Yes
      <INPUT TYPE="radio" NAME="ProviderCreds_Office1OnSiteLab_1" VALUE=0 <<ProviderCreds_Office1OnSiteLab_1=0>> > No
    </TD>
  </TR>
  <TR>
    <TD CLASS="strcol" >CLIA ID # </TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="TEXT" NAME="ProviderCreds_Office1CLIANum_1" VALUE="<<ProviderCreds_Office1CLIANum_1>>" SIZE="50" > 
    </TD>
  </TR>
  <TR>
    <TD CLASS="strcol" >CLIA Waiver # </TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="TEXT" NAME="ProviderCreds_Office1CLIAWaiverNum_1" VALUE="<<ProviderCreds_Office1CLIAWaiverNum_1>>" SIZE="50" > 
    </TD>
  </TR>
  <TR> <TD CLASS="strcol" COLSPAN="2" >Does your office have the following: </TD> </TR>
  <TR>
    <TD CLASS="strcol" COLSPAN="2" >
      <INPUT TYPE="radio" NAME="ProviderCreds_Office1Rad_1" VALUE=1 <<ProviderCreds_Office1Rad_1=1>> > Yes
      <INPUT TYPE="radio" NAME="ProviderCreds_Office1Rad_1" VALUE=0 <<ProviderCreds_Office1Rad_1=0>> > No
Radiology
    </TD>
  </TR>
  <TR>
    <TD CLASS="strcol" COLSPAN="2" >
      <INPUT TYPE="radio" NAME="ProviderCreds_Office1EKG_1" VALUE=1 <<ProviderCreds_Office1EKG_1=1>> > Yes
      <INPUT TYPE="radio" NAME="ProviderCreds_Office1EKG_1" VALUE=0 <<ProviderCreds_Office1EKG_1=0>> > No
EKG
    </TD>
  </TR>
  <TR>
    <TD CLASS="strcol" COLSPAN="2" >
      <INPUT TYPE="radio" NAME="ProviderCreds_Office1Aud_1" VALUE=1 <<ProviderCreds_Office1Aud_1=1>> > Yes
      <INPUT TYPE="radio" NAME="ProviderCreds_Office1Aud_1" VALUE=0 <<ProviderCreds_Office1Aud_1=0>> > No
Audiology 
    </TD>
  </TR>
  <TR>
    <TD CLASS="strcol" COLSPAN="2" >
      <INPUT TYPE="radio" NAME="ProviderCreds_Office1Treadmill_1" VALUE=1 <<ProviderCreds_Office1Treadmill_1=1>> > Yes
      <INPUT TYPE="radio" NAME="ProviderCreds_Office1Treadmill_1" VALUE=0 <<ProviderCreds_Office1Treadmill_1=0>> > No
Treadmill 
    </TD>
  </TR>
  <TR>
    <TD CLASS="strcol" COLSPAN="2" >
      <INPUT TYPE="radio" NAME="ProviderCreds_Office1Sigmoid_1" VALUE=1 <<ProviderCreds_Office1Sigmoid_1=1>> > Yes
      <INPUT TYPE="radio" NAME="ProviderCreds_Office1Sigmoid_1" VALUE=0 <<ProviderCreds_Office1Sigmoid_1=0>> > No
Sigmoidoscopy 
    </TD>
  </TR>
  <TR>
    <TD CLASS="strcol" COLSPAN="2" >
      <INPUT TYPE="radio" NAME="ProviderCreds_Office1Access_1" VALUE=1 <<ProviderCreds_Office1Access_1=1>> > Yes
      <INPUT TYPE="radio" NAME="ProviderCreds_Office1Access_1" VALUE=0 <<ProviderCreds_Office1Access_1=0>> > No
Wheelchair/handicapped access? 
    </TD>
  </TR>
  <TR>
    <TD CLASS="strcol" COLSPAN="2" >
      <INPUT TYPE="radio" NAME="ProviderCreds_Office1OtherDisabilitySvcs_1" VALUE=1 <<ProviderCreds_Office1OtherDisabilitySvcs_1=1>> > Yes
      <INPUT TYPE="radio" NAME="ProviderCreds_Office1OtherDisabilitySvcs_1" VALUE=0 <<ProviderCreds_Office1OtherDisabilitySvcs_1=0>> > No
Other services for the disabled? 
    </TD>
  </TR>
  <TR>
    <TD CLASS="strcol" >If yes, please list: </TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="TEXT" NAME="ProviderCreds_Office1OtherDisabilitySvcsSpecify_1" VALUE="<<ProviderCreds_Office1OtherDisabilitySvcsSpecify_1>>" SIZE="50" > 
    </TD>
  </TR>
  <TR>
    <TD CLASS="strcol" >
      <INPUT TYPE="radio" NAME="ProviderCreds_Office1OtherSvcs_1" VALUE=1 <<ProviderCreds_Office1OtherSvcs_1=1>> > Yes
      <INPUT TYPE="radio" NAME="ProviderCreds_Office1OtherSvcs_1" VALUE=0 <<ProviderCreds_Office1OtherSvcs_1=0>> > No
    </TD>
    <TD CLASS="strcol" >
      Other: 
      <INPUT TYPE="TEXT" NAME="ProviderCreds_Office1OtherSvcsSpecify_1" VALUE="<<ProviderCreds_Office1OtherSvcsSpecify_1>>" SIZE="50" > 
    </TD>
  </TR>
  <TR>
    <TD CLASS="strcol" COLSPAN="2" >
      <INPUT TYPE="radio" NAME="ProviderCreds_Office1Safety_1" VALUE=1 <<ProviderCreds_Office1Safety_1=1>> > Yes
      <INPUT TYPE="radio" NAME="ProviderCreds_Office1Safety_1" VALUE=0 <<ProviderCreds_Office1Safety_1=0>> > No
Does this office meet all state and local fire, safety and sanitation requirements?
    </TD>
  </TR>
  <TR>
    <TD CLASS="strcol" COLSPAN="8" >
      <INPUT TYPE="radio" NAME="ProviderCreds_Office124HrCover_1" VALUE=1 <<ProviderCreds_Office124HrCover_1=1>> > Yes
      <INPUT TYPE="radio" NAME="ProviderCreds_Office124HrCover_1" VALUE=0 <<ProviderCreds_Office124HrCover_1=0>> > No
Do you provide 24-hour, seven day a week coverage? 
    </TD>
  </TR>
  <TR> <TD CLASS="strcol" COLSPAN="2" >List all independent licensed non-physicians working in this office. </TD> </TR>
  <TR>
    <TD CLASS="strcol" >Name </TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="TEXT" NAME="ProviderCreds_Office1Prov1_1" VALUE="<<ProviderCreds_Office1Prov1_1>>" SIZE="50" > 
    </TD>
  </TR>
  <TR>
    <TD CLASS="strcol" >Provider Type </TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="TEXT" NAME="ProviderCreds_Office1Prov1Type_1" VALUE="<<ProviderCreds_Office1Prov1Type_1>>" SIZE="50" > 
    </TD>
  </TR>
  <TR>
    <TD CLASS="strcol" >License Number </TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="TEXT" NAME="ProviderCreds_Office1Prov1LicNum_1" VALUE="<<ProviderCreds_Office1Prov1LicNum_1>>" SIZE="50" > 
    </TD>
  </TR>
  <TR>
    <TD CLASS="strcol" >Name </TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="TEXT" NAME="ProviderCreds_Office1Prov2_1" VALUE="<<ProviderCreds_Office1Prov2_1>>" SIZE="50" > 
    </TD>
  </TR>
  <TR>
    <TD CLASS="strcol" >Provider Type </TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="TEXT" NAME="ProviderCreds_Office1Prov2Type_1" VALUE="<<ProviderCreds_Office1Prov2Type_1>>" SIZE="50" > 
    </TD>
  </TR>
  <TR>
    <TD CLASS="strcol" >License Number </TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="TEXT" NAME="ProviderCreds_Office1Prov2LicNum_1" VALUE="<<ProviderCreds_Office1Prov2LicNum_1>>" SIZE="50" > 
    </TD>
  </TR>
  <TR>
    <TD CLASS="strcol" >Name </TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="TEXT" NAME="ProviderCreds_Office1Prov3_1" VALUE="<<ProviderCreds_Office1Prov3_1>>" SIZE="50" > 
    </TD>
  </TR>
  <TR>
    <TD CLASS="strcol" >Provider Type </TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="TEXT" NAME="ProviderCreds_Office1Prov3Type_1" VALUE="<<ProviderCreds_Office1Prov3Type_1>>" SIZE="50" > 
    </TD>
  </TR>
  <TR>
    <TD CLASS="strcol" >License Number </TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="TEXT" NAME="ProviderCreds_Office1Prov3LicNum_1" VALUE="<<ProviderCreds_Office1Prov3LicNum_1>>" SIZE="50" > 
    </TD>
  </TR>
  <TR> <TD CLASS="strcol" COLSPAN="2" >Fluent Languages: </TD> </TR>
  <TR>
    <TD CLASS="strcol" >You </TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="TEXT" NAME="ProviderCreds_Office1Language_1" VALUE="<<ProviderCreds_Office1Language_1>>" SIZE="50" > 
    </TD>
  </TR>
  <TR>
    <TD CLASS="strcol" >Your Staff </TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="TEXT" NAME="ProviderCreds_Office1LanguageStaff_1" VALUE="<<ProviderCreds_Office1LanguageStaff_1>>" SIZE="50" > 
    </TD>
  </TR>
  <TR>
    <TD CLASS="strcol" >Other Resources </TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="TEXT" NAME="ProviderCreds_Office1LanguageResources_1" VALUE="<<ProviderCreds_Office1LanguageResources_1>>" SIZE="50" > 
    </TD>
  </TR>
    </TABLE></TD></TR>
    <TR ><TD ><TABLE CLASS="home fullsize" >
  <TR> <TD CLASS="strcol" COLSPAN="8" >Office Hours: </TD> </TR>
  <TR>
    <TD CLASS="homesubtitle" >
    <TD CLASS="homesubtitle" >Monday</TD>
    <TD CLASS="homesubtitle" >Tuesday</TD>
    <TD CLASS="homesubtitle" >Wednesday</TD>
    <TD CLASS="homesubtitle" >Thursday</TD>
    <TD CLASS="homesubtitle" >Friday</TD>
    <TD CLASS="homesubtitle" >Saturday</TD>
    <TD CLASS="homesubtitle" >Sunday </TD>
  </TR>
  <TR>
    <TD CLASS="strcol" >From:</TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="TEXT" NAME="ProviderCreds_Office1MonStart_1" VALUE="<<ProviderCreds_Office1MonStart_1>>" SIZE="12" > 
    </TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="TEXT" NAME="ProviderCreds_Office1TueStart_1" VALUE="<<ProviderCreds_Office1TueStart_1>>" SIZE="12" > 
    </TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="TEXT" NAME="ProviderCreds_Office1WedsStart_1" VALUE="<<ProviderCreds_Office1WedsStart_1>>" SIZE="12" > 
    </TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="TEXT" NAME="ProviderCreds_Office1ThurStart_1" VALUE="<<ProviderCreds_Office1ThurStart_1>>" SIZE="12" > 
    </TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="TEXT" NAME="ProviderCreds_Office1FriStart_1" VALUE="<<ProviderCreds_Office1FriStart_1>>" SIZE="12" > 
    </TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="TEXT" NAME="ProviderCreds_Office1SatStart_1" VALUE="<<ProviderCreds_Office1SatStart_1>>" SIZE="12" > 
    </TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="TEXT" NAME="ProviderCreds_Office1SunStart_1" VALUE="<<ProviderCreds_Office1SunStart_1>>" SIZE="12" > 
  </TR>
  <TR>
    <TD CLASS="strcol" >To:</TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="TEXT" NAME="ProviderCreds_Office1MonEnd_1" VALUE="<<ProviderCreds_Office1MonEnd_1>>" SIZE="12" > 
    </TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="TEXT" NAME="ProviderCreds_Office1TueEnd_1" VALUE="<<ProviderCreds_Office1TueEnd_1>>" SIZE="12" > 
    </TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="TEXT" NAME="ProviderCreds_Office1WedsEnd_1" VALUE="<<ProviderCreds_Office1WedsEnd_1>>" SIZE="12" > 
    </TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="TEXT" NAME="ProviderCreds_Office1ThurEnd_1" VALUE="<<ProviderCreds_Office1ThurEnd_1>>" SIZE="12" > 
    </TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="TEXT" NAME="ProviderCreds_Office1FriEnd_1" VALUE="<<ProviderCreds_Office1FriEnd_1>>" SIZE="12" > 
    </TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="TEXT" NAME="ProviderCreds_Office1SatEnd_1" VALUE="<<ProviderCreds_Office1SatEnd_1>>" SIZE="12" > 
    </TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="TEXT" NAME="ProviderCreds_Office1SunEnd_1" VALUE="<<ProviderCreds_Office1SunEnd_1>>" SIZE="12" > 
    </TD>
  </TR>
    </TABLE></TD></TR>
    <TR ><TD ><TABLE CLASS="home fullsize" >
  <TR>
    <TD CLASS="strcol" COLSPAN="2" >List name, specialty, and phone number of physicians covering your practice in your absence. Attach an additional sheet if necessary. </TD>
  </TR>
  <TR>
    <TD CLASS="strcol" COLSPAN="2" >Note: These practitioners must be affiliated with the organization to which you are applying. </TD>
  </TR>
  <TR>
    <TD CLASS="strcol" >Name </TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="TEXT" NAME="ProviderCreds_Office1Dr1_1" VALUE="<<ProviderCreds_Office1Dr1_1>>" SIZE="50" > 
    </TD>
  </TR>
  <TR>
    <TD CLASS="strcol" >Specialty</TD>
    <TD CLASS="strcol" >
      <INPUT ID="MCAutocompleteOffice1Dr1Specialty" TYPE="text" VALUE="[[DBA->getxrefWithDef(%form+xOccupationSnomed+<<<ProviderCreds_Office1Dr1Specialty_1>>>+Description)]]" ONFOCUS="select()" SIZE="50" />
      <INPUT TYPE="hidden" NAME="ProviderCreds_Office1Dr1Specialty_1" VALUE="<<ProviderCreds_Office1Dr1Specialty_1>>" >
    </TD>
  </TR>
  <TR>
    <TD CLASS="strcol" >Telephone </TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="TEXT" NAME="ProviderCreds_Office1Dr1Ph_1" VALUE="<<ProviderCreds_Office1Dr1Ph_1>>" SIZE="50" > 
    </TD>
  </TR>
  <TR>
    <TD CLASS="strcol" >Name </TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="TEXT" NAME="ProviderCreds_Office1Dr2_1" VALUE="<<ProviderCreds_Office1Dr2_1>>" SIZE="50" > 
    </TD>
  </TR>
  <TR>
    <TD CLASS="strcol" >Specialty </TD>
    <TD CLASS="strcol" >
      <INPUT ID="MCAutocompleteOffice1Dr2Specialty" TYPE="text" VALUE="[[DBA->getxrefWithDef(%form+xOccupationSnomed+<<<ProviderCreds_Office1Dr2Specialty_1>>>+Description)]]" ONFOCUS="select()" SIZE="50" />
      <INPUT TYPE="hidden" NAME="ProviderCreds_Office1Dr2Specialty_1" VALUE="<<ProviderCreds_Office1Dr2Specialty_1>>" >
    </TD>
  </TR>
  <TR>
    <TD CLASS="strcol" >Telephone</TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="TEXT" NAME="ProviderCreds_Office1Dr2Ph_1" VALUE="<<ProviderCreds_Office1Dr2Ph_1>>" SIZE="50" > 
    </TD>
  </TR>
  <TR>
    <TD CLASS="strcol" >Name</TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="TEXT" NAME="ProviderCreds_Office1Dr3_1" VALUE="<<ProviderCreds_Office1Dr3_1>>" SIZE="50" > 
    </TD>
  </TR>
  <TR>
    <TD CLASS="strcol" >Specialty </TD>
    <TD CLASS="strcol" >
      <INPUT ID="MCAutocompleteOffice1Dr3Specialty" TYPE="text" VALUE="[[DBA->getxrefWithDef(%form+xOccupationSnomed+<<<ProviderCreds_Office1Dr3Specialty_1>>>+Description)]]" ONFOCUS="select()" SIZE="50" />
      <INPUT TYPE="hidden" NAME="ProviderCreds_Office1Dr3Specialty_1" VALUE="<<ProviderCreds_Office1Dr3Specialty_1>>" >
    </TD>
  </TR>
  <TR>
    <TD CLASS="strcol" >Telephone </TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="TEXT" NAME="ProviderCreds_Office1Dr3Ph_1" VALUE="<<ProviderCreds_Office1Dr3Ph_1>>" SIZE="50" > 
    </TD>
  </TR>
  <TR>
    <TD CLASS="strcol" >Name </TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="TEXT" NAME="ProviderCreds_Office1Dr4_1" VALUE="<<ProviderCreds_Office1Dr4_1>>" SIZE="50" > 
    </TD>
  </TR>
  <TR>
    <TD CLASS="strcol" >Specialty </TD>
    <TD CLASS="strcol" >
      <INPUT ID="MCAutocompleteOffice1Dr4Specialty" TYPE="text" VALUE="[[DBA->getxrefWithDef(%form+xOccupationSnomed+<<<ProviderCreds_Office1Dr4Specialty_1>>>+Description)]]" ONFOCUS="select()" SIZE="50" />
      <INPUT TYPE="hidden" NAME="ProviderCreds_Office1Dr4Specialty_1" VALUE="<<ProviderCreds_Office1Dr4Specialty_1>>" >
    </TD>
  </TR>
  <TR>
    <TD CLASS="strcol" >Telephone</TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="TEXT" NAME="ProviderCreds_Office1Dr4Ph_1" VALUE="<<ProviderCreds_Office1Dr4Ph_1>>" SIZE="50" > 
    </TD>
  </TR>
  <TR>
    <TD CLASS="strcol" COLSPAN="2" >
      <INPUT TYPE="radio" NAME="ProviderCreds_Office1Chain_1" VALUE=1 <<ProviderCreds_Office1Chain_1=1>> > Yes
      <INPUT TYPE="radio" NAME="ProviderCreds_Office1Chain_1" VALUE=0 <<ProviderCreds_Office1Chain_1=0>> > No
Do you or your business own, operate, manage or participate in any medical enterprise or business?
    </TD>
  </TR>
  <TR>
    <TD CLASS="strcol" COLSPAN="2" >If yes, explain on a separate attachment. </TD>
  </TR>
    </TABLE></TD></TR>
    <TR ><TD ><TABLE CLASS="home fullsize" >
  <TR> <TD CLASS="port hdrtxt" COLSPAN="2" >SECTION 11: OFFICE INFORMATION</TD> </TR>
  <TR> <TD CLASS="strcol" >Secondary Office</TD> </TR>
  <TR>
    <TD CLASS="strcol" >Group Name </TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="TEXT" NAME="ProviderCreds_Office2_1" VALUE="<<ProviderCreds_Office2_1>>" SIZE="50" > 
    </TD>
  </TR>
  <TR>
    <TD CLASS="strcol" >Name As It Appears On Your W-9 (if applicable) </TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="TEXT" NAME="ProviderCreds_Office2W9ID2_1" VALUE="<<ProviderCreds_Office2W9ID2_1>>" SIZE="50" > 
    </TD>
  </TR>
  <TR>
    <TD CLASS="strcol" >Business Owned By</TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="TEXT" NAME="ProviderCreds_Office2Owner_1" VALUE="<<ProviderCreds_Office2Owner_1>>" SIZE="50" > 
    </TD>
  </TR>
  <TR> <TD CLASS="strcol" COLSPAN="2" >Type of Practice</TD> </TR>
  <TR>
    <TD CLASS="strcol" COLSPAN="2" >
      <INPUT TYPE="radio" NAME="ProviderCreds_Office2PracticeType_1" VALUE="S" <<ProviderCreds_Office2PracticeType_1=S>> > Solo 
      <INPUT TYPE="radio" NAME="ProviderCreds_Office2PracticeType_1" VALUE="P" <<ProviderCreds_Office2PracticeType_1=P>> > Partnership 
      <INPUT TYPE="radio" NAME="ProviderCreds_Office2PracticeType_1" VALUE="G" <<ProviderCreds_Office2PracticeType_1=G>> > Single-Specialty Group  
      <INPUT TYPE="radio" NAME="ProviderCreds_Office2PracticeType_1" VALUE="M" <<ProviderCreds_Office2PracticeType_1=M>> > Multi-Specialty Group  
      <INPUT TYPE="radio" NAME="ProviderCreds_Office2PracticeType_1" VALUE="O" <<ProviderCreds_Office2PracticeType_1=O>> > Other
    </TD>
  </TR>
  <TR>
    <TD CLASS="strcol" >Other (specify) </TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="TEXT" NAME="ProviderCreds_Office2PracticeTypeOther_1" VALUE="<<ProviderCreds_Office2PracticeTypeOther_1>>" SIZE="50" > 
    </TD>
  </TR>
  <TR>
    <TD CLASS="strcol" >Office Manager </TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="TEXT" NAME="ProviderCreds_Office2Manager_1" VALUE="<<ProviderCreds_Office2Manager_1>>" SIZE="50" > 
    </TD>
  </TR>
  <TR>
    <TD CLASS="strcol" >Nurse Coordinator </TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="TEXT" NAME="ProviderCreds_Office2Nurse_1" VALUE="<<ProviderCreds_Office2Nurse_1>>" SIZE="50" > 
    </TD>
  </TR>
  <TR>
    <TD CLASS="strcol" >Group Medicare Number </TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="TEXT" NAME="ProviderCreds_Office2MedicarePIN_1" VALUE="<<ProviderCreds_Office2MedicarePIN_1>>" SIZE="50" > 
    </TD>
  </TR>
  <TR>
    <TD CLASS="strcol" >Group Medicaid Number </TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="TEXT" NAME="ProviderCreds_Office2MedicaidPIN_1" VALUE="<<ProviderCreds_Office2MedicaidPIN_1>>" SIZE="50" > 
    </TD>
  </TR>
  <TR>
    <TD CLASS="strcol" >IRS Tax ID Number </TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="TEXT" NAME="ProviderCreds_Office2TaxID_1" VALUE="<<ProviderCreds_Office2TaxID_1>>" SIZE="50" > 
    </TD>
  </TR>
  <TR>
    <TD CLASS="strcol" COLSPAN="2" >
      Does this office have lab service? 
      <INPUT TYPE="radio" NAME="ProviderCreds_Office2Lab_1" VALUE=1 <<ProviderCreds_Office2Lab_1=1>> > Yes
      <INPUT TYPE="radio" NAME="ProviderCreds_Office2Lab_1" VALUE=0 <<ProviderCreds_Office2Lab_1=1>> > No
    </TD>
  </TR>
  <TR>
    <TD CLASS="strcol" COLSPAN="2" >
      Reference Lab? 
      <INPUT TYPE="radio" NAME="ProviderCreds_Office2RefLab_1" VALUE=1 <<ProviderCreds_Office2RefLab_1=1>> > Yes
      <INPUT TYPE="radio" NAME="ProviderCreds_Office2RefLab_1" VALUE=0 <<ProviderCreds_Office2RefLab_1=0>> > No
    </TD>
  </TR>
  <TR>
    <TD CLASS="strcol" COLSPAN="2" >
      On Site? 
      <INPUT TYPE="radio" NAME="ProviderCreds_Office2OnSiteLab_1" VALUE=1 <<ProviderCreds_Office2OnSiteLab_1=1>> > Yes
      <INPUT TYPE="radio" NAME="ProviderCreds_Office2OnSiteLab_1" VALUE=0 <<ProviderCreds_Office2OnSiteLab_1=0>> > No
    </TD>
  </TR>
  <TR>
    <TD CLASS="strcol" >CLIA ID # </TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="TEXT" NAME="ProviderCreds_Office2CLIANum_1" VALUE="<<ProviderCreds_Office2CLIANum_1>>" SIZE="50" > 
    </TD>
  </TR>
  <TR>
    <TD CLASS="strcol" >No CLIA Waiver # </TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="TEXT" NAME="ProviderCreds_Office2CLIAWaiverNum_1" VALUE="<<ProviderCreds_Office2CLIAWaiverNum_1>>" SIZE="50" > 
    </TD>
  </TR>
  <TR>
    <TD CLASS="strcol" COLSPAN="2" >Does your office have the following: </TD>
  </TR>
  <TR>
    <TD CLASS="strcol" COLSPAN="2" >
      <INPUT TYPE="radio" NAME="ProviderCreds_Office2Rad_1" VALUE=1 <<ProviderCreds_Office2Rad_1=1>> > Yes
      <INPUT TYPE="radio" NAME="ProviderCreds_Office2Rad_1" VALUE=0 <<ProviderCreds_Office2Rad_1=0>> > No
Radiology
    </TD>
  </TR>
  <TR>
    <TD CLASS="strcol" COLSPAN="2" >
      <INPUT TYPE="radio" NAME="ProviderCreds_Office2EKG_1" VALUE=1 <<ProviderCreds_Office2EKG_1=1>> > Yes
      <INPUT TYPE="radio" NAME="ProviderCreds_Office2EKG_1" VALUE=0 <<ProviderCreds_Office2EKG_1=0>> > No
EKG
    </TD>
  </TR>
  <TR>
    <TD CLASS="strcol" COLSPAN="2" >
      <INPUT TYPE="radio" NAME="ProviderCreds_Office2Aud_1" VALUE=1 <<ProviderCreds_Office2Aud_1=1>> > Yes
      <INPUT TYPE="radio" NAME="ProviderCreds_Office2Aud_1" VALUE=0 <<ProviderCreds_Office2Aud_1=0>> > No
Audiology 
    </TD>
  </TR>
  <TR>
    <TD CLASS="strcol" COLSPAN="2" >
      <INPUT TYPE="radio" NAME="ProviderCreds_Office2Treadmill_1" VALUE=1 <<ProviderCreds_Office2Treadmill_1=1>> > Yes
      <INPUT TYPE="radio" NAME="ProviderCreds_Office2Treadmill_1" VALUE=0 <<ProviderCreds_Office2Treadmill_1=0>> > No
Treadmill 
    </TD>
  </TR>
  <TR>
    <TD CLASS="strcol" COLSPAN="2" >
      <INPUT TYPE="radio" NAME="ProviderCreds_Office2Sigmoid_1" VALUE=1 <<ProviderCreds_Office2Sigmoid_1=1>> > Yes
      <INPUT TYPE="radio" NAME="ProviderCreds_Office2Sigmoid_1" VALUE=0 <<ProviderCreds_Office2Sigmoid_1=0>> > No
Sigmoidoscopy 
    </TD>
  </TR>
  <TR>
    <TD CLASS="strcol" COLSPAN="2" >
      <INPUT TYPE="radio" NAME="ProviderCreds_Office2Access_1" VALUE=1 <<ProviderCreds_Office2Access_1=1>> > Yes
      <INPUT TYPE="radio" NAME="ProviderCreds_Office2Access_1" VALUE=0 <<ProviderCreds_Office2Access_1=0>> > No
Wheelchair/handicapped access? 
    </TD>
  </TR>
  <TR>
    <TD CLASS="strcol" COLSPAN="2" >
      <INPUT TYPE="radio" NAME="ProviderCreds_Office2OtherDisabilitySvcs_1" VALUE=1 <<ProviderCreds_Office2OtherDisabilitySvcs_1=1>> > Yes
      <INPUT TYPE="radio" NAME="ProviderCreds_Office2OtherDisabilitySvcs_1" VALUE=0 <<ProviderCreds_Office2OtherDisabilitySvcs_1=0>> > No
Other services for the disabled? 
    </TD>
  </TR>
  <TR>
    <TD CLASS="strcol" >If yes, please list: </TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="TEXT" NAME="ProviderCreds_Office2OtherDisabilitySvcsSpecify_1" VALUE="<<ProviderCreds_Office2OtherDisabilitySvcsSpecify_1>>" SIZE="50" > 
    </TD>
  </TR>
  <TR>
    <TD CLASS="strcol" >
      <INPUT TYPE="radio" NAME="ProviderCreds_Office2OtherSvcs_1" VALUE=1 <<ProviderCreds_Office2OtherSvcs_1=1>> > Yes
      <INPUT TYPE="radio" NAME="ProviderCreds_Office2OtherSvcs_1" VALUE=0 <<ProviderCreds_Office2OtherSvcs_1=0>> > No
    </TD>
    <TD CLASS="strcol" >
      Other: 
      <INPUT TYPE="TEXT" NAME="ProviderCreds_Office2OtherSvcsSpecify_1" VALUE="<<ProviderCreds_Office2OtherSvcsSpecify_1>>" SIZE="50" > 
    </TD>
  </TR>
  <TR>
    <TD CLASS="strcol" COLSPAN="2" >
      <INPUT TYPE="radio" NAME="ProviderCreds_Office2Safety_1" VALUE=1 <<ProviderCreds_Office2Safety_1=1>> > Yes
      <INPUT TYPE="radio" NAME="ProviderCreds_Office2Safety_1" VALUE=0 <<ProviderCreds_Office2Safety_1=0>> > No
Does this office meet all state and local fire, safety and sanitation requirements?
    </TD>
  </TR>
  <TR>
    <TD CLASS="strcol" COLSPAN="8" >
      <INPUT TYPE="radio" NAME="ProviderCreds_Office224HrCover_1" VALUE=1 <<ProviderCreds_Office224HrCover_1=1>> > Yes
      <INPUT TYPE="radio" NAME="ProviderCreds_Office224HrCover_1" VALUE=0 <<ProviderCreds_Office224HrCover_1=0>> > No
Do you provide 24-hour, seven day a week coverage? 
    </TD>
  </TR>
  <TR> <TD CLASS="strcol" COLSPAN="2" >List all independent licensed non-physicians working in this office. </TD> </TR>
  <TR>
    <TD CLASS="strcol" >Name </TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="TEXT" NAME="ProviderCreds_Office2Prov1_1" VALUE="<<ProviderCreds_Office2Prov1_1>>" SIZE="50" > 
    </TD>
  </TR>
  <TR>
    <TD CLASS="strcol" >Provider Type </TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="TEXT" NAME="ProviderCreds_Office2Prov1Type_1" VALUE="<<ProviderCreds_Office2Prov1Type_1>>" SIZE="50" > 
    </TD>
  </TR>
  <TR>
    <TD CLASS="strcol" >License Number </TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="TEXT" NAME="ProviderCreds_Office2Prov1LicNum_1" VALUE="<<ProviderCreds_Office2Prov1LicNum_1>>" SIZE="50" > 
    </TD>
  </TR>
  <TR>
    <TD CLASS="strcol" >Name </TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="TEXT" NAME="ProviderCreds_Office2Prov2_1" VALUE="<<ProviderCreds_Office2Prov2_1>>" SIZE="50" > 
    </TD>
  </TR>
  <TR>
    <TD CLASS="strcol" >Provider Type </TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="TEXT" NAME="ProviderCreds_Office2Prov2Type_1" VALUE="<<ProviderCreds_Office2Prov2Type_1>>" SIZE="50" > 
    </TD>
  </TR>
  <TR>
    <TD CLASS="strcol" >License Number </TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="TEXT" NAME="ProviderCreds_Office2Prov2LicNum_1" VALUE="<<ProviderCreds_Office2Prov2LicNum_1>>" SIZE="50" > 
    </TD>
  </TR>
  <TR>
    <TD CLASS="strcol" >Name </TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="TEXT" NAME="ProviderCreds_Office2Prov3_1" VALUE="<<ProviderCreds_Office2Prov3_1>>" SIZE="50" > 
    </TD>
  </TR>
  <TR>
    <TD CLASS="strcol" >Provider Type </TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="TEXT" NAME="ProviderCreds_Office2Prov3Type_1" VALUE="<<ProviderCreds_Office2Prov3Type_1>>" SIZE="50" > 
    </TD>
  </TR>
  <TR>
    <TD CLASS="strcol" >License Number </TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="TEXT" NAME="ProviderCreds_Office2Prov3LicNum_1" VALUE="<<ProviderCreds_Office2Prov3LicNum_1>>" SIZE="50" > 
    </TD>
  </TR>
  <TR> <TD CLASS="strcol" COLSPAN="2" >Fluent Languages: </TD> </TR>
  <TR>
    <TD CLASS="strcol" >You </TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="TEXT" NAME="ProviderCreds_Office2Language_1" VALUE="<<ProviderCreds_Office2Language_1>>" SIZE="50" > 
    </TD>
  </TR>
  <TR>
    <TD CLASS="strcol" >Your Staff </TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="TEXT" NAME="ProviderCreds_Office2LanguageStaff_1" VALUE="<<ProviderCreds_Office2LanguageStaff_1>>" SIZE="50" > 
    </TD>
  </TR>
  <TR>
    <TD CLASS="strcol" >Other Resources </TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="TEXT" NAME="ProviderCreds_Office2LanguageResources_1" VALUE="<<ProviderCreds_Office2LanguageResources_1>>" SIZE="50" > 
    </TD>
  </TR>
    </TABLE></TD></TR>
    <TR ><TD ><TABLE CLASS="home fullsize" >
  <TR>
    <TD CLASS="strcol" COLSPAN="8" >Office Hours: </TD>
  </TR>
  <TR>
    <TD CLASS="homesubtitle" >
    <TD CLASS="homesubtitle" >Monday</TD>
    <TD CLASS="homesubtitle" >Tuesday</TD>
    <TD CLASS="homesubtitle" >Wednesday</TD>
    <TD CLASS="homesubtitle" >Thursday</TD>
    <TD CLASS="homesubtitle" >Friday</TD>
    <TD CLASS="homesubtitle" >Saturday</TD>
    <TD CLASS="homesubtitle" >Sunday </TD>
  </TR>
  <TR>
    <TD CLASS="strcol" >From:</TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="TEXT" NAME="ProviderCreds_Office2MonStart_1" VALUE="<<ProviderCreds_Office2MonStart_1>>" SIZE="12" > 
    </TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="TEXT" NAME="ProviderCreds_Office2TueStart_1" VALUE="<<ProviderCreds_Office2TueStart_1>>" SIZE="12" > 
    </TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="TEXT" NAME="ProviderCreds_Office2WedsStart_1" VALUE="<<ProviderCreds_Office2WedsStart_1>>" SIZE="12" > 
    </TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="TEXT" NAME="ProviderCreds_Office2ThurStart_1" VALUE="<<ProviderCreds_Office2ThurStart_1>>" SIZE="12" > 
    </TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="TEXT" NAME="ProviderCreds_Office2FriStart_1" VALUE="<<ProviderCreds_Office2FriStart_1>>" SIZE="12" > 
    </TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="TEXT" NAME="ProviderCreds_Office2SatStart_1" VALUE="<<ProviderCreds_Office2SatStart_1>>" SIZE="12" > 
    </TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="TEXT" NAME="ProviderCreds_Office2SunStart_1" VALUE="<<ProviderCreds_Office2SunStart_1>>" SIZE="12" > 
  </TR>
  <TR>
    <TD CLASS="strcol" >To:</TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="TEXT" NAME="ProviderCreds_Office2MonEnd_1" VALUE="<<ProviderCreds_Office2MonEnd_1>>" SIZE="12" > 
    </TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="TEXT" NAME="ProviderCreds_Office2TueEnd_1" VALUE="<<ProviderCreds_Office2TueEnd_1>>" SIZE="12" > 
    </TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="TEXT" NAME="ProviderCreds_Office2WedsEnd_1" VALUE="<<ProviderCreds_Office2WedsEnd_1>>" SIZE="12" > 
    </TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="TEXT" NAME="ProviderCreds_Office2ThurEnd_1" VALUE="<<ProviderCreds_Office2ThurEnd_1>>" SIZE="12" > 
    </TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="TEXT" NAME="ProviderCreds_Office2FriEnd_1" VALUE="<<ProviderCreds_Office2FriEnd_1>>" SIZE="12" > 
    </TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="TEXT" NAME="ProviderCreds_Office2SatEnd_1" VALUE="<<ProviderCreds_Office2SatEnd_1>>" SIZE="12" > 
    </TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="TEXT" NAME="ProviderCreds_Office2SunEnd_1" VALUE="<<ProviderCreds_Office2SunEnd_1>>" SIZE="12" > 
    </TD>
  </TR>
    </TABLE></TD></TR>
    <TR ><TD ><TABLE CLASS="home fullsize" >
  <TR>
    <TD CLASS="strcol" COLSPAN="2" >List name, specialty, and phone number of physicians covering your practice in your absence. Attach an additional sheet if necessary. </TD>
  </TR>
  <TR>
    <TD CLASS="strcol" COLSPAN="2" >Note: These practitioners must be affiliated with the organization to which you are applying. </TD>
  </TR>
  <TR>
    <TD CLASS="strcol" >Name </TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="TEXT" NAME="ProviderCreds_Office2Dr1_1" VALUE="<<ProviderCreds_Office2Dr1_1>>" SIZE="50" > 
    </TD>
  </TR>
  <TR>
    <TD CLASS="strcol" >Specialty</TD>
    <TD CLASS="strcol" >
      <INPUT ID="MCAutocompleteOffice2Dr1Specialty" TYPE="text" VALUE="[[DBA->getxrefWithDef(%form+xOccupationSnomed+<<<ProviderCreds_Office2Dr1Specialty_1>>>+Description)]]" ONFOCUS="select()" SIZE="50" />
      <INPUT TYPE="hidden" NAME="ProviderCreds_Office2Dr1Specialty_1" VALUE="<<ProviderCreds_Office2Dr1Specialty_1>>" >
    </TD>
  </TR>
  <TR>
    <TD CLASS="strcol" >Telephone </TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="TEXT" NAME="ProviderCreds_Office2Dr1Ph_1" VALUE="<<ProviderCreds_Office2Dr1Ph_1>>" SIZE="50" > 
    </TD>
  </TR>
  <TR>
    <TD CLASS="strcol" >Name </TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="TEXT" NAME="ProviderCreds_Office2Dr2_1" VALUE="<<ProviderCreds_Office2Dr2_1>>" SIZE="50" > 
    </TD>
  </TR>
  <TR>
    <TD CLASS="strcol" >Specialty </TD>
    <TD CLASS="strcol" >
      <INPUT ID="MCAutocompleteOffice2Dr2Specialty" TYPE="text" VALUE="[[DBA->getxrefWithDef(%form+xOccupationSnomed+<<<ProviderCreds_Office2Dr2Specialty_1>>>+Description)]]" ONFOCUS="select()" SIZE="50" />
      <INPUT TYPE="hidden" NAME="ProviderCreds_Office2Dr2Specialty_1" VALUE="<<ProviderCreds_Office2Dr2Specialty_1>>" >
    </TD>
  </TR>
  <TR>
    <TD CLASS="strcol" >Telephone</TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="TEXT" NAME="ProviderCreds_Office2Dr2Ph_1" VALUE="<<ProviderCreds_Office2Dr2Ph_1>>" SIZE="50" > 
    </TD>
  </TR>
  <TR>
    <TD CLASS="strcol" >Name</TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="TEXT" NAME="ProviderCreds_Office2Dr3_1" VALUE="<<ProviderCreds_Office2Dr3_1>>" SIZE="50" > 
    </TD>
  </TR>
  <TR>
    <TD CLASS="strcol" >Specialty </TD>
    <TD CLASS="strcol" >
      <INPUT ID="MCAutocompleteOffice2Dr3Specialty" TYPE="text" VALUE="[[DBA->getxrefWithDef(%form+xOccupationSnomed+<<<ProviderCreds_Office2Dr3Specialty_1>>>+Description)]]" ONFOCUS="select()" SIZE="50" />
      <INPUT TYPE="hidden" NAME="ProviderCreds_Office2Dr3Specialty_1" VALUE="<<ProviderCreds_Office2Dr3Specialty_1>>" >
    </TD>
  </TR>
  <TR>
    <TD CLASS="strcol" >Telephone </TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="TEXT" NAME="ProviderCreds_Office2Dr3Ph_1" VALUE="<<ProviderCreds_Office2Dr3Ph_1>>" SIZE="50" > 
    </TD>
  </TR>
  <TR>
    <TD CLASS="strcol" >Name </TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="TEXT" NAME="ProviderCreds_Office2Dr4_1" VALUE="<<ProviderCreds_Office2Dr4_1>>" SIZE="50" > 
    </TD>
  </TR>
  <TR>
    <TD CLASS="strcol" >Specialty </TD>
    <TD CLASS="strcol" >
      <INPUT ID="MCAutocompleteOffice2Dr4Specialty" TYPE="text" VALUE="[[DBA->getxrefWithDef(%form+xOccupationSnomed+<<<ProviderCreds_Office2Dr4Specialty_1>>>+Description)]]" ONFOCUS="select()" SIZE="50" />
      <INPUT TYPE="hidden" NAME="ProviderCreds_Office2Dr4Specialty_1" VALUE="<<ProviderCreds_Office2Dr4Specialty_1>>" >
    </TD>
  </TR>
  <TR>
    <TD CLASS="strcol" >Telephone</TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="TEXT" NAME="ProviderCreds_Office2Dr4Ph_1" VALUE="<<ProviderCreds_Office2Dr4Ph_1>>" SIZE="50" > 
    </TD>
  </TR>
  <TR>
    <TD CLASS="strcol" COLSPAN="2" >
      <INPUT TYPE="radio" NAME="ProviderCreds_Office2Chain_1" VALUE=1 <<ProviderCreds_Office2Chain_1=1>> > Yes
      <INPUT TYPE="radio" NAME="ProviderCreds_Office2Chain_1" VALUE=0 <<ProviderCreds_Office2Chain_1=0>> > No
Do you or your business own, operate, manage or participate in any medical enterprise or business?
    </TD>
  </TR>
  <TR> <TD CLASS="strcol" COLSPAN="2" >If yes, explain on a separate attachment. </TD> </TR>
    </TABLE></TD></TR>
    <TR ><TD ><TABLE CLASS="home fullsize" >
  <TR> <TD CLASS="port hdrtxt" COLSPAN="2" >SECTION 12: COPIES OF REQUIRED DOCUMENT</TD> </TR>
  <TR> <TD CLASS="strcol" COLSPAN="2" >Please include a copy of the following with this application.  Practitioner should check off needed items that are being attached to this application. </TD> </TR>
  <TR> <TD CLASS="strcol" COLSPAN="2" >Attached Items </TD> </TR>
  <TR>
    <TD CLASS="strcol" COLSPAN="2" >
      <INPUT TYPE="radio" NAME="ProviderCreds_BNDDAttachment_1" VALUE=1 <<ProviderCreds_BNDDAttachment_1=1>> > Yes
      <INPUT TYPE="radio" NAME="ProviderCreds_BNDDAttachment_1" VALUE=0 <<ProviderCreds_BNDDAttachment_1=0>> > No
Oklahoma Bureau of Narcotics and Dangerous Drugs Registration (BNDD)
    </TD>
  </TR>
  <TR>
    <TD CLASS="strcol" COLSPAN="2" >
      <INPUT TYPE="radio" NAME="ProviderCreds_DEAAttachment_1" VALUE=1 <<ProviderCreds_DEAAttachment_1=1>> > Yes
      <INPUT TYPE="radio" NAME="ProviderCreds_DEAAttachment_1" VALUE=0 <<ProviderCreds_DEAAttachment_1=0>> > No
Current Federal DEA Registration Certificate
    </TD>
  </TR>
  <TR>
    <TD CLASS="strcol" COLSPAN="2" >
      <INPUT TYPE="radio" NAME="ProviderCreds_CPRAttachment_1" VALUE=1 <<ProviderCreds_CPRAttachment_1=1>> > Yes
      <INPUT TYPE="radio" NAME="ProviderCreds_CPRAttachment_1" VALUE=0 <<ProviderCreds_CPRAttachment_1=0>> > No
Emergency Care Training Certificates (CPR, etc., if certified) 
    </TD>
  </TR>
  <TR>
    <TD CLASS="strcol" COLSPAN="2" >
      <INPUT TYPE="radio" NAME="ProviderCreds_PhotoAttachment_1" VALUE=1 <<ProviderCreds_PhotoAttachment_1=1>> > Yes
      <INPUT TYPE="radio" NAME="ProviderCreds_PhotoAttachment_1" VALUE=0 <<ProviderCreds_PhotoAttachment_1=0>> > No
Photo Identification 
    </TD>
  </TR>
  <TR>
    <TD CLASS="strcol" COLSPAN="2" >
      <INPUT TYPE="radio" NAME="ProviderCreds_VitaeAttachment_1" VALUE=1 <<ProviderCreds_VitaeAttachment_1=1>> > Yes
      <INPUT TYPE="radio" NAME="ProviderCreds_VitaeAttachment_1" VALUE=0 <<ProviderCreds_VitaeAttachment_1=0>> > No
Curriculum Vitae 
    </TD>
  </TR>
  <TR>
    <TD CLASS="strcol" COLSPAN="2" >
      <INPUT TYPE="radio" NAME="ProviderCreds_W9Attachment_1" VALUE=1 <<ProviderCreds_W9Attachment_1=1>> > Yes
      <INPUT TYPE="radio" NAME="ProviderCreds_W9Attachment_1" VALUE=0 <<ProviderCreds_W9Attachment_1=0>> > No
Tax Identification Information Form W-9 
    </TD>
  </TR>
    </TD>
  </TR>
    </TABLE></TD></TR>
    <TR ><TD ><TABLE CLASS="home fullsize" >
  <TR> <TD CLASS="port hdrtxt" COLSPAN="2" >SECTION 13: ATTESTATION </TD> </TR>
  <TR>
    <TD CLASS="strcol" COLSPAN="2" >All information and documentation contained in this application is true, correct and complete to my best knowledge and belief. I further acknowledge that any material misstatements in or omissions from this application may constitute cause for denial of my application for staff membership, privileges, or participation. </TD>
  </TR>
  <TR>
    <TD CLASS="strcol" >Name (printed) </TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="TEXT" NAME="ProviderCreds_FullName_1" VALUE="<<ProviderCreds_FullName_1>>" SIZE="50" > 
    </TD>
  </TR>
  <TR>
    <TD CLASS="strcol" >Signature Date </TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="TEXT" NAME="ProviderCreds_AttestationDate_1" VALUE="<<ProviderCreds_AttestationDate_1>>" ONCHANGE="return vDate(this);" MAXLENGTH="10" SIZE="10" > 
    </TD>
  </TR>
  <TR>
    <TD CLASS="strcol" COLSPAN="2" >NOTE</TD>
  </TR>
  <TR>
    <TD CLASS="strcol" COLSPAN="2" >Practitioners are reminded that each organization will require submission of additional information.</TD>
  </TR>
    </TABLE></TD></TR>
    <TR ><TD ><TABLE CLASS="home fullsize" >
  <TR> <TD CLASS="port hdrtxt" COLSPAN="2" >SECTION 14: ADDITIONAL INFORMATION </TD> </TR>
  <TR>
    <TD CLASS="strcol" COLSPAN="2" >This page is furnished for your convenience in completing questions or providing additional information.  Please make as many copies of this page as you require to fully answer all questions. </TD>
  </TR>
  <TR>
    <TD CLASS="strcol" COLSPAN="2" >As appropriate, note section number and question number that you are addressing. </TD>
  </TR>
  <TR>
    <TD CLASS="strcol" COLSPAN="2" >
<TEXTAREA NAME="ProviderCreds_AdditionalInfo1_1" COLS=90 ROWS="12" WRAP="virtual" ><<ProviderCreds_AdditionalInfo1_1>></TEXTAREA>
    </TD>
  </TR>
  <TR>
    <TD CLASS="strcol" COLSPAN="2" >
<TEXTAREA NAME="ProviderCreds_AdditionalInfo2_1" COLS=90 ROWS="12" WRAP="virtual" ><<ProviderCreds_AdditionalInfo2_1>></TEXTAREA>
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

</LOADHIDDEN>
</FORM>
<SCRIPT LANGUAGE="JavaScript">
document.Credentials.elements[0].focus();
</SCRIPT>

[[myHTML->rightpane(%form+search)]]

<SCRIPT type="text/javascript" src="/cgi/js/vMCAutocomplete.js?v=202006082124"></SCRIPT>
<SCRIPT LANGUAGE="JavaScript" >
callAjax('xOccupationSnomed','','','&Autocomplete=MCAutocompleteTrain1Specialty&Target=ProviderCreds_Train1Specialty_1','popup.pl');
callAjax('xOccupationSnomed','','','&Autocomplete=MCAutocompleteTrain2Specialty&Target=ProviderCreds_Train2Specialty_1','popup.pl');
callAjax('xOccupationSnomed','','','&Autocomplete=MCAutocompleteTrain3Specialty&Target=ProviderCreds_Train3Specialty_1','popup.pl');
callAjax('xOccupationSnomed','','','&Autocomplete=MCAutocompleteTrain4Specialty&Target=ProviderCreds_Train4Specialty_1','popup.pl');
callAjax('xOccupationSnomed','','','&Autocomplete=MCAutocompleteOffice1Dr1Specialty&Target=ProviderCreds_Office1Dr1Specialty_1','popup.pl');
callAjax('xOccupationSnomed','','','&Autocomplete=MCAutocompleteOffice1Dr2Specialty&Target=ProviderCreds_Office1Dr2Specialty_1','popup.pl');
callAjax('xOccupationSnomed','','','&Autocomplete=MCAutocompleteOffice1Dr3Specialty&Target=ProviderCreds_Office1Dr3Specialty_1','popup.pl');
callAjax('xOccupationSnomed','','','&Autocomplete=MCAutocompleteOffice1Dr4Specialty&Target=ProviderCreds_Office1Dr4Specialty_1','popup.pl');
callAjax('xOccupationSnomed','','','&Autocomplete=MCAutocompleteOffice2Dr1Specialty&Target=ProviderCreds_Office2Dr1Specialty_1','popup.pl');
callAjax('xOccupationSnomed','','','&Autocomplete=MCAutocompleteOffice2Dr2Specialty&Target=ProviderCreds_Office2Dr2Specialty_1','popup.pl');
callAjax('xOccupationSnomed','','','&Autocomplete=MCAutocompleteOffice2Dr3Specialty&Target=ProviderCreds_Office2Dr3Specialty_1','popup.pl');
callAjax('xOccupationSnomed','','','&Autocomplete=MCAutocompleteOffice2Dr4Specialty&Target=ProviderCreds_Office2Dr4Specialty_1','popup.pl');
</SCRIPT>
