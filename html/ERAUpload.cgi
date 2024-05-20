[[myHTML->new(%form+ERA Upload Electronic Document)]]
[[myHTML->hdr(%form)]]
[[myHTML->menu(%form)]]

<DIV ALIGN="center" >
<TABLE WIDTH="90%" BGCOLOR="white" BORDER="0" CELLSPACING="0" CELLPADDING="2" >
  <TR ><TD CLASS="main fullsize" ><B>ERA Document Upload</B></TD></TR>
</TABLE>

<FORM NAME="ERAUpload" METHOD=POST ENCTYPE="multipart/form-data" ACTION="/cgi/bin/Upload.cgi?DocType=ERA" > 
<HR WIDTH=90% >
<TABLE WIDTH="90%" BGCOLOR="white" BORDER="0" CELLSPACING="0" CELLPADDING="2" >
  <TR >
    <TD CLASS="port hdrtxt" COLSPAN="2" ><B>Select Electronic Document to upload</B></TD>
    <TD CLASS="portsublink" >
      <INPUT TYPE="submit" NAME="Action" VALUE="Cancel">
    </TD>
  </TR>
  <TR >
    <TD CLASS="strcol" >File: </TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="file" NAME="TheFile" size="55"> 
      <INPUT TYPE="submit" NAME="Action" VALUE="Upload File"> 
    </TD>
  </TR>
</TABLE>
</DIV>
<HR WIDTH=90% >

<INPUT TYPE="hidden" NAME="DocType" VALUE="ERA" >
<INPUT TYPE="hidden" NAME="Client_ClientID" VALUE="<<Client_ClientID>>" >
</LOADHIDDEN>
</FORM>
