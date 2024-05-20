[[myHTML->newPage(%form+Client Journal)]]

<SCRIPT LANGUAGE="JavaScript" SRC="/cgi/js/vEntry.js"> </SCRIPT>
<SCRIPT LANGUAGE="JavaScript" SRC="/cgi/js/vDate.js"> </SCRIPT>
<SCRIPT LANGUAGE="JavaScript" SRC="/cgi/js/vClientJournal.js"> </SCRIPT>

JournalID=<<<ClientJournals_ID>>>
<FORM NAME="Journal" ACTION="/cgi/bin/mis.cgi" METHOD="POST" >
<TABLE CLASS="main fullsize" >
  <TR >
    <TD CLASS="strcol" >
      <<<Client_FName_1>>> <<<Client_MName_1>>> <<<Client_LName_1>>> (<<<Client_ClientID_1>>>) <<<Client_SSN_1>>>
      <BR>
      Client's Journal
    </TD>
    <TD CLASS="numcol" >[[gHTML->setLINKS(%form+back)]]</TD>
  </TR>
</TABLE>
<TABLE CLASS="home fullsize" >
    <TR ><TD CLASS="port hdrtxt" ><TABLE CLASS="home fullsize" >
  <TR>
    <TD CLASS="strcol" WIDTH="30%" >Type
    <TD CLASS="strcol" >
      <SELECT NAME="ClientJournals_Type_1" >[[DBA->selxTable(%form+xJournalType+<<ClientJournals_Type_1>>+Descr)]]</SELECT> 
    </TD>
  </TR>
  <TR >
    <TD CLASS="strcol" WIDTH="30%" >Effective
    <TD CLASS="strcol" >
      <INPUT TYPE=TEXT SIZE="10" NAME="ClientJournals_EffDate_1" VALUE="<<ClientJournals_EffDate_1>>" ONFOCUS="select()" ONCHANGE="return vDate(this)" SIZE="12" >
    </TD>
  </TR>
  <TR >
    <TD CLASS="strcol" WIDTH="30%" >Expires
    <TD CLASS="strcol" >
      <INPUT TYPE=TEXT SIZE="10" NAME="ClientJournals_ExpDate_1" VALUE="<<ClientJournals_ExpDate_1>>" ONFOCUS="select()" ONCHANGE="return vDate(this)" SIZE="12" >
    </TD>
  </TR>
  <TR >
    <TD CLASS="strcol" WIDTH="30%" >Active
    <TD CLASS="strcol" >
      <INPUT TYPE="radio" NAME="ClientJournals_Active_1" VALUE=1 <<ClientJournals_Active_1=1>> > yes
      <INPUT TYPE="radio" NAME="ClientJournals_Active_1" VALUE=0 <<ClientJournals_Active_1=0>> > no
    </TD>
  </TR>
  <TR>
    <TD CLASS="strcol" WIDTH="30%" >Summary
    <TD CLASS="strcol" >
      <TEXTAREA COLS=70 ROWS=3 WRAP="virtual" NAME="ClientJournals_Summary_1" ><<ClientJournals_Summary_1>></TEXTAREA>
    </TD>
  <TR>
    <TD CLASS="strcol" WIDTH="30%" >Description
    <TD CLASS="strcol" >
      <TEXTAREA COLS=70 ROWS=18 WRAP="virtual" NAME="ClientJournals_Descr_1" ><<ClientJournals_Descr_1>></TEXTAREA>
    </TD>
    </TABLE></TD></TR>
</TABLE>
<TABLE CLASS="main fullsize" >
  <TR>
    <TD CLASS="numcol" >
[[SysAccess->verify(%form+Privilege=DelJournal) <INPUT TYPE="submit" ONCLICK="return vDELETE('Are you sure you want to delete record?');" NAME="ClientJournals_DELETE_1=1&UpdateTables=all&misPOP=1" VALUE="Delete"> ]]
      <INPUT TYPE="submit" ONCLICK="return validate(this.form);" NAME="UpdateTables=all&misPOP=1" VALUE="Add/Update">
    </TD>
  </TR>
</TABLE>

<INPUT TYPE="hidden" NAME="post_update" VALUE="PostUpd->NewJournal(%form)" >
<INPUT TYPE="hidden" NAME="NEWJOURNAL" VALUE="<<<ClientJournals_ID>>>" >
</LOADHIDDEN>
</FORM>
<SCRIPT LANGUAGE="JavaScript">
document.Journal.elements[0].focus();
</SCRIPT>

[[myHTML->rightpane(%form+search)]]
