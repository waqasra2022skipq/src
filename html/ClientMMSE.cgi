[[myHTML->newHTML(%form+Mental Health History+allleft mismenu checkpopupwindow)]]

<SCRIPT LANGUAGE="JavaScript" SRC="/cgi/js/vEntry.js"> </SCRIPT>
<SCRIPT LANGUAGE="JavaScript" SRC="/cgi/js/vClientMMSE.js"> </SCRIPT>
<SCRIPT LANGUAGE="JavaScript" SRC="/cgi/js/vNum.js"> </SCRIPT>
<SCRIPT LANGUAGE="JavaScript" SRC="/cgi/js/qDate.js"> </SCRIPT>

<FORM NAME="MH" ACTION="/cgi/bin/mis.cgi" METHOD="POST" >
<TABLE CLASS="main fullsize" >
  <TR >
    <TD CLASS="strcol" >
      <<<Client_FName_1>>> <<<Client_MName_1>>> <<<Client_LName_1>>> (<<<Client_ClientID_1>>>) <<<Client_SSN_1>>>
      <BR>
      MMSE
    </TD>
    <TD CLASS="numcol" >[[gHTML->setLINKS(%form+back)]]</TD>
  </TR>
</TABLE>
<TABLE CLASS="port fullsize" >
    <TR ><TD ><TABLE CLASS="home fullsize" >
  <TR ><TD CLASS="port hdrtxt" >Mini-Mental State Examination (MMSE)</TD></TR>
  <TR ><TD CLASS="port hdrtxt" COLSPAN="2" >Mini-Mental State Examination (MMSE) Form<BR>(add multiple screenings from the Client Page Testing menu)</TD></TR>
  <TR CLASS="list hdrcol" >
    <TD COLSPAN="2" >
<A HREF="javascript:InputWindow('/cgi/bin/mis.cgi?view=ListClientMMSF.cgi&Client_ClientID=<<<Client_ClientID_1>>>&mlt=<<<mlt>>>&misLINKS=<<<misLINKS>>>&NONAVIGATION=1','MMSE',900,1200)" ><BUTTON TYPE="button" >ENTER Mini-Mental State Examination</BUTTON></A>
    </TD>
  </TR>
  <TR ><TD CLASS="strcol" >How many times have you been treated for any psychological or emotional problems:</TD></TR>
  <TR ><TD CLASS="strcol" >If YES, then <U>Add New</U> below.</TD></TR>
  <TR >
    <TD >
<SPAN ID="ListClientTreatments" >
[[myHTML->ListSel(%form+ListClientTreatments+<<<Client_ClientID>>>+<<<LINKID>>>+<<<Client_Locked_1>>>)]]
</SPAN>
    </TD>
  </TR>
    </TABLE></TD></TR>
    <TR ><TD ><TABLE CLASS="home fullsize" >
  <TR >
    <TD CLASS="strcol" >
      How many suicide attempts?
      <INPUT TYPE=text NAME="MedHx_AttSuicides_1" VALUE="<<MedHx_AttSuicides_1>>" ONFOCUS="select()" ONCHANGE="return vNum(this,0,99);" SIZE="2" >
    </TD>
    <TD CLASS="strcol" >
      Date of last attempt?
      <INPUT TYPE=text NAME="MedHx_AttSuicideDate_1" VALUE="<<MedHx_AttSuicideDate_1>>" ONFOCUS="select()" ONCHANGE="qDate(this)" MAXLENGTH="10" SIZE="10" >
    </TD>
    <TD CLASS="strcol" >  
	  <A HREF="javascript:ReportWindow('/cgi/bin/mis.cgi?view=ListCSSRS.cgi&Client_ClientID=<<Client_ClientID>>&mlt=<<mlt>>&misLINKS=<<misLINKS>>','C-SSRS',700, 1200)"><B><I>Complete Columbia Suicide Scale (C-SSRS)</I></B></A>
    </TD>
  </TR>
  <TR >
    <TD CLASS="strcol" >
      Is there a family history of suicide?
      <INPUT TYPE=radio NAME="MedHx_FamilySuicideHx_1" VALUE=1 <<MedHx_FamilySuicideHx_1=1>> > yes
      <INPUT TYPE=radio NAME="MedHx_FamilySuicideHx_1" VALUE=0 <<MedHx_FamilySuicideHx_1=0>> > no
    </TD>
    <TD CLASS="strcol" COLSPAN="2" >
      Are there firearms in the home?
      <INPUT TYPE=radio NAME="MedHx_Firearms_1" VALUE=1 <<MedHx_Firearms_1=1>> > yes
      <INPUT TYPE=radio NAME="MedHx_Firearms_1" VALUE=0 <<MedHx_Firearms_1=0>> > no
    </TD>
  </TR>
  <TR >
    <TD CLASS="strcol" >In the past 90 days, on how many days did an incident of self-harm occur?</TD>
    <TD CLASS="strcol" COLSPAN="2" >
      <INPUT TYPE=text NAME="MedHx_SelfHarm_1" VALUE="<<MedHx_SelfHarm_1>>" ONFOCUS="select()" ONCHANGE="return vNum(this,0,90);" SIZE=2>
    </TD>
  </TR>
    </TABLE></TD></TR>
</TABLE>
<TABLE CLASS="main fullsize" >
  <TR >
    <TD CLASS="numcol" >
      <INPUT TYPE=submit ONCLICK="return validate(this.form);" NAME="UpdateTables=all&[[myForm->genLink(ClientIntake+ClientSA.cgi)]]" VALUE="Add/Update -> Substance Abuse" >
      <INPUT TYPE=submit ONCLICK="return validate(this.form);" NAME="UpdateTables=all&misPOP=1" VALUE="Add/Update" >
    </TD>
  </TR>
</TABLE>

<INPUT TYPE="hidden" NAME="post_update" VALUE="PostUpd->updPA(%form+<<<Client_ClientID_1>>>)" >
</LOADHIDDEN>
</FORM>
<SCRIPT LANGUAGE="JavaScript" >
document.MH.elements[0].focus();
</SCRIPT>

[[myHTML->rightpane(%form+search)]]
