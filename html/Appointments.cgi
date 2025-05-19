[[myHTML->newPage(%form+Provider Appointments)]]

<SCRIPT LANGUAGE="JavaScript" SRC="/src/cgi/js/NoEnter.js"> </SCRIPT>
<SCRIPT LANGUAGE="JavaScript" SRC="/src/cgi/js/vEntry.js"> </SCRIPT>
<SCRIPT LANGUAGE="JavaScript" SRC="/src/cgi/js/vAppointments.js"> </SCRIPT>
<SCRIPT LANGUAGE="JavaScript" SRC="/src/cgi/js/vDate.js"> </SCRIPT>
<SCRIPT LANGUAGE="JavaScript" SRC="/src/cgi/js/vTime.js"> </SCRIPT>

<FORM NAME="Appointments" ACTION="/src/cgi/bin/mis.cgi" METHOD="POST" >
<TABLE CLASS="main fullsize" >
  <TR >
    <TD CLASS="strcol" >
      <<<Provider_FName_1>>> <<<Provider_MName_1>>> <<<Provider_LName_1>>> 
      <BR>Appointment
    </TD>
    <TD CLASS="numcol" >[[gHTML->setLINKS(%form+back)]]</TD>
  </TR>
</TABLE>
<TABLE CLASS="home fullsize" >
  <TR ><TD CLASS="port hdrtxt" COLSPAN="2" ><U>Appointment</U></TD></TR>
  <TR >
    <TD CLASS="strcol" >
      For Provider<BR>
      <SELECT NAME="Appointments_ProvID_1" SIZE="10" >[[gHTML->selProviders(%form++<<Appointments_ProvID_1>>)]]</SELECT> 
    </TD>
    <TD CLASS="strcol" >
      For Client<BR>
      <SELECT NAME="Appointments_ClientID_1" SIZE="10" >[[DBA->selClients(%form+<<Appointments_ClientID_1>>)]]</SELECT> 
    </TD>
  </TR>
  <TR >
    <TD CLASS="strcol" >Contact Date</TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="text" NAME="Appointments_ContactDate_1" VALUE="<<Appointments_ContactDate_1>>" ONFOCUS="select()" ONCHANGE="return vDate(this)" SIZE="15" >
    </TD>
  </TR>
  <TR >
    <TD CLASS="strcol" >Begin Time</TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="text" NAME="Appointments_BeginTime_1" VALUE="<<Appointments_BeginTime_1>>" ONFOCUS="select()" ONCHANGE="return vTime(this,0,this);" SIZE="15" >
    </TD>
  </TR>
  <TR >
    <TD CLASS="strcol" >Notes/Progress</TD>
    <TD CLASS="strcol" >
      <TEXTAREA NAME="Appointments_Notes_1" COLS="60" ROWS="5" WRAP="virtual" onFocus="select()" ><<Appointments_Notes_1>></TEXTAREA>
    </TD>
  </TR>
  <TR >
    <TD CLASS="strcol" COLSPAN="2" >
      This appointment can be converted into a Treatment Note by clicking the button 'Create Note' below. The Provider, Client, Contact Date, Begin Time, and Notes/Progress are filled into the note. If you complete/finish the note it takes the place of this appointment and this appointment is removed.
    </TD>
  </TR>
</TABLE>
<TABLE CLASS="main fullsize" >
  <TR>
    <TD CLASS="numcol" >
      <INPUT TYPE=submit ONCLICK="return vDelete(this.form);" NAME="UpdateTables=all&misPOP=1" VALUE="DELETE Appointment">
      <INPUT TYPE="submit" ONCLICK="return validate(this.form);" NAME="UpdateTables=all&CreateNote=1" VALUE="Create Note">
      <INPUT TYPE="submit" ONCLICK="return validate(this.form);" NAME="UpdateTables=all&misPOP=1" VALUE="Add/Update">
    </TD>
  </TR>
</TABLE>

<INPUT TYPE="hidden" NAME="Appointments_DELETE_1" VALUE=<<Appointments_DELETE_1>> >
<INPUT TYPE="hidden" NAME="post_update" VALUE="PostUpd->updAppt(%form)" >
</LOADHIDDEN>
</FORM>
<SCRIPT LANGUAGE="JavaScript">
document.Appointments.elements[0].focus();
</SCRIPT>

[[myHTML->rightpane(%form+search)]]
