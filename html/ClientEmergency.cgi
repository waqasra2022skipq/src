[[myHTML->newPage(%form+Client Emergency+++++lhcautocomplete)]]

<SCRIPT LANGUAGE="JavaScript" SRC="/src/cgi/js/vEntry.js"> </SCRIPT>
<SCRIPT LANGUAGE="JavaScript" SRC="/src/cgi/js/vClientEmergency.js"> </SCRIPT>
<SCRIPT type="text/javascript" src="/src/cgi/js/ajaxrequest.js"></SCRIPT>
<SCRIPT TYPE="text/javascript" SRC="/cgi/jquery/jquery-1.12.4.js" ></SCRIPT>
<SCRIPT TYPE="text/javascript" src="https://ajax.googleapis.com/ajax/libs/jquery/3.3.1/jquery.min.js"></SCRIPT>
<script src="https://lhcforms-static.nlm.nih.gov/autocomplete-lhc-versions/17.0.3/autocomplete-lhc.min.js"></script>
<SCRIPT TYPE="text/javascript" SRC="/cgi/jquery/jquery-ui-1.12.1/jquery-ui.min.js" ></SCRIPT>

[[[DBA->setAddress(%form+Physician)]]]
[[[DBA->setAddress(%form+Hospital)]]]
[[[DBA->setAddress(%form+Pharmacy)]]]
[[[DBA->setAddress(%form+Dentist)]]]
[[[DBA->setAddress(%form+Vision)]]]
[[[DBA->setAddress(%form+Hearing)]]]

<FORM NAME="ClientEmergency" ACTION="/cgi/bin/mis.cgi" METHOD="POST" >
<TABLE CLASS="main fullsize" >
  <TR >
    <TD CLASS="strcol" >
      <<<Client_FName_1>>> <<<Client_MName_1>>> <<<Client_LName_1>>> (<<<Client_ClientID_1>>>) <<<Client_SSN_1>>>
      <BR>
      Client Emergency/Parent/Guardian Page
    </TD>
    <TD CLASS="numcol" >[[gHTML->setLINKS(%form+back)]]</TD>
  </TR>
</TABLE>
<TABLE CLASS="port fullsize" >
    <TR ><TD ><TABLE CLASS="home fullsize" >
  <TR ><TD CLASS="port hdrtxt" >check Guardian if client is under 18 <U>or</U> under legal guardianship</TD></TR>
  <TR >
    <TD >
<SPAN ID="ListClientFamily" >
[[myHTML->ListSel(%form+ListClientFamily+<<<Client_ClientID>>>+<<<LINKID>>>+<<<Client_Locked_1>>>)]]
</SPAN>
    </TD>
  </TR>
    </TABLE></TD></TR>
</TABLE>
<TABLE CLASS="home fullsize" >
    <TR ><TD ><TABLE CLASS="home fullsize" >
  <TR ><TD CLASS="port hdrtxt" COLSPAN="2" >Health Care Information and Resources</TD></TR>
  <TR>
    <TD CLASS="strcol" >Opt-Out of MyHealth</TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="radio" NAME="ClientEmergency_MyHealth_1" VALUE=0 <<ClientEmergency_MyHealth_1=0>> > no
      <INPUT TYPE="radio" NAME="ClientEmergency_MyHealth_1" VALUE=1 <<ClientEmergency_MyHealth_1=1>> > yes
      <BR>
      <A HREF="javascript:ReportWindow('http://forms.okmis.com/misdocs/MyHealth/MyHealthOptOutForm_English.pdf','HelpWindow')" >MyHealth Access Network Opt-Out Request Form</A>
      <BR>
      <A HREF="javascript:ReportWindow('http://forms.okmis.com/misdocs/MyHealth/MyHealthOptInForm_English.pdf','HelpWindow')" >MyHealth Access Network Opt-In Request Form</A>
      <BR>
      Fax: 918-236-3435
    </TD>
  </TR>
  <TR>
    <TD CLASS="strcol" >
      Alert
      <A HREF="javascript:ReportWindow('http://okmis.helpdocsonline.com/alertinformationfield','HelpAlert')" TITLE="Click here for Examples of the information needed in the <U>Alert Information</U> field." >
        <IMG SRC="/images/qm1.gif" ALT="" BORDER="0" HEIGHT="20" WIDTH="20" >
      </A>
    </TD>
    <TD CLASS="strcol" >
      <TEXTAREA NAME="ClientEmergency_Alert_1" COLS="80" ROWS="5" WRAP="virtual" ><<ClientEmergency_Alert_1>></TEXTAREA>
      <BR><FONT COLOR="red" >Enter Alert description ONLY if applicable.</FONT>
    </TD>
  </TR>
  <TR >
    <TD CLASS="strcol" >Primary Care Physician</TD>
    <TD CLASS="strcol" >
      Search: <INPUT TYPE="text" class="search_field" ID="SearchPhysNPI" NAME="SearchPhysNPI" VALUE="" ONFOCUS="select()" SIZE="60" >
        <INPUT TYPE="hidden" ID="ClientEmergency_PhysNPI_1" NAME="ClientEmergency_PhysNPI_1" VALUE="<<ClientEmergency_PhysNPI_1>>" >
    </TD>
  </TR>
  <TR >
    <TD CLASS="strcol" >&nbsp;</TD>
    <TD CLASS="strcol" ><<<PhysAddr>>></TD>
  </TR>
  <TR >
    <TD CLASS="strcol" >&nbsp;</TD>
    <TD CLASS="strcol" ><<<PhysCSZ>>></TD>
  </TR>
  <TR >
    <TD CLASS="strcol" >&nbsp;</TD>
    <TD CLASS="strcol" ><<<PhysPh>>></TD>
  </TR>
  <TR >
    <TD CLASS="strcol" >&nbsp;</TD>
    <TD CLASS="strcol" ><<<PhysFax>>></TD>
  </TR>
  <TR >
    <TD CLASS="strcol" >Designated Hospital</TD>
    <TD CLASS="strcol" >
      Search: <INPUT TYPE="text" class="search_field" ID="SearchHosp" NAME="SearchHosp" VALUE="" ONFOCUS="select()" SIZE="60" >
        <INPUT TYPE="hidden" ID="ClientEmergency_DesigHospNPI_1" NAME="ClientEmergency_DesigHospNPI_1" VALUE="<<ClientEmergency_DesigHospNPI_1>>" >
    </TD>
  </TR>
  <TR >
    <TD CLASS="strcol" >&nbsp;</TD>
    <TD CLASS="strcol" ><<<HospAddr>>></TD>
  </TR>
  <TR >
    <TD CLASS="strcol" >&nbsp;</TD>
    <TD CLASS="strcol" ><<<HospCSZ>>></TD>
  </TR>
  <TR >
    <TD CLASS="strcol" >&nbsp;</TD>
    <TD CLASS="strcol" ><<<HospPh>>></TD>
  </TR>
  <TR >
    <TD CLASS="strcol" >
     <A HREF="javascript:ReportWindow('/src/cgi/bin/PrintPharmacyEnroll.cgi?IDs=<<<Client_ClientID_1>>>&mlt=<<<mlt>>>&misLINKS=<<<misLINKS>>>','PrintPharmacyEnroll')" ONMOUSEOVER="window.status='Print Pharmacy Enrollment Form'; return true;" ONMOUSEOUT="window.status=''"><IMG SRC="/images/icon_print.gif" ALT="" BORDER="0" >Print Enrollment Form</A>
    </TD>
    <TD CLASS="strcol" >ie: wal-mart (or you may enter partial zipcode)</TD>
  </TR>
  <TR >
    <TD CLASS="strcol" >Designated Pharmacy</TD>
    <TD CLASS="strcol" >
      Search: <INPUT TYPE="text" class="search_field" ID="SearchPharmacy" NAME="SearchPharmacy" VALUE="" ONFOCUS="select()" SIZE="60" >
        <INPUT TYPE="hidden" ID="ClientEmergency_PharmacyNPI_1" NAME="ClientEmergency_PharmacyNPI_1" VALUE="<<ClientEmergency_PharmacyNPI_1>>" >
    </TD>
  </TR>
  <TR >
    <TD CLASS="strcol" >&nbsp;</TD>
    <TD CLASS="strcol" ><<<PharmacyAddr>>></TD>
  </TR>
  <TR >
    <TD CLASS="strcol" >&nbsp;</TD>
    <TD CLASS="strcol" ><<<PharmacyCSZ>>></TD>
  </TR>
  <TR >
    <TD CLASS="strcol" >&nbsp;</TD>
    <TD CLASS="strcol" ><<<PharmacyPh>>></TD>
  </TR>
  <TR >
    <TD CLASS="strcol" >Designated Dentist</TD>
    <TD CLASS="strcol" >
      Search: <INPUT TYPE="text" class="search_field" ID="SearchDentist" NAME="SearchDentist" VALUE="" ONFOCUS="select()" SIZE="60" >
        <INPUT TYPE="hidden" ID="ClientEmergency_DentistNPI_1" NAME="ClientEmergency_DentistNPI_1" VALUE="<<ClientEmergency_DentistNPI_1>>" >

    </TD>
  </TR>
  <TR >
    <TD CLASS="strcol" >&nbsp;</TD>
    <TD CLASS="strcol" ><<<DentistAddr>>></TD>
  </TR>
  <TR >
    <TD CLASS="strcol" >&nbsp;</TD>
    <TD CLASS="strcol" ><<<DentistCSZ>>></TD>
  </TR>
  <TR >
    <TD CLASS="strcol" >&nbsp;</TD>
    <TD CLASS="strcol" ><<<DentistPh>>></TD>
  </TR>
  <TR >
    <TD CLASS="strcol" >Designated Vision</TD>
    <TD CLASS="strcol" >
      Search: <INPUT TYPE="text" ID="SearchVision" NAME="SearchVision" VALUE="" ONFOCUS="select()" SIZE="60" >
        <INPUT TYPE="hidden" ID="ClientEmergency_VisionNPI_1" NAME="ClientEmergency_VisionNPI_1" VALUE="<<ClientEmergency_VisionNPI_1>>" >

    </TD>
  </TR>
  <TR >
    <TD CLASS="strcol" >&nbsp;</TD>
    <TD CLASS="strcol" ><<<VisionAddr>>></TD>
  </TR>
  <TR >
    <TD CLASS="strcol" >&nbsp;</TD>
    <TD CLASS="strcol" ><<<VisionCSZ>>></TD>
  </TR>
  <TR >
    <TD CLASS="strcol" >&nbsp;</TD>
    <TD CLASS="strcol" ><<<VisionPh>>></TD>
  </TR>
  <TR >
    <TD CLASS="strcol" >Designated Hearing</TD>
    <TD CLASS="strcol" >
      Search: <INPUT TYPE="text" ID="SearchHearing" NAME="SearchHearing" VALUE="" ONFOCUS="select()" SIZE="60" >
        <INPUT TYPE="hidden" ID="ClientEmergency_HearingNPI_1" NAME="ClientEmergency_HearingNPI_1" VALUE="<<ClientEmergency_HearingNPI_1>>" >

    </TD>
  </TR>
  <TR >
    <TD CLASS="strcol" >&nbsp;</TD>
    <TD CLASS="strcol" ><<<HearingAddr>>></TD>
  </TR>
  <TR >
    <TD CLASS="strcol" >&nbsp;</TD>
    <TD CLASS="strcol" ><<<HearingCSZ>>></TD>
  </TR>
  <TR >
    <TD CLASS="strcol" >&nbsp;</TD>
    <TD CLASS="strcol" ><<<HearingPh>>></TD>
  </TR>
  <TR >
    <TD CLASS="strcol" COLSPAN="2" >HealthVault/Direct Email:
      <INPUT TYPE="EMAIL" NAME="ClientEmergency_HealthVault_1" VALUE="<<ClientEmergency_HealthVault_1>>" ONFOCUS="select()" SIZE="30" >
    </TD>
  </TR>
    </TABLE></TD></TR>
    <TR ><TD ><TABLE CLASS="home fullsize" >
  <TR ><TD CLASS="port hdrtxt" COLSPAN="2" >Medical / Legal Documents on file</TD></TR>
  <TR ><TD CLASS="strcol" COLSPAN="2" >Does patient have on file?</TD></TR>
  <TR>
    <TD CLASS="strcol" >&nbsp;&nbsp;&nbsp;&nbsp;Do Not Resuscitate</TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="radio" NAME="ClientEmergency_DNR_1" VALUE=1 <<ClientEmergency_DNR_1=1>> > yes
      <INPUT TYPE="radio" NAME="ClientEmergency_DNR_1" VALUE=0 <<ClientEmergency_DNR_1=0>> > no
    </TD>
  </TR>
  <TR>
    <TD CLASS="strcol" >&nbsp;&nbsp;&nbsp;&nbsp;Mental Health Advanced Directive</TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="radio" NAME="ClientEmergency_AD_1" VALUE=1 <<ClientEmergency_AD_1=1>> > yes
      <INPUT TYPE="radio" NAME="ClientEmergency_AD_1" VALUE=0 <<ClientEmergency_AD_1=0>> > no
    </TD>
  </TR>
  <TR>
    <TD CLASS="strcol" >&nbsp;&nbsp;&nbsp;&nbsp;Living Will</TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="radio" NAME="ClientEmergency_LW_1" VALUE=1 <<ClientEmergency_LW_1=1>> > yes
      <INPUT TYPE="radio" NAME="ClientEmergency_LW_1" VALUE=0 <<ClientEmergency_LW_1=0>> > no
    </TD>
  </TR>
    </TABLE></TD></TR>
</TABLE>

<TABLE CLASS="main fullsize" >
  <TR >
    <TD CLASS="numcol" >
      <INPUT TYPE="submit" ONCLICK="return validate(this.form);" NAME="UpdateTables=all&[[myForm->genLink(ClientIntake+ClientMHProblems.cgi)]]" VALUE="Add/Update -> Problems">
      <INPUT TYPE="submit" ONCLICK="return validate(this.form);" NAME="UpdateTables=all&misPOP=1" VALUE="Add/Update">
    </TD>
  </TR>
</TABLE>

</LOADHIDDEN>
</FORM>
<SCRIPT LANGUAGE="JavaScript">
document.ClientEmergency.elements[0].focus();
</SCRIPT>

[[myHTML->rightpane(%form+search)]]

<SCRIPT LANGUAGE="JavaScript" SRC="/src/cgi/js/clinicalTable.js"> </SCRIPT>