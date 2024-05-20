[[myHTML->newPage(%form+Electonic Documents)]]

<SCRIPT LANGUAGE="JavaScript" SRC="/cgi/js/NoEnter.js"> </SCRIPT>
<SCRIPT LANGUAGE="JavaScript" SRC="/cgi/js/vEntry.js"> </SCRIPT>
<SCRIPT LANGUAGE="JavaScript" SRC="/cgi/js/vClientEDocs.js"> </SCRIPT>

<FORM NAME="ClientEDocs" METHOD=POST ACTION="/cgi/bin/mis.cgi" > 
<TABLE CLASS="main fullsize" >
  <TR >
    <TD CLASS="strcol" >
      <<<Client_FName_1>>> <<<Client_MName_1>>> <<<Client_LName_1>>> 
      <BR>
      Client Electronic Document
    </TD>
    <TD CLASS="numcol" >[[gHTML->setLINKS(%form+back)]]</TD>
  </TR>
</TABLE>
<TABLE CLASS="home fullsize" >
  <TR >
    <TD CLASS="port numcol" COLSPAN="2" >
      <A HREF="javascript:ReportWindow([[DBUtil->quoteSTR(%form+<<<ClientEDocs_Path_1>>>)]],'ViewDocument')" ONMOUSEOVER="window.status='click here to view attached document'; return true;" ONMOUSEOUT="window.status=''" ><IMG BORDER="0" SRC="/images/view_document.gif">View Document</A>
    </TD>
  </TR>
  <TR >
    <TD CLASS="strcol" WIDTH="30%" >Title</TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="TEXT" NAME="ClientEDocs_Title_1" VALUE="<<ClientEDocs_Title_1>>" ONFOCUS="select()" SIZE=35>
    </TD>
  </TR>
  <TR >
    <TD CLASS="strcol" WIDTH="30%" >Description</TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="TEXT" NAME="ClientEDocs_Descr_1" VALUE="<<ClientEDocs_Descr_1>>" ONFOCUS="select()" SIZE=70>
    </TD>
  </TR>
  <TR >
    <TD CLASS="strcol" WIDTH="30%" >Type</TD>
    <TD CLASS="strcol" >
      <SELECT NAME="ClientEDocs_Type_1" >
        [[DBA->selxTable(%form+xEDocType+<<ClientEDocs_Type_1>>+Descr)]]
      </SELECT>
    </TD>
  </TR>
  <TR >
    <TD CLASS="strcol" WIDTH="30%" >Show on Available Forms screen</TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="checkbox" NAME="ClientEDocs_Public_1" VALUE=1 <<ClientEDocs_Public_1=checkbox>> >
    </TD>
  </TR>
  <TR > <TD CLASS="strcol" COLSPAN="2" >(if you put DELETE in both the Title AND Description it will remove/delete this document tonight.)</TD> </TR>
  <TR >
    <TD CLASS="strcol" WIDTH="30%" >CCDA and XML files:</TD>
    <TD CLASS="strcol" >
      <A HREF="javascript:ReportWindow('/cgi/bin/ImportCCDA.cgi?file=<<ClientEDocs_xmlfile_1>>&mlt=<<mlt>>','ImportCCDA',900,1000)" TITLE="Use this link to import this CCDA and create the Client information." >
        The files are available for import: click here to import CCDA
      </A>
    </TD>
  </TR>
</TABLE>
<TABLE CLASS="main fullsize" >
  <TR >
    <TD CLASS="numcol" >
[[SysAccess->verify(%form+Privilege=DeleteEDocs)      <INPUT TYPE="submit" ONCLICK="return vDELETE('Are you sure you want to delete this Electronic Document record and the associated saved Document?')" NAME="ClientEDocs_DELETE_1=1&UpdateTables=all&misPOP=1" VALUE="Delete Document"> ]]
      <INPUT TYPE="submit" ONCLICK="return validate(this.form);" NAME="UpdateTables=all&misPOP=1" VALUE="Add/Update">
    </TD>
  </TR>
</TABLE>

<INPUT TYPE="hidden" NAME="post_update" VALUE="PostUpd->updEDocs(%form+ClientEDocs+<<<ClientEDocs_ID_1>>>)" >
</LOADHIDDEN>
</FORM>
<SCRIPT LANGUAGE="JavaScript">
document.ClientEDocs.elements[0].focus();
</SCRIPT>

[[myHTML->rightpane(%form+search)]]
