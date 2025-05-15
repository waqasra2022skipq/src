[[myHTML->newPage(%form+Electonic Documents)]]

<SCRIPT LANGUAGE="JavaScript" SRC="/src/cgi/js/NoEnter.js"> </SCRIPT>
<SCRIPT LANGUAGE="JavaScript" SRC="/src/cgi/js/vEntry.js"> </SCRIPT>
<SCRIPT LANGUAGE="JavaScript" SRC="/src/cgi/js/vMisEDocs.js"> </SCRIPT>
<SCRIPT type="text/javascript" src="/src/cgi/js/ajaxrequest.js"></SCRIPT>

<FORM NAME="MisEDocs" ACTION="/cgi/bin/mis.cgi" METHOD="POST" > 
<TABLE CLASS="main fullsize" >
  <TR >
    <TD CLASS="strcol" >
      <<<Provider_FName_1>>> <<<Provider_MName_1>>> <<<Provider_LName_1>>> 
      <BR>
      Millennium Electronic Forms
    </TD>
    <TD CLASS="numcol" >[[gHTML->setLINKS(%form+back)]]</TD>
  </TR>
</TABLE>
<TABLE CLASS="home fullsize" >
  <TR >
    <TD CLASS="port numcol" COLSPAN="2" >
      <A HREF="javascript:ReportWindow([[DBUtil->quoteSTR(%form+<<<ProviderEDocs_Path_1>>>)]],'ViewDocument')" ONMOUSEOVER="window.status='click here to view attached document'; return true;" ONMOUSEOUT="window.status=''" ><IMG BORDER="0" SRC="/images/view_document.gif">View Document</A>
    </TD>
  </TR>
  <TR > <TD CLASS="strcol" COLSPAN="2" >(if you put DELETE in both the Title AND Description it will remove/delete this document tonight.)</TD> </TR>
  <TR >
    <TD CLASS="strcol" WIDTH="30%" >Title</TD>
    <TD CLASS="strcol" >
      <TEXTAREA NAME="ProviderEDocs_Title_1" COLS="90" ROWS="2" WRAP="virtual" ><<ProviderEDocs_Title_1>></TEXTAREA>
    </TD>
  </TR>
  <TR >
    <TD CLASS="strcol" WIDTH="30%" >Description</TD>
    <TD CLASS="strcol" >
      <TEXTAREA NAME="ProviderEDocs_Descr_1" COLS="90" ROWS="2" WRAP="virtual" ><<ProviderEDocs_Descr_1>></TEXTAREA>
    </TD>
  </TR>
  <TR >
    <TD CLASS="strcol" WIDTH="30%" >Tag</TD>
    <TD CLASS="strcol" >
      <SELECT NAME="ProviderEDocs_Type_1" ONFOCUS="select()" >
        [[DBA->selxTable(%form+xEDocTags+<<ProviderEDocs_Type_1>>+Tag)]]
      </SELECT> 
    </TD>
  </TR>
  <TR>
    <TD CLASS="strcol" WIDTH="30%" >Upload Document</TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="submit" ONCLICK="return validate(this.form);" NAME="view=Upload.cgi&ProviderEDocs_ID=<<<ProviderEDocs_ID>>>&Provider_ProvID=<<<Provider_ProvID>>>&DocType=MisEDocs&UpdateTables=all" VALUE="upload" >
    </TD>
  </TR>
  <TR>
    <TD CLASS="strcol" WIDTH="30%" >File</TD>
    <TD CLASS="strcol" >
[[gHTML->ifld(%form+ProviderEDocs_Path_1+displayonly)]]
    </TD>
  </TR>
  <TR > <TD CLASS="strcol" COLSPAN="2" >DR. HAMIL</TD> </TR>
  <TR > <TD CLASS="strcol" COLSPAN="2" >(Upload a document above OR enter the http: link to a document below BUT NOT BOTH.)</TD> </TR>
  <TR >
    <TD CLASS="strcol" WIDTH="30%" >Link</TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="TEXT" NAME="ProviderEDocs_Link_1" VALUE="<<ProviderEDocs_Link_1>>" ONFOCUS="select()" SIZE="100" >
    </TD>
  </TR>
</TABLE>
<TABLE CLASS="main fullsize" >
  <TR >
    <TD CLASS="numcol" >
[[SysAccess->verify(%form+Privilege=DeleteEDocs) <INPUT TYPE="submit" ONCLICK="return vDELETE('Are you sure you want to delete this Electronic Document record and the associated saved Document?')" NAME="ProviderEDocs_DELETE_1=1&UpdateTables=all&misPOP=1" VALUE="Delete Document"> ]]
      <INPUT TYPE="submit" ONCLICK="return validate(this.form);" NAME="UpdateTables=all&misPOP=1" VALUE="Add/Update">
    </TD>
  </TR>
</TABLE>

<INPUT TYPE="hidden" NAME="ProviderEDocs_Public_1" VALUE="1" >
<INPUT TYPE="hidden" NAME="post_update" VALUE="PostUpd->updEDocs(%form+ProviderEDocs+<<<ProviderEDocs_ID_1>>>)" >
</LOADHIDDEN>
</FORM>
<SCRIPT LANGUAGE="JavaScript">
document.MisEDocs.elements[0].focus();
callAjax('vUpload','<<<ProviderEDocs_Path_1>>>','','&p=<<<ProviderEDocs_ID_1>>>');
</SCRIPT>

[[myHTML->rightpane(%form+search)]]
