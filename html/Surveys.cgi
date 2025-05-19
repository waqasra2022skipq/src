[[myHTML->newPage(%form+Provider and Client Survey)]]

<LINK REL="stylesheet" TYPE="text/css" HREF="/cgi/jcal/calendar-forest.css" >
<SCRIPT TYPE="text/javascript" SRC="/src/cgi/js/vEntry.js"></SCRIPT>
<SCRIPT TYPE="text/javascript" SRC="/src/cgi/js/utils.js"></SCRIPT>
<SCRIPT TYPE="text/javascript" SRC="/cgi/jcal/calendar.js"></SCRIPT>
<SCRIPT TYPE="text/javascript" SRC="/cgi/jcal/calendar-en.js"></SCRIPT>
<SCRIPT TYPE="text/javascript" SRC="/cgi/jcal/calendar-setup.js"></SCRIPT>
<SCRIPT LANGUAGE="JavaScript" SRC="/src/cgi/js/vSurveys.js"> </SCRIPT>
<SCRIPT LANGUAGE="JavaScript" SRC="/src/cgi/js/vDate.js"> </SCRIPT>

<FORM NAME="Surveys" ACTION="/src/cgi/bin/mis.cgi" METHOD="POST" >
<TABLE CLASS="main fullsize" >
  <TR >
    <TD CLASS="strcol" >
      Entered by: [[DBA->getxref(%form+Provider+<<<Surveys_CreateProvID_1>>>+FName LName)]] &nbsp;
      <BR> Entered on: <<<Surveys_CreateDate_1>>>
      <BR> Satisfaction Survey Information
    </TD>
    <TD CLASS="numcol" >[[gHTML->setLINKS(%form+back)]]</TD>
  </TR>
</TABLE>
<TABLE CLASS="home fullsize" >
  <TR>
    <TD CLASS="strcol" >Survey Date</TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="text" ID="SurveyDate" NAME="Surveys_Date_1" VALUE="<<Surveys_Date_1>>" ONFOCUS="select()" ONCHANGE="return vDate(this)" MAXLENGTH="10" SIZE="10" >
      <BUTTON TYPE="reset" ID="SurveyDateB">calendar</BUTTON>
      <script type="text/javascript">Calendar.setup({inputField:"SurveyDate",button:"SurveyDateB"});</script>
    </TD>
  </TR>
  <TR >
    <TD CLASS="strcol" >
      For Provider<BR>
      <SELECT NAME="Surveys_ProvID_1" SIZE="10" >[[DBA->selProviders(%form+<<Surveys_ProvID_1>>)]]</SELECT> 
    </TD>
    <TD CLASS="strcol" >
      For Client<BR>
      <SELECT NAME="Surveys_ClientID_1" SIZE="10" >[[DBA->selClients(%form+<<Surveys_ClientID_1>>)]]</SELECT> 
    </TD>
  </TR>
  <TR>
    <TD CLASS="strcol" COLSPAN="2" >1. My counselor was on time and kept my scheduled appointment.</TD>
  </TR>
  <TR>
    <TD CLASS="strcol" >&nbsp;</TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="radio" NAME="Surveys_SessionsOK_1" VALUE=1 <<Surveys_SessionsOK_1=1>> > Strongly Disagree
      <INPUT TYPE="radio" NAME="Surveys_SessionsOK_1" VALUE=2 <<Surveys_SessionsOK_1=2>> > Disagree
      <INPUT TYPE="radio" NAME="Surveys_SessionsOK_1" VALUE=3 <<Surveys_SessionsOK_1=3>> > Somewhat Agree
      <INPUT TYPE="radio" NAME="Surveys_SessionsOK_1" VALUE=4 <<Surveys_SessionsOK_1=4>> > Agree
      <INPUT TYPE="radio" NAME="Surveys_SessionsOK_1" VALUE=5 <<Surveys_SessionsOK_1=5>> > Strongly Agree
    </TD>
  </TR>
  <TR>
    <TD CLASS="strcol" COLSPAN="2" >2. I was involved in my treatment plan.</TD>
  </TR>
  <TR>
    <TD CLASS="strcol" >&nbsp;</TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="radio" NAME="Surveys_TrPlan_1" VALUE=1 <<Surveys_TrPlan_1=1>> > Strongly Disagree
      <INPUT TYPE="radio" NAME="Surveys_TrPlan_1" VALUE=2 <<Surveys_TrPlan_1=2>> > Disagree
      <INPUT TYPE="radio" NAME="Surveys_TrPlan_1" VALUE=3 <<Surveys_TrPlan_1=3>> > Somewhat Agree
      <INPUT TYPE="radio" NAME="Surveys_TrPlan_1" VALUE=4 <<Surveys_TrPlan_1=4>> > Agree
      <INPUT TYPE="radio" NAME="Surveys_TrPlan_1" VALUE=5 <<Surveys_TrPlan_1=5>> > Strongly Agree
    </TD>
  </TR>
  <TR>
    <TD CLASS="strcol" COLSPAN="2" >3. I felt my concerns were handled in a confidential way.</TD>
  </TR>
  </TR>
  <TR >
    <TD CLASS="strcol" >&nbsp;</TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="radio" NAME="Surveys_Respected_1" VALUE=1 <<Surveys_Respected_1=1>> > Strongly Disagree
      <INPUT TYPE="radio" NAME="Surveys_Respected_1" VALUE=2 <<Surveys_Respected_1=2>> > Disagree
      <INPUT TYPE="radio" NAME="Surveys_Respected_1" VALUE=3 <<Surveys_Respected_1=3>> > Somewhat Agree
      <INPUT TYPE="radio" NAME="Surveys_Respected_1" VALUE=4 <<Surveys_Respected_1=4>> > Agree
      <INPUT TYPE="radio" NAME="Surveys_Respected_1" VALUE=5 <<Surveys_Respected_1=5>> > Strongly Agree
    </TD>
  </TR>
  <TR>
    <TD CLASS="strcol" COLSPAN="2" >4. I received help resolving trauma issues.</TD>
  </TR>
  <TR >
    <TD CLASS="strcol" >&nbsp;</TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="radio" NAME="Surveys_TraumaIssues_1" VALUE=0 <<Surveys_TraumaIssues_1=0>> > No
      <INPUT TYPE="radio" NAME="Surveys_TraumaIssues_1" VALUE=1 <<Surveys_TraumaIssues_1=1>> > Yes
    </TD>
  </TR>
  <TR>
    <TD CLASS="strcol" COLSPAN="2" >5. I received help with substance abuse issues.</TD>
  </TR>
  <TR >
    <TD CLASS="strcol" >&nbsp;</TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="radio" NAME="Surveys_SAbuseIssues_1" VALUE=0 <<Surveys_SAbuseIssues_1=0>> > No
      <INPUT TYPE="radio" NAME="Surveys_SAbuseIssues_1" VALUE=1 <<Surveys_SAbuseIssues_1=1>> > Yes
    </TD>
  </TR>
  <TR>
    <TD CLASS="strcol" COLSPAN="2" >6. I have benefited from the services received.</TD>
  </TR>
  <TR>
    <TD CLASS="strcol" >&nbsp;</TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="radio" NAME="Surveys_Helped_1" VALUE=1 <<Surveys_Helped_1=1>> > Strongly Disagree
      <INPUT TYPE="radio" NAME="Surveys_Helped_1" VALUE=2 <<Surveys_Helped_1=2>> > Disagree
      <INPUT TYPE="radio" NAME="Surveys_Helped_1" VALUE=3 <<Surveys_Helped_1=3>> > Somewhat Agree
      <INPUT TYPE="radio" NAME="Surveys_Helped_1" VALUE=4 <<Surveys_Helped_1=4>> > Agree
      <INPUT TYPE="radio" NAME="Surveys_Helped_1" VALUE=5 <<Surveys_Helped_1=5>> > Strongly Agree
    </TD>
  </TR>
  <TR>
    <TD CLASS="strcol" COLSPAN="2" >7. I would refer others to this agency.</TD>
  </TR>
  <TR>
    <TD CLASS="strcol" >&nbsp;</TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="radio" NAME="Surveys_Recommend_1" VALUE=1 <<Surveys_Recommend_1=1>> > Strongly Disagree
      <INPUT TYPE="radio" NAME="Surveys_Recommend_1" VALUE=2 <<Surveys_Recommend_1=2>> > Disagree
      <INPUT TYPE="radio" NAME="Surveys_Recommend_1" VALUE=3 <<Surveys_Recommend_1=3>> > Somewhat Agree
      <INPUT TYPE="radio" NAME="Surveys_Recommend_1" VALUE=4 <<Surveys_Recommend_1=4>> > Agree
      <INPUT TYPE="radio" NAME="Surveys_Recommend_1" VALUE=5 <<Surveys_Recommend_1=5>> > Strongly Agree
    </TD>
  </TR>
  <TR>
    <TD CLASS="strcol" COLSPAN="2" >8. The program was explained clearly to me at intake.</TD>
  </TR>
  <TR >
    <TD CLASS="strcol" >&nbsp;</TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="radio" NAME="Surveys_RightsExp_1" VALUE=0 <<Surveys_RightsExp_1=0>> > No
      <INPUT TYPE="radio" NAME="Surveys_RightsExp_1" VALUE=1 <<Surveys_RightsExp_1=1>> > Yes
    </TD>
  </TR>
  <TR>
    <TD CLASS="strcol" COLSPAN="2" >9. I received a copy of my client rights.</TD>
  </TR>
  <TR>
    <TD CLASS="strcol" >&nbsp;</TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="radio" NAME="Surveys_RightsRec_1" VALUE=0 <<Surveys_RightsRec_1=0>> > No
      <INPUT TYPE="radio" NAME="Surveys_RightsRec_1" VALUE=1 <<Surveys_RightsRec_1=1>> > Yes
    </TD>
  </TR>
  <TR>
    <TD CLASS="strcol" COLSPAN="2" >10. What did you like best about your counseling experience?</TD>
  </TR>
  <TR>
    <TD CLASS="strcol" COLSPAN="2" >
       <TEXTAREA NAME="Surveys_LikeBest_1" COLS=80 ROWS=5 WRAP="virtual" ><<Surveys_LikeBest_1>></TEXTAREA>
    </TD>
  </TR>
  <TR>
    <TD CLASS="strcol" COLSPAN="2" >11. What did you like least about your counseling experience?</TD>
  </TR>
  <TR>
    <TD CLASS="strcol" COLSPAN="2" >
       <TEXTAREA NAME="Surveys_LikeLeast_1" COLS=80 ROWS=5 WRAP="virtual" ><<Surveys_LikeLeast_1>></TEXTAREA>
    </TD>
  </TR>
  <TR>
    <TD CLASS="strcol" COLSPAN="2" >12. Suggestions to improve our program.</TD>
  </TR>
  <TR>
    <TD CLASS="strcol" COLSPAN="2" >
       <TEXTAREA NAME="Surveys_Suggestions_1" COLS=80 ROWS=5 WRAP="virtual" ><<Surveys_Suggestions_1>></TEXTAREA>
    </TD>
  </TR>
  <TR>
    <TD CLASS="strcol" COLSPAN="2" >13. I will be better able to handle my problems because of my participation in this program.</TD>
  </TR>
  <TR>
    <TD CLASS="strcol" >&nbsp;</TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="radio" NAME="Surveys_Handle_1" VALUE=1 <<Surveys_Handle_1=1>> > Strongly Disagree
      <INPUT TYPE="radio" NAME="Surveys_Handle_1" VALUE=2 <<Surveys_Handle_1=2>> > Disagree
      <INPUT TYPE="radio" NAME="Surveys_Handle_1" VALUE=3 <<Surveys_Handle_1=3>> > Somewhat Agree
      <INPUT TYPE="radio" NAME="Surveys_Handle_1" VALUE=4 <<Surveys_Handle_1=4>> > Agree
      <INPUT TYPE="radio" NAME="Surveys_Handle_1" VALUE=5 <<Surveys_Handle_1=5>> > Strongly Agree
    </TD>
  </TR>
  <TR>
    <TD CLASS="strcol" COLSPAN="2" >14. I was treated fairly and equitably by the staff and providers.</TD>
  </TR>
  <TR>
    <TD CLASS="strcol" >&nbsp;</TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="radio" NAME="Surveys_Fairly_1" VALUE=1 <<Surveys_Fairly_1=1>> > Strongly Disagree
      <INPUT TYPE="radio" NAME="Surveys_Fairly_1" VALUE=2 <<Surveys_Fairly_1=2>> > Disagree
      <INPUT TYPE="radio" NAME="Surveys_Fairly_1" VALUE=3 <<Surveys_Fairly_1=3>> > Somewhat Agree
      <INPUT TYPE="radio" NAME="Surveys_Fairly_1" VALUE=4 <<Surveys_Fairly_1=4>> > Agree
      <INPUT TYPE="radio" NAME="Surveys_Fairly_1" VALUE=5 <<Surveys_Fairly_1=5>> > Strongly Agree
    </TD>
  </TR>
  <TR>
    <TD CLASS="strcol" COLSPAN="2" >15. The provider assigned to my case was a good match for my needs.</TD>
  </TR>
  <TR>
    <TD CLASS="strcol" >&nbsp;</TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="radio" NAME="Surveys_GoodMatch_1" VALUE=1 <<Surveys_GoodMatch_1=1>> > Strongly Disagree
      <INPUT TYPE="radio" NAME="Surveys_GoodMatch_1" VALUE=2 <<Surveys_GoodMatch_1=2>> > Disagree
      <INPUT TYPE="radio" NAME="Surveys_GoodMatch_1" VALUE=3 <<Surveys_GoodMatch_1=3>> > Somewhat Agree
      <INPUT TYPE="radio" NAME="Surveys_GoodMatch_1" VALUE=4 <<Surveys_GoodMatch_1=4>> > Agree
      <INPUT TYPE="radio" NAME="Surveys_GoodMatch_1" VALUE=5 <<Surveys_GoodMatch_1=5>> > Strongly Agree
    </TD>
  </TR>
</TABLE>
<TABLE CLASS="main fullsize" >
  <TR>
    <TD CLASS="numcol" >
      <INPUT TYPE="submit" ONCLICK="return vDELETE('Are you sure you want to delete this Survey?');" NAME="Surveys_DELETE_1=1&UpdateTables=all&misPOP=1" VALUE="Delete">
      <INPUT TYPE="submit" ONCLICK="return validate(this.form);" NAME="UpdateTables=all&misPOP=1" VALUE="Add/Update">
    </TD>
  </TR>
</TABLE>

</LOADHIDDEN>
</FORM>
<SCRIPT LANGUAGE="JavaScript">
document.Surveys.elements[0].focus();
</SCRIPT>
[[myHTML->rightpane(%form+search)]]
