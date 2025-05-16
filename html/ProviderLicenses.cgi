[[myHTML->newPage(%form+Professional License)]]

<SCRIPT LANGUAGE="JavaScript" SRC="/src/cgi/js/NoEnter.js"> </SCRIPT>
<SCRIPT LANGUAGE="JavaScript" SRC="/src/cgi/js/vEntry.js"> </SCRIPT>
<SCRIPT LANGUAGE="JavaScript" SRC="/src/cgi/js/vProviderLicenses.js"> </SCRIPT>
<SCRIPT LANGUAGE="JavaScript" SRC="/src/cgi/js/vDate.js"> </SCRIPT>
<SCRIPT LANGUAGE="JavaScript" SRC="/src/cgi/js/vNum.js"> </SCRIPT>
<SCRIPT TYPE="text/javascript" SRC="/cgi/jquery/jquery-ui-1.11.2/jquery-ui.min.js" ></SCRIPT>
<SCRIPT type="text/javascript" src="/src/cgi/js/ajaxrequest.js"></SCRIPT>
<LINK HREF="/src/cgi/css/autocomplete.css?v=202008071708" REL="stylesheet">

<FORM NAME="ProviderLicenses" ACTION="/cgi/bin/mis.cgi" METHOD="POST" >
<TABLE CLASS="main fullsize" >
  <TR >
    <TD CLASS="strcol" >
      <<<Provider_FName_1>>> <<<Provider_MName_1>>> <<<Provider_LName_1>>> 
      (<<<Provider_ProvID_1>>>)
      <BR>License Information
    </TD>
    <TD CLASS="numcol" >[[gHTML->setLINKS(%form+back)]]</TD>
  </TR>
</TABLE>
<HR WIDTH="90%" >
<TABLE CLASS="home fullsize" >
  <TR >
    <TD CLASS="strcol" >State</TD>
    <TD CLASS="strcol" >
      <SELECT NAME="ProviderLicenses_State_1">
        [[DBA->selxTable(%form+xStates+<<ProviderLicenses_State_1>>+Descr)]]
      </SELECT> 
    </TD>
  </TR>
  <TR >
    <TD CLASS="strcol" >Type</TD>
    <TD CLASS="strcol" >
      <SELECT NAME="ProviderLicenses_LicType_1">
        [[DBA->selxTable(%form+xLicenseTypes+<<ProviderLicenses_LicType_1>>+Descr)]]
      </SELECT> 
    </TD>
  </TR>
  <TR >
    <TD CLASS="strcol" >Number</TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="TEXT" NAME="ProviderLicenses_LicNumber_1" VALUE="<<ProviderLicenses_LicNumber_1>>" SIZE="50" > 
    </TD>
  </TR>
  <TR >
    <TD CLASS="strcol" >Effective</TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="TEXT" NAME="ProviderLicenses_LicEffDate_1" VALUE="<<ProviderLicenses_LicEffDate_1>>" ONFOCUS="select()" ONCHANGE="return vDate(this)" SIZE="12" > 
    </TD>
  </TR>
  <TR >
    <TD CLASS="strcol" >Expires</TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="TEXT" NAME="ProviderLicenses_LicExpDate_1" VALUE="<<ProviderLicenses_LicExpDate_1>>" ONFOCUS="select()" ONCHANGE="return vDate(this)" SIZE="12" > 
    </TD>
  </TR>
  <TR >
    <TD CLASS="strcol" >NPI</TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="text" NAME="ProviderControl_NPI_1" VALUE="<<ProviderControl_NPI_1>>" ONFOCUS="select()" ONCHANGE="return vNum(this,1000000000)" MAXLENGTH="10" SIZE="10" >
    </TD>
  </TR>
  <TR >
    <TD CLASS="strcol" >DEA</TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="TEXT" NAME="ProviderLicenses_DEA_1" VALUE="<<ProviderLicenses_DEA_1>>" SIZE="50" > 
    </TD>
  </TR>
  <TR >
    <TD CLASS="strcol" >CAQH</TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="TEXT" NAME="ProviderLicenses_CAQH_1" VALUE="<<ProviderLicenses_CAQH_1>>" SIZE="50" > 
    </TD>
  </TR>
  <TR >
    <TD CLASS="strcol" >Specialty</TD>
    <TD CLASS="strcol" >
      <INPUT ID="MCAutocompleteSpecialty" TYPE="text" VALUE="[[DBA->getxrefWithDef(%form+xOccupationSnomed+<<<ProviderLicenses_Specialty_1>>>+Description)]]" ONFOCUS="select()" SIZE="100" />
      <INPUT TYPE="hidden" NAME="ProviderLicenses_Specialty_1" VALUE="<<ProviderLicenses_Specialty_1>>" >
    </TD>
  </TR>
  <TR >
    <TD CLASS="strcol" >Taxonomy</TD>
    <TD CLASS="strcol" >
      <INPUT ID="MCAutocompleteTaxonomy" TYPE="text" VALUE="[[DBA->getxref(%form+xTaxonomy+<<<ProviderLicenses_Taxonomy_1>>>+ID Spec Class Type+++ | )]]" ONFOCUS="select()" SIZE="100" />
      <INPUT TYPE="hidden" NAME="ProviderLicenses_Taxonomy_1" VALUE="<<ProviderLicenses_Taxonomy_1>>" >
    </TD>
  </TR>
</TABLE>
<TABLE CLASS="main fullsize" >
  <TR>
    <TD CLASS="numcol" >
      <INPUT TYPE="submit" ONCLICK="return vDELETE('Are you sure you want to delete this record?');" NAME="ProviderLicenses_DELETE_1=1&UpdateTables=all&misPOP=1" VALUE="Delete">
      <INPUT TYPE="submit" ONCLICK="return validate(this.form);" NAME="UpdateTables=all&misPOP=1" VALUE="Add/Update">
    </TD>
  </TR>
</TABLE>
<HR WIDTH="90%" >
<TABLE CLASS="site fullsize" >
  <TR >
    <TD CLASS="hdrtxt" >
      [[SysAccess->verify(%form+Privilege=ProviderEDocs)<A HREF="javascript:ReportWindow('/src/cgi/bin/mis.cgi?view=ListProviderEDocs.cgi&Provider_ProvID=<<<Provider_ProvID>>>&mlt=<<<mlt>>>&misLINKS=<<<misLINKS>>>','ElecDocs')">View Provider's Electronic Documents</A> ]]
    </TD>
  </TR>
</TABLE>

</LOADHIDDEN>
</FORM>
<SCRIPT LANGUAGE="JavaScript">
document.ProviderLicenses.elements[0].focus();
</SCRIPT>

[[myHTML->rightpane(%form+search)]]

<SCRIPT type="text/javascript" src="/src/cgi/js/vMCAutocomplete.js?v=202006082124"></SCRIPT>
<SCRIPT LANGUAGE="JavaScript" >
callAjax('xOccupationSnomed','','','&Autocomplete=MCAutocompleteSpecialty&Target=ProviderLicenses_Specialty_1','popup.pl');
callAjax('xTaxonomy','','','&Autocomplete=MCAutocompleteTaxonomy&Target=ProviderLicenses_Taxonomy_1','popup.pl');
</SCRIPT>
