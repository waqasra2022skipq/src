[[myHTML->newPage(%form+Family)]]

<SCRIPT LANGUAGE="JavaScript" SRC="/src/cgi/js/NoEnter.js"> </SCRIPT>
<SCRIPT LANGUAGE="JavaScript" SRC="/src/cgi/js/vEntry.js"> </SCRIPT>
<SCRIPT LANGUAGE="JavaScript" SRC="/src/cgi/js/vClientFamily.js"> </SCRIPT>
<SCRIPT LANGUAGE="JavaScript" SRC="/src/cgi/js/vNum.js"> </SCRIPT>
<SCRIPT LANGUAGE="JavaScript" SRC="/src/cgi/js/vDate.js"> </SCRIPT>

<FORM NAME="ClientFamily" ACTION="/cgi/bin/mis.cgi" METHOD="POST" >
<TABLE CLASS="main fullsize" >
  <TR >
    <TD CLASS="strcol" >
      <<<Client_FName_1>>> <<<Client_MName_1>>> <<<Client_LName_1>>> (<<<Client_ClientID_1>>>) <<<Client_SSN_1>>>
      <BR>Family Substance Abuse View/Edit Page
    </TD>
    <TD CLASS="numcol" >[[gHTML->setLINKS(%form+back)]]</TD>
  </TR>
</TABLE>
<TABLE CLASS="home fullsize" >
  <TR ><TD CLASS="port hdrtxt" COLSPAN="2" >FAMILY MEMBER<BR>for domestic violence information</TD></TR>
  <TR >
    <TD CLASS="strcol" >First Name</TD>
    <TD CLASS="strcol" >
      <INPUT TYPE=text NAME="ClientFamily_FName_1" VALUE="<<ClientFamily_FName_1>>" ONFOCUS="select()" SIZE=20>
    </TD>
  </TR>
  <TR >
    <TD CLASS="strcol" >Last Name</TD>
    <TD CLASS="strcol" >
      <INPUT TYPE=text NAME="ClientFamily_LName_1" VALUE="<<ClientFamily_LName_1>>" ONFOCUS="select()" SIZE=20>
    </TD>
  </TR>
  <TR >
    <TD CLASS="strcol" >Relationship</TD>
    <TD CLASS="strcol" >
      <SELECT NAME="ClientFamily_Rel_1">
        [[DBA->selxTable(%form+xRelationship+<<ClientFamily_Rel_1>>+Descr)]]
      </SELECT>
    </TD>
  </TR>
  <TR >
    <TD CLASS="strcol" >Date of Birth</TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="TEXT" NAME="ClientFamily_DOB_1" VALUE="<<ClientFamily_DOB_1>>" ONFOCUS="select()" ONCHANGE="return vDate(this,0,this.form,'ClientFamily_Age_1')" SIZE="10" >
      Age:
      <INPUT TYPE=text NAME="ClientFamily_Age_1" VALUE="<<ClientFamily_Age_1>>" ONCHANGE="return vNum(this,1,99)" ONFOCUS="select()" >
  </TR>
  <TR ><TD CLASS="strcol" COLSPAN="2" >Indicate from view of client:  If person abused client indicate Perpetrator; If client abused person indicate Victim.  If both, check both.</TD></TR>
  <TR >
    <TD CLASS="strcol" >Emotional Abuse</TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="radio" NAME="ClientFamily_AbuseEmotion_1" VALUE=V <<ClientFamily_AbuseEmotion_1=V>> > victim
      <INPUT TYPE="radio" NAME="ClientFamily_AbuseEmotion_1" VALUE=P <<ClientFamily_AbuseEmotion_1=P>> > perpetrator
      <INPUT TYPE="radio" NAME="ClientFamily_AbuseEmotion_1" VALUE=B <<ClientFamily_AbuseEmotion_1=B>> > both
      <INPUT TYPE="radio" NAME="ClientFamily_AbuseEmotion_1" VALUE=N <<ClientFamily_AbuseEmotion_1=N>> > none
    </TD>
  </TR>
  <TR >
    <TD CLASS="strcol" >Physical Abuse</TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="radio" NAME="ClientFamily_AbusePhysical_1" VALUE=V <<ClientFamily_AbusePhysical_1=V>> > victim
      <INPUT TYPE="radio" NAME="ClientFamily_AbusePhysical_1" VALUE=P <<ClientFamily_AbusePhysical_1=P>> > perpetrator
      <INPUT TYPE="radio" NAME="ClientFamily_AbusePhysical_1" VALUE=B <<ClientFamily_AbusePhysical_1=B>> > both
      <INPUT TYPE="radio" NAME="ClientFamily_AbusePhysical_1" VALUE=N <<ClientFamily_AbusePhysical_1=N>> > none
    </TD>
  </TR>
  <TR >
    <TD CLASS="strcol" >Sexual Abuse</TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="radio" NAME="ClientFamily_AbuseSexual_1" VALUE=V <<ClientFamily_AbuseSexual_1=V>> > victim
      <INPUT TYPE="radio" NAME="ClientFamily_AbuseSexual_1" VALUE=P <<ClientFamily_AbuseSexual_1=P>> > perpetrator
      <INPUT TYPE="radio" NAME="ClientFamily_AbuseSexual_1" VALUE=B <<ClientFamily_AbuseSexual_1=B>> > both
      <INPUT TYPE="radio" NAME="ClientFamily_AbuseSexual_1" VALUE=N <<ClientFamily_AbuseSexual_1=N>> > none
    </TD>
  </TR>
</TABLE>
<TABLE CLASS="main fullsize" >
  <TR >
    <TD CLASS="numcol" >
      <INPUT TYPE="submit" ONCLICK="return vDELETE('Are you sure you want to delete this Family member? It will delete all associations for SA,DV,Relations');" NAME="ClientFamily_DELETE_1=1&UpdateTables=all&misPOP=1" VALUE="Delete">
      <INPUT TYPE="submit" ONCLICK="return validate(this.form);" NAME="UpdateTables=all&misPOP=1" VALUE="Add/Update">
    </TD>
  </TR>
</TABLE>

</LOADHIDDEN>
</FORM>
<SCRIPT LANGUAGE="JavaScript">
document.ClientFamily.elements[0].focus();
</SCRIPT>

[[myHTML->rightpane(%form+search)]]
