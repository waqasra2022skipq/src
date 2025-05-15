[[myHTML->newHTML(%form+Problems and Goals+allleft mismenu checkpopupwindow)]]

<SCRIPT LANGUAGE="JavaScript" SRC="/src/cgi/js/NoEnter.js"> </SCRIPT>
<SCRIPT LANGUAGE="JavaScript" SRC="/src/cgi/js/vEntry.js"> </SCRIPT>
<SCRIPT LANGUAGE="JavaScript" SRC="/src/cgi/js/vClientTrPlanPG.js"> </SCRIPT>
<SCRIPT type="text/javascript" src="/src/cgi/js/ajaxrequest.js"></SCRIPT>
<SCRIPT LANGUAGE="JavaScript">
function TPPG(e)
{ InputWindow('/cgi/bin/TPPG.cgi?mlt=<<<mlt>>>&id='+e.value,'ViewPG'); }
// DeCloak -->
</SCRIPT>

<FORM NAME="ClientTrPlanPG" ACTION="/cgi/bin/mis.cgi" METHOD="POST" >
<TABLE CLASS="main fullsize" >
  <TR >
    <TD CLASS="strcol" >
      <<<Client_FName_1>>> <<<Client_MName_1>>> <<<Client_LName_1>>> (<<<Client_ClientID_1>>>) <<<Client_SSN_1>>>
      <BR>Identified Problem #
[[DBUtil->divNUM(<<<ClientTrPlanPG_Priority_1>>>+10)]]
    </TD>
    <TD CLASS="numcol" >[[gHTML->setLINKS(%form+back)]]</TD>
  </TR>
</TABLE>
<TABLE CLASS="home fullsize" >
  <TR>
    <TD CLASS="strcol" >NEED / SKILL</TD>
    <TD CLASS="strcol" >
      <SELECT NAME="ClientTrPlanPG_NeedSkill_1" >
        [[DBA->selxTable(%form+xNS+<<ClientTrPlanPG_NeedSkill_1>>+Descr)]]
      </SELECT> 
      (describe below in PROBLEM if 'Other')
    </TD>
  </TR>
  <TR>
    <TD CLASS="strcol" >
      PROBLEM (brief description only)
      <BR>
      <A HREF="javascript:TPPG(document.ClientTrPlanPG.ClientTrPlanPG_NeedSkill_1)" ONMOUSEOVER="window.status='click here to view attached document'; return true;" ONMOUSEOUT="window.status=''" ><IMG BORDER="0" SRC="/images/view_document.gif">View Problems/Goals/Objectives</A>
    </TD>
    <TD CLASS="strcol" >
      <TEXTAREA NAME="ClientTrPlanPG_Prob_1" COLS="80" ROWS="5" WRAP="virtual" ONFOCUS="select();" ><<ClientTrPlanPG_Prob_1>></TEXTAREA>
    </TD>
  </TR>
  <TR>
    <TD CLASS="strcol" >GOAL/EXPECTATION (in clients own words)</TD>
    <TD CLASS="strcol" >
      <TEXTAREA NAME="ClientTrPlanPG_Goal_1" COLS="80" ROWS="5" WRAP="virtual" ONFOCUS="select();" ><<ClientTrPlanPG_Goal_1>></TEXTAREA>
    </TD>
  </TR>
    <TR>
    <TD CLASS="strcol" >GOAL CATEGORY</TD>
    <TD CLASS="strcol" >
      <SELECT NAME="ClientTrPlanPG_GoalCat_1" >
        [[DBA->selxTable(%form+xGC+<<ClientTrPlanPG_GoalCat_1>>+Descr)]]
      </SELECT> 
    </TD>
  </TR>
</TABLE>
<HR width="50%" >
<TABLE CLASS="home fullsize" >
  <TR >
    <TD CLASS="port hdrtxt" >
      Please Enter Treatment Plan/Objectives to COMPLETE
    </TD>
  </TR>
  <TR >
    <TD CLASS="port hdrtxt" >
<SPAN ID="ListClientTrPlanOBJ" >
[[myHTML->ListSel(%form+ListClientTrPlanOBJ+<<<ClientTrPlanPG_ID>>>+<<<LINKID>>>+<<<ClientTrPlanPG_Locked_1>>>)]]
</SPAN>
    </TD>
  </TR>
</TABLE>
<HR width="50%" >
<TABLE CLASS="home fullsize" >
  <TR>
    <TD CLASS="strcol" COLSPAN="2" >Comments
      <BR>
      <TEXTAREA NAME="ClientTrPlanPG_Comments_1" COLS="80" ROWS="5" WRAP="virtual" ONFOCUS="select();" ><<ClientTrPlanPG_Comments_1>></TEXTAREA>
  <TR ><TD CLASS="strcol" ></TD></TR>
</TABLE>
<TABLE CLASS="main fullsize" >
  <TR>
    <TD CLASS="numcol" >
[[myTables->htmLocked(%form+<<<ClientTrPlanPG_Locked_1>>>+ClientTrPlanPG)]]
    </TD>
  </TR>
</TABLE>

<INPUT TYPE="hidden" NAME="post_update" VALUE="PostUpd->renumClientTrPlanPG(%form+<<<ClientTrPlan_ID_1>>>)" >
</LOADHIDDEN>
</FORM>
<SCRIPT LANGUAGE="JavaScript">
document.ClientTrPlanPG.elements[0].focus();
</SCRIPT>

[[myHTML->rightpane(%form+search)]]
