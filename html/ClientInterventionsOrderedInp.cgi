[[myHTML->newHTML(%form+Client Interventions Ordered+clock mail managertree collapseipad mismenu)]]

<SCRIPT LANGUAGE="JavaScript" SRC="/src/cgi/js/vEntry.js"> </SCRIPT>
<SCRIPT LANGUAGE="JavaScript" SRC="/src/cgi/js/vClientInterventionsOrdered.js"> </SCRIPT>
<SCRIPT LANGUAGE="JavaScript" SRC="/src/cgi/js/vDate.js"> </SCRIPT>
<SCRIPT LANGUAGE="JavaScript" SRC="/src/cgi/js/vNum.js"> </SCRIPT>
<SCRIPT type="text/javascript" src="/src/cgi/js/ajaxrequest.js"></SCRIPT>

<FORM NAME="InterventionsOrdered" ACTION="/src/cgi/bin/mis.cgi" METHOD="POST" >
<TABLE CLASS="main fullsize" >
  <TR >
    <TD CLASS="strcol" >
      <<<Client_FName_1>>> <<<Client_MName_1>>> <<<Client_LName_1>>> (<<<Client_ClientID_1>>>) <<<Client_SSN_1>>>
      <BR>
      Intervention Ordered Page
    </TD>
    <TD CLASS="numcol" >[[gHTML->setLINKS(%form+back)]]</TD>
  </TR>
</TABLE>
<TABLE CLASS="home fullsize" >
  <TR ><TD CLASS="port hdrcol" COLSPAN="2" >Intervention Ordered</TD></TR>
  <TR >
    <TD CLASS="strcol" >
      Order Date
    </TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="text" NAME="ClientInterventionsOrdered_VisitDate_1" VALUE="<<ClientInterventionsOrdered_VisitDate_1>>" ONFOCUS="select()" ONCHANGE="return vDate(this)" MAXLENGTH="10" SIZE="10" >
    </TD>
  </TR>
  <TR >
    <TD CLASS="strcol" >Order</TD>
    <TD CLASS="strcol" COLSPAN="3" >
      <SELECT NAME="ClientInterventionsOrdered_Intervention_1">
        [[DBA->selxTable(%form+xInterventionOrder+<<ClientInterventionsOrdered_Intervention_1>>+ConceptName ConceptCode)]]
      </SELECT>
    </TD>
  </TR>
  <TR >
    <TD CLASS="strcol" >Reason</TD>
    <TD CLASS="strcol" COLSPAN="3" >
      <SELECT NAME="ClientInterventionsOrdered_Reason_1">
        [[DBA->selxTable(%form+xInterventionOrderReason+<<ClientInterventionsOrdered_Reason_1>>+ConceptName ConceptCode)]]
      </SELECT>
    </TD>
  </TR>
  <TR >
    <TD CLASS="strcol" >Rejected Reason</TD>
    <TD CLASS="strcol" COLSPAN="3" >
      <SELECT NAME="ClientInterventionsOrdered_Rejected_1">
        [[DBA->selxTable(%form+xInterventionOrderRejected+<<ClientInterventionsOrdered_Rejected_1>>+ConceptName ConceptCode)]]
      </SELECT>
    </TD>
  </TR>
</TABLE>

<TABLE CLASS="main fullsize" >
  <TR >
    <TD CLASS="numcol" >
[[SysAccess->verify(%form+Privilege=Agent)       <INPUT TYPE="submit" ONCLICK="return vDELETE('Are you sure you want to delete this Ordered record?')" NAME="ClientInterventionsOrdered_DELETE_1=1&UpdateTables=all&misPOP=1" VALUE="Delete" > ]]
      <INPUT TYPE="submit" ONCLICK="return validate(this.form);" NAME="UpdateTables=all&misPOP=1" VALUE="Add/Update">
    </TD>
  </TR>
</TABLE>

</LOADHIDDEN>
</FORM>
<SCRIPT LANGUAGE="JavaScript">
document.InterventionsOrdered.elements[0].focus();
</SCRIPT>

[[myHTML->rightpane(%form+search)]]
