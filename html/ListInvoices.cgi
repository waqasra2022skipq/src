[[myHTML->newPage(%form+Client Invoices)]]

<SCRIPT LANGUAGE="JavaScript" SRC="/src/cgi/js/novalidate.js"> </SCRIPT>
<FORM NAME="ListInvoices" ACTION="/src/cgi/bin/genInvoices.cgi" METHOD="POST" >
<TABLE CLASS="main fullsize" >
  <TR >
    <TD CLASS="strcol" >
      <<<Client_FName_1>>> <<<Client_MName_1>>> <<<Client_LName_1>>> (<<<Client_ClientID_1>>>) <<<Client_SSN_1>>>
      <BR>
      Client Invoices
    </TD>
    <TD CLASS="numcol" >[[gHTML->setLINKS(%form+back)]]</TD>
  </TR>
</TABLE>
<TABLE CLASS="home fullsize" >
  <TR >
    <TD >
      Selects the notes with Amount Due and Reconciled or Denied or (Inprocess and private/group).
    </TD>
  </TR>
  <TR >
    <TD >
<SPAN ID="ListClientInvoices" >
[[myHTML->ListSel(%form+ListClientInvoices+<<<Client_ClientID>>>+<<<LINKID>>>+<<<Client_Locked_1>>>)]]
</SPAN>
    </TD>
  </TR>
</TABLE>
<TABLE CLASS="main fullsize" >
  <TR >
    <TD CLASS="numcol" >
      <INPUT TYPE="submit" ONCLICK="return validate(this.form);" NAME="Client_ClientID=<<<Client_ClientID>>>&UpdateTables=all&misPOP=1" VALUE="Generate New Invoice">
    </TD>
  </TR>
</TABLE>

</LOADHIDDEN>
</FORM>
[[myHTML->rightpane(%form+search)]]
