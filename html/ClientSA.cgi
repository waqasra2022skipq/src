[[myHTML->newHTML(%form+Substance Abuse+allleft mismenu checkpopupwindow)]]

<SCRIPT LANGUAGE="JavaScript" SRC="/src/cgi/js/vEntry.js"> </SCRIPT>
<SCRIPT LANGUAGE="JavaScript" SRC="/src/cgi/js/vClientSA.js"> </SCRIPT>
<SCRIPT LANGUAGE="JavaScript" SRC="/src/cgi/js/vNum.js"> </SCRIPT>

<FORM NAME="SA" ACTION="/cgi/bin/mis.cgi" METHOD="POST" >
<TABLE CLASS="main fullsize" >
  <TR >
    <TD CLASS="strcol" >
      <<<Client_FName_1>>> <<<Client_MName_1>>> <<<Client_LName_1>>> (<<<Client_ClientID_1>>>) <<<Client_SSN_1>>>
      <BR>
      Substance Abuse Page
    </TD>
    <TD CLASS="numcol" >[[gHTML->setLINKS(%form+back)]]</TD>
  </TR>
</TABLE>
<TABLE CLASS="port fullsize" >
    <TR ><TD ><TABLE CLASS="home fullsize" >
  <TR ><TD CLASS="port hdrtxt" COLSPAN="2" >SUBSTANCE ABUSE</TD></TR>
  <TR ><TD CLASS="hdrtxt" COLSPAN="2" >Tobacco/Nicotine Use</TD></TR></TR>
  <TR >
    <TD CLASS="strcol" COLSPAN="2" >
      How many times per day do you use nicotine?
      <INPUT TYPE="text" NAME="MedHx_DailyTobaccoUse_1" VALUE="<<MedHx_DailyTobaccoUse_1>>" ONFOCUS="select()" MAXLENGTH="2" SIZE="2" >
    </TD">
  </TR>
  <TR ><TD CLASS="port hdrtxt" COLSPAN="2" >TOBACCO SCREEN<BR>(add multiple screenings from the Client Page Testing menu)</TD></TR>
  <TR CLASS="list hdrcol" >
    <TD COLSPAN="2" >
<A HREF="javascript:InputWindow('/cgi/bin/mis.cgi?view=ListClientSATobacco.cgi&Client_ClientID=<<<Client_ClientID_1>>>&mlt=<<<mlt>>>&misLINKS=<<<misLINKS>>>&NONAVIGATION=1','TOBACCO',900,1200)" CLASS="mybutton" >ENTER TOBACCO Screening (add new or edit last screening)</A>
    </TD>
  </TR>
  <TR ><TD CLASS="hdrtxt" COLSPAN="2" >Alcohol Use</TD></TR>
  <TR ><TD CLASS="strcol" COLSPAN="2" ><B>History</B></TD></TR>
  <TR >
    <TD CLASS="strcol" >Have you ever used alcohol?</TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="radio" NAME="MedHx_UsedAlcohol_1" VALUE=1 <<MedHx_UsedAlcohol_1=1>> > Yes
      <INPUT TYPE="radio" NAME="MedHx_UsedAlcohol_1" VALUE=0 <<MedHx_UsedAlcohol_1=0>> > No
      If yes, then <U>Add New</U> below.
    </TD>
  </TR>
  <TR >
    <TD CLASS="strcol" >Have you ever used alcohol to intoxication?</TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="radio" NAME="MedHx_AlcoholIntoxD_1" VALUE=1 <<MedHx_AlcoholIntoxD_1=1>> > Yes
      <INPUT TYPE="radio" NAME="MedHx_AlcoholIntoxD_1" VALUE=0 <<MedHx_AlcoholIntoxD_1=0>> > No
    </TD>
  </TR>
  <TR ><TD CLASS="strcol" COLSPAN="2" ><B>Current</B></TD></TR>
  <TR >
    <TD CLASS="strcol" >
      How many times in the past year have you had 5 (for men) or 4 (for women and all adults older than 65 years) or more drinks in a day? 
    </TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="text" NAME="ClientSAAlcohol_in1day_1" VALUE="<<ClientSAAlcohol_in1day_1>>" ONFOCUS="select()" ONCHANGE="return vNum(this,0,99);" SIZE="2" >
    </TD>
  </TR>
  <TR >
    <TD CLASS="hdrtxt" COLSPAN="2" >AUDIT-C Screening Instrument (score &ge; 4 for men; score &ge; 3 for women)</TD>
  </TR>
  <TR >
    <TD CLASS="strcol" >
      Q1: How often did you have a drink containing alcohol in the past year?
    </TD>
    <TD CLASS="strcol" >
      <SELECT NAME="ClientSAAlcohol_howoften_1" >
        [[DBA->selxTable(%form+xAlcoholOften+<<ClientSAAlcohol_howoften_1>>+ID Descr+1)]]
      </SELECT>
    </TD>
  </TR>
  <TR >
    <TD CLASS="strcol" >
      Q2: How many drinks did you have on a typical day when you were drinking in the past year?
    </TD>
    <TD CLASS="strcol" >
      <SELECT NAME="ClientSAAlcohol_howmany_1" >
        [[DBA->selxTable(%form+xAlcoholMany+<<ClientSAAlcohol_howmany_1>>+ID Descr+1)]]
      </SELECT>
    </TD>
  </TR>
  <TR >
    <TD CLASS="strcol" >
      Q3: How often did you have six or more drinks on one occasion in the past year?
    </TD>
    <TD CLASS="strcol" >
      <SELECT NAME="ClientSAAlcohol_sixormore_1" >
        [[DBA->selxTable(%form+xAlcoholMore+<<ClientSAAlcohol_sixormore_1>>+ID Descr+1)]]
      </SELECT>
    </TD>
  </TR>
  <TR >
    <TD CLASS="strcol" >Have you used alcohol in the last 30 days?</TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="radio" NAME="MedHx_AlcoholUseL_1" VALUE=1 <<MedHx_AlcoholUseL_1=1>> > Yes
      <INPUT TYPE="radio" NAME="MedHx_AlcoholUseL_1" VALUE=0 <<MedHx_AlcoholUseL_1=0>> > No
      If yes, then <U>Add New</U> below.
    </TD>
  </TR>
  <TR >
    <TD CLASS="strcol" >Have you used alcohol to intoxication in the past 30 days?</TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="radio" NAME="MedHx_AlcoholIntoxL_1" VALUE=1 <<MedHx_AlcoholIntoxL_1=1>> > Yes
      <INPUT TYPE="radio" NAME="MedHx_AlcoholIntoxL_1" VALUE=0 <<MedHx_AlcoholIntoxL_1=0>> > No
    </TD>
  </TR>
  <TR >
    <TD CLASS="strcol" >How many times have you had Alcohol DT's</TD>
    <TD CLASS="strcol" ALIGN=left >
      <INPUT TYPE="text" NAME="MedHx_AlcoholDTs_1" VALUE="<<MedHx_AlcoholDTs_1>>" ONFOCUS="select()" ONCHANGE="return vNum(this,0,99);" SIZE="2">
    </TD>
  </TR>
    </TABLE></TD></TR>
    <TR ><TD ><TABLE CLASS="home fullsize" >
  <TR ><TD CLASS="port hdrtxt" COLSPAN="2" >ALCOHOL SCREEN</TD></TR>
  <TR CLASS="list hdrcol" >
    <TD COLSPAN="2" >
[[DBA->isCHILD(%form+<<<Client_DOB_1>>>)      <A HREF="javascript:InputWindow('/cgi/bin/mis.cgi?view=ListCRAFFT.cgi&Client_ClientID=<<<Client_ClientID_1>>>&mlt=<<<mlt>>>&misLINKS=<<<misLINKS>>>&NONAVIGATION=1','CRAFFT',900,1200)" CLASS="mybutton" >ENTER Substance-Related Risks and Problems in Adolescents (CRAFFT)</A> ]]
[[DBA->isADULT(%form+<<<Client_DOB_1>>>)      <A HREF="javascript:InputWindow('/cgi/bin/mis.cgi?view=ListAUDIT.cgi&Client_ClientID=<<<Client_ClientID_1>>>&mlt=<<<mlt>>>&misLINKS=<<<misLINKS>>>&NONAVIGATION=1','AUDIT',900,1200)" CLASS="mybutton" >ENTER AUDIT (Alcohol Use Disorders Identification Test)</A> ]]
    </TD>
  </TR>
    </TABLE></TD></TR>
    <TR ><TD ><TABLE CLASS="home fullsize" >
  <TR ><TD CLASS="port hdrtxt" COLSPAN="2" >DRUG SCREEN</TD></TR>
  <TR >
    <TD CLASS="strcol" >Have you ever abused any drug?</TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="radio" NAME="MedHx_DrugAbuse_1" VALUE=1 <<MedHx_DrugAbuse_1=1>> > Yes
      <INPUT TYPE="radio" NAME="MedHx_DrugAbuse_1" VALUE=0 <<MedHx_DrugAbuse_1=0>> > No
    </TD>
  </TR>
  <TR CLASS="list hdrcol" >
    <TD COLSPAN="2" >
      <A HREF="javascript:InputWindow('/cgi/bin/mis.cgi?view=ListClientASAM.cgi&Client_ClientID=<<<Client_ClientID_1>>>&mlt=<<<mlt>>>&misLINKS=<<<misLINKS>>>&NONAVIGATION=1','ASAML',900,1200)" CLASS="mybutton" >ASAM Testing</A>
    </TD>
  </TR>
  <TR CLASS="list hdrcol" >
    <TD COLSPAN="2" >
      <A HREF="javascript:InputWindow('/cgi/bin/mis.cgi?view=ListODAS.cgi&Client_ClientID=<<<Client_ClientID_1>>>&mlt=<<<mlt>>>&misLINKS=<<<misLINKS>>>&NONAVIGATION=1','ODASL',900,1200)" CLASS="mybutton" >ENTER Oklahoma Determination of ASAM Level</A>
    </TD>
  </TR>
  <TR CLASS="list hdrcol" >
    <TD COLSPAN="2" >
      <A HREF="javascript:InputWindow('/cgi/bin/mis.cgi?view=ListTCUDS.cgi&Client_ClientID=<<<Client_ClientID_1>>>&mlt=<<<mlt>>>&misLINKS=<<<misLINKS>>>&NONAVIGATION=1','TCUDS',900,1200)" CLASS="mybutton" >ENTER TCUDS (TCU Drug Screen V)</A>
    </TD>
  </TR>
  <TR ><TD CLASS="hdrtxt" COLSPAN="2" >Drug Use</TD></TR>
  <TR ><TD CLASS="strcol" COLSPAN="2" >Add all Drug Use History and Current below.</TD></TR>
  <TR ><TD CLASS="strcol" COLSPAN="2" ><B>History</B> [Check substance(s) used and indicate age first used]
  <TR ><TD CLASS="strcol" COLSPAN="2" ><B>Current</B></TD></TR>
  <TR ><TD CLASS="strcol" COLSPAN="2" >Do you currently use and of the following drugs? (for History select 'current no' and for Current select 'current yes' below)</TD></TR>
  <TR ><TD CLASS="port hdrtxt" COLSPAN="2" >
    Tobacco/Nicotine Use, Alcohol Use, and Drug Use (History and Current)</TD>
  </TR>
  <TR >
    <TD COLSPAN="2" >
<SPAN ID="ListClientSA" >
[[myHTML->ListSel(%form+ListClientSA+<<<Client_ClientID>>>+<<<LINKID>>>+<<<Client_Locked_1>>>)]]
</SPAN>
    </TD>
  </TR>
  <TR >
    <TD CLASS="strcol" >Have you ever used any substance by injection (needle)?</TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="radio" NAME="MedHx_DrugInject_1" VALUE=1 <<MedHx_DrugInject_1=1>> > Yes
      <INPUT TYPE="radio" NAME="MedHx_DrugInject_1" VALUE=0 <<MedHx_DrugInject_1=0>> > No
    </TD>
  </TR>
  <TR >
    <TD CLASS="strcol" >How many times have you overdosed on drugs?</TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="text" NAME="MedHx_OD_1" VALUE="<<MedHx_OD_1>>" ONFOCUS="select()" ONCHANGE="return vNum(this,0,99);" SIZE="2">
    </TD>
  </TR>
    </TABLE></TD></TR>
    <TR ><TD ><TABLE CLASS="home fullsize" >
  <TR ><TD CLASS="port hdrtxt" COLSPAN="2" >Treatments</TD></TR>
  <TR ><TD CLASS="strcol" COLSPAN="2" >Have you received any treatment specifically for alcohol abuse?</TD></TR>
  <TR ><TD CLASS="strcol" COLSPAN="2" >Have you received any treatment specifically for drug abuse?</TD></TR>
  <TR><TD CLASS="homesublink" COLSPAN="2" >If yes, then <U>Add New</U> below.</TD></TR>
  <TR >
    <TD COLSPAN="2" >
<SPAN ID="ListClientTreatments" >
[[myHTML->ListSel(%form+ListClientTreatments+<<<Client_ClientID>>>+<<<LINKID>>>+<<<Client_Locked_1>>>)]]
</SPAN>
    </TD>
  </TR>
    </TABLE></TD></TR>
    <TR ><TD ><TABLE CLASS="home fullsize" >
  <TR ><TD CLASS="port hdrtxt" COLSPAN="2" >Family History of Alcohol or Drug Use</TD></TR>
  <TR >
    <TD CLASS="strcol" >Did you experience any prenatal exposure to drugs or alcohol?</TD>
    <TD CLASS="strcol" >
      <SELECT NAME="MedHx_PrenatalExp_1" MULTIPLE SIZE="10" >
        [[DBA->selxTable(%form+xDrugs+<<MedHx_PrenatalExp_1>>+Descr)]]
      </SELECT>
    </TD>
  </TR>
  <TR >
    <TD CLASS="strcol" COLSPAN="2" >
      Have any of your family members had a drinking, drug or psychological problem?</I>
    </TD>
  </TR>
  <TR><TD CLASS="homesublink" COLSPAN="2" >If yes, then <U>Add New</U> below.</TD></TR>
  <TR >
    <TD COLSPAN="2" >
<SPAN ID="ListClientSAFamily" >
[[myHTML->ListSel(%form+ListClientSAFamily+<<<Client_ClientID>>>+<<<LINKID>>>+<<<Client_Locked_1>>>)]]
</SPAN>
    </TD>
  </TR>
  <TR ><TD CLASS="port hdrtxt" >Orientation to Change</TD><TD>&nbsp;</TD></TR>
  <TR ><TD CLASS="strcol" COLSPAN="2" >Describe how alcohol/substance use has resulted in changes in your life:</TD></TR>
  <TR >
    <TD CLASS="strcol" COLSPAN="2" >
      <TEXTAREA NAME="MedHx_ToChange_1" COLS="90" ROWS="8" WRAP="virtual" ><<MedHx_ToChange_1>></TEXTAREA>
    </TD>
  </TR>
    </TABLE></TD></TR>
</TABLE>

<TABLE CLASS="main fullsize" >
  <TR >
    <TD CLASS="numcol" >
      <INPUT TYPE="submit" ONCLICK="return validate(this.form);" NAME="UpdateTables=all&[[myForm->genLink(Gambling+ClientGambling.cgi)]]" VALUE="Add/Update -> Gambling">
      <INPUT TYPE="submit" ONCLICK="return validate(this.form);" NAME="UpdateTables=all&misPOP=1" VALUE="Add/Update">
    </TD>
  </TR>
</TABLE>

</LOADHIDDEN>
</FORM>
<SCRIPT LANGUAGE="JavaScript">
document.SA.elements[0].focus();
</SCRIPT>

[[myHTML->rightpane(%form+search)]]
