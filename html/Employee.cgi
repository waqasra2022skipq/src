[[myHTML->newPage(%form+Employee Information)]]

<SCRIPT LANGUAGE="JavaScript" SRC="/cgi/js/NoEnter.js"> </SCRIPT>
<SCRIPT LANGUAGE="JavaScript" SRC="/cgi/js/vEntry.js"> </SCRIPT>
<SCRIPT LANGUAGE="JavaScript" SRC="/cgi/js/vEmployee.js"> </SCRIPT>
<SCRIPT LANGUAGE="JavaScript" SRC="/cgi/js/vDate.js"> </SCRIPT>
<SCRIPT LANGUAGE="JavaScript" SRC="/cgi/js/vNum.js"> </SCRIPT>
<SCRIPT LANGUAGE="JavaScript" SRC="/cgi/js/vZip.js"> </SCRIPT>
<SCRIPT TYPE="text/javascript" SRC="/cgi/jquery/jquery-ui-1.11.2/jquery-ui.min.js" ></SCRIPT>
<SCRIPT type="text/javascript" src="/cgi/js/ajaxrequest.js"></SCRIPT>
<LINK HREF="/cgi/css/autocomplete.css?v=202008071708" REL="stylesheet">

<FORM NAME="Employee" ACTION="/cgi/bin/mis.cgi" METHOD="POST" >
<TABLE CLASS="main fullsize" >
  <TR >
    <TD CLASS="strcol" >
      <<<Provider_FName_1>>> <<<Provider_MName_1>>> <<<Provider_LName_1>>> 
      <BR>Employee Information
    </TD>
    <TD CLASS="numcol" >[[gHTML->setLINKS(%form+back)]]</TD>
  </TR>
</TABLE>
<TABLE CLASS="home fullsize" >
    <TR ><TD ><TABLE CLASS="home fullsize" >
  <TR ><TD CLASS="port hdrtxt" COLSPAN="4" >Employee Information</TD></TR>
 <TR >
    <TD CLASS="strcol" >Job Title</TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="text" NAME="Provider_JobTitle_1" VALUE="<<<Provider_JobTitle_1>>>" SIZE="50" />
    </TD>
    <TD CLASS="strcol" COLSPAN="2" >&nbsp;</TD>
  </TR>
  <TR >
    <TD CLASS="strcol" >Job Classification</TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="text" id="JobClassification_onet_search" SIZE="50" />
      <INPUT TYPE="hidden" NAME="Provider_JobClassification_1" VALUE="<<Provider_JobClassification_1>>" >
    </TD>
    <TD CLASS="strcol" COLSPAN="2" >
      <a href="https://www.onetonline.org/link/summary/<<Provider_JobClassification_1>>" target="_blank" id="JobClassification_onet_link">View in O*NET OnLine</a>
    </TD>
  </TR>

  [[NewCrop->setRole(%form+Agent)]]
  <TR >
    <TD CLASS="strcol" >Hire Date</TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="text" NAME="EmplInfo_HireDate_1" VALUE="<<EmplInfo_HireDate_1>>" ONFOCUS="select()" ONCHANGE="return vDate(this)" SIZE=10>
    </TD>
    <TD CLASS="strcol" COLSPAN="2" >&nbsp;</TD>
  </TR>
  <TR >
    <TD CLASS="strcol" >Begin Full Time Date</TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="text" NAME="EmplInfo_FullTimeDate_1" VALUE="<<EmplInfo_FullTimeDate_1>>" ONFOCUS="select()" ONCHANGE="return vDate(this)" SIZE=10>
    </TD>
    <TD CLASS="strcol" COLSPAN="2" >&nbsp;</TD>
  </TR>
  <TR >
    <TD CLASS="strcol" >Termination Date</TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="text" NAME="EmplInfo_TermDate_1" VALUE="<<EmplInfo_TermDate_1>>" ONFOCUS="select()" ONCHANGE="return vDate(this,1)" SIZE=10>
    </TD>
    <TD CLASS="strcol" COLSPAN="2" >&nbsp;</TD>
  </TR>
  <TR>
    <TD CLASS="strcol" >ALERT: Should there be an item of concern briefly identify the nature of the concern?</TD>
    <TD CLASS="strcol" >
      <TEXTAREA NAME="EmplInfo_Alert_1" COLS="80" ROWS="5" WRAP="virtual" ><<EmplInfo_Alert_1>></TEXTAREA>
    </TD>
  </TR>
  <TR ><TD CLASS="port hdrtxt" COLSPAN="4" >Contract Information</TD></TR>
  <TR >
    <TD CLASS="strcol" >Primary Care Physician</TD>
    <TD CLASS="strcol" >
      Search: <INPUT TYPE="text" ID="SearchPhysNPI" NAME="SearchPhysNPI" VALUE="" ONFOCUS="select()" ONCHANGE="callAjax('Physicians','<<ProviderControl_NPI_1>>','selPhysNPI','&name=ProviderControl_NPI_1&pattern='+this.value,'popup.pl');" SIZE="60" >
      <BR><SPAN ID="selPhysNPI"></SPAN>
    </TD>
    <TD CLASS="strcol" >Contract Zip</TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="text" NAME="ProviderControl_ContractZip_1" VALUE="<<ProviderControl_ContractZip_1>>" ONFOCUS="select()" MAXLENGTH="10" SIZE="10" ONCHANGE="return vZip(this)" >
      <BR>multiple contracts for <BR>Rendering NPI<BR>Provider only
    </TD>
  </TR>
  <TR >
    <TD CLASS="strcol" >CAQH #</TD>
    <TD CLASS="strcol" COLSPAN="3" >
      <INPUT TYPE="text" NAME="ProviderControl_CAQH_1" VALUE="<<ProviderControl_CAQH_1>>" ONFOCUS="select()" MAXLENGTH="12" SIZE="12" >
    </TD>
  </TR>
  <TR ><TD CLASS="port hdrtxt" COLSPAN="4" >File Information</TD></TR>
  <TR >
    <TD CLASS="strcol" >Resume</TD>
    <TD CLASS="strcol" COLSPAN="3" >
      <INPUT TYPE=radio NAME="EmplInfo_Resume_1" VALUE=1 <<EmplInfo_Resume_1=1>> > Yes
      <INPUT TYPE=radio NAME="EmplInfo_Resume_1" VALUE=0 <<EmplInfo_Resume_1=0>> > No
      <INPUT TYPE=radio NAME="EmplInfo_Resume_1" VALUE="N" <<EmplInfo_Resume_1=N>> > N/A
    </TD>
  <TR >
    <TD CLASS="strcol" >OSBI Check</TD>
    <TD CLASS="strcol" COLSPAN="3" >
      <INPUT TYPE=radio NAME="EmplInfo_OSBI_1" VALUE=1 <<EmplInfo_OSBI_1=1>> > Yes
      <INPUT TYPE=radio NAME="EmplInfo_OSBI_1" VALUE=0 <<EmplInfo_OSBI_1=0>> > No
      <INPUT TYPE=radio NAME="EmplInfo_OSBI_1" VALUE="N" <<EmplInfo_OSBI_1=N>> > N/A
    </TD>
  <TR >
    <TD CLASS="strcol" >Supervision Letter</TD>
    <TD CLASS="strcol" >
      <INPUT TYPE=radio NAME="EmplInfo_Supervision_1" VALUE=1 <<EmplInfo_Supervision_1=1>> > Yes
      <INPUT TYPE=radio NAME="EmplInfo_Supervision_1" VALUE=0 <<EmplInfo_Supervision_1=0>> > No
      <INPUT TYPE=radio NAME="EmplInfo_Supervision_1" VALUE="N" <<EmplInfo_Supervision_1=N>> > N/A
    </TD>
    <TD CLASS="strcol" COLSPAN="2" >
      [[SysAccess->verify(%form+Privilege=ProviderEDocs)<A HREF="javascript:ReportWindow('/cgi/bin/mis.cgi?view=ListProviderEDocs.cgi&Provider_ProvID=<<<Provider_ProvID>>>&mlt=<<<mlt>>>&misLINKS=<<<misLINKS>>>','ElecDocs')">View Document</A> ]]
      [[SysAccess->verify(%form+Privilege=ProviderEDocs)<A HREF="javascript:ReportWindow('/cgi/bin/mis.cgi?view=ListProviderEDocs.cgi&Provider_ProvID=<<<Provider_ProvID>>>&mlt=<<<mlt>>>&misLINKS=<<<misLINKS>>>','ElecDocs')">Add Document</A> ]]
    </TD>
  </TR>
  <TR >
    <TD CLASS="strcol" >Board License/Supervision Approval Letter</TD>
    <TD CLASS="strcol" >
      <INPUT TYPE=radio NAME="EmplInfo_DocOnFile_1" VALUE=1 <<EmplInfo_DocOnFile_1=1>> > Yes
      <INPUT TYPE=radio NAME="EmplInfo_DocOnFile_1" VALUE=0 <<EmplInfo_DocOnFile_1=0>> > No
      <INPUT TYPE=radio NAME="EmplInfo_DocOnFile_1" VALUE="N" <<EmplInfo_DocOnFile_1=N>> > N/A
    </TD>
    <TD CLASS="strcol" COLSPAN="2" >
      [[SysAccess->verify(%form+Privilege=ProviderEDocs)<A HREF="javascript:ReportWindow('/cgi/bin/mis.cgi?view=ListProviderEDocs.cgi&Provider_ProvID=<<<Provider_ProvID>>>&mlt=<<<mlt>>>&misLINKS=<<<misLINKS>>>','ElecDocs')">View Document</A> ]]
      [[SysAccess->verify(%form+Privilege=ProviderEDocs)<A HREF="javascript:ReportWindow('/cgi/bin/mis.cgi?view=ListProviderEDocs.cgi&Provider_ProvID=<<<Provider_ProvID>>>&mlt=<<<mlt>>>&misLINKS=<<<misLINKS>>>','ElecDocs')">Add Document</A> ]]
    </TD>
  </TR>
  <TR >
    <TD CLASS="strcol" >Diploma</TD>
    <TD CLASS="strcol" >
      <INPUT TYPE=radio NAME="EmplInfo_Diploma_1" VALUE=1 <<EmplInfo_Diploma_1=1>> > Yes
      <INPUT TYPE=radio NAME="EmplInfo_Diploma_1" VALUE=0 <<EmplInfo_Diploma_1=0>> > No
      <INPUT TYPE=radio NAME="EmplInfo_Diploma_1" VALUE="N" <<EmplInfo_Diploma_1=N>> > N/A
    </TD>
    <TD CLASS="strcol" COLSPAN="2" >
      [[SysAccess->verify(%form+Privilege=ProviderEDocs)<A HREF="javascript:ReportWindow('/cgi/bin/mis.cgi?view=ListProviderEDocs.cgi&Provider_ProvID=<<<Provider_ProvID>>>&mlt=<<<mlt>>>&misLINKS=<<<misLINKS>>>','ElecDocs')">View Document</A> ]]
      [[SysAccess->verify(%form+Privilege=ProviderEDocs)<A HREF="javascript:ReportWindow('/cgi/bin/mis.cgi?view=ListProviderEDocs.cgi&Provider_ProvID=<<<Provider_ProvID>>>&mlt=<<<mlt>>>&misLINKS=<<<misLINKS>>>','ElecDocs')">Add Document</A> ]]
    </TD>
  </TR>
  <TR >
    <TD CLASS="strcol" >Transcript</TD>
    <TD CLASS="strcol" >
      <INPUT TYPE=radio NAME="EmplInfo_Transcript_1" VALUE=1 <<EmplInfo_Transcript_1=1>> > Yes
      <INPUT TYPE=radio NAME="EmplInfo_Transcript_1" VALUE=0 <<EmplInfo_Transcript_1=0>> > No
      <INPUT TYPE=radio NAME="EmplInfo_Transcript_1" VALUE="N" <<EmplInfo_Transcript_1=N>> > N/A
    </TD>
    <TD CLASS="strcol" COLSPAN="2" >
      [[SysAccess->verify(%form+Privilege=ProviderEDocs)<A HREF="javascript:ReportWindow('/cgi/bin/mis.cgi?view=ListProviderEDocs.cgi&Provider_ProvID=<<<Provider_ProvID>>>&mlt=<<<mlt>>>&misLINKS=<<<misLINKS>>>','ElecDocs')">View Document</A> ]]
      [[SysAccess->verify(%form+Privilege=ProviderEDocs)<A HREF="javascript:ReportWindow('/cgi/bin/mis.cgi?view=ListProviderEDocs.cgi&Provider_ProvID=<<<Provider_ProvID>>>&mlt=<<<mlt>>>&misLINKS=<<<misLINKS>>>','ElecDocs')">Add Document</A> ]]
    </TD>
  </TR>
  <TR >
    <TD CLASS="strcol" >Credentialing Form</TD>
    <TD CLASS="strcol" >
      <INPUT TYPE=radio NAME="EmplInfo_Credential_1" VALUE=1 <<EmplInfo_Credential_1=1>> > Yes
      <INPUT TYPE=radio NAME="EmplInfo_Credential_1" VALUE=0 <<EmplInfo_Credential_1=0>> > No
      <INPUT TYPE=radio NAME="EmplInfo_Credential_1" VALUE="N" <<EmplInfo_Credential_1=N>> > N/A
    </TD>
    <TD CLASS="strcol" COLSPAN="2" >
      [[SysAccess->verify(%form+Privilege=ProviderEDocs)<A HREF="javascript:ReportWindow('/cgi/bin/mis.cgi?view=ListProviderEDocs.cgi&Provider_ProvID=<<<Provider_ProvID>>>&mlt=<<<mlt>>>&misLINKS=<<<misLINKS>>>','ElecDocs')">View Document</A> ]]
      [[SysAccess->verify(%form+Privilege=ProviderEDocs)<A HREF="javascript:ReportWindow('/cgi/bin/mis.cgi?view=ListProviderEDocs.cgi&Provider_ProvID=<<<Provider_ProvID>>>&mlt=<<<mlt>>>&misLINKS=<<<misLINKS>>>','ElecDocs')">Add Document</A> ]]
    </TD>
  </TR>
  <TR >
    <TD CLASS="strcol" >Code of Ethics Form</TD>
    <TD CLASS="strcol" >
      <INPUT TYPE=radio NAME="EmplInfo_CodeOfEthics_1" VALUE=1 <<EmplInfo_CodeOfEthics_1=1>> > Yes
      <INPUT TYPE=radio NAME="EmplInfo_CodeOfEthics_1" VALUE=0 <<EmplInfo_CodeOfEthics_1=0>> > No
      <INPUT TYPE=radio NAME="EmplInfo_CodeOfEthics_1" VALUE="N" <<EmplInfo_CodeOfEthics_1=N>> > N/A
    </TD>
    <TD CLASS="strcol" COLSPAN="2" >
      [[SysAccess->verify(%form+Privilege=ProviderEDocs)<A HREF="javascript:ReportWindow('/cgi/bin/mis.cgi?view=ListProviderEDocs.cgi&Provider_ProvID=<<<Provider_ProvID>>>&mlt=<<<mlt>>>&misLINKS=<<<misLINKS>>>','ElecDocs')">View Document</A> ]]
      [[SysAccess->verify(%form+Privilege=ProviderEDocs)<A HREF="javascript:ReportWindow('/cgi/bin/mis.cgi?view=ListProviderEDocs.cgi&Provider_ProvID=<<<Provider_ProvID>>>&mlt=<<<mlt>>>&misLINKS=<<<misLINKS>>>','ElecDocs')">Add Document</A> ]]
    </TD>
  </TR>
  <TR >
    <TD CLASS="strcol" >Job Description</TD>
    <TD CLASS="strcol" >
      <INPUT TYPE=radio NAME="EmplInfo_JobDescr_1" VALUE=1 <<EmplInfo_JobDescr_1=1>> > Yes
      <INPUT TYPE=radio NAME="EmplInfo_JobDescr_1" VALUE=0 <<EmplInfo_JobDescr_1=0>> > No
      <INPUT TYPE=radio NAME="EmplInfo_JobDescr_1" VALUE="N" <<EmplInfo_JobDescr_1=N>> > N/A
    </TD>
    <TD CLASS="strcol" COLSPAN="2" >
      [[SysAccess->verify(%form+Privilege=ProviderEDocs)<A HREF="javascript:ReportWindow('/cgi/bin/mis.cgi?view=ListProviderEDocs.cgi&Provider_ProvID=<<<Provider_ProvID>>>&mlt=<<<mlt>>>&misLINKS=<<<misLINKS>>>','ElecDocs')">View Document</A> ]]
      [[SysAccess->verify(%form+Privilege=ProviderEDocs)<A HREF="javascript:ReportWindow('/cgi/bin/mis.cgi?view=ListProviderEDocs.cgi&Provider_ProvID=<<<Provider_ProvID>>>&mlt=<<<mlt>>>&misLINKS=<<<misLINKS>>>','ElecDocs')">Add Document</A> ]]
    </TD>
  </TR>
  <TR >
    <TD CLASS="strcol" >New Hire Form</TD>
    <TD CLASS="strcol" >
      <INPUT TYPE=radio NAME="EmplInfo_HireForm_1" VALUE=1 <<EmplInfo_HireForm_1=1>> > Yes
      <INPUT TYPE=radio NAME="EmplInfo_HireForm_1" VALUE=0 <<EmplInfo_HireForm_1=0>> > No
      <INPUT TYPE=radio NAME="EmplInfo_HireForm_1" VALUE="N" <<EmplInfo_HireForm_1=N>> > N/A
    </TD>
    <TD CLASS="strcol" COLSPAN="2" >
      [[SysAccess->verify(%form+Privilege=ProviderEDocs)<A HREF="javascript:ReportWindow('/cgi/bin/mis.cgi?view=ListProviderEDocs.cgi&Provider_ProvID=<<<Provider_ProvID>>>&mlt=<<<mlt>>>&misLINKS=<<<misLINKS>>>','ElecDocs')">View Document</A> ]]
      [[SysAccess->verify(%form+Privilege=ProviderEDocs)<A HREF="javascript:ReportWindow('/cgi/bin/mis.cgi?view=ListProviderEDocs.cgi&Provider_ProvID=<<<Provider_ProvID>>>&mlt=<<<mlt>>>&misLINKS=<<<misLINKS>>>','ElecDocs')">Add Document</A> ]]
    </TD>
  </TR>
  <TR >
    <TD CLASS="strcol" >New Employee Information/Orientation</TD>
    <TD CLASS="strcol" >
      <INPUT TYPE=radio NAME="EmplInfo_InfoForm_1" VALUE=1 <<EmplInfo_InfoForm_1=1>> > Yes
      <INPUT TYPE=radio NAME="EmplInfo_InfoForm_1" VALUE=0 <<EmplInfo_InfoForm_1=0>> > No
      <INPUT TYPE=radio NAME="EmplInfo_InfoForm_1" VALUE="N" <<EmplInfo_InfoForm_1=N>> > N/A
    </TD>
    <TD CLASS="strcol" COLSPAN="2" >
      [[SysAccess->verify(%form+Privilege=ProviderEDocs)<A HREF="javascript:ReportWindow('/cgi/bin/mis.cgi?view=ListProviderEDocs.cgi&Provider_ProvID=<<<Provider_ProvID>>>&mlt=<<<mlt>>>&misLINKS=<<<misLINKS>>>','ElecDocs')">View Document</A> ]]
      [[SysAccess->verify(%form+Privilege=ProviderEDocs)<A HREF="javascript:ReportWindow('/cgi/bin/mis.cgi?view=ListProviderEDocs.cgi&Provider_ProvID=<<<Provider_ProvID>>>&mlt=<<<mlt>>>&misLINKS=<<<misLINKS>>>','ElecDocs')">Add Document</A> ]]
    </TD>
  </TR>
  <TR >
    <TD CLASS="strcol" >Employee Agreement/Contract</TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="text" NAME="EmplInfo_AgreeDate_1" VALUE="<<EmplInfo_AgreeDate_1>>" ONFOCUS="select()" ONCHANGE="return vDate(this,1)" SIZE=10>
    </TD>
    <TD CLASS="strcol" COLSPAN="2" >
      [[SysAccess->verify(%form+Privilege=ProviderEDocs)<A HREF="javascript:ReportWindow('/cgi/bin/mis.cgi?view=ListProviderEDocs.cgi&Provider_ProvID=<<<Provider_ProvID>>>&mlt=<<<mlt>>>&misLINKS=<<<misLINKS>>>','ElecDocs')">View Document</A> ]]
      [[SysAccess->verify(%form+Privilege=ProviderEDocs)<A HREF="javascript:ReportWindow('/cgi/bin/mis.cgi?view=ListProviderEDocs.cgi&Provider_ProvID=<<<Provider_ProvID>>>&mlt=<<<mlt>>>&misLINKS=<<<misLINKS>>>','ElecDocs')">Add Document</A> ]]
    </TD>
  </TR>
  <TR >
    <TD CLASS="strcol" >Evaluation Due</TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="text" NAME="EmplInfo_EvalDate_1" VALUE="<<EmplInfo_EvalDate_1>>" ONFOCUS="select()" ONCHANGE="return vDate(this,1)" SIZE=10>
    </TD>
    <TD CLASS="strcol" COLSPAN="2" >&nbsp;</TD>
  </TR>
  <TR >
    <TD CLASS="strcol" >SSN on file</TD>
    <TD CLASS="strcol" >
      <INPUT TYPE=radio NAME="EmplInfo_SSNonFile_1" VALUE=1 <<EmplInfo_SSNonFile_1=1>> > Yes
      <INPUT TYPE=radio NAME="EmplInfo_SSNonFile_1" VALUE=0 <<EmplInfo_SSNonFile_1=0>> > No
      <INPUT TYPE=radio NAME="EmplInfo_SSNonFile_1" VALUE="N" <<EmplInfo_SSNonFile_1=N>> > N/A
    </TD>
    <TD CLASS="strcol" COLSPAN="2" >
      [[SysAccess->verify(%form+Privilege=ProviderEDocs)<A HREF="javascript:ReportWindow('/cgi/bin/mis.cgi?view=ListProviderEDocs.cgi&Provider_ProvID=<<<Provider_ProvID>>>&mlt=<<<mlt>>>&misLINKS=<<<misLINKS>>>','ElecDocs')">View Document</A> ]]
      [[SysAccess->verify(%form+Privilege=ProviderEDocs)<A HREF="javascript:ReportWindow('/cgi/bin/mis.cgi?view=ListProviderEDocs.cgi&Provider_ProvID=<<<Provider_ProvID>>>&mlt=<<<mlt>>>&misLINKS=<<<misLINKS>>>','ElecDocs')">Add Document</A> ]]
    </TD>
  </TR>
  <TR >
    <TD CLASS="strcol" >I9</TD>
    <TD CLASS="strcol" >
      <INPUT TYPE=radio NAME="EmplInfo_I9_1" VALUE=1 <<EmplInfo_I9_1=1>> > Yes
      <INPUT TYPE=radio NAME="EmplInfo_I9_1" VALUE=0 <<EmplInfo_I9_1=0>> > No
      <INPUT TYPE=radio NAME="EmplInfo_I9_1" VALUE="N" <<EmplInfo_I9_1=N>> > N/A
    </TD>
    <TD CLASS="strcol" COLSPAN="2" >
      [[SysAccess->verify(%form+Privilege=ProviderEDocs)<A HREF="javascript:ReportWindow('/cgi/bin/mis.cgi?view=ListProviderEDocs.cgi&Provider_ProvID=<<<Provider_ProvID>>>&mlt=<<<mlt>>>&misLINKS=<<<misLINKS>>>','ElecDocs')">View Document</A> ]]
      [[SysAccess->verify(%form+Privilege=ProviderEDocs)<A HREF="javascript:ReportWindow('/cgi/bin/mis.cgi?view=ListProviderEDocs.cgi&Provider_ProvID=<<<Provider_ProvID>>>&mlt=<<<mlt>>>&misLINKS=<<<misLINKS>>>','ElecDocs')">Add Document</A> ]]
    </TD>
  </TR>
  <TR >
    <TD CLASS="strcol" >E-Verify</TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="text" NAME="EmplInfo_EVerify_1" VALUE="<<EmplInfo_EVerify_1>>" ONFOCUS="select()" SIZE=50>
    </TD>
    <TD CLASS="strcol" COLSPAN="2" >&nbsp;</TD>
  </TR>
  <TR >
    <TD CLASS="strcol" >Driver License #</TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="text" NAME="EmplInfo_DLNum_1" VALUE="<<EmplInfo_DLNum_1>>" ONFOCUS="select()" SIZE=12>
    </TD>
    <TD CLASS="strcol" COLSPAN="2" >
      [[SysAccess->verify(%form+Privilege=ProviderEDocs)<A HREF="javascript:ReportWindow('/cgi/bin/mis.cgi?view=ListProviderEDocs.cgi&Provider_ProvID=<<<Provider_ProvID>>>&mlt=<<<mlt>>>&misLINKS=<<<misLINKS>>>','ElecDocs')">View Document</A> ]]
      [[SysAccess->verify(%form+Privilege=ProviderEDocs)<A HREF="javascript:ReportWindow('/cgi/bin/mis.cgi?view=ListProviderEDocs.cgi&Provider_ProvID=<<<Provider_ProvID>>>&mlt=<<<mlt>>>&misLINKS=<<<misLINKS>>>','ElecDocs')">Add Document</A> ]]
    </TD>
  </TR>
  <TR >
    <TD CLASS="strcol" ></TD>
    <TD CLASS="strcol" >
      <SELECT NAME="EmplInfo_ST_1">
        [[DBA->selxTable(%form+xState+<<EmplInfo_ST_1>>+Descr)]]
      </SELECT>
    </TD>
    <TD CLASS="strcol" COLSPAN="2" >&nbsp;</TD>
  </TR>
  <TR >
    <TD CLASS="strcol" >Driver License Expires</TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="text" NAME="EmplInfo_DLExpDate_1" VALUE="<<EmplInfo_DLExpDate_1>>" ONFOCUS="select()" ONCHANGE="return vDate(this)" SIZE=10>
    </TD>
    <TD CLASS="strcol" COLSPAN="2" >&nbsp;</TD>
  </TR>
<TR >
    <TD CLASS="strcol" >OHCA Contract Expires</TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="text" NAME="EmplInfo_OHCAExpDate_1" VALUE="<<EmplInfo_OHCAExpDate_1>>" ONFOCUS="select()" ONCHANGE="return vDate(this)" SIZE=10>
    </TD>
    <TD CLASS="strcol" COLSPAN="2" >&nbsp;</TD>
  </TR>
  <TR >
    <TD CLASS="strcol" >Auto Insurance Expires</TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="text" NAME="EmplInfo_AutoExpDate_1" VALUE="<<EmplInfo_AutoExpDate_1>>" ONFOCUS="select()" ONCHANGE="return vDate(this)" SIZE=10>
    </TD>
    <TD CLASS="strcol" COLSPAN="2" >&nbsp;</TD>
  </TR>
  <TR >
    <TD CLASS="strcol" >Professional Liability Carrier</TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="text" NAME="EmplInfo_Carrier_1" VALUE="<<EmplInfo_Carrier_1>>" ONFOCUS="select()" SIZE=50>
    </TD>
    <TD CLASS="strcol" COLSPAN="2" >&nbsp;</TD>
  </TR>
  <TR >
    <TD CLASS="strcol" >Professional Liability Policy #</TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="text" NAME="EmplInfo_PolicyNum_1" VALUE="<<EmplInfo_PolicyNum_1>>" ONFOCUS="select()" SIZE=50>
    </TD>
    <TD CLASS="strcol" COLSPAN="2" >
      [[SysAccess->verify(%form+Privilege=ProviderEDocs)<A HREF="javascript:ReportWindow('/cgi/bin/mis.cgi?view=ListProviderEDocs.cgi&Provider_ProvID=<<<Provider_ProvID>>>&mlt=<<<mlt>>>&misLINKS=<<<misLINKS>>>','ElecDocs')">View Document</A> ]]
      [[SysAccess->verify(%form+Privilege=ProviderEDocs)<A HREF="javascript:ReportWindow('/cgi/bin/mis.cgi?view=ListProviderEDocs.cgi&Provider_ProvID=<<<Provider_ProvID>>>&mlt=<<<mlt>>>&misLINKS=<<<misLINKS>>>','ElecDocs')">Add Document</A> ]]
    </TD>
  </TR>
  <TR >
    <TD CLASS="strcol" >Professional Liability Expires</TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="text" NAME="EmplInfo_PolicyNumExpDate_1" VALUE="<<EmplInfo_PolicyNumExpDate_1>>" ONFOCUS="select()" ONCHANGE="return vDate(this)" SIZE=10>
    </TD>
    <TD CLASS="strcol" COLSPAN="2" >&nbsp;</TD>
  </TR>
  <TR >
    <TD CLASS="strcol" >Professional Liability Occurrence Limit</TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="text" NAME="EmplInfo_OccLimit_1" VALUE="<<EmplInfo_OccLimit_1>>" ONFOCUS="select()" ONCHANGE="return vNum(this,0,10000000)" SIZE=10>
    </TD>
    <TD CLASS="strcol" COLSPAN="2" >&nbsp;</TD>
  </TR>
  <TR >
    <TD CLASS="strcol" >Professional Liability Aggregate</TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="text" NAME="EmplInfo_Aggregate_1" VALUE="<<EmplInfo_Aggregate_1>>" ONFOCUS="select()" ONCHANGE="return vNum(this,0,10000000)" SIZE=10>
    </TD>
    <TD CLASS="strcol" COLSPAN="2" >&nbsp;</TD>
  </TR>
  <TR >
    <TD CLASS="strcol" >W4</TD>
    <TD CLASS="strcol" >
      <INPUT TYPE=radio NAME="EmplInfo_W4_1" VALUE=1 <<EmplInfo_W4_1=1>> > Yes
      <INPUT TYPE=radio NAME="EmplInfo_W4_1" VALUE=0 <<EmplInfo_W4_1=0>> > No
      <INPUT TYPE=radio NAME="EmplInfo_W4_1" VALUE="N" <<EmplInfo_W4_1=N>> > N/A
    </TD>
    <TD CLASS="strcol" COLSPAN="2" >
      [[SysAccess->verify(%form+Privilege=ProviderEDocs)<A HREF="javascript:ReportWindow('/cgi/bin/mis.cgi?view=ListProviderEDocs.cgi&Provider_ProvID=<<<Provider_ProvID>>>&mlt=<<<mlt>>>&misLINKS=<<<misLINKS>>>','ElecDocs')">View Document</A> ]]
      [[SysAccess->verify(%form+Privilege=ProviderEDocs)<A HREF="javascript:ReportWindow('/cgi/bin/mis.cgi?view=ListProviderEDocs.cgi&Provider_ProvID=<<<Provider_ProvID>>>&mlt=<<<mlt>>>&misLINKS=<<<misLINKS>>>','ElecDocs')">Add Document</A> ]]
    </TD>
  </TR>
  <TR >
    <TD CLASS="strcol" >Tax status</TD>
    <TD CLASS="strcol" >
      <SELECT NAME="EmplInfo_TaxStatus_1">
        [[DBA->selxTable(%form+xTaxStatus+<<EmplInfo_TaxStatus_1>>+Descr)]]
      </SELECT> 
    </TD>
    <TD CLASS="strcol" COLSPAN="2" >&nbsp;</TD>
  </TR>
  <TR >
    <TD CLASS="strcol" >Allowances</TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="text" NAME="EmplInfo_TaxAllows_1" VALUE="<<EmplInfo_TaxAllows_1>>" ONFOCUS="select()" ONCHANGE="return vNum(this,0,19)" SIZE=10>
    </TD>
    <TD CLASS="strcol" COLSPAN="2" >&nbsp;</TD>
  </TR>
  <TR >
    <TD CLASS="strcol" >Additional Tax withheld</TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="text" NAME="EmplInfo_TaxWithheld_1" VALUE="<<EmplInfo_TaxWithheld_1>>" ONFOCUS="select()" ONCHANGE="return vNum(this,0,1000)" SIZE=10>
    </TD>
    <TD CLASS="strcol" COLSPAN="2" >&nbsp;</TD>
  </TR>
  <TR >
    <TD CLASS="strcol" >W9</TD>
    <TD CLASS="strcol" >
      <INPUT TYPE=radio NAME="EmplInfo_W9_1" VALUE=1 <<EmplInfo_W9_1=1>> > Yes
      <INPUT TYPE=radio NAME="EmplInfo_W9_1" VALUE=0 <<EmplInfo_W9_1=0>> > No
      <INPUT TYPE=radio NAME="EmplInfo_W9_1" VALUE="N" <<EmplInfo_W9_1=N>> > N/A
    </TD>
    <TD CLASS="strcol" COLSPAN="2" >
      [[SysAccess->verify(%form+Privilege=ProviderEDocs)<A HREF="javascript:ReportWindow('/cgi/bin/mis.cgi?view=ListProviderEDocs.cgi&Provider_ProvID=<<<Provider_ProvID>>>&mlt=<<<mlt>>>&misLINKS=<<<misLINKS>>>','ElecDocs')">View Document</A> ]]
      [[SysAccess->verify(%form+Privilege=ProviderEDocs)<A HREF="javascript:ReportWindow('/cgi/bin/mis.cgi?view=ListProviderEDocs.cgi&Provider_ProvID=<<<Provider_ProvID>>>&mlt=<<<mlt>>>&misLINKS=<<<misLINKS>>>','ElecDocs')">Add Document</A> ]]
    </TD>
  </TR>
  <TR >
    <TD CLASS="strcol" >Workers Comp Certificate of New Coverage</TD>
    <TD CLASS="strcol" >
      <INPUT TYPE=radio NAME="EmplInfo_WorkersComp_1" VALUE=1 <<EmplInfo_WorkersComp_1=1>> > Yes
      <INPUT TYPE=radio NAME="EmplInfo_WorkersComp_1" VALUE=0 <<EmplInfo_WorkersComp_1=0>> > No
      <INPUT TYPE=radio NAME="EmplInfo_WorkersComp_1" VALUE="N" <<EmplInfo_WorkersComp_1=N>> > N/A
    </TD>
    <TD CLASS="strcol" COLSPAN="2" >
      [[SysAccess->verify(%form+Privilege=ProviderEDocs)<A HREF="javascript:ReportWindow('/cgi/bin/mis.cgi?view=ListProviderEDocs.cgi&Provider_ProvID=<<<Provider_ProvID>>>&mlt=<<<mlt>>>&misLINKS=<<<misLINKS>>>','ElecDocs')">View Document</A> ]]
      [[SysAccess->verify(%form+Privilege=ProviderEDocs)<A HREF="javascript:ReportWindow('/cgi/bin/mis.cgi?view=ListProviderEDocs.cgi&Provider_ProvID=<<<Provider_ProvID>>>&mlt=<<<mlt>>>&misLINKS=<<<misLINKS>>>','ElecDocs')">Add Document</A> ]]
    </TD>
  </TR>
  <TR >
    <TD CLASS="strcol" >Health Insurance Enrollment</TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="text" NAME="EmplInfo_InsuranceEnroll_1" VALUE="<<EmplInfo_InsuranceEnroll_1>>" ONFOCUS="select()" SIZE=50>
    </TD>
    <TD CLASS="strcol" COLSPAN="2" >&nbsp;</TD>
  </TR>
  <TR >
    <TD CLASS="strcol" >Payroll Set Up</TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="text" NAME="EmplInfo_Payroll_1" VALUE="<<EmplInfo_Payroll_1>>" ONFOCUS="select()" SIZE=50>
    </TD>
    <TD CLASS="strcol" COLSPAN="2" >&nbsp;</TD>
  </TR>
  <TR >
    <TD CLASS="strcol" >Intuit Set Up</TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="text" NAME="EmplInfo_Intuit_1" VALUE="<<EmplInfo_Intuit_1>>" ONFOCUS="select()" SIZE=50>
    </TD>
    <TD CLASS="strcol" COLSPAN="2" >&nbsp;</TD>
  </TR>
  <TR >
    <TD CLASS="strcol" >T-Sheets Set Up</TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="text" NAME="EmplInfo_TSheets_1" VALUE="<<EmplInfo_TSheets_1>>" ONFOCUS="select()" SIZE=50>
    </TD>
    <TD CLASS="strcol" COLSPAN="2" >&nbsp;</TD>
  </TR>
  <TR >
    <TD CLASS="strcol" >CPR Expires (Adult)</TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="text" NAME="EmplInfo_CPRAdultExpDate_1" VALUE="<<EmplInfo_CPRAdultExpDate_1>>" ONFOCUS="select()" ONCHANGE="return vDate(this,1)" SIZE=10>
    </TD>
    <TD CLASS="strcol" COLSPAN="2" >
      [[SysAccess->verify(%form+Privilege=ProviderEDocs)<A HREF="javascript:ReportWindow('/cgi/bin/mis.cgi?view=ListProviderEDocs.cgi&Provider_ProvID=<<<Provider_ProvID>>>&mlt=<<<mlt>>>&misLINKS=<<<misLINKS>>>','ElecDocs')">View Document</A> ]]
      [[SysAccess->verify(%form+Privilege=ProviderEDocs)<A HREF="javascript:ReportWindow('/cgi/bin/mis.cgi?view=ListProviderEDocs.cgi&Provider_ProvID=<<<Provider_ProvID>>>&mlt=<<<mlt>>>&misLINKS=<<<misLINKS>>>','ElecDocs')">Add Document</A> ]]
    </TD>
  </TR>
  <TR >
    <TD CLASS="strcol" >CPR Expires (Child)</TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="text" NAME="EmplInfo_CPRChildExpDate_1" VALUE="<<EmplInfo_CPRChildExpDate_1>>" ONFOCUS="select()" ONCHANGE="return vDate(this,1)" SIZE=10>
    </TD>
    <TD CLASS="strcol" COLSPAN="2" >
      [[SysAccess->verify(%form+Privilege=ProviderEDocs)<A HREF="javascript:ReportWindow('/cgi/bin/mis.cgi?view=ListProviderEDocs.cgi&Provider_ProvID=<<<Provider_ProvID>>>&mlt=<<<mlt>>>&misLINKS=<<<misLINKS>>>','ElecDocs')">View Document</A> ]]
      [[SysAccess->verify(%form+Privilege=ProviderEDocs)<A HREF="javascript:ReportWindow('/cgi/bin/mis.cgi?view=ListProviderEDocs.cgi&Provider_ProvID=<<<Provider_ProvID>>>&mlt=<<<mlt>>>&misLINKS=<<<misLINKS>>>','ElecDocs')">Add Document</A> ]]
    </TD>
  </TR>
  <TR >
    <TD CLASS="strcol" >First Aid Expires</TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="text" NAME="EmplInfo_FirstAidExpDate_1" VALUE="<<EmplInfo_FirstAidExpDate_1>>" ONFOCUS="select()" ONCHANGE="return vDate(this,1)" SIZE=10>
    </TD>
    <TD CLASS="strcol" COLSPAN="2" >
      [[SysAccess->verify(%form+Privilege=ProviderEDocs)<A HREF="javascript:ReportWindow('/cgi/bin/mis.cgi?view=ListProviderEDocs.cgi&Provider_ProvID=<<<Provider_ProvID>>>&mlt=<<<mlt>>>&misLINKS=<<<misLINKS>>>','ElecDocs')">View Document</A> ]]
      [[SysAccess->verify(%form+Privilege=ProviderEDocs)<A HREF="javascript:ReportWindow('/cgi/bin/mis.cgi?view=ListProviderEDocs.cgi&Provider_ProvID=<<<Provider_ProvID>>>&mlt=<<<mlt>>>&misLINKS=<<<misLINKS>>>','ElecDocs')">Add Document</A> ]]
    </TD>
  </TR>
  <TR >
    <TD CLASS="strcol" >CPI Expires</TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="text" NAME="EmplInfo_CPIExpDate_1" VALUE="<<EmplInfo_CPIExpDate_1>>" ONFOCUS="select()" ONCHANGE="return vDate(this,1)" SIZE=10>
    </TD>
    <TD CLASS="strcol" COLSPAN="2" >
      [[SysAccess->verify(%form+Privilege=ProviderEDocs)<A HREF="javascript:ReportWindow('/cgi/bin/mis.cgi?view=ListProviderEDocs.cgi&Provider_ProvID=<<<Provider_ProvID>>>&mlt=<<<mlt>>>&misLINKS=<<<misLINKS>>>','ElecDocs')">View Document</A> ]]
      [[SysAccess->verify(%form+Privilege=ProviderEDocs)<A HREF="javascript:ReportWindow('/cgi/bin/mis.cgi?view=ListProviderEDocs.cgi&Provider_ProvID=<<<Provider_ProvID>>>&mlt=<<<mlt>>>&misLINKS=<<<misLINKS>>>','ElecDocs')">Add Document</A> ]]
    </TD>
  </TR>
  <TR >
    <TD CLASS="strcol" >Mandt Expires</TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="text" NAME="EmplInfo_MandtExpDate_1" VALUE="<<EmplInfo_MandtExpDate_1>>" ONFOCUS="select()" ONCHANGE="return vDate(this,1)" SIZE=10>
    </TD>
    <TD CLASS="strcol" COLSPAN="2" >
      [[SysAccess->verify(%form+Privilege=ProviderEDocs)<A HREF="javascript:ReportWindow('/cgi/bin/mis.cgi?view=ListProviderEDocs.cgi&Provider_ProvID=<<<Provider_ProvID>>>&mlt=<<<mlt>>>&misLINKS=<<<misLINKS>>>','ElecDocs')">View Document</A> ]]
      [[SysAccess->verify(%form+Privilege=ProviderEDocs)<A HREF="javascript:ReportWindow('/cgi/bin/mis.cgi?view=ListProviderEDocs.cgi&Provider_ProvID=<<<Provider_ProvID>>>&mlt=<<<mlt>>>&misLINKS=<<<misLINKS>>>','ElecDocs')">Add Document</A> ]]
    </TD>
  </TR>
  <TR >
    <TD CLASS="strcol" >Cape Expires</TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="text" NAME="EmplInfo_CapeExpDate_1" VALUE="<<EmplInfo_CapeExpDate_1>>" ONFOCUS="select()" ONCHANGE="return vDate(this,1)" SIZE=10>
    </TD>
    <TD CLASS="strcol" COLSPAN="2" >
      [[SysAccess->verify(%form+Privilege=ProviderEDocs)<A HREF="javascript:ReportWindow('/cgi/bin/mis.cgi?view=ListProviderEDocs.cgi&Provider_ProvID=<<<Provider_ProvID>>>&mlt=<<<mlt>>>&misLINKS=<<<misLINKS>>>','ElecDocs')">View Document</A> ]]
      [[SysAccess->verify(%form+Privilege=ProviderEDocs)<A HREF="javascript:ReportWindow('/cgi/bin/mis.cgi?view=ListProviderEDocs.cgi&Provider_ProvID=<<<Provider_ProvID>>>&mlt=<<<mlt>>>&misLINKS=<<<misLINKS>>>','ElecDocs')">Add Document</A> ]]
    </TD>
  </TR>
  <TR >
    <TD CLASS="strcol" >MAB Expires</TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="text" NAME="EmplInfo_MABExpDate_1" VALUE="<<EmplInfo_MABExpDate_1>>" ONFOCUS="select()" ONCHANGE="return vDate(this,1)" SIZE=10>
    </TD>
    <TD CLASS="strcol" COLSPAN="2" >
      [[SysAccess->verify(%form+Privilege=ProviderEDocs)<A HREF="javascript:ReportWindow('/cgi/bin/mis.cgi?view=ListProviderEDocs.cgi&Provider_ProvID=<<<Provider_ProvID>>>&mlt=<<<mlt>>>&misLINKS=<<<misLINKS>>>','ElecDocs')">View Document</A> ]]
      [[SysAccess->verify(%form+Privilege=ProviderEDocs)<A HREF="javascript:ReportWindow('/cgi/bin/mis.cgi?view=ListProviderEDocs.cgi&Provider_ProvID=<<<Provider_ProvID>>>&mlt=<<<mlt>>>&misLINKS=<<<misLINKS>>>','ElecDocs')">Add Document</A> ]]
    </TD>
  </TR>
  <TR >
    <TD CLASS="strcol" >Equipment out</TD>
    <TD CLASS="strcol" >
      <INPUT TYPE=radio NAME="EmplInfo_Equip_1" VALUE=1 <<EmplInfo_Equip_1=1>> > Yes
      <INPUT TYPE=radio NAME="EmplInfo_Equip_1" VALUE=0 <<EmplInfo_Equip_1=0>> > No
      <INPUT TYPE=radio NAME="EmplInfo_Equip_1" VALUE="N" <<EmplInfo_Equip_1=N>> > N/A
    </TD>
    <TD CLASS="strcol" COLSPAN="2" >&nbsp;</TD>
  </TR>
  <TR >
    <TD CLASS="strcol" >Appendix A Submitted</TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="text" NAME="EmplInfo_AppendixA_1" VALUE="<<EmplInfo_AppendixA_1>>" ONFOCUS="select()" SIZE=50>
    </TD>
    <TD CLASS="strcol" COLSPAN="2" >&nbsp;</TD>
  </TR>
  <TR >
    <TD CLASS="strcol" >Email Set Up</TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="EMAIL" NAME="EmplInfo_EmailSetUp_1" VALUE="<<EmplInfo_EmailSetUp_1>>" ONFOCUS="select()" SIZE=50>
    </TD>
    <TD CLASS="strcol" COLSPAN="2" >&nbsp;</TD>
  </TR>
  <TR >
    <TD CLASS="strcol" >Corporate Email Address</TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="EMAIL" NAME="EmplInfo_CorpEmail_1" VALUE="<<EmplInfo_CorpEmail_1>>" ONFOCUS="select()" SIZE=50>
    </TD>
    <TD CLASS="strcol" COLSPAN="2" >&nbsp;</TD>
  </TR>
  <TR >
    <TD CLASS="strcol" >HIPAA Training Completed</TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="text" NAME="EmplInfo_HIPAATraining_1" VALUE="<<EmplInfo_HIPAATraining_1>>" ONFOCUS="select()" SIZE=50>
    </TD>
    <TD CLASS="strcol" COLSPAN="2" >&nbsp;</TD>
  </TR>
  <TR ><TD CLASS="port hdrtxt" COLSPAN="4" >Additional Comments</TR>
  <TR >
    <TD CLASS="strcol" COLSPAN="4" >
      <TEXTAREA NAME="EmplInfo_Comments_1" COLS=80 ROWS=5 WRAP="virtual" ><<EmplInfo_Comments_1>></TEXTAREA>
    </TD>
  </TR>
  <TR ><TD CLASS="port hdrtxt" COLSPAN="4" >Provider System Control</TR>
  <TR>
    <TD CLASS="strcol" >Logout in Minutes</TD>
    <TD CLASS="strcol" COLSPAN="3">
      <INPUT TYPE="text" NAME="ProviderControl_minToLogOut_1" VALUE="<<ProviderControl_minToLogOut_1>>" ONFOCUS="select()" ONCHANGE="return vNum(this,1,60);" MAXLENGTH="5" SIZE="5" > default minutes for user to be timed out and logged out.
    </TD>
  </TR>
    </TABLE></TD></TR>
</TABLE>
<TABLE CLASS="main fullsize" >
  <TR>
    <TD CLASS="numcol" >
      <INPUT TYPE="submit" ONCLICK="return validate(this.form);" NAME="UpdateTables=all&misPOP=1" VALUE="Add/Update">
    </TD>
  </TR>
</TABLE>

<INPUT TYPE="hidden" NAME="post_update" VALUE="DBA->updProvider(%form)" >
</LOADHIDDEN>
</FORM>
<SCRIPT LANGUAGE="JavaScript">
document.Employee.elements[0].focus();
</SCRIPT>

[[myHTML->rightpane(%form+search)]]

<SCRIPT type="text/javascript" src="/cgi/js/vMCAutocomplete.js?v=202006082124"></SCRIPT>
<SCRIPT LANGUAGE="JavaScript" src="/cgi/onet/OnetWebService.js"></SCRIPT>
<SCRIPT LANGUAGE="JavaScript" src="/cgi/js/vOnetKeywordSearch.js?v=202008070756"></SCRIPT>
<SCRIPT LANGUAGE="JavaScript" >
  callAjax('Physicians','<<ProviderControl_NPI_1>>','selPhysNPI','&name=ProviderControl_NPI_1','popup.pl');
$(document).ready(function() {
  onetAutocomplete('JobClassification_onet_search', 'Provider_JobClassification_1', 'JobClassification_onet_link');
  callAjax('getOccupationInfo','<<Provider_JobClassification_1>>','JobClassification_onet_search','','onet.pl')
});
</SCRIPT>
