[[myHTML->newHTML(%form+Objectives+allleft mismenu checkpopupwindow)]]

<SCRIPT LANGUAGE="JavaScript" SRC="/cgi/js/vEntry.js"> </SCRIPT>
<SCRIPT LANGUAGE="JavaScript" SRC="/cgi/js/vClientTrPlanOBJ.js"> </SCRIPT>
<SCRIPT type="text/javascript" src="/cgi/js/ajaxrequest.js"></SCRIPT>
<SCRIPT LANGUAGE="JavaScript" SRC="/cgi/js/mDate.js"> </SCRIPT>
<SCRIPT LANGUAGE="JavaScript" SRC="/cgi/js/vDate.js"> </SCRIPT>
<SCRIPT LANGUAGE="JavaScript" SRC="/cgi/js/vNum.js"> </SCRIPT>
<SCRIPT LANGUAGE="JavaScript">
function TPPG(e)
{ InputWindow('/cgi/bin/TPPG.cgi?mlt=<<<mlt>>>&id='+e,'ViewPG'); }
// DeCloak -->
</SCRIPT>

<FORM NAME="ClientTrPlanOBJ" ACTION="/cgi/bin/mis.cgi" METHOD="POST" >
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
      OBJECTIVE: <<ClientTrPlanOBJ_Obj_1>>
    </TD>
  </TR>
  <TR>
    <TD CLASS="strcol" >
      <BR>PROGRESS:
      <BR>
      <TEXTAREA NAME="ClientTrPlanOBJ_Progress_1" COLS="60" ROWS="3" WRAP="virtual" ONFOCUS="select();" ><<ClientTrPlanOBJ_Progress_1>></TEXTAREA>
    </TD>
  </TR>
  <TR>
    <TD CLASS="strcol" >
      RESOLVED DATE:
      <BR>
      <INPUT TYPE="text" NAME="ClientTrPlanOBJ_ResolvedDate_1" VALUE="<<ClientTrPlanOBJ_ResolvedDate_1>>" ONFOCUS="select();" ONCHANGE="return vDate(this,1);" SIZE="10" >
    </TD>
  </TR>
  <TR>
    <TD CLASS="strcol" >
      <BR>DATE INITIATED: <<ClientTrPlanOBJ_InitiatedDate_1>>
      <BR>TARGET DATE: <<ClientTrPlanOBJ_TargetDate_1>>
    </TD>
  </TR>
  <TR>
    <TD CLASS="strcol" >
      <BR>FREQUENCY: <<ClientTrPlanOBJ_Frequency_1>>
    </TD>
  </TR>
  <TR>
    <TD CLASS="strcol" >
      <BR>SERVICES: 
        [[DBA->getxref(%form+xServices+<<ClientTrPlanOBJ_Service1_1>>+Descr)]]
      <BR>PROVIDER:
        [[DBA->getxref(%form+Provider+<<ClientTrPlanOBJ_ProvID1_1>>+LName FName)]]
    </TD>
  </TR>
  <TR>
    <TD CLASS="strcol" >
      <BR>SERVICES: 
        [[DBA->getxref(%form+xServices+<<ClientTrPlanOBJ_Service2_1>>+Descr)]]
      <BR>PROVIDER:
        [[DBA->getxref(%form+Provider+<<ClientTrPlanOBJ_ProvID2_1>>+LName FName)]]
    </TD>
  </TR>
  <TR>
    <TD CLASS="strcol" >
      <BR>SERVICES: 
        [[DBA->getxref(%form+xServices+<<ClientTrPlanOBJ_Service3_1>>+Descr)]]
      <BR>PROVIDER:
        [[DBA->getxref(%form+Provider+<<ClientTrPlanOBJ_ProvID3_1>>+LName FName)]]
    </TD>
  </TR>
</TABLE>
<TABLE CLASS="main fullsize" >
  <TR>
    <TD CLASS="numcol" >
      <INPUT TYPE="submit" ONCLICK="return validate(this.form);" NAME="UpdateTables=all&misPOP=1" VALUE="Add/Update">
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
