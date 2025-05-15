[[myHTML->newPage(%form+Client Procedure)]]

<SCRIPT LANGUAGE="JavaScript" SRC="/src/cgi/js/vEntry.js"> </SCRIPT>
<SCRIPT LANGUAGE="JavaScript" SRC="/src/cgi/js/vClientProcedure.js"> </SCRIPT>
<SCRIPT LANGUAGE="JavaScript" SRC="/src/cgi/js/vDate.js"> </SCRIPT>
<SCRIPT type="text/javascript" src="/src/cgi/js/ajaxrequest.js"></SCRIPT>

<FORM NAME="ClientProcedure" ACTION="/cgi/bin/mis.cgi" METHOD="POST" >
<TABLE CLASS="main fullsize" >
  <TR >
    <TD CLASS="strcol" >
      <<<Client_FName_1>>> <<<Client_MName_1>>> <<<Client_LName_1>>> (<<<Client_ClientID_1>>>) <<<Client_SSN_1>>>
      <BR>
      Client Procedure
    </TD>
    <TD CLASS="numcol" >[[gHTML->setLINKS(%form+back)]]</TD>
  </TR>
</TABLE>
<TABLE CLASS="home fullsize" >
  <TR ><TD CLASS="port hdrtxt" COLSPAN="2" >Procedure Information and Resources [<<ClientProcedures_TrID_1>>]</TD></TR>
  <TR >
    <TD CLASS="strcol" >Procedure</TD>
    <TD CLASS="strcol" >
      Search: <INPUT TYPE="text" ID="SearchProcedure" NAME="SearchProcedure" VALUE="" ONFOCUS="select()" ONCHANGE="callAjax('Procedure','<<ClientProcedures_ProcedureID_1>>','selProcedure','&name=ClientProcedures_ProcedureID_1&pattern='+this.value,'popup.pl');" SIZE="60" >
<BR><SPAN ID="selProcedure"></SPAN>
    </TD>
  </TR>
  <TR >
    <TD CLASS="strcol" >Rejected Reason</TD>
    <TD CLASS="strcol" >
      <SELECT NAME="ClientProcedures_Rejected_1">
        [[DBA->selxTable(%form+xProcedureRejected+<<ClientProcedures_Rejected_1>>+ConceptName ConceptCode)]]
      </SELECT>
    </TD>
  </TR>
  <TR >
    <TD CLASS="strcol" >Target</TD>
    <TD CLASS="strcol" >
      <SELECT NAME="ClientProcedures_TargetID_1" >
        [[DBA->selxTable(%form+xProcedureTarget+<<ClientProcedures_TargetID_1>>+ConceptName ConceptCode)]]
      </SELECT>
    </TD>
  </TR>
  <TR >
    <TD CLASS="strcol" >Date of Start</TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="date" NAME="ClientProcedures_StartDate_1" VALUE="<<ClientProcedures_StartDate_1>>" ONFOCUS="select()" ONCHANGE="return vDate(this,1)" SIZE="10" >
    </TD>
  </TR>
  <TR >
    <TD CLASS="strcol" >Date of End</TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="date" NAME="ClientProcedures_EndDate_1" VALUE="<<ClientProcedures_EndDate_1>>" ONFOCUS="select()" ONCHANGE="return vDate(this,1)" SIZE="10" >
    </TD>
  </TR>
  <TR >
    <TD CLASS="strcol" >Active
    <TD CLASS="strcol" >
      <INPUT TYPE="radio" NAME="ClientProcedures_Active_1" VALUE=1 <<ClientProcedures_Active_1=1>> > yes
      <INPUT TYPE="radio" NAME="ClientProcedures_Active_1" VALUE=0 <<ClientProcedures_Active_1=0>> > no
    </TD>
  </TR>
  <TR >
    <TD CLASS="strcol" >Performer</TD>
    <TD CLASS="strcol" >
      Search: <INPUT TYPE="text" ID="SearchPerformerNPI" NAME="SearchPerformerNPI" VALUE="" ONFOCUS="select()" ONCHANGE="callAjax('Agency','<<ClientProcedures_PerformerNPI_1>>','selPerformerNPI','&name=ClientProcedures_PerformerNPI_1&pattern='+this.value,'popup.pl');" SIZE="60" >
<BR><SPAN ID="selPerformerNPI"></SPAN>
    </TD>
  </TR>
  <TR >
    <TD CLASS="strcol" >Device ID/Num</TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="text" NAME="ClientProcedures_udi_1" VALUE="<<ClientProcedures_udi_1>>" ONFOCUS="select()" SIZE="100" >
    </TD>
  </TR>
  <TR >
    <TD CLASS="strcol" >for testing use: udi</TD>
    <TD CLASS="strcol" >
      <<ClientProcedures_udicopy_1>>
    </TD>
  </TR>
</TABLE>

<TABLE CLASS="main fullsize" >
  <TR >
    <TD CLASS="numcol" >
      <INPUT TYPE="submit" ONCLICK="return validate(this.form);" NAME="UpdateTables=all&misPOP=1" VALUE="Add/Update">
    </TD>
  </TR>
</TABLE>

<INPUT TYPE="hidden" NAME="post_update" VALUE="PostUpd->updDeviceInfo(%form)" >
</LOADHIDDEN>
</FORM>
<SCRIPT LANGUAGE="JavaScript">
document.ClientProcedure.elements[0].focus();
callAjax('Procedure','<<ClientProcedures_ProcedureID_1>>','selProcedure','&name=ClientProcedures_ProcedureID_1','popup.pl');
callAjax('Agency','<<ClientProcedures_PerformerNPI_1>>','selPerformerNPI','&name=ClientProcedures_PerformerNPI_1','popup.pl');
</SCRIPT>

[[myHTML->rightpane(%form+search)]]
