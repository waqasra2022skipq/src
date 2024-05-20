[[myHTML->newPage(%form+Client MHSF)]]

<SCRIPT LANGUAGE="JavaScript" SRC="/cgi/js/NoEnter.js"> </SCRIPT>
<SCRIPT LANGUAGE="JavaScript" SRC="/cgi/js/vEntry.js"> </SCRIPT>
<SCRIPT LANGUAGE="JavaScript" SRC="/cgi/js/vClientMHSF.js"> </SCRIPT>
<SCRIPT LANGUAGE="JavaScript" SRC="/cgi/js/vDate.js"> </SCRIPT>

<FORM NAME="ClientMHSF" ACTION="/cgi/bin/mis.cgi" METHOD="POST" >
<TABLE CLASS="main fullsize" >
  <TR >
    <TD CLASS="strcol" >
      <<<Client_FName_1>>> <<<Client_MName_1>>> <<<Client_LName_1>>> (<<<Client_ClientID_1>>>) <<<Client_SSN_1>>>
      <BR>
      Substance Abuse View/Edit Page
    </TD>
    <TD CLASS="numcol" >[[gHTML->setLINKS(%form+back)]]</TD>
  </TR>
</TABLE>
<TABLE CLASS="home fullsize" >
  <TR ><TD CLASS="port hdrtxt" >Mental Health Screening Form-III FY15</TD></TR>
  <TR ><TD CLASS="port strcol" >Instructions: In this program, we help people with all their problems, not just their addictions. This commitment includes helping people with emotional problems. Our staff is ready to help you to deal with any emotional problems you may have, but we can do this only if we are aware of the problems. Any information you provide to us on this form will be kept in strict confidence. It will not be released to any outside person or agency without your permission. If you do not know how to answer these questions, ask the staff member giving you this form for guidance. Please note, each item refers to your <U>entire life history</U>, not just your current situation, this is why each question begins - &quot;Have you ever ....&quot;</TD></TR>
  <TR >
    <TD CLASS="port hdrtxt" >
[[[myHTML->setHTML(%form+ClientMHSF)]]]
    </TD>
  </TR>
</TABLE>
<TABLE CLASS="main fullsize" >
  <TR >
    <TD CLASS="numcol" >
      <INPUT TYPE="submit" ONCLICK="return vDELETE('Are you sure you want to delete this record?');" NAME="ClientMHSF_DELETE_1=1&UpdateTables=all&misPOP=1" VALUE="Delete">
      <INPUT TYPE="submit" ONCLICK="return validate(this.form);" NAME="UpdateTables=all&misPOP=1" VALUE="Add/Update">
    </TD>
  </TR>
</TABLE>

</LOADHIDDEN>
</FORM>
<SCRIPT LANGUAGE="JavaScript">
document.ClientMHSF.elements[0].focus();
// just to OPENTABLES...
//<<<ClientMHSF_ClientID_1>>>
</SCRIPT>

[[myHTML->rightpane(%form+search)]]
