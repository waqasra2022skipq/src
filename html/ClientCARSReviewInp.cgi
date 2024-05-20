[[myHTML->newPage(%form+CARS Review)]]

<SCRIPT LANGUAGE="JavaScript" SRC="/cgi/js/NoEnter.js"> </SCRIPT>
<SCRIPT LANGUAGE="JavaScript" SRC="/cgi/js/vEntry.js"> </SCRIPT>
<SCRIPT LANGUAGE="JavaScript" SRC="/cgi/js/vClientCARSReview.js"> </SCRIPT>

<FORM NAME="ClientCARSReview" ACTION="/cgi/bin/mis.cgi" METHOD="POST" >
<TABLE CLASS="main fullsize" >
  <TR >
    <TD CLASS="strcol" >
      <<<Client_FName_1>>> <<<Client_MName_1>>> <<<Client_LName_1>>> (<<<Client_ClientID_1>>>) <<<Client_SSN_1>>>
      <BR>
      CARSReview Member
    </TD>
    <TD CLASS="numcol" >[[gHTML->setLINKS(%form+back)]]</TD>
  </TR>
</TABLE>
<TABLE CLASS="home fullsize" >
  <TR >
    <TD CLASS="strcol" >Month for:
      <SELECT NAME="ClientCARSReview_Month_1" >[[PopUp->selYearMonth(%form+<<ClientCARSReview_Month_1>>)]]</SELECT>
    </TD>
  </TR>
  <TR > <TD CLASS="strcol" >Progress Evidence</TD> </TR>
  <TR >
    <TD CLASS="strcol" >
      <TEXTAREA NAME="ClientCARSReview_ProgEvidence_1" COLS="80" ROWS="5" WRAP=virtual ><<ClientCARSReview_ProgEvidence_1>></TEXTAREA>
    </TD>
  </TR>
  <TR > <TD CLASS="strcol" >Issues / Concerns</TD> </TR>
  <TR >
    <TD CLASS="strcol" >
      <TEXTAREA NAME="ClientCARSReview_Issues_1" COLS="80" ROWS="5" WRAP=virtual ><<ClientCARSReview_Issues_1>></TEXTAREA>
    </TD>
  </TR>
</TABLE>
<TABLE CLASS="main fullsize" >
  <TR>
    <TD CLASS="numcol" >
      <INPUT TYPE="submit" ONCLICK="return vDELETE('Are you sure you want to delete record?');" NAME="ClientCARSReview_DELETE_1=1&UpdateTables=all&misPOP=1" VALUE="Delete">
      <INPUT TYPE="submit" ONCLICK="return validate(this.form);" NAME="UpdateTables=all&misPOP=1" VALUE="Add/Update">
    </TD>
  </TR>
</TABLE>

</LOADHIDDEN>
</FORM>
<SCRIPT LANGUAGE="JavaScript">
document.ClientCARSReview.elements[0].focus();
</SCRIPT>
[[myHTML->rightpane(%form+search)]]
