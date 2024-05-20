Content-Type: text/html; charset=ISO-8859-1

<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.0//EN">
<HTML lang="en" >
<HEAD> <TITLE>Login</TITLE> </HEAD>
<STYLE>
 .{ font-family: Verdana, Arial, Helvetica; }
 BODY  { background: #5a7d9b; color: black; }
 H1    { font-size: 18pt; color: orange; }
 TABLE { background-color: #FBFFE7; padding: 20px; }
 TD    { text-align: center; }
 TH    { text-align: right; }
</STYLE>
<SCRIPT LANGUAGE="JavaScript" SRC="/cgi/js/vEntry.js"> </SCRIPT>
<SCRIPT LANGUAGE="JavaScript" >
function vLogin(form)
{ return vEntry("notnull",form.user,form.pass); }
</SCRIPT>

<BODY >
<CENTER>
<BR>
<H1>Millennium Information Services</H1>
<H1>{MSG}</H1>
<BR>
<TABLE BORDER="3" CELLPADDING="20" >
  <TR>
    <TD >
    <IMG ALT="logo" BORDER=0 SRC="{LOGO}" >
    <H2 >{SITENAME}</H2>
<P>
<FORM NAME="login" METHOD="post" ACTION="/cgi/bin/mis.cgi" >
      <TABLE WIDTH="100%" >
	<TR>
	  <TD ALIGN="center" >
	    <TABLE>
	      <TR>
		<TH ALIGN="right" >Email</TH>
		<TD><INPUT TYPE="text" NAME="user" SIZE="30" ></TD>
	      </TR> 
	      <TR>
		<TH ALIGN="right" >Password</TH>
		<TD><INPUT TYPE="password" NAME="pass" SIZE="30" ></TD>
	      </TR>
	    </TABLE>
	    <BR>
	    <INPUT TYPE="submit" NAME="Login" VALUE="Login" ONCLICK="return vLogin(this.form);" >
	    <INPUT TYPE="hidden" NAME="xx" VALUE="{XX}" >
	  </TD>
	</TR>
	<TR><TD >&nbsp;</TD></TR>
	<TR>
	  <TD ALIGN="center" >
            <A HREF="/cgi/bin/mis.cgi?RenewLogin=yes">Forgot password</A>
	  </TD>
	</TR>
      </TABLE>
</LOADHIDDEN>
</FORM>
    </TD>
  </TR>
</TABLE>
<H1>{MSG}</H1>
<a href="http://www.healthit.gov/providers-professionals/your-mobile-device-and-health-information-privacy-and-security" target="_blank"><img src="http://www.healthit.gov/sites/default/files/onc-banner-728x90.jpg.jpg" border="0" alt="HealthIT.gov Mobile Devices Privacy and Security"></a>
<SCRIPT LANGUAGE="JavaScript" >
document.login.elements[0].focus();
</SCRIPT>
</BODY>
</HTML>
