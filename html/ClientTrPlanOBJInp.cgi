[[myHTML->newHTML(%form+Objectives+allleft mismenu checkpopupwindow)]]

<SCRIPT LANGUAGE="JavaScript" SRC="/src/cgi/js/NoEnter.js"> </SCRIPT>
<SCRIPT LANGUAGE="JavaScript" SRC="/src/cgi/js/vClientTrPlanOBJ.js"> </SCRIPT>
<SCRIPT LANGUAGE="JavaScript" SRC="/src/cgi/js/mDate.js"> </SCRIPT>
<SCRIPT LANGUAGE="JavaScript" SRC="/src/cgi/js/vDate.js"> </SCRIPT>
<SCRIPT LANGUAGE="JavaScript" SRC="/src/cgi/js/vNum.js"> </SCRIPT>
<SCRIPT LANGUAGE="JavaScript">
function TPPG(e)
{ InputWindow('/src/cgi/bin/TPPG.cgi?mlt=<<<mlt>>>&id='+e,'ViewPG'); }
// DeCloak -->
</SCRIPT>

<FORM NAME="ClientTrPlanOBJ" ACTION="/src/cgi/bin/mis.cgi" METHOD="POST" >
<TABLE CLASS="main fullsize" >
  <TR >
    <TD CLASS="strcol" >
      <<<Client_FName_1>>> <<<Client_MName_1>>> <<<Client_LName_1>>> (<<<Client_ClientID_1>>>) <<<Client_SSN_1>>>
      <BR>Identified Objective #
[[DBUtil->divNUM(<<<ClientTrPlanOBJ_Priority_1>>>+10)]]
    </TD>
    <TD CLASS="numcol" >[[gHTML->setLINKS(%form+back)]]</TD>
  </TR>
</TABLE>
<TABLE CLASS="home fullsize" >
  <TR>
    <TD CLASS="strcol" >
      OBJECTIVE:
      <A HREF="javascript:TPPG(<<<ClientTrPlanPG_NeedSkill_1>>>)" ONMOUSEOVER="window.status='click here to view attached document'; return true;" ONMOUSEOUT="window.status=''" ><IMG BORDER="0" SRC="/images/view_document.gif">View Problems/Goals/Objectives</A>
      <BR>
      <TEXTAREA NAME="ClientTrPlanOBJ_Obj_1" COLS="60" ROWS="3" WRAP="virtual" ONFOCUS="select();" ><<ClientTrPlanOBJ_Obj_1>></TEXTAREA>
    </TD>
  </TR>
  <TR>
    <TD CLASS="strcol" >
      DATE INITIATED:
      <BR>
      <INPUT TYPE="text" NAME="ClientTrPlanOBJ_InitiatedDate_1" VALUE="<<ClientTrPlanOBJ_InitiatedDate_1>>" ONFOCUS="select();" ONCHANGE="return vSetDate(this,1,this.form,'ClientTrPlanOBJ_TargetDate_1',6,-1)" SIZE="10" >
      <BR>
      TARGET DATE:
      <BR>
      <INPUT TYPE="text" NAME="ClientTrPlanOBJ_TargetDate_1" VALUE="<<ClientTrPlanOBJ_TargetDate_1>>" ONFOCUS="select();" ONCHANGE="return vDate(this,1);" SIZE="10" >
    </TD>
  </TR>
  <TR>
    <TD CLASS="strcol" >
      Note: for FREQUENCY; Individual and Interactive are noted in hours.  Other treatments are in sessions / week.
      <BR>
      FREQUENCY:
      <BR>
      <INPUT TYPE="text" NAME="ClientTrPlanOBJ_Frequency_1" VALUE="<<ClientTrPlanOBJ_Frequency_1>>" ONFOCUS="select();" ONCHANGE="return vNum(this,0.1,515)" SIZE=5> / week
    </TD>
  </TR>
  <TR>
    <TD CLASS="strcol" >
      TREATMENT SERVICES / PROVIDER:
      <BR>
      <SELECT NAME="ClientTrPlanOBJ_Service1_1" >
        [[DBA->selxTable(%form+xServices+<<ClientTrPlanOBJ_Service1_1>>+Descr)]]
      </SELECT> 
      <SELECT NAME="ClientTrPlanOBJ_ProvID1_1" >
        [[DBA->selProviders(%form+<<ClientTrPlanOBJ_ProvID1_1>>)]] </SELECT> 
      </SELECT> 
    </TD>
  </TR>
  <TR>
    <TD CLASS="strcol" >
      TREATMENT SERVICES / PROVIDER:
      <BR>
      <SELECT NAME="ClientTrPlanOBJ_Service2_1" >
        [[DBA->selxTable(%form+xServices+<<ClientTrPlanOBJ_Service2_1>>+Descr)]]
      </SELECT> 
      <SELECT NAME="ClientTrPlanOBJ_ProvID2_1" >
        [[DBA->selProviders(%form+<<ClientTrPlanOBJ_ProvID2_1>>)]] </SELECT> 
      </SELECT> 
    </TD>
  </TR>
  <TR>
    <TD CLASS="strcol" >
      TREATMENT SERVICES / PROVIDER:
      <BR>
      <SELECT NAME="ClientTrPlanOBJ_Service3_1" >
        [[DBA->selxTable(%form+xServices+<<ClientTrPlanOBJ_Service3_1>>+Descr)]]
      </SELECT> 
      <SELECT NAME="ClientTrPlanOBJ_ProvID3_1" >
        [[DBA->selProviders(%form+<<ClientTrPlanOBJ_ProvID3_1>>)]] </SELECT> 
      </SELECT> 
    </TD>
  </TR>
  <TR>
    <TD CLASS="strcol" >
      PROGRESS:
      <BR>
      <TEXTAREA NAME="ClientTrPlanOBJ_Progress_1" COLS="60" ROWS="3" WRAP="virtual" ONFOCUS="select();" ><<ClientTrPlanOBJ_Progress_1>></TEXTAREA>
    </TD>
  </TR>
  <TR>
    <TD CLASS="strcol" >
      RESOLVED DATE:
      <BR>
      <INPUT TYPE="text" NAME="ClientTrPlanOBJ_ResolvedDate_1" VALUE="<<ClientTrPlanOBJ_ResolvedDate_1>>" ONFOCUS="select();" ONCHANGE="return vDate(this,1);" SIZE="10" >
      <BR>
      Resolve only if needed, otherwise leave blank and enter later. There will be a 'Resolve' button if TP is signed.
    </TD>
  </TR>
</TABLE>
<TABLE CLASS="main fullsize" >
  <TR>
    <TD CLASS="numcol" >
[[myTables->htmLocked(%form+<<<ClientTrPlanPG_Locked_1>>>+ClientTrPlanOBJ)]]
    </TD>
  </TR>
</TABLE>

<INPUT TYPE="hidden" NAME="post_update" VALUE="PostUpd->renumClientTrPlanOBJ(%form+<<<ClientTrPlanPG_ID_1>>>)" >
</LOADHIDDEN>
</FORM>
<SCRIPT LANGUAGE="JavaScript">
document.ClientTrPlanOBJ.elements[0].focus();
</SCRIPT>

[[myHTML->rightpane(%form+search)]]
