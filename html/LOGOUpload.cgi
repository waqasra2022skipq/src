[[myHTML->newPage(%form+Upload LOGO)]]

<DIV ALIGN="center" >
<TABLE WIDTH="90%" BGCOLOR="white" BORDER="0" CELLSPACING="0" CELLPADDING="2" >
  <TR ><TD CLASS="main fullsize" ><B>LOGO Upload</B></TD></TR>
</TABLE>

<FORM NAME="LOGOUpload" METHOD=POST ENCTYPE="multipart/form-data" ACTION="/cgi/bin/Upload.cgi?DocType=LOGO&Provider_ProvID=<<<Provider_ProvID>>>" > 
<HR WIDTH="90%" >
<TABLE WIDTH="90%" BGCOLOR="white" BORDER="0" CELLSPACING="0" CELLPADDING="2" >
  <TR >
    <TD CLASS="port hdrtxt" COLSPAN="2" ><B>Select Image file to upload</B></TD>
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
<HR WIDTH="90%" >

<INPUT TYPE="hidden" NAME="DocType" VALUE="LOGO" >
<INPUT TYPE="hidden" NAME="Provider_ProvID" VALUE="<<Provider_ProvID>>" >
</LOADHIDDEN>
</FORM>
</HTML>
