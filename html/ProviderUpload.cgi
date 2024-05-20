[[myHTML->newPage(%form+Provider Upload Electronic Document)]]

<FORM NAME="ProviderUpload" METHOD=POST ENCTYPE="multipart/form-data" ACTION="/cgi/bin/Upload.cgi?DocType=Provider&Provider_ProvID=<<<Provider_ProvID>>>" > 
<TABLE CLASS="main fullsize" >
  <TR >
    <TD CLASS="strcol" >
      <<<Provider_FName_1>>> <<<Provider_MName_1>>> <<<Provider_LName_1>>> 
      <BR>Provider Document Upload
    </TD>
    <TD CLASS="numcol" >[[gHTML->setLINKS(%form+back)]]</TD>
  </TR>
</TABLE>
<TABLE CLASS="port fullsize" >
  <TR >
    <TD CLASS="hdrtxt" COLSPAN=2 ><B>Select Electronic Document to upload</B></TD>
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

<INPUT TYPE="hidden" NAME="DocType" VALUE="Provider" >
<INPUT TYPE="hidden" NAME="Provider_ProvID" VALUE="<<Provider_ProvID>>" >
</LOADHIDDEN>
</FORM>
[[myHTML->rightpane(%form+search)]]
