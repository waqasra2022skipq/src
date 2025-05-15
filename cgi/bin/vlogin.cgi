#!/usr/bin/perl
############################################################################
use CGI;
my $q = CGI->new();
my $LOGINSCREEN = $q->param('ls');
############################################################################
#warn "vlogin.cgi: LOGINSCREEN=${LOGINSCREEN}\n";
print qq|Content-Type: text/html; charset=ISO-8859-1

<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.0//EN">
<HTML>
<HEAD>
<TITLE>MIS-Health Care Version 2.1</TITLE>
<LINK REL="stylesheet" HREF="/src/cgi/css/mis.css" TYPE="text/css" TITLE="Millennium style sheet">
<SCRIPT Language="JavaScript" SRC="/src/cgi/js/Login.js" ></SCRIPT>
<SCRIPT Language="JavaScript" >
function checkLoginCookies() 
{
  var strCookieVal = getCookie('MillenniumIS');
//alert('checkLoginCookies: LOGINSCREEN=${LOGINSCREEN}');
//alert('checkLoginCookies: val=' + strCookieVal);
  if ( strCookieVal != null && strCookieVal != '' )
  { 
    var strCookieVal = getCookie('MillenniumISNP');
//alert('checkLoginCookies: NPval=' + strCookieVal);
    if ( strCookieVal != null && strCookieVal != '' )
    { 
//alert('checkLoginCookies: mgrtree'); 
      window.location.href = "https://$ENV{HTTP_HOST}/cgi/bin/mis.cgi?vlogin=1&mlt=" + strCookieVal + "&LOGINSCREEN=${LOGINSCREEN}";
    }
    else
    {
//alert('checkLoginCookies: mis.cgi 1'); 
      window.location.href = "https://$ENV{HTTP_HOST}/cgi/bin/mis.cgi?LOGINSCREEN=${LOGINSCREEN}";
    }
  }
  else
  {
//alert('checkLoginCookies: mis.cgi 2'); 
    window.location.href = "https://$ENV{HTTP_HOST}/cgi/bin/mis.cgi?LOGINSCREEN=${LOGINSCREEN}";
  }
}
</SCRIPT>
</HEAD>
<BODY ONLOAD="checkLoginCookies()">
</BODY>
</HTML>
|;
exit;
############################################################################
