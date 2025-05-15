[[myHTML->newPage(%form+Reminder Entry)]]

<SCRIPT LANGUAGE="JavaScript" SRC="/src/cgi/js/NoEnter.js"> </SCRIPT>
<SCRIPT LANGUAGE="JavaScript" SRC="/src/cgi/js/vEntry.js"> </SCRIPT>
<SCRIPT LANGUAGE="JavaScript" SRC="/src/cgi/js/vReminders.js"> </SCRIPT>
<SCRIPT LANGUAGE="JavaScript" SRC="/src/cgi/js/vDate.js"> </SCRIPT>
<SCRIPT LANGUAGE="JavaScript" SRC="/src/cgi/js/pickDate.js"> </SCRIPT>
<SCRIPT LANGUAGE="JavaScript" SRC="/src/cgi/js/vTime.js"> </SCRIPT>

<FORM NAME="Reminders" ACTION="/cgi/bin/mis.cgi" METHOD="POST" >
<TABLE CLASS="main fullsize" >
  <TR >
    <TD CLASS="strcol" >
      <<<Provider_FName_1>>> <<<Provider_MName_1>>> <<<Provider_LName_1>>> 
      <BR>Provider Reminders
    </TD>
    <TD CLASS="numcol" >[[gHTML->setLINKS(%form+back)]]</TD>
  </TR>
</TABLE>
<TABLE CLASS="home fullsize" >
  <TR > <TD CLASS="port hdrtxt" COLSPAN=3 ><B>Email a reminder message to yourself (make sure you have an email entered for yourself).</B></TD> </TR>
  <TR >
    <TD CLASS="strcol" >Message</TD>
    <TD CLASS="strcol" >
      <TEXTAREA NAME="Reminders_Message_1" COLS="70" ROWS="5" WRAP="virtual" ><<Reminders_Message_1>></TEXTAREA>
    </TD>
  </TR>
  <TR >
    <TD CLASS="strcol" >Date</TD>
    <TD CLASS="strcol" >
      <A HREF="javascript:show_calendar('Reminders.Reminders_RDate_1');" onmouseover="window.status='Calendar to select date';return true;" onmouseout="window.status='';return true;">
        <IMG SRC="/images/show_calendar.gif" WIDTH=24 HEIGHT=22 BORDER=0>
      </A>
      <INPUT TYPE=text NAME="Reminders_RDate_1" VALUE="<<Reminders_RDate_1>>" ONFOCUS="select()" ONCHANGE="return vDate(this)" MAXLENGTH="10" SIZE="10" >
    </TD>
  </TR>
  <TR >
    <TD CLASS="strcol" WIDTH=30% >Frequency</TD>
    <TD CLASS="strcol" >
      <INPUT TYPE=radio NAME="Reminders_Freq_1" VALUE=0 <<Reminders_Freq_1=0>> > Once
      <INPUT TYPE=radio NAME="Reminders_Freq_1" VALUE=1 <<Reminders_Freq_1=1>> > Every Day
      <INPUT TYPE=radio NAME="Reminders_Freq_1" VALUE=2 <<Reminders_Freq_1=2>> > Every Week
      <INPUT TYPE=radio NAME="Reminders_Freq_1" VALUE=3 <<Reminders_Freq_1=3>> > Every Month
    </TD>
  </TR>
  <TR >
    <TD CLASS="strcol" >Time</TD>
    <TD CLASS="strcol" >
      <INPUT TYPE=text NAME="Reminders_RTime_1" VALUE="<<Reminders_RTime_1>>" ONFOCUS="select()" ONCHANGE="return vTime(this,1,this)" MAXLENGTH="10" SIZE="10" >
    </TD>
  </TR>
  <TR>
    <TD CLASS="strcol" WIDTH=30% >Done</TD>
    <TD CLASS="strcol" >
      <INPUT TYPE=radio NAME="Reminders_Done_1" VALUE=1 <<Reminders_Done_1=1>> > yes
      <INPUT TYPE=radio NAME="Reminders_Done_1" VALUE=0 <<Reminders_Done_1=0>> > no
    </TD>
  </TR>
  <TR>
    <TD CLASS="strcol" COLSPAN="2" >Enter a Message to email. Then enter a date,frequency,time. The date, based on the frequency, will execute one or more times. When the message has been sent the Done flag is set to 'yes'. To resend you can change the date,frequency and check the Done flag to 'no'. If frequency is other than Once, then based on the date's day of week or day of month it will repeat sending the message, ignoring the Done flag.</TD>
  </TR>
</TABLE>
<TABLE CLASS="main fullsize" >
  <TR>
    <TD CLASS="numcol" >
      <INPUT TYPE="submit" ONCLICK="return vDELETE('Are you sure you want to delete this reminder?')" NAME="Reminders_DELETE_1=1&UpdateTables=all&misPOP=1" VALUE="Delete" >
      <INPUT TYPE="submit" ONCLICK="return validate(this.form);" NAME="UpdateTables=all&misPOP=1" VALUE="Add/Update">
    </TD>
  </TR>
</TABLE>

</LOADHIDDEN>
</FORM>
<SCRIPT LANGUAGE="JavaScript">
document.Reminders.elements[0].focus();
</SCRIPT>

[[myHTML->rightpane(%form+search)]]
