[[myHTML->new(%form+Insurance Entry)]]

<SCRIPT LANGUAGE="JavaScript" SRC="/cgi/js/vDate.js"> </SCRIPT>
<SCRIPT LANGUAGE="JavaScript" SRC="/cgi/js/pickDate.js"> </SCRIPT>
<SCRIPT LANGUAGE="JavaScript" SRC="/cgi/js/vEntry.js"> </SCRIPT>
<SCRIPT LANGUAGE="JavaScript" SRC="/cgi/js/popupMsg.js"> </SCRIPT>
<SCRIPT LANGUAGE="JavaScript">
function validate(form) 
{ 
  return vEntry("notnull",form.InsID);
}
function setDate(form)
{
  form.ToDate.value = form.FromDate.value;
  form.ToDate.select();
  return true;
}
</SCRIPT>

<FORM NAME="vInsID" ONSUBMIT="return validate(this);" ACTION="/cgi/bin/<<action>>.cgi" METHOD="POST" >
<DIV CLASS="main header" > <<title>> </DIV>
<DIV CLASS="main header" ><INPUT TYPE="button" ONCLICK="window.close()" VALUE="Cancel / Close" ></DIV>
<TABLE CLASS="home" >
    <TR ><TD CLASS="port" ><TABLE CLASS="homeheading" >
  <TR > <TD CLASS="port" ALIGN=left COLSPAN="3" ><B>Please select the Insurance</B> </TR>
  <TR >
    <TD CLASS="strcol" >Name</TD>
    <TD CLASS="strcol" >
      <SELECT NAME="InsID" >
        [[DBA->selInsurance(%form+<<InsID>>)]]
      </SELECT>
    </TD>
    <TD >&nbsp; </TD>
  </TR>
  <TR >
    <TD >From Date</TD>
    <TD CLASS="strcol" >
      <INPUT TYPE="text" NAME="FromDate" VALUE="" ONFOCUS="select()" ONCHANGE="return vDate(this);" SIZE=10>
      <A HREF="javascript:show_calendar('vInsID.FromDate');" onmouseover="window.status='Calendar to select date';return true;" onmouseout="window.status='';return true;">
        <IMG SRC="/images/show_calendar.gif" WIDTH=24 HEIGHT=22 BORDER=0>
      </A>
      To Date
      <INPUT TYPE="text" NAME="ToDate" VALUE="" ONFOCUS="return setDate(this.form);" ONCHANGE="return vDate(this);" SIZE=10>
      <A HREF="javascript:show_calendar('vInsID.ToDate');" onmouseover="window.status='Calendar to select date';return true;" onmouseout="window.status='';return true;">
        <IMG SRC="/images/show_calendar.gif" WIDTH=24 HEIGHT=22 BORDER=0>
      </A>
    </TD>
    <TD CLASS="numcol" >
      <INPUT TYPE="submit" NAME="pushID=<<LINKID>>" VALUE="search">
    </TD>
  </TR>
    </TABLE></TD></TR>
</TABLE>

</LOADHIDDEN>
</FORM>
<SCRIPT LANGUAGE="JavaScript">
document.vInsID.elements[1].focus();
</SCRIPT>
