[[myHTML->newPage(%form+Family Relations)]]

<SCRIPT LANGUAGE="JavaScript" SRC="/src/cgi/js/vEntry.js"> </SCRIPT>
<SCRIPT LANGUAGE="JavaScript" SRC="/src/cgi/js/vClientFamilyRel.js"> </SCRIPT>
<SCRIPT type="text/javascript" src="/src/cgi/js/ajaxrequest.js"></SCRIPT>
<SCRIPT LANGUAGE="JavaScript" SRC="/src/cgi/js/vZip.js"> </SCRIPT>
<SCRIPT LANGUAGE="JavaScript" SRC="/src/cgi/js/vNum.js"> </SCRIPT>
<SCRIPT LANGUAGE="JavaScript" SRC="/src/cgi/js/vDate.js"> </SCRIPT>
<SCRIPT LANGUAGE="JavaScript" >
var PopupWindowObj="";
function uspsWindow(newName,h,w)
{
  if (h==undefined) { h = '700'; }
  if (w==undefined) { w = '1000'; }
  var ws = "HEIGHT=" + h + ",WIDTH=" + w + ",SCROLLBARS=yes";
  newURL="/cgi/bin/usps.pl?mlt=<<mlt>>&Tag=Address&Addr1="+document.ClientFamily.GuardianHistory_Addr1_1.value+"&Addr2="+document.ClientFamily.GuardianHistory_Addr2_1.value+"&City="+document.ClientFamily.GuardianHistory_City_1.value+"&State="+document.ClientFamily.GuardianHistory_ST_1.value+"&Zip="+document.ClientFamily.GuardianHistory_Zip_1.value;
  PopupWindowObj = window.open(newURL,newName,ws);
  PopupWindowObj.focus();
}
</SCRIPT>

<FORM NAME="ClientFamily" ACTION="/cgi/bin/mis.cgi" METHOD="POST" >
<TABLE CLASS="main fullsize" >
  <TR >
    <TD CLASS="strcol" >
      <<<Client_FName_1>>> <<<Client_MName_1>>> <<<Client_LName_1>>> (<<<Client_ClientID_1>>>) <<<Client_SSN_1>>>
      <BR>
      Family Relationships Page
    </TD>
    <TD CLASS="numcol" >[[gHTML->setLINKS(%form+back)]]</TD>
  </TR>
</TABLE>
<TABLE CLASS="port fullsize" >
    <TR ><TD ><TABLE CLASS="home fullsize" >
  <TR ><TD CLASS="port hdrtxt" COLSPAN="2" >FAMILY HISTORY</TD></TR>
  <TR ><TD CLASS="port hdrtxt" COLSPAN="2" >Marital/Significant Other Relationship History</TD></TR>
  <TR >
    <TD CLASS="strcol" >Status</TD>
    <TD CLASS="strcol" >
      <SELECT NAME="ClientRelations_MarStat_1" >
        [[DBA->selxTable(%form+xMarStat+<<ClientRelations_MarStat_1>>+Descr Text)]]
      </SELECT>
    </TD>
  </TR>
  <TR >
    <TD CLASS="strcol" >How long have you been in this marital status?</TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="text" NAME="ClientRelations_MarStatY_1" VALUE="<<ClientRelations_MarStatY_1>>" ONFOCUS="select()" ONCHANGE="return vNum(this,0,99);" SIZE="2" > Years
      <INPUT TYPE="text" NAME="ClientRelations_MarStatM_1" VALUE="<<ClientRelations_MarStatM_1>>" ONFOCUS="select()" ONCHANGE="return vNum(this,0,12);" SIZE="2" > Months
    </TD>
  </TR>
  <TR >
    <TD CLASS="strcol" >Number of times married</TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="text" NAME="ClientRelations_MarStatTimes_1" VALUE="<<ClientRelations_MarStatTimes_1>>" ONFOCUS="select()" ONCHANGE="return vNum(this,0,10);" SIZE="5" >
    </TD>
  </TR>
  <TR >
    <TD CLASS="strcol" COLSPAN="2" >Relationships History (Narrative of relationships history, separations, divorce, affairs, sex partners, functional level of current relationship):</TD>
  </TR>
  <TR >
    <TD CLASS="strcol" COLSPAN="2" >
      <TEXTAREA NAME="ClientRelations_RelHistory_1" COLS="90" ROWS="5" WRAP="virtual" ><<ClientRelations_RelHistory_1>></TEXTAREA>
    </TD>
  </TR>
  <TR ><TD CLASS="strcol" >Significant Other's Name: <I>[Enter in Family List - Emergency Contact]</I></TD></TR>
  <TR >
    <TD COLSPAN="2" >
<SPAN ID="ListClientFamily" >
[[myHTML->ListSel(%form+ListClientFamily+<<<Client_ClientID>>>+<<<LINKID>>>+<<<Client_Locked_1>>>)]]
</SPAN>
    </TD>
  </TR>
    </TABLE></TD></TR>
    <TR ><TD ><TABLE CLASS="home fullsize" >
  <TR ><TD CLASS="port hdrtxt" COLSPAN="2" >Family Relationship</TD></TR>
  <TR >
    <TD CLASS="strcol" >Structure of family you live with?</TD>
    <TD CLASS="strcol" >
      <SELECT NAME="ClientRelations_LivesWith_1" >
        [[DBA->selxTable(%form+xLivesWith+<<ClientRelations_LivesWith_1>>+APS Descr)]]
      </SELECT>
    </TD>
  </TR>
  <TR >
    <TD CLASS="strcol" >Description</TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="text" NAME="ClientRelations_LivesWithDesc_1" VALUE="<<ClientRelations_LivesWithDesc_1>>" MAXLENGTH="50" SIZE="50" >
    </TD>
  </TR>
  <TR >
    <TD CLASS="strcol" >Parents Status</TD>
    <TD CLASS="strcol" >
      <SELECT NAME="ClientRelations_ParStat_1" >
        [[DBA->selxTable(%form+xParentsStatus+<<ClientRelations_ParStat_1>>+Descr)]]
      </SELECT>
    </TD>
  </TR>
  <TR><TD CLASS="strcol" COLSPAN="2" >While growing up, have you (or did you) live under the care of anyone other than your parents?</TD></TR>
  <TR >
    <TD CLASS="strcol" >Guardian Relationship</TD>
    <TD CLASS="strcol" >
      <SELECT NAME="GuardianHistory_ClientRel_1" >
        [[DBA->selxTable(%form+xRelationship+<<GuardianHistory_ClientRel_1>>+Descr)]]
      </SELECT>
    </TD>
  </TR>
    <TD CLASS="strcol" >How Long?</TD>
    <TD CLASS="strcol" >
       <INPUT TYPE="text" NAME="GuardianHistory_GrdnComments_1" VALUE="<<GuardianHistory_GrdnComments_1>>" SIZE="20" >
    </TD>
  </TR>
  <TR><TD CLASS="strcol" COLSPAN="2" >If yes, with whom?</TD></TR>
  <TR >
    <TD CLASS="homesublink" >Last Name</TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="text" NAME="GuardianHistory_LName_1" VALUE="<<GuardianHistory_LName_1>>" onFocus="select()" SIZE="20" >
    </TD>
  </TR>
    <TD CLASS="homesublink" >First Name</TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="text" NAME="GuardianHistory_FName_1" VALUE="<<GuardianHistory_FName_1>>" onFocus="select()" SIZE="20" >
    </TD>
  </TR>
    <TD CLASS="homesublink" >Middle</TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="text" NAME="GuardianHistory_MName_1" VALUE="<<GuardianHistory_MName_1>>" onFocus="select()" SIZE="10" >
    </TD>
  </TR>
  <TR >
    <TD CLASS="strcol" >Suffix</TD>
    <TD CLASS="strcol" >
      <SELECT NAME="GuardianHistory_Suffix_1">
        [[DBA->selxTable(%form+xSuffix+<<GuardianHistory_Suffix_1>>+Descr)]]
      </SELECT>
    </TD>
  </TR>
  <TR >
    <TD CLASS="homesublink" >Address 1</TD>
    <TD CLASS="strcol" COLSPAN=5 ALIGN=left >
      <INPUT TYPE="text" NAME="GuardianHistory_Addr1_1" VALUE="<<GuardianHistory_Addr1_1>>" onFocus="select()" SIZE="30" >
    </TD>
  </TR>
  <TR >
    <TD CLASS="homesublink" >Address 2</TD>
    <TD CLASS="strcol" COLSPAN=5 ALIGN=left >
      <INPUT TYPE="text" NAME="GuardianHistory_Addr2_1" VALUE="<<GuardianHistory_Addr2_1>>" onFocus="select()" SIZE="30" >
    </TD>
  </TR>
  <TR >
    <TD CLASS="homesublink" >City</TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="text" NAME="GuardianHistory_City_1" VALUE="<<GuardianHistory_City_1>>" onFocus="select()" SIZE="20" >
    </TD>
  </TR>
  <TR>
    <TD CLASS="homesublink" >State</TD>
    <TD CLASS="strcol" >
      <SELECT NAME="GuardianHistory_ST_1">
        [[DBA->selxTable(%form+xState+<<GuardianHistory_ST_1>>+Descr)]]
      </SELECT>
    </TD>
  </TR>
  <TR>
    <TD CLASS="homesublink" >Zip</TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="text" NAME="GuardianHistory_Zip_1" VALUE="<<GuardianHistory_Zip_1>>" onFocus="select()" MAXLENGTH="10" SIZE="10" ONCHANGE="return vZip(this)" >
      <A HREF="javascript:uspsWindow('Address Check',300,300)" ONMOUSEOVER="window.status='Address Check'; return true;" ONMOUSEOUT="window.status=''">(check address)</A>
    </TD>
  </TR>
  <TR >
    <TD CLASS="strcol" >Who is (or was) the primary disciplinarian in the home?</TD>
    <TD CLASS="strcol" >
      <SELECT NAME="ClientRelations_DisciplineBy_1" >
        [[DBA->selxTable(%form+xRelationship+<<ClientRelations_DisciplineBy_1>>+Descr)]]
      </SELECT>
    </TD>
  </TR>
  <TR ><TD CLASS="strcol" COLSPAN="2" >Was it deserved and fair?</TD></TR>
  <TR >
    <TD CLASS="strcol" >If not, why?</TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="text" NAME="ClientRelations_DisciplineDesc_1" VALUE="<<ClientRelations_DisciplineDesc_1>>" MAXLENGTH="50" SIZE="80" >
    </TD>
  </TR>
  <TR >
    <TD CLASS="strcol" >How were you punished?</TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="text" NAME="ClientRelations_PunishDesc_1" VALUE="<<ClientRelations_PunishDesc_1>>" SIZE="70" >
    </TD>
  </TR>
  <TR ><TD CLASS="strcol" COLSPAN="2" >Brothers/Sisters: (List last, first, middle name, and age of each)</TD></TR>
  <TR ><TD CLASS="strcol" COLSPAN="2" >Name and Rate your relationship with the following people from 1 to 10 (1=bad, 10=excellent)</TD></TR>
  <TR ><TD CLASS="strcol" COLSPAN="2" >Persons Living In Home</TD></TR>
  <TR >
    <TD COLSPAN="2" >
<SPAN ID="ListClientIHFamily" >
[[myHTML->ListSel(%form+ListClientIHFamily+<<<Client_ClientID>>>+<<<LINKID>>>+<<<Client_Locked_1>>>)]]
</SPAN>
    </TD>
  </TR>
    </TABLE></TD></TR>
</TABLE>
<TABLE CLASS="port fullsize" >
    <TR ><TD ><TABLE CLASS="home fullsize" >
  <TR ><TD CLASS="port hdrtxt" COLSPAN="2" >Current Living Situation</TD></TR>
  <TR >
    <TD CLASS="strcol" >Client Residence</TD>
    <TD CLASS="strcol" >
      <SELECT NAME="ClientRelations_Residence_1" >
        [[DBA->selxTable(%form+xResidence+<<ClientRelations_Residence_1>>+CDC Descr)]]
      </SELECT>
    </TD>
  </TR>
  <TR >
    <TD CLASS="strcol" >Admit/Placement Date</TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="text" NAME="ClientRelations_ResAdmitDate_1" VALUE="<<ClientRelations_ResAdmitDate_1>>" ONCHANGE="vDate(this,1)" SIZE="10" >
      (for ICF/MR and Nursing Home)
    </TD>
  </TR>
  <TR >
    <TD CLASS="strcol" >
      Are you satisfied with these arrangements?
    </TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="radio" NAME="ClientRelations_SatResidence_1" VALUE=0 <<ClientRelations_SatResidence_1=0>> > No
      <INPUT TYPE="radio" NAME="ClientRelations_SatResidence_1" VALUE=1 <<ClientRelations_SatResidence_1=1>> > Yes
    </TD>
  </TR>
  <TR >
    <TD CLASS="strcol" >Group Home Level</TD>
    <TD CLASS="strcol" >
      <SELECT NAME="ClientRelations_GHLevel_1" >
        [[DBA->selxTable(%form+xGHLevel+<<ClientRelations_GHLevel_1>>+Descr)]]
      </SELECT>
    </TD>
  </TR>
  <TR >
    <TD CLASS="strcol" >Multiple placements in the past 2 years</TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="text" NAME="ClientRelations_ResNum_1" VALUE="<<ClientRelations_ResNum_1>>" ONFOCUS="select()" ONCHANGE="return vNum(this,0,24);" SIZE="10" >
      (0-24)
    </TD>
  </TR>
  <TR >
    <TD CLASS="strcol" >In the past 90 days, how many days in a restrictive placement?</TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="text" NAME="MedHx_RestrictivePlacement_1" VALUE="<<MedHx_RestrictivePlacement_1>>" ONFOCUS="select()" ONCHANGE="return vNum(this,0,90);" SIZE="2" >
    </TD>
  </TR>
  <TR >
    <TD CLASS="strcol" COLSPAN="2" >Facility where services are rendered (if other than home or office)</TD>
  </TR>
  <TR >
    <TD CLASS="strcol" COLSPAN="2" >
      Search: <INPUT TYPE="text" ID="SearchFac" NAME="SearchFac" VALUE="" ONFOCUS="select()" ONCHANGE="callAjax('Agency','<<ClientRelations_FacIDNPI_1>>','selFac','&name=ClientRelations_FacIDNPI_1&pattern='+this.value,'popup.pl');" SIZE="60" >
<BR><SPAN ID="selFac"></SPAN>
    </TD>
  </TR>
  <TR >
    <TD CLASS="strcol" >Client has been continuously homeless for a year or more?</TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="radio" NAME="ClientRelations_HomelessLong_1" VALUE=0 <<ClientRelations_HomelessLong_1=0>> > No
      <INPUT TYPE="radio" NAME="ClientRelations_HomelessLong_1" VALUE=1 <<ClientRelations_HomelessLong_1=1>> > Yes
    </TD>
  </TR>
  <TR >
    <TD CLASS="strcol" >Client has had at least 4 episodes of homelessness in the past 3 years?</TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="radio" NAME="ClientRelations_HomelessMany_1" VALUE=0 <<ClientRelations_HomelessMany_1=0>> > No
      <INPUT TYPE="radio" NAME="ClientRelations_HomelessMany_1" VALUE=1 <<ClientRelations_HomelessMany_1=1>> > Yes
    </TD>
  </TR>
    </TABLE></TD></TR>
    <TR ><TD ><TABLE CLASS="home fullsize" >
  <TR ><TD CLASS="port hdrtxt" COLSPAN="2" >Other Persons Living In The Home</TD></TR>
  <TR ><TD CLASS="homelabel" COLSPAN="2" >[Enter above under Family Members - Add New Member</TD></TR>
    </TABLE></TD></TR>
    <TR ><TD ><TABLE CLASS="home fullsize" >
  <TR ><TD CLASS="port hdrtxt" COLSPAN="2" >Usual Living Arrangement (past 3 years)(check only one)</TD></TR>
  <TR >
    <TD CLASS="strcol" >
      Usual living arrangements (past 3 years):
      <BR>� Choose arrangements most representative of the past 3 years. If there is an even split in time between these arrangements, choose the most recent arrangement.
    </TD>
    <TD CLASS="strcol" >
      <SELECT NAME="ClientRelations_FamUsualLivArr_1">
        [[DBA->selxTable(%form+xLivingArrASI+<<ClientRelations_FamUsualLivArr_1>>+ID Descr)]]
      </SELECT>
    </TD>
  </TR>
  <TR >
    <TD CLASS="strcol" >
      Are you satisfied with these arrangements?
    </TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="radio" NAME="ClientRelations_SatUsualLivArr_1" VALUE=0 <<ClientRelations_SatUsualLivArr_1=0>> > No
      <INPUT TYPE="radio" NAME="ClientRelations_SatUsualLivArr_1" VALUE=1 <<ClientRelations_SatUsualLivArr_1=1>> > Indifferent
      <INPUT TYPE="radio" NAME="ClientRelations_SatUsualLivArr_1" VALUE=2 <<ClientRelations_SatUsualLivArr_1=2>> > Yes
    </TD>
  </TR>
    </TABLE></TD></TR>
</TABLE>
<TABLE CLASS="main fullsize" >
  <TR >
    <TD CLASS="numcol" >
      <INPUT TYPE="submit" ONCLICK="return validate(this.form);" NAME="UpdateTables=all&[[myForm->genLink(ClientIntake+ClientResources.cgi)]]" VALUE="Add/Update -> Resources">
      <INPUT TYPE="submit" ONCLICK="return validate(this.form);" NAME="UpdateTables=all&misPOP=1" VALUE="Add/Update">
    </TD>
  </TR>
</TABLE>

<INPUT TYPE="hidden" NAME="post_update" VALUE="PostUpd->updPA(%form+<<<Client_ClientID_1>>>)" >
</LOADHIDDEN>
</FORM>
<SCRIPT LANGUAGE="JavaScript">
document.ClientFamily.elements[0].focus();
callAjax('Agency','<<ClientRelations_FacIDNPI_1>>','selFac','&name=ClientRelations_FacIDNPI_1','popup.pl');
</SCRIPT>

[[myHTML->rightpane(%form+search)]]
