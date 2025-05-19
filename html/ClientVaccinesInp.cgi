[[myHTML->newPage(%form+Client Vaccines)]]

<SCRIPT LANGUAGE="JavaScript" SRC="/src/cgi/js/vEntry.js"> </SCRIPT>
<SCRIPT LANGUAGE="JavaScript" SRC="/src/cgi/js/vClientVaccines.js"> </SCRIPT>
<SCRIPT LANGUAGE="JavaScript" SRC="/src/cgi/js/vDate.js"> </SCRIPT>

<FORM NAME="ClientVaccines" ACTION="/src/cgi/bin/mis.cgi" METHOD="POST" >
<HR WIDTH="90%" >
<TABLE CLASS="main fullsize" >
  <TR >
    <TD CLASS="strcol" >
      <<<Client_FName_1>>> <<<Client_MName_1>>> <<<Client_LName_1>>> (<<<Client_ClientID_1>>>) <<<Client_SSN_1>>>
      <BR>
      Vaccines Page
    </TD>
    <TD CLASS="numcol" >[[gHTML->setLINKS(%form+back)]]</TD>
  </TR>
</TABLE>
<TABLE CLASS="home fullsize" >
  <TR ><TD CLASS="port hdrtxt" COLSPAN="2" >VACCINES</TD></TR>
  <TR >
    <TD CLASS="strcol" >Vaccine</TD>
    <TD CLASS="strcol" >
      <SELECT NAME="ClientVaccines_CVX_1" >
        [[DBA->selxTable(%form+xVaccines+<<ClientVaccines_CVX_1>>+Descr ID)]]
      </SELECT>
    </TD>
  </TR>
  <TR >
    <TD CLASS="strcol" >Route</TD>
    <TD CLASS="strcol" >
      <SELECT NAME="ClientVaccines_RouteCode_1" >
        [[DBA->selxTable(%form+xDrugRouteOfAdmin+<<ClientVaccines_RouteCode_1>>+Descr ID)]]
      </SELECT>
    </TD>
  </TR>
  <TR >
    <TD CLASS="strcol" >Vaccine Rejected</TD>
    <TD CLASS="strcol" >
      <SELECT NAME="ClientVaccines_RejectCode_1" >
        [[DBA->selxTable(%form+xVaccineReject+<<ClientVaccines_RejectCode_1>>+Descr)]]
      </SELECT>
    </TD>
  </TR>
  <TR >
    <TD CLASS="strcol" >Date of Visit</TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="date" NAME="ClientVaccines_VisitDate_1" VALUE="<<ClientVaccines_VisitDate_1>>" ONFOCUS="select()" ONCHANGE="return vDate(this)" SIZE="10" >
    </TD>
  </TR>
  <TR >
    <TD CLASS="strcol" >Shot Number</TD>
    <TD CLASS="strcol" >
      <SELECT NAME="ClientVaccines_ShotNum_1" >
        <OPTION VALUE="1" >1
        <OPTION VALUE="2" >2
        <OPTION VALUE="3" >3
        <OPTION VALUE="4" >4
        <OPTION VALUE="5" >5
        <OPTION VALUE="6" >6
        <OPTION VALUE="7" >7
        <OPTION VALUE="8" >8
      </SELECT>
    </TD>
  <TR >
    <TD CLASS="strcol" >Lot Number</TD>
    <TD CLASS="strcol" >
      <SELECT NAME="ClientVaccines_LotNum_1" >
        <OPTION VALUE="1" >1
        <OPTION VALUE="2" >2
        <OPTION VALUE="3" >3
        <OPTION VALUE="4" >4
        <OPTION VALUE="5" >5
        <OPTION VALUE="6" >6
        <OPTION VALUE="7" >7
        <OPTION VALUE="8" >8
      </SELECT>
    </TD>
  </TR>
</TABLE>
<HR WIDTH="90%" >
<TABLE CLASS="main fullsize" >
  <TR>
    <TD CLASS="numcol" >
      <INPUT TYPE="submit" ONCLICK="return vDELETE('Are you sure you want to delete this record?');" NAME="ClientVaccines_DELETE_1=1&UpdateTables=all&misPOP=1" VALUE="Delete">
      <INPUT TYPE="submit" ONCLICK="return validate(this.form);" NAME="UpdateTables=all&misPOP=1" VALUE="Add/Update">
    </TD>
  </TR>
</TABLE>

<INPUT TYPE="hidden" NAME="post_update" VALUE="PostUpd->renumClientProblems(%form+<<<Client_ClientID_1>>>)" >
</LOADHIDDEN>
</FORM>
<SCRIPT LANGUAGE="JavaScript">
document.ClientVaccines.elements[0].focus();
</SCRIPT>

[[myHTML->rightpane(%form+search)]]
