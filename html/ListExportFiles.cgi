[[myHTML->newPage(%form+Export CCDA Documtemts)]]
[[[DBForm->pushLINK()]]]

<SCRIPT LANGUAGE="JavaScript" SRC="/src/cgi/js/novalidate.js"> </SCRIPT>
<FORM NAME="ListExportFiles" ACTION="/cgi/bin/mis.cgi" METHOD="POST" >

<TABLE CLASS="main fullsize" >
  <TR >
    <TD CLASS="strcol" >
      <<<Provider_FName_1>>> <<<Provider_MName_1>>> <<<Provider_LName_1>>>
      <BR>Export CCDA Documents
    </TD>
    <TD CLASS="numcol" >[[gHTML->setLINKS(%form+back)]]</TD>
  </TR>
</TABLE>
<SPAN ID="ListExportFiles" >
[[myHTML->ListSel(%form+ListExportFiles+<<<Provider_ProvID>>>+<<<LINKID>>>+<<<Provider_Locked_1>>>)]]
</SPAN>

[[SysAccess->verify(%form+Privilege=MUAgent)      <A HREF="javascript:ReportWindow('/src/cgi/bin/GenReport.cgi?Name=GenerateCCDAs&mlt=<<mlt>>&daterange=last3m\&InsID=100&xtable=','GenerateCCDAs',900,1000)" TITLE="Use this link to generate CCDAs for Export.<BR>Then refresh this page.<BR>Also found on User Reports-System." >Generate CCDAs for export</A><BR> ]]
[[SysAccess->verify(%form+Privilege=MUAgent)      <A HREF="javascript:ReportWindow('/src/cgi/bin/GenReport.cgi?Name=GENJOB&mlt=<<mlt>>&daterange=last3m\&InsID=100&xtable=','GenerateCCDAJob',900,1000)" TITLE="Use this link to generate Job to execute CCDAs for Export.<BR>Then refresh this page.<BR>Also found on User Reports-System." >Set Up Job for Scheduler</A><BR> ]]
[[SysAccess->verify(%form+Privilege=MUAgent)      <A HREF="javascript:ReportWindow('/src/cgi/bin/GenReport.cgi?Name=GenerateQRDAs&mlt=<<mlt>>&daterange=last3m\&InsID=100&xtable=','GenerateQRDAs',900,1000)" TITLE="Use this link to generate QRDAs for Export.<BR>Then refresh this page.<BR>Also found on User Reports-System." >Generate QRDAs for export</A><BR> ]]

</LOADHIDDEN>
</FORM>
[[myHTML->rightpane(%form+search)]]
