[[myHTML->newPage(%form+Provider Jobs)]]

<SCRIPT LANGUAGE="JavaScript" SRC="/cgi/js/NoEnter.js"> </SCRIPT>
<SCRIPT LANGUAGE="JavaScript" SRC="/cgi/js/vEntry.js"> </SCRIPT>
<SCRIPT LANGUAGE="JavaScript" SRC="/cgi/js/vProviderJobsInp.js"> </SCRIPT>
<SCRIPT LANGUAGE="JavaScript" SRC="/cgi/js/ajaxrequest.js"> </SCRIPT>
<SCRIPT LANGUAGE="JavaScript" SRC="/cgi/js/vDate.js"> </SCRIPT>
<SCRIPT LANGUAGE="JavaScript" SRC="/cgi/js/vTime.js"> </SCRIPT>
<SCRIPT LANGUAGE="JavaScript" SRC="/cgi/js/vNum.js"> </SCRIPT>

<FORM NAME="ProviderJobs" ACTION="/cgi/bin/mis.cgi" METHOD="POST" >
<TABLE CLASS="main fullsize" >
  <TR >
    <TD CLASS="strcol" >
      <<<Provider_FName_1>>> <<<Provider_MName_1>>> <<<Provider_LName_1>>> 
      <BR>Edit/View Provider Jobs
    </TD>
    <TD CLASS="numcol" >[[gHTML->setLINKS(%form+back)]]</TD>
  </TR>
</TABLE>
<TABLE CLASS="home fullsize" >
  <TR >
    <TD CLASS="strcol" >InsIDs</TD>
    <TD CLASS="strcol" >
      <SELECT NAME="ProviderJobs_InsIDs_1" MULTIPLE SIZE="10" >
        [[DBA->selInsurance(%form+<<ProviderJobs_InsIDs_1>>)]]
      </SELECT>
    </TD>
  </TR>
</TABLE >
<TABLE CLASS="home fullsize" >
  <TR >
    <TD > Select Providers:<BR>
      <SELECT NAME="ProviderJobs_ProvIDs_1" ONCHANGE="callAjax('ListProviderClients','','ListProviderClients','&id='+this.value,'popup.pl');" SIZE="15" >
        [[gHTML->selProviders(%form+<<<Provider_ProvID_1>>>+<<ProviderJobs_ProvIDs_1>>)]]
      </SELECT>
    </TD>
    <TD WIDTH="66%" >
      <SPAN ID="ListProviderClients" >
<<<ProviderJobs_ClientIDs_1>>>
      [[myHTML->set1CheckBoxColumn(%form+select * from Client where ProvID='<<<ProviderJobs_ProvIDs_1>>>' order by LName,FName+ProviderJobs_ClientIDs_1+ClientID+LName~Last Name~strcol:FName~First Name~strcol:DOB~~hdrcol+Select Clients+<<<ProviderJobs_ClientIDs_1>>>)]]
      </SPAN>
    </TD >
  </TR>
</TABLE >
<TABLE CLASS="home fullsize" >
  <TR >
    <TD CLASS="strcol" >FromDate</TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="TEXT" NAME="ProviderJobs_FromDate_1" VALUE="<<ProviderJobs_FromDate_1>>" ONFOCUS="select()" ONCHANGE="return vDate(this)" MAXLENGTH="10" SIZE="10" >
    </TD>
  </TR>
  <TR >
    <TD CLASS="strcol" >ToDate</TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="TEXT" NAME="ProviderJobs_ToDate_1" VALUE="<<ProviderJobs_ToDate_1>>" ONFOCUS="select()" ONCHANGE="return vDate(this)" MAXLENGTH="10" SIZE="10" >
    </TD>
  </TR>
  <TR >
    <TD CLASS="strcol" >Folder</TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="TEXT" NAME="ProviderJobs_Folder_1" VALUE="<<ProviderJobs_Folder_1>>" ONFOCUS="select()" SIZE="80" >
    </TD>
  </TR>
  <TR >
    <TD CLASS="strcol" >StartTime</TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="TEXT" NAME="ProviderJobs_CronTime_1" VALUE="<<ProviderJobs_CronTime_1>>" ONFOCUS="select()" ONCHANGE="return vTime(this,0,this)" MAXLENGTH="12" SIZE="12" >
    </TD>
  </TR>
  <TR >
    <TD CLASS="strcol" >Day</TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="TEXT" NAME="ProviderJobs_CronDay_1" VALUE="<<ProviderJobs_CronDay_1>>" ONFOCUS="select()" ONCHANGE="return vNum(this,1,31)" SIZE="10" >
    </TD>
  </TR>
  <TR >
    <TD CLASS="strcol" >Month</TD>
    <TD CLASS="strcol" >
      <SELECT NAME="ProviderJobs_CronMonth_1">
        [[DBA->selxTable(%form+xMonths+<<ProviderJobs_CronMonth_1>>+ID Descr+1)]]
      </SELECT> 
    </TD>
  </TR>
  <TR >
    <TD CLASS="strcol" >Day Of the Week</TD>
    <TD CLASS="strcol" >
      <SELECT NAME="ProviderJobs_CronWeek_1">
        [[DBA->selxTable(%form+xDaysOfWeek+<<ProviderJobs_CronWeek_1>>+ID Descr)]]
      </SELECT> 
    </TD>
  </TR>
  <TR >
    <TD CLASS="strcol" >Command</TD>
    <TD CLASS="strcol" >
      <SELECT NAME="ProviderJobs_Command_1">
        [[DBA->selxTable(%form+xCronJobs+<<ProviderJobs_Command_1>>+ID Descr)]]
      </SELECT> 
    </TD>
  </TR>
</TABLE>
<TABLE CLASS="main fullsize" >
  <TR>
    <TD CLASS="numcol" >
      <INPUT TYPE="submit" ONCLICK="return vDELETE('Are you sure you want to delete this record?');" NAME="ProviderJobs_DELETE_1=1&UpdateTables=all&misPOP=1" VALUE="Delete">
      <INPUT TYPE="submit" ONCLICK="return validate(this.form);" NAME="UpdateTables=all&misPOP=1" VALUE="Add/Update">
    </TD>
  </TR>
</TABLE>

<INPUT TYPE="hidden" NAME="post_update" VALUE="PostUpd->updCronJob(%form+<<<ProviderJobs_ID_1>>>)" >
</LOADHIDDEN>
</FORM>
<SCRIPT LANGUAGE="JavaScript">
document.ProviderJobs.elements[0].focus();
</SCRIPT>

[[myHTML->rightpane(%form+search)]]
