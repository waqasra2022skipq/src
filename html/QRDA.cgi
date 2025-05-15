[[myHTML->newPage(%form+Agency Control)]]

<SCRIPT LANGUAGE="JavaScript" SRC="/src/cgi/js/NoEnter.js"> </SCRIPT>

[[*SysAccess->verify(%form+Privilege=Agent)]]

<FORM NAME="QRDA" ACTION="/cgi/bin/mis.cgi" METHOD="POST" >
<TABLE CLASS="main fullsize" >
  <TR >
    <TD CLASS="strcol" >
      <<<Provider_FName_1>>> <<<Provider_MName_1>>> <<<Provider_LName_1>>> 
      (<<<Provider_ProvID_1>>>)
      <BR>Provider Control
    </TD>
    <TD CLASS="numcol" >[[gHTML->setLINKS(%form+back)]]</TD>
  </TR>
</TABLE>
<HR WIDTH="90%" >
<TABLE CLASS="home fullsize" >
  <TR>
    <TD CLASS="strcol" >
      <A HREF="javascript:ReportWindow('/tmp/FILEs/CQM2/QRDA_kls_2503_55284.htm','QRDQ2')" >click to display CDA</A>
    </TD>
  </TR>
</TABLE>

</LOADHIDDEN>
</FORM>
<SCRIPT LANGUAGE="JavaScript">
document.QRDA.elements[0].focus();
</SCRIPT>

[[myHTML->rightpane(%form+search)]]
