[[myHTML->newPage(%form+Client Opioid Registry Document)]]

<DIV ALIGN="center" >
<TABLE CLASS="main fullsize" BORDER="0" CELLSPACING="0" CELLPADDING="2" >
  <TR ><TD><B>Client Opioid Registry Document Upload</B></TD></TR>
</TABLE>

<FORM NAME="ClientOpioidRegistry" METHOD=POST ENCTYPE="multipart/form-data" ACTION="/cgi/bin/Upload.cgi?DocType=OpioidRegistry&Client_ClientID=<<<Client_ClientID>>>" > 
<HR >
<TABLE CLASS="home fullsize" BORDER="0" CELLSPACING="0" CELLPADDING="2" >
  <TR >
    <TD CLASS="port hdrtxt" COLSPAN="2" ><B>Select Opioid Registry Document to upload</B></TD>
    <TD CLASS="portsublink" >
      <INPUT TYPE="submit" NAME="Action" VALUE="Cancel">
    </TD>
  </TR>
  <TR >
    <TD CLASS="strcol" > </TD>
    <TD CLASS="strcol" >
      <INPUT ID="get_opioid_registry_link" TYPE="button" VALUE="Get Opioid Registry Download Link">
    </TD>
  </TR>
  <TR > <TD CLASS="strcol" COLSPAN="2" ><HR></TD> </TR>
  <TR >
    <TD CLASS="strcol" >File: </TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="file" NAME="TheFile" size="55"> 
      <INPUT TYPE="submit" NAME="Action" VALUE="Upload File"> 
    </TD>
  </TR>
</TABLE>
</DIV>
<HR >

<INPUT TYPE="hidden" NAME="DocType" VALUE="OpioidRegistry" >
<INPUT TYPE="hidden" NAME="Client_ClientID" VALUE="<<Client_ClientID>>" >
</LOADHIDDEN>
</FORM>
[[myHTML->rightpane(%form+search)]]
<SCRIPT LANGUAGE="JavaScript" SRC="/cgi/js/vOpioidRegistry.js?202010261243"> </SCRIPT>
<SCRIPT LANGUAGE="Javascript">
$(document).ready(function() {
  createOpioidRegistryDownloadLink("get_opioid_registry_link", "<<<Client_ClientID>>>", "<<<mlt>>>");
});
</SCRIPT>
