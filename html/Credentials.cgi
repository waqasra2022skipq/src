[[myHTML->newPage(%form+Provider Credentials)]]

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
      (<<<Provider_ProvID_1>>>)
      <BR>Credentials
    </TD>
    <TD CLASS="numcol" >[[gHTML->setLINKS(%form+back)]]</TD>
  </TR>
</TABLE>
<HR WIDTH="90%" >
<TABLE CLASS="home fullsize" >
  <TR >
    <TD CLASS="strcol" WIDTH="20%" >Assoc. Insurance</TD>
    <TD CLASS="strcol" >
      <SELECT NAME="Credentials_InsID_1" >
        [[DBA->selInsurance(%form+<<Credentials_InsID_1>>)]]
      </SELECT>
    </TD>
  </TR>
  <TR >
    <TD CLASS="strcol" WIDTH="20%" >Provider ID (PIN)</TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="TEXT" NAME="Credentials_PIN_1" VALUE="<<Credentials_PIN_1>>" SIZE=50 > 
    </TD>
  </TR>
  <TR >
    <TD CLASS="strcol" WIDTH="20%" >PIN Qualifier</TD>
    <TD CLASS="strcol" >
      <SELECT NAME="Credentials_RefID_1">[[DBA->selxTable(%form+xRefID+<<Credentials_RefID_1>>+ID Descr)]]</SELECT> 
    </TD>
  </TR>
  <TR >
    <TD CLASS="strcol" WIDTH="20%" >Credential Type</TD>
    <TD CLASS="strcol" >
      <SELECT NAME="Credentials_CredID_1">
        [[DBA->selxTable(%form+xCredentials+<<Credentials_CredID_1>>+Descr Rank)]]
      </SELECT> 
    </TD>
  </TR>
  <TR >
    <TD CLASS="strcol" WIDTH="20%" >Rank Credential</TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="text" NAME="Credentials_Rank_1" VALUE="<<Credentials_Rank_1>>" ONFOCUS="select()" ONCHANGE="return vNum(this,1,9);" MAXLENGTH=3 SIZE=3>  (used if Provider has more than 1 Credential for an Insurance)
    </TD>
  </TR>
  <TR >
    <TD CLASS="strcol" >Taxonomy</TD>
    <TD CLASS="strcol" >
      <INPUT ID="MCAutocomplete" TYPE="text" VALUE="[[DBA->getxref(%form+xTaxonomy+<<<Credentials_Taxonomy_1>>>+ID Spec Class Type+++ | )]]" ONFOCUS="select()" SIZE="100" />
      <INPUT TYPE="hidden" NAME="Credentials_Taxonomy_1" VALUE="<<Credentials_Taxonomy_1>>" >
    </TD>
  </TR>
  <TR >
    <TD CLASS="strcol hotmsg" COLSPAN="2" >Billing/rendering Provider taxonomy codes MUST match the OHCA Master Provider List (MPL), billing/rendering Provider addresses MUST ALSO match the OHCA MPL.  Check the OHCA Provider Contract to verify.</TD>
  </TR>
  <TR >
    <TD CLASS="strcol" WIDTH="20%" >Restriction</TD>
    <TD CLASS="strcol" >
      <SELECT NAME="Credentials_Restriction_1" >
        [[DBA->selxTable(%form+xSCRestrictions+<<Credentials_Restriction_1>>)]]
      </SELECT> 
    </TD>
  </TR>
  <TR >
    <TD CLASS="strcol" WIDTH="30%" >Designated Provider</TD>
    <TD CLASS="strcol" >
      <SELECT ID="DesigProvID" NAME="Credentials_DesigProvID_1" ONCHANGE="callAjax('vInsID',this.value,this.id,'&i='+document.Credentials.Credentials_InsID_1.value);" >
        [[DBA->selProviders(%form+<<Credentials_DesigProvID_1>>)]]
      </SELECT>
      <SPAN ID="msgDesigProvID"></SPAN>
    </TD>
  </TR>
  <TR >
    <TD CLASS="strcol hotmsg" COLSPAN="2" >Do not select a Designated Provider unless required under Medicare. The Designated Provider is only used when the Rendering Provider does not have a PIN for the insurance.  The Designated Provider's PIN will then be used for billing instead of the Provider on the note.</TD>
  </TR>
</TABLE>
[[gHTML->RestrictedCredentialsFields(%form+Agent)]]
<TABLE CLASS="main fullsize" >
  <TR>
    <TD CLASS="numcol" >
      <INPUT TYPE="submit" ONCLICK="return vDELETE('Are you sure you want to delete this Credential?');" NAME="Credentials_DELETE_1=1&UpdateTables=all&misPOP=1" VALUE="Delete">
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
callAjax('xTaxonomy','','','&Autocomplete=MCAutocomplete&Target=Credentials_Taxonomy_1','popup.pl');
</SCRIPT>
