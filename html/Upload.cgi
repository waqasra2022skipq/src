[[myHTML->newHTML(%form+UPLOAD Document)]]

<FORM NAME="Upload" METHOD=POST ENCTYPE="multipart/form-data" ACTION="/cgi/bin/Upload.cgi?DocType=<<DocType>>" > 
<TABLE CLASS="main fullsize" >
  <TR >
    <TD CLASS="strcol" >
      <B><<DocType>> Document Upload</B>
    </TD>
  </TR>
</TABLE>

<HR WIDTH="90%" >
<TABLE CLASS="port fullsize" >
  <TR >
    <TD CLASS="port hdrtxt" COLSPAN="2" ><B>Select Electronic Document to upload</B></TD>
    <TD CLASS="portsublink" >
      <INPUT TYPE="submit" NAME="Action" VALUE="Cancel">
    </TD>
  </TR>
</TABLE>
<TABLE CLASS="home fullsize" >
  <TR >
    <TD CLASS="strcol" >File: </TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="file" NAME="TheFile" style="border: solid 1px black" SIZE="55" >
      <INPUT TYPE="submit" NAME="Action" VALUE="Upload File"> 
    </TD>
  </TR>
</TABLE>
<HR WIDTH="90%" >

<INPUT TYPE="hidden" NAME="DocType" VALUE="<<DocType>>" >
</LOADHIDDEN>
</FORM>
