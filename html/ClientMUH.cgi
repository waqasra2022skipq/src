[[myHTML->newPage(%form+Client Intake)]]

<SCRIPT type="text/javascript" SRC="/src/cgi/js/ajaxrequest.js"> </SCRIPT>
<SCRIPT LANGUAGE="JavaScript" SRC="/src/cgi/js/novalidate.js"> </SCRIPT>

<FORM NAME="Intake" ACTION="/cgi/bin/mis.cgi" METHOD="POST" >
<TABLE CLASS="main fullsize" >
  <TR >
    <TD CLASS="strcol" >
      <<<Client_FName_1>>> <<<Client_MName_1>>> <<<Client_LName_1>>> (<<<Client_ClientID_1>>>) <<<Client_SSN_1>>>
      <BR>
      Treatment History
    </TD>
    <TD CLASS="numcol" >[[gHTML->setLINKS(%form+back)]]</TD>
  </TR>
</TABLE>
<TABLE CLASS="home fullsize" >
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
<A HREF="javascript:InputWindow('/src/cgi/bin/mis.cgi?view=ListClientSATobacco.cgi&Client_ClientID=<<<Client_ClientID_1>>>&mlt=<<<mlt>>>&misLINKS=<<<misLINKS>>>&NONAVIGATION=1','TOBACCO',900,1200)" CLASS="mybutton" >ENTER TOBACCO Screening (add new or edit last screening)</A>
    </TD>
  </TR>
</TABLE>
<TABLE CLASS="home fullsize" >
  <TR ><TD CLASS="port hdrtxt" COLSPAN="2" >HEALTH INFORMATION</TD></TR>
  <TR ><TD CLASS="port hdrtxt" WIDTH="50%" >Vaccine Information</TD><TD WIDTH="50%" >&nbsp;</TD></TR>
  <TR >
    <TD COLSPAN="2" >
<SPAN ID="ListClientVaccines" >
[[myHTML->ListSel(%form+ListClientVaccines+<<<Client_ClientID>>>+<<<LINKID>>>+<<<Client_Locked_1>>>)]]
</SPAN>
    </TD>
  </TR>
  <TR ><TD CLASS="port hdrtxt" WIDTH="50%" >Vitals Information</TD><TD WIDTH="50%" >&nbsp;</TD></TR>
  <TR >
    <TD COLSPAN="2" >
<SPAN ID="ListClientVitalSigns" >
[[myHTML->ListSel(%form+ListClientVitalSigns+<<<Client_ClientID>>>+<<<LINKID>>>+<<<Client_Locked_1>>>)]]
</SPAN>
    </TD>
  </TR>
  <TR ><TD CLASS="port hdrtxt" WIDTH="50%" >Procedures Information</TD><TD WIDTH="50%" >&nbsp;</TD></TR>
  <TR >
    <TD COLSPAN="2" >
<SPAN ID="ListClientProcedures" >
[[myHTML->ListSel(%form+ListClientProcedures+<<<Client_ClientID>>>+<<<LINKID>>>+<<<Client_Locked_1>>>)]]
</SPAN>
    </TD>
  </TR>
  <TR ><TD CLASS="port hdrtxt" ><A NAME="AdjDis">Handicaps/Disabilities/Limitations/Challenges</TD></TR>
  <TR ><TD CLASS="strcol" COLSPAN="2" >Are you experiencing any chronic medical, ambulatory, speech, hearing or visual functioning problems?</TD></TR>
  <TR>
    <TD CLASS="strcol" >Handicap 1</TD>
    <TD CLASS="strcol" COLSPAN="2" >
      <SELECT NAME="ClientDevl_Handicap1_1" ONCHANGE="callAjax('FunctionalStatus','','selFS1','&name=ClientDevl_FuncStatus1_1&Handicap='+this.value,'popup.pl');" >
        [[DBA->selxTable(%form+xHandicap+<<ClientDevl_Handicap1_1>>+CDC Descr)]]
      </SELECT>
    </TD>
  </TR>
  <TR>
    <TD CLASS="strcol" >Functional Status 1</TD>
    <TD CLASS="strcol" >
      <SPAN ID="selFS1">
      <SELECT NAME="ClientDevl_FuncStatus1_1" >
        [[DBA->selxTable(%form+xFunctionalStatus+<<ClientDevl_FuncStatus1_1>>+ConceptName+++Handicap='<<ClientDevl_Handicap1_1>>')]]
      </SELECT>
      </SPAN>
    </TD>
  </TR>
  <TR>
    <TD CLASS="strcol" >Handicap 2</TD>
    <TD CLASS="strcol" COLSPAN="2" >
      <SELECT NAME="ClientDevl_Handicap2_1" ONCHANGE="callAjax('FunctionalStatus','','selFS2','&name=ClientDevl_FuncStatus2_1&Handicap='+this.value,'popup.pl');" >
        [[DBA->selxTable(%form+xHandicap+<<ClientDevl_Handicap2_1>>+CDC Descr)]]
      </SELECT>
    </TD>
  </TR>
  <TR>
    <TD CLASS="strcol" >Functional Status 2</TD>
    <TD CLASS="strcol" >
      <SPAN ID="selFS2">
      <SELECT NAME="ClientDevl_FuncStatus2_1" >
        [[DBA->selxTable(%form+xFunctionalStatus+<<ClientDevl_FuncStatus2_1>>+ConceptName+++Handicap='<<ClientDevl_Handicap2_1>>')]]
      </SELECT>
      </SPAN>
    </TD>
  </TR>
  <TR>
    <TD CLASS="strcol" >Handicap 3</TD>
    <TD CLASS="strcol" COLSPAN="2" >
      <SELECT NAME="ClientDevl_Handicap3_1" ONCHANGE="callAjax('FunctionalStatus','','selFS3','&name=ClientDevl_FuncStatus3_1&Handicap='+this.value,'popup.pl');" >
        [[DBA->selxTable(%form+xHandicap+<<ClientDevl_Handicap3_1>>+CDC Descr)]]
      </SELECT>
    </TD>
  </TR>
  <TR>
    <TD CLASS="strcol" >Functional Status 3</TD>
    <TD CLASS="strcol" >
      <SPAN ID="selFS3">
      <SELECT NAME="ClientDevl_FuncStatus3_1" >
        [[DBA->selxTable(%form+xFunctionalStatus+<<ClientDevl_FuncStatus3_1>>+ConceptName+++Handicap='<<ClientDevl_Handicap3_1>>')]]
      </SELECT>
      </SPAN>
    </TD>
  </TR>
  <TR>
    <TD CLASS="strcol" >Handicap 4</TD>
    <TD CLASS="strcol" COLSPAN="2" >
      <SELECT NAME="ClientDevl_Handicap4_1" ONCHANGE="callAjax('FunctionalStatus','','selFS4','&name=ClientDevl_FuncStatus4_1&Handicap='+this.value,'popup.pl');" >
        [[DBA->selxTable(%form+xHandicap+<<ClientDevl_Handicap4_1>>+CDC Descr)]]
      </SELECT>
    </TD>
  </TR>
  <TR>
    <TD CLASS="strcol" >Functional Status 4</TD>
    <TD CLASS="strcol" >
      <SPAN ID="selFS4">
      <SELECT NAME="ClientDevl_FuncStatus4_1" >
        [[DBA->selxTable(%form+xFunctionalStatus+<<ClientDevl_FuncStatus4_1>>+ConceptName+++Handicap='<<ClientDevl_Handicap4_1>>')]]
      </SELECT>
      </SPAN>
    </TD>
  </TR>
  <TR ><TD CLASS="strcol" COLSPAN="2" >Client's adjustment to disabilities or disorders?</TD></TR>
  <TR >
    <TD CLASS="strcol" COLSPAN="2" >
      <TEXTAREA NAME="MedHx_AdjDis_1" COLS="90" ROWS="2" WRAP=virtual ><<MedHx_AdjDis_1>></TEXTAREA>
    </TD>
  </TR>
</TABLE>
<TABLE CLASS="main fullsize" >
  <TR >
    <TD CLASS="numcol" >
      <INPUT TYPE=submit ONCLICK="return validate(this.form);" NAME="[[myForm->genLink(ClientMeds+ClientMUT.cgi)]]" VALUE="Client MEDICATIONS &amp; LABS Information">
      <INPUT TYPE="submit" ONCLICK="return validate(this.form);" NAME="UpdateTables=all&misPOP=1" VALUE="Add/Update" >
    </TD>
  </TR>
</TABLE>

<INPUT TYPE="hidden" NAME="ProviderID" VALUE="<<ProviderID>>" >
</LOADHIDDEN>
</FORM>
<SCRIPT LANGUAGE="JavaScript">
document.Intake.elements[0].focus();
</SCRIPT>

[[myHTML->rightpane(%form+search)]]
