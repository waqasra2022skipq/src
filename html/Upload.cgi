[[myHTML->newPage(%form+Provider Upload Electronic Document)]]

<FORM NAME="Upload" METHOD="POST" ENCTYPE="multipart/form-data" ACTION="/cgi/bin/Upload.cgi" > 
<TABLE CLASS="port fullsize" >
  <TR >
    <TD CLASS="hdrtxt" COLSPAN="2" ><B>Select Electronic Document to upload</B></TD>
    <TD CLASS="numcol" >
      <INPUT TYPE="submit" NAME="Action" VALUE="Cancel">
    </TD>
  </TR>
</TABLE >
<TABLE CLASS="home fullsize" >
  <TR >
    <TD CLASS="strcol" >File: </TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="file" NAME="TheFile" size="55"> 
      <INPUT TYPE="submit" NAME="Action" VALUE="Upload File"> 
    </TD>
  </TR>
</TABLE>
</DIV>

<INPUT TYPE="hidden" NAME="DocType" VALUE="<<DocType>>" >
<INPUT TYPE="hidden" NAME="Provider_ProvID" VALUE="<<Provider_ProvID>>" >
<INPUT TYPE="hidden" NAME="DocID" VALUE="<<ProviderEDocs_ID_1>>" >
<INPUT TYPE="hidden" NAME="DocTitle" VALUE="<<ProviderEDocs_Title_1>>" >
<INPUT TYPE="hidden" NAME="DocDescr" VALUE="<<ProviderEDocs_Descr_1>>" >
<INPUT TYPE="hidden" NAME="DocTag" VALUE="<<ProviderEDocs_Type_1>>" >
<INPUT TYPE="hidden" NAME="DocPath" VALUE="<<ProviderEDocs_Path_1>>" >
<INPUT TYPE="hidden" NAME="DocLink" VALUE="<<ProviderEDocs_Link_1>>" >
</LOADHIDDEN>
</FORM>
</BODY>
</HTML>
