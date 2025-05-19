[[myHTML->newPage(%form+Electronic Documents+++++lhcautocomplete)]]

<SCRIPT LANGUAGE="JavaScript" SRC="/src/cgi/js/NoEnter.js"> </SCRIPT>
<SCRIPT LANGUAGE="JavaScript" SRC="/src/cgi/js/vEntry.js"> </SCRIPT>
<SCRIPT LANGUAGE="JavaScript" SRC="/src/cgi/js/vClientEDocs.js?v=202009141810"> </SCRIPT>
<SCRIPT LANGUAGE="JavaScript" SRC="/src/cgi/js/vNum.js"> </SCRIPT>
<SCRIPT TYPE="text/javascript" SRC="/cgi/jquery/jquery-1.12.4.js" ></SCRIPT>
<SCRIPT TYPE="text/javascript" src="/cgi/lhc/autocomplete-lhc-17.0.3/autocomplete-lhc.min.js"></SCRIPT>
<SCRIPT TYPE="text/javascript" SRC="/cgi/jquery/jquery-ui-1.12.1/jquery-ui.min.js" ></SCRIPT>

<FORM NAME="ClientEDocs" METHOD=POST ACTION="/src/cgi/bin/mis.cgi" > 
<TABLE CLASS="main fullsize" >
  <TR >
    <TD CLASS="strcol" >
      <<<Client_FName_1>>> <<<Client_MName_1>>> <<<Client_LName_1>>> (<<<Client_ClientID_1>>>) <<<Client_SSN_1>>>
      <BR>
      Client Electronic Document
    </TD>
    <TD CLASS="numcol" >[[gHTML->setLINKS(%form+back)]]</TD>
  </TR>
</TABLE>
<TABLE CLASS="home fullsize" >														   
  <TR >
    <TD CLASS="numcol" COLSPAN="2" >
      <A HREF="javascript:ReportWindow([[DBUtil->quoteSTR(%form+<<<ClientEDocs_Path_1>>>)]],'ViewDocument')" ONMOUSEOVER="window.status='click here to view attached document'; return true;" ONMOUSEOUT="window.status=''" ><IMG BORDER="0" SRC="/images/view_document.gif">View Document</A>																								   
    </TD>
  </TR>
  <TR >
    <TD CLASS="strcol" WIDTH=30% >Title</TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="TEXT" NAME="ClientEDocs_Title_1" VALUE="<<ClientEDocs_Title_1>>" ONFOCUS="select()" SIZE=35>
    </TD>
  </TR>
  <TR >
    <TD CLASS="strcol" WIDTH=30% >Description</TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="TEXT" NAME="ClientEDocs_Descr_1" VALUE="<<ClientEDocs_Descr_1>>" ONFOCUS="select()" SIZE=70>
    </TD>
  </TR>
  <TR >
    <TD CLASS="strcol" WIDTH=30% >LOINC Description</TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="TEXT" ID="DocumentOntology_Descr" SIZE=40 ONFOCUS="select()" VALUE="[[DBA->getxref(%form+xLDO+<<<ClientEDocs_Loinc_1>>>)]]" >
      <INPUT TYPE="hidden" NAME="ClientEDocs_Loinc_1" SIZE=40 VALUE="<<ClientEDocs_Loinc_1>>" >
      <span>&nbsp;(Common keywords include: Assessment, Consent, Insurance, Mental Health, Plan, Release, etc.)</span>
    </TD>
  </TR>
  <TR ><TD CLASS="port hdrtxt" COLSPAN="2" >Document Ontology</TD></TR>
  <TR >
    <TD CLASS="strcol" WIDTH=30% ></TD>
    <TD CLASS="strcol" >ie: or you may enter wildcard * to see all suggestions</TD>
  </TR>
  <TR >
    <TD CLASS="strcol" WIDTH=30% >Subject Matter Domain</TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="TEXT" ID="DocumentOntology_SubjectMatterDomain" SIZE=40 ONFOCUS="select()" VALUE="[[DBA->getxxref(%form+xLDO+xLDOSubjectMatterDomain+<<<ClientEDocs_Loinc_1>>>+SubjectMatterDomain)]]" >
    </TD>
  </TR>
  <TR >
    <TD CLASS="strcol" WIDTH=30% >Role</TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="TEXT" ID="DocumentOntology_Role" SIZE=40 ONFOCUS="select()" VALUE="[[DBA->getxxref(%form+xLDO+xLDORole+<<<ClientEDocs_Loinc_1>>>+Role)]]" >
    </TD>
  </TR>
  <TR >
    <TD CLASS="strcol" WIDTH=30% >Setting</TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="TEXT" ID="DocumentOntology_Setting" SIZE=40 ONFOCUS="select()" VALUE="[[DBA->getxxref(%form+xLDO+xLDOSetting+<<<ClientEDocs_Loinc_1>>>+Setting)]]" >
    </TD>
  </TR>
  <TR >
    <TD CLASS="strcol" WIDTH=30% >Type of Service</TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="TEXT" ID="DocumentOntology_TypeOfService" SIZE=40 ONFOCUS="select()" VALUE="[[DBA->getxxref(%form+xLDO+xLDOTypeOfService+<<<ClientEDocs_Loinc_1>>>+TypeOfService)]]" >
    </TD>
  </TR>
  <TR >
    <TD CLASS="strcol" WIDTH=30% >Kind of Document</TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="TEXT" ID="DocumentOntology_Kind" SIZE=40 ONFOCUS="select()" VALUE="[[DBA->getxxref(%form+xLDO+xLDOKind+<<<ClientEDocs_Loinc_1>>>+Kind)]]" >
    </TD>
  </TR>
  <TR > <TD CLASS="strcol" COLSPAN="2" ><HR></TD> </TR>
  <TR >
    <TD CLASS="strcol" WIDTH=30% >Freeform Type (Deprecated)</TD>
    <TD CLASS="strcol" >
      <<ClientEDocs_Descr_1>>
    </TD>
  </TR>
  <TR >			
    <TD CLASS="strcol" WIDTH=30% >Type</TD>
    <TD CLASS="strcol" >
      <SELECT NAME="ClientEDocs_Type_1" >
        [[DBA->selxTable(%form+xEDocType+<<ClientEDocs_Type_1>>+Descr)]]
      </SELECT>
    </TD>
  </TR>
  <TR > <TD CLASS="strcol" COLSPAN="2" >(Try to maintain the Title: DELETE Description: DELETE for overnight cron job deletion.)</TD> </TR>										  
</TABLE>
<TABLE CLASS="main fullsize" >
  <TR >
    <TD CLASS="numcol" >
[[SysAccess->verify(%form+Privilege=DeleteEDocs) <INPUT TYPE="submit" ONCLICK="return vDELETE('Are you sure you want to delete this Electronic Document record and the associated saved Document?')" NAME="ClientEDocs_DELETE_1=1&UpdateTables=all&misPOP=1" VALUE="Delete Document" > ]]
      <INPUT TYPE="submit" ONCLICK="return validate(this.form);" NAME="UpdateTables=all&misPOP=1" VALUE="Add/Update" >
    </TD>
  </TR>
</TABLE>

<INPUT TYPE="hidden" NAME="post_update" VALUE="PostUpd->updEDocs(%form+ClientEDocs+<<<ClientEDocs_ID_1>>>)" >
</LOADHIDDEN>
</FORM>
<SCRIPT type="text/javascript" src="/src/cgi/js/vEDocsAutocomplete.js?v=202009120626"></SCRIPT>
<SCRIPT LANGUAGE="JavaScript">
document.ClientEDocs.elements[0].focus();
$(document).ready(function() {
  eDocsAutocompletes('<<mlt>>');
});
</SCRIPT>

[[myHTML->rightpane(%form+search)]]
